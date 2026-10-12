# 07 - Agent运行机制与系统设计练习

本文件解释Agent内部如何工作，配合[00主路径](00-ROADMAP.md)目标2/7/8/9/10/12。它提供职责、输入输出、约束和练习，初版Loop、State/安全状态机、Verifier核心实现仍由学习者设计与编写。DDL、工具/审批/SSE枚举以[repo-structure](repo-structure.md)为准，密码限制见[06](06-CRYPTO-AGENT-SCOPE.md)，接口见[08](08-API-AND-WEB.md)。以下是目标设计，不能据此声称当前代码已有完整实现。

## 1. 先区分三个角色

| 角色 | 可以做什么 | 不能靠它保证什么 |
|---|---|---|
| 模型 | 理解意图、提议工具和参数、生成计划/草稿 | 不能自行授权、证明动作成功、读取秘密或决定资源归属 |
| Agent运行时 | 管上下文/预算/步骤，调用检索与执行入口，保存状态 | 不能因为模型说成功就修改实际资源状态 |
| 确定性服务 | 检查身份/权限/审批，执行固定Provider操作，返回真实结果 | 不能用schema通过代替授权，不能把模型参数当任意路径/SQL |

一个自然语言请求可能产生零、一或多次工具调用。没有必要调用时允许直接回答或澄清；有事实性操作结论时必须绑定实际结果。Router缩小候选池，Planner组织步骤，两者都不能放宽服务端policy。

## 2. 数据流、控制流与信任边界

```text
浏览器 ──身份/请求──> API ──提交Run──> Agent运行时
                                      │
              History/Memory ──限量───┤
              Knowledge ──授权检索────┤──> 模型提议/草稿
                                      │
                        统一Executor <┘
                           │校验/授权/固定审批/intent
                           ▼
                 Provider / 本地工具 / MCP bridge
                           │实际结果与result_ref
                           ▼
           结果回上下文 → Draft → Verifier → Final
                           │
            DB状态/动作账本/审计/事件 → 浏览器快照与SSE
```

模型看到必要的资源ID、公开字段和脱敏结果。keystore、真实路径、密钥口令、解密正文留在受控服务。输入文件和知识文档都可能含不可信文本；不能把其中“请忽略规则”转为system、审批或Memory。

**设计练习**：用不同颜色画可信身份、用户文本、文档、模型结果、MCP结果、密钥服务；给每条跨界箭头写“谁校验什么”。通过标准：能沿一次请求指出每个授权点和秘密停止的位置。

## 3. 同一系统的交付演进

| 交付阶段 | 控制与接口 | 新增能力/保留理解 |
|---|---|---|
| V1 | 手写有限Loop、直接业务函数 | 提议/授权/执行/反馈/停止，NDJSON |
| V2 | JSON API、DB、基础Web | 真实Run/Trace与资源归属，快照恢复 |
| V3 | 一个Crypto MCP Server | 业务函数复用，协议与模型调用逐层关联 |
| V4 | 固定审批、账本、最小Graph | 一种写动作、暂停/重放/崩溃核对 |
| V5 | 条件Retrieval、完整Verifier/Memory、SSE | 知识与上下文来源，引用与事实，事件恢复 |
| V6 | 补齐工具/MCP/图与完整交付 | 模型/场景/安全实验、完整UI与清洁复现 |

按00/05切片，目标编号是索引。MCP不需要等待写执行器或RAG；先统一只读入口，Server调用同一密码业务服务，最终授权在服务端。V4只用Tool分支，V5再加Retrieval。单进程先正确恢复，引入worker才做竞争/队列验收。

## 4. V1：手写Loop需要自己决定的接口与行为

| 部件 | 输入 | 输出 | 本人必须决定的边界 |
|---|---|---|---|
| ModelClient | messages、当前工具schema、运行配置 | assistant消息、tool_calls、计量 | 协议版本、超时、最大响应、NDJSON累积 |
| ContextBuilder | 请求、授权历史、有限结果 | 送模型的消息序列 | 截断策略、秘密过滤、可信与不可信来源 |
| ToolRegistry | 本地工具与受信任桥接配置 | 可见工具schema | 名称唯一、能力范围、risk/permission来自本地 |
| Executor | ToolCall与可信运行上下文 | ToolResult与审计关联 | schema、权限、资源、预算、超时、结果校验 |
| LoopController | 模型结果、工具反馈、剩余预算 | 下一轮或明确停止 | 无调用、重复、失败、取消、总deadline |
| TraceWriter | 一次真实步骤/计量/拒绝 | 可定位记录 | 脱敏、截断、run/call关联 |

Ollama原生`/api/chat`的工具反馈使用`role:tool`与`tool_name`；保存assistant的实际调用消息，再反馈真实结果。应用生成内部call_id关联并保持同名工具结果顺序；不能直接套兼容端点的tool_call_id/delta字符串假设。实际报文以锁定版本Trace为准。[官方tool calling文档](https://docs.ollama.com/capabilities/tool-calling)

**自己写实现前的五项练习**：

1. 用真实非流式请求标注每个消息的产生者、用途、可信程度。
2. 画出正常单调用、多调用、工具失败、无工具结束四条路径。
3. 为steps/deadline/token/output分别写一个能触发上限的受控实验预期。
4. 解释自动重试与模型重新提议为何都要经过执行入口和预算。
5. 先做到1–4，再解析NDJSON；网络块、JSON行、完整工具调用不要混为一层。

证据：脱敏原始报文、消息回传顺序、停止原因、失败与成功对照、本人修改Loop的diff。文档不提供可直接粘贴的完整Loop代码。

## 5. Context：四种来源不要混用

| 来源 | 保存什么 | 生命周期/读取范围 | 权威性与限制 |
|---|---|---|---|
| History | 用户/模型/工具的会话消息 | 当前授权session，按预算截断 | 是对话历史，模型旧回答不是资源现状 |
| Run State | 当前节点、预算、pending action、结果引用 | 一次run/checkpoint；版本化 | 恢复控制流；真实副作用以账本/Provider核对 |
| Memory | 用户偏好与可追溯事实候选 | 按user/project跨session，可纠正删除 | 不保存秘密，不把文档命令当用户偏好 |
| Knowledge | 经授权的操作资料及chunk | corpus/version/index/ACL | 支持知识结论，不证明当前证书可信或密钥有效 |

Context预算包括system、用户问题、工具schema、历史、Memory、检索证据、工具结果、预留输出。每轮记录实际prompt/completion计量与剩余预算。超长结果存blob引用，只放必要摘要；摘要不能删除资源版本、单位、否定条件和待审批动作。压缩是独立实验变量，不能在比较模型时偷偷改变。

**练习**：在一次“检查证书并解释风险”中标注哪些来自证书当前解析、哪些来自规范、哪些来自用户偏好。通过标准：不靠历史或Memory宣布证书当前有效。

## 6. Router、Planner与RAG的职责

| 需求 | 合理路线 | 必须保留的判断 |
|---|---|---|
| 查看公开证书字段/摘要 | 只读工具 | 授权对象ID、实际Provider能力 |
| 问操作规则/术语 | RAG，必要时澄清 | 文档版本、有效引用、无证据拒答 |
| 密钥状态/失败排行 | 固定query_database或元数据工具 | 固定query_id、可信tenant过滤、无任意SQL |
| 加密/轮换/测试签发 | 工具提议→固定审批→执行 | 参数/资源版本锁定、真实artifact或新版本 |
| 记住/纠正偏好 | Memory操作 | 来源、用户确认策略、可删与隔离 |
| 多项组合 | 有限计划串联各路线 | 每步依赖与成功谓词，不绕过单步授权 |

Planner输出供运行时检查的步骤提议，而非shell脚本。计划变更影响写动作时重新绑定审批。Retrieval是证据获取，不把检索文本当工具执行指令。V6 Router实验固定候选池，记录路由漏召与后续选错工具分别导致的失败。

## 7. Tool与MCP桥接

canonical工具、风险、审批与执行顺序按结构文档，业务输入输出按06。MCP只负责互操作，外部工具描述/annotation不能覆盖本地permission或read_only。桥接应保存外部server/tool名称、canonical ID、SDK/协议与本地policy版本。

MCP的Tools、Resources、Prompts是不同能力：本项目用工具执行，Resource提供受控内容，Prompt提供提示模板；后两者仍是不可信输入，需要授权和内容边界。能力协商与连接生命周期依锁定实现，不因为新协议文档存在就默认本机支持全部特性。[MCP官方架构](https://modelcontextprotocol.io/docs/2026-07-28/learn/architecture)

**验收**：同一调用经本地与MCP入口时有相同canonical ID与本地策略；协议报错不变成success；工具列表变化与新增授权Server分开验证。

## 8. Graph设计卡：字段类别与节点合同

以下是字段类别与约束，不是完整State定义。学习者决定字段类型、reducer、并发合并和状态机，并写自己的取舍。

| 类别 | 最少需要的信息 | 约束 |
|---|---|---|
| 身份/版本 | run_id、可信user/project、graph/schema/config版本 | 客户端不可覆盖可信身份，旧checkpoint需兼容检查 |
| 控制/预算 | 节点、步数、deadline、停止/失败原因 | 有界循环，恢复后不重置预算逃避上限 |
| 上下文/证据 | 有限消息摘要、document/version/chunk/result_ref | 不存密钥和全文；撤权/删除后重新检查可用性 |
| 动作/审批 | pending action ID/hash、approval ID/状态引用 | 参数固定，与账本核对；不在State中自授权 |
| 草稿/验证 | draft_ref、Claim/Citation引用、Verifier报告引用 | 未通过不得展示为已验证final |

| 节点 | 输出合同 | 失败/恢复问题 |
|---|---|---|
| Router/Planner | 有限路线/步骤提议 | 路由错、计划超预算如何结束或澄清？ |
| Retrieval | 授权、版本化EvidenceRefs | 缺证据、撤权、旧版本不存在怎么办？ |
| Tool/Approval | 固定action引用与真实结果引用 | node重跑如何不创建第二动作？ |
| Draft | 回答草稿与绑定Claim/Citation | 草稿事实如何追溯？ |
| Verify | 必需检查、violations、修复建议 | unknown/N/A和fail如何区分？ |
| Final | 答案、引用、验证状态、终态 | verify未通过时怎样诚实展示？ |

thread_id=run_id表示一请求一工作流；会话历史单独由messages加载。若改成一session一thread，另写并发与映射规则。checkpoint schema、graph代码、动作policy和资源版本都要记录，不能混成一个prompt_version。

动态审批interrupt恢复使用`Command(resume=...)`；节点可能从头重跑，因此中断前后的副作用都要受账本与幂等控制。checkpointer的setup放部署迁移，恢复旧任务先查版本兼容。[LangGraph官方interrupt说明](https://docs.langchain.com/oss/python/langgraph/interrupts)

## 9. 固定审批与外部副作用

action_hash绑定身份/项目、工具版本、规范参数、资源版本与policy版本。审批身份来自鉴权；前端只提交approval_id/hash/decision，不提交风险或角色。发生变更则旧批准失效。结构文档是状态枚举与崩溃矩阵的唯一来源。

| 故障点 | 必须证明的行为 | 证据来源 |
|---|---|---|
| intent未提交 | 没有执行动作 | 账本与真实资源 |
| 待审批重启 | 展示原pending与hash，不默认同意 | snapshot/approval/action |
| 批准后执行前 | 领取原动作，不再生成新参数 | action/approval关联 |
| 执行中或外部完成未写回 | 核对job_id/幂等键，不盲重跑unknown | Provider/产物/账本 |
| 已完成后重复请求 | 返回已有result_ref | 相同action与产物hash |
| 有worker并发领取 | CAS/lease/fencing拒绝陈旧领取/结果 | 双worker与外部执行次数 |

V2简单同步默认断线cancel；V4持久化审批/后台任务默认detach，V5再完成SSE断线专项。显式取消是协作请求，外部状态仍需核对，不能收到cancel就伪报停止。独立worker是条件性扩展，未引入时标明未适用，不假称已测双worker。

## 10. Verifier、Trace与可观测性

Verifier读取真实工具最终状态、事实来源与Citation，不能只在回答里搜索数字。事实绑定subject/metric/value/unit/source；派生值记录输入与计算依据。引用的存在、定位、支持分别判定。必需检查unknown/skipped不能当pass；无引用闲聊/合理拒答可N/A。误报与漏报使用≥20正确/20错误双集，定义见02。

Trace同时记录提议、拒绝、执行与结果，不把它们合并。关联request_id/run_id/step_id/action_id/call_id与event_id，测total与各段耗时，人工审批等待单列。只保存必要脱敏参数和摘要；模型thinking如记录须同样审查敏感信息与访问权限。

**排错顺序**：前端快照/事件 → API身份/Run → 模型原始调用 → registry/schema → policy/approval → action账本 → Provider产物 → Claim/Citation → Verifier。按证据定位，不因模型回答错就先换模型。

## 11. 本文件完成标准

- 自绘一次只读、一次审批写动作、一次知识问答的序列图。
- 明确四类上下文、每种版本、所有秘密边界和停止条件。
- 用真实证据解释一次拒绝、一次失败、一次重启恢复及一次Verifier误判。
- 独立完成Loop修改、State设计和关键边界说明；AI只能审查本人核心实现。
- 设计与结构文档/实际代码差异有迁移记录，未实现能力不标完成。

## 12. 阶段通过与技术全表通过

V3单Server可进入V4，不等目标8三职责全表；V4一写动作和恢复通过可进入V5，不等所有CSR/签发或知识引用。对应目标全表及稳定任务范围仍须在指定补齐阶段完成，见00分配表与05导航。每次新增能力都重新检查已有授权/固定审批/结果与预算，不允许后续框架改变已验证边界。
