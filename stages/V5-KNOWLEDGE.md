# V5 知识与可靠性增强

本阶段基础预算**105h**；实现成果：基础RAG/引用、完整Verifier、Memory、检索实验与SSE。先读实现目标与当前切片，再执行详细任务；完成标准以实际证据为准。

## 实现目标与学习结果要求

让Agent在需要操作依据时检索授权资料，加入版本引用与本人Verifier，再增加可追溯Memory、四组检索实验和浏览器SSE。RAG是条件性分支，不能替代实际密码结果或让每条摘要请求都经过知识库。

| 需要学习的技术 | 学习结果要求 | 独立实现与排错证据 |
|---|---|---|
| PDF/MD/TXT解析与版本化chunk | 识别真实定位、needs_ocr与解析失败；保存来源/hash/版本/ACL | 原文对照、三格式样本、更新删除和staging→active失败恢复 |
| Dense、BM25、RRF与rerank | 在同一授权候选与冻结语料上做四组对照，正确计算检索指标 | ≥50人工审定RAG题、分母/n、无答案与漏召回分别报告 |
| Citation、Claim与本人Verifier | 检查来源存在/定位/支持、实体/单位/派生值与必要工具最终状态 | ≥20正确/≥20错误，误报漏报与unknown/N/A可解释；AI只审查核心 |
| History、State、Knowledge与Memory | 区分生命周期与权威性，Context有限且不把历史当当前资源状态 | 真实任务逐项标来源、预算和秘密边界 |
| Memory来源、改口、删除与并发 | 同user/project跨session偏好可追溯、可纠正删除且按权限读取 | 显式短偏好、重复/矛盾、并发冲突、删除/跨用户/投毒反例 |
| SSE、持久事件、snapshot与重连 | 分开模型NDJSON和浏览器事件流，state/event提交后发送并按游标去重 | UTF8/CRLF/半帧、重复事件、刷新/断线同Run恢复，不重POST |
| 引用/检查/Memory前端与可选GPU环境 | 安全展示真实来源与验证状态，按需使用检索依赖和实测GPU | 原片段鉴权、Verifier失败、Memory纠正删除、真实资源/版本记录 |

## 必须独立回答的关键问题

这些问题必须由你结合自己的实现作答，AI只审查。记录在代码仓库docs/progress.md，写清场景、自己的理由、真实证据与未覆盖边界；只背定义或复制AI答案不算通过。

| 编号 | 必须自己回答的问题 | 回答达到标准所需的说明或证据 |
|---|---|---|
| Q01 | 为什么当前密码工具结果与操作文档是不同证据？ | 用证书检查+解释规则的同一请求区分来源和结论 |
| Q02 | 什么请求需要RAG，什么请求可以只调工具？ | 给出自己的路线和失败处理，不把检索当固定前置 |
| Q03 | 扫描PDF、普通PDF、MD和TXT怎样分别定位？ | 真实样本、页码/章节/字符与needs_ocr处理 |
| Q04 | chunk_id、document_version、content_hash与Qdrant point_id有什么区别？ | 一个真实片段到原文/版本/索引记录的映射 |
| Q05 | 资料更新、删除或入库失败后，旧索引与引用怎么处理？ | 解释staging/active、版本一致性和实际恢复证据 |
| Q06 | ACL过滤应该在哪里发生？多路检索和rerank能否扩大权限？ | 同一授权集合与跨用户拒绝的实测对照 |
| Q07 | Dense、BM25、RRF与rerank各改变哪一部分？ | 四组实验固定项、唯一变化、输入与输出说明 |
| Q08 | Hit、Recall与MRR的分母分别是什么？无答案题如何处理？ | 自己的公式、n和一个手工核对例子 |
| Q09 | top-K没有命中为什么不能直接把问题标成无答案？ | 原文与多路候选的人工可答性审定证据 |
| Q10 | 一个引用存在、位置正确和支持结论，是同一件事吗？ | 三类反例与本人Verifier的不同判定 |
| Q11 | 为什么只比较回答中的数字集合无法验证事实？ | 展示实体错绑/单位/来源/派生量的正反例 |
| Q12 | Verifier的unknown、skipped、N/A和fail怎么区分？ | 自己的必需检查规则、合理无引用回答与失败展示 |
| Q13 | Verifier漏报与误报如何量化，为什么要同时准备正确和错误集？ | ≥20+20的混淆结果、TPR/FPR与本人误判分析 |
| Q14 | History、Run State、Memory与Knowledge分别何时读取和失效？ | 标注一次任务的四来源与可信边界，不能从旧聊天断言现状 |
| Q15 | Memory怎样证明偏好来自该用户，而不是检索文档或攻击文本？ | 来源、确认策略、显式短偏好与投毒拒绝证据 |
| Q16 | 用户改口、重复表达或删除偏好时怎样保持一致？ | 解释失效旧记录/新记录/有效唯一性与删除后注入验证 |
| Q17 | 为什么Memory content_hash不能作为授权凭据？并发修改怎样处理？ | 归属与expected_content_hash校验、409和真实状态 |
| Q18 | 模型NDJSON与浏览器SSE为什么必须分开解析？ | 分别画网络块/记录/事件，给切块与UTF8反例 |
| Q19 | event_id、run_id、snapshot和after游标怎样一起恢复页面？ | 同Run刷新/断线/重复事件证据，不发新POST |
| Q20 | 事件已过保留窗口或游标不属于该Run时怎样处理？ | 错误与快照重建策略，不能悄悄重跑原任务 |
| Q21 | 草稿token、final、verify与done在页面上各代表什么？ | 真实状态与失败/未验证展示，不能网络关闭就显示完成 |
| Q22 | 怎样证明检索和Memory增强改善了系统而非掩盖工具失败？ | 同一任务的来源/工具/检查结果与固定变量对照 |

## 分步任务与技术掌握标准

先按当前切片实现最小输入输出，再补齐技术表。本阶段首次运行、正常/失败/权限、本人解释与独立修改分别验收；未实际运行不签收。

**当前105h**：目标5基础RAG35h、目标12剩10h、目标10 Memory20h、目标6检索35h、目标3 SSE5h。按以下顺序逐项加；知识检索是条件性分支，摘要/加密不必每次经过RAG。


### 目标5：基础 RAG 与版本化引用（35h）

**进入条件**：V4交付通过，V2的数据/权限基础可复用；V5开始知识库，不以知识库作为密码工具或MCP前置。

**Agent目标**：从操作规范找依据；知识不能代替当前工具实际状态，查不到就诚实说明。 对应详细任务：**M3 01–07**。

**技术点掌握程度标准**

| 技术点 | 能解释 | 独立做到 | 排错与边界 | 验收证据 | 后置内容 |
|---|---|---|---|---|---|
| 语料/Parse | 原文、解析文本、扫描页不同 | 小型操作知识库，PDF/MD/TXT保留来源 | needs_ocr不造正文，复杂表格标限制 | 三格式样本与定位对照 | OCR/多模态 |
| Chunk/Metadata | 文档/version/hash/locator与chunk | 切分并保留页区间/section、project与ACL | 同内容不同项目不全局去重泄露存在 | chunk清单与定位检查 | 学习型切分 |
| Embedding/Qdrant | 维度、相似度、payload与point ID | UUID/uint64 point_id，业务chunk_id独立 | 维度错、过滤漏、版本混用能定位 | collection与检索记录 | 索引底层算法 |
| 发布/更新 | staging与active隔离半成品 | 成功后发布manifest，重复不重复，更新删除同步 | 失败不进active，旧Run版本与权限复查 | 重复/失败/更新/删除断言 | 大规模异步索引 |
| 引用/拒答 | 存在、定位、支持答案三种判断 | 可追溯引用，无证据合理拒答 | 不编页码，不把正文指令当工具命令 | 有答案/无答案/撤权记录 | 复杂跨文档推理 |

**学习与实现顺序**：少量可信操作资料/授权 → Parse定位 → Chunk/version → dense召回 → 引用答案 → 权限/失败/更新检查。密钥、秘密和解密正文不入知识库。

**必须独立回答**：point_id为什么不同于chunk_id？引用存在为什么不代表支持答案？旧Run读取资料时为何仍要复查权限？

**独立练习**：修改chunk长度观察定位；发布v2并检查旧Run；另一用户不得看到无权资料。

**退出条件**：三格式真实可定位；索引发布与权限一致，引用支持回答，缺证据不伪造。

**具体实践与逐项操作**


当前先M3 01–07；从3–5份说明/10题dev起步，再补三格式/版本/权限与正式gold，不提前堆高级检索。

先学文档解析、chunk、embedding、向量相似度、metadata、授权过滤、文档版本与引用。你应能画出“文档→切块→向量/metadata→检索→证据→回答”的数据流，并指出业务文件与说明文档的差别。

**技术点掌握程度标准**

| 技术点 | 本阶段必须能独立做到 | 练习与验收证据 | 可后置内容 |
|---|---|---|---|
| PDF/MD/TXT 解析与定位 | 从原文核对正文、章节/页码；识别扫描页与失败，不给无页码文档编造页码 | M3 02 三类样本的原文与解析输出；扫描页明确标记 | OCR、复杂表格和版面恢复 |
| Chunk 与版本 metadata | 定义切块大小/重叠与稳定定位；保留 document/version/chunk/hash 和 ACL | M3 03 找回某块原文；更新后新旧版本可区分，说明切块取舍 | 复杂语义切块与自动文档结构学习 |
| Embedding 与相似度 | 区分向量表示、相似度与答案正确性；固定模型、维度和索引配置 | 同一问题返回 top-K 与分数；维度错误明确失败，解释高分不等于事实可信 | 训练 embedding、向量算法推导 |
| Qdrant 与授权过滤 | 写入 point/payload，按用户/项目/版本过滤；返回证据之前完成授权 | M3 04、06 重复入库不重复；两个用户检索同一问题无跨范围证据 | 集群分片和海量向量调优 |
| Manifest 与索引发布 | 完成 staging 后发布 active；更新、删除、失败有一致版本状态 | M3 05 中断入库后旧版本仍可用，半成品未被发布 | 分布式索引构建系统 |
| RAG 回答与引用 | 将有限证据交给模型；来源可定位；区分无检索结果、证据不足与操作尚未执行 | M3 07 有答案/无答案例子与原文对照，不用知识文档证明动作已成功 | 长文综合、自动研究 Agent |

| 顺序 | 学习任务 | 具体操作 | 验收指标 |
|---|---|---|---|
| M3 01 | 准备资料与问题 | 先 3–5 份说明、10 个 dev 问题，核对能回答什么 | 每题有来源或明确无答案依据 |
| M3 02 | 实现解析 | 各准备 PDF/MD/TXT 样本，标注扫描页 | 原文可核对；需要 OCR 的页不产生假正文 |
| M3 03 | 切块与版本 | 保留 document/version/chunk/hash/定位/project/ACL | 找得到原文区间，不给 MD/TXT 伪造页码 |
| M3 04 | 加 embedding 与 Qdrant | 确认向量维度、UUID point_id 与 payload | 重复入库不重复；检索返回对应版本 |
| M3 05 | staging→active 发布 | 整批完成后才发布索引；更新/删除同步 | 入库失败不发布半成品 |
| M3 06 | 检索工具与引用 | query→授权候选→top-K→source_ref | 引用能点击/定位；无权证据不进入结果 |
| M3 07 | 简单知识回答 | 将有限证据给模型，输出事实与来源 | 无证据时明确不足，不能伪造操作成功 |

只在此阶段引入 bge-m3 和 Qdrant。实际 embedding 维度通过返回值检查，版本写入 manifest；不要把任意 chunk_id 字符串当 Qdrant point_id。dense 与后续 sparse、rerank 使用同一服务端授权条件。Qdrant 可通过 payload 条件过滤，具体接口按锁定版本实现，参见 [官方过滤文档](https://qdrant.tech/documentation/search/filtering/)。

冻结证据版本不等于永久保留访问权限；权限撤销或证据删除后，旧 Run 恢复也要重新授权，必要时返回 evidence_unavailable。

**产物**：解析器、版本化 chunk、入库 pipeline、manifest、检索工具和引用展示数据。至少三种格式各有真实样本，不把 placeholder 证据当 baseline。

**独立练习**：修改一份工具说明，重建索引后新请求引用新版本，旧请求仍能指出原版本；证据被删除时给出明确恢复结果。

### 补齐目标十二事实与引用检查

回[V4目标12完整标准](V4-APPROVAL-CRYPTO.md#目标12事实引用与动作-verifier15h)，沿自己的逻辑增加Claim实体/metric/value/unit/source绑定，派生输入与公式、引用版本/locator与支持性；MD/TXT不用假页码。准备≥20错误和≥20正确，报TPR/FPR与误判。把检查项和引用接到M6 06，允许点击授权原片段；必需unknown/skipped不能当pass，有界修复或明确未验证。


### 目标10：可追溯 Memory（20h）

**进入条件**：V5基础知识与来源边界已理解；MCP三职责和全部写工具无需先完成。

**Agent目标**：跨会话保存有来源、可纠正的偏好，不记秘密或文档指令。 对应详细任务：**M5 01–04**。

**技术点掌握程度标准**

| 技术点 | 能解释 | 独立做到 | 排错与边界 | 验收证据 | 后置内容 |
|---|---|---|---|---|---|
| 四类上下文 | History/State/Memory/Knowledge生命周期不同 | 画存取位置，按任务选择并限制注入量 | 历史模型回答不当当前资源权威 | 上下文来源图 | 认知架构研究 |
| 提取/来源 | 显式记住与推断候选不同 | 规则过滤后提候选，留类型/来源/时间 | 短偏好不过滤，文档指令不提为用户偏好 | 短偏好/投毒拒绝证据 | 无限自动记忆 |
| 去重/改口/删除 | hash唯一与语义相似两层 | user/project隔离，事务失效旧值，支持纠正删除 | 并发重复、删除后仍检索、撤回来源可定位 | 改口/删除/并发断言 | 记忆图谱 |
| 检索/相关性 | topK不是必须注入K条 | 阈值、最多5条，同用户跨session生效 | 20条无关问题不形成20条Memory | 跨session/异用户/无关记录 | 长期自学习策略 |

**学习与实现顺序**：四类上下文图 → 显式偏好 → 来源/去重 → 纠正删除 → 阈值 → 隔离/无关检查。

**必须独立回答**：用户改口怎样替代旧记忆？Memory为何不能提供密钥当前状态？删除如何同时影响存储与检索？

**独立练习**：将中文偏好改成英文再删除，用同用户两session和另一用户验证。

**退出条件**：同用户跨会话有效，跨用户/项目不共享，可追溯、纠正、删除，且无关输入不被滥存。

**具体实践与逐项操作**


完成基础知识/引用后再M5 01–04；仅必要偏好，支持纠正删除。任务资源当前状态仍从工具查，不从Memory猜。

学习 History、Run State、长期 Memory 与 Knowledge 的区别。记忆可保存“默认项目”“喜欢先显示检查计划”“报告使用中文”等偏好；它不能替代密钥权限、审批记录、算法允许列表或证书实际状态。

**技术点掌握程度标准**

| 技术点 | 本阶段必须能独立做到 | 练习与验收证据 | 可后置内容 |
|---|---|---|---|
| 四类信息的职责 | 判断会话历史、运行状态、偏好记忆、文档知识分别放哪里；不把权限或当前证书状态当记忆 | 为每类写一个本项目例子，解释过期状态为什么要查真实资源 | 复杂认知记忆架构 |
| 候选提取与 provenance | 从授权用户明确表达提取偏好，记录来源、时间与范围；不以长度决定是否有效 | M5 01 短指令与来源记录，文档中的伪造偏好不写入 | 隐式行为画像与自动用户建模 |
| Scope、去重与并发 | 按 user/project 读写，同范围重复不产生多条冲突记录 | M5 02 跨会话读取、跨范围拒绝与重复写入结果 | 多组织记忆共享与同步 |
| 更正、失效与删除 | 显式更正后新值生效；旧记录失效或按策略删除，查询结果可验证 | M5 03 更正/删除前后对照，界面或 API 可查看来源 | 自动遗忘策略、复杂时间推理 |
| 相关性与上下文注入 | 仅注入当前问题相关偏好，控制长度；记忆不改变工具授权或审批 | M5 04 无关记忆不注入，偏好不能扩大资源权限 | 训练记忆检索模型 |

| 顺序 | 学习任务 | 业务练习 | 验收指标 |
|---|---|---|---|
| M5 01 | 候选提取与来源 | 用户显式“记住报告用中文” | 来源能追踪，短指令不被长度规则误删 |
| M5 02 | 用户/项目过滤与去重 | 同用户不同 session 读取偏好 | 跨用户/跨项目无共享；并发不重复插入 |
| M5 03 | 修改与删除 | 用户改口、查看、纠正、删除 | 旧记录失效，新记录生效，删除可验证 |
| M5 04 | 相关性与污染检查 | 无关问题、知识库内伪造偏好 | 无关内容不注入；文档指令不能变成权限 |

**产物**：Memory schema/迁移、CRUD、来源记录与多会话场景。20 条无关问题不能自动生成 20 条 Memory。阶段掌握条件是能解释哪些信息要持久化、哪些需要实时查工具。

**独立练习**：用户偏好“以后不用审批”时，区分显示偏好与服务端审批策略，证明偏好无法取消审批。

### 目标6：混合检索与消融实验（35h）

**进入条件**：dense baseline可运行。

**Agent目标**：用实测选择检索策略，避免堆组件却不能证明收益。指标公式见本阶段检索指标章节。 对应详细任务：**M3 08–13**。

**技术点掌握程度标准**

| 技术点 | 能解释 | 独立做到 | 排错与边界 | 验收证据 | 后置内容 |
|---|---|---|---|---|---|
| BM25/中文分词 | 词频与稀有术语影响排序 | 已分词语料建sparse，与dense同ACL | 整段中文当一词、术语切分错可发现 | 术语查询与分词样例 | learned sparse |
| RRF/rerank | rank融合与重排分数不同 | 候选去重/融合/重排分别可控 | topK、重复、换模开销可定位 | 配置与排名对照 | 训练reranker |
| Rewrite | 改写意图与添加条件不同 | 单独开关，保存原问题和改写 | 不改变权限或用户约束 | 成功/失败改写案例 | 复杂多查询 |
| Gold/指标 | Hit/Recall/MRR/覆盖/拒答分母不同 | ≥50题审定，源文档和多路候选共同定gold | 检索失败不改无答案，不完整gold不冒充全召回 | 标注与手算指标抽查 | 大型标注平台 |
| 实验设计 | 固定项、变量、case比较与代价 | dense/sparse/hybrid/hybrid+rerank四组 | Hybrid不赢也分析，rewrite另消融 | 四组原始结果/失败/延迟表 | 自动参数搜索 |

**学习与实现顺序**：人工问题/gold → dense冻结 → BM25 → RRF → rerank → 四组比较 → 分类失败分析。检索质量与生成质量分开。

**必须独立回答**：为什么多证据题不能只看Hit？RRF解决什么？无答案样本为什么不进Recall分母？

**独立练习**：手算小排名RRF与一题Recall；找新配置变差的一题解释原因。

**退出条件**：≥50审定RAG题、manifest与四组实验齐全，质量/延迟/失败结论有证据，不预设赢家，标记m3-done。

**具体实践与逐项操作**


当前执行M3 08–13；四组检索单变量，rewrite另开关，≥50RAG题审定；模型矩阵到V6，不让换Controller干扰检索消融。

学习 BM25、中文分词、RRF、rerank、Hit/Recall/MRR、必要事实槽与无答案问题。你可以先用 20 个已审定 dev 问题跑通指标计算，再扩成本项目要求的 **至少 50 个经审定 RAG 问题**。20 个仅是中间练习规模，不算完整 M3 毕业。

**技术点掌握程度标准**

| 技术点 | 本阶段必须能独立做到 | 练习与验收证据 | 可后置内容 |
|---|---|---|---|
| BM25 与中文分词 | 解释词项检索为何擅长错误码/算法名；检查分词对关键术语的影响 | 一题看原查询、分词、命中与漏召回，和 dense 对照 | BM25 数学推导、搜索引擎内部实现 |
| Dense/Sparse 与 RRF | 区分两路候选和排名；按排名融合，不直接混加不同比例的原始分数 | M3 08–10 固定题集的候选/融合排名，能手算一个小例子 | 学习型融合与复杂查询路由 |
| Rerank 与 rewrite | 说明重排改变候选顺序、改写可能改变意图；分别设开关，保留原问题 | M3 11–12 候选前后对照与耗时；独立报告 rewrite 误改实例 | 训练 reranker、多跳检索 |
| Hit@K、Recall@K、MRR | 写清相关证据集合、K 和适用分母；能手算再用程序核对；不把命中等同回答正确 | 少量人工算例与脚本输出一致；无答案题不套有证据召回分母 | 高级统计检验与大规模评测框架 |
| Gold、事实槽与拒答 | 从原文审定来源与必要事实；无答案问题有明确不足依据，保留 dev/test 区别 | M3 13 至少 50 题的审定记录；错误来源/漏事实/应拒答分别计数 | 完全自动标注、仅靠模型 Judge 评分 |
| 消融与实验记录 | 固定 corpus/chunk/query/config，只改比较项；同时记录质量、耗时与失败类型 | 四组主实验可复现；能指出一次指标改善的样本证据与代价 | 穷举所有超参数与大规模调参 |

| 顺序 | 学习任务 | 固定项与变化项 | 应留下的结果 |
|---|---|---|---|
| M3 08 | 先 dense baseline | 固定 corpus/chunk/query/config | 每题检索结果和原始指标 |
| M3 09 | BM25 only | 同一资料和问题，正确分词 | 与 dense 的失败类型对照 |
| M3 10 | dense+sparse+RRF | 只改变融合策略 | 同一查询的排名变化与原因 |
| M3 11 | 加 rerank | 保持候选与实验记录可追溯 | 质量与耗时变化 |
| M3 12 | 独立开关 rewrite | 不混在主四组结果中 | 是否补召回、是否改错意图 |
| M3 13 | 审定与冻结 | 从原文与多路候选核对 gold | ≥50 问题、真实证据、完整成功条件 |

完整四组为 dense、sparse、dense+sparse+RRF、再加 rerank。reranker 可先 CPU；GPU 是单独环境配置，不能未验证 CUDA 就声称 GPU 已启用。不要用本机实验结论保证 Hybrid 一定更好。

**指标与通过条件**：正样本报 Hit@5/10、Recall@5/10、MRR@10、EvidenceCoverage；无答案样本报正确拒答率，正样本另报误拒答率；引用有效性、引用支持性和答案关键事实分别统计。每项带适用样本数。计算实现应与手工小例子一致，四组结果完整且能定位失败案例；**质量百分比先测 baseline，再制定改进目标**，不凭空要求 4B 达到 95%。公式沿用 [模型与实验协议](V6-DELIVERY.md#eval-1)。

dev 用于调 chunk/top-K/rerank 参数；test 不参与调参。近义问题和共享来源/模板的组整体划分，不把同一问法变体放两边。如果小语料导致所有题都连成一个来源组，先增加独立文档组或将其全部用于 dev，再另备 test；不要悄悄取消防泄漏规则。

**独立练习**：选一个 dense 失败但 BM25 命中的问题，解释它是关键词、切分、授权还是向量问题，再做一次仅改一个变量的实验。

保存四组报告、失败清单和冻结记录，目标5/6全表通过后标m3-done。MCP与审批已在V3/V4完成本切片；本次下一步补SSE/页面，再进入V6完整实验与专项。

### SSE与页面继续联调

回[V2目标3](V2-WEB.md#目标3fastapi鉴权与-sse30h)做M2 06–07，回[V2目标15](V2-WEB.md#目标15reacttypescript-与-agent-交互30h)做M6 04：state/event先持久化，SSE空行分帧、UTF-8跨块/CRLF/重复事件正确；用snapshot和after游标重连同Run，不重POST。V4后台/审批使用detach，显式cancel单独处理。M6 06现在增加真实引用和完整Verifier，Memory查看/纠正/删除接08合同。V6再完整跑浏览器断线、冲突与状态回归。

### V5出口

资料入库/授权/更新失败边界通过；引用定位与支持有证据，Verifier双集完整，Memory来源/纠正删除/隔离通过，≥50RAG与四组消融齐全，SSE正常/错误/重连有真实记录。目标5/6通过可标m3-done，目标3/15的最终专项在V6补齐。下一步V6，网页已在V2运行，不重新从零做UI。

## 本阶段的接口与实践细节

以下内容属于本阶段，按任务用到的部分查阅；涉及后续能力的字段仅作为扩展合同，当前切片不要求提前全部实现。

<a id="env-6"></a>
<a id="env-6-6-pytorch--blackwellv5检索实验按需"></a>
### PyTorch / Blackwell（V5检索实验按需）

NVIDIA 驱动显示的 CUDA Version 是驱动支持上限，不证明 wheel 包含 sm_120 的代码。Ollama 与预编译 PyTorch 一般不需要 nvcc；自行编译扩展另行安装 Toolkit。

不要使用旧的 cu124 命令。选择支持 RTX 50 系的官方 wheel，固定 PyTorch 版本、CUDA 构建与依赖。**兼容起点示例**为 torch 2.7.1 + cu128，代表历史可用组合而非“最新版本”；实际通过后才锁定。当前安装也可按官网选支持 Blackwell 的更新稳定版，再重新验证，不能悄悄覆盖实验环境。

```bash
uv pip install "torch==2.7.1" --index-url https://download.pytorch.org/whl/cu128
python -c "import torch; assert torch.cuda.is_available(); x=torch.randn(256,256,device='cuda'); y=x@x; torch.cuda.synchronize(); print(torch.__version__, torch.version.cuda, torch.cuda.get_device_name(0), torch.cuda.get_device_capability(0), float(y.mean()))"
```

该一次性诊断命令之后必须把通过的依赖与源索引写入 pyproject/lock，防止下次 uv sync 替换 CUDA 构建。还要跑一对真实 reranker 输入；仅 `is_available()` 不足以验收。[PyTorch 2.7 Blackwell 支持](https://pytorch.org/blog/pytorch-2-7/)、[官方安装选择器](https://pytorch.org/get-started/locally/)

<a id="contract-6"></a>
<a id="contract-6-6-api-与-sse"></a>
### API 与 SSE

本节定义事件与状态的工程合同；完整HTTP端点/错误/前端恢复见[API合同](V2-WEB.md#api-1)，运行职责见[Agent运行机制](V1-CORE-DEMO.md#agent-1)。接口表是目标设计，应用完成需OpenAPI与真实合同验收。

POST /chat 返回/关联 run_id，支持 stream=false JSON 和 stream=true SSE。GET /runs/{id} 返回 status、steps、actions、approval、final_answer、verifier；GET /runs/{id}/events?after={event_id} 支持恢复事件，POST /runs/{id}/cancel 显式取消。文件/会话/Memory/事件全部鉴权与资源校验。

所有事件 envelope：schema_version=1、event_id、run_id、timestamp、payload。event_id 为持久化序号，同一 Run 严格递增，允许全局间隙。响应中的 SSE id 与 envelope event_id 一致；客户端去重。事件和对应 DB 状态在同一短事务提交后才发送，避免收到事件却读不到状态。

唯一事件枚举：run_start、step、tool_call、tool_result、approval_required、token、verify、final、done、error。

```text
id: 101
event: approval_required
data: {"schema_version":1,"event_id":101,"run_id":"<uuid>","timestamp":"2026-10-10T00:00:00Z","payload":{"approval_id":"<uuid>","action_id":"<uuid>","action_hash":"<sha256>","tool_id":"encrypt_file","arguments":{"file_id":"<uuid>","key_id":"<uuid>","profile":"aes-gcm-v1"},"expires_at":"2026-10-10T00:15:00Z"}}

```

step 有 step_id/index/status；tool_call/tool_result 有 action_id/call_id/status；token 有 text/draft=true；verify 有 passed/checks/violations；final 有 answer/claims/citations/verification_status；done 有终态 status/计量；error 有 code/message/retryable/fatal。必要的 running→终态事件成对。token 是未验证草稿，final 才替换为最终答案。

fatal error 后持久化 done(failed/cancelled) 并结束；非致命 error 可后续恢复。审批中断时可以关闭传输但 Run 留 awaiting_approval，不能发 done(completed)。heartbeat 使用 SSE 注释，不作为业务事件。parser 按 SSE 空行组帧，处理 CRLF/多 data 行/UTF-8 跨块；发送器把 JSON 编码成单行。

disconnect_policy 在 Run 创建时保存：M2 简单同步任务默认 cancel；持久化审批/后台任务 detach。detach 流断开不取消动作；重连读取 events 和 snapshot，不重新 POST。保留窗口之外返回明确 event_history_expired 并提供 snapshot。Run events 不要求永久保留所有 token，过期状态须有快照和明确恢复规则。

<a id="contract-7"></a>
<a id="contract-7-7-证据引用与-verifier"></a>
### 证据、引用与 Verifier

chunk payload：业务 chunk_id、point_id(UUID)、document_id/version、content_hash、project_id、ACL、page_start/page_end 或 section/char_start/char_end。检索权限在 dense/sparse 候选前执行，所有路线一致。Qdrant point_id 与业务引用 ID 分离。[Qdrant point IDs](https://qdrant.tech/documentation/manage-data/points/)

index manifest 记录 corpus/parse/chunk/embed/BM25/collection 版本及 hash；入库 staging 完成后发布 active manifest，旧 Run 固定读原版本。删除/权限撤销恢复前再校验，访问权限优先于复现；必要时返回 evidence_unavailable。

Citation={source_ref,document_version,chunk_id,locator,claim_ids}。locator 用 PDF 实际页区间、Markdown section/字符区间；不允许统一 ±1 页。存在性、定位正确性、语义支持性、事实覆盖分别报告；没有引用的非 RAG 闲聊/合理拒答为 N/A。

Claim={claim_id,subject,metric,value,unit,source_refs,derivation?}。派生量 derivation 记录输入 claim/ref、公式、计算工具版本、容差。Verifier 确定性核对绑定关系与单位，LLM/NLI 辅助语义判断。source 支持不证明真实世界数据正确，synthetic fixture 永远只证明工程行为。

VerifierReport={passed,checks,violations,unsupported_claim_rate?,duration_ms}，violations 含 check/type/severity/detail/found/expected?。未知正确答案时 expected 可以缺省，但必须给修复方向，不能编造期望值。必需项 skipped/unknown 不能当 pass；unsupported_claim_rate 无事实断言时 N/A。failed 后可限次重写或输出明确未验证结果，不能展示为已验证。

<a id="api-5"></a>
<a id="api-5-5-sse合同与重连"></a>
### SSE合同与重连

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

<a id="eval-2"></a>
<a id="eval-2-2-操作知识库-rag-指标"></a>
### 操作知识库 RAG 指标

令 Q+ 为有可回答且完整 gold 的问题，Q- 为明确无答案问题。R_K(q) 为 top-K 去重结果，G(q) 为 gold 集合；K、候选级/最终级与 corpus/chunk 版本均写报告。

```text
Hit@K = mean_q[ |R_K(q) ∩ G(q)| > 0 ]
Recall@K = mean_q[ |R_K(q) ∩ G(q)| / |G(q)| ]       q 属于 Q+
MRR@K = mean_q[ 1 / 首个 relevant rank ]           无命中记0
EvidenceCoverage@K = mean_q[已覆盖必要事实槽数 / 必要事实槽数]
```

chunk/doc 两级分别计算；同文档多个 chunk 的 doc ranking 按首次出现去重。多证据任务不能用 Hit 替代 Recall；gold 若是不完整相关性标注，报告为 annotated Recall，不声称全语料 Recall。相关性与答案所需证据槽是不同标注，必要事实槽允许多个等价 chunk。

Q- 不进入正样本 Recall/MRR 分母：报告 Correct Refusal Rate（合理拒答/无答案样本）、False Refusal Rate（误拒答/可回答样本）与样本数。真实存在答案但检索失败仍是正样本失败，不能改标为 no_answer。[信息检索 Recall 定义](https://nlp.stanford.edu/IR-book/html/htmledition/evaluation-of-unranked-retrieval-sets-1.html)

引用分别报告：Citation Validity（存在、版本、授权和定位有效比例）、Citation Support（引用支持其绑定断言比例）、Claim Citation Coverage（需要引用的事实有有效支持比例）。支持性判断使用固定 Judge/NLI + 人工抽检。页码按证据真实区间，不统一放宽 ±1。要求引用却没有引用记失败；合法无引用任务记 N/A，不能统一记0。

Faithfulness = 被证据支持的原子事实断言/全部原子事实断言；Answer Correctness 按关键事实槽、数值容差、单位与期望结论判定。空分母记 N/A；无事实的空回答还要受任务成功谓词约束，不能因 Faithfulness N/A 自动通过。

<a id="agent-5"></a>
<a id="agent-5-5-context四种来源不要混用"></a>
### Context：四种来源不要混用

| 来源 | 保存什么 | 生命周期/读取范围 | 权威性与限制 |
|---|---|---|---|
| History | 用户/模型/工具的会话消息 | 当前授权session，按预算截断 | 是对话历史，模型旧回答不是资源现状 |
| Run State | 当前节点、预算、pending action、结果引用 | 一次run/checkpoint；版本化 | 恢复控制流；真实副作用以账本/Provider核对 |
| Memory | 用户偏好与可追溯事实候选 | 按user/project跨session，可纠正删除 | 不保存秘密，不把文档命令当用户偏好 |
| Knowledge | 经授权的操作资料及chunk | corpus/version/index/ACL | 支持知识结论，不证明当前证书可信或密钥有效 |

Context预算包括system、用户问题、工具schema、历史、Memory、检索证据、工具结果、预留输出。每轮记录实际prompt/completion计量与剩余预算。超长结果存blob引用，只放必要摘要；摘要不能删除资源版本、单位、否定条件和待审批动作。压缩是独立实验变量，不能在比较模型时偷偷改变。

**练习**：在一次“检查证书并解释风险”中标注哪些来自证书当前解析、哪些来自规范、哪些来自用户偏好。通过标准：不靠历史或Memory宣布证书当前有效。

<a id="agent-10"></a>
<a id="agent-10-10-verifiertrace与可观测性"></a>
### Verifier、Trace与可观测性

Verifier读取真实工具最终状态、事实来源与Citation，不能只在回答里搜索数字。事实绑定subject/metric/value/unit/source；派生值记录输入与计算依据。引用的存在、定位、支持分别判定。必需检查unknown/skipped不能当pass；无引用闲聊/合理拒答可N/A。误报与漏报使用≥20正确/20错误双集，实验指标定义见V6。

Trace同时记录提议、拒绝、执行与结果，不把它们合并。关联request_id/run_id/step_id/action_id/call_id与event_id，测total与各段耗时，人工审批等待单列。只保存必要脱敏参数和摘要；模型thinking如记录须同样审查敏感信息与访问权限。

**排错顺序**：前端快照/事件 → API身份/Run → 模型原始调用 → registry/schema → policy/approval → action账本 → Provider产物 → Claim/Citation → Verifier。按证据定位，不因模型回答错就先换模型。

<a id="full-m3"></a>
<a id="full-m3-m370h"></a>
#### M3（70h）

- [ ] 目标5：PDF/MD/TXT真实样本，扫描页需OCR、复杂表格限制记录。
- [ ] chunk有版本/hash/定位/project/ACL，业务chunk_id与Qdrant UUID point_id分开。
- [ ] staging→active索引发布；重复入库、更新/删除、失败恢复一致。
- [ ] dense/sparse/rerank/引用在服务端遵守相同授权。
- [ ] 目标6：dense/BM25/RRF/rerank四组消融，rewrite另开关。
- [ ] ≥50条审定RAG问题，正样本与无答案分开；gold从源文档和多路候选审定。
- [ ] Hit/Recall/MRR/证据覆盖/引用有效与支持/正确拒答/误拒答与n都报告。
- [ ] corpus/index/config冻结，失败用例与延迟分析，m3-done。

<a id="rag-drafts"></a>
<a id="rag-drafts-密码工具操作知识检索起步草稿"></a>
## 密码工具操作知识检索起步草稿

下表8题围绕本项目的工具、操作规则和能力范围，仅供起步练习，不代表M3要求的至少50题已经完成。由你在代码仓库建立自己的评测数据；来源入库、gold chunk和必要事实槽需逐条人工核对。

| ID | 问题 | 预期可答性 | 起步来源 |
|---|---|---|---|
| rag-001 | 解析证书成功是否说明证书链可信？ | answerable | [V1证书结果契约](V1-CORE-DEMO.md#crypto-6.3) |
| rag-002 | 系统OpenSSL CLI和Python密码包后端为什么要分别记录版本？ | answerable | [V1 OpenSSL能力](V1-CORE-DEMO.md#crypto-3.1) |
| rag-003 | 同一密钥版本下nonce为什么必须由服务端管理唯一性？ | answerable | [V4认证加密](V4-APPROVAL-CRYPTO.md#crypto-6.1) |
| rag-004 | 修改认证数据后，解密应怎样处理输出文件？ | answerable | [V4认证加密](V4-APPROVAL-CRYPTO.md#crypto-6.1) |
| rag-005 | 证书验证应记录哪些时钟、域名、用途和信任根条件？ | answerable | [V1证书结果契约](V1-CORE-DEMO.md#crypto-6.3) |
| rag-006 | 轮换后旧密文应关联哪个密钥版本？ | answerable | [V4 keystore版本](V4-APPROVAL-CRYPTO.md#crypto-5) |
| rag-007 | 签名验证通过与签名者身份可信有什么区别？ | answerable | [V6签名验签](V6-DELIVERY.md#crypto-6.2) |
| rag-008 | 未收录的HSM型号X，其接口超时默认值是多少？ | unanswerable | 语料覆盖需审定 |

准备索引后，在代码仓库记录证据清单与逐题gold映射，再把真实chunk、事实槽与定位写回评测记录。Markdown来源使用章节/字符定位；页码仅用于实际PDF。无答案题也须在实际语料中核对，不以top-K没命中作为无答案依据。冻结流程见[评测说明](V6-DELIVERY.md#dataset-1)。

## 本阶段签收清单

- [ ] 本阶段学习技术表逐项有本人解释、独立实现/修改和失败验证证据。
- [ ] Q01–Q22已由本人结合实现作答，证据与未覆盖边界记入docs/progress.md；AI仅审查。

- [ ] 基础RAG后补完整Verifier；三格式/版本/授权/定位/无答案与≥20错20对通过。
- [ ] Memory来源/改口/删除/隔离/无关防护通过，检索≥50审定题和四组消融齐全。
- [ ] SSE/前端引用/去重重连同Run通过，当前阶段出口与未完专项登记。
- [ ] 目标5/6全表通过可标m3-done，不把V5视为全部M5技术毕业。

## 下一步

本阶段出口有证据后进入[V6阶段](V6-DELIVERY.md)。跨阶段未完标准登记补齐位置。
