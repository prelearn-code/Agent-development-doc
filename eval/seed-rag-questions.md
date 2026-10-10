# RAG检索评测种子（60条）

> 机器字段以[seed-rag-questions.jsonl](seed-rag-questions.jsonl)为准。全部为draft；58条可回答假设待实际语料审定，2条无答案假设也必须核对完整语料。TODO不是有效证据。

## 问题清单

| id | 问题 | 类型 | 难度 | 可答性假设 | 预期文档（待核对） |
|---|---|---|---|---|---|
| rag-001 | 完整性审计算法要解决的核心问题是什么？ | concept | easy | answerable | doc_algo |
| rag-002 | 审计协议里挑战（challenge）和证明（proof）分别由谁生成？ | proc | easy | answerable | doc_algo |
| rag-003 | 抽样策略为什么采用分层抽样而不是简单随机抽样？ | concept | medium | answerable | doc_algo |
| rag-004 | 分层抽样的层（stratum）是怎么划分的？ | proc | medium | answerable | doc_algo |
| rag-005 | 每次审计抽取的样本块数量是如何确定的？ | num | medium | answerable | doc_algo |
| rag-006 | 漏报率（false negative rate）与抽样比例之间的关系是什么？ | concept | hard | answerable | doc_algo |
| rag-007 | 审计算法的安全假设有哪些？ | concept | medium | answerable | doc_algo |
| rag-008 | 算法如何抵抗重放攻击？ | concept | medium | answerable | doc_algo |
| rag-009 | 审计失败时的恢复流程是什么？ | proc | hard | answerable | doc_algo |
| rag-010 | 算法支持哪些类型的数据损坏检测？请列举。 | proc | medium | answerable | doc_algo |
| rag-011 | 审计过程中的时间戳机制起什么作用？ | concept | medium | answerable | doc_algo |
| rag-012 | 与基于签名的方案相比，本算法的计算开销优势来自哪里？ | compare | hard | answerable | doc_algo |
| rag-013 | Merkle 树在这里的叶子节点存储的是什么？ | term | easy | answerable | doc_merkle |
| rag-014 | Merkle 证明路径的长度是多少？与什么有关？ | num | medium | answerable | doc_merkle |
| rag-015 | 树的分支因子（branching factor）选了多少？为什么这么选？ | num | medium | answerable | doc_merkle |
| rag-016 | 批量验证多个证明时如何减少哈希计算次数？ | proc | hard | answerable | doc_merkle |
| rag-017 | 树的结构在数据更新时如何维护？ | proc | medium | answerable | doc_merkle |
| rag-018 | 与二叉 Merkle 树相比，多叉树的通信开销如何变化？ | compare | hard | answerable | doc_merkle |
| rag-019 | 证明缓存（proof caching）策略解决了什么问题？ | concept | medium | answerable | doc_merkle |
| rag-020 | 哈希函数选的是哪一个？为什么不选其他？ | term | easy | answerable | doc_merkle |
| rag-021 | 树高对验证时间复杂度的影响是什么？ | concept | medium | answerable | doc_merkle |
| rag-022 | 增量更新场景下，树的重建代价是多少？ | num | hard | answerable | doc_merkle |
| rag-023 | 系统采用的纠删码参数 (k, m) 是多少？ | num | easy | answerable | doc_erasure |
| rag-024 | 纠删码的冗余度是怎么计算的？ | num | medium | answerable | doc_erasure |
| rag-025 | 单块损坏时修复需要读取多少数据？ | num | medium | answerable | doc_erasure |
| rag-026 | 纠删码与三副本方案的存储开销对比是多少？ | compare | medium | answerable | doc_erasure |
| rag-027 | 修复带宽（repair bandwidth）如何优化？ | proc | hard | answerable | doc_erasure |
| rag-028 | 为什么审计算法需要与纠删码协同设计？ | concept | hard | answerable | doc_erasure |
| rag-029 | 编码块和校验块在审计中的处理有什么区别？ | compare | medium | answerable | doc_erasure |
| rag-030 | 纠删码参数变化对审计精度有什么影响？ | concept | hard | answerable | doc_erasure |
| rag-031 | 实验是在什么环境下进行的？节点配置是什么？ | term | easy | answerable | doc_experiment |
| rag-032 | 三档数据规模（100MB/500MB/1GB）是怎么定义的？ | num | easy | answerable | doc_experiment |
| rag-033 | 每个实验配置重复运行了几次？报告的是均值还是中位数？ | num | easy | answerable | doc_experiment |
| rag-034 | 通信开销是怎么计量的？包含哪些部分？ | term | medium | answerable | doc_metrics |
| rag-035 | 计算开销的定义是什么？与 CPU 时间有什么区别？ | term | medium | answerable | doc_metrics |
| rag-036 | 审计精度是如何评测的？ | proc | medium | answerable | doc_metrics |
| rag-037 | 实验中的故障注入有哪些类型？ | proc | medium | answerable | doc_experiment |
| rag-038 | 为什么用 p95 而不是平均值报告延迟？ | concept | medium | answerable | doc_metrics |
| rag-039 | 实验的对照组设置是什么？ | term | medium | answerable | doc_experiment |
| rag-040 | 测量审计时间时，哪些部分被排除在外？ | num | hard | answerable | doc_experiment |
| rag-041 | 100MB 数据规模下的审计时间是多少？ | num | easy | answerable | doc_results |
| rag-042 | 500MB 数据规模下的通信开销是多少？ | num | easy | answerable | doc_results |
| rag-043 | 1GB 规模下的 CPU 时间是多少？ | num | easy | answerable | doc_results |
| rag-044 | 从 100MB 到 1GB，审计时间增长了多少倍？ | num | medium | answerable | doc_results |
| rag-045 | 通信开销随数据规模是线性增长吗？ | concept | medium | answerable | doc_results |
| rag-046 | 哪个规模下计算开销占比最高？ | compare | medium | answerable | doc_results |
| rag-047 | 与 baseline 方案相比，吞吐量提升了多少？ | compare | medium | answerable | doc_results, doc_baseline |
| rag-048 | 峰值内存占用随规模如何变化？ | num | medium | answerable | doc_results |
| rag-049 | 哪些实验配置出现了异常值？原因是什么？ | concept | hard | answerable | doc_results |
| rag-050 | 实验结果的方差有多大？统计上显著吗？ | num | hard | answerable | doc_results |
| rag-051 | 不同节点数配置下，审计时间如何变化？ | num | medium | answerable | doc_results |
| rag-052 | 故障注入实验的漏检率是多少？ | num | medium | answerable | doc_results |
| rag-053 | 抽样比例是如何影响通信开销和漏报率的？ | multi | hard | answerable | doc_algo, doc_metrics |
| rag-054 | Merkle 树的分支因子选择如何影响审计的通信开销？ | multi | hard | answerable | doc_merkle, doc_metrics |
| rag-055 | 纠删码的冗余度与审计精度之间是什么关系？ | multi | hard | answerable | doc_erasure, doc_metrics |
| rag-056 | 完整走一遍审计流程需要调用哪些组件？各自的作用是什么？ | multi | hard | answerable | doc_spec, doc_algo, doc_merkle |
| rag-057 | 如果数据规模再扩大 10 倍，哪些指标会成为瓶颈？ | multi | hard | answerable | doc_results, doc_metrics |
| rag-058 | 与 baseline 方案相比，本方案在通信和计算两个维度上的取舍是什么？ | compare | hard | answerable | doc_baseline, doc_results |
| rag-059 | 这个系统支持 GPU 加速审计吗？ | concept | medium | unanswerable | 待核对无答案 |
| rag-060 | 审计日志的保留策略是多久？ | num | medium | unanswerable | 待核对无答案 |

## 使用与扩写

1. 先核对真实语料，再pool多路候选并回到原文审定gold；baseline检索不到不等于无答案。
2. 多证据题标必要事实槽与所有支持来源；MD/TXT使用section/字符定位，不填虚构页码。
3. 新增近义变体保留同group_id并同split，正式heldout不参与调参。
4. 按qt/difficulty分层报告Hit/Recall/MRR/证据覆盖；Hybrid是否更优是实验结果，不预先保证。
5. 回填映射模板并逐条审定后使用frozen校验，流程见[README.md](README.md)。
