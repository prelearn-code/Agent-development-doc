# Agent Development Doc —— Local Professional Agent 学习路径

> 修订日期：2026-10-10。目标：在本地硬件上独立实现、解释并验证一个有证据、可恢复、受权限约束的 Agent 系统。
>
> 仓库更名记录：`local-agent-learning-path` → `Agent-development-doc`（2026-10-10）。
> 配套实现仓库：`Agent-development-code`（原 `local-professional-agent`）。

本包是学习与工程设计文档，包含评测种子和离线校验工具；应用代码在独立的
`Agent-development-code` 仓库实现。

**当前学习主题**：以 OpenSSL/GmSSL 的简单封装作为业务工具，学习完整的 AI Agent
开发流程，包含工具调用、API、数据库、审批恢复、评测、前端与部署。本次修订只编写文档，
不实现应用代码。入门请先读 [05-UBUNTU-STEP-BY-STEP.md](05-UBUNTU-STEP-BY-STEP.md)，
业务范围读 [06-CRYPTO-AGENT-SCOPE.md](06-CRYPTO-AGENT-SCOPE.md)。

**实现边界（2026-10-10 确定）**：仓库、Ollama、Docker、数据库、向量库、API 与前端
**全部运行在 Ubuntu 内**，Windows 不承担任何实现角色。最终交付物是一个**前端页面**，
验收方式就是「Windows 能用浏览器从网络打开它」。详见 [01-ENVIRONMENT.md](01-ENVIRONMENT.md) §0 与 §5。

引用的《Agent 全栈开发学习目标与成果验收文档》原件未随本包提供，因此原章节编号仅保留为对照，不能声称已经核对原件全部要求。

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
| [05-UBUNTU-STEP-BY-STEP.md](05-UBUNTU-STEP-BY-STEP.md) | 每周20–25h、前两周、逐阶段任务与指标 | 通用路线的详细执行方法 |
| [06-CRYPTO-AGENT-SCOPE.md](06-CRYPTO-AGENT-SCOPE.md) | OpenSSL/GmSSL适配、首版、密钥与证书场景 | 密码业务范围与验收设计 |
| [checklist.md](checklist.md) | 阶段交付物与检查 | 只引用上述契约，不重新定义 |

**2026-10-10 补充修订（已按 Ubuntu 单机重写）**：环境拓扑改为
「**全部在 Ubuntu 内实现**」——Ollama 已迁为 Ubuntu 内的 systemd 服务
（`127.0.0.1:11434`），Docker 用 Ubuntu 原生 engine，Windows 侧不再有任何实现步骤。
据此次重写更新了 [01-ENVIRONMENT.md](01-ENVIRONMENT.md) §0、§3、§4、§5 与 §8。
详见 [REVISION-2026-10-10.md](REVISION-2026-10-10.md) §5 与本包 §5「实现仓库与同步」。

冲突按权威范围修复；修改契约时同步引用文档和种子，不能仅在新增附录里覆盖旧规则。

## 4. 从今天开始

1. 读详细指南第2节与第4节，在 Ubuntu 重新检查当前环境。先准备一张公开测试证书和一个小型非敏感文件。
2. 依次完成 P0 01–04：环境、依赖锁、最小模型请求和首个测试。`qwen3.5:4b` 在最新只读核对中已下载，缺失时才拉取；不一次启动全部服务。
3. 先直接实现并核对只读证书解析/文件摘要，再封装为安全工具，最后接非流式手写 Loop。流式、API、数据库和前端按阶段增加。
4. 每个任务保存真实证据和自己的说明。修改 Prompt 前收集回归问题；M3 建操作说明知识库，M4 再正式接审批的写操作。

今天只需完成 Phase 0 的最小闭环。完整路线含余量520–565h，按已选择的每周20–25h约21–29周；先可用首版的裁剪方式见业务范围第2节。

在本包根目录运行离线检查：

```bash
python3 eval/validate_dataset.py --all --mode draft
python3 -m unittest discover -s eval -p 'test_*.py' -v
python3 scripts/check_docs.py
```

种子共 60 条 RAG、25 条 Tool、40 条综合用例，均是待人工审定的草稿。60 行 gold 映射模板不是另外 60 个测试。源文档尚未入库时不伪造证据 ID，也不将 draft 结果写成 baseline。

这些种子仍是原完整性审计领域的参考草稿。本次没有把它们改成密码业务用例；后续新增密码工具时须同步registry、schema/validator、fixtures与gold审定。文档检查通过不代表新业务已实现或评测通过。

## 5. 实现仓库与同步

文档仓库、实现仓库以及两个密码库源码仓库统一放在
`/home/zsw/work/agent_development/`（Ubuntu 的 ext4，**不要**放 `/mnt/c`、`/mnt/d`）：

```text
/home/zsw/work/agent_development/
├── Agent-development-doc/     学习文档仓库
├── Agent-development-code/    Agent 实现仓库
├── openssl/                   OpenSSL 官方源码仓库
└── GmSSL/                     GmSSL 官方源码仓库
```

**四个仓库共享同一个父目录，彼此同级**。两个密码库不放进文档仓库、实现仓库或额外的`_deps`子目录。
Ubuntu区分大小写，目录名统一为`openssl`与`GmSSL`。文档与实现同级也保证`../Agent-development-code/`链接有效。
源码目录与编译安装前缀分别记录，源码同级不表示要覆盖系统OpenSSL。GmSSL-Python若另行克隆源码，也作为该父目录下的独立同级仓库。本次只更新约定，尚未克隆或移动密码库。

同步方式、目录约定与新机器部署步骤见实现仓库的
[docs/GIT-SYNC.md](../Agent-development-code/docs/GIT-SYNC.md)。

实现仓库已就绪的部分：分层骨架、`packages/core` 契约（`ToolResult`/`ToolSpec`/`RiskLevel`/`Policy`）、
`pyproject.toml` 的分里程碑依赖分组、`.env.example`、`AGENTS.md`（AI 协作红线），
以及纯标准库的 `scripts/selftest.py`（在 `uv sync` 之前即可验证骨架与配置对齐）。
