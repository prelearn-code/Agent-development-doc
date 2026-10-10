# 仓库结构与工程契约

> 应用接口、数据库与执行语义的唯一设计来源。评测记录字段另由 [eval/dataset.schema.json](eval/dataset.schema.json) 管理。结构随里程碑逐步建立，经过迁移与版本管理可以修改，不要求第一天冻结全部模块。

## 1. 目录与依赖

```text
Agent-development-code/
  pyproject.toml / uv.lock / .env.example / tasks.sh
  infra/compose.yml / migrations/ / dockerfiles/
  src/lpa/
    core/         Pydantic 契约、枚举、纯计算；无外部 IO
    config/       Settings、日志配置与脱敏
    llm/          Ollama 原生 NDJSON adapter；兼容端点单独 adapter
    db/           ORM、短事务 repositories、授权视图
    security/     policy、executor、审批校验、审计接口
    crypto/       OpenSSL/GmSSL adapters、能力探测、keystore接口
    tools/        registry、密码/知识工具与 handler
    ingest/       解析、版本化 chunk 与 index manifest
    retrieval/    dense、sparse、fusion、rerank、rewrite
    mcp_adapter/  MCP client、canonical tool bridge、连接配置
    graph/        State、节点、checkpoint、resume
    memory/       提取、授权、更新、去重
    verifier/     事实/引用/输出检查
    api/          FastAPI assembly、资源路由、SSE
    worker/       持久化任务、lease、取消和结果核对
  minimal_agent/  M1 手写版本；从同一 tools/executor 调用
  mcp_servers/    fs/db/domain；独立 entrypoint
  web/           前端
  eval/          Schema、fixtures、scenario runner、metrics、compare
  tests/         合同、故障和集成测试
  docs/decisions/ / docs/progress.md / docs/to-digest.md
  reports/ / data/（不提交真实数据/秘密）
```

Python 包使用合法可导入名称，不把 `agent-api` 目录当 import package，也不使用 `mcp` 顶级包名遮蔽第三方 SDK。M1 可以只建 core/config/tools/llm/minimal_agent。工具包默认在同一个可安装项目内；确需独立发布时再定义 workspace 包和依赖。

core 不依赖 IO 层；llm/db 依赖 core；tools 通过注入 ports 使用 db/retrieval/crypto；graph 编排上述模块；api/worker 装配。executor 调 handler，handler 不回调 graph/api。使用 AST/import-linter 检查分层与唯一 handler 调用点，不用简单 grep 作为安全证明。

## 2. 身份、资源与运行

- user_id 来自服务端鉴权，session_id/project_id 必须核对归属或 membership。
- run_id 表示一次请求；client_request_id 在同一用户下唯一，POST 重传返回原 Run。
- thread_id=run_id 是本项目工作流策略；每轮聊天历史显式从 messages 加载。
- action_id 表示一次具体外部动作，tool_call_id 表示一次执行 attempt；模型报文 ID 不承担幂等作用。
- 每次检索绑定 corpus_version/index_manifest；每个证据和结果引用都能恢复到同一内容版本。
- 任何查看、下载、approve、resume、cancel、events、Memory 操作都检查用户与资源权限。

## 3. 数据库设计

以下为 PostgreSQL 16 + pgvector 的参考迁移 DDL。扩展由bootstrap管理员安装，应用表以migration_owner身份创建并保持其所有权。执行顺序已按 FK 依赖排列；checkpointer 使用独立 schema，由锁定版本的 AsyncPostgresSaver.setup 管理，不能把全部内部表当作一张 checkpoints 表。初期表按里程碑迁移，SQL 未在本包连接真实 PostgreSQL 执行。

```sql
CREATE EXTENSION IF NOT EXISTS pgcrypto;
CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  username TEXT NOT NULL UNIQUE,
  api_key_hash TEXT NOT NULL UNIQUE,
  role TEXT NOT NULL DEFAULT 'viewer' CHECK (role IN ('admin','engineer','viewer')),
  is_active BOOLEAN NOT NULL DEFAULT TRUE,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE TABLE projects (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(), name TEXT NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE TABLE project_members (
  project_id UUID NOT NULL REFERENCES projects(id),
  user_id UUID NOT NULL REFERENCES users(id),
  role TEXT NOT NULL CHECK (role IN ('owner','editor','viewer')),
  PRIMARY KEY(project_id,user_id)
);
CREATE TABLE sessions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id),
  project_id UUID NOT NULL REFERENCES projects(id),
  title TEXT, created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  FOREIGN KEY(project_id,user_id) REFERENCES project_members(project_id,user_id)
);
CREATE TABLE files (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  project_id UUID NOT NULL REFERENCES projects(id),
  owner_id UUID NOT NULL REFERENCES users(id),
  original_name TEXT NOT NULL, storage_ref TEXT NOT NULL UNIQUE,
  content_hash TEXT NOT NULL, size_bytes BIGINT NOT NULL CHECK(size_bytes>=0),
  media_type TEXT NOT NULL, version TEXT NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  FOREIGN KEY(project_id,owner_id) REFERENCES project_members(project_id,user_id)
);
CREATE TABLE crypto_keys (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  project_id UUID NOT NULL REFERENCES projects(id),
  owner_id UUID NOT NULL REFERENCES users(id),
  name TEXT NOT NULL, provider TEXT NOT NULL CHECK(provider IN ('openssl','gmssl')),
  algorithm TEXT NOT NULL, usage JSONB NOT NULL,
  status TEXT NOT NULL CHECK(status IN ('active','disabled','revoked')),
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  FOREIGN KEY(project_id,owner_id) REFERENCES project_members(project_id,user_id)
);
CREATE TABLE key_versions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  key_id UUID NOT NULL REFERENCES crypto_keys(id),
  version INT NOT NULL CHECK(version>=1), encrypted_blob_ref TEXT NOT NULL UNIQUE,
  status TEXT NOT NULL CHECK(status IN ('active','decrypt_only','disabled','revoked')),
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  UNIQUE(key_id,version)
);
CREATE UNIQUE INDEX idx_key_one_active ON key_versions(key_id) WHERE status='active';
CREATE TABLE certificates (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  file_id UUID NOT NULL REFERENCES files(id),
  key_version_id UUID REFERENCES key_versions(id),
  fingerprint TEXT NOT NULL, subject JSONB NOT NULL, issuer JSONB NOT NULL,
  serial TEXT NOT NULL, san JSONB NOT NULL,
  not_before TIMESTAMPTZ NOT NULL, not_after TIMESTAMPTZ NOT NULL,
  usages JSONB NOT NULL, parse_version TEXT NOT NULL,
  CHECK(not_after>=not_before)
);
CREATE TABLE agent_runs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id),
  session_id UUID NOT NULL REFERENCES sessions(id),
  client_request_id TEXT NOT NULL,
  graph_version TEXT NOT NULL, prompt_version TEXT NOT NULL,
  runtime_config JSONB NOT NULL,
  corpus_version TEXT,
  disconnect_policy TEXT NOT NULL CHECK(disconnect_policy IN ('cancel','detach')),
  status TEXT NOT NULL CHECK(status IN ('queued','running','awaiting_approval','reconciling','completed','failed','cancelled')),
  final_answer JSONB, verifier_report JSONB, error JSONB,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(), finished_at TIMESTAMPTZ,
  UNIQUE(user_id,client_request_id)
);
CREATE INDEX idx_runs_session ON agent_runs(session_id,created_at DESC);
CREATE TABLE messages (
  id BIGSERIAL PRIMARY KEY,
  session_id UUID NOT NULL REFERENCES sessions(id),
  run_id UUID REFERENCES agent_runs(id),
  role TEXT NOT NULL CHECK(role IN ('system','user','assistant','tool')),
  content JSONB NOT NULL,
  sequence_no BIGINT NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  UNIQUE(session_id,sequence_no)
);
CREATE TABLE agent_steps (
  id BIGSERIAL PRIMARY KEY,
  run_id UUID NOT NULL REFERENCES agent_runs(id),
  step_index INT NOT NULL CHECK(step_index>=0),
  attempt INT NOT NULL DEFAULT 1 CHECK(attempt>=1),
  step_type TEXT NOT NULL,
  status TEXT NOT NULL CHECK(status IN ('running','ok','failed','skipped','cancelled')),
  input_ref JSONB, output_ref JSONB,
  started_at TIMESTAMPTZ NOT NULL DEFAULT now(), finished_at TIMESTAMPTZ,
  UNIQUE(run_id,step_index,attempt)
);
CREATE TABLE actions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  run_id UUID NOT NULL REFERENCES agent_runs(id),
  tool_id TEXT NOT NULL, tool_version TEXT NOT NULL,
  canonical_arguments JSONB NOT NULL,
  action_hash TEXT NOT NULL,
  policy_version TEXT NOT NULL,
  idempotency_key TEXT NOT NULL UNIQUE,
  risk_level SMALLINT NOT NULL CHECK(risk_level BETWEEN 0 AND 4),
  status TEXT NOT NULL CHECK(status IN ('proposed','awaiting_approval','ready','executing','succeeded','failed','cancelled','unknown')),
  external_job_id TEXT, result_ref JSONB,
  lease_owner TEXT, lease_until TIMESTAMPTZ,
  fencing_token BIGINT NOT NULL DEFAULT 0,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(), updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX idx_actions_run ON actions(run_id,created_at);
CREATE TABLE artifacts (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  project_id UUID NOT NULL REFERENCES projects(id),
  owner_id UUID NOT NULL REFERENCES users(id),
  action_id UUID NOT NULL REFERENCES actions(id),
  input_file_id UUID REFERENCES files(id), key_version_id UUID REFERENCES key_versions(id),
  kind TEXT NOT NULL CHECK(kind IN ('ciphertext','plaintext','signature','csr','certificate')),
  storage_ref TEXT NOT NULL UNIQUE, content_hash TEXT NOT NULL,
  size_bytes BIGINT NOT NULL CHECK(size_bytes>=0), format_version TEXT NOT NULL,
  profile TEXT NOT NULL, metadata JSONB NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  FOREIGN KEY(project_id,owner_id) REFERENCES project_members(project_id,user_id)
);
CREATE TABLE approvals (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  action_id UUID NOT NULL REFERENCES actions(id),
  action_hash TEXT NOT NULL,
  requested_by UUID NOT NULL REFERENCES users(id),
  decided_by UUID REFERENCES users(id),
  decision TEXT NOT NULL CHECK(decision IN ('pending','approved','rejected','expired','revoked')),
  expires_at TIMESTAMPTZ NOT NULL,
  decided_at TIMESTAMPTZ, consumed_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE UNIQUE INDEX idx_one_pending_approval ON approvals(action_id) WHERE decision='pending';
CREATE TABLE tool_calls (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  run_id UUID NOT NULL REFERENCES agent_runs(id),
  step_id BIGINT REFERENCES agent_steps(id),
  action_id UUID NOT NULL REFERENCES actions(id),
  attempt INT NOT NULL CHECK(attempt>=1),
  source TEXT NOT NULL CHECK(source IN ('builtin','mcp')),
  mcp_server TEXT, status TEXT NOT NULL CHECK(status IN ('running','ok','failed','denied','timeout','cancelled','unknown')),
  result_ref JSONB, error JSONB,
  started_at TIMESTAMPTZ NOT NULL DEFAULT now(), finished_at TIMESTAMPTZ,
  UNIQUE(action_id,attempt)
);
CREATE TABLE llm_calls (
  id BIGSERIAL PRIMARY KEY,
  run_id UUID NOT NULL REFERENCES agent_runs(id), step_id BIGINT REFERENCES agent_steps(id),
  purpose TEXT NOT NULL CHECK(purpose IN ('route','plan','generate','rewrite','memory','verify','judge')),
  model_name TEXT NOT NULL, model_digest TEXT NOT NULL,
  config JSONB NOT NULL, prompt_tokens INT CHECK(prompt_tokens>=0),
  completion_tokens INT CHECK(completion_tokens>=0),
  load_ms INT CHECK(load_ms>=0), inference_ms INT CHECK(inference_ms>=0),
  started_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE TABLE documents (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  project_id UUID NOT NULL REFERENCES projects(id),
  uploaded_by UUID REFERENCES users(id), document_name TEXT NOT NULL,
  version TEXT NOT NULL, content_hash TEXT NOT NULL, source_uri TEXT NOT NULL,
  status TEXT NOT NULL CHECK(status IN ('pending','parsing','embedding','indexed','failed','deleted')),
  needs_ocr BOOLEAN NOT NULL DEFAULT FALSE,
  metadata JSONB NOT NULL DEFAULT '{}',
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  UNIQUE(project_id,content_hash,version)
);
CREATE TABLE memories (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id),
  project_id UUID NOT NULL REFERENCES projects(id),
  memory_type TEXT NOT NULL CHECK(memory_type IN ('preference','fact','procedure','episodic')),
  content JSONB NOT NULL, content_hash TEXT NOT NULL,
  importance REAL NOT NULL CHECK(importance BETWEEN 0 AND 1),
  source_message_id BIGINT REFERENCES messages(id),
  source_snapshot JSONB NOT NULL,
  embedding vector(1024),
  valid_from TIMESTAMPTZ NOT NULL DEFAULT now(), valid_to TIMESTAMPTZ,
  superseded_by UUID REFERENCES memories(id),
  CHECK(valid_to IS NULL OR valid_to>=valid_from)
);
CREATE UNIQUE INDEX idx_memories_active_hash ON memories(user_id,project_id,content_hash) WHERE valid_to IS NULL;
CREATE INDEX idx_memories_scope ON memories(user_id,project_id,memory_type) WHERE valid_to IS NULL;
CREATE INDEX idx_memories_vector ON memories USING hnsw(embedding vector_cosine_ops);
CREATE TABLE run_events (
  event_id BIGSERIAL PRIMARY KEY, run_id UUID NOT NULL REFERENCES agent_runs(id),
  event_type TEXT NOT NULL, payload JSONB NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX idx_events_run ON run_events(run_id,event_id);
CREATE TABLE audit_logs (
  id BIGSERIAL PRIMARY KEY, occurred_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  actor_id UUID, project_id UUID, run_id UUID, action_id UUID,
  event TEXT NOT NULL, decision TEXT NOT NULL,
  policy_version TEXT NOT NULL, detail JSONB NOT NULL
);
CREATE TABLE eval_runs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(), name TEXT NOT NULL UNIQUE,
  dataset_hash TEXT NOT NULL, fixture_hash TEXT NOT NULL, corpus_hash TEXT,
  environment_hash TEXT NOT NULL, git_commit TEXT NOT NULL,
  config JSONB NOT NULL, metrics JSONB NOT NULL, results_uri TEXT NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
```

这是实体拆分后的参考方案，项目不是“必须恰好 9 张表”。跨表一致性（run 的 user 与 session owner、tool_call 的 action/step 与 run 一致、approval_hash 与 action 一致）在 repository 短事务中校验，并用集成测试；需数据库强保证时增加复合唯一键/FK 或触发器。删除策略默认 RESTRICT，删除用户/项目先走显式清理/匿名化流程；audit 不 FK 到可删除实体。session/project 归属不因 UUID 难猜而省略权限检查。

Memory hash 使用规范化结构且包含类型，冲突更新加锁；语义去重不能仅靠唯一索引。source_snapshot 按隐私保留政策清理，不能以追溯为由永久保留已请求删除的个人内容。

files保存授权输入；certificates保存解析字段而不预设信任结论；crypto_keys与key_versions保存用途和版本，encrypted_blob_ref仅引用受控加密材料。artifacts绑定具体action、文件与key version，下载重新鉴权。证书检查的clock/trust_store/hostname/purpose及分项结果保存在版本化action结果中。nonce分配和唯一性由密码服务的持久化机制保证，metadata中的nonce字段本身不构成防复用控制。跨项目/用户及action引用一致性由短事务校验，必要时增加复合FK。

### 3.1 数据库权限

bootstrap_admin 仅初始化扩展与角色；migration_owner 拥有应用表，密钥只交迁移进程。app_user 仅有必要 CRUD，不可 UPDATE/DELETE/TRUNCATE audit_logs，也不是其 owner；query_reader 只 SELECT 经授权视图并设置默认事务只读；audit_writer 仅 INSERT audit_logs 和 USAGE sequence。app_user 读取审计也需获授权的视图。运行时不持有能切到 owner 的角色成员权限。

role 密码由环境/secret 注入，不在 DDL 中固定 `'from-env'` 字符串。外部密码动作与 DB 事务无法整体原子提交，不能声称 exactly-once；幂等下游、执行账本、reconciliation 明确覆盖边界。

迁移脚本对明确表名授权，不使用可能误含审计的`GRANT ALL ON ALL TABLES`。例如审计权限如下；角色先由bootstrap创建，应用不具备这些角色的管理权限：

```sql
REVOKE ALL ON audit_logs FROM PUBLIC, app_user, query_reader, audit_writer;
GRANT INSERT ON audit_logs TO audit_writer;
GRANT USAGE ON SEQUENCE audit_logs_id_seq TO audit_writer;
-- 审计读取另建经授权查询接口/视图；不要给app_user审计修改或TRUNCATE权限。
ALTER ROLE query_reader SET default_transaction_read_only = on;
ALTER ROLE query_reader SET statement_timeout = '5s';
```

默认只读事务可由普通连接改变，不作为唯一安全边界；query_reader还必须无写权限、无owner成员资格并仅获得需要的SELECT。project/user过滤由服务端可信上下文绑定，不接受模型传入的tenant_id，角色只读本身不能保证跨用户隔离。

### 3.2 六个验收查询

q1 Run→actions→tool_calls 列调用；q2 包含 failed/timeout/unknown；q3 查 canonical_arguments；q4 llm_calls 按 purpose 汇总模型/digest/token；q5 messages 按 sequence_no 排序；q6 失败排行参数化 start_time/end_time。结果空是有效结果，unknown 独立显示而不是计作成功。

## 4. 工具与唯一执行入口

```python
from enum import IntEnum
from typing import Any, Awaitable, Callable, Generic, TypeVar
from pydantic import BaseModel, Field, ConfigDict

T = TypeVar('T')
class RiskLevel(IntEnum):
    READ = 0
    RESTRICTED_COMPUTE = 1
    WRITE = 2
    EXECUTE = 3
    DESTRUCTIVE = 4

class ToolResult(BaseModel, Generic[T]):
    model_config = ConfigDict(extra='forbid')
    success: bool
    data: T | None = None
    error_type: str | None = None
    error: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)
    evidence_refs: list[dict[str, Any]] = Field(default_factory=list)

class ToolSpec(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, extra='forbid')
    tool_id: str
    version: str
    description: str
    input_schema: dict[str, Any]
    output_schema: dict[str, Any]
    timeout_s: float
    permission: str
    risk_level: RiskLevel
    read_only: bool
    idempotent: bool
    max_retries: int
    handler: Callable[..., Awaitable[ToolResult[Any]]]
```

字段运行时需要约束：timeout>0、retry>=0，max_retries>0 必须 idempotent=True 且由本地政策允许。read_only 不等于幂等（读操作也可能有费用/限额）；所有非只读操作max_retries=0；动作重传通过账本返回已有结果，不靠自动重试写操作。handler 的异常由 executor 捕获分类；取消不被吞掉；客户端超时不能被当作外部操作已停止。

canonical tools：inspect_certificate、verify_certificate、digest_file、verify_signature、get_key_metadata、encrypt_file、decrypt_file、sign_file、rotate_key、create_csr、issue_test_certificate、search_knowledge、query_database。MCP bridge将domain.inspect_certificate映射inspect_certificate、db.query_metadata映射query_database；新工具本地登记风险/权限之前只能发现，不能执行。

query_database输入为固定query_id与结构化参数，查询只返回获授权的密码资源元数据和执行记录，禁止模型传原始SQL。密码工具输入使用file_id/certificate_id/key_id与固定profile；真实路径、key version和秘密在服务端解析。加解密、签名、轮换、CSR与测试签发须绑定审批；默认禁止私钥导出、销毁和系统信任修改。各工具输入输出见[业务工具集合](06-CRYPTO-AGENT-SCOPE.md#4-建议的最小工具集合)。

执行器顺序：

1. 创建内部 attempt/correlation，规范化参数、schema 与业务校验。
2. 校验用户、项目、资源、工具 permission 与预算；记录拒绝。
3. 将用户/项目/工具版本/规范参数/资源版本/策略版本绑定到 action_hash。审批必须匹配该 hash。
4. 短事务写 action intent 和审批/lease 状态，再释放 DB 事务。
5. 经受控 runner 执行，校验输出大小与 schema，写结果和最终审计。
6. 失败/取消/拒绝使用 finally 或统一 outcome 路径记录；执行前安全审计无法持久化时 fail closed。执行后审计失败则保留结果/待补偿状态，不重新执行动作。

日志脱敏、截断与结果 blob 引用统一处理。MCP server 的 readOnlyHint 等注解不直接成为本地授权。[MCP tools 规范](https://modelcontextprotocol.io/specification/2025-06-18/server/tools)

## 5. 审批与动作恢复

审批请求展示规范参数、影响资源和实际版本。POST /runs/{id}/approve body：approval_id、action_hash、decision=approved/rejected；审批者身份来自鉴权。校验权限、有效期、pending 状态、未消费、action 未变。重复请求返回原决定；并发批准与拒绝只有一个成功。审批只授权特定动作，不能授权后续模型新提议。

approve提交决定后由持久化调度器发起一次动态`Command(resume=...)`；重复投递受动作状态/lease保护。测试步骤resume是幂等地驱动或核对恢复，不把pending审批当默认同意，也不再生成新的审批值。暂停后返回snapshot；拒绝决策使对应动作终止，不继续执行。

状态机：proposed → awaiting_approval → ready → executing → succeeded/failed/cancelled/unknown。拒绝/过期不执行。参数或资源/策略版本变更使旧审批失效，重新提议。L4 默认拒绝，例外需专门策略和更强确认。

crash matrix：

| 崩溃位置 | 恢复动作 |
|---|---|
| intent 未提交 | 不存在动作，不执行 |
| intent 已提交、未批准 | 恢复待审批，展示同一 hash |
| 已批准、未开始 | 原 approval + 幂等键领取 |
| 执行中 | 按外部 job_id/幂等键核对，等待或标 unknown |
| 外部已完成、完成记录未提交 | 核对已完成结果并补账；不可盲目重跑 |
| 已记录完成 | 返回已有 result_ref |

worker 在短事务 CAS claim，增加 fencing_token；结果只接受当前 owner/token，过期 worker 的结果不得覆盖新 owner。下游也须接受幂等键/fencing 才能更强地防重复；不支持时 unknown 需人工核对。取消请求协作取消并核对外部任务状态，不能立即伪报已停止。

Graph 动态审批使用 `Command(resume=decision)`，interrupt 节点重跑，之前不能创建无幂等检查的副作用。checkpointer 与动作账本分工：前者恢复控制流，后者处理副作用。版本不兼容的旧 checkpoint 明确拒绝或迁移，不直接用新 graph 执行。[LangGraph interrupts](https://docs.langchain.com/oss/python/langgraph/interrupts)

## 6. API 与 SSE

POST /chat 返回/关联 run_id，支持 stream=false JSON 和 stream=true SSE。GET /runs/{id} 返回 status、steps、actions、approval、final_answer、verifier；GET /runs/{id}/events?after={event_id} 支持恢复事件，POST /runs/{id}/cancel 显式取消。文件/会话/Memory/事件全部鉴权与资源校验。

所有事件 envelope：schema_version=1、event_id、run_id、timestamp、payload。event_id 为持久化序号，同一 Run 严格递增，允许全局间隙。响应中的 SSE id 与 envelope event_id 一致；客户端去重。事件和对应 DB 状态在同一短事务提交后才发送，避免收到事件却读不到状态。

唯一事件枚举：run_start、step、tool_call、tool_result、approval_required、token、verify、final、done、error。

```text
id: 101
event: approval_required
data: {"schema_version":1,"event_id":101,"run_id":"<uuid>","timestamp":"2026-10-10T00:00:00Z","payload":{"approval_id":"<uuid>","action_id":"<uuid>","action_hash":"<sha256>","tool_id":"encrypt_file","arguments":{"file_id":"<uuid>","key_id":"<uuid>","profile":"aes-gcm-v1"},"expires_at":"2026-10-10T00:15:00Z"}}

```

step 有 step_id/index/status；tool_call/tool_result 有 action_id/call_id/status；token 有 text/draft=true；verify 有 passed/checks/violations；final 有 answer/claims/citations/verification_status；done 有终态 status/计量；error 有 code/message/retryable/fatal。必要的 running→终态事件成对。token 是未验证草稿，final 才替换为最终答案。

fatal error 后持久化 done(failed/cancelled) 并结束；非致命 error 可后续恢复。审批中断时可以关闭传输但 Run 留 awaiting_approval，不能发 done(completed)。heartbeat 使用 SSE 注释，不作为业务事件。parser 按 SSE 空行组帧，处理 CRLF/多 data 行/UTF-8 跨块；发送器把 JSON 编码成单行。

disconnect_policy 在 Run 创建时保存：M2 简单同步任务默认 cancel；持久化审批/后台任务 detach。detach 流断开不取消动作；重连读取 events 和 snapshot，不重新 POST。保留窗口之外返回明确 event_history_expired 并提供 snapshot。Run events 不要求永久保留所有 token，过期状态须有快照和明确恢复规则。

## 7. 证据、引用与 Verifier

chunk payload：业务 chunk_id、point_id(UUID)、document_id/version、content_hash、project_id、ACL、page_start/page_end 或 section/char_start/char_end。检索权限在 dense/sparse 候选前执行，所有路线一致。Qdrant point_id 与业务引用 ID 分离。[Qdrant point IDs](https://qdrant.tech/documentation/manage-data/points/)

index manifest 记录 corpus/parse/chunk/embed/BM25/collection 版本及 hash；入库 staging 完成后发布 active manifest，旧 Run 固定读原版本。删除/权限撤销恢复前再校验，访问权限优先于复现；必要时返回 evidence_unavailable。

Citation={source_ref,document_version,chunk_id,locator,claim_ids}。locator 用 PDF 实际页区间、Markdown section/字符区间；不允许统一 ±1 页。存在性、定位正确性、语义支持性、事实覆盖分别报告；没有引用的非 RAG 闲聊/合理拒答为 N/A。

Claim={claim_id,subject,metric,value,unit,source_refs,derivation?}。派生量 derivation 记录输入 claim/ref、公式、计算工具版本、容差。Verifier 确定性核对绑定关系与单位，LLM/NLI 辅助语义判断。source 支持不证明真实世界数据正确，synthetic fixture 永远只证明工程行为。

VerifierReport={passed,checks,violations,unsupported_claim_rate?,duration_ms}，violations 含 check/type/severity/detail/found/expected?。未知正确答案时 expected 可以缺省，但必须给修复方向，不能编造期望值。必需项 skipped/unknown 不能当 pass；unsupported_claim_rate 无事实断言时 N/A。failed 后可限次重写或输出明确未验证结果，不能展示为已验证。

## 8. 配置与持续检查

`.env.example` 至少：APP_ENV、API_KEY_HEADER、OLLAMA_BASE_URL、模型名、LLM_THINK、LLM_NUM_CTX、LLM_TIMEOUT_S、DATABASE_URL(app_user)、QUERY_DATABASE_URL(query_reader)、AUDIT_DATABASE_URL(audit_writer)、MIGRATION_DATABASE_URL（仅迁移）、QDRANT_URL、项目空间/collection、可选 Redis/存储 URL、路径roots、密码Provider/keystore配置、受信任 MCP endpoints、EVAL_CONCURRENCY=1。

app API/worker 不加载 migration/bootstrap 密钥；不把完整 OLLAMA_* 环境或配置秘密写进日志。存储roots按knowledge/业务上传/artifact/keystore分别声明；每次核对用户与项目ACL。keystore只供受控密码服务加载，不能作为通用读取root；明文和私钥不写入messages、State、Trace或工具结果。

RetrievalConfig 包含 dense/sparse/backend/fusion/rrf_k/rerank/top_k/query_rewrite/filters，JSON 写入 agent_runs.runtime_config 和 eval_runs.config；prompt_version 只存 prompt 版本字符串。模型实际计量写 llm_calls。

CI 分层：普通 CI 执行 lint/typecheck/合同/schema/mock 场景；专用本机 GPU job 跑冻结集、固定环境和版本对比，按变更范围与发布节奏执行。安全确定性回归每次相关变更必跑，LLM 全量评测不假设托管 runner 有 GPU。阈值使用 pp 和相同 snapshot；报告完整 case failures，不能仅比总体平均。
