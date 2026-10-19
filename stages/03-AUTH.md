# 03. 授权层（10h）

> 完成这一段，你能做到：**模型给的东西一律先当作不可信输入，在执行任何动作之前就把不该跑的打回去，并留下拒绝记录。**

02 段的链路是"模型说调就调"。这一段加上唯一一道闸门。**它只有 10 小时，但它是整个项目的安全边界。**

---

## 在流程中的位置

[FLOW.md](../FLOW.md) 的 **⑤**：`tool_calls` 进入 `execute_tool` 之后的全部判定。

前置：02 段。解锁：04 段的预算与 Trace（它们挂在同一个入口上），以及 06 段的审批闸门（同为这一层的延伸）。

```text
tool_calls（不可信）
      ↓
  ① schema 校验      参数形状对不对
  ② 工具登记校验     这个名字存在吗
  ③ 资源授权         这个 file_id 属于当前用户/项目吗
  ④ 风险策略         这个风险等级允许自动执行吗
      ↓
  Provider 执行
```

---

## 要写的代码

| 文件 | 职责 | 现状 |
|---|---|---|
| `packages/core/models.py` | `ToolResult` / `ToolSpec` / `RiskLevel` / `DEFAULT_POLICY` | ✅ 已定义，**但零调用方** |
| `packages/core/errors.py` | 7 个异常类型 | ✅ 已定义，**但零调用方** |
| `tools/executor.py` | 唯一执行入口 | ⚠️ 返回裸 dict，需改成 `ToolResult` |
| `tools/registry.py` | schema 校验 | ⚠️ 只做 schema，无授权 |
| `packages/security/resources.py` | **资源解析与越界拒绝** | ❌ 空桩 |
| `packages/security/policy.py` | **风险策略判定** | ❌ 空桩 |
| `mcp_integration/server_crypto/gmssl_tools/sm_tools.py` | 4 个写工具的注册 | ⚠️ **需摘掉注册** |

### 一个必须知道的事实

契约层（`ToolResult`/`ToolSpec`/`errors.py`）**已经写好了，但没有任何生产代码 import 它们**。grep 确认只有 `packages/core/__init__.py` 做了 re-export。

后果是文档里那两条契约**当前都不成立**：

- "异常由 `execute_tool` 转为 ToolResult" → 现在是裸 `dict`，从不转换
- "`DEFAULT_POLICY` 生效" → 没有任何代码读它

**这一段的第一个任务就是把这个断掉的接线接上。**

---

## 核心概念

### 1. 四道检查，顺序不能变

```text
schema → 登记 → 资源 → 策略 → 执行
```

**为什么顺序重要**：便宜的先做。schema 校验是纯内存操作，资源解析要碰文件系统，策略判定可能要查库。把便宜的放前面，非法请求在最早的位置就被拒，不会浪费后续步骤。

**为什么要分开记原因**：模型传了 `key_id: 123`（类型错）和传了别人的 `key_id`（越权）是两类问题，前者要它改参数，后者要报警。混成一个 `error` 就没法区分。

### 2. `ToolResult` 是唯一的返回形状

```python
ToolResult.ok(data, tool_name=..., duration_ms=...)
ToolResult.fail("file not found", error_type="ToolPermissionError")
```

规则（完整定义见 [CONTRACTS.md](../CONTRACTS.md#1-toolresult所有工具的唯一返回类型)）：

- **handler 不抛异常**：预期失败转成 `success=False`
- **意外异常由 `executor` 捕获并分类**，不是往上抛
- **取消（`CancelledError`）必须继续传播**，不能被吞
- **空结果是成功**：`success=True, data=[]` 代表"查了，没有"，不是失败

### 3. 资源授权在服务端，不在 schema 里

`file_id` 格式合法（`file_002`）**不代表你有权访问它**。这两件事必须分开：

```text
schema: file_id 是 1–128 个 [A-Za-z0-9_-] 字符     ← 形状
授权:   file_002 属于 project_alpha，当前用户在其中  ← 归属
```

06 段加上身份之后，同一个 `file_002` 对不同用户会有不同结果。**schema 永远回答不了"该不该"**。

### 4. 风险等级决定"能不能自动跑"

| 等级 | 含义 | 默认策略 |
|---|---|---|
| L0_READ | 读、摘要、解析 | 自动执行 |
| L1_COMPUTE | 沙箱内计算 | 自动执行，进沙箱 |
| L2_WRITE | 写文件、签名、加密 | **需审批** |
| L3_EXECUTE | 执行外部程序 | 需审批 + 沙箱 |
| L4_DESTRUCTIVE | 销毁、改信任 | 需强审批 |

"需审批"在 06 段实现。这一段只需保证：**L2 及以上没有审批就拒绝**。

### 5. 只读工具池——现在超界了

实测当前注册到 MCP server、并被 `bridge.discover_tools()` 全部暴露给模型的工具：

| 工具 | 类型 | 本段应该 |
|---|---|---|
| `sha256_file` | 只读 | 保留 |
| `sm2_verify_signature` | 只读 | 保留 |
| `sm2_generate_key` | **写** | **摘掉注册** |
| `sm2_sign_message` | **写** | **摘掉注册** |
| `sm2_enc` | **写** | **摘掉注册** |
| `sm2_dec` | **写** | **摘掉注册** |

`sm2_generate_key` 会真的往 `keys/` 写密钥。在 02–04 段，**写操作在模型面前不该存在**——不是"被拒绝"，而是**根本不出现在工具列表里**。

二者区别很大：被拒绝会诱导模型反复尝试；看不见它就不会提。

---

## 分步实现

### 步骤 1 先把契约接上

把 `execute_tool` 的返回从裸 dict 改成 `ToolResult`：

```python
async def execute_tool(session, name, arguments, tools) -> ToolResult[Any]:
    ...
    if error is not None:
        return ToolResult.fail(error["message"], error_type=error["error"])
    ...
    return ToolResult.ok(result, tool_name=name)
```

同时让 handler 的异常在这里落地：

```python
except ToolNotFoundError as e:
    return ToolResult.fail(str(e), error_type="ToolNotFoundError")
except CancelledError:
    raise                      # 取消必须传播，不能吞
except Exception as e:         # 意外异常在这层分类
    return ToolResult.fail(scrub(str(e)), error_type="ToolError")
```

改完之后跑一遍现有测试——**大概率有测试会红**，因为断言的是 dict 形状。这时要判断：是测试在测实现细节（改断言），还是在测契约（改实现）。**不要无条件改测试。**

### 步骤 2 摘掉写工具

```python
# mcp_integration/server_crypto/gmssl_tools/sm_tools.py
def register_tools(mcp: MCPServer) -> None:
    # 02–04 段只暴露只读工具；写操作 06 段再开
    mcp.tool(annotations=ToolAnnotations(read_only_hint=True, destructive_hint=False))(
        sm2_verify_signature
    )
    # sm2_generate_key / sm2_sign_message / sm2_enc / sm2_dec 暂不注册
```

**代码保留**，只关注册。然后确认模型看不见了：

```bash
python -c '
import asyncio
from mcp_integration.client.connection import connect_tools
async def main():
    async with connect_tools() as (session, tools):
        print([t["function"]["name"] for t in tools])
asyncio.run(main())
'
```

**预期**：只剩只读工具。

### 步骤 3 实现 `security/resources.py`

职责只有一件：把不可信的资源 ID 变成可信的路径，越界就拒绝。

```python
from pathlib import Path

def resolve_file(file_id: str) -> Path:
    """把服务端 ID 解析为受控路径；任何不合规都抛 ToolPermissionError。"""
    if not re.fullmatch(r"[A-Za-z0-9_-]{1,128}", file_id):
        raise ToolPermissionError("invalid file_id", file_id=file_id)
    root = get_settings().crypto_data_root.resolve()
    path = (root / file_id).resolve()
    if not path.is_relative_to(root):          # 关键：防目录穿越
        raise ToolPermissionError("path escapes root", file_id=file_id)
    if path.is_symlink() or not path.is_dir():
        raise ToolPermissionError("not a directory", file_id=file_id)
    return path
```

三个要点：

- **`resolve()` 之后再比较**，否则 `..` 和软链都能绕过
- **`is_relative_to` 而不是 `startswith`**，因为字符串前缀会把 `/data_evil` 当成 `/data` 的子目录
- 越界抛**专门的权限异常**，不要复用"文件不存在"

### 步骤 4 实现 `security/policy.py`

```python
def check_policy(spec: ToolSpec) -> None:
    policy = DEFAULT_POLICY[spec.risk_level]
    if not policy.allowed:
        raise ToolPermissionError("risk level not allowed", risk=spec.risk_level.name)
    if not policy.auto:
        raise ToolPermissionError(
            "requires approval, not implemented until stage 06",
            tool=spec.tool_id, risk=spec.risk_level.name,
        )
```

**在审批实现之前，"需要审批"就等于"不许执行"。** 这是安全的选择：默认拒绝，而不是默认放行。

### 步骤 5 让执行入口按顺序调用

```text
validate_tool_arguments  →  schema
lookup_toolspec          →  登记（不存在 → ToolNotFoundError）
resolve_resource         →  resources.py
check_policy             →  policy.py
call_provider            →  执行
```

每一步失败都返回 `ToolResult.fail(...)`，带**不同的 `error_type`**。

### 步骤 6 验证六个反例

| 输入 | 期望 `error_type` | 要证明什么 |
|---|---|---|
| `tool_name="run_shell"` | `ToolNotFoundError` | 未登记的工具被拒 |
| `file_id=123`（整数） | `ToolValidationError` | schema 拦类型错 |
| `file_id="../../etc/passwd"` | `ToolPermissionError` | 目录穿越被拒 |
| 不存在的 `file_id` | `ToolPermissionError` | 存在性检查 |
| 超过大小上限的文件 | `ToolValidationError` | 边界值 |
| 调用写工具名 | `ToolNotFoundError` | 已摘掉注册 |

**每一个都要证明 Provider 没有被调用**。方法：给 Provider 函数打桩计数，或看 `subprocess` 是否真的起过。

---

## 常见坑

1. **用 `str(path).startswith(root)` 判断越界。** `/data_evil/x` 会被误判成在 `/data` 里。用 `is_relative_to`。
2. **先 `resolve()` 一次就以为安全了。** 必须在解析**之后**比较；软链和 `..` 都靠这一步拦住。
3. **把"未找到"和"越权"混成一个错误。** 会让攻击者通过错误差异探测哪些 ID 存在。
4. **在 schema 里塞业务授权。** JSON Schema 表达不了"这个 file 属于这个 project"。
5. **改测试来迁就新的返回值。** 先判断测试测的是契约还是实现。
6. **忘了摘写工具的注册。** 只要它还出现在 `tools/list` 里，模型就会尝试调用。
7. **把 `DEFAULT_POLICY` 当真实授权。** 它只是本地第一道闸门，不代表用户身份或项目归属。

---

## 自检问题

1. 模型传 `{"file_id": "../../etc/passwd"}`，哪一行代码拦住的？如果只做 schema 校验会怎样？
2. 为什么"需要审批"在 06 段之前必须等于"拒绝"？如果这一段先放行，会有什么后果？
3. `attempt`（模型提议）、`denied`（执行器拒绝）、`executed`（真实执行）三者怎么在结果里区分？
4. 摘掉写工具注册之后，模型还会尝试调用它们吗？怎么证明它看不见了？
5. 你改的一处授权规则是什么？正常和越权两条路分别怎么变？

---

## 本人记录

```text
日期：
实际工时：
接上契约后哪些测试红了，你怎么判断该改哪边：
六个反例的实际 error_type：
摘掉写工具后模型看到的工具清单：
还没理解的：
```
