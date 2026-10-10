# 08 - API契约与全栈页面学习设计

配合[00](00-ROADMAP.md)目标3/4/15和[05](05-UBUNTU-STEP-BY-STEP.md)任务实施。这里是目标接口与前端验收设计；实现后以OpenAPI与合同测试确认，不把此表视为当前代码已有路由。DDL、状态/SSE枚举以[repo-structure](repo-structure.md)为准，业务工具约束见[06](06-CRYPTO-AGENT-SCOPE.md)，交付见[09](09-DELIVERY-AND-ACCEPTANCE.md)。

## 1. 从最小API开始

学习顺序：live/ready → 非流式chat → sessions/run snapshot → 身份与归属 → 上传 → SSE → 取消 → 审批 → Knowledge/Memory → artifact下载。先curl验证，再用React实现同一接口。FastAPI的请求模型、依赖、错误与响应学习以[官方教程](https://fastapi.tiangolo.com/tutorial/)为入口；不用一次学完全部框架。

首版采用学习用API key鉴权，推荐明确header为`X-API-Key`，由后端映射固定测试用户；如果当前代码字段不同，在实现配置中显式适配。它是学习认证方案，公网部署须补TLS与合适的会话/认证管理。前端不自报可信user_id/role；project/session/file/run只是待授权对象，UUID难猜不是权限。

学习调试UI可在本地输入教学key并仅保存在内存，刷新重新认证；不要提交到源码、URL、localStorage或日志。fetch发header，跨源时明确Origin allowlist与header许可，避免宽泛配置。下载通过带鉴权fetch获取Blob；使用cookie会话属于另一方案，须补CSRF/凭据规则并同步接口，不能混用两套假设。

## 2. 公共字段、错误与资源范围

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

## 3. 目标端点总表

所有业务端点使用鉴权和服务端scope过滤；下表是建议单一接口集合，确定实现时固定响应schema/分页/错误并更新OpenAPI。health不泄露秘密配置。

| 阶段 | 方法/路径 | 最小请求或查询 | 成功返回/验收重点 |
|---|---|---|---|
| M2 | GET /health/live | 无 | 进程存活，不等同ready |
| M2 | GET /health/ready | 无 | 当前启用能力与必要依赖可用；失败503 |
| M2 | POST /sessions | project_id、title可选 | 授权session ID |
| M2 | GET /sessions | project_id、cursor、limit | 仅本人授权会话，稳定分页 |
| M2 | GET /sessions/{id}/messages | cursor、limit | 顺序消息与Run关联，秘密不回传 |
| M2 | POST /chat | project_id、session_id、client_request_id、message、resource_ids、stream | 非流式结果或SSE；流前Run已持久化 |
| M2 | GET /runs | project_id、session_id/status可选、cursor、limit | 仅授权Run历史 |
| M2 | GET /runs/{id} | 无 | snapshot、步骤/动作摘要、pending审批、final、verifier |
| M2 | GET /runs/{id}/events | after、limit可选 | SSE恢复，同Run event_id递增 |
| M2 | POST /runs/{id}/cancel | 原因可选 | 202取消请求或已终态快照，不伪报外部停止 |
| M2 | POST /files | multipart file、project_id、purpose | 201 file ID/size/hash/status，校验后发布 |
| M2 | GET /files | project_id、cursor、limit | 授权文件元数据，无服务端真实路径 |
| M2/M4 | GET /certificates | project_id、cursor、limit | 已解析证书元数据与检查状态 |
| M2/M4 | GET /keys | project_id、cursor、limit | 用途/状态/版本元数据，不含密钥材料 |
| M4 | GET /keys/{id}/versions | cursor、limit | 授权版本历史，轮换前后可核对 |
| M4 | POST /runs/{id}/approve | approval_id、action_hash、decision | 原子决定与snapshot；不直接由API重跑Provider |
| M4 | GET /artifacts/{id} | 无 | 格式/大小/hash/action/key version与可下载状态 |
| M4/M6 | GET /artifacts/{id}/download | 无 | 授权文件流；敏感解密产物遵守当前权限/策略 |
| M3 | POST /knowledge/documents | 授权file_id、project_id | 202入库任务/文档，staging状态 |
| M3 | GET /knowledge/documents | project_id、cursor、limit | 版本与active/failed/needs_ocr状态 |
| M3 | GET /knowledge/documents/{id}/chunks/{chunk_id} | document_version | 授权源片段与真实locator，已撤权拒绝 |
| M3 | DELETE /knowledge/documents/{id} | 可选expected_version | 删除/撤回发布任务状态，多索引同步 |
| M5 | GET /memories | project_id、cursor、limit | 本人有效Memory与来源摘要 |
| M5 | PATCH /memories/{id} | content、expected_content_hash | 事务纠正，旧值失效，可追溯 |
| M5 | DELETE /memories/{id} | expected_content_hash | 删除后不再注入，按隐私策略清理来源 |

文件下载不允许任意path参数；原始文件是否可下载须另定policy，不自动提供通用fs读取。Provider动作通过Agent→Executor，不增加绕过审批的`/encrypt`裸路由。学习用后台不提供任意SQL控制台、私钥导出或系统信任修改按钮。

## 4. Chat与Run响应

POST /chat的resource_ids表示用户显式引用的授权文件/证书/密钥；服务端校验类型及归属，再让模型见必要ID和公开摘要。message限长度，历史由服务端载入，不接受客户端伪造完整tool结果或system权限。一个请求可包含澄清结果，但等待用户补参数不能默认猜测敏感写动作。

非流式同步首版在任务结束后返回run_id/status/answer/claims/citations/verification_status/usage；遇awaiting_approval返回pending_action与approval而非假终态。持久化后台阶段可202返回run_id与snapshot/events地址。明确实现采用哪个模式，同一合同不因环境随机切换；UI支持两者的定义分别测试。

snapshot最少包含：schema_version、run_id、status、disconnect_policy、last_event_id、步骤/动作摘要、pending approval、draft引用、final_answer、Verifier摘要、安全error、计量。可另分页查详细步骤，不把全部大blob塞一个响应。final_answer只在已生成时存在，验证状态可为passed/failed/not_run，not_run不能显示为已验证。

资源字段以服务端真实记录为准：证书not_after不是“受信任”结论；证书链、hostname、purpose、撤销检查各显示passed/failed/not_checked/unknown。key当前active version与本次action使用version分别展示。

### 4.1 最小请求与错误样例

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

## 5. SSE合同与重连

事件只有结构文档枚举的10种：run_start、step、tool_call、tool_result、approval_required、token、verify、final、done、error。envelope统一schema_version/event_id/run_id/timestamp/payload，SSE id与event_id一致。state和event同一短事务提交后发送。网络分块不是事件，发送器JSON为单行，客户端按空行组帧，支持CRLF/多data行/UTF-8跨块。

| 事件 | UI用途 | 必须遵守的语义 |
|---|---|---|
| run_start | 关联Run与运行状态 | 去重后不新建第二任务 |
| step | 显示节点与状态 | 不把计划步骤当已经完成 |
| tool_call/tool_result | 提议/执行/拒绝/失败与结果摘要 | action/call关联，不只显示工具名称 |
| approval_required | 显示固定动作和决定入口 | 不自动同意，不用最新聊天重算参数 |
| token | 流式草稿 | 明示未验证，可随后替换 |
| verify | 检查、violations与修复中状态 | 必需unknown不是pass |
| final | 最终回答与引用/验证状态 | 替换草稿，不把失败验证包装成功 |
| done | 终态与计量 | pending审批关闭连接不能发completed |
| error | 可理解失败与恢复指引 | fatal后有真实done终态，非fatal可能继续 |

重连步骤：保留run_id和最后应用event_id → GET snapshot核对权限/终态/审批 → GET events?after=游标读取严格大于游标的事件 → 去重应用 → 保持同Run。若快照last_event_id已覆盖之前事件，可按实现的快照版本跳过已反映状态；需要聊天草稿恢复时用持久draft_ref，不假设永久保留所有token。

游标不属于该Run或格式无效报明确错误；保留窗口已过返回410 event_history_expired和snapshot地址，UI从快照重建。heartbeat是SSE注释，不占业务event_id。禁止把网络关闭当done或默认取消detach任务。

初版POST流与恢复GET流均使用fetch携带认证header；原生EventSource不能随意设置自定义header，不要把API key塞URL。若改cookie方案，独立处理凭据和CSRF。

## 6. 审批与取消交互

审批面板显示canonical tool、规范参数、影响资源与版本、风险/策略版本、hash、期限、发起者与执行状态。用户批准的是显示出的固定动作；body只含approval_id/hash/decision，后端重新鉴权、查pending、期限、hash和消费状态。

重复相同决定返回已有决定；并发冲突或反向决定返回409及当前snapshot。决定提交后调度恢复一次工作流，API响应不宣称密码动作已完成。版本变更/过期/撤权让审批失效并展示重新提议指引。用户刷新须仍看到同一pending；按钮禁用只改善体验，服务端CAS/单次消费才提供正确性。

cancel按钮发送显式取消请求，然后展示cancelling提示并查询真实Run状态；这只是UI本地提示，不新增数据库Run枚举。外部已完成的动作不能回滚为未执行；无法确认时展示unknown/reconciling与核对说明。后端终态以结构文档枚举为准。

## 7. 页面与学习任务

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

## 8. 全栈联调验收表

| 场景 | API/DB必须成立 | 页面必须可见 |
|---|---|---|
| 正常只读 | 同Run真实tool结果，计量可关联 | 调用、公开字段/摘要与final |
| 上传超限/非法参数 | 无有效已发布资源/动作 | 错误code与修改指引 |
| 跨用户读取 | 404/403，不泄露资源数据 | 拒绝，不出现他人元数据 |
| 重复POST/事件 | 同Run，无重复副作用 | 无重复回答/调用卡片 |
| pending刷新 | 原hash与approval不变 | 原动作和剩余期限 |
| 拒绝/过期/变更 | 不执行，决定与原因有审计 | 不展示已执行或可沿用旧批准 |
| detach断线/重连 | 后台状态不因断线改变 | 同Run继续，不能自动新POST |
| Verifier失败 | 必需检查未通过 | 未验证与violations，不能绿色成功 |
| Provider崩溃/unknown | 不盲重跑非幂等动作 | 核对中/unknown与操作说明 |
| 下载越权/撤权 | 当前授权重新检查 | 可理解拒绝，不能凭旧链接绕过 |

完成证据：同一run_id的curl/API响应、DB状态、SSE与浏览器行为；UI截图只能作为辅助。系统与本人TS/异步理解分别按00标准验收，不只检查页面好看。
