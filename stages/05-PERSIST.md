# 05. 持久化（40h）

> 完成这一段，你能做到：**一次 Run 从创建到结束的全过程都能在数据库里查到**——谁发起的、走了几步、调了哪些工具、花了多少 token、为什么停。刷新页面不丢，重启服务不丢。

04 段之前，Loop 的所有状态都在内存里，进程一退就没了。这一段把状态落到 PostgreSQL，并加一层 HTTP 接口让外部能创建和查询 Run。

---

## 在流程中的位置

[FLOW.md](../FLOW.md) 的 **⑨⑪**（intent / 结果持久化）和后续所有"查询"类能力的地基。

前置：04 段的 Trace（它就是 Step 表的数据来源）。解锁：06 段的账本与审批（都是这张表的扩展）。

```text
POST /chat → 先写 agent_runs(status=queued) → 执行 Loop
                    ↓ 每步
            agent_steps / tool_calls / llm_calls / run_events
                    ↓ 结束
            status=completed + final_answer
```

---

## 要写的代码

| 文件 | 职责 | 现状 |
|---|---|---|
| `packages/db/models.py` | ORM 模型 / 表定义 | ❌ 空桩 |
| `packages/db/session.py` | 引擎、会话、短事务 | ❌ 空桩 |
| `packages/db/migrations/` | Alembic 迁移 | ❌ 空目录 |
| `packages/db/repository/` | 读写接口 | ❌ 空目录 |
| `packages/db/queries/` | 六类固定查询 | ❌ 空目录 |
| `services/agent_api/main.py` | FastAPI 应用 | ❌ 空桩 |
| `services/agent_api/routers/` | 端点 | ❌ 空目录 |

依赖组：`uv sync --extra m1 --extra m2 --extra dev`（m2 = fastapi/uvicorn/sqlalchemy/asyncpg/alembic）。

---

## 核心概念

### 1. 五个 ID，各管一件事

| ID | 作用域 | 解决什么 | 不能代替 |
|---|---|---|---|
| `run_id` | 一次 Agent 任务 | 定位这次执行 | 幂等 |
| `client_request_id` | 用户 + 项目 | **幂等键**：同一请求重传返回原 Run | Run 主键 |
| `session_id` | 聊天容器 | 多轮会话归组 | 用户身份 |
| `action_id` | 一次外部动作 | 06 段的账本单元 | tool_call |
| `call_id` | 一次执行 attempt | 关联提议与实际执行 | action |

模型报文里的 `id` 字段**不承担任何业务标识**。身份来自鉴权上下文，不来自 body。

### 2. 短事务：绝不在事务里等外部世界

```text
❌ 错：BEGIN → 调模型 → 起子进程加密 → 写结果 → COMMIT
✅ 对：BEGIN → 写 intent → COMMIT → 调模型/子进程 → BEGIN → 写结果 → COMMIT
```

**为什么**：模型请求可能 120 秒，密码子进程可能 10 秒。握着数据库连接等这么久，连接池会被打满，锁也会阻塞别人。

**代价**：外部动作和 DB 写入之间有了时间窗。这正是 06 段要解决的"崩溃恢复"问题——**不要假装它不存在**。

### 3. "先写 Run 再执行"

```text
POST /chat
  → 写 agent_runs(status=queued)  ← 先落盘
  → 返回 run_id 或开始执行
```

**为什么**：如果先执行后落盘，模型刚开口服务就崩了，你连"刚才有人发起过一个任务"都不知道，用户只能凭空重发。先落盘，至少能查到 `status=running` 然后判定为 `unknown`。

### 4. 核心表（本段要建的）

```sql
CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  username TEXT NOT NULL UNIQUE,
  api_key_hash TEXT NOT NULL UNIQUE,
  role TEXT NOT NULL DEFAULT 'viewer'
       CHECK (role IN ('admin','engineer','viewer')),
  is_active BOOLEAN NOT NULL DEFAULT TRUE,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE projects (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name TEXT NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE project_members (
  project_id UUID NOT NULL REFERENCES projects(id),
  user_id    UUID NOT NULL REFERENCES users(id),
  role TEXT NOT NULL CHECK (role IN ('owner','editor','viewer')),
  PRIMARY KEY (project_id, user_id)
);

CREATE TABLE sessions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id    UUID NOT NULL REFERENCES users(id),
  project_id UUID NOT NULL REFERENCES projects(id),
  title TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  FOREIGN KEY (project_id, user_id) REFERENCES project_members(project_id, user_id)
);

CREATE TABLE files (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  project_id UUID NOT NULL REFERENCES projects(id),
  owner_id   UUID NOT NULL REFERENCES users(id),
  original_name TEXT NOT NULL,
  storage_ref   TEXT NOT NULL UNIQUE,     -- 服务端路径，绝不出传给模型
  content_hash  TEXT NOT NULL,
  size_bytes BIGINT NOT NULL CHECK (size_bytes >= 0),
  media_type TEXT NOT NULL,
  version TEXT NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  FOREIGN KEY (project_id, owner_id) REFERENCES project_members(project_id, user_id)
);

CREATE TABLE agent_runs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id    UUID NOT NULL REFERENCES users(id),
  session_id UUID NOT NULL REFERENCES sessions(id),
  client_request_id TEXT NOT NULL,
  graph_version  TEXT NOT NULL,
  prompt_version TEXT NOT NULL,
  runtime_config JSONB NOT NULL,
  disconnect_policy TEXT NOT NULL CHECK (disconnect_policy IN ('cancel','detach')),
  status TEXT NOT NULL CHECK (status IN (
    'queued','running','awaiting_approval','reconciling',
    'completed','failed','cancelled')),
  final_answer    JSONB,
  verifier_report JSONB,
  error JSONB,
  created_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
  finished_at TIMESTAMPTZ,
  UNIQUE (user_id, client_request_id)      -- 幂等约束在这一行
);
CREATE INDEX idx_runs_session ON agent_runs(session_id, created_at DESC);

CREATE TABLE messages (
  id BIGSERIAL PRIMARY KEY,
  session_id UUID NOT NULL REFERENCES sessions(id),
  run_id     UUID REFERENCES agent_runs(id),
  role TEXT NOT NULL CHECK (role IN ('system','user','assistant','tool')),
  content JSONB NOT NULL,
  sequence_no BIGINT NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  UNIQUE (session_id, sequence_no)
);

CREATE TABLE agent_steps (
  id BIGSERIAL PRIMARY KEY,
  run_id UUID NOT NULL REFERENCES agent_runs(id),
  step_index INT NOT NULL CHECK (step_index >= 0),
  attempt INT NOT NULL DEFAULT 1 CHECK (attempt >= 1),
  step_type TEXT NOT NULL,
  status TEXT NOT NULL CHECK (status IN ('running','ok','failed','skipped','cancelled')),
  input_ref JSONB, output_ref JSONB,
  started_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  finished_at TIMESTAMPTZ,
  UNIQUE (run_id, step_index, attempt)
);

CREATE TABLE tool_calls (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  run_id UUID NOT NULL REFERENCES agent_runs(id),
  step_id BIGINT REFERENCES agent_steps(id),
  attempt INT NOT NULL CHECK (attempt >= 1),
  source TEXT NOT NULL CHECK (source IN ('builtin','mcp')),
  mcp_server TEXT,
  status TEXT NOT NULL CHECK (status IN (
    'running','ok','failed','denied','timeout','cancelled','unknown')),
  result_ref JSONB, error JSONB,
  started_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
  finished_at TIMESTAMPTZ
);

CREATE TABLE llm_calls (
  id BIGSERIAL PRIMARY KEY,
  run_id  UUID NOT NULL REFERENCES agent_runs(id),
  step_id BIGINT REFERENCES agent_steps(id),
  purpose TEXT NOT NULL CHECK (purpose IN (
    'route','plan','generate','rewrite','memory','verify','judge')),
  model_name   TEXT NOT NULL,
  model_digest TEXT NOT NULL,
  config JSONB NOT NULL,
  prompt_tokens     INT CHECK (prompt_tokens >= 0),
  completion_tokens INT CHECK (completion_tokens >= 0),
  load_ms INT CHECK (load_ms >= 0),
  inference_ms INT CHECK (inference_ms >= 0),
  started_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE audit_logs (
  id BIGSERIAL PRIMARY KEY,
  occurred_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  actor_id UUID, project_id UUID, run_id UUID, action_id UUID,
  event TEXT NOT NULL,
  decision TEXT NOT NULL,
  policy_version TEXT NOT NULL,
  detail JSONB NOT NULL
);
```

**`llm_calls.config` 必须存运行时配置**（模型名、温度、num_ctx、think）。否则两个实验的数字无法归因。

**`llm_calls` 的 token 字段来自 API 真实返回**，不是估算历史文本长度。

后面阶段的表（本段不建）：`06` 要 `actions` / `approvals` / `artifacts` / `crypto_keys` / `key_versions`；`08` 要 `documents` / `memories`；`10` 要 `eval_runs`。

### 5. 数据库角色要分开

| 角色 | 权限 |
|---|---|
| `bootstrap_admin` | 建扩展、建库。**应用不使用它** |
| `migration_owner` | 拥有表，跑 Alembic |
| `app_user` | 读写业务表。**不能 UPDATE/DELETE `audit_logs`** |
| `query_reader` | 只读视图 + `default_transaction_read_only=on` + `statement_timeout='5s'` |
| `audit_writer` | 只 `INSERT` + `USAGE` sequence |

```sql
REVOKE ALL ON audit_logs FROM PUBLIC, app_user, query_reader, audit_writer;
GRANT INSERT ON audit_logs TO audit_writer;
GRANT USAGE ON SEQUENCE audit_logs_id_seq TO audit_writer;
ALTER ROLE query_reader SET default_transaction_read_only = on;
ALTER ROLE query_reader SET statement_timeout = '5s';
```

"只读角色"不等于隔离：它必须**没有写权限、不是表 owner、只拿到必要的 SELECT**。光设 `default_transaction_read_only` 只要拿普通连接就能改回来。

### 6. 六类固定查询

| # | 查什么 | 要点 |
|---|---|---|
| q1 | Run → actions → tool_calls | 一次调用全链路 |
| q2 | 失败的调用 | 含 `failed`/`timeout`/`denied`/`unknown` |
| q3 | 规范参数 | `canonical_arguments` 原样 |
| q4 | token 汇总 | 按 `purpose` 分组，带 model/digest |
| q5 | 会话消息 | 按 `sequence_no` 排序 |
| q6 | 失败工具排行 | **时间窗口必须参数化** |

q6 至少测 7 天和 30 天两个窗口。**写死时间窗口的查询等于没做**。

空结果是有效结果。`unknown` 要单独显示，不能算进"成功"。

---

## 分步实现

### 步骤 1 起 PostgreSQL（单服务，先不上 Compose）

```bash
docker run -d --name agent-pg \
  -e POSTGRES_PASSWORD=$(openssl rand -hex 16) \
  -e POSTGRES_DB=agentdev \
  -p 127.0.0.1:5432:5432 \
  -v agent-pg-data:/var/lib/postgresql/data \
  postgres:16
```

绑 `127.0.0.1` 而不是 `0.0.0.0`：数据库不需要被 Windows 访问。

验证：重启容器后数据还在（`docker restart agent-pg`）。

### 步骤 2 Alembic 迁移

要求：

- **空库初始化**能一次成功
- **已升级的库重复 upgrade 不重建表**
- 迁移失败能定位，用前向修复而不是回滚

```bash
alembic upgrade head
alembic upgrade head          # 第二次必须是 no-op
```

### 步骤 3 短事务边界

```python
# 错
async with session.begin():
    run = await create_run(...)
    result = await agent.run(...)      # 120 秒！
    await save_result(run, result)

# 对
async with session.begin():
    run_id = await create_run(...)     # 立刻提交
result = await agent.run(...)
async with session.begin():
    await save_result(run_id, result)
```

**不要跨**：模型请求、人工审批等待、密码子进程。

### 步骤 4 加 API（先 curl，后页面）

最小端点：

```text
GET  /health/live         进程存活（不查外部依赖）
GET  /health/ready        依赖可用（模型/DB/迁移），不可用返回 503
POST /sessions            建会话
POST /chat                建 Run 并执行
GET  /runs/{id}           查 Run 快照
POST /files               上传（先校验再发布）
```

**`live` 和 `ready` 必须分开**：`live` 只证明进程没死；`ready` 证明能干活。容器启动不等于 ready。

`POST /chat` 的最小请求（可直接当 fixture）：

```json
{
  "project_id": "11111111-1111-4111-8111-111111111111",
  "session_id": "22222222-2222-4222-8222-222222222222",
  "client_request_id": "33333333-3333-4333-8333-333333333333",
  "message": "计算这个教学文件的 SHA-256 摘要，并说明实际使用的工具。",
  "resource_ids": [{"type": "file", "id": "44444444-4444-4444-8444-444444444444"}],
  "stream": false
}
```

错误码分工：

| 码 | 含义 |
|---|---|
| 422 | 参数错误 |
| 401 | 未认证 |
| 403 | 已认证但无权限 |
| 404 | 资源不可见/不存在 |
| 409 | 请求 ID 或状态冲突 |
| 413 | 超限 |
| 503 | 依赖不可用 |

错误体固定 `{"error": {"code","message","retryable"}, "request_id"}`。**流开始之后不能再改 HTTP 状态码。**

### 步骤 5 幂等

同一 `(user_id, client_request_id)` 重传：

- 请求内容相同 → **返回原 Run**，不新建
- 请求内容不同 → `409 request_conflict`，不静默复用

记录请求的规范化 hash 才能判断"是否相同"。

### 步骤 6 六类查询 + 参数化窗口

每个查询都要有真实断言，包括：

- 空结果 → 返回空列表，**不是错误**
- 越权访问 → 404（不是 403，避免探测存在性）
- 时间窗口切换 → 结果集真的变

---

## 常见坑

1. **事务里调模型。** 连接池打满，表现为"莫名其妙全部超时"。
2. **先执行后落盘。** 崩了就完全无法追溯。
3. **合并 401 和 403。** 一个是"你没登录"，一个是"你登录了但没权限"，前者能重试，后者不能。
4. **越权返回 403。** 会让攻击者据此枚举哪些资源存在。用 404。
5. **`storage_ref` 回传给前端。** 那是服务端真实路径，泄露目录结构。
6. **忘了 `UNIQUE (user_id, client_request_id)`。** 并发重传会创建两个 Run，两个都执行。
7. **把 `unknown` 算进成功。** 它恰恰是"不知道做没做"。
8. **只测 7 天窗口。** 30 天的查询路径从没被执行过。
9. **`default_transaction_read_only` 当成安全边界。** 普通连接就能改。
10. **启动模块路径写错。** 必须是真实存在的可导入包，如 `services.agent_api.main:app`。

---

## 自检问题

1. `session_id` / `run_id` / `client_request_id` 各解决什么问题？用一次提问、一次重传、一次刷新分别说明。
2. 为什么先保存 Run 再执行？如果反过来，刷新页面时你还能查到什么？
3. 事务为什么不能跨整个模型请求？画出你实际的短事务边界。
4. HTTP 200、Run `completed`、工具 `ok` 是同一个状态吗？举一个三者不一致的例子。
5. 你的 q6 怎么参数化时间窗口？7 天和 30 天的结果差多少？

---

## 本人记录

```text
日期：
实际工时：
迁移命令与输出（含重复 upgrade）：
重启验证过程：
六类查询各一条真实结果：
幂等重传的两次响应差异：
还没理解的：
```
