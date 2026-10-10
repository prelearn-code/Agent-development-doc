# Checklist - 进度与交付物

> 未运行不勾选；降级写原因、影响、补测时间。权威契约见 [repo-structure.md](repo-structure.md)，指标见 [02-MODEL-AND-EVAL.md](02-MODEL-AND-EVAL.md)，数据见 [eval/README.md](eval/README.md)。基础预算450h，含余量520~565h。

当前以OpenSSL/GmSSL封装学习Agent全栈开发。逐步操作和独立练习见[05-UBUNTU-STEP-BY-STEP.md](05-UBUNTU-STEP-BY-STEP.md)，领域验收见[06-CRYPTO-AGENT-SCOPE.md](06-CRYPTO-AGENT-SCOPE.md)。本清单保持未勾选；文档编写不等于应用实现完成。

## Phase0（20h）

- [ ] 应用独立目录、Git、Python3.12/uv/venv、合法pyproject/lock。
- [ ] Ollama与qwen3.5:4b能完成最小请求，保存版本/digest与GPU/CPU实测状态。
- [ ] 配置样例、脱敏日志、测试与lint入口、实际工时记录。
- [ ] Phase0无需一次装4模型/启动4服务，核心验收通过，phase0-done。

## M1（70h）

- [ ] 目标1：Pydantic ToolResult与schema一致，公开证书解析/授权摘要有独立对照；固定provider入口与资源ID解析。
- [ ] 空结果成功；unknown tool/参数/输出大小检查；密码材料不回模型，受控加解密有往返与认证失败证据。
- [ ] 固定Provider API/CLI参数，不开放任意脚本或shell；输入/输出、超时与资源范围受控。
- [ ] 超时取消确实kill/wait/清理；所有工具走统一入口、拒绝也审计。
- [ ] 目标2：初版手写Loop，非流式后原生NDJSON，不混用SSE/delta/tool_call_id。
- [ ] 单步/多步/多调用/失败回传、deadline/token/step预算、重复调用熔断。
- [ ] 保存原始Trace并回答五问；流式与非流式遵守相同协议/策略并完成相同任务类型，m1-done。

## M2（60h）

- [ ] 目标3：鉴权、资源归属、POST/chat/files、sessions/runs/events/cancel、live/ready。
- [ ] 流前持久化Run；同client_request_id返回原Run。
- [ ] SSE统一事件envelope，run_id/event_id必带，跨UTF8/CRLF/半帧正常。
- [ ] cancel/detach分开，断线不当作审批，重连不重跑请求。
- [ ] 目标4：Alembic迁移、owner/app/query/audit角色隔离，运行角色不能DDL/改审计。
- [ ] 六个查询可跑；q4从llm_calls实际计量，q6窗口参数化，失败包含timeout。
- [ ] 文件/证书/key元数据按项目与用户隔离；DB/Trace不存私钥或解密文件内容。
- [ ] 短DB事务不跨外部任务；run/user/session一致性检查，重启数据不丢，m2-done。

## M3（70h）

- [ ] 目标5：PDF/MD/TXT真实样本，扫描页需OCR、复杂表格限制记录。
- [ ] chunk有版本/hash/定位/project/ACL，业务chunk_id与Qdrant UUID point_id分开。
- [ ] staging→active索引发布；重复入库、更新/删除、失败恢复一致。
- [ ] dense/sparse/rerank/引用在服务端遵守相同授权。
- [ ] 目标6：dense/BM25/RRF/rerank四组消融，rewrite另开关。
- [ ] ≥50条审定RAG问题，正样本与无答案分开；gold从源文档和多路候选审定。
- [ ] Hit/Recall/MRR/证据覆盖/引用有效与支持/正确拒答/误拒答与n都报告。
- [ ] corpus/index/config冻结，失败用例与延迟分析，m3-done。

## M4（80h）

- [ ] 目标7：ToolSpec与本地policy、密码操作风险、输出schema、幂等retry与预算。
- [ ] ≥50工具用例允许多解，gold_calls按occurrence表达多次调用，单位SI明确。
- [ ] 未授权/参数错误/取消/失败均审计；MCP注解不可自授权。
- [ ] 密码写动作/敏感解密审批绑定规范参数、资源/策略版本；轮换、CSR或测试签发有实际状态断言。
- [ ] 目标8：三Server+Resource+Prompt；stdout协议、stderr日志、canonical ID映射。
- [ ] 已连接Server工具变化刷新；新增授权endpoint热加载另测；不假设自动扫描Server。
- [ ] 目标9：State只存有限摘要/版本化引用，AsyncPostgresSaver迁移setup与锁定graph版本。
- [ ] 动态interrupt用Command(resume)，同pending action恢复不重新改参数。
- [ ] approvals绑定hash/身份/有效期/单次消费；重复/并发approve与拒绝可测。
- [ ] actions账本、幂等键、执行前/中/后崩溃核对；unknown不自动重跑；引入独立worker时补lease/fencing与双worker竞争。
- [ ] 重连恢复待审批，显式cancel，副作用只执行一次或进入明确unknown，m4-done。

## M5（90h）

- [ ] 目标10（20h）：同用户跨session Memory，不同user/project隔离；短显式偏好不误过滤。
- [ ] 改口事务、有效hash唯一索引、语义复核、来源/查看/纠正/删除与投毒防护。
- [ ] 目标11（15h）：4B/9B±router与可选27B，全组相同Judge/config/fixture。
- [ ] 每配置3次，原始结果/方差/区间/质量/延迟/tokens/峰值VRAM与换模成本。
- [ ] 目标12（15h）：必要tool最终状态、事实绑定、单位/派生量、引用存在/定位/支持、unsupported、schema。
- [ ] 已知错误/正确集TPR/FPR，实体错绑/引用版本/合理无引用覆盖；不只查数字集合。
- [ ] 目标13（20h）：100~180审定记录、split分组隔离、无TODO，frozen校验通过。
- [ ] Runner驱动fixture/turn/approve/fault/resume/assert/cleanup，实验+重复namespace隔离Memory。
- [ ] 结果含intent/proposed/executed/denied/retrieval/evidence/claims/states/timing/errors。
- [ ] 普通CI合同/mock与专用GPU评测分开；配对compare按pp并列case回归。
- [ ] 目标14（20h）：注入/SQL/命令/路径/SSRF/泄密/提权、审批重放、跨用户、MCP/Memory投毒。
- [ ] 安全判断区分拒绝尝试与真实执行；实际副作用Unauthorized Action Rate=0，m5-done。

## M6（60h）

- [ ] 目标15（30h）：九UI区块、实时状态、刷新/reconnect/审批/cancel正确。
- [ ] draft token显示未验证；final替换，错误不展示为已验证；安全Markdown渲染。
- [ ] 目标16（15h）：profiles、固定镜像/依赖/model、健康/迁移/volume/网络/日志轮转。
- [ ] API无Docker socket与bootstrap/migration秘密；**Ollama仅监听127.0.0.1**，仅前端/API端口对外。
- [ ] 干净目录安装→迁移→启动→smoke，重启数据不丢。
- [ ] 综合项目（15h）：上传/只读检查/key元数据/加解密审批/执行/轮换与版本验证/UI审计全链路，补证书验证或测试CSR/签发。
- [ ] 故障恢复不静默重复密码动作，版本化来源/审计完整，冻结scenario回归，m6-done。
- [ ] **交付验收**：Windows 浏览器从网络打开前端地址即可复现全链路，Windows 侧零安装。

## 文档配套与完整交付

- [ ] 00每目标表逐行有状态与证据，解释/实现/排错/证据分别检查，未运行不标通过。
- [ ] 07自绘只读/审批/知识三条序列与信任边界图，State/安全边界本人确定。
- [ ] 08接口错误/幂等/分页/鉴权与OpenAPI一致，全栈联调表逐场景通过。
- [ ] 09干净目录复现、DB/文件/index/keystore/checkpoint备份恢复与unknown核对有证据。
- [ ] 四仓库同级并独立固定版本；源码/prefix分离，密码仓库不成为文档子目录。
- [ ] A–J毕业矩阵正常/失败/个人能力齐全；选修不适用有理由，首版缺口未冒充完整版。

## 阶段共同检查

- [ ] 学习者独立解释、改一个需求或修一个缺陷，运行证据可定位。
- [ ] 自己的ADR记录背景/取舍/证据/限制；to-digest有截止时间或已消化。
- [ ] AI改动diff与测试变化经过审查，gold修改有依据并重跑baseline。
- [ ] 未验证/降级/延期明确登记；安全与协议关键契约未留作以后补。

| 日期 | 阶段 | 实际工时 | 缺口/降级 | 对验收的影响 | 补测时间 |
|---|---|---:|---|---|---|
| | | | | | |

毕业A~J：模型、RAG、DB、Tools、MCP、Workflow、Memory、Eval、Security、全栈，每项具备可运行正常与失败证据和独立解释，不能仅凭总Demo运行通过。
