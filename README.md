# 密码工具 Agent 全栈开发学习项目

这是学习文档仓库，应用在同级Agent-development-code实现。每周投入20–25小时，沿最小Agent Demo逐步建设可复用部件。当前密码后端使用已编译的OpenSSL/GmSSL可执行程序，后续将固定调用提取到Python Provider；模型负责理解请求与提议操作，执行器负责授权和真实执行。

## 文档目录

```text
README.md                       项目、环境、协作与通用学习记录
ROADMAP.md                      实现顺序、阶段成果、工时与任务导航
CLI-CRYPTO-REFERENCE.md         OpenSSL/GmSSL 命令、参数与本机验证边界
CLI-OPENSSL-HELP.md              OpenSSL 全部标准命令及摘要/加密别名的帮助索引
CLI-GMSSL-HELP.md                GmSSL 全部子命令的本机帮助与解读
stages/
  V0-ENVIRONMENT.md              环境请求与首测
  V1-CORE-DEMO.md                单工具Agent Demo与核心扩展
  V2-WEB.md                      API、数据库、第一网页
  V3-MCP.md                      封装并接入一个Crypto MCP
  V4-APPROVAL-CRYPTO.md           审批、加解密与恢复
  V5-KNOWLEDGE.md                RAG、Memory、Verifier、SSE
  V6-DELIVERY.md                 完整实验、安全与部署验收
```

先读[Roadmap](ROADMAP.md)确定当前阶段，再打开当前任务文档；常用密码程序操作查[命令行速查](CLI-CRYPTO-REFERENCE.md)，逐条核对帮助查 [OpenSSL](CLI-OPENSSL-HELP.md) 与 [GmSSL](CLI-GMSSL-HELP.md) 目录。每阶段集中写实现目标、学习技术、结果要求、分步任务、必须自己回答的问题和验收。数据库DDL、API合同、密码实践和实验协议分别放进所属阶段。本仓库只保存Markdown；评测数据、schema与校验器由你在代码仓库实现，任务见V6。

**交付阶段只使用 V0–V6。** 阅读和实施均以[Roadmap](ROADMAP.md)中的 V 阶段为准；文内 `T001` 等编号仅用于定位细分任务，不表示另一套阶段。`m1` 等小写名称是代码仓库现有的依赖组名，也不是阶段。

## 开发与同步位置

应用开发、依赖安装、模型/密码工具、前端构建和测试在Ubuntu中进行；Windows浏览器访问网页。文档与代码是独立Git仓库，操作前核对当前路径和未提交修改，提交与推送按用户授权执行。下文命令是学习操作，尚未执行的业务保持未验证。

四仓库必须处于同一父目录：

```text
/home/zsw/work/agent_development/
├── Agent-development-doc/
├── Agent-development-code/
├── openssl/
└── GmSSL/
```

OpenSSL与GmSSL是独立源码仓库，与文档目录同级；源码、构建目录和安装prefix分别记录，可选GmSSL-Python也放同级。不在文档仓库放密钥、解密产物、真实工作资料或模型权重。

## 当前实现与后续接入

2026年10月13日迁移后核对：最小Demo的有限Loop与终端交互位于`packages/app/agent.py`；模型请求位于`packages/llm/client.py`，工具参数校验与MCP调用位于`tools/`，MCP客户端与Crypto服务位于`mcp_integration/`，现有SM2可执行程序调用与教学密钥管理位于`packages/crypto/`。SM2密钥生成、签名和验签仍是当前已有功能，后续直接在这些模块完善。

`packages.app run`已调用`packages.app.agent.run`执行一轮请求；交互入口使用同一Loop完成多轮会话。正式登记、授权、审批、Graph与恢复等部件仍有待实现骨架，现有Demo不自动签收V1–V4的完整要求。

实际代码目录、功能状态与运行命令统一见[代码仓库README](../Agent-development-code/README.md)，目录契约在[代码仓库scripts/layout.json](../Agent-development-code/scripts/layout.json)。代码仓库已移除`docs/`；环境、阶段学习与本人决策记录放在本学习文档仓库的现有文件中。

未验证环境先按[V0](stages/V0-ENVIRONMENT.md)核对，再对照[V1摘要Demo与核心扩展](stages/V1-CORE-DEMO.md#first-demo)补齐相应能力。已有Demo代码、配置与uv.lock先检查再复用，不覆盖未提交成果。同步仓库时先看`git status`，工作区干净再快进拉取；有本地修改时先保留并处理冲突。

## README页内阅读入口

- [Ubuntu与目录](#env-0)：四仓库、用户权限、开发位置。
- [Python与虚拟环境](#env-2)、[Ollama请求环境](#env-3)：V0最先核对。
- [版本与环境记录](#env-8)：历史快照与本人重新验证。
- [AI协作与本人必须完成的内容](#ai-assistance)。
- [任务卡与检查记录](#study-共用任务卡与记录)、[卡住时怎么排错](#study-卡住时先检查什么)。

## 环境如何分阶段启用

| 阶段 | 需要的环境 | 验证到什么程度 |
|---|---|---|
| V0与第一个Demo | Ubuntu、Git、Python3.12/uv/venv、Ollama与一个模型、OpenSSL CLI | 新终端定位同一解释器；真实模型请求、固定摘要与首测可核对 |
| V1扩展 | 已编译的OpenSSL/GmSSL CLI、Python Provider、pytest/httpx/Pydantic | 能力探测、独立向量与错误分类；未支持不伪装成功 |
| V2 | PostgreSQL/Alembic、FastAPI、Node/pnpm/React；Docker按服务方式引入 | 教学身份/上传/JSON请求/快照、迁移与浏览器访问真实通过 |
| V3 | 单Crypto MCP Server与锁定SDK | 固定授权连接、list/call、直调对照；不一次启动三个Server |
| V4 | 固定AEAD能力、受控keystore、Graph与持久checkpoint | 审批绑定、账本、产物与崩溃核对；不能只验证库导入 |
| V5 | 语料/索引、BM25/向量/重排所需依赖、可选PyTorch/GPU、SSE | 真实引用/授权检索、指标、Memory纠正与事件重连 |
| V6 | 锁定完整模型矩阵、Scenario Runner、部署profiles与备份工具 | 干净目录重建、完整回归、恢复与运行限制可复现 |

下面的已知版本是带日期的历史快照，开始学习时由你重新检查并保存实际输出。不要为了做第一个Demo先安装所有模型、数据库和向量服务。


<a id="env-0"></a>
<a id="env-0-0-决策全部在-ubuntu-内实现windows-只作浏览器客户端"></a>
### 决策：全部在 Ubuntu 内实现，Windows 只作浏览器客户端

**结论：仓库、Ollama、Docker、数据库、向量库、API、前端全部运行在 Ubuntu 内；
Windows 不承担任何实现角色，只通过浏览器从网络访问前端页面。**

本机 Ubuntu 是 WSL2 里的 Ubuntu-22.04.5（内核 `6.6.87.2-microsoft-standard-WSL2`），
但它对项目而言就是**一台 Linux 主机**：所有进程、文件、容器、GPU 访问都在它内部完成。
除「用浏览器打开页面」以外，本指南不包含任何 Windows 侧的实现步骤。

本项目采用单台 Ubuntu 主机，减少跨主机配置，便于从开发环境逐步学习到部署。密码工具始终由受控适配层调用，应用进程、数据和库安装路径明确分开。

历史实测依据（2026年10月10日记录，开始时由本人重新核对）：

| 项 | 实测值 | 含义 |
|---|---|---|
| 发行版 | Ubuntu 22.04.5 LTS（WSL2） | 可用 |
| Ubuntu 内 Docker | **原生 29.1.3**，`/var/run/docker.sock` | 无需 Docker Desktop |
| Docker 能力 | `overlay2` + cgroup v2 + seccomp | 可用于服务容器；应用隔离仍需实测 |
| Ubuntu 内 GPU | `nvidia-smi` 可见 RTX 5060 Ti，驱动 591.86 | GPU 直通已生效 |
| Ubuntu 内 Ollama | **0.32.15，systemd 服务 enabled 且运行中** | 已是 Ubuntu 服务 |
| uv | `~/.local/bin/uv`，0.11.12 | 已装 |
| Ubuntu 内 Node | v22.23.2 + pnpm 12.3.4 | V2基础前端可用，开始时重新核对 |
| 磁盘 | `/` 1007 GB，可用 750 GB | 充足 |
| Ubuntu 用户 | `zsw`（非 root） | 符合最小权限 |


<a id="env-0-01-仓库放在-ubuntu-的文件系统上"></a>
#### 仓库放在 Ubuntu 的文件系统上

文档、实现和两个密码库源码仓库同级摆放在 `/home/zsw/work/agent_development/`：

```
/home/zsw/work/agent_development/
├── Agent-development-doc/     ← 指南（静态 Markdown）
├── Agent-development-code/    ← 实现仓库
├── openssl/                   ← OpenSSL 官方源码仓库
└── GmSSL/                     ← GmSSL 官方源码仓库
```

同级是硬要求：指南里的 `../Agent-development-code/` 相对链接否则会断。

两个密码库同样直接放在上述父目录，不嵌套在文档、实现或`_deps`中；目录大小写固定为`openssl`、`GmSSL`。
各仓库独立管理版本。编译安装使用单独受控前缀，不能把源码位置当作运行时已安装路径。
如需克隆GmSSL-Python绑定源码，也放在此父目录同级。本段是后续目录约定，不声明这些源码已准备完成。

**不要**把实现仓库放到 `/mnt/c`、`/mnt/d` 这类 Windows 挂载点：它们走 9P 协议，
venv、node_modules 这种大量小文件操作会慢数倍。实现仓库必须在 Ubuntu 的 ext4 上。


<a id="env-0-02-ollama-与应用的连接"></a>
#### Ollama 与应用的连接

Ollama 使用 Ubuntu 内的 systemd 服务，应用连接 `http://127.0.0.1:11434`。模型服务不对浏览器或外部网络直接开放；容器访问宿主服务按第5节的实际网络路线配置。


<a id="env-0-03-环境改变的纪律"></a>
#### 环境改变的纪律

环境变更后必须新建实验，不修改旧结果（§8）。上面每一项数值都要能被
`environment.lock.json` 复现；对不上的值以 lock 文件为准。

<a id="env-1"></a>
<a id="env-1-1-分阶段引入"></a>
### 分阶段引入

| 交付阶段 | 本次引入/核对 | 可后置 |
|---|---|---|
| V0 | Git/Python3.12/uv/Ollama/4B、配置首测 | Node构建、DB、9B、向量库 |
| V1 | 只读OpenSSL/GmSSL适配、受控资源/超时、httpx/测试 | 受控AEAD练习到V4 |
| V2 | Ubuntu Docker/Compose、PostgreSQL/Alembic、Node/pnpm、API与React小页 | SSE/六查询/完整前端专项 |
| V3 | 锁定MCP SDK，一个stdio Crypto Server与Client | 三Server、Resource/Prompt、新端点到V6 |
| V4 | 教学keystore/profile、动作账本、Graph saver、审批/产物 | RAG、worker/队列按需后置 |
| V5 | Qdrant/embed、reranker按需、Memory表、SSE | 9B/正式实验到V6 |
| V6 | 9B/固定Judge、三职责MCP、完整部署/恢复；选修worker | 27B、WebSocket、HSM/KMS、多Agent |

按[Roadmap](ROADMAP.md)分配，不把目标编号或M依赖组名当新阶段。第一前端在V2构建运行；模型/Provider/网络与权限先验证再升级。

Ubuntu宿主与容器使用各自可达地址，按第5节选定host或bridge路线。宿主不要直接使用仅容器可解析的postgres/qdrant服务名，容器127.0.0.1也不是宿主Ollama。

<a id="env-2"></a>
<a id="env-2-2-python-与目录"></a>
### Python 与目录

指南与实现仓库都在 `/home/zsw/work/agent_development/`（同级）。命令从应用根目录运行。

**Ubuntu 系统自带 Python 3.10.12，不满足项目的 3.12 要求。用 uv 提供，不要 `apt install`**
（Ubuntu 22.04 默认源没有 3.12，加 deadsnakes PPA 会污染系统环境）：

```bash
# Ubuntu 内执行，工作目录 = 实现仓库根
uv venv --python 3.12 .venv          # uv 自动下载 cpython-3.12，无需 root
source .venv/bin/activate
python -c "import sys; print(sys.executable, sys.prefix)"   # 必须指向 .venv
```

先创建合法 pyproject（至少 name/version/requires-python），按里程碑加入依赖；
提交 uv.lock，正式启动 `uv sync --frozen`。开发依赖 pytest/pytest-asyncio/ruff/mypy；
V1 加 pydantic/httpx/pydantic-settings，V2 加 fastapi/uvicorn/sqlalchemy/asyncpg/alembic，
V5 再加 qdrant-client/pymupdf/BM25/分词器，V4 按需加 langgraph/checkpoint-postgres；当前Demo所用的MCP已在基础依赖中。实际安装时仍按代码仓库现有的 `m1`/`m2` 等 extra 名称选择依赖。
不能靠无上界的最低版本声明保证 API 稳定，实际版本锁定后保存兼容 smoke Trace。

> 应用仓库已按上述分组写好 `pyproject.toml`（`m1`/`m2`/`m3`/`m4`/`mcp`/`workflow`/`ml`/`dev` extras），
> 并带有纯标准库的自检脚本 `scripts/selftest.py`（校验目录布局、`.env.example` 与
> `Settings` 字段双向一致、密钥扫描、分层反向依赖）。**在 `uv sync` 之前就能跑**。

<a id="env-3"></a>
<a id="env-3-3-ollamaubuntu-内-systemd-服务"></a>
### Ollama（Ubuntu 内 systemd 服务）

Ollama作为Ubuntu内的系统服务运行，检查方式：

```bash
# 状态与版本
systemctl status ollama --no-pager
ollama --version                     # 实测 0.32.15
curl -s http://127.0.0.1:11434/api/version

# 模型
ollama list
ollama pull qwen3.5:4b               # V0 唯一必需模型；仅缺失时拉取
ollama run qwen3.5:4b "用一句话说明工具调用"
ollama ps
```

模型文件在 `/usr/share/ollama/.ollama/models`（当前 20 GB）。V5 引入检索时拉 bge-m3，
V6 模型对照时按需拉 qwen3.5:9b。模型名可变，实验记录实际 digest、量化、template、上下文参数；
权重体积不能直接当推理峰值显存。

`qwen3.5:4b` 要求 Ollama ≥ 0.30.0（本机 0.32.15 满足）。它是**统一多模态**模型
（文本 + 图像输入，256K 上下文，原生支持 tools 与 thinking），因此不需要再单独部署
视觉模型。出厂采样参数为 `temperature=1 / top_p=0.95 / top_k=20 / presence_penalty=1.5`，
必须原样记录，并与消融实验的配置分开报告。

Ollama 的服务参数通过 systemd override 设置，不用 Windows 环境变量：

```bash
sudo systemctl edit ollama
# 在 [Service] 段加入，然后 sudo systemctl restart ollama
#   Environment="OLLAMA_MAX_LOADED_MODELS=1"
#   Environment="OLLAMA_NUM_PARALLEL=1"
#   Environment="OLLAMA_KEEP_ALIVE=5m"
#   Environment="OLLAMA_FLASH_ATTENTION=1"
```

| 变量 | 起点 | 注意 |
|---|---|---|
| OLLAMA_HOST | 127.0.0.1:11434 | **默认仅本机即可**，不要为了容器改成 0.0.0.0（§5） |
| OLLAMA_MODELS | /usr/share/ollama/.ollama/models | 按磁盘空间选择 |
| OLLAMA_MAX_LOADED_MODELS | 1 | 限 Ollama 管理的模型，不限制 PyTorch |
| OLLAMA_NUM_PARALLEL | 1 | baseline 固定串行 |
| OLLAMA_KEEP_ALIVE | 5m | embedding 与 controller 切换可能导致重复加载 |
| OLLAMA_FLASH_ATTENTION | 1 | 核对实际版本支持 |
| OLLAMA_KV_CACHE_TYPE | q8_0 | 和上下文长度一起固定与记录 |

如果全部 embedding/controller 共用单模型槽，不声称两者都处于 warm 状态。可选择 CPU embedding、单独部署、预计算用于检索质量实验，或接受换模并计入端到端延迟。生成与 Judge 分批运行，避免每题来回换模型。

原生 `/api/chat` 的流是 NDJSON；应用 `/chat` 给前端的流是 SSE，两层分别适配。[Ollama streaming](https://docs.ollama.com/api/streaming)、[tool calling](https://docs.ollama.com/capabilities/tool-calling)

<a id="env-7"></a>
<a id="env-7-7-密码-provider-与资源边界"></a>
### 密码 Provider 与资源边界

OpenSSL/GmSSL源码仓库与文档同级，当前运行路线采用已编译的CLI及受控程序路径。`packages/crypto/providers/openssl_cli.py`与`gmssl_cli.py`负责封装固定调用，MCP工具调用对应Python函数；每次实际计算仍由Provider执行可执行程序。记录二进制位置、版本与能力，不依据源码目录存在认定能力已可用。Python库/绑定属于后续可选替代路线，采用时再记录相应包与后端版本。

固定 API 或参数数组调用 Provider，限制输入大小、超时和输出。模型只提交获授权的 file_id/certificate_id/key_id；服务端解析真实位置，密钥与解密明文不进入模型。算法不支持时明确拒绝，不静默切换为其他模式。

安装与能力验证任务见 [Provider 入门练习](stages/V1-CORE-DEMO.md#provider-practice-10-后续可以照着操作的-provider-入门练习)，加解密、签名、证书与密钥掌握标准见同文件第3、5、6节。

<a id="env-8"></a>
<a id="env-8-8-环境记录与待验证项"></a>
### 环境记录与待验证项


<a id="env-8-81-项目环境记录"></a>
#### 项目环境记录

以下记录来自2026年10月10日的只读检查，供V0确定起点。开始学习时重新运行对应检查，记录当次版本与结果，不用记录表代替实际验收。

| 项目 | 已记录的状态 | 后续检查 |
|---|---|---|
| Ubuntu | Ubuntu 22.04.5 LTS，用户zsw | 当前发行版、用户、工作目录 |
| Python | 系统3.10.12；项目venv为3.12.13 | 新终端解释器与依赖锁 |
| Ollama | Ubuntu内服务，模型列表已有qwen3.5:4b | version、digest与真实请求 |
| 模型配置 | `.env.example`为127.0.0.1:11434和qwen3.5:4b | 当前Settings与本地配置一致 |
| OpenSSL CLI | 3.0.2 | 路径、实际版本、帮助与smoke |
| Python密码后端（可选扩展） | 尚未验证 | 采用库路线时再记录包与实际后端版本 |
| GmSSL | 尚未验证 | 编译后的CLI路径、版本与能力清单；采用绑定时另行记录 |
| 项目基础 | 已有core配置与模型骨架；检查时无uv.lock和工具/Loop测试 | 按P0任务补依赖锁和首个测试 |
| Compose与应用运行 | 本轮未作运行验证 | 插件、迁移、服务readiness与应用smoke |


<a id="env-8-82-模型与资源记录"></a>
#### 模型与资源记录

V0只需qwen3.5:4b；9B在V6模型比较前准备。Embedding到V5引入，reranker按消融需求准备，27B属于可选配置。每次实验保存实际model digest、推理配置、空闲/峰值显存、冷/热加载状态，下载体积不能直接当显存占用。


<a id="env-8-83-环境验收记录方式"></a>
#### 环境验收记录方式

在本README的环境记录中按日期追加当次版本、命令摘要、证据位置、未验证项和必要降级说明，保留旧快照的日期。原始输出留在代码仓库受控本地数据目录，文档只引用脱敏证据。`scripts/selftest.py`读取`scripts/layout.json`并核对代码README、配置和分层。出现差异时先核对实际环境，再更新说明。学习从[V0环境检查](stages/V0-ENVIRONMENT.md#v0-01-检查已有环境)开始。

<a id="contract-8"></a>
<a id="contract-8-8-配置与持续检查"></a>
### 配置与持续检查

干净目录复现、服务依赖、备份/keystore恢复与毕业证据见[交付验收](stages/V6-DELIVERY.md#delivery-1)。V2阶段DDL为参考设计，文档静态检查不等于PostgreSQL实际迁移与权限已验收。

`.env.example` 至少：APP_ENV、API_KEY_HEADER、OLLAMA_BASE_URL、模型名、LLM_THINK、LLM_NUM_CTX、LLM_TIMEOUT_S、DATABASE_URL(app_user)、QUERY_DATABASE_URL(query_reader)、AUDIT_DATABASE_URL(audit_writer)、MIGRATION_DATABASE_URL（仅迁移）、QDRANT_URL、项目空间/collection、可选 Redis/存储 URL、路径roots、密码Provider/keystore配置、受信任 MCP endpoints、EVAL_CONCURRENCY=1。

app API/worker 不加载 migration/bootstrap 密钥；不把完整 OLLAMA_* 环境或配置秘密写进日志。存储roots按knowledge/业务上传/artifact/keystore分别声明；每次核对用户与项目ACL。keystore只供受控密码服务加载，不能作为通用读取root；明文和私钥不写入messages、State、Trace或工具结果。

RetrievalConfig 包含 dense/sparse/backend/fusion/rrf_k/rerank/top_k/query_rewrite/filters，JSON 写入 agent_runs.runtime_config 和 eval_runs.config；prompt_version 只存 prompt 版本字符串。模型实际计量写 llm_calls。

CI 分层：普通 CI 执行 lint/typecheck/合同/schema/mock 场景；专用本机 GPU job 跑冻结集、固定环境和版本对比，按变更范围与发布节奏执行。安全确定性回归每次相关变更必跑，LLM 全量评测不假设托管 runner 有 GPU。阈值使用 pp 和相同 snapshot；报告完整 case failures，不能仅比总体平均。

<a id="ai-assistance"></a>
<a id="ai-assistance-ai协作与个人能力验收"></a>
### AI协作与个人能力验收

> 本项目同时验收系统行为与学习者能力。AI可以提方案、写样板、查文档、审查与补充测试；最终选择、gold审定和能力解释由学习者负责。本文件不禁止正常求助，也不要求故意踩已知的坑。


<a id="ai-assistance-1-使用原则"></a>
#### 使用原则

1. 先明确输入/输出、边界、权威契约和成功条件，再请AI实现或审查。
2. 用实际运行、diff与失败场景验收，不把“应该能跑”当证据。
3. 测试与gold独立审定；AI同时生成实现/测试可能同错，增加独立fixture或反例。
4. AI可以指出测试本身错误；修改错误断言需要说明依据、审查并重跑baseline，不能为了通过模型结果放宽gold。
5. 核心学习逻辑先独立尝试，再让AI审查/解释；无法理解的内容进to-digest，按阶段消化。


<a id="ai-assistance-2-16个目标的分工"></a>
#### 16个目标的分工

| 目标 | AI可协助 | 学习者必须掌握/独立验收 |
|---|---|---|
| 1 Python Tool | 模型、日志、异常包装 | 超时清理、路径/资源权限、安全执行 |
| 2 手写Loop | 协议查证、失败反例、审查 | 初版Loop、回传、预算、原生NDJSON |
| 3 API | 路由、OpenAPI、前端调用例子 | Run生命周期、鉴权、SSE重连 |
| 4 PostgreSQL | DDL/migration/repository样板 | 权限、事务边界、6查询与动作一致性 |
| 5 RAG | parser/client适配 | 版本、定位、授权、入库失败行为 |
| 6 高级RAG | BM25/RRF/reranker适配 | gold审定、正确指标、消融设计 |
| 7 Tools | 注册表/schema | 描述、能力范围、幂等与预算 |
| 8 MCP | Server/client样板、排错 | Server信任、通知刷新、风险映射 |
| 9 Graph | 节点/边/checkpointer适配 | State、审批hash、未知结果恢复 |
| 10 Memory | 提取/去重候选实现 | 用户/项目边界、改口、删除与来源 |
| 11 小模型 | router和报告代码 | 固定变量、heldout隔离、结论限制 |
| 12 Verifier | 审查本人写的检查与测试、解释误判 | 事实绑定、派生量、误报漏报判定 |
| 13 Eval | Runner/validator/compare样板 | 成功谓词、场景与人工gold审定 |
| 14 Security | 审查本人确定的威胁模型与测试 | 策略、授权、实际副作用断言 |
| 15 前端 | 页面与状态展示 | 审批/断线/草稿最终答案行为验收 |
| 16 部署 | Compose/镜像配置 | 干净环境启动、权限与持久化 |

初版手写Loop、Verifier检查逻辑与对抗性测试、个人决策记录由学习者独立编写，AI只审查；安全判断与状态机由学习者定边界。其他模块可让AI协助样板实现，但必须能独立解释、改需求和排错。安全测试由学习者按实际攻击面自行设计，不能将未审定样本标为人工验证。协作细则见实现仓库[AGENTS.md](../Agent-development-code/AGENTS.md)。


<a id="ai-assistance-3-接受修改前的检查"></a>
#### 接受修改前的检查

- 能画出数据和控制流，指出安全/资源/性能假设。
- 能构造正常与失败输入，并说明失败后恢复行为。
- 能解释为何选此设计，哪些边界尚未覆盖。
- 能在不依赖AI完整代写的情况下完成一个需求变化或缺陷修复。

不要求独立重写全部第三方库和所有前端样板。to-digest为空可能表示已经理解，并不证明自欺；一直增长则需要安排消化。


<a id="ai-assistance-4-每轮工作流"></a>
#### 每轮工作流

学习者定义任务与权威接口 → 独立确定关键成功条件/fixture → AI协助实现或审查 → 实际运行 → 审查diff与测试改动 → 相关回归 → 记录自己的选择与证据。已有正确测试保持，新的修订有理由；不强制每次diff都包含测试文件。

默认先用非流式Trace验证Ollama报文，不围绕错误的tool_call_id/arguments字符串假设写测试。工具、资源与审批验收按本项目契约核对。


<a id="ai-assistance-5-可直接使用的审查提示"></a>
#### 可直接使用的审查提示

```text
这是我的接口、实现和验收。请引用位置回答：
1. 未知工具、非法参数、越权资源和超时如何处理？
2. 动作已完成但结果未提交时崩溃，恢复会不会重复副作用？
3. 审批是否绑定当前规范参数与资源版本？
4. 哪个测试可能与实现一起错，缺什么独立证据？
5. 哪些指标/成功谓词不能证明我声称的能力？
先指出问题与可复现输入，不直接重写整个模块。
```

```text
请用我的运行Trace逐条核对验收。
对满足/部分满足/未满足给出证据与缺口；
缺少运行证据时标“未验证”，不要把静态审查称作实测。
```


<a id="ai-assistance-6-评测与秘密"></a>
#### 评测与秘密

dev问题可提供给AI调参，heldout test/gold不进入few-shot或反复调Prompt。AI可以检查Schema/报告结构；正式gold来源需要人核对文档/数据。成功条件改变即新数据版本并重跑baseline，禁止修改旧报告。

仅提供任务必要上下文，秘密用脱敏样例，`.env`与生产凭据不作为排错材料。模型强弱分工按验证结果，不承诺“本地27B审查一定可靠”或“AI提升三倍”等未经测量结论。

每阶段留一次独立练习：解释关键决策、修复注入缺陷、改变一个需求并验证。通过运行与独立能力两道检查再勾选 [技术专项清单](ROADMAP.md#task-index)。


<a id="ai-assistance-7-用主路径表验收ai协助结果"></a>
#### 用主路径表验收AI协助结果

每次协助只针对当前目标一条可验收任务，提供相关契约和必要脱敏上下文。让AI指出依据与缺口，再由本人实际运行。各阶段的“能解释/独立做到/排错/证据”都通过才能标已掌握；当前阶段的执行步骤、本文件的设计问题、API参考的接口和V6交付章节的证据卡共同定位。

样板可由AI协助；本人至少改变一条需求并验证。Loop、Verifier核心与对抗测试、个人ADR仅允许审查，不请AI生成完整答案。安全/State边界本人确定后再审查，不因已有示意图就省略自己的设计。


<a id="ai-assistance-8-按交付切片请求协助"></a>
#### 按交付切片请求协助

每次说明当前V、目标编号、稳定任务ID、本切片范围、正常/失败条件与已有证据。V2只读网页协助无需假定审批/RAG已完成；V3单Server不生成全套工具平台；V4开放写动作的安全/恢复边界不得延期。后续回来补齐原掌握标准，不能以切片通过把整目标标毕业。

AI协助分工与16目标表保持，核心Loop、Verifier/对抗测试、个人ADR仍仅审查，State/安全判断本人设计。基础网页提前不降低目标15的独立理解要求；样板之后本人改一项交互并定位异步失败。

<a id="crypto-3.0"></a>
<a id="crypto-3.0-30-密码库源码仓库的位置"></a>
#### 密码库源码仓库的位置

OpenSSL与GmSSL必须放在同一个父目录下，与本文档仓库、Agent实现仓库彼此同级：

```text
/home/zsw/work/agent_development/
├── Agent-development-doc/
├── Agent-development-code/
├── openssl/
└── GmSSL/
```

目录名按上面的大小写固定，不使用`Agent-development-code/openssl`、`Agent-development-doc/GmSSL`或`_deps/GmSSL`。两个密码库独立管理版本，源码位置与编译安装前缀分开记录；这不要求替换系统已有OpenSSL。如果后续另行克隆GmSSL-Python源码，使用同级的`GmSSL-Python/`。V0核对位置并登记是否已准备；按实际Provider需要在V1/V4准备和锁定源码版本，不因安装第二库所有能力而延迟只读闭环。

<a id="study-学到什么程度才算完成"></a>
<a id="study-学到什么程度才算完成-学到什么程度才算完成"></a>
### 学到什么程度才算完成

每个目标通过四道检查；读过教程、照抄后运行、AI声称正确，都不能单独算掌握。允许查官方文档与API签名，不要求背诵整个框架。

| 维度 | 完成标准 | 未完成的典型表现 |
|---|---|---|
| 能解释 | 自己画输入输出、数据流、控制流与信任边界，说明选择理由 | 只知道名称，不知失败后状态在哪 |
| 能实现 | 根据契约做最小功能，再独立修改一条需求 | 只能运行完整示例，加字段就要全部代写 |
| 能排错 | 用Trace、DB与真实资源定位相关失败，修复后回归 | 只改prompt或反复重启等待偶然成功 |
| 有证据 | 命令、版本、输入来源、预期、实际结果、case/run可定位 | 只有成功截图，没有原始记录和失败 |

下文表格的“独立做到”和“排错与边界”均为必修深度；后置列不影响当前阶段。初版手写Loop、Verifier核心检查与对抗性测试、个人ADR由学习者独立编写，AI仅审查，细则见[04](README.md#ai-assistance)。每项记录“待学/在做/已验证/有缺口”，系统行为和个人理解分别验收。关键授权、协议、恢复不能延期；缺少真实证据写未验证。

<a id="study-共用任务卡与记录"></a>
<a id="study-共用任务卡与记录-共用任务卡与记录"></a>
### 共用任务卡与记录


<a id="study-共用任务卡与记录-一次任务只写一张卡"></a>
#### 一次任务只写一张卡

在当前阶段文档末尾追加“本人学习记录”，自己记录以下字段；环境版本记录追加在本README的环境记录中。任务卡模板不是应用已实现接口，也不是正式评测schema，不需要在代码仓库另建文档目录。

| 字段 | 要写的内容 |
|---|---|
| 任务 | 如 T002，解析公开测试证书 |
| 要解决的问题 | 当前系统缺什么能力，谁会使用 |
| 先学内容 | 本次真正需要的 2–4 个概念和参考资料 |
| 掌握标准与进度 | 对应本阶段表中的技术行；逐项记“待学 / 在做 / 已验证”，补上能解释、独立实现和排错的证据 |
| 输入 | certificate_id、测试资源、身份与时钟等 |
| 输出 | 必要字段、状态和 artifact，不包含秘密 |
| 成功条件 | 可以独立运行并核对的断言 |
| 失败条件 | 与本次范围相关的非法输入或异常 |
| 实际证据 | 命令、结果/Trace 路径、git commit、测试位置 |
| 独立理解 | 输入/输出/授权/状态/恢复怎样工作 |
| 实际工时与下一步 | 花了多久、卡点、下次先做哪一步 |


<a id="study-共用任务卡与记录-完成与进入下一阶段的规则"></a>
#### 完成与进入下一阶段的规则

| 类型 | 处理方式 |
|---|---|
| 确定性密码/权限/状态错误 | 修复并重跑相关验证，不能靠总体平均率盖过去 |
| 协议与结构检查失败 | 修接口或解析器，保持原正确断言 |
| 模型质量不够 | 分析失败类型，在 dev 小步改进并记录 baseline |
| 无实际运行证据 | 记为未验证，不勾完成 |
| 选修或超范围能力 | 登记扩展清单，不阻塞当前最小闭环 |
| 未理解代码 | 记入当前阶段文末的本人学习记录，关键安全/协议内容阶段内消化 |

每个阶段末在同一学习记录中自己写简短决策，说明选择、证据、限制和重审条件。实现仓库[AGENTS.md](../Agent-development-code/AGENTS.md)的手写Loop、Verifier、安全判断与个人决策边界在后续代码任务中适用；独立编写要求在对应实现阶段执行。


<a id="study-共用任务卡与记录-相关检查入口"></a>
#### 相关检查入口

文档以Markdown阅读和维护，提交前核对目录、链接、表格、技术标准与阶段任务。应用检查在代码仓库、对应依赖已安装后运行：

```bash
cd /home/zsw/work/agent_development/Agent-development-code
source .venv/bin/activate
python3 scripts/selftest.py
python -m pytest -q
python -m ruff check .
python -m mypy packages/
```

类型检查范围随着合法包布局调整。mock、单元/合同、安全确定性检查与真实 Ollama/GPU 评测分开记录。文档完整不等于应用完成，实际业务由运行与独立验证证据签收。

<a id="study-阶段共同检查"></a>
<a id="study-阶段共同检查-阶段共同检查"></a>
### 阶段共同检查

- [ ] 学习者独立解释、改一个需求或修一个缺陷，运行证据可定位。
- [ ] 自己的ADR记录背景/取舍/证据/限制；to-digest有截止时间或已消化。
- [ ] AI改动diff与测试变化经过审查，gold修改有依据并重跑baseline。
- [ ] 未验证/降级/延期明确登记；安全与协议关键契约未留作以后补。

| 日期 | 阶段 | 实际工时 | 缺口/降级 | 对验收的影响 | 补测时间 |
|---|---|---:|---|---|---|
| | | | | | |

毕业A~J：模型、RAG、DB、Tools、MCP、Workflow、Memory、Eval、Security、全栈，每项具备可运行正常与失败证据和独立解释，不能仅凭总Demo运行通过。

<a id="study-卡住时先检查什么"></a>
<a id="study-卡住时先检查什么-卡住时先检查什么"></a>
### 卡住时先检查什么

| 现象 | 先检查 | 下一步 |
|---|---|---|
| Python import 失败 | 解释器路径、已安装 extras、当前目录 | 补本阶段依赖，确认真实包名和导入来源 |
| pytest 没测试 | test 文件名、testpaths、是否真写了断言 | 写首个可执行测试，不把 exit code 5 当成功 |
| Ollama 连接失败 | service、11434、回环地址与日志 | 修服务或配置，不迁回 Windows |
| 工具一直不选 | 原始 schema、实际 tool_calls、问题是否需工具 | 一次只暴露一个只读工具，先验证协议 |
| 工具参数错误 | required/default/type、资源 ID 与模型说明 | 执行前拒绝；缺参数时澄清 |
| 密文无法解密 | key/version、nonce、AAD、tag、格式版本 | 核对独立工具结果，不让模型猜密钥 |
| GmSSL 导入错误 | C 共享库、绑定来源/版本、加载路径 | 用官方安装说明定位，不混装同名包 |
| 证书验证不一致 | 信任根、用途、域名、时钟、链与吊销检查范围 | 分项报告 checked/pass/fail/unknown |
| SSE 中文乱码/丢事件 | UTF-8 增量解码、空行组帧、event_id | 用确定性切块输入定位解析器 |
| 恢复重复签发/轮换 | action hash、账本、checkpoint、副作用位置 | 先停写动作，修复核对与幂等再重测 |
| RAG 回答胡编 | 检索证据、版本、定位和事实槽 | 无证据明确不足，不扩大授权补召回 |
| 前端说成功但资源没变 | API snapshot、工具结果与 Verifier | 页面展示真实服务端状态 |

一次卡住先缩小到“一个输入、一个工具、一个预期结果”。保存最小复现、实际报文、版本和已尝试步骤，再请 AI 审查。不要一次贴整个项目让 AI 重写。

<a id="study-初学者术语速查与资料使用"></a>
<a id="study-初学者术语速查与资料使用-初学者术语速查与资料使用"></a>
### 初学者术语速查与资料使用

先理解它在当前任务里解决什么，再查官方API；主路径必修深度就是当前停止条件，不要求学完每个库。

| 术语 | 在项目里的具体含义 | 首次学习 |
|---|---|---|
| Schema / Pydantic | 规定输入输出字段、类型、默认与错误；不代替权限 | 目标1 |
| async / await / cancel | 并发等待I/O与协作取消；外部进程还需清理 | 目标1 |
| Provider | 固定库或CLI的适配层，负责真实密码结果 | 目标1 |
| Tool / ToolCall / ToolResult | 能力定义、一次提议/调用、实际结果 | 目标1–2 |
| Agent / Loop | 观察需求和结果，有限提议/执行/反馈直到停止 | 目标2 |
| Context / token | 一轮模型输入与长度计量，含预算和输出预留 | 目标2 |
| NDJSON / SSE | 模型原生JSON行流、浏览器业务事件流 | 目标2–3 |
| Run / Step / Action | 一次任务、内部步骤、绑定参数与资源的动作 | 目标2–4、7 |
| API / DI / RBAC | HTTP入口、依赖注入、按角色权限；还需资源归属 | 目标3 |
| Idempotency | 重复请求对应同一动作/结果，不能靠模型保证 | 目标3、7 |
| Migration / Transaction | 数据结构升级、短原子状态写入 | 目标4 |
| RAG / chunk / embedding | 授权资料检索辅助回答、证据片段、向量表示 | 目标5 |
| Manifest / Citation | 固定资料索引版本清单、答案来源与定位 | 目标5 |
| BM25 / RRF / rerank | 词项检索、排名融合、候选重新排序 | 目标6 |
| MCP / registry bridge | 工具互操作协议、外部名称到本地策略映射 | 目标8 |
| Graph / State / checkpoint | 节点控制流、当前任务状态、持久暂停/恢复点 | 目标9 |
| interrupt / reconciliation | 等人工决定、核对不确定外部执行状态 | 目标9 |
| Memory | 有来源且可纠正删除的长期用户上下文 | 目标10 |
| Router / ablation | 缩小候选路线/工具、一次只改变一个变量的实验 | 目标11 |
| Claim / Evidence / Verifier | 原子事实、实际来源、结构/状态/事实/引用检查 | 目标12 |
| Fixture / gold / frozen | 受控测试材料、人工期望、不可静默改动的版本 | 目标13 |
| Scenario / heldout | 多轮及故障场景、不参与调参的测试数据 | 目标13 |
| Prompt injection | 不可信文本试图改变运行规则；最终防线是执行授权 | 目标14 |
| Snapshot / event_id | 当前服务器状态、持久事件游标，用于前端恢复 | 目标15 |
| Ready / volume / runbook | 依赖可用、持久数据、真实可执行操作指南 | 目标16 |

资料使用：环境在README，Provider实践在V1，MCP在V3，审批/Graph在V4，检索/引用/SSE在V5，API/React在V2，实验/部署在V6。每次只读当前概念相关段落，做一个输入输出实验，再回表格验收。已有日期快照与模型标签开发时重新核对，固定实际版本后再比较，不盲目追新。


<a id="starting-snapshot"></a>
<a id="starting-snapshot-真实起点与操作约定"></a>
### 真实起点与操作约定


<a id="starting-snapshot-2026-年-10-月-10-日只读核对结果"></a>
#### 2026年10月10日只读核对结果（历史快照）

| 项目 | 核对到的状态 | 下一步 |
|---|---|---|
| Ubuntu 文档仓库 | `/home/zsw/work/agent_development/Agent-development-doc` | 后续从此处阅读与修订指南 |
| Ubuntu 实现仓库 | 同级 `Agent-development-code`，提交 `242aa44`，工作区干净 | 从骨架开始实现 |
| Ubuntu 系统 Python | 3.10.12 | 不用它安装应用依赖 |
| 项目虚拟环境 | `.venv` 已存在，Python 3.12.13 | 检查依赖、补齐首个测试 |
| Ollama 模型 | 已列出 `qwen3.5:4b` | 做一次真实请求并保存输出 |
| 配置样例 | 已使用 `127.0.0.1:11434` 和 `qwen3.5:4b` | 检查实际 Settings 与本地配置 |
| OpenSSL CLI | 3.0.2 | 固定实际版本，后续检查兼容与更新需求 |
| 实现内容 | core 配置与模型骨架；未发现工具、Loop 或 `test_*.py` 实现 | 骨架齐全不等于阶段完成 |
| 依赖锁 | 核对时未发现 `uv.lock` | V0 生成并核对锁文件 |
| GmSSL | 尚未验证安装状态 | V0 后段或 V1 按选定路线安装验证 |

这是一次起点记录，不代表已经完成 V0。机器状态可能变化，学习开始时按下面命令重新检查。后续以 Ubuntu 工作目录为开发现场。


<a id="starting-snapshot-所有开发命令在-ubuntu-bash-中执行"></a>
#### 所有开发命令在 Ubuntu Bash 中执行

文档默认 Ubuntu 用户为 `zsw`，路径如下。如果换机器或用户名，统一替换父目录，保持文档、实现、OpenSSL和GmSSL四个仓库同级。

```text
/home/zsw/work/agent_development/
  Agent-development-doc/      学习指南与评测规范
  Agent-development-code/     应用实现
  openssl/                    OpenSSL 官方源码仓库
  GmSSL/                      GmSSL 官方源码仓库
```

两个密码库直接位于同一父目录，不放入应用或文档，也不放入`_deps`。Ubuntu目录名区分大小写，统一采用`openssl`、`GmSSL`；各仓库独立锁定commit/tag。源码仓库与安装前缀是不同概念，后续构建安装仍用受控独立前缀。若克隆GmSSL-Python源码，采用同级的`GmSSL-Python/`。源码目录与安装路径在环境记录中分别保存。

应用、Ollama、数据库、向量库、适配层、前端构建和测试全部在 Ubuntu 内执行。Windows 只用于浏览器访问最终页面。实现目录放在 Ubuntu 文件系统，不在 `/mnt/c` 或 `/mnt/d` 上创建应用虚拟环境和 node_modules。

每次新开终端，先执行：

```bash
cd /home/zsw/work/agent_development/Agent-development-code
pwd
git status --short --branch
source .venv/bin/activate
python --version
python -c 'import sys; print(sys.executable)'
```

预期最后一行指向实现仓库的 `.venv/bin/python`，版本为 3.12.x。没有虚拟环境时先做 V0 的环境任务。

已有仓库同步时先看 `git status`，工作区干净再 `git pull --ff-only`。有自己的修改时先决定提交、保留或合并，不执行覆盖式 reset，也不把 clone 命令运行到已存在的目录上。


<a id="starting-snapshot-先理解目录与接口的区别"></a>
#### 先理解目录与接口的区别

当前结构使用`packages/`、`tools/`、`mcp_integration/`等目录，最小Demo已迁入这些模块；完整目录树以[代码README](../Agent-development-code/README.md#目录结构)为准，阶段职责见[V1目录与依赖](stages/V1-CORE-DEMO.md#contract-1)。后续在主项目扩展时同步导入路径、打包配置、代码README、`scripts/layout.json`和`selftest.py`。

特别注意顶级 `mcp/` 目录可能遮蔽第三方 SDK，`agent-api` 也不能直接当 Python 包名导入。落地时选择合法包名并验证 `import` 来源；指南中的业务模块名称表示职责，不保证当前已经存在对应命令入口。


<a id="starting-snapshot-如何判断学会了"></a>
#### 如何判断学会了

每项任务完成都要留下三个结果：

1. **程序证据**：正常输入和相关失败输入的真实输出、Trace 或测试报告。
2. **自己的解释**：不照着代码读，能说明输入、输出、状态变化、失败行为。
3. **一个变化**：独立改一项需求或修一个缺陷，再验证它。

“安装完成”“页面能打开”“模型回答很像正确答案”分别只能证明一部分。未验证的任务保持未完成。阶段标签只在相关证据齐全后创建。

下面各阶段的“技术点掌握程度标准”是学习验收表，描述你在阶段结束时应达到的程度，不表示当前已经完成。按本周任务只学相关行；同一技术在后续阶段会提高要求，例如 V0会运行测试，V1才要求自己设计只读工具行为测试，V4再验证密码写行为。

| 学习层次 | 怎样判断达到 | 怎样留证据 |
|---|---|---|
| 能解释 | 不照读代码，能说清作用、输入输出、与相邻模块的责任边界 | 用自己的话写说明或画流程图，回答“为什么需要它” |
| 能独立实现 | 可以查官方文档，但不整段照搬教程；能在项目中完成本行列出的行为 | 实现位置、运行命令、真实输出和对应提交 |
| 能排错验证 | 能定位相关失败，区分配置、协议、业务、权限与模型问题，修改后验证 | 正常结果、相关反例、修复前后结果及原因 |

“可后置内容”不纳入本阶段必过条件，也不要求先学完才能动手。表中的练习与阶段任务配合使用，按相应阶段的工时与业务验收指标执行。每行记录“待学 / 在做 / 已验证”及证据路径，不能用看完视频、阅读时长或主观掌握百分比替代结果。密码工具的具体掌握标准另见 [本阶段密码工具合同](stages/V1-CORE-DEMO.md#crypto-3.1)。
