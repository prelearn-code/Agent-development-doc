# V3 MCP接入

本阶段基础预算**12h**；实现成果：同一业务服务直调与一个Crypto MCP Server调用对照。先读实现目标与当前切片，再执行详细任务；完成标准以实际证据为准。

## 实现目标与学习结果要求

先包装一个Crypto MCP Server，复用V1业务函数，保持与直接调用相同的授权、结果与错误。学习协议和调用层次，不把业务藏进一个自动框架；三个职责Server、Resource/Prompt完整专项在V6补齐。

当前Demo已在`mcp_integration/server_crypto/gmssl_tools/sm_tools.py`注册SM2密钥生成、签名和验签，服务入口为`server.py`；`mcp_integration/client/`负责连接并通过`session.list_tools()`发现工具。现有SM2固定CLI调用已迁到`packages/crypto/providers/gmssl_cli.py`，教学密钥在`packages/crypto/keystore.py`。OpenSSL工具包装及更完整的桥接与授权策略仍需后续实现。

当前SM2模块提供`register_tools(mcp)`函数，服务入口创建一个MCP实例并调用注册函数后启动。仅导入Provider函数不会把它发布为MCP工具；只有注册到客户端所连接服务的工具，才会出现在该服务的工具列表中。新增工具时继续向同一实例注册，再重启服务并刷新客户端工具列表，核对真实list/call结果。

目标调用链为：Agent Loop → `tools/executor.py`执行控制 → MCP客户端 → Crypto MCP工具与服务端授权 → Provider函数 → 已编译的OpenSSL/GmSSL程序。`tools/`管理登记与执行，`packages/crypto/`封装密码后端；业务工具无需每次自行编写子进程调用，但每次实际密码计算仍由Provider调用可执行程序。

| 需要学习的技术 | 学习结果要求 | 独立实现与排错证据 |
|---|---|---|
| MCP Client/Server与连接生命周期 | 解释stdio与一次工具请求的路径，能力协商依锁定SDK实际支持 | 真实启动、连接、list/call、退出与断开记录 |
| Tools Schema与工具桥接 | 外部名称映射canonical ID，保留本地schema/风险/权限策略 | 同一输入直调/MCP对照；未知/重名/不匹配受控拒绝 |
| 业务服务复用与Server授权 | Server调用同一确定性服务，最终资源授权在服务端复查 | 不经Agent直调Server也不能越权或绕过未来审批 |
| 错误、超时、取消与Trace关联 | 分开协议错误/业务拒绝/Provider失败，关联模型提议与实际调用 | 断线/超时/Provider错误不伪装成功；原始请求和结果可定位 |
| 工具刷新、Tools/Resources/Prompts | 识别三类能力，区分已连接Server变化与新增授权endpoint | 已有连接工具刷新真实验证；未实现能力明确登记 |
| Python包与协议输出 | 项目mcp_integration不遮蔽SDK；stdout只用于协议，日志走stderr | 核对import来源和协议流，普通日志不污染报文 |

## 必须独立回答的关键问题

这些问题必须由你结合自己的实现作答，AI只审查。记录在本阶段文末的本人学习记录中，写清场景、自己的理由、真实证据与未覆盖边界；只背定义或复制AI答案不算通过。

| 编号 | 必须自己回答的问题 | 回答达到标准所需的说明或证据 |
|---|---|---|
| Q01 | MCP在已有Demo上具体增加了什么？哪些Agent职责仍由你自己实现？ | 画加入协议前后的调用链，指出Loop/授权/Provider的位置 |
| Q02 | 模型tool call与MCP tools/call是否是同一层请求？ | 关联两层实际报文与内部call ID，说明转换边界 |
| Q03 | 为什么先一个Crypto Server，而不是按OpenSSL/GmSSL各建一个？ | 说明业务能力与Provider选择的关系以及当前部署范围 |
| Q04 | Server怎样复用原handler或业务服务？如何避免两套结果逻辑？ | 指出真实复用函数与直接/MCP对照证据 |
| Q05 | 工具列表中的描述和annotation能否决定本地授权？ | 解释本地policy、schema与服务端复查的依据 |
| Q06 | 绕过Agent直接请求MCP Server时，如何仍保证资源归属？ | 提供越权拒绝和Provider未执行的证明 |
| Q07 | 外部server/tool名称与canonical工具ID如何关联？ | 解释映射唯一性、版本与重名处理 |
| Q08 | 参数在Client校验过，Server为什么还需要检查？ | 说明服务边界与不可信请求，构造绕过Client的反例 |
| Q09 | 为什么stdout上的一条普通日志可能破坏stdio协议？ | 展示协议/日志各自通道与真实输出 |
| Q10 | 项目目录为什么不能叫顶级mcp？怎样核对导入来源？ | 给出SDK实际文件来源与合法项目包名 |
| Q11 | 协议请求失败、业务拒绝和密码工具失败怎么区分？ | 实际错误码、ToolResult与最终回答分别核对 |
| Q12 | 连接中断是否证明Server里的操作没有发生？ | 说明只读当前范围与未来写动作的不确定性核对 |
| Q13 | 一个超时请求如何关联到模型提议、handler和Provider？ | 展示完整Trace关联及脱敏，不能只记录工具名字 |
| Q14 | Tools、Resources和Prompts各提供什么？内容为什么仍不自动可信？ | 说明授权/内容来源及当前已实现和后续范围 |
| Q15 | 已有Server工具列表变化与新增Server连接为什么要分别测试？ | 解释刷新、授权配置与不自动扫描的边界 |
| Q16 | SDK升级后，怎样证明本机支持的协议能力没有被文档假设替代？ | 实际版本、协商和最小调用，不凭最新文档宣称已支持 |
| Q17 | 直调与MCP输出必须逐字相同吗？该比较哪些实际行为？ | 列出结构/语义/允许拒绝/资源结果，排除随机措辞 |
| Q18 | MCP包装以后你还能逐层定位一次失败吗？ | 本人解释并修复一个连接/映射/业务问题后回归 |

## 分步任务与技术掌握标准

先按当前切片实现最小输入输出，再补齐技术表。本阶段首次运行、正常/失败/权限、本人解释与独立修改分别验收；未实际运行不签收。

**当前切片**：目标8的12h；复用V1真实业务函数和V2身份资源上下文，不要求先实现密码写工具或知识库。MCP只增加协议入口，秘密与最终授权仍在受控服务端。


### 目标8：MCP 工具互操作（20h）

**进入条件**：V1已有canonical registry与只读执行入口，V2身份/资源授权可用。V3用12h接一个Crypto MCP Server，V6用8h补三职责/Resource/Prompt/新端点验收；不等待目标7全部写动作。

**Agent目标**：协议发现和互操作统一接回本地执行入口。 对应详细任务：**T047–T051**。

**技术点掌握程度标准**

| 技术点 | 能解释 | 独立做到 | 排错与边界 | 验收证据 | 后置内容 |
|---|---|---|---|---|---|
| 协议/Client/Server | 发现调用不等于授权 | fs/db/domain三角色Server，一个Resource与Prompt | 锁定SDK/协议，协议失败不能包装成功 | initialize/list/call脱敏记录 | 全部协议扩展 |
| stdio生命周期 | stdout协议、stderr日志 | 受控启动/关闭/超时/断连 | 普通print污染协议与僵尸进程可定位 | 断连与退出检查 | 远程HTTP传输 |
| Registry bridge | 外部名称映射本地canonical ID | fs./db./domain.命名空间桥接统一执行器 | 名称冲突、schema不符、未知风险拒绝 | 注册与调用对照 | 全网自动发现 |
| 刷新/可信配置 | 工具变化与新增Server不同 | 通知或显式refresh，热加载授权端点 | 未配置端点不连接，annotation不自授权 | 两类变化分别验证 | 公共MCP市场接入 |

**学习与实现顺序**：单stdio只读Server → bridge → 三角色 → Resource/Prompt → 工具刷新 → 新授权端点。选修Streamable HTTP需补认证、Origin/host与网络约束。

**必须独立回答**：发现成功为什么可能执行拒绝？Server日志为何不能写stdout？新端点由谁授权？

**独立练习**：不改Agent业务代码新增一个本地登记的只读工具；刷新后检查策略仍生效。

**退出条件**：三Server与Resource/Prompt可见；两类刷新可复现，调用均经本地policy；V3只签收单Server切片，目标8全表留到V6验收。

**具体实践与逐项操作**


V3执行T047–T048与T051已有Server刷新切片。T049–T050和T051新增授权端点留V6；下面是完整目标表，V3单Server不等于完整MCP毕业。

先学 Client/Server、tools/list、tools/call、Resource、Prompt、stdio 和连接配置。不要把 MCP 当权限系统；Agent 仍然使用本地执行器。

**技术点掌握程度标准**

| 技术点 | 本阶段必须能独立做到 | 练习与验收证据 | 可后置内容 |
|---|---|---|---|
| MCP Client/Server 与 stdio | 启动一个只读 Server，Client 完成发现和调用；协议输出与普通日志分开，管理退出与超时 | T047 tools/list、tools/call 原始记录，断开/错误不伪装成功 | 多传输适配、远程 MCP 运维 |
| Schema 与工具桥接 | 外部工具名映射到 canonical tool_id；输入输出经过本地契约，仍走执行器授权 | T048 同一工具直调/MCP 路线的允许与拒绝结果一致 | 大量异构工具自动适配 |
| Resource 与 Prompt | 解释读取资料、提供模板和执行工具的区别；资料不能给自己新增权限 | T050 各调用记录，说明模板内容如何进入模型上下文 | 完整模板管理系统 |
| 三职责 Server 与连接生命周期 | 分开 fs/db/domain，记录来源；启动、断开、失败清理可追踪，命名不遮蔽 SDK | T049 三个连接的职责图与调用证据 | 大规模插件隔离与集群编排 |
| 工具刷新与可信端点配置 | 分清现有连接工具变更和新端点连接；只从可信配置加载端点，审查新增工具风险 | T051 两种刷新各一记录，未授权端点没有实际连接 | 任意公共 MCP 自动发现与接入 |

| 顺序 | 学习任务 | 实现结果 | 验收指标 |
|---|---|---|---|
| T047 | 做一个只读密码 MCP Server | 暴露证书检查或文件摘要 | Client 能发现并调用，协议错误不伪装成功 |
| T048 | 接到本地 registry | MCP tool name→canonical tool_id | 相同权限规则不能因 MCP 路线绕过 |
| T049 | 增加 fs/db/domain 三职责 Server | fs 授权文件、db 元数据、domain 密码工具 | 包布局不遮蔽 SDK，全部连接可追溯 |
| T050 | 一个 Resource 与 Prompt | 公开工具说明、操作计划模板 | Resource/Prompt 不含秘密或自授权指令 |
| T051 | 刷新与可信新连接 | 已连接工具变更刷新；新端点配置热加载 | 两种情况分别验证；未授权端点不连接 |

stdio 的 stdout 是协议，日志走 stderr。MCP server 只给必要资源权限，不通过“远端说它 read_only”自动降低风险。先 stdio，再考虑 Streamable HTTP；后者需要额外鉴权、Origin/host 与网络边界检查。

**独立练习**：在已连接 Server 增加只读工具，不改 Agent 核心代码，刷新后发现它；然后新增一个未配置 Server，证明它不能自动被信任。

保存发现/调用/拒绝日志；V3单Server签收，目标8全表须在V6完整通过。

### 单Server的逐步对照与出口

1. 固定当前已支持的证书/摘要输入输出schema，先保存直接调用正常/拒绝/失败的结果。
2. 在合法包名下建立stdio Server，工具handler调用同一业务服务；stdout仅协议、stderr日志，禁止任意CLI参数透传。
3. Client获取工具描述和schema，将外部domain名称映射本地canonical ID；模型提议先经execute_tool，再发MCP请求。
4. 服务端校验可信身份/资源/本地policy；不信任模型传来的user_id、角色或approved字段。V3可先固定一个授权教学用户的受限Server/连接；多个API用户不能共享这个固定身份，后端须选择对应受限连接或可信凭据映射。身份来自已鉴权上下文，不来自模型参数。
5. 给同一次调用关联run/call记录，保存模型提议→MCP请求→Server handler→Provider结果→回传模型的脱敏链路。
6. 用同一文件/证书对照直调与MCP；断连、未知工具、非法参数和越权结果都符合本地策略。
7. 已连接Server增加一个经本地登记的只读能力后验证刷新；未登记的工具只发现不执行。

**出口**：两个入口语义一致、授权一致，可独立说明每层职责；只签收V3。下一步V4审批写操作，目标8全表留V6。

## 本阶段的接口与实践细节

以下内容属于本阶段，按任务用到的部分查阅；涉及后续能力的字段仅作为扩展合同，当前切片不要求提前全部实现。

<a id="agent-7"></a>
<a id="agent-7-7-tool与mcp桥接"></a>
### Tool与MCP桥接

canonical工具、风险、审批与执行顺序按[V1工具契约](V1-CORE-DEMO.md#contract-4)与[V4审批合同](V4-APPROVAL-CRYPTO.md)，业务输入输出按V1/V4/V6的密码工具合同。MCP只负责互操作，外部工具描述/annotation不能覆盖本地permission或read_only。桥接应保存外部server/tool名称、canonical ID、SDK/协议与本地policy版本。

MCP的Tools、Resources、Prompts是不同能力：本项目用工具执行，Resource提供受控内容，Prompt提供提示模板；后两者仍是不可信输入，需要授权和内容边界。能力协商与连接生命周期依锁定实现，不因为新协议文档存在就默认本机支持全部特性。[MCP官方架构](https://modelcontextprotocol.io/docs/2026-07-28/learn/architecture)

**验收**：同一调用经本地与MCP入口时有相同canonical ID与本地策略；协议报错不变成success；工具列表变化与新增授权Server分开验证。

## 本阶段签收清单

- [ ] 本阶段学习技术表逐项有本人解释、独立实现/修改和失败验证证据。
- [ ] Q01–Q18已由本人结合实现作答，证据与未覆盖边界记入本阶段文末的本人学习记录；AI仅审查。

- [ ] T047–T048与T051已有连接刷新：一个Crypto Server复用原业务服务。
- [ ] 模型提议/MCP请求/handler/Provider/反馈关联，直调与MCP允许/拒绝/失败一致。
- [ ] 三职责/Resource/Prompt/新端点留V6，不提前认定目标8全表通过。

## 下一步

本阶段出口有证据后进入[V4阶段](V4-APPROVAL-CRYPTO.md)。跨阶段未完标准登记补齐位置。
