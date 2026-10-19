# 08. 知识能力（105h）

> 完成这一段，你能做到：**Agent 引用一段资料时，你能点回原文、说清版本、证明它有权看到；说错时能被 Verifier 抓到；用户改口后旧记忆不再生效。**

这一段最长（105h），因为它包含三个独立子系统：检索、记忆、事件流。它们各自都能单独验收。

---

## 在流程中的位置

[FLOW.md](../FLOW.md) 的 ②（Context 来源）和第 12 节数据流里 `Knowledge` / `Memory` / SSE 三条支路。

前置：07 段。解锁：09 段的前端（它消费 SSE 和引用）。

```text
文档 → 解析 → 切块 → 向量/词项索引 → 授权检索 → 证据进 Context → 回答带引用
用户偏好 → 提取 → 去重 → 纠正/删除 → 跨会话注入
Run 事件 → 持久化 → SSE 推送 → 前端重连
```

---

## 要写的代码

| 文件 | 职责 | 现状 |
|---|---|---|
| `pipelines/ingest/` | 解析、切块、索引发布 | ❌ 空目录 |
| `pipelines/retrieval/` | 稠密/稀疏检索、融合、重排 | ❌ 空目录 |
| `pipelines/citation/` | 来源、版本、定位 | ❌ 空目录 |
| `packages/db/models.py` | `documents` / `memories` | ❌ 需扩展 |
| `services/agent_api/routers/` | `/knowledge/*`、`/memories/*`、`/runs/{id}/events` | ❌ 需新增 |
| `verifier/checks/` | Claim/引用/事实检查 | ❌ 空目录 |

依赖组：新增 `m3`（qdrant-client / pymupdf / rank-bm25 / jieba）和 Ollama 的 `bge-m3`。

---

## 核心概念

### 1. 三个 ID 不能混

| ID | 是什么 | 用途 |
|---|---|---|
| `chunk_id` | **业务**片段标识 | 引用、展示 |
| `point_id` | 向量库的 **UUID** | 检索 |
| `content_hash` | 内容指纹 | 去重、版本 |

**不要把任意 `chunk_id` 字符串当 `point_id` 用。** Qdrant 的 point 标识有自己的类型要求，混用后改内容、改版本都会出问题。

`document_version` 是文档级版本：**旧 Run 固定读原版本**，索引更新不影响已完成的引用。

### 2. 授权必须在检索之前

```text
❌ 检索 top-50 → 过滤掉无权 → 返回 3 条
✅ 检索范围内只有权 → top-K
```

第一种做法的问题：**top-K 的 K 被无权内容占掉了**，用户本来能拿到 3 条，实际返回 0 条。

第二点：ACL 过滤要在**所有路线**上做——dense、sparse、rerank 之后都不能漏。rerank 不能扩大权限。

### 3. `staging → active` 发布

```text
整批解析+切块+embedding 全部成功
    ↓
写 manifest（corpus/parse/chunk/embed/BM25/collection 各版本 + hash）
    ↓
一次性切换 active
```

**失败不进 active**：半成品索引会让检索返回不存在的片段。中断后旧版本仍然可用。

重复入库不重复；更新和删除要同步到所有索引。

### 4. Citation 的三层检查

```python
Citation = {
    "source_ref", "document_version", "chunk_id", "locator", "claim_ids"
}
```

三层要分别报，不能合并：

| 层 | 检查什么 | 失败含义 |
|---|---|---|
| 存在性 | 片段还在、版本对得上 | 引用编造的 |
| 定位正确性 | `locator` 指向那段原文 | 引对了但页码错 |
| 支持性 | 这段原文真的支持那个结论 | 引对了但推不出 |

**引用存在 ≠ 位置正确 ≠ 支持结论。**

`locator` 规则：

- PDF：**真实页区间** `page_start/page_end`，不允许统一 ±1 页
- Markdown / TXT：`section` + `char_start/char_end`，**禁止编造页码**

### 5. 四种 Context 来源（04 段给过，这里补齐读取时机）

| 来源 | 何时读 | 何时失效 |
|---|---|---|
| History | 每轮组装 | 超出预算截断 |
| Run State | 恢复时 | Run 结束 |
| Memory | 每轮按 user/project | 用户改口/删除 |
| Knowledge | 需要事实时 | 索引版本变化、撤权 |

**不能用 History 里的旧回答断言资源现状**，也不能用 Knowledge 证明"当前证书可信或密钥有效"。

### 6. Memory 的四件事

```text
① 提取   留类型/来源/时间。不要用长度决定是否有效（"记住报告用中文"很短但重要）
② 去重   两层：content_hash 唯一 + 语义相似
③ 纠正   事务里失效旧值、写新值（valid_to / superseded_by）
④ 删除   删除后可验证不再被注入
```

注入时的硬限制：**阈值 + 最多 5 条**。20 条无关问题不能形成 20 条 Memory。

隔离：按 `user_id` + `project_id`。跨用户、跨项目**不共享**。并发不重复插入（靠唯一索引）。

投毒防护：文档里的指令**不能**变成用户偏好。"以后不用审批"这种话不能让审批消失。

### 7. SSE 的十个事件

```text
run_start  step  tool_call  tool_result  approval_required
token  verify  final  done  error
```

统一 envelope：

```json
{"schema_version": 1, "event_id": 101, "run_id": "...", "timestamp": "...", "payload": {}}
```

规则：

- `event_id` 是**持久化序号**，同一 Run 严格递增（允许全局有间隙）
- **状态和事件在同一短事务提交后才发送**。否则客户端收到事件却查不到状态
- SSE 的 `id:` 与 envelope 的 `event_id` 一致，客户端据此去重
- `heartbeat` 是注释行，**不占业务 event_id**

重连：

```text
保留 run_id + 最后应用的 event_id
  → GET snapshot（核对权限/终态/pending）
  → GET events?after={event_id}
  → 去重应用，保持同一 Run
```

**不要重新 POST 原任务。** 那会创建第二个 Run。

超过保留窗口返回 `410 event_history_expired` + snapshot，**不能悄悄重跑**。

### 8. 指标与分母

```text
Hit@K             = mean_q[ |R_K(q) ∩ G(q)| > 0 ]
Recall@K          = mean_q[ |R_K(q) ∩ G(q)| / |G(q)| ]     q ∈ Q+
MRR@K             = mean_q[ 1 / 首个相关 rank ]             无命中记 0
EvidenceCoverage  = mean_q[ 已覆盖必要事实槽数 / 必要事实槽数 ]
```

**分母是最容易作弊的地方**：

- `Q-`（无答案题）**不进** Recall/MRR 的分母
- 无答案单独报 **Correct Refusal Rate** / **False Refusal Rate**，各带 n
- 空分母记 **N/A**，不记 0
- 真实有答案但检索失败，**仍是正样本失败**，不能改成 `no_answer`

### 9. 四组消融

```text
① dense only
② sparse (BM25) only
③ dense + sparse + RRF
④ ③ + rerank
```

固定：corpus、chunk、query、其他 config。
单独开关：query rewrite（**不混进主四组**）。

RRF 只按**排名**融合，不直接混加不同来源的原始分数。Hybrid 不赢也要分析——那本身就是结论。

### 10. Verifier 的 Claim

```python
Claim = {
    "claim_id", "subject", "metric", "value", "unit", "source_refs", "derivation"
}
VerifierReport = {
    "passed", "checks", "violations", "unsupported_claim_rate", "duration_ms"
}
```

三类检查：

- **确定性**：实体、数值、单位、绑定关系（必须优先）
- **引用**：三层检查
- **语义**：LLM/NLI 辅助，但不能替代确定性检查

**必须读真实工具最终状态和 Citation，不能只在回答文本里搜数字。**

必需项 `unknown` / `skipped` **不能当 pass**。

---

## 分步实现

### 步骤 1 解析与定位

准备三种格式的真实样本：PDF（含至少一页扫描件）、Markdown、TXT。

要求：

- 原文可核对
- 扫描页标 `needs_ocr`，**不产生假正文**
- MD/TXT 用 `section`/`char`，PDF 用真实页区间

### 步骤 2 切块与索引

chunk 元数据至少保留：

```text
document_id, version, chunk_id, content_hash, locator,
project_id, ACL
```

Qdrant payload 加 `point_id`（UUID）。**同一内容不同项目不做全局去重**——那会泄露"某内容存在"这件事。

### 步骤 3 staging → active

```text
解析 → 切块 → embedding → 写 collection(staging)
  → 全部成功 → 写 manifest → 切 active
```

失败验证：中途失败，active 仍是旧版本，检索仍可用。

### 步骤 4 检索工具与引用

```text
query → 授权范围内候选 → (dense | sparse | 融合 | rerank) → top-K
  → 每条带 chunk_id/version/locator → 进 Context
```

验证：两个用户问同一问题，结果集无交集泄漏。

### 步骤 5 四组消融

固定一切，只改一组。每组记录：质量指标 + 耗时 + 失败类型分布。

至少 50 个经审定的 RAG 题（20 个可先做中间练习）。

### 步骤 6 Memory

```sql
CREATE TABLE memories (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id    UUID NOT NULL REFERENCES users(id),
  project_id UUID NOT NULL REFERENCES projects(id),
  memory_type TEXT NOT NULL CHECK (memory_type IN ('preference','fact','procedure','episodic')),
  content JSONB NOT NULL,
  content_hash TEXT NOT NULL,
  importance REAL NOT NULL CHECK (importance BETWEEN 0 AND 1),
  source_message_id BIGINT REFERENCES messages(id),
  source_snapshot JSONB NOT NULL,
  embedding vector(1024),
  valid_from TIMESTAMPTZ NOT NULL DEFAULT now(),
  valid_to   TIMESTAMPTZ,
  superseded_by UUID REFERENCES memories(id),
  CHECK (valid_to IS NULL OR valid_to >= valid_from)
);
CREATE UNIQUE INDEX idx_memories_active_hash
  ON memories(user_id, project_id, content_hash) WHERE valid_to IS NULL;
CREATE INDEX idx_memories_scope
  ON memories(user_id, project_id, memory_type) WHERE valid_to IS NULL;
CREATE INDEX idx_memories_vector
  ON memories USING hnsw (embedding vector_cosine_ops);
```

`PATCH`/`DELETE` 用 `expected_content_hash` 做乐观检查，冲突返回 409。**`content_hash` 不是授权凭据**——它只防并发覆盖。

### 步骤 7 SSE

```sql
CREATE TABLE run_events (
  event_id BIGSERIAL PRIMARY KEY,
  run_id UUID NOT NULL REFERENCES agent_runs(id),
  event_type TEXT NOT NULL,
  payload JSONB NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX idx_events_run ON run_events(run_id, event_id);
```

发送逻辑：**写 event + 改状态 → 同一事务提交 → 才推给客户端**。

示例帧：

```text
id: 101
event: approval_required
data: {"schema_version":1,"event_id":101,"run_id":"<uuid>","timestamp":"2026-10-10T00:00:00Z","payload":{"approval_id":"<uuid>","action_id":"<uuid>","action_hash":"<sha256>","tool_id":"encrypt_file","arguments":{"file_id":"<uuid>","key_id":"<uuid>","profile":"aes-gcm-v1"},"expires_at":"2026-10-10T00:15:00Z"}}
```

前端用 `fetch` 而不是原生 `EventSource`——后者不支持自定义鉴权头。

### 步骤 8 Verifier 双集

≥20 个已知正确 + ≥20 个已知错误。报 TPR / FPR，附样本量。

错误集要覆盖：实体错绑、单位错、派生值错、引用过期、引用不支持结论、未检查项当已通过。

---

## 常见坑

1. **先检索再过滤 ACL。** 无权内容占掉了 top-K 名额。
2. **给 MD/TXT 编页码。** 或者统一放宽 ±1 页。
3. **扫描页产生假正文。** 应该标 `needs_ocr` 并返回明确限制。
4. **把 `Q-` 放进 Recall 分母。** 指标会好看但没意义。
5. **检索失败改标成 `no_answer`。** 那是改标签自欺。
6. **top-K 没命中就断定"资料里没有"。** 必须回原文核对。
7. **半成品索引进 active。** 检索会返回不存在的片段。
8. **跨项目全局去重。** 泄露"这个内容存在"。
9. **事件先发后落库。** 客户端收到事件却查不到状态。
10. **重连时重新 POST。** 创建第二个 Run。
11. **heartbeat 占了 event_id。** 游标计算全错。
12. **Memory 用长度筛重要性。** 短而关键的偏好会丢。
13. **把文档里的指令写进 Memory。** 等于让文档改系统规则。
14. **只在回答里搜数字做 Verifier。** 必须读工具真实状态。
15. **`unknown` 当 pass。** 未检查 ≠ 通过。

---

## 自检问题

1. `chunk_id`、`document_version`、`content_hash`、`point_id` 各是什么？给一个真实片段到原文/版本/索引记录的映射。
2. ACL 过滤应该在哪一步？为什么放在 rerank 之后是错的？
3. Dense、BM25、RRF、rerank 各改变哪一部分？Hit@K / Recall@K / MRR@K 的分母分别是什么？无答案题怎么处理？
4. `event_id`、`run_id`、snapshot、`after` 游标怎么一起恢复页面？给出一次真实断线重连记录。
5. History / Run State / Memory / Knowledge 各在何时读取、何时失效？举一个"不能靠旧聊天断言现状"的例子。

---

## 本人记录

```text
日期：
实际工时：
入库 → 检索 → 引用的完整链路（贴一次真实结果）：
四组消融的数字表：
Memory 改口与删除的验证过程：
SSE 断线重连的 event_id 序列：
Verifier 双集的 TPR / FPR：
还没理解的：
```
