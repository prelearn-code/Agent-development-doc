# 密码工具 Agent 评测与冻结流程

## 1. 起步资料与检查入口

本目录提供 **8条RAG、11条Tool、5条综合草稿**，均为schema_version=3、status=draft、split=dev；对应8行gold映射是回填模板，不是额外测试。草稿描述本项目的证书检查、摘要、密钥元数据、逐项审批加密和报告偏好。文件字节和元数据示例明确标synthetic；证书、密钥材料与知识索引尚待准备，标为resolved=false。

```bash
cd /home/zsw/work/agent_development/Agent-development-doc
python3 eval/validate_dataset.py --all --mode draft
python3 -m unittest discover -s eval -p 'test_*.py' -v
python3 scripts/check_docs.py
```

草稿检查允许明确未完成项并报告warning，不代表Agent或密码功能已通过。正式门禁示例：

```bash
python3 eval/validate_dataset.py eval/seed-eval-dataset.jsonl --mode frozen --evidence-manifest eval/evidence-manifest.template.json
```

当前草稿执行正式门禁应失败。准备真实资源、证据与人工审定后，对冻结文件执行该命令。

## 2. 字段与工具契约

[dataset.schema.json](dataset.schema.json)定义字段和枚举，[validate_dataset.py](validate_dataset.py)检查结构、语义与冻结条件；应用工具契约见[repo-structure.md](../repo-structure.md)，指标见[02-MODEL-AND-EVAL.md](../02-MODEL-AND-EVAL.md)。离线校验器不执行真实Agent、Provider或指标计算。

公共字段包含id、schema_version、status、split、group_id、category、difficulty、question、answerability、expected_behavior、fixture_refs、allowed_tool_plans、gold_calls、success_criteria、provenance。RAG增加gold_chunk_ids/gold_doc_ids/gold_pages/gold_section/gold_fact_slots；场景增加scenario。未知字段拒绝，字段或工具范围变更通过版本管理同步schema、validator与应用registry。

本项目canonical工具为证书解析/验证、文件摘要、签名验签、密钥元数据、加解密、签名、轮换、CSR、测试签发、知识检索和固定元数据查询；工具ID与结构文档一致。intent_crypto表示密码操作意图，不替代权限或审批。

status=ready仅说明内容经审定，不能代表应用测试成功。ready/frozen要求provenance中reviewer_kind=human、实际verified_by和ISO reviewed_at。AI生成的草稿保留synthesized与空审核字段；测试模块中的mock审核仅用于验证门禁。

## 3. 成功条件

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

## 4. 场景与审批

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

## 5. Fixture与证据准备

[fixtures.json](fixtures.json)定义id/kind/resolved/source/data。small_files_sample是3个公开教学字节样本；key_metadata_sample仅是元数据，不含真实材料；tool_failures_sample提供固定时钟的调用排行预期。fixture别名由应用Runner映射为隔离namespace内的UUID。

certificate_draft、key_material_draft和crypto_corpus_draft保持unresolved。后续按[Provider练习](../06-CRYPTO-AGENT-SCOPE.md#10-后续可以照着操作的-provider-入门练习)准备样本，核对实际字段与参数后更新记录。只填resolved=true而没有对应资源不构成验收。

[evidence-manifest.template.json](evidence-manifest.template.json)保留空chunks；索引完成后填manifest_version、corpus_version、chunk_id、doc_id、document_version、locator、content_hash。Qdrant point_id与业务chunk_id分开。[gold映射模板](gt-chunk-ids.template.jsonl)逐题回填后同步到RAG记录，实际事实槽仍需逐条审定。

## 6. 标注、冻结与回归

1. 按实际密码工具与操作文档核对问题可答性、能力范围和所需参数。
2. RAG合并多路检索候选并直接查原文，核对真实gold和必要事实；top-K未命中不直接改为无答案。
3. 数值绑定fixture或真实快照的实体、字段、单位和版本；派生值独立计算。
4. 逐条人工审定，补审核者与日期；20%抽检只用于批次质量判断，不代替其余记录的审核。
5. 相关来源、模板和场景按group整体划分dev/test；test不用于反复调参。
6. 冻结要求ready、无TODO、fixture已准备、证据真实、成功条件有效、场景支持且审批明确。
7. 每个实验/重复/case隔离user/project/session/文件/索引/Memory；cleanup只清理自己的namespace。
8. 固定dataset/schema/fixture/corpus/index/environment hash与模型digest；结果一对一配对，缺失、重复、额外和超时不可静默跳过。

后续目标仍为RAG≥50、Tool≥50、综合100–180条逐项审定用例。当前24条草稿仅帮助起步，不包含完整安全回归，也不能替代最终题库和应用运行证据。

## 7. 按交付阶段积累，V6完成正式冻结

V1记录少量证书/摘要/Loop的明确输入输出与失败；V2增加API/幂等/权限；V3直调/MCP对照；V4逐动作审批与故障恢复；V5完成RAG≥50/四组检索及Verifier正误双集、Memory；V6固定完整工具池后完成Tool≥50、100–180综合、隔离Runner/cleanup/配对报告。

M5 09/12是稳定任务ID，草稿从V1开始，正式范围到V6完成；manual小case不冒充Runner或frozen。原schema_version=3、canonical 13工具、人工审定/真实fixture/证据/审批门禁均保持。各V目标和预算见[00](../00-ROADMAP.md)，task切片见[05](../05-UBUNTU-STEP-BY-STEP.md)。
