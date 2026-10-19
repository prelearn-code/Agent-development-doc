# 10. 评测与交付（133h）

> 完成这一段，你能做到：**用固定数据证明"这一版比上一版好"或"没有变差"，并且能从一台干净机器把整个系统重新跑起来。**

前九段产出一个能用的系统。这一段证明它**可靠**，并且证明你的结论**不是挑出来的**。

---

## 在流程中的位置

[FLOW.md](../FLOW.md) 之外——这一段不是新增链路，而是给整条链路加**度量**和**可重建性**。

前置：09 段。出口：整个项目完成。

---

## 要写的代码

| 文件 | 职责 | 现状 |
|---|---|---|
| `eval/runner.py` | Scenario Runner | ❌ 空桩 |
| `eval/datasets/` | 固定数据集 | ❌ 空目录 |
| `infra/dockerfiles/` | 镜像 | ❌ 空目录 |
| `infra/init/` | 首次初始化 | ❌ 空目录 |
| `scripts/` | 部署与备份脚本 | ⚠️ 只有 selftest |

---

## 核心概念

### 1. 先补前面的欠账

这一段开始前，先回头补齐前九段登记为"留到后面"的项：

| 来自 | 补什么 |
|---|---|
| 03 | 完整授权回归 |
| 05 | 全部六类查询 + 索引/事务复核 |
| 06 | 密钥轮换、CSR/测试签发、≥50 工具用例 |
| 07 | 三职责 Server（fs/db/domain）、Resource/Prompt、两类刷新 |
| 08 | 完整 Verifier、完整威胁模型与安全回归 |

**这些不做完，"交付"没有意义。**

### 2. 成功谓词要分层

一条用例的"成功"不是一句话，是一组条件：

| 字段 | 判定范围 |
|---|---|
| `allowed_tool_plans` | 允许的工具序列（二维，任一合法即可；空计划写 `[[]]`） |
| `gold_calls` | `tool_id` + occurrence 绑定的参数约束 |
| `must_call_tools` / `must_not_call_tools` | **提议层**（模型有没有提） |
| `must_execute_tools` / `must_not_execute_tools` | **执行层**（真的执行了没有） |
| `expected_values` | subject / metric / value / unit / atol / rtol / source_ref |
| `state_assertions` | 真实资源状态、执行计数、审批、恢复、Memory |
| `final_answer_all_of` / `any_of` / `none_of` | 回答文本的 AND / OR / 禁止 |
| `expected_behavior` | `answer` / `refuse` / `clarify` |

**提议层和执行层必须分开**：模型提了但被拒绝，和模型根本没提，是两种完全不同的失败。

几条不能单独当证据的：

- `min_citations > 0` 单独不能证明答案正确
- `verifier_passed = true` 单独不能证明任务完成
- 关键词匹配不能当主判据

### 3. 数据集 schema

```json
{
  "id": "tool-003",
  "schema_version": 3,
  "status": "draft | ready | frozen",
  "split": "dev | test",
  "group_id": "...",
  "category": "intent|rag|tool|database|workflow|memory|security|complex",
  "difficulty": "...",
  "question": "...",
  "answerability": "answerable | unanswerable",
  "expected_behavior": "answer|refuse|clarify",
  "fixture_refs": [],
  "allowed_tool_plans": [],
  "gold_calls": [],
  "success_criteria": {},
  "provenance": {"reviewer_kind": "human", "verified_by": "...", "reviewed_at": "..."}
}
```

未知字段**拒绝**。字段或工具范围变了要升 `schema_version` 并同步 validator 与 registry。

初始状态一律 `schema_version=3, status=draft, split=dev`。教学材料标 `synthetic`。

### 4. gold 的三条铁律

```text
① 合成问题只产生 draft，不能直接 ready
② 20% 抽检只决定"整批是否返工"，不能把剩下 80% 标成人工验证
③ status=ready 只说明内容审过，不代表应用测试通过
```

`ready` / `frozen` 的硬要求：`provenance.reviewer_kind = human`、有实际 `verified_by`、有 ISO 格式 `reviewed_at`。

**绝对禁止**：

- 悄悄改 gold 去适配模型结果
- 为了通过而放宽断言
- 改了 gold 不重跑 baseline

### 5. heldout 隔离

```text
近义变体、同源模板、同场景组 → 整体进同一个 split
```

做不到就**加独立文档组**，或全部用于 dev 再另备 test。不能"悄悄取消防泄漏规则"。

`test` 不参与调参：prompt、router 阈值、top-K 都只能用 dev 选。

### 6. 统计：pp 和样本量

```text
40 题的测试集：一题 = 2.5pp
180 题的测试集：一题 ≈ 0.56pp
```

所以"提升 2pp"在 40 题上就是**不到一题**。报告必须给：

- 逐次结果（每配置至少 3 次）
- 均值、方差、区间
- `case-level` 回归
- 样本量 n

**不许只挑最好一次**。多数投票要单列为一种策略。

### 7. 六个核心指标

| 指标 | 分母 / 口径 |
|---|---|
| Intent Accuracy | 有 `gold_intent` 的适用样本 |
| Tool Exact Match | 与任一 `allowed_tool_plans` **完全一致**（顺序、重复敏感） |
| Tool Set Match | 工具集合一致（不证明次数/顺序） |
| Joint Call Accuracy | 工具 + 次序 + 参数全对 |
| Task Success | 全部显式谓词 + 安全必要条件成立 |
| Unauthorized Action Rate | **实际执行**越权的场景数 / 有效安全场景数，**必须为 0** |

延迟口径：`p50/p95/max` 是基本报告，`p99` 小样本不稳（须带 n）。超时和失败也记耗时。并行分段之和可能超过 wall clock，要注明。

token 口径：从 `llm_calls` 的**实际返回**聚合，区分 controller / rewrite / memory / verifier / judge。**Judge 的 token 不进在线成本。** 不用 tiktoken 估计冒充实测。

### 8. Scenario Runner

```python
run_dataset(dataset, config, experiment_id, repetition)
  namespace = f"{experiment_id}/{repetition}/{case.id}"
  env = fixture_manager.create(case)
  try:
      result = scenario_runner.run(case) or agent.run(case)
      evaluate_case(case, result)
  finally:
      fixture_manager.cleanup(env)
```

每个 case 的 namespace 必须隔离：用户、资源、session、文件、索引、Memory。`cleanup` **只清自己的 namespace**。

场景步骤：`turn` / `approval` / `inject_fault` / `restart` / `resume` / `cancel` / `assert_state`。

**只有 `turn` 是真正发给模型的用户消息。** approval、fault、restart 是 Runner 带外驱动的控制动作，**不能当普通问题发给模型**。

### 9. readiness 和干净复现

`live` ≠ `ready`。ready 要检查真实业务依赖：

| 状态 | 含义 |
|---|---|
| `enabled` | 能力启用，依赖必须可用 |
| `disabled` | 能力未启用，不当依赖 |
| `unavailable` | 承诺了但缺库 → **必须拒绝调用** |

依赖不可用时 readiness **不能报成功**。

干净目录十步：

```text
① 定位    核对四仓库 remote/commit，选教学实例
② 配置    从样例生成本地配置，注入测试凭据
③ 依赖    按 lock 恢复 Python/前端
④ 模型    只装当前阶段模型，核对 digest
⑤ 存储    启动 DB/向量库，迁移，初始化
⑥ 应用    启动 API + Web
⑦ smoke   认证 + 只读工具 + 一次完整业务
⑧ 浏览器  Windows 打开 Ubuntu 入口
⑨ 重启    停启后查 pending/产物/历史
⑩ 备份恢复 独立实例恢复一份一致备份
```

**先写实际命令，再由另一台机器照着跑。** 只有你自己跑得通不算。

### 10. 备份恢复的六类数据

```text
DB / 审计 / 审批 / 账本 / checkpoint
上传文件 / artifact
corpus / parse / index manifest
keystore 加密 blob
解锁材料 / 恢复秘密
配置 / 版本清单
```

流程：

```text
① 维护窗口：暂停新写 → 等可确认动作结束 → 记录 unknown
② 取一致版本（加密 blob / DB / 文件要有共同快照清单）
③ 恢复顺序：配置 → 服务/版本 → 迁移 → DB+材料+文件 → 核对 hash/ACL
   → 查 pending/unknown → 只读 smoke → 受控教学动作 → 最后开写
④ 旧批准若资源或 policy 版本不匹配 → 失效
```

**只恢复 DB 不等于恢复密钥能力。** 没有 keystore blob，密钥就是废的。

必须做的四个实验：

1. 重启后数据不丢
2. 从备份恢复一个已完成 artifact
3. 从备份恢复一个待审批 Run
4. 缺 key blob 时**正确拒绝**解密，而不是编造成功

---

## 分步实现

### 步骤 1 补齐前九段欠账

按上表逐项做，每项都要有真实验证。

### 步骤 2 建数据集

```text
先 100 条：Intent 10 / RAG 15 / Tool 15 / Database 10
          / Workflow 15 / Memory 10 / Security 15 / Complex 10
完整 180 条：20 / 30 / 25 / 20 / 20 / 15 / 25 / 25
```

全部 `draft` 起步。逐条审定后升 `ready`，冻结后升 `frozen`。

### 步骤 3 写 Runner

先做**单条**：建 namespace → 请求 → 记录 → 断言 → cleanup。每条 case 只能有一个结果。

再做场景版：加 `approval` / `inject_fault` / `restart` / `resume` / `cancel` / `assert_state`。

### 步骤 4 三个必做实验

```text
① RAG 四组消融     固定语料/切分/问题，rewrite 单独开关
② 4B/9B ± router   固定候选工具/上下文/think/Judge/fixture
③ Verifier         已知错误 + 已知正确双集，报 TPR/FPR
```

Router 要把两类错**分开计量**：

- **路由错**：正确工具没进候选池
- **选工具错**：正确工具在候选池里但模型选了别的

合并报告会掩盖真实问题。

### 步骤 5 比较与 CI

```text
普通 CI：lint / typecheck / 合同 / mock 场景 / 确定性安全回归
GPU job：frozen 数据集 + 固定环境 + 版本对比
```

compare 检查：

- 全部 hash 相同（dataset / fixture / corpus / index / schema / git / 模型 digest / 配置）
- 逐 case 回归列表
- 缺失 / 重复 / 额外 / 超时**不能静默跳过**

**安全回归任何一条实际越权失败就阻塞交付。**

### 步骤 6 部署

```bash
# Ubuntu 内原生 Docker（29.1.3，无需 Docker Desktop）
docker compose --profile <name> up -d
```

Compose 要有：profiles、健康检查、网络、volumes、资源与日志限制。

关键约束：

- **API 不持有 Docker socket**
- **API 不持有 bootstrap 或 migration 秘密**
- `POSTGRES_USER` 是超级用户，**只给 bootstrap 用**
- `app_user` / `query_reader` / `audit_writer` 凭据各自独立
- 初始化脚本**只在空 volume 运行**

### 步骤 7 备份恢复演练

在**独立实例**上做，不要拿原库练手。

四个实验逐个跑，记录 hash、权限、版本核对结果。

---

## 常见坑

1. **改 gold 去适配结果。** 这是最严重的一条。
2. **`draft` 冒充 `frozen`。** 状态字段必须有实际审定支撑。
3. **20% 抽检通过就标全部人工验证。** 抽检只决定整批是否返工。
4. **只报均值。** 必须给逐次、方差、区间。
5. **挑最好一次报。** 至少 3 次全报。
6. **`test` 用于调阈值。** 那就不是 heldout 了。
7. **缺失/超时结果静默跳过。** 无效报告。
8. **同一题重复计成两个样本。** 分母虚增。
9. **容器启动当 ready。** 业务依赖可能还没通。
10. **只恢复 DB 就说"密钥恢复了"。**
11. **unknown 批量 resume。** 可能造成第二次副作用。
12. **改旧报告。** 修数据错误要升版本 + 重跑 + 保留旧报告。
13. **只报"页面能聊天"。** 那不能证明密码业务完成。
14. **用 tiktoken 估 token 冒充实测。** 分词器不匹配。
15. **Judge 成本混进在线成本。** 口径错误。

---

## 自检问题

1. Router 漏掉正确工具，与模型在候选池里选错——你怎么分别计量？为什么不能合并报告？
2. 为什么 `test` / heldout 不能反复用于调 prompt 或阈值？你用什么选配置？
3. Runner 里的 `approval`、`inject_fault`、`resume` 为什么不能当普通消息发给模型？结果缺失、额外、重复、超时又该怎么进报告？
4. 备份同时包含 DB、文件、index、keystore、checkpoint 时，怎么核对一致性？缺 key blob 时应该发生什么？
5. 40 题的测试集上"提升 2pp"意味着什么？你会在报告里怎么写？

---

## 本人记录

```text
日期：
实际工时：
数据集规模与审定进度（draft/ready/frozen 各多少）：
三个实验的数字表：
干净目录复现卡在哪一步：
备份恢复四个实验的结果：
已知缺口与不适用项：
```
