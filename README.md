# 密码工具 Agent 全栈学习项目

用OpenSSL/GmSSL提供可核对的密码工具，学习模型工具调用、本人手写Loop、API/数据库、React、MCP、审批恢复、RAG/Memory、Verifier、评测与Ubuntu交付。先写一个可运行的小Demo，后续逐步扩展同一套代码。

## 只从这两个入口开始

1. [学习总览](LEARNING-PATH.md)：阶段实现目标、M1–M6对应位置、每周20–25h安排、工时与通用验收。
2. 当前阶段：先[V0环境](stages/V0-ENVIRONMENT.md)，验证后进入[V1摘要Agent Demo](stages/V1-CORE-DEMO.md#first-demo)。每个阶段文件已经包含技术掌握程度、详细步骤与签收清单。

其余资料在reference目录，按需查阅；原任务编号见[任务索引](reference/TASK-INDEX.md)。无需在主路径、步骤、计划和清单之间反复切换。

| 文件夹或文件 | 用途 |
|---|---|
| LEARNING-PATH.md | 唯一总览与周计划入口 |
| stages/ | V0–V6逐阶段实施，目标/深度/步骤/验收集中在当前文件 |
| reference/ | 环境、密码领域、Agent/AI协作、工程/DDL、API/Web、实验、交付与技术索引 |
| eval/ | 评测草稿、schema、fixture、冻结规则与校验器 |
| learning-plan.json | 450h预算、目标切片、86个任务和文档入口的导航数据，非应用配置 |
| scripts/check_docs.py | 链接、示例、技术表、任务、预算、DDL与数据契约检查 |

学习完成标准以当前阶段目标卡和实践表为准；业务范围以[密码范围](reference/06-CRYPTO-AGENT-SCOPE.md)；DDL/canonical工具/状态/事件以[工程契约](reference/repo-structure.md)；HTTP/页面以[API与Web](reference/08-API-AND-WEB.md)；指标/实验以[实验协议](reference/02-MODEL-AND-EVAL.md)，数据字段以[dataset.schema.json](eval/dataset.schema.json)。AI协作边界在[Agent设计参考](reference/07-AGENT-SYSTEM-DESIGN.md#ai-assistance)。差异登记迁移，关联registry/schema/评测版本同步修改。


## 参考资料按需查阅

| 资料 | 查什么 |
|---|---|
| [环境](reference/01-ENVIRONMENT.md) | Ubuntu依赖、端口、Provider与网络 |
| [密码业务](reference/06-CRYPTO-AGENT-SCOPE.md) | OpenSSL/GmSSL封装、摘要/加解密/证书的具体条件 |
| [Agent设计与AI协作](reference/07-AGENT-SYSTEM-DESIGN.md) | Loop/Context/MCP/Graph原理与本人编写边界 |
| [工程契约](reference/repo-structure.md) | 分层、DDL、工具、审批、状态和证据字段 |
| [API与页面](reference/08-API-AND-WEB.md) | 端点、幂等、SSE、页面交互与联调 |
| [模型与实验](reference/02-MODEL-AND-EVAL.md) | 模型矩阵、指标、冻结、消融和回归 |
| [交付验收](reference/09-DELIVERY-AND-ACCEPTANCE.md) | Ubuntu复现、备份恢复、证据卡和完整毕业矩阵 |

## 四仓库同级

```text
/home/zsw/work/agent_development/
├── Agent-development-doc/      学习文档
├── Agent-development-code/     应用实现
├── openssl/                    OpenSSL官方源码
└── GmSSL/                      GmSSL官方C源码
```

**两个密码学仓库与本项目文档目录处于同一级，共用一个父目录**，不是文档或应用的子目录。每仓库独立固定commit/tag，源码与安装prefix分开；可选绑定源码使用同级GmSSL-Python。实际Ubuntu用户名可替换，目录大小写与层级保持一致。

应用协作规则见[AGENTS.md](../Agent-development-code/AGENTS.md)，目录/同步见[docs/GIT-SYNC.md](../Agent-development-code/docs/GIT-SYNC.md)。本仓库不自动克隆/构建这两个库，不放真实密钥、私钥、解密产物或模型权重。


## 文档与评测检查

```bash
cd /home/zsw/work/agent_development/Agent-development-doc
python3 scripts/check_docs.py
python3 eval/validate_dataset.py --all --mode draft
python3 -m unittest discover -s eval -p 'test_*.py' -v
```

检查覆盖本地链接、代码示例语法、表格、主路径17目标表与既有领域表、DDL依赖、canonical工具和评测格式。**这些是文档检查，不执行数据库、模型或业务工具，不证明应用已经完成。**

评测起步包目前24条未审定草稿，部分fixture与证据仍待准备；draft通过只说明结构有效。完整版要求人工审定与真实证据的frozen数据、RAG≥50、Tool≥50和100–180综合用例，复用case ID不能重复计数。完成状态由学习者依据真实运行逐项填写，不由文档编写自动勾选。
