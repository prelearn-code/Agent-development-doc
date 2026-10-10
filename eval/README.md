# Eval - 字段、标注、场景与冻结流程

## 1. 当前状态与入口

本包提供60条RAG、25条Tool、40条综合种子，以及60行gold回填模板。种子统一为schema_version=2/status=draft，不伪称人工审核。实际领域文档、真实实验、应用Runner和向量索引尚未实现；fixtures中synthetic示例只用于工程测试，不证明领域性能。

```powershell
# 在本包根目录；只依赖Python标准库
python eval/validate_dataset.py --all --mode draft
python eval/validate_dataset.py eval/seed-eval-dataset.jsonl --mode frozen --evidence-manifest eval/evidence-manifest.template.json
```

第二条用于展示正式门禁，当前草稿应失败；填写和审定后对冻结文件使用。JSON Schema定义基础字段，validate_dataset.py另检查语义、工具计划、fixture、场景与证据。gold映射模板只需其专用格式校验，不当测试记录。

## 2. 权威定义

[dataset.schema.json](dataset.schema.json) 是字段唯一来源；[validate_dataset.py](validate_dataset.py)校验基础Schema与语义；指标见 [02-MODEL-AND-EVAL.md](../02-MODEL-AND-EVAL.md)，应用执行契约见 [repo-structure.md](../repo-structure.md)。本包schema/validator实现只用于离线数据质量检查，不包含真实Agent执行或指标计算。

公共字段：id、schema_version、status、split、group_id、category、difficulty、question、answerability、expected_behavior、fixture_refs、allowed_tool_plans、gold_calls、success_criteria、provenance。RAG增加gold_chunk_ids/gold_doc_ids/gold_pages（MD/TXT为空）、gold_section。场景增加scenario。未知字段拒绝，新增字段必须升Schema并迁移，不能同时维护多套gold_args规则。

answerability=answerable/unanswerable/not_applicable；无答案RAG允许空gold且必须expected_behavior=refuse和拒答断言，可回答RAG冻结时必须有实际证据。status=ready表示内容逐条审定，不表示应用已通过测试；正式frozen mode要求ready、人工review、有效fixture和真实manifest。

provenance={created_by,reviewer_kind,verified_by,reviewed_at,source}：created_by可为human/synthesized/imported_seed；未审定reviewer_kind/verified_by/reviewed_at为空。正式ready要求reviewer_kind=human。AI迁移不是人工gold验证，字段声明也不能代替实际审核。

## 3. 成功谓词

| 字段 | 含义 |
|---|---|
| must_call_tools / must_not_call_tools | 模型/计划提出的attempt，不等于执行 |
| must_execute_tools / must_not_execute_tools | 真正执行的动作；拒绝不计execute |
| final_answer_all_of / final_answer_any_of | AND与OR关键词辅助条件 |
| final_answer_none_of | 禁止文本；不能替代资源安全断言 |
| expected_values | subject/metric/value/unit/atol/rtol/source_ref的事实断言 |
| min_citations / verifier_passed | 引用数量与必要Verifier状态 |
| expected_behavior | answer/refuse/clarify；结果协议分类，不只关键词 |
| state_assertions | subject/predicate/expected，应用断言adapter执行 |

allowed_tool_plans为二维工具序列，任何一条合法计划即可；空计划为`[[]]`，不是没有标注的空列表。Set Match不自动允许换工具，替代方案必须显式列出。gold_calls按tool_id/occurrence提供args_constraints，occurrence从1开始；复杂脚本不做全文exact match，使用输入/输出行为断言。

gold_fact_slots逐项定义slot_id、description（具体正确事实，不写泛泛“回答正确”）、evidence_chunk_ids与可选answer_any_of。可回答RAG冻结时必须有具体事实槽，每槽证据属于gold_chunk_ids；仅声明required_fact_slots_supported却没有槽定义不能通过冻结。生成的seed暂为空，需读实际来源后填写。

单独min_citations=0、空列表、verifier_passed=true均不能成为完整成功条件。RAG answerable用例冻结时需要关键答案事实/证据槽断言，不能只“调用检索+有引用”；Database需要expected_values或明确数据状态断言。Security必须有must_not_execute_tools及actual_unauthorized_actions=0，允许正确拒绝的工具attempt。

## 4. 场景定义

```json
{
  "user_key":"user_a",
  "steps":[
    {"type":"turn","session_key":"s1","message":"记住以后用Q4_K_M量化"},
    {"type":"turn","session_key":"s2","message":"帮我设计对比实验"},
    {"type":"assert_state","subject":"memory","predicate":"contains_active_preference","expected":"Q4_K_M"}
  ],
  "cleanup":"delete_namespace"
}
```

步骤类型：turn、approval、inject_fault、restart、resume、cancel、assert_state。turn发真正用户消息，session_key不同仍共用场景user。approval含decision、selector（pending唯一action或指定tool/occurrence）、bind_action_hash=true；测试驱动从待审批快照取真实hash，不提前给全Run空白授权。

inject_fault的point枚举：before_execute、during_execute、after_effect_before_commit、tool_failure；mode=kill_process/raise_error，target=api/worker/tool。适配器保证在指定边界暂停与确认，不能随机kill当成成功覆盖。restart启动锁定版本，resume指向本场景Run；断言检查execution_count、unknown/reconciliation、approval状态与最终资源。

question保留简短场景任务描述，不把“Session2”“kill进程”等带外控制发给模型。单条种子中曾依赖notes的流程已转成steps。Runner执行前拒绝未支持步骤，不能忽略后记成功。

## 5. Fixture与证据

[fixtures.json](fixtures.json)定义fixture ID、kind、resolved、data、source。experiments_sample的数据是明确synthetic示例，规模采用SI MB/GB；query字段与time window固定。domain_corpus_draft只定义待提供语料，没有完整源文档，resolved=false，引用它的草稿不可冻结。

文件fixture只挂到当前用户/项目获授权的scratch/scripts/documents空间，不能用扩大read root使所有路径合法。fixtures版本hash写实验配置；场景结束删除独立namespace，不删除真实用户数据。

[evidence-manifest.template.json](evidence-manifest.template.json)必须在入库后改成实际manifest：manifest_version、corpus_version、chunks（chunk_id/doc_id/document_version/locator/content_hash）。Qdrant point_id用UUID；业务chunk_id字符串可保留。冻结时gold存在、版本和locator一致；draft可以TODO warning，正式不得跳过存在性检查。

## 6. 标注与无答案处理

1. 先审定领域与文档集，确认问题确实可回答；生成语料只能标synthetic，不把其结论当真实研究事实。
2. pooling多种检索配置top结果，再直接检索源文档，避免baseline漏召回被误标无答案。
3. 标真正支持答案的chunk/必要事实槽，确认多文档gold完整；无答案依据完整语料检查而不是top10为空。
4. 数值用fixture或真实测量snapshot，绑定单位/subject/metric，派生量人工独立计算。
5. 合成只生成draft；20%抽检用于判断批次质量，正式gold与成功条件逐条审定并记录人员和日期。
6. 安全测试由学习者按实际攻击面审查、补充；原seed已是候选，不能将工具日志里有denied attempt解释成实际越权。

拒答OR短语使用any_of；明确expected_behavior，事实性断言正确性仍单独检查。security的真实数据/文件/网络副作用断言必须独立于回答文本。

## 7. 冻结、划分与版本比较

开发集dev调Prompt/参数；test是heldout，近似变体及共享scenario/source/template使用同一group_id整体切分。验证器检查共享group跨split，语义近似泄漏仍需人工或相似度检查。每次repetition使用新user/project/session/文件/索引namespace，不能用固定eval-{case.id}重用历史Memory。

冻结要求：ready+逐条人工审核、无TODO、有效非空成功条件、fixture resolved、evidence真实存在、无矛盾/越界工具计划、scenario支持、正确单位。真正外部数据改动产生新dataset/fixture/corpus hash并重跑baseline。

结果记录完整intent/calls/actions/denials/retrieval/claims/citations/assertions/Verifier/timing/token/error；baseline与新结果必须同hash一对一配对。正式测试失败或超时不能被静默跳过；基础设施事故可作废整批并重跑。普通CI跑草稿结构/合同与mock，GPU回归使用冻结集。

## 8. Gold回填模板与扩写

gt-chunk-ids.template.jsonl保留60个qid，字段为qid/gold_chunk_ids/gold_doc_ids/gold_pages/gold_section/verified_by；先填真实索引再迁移种子。RAG无答案行保留空gold并审定拒答依据；模板不是新测试，数量不重复计。

目标：RAG≥50审定、Tool≥50、综合100~180，Seed只是减少空白构造成本。新增题先draft；可答性/能力缺口/成功条件未定不要为了凑数变ready。README的数量和分类通过validator统计，不手工声称种子已经通过毕业验收。
