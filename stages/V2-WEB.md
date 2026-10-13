# V2 第一版网页闭环

本阶段基础预算**55h**；实现成果：上传/提问/结果/Trace/历史、基础API和持久任务。先读实现目标与当前切片，再执行详细任务；完成标准以实际证据为准。

## 实现目标与学习结果要求

把已验证的核心Demo接到JSON API、持久Run和基础React网页。实现教学身份、文件上传、提问、真实结果/Trace、历史与刷新。SSE到V5，审批写操作到V4；首次迁移只开当前必要功能，完整版DDL保留在本文件内。

| 需要学习的技术 | 学习结果要求 | 独立实现与排错证据 |
|---|---|---|
| FastAPI、HTTP合同与依赖注入 | 定义请求/响应/错误与加载路径，核心Agent不依赖Web框架 | curl与页面同输入得到关联Run；坏请求和真实失败分类明确 |
| 鉴权、用户/项目/资源归属 | 可信身份由服务端提供，每个读取/上传/运行入口检查归属 | 跨用户/项目和撤权访问被拒绝，不能信任question中的角色 |
| PostgreSQL、SQL、Alembic与角色 | 实际迁移必要表，解释关系/约束/owner与运行角色；数据能重启保留 | 升级/回滚或前向修复；越权SQL/DDL拒绝；基础查询结果可核对 |
| 短事务、Run与请求幂等 | 先持久Run再执行，一个client_request_id稳定关联同一请求 | 重复/并发请求与不同payload冲突，证明未重复启动 |
| 受控上传和资源元数据 | 限制类型/大小/归属，发布受控资源ID，不返回真实路径或秘密 | 正常/超限/非法上传和跨用户下载的状态/数据对照 |
| React、TypeScript、异步状态 | 自己理解组件/接口/加载错误空状态，区分本地输入与服务器快照 | 页面上传→提问→结果/Trace/历史；独立改交互并定位错误 |
| Ubuntu服务、Docker与网络 | 只引入当前服务，明确容器与宿主回环、前端访问地址 | 真实端口、健康、迁移和浏览器访问证据；Ollama保持受控监听 |

## 必须独立回答的关键问题

这些问题必须由你结合自己的实现作答，AI只审查。记录在代码仓库docs/progress.md，写清场景、自己的理由、真实证据与未覆盖边界；只背定义或复制AI答案不算通过。

| 编号 | 必须自己回答的问题 | 回答达到标准所需的说明或证据 |
|---|---|---|
| Q01 | 为什么已有终端Demo还需要API？API是否应重写Agent Loop？ | 说明复用同一核心的装配入口、请求边界与职责图 |
| Q02 | HTTP请求成功、Run完成和工具成功是否是同一状态？ | 用真实JSON/Run/ToolResult区分并说明错误映射 |
| Q03 | user_id和project_id分别从哪里来？为什么question里的身份无效？ | 给出鉴权上下文与归属校验，构造一条越权请求 |
| Q04 | 一个用户知道别人的file_id，为什么仍不能读取或执行？ | 说明授权过滤和拒绝证据，避免泄露资源数据 |
| Q05 | session_id、run_id、client_request_id分别解决什么问题？ | 用一次提问/重传/刷新解释三者生命周期 |
| Q06 | 相同请求ID携带不同内容应怎样处理？ | 解释服务端冲突规则与真实并发/重复测试 |
| Q07 | 为什么先保存Run，而不是等模型回答后才保存？ | 说明刷新/断线/重启时如何定位当前任务 |
| Q08 | 事务为什么不应该跨整个模型请求或密码子进程？ | 展示短事务范围、失败后的真实状态与锁影响 |
| Q09 | 数据库外键、唯一约束与代码校验分别提供什么保证？ | 以会话归属/请求幂等为例，构造不合法写入 |
| Q10 | 迁移失败怎样处理？运行角色为什么不拥有DDL权限？ | 自己的升级记录、角色权限和修复方案 |
| Q11 | 上传后的文件如何变成受控资源？失败上传是否可见？ | 展示大小/类型/归属、临时与发布状态，核对实际文件 |
| Q12 | 为什么元数据可以进数据库而私钥或明文不能随意放JSON？ | 标出元数据与材料位置、访问者和日志边界 |
| Q13 | React本地输入、服务器snapshot和任务结果如何区分？ | 解释一次加载/错误/刷新与切换Run的状态变化 |
| Q14 | effect清理或AbortController中断是否表示后端已停止？ | 区分本地reader和服务端取消，并核对真实Run |
| Q15 | 页面刷新为什么不能再次POST原任务？ | 说明查询原Run与新建Run的差异，提供执行计数 |
| Q16 | 容器中的127.0.0.1是否等于Ubuntu宿主的127.0.0.1？ | 画实际网络路线与采用方式，用请求验证 |
| Q17 | 为什么V2可以先JSON而暂不实现SSE？哪些条件仍不可省？ | 列出当前身份/幂等/真实状态要求与后续补齐位置 |
| Q18 | 你怎样证明第一网页闭环真实完成，而不只是页面能打开？ | 关联同一Run的浏览器/API/DB/Provider结果及失败反例 |

## 分步任务与技术掌握标准

先按当前切片实现最小输入输出，再补齐技术表。本阶段首次运行、正常/失败/权限、本人解释与独立修改分别验收；未实际运行不签收。

**当前切片**：目标3 20h、目标4 20h、目标15 15h。先SQL最少迁移/权限，再JSON API，再网页；无需SSE/RAG/审批即可完成两个只读工具的全栈闭环。模型流解析已在V1学过，前端此时用非流式JSON与Run快照。


### 目标3：FastAPI、鉴权与 SSE（30h）

**进入条件**：V1只读Loop通过；V2做JSON API20h，V5做SSE5h，V6补齐重连/错误回归5h。不等待RAG或审批模块。

**Agent目标**：多用户稳定调用；同一请求有稳定Run，客户端可查看进度与恢复。接口详见API合同。 对应详细任务：**M2 01–07**。

**技术点掌握程度标准**

| 技术点 | 能解释 | 独立做到 | 排错与边界 | 验收证据 | 后置内容 |
|---|---|---|---|---|---|
| HTTP/FastAPI/DI | 校验、认证、授权、业务错误分工 | 实现chat/files/sessions/runs/health并查OpenAPI | 稳定error code，不返原始堆栈 | curl契约用例与响应 | OAuth/SSO |
| 身份/资源权限 | API key身份不是客户端自报user_id | 可信上下文检查user/project/session/file/run | 他人ID、无权项目与无认证均拒绝 | 两用户跨资源用例 | 企业身份平台 |
| Run/请求幂等 | client_request_id与run_id各解决什么 | 流前提交Run，同身份同请求重传返回原Run | 同幂等ID不同请求体冲突，不重复动作 | 重复POST和冲突记录 | 全局幂等服务 |
| 上传/下载 | 文件ID、路径与artifact权限不同 | 限大小/类型，受控存储，下载重新授权 | 文件名不透传，超限/未完整上传不发布 | 正常/超限/拒绝用例 | 分片上传、对象存储 |
| SSE/取消 | snapshot、event、断线与cancel不同 | 持久化事件，after游标，半帧/CRLF/跨UTF-8处理 | M2默认cancel；后台阶段detach；重连不POST | 断线/重连/重复事件/取消证据 | WebSocket |

**学习与实现顺序**：健康与非流式chat → 身份/归属 → 上传 → Run查询/重传 → SSE → 取消/重连。先curl后调试页面。

**必须独立回答**：为什么Run要在流返回前提交？401/404/409/422分别意味着什么？为什么重连不能重新发chat？

**独立练习**：模拟断线，恢复同一Run；复用请求ID但改变body，确认返回冲突。

**退出条件**：正常、错误、越权可测；同请求不创建第二Run；快照与事件一致，断线不等于审批决定。

**具体实践与逐项操作**


V2先M2 01–05。M2 06–07到V5接SSE，再V6做全范围回归。下表保留完整目标标准，当前只读JSON切片不要求提前完成全部SSE。

先学习路由、请求/响应模型、HTTP 错误码、依赖注入、鉴权、上传、异步请求与 SSE。FastAPI 教程按当前任务选读模型、依赖、错误处理与文件上传部分，参见 [官方教程](https://fastapi.tiangolo.com/tutorial/)。

**技术点掌握程度标准**

| 技术点 | 本阶段必须能独立做到 | 练习与验收证据 | 可后置内容 |
|---|---|---|---|
| 路由、请求/响应与状态码 | 独立定义 health/chat/run/upload 接口；客户端看到明确状态与资源 ID，不暴露内部异常 | M2 01–04 正常响应及非法请求；存活检查与就绪检查结果可区分 | API 网关与多版本兼容 |
| 依赖注入与身份校验 | 服务端从可信凭据得到身份并注入请求；区别未认证与已认证但无权限，不信任 body 中的 user_id | 两个测试用户访问同一资源，保存允许/拒绝与无结果泄露证据 | 完整 OAuth/OIDC、企业单点登录 |
| 文件上传与资源访问 | 限制大小/类型，分配服务端 file_id 与受控存储路径；按归属授权 | 合法上传、超限、危险文件名、跨用户查询均有结果与文件状态 | 大文件分片、对象存储扩展 |
| 异步 API 与请求幂等 | 不阻塞事件循环；一个 client_request_id 对应原 Run，超时重传不重复启动动作 | M2 05 重传返回同一 run_id；解释请求生命周期与 Run 生命周期差别 | 高并发压测、复杂任务队列 |
| SSE 事件契约 | 定义 event_id/run_id/type/data 与持久化顺序；能解释 SSE 和 Ollama NDJSON 差别 | M2 06 中文、半帧、结束/错误事件验证，重放能关联原 Run | WebSocket、复杂事件总线 |
| 重连、取消与状态查询 | 明确断开后任务继续还是取消；通过快照/事件恢复，取消请求与实际取消结果分开 | M2 07 断线重连不重新 POST，取消后状态与执行记录一致 | 分布式取消与跨服务协调 |

| 顺序 | 要做的任务 | 怎么逐步完成 | 验收指标 |
|---|---|---|---|
| M2 01 | 建 API 与健康检查 | live 先不检查外部服务；ready 检查模型/必要依赖与迁移 | 两种健康检查能区分进程存活和业务可用 |
| M2 02 | 给 Loop 加 POST /chat | 先 JSON 响应，返回 run_id、状态和结果 | 同一练习在 CLI/API 得到语义一致结果 |
| M2 03 | 文件与证书上传 | 大小、类型、归属、受控存储、file_id | 非法上传拒绝；原始名字不成为系统路径 |
| M2 04 | 增加 session/run 查询 | 每个用户只能看自己被授权的资源 | 跨用户访问返回拒绝，不泄露结果 |
| M2 05 | 幂等请求 | 用 client_request_id 关联一次请求，先保存 Run | 重传返回原 Run，不产生第二次动作 |
| M2 06 | 加 SSE | 先事件契约和持久化，再逐条发送 | event_id/run_id 正确，UTF-8 和半帧可解析 |
| M2 07 | 断线、重连与取消 | 保存 disconnect_policy，重连查 events/snapshot | 重连不重新 POST；取消有明确状态 |

Run 是一次请求，Step 是请求中的一步，Session 是聊天容器；不要用一张聊天消息表替代所有任务状态。接口与 SSE envelope 以 [工程合同](V1-CORE-DEMO.md#contract-4) 第 6 节为准。

先用 curl 完成 JSON 路线，再看 SSE。SSE 的空行用于组帧，网络块不等于事件；解析器要处理 UTF-8 跨块、CRLF、heartbeat 和事件去重。V2简单同步默认断线cancel；V4持久化审批/后台任务采用detach，V5学习SSE后再做网络断线专项。任何断线都不是批准或拒绝。

**产物**：可启动 API、OpenAPI、上传与资源权限规则、JSON/SSE 示例、断线/重连/取消证据。未来启动命令的模块路径必须是你实际创建的可导入包，不能复制文档里的假入口后宣布应用完成。

**独立练习**：在请求中增加“只展示证书摘要”选项，响应模型与前端可用字段保持稳定；旧请求仍可运行。

### 目标4：PostgreSQL、事务、审计与动作意图（30h）

**进入条件**：V2与目标3交替：20h完成必要表、角色、短事务和持久记录；V6用10h补六查询/索引及专项回归。写动作intent在V4按目标7落实。

**Agent目标**：持久化任务/资源/审计，为审批、恢复、评测提供可信事实。DDL以结构文档为准。 对应详细任务：**M2 08–14**。

**技术点掌握程度标准**

| 技术点 | 能解释 | 独立做到 | 排错与边界 | 验收证据 | 后置内容 |
|---|---|---|---|---|---|
| SQL/关系/约束 | PK/FK/唯一键/索引/JOIN/NULL | 按阶段迁移用户、Run、消息、调用与密码元数据 | run/session/user及资源版本引用一致 | 迁移与一致性断言 | 数据库内核 |
| Alembic/volume | 初始化与升级不同，volume不是迁移 | 从空库升级，再升级已有库并记录版本 | 重复启动不丢数据，失败迁移可定位 | 空库/已有库/重启记录 | 零停机大表迁移 |
| 事务/并发 | DB原子性不覆盖外部密码操作 | 短事务写intent，释放后执行，再写结果 | 不跨模型/审批持锁，不承诺exactly-once | 边界图与失败记录 | 分布式事务 |
| 最小权限 | owner/app/query/audit权限不同 | 运行角色不能DDL或改审计，query仅授权视图 | 只读角色仍需tenant过滤，不接受模型SQL | 角色权限检查 | 复杂RLS运维 |
| 六查询/计量 | token来自llm_calls而非历史文本长度 | 工具/失败/参数/计量/消息/N天排行六查询 | 7与30天参数化，timeout/unknown可见 | 固定fixture与实际结果 | 大型分析平台 |

**学习与实现顺序**：最少表/迁移 → repository短事务 → 六查询 → 资源引用 → 角色 → 重启/intent演练。Memory/eval表到对应阶段添加，不要求一次实现全部业务。

**必须独立回答**：外部动作已完成但DB没写回怎么办？角色只读为何不能保证跨用户隔离？哪些字段需要唯一约束？

**独立练习**：查询7天和30天失败排行；运行账号尝试修改审计必须失败；解释外部执行的事务边界。

**退出条件**：六查询有真实断言；重启保留数据，权限边界通过，Run/工具/资源证据贯通，完整专项在V6通过后标记m2-done。

**具体实践与逐项操作**


V2做M2 08–12与M2 14短事务基础；M2 13六查询/索引专项到V6，M2 14写intent在V4按目标7补齐。运行角色、审计保护与资源隔离不能延期。

先学表、主外键、唯一约束、JOIN、索引、短事务、迁移、只读角色和参数化查询。数据库保存资源关系与执行元数据；密钥材料另存于受控 keystore，不能简单加入 messages 或工具结果 JSON。

**技术点掌握程度标准**

| 技术点 | 本阶段必须能独立做到 | 练习与验收证据 | 可后置内容 |
|---|---|---|---|
| 表设计与约束 | 画 owner/project/session/run/step/resource 关系；用主外键和唯一约束表达身份、版本与幂等条件 | M2 10–11 关系图与迁移；重复或错误关联插入被约束拒绝 | 数据仓库建模与大规模分区 |
| SQL、JOIN 与参数化查询 | 写六个业务查询；解释 JOIN 与计数范围；值使用参数绑定，动态标识符走允许列表 | M2 13 与独立 fixture 预期一致，特殊输入不能改变查询意图 | 任意自然语言转 SQL、复杂分析查询 |
| 索引与查询计划 | 为常用用户/项目/Run 查询提出索引；能读基本执行计划，解释全表扫描与索引代价 | 保存一个查询计划和索引理由；小表选择扫描不直接认定错误 | 数据库内核、系统级性能调优 |
| 事务与连接生命周期 | 说明提交/回滚、连接归还；异常不留下半套元数据；外部操作不占长事务 | M2 14 注入失败后核对数据；模型请求或审批等待期间不持锁 | 分布式事务、完整隔离级别理论 |
| Alembic 迁移 | 区分建库、升级与应用运行；空库初始化、已有库升级可复现，知道破坏性回退风险 | M2 09 两种初始化路径与当前 revision；重复 upgrade 不重复建表 | 零停机复杂迁移 |
| DB 角色与审计权限 | 区分 owner/app/query/audit；运行账号不执行 DDL，不修改既有审计；秘密不存消息表 | M2 12 各账号允许/拒绝结果与权限说明 | 企业 DBA、独立防篡改审计平台 |
| Volume 与持久化 | 解释容器、volume、数据库三者关系；服务重启后查询原数据，不靠重新 seed 假装恢复 | M2 08 重启前后资源 ID 与记录一致 | 高可用集群、复制与自动故障转移 |

V2按API/数据库需要增加依赖（m2是依赖组名）：

```bash
cd /home/zsw/work/agent_development/Agent-development-code
uv sync --extra m1 --extra m2 --extra crypto --extra dev
source .venv/bin/activate
docker compose version
```

若 compose 插件缺失，先按 [README环境](../README.md#env-0) 和 [Docker Ubuntu 安装说明](https://docs.docker.com/engine/install/ubuntu/) 检查包源，再安装插件。没有插件不代表要重装已有 engine。数据库镜像使用验证过的版本/digest，配置模板里的占位符不能直接运行。

上面的`crypto`组在M1按[provider入门练习](V1-CORE-DEMO.md#provider-practice-104-python-绑定与能力检查)创建；若尚未引入密码库先完成该任务，不能把不存在的extra当环境已齐全。只读CLI路线暂未创建该组时可省略它，但要在实际运行说明中记录。

| 顺序 | 要做的任务 | 学习重点 | 验收指标 |
|---|---|---|---|
| M2 08 | 启动 PostgreSQL 单服务 | volume、连接、readiness、端口 | 重启数据保留；只在本机开发端口访问 |
| M2 09 | 写 Alembic 迁移 | schema 版本与已有库升级 | 空库能初始化；已升级库重复升级不重建 |
| M2 10 | 保存用户/项目/会话/Run/Step/事件 | 外键与一致性、有限状态 | 能完整查一次请求，不产生跨用户错误关联 |
| M2 11 | 添加文件、证书、密钥元数据 | owner/project/provider/version/status | 元数据可查；查表不能得到私钥明文 |
| M2 12 | 区分 DB 角色 | owner/app/query/audit 权限 | 运行账号不能 DDL 或篡改审计 |
| M2 13 | 写六个查询与参数测试 | JOIN、计量、时间窗口 | 每个查询与独立 fixture 预期一致 |
| M2 14 | 保证短事务和动作 intent | 外部执行与 DB 提交边界 | 不跨模型推理或人工审批持锁 |

六个验收查询沿用通用契约：Run 工具列表；失败调用含 timeout；调用参数；每次 LLM 的实际模型和计量；Session 消息；最近 N 天失败工具排行。时间窗口至少检查 7 天与 30 天，不能共用一个写死的窗口。可再加“30 天内到期的测试证书”“某 key_id 的版本历史”作为业务查询。

证书剩余天数由固定测试时钟和规则计算，真实业务用 UTC 时间比较；报告说明部分天如何取整。不要让模型看到时间字符串后自行判定通过。

**产物**：Compose 单服务、迁移、repository、六个可验证查询、持久化 Trace 和重启证据。V2不必一次建齐Memory/评测表；V4/V5/V6按业务逐步迁移。

**独立练习**：将证书到期查询从固定 30 天改为 `within_days`，验证 0、1、30 和非法值。用 query_reader 运行同一查询，证明它无法修改证书记录。

### 目标15：React/TypeScript 与 Agent 交互（30h）

**进入条件**：V2只需只读JSON API/upload/run合同稳定，用15h做基础网页；V4增加审批/下载，V5增加SSE/引用；V6再用15h完成React异步状态与全链路专项验收。

**Agent目标**：页面展示全过程，用户能理解、批准、恢复和下载真实产物。 对应详细任务：**M6 01–07**。

**技术点掌握程度标准**

| 技术点 | 能解释 | 独立做到 | 排错与边界 | 验收证据 | 后置内容 |
|---|---|---|---|---|---|
| TS/React/状态 | 类型、组件、props/state/effect、异步清理 | 分服务端Run状态与本地输入，做基础请求页 | stale closure、重复请求、卸载流清理能定位 | 修改状态字段与回归 | 复杂前端架构 |
| 页面/API | Chat/资源/Knowledge/Memory/Trace/审批/历史职责 | 展示调用输入结果、定位、版本与下载 | loading/empty/error/denied可见，不泄密 | 页面与API映射 | 设计系统 |
| SSE/reconnect | 网络块不是事件，snapshot是恢复基准 | fetch消费流、event_id去重、刷新同Run | CRLF/跨UTF8/半帧/过期游标，重连不重POST | 浏览器断线刷新对照 | WebSocket |
| 审批/draft/final | 审批只提交固定决定，不能提交权限 | 展示hash/版本/风险/期限，draft未验证、final替换 | 双击/过期/变更/失败不显示成功 | 审批分支与Verifier失败页 | 多级审批体验 |
| 安全渲染/认证 | Markdown、文件名、工具输出不可信 | 安全渲染、下载重鉴权，不记录认证信息 | 禁危险原始HTML，不持久保存生产秘密 | 恶意文本/拒绝下载检查 | 企业SSO |

**学习与实现顺序**：TS/基础请求 → session/chat → SSE → 资源/Trace → 审批 → Sources/Verifier/Memory → 刷新/失败体验。AI可帮样板，本人须修改交互并定位异步问题。

**必须独立回答**：网络断开时任务一定停止吗？草稿和final如何替换？刷新后待审批状态从哪里来？

**独立练习**：刷新待审批页，重连运行任务，双击决定；改变一个UI状态字段并验证。

**退出条件**：Windows浏览器访问Ubuntu页面完成业务；空、失败、拒绝、pending、unknown如实显示；刷新重连不重复执行。

**具体实践与逐项操作**


V2先M6 01–02，M6 03先文件/公开证书元数据；M6 04到V5，M6 05–07随V4/V5能力开放，V6补齐完整React与全链路标准。不要因下表有审批/引用就等待后端所有模块。

先学组件、props/state、TypeScript 类型、fetch、异步错误、列表、表单、路由与 SSE 解析。CSS 用够用的页面结构，优先证明完整业务流程。

**技术点掌握程度标准**

| 技术点 | 本阶段必须能独立做到 | 练习与验收证据 | 可后置内容 |
|---|---|---|---|
| JavaScript/TypeScript 基础 | 使用对象、数组、模块、Promise/async；为 API 与事件定义类型，运行时仍校验不可信数据 | 一次请求的 typed 数据流与坏响应处理；解释类型检查不能证明后端可信 | 高级类型体操与编译器实现 |
| React 组件、props/state 与 effect | 拆分页面组件，理解渲染与异步更新；订阅有清理，服务端状态与本地表单状态分开 | M6 01–03 正常渲染；切换 Run 不残留旧订阅/旧结果 | 复杂状态框架、前端性能极限优化 |
| HTML/CSS、表单与路由 | 做可读列表、表单、错误/空状态；键盘可操作主要按钮，刷新资源路由可恢复 | 上传/资源/Chat 页面演示，字段错误与无数据不白屏 | 精细视觉设计、动画与组件库制作 |
| fetch、鉴权与错误处理 | 按可信服务端身份调用 API；处理 loading/error/success 与取消，不在 URL/日志放秘密 | 非法上传、无权查询、后端错误的 UI；按钮权限与 API 拒绝一致 | 浏览器端复杂认证框架 |
| SSE 增量解码与状态归并 | 处理 UTF-8、CRLF、半帧；按事件 ID 去重，重连恢复原 Run，不重新触发动作 | M6 04 确定性切块与浏览器断线验证，状态和后端快照一致 | WebSocket 与复杂离线同步 |
| 审批、取消与 Verifier 展示 | 显示固定动作/影响范围，批准或拒绝发送具体 action；draft、final、未检查、失败不混淆 | M6 05–06 刷新 pending 可恢复，重复点击不多执行，引用可定位 | 企业多人协同界面 |
| Artifact 下载与浏览器验收 | 获授权获取文件，处理拒绝/过期；页面不显示原始密钥，下载结果能对照真实资源 | M6 07 正常/无权下载与完整业务录像或截图、后端 Trace | CDN、大文件分片下载 |

| 顺序 | 学习任务 | 页面成果 | 验收指标 |
|---|---|---|---|
| M6 01 | 普通 API 小页面 | 登录/鉴权、上传、一次证书检查 | 资源结果与后端一致 |
| M6 02 | Chat 与 Run | 聊天、进度、Step、工具调用、历史 | 相同 run_id 可追溯 |
| M6 03 | 密码资源页 | 文件、密钥元数据、证书与版本 | 页面不显示密钥/私钥值 |
| M6 04 | SSE 与断线 | 实时事件、重连、刷新恢复 | 去重/UTF-8/CRLF 正确，不重复执行 |
| M6 05 | 审批与取消 | 固定动作、影响范围、批准/拒绝 | 身份服务端验证；刷新可重建 pending |
| M6 06 | 验证与引用 | draft 标未验证，final 显示检查项与来源 | 未检查和失败项不冒充已通过 |
| M6 07 | artifact 下载与错误页 | 密文、获授权解密文件、公开证书 | 每次下载鉴权；日志与 URL 无秘密 |

沿用九个通用区块：Chat、Session、Upload、Knowledge、Steps、Tool Calls、Sources、Approval、Run History，另用资源标签页呈现领域对象。POST 流使用 fetch，带鉴权 GET events 也可用 fetch；不能默认原生 EventSource 支持自定义鉴权头。

审批只提交 approval_id/action_hash/decision，前端不决定角色、风险或实际参数。 Markdown、文件名、工具输出安全渲染；解密文件由浏览器通过受权下载接口拿到，聊天里只显示状态与 artifact_id。

**产物**：源码、构建结果、各状态截图或演示记录、页面与资源权限验收。UI 能清楚表达“证书已解析但尚未验证信任链”。

**独立练习**：任务等待审批时刷新页面，再打开另一个客户端读取它。确认看到同一动作，只有一次审批与执行消费。

### V2详细联调与出口

1. 按M2 08–12创建必要身份/资源/Run/调用/审计迁移与角色，做一次真实重启查询。
2. 按M2 01–05用curl完成认证、上传、JSON chat、Run查询、同请求重传与跨用户拒绝。
3. 按M6 01建立一个React/TypeScript小页面，设置API地址与教学身份，上传后使用返回的file/certificate ID。
4. 按M6 02把聊天与run_id关联，展示公开结果、工具输入/输出摘要、停止原因与错误；页面状态以服务器snapshot为准。
5. 输入一项只读任务，沿同Run对照UI/API/DB/直接Provider。模型未做Verifier时显示not_run，不显示已验证。
6. 刷新页面查询原Run；重复提交同client_request_id不创建第二任务；未授权资源不出现在UI。

**出口**：Windows浏览器可完成上传→提问→只读执行→结果/Trace/历史；错误、权限、重传、重启有证据。只签收V2及目标3/4/15的本切片，下一步V3；不创建m2-done或m6-done。

## 本阶段的接口与实践细节

以下内容属于本阶段，按任务用到的部分查阅；涉及后续能力的字段仅作为扩展合同，当前切片不要求提前全部实现。

<a id="env-4"></a>
<a id="env-4-4-dockerubuntu-内原生-engine"></a>
### Docker：Ubuntu 内原生 engine

本机实测：**Ubuntu 内已有原生 Docker engine 29.1.3**（`overlay2` + cgroup v2 + seccomp），
Windows 侧**未安装也不需要** Docker Desktop。整个项目只有这一条路线。

```bash
# 先检查 compose 插件，仅缺失时按官方 Ubuntu 安装说明补齐
if ! docker compose version; then
  sudo apt update
  sudo apt install -y docker-compose-plugin
fi
docker version
docker compose version
docker run --rm hello-world
```

优点：少一层转发，compose 行为与 Linux 服务器一致，M6 的"干净环境部署"验收更真实；
服务容器可以配置只读挂载、网络范围与PID/内存限制；各项按实际服务需求验证。

Docker daemon 的资源上限由 WSL 的 `.wslconfig` 控制。实测 Ubuntu 内可见
RAM 15 GB / 20 线程（宿主 31.8 GB / 20 线程），容器上限不得超出这个可见范围。

开发 Compose 从 PostgreSQL 单服务开始；向量库、队列、对象存储使用 profiles。下例是**待填版本的模板**，尖括号值不可直接执行，选择版本、验证后记录 digest。完整 DB role/迁移契约见 [工程合同](V1-CORE-DEMO.md#contract-4)。

```yaml
services:
  postgres:
    image: pgvector/pgvector:<已验证的pg16版本或digest>
    environment:
      POSTGRES_USER: bootstrap_admin
      POSTGRES_PASSWORD: ${POSTGRES_BOOTSTRAP_PASSWORD:?required}
      POSTGRES_DB: lpa
    ports: ["127.0.0.1:5432:5432"]
    volumes: ["pgdata:/var/lib/postgresql/data"]
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U bootstrap_admin -d lpa"]
      interval: 5s
      timeout: 3s
      retries: 20
    restart: unless-stopped
  qdrant:
    profiles: ["rag"]
    image: qdrant/qdrant:<已验证版本或digest>
    ports: ["127.0.0.1:6333:6333"]
    volumes: ["qdrantdata:/qdrant/storage"]
    restart: unless-stopped
volumes:
  pgdata:
  qdrantdata:
```

Qdrant readiness 使用外部探针检查该版本 `/readyz`，或构建带探针的镜像；不假设官方镜像内有 bash/curl。`pg_isready` 只表示服务能接连接，应用 readiness 还要检查 schema_version/迁移是否完成。PostgreSQL 初始化脚本只在空 volume 运行；角色与后续 schema 升级由独立迁移步骤管理。

`POSTGRES_USER` 初始化为超级用户，只给 bootstrap 工具使用。app_user/query_reader/audit_writer 密钥各自独立，服务不拿 bootstrap 凭据。开发端口绑定 127.0.0.1；部署内部数据库不映射宿主机端口。[官方镜像账号说明](https://hub.docker.com/_/postgres)

<a id="env-5"></a>
<a id="env-5-5-网络ubuntu-内部回环windows-只访问前端"></a>
### 网络：Ubuntu 内部回环，Windows 只访问前端

现在只有两条链路，且方向相反：**Ubuntu 内部全是回环，跨系统只有"Windows 浏览器 → 前端页面"这一条**。


<a id="env-5-51-ubuntu-内部"></a>
#### Ubuntu 内部

```
Ubuntu 上的 Python 应用  ──►  127.0.0.1:11434   (Ollama)
Ubuntu 上的容器          ──►  postgres / qdrant 服务名
```

Ollama 默认只监听 `127.0.0.1`，这是**推荐状态**。如果 M2/M4 的容器里确实需要调 Ollama，
用下面两种方式之一，**不要**把 Ollama 改成监听 `0.0.0.0` 再开防火墙：

```yaml
# 方式一（推荐，单机开发）：容器共享宿主网络，直接 127.0.0.1:11434
services:
  agent-api:
    network_mode: host
    environment:
      OLLAMA_BASE_URL: http://127.0.0.1:11434
```

```yaml
# 方式二：显式声明宿主机，此时 Ollama 必须额外监听 docker0 地址
services:
  agent-api:
    extra_hosts:
      - "host.docker.internal:host-gateway"
    environment:
      OLLAMA_BASE_URL: http://host.docker.internal:11434
```

方式二的 `host.docker.internal` 解析到 `172.17.0.1`（docker0）；若 Ollama 仍只绑
`127.0.0.1` 则连不通，需要把 `OLLAMA_HOST` 改为 `172.17.0.1:11434`。
该地址只在本机 docker0 网桥上可达，不暴露到局域网，但**改了就要用
`ss -ltnp | grep 11434` 和一次真实 `curl` 各自确认**，不能凭本文件的示例值认定生效。

> 无论哪种方式，Ollama **不监听 `0.0.0.0`**，也不加任何对外放行规则。


<a id="env-5-52-windows-访问前端唯一跨系统链路"></a>
#### Windows 访问前端（唯一跨系统链路）

最终交付物是一个**前端页面**，验收方式就是"Windows 上能用浏览器打开它"。
因此前端（以及 M6 的静态站点）必须监听所有网卡，而不是只绑回环：

```bash
# 前端与 API 监听 0.0.0.0:<port>，例如
uv run uvicorn services.agent_api.main:app --host 0.0.0.0 --port 8000
```

Windows 侧打开浏览器访问下列任一地址：

```text
http://172.26.9.67:8000      # Ubuntu 的 eth0 地址（实测；WSL 重建后会变）
http://localhost:8000         # WSL2 的 localhost 转发，多数情况可用
```

取当前 Ubuntu 地址：

```bash
hostname -I | awk '{print $1}'
```

约束与纪律：

- **只放行前端/API 端口**。数据库、Qdrant、Redis、Ollama 一律绑 `127.0.0.1`，
  不映射到对外网卡 —— 前端是唯一的对外入口。
- API 自身的鉴权（`API_KEY_HEADER`）不因为是"内网"而省略；
  M2 的越权用例必须在**从 Windows 访问**的同一条链路上验证。
- 前端绑 `0.0.0.0` 意味着同网段可访问。仅在可信网络下这样做，
  需要更严时改为绑定具体网卡地址或用反向代理加鉴权。
- 端口与地址的实际值必须在改完后用 `ss -ltnp` 与一次真实浏览器访问各自验证一次。

<a id="contract-2"></a>
<a id="contract-2-2-身份资源与运行"></a>
### 身份、资源与运行

- user_id 来自服务端鉴权，session_id/project_id 必须核对归属或 membership。
- run_id 表示一次请求；client_request_id 在同一用户下唯一，POST 重传返回原 Run。
- thread_id=run_id 是本项目工作流策略；每轮聊天历史显式从 messages 加载。
- action_id 表示一次具体外部动作，tool_call_id 表示一次执行 attempt；模型报文 ID 不承担幂等作用。
- 每次检索绑定 corpus_version/index_manifest；每个证据和结果引用都能恢复到同一内容版本。
- 任何查看、下载、approve、resume、cancel、events、Memory 操作都检查用户与资源权限。

<a id="contract-3"></a>
<a id="contract-3-3-数据库设计"></a>
### 数据库设计

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

Memory hash 使用规范化结构且包含类型，冲突更新加锁；API纠正/删除用expected_content_hash做乐观并发检查，锁定有效记录后失效旧值并返回新ID/hash，不把hash当权限；语义去重不能仅靠唯一索引。source_snapshot 按隐私保留政策清理，不能以追溯为由永久保留已请求删除的个人内容。

files保存授权输入；certificates保存解析字段而不预设信任结论；crypto_keys与key_versions保存用途和版本，encrypted_blob_ref仅引用受控加密材料。artifacts绑定具体action、文件与key version，下载重新鉴权。证书检查的clock/trust_store/hostname/purpose及分项结果保存在版本化action结果中。nonce分配和唯一性由密码服务的持久化机制保证，metadata中的nonce字段本身不构成防复用控制。跨项目/用户及action引用一致性由短事务校验，必要时增加复合FK。


<a id="contract-3-31-数据库权限"></a>
#### 数据库权限

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


<a id="contract-3-32-六个验收查询"></a>
#### 六个验收查询

q1 Run→actions→tool_calls 列调用；q2 包含 failed/timeout/unknown；q3 查 canonical_arguments；q4 llm_calls 按 purpose 汇总模型/digest/token；q5 messages 按 sequence_no 排序；q6 失败排行参数化 start_time/end_time。结果空是有效结果，unknown 独立显示而不是计作成功。

<a id="api-1"></a>
<a id="api-1-1-从最小api开始"></a>
### 从最小API开始

交付顺序：V2身份/归属、live/ready、非流式chat/upload/snapshot和基础页 → V3MCP复用 → V4固定审批/取消/产物下载 → V5知识/Memory/Verifier/SSE → V6全接口与浏览器专项。先curl验证，再用React实现同一接口。FastAPI的请求模型、依赖、错误与响应学习以[官方教程](https://fastapi.tiangolo.com/tutorial/)为入口；不用一次学完全部框架。

首版采用学习用API key鉴权，推荐明确header为`X-API-Key`，由后端映射固定测试用户；如果当前代码字段不同，在实现配置中显式适配。它是学习认证方案，公网部署须补TLS与合适的会话/认证管理。前端不自报可信user_id/role；project/session/file/run只是待授权对象，UUID难猜不是权限。

学习调试UI可在本地输入教学key并仅保存在内存，刷新重新认证；不要提交到源码、URL、localStorage或日志。fetch发header，跨源时明确Origin allowlist与header许可，避免宽泛配置。下载通过带鉴权fetch获取Blob；使用cookie会话属于另一方案，须补CSRF/凭据规则并同步接口，不能混用两套假设。

<a id="api-2"></a>
<a id="api-2-2-公共字段错误与资源范围"></a>
### 公共字段、错误与资源范围

| 字段 | 含义与规范 |
|---|---|
| request_id | HTTP请求关联标识，错误与日志均带，不能替代Run |
| client_request_id | 客户端生成的业务幂等UUID，作用域绑定可信用户/项目；相同ID同规范请求返回原Run |
| run_id | 一次Agent任务持久ID，关联事件、动作、计量与结果 |
| project_id/session_id | 选择授权项目/会话，服务端校验成员与一致性 |
| action_id/approval_id/action_hash | 固定动作/决定与版本绑定，身份不来自body |
| resource ID/version | 服务端解析真实路径和具体版本，绝不接收模型任意绝对路径 |
| timestamp | UTC时间，事件/过期/延迟用同一时钟策略记录 |

错误响应统一包含error.code、message、retryable和request_id，可有安全的details；HTTP状态与code都要在合同测试固定。参数错误422，未认证401，已认证但无功能权限403，资源不可见/不存在404，请求ID或状态冲突409，超限413，依赖不可用503。流开始后不能改HTTP状态，改用error事件与真实终态；原始栈、SQL、秘密和主机路径不返回浏览器。

幂等ID相同但规范body不同返回409 request_conflict，不静默复用另一任务。规范body至少包括项目、会话、message、资源ID、stream以外的业务选项；stream是传输方式，可改变但不能改变已创建Run策略。记录请求hash与策略；重复POST可订阅既有Run，不重新执行。

<a id="api-3"></a>
<a id="api-3-3-目标端点总表"></a>
### 目标端点总表

所有业务端点使用鉴权和服务端scope过滤；下表是建议单一接口集合，确定实现时固定响应schema/分页/错误并更新OpenAPI。health不泄露秘密配置。

| 阶段 | 方法/路径 | 最小请求或查询 | 成功返回/验收重点 |
|---|---|---|---|
| V2 | GET /health/live | 无 | 进程存活，不等同ready |
| V2 | GET /health/ready | 无 | 当前启用能力与必要依赖可用；失败503 |
| V2 | POST /sessions | project_id、title可选 | 授权session ID |
| V2 | GET /sessions | project_id、cursor、limit | 仅本人授权会话，稳定分页 |
| V2 | GET /sessions/{id}/messages | cursor、limit | 顺序消息与Run关联，秘密不回传 |
| V2 JSON/V5 SSE | POST /chat | project_id、session_id、client_request_id、message、resource_ids、stream | 非流式结果或SSE；流前Run已持久化 |
| V2 | GET /runs | project_id、session_id/status可选、cursor、limit | 仅授权Run历史 |
| V2 | GET /runs/{id} | 无 | snapshot、步骤/动作摘要、pending审批、final、verifier |
| V5 | GET /runs/{id}/events | after、limit可选 | SSE恢复，同Run event_id递增 |
| V4；V5流回归 | POST /runs/{id}/cancel | 原因可选 | 202取消请求或已终态快照，不伪报外部停止 |
| V2 | POST /files | multipart file、project_id、purpose | 201 file ID/size/hash/status，校验后发布 |
| V2 | GET /files | project_id、cursor、limit | 授权文件元数据，无服务端真实路径 |
| V2元数据/V4写 | GET /certificates | project_id、cursor、limit | 已解析证书元数据与检查状态 |
| V2元数据/V4写 | GET /keys | project_id、cursor、limit | 用途/状态/版本元数据，不含密钥材料 |
| V4 | GET /keys/{id}/versions | cursor、limit | 授权版本历史，轮换前后可核对 |
| V4 | POST /runs/{id}/approve | approval_id、action_hash、decision | 原子决定与snapshot；不直接由API重跑Provider |
| V4 | GET /artifacts/{id} | 无 | 格式/大小/hash/action/key version与可下载状态 |
| V4 | GET /artifacts/{id}/download | 无 | 授权文件流；敏感解密产物遵守当前权限/策略 |
| V5 | POST /knowledge/documents | 授权file_id、project_id | 202入库任务/文档，staging状态 |
| V5 | GET /knowledge/documents | project_id、cursor、limit | 版本与active/failed/needs_ocr状态 |
| V5 | GET /knowledge/documents/{id}/chunks/{chunk_id} | document_version | 授权源片段与真实locator，已撤权拒绝 |
| V5 | DELETE /knowledge/documents/{id} | 可选expected_version | 删除/撤回发布任务状态，多索引同步 |
| V5 | GET /memories | project_id、cursor、limit | 本人有效Memory与来源摘要 |
| V5 | PATCH /memories/{id} | content、expected_content_hash | 事务纠正，旧值失效，可追溯 |
| V5 | DELETE /memories/{id} | expected_content_hash | 删除后不再注入，按隐私策略清理来源 |

文件下载不允许任意path参数；原始文件是否可下载须另定policy，不自动提供通用fs读取。Provider动作通过Agent→Executor，不增加绕过审批的`/encrypt`裸路由。学习用后台不提供任意SQL控制台、私钥导出或系统信任修改按钮。

<a id="api-4"></a>
<a id="api-4-4-chat与run响应"></a>
### Chat与Run响应

POST /chat的resource_ids表示用户显式引用的授权文件/证书/密钥；服务端校验类型及归属，再让模型见必要ID和公开摘要。message限长度，历史由服务端载入，不接受客户端伪造完整tool结果或system权限。一个请求可包含澄清结果，但等待用户补参数不能默认猜测敏感写动作。

非流式同步首版在任务结束后返回run_id/status/answer/claims/citations/verification_status/usage；遇awaiting_approval返回pending_action与approval而非假终态。持久化后台阶段可202返回run_id与snapshot/events地址。明确实现采用哪个模式，同一合同不因环境随机切换；UI支持两者的定义分别测试。

snapshot最少包含：schema_version、run_id、status、disconnect_policy、last_event_id、步骤/动作摘要、pending approval、draft引用、final_answer、Verifier摘要、安全error、计量。可另分页查详细步骤，不把全部大blob塞一个响应。final_answer只在已生成时存在，验证状态可为passed/failed/not_run，not_run不能显示为已验证。

资源字段以服务端真实记录为准：证书not_after不是“受信任”结论；证书链、hostname、purpose、撤销检查各显示passed/failed/not_checked/unknown。key当前active version与本次action使用version分别展示。


<a id="api-4-41-最小请求与错误样例"></a>
#### 最小请求与错误样例

下面UUID仅示范字段形状；使用时替换为当前测试用户真实授权资源，示例本身不是可直接请求的fixture。resource_ids是带type与id的列表，首版type限定file/certificate/key；这些对象仍需服务端归属检查。没有资源时用空列表，不能让模型猜其他用户ID。

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

```json
{
  "error": {"code": "request_conflict", "message": "该请求标识已用于不同的任务内容。", "retryable": false},
  "request_id": "55555555-5555-4555-8555-555555555555"
}
```

每个端点由实现补齐Pydantic字段约束：长度/limit最大值、枚举、可空、默认、分页游标与响应版本；API key不出现在body样例。cursor为服务端不透明游标、稳定排序/唯一ID防重复，limit有限上界。Resource与Memory返回安全元数据，工具与RAG大结果通过引用取，不返回真实路径。

Memory乐观并发与现有DDL对齐：GET返回content_hash，PATCH/DELETE提交expected_content_hash；短事务锁定对应ID并校验仍有效、归属与hash，纠正失效旧记录并创建新记录，返回新ID/hash。不同并发修改返回409，不增加一个尚未设计的version列。相同内容无变化可返回原记录；不把内容hash当授权凭据。

<a id="api-7"></a>
<a id="api-7-7-页面与学习任务"></a>
### 页面与学习任务

React基础按[官方Learn](https://react.dev/learn)学习组件、状态、effect与事件，再实现下表。可以采用路由页或同页面板，不要求固定九个路由；功能必须完整。

| 页面/区块 | 必须功能 | 对应掌握/验收 |
|---|---|---|
| Session/Chat | 会话列表、新建、提问、Run关联、历史 | 同请求重传不重复Run，空/错误/加载状态 |
| Resources | 上传、文件/证书/key元数据、version与artifact | 大小/归属/Provider能力限制与下载拒绝 |
| Knowledge | 文档版本、入库状态、来源片段 | needs_ocr/failed不假active，引用点击定位 |
| Steps/Tool Calls | 节点、调用、拒绝、结果、耗时 | proposed/executed/denied各自可辨 |
| Approval | 固定动作详情、批准/拒绝、过期/冲突 | 刷新/双击/变更不二次授权 |
| Sources/Verifier | 引用与检查项/violations | 草稿/已验证/未验证区别，N/A解释 |
| Memory | 查看、纠正、删除与来源摘要 | 删除后不注入，跨用户不可见 |
| Run History | 运行/失败/pending/unknown筛选与恢复 | 重连同Run，显式cancel，失败记录可定位 |
| Delivery信息 | 安全的版本/能力与限制摘要 | 不公开秘密配置；证书未检查项如实显示 |

前端状态分三层：本地输入/选择、服务器snapshot、流事件增量。以run_id和event_id关联，避免新旧Run串流；effect关闭或切换Run时清理reader/AbortController，但不把关闭本地reader当服务端取消。不同tab查看同Run不会触发Provider执行。

Markdown、文件名和工具输出安全渲染；禁用危险原始HTML，外链策略明确。解密产物只经授权下载，不作为聊天正文/模型上下文；浏览器console、错误上报、UI截图不包含秘密。

<a id="api-9"></a>
<a id="api-9-9-提前做网页时的功能切片"></a>
### 提前做网页时的功能切片

| 阶段 | 页面必需 | 本次可以留待后续 |
|---|---|---|
| V2 | 教学身份、上传、JSON提问、公开结果/工具Trace、Run历史/刷新/错误 | SSE、审批、密钥秘密/写工具、引用/Memory |
| V3 | 同页面调用经MCP，Trace能区分协议层 | 三Server管理界面 |
| V4 | key版本元数据、固定批准/拒绝/过期/冲突、artifact下载、pending/unknown | RAG引用、完整事实Verifier |
| V5 | SSE去重/重连、资料/引用、完整检查与Memory纠正删除 | 全量模型实验展示 |
| V6 | 全页面与异步清理/断线/取消/安全渲染/下载撤权专项 | 企业SSO、复杂设计系统 |

先已有功能的JSON/snapshot，后SSE。V2未做Verifier显示not_run，V4仅显示已做状态检查与未检查项，V5才展示完整六检查；不会因为界面先存在就冒充所有功能完成。所有开放接口从第一天鉴权/归属/限额/错误和幂等验证，MCP handler不能提供绕过审批的写入口。

<a id="crypto-7"></a>
<a id="crypto-7-7-页面与业务元数据"></a>
### 页面与业务元数据

页面建议包含聊天与 Run 详情、文件列表、key 元数据/版本、证书列表/检查详情、审批、审计与 artifact 下载。先让最小页面调用 API，再加聊天；用户也应能通过固定按钮进行同样的只读检查，用来对照 Agent 编排是否正确。

业务元数据逐步加迁移：files/artifacts、keys/key_versions、certificates/certificate_checks、CSRs、approval/actions。具体命名由实现时与既有 DDL 对齐。添加 owner/project、资源版本和用途；不在 JSON 字段里塞私钥或明文文件来省一个存储组件。

首页先显示“支持哪些能力”和“当前 provider 是否就绪”，不让模型编造 capabilities。历史 Run 显示当时 provider/模型/策略版本；当前资源状态由实时查询呈现，不用旧聊天结论替代。

## 本阶段签收清单

- [ ] 本阶段学习技术表逐项有本人解释、独立实现/修改和失败验证证据。
- [ ] Q01–Q18已由本人结合实现作答，证据与未覆盖边界记入docs/progress.md；AI仅审查。

- [ ] 必要DB迁移/角色/短事务/重启与身份、上传、JSON chat/Run/请求幂等通过。
- [ ] M6 01–02与03文件/证书切片，Windows浏览器可上传→执行→结果/Trace/历史。
- [ ] 刷新同Run、重复请求、跨用户、非法上传、错误均有真实证据；未做Verifier显示not_run。
- [ ] SSE/完整六查询/前端专项登记V5/V6，不提前标m2/m6毕业。

## 下一步

本阶段出口有证据后进入[V3阶段](V3-MCP.md)。跨阶段未完标准登记补齐位置。
