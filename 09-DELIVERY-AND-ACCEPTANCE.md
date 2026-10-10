# 09 - Ubuntu交付、证据与毕业验收

配合[00主路径](00-ROADMAP.md)目标16及综合15h。本文给出未来应用交付流程，不宣称当前代码已支持这些启动命令或备份脚本。文档静态检查不执行密码业务，也不代表应用已完成验收。

环境、网络与历史快照见[01](01-ENVIRONMENT.md)，任务操作见[05](05-UBUNTU-STEP-BY-STEP.md)，接口见[08](08-API-AND-WEB.md)，评测流程见[eval/README](eval/README.md)。命令、服务名、迁移版本与资源路径必须先按实际实现填写，不能把占位命令包装成一键可用。

## 1. 四仓库布局与版本

```text
/home/zsw/work/agent_development/
├── Agent-development-doc/      本学习文档
├── Agent-development-code/     应用实现
├── openssl/                    OpenSSL官方源码
└── GmSSL/                      GmSSL官方C源码
```

四仓库同父目录、同级、独立Git历史。需要官方Python绑定源码时增加同级GmSSL-Python。实际用户名可替换，但保持结构；clone/build/test都在Ubuntu文件系统。源码与安装prefix分离；不要将两个密码源码塞进文档或应用仓库，不提交库构建产物/私钥/模型权重。

| 固定项 | 记录内容 | 验证用途 |
|---|---|---|
| doc/code | remote、branch、commit、dirty状态 | 确认使用同版规格与实现 |
| OpenSSL/GmSSL/绑定 | tag/commit、构建参数、prefix、动态库路径、能力列表 | 确认真实Provider支持，系统CLI与Python backend分开 |
| Python/前端 | 解释器、uv.lock、pnpm锁、Node/pnpm版本 | 新目录依赖复现 |
| 模型/检索 | Ollama版本、model digest、量化/template/think、embed/rerank、index hash | 防止环境变化冒充模型收益 |
| DB/Graph/policy | Alembic revision、graph/schema版本、policy版本 | 恢复兼容检查 |
| 服务镜像 | image tag+digest、Compose配置hash、profile | 依赖与部署可复现 |

版本清单不放数据库口令、API key、keystore解锁材料和完整带密URL。文档中的环境版本是日期快照，实际交付重新测量，不能声称一直最新。

## 2. 最小交付包

| 位置（应用仓库建议） | 应有内容 | 完成标准 |
|---|---|---|
| README / docs/runbook.md | 当前有效安装、迁移、启动、停止、smoke、恢复命令 | 新终端/干净clone实际执行过 |
| .env.example / config | 所有已使用字段、默认值、必需/可选、秘密来源 | 与Settings/启动校验一致；无真实秘密 |
| pyproject / uv.lock / frontend锁 | 分阶段extras、固定依赖 | 不因加crypto extra覆盖已有extras |
| migrations | schema与角色迁移、checkpointer初始化方式 | 空库与已有库升级测试 |
| compose/镜像配置 | profiles、健康、网络、volumes、资源与日志限制 | 启动顺序与ready分别验证 |
| tests / eval runner | 合同/mock/集成/安全/专用GPU入口 | 分类执行；没有GPU不伪报实测 |
| docs/decisions | 本人阶段ADR | 记录证据、限制、重审条件 |
| reports/或外部结果目录 | 版本清单、逐case结果、Trace与恢复演练 | 引用路径可定位，敏感结果不公开提交 |

报告目录是建议，实际代码若用别名要在runbook说明。大blob、解密产物与真实.env不进入Git；评测fixture只使用审定教学资源。交付过程记录每一步状态“已验证/未验证/不适用及理由”。

## 3. 服务与网络

| 服务 | 首版角色 | 监听/权限要求 |
|---|---|---|
| Web/API | 浏览器入口与鉴权 | Ubuntu受控网卡/端口，Windows浏览器可访问；仅开放需要端口 |
| Ollama | 本机模型服务 | Ubuntu127.0.0.1；host网络路线按01；bridge路线另配置可达地址，不默认全网开放 |
| PostgreSQL | Run/资源/审计/checkpoint | 回环或内部网络；app/query/audit/migration不同凭据 |
| Qdrant | 授权向量检索 | 内部网络，不能让浏览器直连绕过API |
| MCP | 受信任工具进程/端点 | stdio优先，日志stderr；远程另补鉴权/Origin/host |
| Provider/keystore | 固定密码API与受控材料 | keystore不是通用读取root，运行账号最小权限 |
| worker/Redis/对象存储 | 按需扩展 | 未引入不算缺核心；引入后验收领取、持久化与网络权限 |

默认方案可让API使用host网络访问Ubuntu回环Ollama，DB/向量库发布到回环；alternative bridge不能把容器127.0.0.1当宿主。两套网络选一套实际验证并在runbook写清。容器不是自动安全边界，API不持有Docker socket、bootstrap或migration秘密。

启动不等于ready；Compose的依赖条件/健康检查要与真实业务依赖对应，应用还需超时和明确失败。只有启用的能力列为ready依赖；GmSSL未启用可标disabled，已承诺工具却缺库必须标unavailable并拒绝调用。[Docker Compose官方启动顺序](https://docs.docker.com/compose/how-tos/startup-order/)

## 4. 干净目录复现的逐步表

所有操作在Ubuntu；先保存现有改动与资源，不复用生产密钥，不删除原工作目录。给隔离教学实例分配不同端口、项目/用户/索引空间。

| 步骤 | 学习者操作 | 应得到的证据 | 不通过时先看 |
|---|---|---|---|
| 1 定位 | 核对四仓库remote/commit与目录，选教学实例 | 路径/版本清单，dirty说明 | clone/ref/大小写/权限 |
| 2 配置 | 从样例生成本地配置，注入测试凭据与受控root | 脱敏字段校验结果 | 缺变量、错误路径、误装到另一环境 |
| 3 依赖 | 用lock恢复Python/前端，按选定Provider构建/加载 | 解释器/锁/库能力记录 | 动态库路径、prefix、backend差异 |
| 4 模型 | 只安装当前阶段模型，真实请求核对digest/计量 | 模型请求与GPU/CPU状态 | listener、名称、内存/显存 |
| 5 存储 | 启动所需DB/向量库，迁移与角色，初始化saver | revision/权限/健康结果 | 依赖未ready、连接凭据、旧schema |
| 6 应用 | 启动API与Web，可选worker/MCP | live/ready、端口与配置版本 | 网络模式、CORS、可信端点 |
| 7 smoke | 认证、只读工具、snapshot/SSE、权限拒绝 | 同Run全链路证据 | 按07排错顺序定位 |
| 8 浏览器 | Windows打开Ubuntu入口，审批/刷新/下载 | 交互与实际状态对照 | 防火墙/监听/鉴权/SSE |
| 9 重启 | 受控停启，检查pending/产物/历史 | 数据保留与恢复记录 | volume、checkpoint、动作账本 |
| 10 备份恢复 | 在独立实例恢复一份一致备份 | hash/权限/版本/旧动作核对 | 缺keystore、index版本、unknown |

首版先写实际命令，再由另一个终端按文档跑，修正遗漏；不直接假设代码目标目录src/lpa已经存在，当前packages骨架按结构文档映射。学习者须独立说明一个启动故障与一条修复依据。

## 5. 数据与密钥备份恢复

| 数据 | 为什么需要 | 恢复核对 |
|---|---|---|
| DB/审计/审批/账本/checkpoint | 持久任务和动作决定 | revision/graph/schema兼容、引用、未完成动作 |
| 上传文件/artifact | 工具输入与真实产物 | ID/size/hash/版本/权限与DB关联 |
| corpus/parse/index manifest | 引用与实验复现 | 旧document版本/locator和active状态，必要时重建索引 |
| keystore加密blob | 旧密文与签名对应的密钥版本 | 材料存在、完整性、用途/状态、旧版本仍按策略可用 |
| 解锁材料/恢复秘密 | 解密keystore备份所需 | 独立安全保管；不随报告/Git提交 |
| 配置/版本清单 | 可解释恢复环境 | 固定库/模型/图/policy，脱敏且与实际对应 |

首版使用维护窗口：暂停新写动作，等待可确认动作结束，记录无法确认的unknown；再按所选DB与存储的受控备份方法取一致版本。加密blob、DB与文件必须有共同快照清单。教学用nonce分配持久状态也属于需要一致恢复的数据，恢复后不能回退计数导致旧key/nonce复用；采用安全分配/轮换策略后再开放写操作。

恢复顺序由实际依赖确定：隔离配置 → 固定服务/版本 → 迁移兼容 → 恢复DB及材料/文件/manifest → 核对hash与ACL → 检查pending/unknown → 只读smoke → 受控教学动作 → 最后重新开放写动作。旧批准若资源或policy版本不匹配必须失效；unknown核对前不得批量resume。

**必须实验**：重启数据不丢；从一份备份恢复一个已完成artifact与一个待审批Run；缺失key blob时正确拒绝解密而非编造成功。恢复用测试材料，不在原库上做破坏性演练。

## 6. 三条综合验收路线

### 路线A：证书/摘要只读闭环

1. 上传公开教学证书和非敏感小文件，记录来源/hash/权限。
2. 问证书字段与文件摘要，查看模型提议、授权与实际Provider结果。
3. 用独立命令/已知向量对照，确认公开字段/摘要，而非只比两段模型文本。
4. 页面查看ToolResult、Run计量与Verifier；未进行的信任/撤销检查显示not_checked。
5. 用另一测试用户读取同资源必须失败；Trace不得泄露真实路径/秘密。

### 路线B：固定审批、产物/版本与恢复

1. 查询教学key元数据，选明确profile与≤1MiB教学文件。
2. 提议加密或轮换，页面展示固定参数、key/resource/policy版本、hash与期限。
3. 拒绝一次，确认没有产物/版本变化；新提议批准后核对真实artifact/hash或新版本。
4. 刷新待审批、重复同决定、资源变更各验证，不能二次授权新动作。
5. 在执行前/中/后指定故障点演练恢复，核对账本与外部结果；不确认则unknown。
6. 加解密闭环按06验证往返/认证失败；轮换验证旧版本策略，秘密不进入模型/页面日志。
7. 补证书链验证或测试CSR/签发，区分自签/测试签发与生产信任。

### 路线C：知识、Memory与验证

1. 入库已审定PDF/MD/TXT操作资料，发布manifest。
2. 问一个可回答知识问题，点击引用定位，Verifier绑定支持的Claim；再问无答案问题。
3. 纠正/删除显式偏好，用同用户新session与其他用户确认隔离。
4. 展示≥20正/20错Verifier报告和四配置模型实验，定位一条失败/误判。
5. 把完整任务加入frozen scenario，带真实fixture/版本与成功谓词，不用截图代替断言。

三条路线都记录同一请求中的UI/API/DB/Provider证据。失败与拒绝是验收的一部分，不为演示隐藏或临时放宽权限。

## 7. 毕业能力矩阵

| 能力 | 正常证据 | 失败/边界证据 | 个人掌握检查 |
|---|---|---|---|
| A 模型/Loop | 原始协议、单多调用、计量 | 失败回传、预算、重复停止 | 本人修改Loop并解释反馈顺序 |
| B RAG | 三格式定位、≥50审定题、四组检索 | 无答案/越权/索引失败/版本 | 手算指标并解释消融 |
| C DB | 迁移、六查询、短事务 | 角色拒绝、重启、一致性 | 独立写/改查询，解释intent |
| D Tools | 真实密码结果、≥50工具题 | schema/超时/审批/认证失败 | 新增受控参数与风险理由 |
| E MCP | 三Server、Resource/Prompt、刷新 | 未授权端点、协议错/未知风险 | 解释发现与本地授权区别 |
| F Workflow | checkpoint/固定审批/恢复 | 重放/过期/变更/三处崩溃 | 本人State设计、unknown核对 |
| G Memory | 跨session、来源、纠正删除 | 跨用户/无关输入/投毒 | 解释四上下文与事务替代 |
| H Eval | 100–180frozen、Runner、配对compare | 无效fixture、结果缺失、泄漏检查 | 本人gold与成功谓词，pp/分母 |
| I Security | 威胁模型、拒绝审计 | 关键攻击面实际资源断言 | 本人设计边界测试，实际越权0 |
| J Full stack | 页面、干净复现、备份恢复 | 断线/刷新/冲突/unknown/下载拒绝 | 改交互、诊断网络、说明恢复依赖 |

RAG≥50、Tool≥50是能力专项要求；综合100–180按唯一case ID计数，可以交叉覆盖但不能虚增样本。未引入worker等选修标“不适用与理由”，不能用它豁免核心审批/恢复。

## 8. 证据卡与阶段签收模板

| 字段 | 由学习者填写 |
|---|---|
| 目标/技术项/状态 | 目标编号、表格行名、待学/在做/已验证/缺口 |
| 预期与成功谓词 | 正常、失败、安全必要条件 |
| 输入/环境 | fixture来源、hash、code/model/config版本 |
| 执行记录 | 命令、退出码、case/run/action ID、日志位置 |
| 实际结果 | 与预期差异、计量、真实资源状态 |
| 个人检查 | 自己解释、需求修改/排错、尚不理解之处 |
| 限制与补测 | 降级、不适用理由、责任与补测时间 |

每阶段使用[checklist](checklist.md)打勾，自己写ADR，检查to-digest是否仍含本阶段关键内容。本人不会解释的核心模块，即使测试通过也不签收。

## 9. 发布前门禁与完成边界

确定性合同/授权/审批/恢复回归通过；相关LLM变更用同frozen数据/环境compare，报告全部case与性能；任何实际越权阻止发布。普通CI不假定有本机Ollama/GPU。安全和关键协议测试不能为了展示而放宽。

毕业包包含实际可执行runbook、锁/版本、测试结果、评测报告、脱敏正常/失败Trace、浏览器路线、备份恢复记录与本人ADR。未完项/CPU降级/未支持Provider能力如实列出。首版只能称首版；这套学习系统验收不等于生产密码服务合规认证。
