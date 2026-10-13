# V6 完整实验与交付

本阶段基础预算**138h**；实现成果：补齐工具/三职责MCP/专项验收、模型与场景实验、完整UI/部署/恢复。先读实现目标与当前切片，再执行详细任务；完成标准以实际证据为准。

## 实现目标与学习结果要求

补齐全部技术专项、签名/轮换/CSR/测试签发及三职责MCP，再锁定完整工具池做模型与Scenario实验。完成前端专项、安全回归、干净Ubuntu部署与备份恢复；Demo成功不是毕业，当前生产PKI/HSM等扩展不计入本轮。

| 需要学习的技术 | 学习结果要求 | 独立实现与排错证据 |
|---|---|---|
| 完整密码工具与Provider能力 | 实际完成签名验签、版本轮换、CSR/受限测试签发并保留审批/状态边界 | 独立数学/身份/字段/版本对照，重复与越范围拒绝 |
| 三职责MCP与完整工程专项 | 补Tools/Resources/Prompts、授权配置刷新、API/DB六查询与Graph全表 | 实际直调/协议/权限/版本证据；worker仅在引入时验证竞争 |
| 小模型、Router、Context消融 | 固定环境/工具池/数据/预算，比较四必做配置各3次与独立变量 | 质量、逐case差异、耗时/tokens/VRAM、换模成本与结论限制 |
| Schema、人工gold、Fixture与冻结 | 准备真实资源/引用，按source/group隔离dev/test，不为结果放宽正确断言 | RAG≥50、Tool≥50、100–180综合人工审定；draft不能冒充frozen |
| Scenario Runner、指标与配对回归 | 驱动turn/approval/fault/restart/resume/assert/cleanup并隔离每次namespace | 完整缺失/重复/超时与实际副作用报告，配对差值/区间与失败case |
| Agent安全与本人对抗性验证 | 本人定义威胁/授权边界，区分拒绝尝试和实际越权动作 | 注入/路径/SQL/命令/SSRF/审批重放/跨用户/Memory/MCP反例；实际越权=0 |
| 完整React交互与Ubuntu交付 | 真实状态/审批/恢复/引用/Memory/下载可用；锁版本、最小权限、健康与迁移 | 干净目录复现、重启持久化、下载撤权、安全渲染与网络限制 |
| 备份恢复、版本与毕业证据 | 恢复DB/文件/index/keystore/checkpoint且核对unknown，不静默重复动作 | 三条综合路线与A–J能力矩阵；本人解释、改需求、排错均有证据 |

## 必须独立回答的关键问题

这些问题必须由你结合自己的实现作答，AI只审查。记录在代码仓库docs/progress.md，写清场景、自己的理由、真实证据与未覆盖边界；只背定义或复制AI答案不算通过。

| 编号 | 必须自己回答的问题 | 回答达到标准所需的说明或证据 |
|---|---|---|
| Q01 | 签名验证通过为什么不能直接宣布签名者身份可信？ | 分开数学结果、公钥来源、证书/信任条件与未检查项 |
| Q02 | 密钥轮换后，新加密和旧密文解密分别关联哪个版本？ | 真实新旧元数据、产物版本与允许/拒绝行为 |
| Q03 | CSR与证书有什么区别？测试CA为什么限制SAN/用途/有效期？ | 自己的固定profile、审批payload与实际签发字段对照 |
| Q04 | 现在已经补齐哪些canonical工具？Provider不支持的能力怎样呈现？ | 实际能力列表/版本和独立结果，不能依据模型猜测 |
| Q05 | 三个MCP职责为什么不等于三个Provider？Resource和Prompt如何验收？ | 部署/映射/授权/不可信内容边界和实际生命周期 |
| Q06 | 四模型配置比较时必须固定哪些变量？哪项变化算另一实验？ | 自己的配置/环境/工具/数据hash与消融表 |
| Q07 | 质量变好而延迟/显存变差时，怎样给出有边界的模型结论？ | 逐case、n、波动、实际成本与适用任务，不能只报均值 |
| Q08 | Router漏掉正确工具与模型选错已候选工具怎样分别计量？ | 提议/候选池/执行与实际成功的分层记录 |
| Q09 | 为什么test或heldout不能反复用于调prompt？ | source/group切分、实际调参记录与新版本规则 |
| Q10 | draft、ready和frozen分别说明什么？人工审定字段如何证明？ | 真实审核者/日期/fixture/证据，不把AI生成当人工验证 |
| Q11 | RAG/Tool专项和综合题复用时怎样避免重复计数？ | case ID复用与题库规模/类别清单 |
| Q12 | allowed_tool_plans与gold_calls occurrence怎样表达多个合法计划？ | 自己审定的多解与重复工具调用例子，不只看工具名字 |
| Q13 | Runner中的approval、fault与resume为什么不能当普通消息发给模型？ | 真实控制边界、pending hash与状态断言 |
| Q14 | 每次case/repeat如何隔离Memory、文件和索引？cleanup能删哪些数据？ | namespace划分与只清理本次资源的证据 |
| Q15 | 缺失、额外、重复、超时结果怎样进入报告？ | 一对一配对检查、分母和逐case失败，不静默跳过 |
| Q16 | 拒绝了一次越权提议与真实越权执行分别怎样判断？ | 策略拒绝记录与资源/执行计数，实际副作用不能被平均率遮盖 |
| Q17 | prompt注入文本到执行器之间有哪些真实防线？ | 本人设计反例、授权点和实际拒绝，不能只依赖提示词 |
| Q18 | 为什么前端按钮禁用、健康检查绿色与CI通过都不是完整安全证明？ | 各自覆盖范围及剩余服务端/业务证据 |
| Q19 | 干净目录复现需要固定哪些版本和配置？秘密如何单独提供？ | 实际安装/迁移/启动/smoke与安全配置，不能只有现有机器截图 |
| Q20 | 备份同时包含DB、文件、index、keystore和checkpoint时如何核对一致性？ | 恢复顺序、版本/引用/产物对照与unknown处理 |
| Q21 | 未引入worker时如何登记竞争专项？引入后新增哪些恢复风险？ | 不适用理由或实际lease/fencing与双worker执行证据 |
| Q22 | 你能脱离教程完整解释并修改哪条Agent业务链？哪些能力仍未验证？ | A–J正常/失败/个人证据、本人变更回归与明确扩展清单 |

## 分步任务与技术掌握标准

先按当前切片实现最小输入输出，再补齐技术表。本阶段首次运行、正常/失败/权限、本人解释与独立修改分别验收；未实际运行不签收。

**当前138h**包含跨阶段补齐、固定工具池后的模型实验、正式Runner/安全、前端专项、部署与综合15h。先按“先补跨阶段目标”补齐业务池，再做模型/数据实验，最后完善交付。小用例一直收集，正式100–180题在这里逐条审定与冻结。

### 先补跨阶段目标

| 回看位置 | 本次任务 | 全表完成条件 |
|---|---|---|
| 第6.1 API | 目标3剩5h，M2 06–07全链路回归 | 请求/事件/断线/取消/身份合同完整 |
| 第6.2 DB | 目标4剩10h，M2 13及全部六查询/索引/事务/角色复核 | 时间窗口参数化、llm_calls真实计量与权限证据 |
| 第8.1执行器 | 目标7剩10h，M4 03轮换、04 CSR/测试签发、06≥50Tool题 | 已开放全部工具实际结果、版本、审批/失败齐全 |
| 第7.1 MCP | 目标8剩8h，M4 09–10与11新端点 | 三职责Server、Resource/Prompt、两类刷新 |
| 第8.2 Graph | 目标9剩10h，图/schema兼容与全范围回归；条件性M4 16 | 原pending恢复、未知核对；有worker才竞争/lease/fencing |
| 第8.4安全 | 目标14剩15h，由本人完整威胁模型和回归 | 所有实际关键攻击面，实际越权0 |

如当前Server只开放两只读工具，补写工具后同步registry/schema/审批/用例，再固定候选池做下列模型实验。没有真实材料的fixture不能标resolved；不能为冻结降低断言。


### 目标11：小模型、Router 与 Context 优化（15h）

**进入条件**：V6：目标7/8补齐后工具池稳定，冻结同一任务集，再做四配置实验。

**Agent目标**：用质量和成本确定小模型适用边界，避免先凭印象选框架。 对应详细任务：**M5 05–08**。

**技术点掌握程度标准**

| 技术点 | 能解释 | 独立做到 | 排错与边界 | 验收证据 | 后置内容 |
|---|---|---|---|---|---|
| 模型基线/配置 | 参数量、量化、模板、think、上下文各是变量 | 固定digest、采样、工具池、fixture与Judge | 冷加载/换模不从端到端成本隐去 | 配置hash与计量来源 | 微调/蒸馏 |
| Router/候选池 | 路由减少选择面也可能漏正确工具 | 4B±router、9B±router四必做组各3次 | 路由错与选工具错分开，不用test调阈值 | 12次完整实验与case表 | 27B第五组可选 |
| Context压缩 | 摘要可能丢约束，关键版本不可删 | 单独消融并保留审批/资源/证据必要信息 | 丢单位、版本、否定条件能发现 | 前后失败与token对照 | 自动长期压缩 |
| 质量/成本 | 准确率、延迟、token与显存取舍 | 逐次/均值/方差与分任务结果 | 不挑最好一次，seed不承诺逐bit一致 | 哪些任务4B够用的有界结论 | 大模型部署调优 |

**学习与实现顺序**：基线冻结 → router单变量 → 四组各3次 → 压缩单变量 → 分任务失败分析。

**必须独立回答**：路由收益来自什么？为什么同Judge和同工具池重要？什么证据支持升级到9B？

**独立练习**：找一题router降低质量并解释漏工具原因，手查在线token来源。

**退出条件**：四组12次为必修，27B可选；适用边界和升级依据有证据，不要求小模型无条件胜出。

**具体实践与逐项操作**


M5 05–08：四必做配置各3次；压缩单变量，27B选修。工具池与固定项在“先补跨阶段目标”完成后冻结。

学习固定变量、单变量消融、配对结果、样本量、方差、冷/热启动与 GPU 资源。关注本项目的证书/摘要/密钥任务，分别验证意图、参数、真实执行与结果解释。

**技术点掌握程度标准**

| 技术点 | 本阶段必须能独立做到 | 练习与验收证据 | 可后置内容 |
|---|---|---|---|
| Baseline 与固定变量 | 记录模型身份/量化、prompt、工具池、fixtures、上下文和预算；同一评测只改目标变量 | M5 05 配置与数据 hash，能指出两个不可公平比较的配置差异 | 大规模模型榜单与训练实验 |
| Router 与模型选择 | 区分路由/工具候选筛选的作用和模型自身能力；保持明确开关，路由不越过权限 | M5 06 四组 4B±router、9B±router，保留路由决策和错路由实例 | 训练 Router、MoE 内部机制 |
| 消融与配对比较 | 每个 case 对齐比较；每组运行 3 次，报告逐次和汇总，不把一次成功当稳定提升 | 四组原始结果与按 case 的改善/退化表；说明随机性与样本局限 | 高级显著性检验、因果实验设计 |
| 上下文压缩 | 独立比较压缩开关；保留必要资源、版本和动作事实，不能压掉失败状态 | M5 07 与 Router 分离的实验及丢事实实例 | 学习型压缩、长任务自动摘要体系 |
| 延迟、tokens 与显存 | 区分端到端和模型耗时；能计算 p50/p95，说明样本量；记录冷/热加载与峰值显存 | M5 08 原始计时与汇总，说明换模成本及运行环境 | 内核级推理优化、模型量化训练 |
| 错误分类与改进决策 | 区分意图、计划、参数、执行、解释失败；根据样本选择 schema/路由/提示改进 | 至少一组失败样本分析，说明质量改善是否抵消耗时增加 | 仅靠总体均分自动选模型 |

| 顺序 | 学习任务 | 固定条件 | 应报告什么 |
|---|---|---|---|
| M5 05 | 定义工具选择 baseline | 工具池、描述、fixtures、参数、Judge | intent、计划、参数、任务成功和失败类型 |
| M5 06 | 比较 4B±router、9B±router | 同族同量化、think/context/预算一致 | 每组 3 次，逐次及汇总结果 |
| M5 07 | 另测上下文压缩 | 与 router 单独开关 | 哪类误调用减少或增加 |
| M5 08 | 记录成本 | 同环境与串行路线 | 端到端 p50/p95、tokens、峰值显存、换模/加载 |

router 是先缩小候选工具范围的组件，不是强制所有请求用某工具。27B 是选修；本机不能保证全部驻留显存，不能把 offload 延迟与 4B/9B 混作公平硬件比较。80 工具压力池也属选修，几个业务工具的结果不能证明大规模工具池能力。

**指标**：沿用 Intent/Tool/Argument/Joint/Task Success；timings 带样本数与失败耗时。小模型能力不足时先缩小工具池、明确参数说明、增加缺失信息澄清与确定性校验，再比较改动；不要通过给模型更大权限掩盖错误。

**独立练习**：找一条错误参数用例，只改工具说明，在 dev 测试是否改善。test 不用于反复选择 Prompt。

### 目标13：Eval 数据、Scenario Runner 与回归（20h）

**进入条件**：从V1收集小用例与成功条件；V6用20h完成Runner、100–180综合题、冻结和回归。初期手动case不冒充正式题库。

**Agent目标**：把单次Demo变成可重复实验，定位改动收益与回归。 对应详细任务：**M5 09–13**。

**技术点掌握程度标准**

| 技术点 | 能解释 | 独立做到 | 排错与边界 | 验收证据 | 后置内容 |
|---|---|---|---|---|---|
| 成功谓词/schema | proposed/executed/denied、答案与状态分别验证 | 每题有条件、真实fixture/证据和审核来源 | min_citations=0或verifier_passed单项不证明成功 | 人工审定与frozen校验 | 自动合成即正式gold |
| 数据/split | 变体与同source分组会泄漏 | 100–180综合题，近似组整体切分 | RAG≥50/Tool≥50可复用ID但不重复计数 | 分类/去重/分组清单 | 大型benchmark平台 |
| Scenario Runner | 对话与带外approve/fault/resume不同 | fixture→turn→审批故障→断言→cleanup | 实验/重复user/project/索引/Memory空间隔离 | 正常/失败场景记录 | 通用测试编排服务 |
| Compare/CI | 条件分母、N/A、invalid、pp区别 | 一对一case结果，配对比较，合同/mock/GPU分层 | 缺结果、只跳失败、改gold不重基线阻止报告 | 逐case差异与CI记录 | 统计工具全体系 |

**学习与实现顺序**：审定小批 → Runner与cleanup → 补齐全类100–180 → freeze → baseline → 变更compare。由你在代码仓库积累和审定评测记录，小批草稿不算完整验收。

**必须独立回答**：怎么定义加密任务真正成功？为什么只换session不能隔离Memory？frozen和draft有何区别？

**独立练习**：手算条件参数准确率；引入一条回归并用报告定位，不修改正确gold。

**退出条件**：正式数据无未解决fixture/TODO，结果完整；安全实际越权任一条阻止通过。

**具体实践与逐项操作**


回收V1草稿、V2简单驱动、V4人工故障演练，按M5 09–13补真实fixture/gold、隔离Runner/cleanup、100–180题与配对compare。前面的小批验收不被自动视为frozen。

学习 fixture、gold、success predicate、dev/test、group split、hash、scenario 与 cleanup。你需要一个能驱动多步动作的 Runner；草稿 schema 校验器不是应用 Runner。

**技术点掌握程度标准**

| 技术点 | 本阶段必须能独立做到 | 练习与验收证据 | 可后置内容 |
|---|---|---|---|
| Fixture、gold 与成功断言 | 构造受控资源与固定时钟；审定预期计划、事实、授权和副作用，不只比答案字符串 | M5 09 每类样本有真实来源/状态预期；实际资源与期望状态逐项审定 | 自动生成大规模 gold |
| Dev/test、group split 与 hash | 相关文档/场景按组划分，避免同源泄漏；记录数据/配置 hash，测试集不用于反复调参 | 一份划分说明和实验 manifest；知道修改数据后哪些结果不可直接比较 | 复杂数据版本平台 |
| 单条 Runner 与隔离清理 | 为 case 建独立 namespace；驱动请求、记录、断言与 cleanup，超时失败同样记结果 | M5 10 单例正常/失败/超时记录，清理后无遗留资源且不删别人的资源 | 分布式评测队列 |
| Scenario 与故障控制 | 驱动 turn/approve/fault/restart/resume/cancel；控制动作与用户自然语言分开 | M5 11 审批和恢复场景包含实际状态断言；模型没有收到故障控制指令 | 通用混沌工程平台 |
| 结果完整性与配对回归 | 每个 case 恰有一条结果，缺失/重复/额外均报错；逐样本对比，不只看平均值 | M5 13 固定 hash 的结果差异，安全退化能定位到 case 并阻塞 | 完全自动判定全部语义等价 |
| CI 与质量门槛 | 将已审定可重复的检查接入 CI；区分配置失败、程序失败和模型质量变化，不通过放宽断言求绿 | 100–180 条审定综合用例清单与回归报告；失败任务保留日志 | 多平台矩阵与复杂发布流水线 |

| 顺序 | 学习任务 | 产物 | 验收指标 |
|---|---|---|---|
| M5 09 | 为密码业务建数据记录 | 密码业务 fixtures、工具枚举、证据与用例 | schema/validator/registry 同步，真实来源与状态断言齐全 |
| M5 10 | 单条 Runner | 建 namespace→请求→记录→断言→cleanup | 每个 case 唯一结果，失败/超时不遗漏 |
| M5 11 | Scenario Runner | turn/approve/fault/restart/resume/cancel | 带外控制由 Runner 驱动，不发给模型当普通问题 |
| M5 12 | 扩充并逐条审定 | 100–180 条综合用例 | 无 TODO，真实证据与明确成功条件 |
| M5 13 | 比较与 CI | 固定 hash 的 case-level paired compare | 缺失/重复/额外结果拒绝，安全失败阻塞 |

评测使用本项目schema v3，工具枚举与结构文档一致。起步草稿都保留draft；应用registry落地时核对资源、参数、计划、事实与成功条件，逐条审定后才能冻结。

综合用例建议先达到 100 条：Intent10/RAG15/Tool15/Database10/Workflow15/Memory10/Security15/Complex10。完整 180 条建议分布：20/30/25/20/20/15/25/25。RAG≥50、Tool≥50 是各能力专项题库；综合集可以从其中抽取已审定题，但要记录复用 ID，不能把同一题重复计成独立新样本。

**正式冻结前**：你逐条核对 gold/预期事实/状态断言，来源真实、fixture resolved、无占位符、按组划分；一份配置含 dataset/fixture/corpus/index/schema hash、git_commit、模型 digest、环境与 Judge。实验+重复+case 的 namespace 必须隔离用户、资源与 Memory。

**报告指标**：每项说明适用 n、通过/失败、N/A 原因与 case-level 回归。Task Success 是所有必要成功与安全条件成立；安全场景看实际执行和资源快照。审批等待另计，不混系统延迟；离线 Judge 成本不混在线 tokens。基础设施事故作废整批或明确 invalid，不只跳过失败题。

**独立练习**：让某个 case 缺结果，验证 compare 拒绝报告；更改 fixture 后证明不能直接和旧 baseline 配对。

### 完成目标十五全栈专项

回[V2目标15完整表](V2-WEB.md#目标15reacttypescript-与-agent-交互30h)，使用目标15剩15h补React异步/清理、历史资源/审批/Memory/来源/Verifier/错误/unknown体验。把M6 01–07所有范围逐一跑：正常、空、拒绝、冲突、断线、刷新、取消、撤权下载、Verifier失败。不重复计V2已完成15h，不因为页面存在就认为TS与异步状态已掌握。


### 目标16：配置、部署、监控与恢复（15h）

**进入条件**：V6完整功能联调后15h部署/恢复；V2已有Ubuntu开发运行和Web构建，不能把首次看网页拖到这里。

**Agent目标**：让他人从清洁目录复现，服务故障能定位、恢复与核对。交付细节见V6交付章节。 对应详细任务：**M6 08–12**。

**技术点掌握程度标准**

| 技术点 | 能解释 | 独立做到 | 排错与边界 | 验收证据 | 后置内容 |
|---|---|---|---|---|---|
| 版本/配置 | 源码tag、Python lock、镜像/model digest各锁什么 | 干净目录恢复，不提交真实.env和秘密 | 缺配置/Provider明确失败或受控降级 | 复现清单与快照 | 多平台发行 |
| Compose/网络 | 启动不等于ready，host与bridge不同 | profiles/健康/迁移/volume/限制，Web/API可访问 | 内部服务不无条件对外，容器localhost错误可定位 | 端口、ready与恢复记录 | Kubernetes |
| 可观测性 | request/run/action/call关联，状态与耗时不同 | 串起API/模型/工具/DB/前端，脱敏与日志轮转 | 耗时/未知动作/磁盘问题能定位，不能靠重启猜测 | 一次故障诊断记录 | 完整APM平台 |
| 备份/恢复 | DB、artifact、index、keystore、checkpoint相关 | 固定版本备份，隔离目录恢复并核对引用 | DB恢复不等于解密恢复，unknown先核对 | 恢复演练与hash检查 | 跨区域容灾 |

**学习与实现顺序**：实际启动命令 → 配置/版本锁 → 迁移与健康 → 网络 → 清洁clone复现 → 备份恢复。API不持有migration/bootstrap秘密或Docker socket。

**必须独立回答**：容器启动为何不等于ready？只备份数据库为何不够？恢复时为何不能自动执行unknown动作？

**独立练习**：模拟依赖未ready并诊断；在隔离目录恢复一份备份，核对元数据与产物。

**退出条件**：清洁目录安装/迁移/启动/smoke通过；重启与备份恢复有证据，CPU降级不标GPU基线，完成综合验收后标记m6-done。

**具体实践与逐项操作**


M6 08–12在隔离教学实例执行清洁clone复现、版本/网络/迁移/volume与备份恢复；首次前端运行已经V2完成。

学习镜像、Compose profiles、版本/digest、配置、迁移、volume、健康检查、网络、日志轮转与备份恢复。先把现有服务按层装配，Redis、对象存储不需要时不用增加。

**技术点掌握程度标准**

| 技术点 | 本阶段必须能独立做到 | 练习与验收证据 | 可后置内容 |
|---|---|---|---|
| 镜像与 Compose | 分清 image/container/service/volume；按依赖启动必要服务，固定验证过的版本与配置 | M6 08–09 在新目录按文档装配，记录实际镜像与依赖版本 | Kubernetes、服务网格 |
| Ubuntu 启停与进程托管 | 会查服务状态与日志；明确 host/容器中谁托管进程，停止和重启不留下多实例 | 保存实际路线的启动/停止/重启记录；需要 host 服务时再学对应 systemd 配置 | 通用 Linux 运维平台 |
| 配置、秘密与迁移职责 | 样例可复现，实际秘密受限挂载/配置；迁移账号与应用账号分开，不把秘密打入镜像 | 配置清单、权限与迁移日志，应用账号无 bootstrap/DDL 权限 | 自动秘密轮换与配置中心 |
| 网络、浏览器入口与 readiness | 理解 host 回环、容器内地址和端口映射；只开放必要入口；区分存活与依赖就绪 | M6 10 浏览器可访问，DB/模型端点受限；依赖不可用时 readiness 不报成功 | 公网发布时再补域名/TLS/反向代理；复杂网络选修 |
| Volume、资源与密钥持久化 | 识别 DB、artifact、加密 key blobs 的存储位置；重启后版本与资源引用仍有效 | M6 11 重启前后相同 Run/资源/版本可查询，实际文件存在 | 集群共享存储与高可用 |
| 日志轮转与基本可观测性 | 通过 run_id 定位跨模块失败，记录耗时与状态；限制日志空间，日志无秘密 | 一次端到端失败的排查记录与轮转/保留配置 | Prometheus、完整分布式追踪平台 |
| 备份与恢复 | 写清 DB、blobs、主秘密的恢复依赖；在隔离教学环境做恢复并核对资源，不只验证备份命令退出成功 | M6 12 恢复演练结果与缺少主秘密时的明确限制 | 多区域灾备、企业 RPO/RTO 承诺 |

| 顺序 | 学习任务 | 操作顺序 | 验收指标 |
|---|---|---|---|
| M6 08 | 固定环境与依赖 | 新目录 clone→配置→sync→模型/密码库验证 | 无隐含手工步骤，实际版本可查 |
| M6 09 | 部署服务与迁移 | DB→迁移→必要服务→API/worker→前端 | readiness 正确，应用无 bootstrap/迁移密钥 |
| M6 10 | 验证网络 | 前端/API 对外，其余内部或回环 | 浏览器可访问，DB/Ollama/GmSSL 服务不裸露 |
| M6 11 | 重启与持久化 | 保存测试资源→重启→查询 | 任务/资源/密钥版本记录保留 |
| M6 12 | 备份与恢复说明 | 元数据、加密 keystore、主密钥依赖分别说明 | 只恢复 DB 不冒充已恢复密钥能力 |

Ollama 默认在 Ubuntu `127.0.0.1:11434`，容器访问方式按 [README环境](../README.md#env-0) 核对；不能假设 host-gateway 能访问只监听回环的进程。密码适配服务与API不持有Docker socket，容器只挂载各自必要的受控资源。

验证时使用当前 Ubuntu 地址，不复制旧快照 IP：

```bash
hostname -I
ss -ltnp
```

前端/API 实际监听地址与反向代理策略要记录；浏览器访问后再验收鉴权和断线。生产式外部暴露和部署配置留在部署任务中审查，本地演示先用测试身份与测试资源。

**产物**：部署说明、配置模板、固定依赖、启动/迁移入口、smoke 与重启证据。不是只交一份 compose.yml。

### 综合业务验收（15h）

按下面顺序完成一条全链路，再复用到其他操作：

1. 上传测试文件，保存 file_id 与归属。
2. 请求摘要或证书检查，Agent 选择正确只读工具。
3. 请求使用某 key_id 加密文件，读取元数据并检查用途/状态。
4. 页面展示准确的影响范围，用户审批固定动作。
5. 执行一次，写动作账本与 artifact，Verifier 核对状态。
6. 请求获授权解密，结果下载后与原文件逐字节比较。
7. 轮换测试密钥，证明新加密绑定新版本，旧密文按原版本获授权解密。
8. 注入一次明确的崩溃并恢复，证明无重复副作用或进入明确核对状态。
9. 在页面查审批、工具结果、拒绝/失败、版本与审计。

另演示一条公开证书解析/验证或测试 CSR/签发流程。若某项延后，写明缺口，不能用 Chat 页面“看起来能聊天”代替密码业务验收。

**最终指标**：完整场景的全部成功谓词成立；关键确定性密码结果与独立核对一致；恢复不静默重复动作；安全实际越权为 0；未检查项明确标记；干净 Ubuntu 环境能按文档重现；Windows 浏览器能看到全链路。标签 `m6-done` 只在这些结果完成后建立。

**V6出口**：所有16目标表必修项与P0通过，A–J毕业矩阵正常/失败/本人证据完整，正式实验/安全与清洁部署/恢复通过。选修不适用有理由，所有技术标签按学习总览的专项标签条件创建，不以累计小时或一次Demo代替。

## 本阶段的接口与实践细节

以下内容属于本阶段，按任务用到的部分查阅；涉及后续能力的字段仅作为扩展合同，当前切片不要求提前全部实现。

<a id="api-8"></a>
<a id="api-8-8-全栈联调验收表"></a>
### 全栈联调验收表

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

完成证据：同一run_id的curl/API响应、DB状态、SSE与浏览器行为；UI截图只能作为辅助。系统与本人TS/异步理解分别按对应阶段目标表标准验收，不只检查页面好看。

<a id="eval-1"></a>
<a id="eval-1-1-模型与推理配置"></a>
### 模型与推理配置

| 角色 | 起点 | 规则 |
|---|---|---|
| Controller A/B | qwen3.5:4b / qwen3.5:9b，同量化(Q4_K_M) | 比参数量时同模型族、template、思考模式；Qwen3.5 无 8B 尺寸，对照取最近的 9B |
| 可选 C | qwen3.5:27b | 17.48 GB > 可用显存 13.4 GB，必然 offload，延迟不可与 A/B 并列 |
| Embedding | bge-m3 dense，1024维 | Ollama 仅 dense；learned sparse 另用 FlagEmbedding |
| Reranker | BAAI/bge-reranker-v2-m3 | CPU/GPU 是独立环境变量，必须记录 |
| Judge | 固定的独立模型/版本 | 所有待比较 Controller 使用相同 Judge |

比较 4B/9B 时可用固定 27B Judge；比较包含 27B 时另选全组统一 Judge 或人工审定，不能只给 27B 组换一个 9B Judge。不同模型并不能保证无偏；Judge 随机顺序、隐藏系统身份，与人工标注校准。不能假设大模型 Judge 一定偏严。

`qwen3.5:4b` 出厂采样参数为 `temperature=1 / top_p=0.95 / top_k=20 / presence_penalty=1.5`；下面的固定值属于**实验配置**，必须与出厂参数分开记录，不能混为一谈。

固定 think=false、temperature=0（或明确预设）、seed（若后端支持）、num_ctx、输出预算、MAX_STEPS、工具池、router、模板、KV cache、并行度。即使固定 seed 也不承诺 GPU 结果逐 bit 相同。结构化输出不能代替执行前 schema/业务校验。

16GB 应监控桌面/其他进程、权重、KV cache 和 PyTorch 开销，不能将下载大小当占用。OLLAMA_MAX_LOADED_MODELS=1 只限制 Ollama，自行启动的 reranker 仍会占 GPU。单槽下实时 embed/rewrite/controller 会换模，延迟计入生产端到端；检索-only 预计算 query embeddings 是独立实验，不能声称代表在线延迟。

<a id="eval-3"></a>
<a id="eval-3-3-agent-指标"></a>
### Agent 指标

| 指标 | 口径 |
|---|---|
| Intent Accuracy | 有 gold_intent 的适用样本；预测需记录在结果 |
| Tool Exact Match | 与任一 allowed_tool_plans 完全一致，顺序/重复敏感 |
| Tool Set Match | 与任一允许计划的工具集合一致；不证明调用次数/顺序正确 |
| First Tool Accuracy | 首工具属于允许计划首项；空计划双方无调用才通过 |
| Argument Accuracy (conditional) | 工具计划正确且有 gold_calls 时，按对应调用的字段/语义比较 |
| Joint Call Accuracy | 所有需验证的工具/调用次序/参数都正确，占适用总样本比例 |
| Task Success | 全部显式成功谓词和安全必要条件成立才成功 |
| Unsupported Claim Rate | 无支持原子事实/全部事实，固定 Judge、样本量与区间 |
| Unauthorized Action Rate | 实际执行越权动作的 Security 场景数/有效 Security 场景数 |

必须分开 attempt、denied 与 executed：模型提出路径越界调用而执行器拒绝，可以安全通过；真实读取越权文件一定失败。intent_security 标签只是数据标签，不授权也不阻止动作。Unauthorized Action Rate 必须为0且逐例无副作用；有限样本的0不证明系统没有任何安全漏洞。

gold_calls 按 tool_id + occurrence 绑定参数；多解可给参数约束而非全文字符串。同一工具多次调用分别用occurrence表达。字段缺失按 schema defaults 规范化，不能把任意字符串都小写或把所有数值字符串强制转类型。单位固定 SI：MB=1,000,000 bytes、GB=1,000,000,000 bytes；MiB/GiB 为二进制，文件上限1 MiB对应1,048,576 bytes。

Task Success 使用 success_criteria：must_call_tools 为 proposed attempt 层；must_not_call_tools 禁止提出；must_execute_tools/must_not_execute_tools 为实际执行层；allowed_tool_plans 为计划层；final_answer_all_of 与 any_of 明确区分逻辑；expected_values 绑定 subject/metric/unit/数值与容差；state_assertions 验证资源/审批/恢复/Memory 状态。

关键词只适合作为辅助，拒答不能要求同时出现“未找到”“没有找到”“未提及”。min_citations=0 单独不是有效成功谓词；verifier_passed=true 单独也不能证明答案正确。不会定义成功条件的用例保留 draft，不拼一个弱规则使它进 baseline。

<a id="eval-4"></a>
<a id="eval-4-4-延迟token-与显存"></a>
### 延迟、token 与显存

串行运行 baseline；并发实验单列。报告 total_ms、time_to_first_token_ms、time_to_verified_final_ms、retrieval/rerank/LLM/tool/verify_ms。LLM load 与推理分开，warm total 仍包含流程中真实换模。人工审批等待不混入系统 latency，单报 approval_wait_ms；自动审批 fixture 只能批准具体 action hash。

每次配置预热固定模型和固定路径，冷启动另外测。p50/p95/max 是基本报告，p99 在小样本时不稳，应带 n 与计算方法且不作硬门槛。超时/失败也记录耗时，不只统计成功题；并行分段耗时之和可能超过 wall clock，要注明。

token 从每次 llm_calls 实际返回的 prompt/completion 计数聚合，区分 Controller、rewrite、Memory、Verifier 和离线 Judge。Judge token 不加入在线 Agent 成本；不要用不匹配 Qwen 分词器的 tiktoken 估计充当实测值。记录 think/template 与 token 来源。

显存在**整次任务**周期采样，GPU总峰值、空闲基线与进程归因分别记录；Ubuntu 内用 `nvidia-smi --query-compute-apps` 做进程级归因，无法精确归因时明确限制，不只看第一个任务或加载瞬间。记录 Ubuntu 内可见显存与实测空闲占用，不用宿主机记录值代替。

<a id="eval-5"></a>
<a id="eval-5-5-数据与实验冻结"></a>
### 数据与实验冻结

最终目标 180 条：Intent20/RAG30/Tool25/Database20/Workflow20/Memory15/Security25/Complex Task25。预算不足可先冻结100条，必须列各类样本与缺口。本项目起步草稿用于示范记录结构，正式题库从证书、摘要、加解密、密钥与操作知识中逐项审定；复用问题记录ID，不重复计为独立新样本。

合成问题仅产生 draft；逐条审定 gold/关键成功条件并记录 verified_by/reviewed_at。20% 抽检只决定整批是否需要返工，不能把剩余80%标为“human verified”。近义变体、同一 source/template/场景组整体进入同一 split，避免 dev/test 泄漏。

每次报告固定 dataset/schema/fixture/corpus/index hash、git_commit、环境锁、模型 digest、配置、Judge 配置与校准集。freeze 要检查没有 TODO、有效 fixture、证据清单和审核；可选工具组更改必须同步 registry 与测试，不悄悄改 gold 适配模型结果。

结果保留 predicted_intent、proposed_calls、executed_actions、denied_attempts、retrieved_chunk_ids/版本、claims/citations、state_assertions、verifier、error、timings、tokens 和测试用例 ID。结果按 dataset ID 一对一关联；缺失/额外结果、重复 ID 是无效报告。

<a id="eval-6"></a>
<a id="eval-6-6-场景-runner"></a>
### 场景 Runner

```python
async def run_dataset(dataset, config, experiment_id, repetition):
    results = []
    for case in dataset:
        namespace = f'{experiment_id}/{repetition}/{case.id}'
        env = await fixture_manager.create(case.fixture_refs, namespace)
        try:
            if case.scenario:
                # turns 共用逻辑用户，session keys 可不同；按步骤驱动审批/故障/恢复
                result = await scenario_runner.run(case, env, config)
            else:
                result = await agent.run(case.question, user_id=env.user_id,
                                         session_id=env.new_session())
            results.append(await evaluate_case(case, result, env))
        finally:
            await fixture_manager.cleanup(env)
    return results
```

这是应用侧待实现接口，不是本包已有 runner。namespace 必须进入测试 user/project/session/文件/collection 的映射；只给独立 session_id 不能隔离长期 Memory。带外场景动作由测试驱动执行，不能把“Session2”“kill进程”等说明作为普通用户 question 发给模型。

<a id="eval-7"></a>
<a id="eval-7-7-比较统计与-ci"></a>
### 比较、统计与 CI

同一冻结数据/环境/Judge 做配对比较，配置至少3次，报告逐次结果、均值、方差和区间。Task Success 的百分点用 pp：40题的一题=2.5pp，180题的一题约0.56pp；-2pp 阈值必须结合样本量、case 回归和置信区间解释。重复结果不允许只挑最好一次；多数投票单列为一种策略。

冻结测试集禁止用于选 prompt/router threshold；用 dev 选配置，test 做最终报告。Judge 先生成所有配置结果，再统一离线判定，避免换模污染在线耗时。Judge 与人工一致率先用至少20条双标样本初测，低于80%时审查类别分歧、修规则或标指标不可靠；不能只改 Judge 直到偏好自己答案。

CI 普通任务跑校验、mock 场景和确定性安全测试；本地 GPU 任务用 frozen。compare 检查全部 hash 相同，列 case-level regressions 与通过数；安全实际越权任何一条失败阻塞。性能门槛以本机 baseline 后确定，不在未测量前声明固定500ms保证。

<a id="eval-8"></a>
<a id="eval-8-8-三个必做实验"></a>
### 三个必做实验

1. RAG 四组消融：同语料/切分/问题，检索质量与生成结果分阶段测；rewrite 单独开关。
2. 4B/9B±router，可选27B：同候选工具/上下文/think/Judge/fixture。压力工具池另列。
3. Verifier：已知错误与已知正确双集，覆盖实体错绑、单位、派生值、引用版本/定位/支持，TPR/FPR附样本量和漏报误报。

报告模板：问题、固定项与变量、环境与hash、适用样本数、结果/区间、失败用例、限制和下一步。按证据回答改动是否有益，不要求复杂配置必须胜过 baseline。

<a id="eval-9"></a>
<a id="eval-9-9-学习阶段与变更回归门禁"></a>
### 学习阶段与变更回归门禁

| 改动 | 最少重新检查 | 必须记录的影响 |
|---|---|---|
| Provider/profile/key version | 已知摘要/验签、AEAD往返认证失败、版本/产物 | 实际库能力、容器格式、nonce策略、审批失效 |
| Tool schema/描述/registry | 合同与相关工具题，审批/hash/权限 | canonical映射、occurrence与多解计划 |
| Model/prompt/router/context | 同frozen题配对compare与各配置重复 | 固定变量、逐case回归、质量/延迟/token/显存 |
| Parse/chunk/embed/retrieval | 定位/权限/更新发布与四组检索 | manifest变化；重新审定受影响gold后新版本baseline |
| Graph/State/checkpoint | 版本兼容、审批全分支、三处崩溃 | unknown核对与旧任务恢复，worker条件性测试 |
| Verifier | 正确/错误双集、引用与事实绑定 | TPR/FPR、n、漏报误报，不降低正确gold |
| Memory | 来源、改口/删除、跨用户/无关输入 | 事务去重与索引清理 |
| API/Web/部署 | 幂等、鉴权、SSE刷新断线、下载/恢复 | 同Run实际状态、网络/配置变化 |

个人学习通过标准见[Roadmap](../ROADMAP.md)，全链路与证据清单见[交付验收](V6-DELIVERY.md#delivery-1)。先有baseline再确定质量/性能阈值；示例百分点或耗时不是未实测的硬保证。实际越权必须0，任何相关确定性安全回归失败阻止发布。修数据错误需要证据、版本变更和重跑原配置，不覆盖旧报告；test不可用于反复调阈值。

<a id="eval-10"></a>
<a id="eval-10-10-小批学习验证与完整实验的时机"></a>
### 小批学习验证与完整实验的时机

| 交付阶段 | 当前验证范围 | 正式规模与剩余验收 |
|---|---|---|
| V1 | 证书/摘要、手写反馈、失败/预算，小case与成功谓词 | 不要求100题，也不称frozen baseline |
| V2 | 身份/上传/Run幂等、快照/UI、DB重启 | SSE/六查询专项分别V5/V6 |
| V3 | 两只读工具直调/MCP正常/拒绝/失败对照 | 三职责与完整端点V6 |
| V4 | 一种加解密、固定审批、结果状态、故障核对 | 全工具≥50题/完整安全/图兼容V6 |
| V5 | RAG≥50、四组检索、Verifier≥20错20对、Memory、SSE | 模型矩阵与全类Scenario V6 |
| V6 | 固定工具池后四模型配置各3次、100–180综合frozen、配对compare | 全部指标口径和正式门禁不降低 |

早期测试不是另加一套工时，属于当前目标练习；正式Runner/数据预算在目标13/V6，人工审定仍逐条。RAG/Tool专项可复用唯一case ID但不重复计数；基础权限/审批/秘密/状态错误从第一天就阻止当前功能交付。按[Roadmap](../ROADMAP.md)与[Roadmap](../ROADMAP.md)区分交付通过和全目标毕业。

<a id="delivery-1"></a>
<a id="delivery-1-1-四仓库布局与版本"></a>
### 四仓库布局与版本

```text
/home/zsw/work/agent_development/
├── Agent-development-doc/      本学习文档
├── Agent-development-code/     应用实现
├── openssl/                    OpenSSL官方源码
└── GmSSL/                      GmSSL官方C源码
```

四仓库同父目录、同级、独立Git历史。需要官方Python绑定源码时增加同级GmSSL-Python。实际用户名可替换，但保持结构；clone/build/test都在Ubuntu文件系统。源码与安装prefix分离；不要将两个密码源码塞进文档或应用仓库，不提交库构建产物/私钥/模型权重。

| 固定项 | 记录内容 | 验证用途 |
|---|---|---|
| doc/code | remote、branch、commit、dirty状态 | 确认使用同版规格与实现 |
| OpenSSL/GmSSL/绑定 | tag/commit、构建参数、prefix、动态库路径、能力列表 | 确认真实Provider支持，系统CLI与Python backend分开 |
| Python/前端 | 解释器、uv.lock、pnpm锁、Node/pnpm版本 | 新目录依赖复现 |
| 模型/检索 | Ollama版本、model digest、量化/template/think、embed/rerank、index hash | 防止环境变化冒充模型收益 |
| DB/Graph/policy | Alembic revision、graph/schema版本、policy版本 | 恢复兼容检查 |
| 服务镜像 | image tag+digest、Compose配置hash、profile | 依赖与部署可复现 |

版本清单不放数据库口令、API key、keystore解锁材料和完整带密URL。文档中的环境版本是日期快照，实际交付重新测量，不能声称一直最新。

<a id="delivery-2"></a>
<a id="delivery-2-2-最小交付包"></a>
### 最小交付包

| 位置（应用仓库建议） | 应有内容 | 完成标准 |
|---|---|---|
| README / docs/runbook.md | 当前有效安装、迁移、启动、停止、smoke、恢复命令 | 新终端/干净clone实际执行过 |
| .env.example / config | 所有已使用字段、默认值、必需/可选、秘密来源 | 与Settings/启动校验一致；无真实秘密 |
| pyproject / uv.lock / frontend锁 | 分阶段extras、固定依赖 | 不因加crypto extra覆盖已有extras |
| migrations | schema与角色迁移、checkpointer初始化方式 | 空库与已有库升级测试 |
| compose/镜像配置 | profiles、健康、网络、volumes、资源与日志限制 | 启动顺序与ready分别验证 |
| tests / eval runner | 合同/mock/集成/安全/专用GPU入口 | 分类执行；没有GPU不伪报实测 |
| docs/decisions | 本人阶段ADR | 记录证据、限制、重审条件 |
| reports/或外部结果目录 | 版本清单、逐case结果、Trace与恢复演练 | 引用路径可定位，敏感结果不公开提交 |

报告目录是建议，实际代码若用别名要在runbook说明。大blob、解密产物与真实.env不进入Git；评测fixture只使用审定教学资源。交付过程记录每一步状态“已验证/未验证/不适用及理由”。

<a id="delivery-3"></a>
<a id="delivery-3-3-服务与网络"></a>
### 服务与网络

| 服务 | 首版角色 | 监听/权限要求 |
|---|---|---|
| Web/API | 浏览器入口与鉴权 | Ubuntu受控网卡/端口，Windows浏览器可访问；仅开放需要端口 |
| Ollama | 本机模型服务 | Ubuntu127.0.0.1；host网络路线按[V2网络说明](V2-WEB.md#env-5)；bridge路线另配置可达地址，不默认全网开放 |
| PostgreSQL | Run/资源/审计/checkpoint | 回环或内部网络；app/query/audit/migration不同凭据 |
| Qdrant | 授权向量检索 | 内部网络，不能让浏览器直连绕过API |
| MCP | 受信任工具进程/端点 | stdio优先，日志stderr；远程另补鉴权/Origin/host |
| Provider/keystore | 固定密码API与受控材料 | keystore不是通用读取root，运行账号最小权限 |
| worker/Redis/对象存储 | 按需扩展 | 未引入不算缺核心；引入后验收领取、持久化与网络权限 |

默认方案可让API使用host网络访问Ubuntu回环Ollama，DB/向量库发布到回环；alternative bridge不能把容器127.0.0.1当宿主。两套网络选一套实际验证并在runbook写清。容器不是自动安全边界，API不持有Docker socket、bootstrap或migration秘密。

启动不等于ready；Compose的依赖条件/健康检查要与真实业务依赖对应，应用还需超时和明确失败。只有启用的能力列为ready依赖；GmSSL未启用可标disabled，已承诺工具却缺库必须标unavailable并拒绝调用。[Docker Compose官方启动顺序](https://docs.docker.com/compose/how-tos/startup-order/)

<a id="delivery-4"></a>
<a id="delivery-4-4-干净目录复现的逐步表"></a>
### 干净目录复现的逐步表

所有操作在Ubuntu；先保存现有改动与资源，不复用生产密钥，不删除原工作目录。给隔离教学实例分配不同端口、项目/用户/索引空间。

| 步骤 | 学习者操作 | 应得到的证据 | 不通过时先看 |
|---|---|---|---|
| 1 定位 | 核对四仓库remote/commit与目录，选教学实例 | 路径/版本清单，dirty说明 | clone/ref/大小写/权限 |
| 2 配置 | 从样例生成本地配置，注入测试凭据与受控root | 脱敏字段校验结果 | 缺变量、错误路径、误装到另一环境 |
| 3 依赖 | 用lock恢复Python/前端，按选定Provider构建/加载 | 解释器/锁/库能力记录 | 动态库路径、prefix、backend差异 |
| 4 模型 | 只安装当前阶段模型，真实请求核对digest/计量 | 模型请求与GPU/CPU状态 | listener、名称、内存/显存 |
| 5 存储 | 启动所需DB/向量库，迁移与角色，初始化saver | revision/权限/健康结果 | 依赖未ready、连接凭据、旧schema |
| 6 应用 | 启动API与Web，可选worker/MCP | live/ready、端口与配置版本 | 网络模式、CORS、可信端点 |
| 7 smoke | 认证、只读工具、snapshot/SSE、权限拒绝 | 同Run全链路证据 | 按[V5观察与排错章节](V5-KNOWLEDGE.md#agent-10)定位 |
| 8 浏览器 | Windows打开Ubuntu入口，审批/刷新/下载 | 交互与实际状态对照 | 防火墙/监听/鉴权/SSE |
| 9 重启 | 受控停启，检查pending/产物/历史 | 数据保留与恢复记录 | volume、checkpoint、动作账本 |
| 10 备份恢复 | 在独立实例恢复一份一致备份 | hash/权限/版本/旧动作核对 | 缺keystore、index版本、unknown |

首版先写实际命令，再由另一个终端按文档跑，修正遗漏；不直接假设代码目标目录src/lpa已经存在，当前packages骨架按结构文档映射。学习者须独立说明一个启动故障与一条修复依据。

<a id="delivery-5"></a>
<a id="delivery-5-5-数据与密钥备份恢复"></a>
### 数据与密钥备份恢复

| 数据 | 为什么需要 | 恢复核对 |
|---|---|---|
| DB/审计/审批/账本/checkpoint | 持久任务和动作决定 | revision/graph/schema兼容、引用、未完成动作 |
| 上传文件/artifact | 工具输入与真实产物 | ID/size/hash/版本/权限与DB关联 |
| corpus/parse/index manifest | 引用与实验复现 | 旧document版本/locator和active状态，必要时重建索引 |
| keystore加密blob | 旧密文与签名对应的密钥版本 | 材料存在、完整性、用途/状态、旧版本仍按策略可用 |
| 解锁材料/恢复秘密 | 解密keystore备份所需 | 独立安全保管；不随报告/Git提交 |
| 配置/版本清单 | 可解释恢复环境 | 固定库/模型/图/policy，脱敏且与实际对应 |

首版使用维护窗口：暂停新写动作，等待可确认动作结束，记录无法确认的unknown；再按所选DB与存储的受控备份方法取一致版本。加密blob、DB与文件必须有共同快照清单。教学用nonce分配持久状态也属于需要一致恢复的数据，恢复后不能回退计数导致旧key/nonce复用；采用安全分配/轮换策略后再开放写操作。

恢复顺序由实际依赖确定：隔离配置 → 固定服务/版本 → 迁移兼容 → 恢复DB及材料/文件/manifest → 核对hash与ACL → 检查pending/unknown → 只读smoke → 受控教学动作 → 最后重新开放写动作。旧批准若资源或policy版本不匹配必须失效；unknown核对前不得批量resume。

**必须实验**：重启数据不丢；从一份备份恢复一个已完成artifact与一个待审批Run；缺失key blob时正确拒绝解密而非编造成功。恢复用测试材料，不在原库上做破坏性演练。

<a id="delivery-6"></a>
<a id="delivery-6-6-三条综合验收路线"></a>
### 三条综合验收路线


<a id="delivery-6-路线a证书摘要只读闭环"></a>
#### 路线A：证书/摘要只读闭环

1. 上传公开教学证书和非敏感小文件，记录来源/hash/权限。
2. 问证书字段与文件摘要，查看模型提议、授权与实际Provider结果。
3. 用独立命令/已知向量对照，确认公开字段/摘要，而非只比两段模型文本。
4. 页面查看ToolResult、Run计量与Verifier；未进行的信任/撤销检查显示not_checked。
5. 用另一测试用户读取同资源必须失败；Trace不得泄露真实路径/秘密。


<a id="delivery-6-路线b固定审批产物版本与恢复"></a>
#### 路线B：固定审批、产物/版本与恢复

1. 查询教学key元数据，选明确profile与≤1MiB教学文件。
2. 提议加密或轮换，页面展示固定参数、key/resource/policy版本、hash与期限。
3. 拒绝一次，确认没有产物/版本变化；新提议批准后核对真实artifact/hash或新版本。
4. 刷新待审批、重复同决定、资源变更各验证，不能二次授权新动作。
5. 在执行前/中/后指定故障点演练恢复，核对账本与外部结果；不确认则unknown。
6. 加解密闭环按[V4认证加密合同](V4-APPROVAL-CRYPTO.md#crypto-6.1)验证往返/认证失败；轮换验证旧版本策略，秘密不进入模型/页面日志。
7. 补证书链验证或测试CSR/签发，区分自签/测试签发与生产信任。


<a id="delivery-6-路线c知识memory与验证"></a>
#### 路线C：知识、Memory与验证

1. 入库已审定PDF/MD/TXT操作资料，发布manifest。
2. 问一个可回答知识问题，点击引用定位，Verifier绑定支持的Claim；再问无答案问题。
3. 纠正/删除显式偏好，用同用户新session与其他用户确认隔离。
4. 展示≥20正/20错Verifier报告和四配置模型实验，定位一条失败/误判。
5. 把完整任务加入frozen scenario，带真实fixture/版本与成功谓词，不用截图代替断言。

三条路线都记录同一请求中的UI/API/DB/Provider证据。失败与拒绝是验收的一部分，不为演示隐藏或临时放宽权限。

<a id="delivery-7"></a>
<a id="delivery-7-7-毕业能力矩阵"></a>
### 毕业能力矩阵

| 能力 | 正常证据 | 失败/边界证据 | 个人掌握检查 |
|---|---|---|---|
| A 模型/Loop | 原始协议、单多调用、计量 | 失败回传、预算、重复停止 | 本人修改Loop并解释反馈顺序 |
| B RAG | 三格式定位、≥50审定题、四组检索 | 无答案/越权/索引失败/版本 | 手算指标并解释消融 |
| C DB | 迁移、六查询、短事务 | 角色拒绝、重启、一致性 | 独立写/改查询，解释intent |
| D Tools | 真实密码结果、≥50工具题 | schema/超时/审批/认证失败 | 新增受控参数与风险理由 |
| E MCP | 三Server、Resource/Prompt、刷新 | 未授权端点、协议错/未知风险 | 解释发现与本地授权区别 |
| F Workflow | checkpoint/固定审批/恢复 | 重放/过期/变更/三处崩溃 | 本人State设计、unknown核对 |
| G Memory | 跨session、来源、纠正删除 | 跨用户/无关输入/投毒 | 解释四上下文与事务替代 |
| H Eval | 100–180frozen、Runner、配对compare | 无效fixture、结果缺失、泄漏检查 | 本人gold与成功谓词，pp/分母 |
| I Security | 威胁模型、拒绝审计 | 关键攻击面实际资源断言 | 本人设计边界测试，实际越权0 |
| J Full stack | 页面、干净复现、备份恢复 | 断线/刷新/冲突/unknown/下载拒绝 | 改交互、诊断网络、说明恢复依赖 |

RAG≥50、Tool≥50是能力专项要求；综合100–180按唯一case ID计数，可以交叉覆盖但不能虚增样本。未引入worker等选修标“不适用与理由”，不能用它豁免核心审批/恢复。

<a id="delivery-8"></a>
<a id="delivery-8-8-证据卡与阶段签收模板"></a>
### 证据卡与阶段签收模板

| 字段 | 由学习者填写 |
|---|---|
| 目标/技术项/状态 | 目标编号、表格行名、待学/在做/已验证/缺口 |
| 预期与成功谓词 | 正常、失败、安全必要条件 |
| 输入/环境 | fixture来源、hash、code/model/config版本 |
| 执行记录 | 命令、退出码、case/run/action ID、日志位置 |
| 实际结果 | 与预期差异、计量、真实资源状态 |
| 个人检查 | 自己解释、需求修改/排错、尚不理解之处 |
| 限制与补测 | 降级、不适用理由、责任与补测时间 |

每阶段使用[checklist](../ROADMAP.md#task-index)打勾，自己写ADR，检查to-digest是否仍含本阶段关键内容。本人不会解释的核心模块，即使测试通过也不签收。

<a id="delivery-9"></a>
<a id="delivery-9-9-发布前门禁与完成边界"></a>
### 发布前门禁与完成边界

确定性合同/授权/审批/恢复回归通过；相关LLM变更用同frozen数据/环境compare，报告全部case与性能；任何实际越权阻止发布。普通CI不假定有本机Ollama/GPU。安全和关键协议测试不能为了展示而放宽。

毕业包包含实际可执行runbook、锁/版本、测试结果、评测报告、脱敏正常/失败Trace、浏览器路线、备份恢复记录与本人ADR。未完项/CPU降级/未支持Provider能力如实列出。首版只能称首版；这套学习系统验收不等于生产密码服务合规认证。

<a id="delivery-10"></a>
<a id="delivery-10-10-分阶段交付而非最后才看页面"></a>
### 分阶段交付，而非最后才看页面

| 交付阶段 | 演示路线与证据 | 对应毕业要求的剩余部分 |
|---|---|---|
| V1 | CLI只读工具/Loop与原始反馈、失败/预算 | API/网页与后续业务 |
| V2 | 路线A的JSON网页/上传/Run/Trace/权限/重启 | full Verifier/SSE/完整前端与清洁部署 |
| V3 | 同只读业务直调/MCP对照、断连/拒绝 | 三职责/Resource/Prompt/新端点 |
| V4 | 路线B的一种加解密/固定审批/产物/三处故障 | 全轮换/CSR/签发、完整安全与所有状态回归 |
| V5 | 路线C的知识/引用/Memory/Verifier，加SSE | 模型矩阵/完整frozen Scenario/毕业交付 |
| V6 | 本文全部三路线与A–J矩阵、clean复现/备份恢复 | 选修登记，必修不得缺漏 |

V2网页是教学开发实例，V6才完成部署专项；Ubuntu执行约束始终相同。证据卡增加当前V、目标编号、task ID、本切片范围、剩余必修与补齐V。阶段通过只签收当前开放范围，16目标毕业必须全表通过，标签规则见学习总览。正式规模不提前堵住只读网页，当前权限/写恢复边界也不为赶进度延期。

<a id="agent-6"></a>
<a id="agent-6-6-routerplanner与rag的职责"></a>
### Router、Planner与RAG的职责

| 需求 | 合理路线 | 必须保留的判断 |
|---|---|---|
| 查看公开证书字段/摘要 | 只读工具 | 授权对象ID、实际Provider能力 |
| 问操作规则/术语 | RAG，必要时澄清 | 文档版本、有效引用、无证据拒答 |
| 密钥状态/失败排行 | 固定query_database或元数据工具 | 固定query_id、可信tenant过滤、无任意SQL |
| 加密/轮换/测试签发 | 工具提议→固定审批→执行 | 参数/资源版本锁定、真实artifact或新版本 |
| 记住/纠正偏好 | Memory操作 | 来源、用户确认策略、可删与隔离 |
| 多项组合 | 有限计划串联各路线 | 每步依赖与成功谓词，不绕过单步授权 |

Planner输出供运行时检查的步骤提议，而非shell脚本。计划变更影响写动作时重新绑定审批。Retrieval是证据获取，不把检索文本当工具执行指令。V6 Router实验固定候选池，记录路由漏召与后续选错工具分别导致的失败。

<a id="agent-11"></a>
<a id="agent-11-11-本文件完成标准"></a>
### 本文件完成标准

- 自绘一次只读、一次审批写动作、一次知识问答的序列图。
- 明确四类上下文、每种版本、所有秘密边界和停止条件。
- 用真实证据解释一次拒绝、一次失败、一次重启恢复及一次Verifier误判。
- 独立完成Loop修改、State设计和关键边界说明；AI只能审查本人核心实现。
- 设计与结构文档/实际代码差异有迁移记录，未实现能力不标完成。

<a id="crypto-6.2"></a>
<a id="crypto-6.2-62-签名与验签"></a>
#### 签名与验签

首版只选一个 OpenSSL 系方案和一个 GmSSL SM2 方案；确切算法、编码、摘要与 SM2 用户 ID 通过 profile 固定。签名不等于加密，验签通过不代表签名者身份已被信任。

验签工具返回 signature_valid，与 identity_trusted 分开。后者需要验证实际公钥来源、证书链和检查范围，不能直接由签名数学验证推出。原文件变化、签名变化、公钥错误及 profile 不匹配都要有明确结果。

**技术点掌握程度标准**

| 技术点与阶段 | 本阶段必须能独立做到 | 练习与验收证据 | 可后置内容 |
|---|---|---|---|
| 签名 profile（M1） | 固定一种 OpenSSL 系和一种 SM2 路线；说明摘要、编码及 SM2 用户 ID 的作用 | profile 配置与独立验签结果，修改 profile 后行为明确 | 全部签名算法与编码体系 |
| 正反验签（M1） | 对合法签名、改文件、改签名、错公钥分别给出 valid/invalid/操作错误 | 独立对照与反例，坏编码不伪装成工具成功 | 数学证明与签名安全研究 |
| 身份信任（M1→M2） | 分开 signature_valid 和 identity_trusted；指出公钥来源及已做/未做信任检查 | 数学验签通过但身份未核验的输出与最终解释 | 完整证书身份体系与长期验证 |
| 签名副作用（M4） | 私钥只在受控服务加载，审批绑定文件/key 版本/profile，重复动作不重复签 | 审批和动作账本、signature artifact 与权限证据 | 生产文档签署、时间戳服务 |

<a id="crypto-8"></a>
<a id="crypto-8-8-领域验收任务"></a>
### 领域验收任务

下面是待你实现与审定的任务规格，包含预期行为。正式用例要补齐独立 fixture、gold、身份、资源和成功谓词；审定前保持draft，资源和成功条件齐全后再进入ready与冻结流程。

| 任务 | 程序成功条件 | Agent 成功条件 |
|---|---|---|
| 摘要 | 与独立向量/工具结果一致，绑定文件版本 | 选对 provider/algorithm，正确报告来源 |
| 证书有效期 | 与固定时钟、原始字段和取整规则一致 | 不把时间有效等同链可信 |
| 证书用途/域名/链 | 指定条件的实际验证结果完整 | 清楚说明 passed/failed/not_checked |
| 加密 | 生成认证密文与可追溯 key version | 权限/审批成立，参数与结果一致 |
| 解密 | 认证成功且输出字节正确；失败不泄露明文 | 使用授权资源，结果通过下载获取 |
| 签名/验签 | 固定 profile 的数学结果正确 | 不混淆加密、签名与身份信任 |
| 密钥轮换 | 新旧版本状态和使用行为符合策略 | 先读状态，审批绑定版本，不重复执行 |
| 测试签发 | CSR/SAN/用途/时间符合 profile，serial 可追踪 | 不静默扩大用途或修改审批参数 |
| 故障恢复 | 实际动作一次或进入明确 unknown 核对 | 不宣称尚未确认的动作成功 |
| 权限边界 | denied 与实际 executed 分开，无越权副作用 | 对缺信息澄清，对无权请求拒绝 |

领域的确定性密码、权限和状态检查要求全部通过。模型质量报告使用 Task Success、Tool/Argument/Joint Accuracy、误报与无支持结论；延迟门槛由本机 baseline 定，不预设 500ms 或任意 95% 保证。

<a id="full-m2"></a>
<a id="full-m2-m260h"></a>
#### M2（60h）

- [ ] 目标3：鉴权、资源归属、POST/chat/files、sessions/runs/events/cancel、live/ready。
- [ ] 流前持久化Run；同client_request_id返回原Run。
- [ ] SSE统一事件envelope，run_id/event_id必带，跨UTF8/CRLF/半帧正常。
- [ ] cancel/detach分开，断线不当作审批，重连不重跑请求。
- [ ] 目标4：Alembic迁移、owner/app/query/audit角色隔离，运行角色不能DDL/改审计。
- [ ] 六个查询可跑；q4从llm_calls实际计量，q6窗口参数化，失败包含timeout。
- [ ] 文件/证书/key元数据按项目与用户隔离；DB/Trace不存私钥或解密文件内容。
- [ ] 短DB事务不跨外部任务；run/user/session一致性检查，重启数据不丢，m2-done。

<a id="full-m4"></a>
<a id="full-m4-m480h"></a>
#### M4（80h）

- [ ] 目标7：ToolSpec与本地policy、密码操作风险、输出schema、幂等retry与预算。
- [ ] ≥50工具用例允许多解，gold_calls按occurrence表达多次调用，单位SI明确。
- [ ] 未授权/参数错误/取消/失败均审计；MCP注解不可自授权。
- [ ] 密码写动作/敏感解密审批绑定规范参数、资源/策略版本；轮换、CSR或测试签发有实际状态断言。
- [ ] 目标8：三Server+Resource+Prompt；stdout协议、stderr日志、canonical ID映射。
- [ ] 已连接Server工具变化刷新；新增授权endpoint热加载另测；不假设自动扫描Server。
- [ ] 目标9：State只存有限摘要/版本化引用，AsyncPostgresSaver迁移setup与锁定graph版本。
- [ ] 动态interrupt用Command(resume)，同pending action恢复不重新改参数。
- [ ] approvals绑定hash/身份/有效期/单次消费；重复/并发approve与拒绝可测。
- [ ] actions账本、幂等键、执行前/中/后崩溃核对；unknown不自动重跑；引入独立worker时补lease/fencing与双worker竞争。
- [ ] 重连恢复待审批，显式cancel，副作用只执行一次或进入明确unknown，m4-done。

<a id="full-m5"></a>
<a id="full-m5-m590h"></a>
#### M5（90h）

- [ ] 目标10（20h）：同用户跨session Memory，不同user/project隔离；短显式偏好不误过滤。
- [ ] 改口事务、有效hash唯一索引、语义复核、来源/查看/纠正/删除与投毒防护。
- [ ] 目标11（15h）：4B/9B±router与可选27B，全组相同Judge/config/fixture。
- [ ] 每配置3次，原始结果/方差/区间/质量/延迟/tokens/峰值VRAM与换模成本。
- [ ] 目标12（15h）：必要tool最终状态、事实绑定、单位/派生量、引用存在/定位/支持、unsupported、schema。
- [ ] 已知错误/正确集TPR/FPR，实体错绑/引用版本/合理无引用覆盖；不只查数字集合。
- [ ] 目标13（20h）：100~180审定记录、split分组隔离、无TODO，frozen校验通过。
- [ ] Runner驱动fixture/turn/approve/fault/resume/assert/cleanup，实验+重复namespace隔离Memory。
- [ ] 结果含intent/proposed/executed/denied/retrieval/evidence/claims/states/timing/errors。
- [ ] 普通CI合同/mock与专用GPU评测分开；配对compare按pp并列case回归。
- [ ] 目标14（20h）：注入/SQL/命令/路径/SSRF/泄密/提权、审批重放、跨用户、MCP/Memory投毒。
- [ ] 安全判断区分拒绝尝试与真实执行；实际副作用Unauthorized Action Rate=0，m5-done。

<a id="full-m6"></a>
<a id="full-m6-m660h"></a>
#### M6（60h）

- [ ] 目标15（30h）：九UI区块、实时状态、刷新/reconnect/审批/cancel正确。
- [ ] draft token显示未验证；final替换，错误不展示为已验证；安全Markdown渲染。
- [ ] 目标16（15h）：profiles、固定镜像/依赖/model、健康/迁移/volume/网络/日志轮转。
- [ ] API无Docker socket与bootstrap/migration秘密；**Ollama仅监听127.0.0.1**，仅前端/API端口对外。
- [ ] 干净目录安装→迁移→启动→smoke，重启数据不丢。
- [ ] 综合项目（15h）：上传/只读检查/key元数据/加解密审批/执行/轮换与版本验证/UI审计全链路，补证书验证或测试CSR/签发。
- [ ] 故障恢复不静默重复密码动作，版本化来源/审计完整，冻结scenario回归，m6-done。
- [ ] **交付验收**：Windows 浏览器从网络打开前端地址即可复现全链路，Windows 侧零安装。

<a id="dataset-1"></a>
<a id="dataset-1-1-起步资料与检查入口"></a>
### 起步资料与检查入口

评测数据、schema、fixture、校验器和Runner由你在实现仓库的`eval/`中逐步建设；文档仓库只提供本章的设计要求和V5的八道起步题。先从少量证书检查、摘要、密钥元数据、逐项审批加密和报告偏好场景开始，逐条写清成功条件与独立证据。

初始记录使用schema_version=3、status=draft、split=dev；教学文件与元数据明确标synthetic，尚未准备的证书、密钥材料与知识索引标resolved=false。逐题gold映射是审核记录，不计为额外测试。

你需要实现两种校验模式：draft允许明确未完成项并报告缺口；frozen拒绝未准备资源、无真实证据、未人工审核、无有效成功条件或审批不完整的记录。离线格式检查不执行Agent，也不证明密码业务通过；真实运行与资源断言另留证据。具体命令入口在代码仓库实现后记录。

<a id="dataset-2"></a>
<a id="dataset-2-2-字段与工具契约"></a>
### 字段与工具契约

按下列字段和枚举要求，在代码仓库定义评测schema并实现结构、语义与冻结校验；应用工具契约见[工程合同](V1-CORE-DEMO.md#contract-4)，指标见[模型与实验协议](V6-DELIVERY.md#eval-1)。离线校验器不执行真实Agent、Provider或指标计算。

公共字段包含id、schema_version、status、split、group_id、category、difficulty、question、answerability、expected_behavior、fixture_refs、allowed_tool_plans、gold_calls、success_criteria、provenance。RAG增加gold_chunk_ids/gold_doc_ids/gold_pages/gold_section/gold_fact_slots；场景增加scenario。未知字段拒绝，字段或工具范围变更通过版本管理同步schema、validator与应用registry。

本项目canonical工具为证书解析/验证、文件摘要、签名验签、密钥元数据、加解密、签名、轮换、CSR、测试签发、知识检索和固定元数据查询；工具ID与结构文档一致。intent_crypto表示密码操作意图，不替代权限或审批。

status=ready仅说明内容经审定，不能代表应用测试成功。ready/frozen要求provenance中reviewer_kind=human、实际verified_by和ISO reviewed_at。AI生成的草稿保留synthesized与空审核字段；测试模块中的mock审核仅用于验证门禁。

<a id="dataset-3"></a>
<a id="dataset-3-3-成功条件"></a>
### 成功条件

| 字段 | 判定范围 |
|---|---|
| allowed_tool_plans | 二维工具序列，任一合法计划即可；空计划写`[[]]` |
| gold_calls | tool_id与occurrence绑定参数约束，重复同工具分别记录 |
| must_call_tools / must_not_call_tools | 调用提议层，与实际执行分开 |
| must_execute_tools / must_not_execute_tools | 真正执行层，拒绝不计execute |
| expected_values | subject/metric/value/unit/atol/rtol/source_ref绑定数值与来源 |
| state_assertions | 真实资源、执行计数、恢复、Memory与事实支持状态 |
| final_answer_all_of / any_of / none_of | AND、OR与禁止文本辅助条件 |
| expected_behavior | answer/refuse/clarify，不能只看关键词 |
| min_citations / verifier_passed | 必要引用与检查状态，单独不能证明任务完成 |

RAG可回答用例冻结时需要真实gold与具体事实槽，每槽证据属于gold_chunk_ids；MD/TXT用章节/字符定位，PDF才用真实页码。无答案用例必须refuse和空gold，仍需实际语料manifest支持可答性判断。Database须有数值或结果状态断言。

Security用例由学习者按实际入口自行设计，必须禁止越权执行并断言actual_unauthorized_actions=0；模型提出请求而执行器拒绝，与实际越权执行分别计量。文本“已拒绝”不能代替资源状态证据。

<a id="dataset-4"></a>
<a id="dataset-4-4-场景与审批"></a>
### 场景与审批

scenario包含user_key、steps和cleanup=delete_namespace。步骤支持turn、approval、inject_fault、restart、resume、cancel、assert_state。turn是真正用户消息；其余控制由Runner驱动，不当普通问题发给模型。

```json
{
  "user_key":"user_a",
  "steps":[
    {"type":"turn","session_key":"s1","message":"记住我的密码操作报告用中文。"},
    {"type":"turn","session_key":"s2","message":"我的报告应该用什么语言？"},
    {"type":"assert_state","subject":"memory","predicate":"cross_session_preference_used","expected":"中文"}
  ],
  "cleanup":"delete_namespace"
}
```

加解密、签名、轮换、CSR和测试签发的执行场景须逐动作approval，selector对应tool_id:occurrence或唯一pending action，bind_action_hash=true。Runner从真实pending快照读取hash；一条approval不能空白授权整个Run。execution_count_by_tool如`{"encrypt_file":3}`用于绑定三次调用和逐项审批，实际资源/输出仍须独立断言。

故障点支持before_execute、during_execute、after_effect_before_commit、tool_failure，控制边界由适配器确认。恢复核对action账本、执行计数、unknown/reconciliation与实际artifact，不能用随机kill或重新发请求代替恢复验证。

<a id="dataset-5"></a>
<a id="dataset-5-5-fixture与证据准备"></a>
### Fixture与证据准备

在代码仓库构造自己的fixture，记录id/kind/resolved/source/data。可用small_files_sample表示公开教学字节样本，key_metadata_sample仅保存元数据，tool_failures_sample保存固定时钟的调用排行预期。每个预期由你独立核对；fixture别名由应用Runner映射为隔离namespace内的UUID。

尚未准备的证书、密钥材料与知识语料保持unresolved。按[Provider练习](V1-CORE-DEMO.md#provider-practice-10-后续可以照着操作的-provider-入门练习)准备样本，核对实际字段与参数后更新记录。只填resolved=true而没有对应资源不构成验收。

为实际索引创建证据清单，记录manifest_version、corpus_version、chunk_id、doc_id、document_version、locator、content_hash。Qdrant point_id与业务chunk_id分开。逐题审定gold映射后同步到RAG记录，实际事实槽仍需逐条核对；空清单不构成可定位证据。

<a id="dataset-6"></a>
<a id="dataset-6-6-标注冻结与回归"></a>
### 标注、冻结与回归

1. 按实际密码工具与操作文档核对问题可答性、能力范围和所需参数。
2. RAG合并多路检索候选并直接查原文，核对真实gold和必要事实；top-K未命中不直接改为无答案。
3. 数值绑定fixture或真实快照的实体、字段、单位和版本；派生值独立计算。
4. 逐条人工审定，补审核者与日期；20%抽检只用于批次质量判断，不代替其余记录的审核。
5. 相关来源、模板和场景按group整体划分dev/test；test不用于反复调参。
6. 冻结要求ready、无TODO、fixture已准备、证据真实、成功条件有效、场景支持且审批明确。
7. 每个实验/重复/case隔离user/project/session/文件/索引/Memory；cleanup只清理自己的namespace。
8. 固定dataset/schema/fixture/corpus/index/environment hash与模型digest；结果一对一配对，缺失、重复、额外和超时不可静默跳过。

最终目标为RAG≥50、Tool≥50、综合100–180条逐项审定用例。少量起步题不包含完整安全回归，也不能替代最终题库和应用运行证据。

<a id="dataset-7"></a>
<a id="dataset-7-7-按交付阶段积累v6完成正式冻结"></a>
### 按交付阶段积累，V6完成正式冻结

V1记录少量证书/摘要/Loop的明确输入输出与失败；V2增加API/幂等/权限；V3直调/MCP对照；V4逐动作审批与故障恢复；V5完成RAG≥50/四组检索及Verifier正误双集、Memory；V6固定完整工具池后完成Tool≥50、100–180综合、隔离Runner/cleanup/配对报告。

M5 09/12是稳定任务ID，草稿从V1开始，正式范围到V6完成；manual小case不冒充Runner或frozen。原schema_version=3、canonical 13工具、人工审定/真实fixture/证据/审批门禁均保持。各V目标和预算见[Roadmap](../ROADMAP.md)，task切片见[阶段路线](../ROADMAP.md)。

## 本阶段签收清单

- [ ] 本阶段学习技术表逐项有本人解释、独立实现/修改和失败验证证据。
- [ ] Q01–Q22已由本人结合实现作答，证据与未覆盖边界记入docs/progress.md；AI仅审查。

- [ ] 按学习总览的工时分配补API/DB/全部工具/三职责MCP/Graph/完整安全及前端专项。
- [ ] 固定工具池后四模型配置各3次，≥50Tool及100–180综合frozen，完整Runner/隔离/cleanup/compare通过。
- [ ] 16目标全表/A–J/clean部署/备份恢复/综合15h通过，选修不适用有理由。
- [ ] 所有专项标签按学习总览的专项标签条件创建，未用小时或单次Demo代替掌握。

### 综合交付（15h）

按[交付验收](V6-DELIVERY.md#delivery-1)执行只读证书/摘要、审批加密/轮换与恢复、知识/引用/Verifier三条路线，补证书验证或测试CSR/签发。用同Run对照页面、API、DB与Provider，不以成功截图替代断言。

毕业独立回答：为何选工具或检索？为何允许执行？用了哪版密钥与证据？外部完成后崩溃如何核对？Verifier误判怎样发现？4B/9B差异怎样量化？刷新为何不二次执行？

A模型/B RAG/C DB/D Tools/E MCP/F Workflow/G Memory/H Eval/I Security/J全栈正常/失败/个人证据齐全，按本阶段毕业矩阵和完整专项清单签收；选修不适用有理由，首版不冒充完整毕业。


## 文档配套与完整交付

- [ ] 各阶段的每目标表逐行有状态与证据，解释/实现/排错/证据分别检查，未运行不标通过。
- [ ] 自绘只读/审批/知识三条序列与信任边界图，State/安全边界本人确定。
- [ ] 接口错误/幂等/分页/鉴权与OpenAPI一致，全栈联调表逐场景通过。
- [ ] 干净目录复现、DB/文件/index/keystore/checkpoint备份恢复与unknown核对有证据。
- [ ] 四仓库同级并独立固定版本；源码/prefix分离，密码仓库不成为文档子目录。
- [ ] A–J毕业矩阵正常/失败/个人能力齐全；选修不适用有理由，首版缺口未冒充完整版。

## 下一步

按完整交付矩阵签收；未验证内容保留缺口，不因运行Demo成功自动毕业。
