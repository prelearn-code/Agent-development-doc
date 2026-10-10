# Local Professional Agent 学习路径

> 修订日期：2026-10-10。目标：在本地硬件上独立实现、解释并验证一个有证据、可恢复、受权限约束的 Agent 系统。

本包是学习与工程设计文档，包含评测种子和离线校验工具；应用代码将在独立的 `D:\work\local-professional-agent` 仓库实现。引用的《Agent 全栈开发学习目标与成果验收文档》原件未随本包提供，因此原章节编号仅保留为对照，不能声称已经核对原件全部要求。

## 1. 设计原则

- 先实现小闭环，再增加基础设施和抽象；M1 的 Agent Loop 由学习者手写。
- 能力通过可运行产物、失败场景和独立解释共同验收；没有运行证据不勾选完成。
- 权限、隔离、审计在第一次危险操作前落实，M5 再完善威胁模型和覆盖范围。
- 冻结评测集与开发调参集分开；种子有占位符时只能校验草稿，不能作为通过验收的依据。
- 用相同配置、数据快照和 Judge 比较实验；模型、检索、工具的变化分别记录。

## 2. 阶段与预算

| 阶段 | 对应目标 | 基础工时 | 累计 | 最小产物 |
|---|---|---:|---:|---|
| Phase 0 | 环境 | 20h | 20h | Python + Ollama + 一个模型 + 测试入口 |
| M1 | 1 Python / 2 LLM | 70h | 90h | 安全工具 + 手写 Agent Loop |
| M2 | 3 FastAPI / 4 PostgreSQL | 60h | 150h | API + SSE + 持久化 Trace |
| M3 | 5 基础 RAG / 6 高级 RAG | 70h | 220h | 文档入库、引用、检索消融 |
| M4 | 7 Tool / 8 MCP / 9 LangGraph | 80h | 300h | 统一执行器、审批、恢复 |
| M5 | 10 Memory / 11 小模型 / 12 Verifier / 13 Eval / 14 Security | 90h | 390h | 场景评测、验证、安全回归 |
| M6 | 15 前端 / 16 部署 / 综合项目 | 60h | 450h | UI 全链路与干净环境部署 |

基础预算包含约 10h 最小理论地基和种子标注；加 15%~25% 集成、返工与领域适配余量，建议预留 **520~565h**。每周 12~15h 约 35~48 周，每周 25h 约 21~23 周。这是排期估算；前两周记录实际耗时后重新估计。

## 3. 文件与权威边界

| 文件 | 内容 | 权威范围 |
|---|---|---|
| [00-ROADMAP.md](00-ROADMAP.md) | 16 个目标、依赖与阶段验收 | 学习顺序、工时、范围 |
| [01-ENVIRONMENT.md](01-ENVIRONMENT.md) | 分阶段安装、主机/容器拓扑 | 环境操作与兼容验证 |
| [repo-structure.md](repo-structure.md) | 分层、DDL、运行/审批/SSE/证据契约 | 应用接口与数据库 |
| [02-MODEL-AND-EVAL.md](02-MODEL-AND-EVAL.md) | 模型配置、指标与实验协议 | 指标计算和实验控制 |
| [eval/README.md](eval/README.md) | 标注、场景、草稿与冻结流程 | 数据集操作流程 |
| [eval/dataset.schema.json](eval/dataset.schema.json) | JSON Schema | 评测记录字段与枚举 |
| [eval/validate_dataset.py](eval/validate_dataset.py) | 离线校验 | 语义、场景、冻结门禁 |
| [REVISION-2026-10-10.md](REVISION-2026-10-10.md) | 本次修订与验证范围 | 变更记录 |
| [03-LEARNING-ORDER.md](03-LEARNING-ORDER.md) | 入门与每周节奏 | 学习方法 |
| [04-AI-ASSISTED-DEV.md](04-AI-ASSISTED-DEV.md) | AI 辅助与独立能力验收 | 人机分工 |
| [checklist.md](checklist.md) | 阶段交付物与检查 | 只引用上述契约，不重新定义 |

**2026-10-10 补充修订**：新增 WSL 开发环境决策与实测快照（见
[01-ENVIRONMENT.md](01-ENVIRONMENT.md) §0 与 §8），并把 Docker 路线改为
「WSL 内原生 engine」为主、「Docker Desktop」为备选（§4）；§5 相应改写为
宿主 IP 访问方式。据此新增下方 §5「实现仓库与同步」。

冲突按权威范围修复；修改契约时同步引用文档和种子，不能仅在新增附录里覆盖旧规则。

## 4. 从今天开始

1. 选择真实领域、三份文档和一个数据源；没有真实领域时先使用明确标注为 synthetic 的小型测试夹具。
2. 完成 Phase 0 核心环境，先只拉 `qwen3:4b`。不要求一次启动全部服务。
   当前环境的实测状态与缺口见 [01-ENVIRONMENT.md](01-ENVIRONMENT.md) §8。
3. 做 M1 安全工具和非流式 Loop，再实现原生 NDJSON 流解析。
4. 修改 Prompt 前收集回归问题；M3 开始形成可冻结的数据集。

在本包根目录运行离线检查：

```bash
python3 eval/validate_dataset.py --all --mode draft
python3 -m unittest discover -s eval -p 'test_*.py' -v
python3 scripts/check_docs.py
```

种子共 60 条 RAG、25 条 Tool、40 条综合用例，均是待人工审定的草稿。60 行 gold 映射模板不是另外 60 个测试。源文档尚未入库时不伪造证据 ID，也不将 draft 结果写成 baseline。

## 5. 实现仓库与同步

应用实现建在**独立仓库** `local-professional-agent`，按 §0 的 WSL 决策放在
`~/projects/local-professional-agent`（WSL ext4，**不要**放 `/mnt/d`）。

两个仓库必须**同级摆放**，否则本文档里的 `../local-agent-learning-path/` 相对链接会断。

同步方式、目录约定与新机器部署步骤见实现仓库的
[docs/GIT-SYNC.md](../local-professional-agent/docs/GIT-SYNC.md)。

实现仓库已就绪的部分：分层骨架、`packages/core` 契约（`ToolResult`/`ToolSpec`/`RiskLevel`/`Policy`）、
`pyproject.toml` 的分里程碑依赖分组、`.env.example`、`AGENTS.md`（AI 协作红线），
以及纯标准库的 `scripts/selftest.py`（在 `uv sync` 之前即可验证骨架与配置对齐）。
