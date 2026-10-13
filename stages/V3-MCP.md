# V3 MCP接入

本阶段基础预算**12h**；实现成果：同一业务服务直调与一个Crypto MCP Server调用对照。先读实现目标与当前切片，再执行详细任务；完成标准以实际证据为准。

| 入口问题 | 本阶段安排 |
|---|---|
| 从哪里开始 | 按当前切片与本章分步操作扩展已有Demo |
| 首次进入的任务 | M4 07、M4 08、M4 11；可能只实现本阶段范围，完整版完成位置见任务索引 |
| 完整技术目标卡 | 目标8；跨阶段项目以后补齐，不将全表当当前前置 |
| 如何判断完成 | 正常/失败/权限与真实结果可核对，本人能解释、改需求和排错；本章出口清单全部有证据 |
| 按需参考 | [07-AGENT-SYSTEM-DESIGN.md](../reference/07-AGENT-SYSTEM-DESIGN.md)；[06-CRYPTO-AGENT-SCOPE.md](../reference/06-CRYPTO-AGENT-SCOPE.md) |

每个技术目标的第一张表说明能力深度，紧接的实践表说明具体练习；两者在此集中阅读。通用周计划/任务卡见[学习总览](../LEARNING-PATH.md)，原M1–M6查[任务索引](../reference/TASK-INDEX.md)。

**当前切片**：目标8的12h；复用V1真实业务函数和V2身份资源上下文，不要求先实现密码写工具或知识库。MCP只增加协议入口，秘密与最终授权仍在受控服务端。


### 目标8：MCP 工具互操作（20h）

**进入条件**：V1已有canonical registry与只读执行入口，V2身份/资源授权可用。V3用12h接一个Crypto MCP Server，V6用8h补三职责/Resource/Prompt/新端点验收；不等待目标7全部写动作。

**Agent目标**：协议发现和互操作统一接回本地执行入口。 对应详细任务：**M4 07–11**。

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

**退出条件**：三Server与Resource/Prompt可见；两类刷新可复现，调用均经本地policy，V3只签收单Server切片，V6全部通过才标记m4-mcp-done。

**具体实践与逐项操作**


V3执行M4 07–08与M4 11已有Server刷新切片。M4 09–10和M4 11新增授权端点留V6；下面是完整目标表，V3单Server不等于完整MCP毕业。

先学 Client/Server、tools/list、tools/call、Resource、Prompt、stdio 和连接配置。不要把 MCP 当权限系统；Agent 仍然使用本地执行器。

**技术点掌握程度标准**

| 技术点 | 本阶段必须能独立做到 | 练习与验收证据 | 可后置内容 |
|---|---|---|---|
| MCP Client/Server 与 stdio | 启动一个只读 Server，Client 完成发现和调用；协议输出与普通日志分开，管理退出与超时 | M4 07 tools/list、tools/call 原始记录，断开/错误不伪装成功 | 多传输适配、远程 MCP 运维 |
| Schema 与工具桥接 | 外部工具名映射到 canonical tool_id；输入输出经过本地契约，仍走执行器授权 | M4 08 同一工具直调/MCP 路线的允许与拒绝结果一致 | 大量异构工具自动适配 |
| Resource 与 Prompt | 解释读取资料、提供模板和执行工具的区别；资料不能给自己新增权限 | M4 10 各调用记录，说明模板内容如何进入模型上下文 | 完整模板管理系统 |
| 三职责 Server 与连接生命周期 | 分开 fs/db/domain，记录来源；启动、断开、失败清理可追踪，命名不遮蔽 SDK | M4 09 三个连接的职责图与调用证据 | 大规模插件隔离与集群编排 |
| 工具刷新与可信端点配置 | 分清现有连接工具变更和新端点连接；只从可信配置加载端点，审查新增工具风险 | M4 11 两种刷新各一记录，未授权端点没有实际连接 | 任意公共 MCP 自动发现与接入 |

| 顺序 | 学习任务 | 实现结果 | 验收指标 |
|---|---|---|---|
| M4 07 | 做一个只读密码 MCP Server | 暴露证书检查或文件摘要 | Client 能发现并调用，协议错误不伪装成功 |
| M4 08 | 接到本地 registry | MCP tool name→canonical tool_id | 相同权限规则不能因 MCP 路线绕过 |
| M4 09 | 增加 fs/db/domain 三职责 Server | fs 授权文件、db 元数据、domain 密码工具 | 包布局不遮蔽 SDK，全部连接可追溯 |
| M4 10 | 一个 Resource 与 Prompt | 公开工具说明、操作计划模板 | Resource/Prompt 不含秘密或自授权指令 |
| M4 11 | 刷新与可信新连接 | 已连接工具变更刷新；新端点配置热加载 | 两种情况分别验证；未授权端点不连接 |

stdio 的 stdout 是协议，日志走 stderr。MCP server 只给必要资源权限，不通过“远端说它 read_only”自动降低风险。先 stdio，再考虑 Streamable HTTP；后者需要额外鉴权、Origin/host 与网络边界检查。

**独立练习**：在已连接 Server 增加只读工具，不改 Agent 核心代码，刷新后发现它；然后新增一个未配置 Server，证明它不能自动被信任。

保存发现/调用/拒绝日志；V3单Server签收，m4-mcp-done须V6完整目标8通过。

### 单Server的逐步对照与出口

1. 固定当前已支持的证书/摘要输入输出schema，先保存直接调用正常/拒绝/失败的结果。
2. 在合法包名下建立stdio Server，工具handler调用同一业务服务；stdout仅协议、stderr日志，禁止任意CLI参数透传。
3. Client获取工具描述和schema，将外部domain名称映射本地canonical ID；模型提议先经execute_tool，再发MCP请求。
4. 服务端校验可信身份/资源/本地policy；不信任模型传来的user_id、角色或approved字段。V3可先固定一个授权教学用户的受限Server/连接；多个API用户不能共享这个固定身份，后端须选择对应受限连接或可信凭据映射。身份来自已鉴权上下文，不来自模型参数。
5. 给同一次调用关联run/call记录，保存模型提议→MCP请求→Server handler→Provider结果→回传模型的脱敏链路。
6. 用同一文件/证书对照直调与MCP；断连、未知工具、非法参数和越权结果都符合本地策略。
7. 已连接Server增加一个经本地登记的只读能力后验证刷新；未登记的工具只发现不执行。

**出口**：两个入口语义一致、授权一致，可独立说明每层职责；只签收V3。下一步V4审批写操作，m4-mcp-done留V6。

## 本阶段签收清单

- [ ] M4 07–08与11已有连接刷新：一个Crypto Server复用原业务服务。
- [ ] 模型提议/MCP请求/handler/Provider/反馈关联，直调与MCP允许/拒绝/失败一致。
- [ ] 三职责/Resource/Prompt/新端点留V6，不提前标m4-mcp-done。

## 下一步

本阶段出口有证据后进入[V4阶段](V4-APPROVAL-CRYPTO.md)。跨阶段未完标准登记补齐位置。
