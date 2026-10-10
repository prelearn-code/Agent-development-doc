# OpenSSL/GmSSL 全栈 AI Agent 学习项目

本项目通过简单封装 OpenSSL 和 GmSSL，逐步实现一个能够检查证书、计算摘要、审批加解密、管理密钥版本并展示执行过程的 AI Agent。主要学习目标是 Agent 全栈开发：Python 工具、手写 Loop、API、数据库、RAG、MCP、工作流、Memory、Verifier、评测、前端和部署。

文档与应用分仓管理：本仓库保存学习指南、工程契约和评测草稿；应用在 `Agent-development-code` 中实现。所有开发、构建、测试与服务运行都在 Ubuntu 内完成，Windows 浏览器用于访问最终页面。

## 1. 从哪里开始

1. 阅读 [逐步学习指南](05-UBUNTU-STEP-BY-STEP.md) 第 1–4 节，了解首版闭环和 Phase 0 任务。
2. 完成 P0 01–04：环境检查、依赖锁、一次真实模型请求、首个确定性测试。
3. 用公开测试证书和非敏感小文件，直接验证证书解析和文件摘要，再接入手写 Agent Loop。
4. 按阶段增加 API、数据库、知识检索、审批恢复、评测和前端，每次保留真实运行证据。

各阶段的技术介绍含掌握标准表：必须独立做到什么、验证练习与证据、可以后置的深入内容。学习时逐行记录“待学 / 在做 / 已验证”，以能解释、能实现、能排错判断掌握程度。

## 2. 阶段与预算

| 阶段 | 学习目标 | 基础工时 | 累计 | 阶段成果 |
|---|---|---:|---:|---|
| Phase 0 | Ubuntu、环境、HTTP、配置、测试 | 20h | 20h | 真实模型请求、首个测试、版本记录 |
| M1 | 1 Python 工具 / 2 LLM 与 Loop | 70h | 90h | 密码工具、手写 Loop、工具调用 Trace |
| M2 | 3 FastAPI / 4 PostgreSQL | 60h | 150h | API、SSE、资源元数据、持久化审计 |
| M3 | 5 基础 RAG / 6 检索实验 | 70h | 220h | 操作知识库、引用、四组消融 |
| M4 | 7 执行器 / 8 MCP / 9 LangGraph | 80h | 300h | 固定动作审批、密钥版本、恢复 |
| M5 | 10 Memory / 11 小模型 / 12 Verifier / 13 Eval / 14 Security | 90h | 390h | 模型对比、事实核对、场景与安全回归 |
| M6 | 15 前端 / 16 部署 / 综合交付 | 60h | 450h | 网页业务闭环、Ubuntu 部署与恢复演练 |

按每周 **20–25 小时**安排，含集成返工余量建议预留 **520–565 小时，约 21–29 周**。前两周用真实耗时调整排期；具体任务与掌握标准见逐步指南。首版裁剪范围见 [业务范围](06-CRYPTO-AGENT-SCOPE.md) 第 2 节。

## 3. 阅读与执行顺序

| 文档 | 用途 |
|---|---|
| [05-UBUNTU-STEP-BY-STEP.md](05-UBUNTU-STEP-BY-STEP.md) | 日常执行入口：任务顺序、学习内容、掌握标准、验收和排错 |
| [06-CRYPTO-AGENT-SCOPE.md](06-CRYPTO-AGENT-SCOPE.md) | 密码业务范围、Provider 路线、密钥与证书标准、入门练习 |
| [00-ROADMAP.md](00-ROADMAP.md) | 16 个目标、阶段依赖、工时与毕业要求 |
| [01-ENVIRONMENT.md](01-ENVIRONMENT.md) | Ubuntu、服务网络、依赖与环境记录 |
| [repo-structure.md](repo-structure.md) | 分层、密码资源元数据、工具、审批、SSE 与证据契约 |
| [02-MODEL-AND-EVAL.md](02-MODEL-AND-EVAL.md) | 模型配置、指标、消融、冻结与实验比较 |
| [03-LEARNING-ORDER.md](03-LEARNING-ORDER.md) | 每周节奏和按需学习方法 |
| [04-AI-ASSISTED-DEV.md](04-AI-ASSISTED-DEV.md) | AI 协作分工与独立能力验收 |
| [checklist.md](checklist.md) | 阶段进度与交付检查 |
| [eval/README.md](eval/README.md) | 密码项目评测草稿、标注与冻结操作 |
| [eval/dataset.schema.json](eval/dataset.schema.json) | 评测字段、当前工具枚举 |
| [eval/validate_dataset.py](eval/validate_dataset.py) | 离线结构、审批、证据与冻结门禁 |

工程接口以结构文档为准，业务限制以范围文档为准，指标以模型与评测文档为准。涉及接口修改时同步相应文档、应用 registry 和评测记录。

## 4. 仓库位置

```text
/home/zsw/work/agent_development/
├── Agent-development-doc/     学习文档
├── Agent-development-code/    应用实现
├── openssl/                   OpenSSL 官方源码
└── GmSSL/                     GmSSL 官方源码
```

四个仓库共用同一父目录，彼此同级，目录名区分大小写。GmSSL-Python 如需单独源码，也使用同级 `GmSSL-Python/`。各仓库独立固定 commit/tag；源码目录与安装前缀分开，构建使用受控前缀。应用使用 Ubuntu 文件系统中的工作目录。

应用仓库的目录与同步操作见 [docs/GIT-SYNC.md](../Agent-development-code/docs/GIT-SYNC.md)，协作规则见 [AGENTS.md](../Agent-development-code/AGENTS.md)。

## 5. 文档与评测检查

```bash
cd /home/zsw/work/agent_development/Agent-development-doc
python3 scripts/check_docs.py
python3 eval/validate_dataset.py --all --mode draft
python3 -m unittest discover -s eval -p 'test_*.py' -v
```

评测目录提供本项目的少量起步草稿和空证据模板。草稿尚未审定，待准备的文件、证书、密钥与语料标为 unresolved；结构校验通过只说明格式与契约一致。正式报告必须使用逐条人工审核、真实 fixture 与证据齐全的 frozen 数据集。完整学习指标仍要求 RAG ≥50、Tool ≥50，以及 100–180 条综合用例。
