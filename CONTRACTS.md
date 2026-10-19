# 接口契约

这里放**跨阶段稳定**的类型与规则。它们被多个阶段引用，所以单独成文：改这里会影响所有阶段，改之前先跑相关回归。

契约分三类：**① 数据类型**（ToolResult / ToolSpec）、**② 执行规则**（唯一入口、执行顺序、重试）、**③ 工具清单**（canonical ID、输入、风险）。

> 状态说明：下面的代码是**目标契约**，不是当前应用已实现的全部类型。当前骨架字段与迁移任务见 §5。

---

## 1. ToolResult：所有工具的唯一返回类型

```python
from typing import Any, Generic, TypeVar
from pydantic import BaseModel, ConfigDict, Field

T = TypeVar("T")


class ToolResult(BaseModel, Generic[T]):
    model_config = ConfigDict(extra="forbid")

    success: bool
    data: T | None = None
    error_type: str | None = None
    error: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)
    evidence_refs: list[dict[str, Any]] = Field(default_factory=list)
```

四条硬规则：

| 规则 | 说明 |
|---|---|
| **handler 不抛异常** | 工具函数内部把预期失败转成 `success=False`；意外异常由 `execute_tool` 捕获并分类 |
| **空结果不是失败** | `success=True, data=[]` 是合法的"查到了但没有"。这个区分决定要不要重试 |
| **容器字段用 default_factory** | 禁止可变默认值共享 |
| **序列化用 `model_dump_json()`** | 不用 dataclass，因为它没有这个方法且嵌套校验弱 |

`error_type` 的取值来自 `packages/core/errors.py`：

```text
ToolValidationError  入参不符合 schema 或业务规则
ToolPermissionError  RBAC 拒绝，或资源不在白名单内
ToolTimeoutError     工具执行超时（注意：wait_for 超时 ≠ 子进程已死）
ToolOutputTooLargeError  输出超限，应截断或转 result_ref
ToolNotFoundError    模型请求了注册表里不存在的工具（必须显式拒绝）
SandboxError         隔离环境失败，不可降级为宿主机执行
BudgetExceededError  步骤/总时限/token 预算耗尽
```

**取消（CancelledError）必须继续传播，不能被吞掉。**

---

## 2. ToolSpec：注册表条目

```python
from enum import IntEnum
from typing import Any, Awaitable, Callable
from pydantic import BaseModel, ConfigDict


class RiskLevel(IntEnum):
    L0_READ = 0
    L1_COMPUTE = 1
    L2_WRITE = 2
    L3_EXECUTE = 3
    L4_DESTRUCTIVE = 4


class ToolSpec(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, extra="forbid")

    tool_id: str                    # canonical ID，不是外部 server 的名字
    version: str
    description: str                # 必须写清"什么时候用"和"什么时候不用"
    input_schema: dict[str, Any]
    output_schema: dict[str, Any]
    timeout_s: float                # > 0
    permission: str
    risk_level: RiskLevel
    read_only: bool
    idempotent: bool
    max_retries: int                # >= 0
    handler: Callable[..., Awaitable[ToolResult[Any]]]
```

运行时必须约束（`model_post_init` 里守卫）：

| 约束 | 理由 |
|---|---|
| `timeout_s > 0`、`max_retries >= 0` | 无超时/负数重试都是一次故障的温床 |
| `max_retries > 0` **必须** `idempotent=True` | 非幂等操作不得自动重试 |
| **所有非只读操作 `max_retries = 0`** | 签名/加密/轮换不因模型重复提议或连接错误自动重跑 |
| `read_only=True` **不等于** 幂等 | 读操作也可能有费用或限额 |

写入类动作的重传靠**账本返回已有结果**，不靠自动重试。

### 默认风险策略

```python
DEFAULT_POLICY = {
    RiskLevel.L0_READ:        Policy(auto=True,  sandbox=False, approval=False),
    RiskLevel.L1_COMPUTE:     Policy(auto=True,  sandbox=True,  approval=False),
    RiskLevel.L2_WRITE:       Policy(auto=False, sandbox=False, approval=True),
    RiskLevel.L3_EXECUTE:     Policy(auto=False, sandbox=True,  approval=True),
    RiskLevel.L4_DESTRUCTIVE: Policy(auto=False, sandbox=True,  approval="strong"),
}
```

**默认 Policy 不替代真实授权和审批。** 它只是本地的第一道闸门。

---

## 3. 唯一执行入口：六步顺序

所有模型发起的工具调用只走 `execute_tool`。不允许别的路径。

1. 创建内部 `attempt` / `correlation`，规范化参数，做 schema 与业务校验。
2. 校验用户、项目、资源、工具 permission 与预算；**记录拒绝**。
3. 把 用户 / 项目 / 工具版本 / 规范参数 / 资源版本 / 策略版本 绑定到 `action_hash`。审批必须匹配这个 hash。
4. 短事务写 action intent 和审批/lease 状态，**然后释放 DB 事务**。
5. 经受控 runner 执行，校验输出大小与 schema，写结果和最终审计。
6. 失败/取消/拒绝走统一的 finally 或 outcome 路径记录。

两条 fail 语义：

- **执行前**安全审计持久化失败 → **fail closed，不执行**。
- **执行后**审计失败 → 保留结果 / 标记待补偿，**绝不重新执行动作**。

日志脱敏、截断、结果 blob 引用统一在这一层处理。

---

## 4. 工具清单（canonical ID）

这些 ID 已进入评测 schema，**不代表应用全部实现**。新增/修改要同步 registry、schema、validator、MCP bridge 与用例。

| 工具 | 主要输入 | 返回给 Agent | 引入阶段 |
|---|---|---|---|
| `digest_file` | file_id / provider / algorithm | 摘要、编码、文件大小、版本 | 02 |
| `inspect_certificate` | certificate_id | subject/issuer/serial/SAN/有效期/用途/指纹 | 02 |
| `verify_certificate` | certificate_id / trust_store_id / hostname / purpose | 各检查的 status、错误、检查时钟 | 03 |
| `verify_signature` | file_id / signature_id / public_key_id / scheme | valid/invalid 与方案参数 | 03 |
| `get_key_metadata` | key_id | provider、用途、版本、状态、归属 | 05 |
| `encrypt_file` | file_id / key_id / profile | 密文 artifact_id、版本、算法 | 06 |
| `decrypt_file` | encrypted_artifact_id | 输出 artifact_id 与状态 | 06 |
| `sign_file` | file_id / key_id / scheme | signature artifact_id 与实际方案 | 06 |
| `rotate_key` | key_id / expected_version | 新旧版本与生命周期状态 | 06 |
| `create_csr` | 测试私钥引用 / subject / SAN | CSR artifact_id 与解析字段 | 06 |
| `issue_test_certificate` | csr_id / profile | certificate_id / serial / 有效期 / 用途 | 06 |
| `search_knowledge` | query / filters | 片段 + 来源 + 版本 | 08 |
| `query_database` | 固定 query_id + 结构化参数 | 获授权的元数据与执行记录 | 08 |

**不提供的**：通用 `run_shell`、任意 `openssl`/`gmssl` 参数透传、任意路径工具。Provider 是明确枚举，algorithm/profile 是允许列表。

`generate_key` 可作为专门的管理 API，首版不直接开放给模型。

`query_database` 只接受固定 `query_id`，**禁止模型传原始 SQL**。

---

## 5. 当前骨架 → 目标契约的映射

以 2026-10-10 读取的 Ubuntu 应用骨架为起点。开发时重新核对实际模型与 registry，不要把本表当永久事实。

| 当前骨架 | 目标语义 | 迁移任务 |
|---|---|---|
| `ToolSpec.name` | canonical `tool_id` | 02 保留 `name` 作为注册键；06 明确适配并锁定 canonical 映射，避免两个名称漂移 |
| `ToolSpec.retry` | `max_retries` + 幂等策略 | 非只读 `retry=0` 保持；增加 `idempotent` 与本地许可，不能从 `read_only` 自动推断可重试 |
| 尚无独立 `version` 字段 | tool version | 初期 registry 配置记录版本；06 写入 Spec/action/approval/runtime 快照，变更即审批失效 |
| `ToolResult.citations`（文档型） | 通用 `evidence_refs` + 知识 Citation | 02 按现有 citations 验证；08 设计文档证据与工具结果引用的转换，不把 artifact 伪造为文档页码 |
| `ToolCall.tool_name` / `call_id` | canonical `tool_id` + 内部 call 关联 | ModelClient/bridge 显式转换；原生 `tool_name` 与应用内部 ID **分别保存** |
| `source` / `mcp_server` | 工具来源 / 受信任 Server 关联 | 保留追踪；本地 policy 不信任外部 annotation |
| 当前 `RiskLevel` L0–L4 | 本地风险语义 0–4 | 数值/名字差异显式映射；敏感解密与写动作按 06 固定审批，不因名字自动降级 |

**新增 `idempotent` / `version` / `evidence_refs` 前，先定义读取旧记录的行为。** 迁移后的输出与评测 schema 必须一致。

---

## 6. 配置契约

`Settings` 字段名（大写）与 `.env.example` 的键必须**双向一致**，由 `scripts/selftest.py` 自动校验。所以不存在"文档里有、代码里没有"的配置项。

几条与契约相关的配置：

| 字段 | 作用 | 注意 |
|---|---|---|
| `CRYPTO_TIMEOUT_S` | Provider 子进程超时 | 超时后必须核对进程真的退出了 |
| `CRYPTO_MAX_FILE_BYTES` | 输入文件上限 | 边界值可接受、超出被拒绝 |
| `LLM_TIMEOUT_S` | 模型请求超时 | 与工具超时是两件事 |
| `LLM_NUM_CTX` | 上下文窗口 | 当前配置了但代码没读，04 阶段要接上 |
| `OLLAMA_BASE_URL` / `CONTROLLER_MODEL` | 模型地址与名称 | 必须走 Settings，不要硬编码 |

---

## 7. 改契约前必须做的事

```text
[ ] 找全调用方（grep tool_id / ToolResult / max_retries）
[ ] 定义旧数据的读取行为（本次不迁就下次迁）
[ ] 同步 registry、schema、validator、MCP bridge、评测 schema
[ ] 跑相关阶段的自检问题
[ ] 跑 pytest（契约改动通常会打穿多个测试）
```

**不要**为了通过某个测试去放宽契约。契约改了要说明依据。
