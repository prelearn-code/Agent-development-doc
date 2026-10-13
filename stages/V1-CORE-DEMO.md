# V1 核心工具调用

本阶段基础预算**65h**；实现成果：两个只读工具、手写Loop、原始工具调用Trace。先读实现目标与当前切片，再执行详细任务；完成标准以实际证据为准。

## 实现目标与学习结果要求

先用一个digest_file跑通终端Agent Demo：模型提议、程序校验、OpenSSL执行、真实结果反馈、本人有限Loop与回答。Demo通过后在同一代码上加证书工具，再补完整预算、失败、多调用、Context与NDJSON。AEAD练习留V4。

| 需要学习的技术 | 学习结果要求 | 独立实现与排错证据 |
|---|---|---|
| Python模块、类型、bytes/编码 | 把Provider/handler/executor/Loop分开；摘要针对实际字节而不是展示文本 | 直接摘要与独立向量对照；修改字节、非ASCII和坏输入有结果 |
| Pydantic与JSON Schema、ToolResult | 定义受限输入和可序列化结果，分开校验、授权与执行 | 正常/缺字段/错误类型/空结果/失败；错误码和证据不依赖模型措辞 |
| 固定OpenSSL适配与异步生命周期 | 固定程序/参数数组，控制超时、输出上限和子进程清理 | 真实Provider对照，超时后进程结束；不接受模型拼接shell |
| Registry、资源ID和唯一execute_tool | 只暴露已登记能力，服务端映射教学资源并检查允许范围 | 未知工具/越界资源执行前拒绝，证明Provider没有被调用 |
| httpx、Messages与原生Tool Calling | 发送非流式请求，保留assistant提议并回传真实tool结果 | 逐条标注原生报文；网络/HTTP/解析/工具失败能定位 |
| 本人Agent Loop、停止与预算 | 自己控制继续/停止、最大步数/总deadline/重复提议，CLI只调用runner一次 | 无工具、单/多调用、失败/超限Trace；独立改约束后回归 |
| Context、Trace与最后的NDJSON | 管理消息来源和上下文预算，分开网络块、JSON行与完整调用 | 截断/脱敏/计量说明；切块、UTF8残片与中断测试 |
| 证书字段与GmSSL能力扩展 | 摘要Demo后解析公开证书；分开解析与信任，按能力补SM3 | 字段/向量独立对照；未支持明确unsupported，不静默替换 |

## 必须独立回答的关键问题

这些问题必须由你结合自己的实现作答，AI只审查。记录在代码仓库docs/progress.md，写清场景、自己的理由、真实证据与未覆盖边界；只背定义或复制AI答案不算通过。

第一个单工具Demo先回答Q01–Q10；扩展到两个工具与完整V1后回答全部问题。不要为回答后续问题而推迟第一个Demo。

| 编号 | 必须自己回答的问题 | 回答达到标准所需的说明或证据 |
|---|---|---|
| Q01 | 第一个Demo的完整输入输出是什么？哪一步才真正发生密码运算？ | 画从问题到最终回答的链路，标出真实OpenSSL执行点 |
| Q02 | 为什么选摘要作为第一工具？怎样验证结果来自真实计算？ | 独立向量/CLI对照和实际ToolResult，而非模型自述 |
| Q03 | 文件多一个换行后摘要为何变化？bytes、hex和Base64有什么不同？ | 给出自己的字节长度与摘要对照，不把编码当加密 |
| Q04 | 模型生成的工具名字和参数，为什么不能直接当可信程序输入？ | 分别说明schema、工具登记与资源授权的校验点 |
| Q05 | 教学资源ID怎样映射为路径？用户或模型能否指定任意文件？ | 给出固定资源范围与拒绝记录，证明Provider未执行 |
| Q06 | Provider、handler、executor和Loop分别负责什么？ | 用同一次摘要调用标出职责和错误传播位置 |
| Q07 | assistant工具提议与tool结果如何一起放回下一轮消息？ | 标注自己锁定版本的真实报文与回传顺序 |
| Q08 | 模型没有提出工具调用时，Loop应怎样结束或澄清？ | 解释自己的停止条件与一次实际无工具结果 |
| Q09 | 最大轮数与工具超时分别保护什么？工具失败后怎样反馈？ | 提供有界退出和结构化错误，不能无限重试 |
| Q10 | CLI调用runner一次，为什么还可能发生多轮模型请求？ | 解释启动入口与自己Loop的边界，不把适配器当Agent实现 |
| Q11 | 给工具传入错误类型、缺字段或额外字段会怎样？ | 自己的schema与执行前拒绝测试 |
| Q12 | success=True但结果为空，是否必然是错误？ | 区分合法空结果、未执行和执行失败，并提供序列化例子 |
| Q13 | await超时后子进程一定结束了吗？取消如何清理？ | 检查terminate/kill/wait和临时资源，提供真实退出证据 |
| Q14 | 如何确认超大输出没有撑爆上下文或日志？ | 说明输出上限、截断/结果引用与失败策略 |
| Q15 | 重复工具提议如何识别？只读重试与未来写重试如何区分？ | 解释自己的重复/预算策略和执行计数，不依赖模型自律 |
| Q16 | step、deadline、token和输出限制是否能互相替代？ | 分别说明触发条件、计量来源和停止原因 |
| Q17 | 加入第二个证书工具后，怎样区分选错工具与参数错误？ | 提供两个工具的schema、提议与实际执行对照 |
| Q18 | 解析证书成功、时间有效和链可信分别意味着什么？ | 指出实际已检查和未检查条件，不能从字段展示推出信任 |
| Q19 | 网络chunk、NDJSON记录与完整tool call为什么是不同层？ | 解释半行、UTF8跨块与中断的受控测试 |
| Q20 | 一轮Context包含哪些来源？什么不能进入system或模型输入？ | 标注来源、预算、秘密停止位置与不可信文本边界 |
| Q21 | Trace应怎样关联提议、拒绝、执行与结果？ | 用一次成功和一次失败还原调用路径，审查脱敏 |
| Q22 | 你自己改一个工具约束或Loop预算后，哪些验证必须重跑？ | 提供本人diff、正常/失败结果和受影响接口说明 |

## 分步任务与技术掌握标准

先按当前切片实现最小输入输出，再补齐技术表。本阶段首次运行、正常/失败/权限、本人解释与独立修改分别验收；未实际运行不签收。

<a id="first-demo"></a>
## 第一个Demo 先跑通一个摘要工具

本阶段先完成一个小成果，不把全部V1标准当成Demo启动前置。输入“计算教学文件sample.txt的SHA-256摘要”，让模型提议digest_file，程序校验并调用OpenSSL，把真实结果反馈给模型，再返回答案。输入只引用教学资源ID，固定映射到项目内非敏感文件；拒绝任意系统路径、未知工具和额外命令参数。

```text
用户问题 → 模型tool_calls → execute_tool校验 → 固定OpenSSL适配器
                                                ↓
最终回答 ← 模型读取实际结果 ← 结构化ToolResult/错误
```

| 小步 | 对应任务 | 实现位置 | 学习内容与达到的程度 | 通过后得到什么 |
|---|---|---|---|---|
| 1 直接计算摘要 | M1 01、03 | packages/crypto/providers/openssl_cli.py；tools/builtin/digest_file.py | 理解bytes、摘要和固定参数数组；不接模型独立运行，对照OpenSSL命令结果 | 确定性工具可运行 |
| 2 注册并校验唯一工具 | M1 04–05、07当前范围 | tools/registry.py、tools/executor.py；packages/security；tools/tests | 解释schema与权限不同；未知工具/坏参数/非教学资源执行前拒绝；有超时和输出上限 | 一个允许工具的受控执行入口 |
| 3 得到一次工具提议 | M1 08–09 | packages/llm/client.py | 非流式请求只暴露digest_file；保留原生tool_calls，解释名字和arguments来源 | 模型能提出调用，尚不能据此声称执行成功 |
| 4 回传一次真实结果 | M1 10 | 消息构建与工具反馈接口 | 保存assistant提议和实际tool结果，说明报文顺序；工具失败也回传 | 模型根据真实摘要作答 |
| 5 本人手写有限Loop | M1 11及12–13相关小范围 | minimal_agent/runner.py | 自己决定继续/结束，设置最大轮数/总超时，输出停止原因；AI只审查 | 可重复运行的CLI Agent Demo |
| 6 验证并解释 | M1 07、12–13当前范围 | tools/tests；脱敏Trace；docs/progress.md | 正常、非法文件、工具失败、超轮数均有结果；自己改一个约束后回归 | 最小Demo可以签收，但完整V1尚未签收 |

以上步骤调整了M1 02和03的实践先后，任务编号不变：先M1 03摘要，单工具闭环后才M1 02证书。不是重排整个技术任务编号。Demo只使用非流式协议、一个工具和固定教学资源；NDJSON、第二工具、多调用和完整预算随后在本V1补齐。

本人入口只要求满足已有CLI合同：`minimal_agent.runner.run`为异步函数，接收question关键字并返回可序列化JSON对象。签名和退出码见代码仓库[CORE-FIRST](../../Agent-development-code/docs/CORE-FIRST.md)；入口适配器不替你实现Loop。

```bash
# Ubuntu实现仓库；完成自己的runner后才运行第二条
python -m packages.app status
python -m packages.app run --question '计算教学文件 sample.txt 的 SHA-256 摘要'
```

`status`只证明入口可启动；`run`退出0只证明函数返回，必须继续核对真实ToolResult、独立摘要和Trace，不能据此认定业务成功。没有runner时应明确失败，不返回空答案伪装成功。

### Demo验收清单

- [ ] Q01–Q10由本人结合单工具Demo作答；后续Q11–Q22不阻塞第一次Demo签收。

- [ ] 摘要与独立OpenSSL结果一致；同文件字节修改后结果变化。
- [ ] Trace中可定位原始模型提议、执行输入、真实结果、工具反馈和停止原因。
- [ ] 未知工具、非法资源/参数在Provider调用前拒绝。
- [ ] 工具失败有结构化错误；超时清理进程；最大轮数阻止无限继续。
- [ ] 本人能解释每一轮是谁决定参数、是谁授权、结果怎样回到模型。
- [ ] 本人独立改一个输入约束或预算，并验证正常与失败路径。

### 在同一Demo上补齐V1

添加公开教学证书inspect_certificate，再验证两个工具选择、无须调用工具的请求、多调用、失败反馈、重复提议/预算、Context和最后的NDJSON。下面目标1/2能力表和详细任务用于逐项补齐，不要求第一个摘要Demo包含所有这些行为。V1通过也不代表M1全技术组毕业：AEAD练习留V4。

**当前切片**：目标1只读20h与目标2全部45h。先按第一个Demo完成M1 01/03–05/07和08–13的必要切片，再补M1 02与完整只读范围；M1 06和M1 07写范围留V4。小用例从现在登记，不接RAG/MCP，不提前开放写操作。

**目标**：从“我能直接调用一个工具”发展到“模型选择工具，经执行器校验后调用，结果回到模型”。V1预算65h：只读Python/工具20h、协议/Loop45h。目标1剩5h AEAD练习留V4，届时先直接教学验证再开放审批写动作。

### 目标1：Python 工具工程（25h）

**进入条件**：V0通过。V1学习只读工具20h，V4再用5h做受控AEAD练习；25h含约10h最小Python/HTTP地基，不重复计费。

**Agent目标**：工具输出可预测、输入受控、失败能回传，模型不直接访问系统。 对应详细任务：**M1 01–07**。

**技术点掌握程度标准**

| 技术点 | 能解释 | 独立做到 | 排错与边界 | 验收证据 | 后置内容 |
|---|---|---|---|---|---|
| 包/类型/Pydantic | 模块职责、输入输出类型、序列化与校验区别 | 定义Tool输入与泛型ToolResult，默认工厂隔离列表 | 拒绝非法类型/额外字段，空查询结果仍成功 | 正常/非法/空结果断言 | 元编程 |
| async/生命周期 | await、阻塞I/O、超时与取消区别 | 管理HTTP client与固定子进程的创建关闭 | 超时后terminate/kill、wait与清理，不能只停止等待 | 进程退出和临时文件检查 | 高并发调度 |
| Provider适配 | CLI、Python backend、官方GmSSL绑定是不同入口 | 直接做证书解析/摘要，固定参数数组并记录能力 | 库缺失、版本差异、解析失败、输出超限可分类 | 独立摘要对照与Provider版本 | 库内部算法实现 |
| 资源/唯一入口 | 模型给ID，服务端给路径、权限与秘密 | registry注册只读工具，execute_tool解析授权资源 | 未知工具、越界路径、跨项目资源拒绝并审计 | 正常与拒绝调用记录 | 任意脚本执行不开放 |
| 测试/脱敏/密码练习 | 独立对照与同实现测试的区别 | 关联run/call，做教学材料AEAD往返与认证失败 | 私钥/口令/明文不进ToolResult或Trace | 正反用例与日志审查 | 大文件流加密 |

**学习与实现顺序**：①补最小Python地基；②先直接调用摘要Provider，摘要Demo通过后补证书解析；③封装输入输出/能力检查；④registry与资源授权；⑤失败与超时；⑥受控小文件密码原语练习。AEAD练习不通过Agent开放写动作，正式审批在M4落实。

**必须独立回答**：为什么空结果不是异常？模型为什么不能传真实路径？协程超时为什么不等于外部进程结束？

**独立练习**：新增一个允许的输入字段，自己调整schema和正常/非法用例；制造超时并确认进程与临时资源被清理。

**退出条件**：证书解析与摘要可直接运行；输入/资源/输出/超时反例齐全；教学密码练习满足密码工具合同标准。当前字段与目标字段按结构文档§4.1映射，不能声称规划字段已存在；V1先签收只读切片，V4补齐AEAD后才标记m1-tools-done。

**具体实践与逐项操作**


你要先学类型提示、函数参数、Pydantic schema、异常、JSON、日志、pytest、`async/await` 和超时。重点不是语法数量，而是把一个密码操作封装成稳定、可解释、能失败的工具。

**技术点掌握程度标准**

| 技术点 | 本阶段必须能独立做到 | 练习与验收证据 | 可后置内容 |
|---|---|---|---|
| Python 函数、类型与模块 | 用函数与小模块分开 adapter/handler/executor；写清参数和返回类型，理解类型提示不会自动校验运行时输入 | 不接模型调用一个工具；独立增加大小上限，说明改动涉及哪些模块 | 元类、复杂继承、泛型框架设计 |
| Pydantic 与 JSON Schema | 为工具定义必填字段、范围和枚举；明确缺失值、null、默认值与类型转换策略 | 合法输入通过，缺字段/错误类型/策略外值在执行前拒绝；核对导出的 schema | 自定义 schema 生成器、复杂模型继承 |
| 字节、文本与编码 | 区分 bytes、UTF-8、hex、Base64；摘要针对实际字节，编码仅用于表示 | 对同一测试文件核对长度与摘要；用非 ASCII 输入验证编码，拒绝坏编码 | 通用二进制协议与高性能编码 |
| 异常与 ToolResult | 区分业务拒绝、工具失败、超时、程序缺陷；成功空结果不当错误；返回可序列化且有错误码 | M1 01、05 的正常/失败结果，原始异常只在受控排错位置留存并脱敏 | 全局异常框架、复杂错误层级 |
| Registry 与执行入口 | 由注册表查固定工具；所有调用先校验资源与参数再执行，模型不直接调 handler | 未知工具、不存在/越权资源的拒绝记录；证明对应 adapter 未被调用 | 插件自动发现后置到 MCP；大规模工具注册 |
| async/await 与进程调用 | 解释等待和阻塞；固定程序/参数数组调用 CLI；设置超时、输出上限，取消后清理子进程 | 正常执行、超时和输出超限；检查超时后进程结束，解释为何等待超时不等于杀进程 | 高吞吐并发调优、复杂进程池 |
| 日志与 Trace | 关联 run/step/tool、耗时与错误；输出足以排错且不含秘密、文件明文 | 用一条成功和一条失败 Trace 还原调用路径，并检查秘密字段处理 | 分布式追踪平台与完整监控栈 |
| pytest fixtures 与参数化 | 自己构造小型受控资源；测试正常、边界和失败行为，区别 mock 与真实 provider 验证 | M1 07 的行为断言；mock 超时测试与 provider smoke 分别留证据 | 追求覆盖率数字、测试框架扩展 |
| 密码 Provider 适配 | 统一输出而不掩盖 provider 差异；能完成证书解析、摘要和受控加解密并核对失败行为 | M1 02、03、06 结果；细项按密码工具合同的 Provider 与结果契约表验证 | 算法内部实现、完整 PKI、HSM |

| 顺序 | 任务与学习内容 | 待实现位置或职责 | 完成后检查 |
|---|---|---|---|
| M1 01 | 读 core 的 ToolResult/ToolSpec，理解参数模型、成功与错误 | `packages/core` | 空结果是成功；错误有 code/message，输出可序列化 |
| M1 02 | 先不用模型，解析一张公开测试证书 | OpenSSL adapter、证书工具 | subject/issuer/serial/有效期/用途等字段与 CLI 对照 |
| M1 03 | 计算授权文件 SHA-256，后补 SM3 | provider adapter、摘要工具 | 已知测试向量与直接工具输出一致 |
| M1 04 | 写 registry 和唯一 `execute_tool` 入口 | registry/executor | 未知工具、非法参数、越权文件在执行前拒绝 |
| M1 05 | 统一错误和日志，学习真正的进程超时清理 | adapter/executor | 超时后子进程结束；输出有上限；日志无秘密 |
| M1 06 | 在受控练习中封装小文件加解密 | OpenSSL/GmSSL adapter | 往返一致；修改密文后认证失败；不覆盖原文件 |
| M1 07 | 为工具正常和失败行为写独立验证 | `tools/tests` | 反例触发预期拒绝，所有路径走执行器 |

M1 02 的第一轮只读本地文件，先不连接真实站点，不扫描网络。读文件用服务端解析出的获授权资源，不让模型任意传系统路径。CLI 封装使用固定程序和参数数组，不把模型字符串拼成 shell 命令。

M1 06 的详细条件见本阶段密码工具合同：nonce 由服务端生成并管理，工具只接受 key_id；写操作暂只在明确确认的学习脚本中调用，不开放无人审批的 Agent 自动写入。加解密的明文是小型 synthetic 测试文件；输出是受控文件句柄，不把明文或密钥作为 ToolResult 回传。

本项目工具只封装固定密码功能，模型不获得任意脚本或shell执行入口。

**此目标的验收指标**：适配层与执行器的确定性检查全部通过；正常输入、未知工具、错误参数、不存在资源、越权资源、超时、输出超限均有证据。每个秘密字段都能指出存储位置、访问者与日志处理。测试数量服务于这些行为，不能用“写了十个测试”替代覆盖。

**独立练习**：为工具增加文件大小上限，证明边界值可接受、超出被拒绝；不改为无限制读取。能解释adapter/handler/executor后先签收V1只读切片；V4补M1 06与写工具验证且目标1全表通过，才标记m1-tools-done。

### 目标2：LLM 协议、Context 与手写 Loop（45h）

**进入条件**：只读工具直接调用通过。

**Agent目标**：亲自理解观察→提议→执行→回传→停止，再使用框架。运行设计见本阶段Agent运行机制。 对应详细任务：**M1 08–13**。

**技术点掌握程度标准**

| 技术点 | 能解释 | 独立做到 | 排错与边界 | 验收证据 | 后置内容 |
|---|---|---|---|---|---|
| 消息/上下文 | system/user/assistant/tool与token上限 | 构建一次任务消息，解释保留/截断依据 | 秘密、文件全文与不可信指令不进入system | 消息序列与上下文预算表 | 注意力推导、训练 |
| Ollama协议 | /api/chat、tool_calls、tool_name与计量 | httpx非流式调用，保存锁定版本原始报文 | arguments对象按schema检查，未知工具拒绝 | 请求→调用→结果→响应Trace | 多供应商兼容层 |
| 手写Loop | 模型提议与执行器授权的分工 | 本人实现有限Loop，回传真实结果，单步/多步/多调用 | 失败回传，重复提议不无限循环 | 三类正常任务及失败记录 | 自动多Agent规划 |
| 预算/停止 | steps、deadline、token、output是不同限制 | 总预算、停止原因、取消行为明确 | 无工具、未知工具、超预算均有界结束 | 停止理由、耗时、计量断言 | 复杂动态预算 |
| NDJSON/流 | 原生NDJSON与前端SSE不同 | 累积原生消息和完整tool call后按策略执行 | 半行、UTF-8跨块、thinking/content分开 | 原始流与非流式同类任务对照 | WebSocket、兼容端点delta |

**学习与实现顺序**：①一次模型回答；②一次只读tool call；③一次tool结果回传；④自己写有限循环；⑤失败/重复/预算验证；⑥最后增加NDJSON。不比较随机文本完全一致，比较协议与行为条件。

**必须独立回答**：参数是谁产生的？权限由谁决定？结果如何回上下文？每种停止原因是什么？模型说已加密怎样与实际动作区分？

**独立练习**：亲自修改MAX_STEPS或允许工具池，解释终止差异；根据真实Trace修复一次工具反馈错误。

**退出条件**：能脱离框架解释和修改初版Loop；流式/非流式均通过正常、失败与预算验证；保留脱敏Trace并开始收集评测草稿，V1签收目标2；m1-done须等V4目标1剩余练习完成。

**具体实践与逐项操作**


先学 messages、system/user/assistant/tool 角色、工具 schema、模型上下文、token、工具结果回传、停止条件。这里的关键发现是：模型产生的是调用建议，调用建议还需要执行器批准；工具执行与自然语言回答是两件事。

**技术点掌握程度标准**

| 技术点 | 本阶段必须能独立做到 | 练习与验收证据 | 可后置内容 |
|---|---|---|---|
| httpx 与模型客户端 | 实现一次非流式调用；区分网络失败、HTTP 错误、响应解析失败与模型未选择工具 | M1 08 的请求/响应和分类错误，能从原始响应定位问题 | 多模型网关、复杂重试中间件 |
| Messages 与 Tool Calling | 说明四类角色作用；构造工具 schema，读取调用建议，经执行器执行后回传实际结果 | 画 M1 09–10 消息序列；参数、工具消息与后续回答可逐条核对 | 微调、模型训练、复杂提示词优化 |
| 手写 Agent Loop | 自己写有限循环；覆盖无工具、单步、多步、失败反馈；停止状态明确 | M1 11 的不同路径 Trace，能解释每轮为何继续或退出 | 多 Agent 协作、自动规划框架 |
| 上下文、token 与预算 | 解释上下文长度与输出预算；限制步骤、总 deadline 和结果体积，不把秘密加入上下文 | 确定性触发预算退出与重复动作保护，记录原因；不以改大上限掩盖死循环 | 长上下文策略与压缩实验在 M5 学 |
| NDJSON 流式解析 | 区分网络 chunk 与完整记录；增量处理 UTF-8 与残片，按锁定协议收集内容/工具调用 | M1 13 切块验证；正常结束、残帧和中断可定位，不混用 SSE 解析器 | 多供应商流协议适配 |
| 失败反馈与重试 | 明确哪些只读失败可有限重试，哪些写动作不能凭模型建议重跑；缺参数能澄清 | 工具失败、缺信息、重复建议的 Trace 与执行计数 | 通用自主纠错与复杂重规划 |

| 顺序 | 学习任务 | 输入与预期行为 | 验收证据 |
|---|---|---|---|
| M1 08 | 用 httpx 写非流式客户端 | 普通问题→原始 JSON→提取回答 | 请求、响应与异常记录 |
| M1 09 | 给模型只暴露一个只读工具 | Demo先用“计算教学文件摘要”→digest_file建议；第二工具后用“检查这个 certificate_id 的有效期”→证书工具建议 | tools schema 与实际 arguments |
| M1 10 | 手写一次调用结果回传 | tool call→execute_tool→tool message→再次请求 | 完整多轮消息与真实工具结果 |
| M1 11 | 扩成有限循环 | 无工具问题、一次调用、多次调用、工具失败 | 逐 step Trace 与最终状态 |
| M1 12 | 加预算与拒绝规则 | 未知工具、重复调用、超过步骤/deadline | 退出原因可见；不一直重试 |
| M1 13 | 最后实现原生流式解析 | NDJSON 按实际协议解析，累积内容与完整调用 | 原始 NDJSON 与切块测试 |

初版 Loop 由你手写，先画伪代码和消息流，再让 AI 审查。它必须先通过非流式任务，才能加流式。原生 Ollama 流使用 NDJSON，后续前端使用 SSE，解析器分别实现；原生工具回传用 `role:tool` 与 `tool_name`，应用自己生成调用关联 ID。arguments 的实际形状从锁定版本的 Trace 验证，不能先假设它是字符串 delta。参见 [Ollama 工具调用](https://docs.ollama.com/capabilities/tool-calling) 与 [流式协议](https://docs.ollama.com/api/streaming)。

MAX_STEPS、总 deadline 和 token/输出预算必须有配置。工具是否重试由本地策略决定；生成密钥、签发、轮换等写动作不允许因模型重复提议或连接错误自动重跑。等待超时不等于已经杀掉子进程，你需要核对适配层清理行为。

**建议练习集**：使用无工具回答、证书检查、文件摘要、先找证书再检查、资源不存在、工具超时、信息缺失需澄清这些简单任务；每个任务事先写预期计划和成功条件。任务列表是开发练习，正式 gold 由你审定后再冻结。

**此目标的验收指标**：

- 单步、多步、多调用和失败反馈都有真实 Trace；结束原因明确。
- 必要工具的参数经过 schema 与授权检查，不能直接调 handler。
- 流式与非流式能完成相同任务类型、遵守相同策略并正确关联结果；不要求随机模型逐 token 或逐次计划完全相同。
- MAX_STEPS、deadline、重复动作保护能被确定性输入触发。
- 能回答：谁选工具、谁检查权限、结果怎样回上下文、何时停止、失败后为什么重试或不重试。

**独立练习**：把证书检查增加一个必填 `purpose` 参数。信息不足时让系统澄清，完整输入能通过；你能定位 schema、模型说明、执行器与测试要改的地方。

保存脱敏原始Trace和五问说明，签收目标2及V1。下一步V2给Loop加JSON API和基础网页；m1-done须V4补齐目标1后创建。

## 本阶段的接口与实践细节

以下内容属于本阶段，按任务用到的部分查阅；涉及后续能力的字段仅作为扩展合同，当前切片不要求提前全部实现。

<a id="contract-1"></a>
<a id="contract-1-1-目录与依赖"></a>
### 目录与依赖

```text
Agent-development-code/
  pyproject.toml / uv.lock / .env.example / tasks.sh
  infra/compose.yml / migrations/ / dockerfiles/
  src/lpa/
    core/         Pydantic 契约、枚举、纯计算；无外部 IO
    config/       Settings、日志配置与脱敏
    llm/          Ollama 原生 NDJSON adapter；兼容端点单独 adapter
    db/           ORM、短事务 repositories、授权视图
    security/     policy、executor、审批校验、审计接口
    crypto/       OpenSSL/GmSSL adapters、能力探测、keystore接口
    tools/        registry、密码/知识工具与 handler
    ingest/       解析、版本化 chunk 与 index manifest
    retrieval/    dense、sparse、fusion、rerank、rewrite
    mcp_adapter/  MCP client、canonical tool bridge、连接配置
    graph/        State、节点、checkpoint、resume
    memory/       提取、授权、更新、去重
    verifier/     事实/引用/输出检查
    api/          FastAPI assembly、资源路由、SSE
    worker/       持久化任务、lease、取消和结果核对
  minimal_agent/  M1 手写版本；从同一 tools/executor 调用
  mcp_servers/    fs/db/domain；独立 entrypoint
  web/           前端
  eval/          Schema、fixtures、scenario runner、metrics、compare
  tests/         合同、故障和集成测试
  docs/decisions/ / docs/progress.md / docs/to-digest.md
  reports/ / data/（不提交真实数据/秘密）
```

Python 包使用合法可导入名称，不把 `agent-api` 目录当 import package，也不使用 `mcp` 顶级包名遮蔽第三方 SDK。M1 可以只建 core/config/tools/llm/minimal_agent。工具包默认在同一个可安装项目内；确需独立发布时再定义 workspace 包和依赖。

core 不依赖 IO 层；llm/db 依赖 core；tools 通过注入 ports 使用 db/retrieval/crypto；graph 编排上述模块；api/worker 装配。executor 调 handler，handler 不回调 graph/api。使用 AST/import-linter 检查分层与唯一 handler 调用点，不用简单 grep 作为安全证明。

<a id="contract-4"></a>
<a id="contract-4-4-工具与唯一执行入口"></a>
### 工具与唯一执行入口

下面是**目标契约示意**，不是当前应用已实现的类型。当前骨架字段与迁移见§4.1；规范工具名/风险/审批/执行次序必须保持一致，不能只因类型样例存在就标完成。

```python
from enum import IntEnum
from typing import Any, Awaitable, Callable, Generic, TypeVar
from pydantic import BaseModel, Field, ConfigDict

T = TypeVar('T')
class RiskLevel(IntEnum):
    READ = 0
    RESTRICTED_COMPUTE = 1
    WRITE = 2
    EXECUTE = 3
    DESTRUCTIVE = 4

class ToolResult(BaseModel, Generic[T]):
    model_config = ConfigDict(extra='forbid')
    success: bool
    data: T | None = None
    error_type: str | None = None
    error: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)
    evidence_refs: list[dict[str, Any]] = Field(default_factory=list)

class ToolSpec(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, extra='forbid')
    tool_id: str
    version: str
    description: str
    input_schema: dict[str, Any]
    output_schema: dict[str, Any]
    timeout_s: float
    permission: str
    risk_level: RiskLevel
    read_only: bool
    idempotent: bool
    max_retries: int
    handler: Callable[..., Awaitable[ToolResult[Any]]]
```

字段运行时需要约束：timeout>0、retry>=0，max_retries>0 必须 idempotent=True 且由本地政策允许。read_only 不等于幂等（读操作也可能有费用/限额）；所有非只读操作max_retries=0；动作重传通过账本返回已有结果，不靠自动重试写操作。handler 的异常由 executor 捕获分类；取消不被吞掉；客户端超时不能被当作外部操作已停止。

canonical tools：inspect_certificate、verify_certificate、digest_file、verify_signature、get_key_metadata、encrypt_file、decrypt_file、sign_file、rotate_key、create_csr、issue_test_certificate、search_knowledge、query_database。MCP bridge将domain.inspect_certificate映射inspect_certificate、db.query_metadata映射query_database；新工具本地登记风险/权限之前只能发现，不能执行。

query_database输入为固定query_id与结构化参数，查询只返回获授权的密码资源元数据和执行记录，禁止模型传原始SQL。密码工具输入使用file_id/certificate_id/key_id与固定profile；真实路径、key version和秘密在服务端解析。加解密、签名、轮换、CSR与测试签发须绑定审批；默认禁止私钥导出、销毁和系统信任修改。各工具输入输出见[业务工具集合](V1-CORE-DEMO.md#crypto-4-4-建议的最小工具集合)。

执行器顺序：

1. 创建内部 attempt/correlation，规范化参数、schema 与业务校验。
2. 校验用户、项目、资源、工具 permission 与预算；记录拒绝。
3. 将用户/项目/工具版本/规范参数/资源版本/策略版本绑定到 action_hash。审批必须匹配该 hash。
4. 短事务写 action intent 和审批/lease 状态，再释放 DB 事务。
5. 经受控 runner 执行，校验输出大小与 schema，写结果和最终审计。
6. 失败/取消/拒绝使用 finally 或统一 outcome 路径记录；执行前安全审计无法持久化时 fail closed。执行后审计失败则保留结果/待补偿状态，不重新执行动作。

日志脱敏、截断与结果 blob 引用统一处理。MCP server 的 readOnlyHint 等注解不直接成为本地授权。[MCP tools 规范](https://modelcontextprotocol.io/specification/2025-06-18/server/tools)


<a id="contract-4-41-当前代码与目标契约的映射"></a>
#### 当前代码与目标契约的映射

以2026-10-10读取的Ubuntu应用骨架为起点。开发时重新核对实际模型与registry，不把本表当永久版本事实。目标升级需要合同测试、事件/持久化兼容与数据版本同步，本文不修改应用。

| 当前骨架 | 目标语义/字段 | 学习者的迁移任务 |
|---|---|---|
| ToolSpec.name | canonical tool_id | M1保留name作为注册键；M4明确适配并锁定canonical映射，避免两个名称漂移 |
| ToolSpec.retry | max_retries与幂等策略 | 当前非只读retry=0保持；增加idempotent与本地许可，不能从read_only自动推断可重试 |
| 尚无独立version字段 | tool version | 初期registry配置记录版本，M4写入Spec/action/approval/runtime快照，变更审批必须失效 |
| ToolResult.citations，当前Citation为文档型 | 通用evidence_refs及知识Citation | M1按现有citations验证；M3/M4设计文档证据与工具结果引用转换，不把artifact伪造为文档页码 |
| ToolCall.tool_name/call_id | canonical tool_id与内部call关联 | ModelClient/bridge显式转换，原生tool_name与应用内部ID分别保存 |
| source/mcp_server | 工具来源/受信任Server关联 | 保留追踪，本地policy不信任外部annotation |
| 当前RiskLevel枚举 | 0–4本地风险语义 | 数值/名字差异显式映射，敏感解密与写动作按V4固定审批政策，不因名字自动降级 |

新增idempotent、version或evidence_refs前先定义读取旧记录的行为；迁移后的输出与评测schema必须一致。样例的泛型Pydantic ToolResult是共同方向，不要求为M1先改动全部成熟契约。没有通用证据字段时明确只支持文档引用范围，不能伪称已覆盖全部Verifier来源。

<a id="agent-1"></a>
<a id="agent-1-1-先区分三个角色"></a>
### 先区分三个角色

| 角色 | 可以做什么 | 不能靠它保证什么 |
|---|---|---|
| 模型 | 理解意图、提议工具和参数、生成计划/草稿 | 不能自行授权、证明动作成功、读取秘密或决定资源归属 |
| Agent运行时 | 管上下文/预算/步骤，调用检索与执行入口，保存状态 | 不能因为模型说成功就修改实际资源状态 |
| 确定性服务 | 检查身份/权限/审批，执行固定Provider操作，返回真实结果 | 不能用schema通过代替授权，不能把模型参数当任意路径/SQL |

一个自然语言请求可能产生零、一或多次工具调用。没有必要调用时允许直接回答或澄清；有事实性操作结论时必须绑定实际结果。Router缩小候选池，Planner组织步骤，两者都不能放宽服务端policy。

<a id="agent-2"></a>
<a id="agent-2-2-数据流控制流与信任边界"></a>
### 数据流、控制流与信任边界

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

<a id="agent-4"></a>
<a id="agent-4-4-v1手写loop需要自己决定的接口与行为"></a>
### V1：手写Loop需要自己决定的接口与行为

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

<a id="crypto-3.1"></a>
<a id="crypto-3.1-31-openssl"></a>
#### OpenSSL

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

<a id="crypto-3.2"></a>
<a id="crypto-3.2-32-gmssl"></a>
#### GmSSL

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

<a id="crypto-3.3"></a>
<a id="crypto-3.3-33-能力探测与安装后的最小验证"></a>
#### 能力探测与安装后的最小验证

| 检查 | 要保存什么 | 不能据此声称什么 |
|---|---|---|
| OpenSSL CLI version/help | 二进制位置、版本、可用命令 | 不证明 Python 后端同版本 |
| Python backend version | Python 包与 OpenSSL backend 版本 | 不证明所有算法均可用 |
| GmSSL C 库 version/self-tests | commit/release、构建与测试记录 | 不证明绑定加载的是同一库 |
| GmSSL-Python 导入 | 模块路径、绑定与库版本 | 不证明 GCM/证书签发都支持 |
| 摘要已知向量 | 输入、期望摘要、实际输出 | 不证明所有密码功能正确 |
| 认证加密/验签 | 往返、认证失败、验签结果 | 不证明应用权限与 keystore 安全 |

provider 的 `capabilities` 来自适配层验证和本地配置，不让模型生成。发现不支持的算法时返回具体错误，再让用户选择受支持方案。

<a id="crypto-4"></a>
<a id="crypto-4-4-建议的最小工具集合"></a>
### 建议的最小工具集合

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

<a id="crypto-6.3"></a>
<a id="crypto-6.3-63-证书解析与验证"></a>
#### 证书解析与验证

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

<a id="provider-practice"></a>
<a id="provider-practice-10-后续可以照着操作的-provider-入门练习"></a>
### 后续可以照着操作的 provider 入门练习

以下命令是**学习步骤**，在完成前置任务后依次执行并记录实际输出。每小节成功后再进入下一节；所有命令在 Ubuntu Bash 中运行。现有文件/源码目录已经存在时先检查内容，不重复生成或覆盖。


<a id="provider-practice-101-准备非敏感文件并核对摘要"></a>
#### 准备非敏感文件并核对摘要

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


<a id="provider-practice-102-没有公开测试证书时生成教学样本"></a>
#### 没有公开测试证书时生成教学样本

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


<a id="provider-practice-103-gmssl-c-库的一次受控构建"></a>
#### GmSSL C 库的一次受控构建

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


<a id="provider-practice-104-python-绑定与能力检查"></a>
#### Python 绑定与能力检查

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


<a id="provider-practice-105-后续同步依赖时保留-crypto-组"></a>
#### 后续同步依赖时保留 crypto 组

`crypto` 组创建后，M2 使用 `uv sync --extra m1 --extra m2 --extra crypto --extra dev`；M3 加 `--extra m3`，M4 再加 `--extra m4`。只有真正做 reranker 才增加 `ml`。锁文件形成后复现加 `--frozen`，不同阶段选择的 extras 写进运行说明。

完成这些练习后，才开始自己实现统一 provider adapter。第一轮只封装证书解析和摘要；输入/输出/异常稳定后再接 execute_tool 和模型。

## 本阶段签收清单

- [ ] 本阶段学习技术表逐项有本人解释、独立实现/修改和失败验证证据。
- [ ] Q01–Q22已由本人结合实现作答，证据与未覆盖边界记入docs/progress.md；AI仅审查。

- [ ] M1 01–05/07只读范围与M1 08–13通过，证书/摘要独立对照。
- [ ] 本人手写Loop、单多调用/失败/预算/NDJSON可解释，已有少量case。
- [ ] M1 06和写范围留V4，未提前标m1全目标毕业。

## 下一步

本阶段出口有证据后进入[V2阶段](V2-WEB.md)。跨阶段未完标准登记补齐位置。
