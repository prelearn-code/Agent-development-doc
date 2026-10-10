# 密码工具操作知识检索起步草稿

本页与[JSONL草稿](seed-rag-questions.jsonl)对应。问题都围绕本项目的工具、操作规则和能力范围。当前8题仅供起步，不代表M3要求的至少50题已经完成；来源入库、gold chunk和必要事实槽需逐条人工核对。

| ID | 问题 | 预期可答性 | 起步来源 |
|---|---|---|---|
| rag-001 | 解析证书成功是否说明证书链可信？ | answerable | 06文档第6.3节 |
| rag-002 | 系统OpenSSL CLI和Python密码包后端为什么要分别记录版本？ | answerable | 06文档第3.1节 |
| rag-003 | 同一密钥版本下nonce为什么必须由服务端管理唯一性？ | answerable | 06文档第6.1节 |
| rag-004 | 修改认证数据后，解密应怎样处理输出文件？ | answerable | 06文档第6.1节 |
| rag-005 | 证书验证应记录哪些时钟、域名、用途和信任根条件？ | answerable | 06文档第6.3节 |
| rag-006 | 轮换后旧密文应关联哪个密钥版本？ | answerable | 06文档第5.3节 |
| rag-007 | 签名验证通过与签名者身份可信有什么区别？ | answerable | 06文档第6.2节 |
| rag-008 | 未收录的HSM型号X，其接口超时默认值是多少？ | unanswerable | 语料覆盖需审定 |

准备索引后填写[证据清单](evidence-manifest.template.json)和[gold映射](gt-chunk-ids.template.jsonl)，再把真实chunk、事实槽与定位写回记录。Markdown来源使用章节/字符定位；页码仅用于实际PDF。无答案题也须在实际语料中核对，不以top-K没命中作为无答案依据。冻结流程见[评测说明](README.md)。
