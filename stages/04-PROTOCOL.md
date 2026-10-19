# 04. 协议与预算（35h）

> 完成这一段，你能做到：**模型请求失败时能说出是哪一类失败；Loop 撞限时给出结构化原因而不是崩掉；工具输出不会撑爆上下文；一行行流式数据能还原成完整调用。**

02 段的 Loop 是"happy path"。这一段让它能应付真实世界：网络会断、模型会重复提议、上下文会满、响应会分块到达。

---

## 在流程中的位置

[FLOW.md](../FLOW.md) 的 **②③⑦**，以及 ⑤ 上的预算与超时。

前置：03 段（预算挂在同一个执行入口上）。解锁：05 段的 Run/Step 记录（Trace 就是它的数据来源）。

```text
② ContextBuilder  组消息、截断、过滤  ← 本段新建
③ 请求模型        httpx + 四类错误    ← 本段重写
⑦ Trace           每次 step 落一条     ← 本段新建
⑤ 预算/超时/重复  挂在 executor 上     ← 本段加强
   流式解析        NDJSON 三层          ← 本段新建
```

---

## 要写的代码

| 文件 | 职责 | 现状 |
|---|---|---|
| `packages/llm/client.py` | httpx 非流式 + 四类错误分类 | ⚠️ 用 urllib，无分类 |
| `packages/llm/context.py` | ContextBuilder：组装、截断、预算 | ❌ 新建 |
| `packages/llm/streaming.py` | NDJSON 解析 | ❌ 空桩（1 行 docstring） |
| `tools/executor.py` | 预算、超时、重复检测 | ⚠️ 需加强 |
| `packages/core/trace.py` | TraceWriter | ❌ 新建 |
| `packages/core/logging.py` | `scrub` / `JsonFormatter` | ✅ 已有，**但零调用** |

### 当前的真实状态

| 项 | 现状 |
|---|---|
| 模型请求库 | `urllib.request`（不是 httpx） |
| 错误分类 | 无，任何故障都是裸异常冒泡 |
| 原始报文留存 | 无 |
| 上下文预算 | `messages` 只增不减，`LLM_NUM_CTX=8192` 配置了但**没人读** |
| 步骤预算 | 只有 `max_steps`，硬编码默认 5 |
| 总 deadline | 无 |
| token / 输出预算 | 无 |
| 重复提议检测 | 无 |
| 停止原因 | 超限抛 `RuntimeError`，不是结构化结果 |
| Trace | 无（`logging.py` 写好了但全链路零 `get_logger()`） |
| NDJSON | 空桩 |

---

## 核心概念

### 1. 四类失败必须分开

| 类型 | 典型现象 | 你怎么处理 |
|---|---|---|
| **连接失败** | `httpx.ConnectError` | 服务没起、地址错。改配置或起服务 |
| **HTTP 错误** | `4xx` / `5xx` | 模型名错(404)、鉴权、服务端崩。看状态码和 body |
| **响应解析失败** | JSON 解不开、缺 `message` 字段 | 协议版本或端点不匹配 |
| **模型没选工具** | 200，但 `tool_calls` 为空 | **这不是错误**，是正常分支 |

前三种要变成有类型的异常或 `ToolResult.fail`，第四种要变成正常结束。

**为什么不能混**：混在一起时，你唯一能做的就是"重试"。而重试对 404 完全无效，对解析失败会掩盖协议不兼容。

### 2. 四种预算保护的是不同东西

| 预算 | 单位 | 保护什么 | 触发后 |
|---|---|---|---|
| `max_steps` | 轮次 | 反复提议不收敛 | 停止并说明 |
| `deadline` | 秒 | 整体超时（用户等不了） | 停止并说明 |
| `token` | 计量 | 上下文窗口和成本 | 截断历史或停止 |
| `output` | 字节/字符 | 单次工具结果撑爆上下文 | 截断或转 result_ref |

**它们不能互相替代**：`max_steps=5` 挡不住"每步都很慢"；`deadline=120s` 挡不住"每步都很快但无限循环"。

当前配置里已有的事实：`LLM_TIMEOUT_S=120`（单次请求），`LLM_NUM_CTX=8192`（窗口）。**这两个是"单次"的量，不是 Loop 的总预算**，别混。

### 3. Context 有四种来源，各自权威性不同

| 来源 | 保存什么 | 权威性 / 限制 |
|---|---|---|
| **History** | 用户/模型/工具的会话消息 | 是对话历史，**模型旧回答不是资源现状** |
| **Run State** | 当前节点、预算、pending action、结果引用 | 恢复控制流；**真实副作用以账本/Provider 核对** |
| **Memory** | 用户偏好与可追溯事实候选 | **不存秘密**，不把文档里的命令当用户偏好 |
| **Knowledge** | 经授权的操作资料与 chunk | 支持知识结论，**不证明当前证书可信或密钥有效** |

组装 Context 时，system prompt 里**不能**放：文件全文、检索原文、模型自己上一轮的回答当作事实、任何秘密。

预算要算上：system + 用户问题 + 工具 schema + 历史 + Memory + 检索证据 + 工具结果 + **预留输出**。

> 工具 schema 本身就占不少 token。6 个工具的 schema 可能上千 token，这是"一次只暴露 1–2 个工具"的实际理由，不只是认知负担。

### 4. NDJSON 是三层，不要混

```text
网络层    TCP/HTTP 分块 → 一次 read 可能拿到半行，也可能拿到 3 行半
   ↓  按 \n 切
记录层    一行 = 一个完整 JSON 对象（一行可能被切成两次 read）
   ↓  json.loads
业务层    累积 message.content、累积 tool_calls 的 fragments
```

三个必踩的坑：

- **半行**：`{"model":"qwen` + `3.5:4b"}` 是两次 read
- **UTF-8 跨块**：一个中文字符的 3 个字节可能被切开
- **一行多个对象**：不该出现，但缓冲区必须能处理

**应用层的 SSE 和模型原生的 NDJSON 是两套协议**，解析器要分开写（SSE 在 08 段）。

### 5. Trace 是后面所有验收的证据来源

每条 Trace 至少要有：`run_id`、`step_index`、`tool_name`、`call_id`、`duration_ms`、`outcome`（ok / denied / failed / timeout）、拒绝原因。

脱敏用现成的 `packages/core/logging.py::scrub`，它已经能处理 `password=...`、`token=...`、DSN 里的口令。

---

## 分步实现

### 步骤 1 换成 httpx 并分四类

```python
import httpx

try:
    r = httpx.post(f"{base}/api/chat", json=body, timeout=settings.LLM_TIMEOUT_S)
    r.raise_for_status()
except httpx.ConnectError as e:
    raise LLMConnectionError(...) from e
except httpx.TimeoutException as e:
    raise LLMTimeoutError(...) from e
except httpx.HTTPStatusError as e:
    raise LLMHTTPError(e.response.status_code, ...) from e

try:
    payload = r.json()
except json.JSONDecodeError as e:
    raise LLMParseError(...) from e

msg = payload.get("message")
if msg is None:
    raise LLMParseError("missing message field")
```

**保留原始报文**：在成功和失败两条路上都把请求体（脱敏后）和响应原文写到 Trace，否则 Q7 类问题永远定位不了。

验证四种失败都能分别复现：

```bash
# 连接失败
python -m packages.app run --question '...' --base-url http://127.0.0.1:9  # 或改 Settings
# 404
# 直接改 CONTROLLER_MODEL 为一个不存在的名字
# 解析失败
# 临时把端点指到一个返回 HTML 的地址
```

### 步骤 2 写 ContextBuilder

最小可用形态：

```python
class ContextBuilder:
    def __init__(self, max_tokens: int, reserve_output: int = 1024): ...

    def build(self, system: str, history: list[dict], user: str,
              tools: list[dict], evidence: list[str] = ()) -> list[dict]:
        """返回送模型的消息序列；超预算时按策略截断 history。"""
```

要点：

- **固定不动的部分**：system、当前用户问题、工具 schema —— 永不截断
- **可截断的部分**：history，从最旧的开始丢
- **截断要成对**：assistant 的 `tool_calls` 和对应的 `role:tool` 结果必须一起丢。只丢一半会让模型看到"孤儿 tool 消息"，很多后端会直接报错
- **摘要不能删除**：资源版本、单位、否定条件、待审批动作

### 步骤 3 加预算与重复检测

```python
class LoopBudget:
    def __init__(self, max_steps: int, deadline_s: float): ...

    def check_step(self) -> None:   # 超限抛 BudgetExceededError
    def check_deadline(self) -> None:
```

重复提议检测：把 `(tool_name, canonical_json(arguments))` 做哈希放进 set。

**关键区分**：

| 情况 | 处理 |
|---|---|
| 只读工具，同一参数重试 | 可以允许有限次（读操作幂等） |
| 写工具，同一参数重复 | **一律拒绝**，交给账本 |

注意：03 段之后写工具还没开放，所以本段只需实现"只读的有限重试 + 其余拒绝"。

**停止原因要结构化**，不要 `raise RuntimeError`：

```python
return {"status": "stopped", "reason": "max_steps", "steps": 5, "elapsed_s": 12.3}
```

### 步骤 4 接上 Trace

在 Loop 的每个分支落一条：

```text
run_start → step(模型请求, 耗时, tokens) → tool_call(名字, 参数hash) 
→ tool_result(outcome, duration) → final(status, reason)
```

`configure_logging()` 现在从没被调用过——在这一步接上，并确认日志里**没有**文件全文、密钥、口令。

### 步骤 5 实现 NDJSON

```python
def iter_ndjson(resp) -> Iterator[dict]:
    buf = ""
    for chunk in resp.iter_bytes():
        buf += chunk.decode("utf-8", errors="replace")   # 注意 errors 策略
        while "\n" in buf:
            line, buf = buf.split("\n", 1)
            line = line.strip()
            if line:
                yield json.loads(line)
```

更好的做法是用 `codecs.getincrementaldecoder("utf-8")` 保持跨块状态，避免替换字符破坏数据。

累积 `tool_calls` 时注意：流式返回的 `function.arguments` 是**分片字符串**，要拼接后再 `json.loads`，不能每片都解析。

### 步骤 6 完成切块测试

构造确定性输入，验证解析器：

```python
# 把完整 NDJSON 按不同边界切块，结果必须一致
cases = [全部一次给, 每个字节一次, 在 JSON 中间切, 在中文中间切, 在 \n 处切]
for c in cases:
    assert accumulate(iter_ndjson(fake(c))) == expected
```

**这类测试必须用固定输入**（自己构造的字节串），不能依赖真实模型的随机输出。

---

## 常见坑

1. **`await asyncio.wait_for(...)` 超时 ≠ 子进程已死。** 它只取消协程，`subprocess` 可能还在跑。必须显式 `terminate()` + `wait()` + 兜底 `kill()`。
2. **用 `errors="replace"` 掩盖编码问题。** 出��替换字符就说明切块逻辑错了，应该修而不是吞。
3. **每片 `arguments` 都 `json.loads`。** 流式分片只在最后一片才是完整 JSON。
4. **截断 history 时把 tool 消息和它的 assistant 提议拆散。** 后端会报 400。
5. **只设 `max_steps` 就以为有预算。** 慢请求、大输出都挡不住。
6. **把 `LLM_NUM_CTX` 当 Loop 总预算。** 它是单次请求的窗口。
7. **重试包括写操作。** `read_only=False` 的工具 `retry` 必须为 0（契约里已有守卫）。
8. **Trace 里记了工具参数原文。** 参数里可能有路径、key_id，甚至（早期实现里）口令。用 `scrub`。

---

## 自检问题

1. 连接失败、404、坏 JSON、模型不选工具——四种情况你怎么分别复现和区分？各记了什么 Trace？
2. `max_steps`、`deadline`、`token`、`output` 各自挡住什么场景？举一个只有其中一种能挡住的例子。
3. 为什么 NDJSON 要分成三层？举一个"只做两层就会错"的具体切块位置。
4. History 截断时，`assistant` 的 `tool_calls` 和 `role:tool` 为什么必须一起丢？
5. 描述一次你构造的重复提议，以及系统实际拦在哪一行。

---

## 本人记录

```text
日期：
实际工时：
四类失败的实际报错文本（各贴一行）：
撞预算时的结构化输出：
NDJSON 切块测试用例与结果：
Trace 样例（脱敏后）：
还没理解的：
```
