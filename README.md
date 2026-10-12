# 密码工具 Agent 全栈学习项目

以简单封装OpenSSL/GmSSL为业务主线，学习完整Agent开发：Python工具、手写Loop、API/数据库、RAG、MCP、持久工作流、Memory、Verifier、评测、安全、React前端与Ubuntu交付。模型负责理解与提议，确定性服务负责权限、审批、密码结果与证据。**主目标是能独立开发和排错Agent，密码库提供可验收的工具动作。**

这是文档仓库，应用在同级`Agent-development-code`实施。所有开发、构建、测试与服务运行都在Ubuntu，Windows只用浏览器访问最终页面。文档中的规划能力、命令和接口不代表当前应用已实现；真实完成状态由运行证据确认。

## 1. 现在从哪里开始

1. 读[00主学习路径](00-ROADMAP.md)第1–4节，了解掌握标准、能力全图、预算与Phase 0。
2. 用[05逐步指南](05-UBUNTU-STEP-BY-STEP.md)第1–4节完成P0 01–04；不一次安装所有服务/模型。
3. 先用公开测试证书/非敏感小文件直接做解析和摘要，按06选Provider；工具直接通过后才接手写Loop。
4. 每个目标按00的“解释、独立实现、排错、证据”逐行验收，05给具体任务；阶段出口与checklist同步。
5. 按V1核心调用→V2基础网页→V3一个MCP→V4审批/恢复→V5知识/可靠性→V6完整实验/交付推进，基础网页不等待知识库。

每周20–25h，完整基础450h/含余量520–565h，约21–29周；V2只读网页累计140h基础（含余量约7–9周），V4审批密码版累计207h基础（含余量约10–13周）。估算按前两周真实耗时校正。16目标编号与M任务ID保留，执行顺序只用V0–V6；同目标切片不重复计费，首版不等于完整版毕业。

## 2. 文档分工与阅读时机

| 文档 | 唯一职责 | 什么时候读 |
|---|---|---|
| [00-ROADMAP.md](00-ROADMAP.md) | 主课程：V0–V6执行顺序、Phase 0+16目标、切片/全表深度、练习与出口 | 第一份；每个目标开始和验收 |
| [05-UBUNTU-STEP-BY-STEP.md](05-UBUNTU-STEP-BY-STEP.md) | 日常任务、操作步骤、阶段练习与排错 | 跟着当前目标逐项执行 |
| [01-ENVIRONMENT.md](01-ENVIRONMENT.md) | Ubuntu环境、依赖、Provider与网络路线、历史快照 | Phase 0与服务首次引入 |
| [03-LEARNING-ORDER.md](03-LEARNING-ORDER.md) | 每周节奏、按需补基础与复盘 | 安排本周与遇到阻塞 |
| [04-AI-ASSISTED-DEV.md](04-AI-ASSISTED-DEV.md) | AI协作边界与个人理解验收 | 请求AI帮助前 |
| [06-CRYPTO-AGENT-SCOPE.md](06-CRYPTO-AGENT-SCOPE.md) | 密码业务、Provider路线、工具与秘密/版本限制 | 工具封装与审批设计 |
| [07-AGENT-SYSTEM-DESIGN.md](07-AGENT-SYSTEM-DESIGN.md) | 运行时、Context/Router/Loop/Graph、设计问题 | 目标2、7–12 |
| [repo-structure.md](repo-structure.md) | 分层、DDL、工具/审批/状态/SSE/证据工程契约 | 改schema或模块边界时 |
| [08-API-AND-WEB.md](08-API-AND-WEB.md) | HTTP端点、错误、幂等/SSE、前端状态与联调 | 目标3/4/15 |
| [02-MODEL-AND-EVAL.md](02-MODEL-AND-EVAL.md) | 模型配置、指标/分母、冻结、消融与回归规则 | 收集问题及目标6/11–14 |
| [eval/README.md](eval/README.md) | 评测草稿、fixture/证据标注、draft/frozen操作 | 逐题审定与Runner实施 |
| [09-DELIVERY-AND-ACCEPTANCE.md](09-DELIVERY-AND-ACCEPTANCE.md) | 各V阶段交付、Ubuntu复现、备份恢复、证据卡与毕业矩阵 | V2起展示成果，V6完整验收 |
| [learning-plan.json](learning-plan.json) | V阶段工时、目标切片、86个任务入口导航数据 | 校验预算与任务覆盖，不作为应用配置 |
| [checklist.md](checklist.md) | 未勾选进度清单与签收记录 | 目标/阶段退出时 |

发生冲突时按职责处理：学习完成标准以00为准；执行任务在05；业务范围以06；DDL、canonical工具/状态/事件字段以结构文档；HTTP与页面以08；指标与实验以02，数据字段以[dataset.schema.json](eval/dataset.schema.json)。实际代码与规划的差异先登记迁移，不静默改变约定；修改时同步关联文档/registry/schema与评测版本。

## 3. 四仓库同级

```text
/home/zsw/work/agent_development/
├── Agent-development-doc/      学习文档
├── Agent-development-code/     应用实现
├── openssl/                    OpenSSL官方源码
└── GmSSL/                      GmSSL官方C源码
```

**两个密码学仓库与本项目文档目录处于同一级，共用一个父目录**，不是文档或应用的子目录。每仓库独立固定commit/tag，源码与安装prefix分开；可选绑定源码使用同级GmSSL-Python。实际Ubuntu用户名可替换，目录大小写与层级保持一致。

应用协作规则见[AGENTS.md](../Agent-development-code/AGENTS.md)，目录/同步见[docs/GIT-SYNC.md](../Agent-development-code/docs/GIT-SYNC.md)。本仓库不自动克隆/构建这两个库，不放真实密钥、私钥、解密产物或模型权重。

## 4. 文档与评测检查

```bash
cd /home/zsw/work/agent_development/Agent-development-doc
python3 scripts/check_docs.py
python3 eval/validate_dataset.py --all --mode draft
python3 -m unittest discover -s eval -p 'test_*.py' -v
```

检查覆盖本地链接、代码示例语法、表格、主路径17目标表与既有领域表、DDL依赖、canonical工具和评测格式。**这些是文档检查，不执行数据库、模型或业务工具，不证明应用已经完成。**

评测起步包目前24条未审定草稿，部分fixture与证据仍待准备；draft通过只说明结构有效。完整版要求人工审定与真实证据的frozen数据、RAG≥50、Tool≥50和100–180综合用例，复用case ID不能重复计数。完成状态由学习者依据真实运行逐项填写，不由文档编写自动勾选。
