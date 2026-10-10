# 00 - 主学习路径

> 450h 基础预算，建议含余量预留 520~565h。目标编号保留与原验收文档的对照；原件未提供。接口以 [repo-structure.md](repo-structure.md) 为准，指标以 [02-MODEL-AND-EVAL.md](02-MODEL-AND-EVAL.md) 为准。

## 1. 依赖与提前落地的护栏

```text
Phase 0 → M1 手写 Loop → M2 API/数据库 → M3 RAG → M4 Tool/MCP/Graph → M5 工程评测 → M6 UI/部署
                   安全执行入口、预算、路径与隔离从 M1 开始；评测问题从第一天收集
```

关键依赖：持久化 Run/Step 支撑 Graph 与评测；文档版本、chunk 和定位元数据支撑 Citation；Tool schema 与唯一执行入口支撑审批、MCP 和 Verifier。M4 的 Verifier 节点先实现最小结构/状态/证据存在检查，M5 再完成语义与事实绑定验证。

## 2. Phase 0：环境与地基（20h，W0）

核心只要求 Git、Python 3.12 虚拟环境、Ollama、`qwen3:4b`、测试与格式检查入口、`.env.example`。Docker 在 M1 第一次执行不可信脚本前引入；PostgreSQL 到 M2，Qdrant 与 embedding 到 M3，Redis 到需要独立 worker 时，对象存储按实际需求引入。

记录机器、GPU 空闲占用、驱动、Ollama 版本和一次真实推理结果。命令详见 [01-ENVIRONMENT.md](01-ENVIRONMENT.md)。Done：从新终端进入虚拟环境能运行最小请求和一个测试，配置中没有真实密钥，标记 `phase0-done`。安装受阻时记录降级；GPU 直通容器不作为核心完成条件。

## 3. M1：LLM Developer（70h，W1~W6）

### 目标一：Python 工具工程（25h，含最小理论地基）

学习包、类型、Pydantic、async、异常、HTTP client、配置与结构化日志。统一 `ToolResult` 为 Pydantic `BaseModel` 泛型，序列化使用 `model_dump_json()`；定义见接口文档。

实现 calculator、read_file、query_database 的 fixture adapter、run_python 的最小版本。calculator 使用受限 AST；read_file 解析规范路径并核对获授权资源，处理符号链接/Windows junction，限制大小。query_database 接受结构化参数，M1 查 JSON fixture，M2 接只读数据库。

`run_python` 首先只支持受信任且版本固定的统计模板；需要执行模型生成脚本时，必须先通过 Docker Sandbox 验收。Sandbox 无网络、无秘密、非 root、只读根文件系统、限制 CPU/内存/PID/输出、仅挂载本次任务输入和输出目录，不挂载 Docker socket。不能降级为宿主机执行不可信代码。容器或子进程超时必须 terminate/kill、wait 和清理，`asyncio.wait_for` 本身不负责杀子进程。

Done：参数错误、未知工具、文件缺失、路径越界、空结果、超时清理、输出超限均有检查；空结果返回 success=True。所有调用走 `execute_tool`，M1 即拒绝未授权资源并审计。学习者能解释生命周期与边界，标记 `m1-tools-done`。

### 目标二：LLM 原理与手写 Loop（45h）

直接用 httpx 调 Ollama 原生 `/api/chat`，先 `stream:false`，再解析 NDJSON。不要把原生协议与 OpenAI 兼容端点或前端 SSE 共用解析器。原生工具报文以锁定版本的实际 Trace 为准：累积 content/thinking，收集完整 tool_calls，对对象 arguments 做 schema 校验；不预设 arguments 是字符串 delta。

原生工具消息使用 `role:tool` 与 `tool_name`。应用为每次调用生成自己的 `call_id`；同名工具并行时保持返回顺序和内部关联。若以后增加兼容端点，单独适配 `tool_call_id` 和 delta 拼接。

Loop 需要 MAX_STEPS、总 deadline、token/输出预算、未知工具拒绝、失败回传、重复调用熔断。执行器自动重试仅限已批准为可重试的幂等操作；模型新提出的调用也要经过预算、权限和动作去重，不能绕过 retry=0。

Done：calculator / get_current_project / query_database 三工具完成单步、多步、多调用和失败任务；保存原始 NDJSON Trace。写五问说明：调用与参数由谁产生、结果如何回到上下文、停止条件是什么、失败如何处理，引用实际报文。非流式与流式得到相同工具计划，标记 `m1-done`。

## 4. M2：LLM Backend Developer（60h，W7~W11）

### 目标三：FastAPI（30h）

实现请求/响应模型、依赖注入、鉴权、资源归属、限流、文件限制、统一错误处理。接口：POST /chat（非流式或 SSE）、POST /files、GET /sessions、GET /runs/{id}、GET /runs/{id}/events、POST /runs/{id}/cancel、GET /health/live、GET /health/ready。WebSocket 是选修，SSE 先完成。

在返回流前提交 Run；重复提交同一个 client_request_id 返回原 Run。SSE 事件遵循唯一契约，具有 run_id/event_id，UTF-8 与跨网络块解析正确。M2 同步推理的 disconnect_policy 默认 cancel；M4 持久化审批、M6 后台任务默认 detach。断线不是批准、拒绝或取消，审批状态能从 GET /runs/{id} 恢复；重连读取持久化事件，不能重新 POST 生成新动作。

Done：浏览器和 curl 可查完整 Trace；非法用户无法读取其他用户会话/Run/文件；断线、重连、显式取消分别验证；同一请求重传不生成第二个 Run。

### 目标四：PostgreSQL（30h）

按迁移创建阶段需要的表，不要求 M2 提前实现 Memory/评测业务。分离 migration_owner、app_user、query_reader、audit_writer；运行账号不是表 owner 或超级用户。只读查询角色只访问授权视图，限制行数、statement_timeout 和允许字段。

写六个验收查询：Run 工具列表、失败调用（含 timeout）、输入参数、每次 LLM 调用实际模型/计量、Session 消息、最近 N 天失败工具排行。窗口必须参数化，7 天与 30 天用例不能共用硬编码。

事务只覆盖短 DB 状态写入，不跨 LLM/实验/审批持锁。先持久化 action intent，再外部执行，最后写结果；恢复靠动作账本而不是试图让 DB 事务包含外部副作用。token 用 LLM 调用记录聚合，不能把累计 prompt token 当每条历史消息的文本长度。

Done：迁移可重跑，数据重启不丢，运行账号不能篡改审计/DDL，六个查询有真实 fixture 断言，标记 `m2-done`。

## 5. M3：RAG Developer（70h，W12~W15）

### 目标五：基础 RAG（35h）

Parse → Chunk → Metadata → Embed → Qdrant。支持 PDF/MD/TXT，扫描页明确标记 needs_ocr，不生成假正文；复杂表格先记录限制。每个 chunk 带 document_id、document_version、chunk_id、point_id、content_hash、page_start/page_end 或 section/字符定位、project_id 与访问范围。

Qdrant point_id 使用 UUID 或 uint64，业务 chunk_id 放 payload。不可把任意 `doc_x_p1_c1` 字符串直接当 point_id。内容去重仅在同一项目/版本边界，不能用全局 hash 暴露其他用户文件存在。

新索引构建完再发布 active manifest；失败可重试但不发布半成品；文档更新/删除同步 dense、sparse 和 metadata。Resume 绑定当时版本，内容不存在时报告 evidence_unavailable。所有检索路线在候选召回前应用服务端授权过滤，不能由模型参数或前端任意放宽。

Done：三种格式各有真实样本；引用能定位；重复入库不重复、索引失败不进入 active；越权证据无法出现在 dense/sparse/rerank/引用中。

### 目标六：高级 RAG（35h）

Dense、中文分词 BM25、RRF、rerank 与 rewrite 可独立配置。先 dense baseline，再三条新增配置：sparse only、dense+sparse+RRF、加 rerank。BM25 接收已经 tokenized 的语料；learned sparse 属于额外实验，Ollama /api/embed 不输出 sparse 权重。

至少 50 个经审定问题，正样本报 Hit@5/10、Recall@5/10、MRR@10 与证据覆盖；无答案样本单独报正确拒答率和误拒答率。引用存在/定位、引用支持性、答案关键点分别报告。标注候选从多种检索路线与源文档合并，不把 baseline 没找到的题直接标成无答案。

Done：冻结 corpus/chunk/index manifest，完成四组消融并列出失败用例、延迟与质量差异；不要求 Hybrid 必须赢，按结果解释，标记 `m3-done`。

## 6. M4：Agent Developer（80h，W16~W20）

### 目标七：Tool 工程化（30h）

ToolSpec 的 schema、timeout、permission、risk、read_only、idempotent、max_retries、handler 统一定义。search_knowledge/query_database/read_file 为 L0；受限统计模板为 L1；任意脚本为 L3；run_experiment 为 L3。写工具默认审批，破坏性工具默认禁止。

统一执行入口：规范化参数 → schema/业务校验 → RBAC/资源 → 绑定动作的审批 → action intent → Sandbox/执行 → 输出校验 → 完成与审计。所有拒绝、失败、取消和超时也记录；风险由本地策略决定，MCP 注解不能自授权限。

Done：50 条工具用例，允许多个合法计划；Exact/Set/First Tool、条件参数正确率、端到端调用正确率分别报。参数按语义类型归一，MB=10^6、MiB=2^20，未知单位必须澄清。

### 目标八：MCP（20h）

实现 fs/db/domain 三 Server、一个 Resource 和一个 Prompt。工具使用 fs./db./domain. 命名空间，registry bridge 映射到本地 canonical tool_id；协议错误不能被包装成成功。

本地 stdio 日志走 stderr。连接配置属于受信任配置；允许端点列表热加载后才能连接新 Server。已有 Server tools/list_changed 通知触发刷新（或显式 refresh），与新 Server 的发现分开验收；MCP 不提供未经配置的全网自动发现。传输迁移到 Streamable HTTP 后须明确鉴权、Origin/host 检查和内部网络边界。

Done：已有连接新增工具、不改 Agent 代码即可刷新并使用；新增授权端点热加载后可用；未授权 Server/风险未知工具不执行，记录完整发现与调用日志，标记 `m4-mcp-done`。

### 目标九：LangGraph（30h）

Router → Planner → Retrieval/Tool → Draft → Verify → Final；失败分支有预算与上限。I/O 节点不是纯函数，持久化状态更新要可重放。AsyncPostgresSaver 在部署迁移时 setup，动态审批恢复用 `Command(resume=...)`，崩溃恢复使用已保存 thread state；不要混用静态断点的 invoke(None) 与审批值。

本项目 thread_id=run_id 表示“一请求一工作流”；聊天上下文由 messages 加载。如果以后采用一会话一 thread，必须新增映射和并发规则。State 只存版本化证据/结果引用和有限摘要。审批节点只构造/读取固定 pending action，恢复不能重新规划出不同参数再沿用旧审批。

action 状态：proposed → awaiting_approval → ready → executing → succeeded/failed/cancelled/unknown。执行完成后、记录结果前崩溃可能进入 unknown；先按幂等键/外部 job_id 核对，不能自动重跑未知的非幂等动作。独立 worker 用 lease + fencing，重复投递不会重复副作用。

Done：审批批准/拒绝/过期、重复 approve、参数变更、执行前/执行中/执行后崩溃、两个 worker 竞争均验证；未知状态需要核对或人工处理，标记 `m4-done`。

## 7. M5：Agent Engineer（90h，W21~W26）

### 目标十：Memory（20h）

区分 History、Run State、长期 Memory、Knowledge。提取候选先做规则过滤；显式“记住”优先，不能仅按长度丢弃“记住用Q8”等短指令。仅从有权限、可信来源提取用户事实；文档中的指令不能写成用户偏好。

按 user_id/project_id 检索与去重；有效 content_hash 唯一索引防并发重复，语义相似候选复核，用户改口在事务中失效旧记录并插入新记录。来源保留快照或在删除时明确失去可追溯性；实现查看、纠正和删除。检索阈值避免无关偏好注入，最多 5 条不是必须塞满 5 条。

Done：跨会话共享同一测试用户；不同用户/项目不共享；纠正、删除、并发去重可验证。20 条无关问题不能自动变成 20 条 Memory。

### 目标十一：小模型优化（15h）

同族同量化比较 qwen3 4B/8B；14B 可选。五组配置为 4B±router、8B±router、14B+router；固定候选工具池与 fixture，80 工具压力实验是选修，不能用 9 工具结果声称证明 80 工具能力。

Router 与上下文压缩分别消融；固定温度、think、num_ctx、seed 和 Judge。重复 3 次，报告每次与汇总方差；多数票是另一个配置，不替代单次准确率。

Done：回答“在哪些任务 4B 够用”，同时报告质量、端到端延迟、tokens、峰值显存和冷加载成本。

### 目标十二：Verifier（15h）

六检查：必要工具最终成功、事实数字绑定、引用存在与定位、引用支持性、unsupported claim、输出结构。失败后成功的历史 attempt 不应永久阻塞；忽略可选工具失败需要显式证据。

数字绑定 metric/entity/value/unit/source_ref；派生量绑定输入与公式/版本固定计算工具，日期、编号和版本按类型处理。仅查数字是否出现在任意结果中会漏掉数据张冠李戴。引用验证用实际 page_start/page_end 或 section，MD/TXT 不伪造页码；存在性与支持性分开。

Done：12.34→13.24、单位错误、正确数字绑定错误实体、派生值、跨页定位、无引用合理拒答均覆盖。至少 20 错误/20 正确回答初测 TPR/FPR 并报样本数和区间，不把小样本 95% 当总体保证。

### 目标十三：Eval（20h）

以 [eval/README.md](eval/README.md) 的单条与 scenario schema 为准，最终 100~180 条审定用例。Runner 执行 fixture、turn、审批、故障、恢复、断言和 cleanup；每个实验/重复使用隔离 user/session/索引空间。

开发集可调参，heldout test 不进入 prompt/few-shot/Judge 调参；近似问题分组切分。Seed 校验使用 draft，正式 CI/baseline 使用 frozen，证据、fixture、人工审定缺失均不能豁免。CI 分确定性合同检查、固定 mock 场景、专用本地 GPU 评测；普通托管 CI 不默认有 Ollama/GPU。

Done：指标报告包含适用样本数、skip 原因和 case-level 回归；阈值单位用百分点 pp，安全实际越权零容忍。排除基础设施无效实验须整批作废或报告 invalid，不能只跳过失败题。

### 目标十四：Security（20h）

完成直接/间接注入、SQL/命令/路径/SSRF、秘密泄露、权限提升测试，新增审批重放、跨用户资源、MCP 恶意注解与 Memory 投毒。执行层与实际资源状态断言为主，不能只检索回答里的“已删除”。输入检测和分隔符是辅助，不保证消除注入。

Done：被拒绝的尝试有审计；实际数据库/文件/网络副作用没有越权；Sandbox 无宿主机秘密/网络/socket；安全回归失败阻塞发布，标记 `m5-done`。

## 8. M6：Full-Stack Engineer（60h，W27~W34）

### 目标十五：前端（30h）

React/TypeScript，Chat、Session、Upload、Knowledge、Steps、Tool Calls、Sources、Approval、Run History 九区块。POST 流使用 fetch；GET events 可使用支持鉴权的 fetch。解析器处理 CRLF、UTF-8 跨块、空行、heartbeat 和 event_id 去重。审批只提交 approval_id/action_hash/decision，不相信前端提供的角色或风险。

Draft token 明确标为未验证；Verifier 完成后 final 事件替换为已验证答案。刷新从 Run 状态重建待审批动作，重连不触发重新执行；显式 cancel 才取消 detach 任务。Markdown/文件名/工具输出安全渲染，秘密不进入浏览器日志。

### 目标十六：部署（15h）

Compose 按 profiles 启动 API/worker/前端/DB/向量库/可选队列对象存储/MCP，Ollama 保留宿主机。版本/digest 冻结、健康检查、迁移、volume、日志轮转、资源限制与网络隔离完整。API 不持有 Docker socket；只有可信 Sandbox launcher 有受控调用能力。

Done：干净 clone → 配置 → 安装固定环境/拉模型 → 迁移 → 启动 → smoke；重启数据不丢，端口不无条件开放；无 GPU 时明确降级，不伪报 GPU baseline。

### 综合项目（15h）

任务：检索原理 → 查历史 → 提议 100MB/500MB/1GB 实验 → 审批 → 执行 → 计算对比 → Verifier → 带版本化来源的报告。数据规模统一明确 MB/GB 十进制；若使用二进制则标 MiB/GiB。

验收：UI 每步可见、恢复不重复实验、正确事实与引用绑定、审计包含审批/失败/拒绝、完整任务加入冻结 scenario。标记 `m6-done`。15h 只预算已有模块集成；领域算法从零实现和大量真实实验另列工时。

## 9. 12 周最小路径

必须先明确每周工时，12 周是范围裁剪，不承诺完成 450h。保留 M1、M2、小型 RAG、一个 MCP、审批/恢复与最小前端。可以减少高级检索、Memory、模型组数和标注规模；不能裁掉权限、隔离、动作幂等、审计和可执行验收。迁移保留最小 Alembic，不用 create_all 代替已有库升级。完成后按缺口补 M5，不称为完整版毕业。

## 10. 决策记录与毕业验收

每阶段写一份简短 ADR：背景、选择、替代方案、证据、限制、触发重新考虑的条件。篇幅不作硬门槛，内容必须来自自己做过的实验。毕业解释：为何检索/查库/选工具、为何允许执行、状态在哪里、失败怎么恢复、引用来源、验证方法、小模型差距、评测如何证明改动。

A 模型、B RAG、C 数据库、D Tools、E MCP、F Workflow、G Memory、H Eval、I Security、J 全栈均有运行与失败证据；任一能力不足记录为缺口，不用“看过教程”替代。
