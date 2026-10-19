# 07. MCP（12h）

> 完成这一段，你能做到：**同一个业务函数，直接调用和经 MCP 协议调用的成功/拒绝/失败结果完全一致**，并且能说清协议层到底加了什么、没加什么。

这一段只有 12 小时。它的价值不在"用了 MCP"，而在**分清协议和授权是两件事**。

---

## 在流程中的位置

[FLOW.md](../FLOW.md) 的 ⑤ 和 ⑩ 之间——把"执行器调本地函数"换成"执行器经协议调远端函数"。

前置：06 段（写工具也要走同一条协议）。解锁：08 段的检索工具包装。

```text
executor → MCP Client → stdio → MCP Server → 业务函数 → Provider
```

---

## 要写的代码

| 文件 | 职责 | 现状 |
|---|---|---|
| `mcp_integration/server_crypto/server.py` | 服务入口 | ✅ 已有 |
| `mcp_integration/server_crypto/*/tools.py` | 工具注册 | ✅ 已有（06 段后补齐写工具） |
| `mcp_integration/client/connection.py` | stdio 生命周期 | ✅ 已有 |
| `mcp_integration/client/bridge.py` | 工具发现与 schema 转换 | ✅ 已有（需加名字映射） |
| `mcp_integration/common/mapping.py` | **外部名 → canonical ID** | ❌ 空桩 |

> 这一段也是**大半已有**的。你的任务是加映射层、补对照证据、踩一遍 stdio 的坑。

---

## 核心概念

### 1. MCP 增加了什么，没增加什么

| 增加 | 没增加 |
|---|---|
| 一个进程边界 | 任何授权能力 |
| 一套发现/调用协议 | 任何结果可信度 |
| 工具描述的标准形状 | 任何对"模型说了算"的修正 |
| 跨语言/跨机器的可能性 | 任何副作用保护 |

**发现成功 ≠ 允许执行。** 工具出现在 `tools/list` 里只说明它注册了，不说明当前用户能用它。

### 2. stdout 是协议通道，日志必须走 stderr

```python
print("debug: 收到请求")   # ← 这一行会破坏 stdio JSON-RPC
```

stdio 传输的 stdout 是**唯一的协议通道**。任何 `print`、任何库的默认日志输出到 stdout，都会让客户端解析失败。

本项目已有的做法（`packages/core/logging.py`）：

```python
configure_logging(level="INFO")     # 默认 StreamHandler(sys.stderr)
```

**排查这类问题时**：把 stdout 和 stderr 分到两个文件，看 stdout 里有没有非 JSON 的行。

### 3. 项目包名不能叫 `mcp`

第三方 SDK 也叫 `mcp`。如果项目里建一个顶级 `mcp/` 目录，`import mcp` 拿到的是你的目录，SDK 就"消失"了。

本项目的选择：项目模块叫 **`mcp_integration`**，SDK 仍然是 `mcp`。

```bash
python -c 'import mcp; print(mcp.__file__)'    # 必须指向 site-packages
```

### 4. Tools / Resources / Prompts 是三件不同的事

| 能力 | 做什么 | 本项目用途 |
|---|---|---|
| **Tools** | 执行一个动作 | 全部密码操作 |
| **Resources** | 提供受控内容 | 可选（教学说明） |
| **Prompts** | 提供提示模板 | 可选（操作计划） |

后两者**仍然是不可信输入**。Resource 里的内容不能自授权，Prompt 里的指令不能改 policy。

### 5. 外部名和内部 ID 必须映射

```text
外部（server 提供）      domain.inspect_certificate
内部（本地 canonical）   inspect_certificate
```

映射表要存：外部 server 名、外部 tool 名、canonical ID、SDK/协议版本、本地 policy 版本。

**为什么必须显式映射**：外部名字会变，本地 policy 按 canonical ID 定义。直接拿外部名当本地 ID，等于让远端决定你的授权规则。

### 6. Server 侧必须复查授权

客户端已经校验过参数了，Server 为什么还要查？

**因为客户端不是信任边界。** 任何人都能直接连 Server 跳过 Agent。

必须构造这个反例：绕过 Agent、拿着有效连接直接 `tools/call` 一个越权资源 → 必须被拒，并证明 Provider 没执行。

### 7. 直调与 MCP 对照什么

**不比**：模型措辞、随机性、时间戳。

**要比**：

| 维度 | 对照什么 |
|---|---|
| 成功 | 相同输入 → 相同结构结果（摘要值完全一致） |
| 拒绝 | 相同越权输入 → 都被拒，且都是执行前拒绝 |
| 失败 | 相同坏输入 → 相同 `error_type` |
| 关联 | 同一次调用能串起 提议 → MCP 请求 → handler → Provider → 回传 |

---

## 分步实现

### 步骤 1 先存一份直调结果

在做 MCP 之前，把直调的成功/拒绝/失败三种结果各存一份。**没有基线就没法对照。**

### 步骤 2 加名字映射

```python
# mcp_integration/common/mapping.py
CANONICAL = {
    "inspect_certificate": "inspect_certificate",
    "domain.inspect_certificate": "inspect_certificate",
    "sha256_file": "digest_file",
}

def to_canonical(external_name: str) -> str:
    if external_name not in CANONICAL:
        raise ToolNotFoundError("unmapped external tool", name=external_name)
    return CANONICAL[external_name]
```

未映射的名字**直接拒绝**，不要 fallback 到原名。

### 步骤 3 验证 stdio 通道干净

```bash
python -m mcp_integration.server_crypto.server 2>/tmp/stderr.log | tee /tmp/stdout.log
# 手工发一行 JSON-RPC，看 stdout 是否只有 JSON
```

或者更简单：客户端能正常 `list_tools` 就说明没被污染；一旦有 `print`，通常立刻出现解析错误。

### 步骤 4 绕过 Agent 直接调，验证 Server 授权

```python
async with connect_tools() as (session, tools):
    r = await session.call_tool("sha256_file", arguments={"file_id": "../../etc/passwd"})
    print(r.structured_content)     # 必须是拒绝
```

这一步证明的是：**Server 自己也在查**，不是只靠客户端。

### 步骤 5 三种结果逐一对照

| 场景 | 直调 | MCP | 必须一致的部分 |
|---|---|---|---|
| `file_002` 摘要 | `88036eec...` | 同 | digest 逐字符 |
| `../../etc/passwd` | 拒绝 | 拒绝 | 都发生在 Provider 之前 |
| 不存在的 file_id | 拒绝 | 拒绝 | `error_type` |

### 步骤 6 关联一次完整链路

保存一条能串起五层的记录：

```text
模型提议（tool name + arguments）
  → MCP 请求（JSON-RPC payload）
  → Server handler 收到的参数
  → Provider 实际执行的命令数组
  → 返回给模型的结果
```

每一层都要能对上**同一次调用**。这是排错能力的分水岭。

---

## 常见坑

1. **在 server 里 `print`。** 一行就能让协议解析失败。
2. **项目建了 `mcp/` 目录。** SDK 被遮蔽，报错信息极具误导性。
3. **把 `read_only_hint` 当授权依据。** 那是远端自称的，不能当本地 policy 输入。
4. **工具描述里写"检查"，就以为没副作用。** 名字不证明行为。
5. **只测客户端校验，不测 Server 复查。** 绕过客户端就能打穿。
6. **拿外部工具名直接当 canonical ID。** 远端一改名，本地授权规则就错位。
7. **断连就认为操作没发生。** 06 段之后有写操作，断连只说明你不知道结果。
8. **一次启动三个 Server。** 这一段只需要一个 Crypto Server。

---

## 自检问题

1. MCP 在已有 Demo 上具体增加了什么？哪些 Agent 职责**仍然**由你自己实现？
2. 模型的 `tool_call` 和 MCP 的 `tools/call` 是同一层吗？内部 call_id 在哪一层生成？
3. Server 已经收到合法参数了，为什么还要查一次授权？构造一个绕过客户端的反例。
4. 为什么 `print` 一行就能破坏 stdio？你怎么定位这种问题？
5. 直调与 MCP 的结果，哪些允许不同、哪些必须相同？

---

## 本人记录

```text
日期：
实际工时：
直调 vs MCP 三次对照的实际输出：
绕过 Agent 的越权尝试结果：
stdio 污染问题的定位过程（如果踩到）：
还没理解的：
```
