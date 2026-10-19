# 06. 审批与写操作（55h）

> 完成这一段，你能做到：**让系统真的写东西，同时在任何一个位置崩掉都不重复动手、也不谎报成功。**

这是全项目最难的一段。前五段的所有动作都可以重跑；从这一段开始，**外部副作用一旦发生就收不回来**。

---

## 在流程中的位置

[FLOW.md](../FLOW.md) 的 **⑧⑨⑪⑫** ——写操作闸门、intent、账本、恢复。

前置：05 段（账本要用它的表）。解锁：07 段的写工具 MCP 包装。

```text
tool_calls（写动作）
      ↓
  ① 审批校验     action_hash 匹配吗？过期吗？消费过吗？
      ↓
  ② 写 intent    短事务落盘"我打算做什么"
      ↓
  ③ 执行         Provider 真正动手（此时副作用可能已发生）
      ↓
  ④ 写结果       成功/失败/unknown
      ↓
  ⑤ 恢复         重启后按账本对账，不盲目重跑
```

---

## 要写的代码

| 文件 | 职责 | 现状 |
|---|---|---|
| `packages/security/approvals.py` | 审批绑定与单次消费 | ❌ 空桩 |
| `packages/db/models.py` | `actions` / `approvals` / `artifacts` / `crypto_keys` / `key_versions` | ❌ 需扩展 |
| `graph/nodes/` | 最小图、审批等待、恢复 | ❌ 空目录 |
| `packages/crypto/keystore.py` | key version 管理 | ⚠️ 已有密钥生成，需加版本 |
| `verifier/checks/` | 事实/引用/动作检查 | ❌ 空目录 |
| `services/agent_api/routers/` | `/runs/{id}/approve`、`/artifacts/{id}/download` | ❌ 需新增 |

---

## 核心概念

### 1. 先做 AEAD，再谈审批

审批是为了保护写操作，而本段第一个写操作是**加密**。所以先在没有 Agent 的情况下把 AEAD 跑通：

```bash
# 直接用 openssl，不经任何项目代码
openssl enc -aes-256-gcm ...   # 或选定方案
```

要求：字节往返一致；改密文/tag/AAD/key 任一都必须失败。

**注意**：`openssl enc` 命令**不支持 GCM**（OpenSSL 3.0.2 的 `enc` 里没有 GCM）。要么用 Python 的 `cryptography` 库，要么用别的已验证方案。**在选定之前不要写"支持 AES-GCM"**。

选定的方案要记进能力清单，并写清：算法、key 长度、nonce 长度、tag 长度、AAD 规则。

### 2. nonce 唯一性不能交给模型

| 谁生成 | 可否 |
|---|---|
| 模型 | ❌ 它会重复 |
| 客户端 | ❌ 多客户端会撞 |
| **密码服务** | ✅ 唯一正确的地方 |

同一 key version 下**禁止复用 nonce**。这一点必须由存储约束或分配方案保证，并在并发和恢复场景下仍然成立。

幂等重传要返回**原动作的 artifact**，不是"用旧 nonce 再加密一次"。

### 3. `action_hash` 绑定的是"这一件事"，不是"这个 Run"

```text
action_hash = H(
    用户/项目身份
  + 工具版本
  + 规范化参数
  + 资源版本（file_id + content_hash、key_id + key_version）
  + policy 版本
)
```

审批批准的是**显示出来的那个具体动作**。所以：

- 参数改了 → hash 变 → 旧审批失效
- 文件内容变了 → 资源版本变 → 旧审批失效
- key 轮换了 → key_version 变 → 旧审批失效
- **不能对整个 Run 发一次空白授权**

### 4. 账本状态机

```text
proposed → awaiting_approval → ready → executing → succeeded
                                            ↓
                              failed / cancelled / unknown
```

`unknown` 是最重要的状态。它表示"我不知道外部动作到底做了没有"。**不能当成功，也不能当失败重试。**

### 5. 账本和 checkpoint 分工不同

| | 恢复什么 | 不能替代 |
|---|---|---|
| **动作账本**（DB 表） | 真实副作用的状态 | 控制流 |
| **checkpoint**（Graph） | 控制流：走到哪个节点 | 副作用记录 |

**不能把 checkpoint 当外部原子事务。** 它的作用是让你回到"待审批"或"执行中"这个位置，但"到底做没做"要查账本和 Provider 侧。

### 6. 六个崩溃位置，六种处理

| 崩在哪 | 恢复动作 |
|---|---|
| intent 未提交 | 不存在动作，不执行 |
| intent 已提交、未批准 | 恢复待审批，展示同一 hash |
| 已批准、未开始 | 原 approval + 幂等键领取 |
| 执行中 | 按 `external_job_id`/幂等键核对，等待或标 unknown |
| 外部已完成、完成记录未提交 | 核对已完成结果并补账，**不可盲目重跑** |
| 已记录完成 | 返回已有 `result_ref` |

### 7. 审批的三条硬规则

```text
① 只授权特定动作，不授权后续模型新提议
② 重复请求返回原决定；并发批准与拒绝只有一个成功
③ 校验权限、有效期、pending 状态、未消费、action 未变
```

**按钮禁用只是体验，服务端 CAS/单次消费才提供正确性。**

审批请求体只有三个字段：

```json
{"approval_id": "...", "action_hash": "...", "decision": "approved"}
```

前端**只提交**这三个。风险等级、角色、参数都从服务端读。审批者身份来自鉴权。

面板必须显示：canonical tool、规范参数、影响资源与版本、风险/策略版本、hash、期限、发起者、执行状态。

### 8. key version 的四层区分

| 层 | 是什么 | 存在哪 |
|---|---|---|
| 逻辑密钥 | `key_id`，用户看到的名字 | DB 元数据 |
| 密钥版本 | `version`，轮换产生 | DB 元数据 |
| 加密密钥材料 | key blob | keystore（受控目录） |
| 保护材料的秘密 | 解锁口令/主密钥 | **不进代码、不进日志、不进配置样例** |

轮换规则：**新加密用新版本，旧密文仍绑原版本**。旧版本能否解密由本地策略决定。

"停用 / 撤销 / 销毁"是三种不同状态，不要混用一个字段。

### 9. artifact 只回 ID，不回内容

`ToolResult` 里只放状态和 `artifact_id`。下载走单独接口，每次重新鉴权。**明文永远不进聊天正文，也不进模型上下文。**

---

## 分步实现

### 步骤 1 AEAD 往返 + 认证失败（T006，5h）

不接 Agent，直接验证：

```text
明文 → 加密 → 密文 → 解密 → 明文（逐字节相同）
改密文一个字节 → 解密失败
改 tag → 解密失败
改 AAD → 解密失败
错 key → 解密失败
```

再补一条**独立已知向量或固定格式对照**。往返只证明两条路径相容，两边一起错也会"通过"。

### 步骤 2 建表

```sql
CREATE TABLE crypto_keys (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  project_id UUID NOT NULL REFERENCES projects(id),
  owner_id   UUID NOT NULL REFERENCES users(id),
  name TEXT NOT NULL,
  provider  TEXT NOT NULL CHECK (provider IN ('openssl','gmssl')),
  algorithm TEXT NOT NULL,
  usage JSONB NOT NULL,
  status TEXT NOT NULL CHECK (status IN ('active','disabled','revoked')),
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  FOREIGN KEY (project_id, owner_id) REFERENCES project_members(project_id, user_id)
);

CREATE TABLE key_versions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  key_id UUID NOT NULL REFERENCES crypto_keys(id),
  version INT NOT NULL CHECK (version >= 1),
  encrypted_blob_ref TEXT NOT NULL UNIQUE,
  status TEXT NOT NULL CHECK (status IN ('active','decrypt_only','disabled','revoked')),
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  UNIQUE (key_id, version)
);
-- 每个 key 只能有一个 active 版本
CREATE UNIQUE INDEX idx_key_one_active ON key_versions(key_id) WHERE status = 'active';

CREATE TABLE actions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  run_id UUID NOT NULL REFERENCES agent_runs(id),
  tool_id TEXT NOT NULL,
  tool_version TEXT NOT NULL,
  canonical_arguments JSONB NOT NULL,
  action_hash TEXT NOT NULL,
  policy_version TEXT NOT NULL,
  idempotency_key TEXT NOT NULL UNIQUE,
  risk_level SMALLINT NOT NULL CHECK (risk_level BETWEEN 0 AND 4),
  status TEXT NOT NULL CHECK (status IN (
    'proposed','awaiting_approval','ready','executing',
    'succeeded','failed','cancelled','unknown')),
  external_job_id TEXT,
  result_ref JSONB,
  lease_owner TEXT, lease_until TIMESTAMPTZ,
  fencing_token BIGINT NOT NULL DEFAULT 0,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE approvals (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  action_id UUID NOT NULL REFERENCES actions(id),
  action_hash TEXT NOT NULL,
  requested_by UUID NOT NULL REFERENCES users(id),
  decided_by   UUID REFERENCES users(id),
  decision TEXT NOT NULL CHECK (decision IN ('pending','approved','rejected','expired','revoked')),
  expires_at TIMESTAMPTZ NOT NULL,
  decided_at TIMESTAMPTZ,
  consumed_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
-- 一个 action 同时只能有一个 pending 审批
CREATE UNIQUE INDEX idx_one_pending_approval ON approvals(action_id) WHERE decision = 'pending';

CREATE TABLE artifacts (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  project_id UUID NOT NULL REFERENCES projects(id),
  owner_id   UUID NOT NULL REFERENCES users(id),
  action_id  UUID NOT NULL REFERENCES actions(id),
  input_file_id  UUID REFERENCES files(id),
  key_version_id UUID REFERENCES key_versions(id),
  kind TEXT NOT NULL CHECK (kind IN ('ciphertext','plaintext','signature','csr','certificate')),
  storage_ref  TEXT NOT NULL UNIQUE,
  content_hash TEXT NOT NULL,
  size_bytes BIGINT NOT NULL CHECK (size_bytes >= 0),
  format_version TEXT NOT NULL,
  profile TEXT NOT NULL,
  metadata JSONB NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  FOREIGN KEY (project_id, owner_id) REFERENCES project_members(project_id, user_id)
);
```

注意 `idx_one_pending_approval` 是**部分唯一索引**——它把"同时只有一个待审批"这件事交给数据库保证，而不是靠应用代码自觉。

### 步骤 3 算 action_hash

规范化参数是关键：同一个语义的两种写法必须得到同一个 hash（字段顺序、数字格式、空格）。

```python
def action_hash(*, user_id, project_id, tool_id, tool_version,
                canonical_args, resource_versions, policy_version) -> str:
    payload = {...}                       # 确定性序列化，键排序
    return hashlib.sha256(canonical_json(payload).encode()).hexdigest()
```

06 段用哪个 hash 函数可以自选，但**必须写进文档并固定**——变了以后所有旧审批都会失效。

### 步骤 4 审批端点

```text
POST /runs/{id}/approve
  body: {approval_id, action_hash, decision}
  → 校验：权限 / 有效期 / pending / 未消费 / action 未变
  → 单次消费（UPDATE ... WHERE consumed_at IS NULL 检查影响行数）
  → 返回新 snapshot
```

**并发测试必须做**：两个请求同时批准同一个 action，只能有一个 succeed。

### 步骤 5 最小 Graph + 持久 checkpoint

```text
Router → Planner → Tool/Approval → Draft → Verify → Final
```

State 里只放**引用**，不放内容：

| 类别 | 放什么 | 约束 |
|---|---|---|
| 身份/版本 | run_id、可信 user/project、graph/schema/config 版本 | 客户端不可覆盖可信身份 |
| 控制/预算 | 节点、步数、deadline、停止原因 | 恢复后**不重置预算** |
| 上下文/证据 | 有限消息摘要、document/version/chunk/result_ref | 不存密钥和全文 |
| 动作/审批 | pending action ID/hash、approval ID/状态 | 参数固定，与账本核对 |
| 草稿/验证 | draft_ref、Claim/Citation 引用 | 未通过不得展示为已验证 |

`thread_id = run_id`：一次请求一个工作流。聊天历史从 `messages` 表加载，不塞进 checkpoint。

### 步骤 6 三处崩溃演练

必须真的 `kill -9` 进程，然后重启观察：

```text
① 批准后、执行前 kill   → 重启后应领取原 action，不生成新参数
② 执行中 kill           → 重启后按 job_id/幂等键核对，等待或标 unknown
③ 外部完成、写回前 kill → 重启后核对已完成结果并补账，不重跑
```

**三种情况都要证明外部副作用只发生了一次。**

### 步骤 7 基础 Verifier（5h）

最小检查项：

```text
结构检查：回答里的字段是否符合预期 schema
动作检查：引用真实 executed 记录，不是模型说的"已完成"
事实检查：数值/单位/实体绑定是否正确
```

区分三件事：**attempt**（模型提议）、**denied**（执行器拒绝）、**executed**（真实执行）。只有 `executed` 能作为"做成了"的证据。

### 步骤 8 写操作的工具评测（部分）

至少 20 个写工具用例，覆盖：正常、参数错、越权、审批过期、重复提交、执行失败。

---

## 常见坑

1. **用 `openssl enc` 做 GCM。** OpenSSL 3.0.2 的 `enc` 不支持 GCM。先确认方案可选再声称支持。
2. **往返通过就认为实现正确。** 实现和测试一起错也会通过。必须有独立向量。
3. **认证失败后仍然生成输出文件。** 必须先完成认证再创建可下载输出，且不覆盖原文件。
4. **只检查"回答里说了拒绝"，不检查副作用。** 要查资源状态和 `execution_count`。
5. **按钮禁用当并发保护。** 必须服务端 CAS/单次消费。
6. **审批跨 Run 复用。** 它只授权那个特定动作。
7. **恢复时重置步数/deadline 预算。** 等于给了无限循环。
8. **把 unknown 当失败直接重试。** 可能造成第二次副作用。
9. **把 checkpoint 当副作用账本。** 它只证明控制流走到哪。
10. **只备份 DB 就说"密钥能力已恢复"。** 没有 keystore blob，密钥就是废的。
11. **明文进了 ToolResult / State / 日志 / 堆栈。** 一条都不能有。
12. **敏感操作把口令放进程命令行。** `ps` 可见。这种 CLI 入口首版不接。

---

## 自检问题

1. 为什么同一 key version 下 nonce 唯一性不能交给模型？你的分配、保存、重复检查各在哪？
2. `action_hash` 绑定了哪几项？审批后文件或 key_version 变了，原批准怎么被拒？
3. 为什么执行前要写 intent？账本和 checkpoint 各证明什么？
4. 批准后执行前 / 执行中 / 外部完成未写回，三种情况分别怎么恢复？给出真实账本对照。
5. `unknown` 为什么既不能当失败重试、也不能当成功展示？你的核对步骤是什么？

---

## 本人记录

```text
日期：
实际工时：
AEAD 方案与参数（算法/nonce/tag/AAD），以及认证失败的实测：
action_hash 的组成与 hash 函数：
三处崩溃演练的过程与账本状态：
并发审批的结果（谁赢了）：
还没理解的：
```
