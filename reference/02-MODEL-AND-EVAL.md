# 02 - 模型矩阵、指标与实验协议

> 按需参考资料。实现步骤与阶段目标集中在[学习总览](../LEARNING-PATH.md)及对应阶段，不需要先通读本文件。

> 本文件定义指标；数据记录字段见 [eval/dataset.schema.json](../eval/dataset.schema.json)，执行与标注流程见 [eval/README.md](../eval/README.md)。基线在实测后冻结，以下性能/显存数值仅用于选起点。

## 1. 模型与推理配置

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

## 2. 操作知识库 RAG 指标

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

## 3. Agent 指标

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

## 4. 延迟、token 与显存

串行运行 baseline；并发实验单列。报告 total_ms、time_to_first_token_ms、time_to_verified_final_ms、retrieval/rerank/LLM/tool/verify_ms。LLM load 与推理分开，warm total 仍包含流程中真实换模。人工审批等待不混入系统 latency，单报 approval_wait_ms；自动审批 fixture 只能批准具体 action hash。

每次配置预热固定模型和固定路径，冷启动另外测。p50/p95/max 是基本报告，p99 在小样本时不稳，应带 n 与计算方法且不作硬门槛。超时/失败也记录耗时，不只统计成功题；并行分段耗时之和可能超过 wall clock，要注明。

token 从每次 llm_calls 实际返回的 prompt/completion 计数聚合，区分 Controller、rewrite、Memory、Verifier 和离线 Judge。Judge token 不加入在线 Agent 成本；不要用不匹配 Qwen 分词器的 tiktoken 估计充当实测值。记录 think/template 与 token 来源。

显存在**整次任务**周期采样，GPU总峰值、空闲基线与进程归因分别记录；Ubuntu 内用 `nvidia-smi --query-compute-apps` 做进程级归因，无法精确归因时明确限制，不只看第一个任务或加载瞬间。记录 Ubuntu 内可见显存与实测空闲占用，不用宿主机记录值代替。

## 5. 数据与实验冻结

最终目标 180 条：Intent20/RAG30/Tool25/Database20/Workflow20/Memory15/Security25/Complex Task25。预算不足可先冻结100条，必须列各类样本与缺口。本项目起步草稿用于示范记录结构，正式题库从证书、摘要、加解密、密钥与操作知识中逐项审定；复用问题记录ID，不重复计为独立新样本。

合成问题仅产生 draft；逐条审定 gold/关键成功条件并记录 verified_by/reviewed_at。20% 抽检只决定整批是否需要返工，不能把剩余80%标为“human verified”。近义变体、同一 source/template/场景组整体进入同一 split，避免 dev/test 泄漏。

每次报告固定 dataset/schema/fixture/corpus/index hash、git_commit、环境锁、模型 digest、配置、Judge 配置与校准集。freeze 要检查没有 TODO、有效 fixture、证据清单和审核；可选工具组更改必须同步 registry 与测试，不悄悄改 gold 适配模型结果。

结果保留 predicted_intent、proposed_calls、executed_actions、denied_attempts、retrieved_chunk_ids/版本、claims/citations、state_assertions、verifier、error、timings、tokens 和测试用例 ID。结果按 dataset ID 一对一关联；缺失/额外结果、重复 ID 是无效报告。

## 6. 场景 Runner

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

## 7. 比较、统计与 CI

同一冻结数据/环境/Judge 做配对比较，配置至少3次，报告逐次结果、均值、方差和区间。Task Success 的百分点用 pp：40题的一题=2.5pp，180题的一题约0.56pp；-2pp 阈值必须结合样本量、case 回归和置信区间解释。重复结果不允许只挑最好一次；多数投票单列为一种策略。

冻结测试集禁止用于选 prompt/router threshold；用 dev 选配置，test 做最终报告。Judge 先生成所有配置结果，再统一离线判定，避免换模污染在线耗时。Judge 与人工一致率先用至少20条双标样本初测，低于80%时审查类别分歧、修规则或标指标不可靠；不能只改 Judge 直到偏好自己答案。

CI 普通任务跑校验、mock 场景和确定性安全测试；本地 GPU 任务用 frozen。compare 检查全部 hash 相同，列 case-level regressions 与通过数；安全实际越权任何一条失败阻塞。性能门槛以本机 baseline 后确定，不在未测量前声明固定500ms保证。

## 8. 三个必做实验

1. RAG 四组消融：同语料/切分/问题，检索质量与生成结果分阶段测；rewrite 单独开关。
2. 4B/9B±router，可选27B：同候选工具/上下文/think/Judge/fixture。压力工具池另列。
3. Verifier：已知错误与已知正确双集，覆盖实体错绑、单位、派生值、引用版本/定位/支持，TPR/FPR附样本量和漏报误报。

报告模板：问题、固定项与变量、环境与hash、适用样本数、结果/区间、失败用例、限制和下一步。按证据回答改动是否有益，不要求复杂配置必须胜过 baseline。


## 9. 学习阶段与变更回归门禁

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

个人学习通过标准见[学习总览](../LEARNING-PATH.md)，全链路与证据清单见[09](09-DELIVERY-AND-ACCEPTANCE.md)。先有baseline再确定质量/性能阈值；示例百分点或耗时不是未实测的硬保证。实际越权必须0，任何相关确定性安全回归失败阻止发布。修数据错误需要证据、版本变更和重跑原配置，不覆盖旧报告；test不可用于反复调阈值。

## 10. 小批学习验证与完整实验的时机

| 交付阶段 | 当前验证范围 | 正式规模与剩余验收 |
|---|---|---|
| V1 | 证书/摘要、手写反馈、失败/预算，小case与成功谓词 | 不要求100题，也不称frozen baseline |
| V2 | 身份/上传/Run幂等、快照/UI、DB重启 | SSE/六查询专项分别V5/V6 |
| V3 | 两只读工具直调/MCP正常/拒绝/失败对照 | 三职责与完整端点V6 |
| V4 | 一种加解密、固定审批、结果状态、故障核对 | 全工具≥50题/完整安全/图兼容V6 |
| V5 | RAG≥50、四组检索、Verifier≥20错20对、Memory、SSE | 模型矩阵与全类Scenario V6 |
| V6 | 固定工具池后四模型配置各3次、100–180综合frozen、配对compare | 全部指标口径和正式门禁不降低 |

早期测试不是另加一套工时，属于当前目标练习；正式Runner/数据预算在目标13/V6，人工审定仍逐条。RAG/Tool专项可复用唯一case ID但不重复计数；基础权限/审批/秘密/状态错误从第一天就阻止当前功能交付。按[学习总览](../LEARNING-PATH.md)与[学习总览](../LEARNING-PATH.md)区分交付通过和全目标毕业。
