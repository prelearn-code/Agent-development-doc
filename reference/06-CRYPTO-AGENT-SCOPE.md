# OpenSSL GmSSL Agent 业务范围与验收设计

> 按需参考资料。实现步骤与阶段目标集中在[学习总览](../LEARNING-PATH.md)及对应阶段，不需要先通读本文件。

本项目使用 OpenSSL 和 GmSSL 的简单封装来学习 AI Agent 全栈开发。业务目标是通过网页与自然语言完成受控的密码工具操作：摘要、证书检查、签名验签、小文件加解密，以及测试密钥和证书的元数据管理。模型负责理解任务与编排；运算、权限、资源状态和结果验证由程序完成。

本文定义领域任务、适配层、风险与首版范围；实施顺序见 [学习总览](../LEARNING-PATH.md)。这里的工具、业务表与页面都是**待实现设计**，在对应学习阶段完成并验收。

## 1 为什么选这个场景

密码工具业务具有可独立核对的结果。摘要能与已知向量或直接命令比较；加解密能做字节往返与认证失败检查；签名能验签；证书能比较字段、信任链、用途、域名与时间。它适合检验 Agent 有没有选对工具、填对参数、遵守授权，以及有没有把失败说成成功。

小模型仍可能选错工具或填错参数，所以本场景不会自动解决模型能力问题。设计时先让模型接触少量、职责清楚的工具；模型错误应变成可解释的澄清、拒绝或工具失败，而非错误密码操作。

你需要学习的是“将可靠工具变成可用的 Agent 产品”。密码理论先达到接口正确使用的程度，算法性能研究、标准符合性证明和产品认证不纳入首版工时。

## 2 首版与完整学习版

### 2.1 第一条可用闭环

第一个Demo：**终端问题→digest_file提议→受控OpenSSL摘要→真实结果反馈→回答与Trace**。V1先完成这条单工具链，再加公开证书工具；详细步骤见[V1](../stages/V1-CORE-DEMO.md#first-demo)。接着扩展为**上传公开证书或教学文件→自然语言提问→只读证书/摘要工具→JSON结果/Trace→网页与Run历史**，V2完成网页，不等待RAG、MCP或审批。

V3给同一业务服务加一个Crypto MCP Server；V4再加一种审批后的加解密与恢复。第一网页不需要先实现SSE/完整Verifier/生产部署；它仍必须有身份/资源权限、受控文件、真实错误与请求幂等。

### 2.2 功能优先级

| 交付节点 | 密码业务功能 | 此时新增Agent能力 |
|---|---|---|
| V0环境 | 公开教学材料/Provider路线 | 请求/配置/首测 |
| V1核心调用 | 公开证书解析、SHA-256/后补SM3 | 手写Loop、schema/授权/预算/Trace |
| V2第一网页 | 授权上传、只读结果、公开元数据 | API/DB/基础React/快照 |
| V3 MCP | 原证书/摘要工具复用 | 一个Crypto Server、协议/bridge/对照 |
| V4审批密码版 | 一种≤1MiB认证加解密、key version、artifact | 固定审批/账本/最小Graph/恢复/必要结果检查 |
| V5可靠性 | 操作知识/错误解释、用户报告偏好 | RAG/引用/Verifier/Memory/检索消融/SSE |
| V6完整学习 | 轮换、签名验签、CSR/测试签发与完整工具范围 | 三职责MCP、模型/正式场景/安全、完整UI/部署 |
| 后续扩展 | 生产CA/吊销、HSM/KMS/ACME/国密TLS等 | 另列领域工程预算 |

两个Provider不用逐API对称；第二Provider先摘要/验签即可，实际未支持明确unsupported。V4首种profile固定，扩充格式/算法先能力验证，不能静默替换。

### 2.3 首版节点与完整学习版的边界

按V0→V1→V2先拿到只读网页，再V3一个MCP、V4审批密码版，最后V5/V6补齐全课程。首版有三种清晰节点：V2只读网页、V3MCP复用、V4审批写操作，不把它们混称完整毕业。

V2不开放密码写工具，基本身份/资源/秘密/错误/Trace/请求幂等先完成；V4开放写动作时固定审批、版本、账本、故障核对必须完成。各技术任务前缀仍P0/M1–M6，用05导航表定位，不沿M前缀顺序提前RAG或延后网页。

## 3 Provider 适配路线

### 3.0 密码库源码仓库的位置

OpenSSL与GmSSL必须放在同一个父目录下，与本文档仓库、Agent实现仓库彼此同级：

```text
/home/zsw/work/agent_development/
├── Agent-development-doc/
├── Agent-development-code/
├── openssl/
└── GmSSL/
```

目录名按上面的大小写固定，不使用`Agent-development-code/openssl`、`Agent-development-doc/GmSSL`或`_deps/GmSSL`。两个密码库独立管理版本，源码位置与编译安装前缀分开记录；这不要求替换系统已有OpenSSL。如果后续另行克隆GmSSL-Python源码，使用同级的`GmSSL-Python/`。V0核对位置并登记是否已准备；按实际Provider需要在V1/V4准备和锁定源码版本，不因安装第二库所有能力而延迟只读闭环。

### 3.1 OpenSSL

采用两种入口但统一业务结果：

- CLI：公开证书解析、检查、辅助独立对照。固定可执行文件与参数数组，确认错误码、stderr、超时和版本。
- 库 API：Python 可通过 `cryptography` 使用 OpenSSL-backed 密码能力与 X.509 解析。锁定包版本与其实际后端版本，不把系统 CLI 版本当作 Python 后端版本。

文件认证加密起点采用 AES-GCM。它同时保护密文机密性与完整性，同一密钥下不得复用 nonce；错误 key/nonce/AAD/tag 均应导致认证失败。选定接口和限制以 [cryptography AEAD 文档](https://cryptography.io/en/stable/hazmat/primitives/aead/) 为准。不要把裸 CBC 或 `openssl enc` 方案当成同等认证加密接口。

证书操作参见 [OpenSSL x509](https://docs.openssl.org/3.0/man1/openssl-x509/)、[verify](https://docs.openssl.org/3.0/man1/openssl-verify/) 与 [X.509 教程](https://cryptography.io/en/stable/x509/tutorial/)。只解析成功不能推出证书可信。

**技术点掌握程度标准**

以下表格细化主指南中的密码领域任务。Phase 0 只要求识别路线、版本和待验证能力；M1 才完成只读工具与受控练习，M4 再开放审批后的写操作。表格是后续学习目标，不表示能力已经实现。

| 技术点与阶段 | 本阶段必须能独立做到 | 练习与验收证据 | 可后置内容 |
|---|---|---|---|
| OpenSSL CLI（Phase 0→M1） | 查 version/help 与程序路径；用固定参数完成摘要和证书检查；解释 exit code/stderr，控制超时 | 公开样本结果与 adapter 对照，正常/坏输入/超时分开记录 | 通读源码、engine/provider 插件开发 |
| cryptography 与后端（M1） | 调用选定的摘要、AEAD、X.509 接口；记录 Python 包与实际后端，统一业务字段 | Python 后端记录与已知向量/CLI 对照，不根据系统 CLI 版本推断后端 | 直接封装全部 OpenSSL C API |
| Provider 契约（M1） | 将不同入口转成同一 ToolResult；保留实际算法/profile/provider，不把能力缺失当成功 | 同一证书两入口字段一致；不支持能力返回明确错误 | 通用跨语言密码插件框架 |
| 范围与独立对照（M1→M4） | 先封装选定的少量功能；区分工具正确、应用授权正确与证书信任成立 | 每项功能有独立结果及失败记录；写操作另有 M4 审批与执行证据 | 完整 PKI、TLS 协议与生产密码服务认证 |

### 3.2 GmSSL

采用 [GmSSL 官方 C 库](https://github.com/guanzhi/GmSSL) 与 [官方 GmSSL-Python 绑定](https://github.com/GmSSL/GmSSL-Python)，也可将少量操作封装为官方 CLI。绑定分发名是 `gmssl-python`，导入名为 `gmssl`，需要可加载的 `libgmssl` 动态库；同名的其他 Python 实现不是这个绑定。

先做 SM3，再做 SM2 签名验签；SM4-GCM 在**锁定的 C 库和绑定实际支持且验证通过**后接入。不能因为 README 描述了接口就认定你安装的版本一定有它，也不能在不支持时静默改成 SM4-CBC。官方绑定文档说明 SM2 证书生成/签发需要库或 CLI 的其他接口，不能假设 `Sm2Certificate` 能完成全部 CA 功能。[GmSSL-Python 接口与安装说明](https://github.com/GmSSL/GmSSL-Python)

源码依赖记录 release/tag 或 commit、来源、构建参数与测试结果。C 库先在独立前缀或受控镜像验证，Python 包加入项目的专用依赖组并进入 lock；不要以一条未锁定的临时 pip 命令作为最终安装流程。编译与provider smoke按阶段任务执行并留存结果。

**技术点掌握程度标准**

| 技术点与阶段 | 本阶段必须能独立做到 | 练习与验收证据 | 可后置内容 |
|---|---|---|---|
| 源码、CMake 与安装前缀（Phase 0→M1） | 理解源码/构建/安装目录区别，固定 commit/tag；按官方流程在受控前缀构建与测试 | 同级 GmSSL 仓库位置、构建参数、测试结果和安装路径记录 | C 语言全套课程、编译器与链接器内部原理 |
| 动态库与 Python 绑定（M1） | 区分分发名/导入名/共享库；能定位实际模块与库版本，排查找不到库或同名包混装 | 导入与版本记录、一次加载问题的定位；依赖进入 crypto 组与 lock | 自己写 ctypes/cffi 绑定 |
| SM3 摘要（M1） | 对实际字节计算摘要，核对已知向量，统一编码与文件版本 | 与独立期望一致；改输入后摘要变化，坏资源在执行前拒绝 | 实现压缩函数与密码分析 |
| SM2 签名验签（M1 练习→M4 写操作） | 固定用户 ID、摘要/编码和 scheme；正确/错误公钥、签名、输入与 profile 有明确结果 | 固定 profile 的正反结果与独立对照；Agent 签名经审批执行 | 曲线数学推导、国密 TLS |
| SM4-GCM 能力探测（M1 或后续扩展） | 先验证锁定库/绑定支持；支持时再按认证加密表接入，缺失时明确禁用且不静默降级 | 能力清单与 smoke；未支持记“未接入”，不阻塞已选 AES-GCM 闭环 | 为学习版补全绑定 API、复杂流式加密 |
| SM2 证书能力范围（M4 或扩展） | 分清解析/验证/CSR/签发的具体接口，不把一个证书类当全部 CA 能力 | 选定路线记录；未实现能力在工具列表中不宣称支持 | 完整国密 CA 与证书互操作体系 |

### 3.3 能力探测与安装后的最小验证

| 检查 | 要保存什么 | 不能据此声称什么 |
|---|---|---|
| OpenSSL CLI version/help | 二进制位置、版本、可用命令 | 不证明 Python 后端同版本 |
| Python backend version | Python 包与 OpenSSL backend 版本 | 不证明所有算法均可用 |
| GmSSL C 库 version/self-tests | commit/release、构建与测试记录 | 不证明绑定加载的是同一库 |
| GmSSL-Python 导入 | 模块路径、绑定与库版本 | 不证明 GCM/证书签发都支持 |
| 摘要已知向量 | 输入、期望摘要、实际输出 | 不证明所有密码功能正确 |
| 认证加密/验签 | 往返、认证失败、验签结果 | 不证明应用权限与 keystore 安全 |

provider 的 `capabilities` 来自适配层验证和本地配置，不让模型生成。发现不支持的算法时返回具体错误，再让用户选择受支持方案。

## 4 建议的最小工具集合

这些canonical工具ID已进入当前评测schema，并不代表应用全部实现。新增/修改工具仍需同步registry、schema、validator、MCP bridge与用例；模型只看当前已注册且已授权的能力。

| 工具 | 主要输入 | 返回给 Agent 的内容 | 何时引入 |
|---|---|---|---|
| `inspect_certificate` | certificate_id | subject/issuer/serial/SAN/有效期/用途/指纹 | M1 首个业务 |
| `verify_certificate` | certificate_id/trust_store_id/hostname/purpose | 各检查的 status、错误与检查时钟 | M1 后段或 M2 |
| `digest_file` | file_id/provider/algorithm | 摘要、编码、文件大小与版本 | M1 |
| `verify_signature` | file_id/signature_id/public_key_id/scheme | valid/invalid 与方案参数 | M1 后段 |
| `get_key_metadata` | key_id | provider、用途、版本、状态、归属 | M2 |
| `encrypt_file` | file_id/key_id/profile | 密文 artifact_id、版本、算法与状态 | 受控练习 M1；正式审批 M4 |
| `decrypt_file` | encrypted_artifact_id | 输出 artifact_id 与状态 | 正式开放前完成授权/审批 |
| `sign_file` | file_id/key_id/scheme | signature artifact_id 与实际方案 | M4 审批 |
| `rotate_key` | key_id/expected_version | 新旧版本与生命周期状态 | M4 |
| `create_csr` | 测试私钥引用/subject/SAN | CSR artifact_id 与解析字段 | M4 |
| `issue_test_certificate` | csr_id/profile | certificate_id/serial/有效期/用途 | M4 测试 CA 选定路线 |

`generate_key` 可以作为专门的受控动作或管理 API，首版不必为了工具数量给模型直接开放它。`search_knowledge` 和 `query_database` 是通用学习工具，用于说明和元数据查询。

开始时模型只看到 `inspect_certificate` 和 `digest_file` 等 1–2 个只读工具；扩展至 5–8 个常用工具后再比较 router。不要一次把全部工具暴露给 4B。

不提供通用 `run_shell`、任意 openssl/gmssl 参数透传或任意路径工具。provider 是明确枚举，algorithm/profile 是允许列表，文件与密钥由服务端 ID 解析；adapter 返回结果前过滤 stdout/stderr 中可能的秘密。

## 5 权限 审批与秘密

### 5.1 适用于本项目的初始策略

| 操作 | 策略起点 | 必须独立验证的限制 |
|---|---|---|
| 公开证书解析、授权元数据、摘要、验签 | 只读，授权后直接执行 | 文件大小、归属、provider/算法范围 |
| 小文件加密 | 写动作，首版审批具体动作 | 输出位置、key 用途/版本、nonce 与预算 |
| 解密与下载解密结果 | 敏感操作，首版审批并单独鉴权 | 文件与 key 双重授权，不把明文回模型 |
| 签名、CSR、生成/轮换密钥、测试签发 | 审批固定 payload | 用途、身份、资源版本、域名与有效期 |
| 原始密钥/私钥导出、销毁、系统信任修改 | 首版默认禁止 | 不能用一条自然语言请求解除禁止 |

这是教学系统初始策略，不是所有系统唯一的风险分类。本地策略映射到原 RiskLevel，并在实现时写明；read_only、risk 和 permission 不能仅凭工具远端注解推断。

### 5.2 两类路径要分开

```text
普通结果路径
用户 → Agent API → 模型 → execute_tool → adapter → 脱敏元数据 → 模型/页面

秘密与文件内容路径
获授权 file/key ID → 受控密码服务 → keystore/文件 → 受控 artifact
                                             → 鉴权下载接口 → 用户
```

Agent 不把上传文件全文自动送入模型。密码服务需要处理明文，但 ToolResult 只返回状态和 artifact_id；公钥/证书是否可展示按资源归属决定。审计保留算法、资源 ID、版本、动作、审批与错误，排除密钥值、口令和文件内容。

CLI 公开证书路径可由受控参数数组传入。敏感操作若只能把口令/原始密钥放进进程命令行，首版不接该 CLI 入口；改为库 API 或验证过的受控输入机制。对密码库输出的异常同样脱敏。

### 5.3 本地 keystore 的最小目标

首版采用受限目录中的加密 key blobs，DB 存 key_id/version/provider/用途/status/owner 等元数据。密钥保护主秘密与数据库分离，通过服务的受限配置/挂载获取，不进入模型上下文、样例配置、代码或日志。加密保护并不使应用进程无法访问解密后的 key，因此还要限制哪个进程可以加载它。

先区分：逻辑密钥、密钥版本、加密密钥材料、保护材料的秘密。轮换创建新版本，新加密用新版本；旧版本是否允许旧密文解密由本地策略决定。停用、撤销、销毁不要混用：停止新用途不一定意味着历史数据可以解密，也不等于已经物理销毁。

学习密钥生命周期可查 [NIST SP 800-57 Part 1 Rev. 5](https://csrc.nist.gov/pubs/sp/800/57/pt1/r5/final)。本文的简化状态和存储方案是项目教学设计，不声称实现了标准全部要求。

备份需要同时考虑加密 blobs、DB 元数据和主秘密的恢复来源。只备份 DB 无法恢复密钥能力；把主秘密与密文无保护地放在同一备份里也不能声称有隔离。

**技术点掌握程度标准**

| 技术点与阶段 | 本阶段必须能独立做到 | 练习与验收证据 | 可后置内容 |
|---|---|---|---|
| ID、版本与元数据（M2） | 解释 key_id/version_id 与实际材料的关系；查表只得到用途、归属、状态与版本 | 同一逻辑密钥两版本的元数据示例，DB/消息无材料明文 | 企业多级密钥层次 |
| 加密 blobs 与主秘密（M1 受控练习→M4） | 区分业务密钥和保护它的主秘密；限制加载进程、目录和配置访问，说明解密后的材料谁可读 | 数据流图、目录权限与受控秘密检查；密钥值不进模型/日志 | HSM/KMS、硬件隔离与远程证明 |
| 生命周期与轮换（M4） | 用明确状态控制新操作与历史解密；新密文绑定新版本，旧密文仍绑定原版本 | 轮换前后版本/密文核对；停用状态的允许/拒绝符合已写策略 | 自动销毁、复杂撤销与生产轮换体系 |
| 资源授权与审批（M4） | 校验请求者、文件、key 版本和用途；审批绑定具体动作，不能用偏好记忆获得权限 | 两用户与重复审批的真实执行/拒绝记录 | 企业双人控制与多级审批 |
| 备份恢复（M6） | 分别恢复元数据、blobs 与受限主秘密来源；缺一项明确说明失去哪些能力 | 隔离教学环境恢复并实际核对；只有 DB 的备份不判“密钥已恢复” | 生产灾备与标准全部合规要求 |

## 6 加解密与证书结果契约

### 6.1 小文件认证加密

首版将文件上限设为 **1 MiB**，这是控制内存和工时的教学选择，不是密码算法限制。后续支持更大文件时单独设计流式认证、临时文件与资源预算。

密文 artifact 的版本化封装至少描述：format_version、provider/algorithm/profile、key_id/key_version、nonce/IV、AAD、tag 的存放方式以及 ciphertext。固定编码与字段长度，拒绝未知格式和策略外算法。文件归属/格式/版本等需要绑定的 metadata 使用确定性序列化，并作为认证数据核对。

nonce 由密码服务生成，不能由模型自由指定；同一 key version 下禁止复用。需要用存储约束或适当分配方案管理唯一性，并明确并发与恢复行为。认证失败不发布任何部分明文；先完成认证再创建可下载的输出。幂等重传可以返回原动作的 artifact，不重新对不同明文使用旧 nonce。

对照方法：小文件往返逐字节相同；密文/tag/认证数据被修改、key 不符时均失败；失败没有产生可下载明文；原文件始终保留。往返只证明两条路径相容，至少再加入独立已知向量或固定格式对照，避免实现与测试共同犯错。

**技术点掌握程度标准**

| 技术点与阶段 | 本阶段必须能独立做到 | 练习与验收证据 | 可后置内容 |
|---|---|---|---|
| 摘要、加密与认证（M1） | 用自己的话区分摘要/加密/认证/签名；说明 AEAD 保护什么及不保护什么 | 为四者各写输入输出例子，不把摘要或编码当可逆加密 | 算法证明与密码学研究 |
| 格式、字节与 profile（M1） | 读写版本化密文，明确字段编码/长度、key 版本与 AAD；拒绝未知格式和算法 | 固定格式对照、坏格式拒绝，解释 metadata 如何绑定 | 大文件流式认证与跨产品格式互通 |
| Nonce 分配（M1 练习→M4） | 服务端管理同 key version 的唯一性，不接受模型自定 nonce；解释重传与重新加密差别 | 已用 nonce 的拒绝或分配约束证据；M4 再核对并发/恢复情况 | 多节点高吞吐 nonce 分配 |
| 认证失败与结果发布（M1） | 错误 key、密文、tag 或 AAD 导致失败；认证完成前不发布明文，原文件不覆盖 | 逐字节往返及独立对照；失败没有可下载输出 | 内存取证与侧信道防护研究 |
| Agent 加解密入口（M4） | 使用 file_id/key_id 与审批，明文不回模型；输出 artifact 单独鉴权 | 动作、文件快照、artifact 归属与下载允许/拒绝证据 | 任意文件批处理与生产加密平台 |

### 6.2 签名与验签

首版只选一个 OpenSSL 系方案和一个 GmSSL SM2 方案；确切算法、编码、摘要与 SM2 用户 ID 通过 profile 固定。签名不等于加密，验签通过不代表签名者身份已被信任。

验签工具返回 signature_valid，与 identity_trusted 分开。后者需要验证实际公钥来源、证书链和检查范围，不能直接由签名数学验证推出。原文件变化、签名变化、公钥错误及 profile 不匹配都要有明确结果。

**技术点掌握程度标准**

| 技术点与阶段 | 本阶段必须能独立做到 | 练习与验收证据 | 可后置内容 |
|---|---|---|---|
| 签名 profile（M1） | 固定一种 OpenSSL 系和一种 SM2 路线；说明摘要、编码及 SM2 用户 ID 的作用 | profile 配置与独立验签结果，修改 profile 后行为明确 | 全部签名算法与编码体系 |
| 正反验签（M1） | 对合法签名、改文件、改签名、错公钥分别给出 valid/invalid/操作错误 | 独立对照与反例，坏编码不伪装成工具成功 | 数学证明与签名安全研究 |
| 身份信任（M1→M2） | 分开 signature_valid 和 identity_trusted；指出公钥来源及已做/未做信任检查 | 数学验签通过但身份未核验的输出与最终解释 | 完整证书身份体系与长期验证 |
| 签名副作用（M4） | 私钥只在受控服务加载，审批绑定文件/key 版本/profile，重复动作不重复签 | 审批和动作账本、signature artifact 与权限证据 | 生产文档签署、时间戳服务 |

### 6.3 证书解析与验证

每项检查输出 `passed/failed/not_checked/unknown`，明确 clock、trust_store、purpose 和 hostname。至少区分：

**技术点掌握程度标准**

| 技术点与阶段 | 本阶段必须能独立做到 | 练习与验收证据 | 可后置内容 |
|---|---|---|---|
| PEM/DER 与 X.509 字段（M1） | 识别格式，解析 subject/issuer/serial/SAN/有效期/用途/指纹，不将展示字段当信任结论 | 测试证书与 CLI 字段对照；坏格式明确失败 | ASN.1 全部语法与手写解析器 |
| 时间、域名与用途（M1→M2） | 按指定时钟/hostname/purpose 检查，说明时区、日期边界与未检查范围 | 固定时钟的有效/过期/未生效结果；域名或用途不符分别报告 | TLS 握手完整实现 |
| 证书链与 trust store（M1 后段→M2） | 使用指定根与中间链验证，理解自签名样本不等于默认可信；不修改系统信任 | 指定教学 trust store 的成功/缺链/不受信任结果，记录验证条件 | 公共信任根治理、链构建全部边界 |
| CSR 与测试 CA（M4） | 区分请求与证书；校验允许的 SAN/用途/有效期，限制测试 CA 权限并追踪 serial | 实际签发字段和审批 payload 对照；越范围被程序拒绝 | 公共 CA、ACME、自动续签 |
| 吊销与检查状态（M1 理解；实现选修） | 说明 CRL/OCSP 目的；未实现吊销检查就返回 not_checked/unknown，不回答“未吊销” | 结果/页面/Agent 解释均保留未检查范围；已实现时另留核对证据 | CRL/OCSP 服务与完整吊销运维 |

下表用于约束结果解释；上表用于判断你是否具备独立操作与排错能力，两者都要满足。

| 检查 | 能说明什么 | 不能顺带宣称什么 |
|---|---|---|
| 解析 | 格式与字段可读 | 签名有效、链可信 |
| 时间 | 在指定时钟是否有效 | 尚未吊销 |
| 域名/SAN | 对指定 hostname 是否匹配 | 其他域名也有效 |
| 证书链与信任根 | 相对于指定 trust store 的链验证结果 | 全世界或系统默认一定信任 |
| KeyUsage/EKU | 符合指定使用目的 | 任意用途均可 |
| 吊销 | 已实际核对的 CRL/OCSP 范围 | 未检查时不能说没有吊销 |

首版可离线验证明确的测试信任库，吊销项先 `not_checked`，不要为了学习 Agent 一开始搭完整吊销服务。自建测试 CA 只在指定测试 trust store 中使用，不自动导入宿主系统或浏览器信任。

## 7 页面与业务元数据

页面建议包含聊天与 Run 详情、文件列表、key 元数据/版本、证书列表/检查详情、审批、审计与 artifact 下载。先让最小页面调用 API，再加聊天；用户也应能通过固定按钮进行同样的只读检查，用来对照 Agent 编排是否正确。

业务元数据逐步加迁移：files/artifacts、keys/key_versions、certificates/certificate_checks、CSRs、approval/actions。具体命名由实现时与既有 DDL 对齐。添加 owner/project、资源版本和用途；不在 JSON 字段里塞私钥或明文文件来省一个存储组件。

首页先显示“支持哪些能力”和“当前 provider 是否就绪”，不让模型编造 capabilities。历史 Run 显示当时 provider/模型/策略版本；当前资源状态由实时查询呈现，不用旧聊天结论替代。

## 8 领域验收任务

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

## 9 每个阶段增加哪些领域能力

实际阶段按第2.2节与学习总览的V顺序；领域六张技术表中的M标签对应稳定任务族，其完整标准保留。V1先摘要Demo再加证书；受控AEAD练习M1 06到V4；正式轮换/CSR/签发全范围在V6，不阻塞首种加密。

开始只需公开证书和小型非敏感文件。先稳定函数，再手写调用，再V2网页，再V3MCP，再V4受控写动作。每项输出都有独立对照、版本与真实状态；RAG支持操作依据，不代替当前工具结果。

## 10 后续可以照着操作的 provider 入门练习

以下命令是**学习步骤**，在完成前置任务后依次执行并记录实际输出。每小节成功后再进入下一节；所有命令在 Ubuntu Bash 中运行。现有文件/源码目录已经存在时先检查内容，不重复生成或覆盖。

### 10.1 准备非敏感文件并核对摘要

工作目录是实现仓库。创建目录与测试文件：

```bash
cd /home/zsw/work/agent_development/Agent-development-code
mkdir -p data/learning/crypto
printf 'abc' > data/learning/crypto/abc.txt
openssl dgst -sha256 data/learning/crypto/abc.txt
openssl dgst -sm3 data/learning/crypto/abc.txt
```

期望 SHA-256 为 `ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad`。期望 SM3 为 `66c7f0f462eeedd9d1f2d46bdc10e4e24167c4875cf2f7a2297da02b8f4ba8e0`。注意 `abc` 后面没有换行；输入多一个字节结果就不同。SM3 向量也可与官方 GmSSL-Python 的示例核对。[GmSSL SM3 示例](https://github.com/GmSSL/GmSSL-Python#sm3哈希)

这一步学的是 bytes、编码、工具结果和独立对照。后续的 Agent 接口接受 file_id，不能直接开放这条命令的任意参数。

### 10.2 没有公开测试证书时生成教学样本

也可以使用你已有的公开证书。需要自建样本时，以下生成一张只用于练习解析的自签证书和**加密保存**的测试私钥；交互时输入本地测试口令，不把口令写在命令行或聊天中。

```bash
cd /home/zsw/work/agent_development/Agent-development-code
umask 077
mkdir -p data/learning/crypto/cert-demo
openssl req -x509 -newkey rsa:2048 -sha256 -days 30 \
  -keyout data/learning/crypto/cert-demo/test-key.pem \
  -out data/learning/crypto/cert-demo/test-cert.pem \
  -subj '/CN=agent-learning.test' \
  -addext 'subjectAltName=DNS:agent-learning.test' \
  -addext 'basicConstraints=critical,CA:FALSE' \
  -addext 'keyUsage=critical,digitalSignature,keyEncipherment' \
  -addext 'extendedKeyUsage=serverAuth'
openssl x509 -in data/learning/crypto/cert-demo/test-cert.pem \
  -noout -subject -issuer -serial -dates -fingerprint -sha256
openssl x509 -in data/learning/crypto/cert-demo/test-cert.pem -noout -text
```

核对 CN、SAN、有效期、用途和 CA:FALSE。你的第一个适配函数只读 `test-cert.pem`；不要读 `test-key.pem` 或把私钥内容交给模型。这个自签样本不是受信任 CA 签发的业务证书，不导入系统信任。命令参数按本机 `openssl req -help` 核对，参见 [OpenSSL req](https://docs.openssl.org/3.0/man1/openssl-req/)。

### 10.3 GmSSL C 库的一次受控构建

先做完上面的 OpenSSL 只读闭环。需要引入 GmSSL 时，检查已有安装；若未安装，以下演示官方源码的本地构建路线。源码直接放在`/home/zsw/work/agent_development/GmSSL`，与`openssl`及文档/实现仓库同级；安装到用户目录的独立前缀，不覆盖系统OpenSSL。已有GmSSL源码时跳过clone，先检查其远端、版本与工作区。

```bash
sudo apt update
sudo apt install -y build-essential cmake git
mkdir -p /home/zsw/work/agent_development
git clone https://github.com/guanzhi/GmSSL.git \
  /home/zsw/work/agent_development/GmSSL
cd /home/zsw/work/agent_development/GmSSL
git status --short
git log -1 --oneline
git tag --list
```

先检查官方 release/tag 和兼容说明，选择要验证的版本；新手可把刚 clone 的 commit 作为候选快照，但它不自动等于稳定版。若 checkout 了选定 tag，以下从当前 commit 记录并构建：

```bash
cd /home/zsw/work/agent_development/GmSSL
gmssl_commit=$(git rev-parse HEAD)
gmssl_prefix="$HOME/.local/opt/gmssl-$gmssl_commit"
printf '%s\n' "$gmssl_commit"
cmake -S . -B build-learning \
  -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_INSTALL_PREFIX="$gmssl_prefix" \
  -DBUILD_SHARED_LIBS=ON
cmake --build build-learning --parallel 2
ctest --test-dir build-learning --output-on-failure
```

测试失败时先定位，不进入安装与 Agent 接入。所选源码必须有相应 CMake 选项；构建接口参考 [官方 CMake 配置](https://github.com/guanzhi/GmSSL/blob/master/CMakeLists.txt)。2 个并行编译进程是降低学习机器负载的起点，不是性能要求。

测试通过后：

```bash
cmake --install build-learning
export PATH="$gmssl_prefix/bin:$PATH"
export LD_LIBRARY_PATH="$gmssl_prefix/lib${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
gmssl version
gmssl help
printf 'abc' | gmssl sm3
```

确认输出的版本和 SM3 摘要。PATH/LD_LIBRARY_PATH 只在当前终端生效；后续将通过验证的前缀写入服务专用环境配置/容器，不依赖终端的偶然状态。记录 commit、prefix、构建参数和测试结果，新版本换新前缀。

### 10.4 Python 绑定与能力检查

回到应用仓库，在 M1 引入专用 `crypto` extra，并保留当前 m1/dev：

```bash
cd /home/zsw/work/agent_development/Agent-development-code
uv add --optional crypto cryptography gmssl-python
uv sync --extra m1 --extra crypto --extra dev
source .venv/bin/activate
```

后续直接在此虚拟环境检查安装来源与版本：

```bash
python -c 'import importlib.metadata as m; print(m.version("cryptography")); print(m.version("gmssl-python"))'
python -c 'from cryptography.hazmat.backends.openssl.backend import backend; print(backend.openssl_version_text())'
python -c 'import gmssl; print(gmssl.__file__); print(gmssl.GMSSL_PYTHON_VERSION); print(gmssl.GMSSL_LIBRARY_VERSION); print("Sm4Gcm:", hasattr(gmssl, "Sm4Gcm"))'
```

如果官方分发包没有所需接口，按官方仓库选定 commit 的源码安装方式更新依赖来源与 lock，再运行上游测试和实际能力检查。不要直接混装另一个导入名相同的 `gmssl` 包。

再对相同输入核对 Python SM3：

```python
from gmssl import Sm3

digest = Sm3()
digest.update(b"abc")
print(digest.digest().hex())
```

这段是 provider smoke 示例，不是 Agent、执行器或正式测试实现。输出需与 CLI 和已知向量一致；能力存在性不能替代 SM4-GCM 的往返与认证失败验证。失败时回到共享库来源、加载路径和版本检查。

### 10.5 后续同步依赖时保留 crypto 组

`crypto` 组创建后，M2 使用 `uv sync --extra m1 --extra m2 --extra crypto --extra dev`；M3 加 `--extra m3`，M4 再加 `--extra m4`。只有真正做 reranker 才增加 `ml`。锁文件形成后复现加 `--frozen`，不同阶段选择的 extras 写进运行说明。

完成这些练习后，才开始自己实现统一 provider adapter。第一轮只封装证书解析和摘要；输入/输出/异常稳定后再接 execute_tool 和模型。


## 11. 密码工具服务于Agent学习

本文件六张密码技术表规定业务正确性；主课程的17张技术表见[学习总览](../LEARNING-PATH.md)。密码封装先固定少量profile和≤1MiB教学文件，重点练Agent输入校验、选工具、资源授权、版本、固定审批、结果验证与恢复；不将路线扩展为算法实现课程。

| 学习业务 | 必须体现的Agent能力 | 深入密码部分的时机 |
|---|---|---|
| 摘要/公开证书解析 | schema、直接对照、工具反馈、Trace | 业务结果已可验证后再读算法原理 |
| 加解密/签名 | 固定profile、审批、秘密边界、artifact/版本、Verifier | 本路线掌握库正确使用；大文件协议后置 |
| 密钥轮换 | 状态账本、幂等、旧版本策略、失败核对 | HSM/KMS、生产轮换合规另立专题 |
| 证书验证/测试签发 | 检查分项、信任来源、审批、当前版本 | 完整CA/吊销服务/生产信任后置 |

端点和页面查[08](08-API-AND-WEB.md)，恢复/材料备份查[09](09-DELIVERY-AND-ACCEPTANCE.md)。官方GmSSL能力以锁定版本实际验证为准，发现库缺能力应明确disabled/unavailable，不能改用另一算法还沿用原profile名称。
