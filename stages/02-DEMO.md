# 02. 最小 Demo（20h）

> 完成这一段，你能做到：**输入一句话，模型自己选择工具、程序执行、真实结果回到模型、最终答案是算出来的而不是编出来的**——并且你能用独立命令证明那个摘要是真的。

这是整条链路的第一次闭环。做完它，"Agent"对你就不再是抽象概念。

---

## 在流程中的位置

[FLOW.md](../FLOW.md) 主链路的 **①③④⑤⑥⑩**。这一段**不含**授权（03 段）、预算与 Trace（04 段）。

前置：01 段。解锁：03 段要加闸门的那个执行入口。

```text
用户问题 → 模型 tool_calls → execute_tool 校验 → 固定 Provider
                                    ↓
            最终回答 ← 模型读实际结果 ← 结构化结果回传
```

---

## 要写的代码

| 文件 | 职责 | 现状 |
|---|---|---|
| `packages/app/cli.py` | 薄入口，只调 `agent.run` 一次 | ✅ 已有 |
| `packages/app/agent.py` | **手写 Loop**（本段核心） | ✅ 已有 |
| `packages/llm/client.py` | 非流式 `/api/chat` | ✅ 已有（urllib） |
| `tools/registry.py` | 参数 schema 校验 | ✅ 已有 |
| `tools/executor.py` | 唯一执行入口 | ✅ 已有（待 03 加强） |
| `packages/crypto/providers/openssl_cli.py` | SHA-256，固定参数数组 | ✅ 已有 |
| `mcp_integration/client/connection.py` | stdio 连接生命周期 | ✅ 已有 |
| `mcp_integration/server_crypto/openssl_tools/tools.py` | `sha256_file` 工具 | ✅ 已有 |

> **这一段是大半已有的。** 你的任务不是从零写，而是**跑通 + 独立验证 + 能逐层讲清**。`agent.py` 的 Loop 属于必须自己理解并改得动的部分。

---

## 核心概念

### 1. 模型产生的是"提议"，不是"执行"

模型返回的 `tool_calls` 长这样：

```json
{"function": {"name": "sha256_file", "arguments": {"file_id": "file_002"}}}
```

这是**一段 JSON 文本**。它没有任何执行能力。真正干活的是 `executor` 拿到它之后，映射到服务端的 `sha256_file()` 函数，再由 `openssl_cli` 起子进程。

**所以模型说的"我已经算好了"和"算好了"无关。** 判断依据只能是 ToolResult。

### 2. 资源 ID ≠ 路径

模型只能传 `file_id`（如 `file_002`），不能传 `/etc/passwd`。服务端在 `sha256_file()` 内部把 `file_id` 映射成 `data/<file_id>/` 下的真实文件。

当前实现（`openssl_tools/tools.py`）的约束：

- `file_id` 必须匹配 `[A-Za-z0-9_-]{1,128}`
- 目录不能是软链，且必须存在
- 排除输出文件（`signature.der` / `ciphertext.der` / `decrypted.bin`）后**恰好一个**普通文件
- 文件大小 ≤ `CRYPTO_MAX_FILE_BYTES`

任何一条不满足 → `{"ok": false, "error": "invalid_file"}`，**Provider 根本没被调用**。

### 3. 固定参数数组，不拼 shell

```python
subprocess.run(
    [str(OPENSSL_BIN), "dgst", "-sha256", "-binary", str(input_file)],
    stdin=subprocess.DEVNULL, capture_output=True, timeout=TIMEOUT_S, check=False,
)
```

数组形式天然免疫注入。**任何"把模型字符串拼成命令"的写法都是错的**，哪怕只是 `f"openssl dgst -sha256 {path}"`。

用 `-binary` 而不是默认输出，是为了拿到 32 字节原始摘要，好做长度校验（`len(completed.stdout) != 32` 即失败），避免解析文本输出。

### 4. Loop 只有四个分支

```text
① 追加 user 消息
② 请求模型 → 追加 assistant 消息
③ 没有 tool_calls？→ 返回 content，结束
④ 有 → 逐个执行 → 追加 role:tool 消息 → 回到 ②
```

就这么简单。复杂的是每一步的**失败处理**，那是 03/04 段的事。

### 5. 为什么先摘要，不先证书

| | 摘要 | 证书解析 |
|---|---|---|
| 输入 | 文件字节 | DER/PEM 结构 |
| 输出 | 32 字节，可穷举对照 | 多层嵌套字段 |
| 失败模式 | 少、明确 | 多、格式相关 |
| 能不能独立验证 | 一行 `openssl dgst` 就够 | 需要逐字段核对 |

先用摘要把"模型提议 → 程序执行 → 结果回传"这条**协议链路**验证干净，再加证书只增加"解析"这一个变量。反过来做，出了错你分不清是链路问题还是解析问题。

---

## 分步实现

### 步骤 1 先不接模型，直接调 Provider

```bash
cd /home/zsw/work/agent_development/Agent-development-code
source .venv/bin/activate
python -c '
from pathlib import Path
from packages.crypto.providers.openssl_cli import sha256_digest_file
print(sha256_digest_file(Path("data/file_002/data.md")))
'
```

**预期**：`{'ok': True, 'algorithm': 'SHA-256', 'digest_hex': '...'}`

**失败时先查**：`OPENSSL_BIN` 指向的文件存在吗？`data/file_002/` 里有几个文件？

### 步骤 2 独立对照（这一步不能省）

```bash
openssl dgst -sha256 data/file_002/data.md
```

两个值必须**逐字符相同**。

**为什么必须做**：如果 Provider 自己写错了（比如用了 `-md5` 却标 SHA-256），测试也可能一起错——因为测试调用的就是同一个函数。唯一可靠的对照是**另一条完全独立的路径**。

### 步骤 3 从 MCP 层调一次

```bash
python -c '
import asyncio
from mcp_integration.client.connection import connect_tools

async def main():
    async with connect_tools() as (session, tools):
        print("工具数:", len(tools))
        for t in tools: print(" -", t["function"]["name"])
        r = await session.call_tool("sha256_file", arguments={"file_id": "file_002"})
        print(r.structured_content)
asyncio.run(main())
'
```

**预期**：列出全部工具名，并返回与步骤 2 相同的摘要。

这一步验证的是 **MCP 链路**独立可用，还没牵扯模型。

### 步骤 4 让模型提议一次

```bash
python -m packages.app run --question '计算教学文件 file_002 里那个文件的 SHA-256 摘要'
```

**实测输出**（2026-10-19，本机）：

```text
[工具]sha256_file({'file_id': 'file_002'}) -> {'ok': True, 'algorithm': 'SHA-256',
        'digest_hex': '88036eecf53de118265ae2c33ec3881e8d98cf3a29507fea6c9802ae4e1f7f4f',
        'file_id': 'file_002'}
{"status": "completed", "run_id": "4cfdada262a549edbd3485fc47b1ed32",
 "answer": "文件 file_002 的 SHA-256 摘要计算完成：\n\n**SHA-256 摘要：**
  `88036eecf53de118265ae2c33ec3881e8d98cf3a29507fea6c9802ae4e1f7f4f`",
 "evidence": [{"run_id": "4cfdada262a549edbd3485fc47b1ed32",
   "call_id": "call_00_0", "provider_call_id": "call_57g264hc",
   "tool_name": "sha256_file", "step_index": 0, "ok": true, "error": null,
   "result": {"ok": true, "algorithm": "SHA-256",
              "digest_hex": "88036eecf53de118265ae2c33ec3881e8d98cf3a29507fea6c9802ae4e1f7f4f",
              "file_id": "file_002"},
   "duration_ms": 5.726, "started_at": "2026-10-19T07:59:06.959973+00:00"}]}
```

**必须核对四件事**，缺一不可：

1. 模型提议的工具名是 `sha256_file`（不是它自己编的名字）
2. 提议的参数是 `{"file_id": "file_002"}`（不是路径，不是编造的 ID）
3. 最终答案里的摘要 **等于步骤 2 的独立结果**
4. `evidence` 里有一条 `ok: true` 记录，其 `result.digest_hex` **逐字符等于**答案里的摘要

第 3 条是关键。模型完全可能在没调工具的情况下编一个 64 位十六进制串出来——**长得一模一样**。只有和独立结果对照才分得清。第 4 条把这件事变成结构判定：答案里每个 64 位十六进制串都必须能追到本 run 的工具结果，不用再靠人读文本。

两个号不要混淆：`call_id`（如 `call_00_0`）是应用自己的账本号，用于 evidence 与审计；`provider_call_id`（如 `call_57g264hc`）是模型侧在 `tool_calls[i].id` 给出的回执号，只用于协议绑定，tool 消息的 `tool_call_id` 优先回填它。provider 没给时回落到 `call_id`。

### 步骤 5 制造一次失败

```bash
python -m packages.app run --question '计算教学文件 file_999 的 SHA-256 摘要'
```

**预期**：工具返回 `invalid_file`，模型据此说明文件不存在，**不编造摘要**。

再试一次非法 ID：

```bash
python -m packages.app run --question '计算 ../../etc/passwd 的摘要'
```

**预期**：被 ID 格式校验拒绝。

### 步骤 6 改一个约束并回归

选一个改动，验证正常和失败两条路都没坏。建议选**文件大小上限**：

```python
# mcp_integration/server_crypto/openssl_tools/tools.py
# 把 openssl_cli.MAX_MESSAGE_BYTES 换成一个更小的值（例如 1000）
```

然后：

```bash
python -m packages.app run --question '计算教学文件 file_002 的 SHA-256 摘要'
# 预期：file_002 的 data.md 是 43831 字节 > 1000 → invalid_file，不返回摘要
```

改回去再跑一次确认恢复。

---

## 常见坑

1. **（2026-10-19 已修）`run()` 硬编码了 model 和 base_url。** 此前 `packages/app/agent.py` 里写死了 `"qwen3.5:4b"` 和 `"http://127.0.0.1:11434"`，改 `.env` 不生效。现在 `run()` 读 `Settings.CONTROLLER_MODEL` / `Settings.OLLAMA_BASE_URL`，`main()` 的 `--model` / `--base-url` 默认值也来自同一份配置（命令行参数仍可临时覆盖）。验证：`OLLAMA_BASE_URL=http://127.0.0.1:1 python -m packages.app run ...` 会连不上，说明地址确实来自配置而不是常量。
2. **（2026-10-19 已修）系统提示词用空字符串垫缺失参数。** 此前 `SYSTEM_PROMPT` 要求模型对缺失的必填参数填 `""`，再由 `registry.py` 的黑名单拦截，是**用提示词补 schema 的窟窿**，且黑名单里塞了 `"待补充"/"未提供"/"未知"` 等中文词，天然可绕过。现在提示词改为"缺参就直接询问用户"，`registry.py` 只判定缺键/空白字符串，占位词作为普通值交给业务层（`keystore.find_sm2_key` 返回 `unknown_key`）。验证：问"对教学文件 file_002 做 SM2 签名"时，模型只传 `file_id`，executor 返回 `missing_arguments`（未调用 MCP），模型据 `missing` 追问 key_id。
3. **（2026-10-19 已修）工具结果没有内部 `call_id`。** `ToolCall.call_id` 契约写了"由应用生成"，但此前没用上。现在每次调用生成 `call_{step}_{index}`，写进 `ToolResult.metadata`、`evidence[].call_id` 与 `run_id`；tool 消息的 `tool_call_id` 优先回填 provider 给的 id（示例 `call_57g264hc`），没有才回落内部号。多轮同名工具可以区分了。
4. **`await asyncio.to_thread(call_model, ...)` 只是把阻塞调用挪走。** 它不会取消，也不会设超时上限。真正的超时在 04 段。
5. **模型可能不调工具直接回答。** 尤其问题措辞模糊时。这不是 bug，但如果在"必须给事实"的场景出现，要靠 04 段的策略处理。
6. **用 `data/file_001` 测会失败。** 那个目录里有 `ciphertext.der` 和 `decrypted.bin`，虽然被列入排除名单，但 `data.md` 之外的残留文件容易让人误判。用 `file_002`（只有一个 `data.md`）更干净。

---

## 自检问题

1. 画出这次调用从用户问题到最终回答的完整链路，标出**真正发生密码运算**的那一步。
2. 模型没调工具却编了一个摘要，你怎么发现？说明你的验证路径。
3. `file_id` 为什么不能是路径？如果模型坚持传 `../../etc/passwd`，哪一行代码拦住它？
4. Loop 在什么条件下结束？如果没有 `max_steps` 会怎样？
5. 你改了哪个约束？正常和失败两条路分别变成什么？

---

## 本人记录

```text
日期：
实际工时：
跑通的命令与输出（贴关键行）：
独立对照结果：
改动的约束 & 前后差异：
卡住的：
还没理解的：
```
