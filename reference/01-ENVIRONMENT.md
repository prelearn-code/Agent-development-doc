# 01 - 分阶段环境搭建

> 按需参考资料。实现步骤与阶段目标集中在[学习总览](../LEARNING-PATH.md)及对应阶段，不需要先通读本文件。

> 开发、构建、测试与全部服务都在 Ubuntu 内完成。安装命令是后续学习操作，完成状态必须有实际验证输出。

## 0. 决策：全部在 Ubuntu 内实现，Windows 只作浏览器客户端

**结论：仓库、Ollama、Docker、数据库、向量库、API、前端全部运行在 Ubuntu 内；
Windows 不承担任何实现角色，只通过浏览器从网络访问前端页面。**

本机 Ubuntu 是 WSL2 里的 Ubuntu-22.04.5（内核 `6.6.87.2-microsoft-standard-WSL2`），
但它对项目而言就是**一台 Linux 主机**：所有进程、文件、容器、GPU 访问都在它内部完成。
除「用浏览器打开页面」以外，本指南不包含任何 Windows 侧的实现步骤。

本项目采用单台 Ubuntu 主机，减少跨主机配置，便于从开发环境逐步学习到部署。密码工具始终由受控适配层调用，应用进程、数据和库安装路径明确分开。

实测依据：

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

### 0.1 仓库放在 Ubuntu 的文件系统上

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

### 0.2 Ollama 与应用的连接

Ollama 使用 Ubuntu 内的 systemd 服务，应用连接 `http://127.0.0.1:11434`。模型服务不对浏览器或外部网络直接开放；容器访问宿主服务按第5节的实际网络路线配置。

### 0.3 环境改变的纪律

环境变更后必须新建实验，不修改旧结果（§8）。上面每一项数值都要能被
`environment.lock.json` 复现；对不上的值以 lock 文件为准。

## 1. 分阶段引入

| 交付阶段 | 本次引入/核对 | 可后置 |
|---|---|---|
| V0 | Git/Python3.12/uv/Ollama/4B、配置首测 | Node构建、DB、9B、向量库 |
| V1 | 只读OpenSSL/GmSSL适配、受控资源/超时、httpx/测试 | 受控AEAD练习到V4 |
| V2 | Ubuntu Docker/Compose、PostgreSQL/Alembic、Node/pnpm、API与React小页 | SSE/六查询/完整前端专项 |
| V3 | 锁定MCP SDK，一个stdio Crypto Server与Client | 三Server、Resource/Prompt、新端点到V6 |
| V4 | 教学keystore/profile、动作账本、Graph saver、审批/产物 | RAG、worker/队列按需后置 |
| V5 | Qdrant/embed、reranker按需、Memory表、SSE | 9B/正式实验到V6 |
| V6 | 9B/固定Judge、三职责MCP、完整部署/恢复；选修worker | 27B、WebSocket、HSM/KMS、多Agent |

按[学习总览](../LEARNING-PATH.md)分配，不把目标编号或M依赖组名当新阶段。第一前端在V2构建运行；模型/Provider/网络与权限先验证再升级。

Ubuntu宿主与容器使用各自可达地址，按第5节选定host或bridge路线。宿主不要直接使用仅容器可解析的postgres/qdrant服务名，容器127.0.0.1也不是宿主Ollama。

## 2. Python 与目录

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
M1 加 pydantic/httpx/pydantic-settings，M2 加 fastapi/uvicorn/sqlalchemy/asyncpg/alembic，
M3 再加 qdrant-client/pymupdf/BM25/分词器，M4 加 mcp/langgraph/checkpoint-postgres。
不能靠无上界的最低版本声明保证 API 稳定，实际版本锁定后保存兼容 smoke Trace。

> 应用仓库已按上述分组写好 `pyproject.toml`（`m1`/`m2`/`m3`/`m4`/`ml`/`dev` extras），
> 并带有纯标准库的自检脚本 `scripts/selftest.py`（校验目录布局、`.env.example` 与
> `Settings` 字段双向一致、密钥扫描、分层反向依赖）。**在 `uv sync` 之前就能跑**。

## 3. Ollama（Ubuntu 内 systemd 服务）

Ollama作为Ubuntu内的系统服务运行，检查方式：

```bash
# 状态与版本
systemctl status ollama --no-pager
ollama --version                     # 实测 0.32.15
curl -s http://127.0.0.1:11434/api/version

# 模型
ollama list
ollama pull qwen3.5:4b               # Phase 0 唯一必需模型；仅缺失时拉取
ollama run qwen3.5:4b "用一句话说明工具调用"
ollama ps
```

模型文件在 `/usr/share/ollama/.ollama/models`（当前 20 GB）。M3 拉 bge-m3，
M5 按需拉 qwen3.5:9b。模型名可变，实验记录实际 digest、量化、template、上下文参数；
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

## 4. Docker：Ubuntu 内原生 engine

本机实测：**Ubuntu 内已有原生 Docker engine 29.1.3**（`overlay2` + cgroup v2 + seccomp），
Windows 侧**未安装也不需要** Docker Desktop。整个项目只有这一条路线。

```bash
# 先检查 compose 插件，仅缺失时按官方 Ubuntu 安装说明补齐
if ! docker compose version; then
  sudo apt update
  sudo apt install -y docker-compose-plugin
fi
docker version
docker compose version
docker run --rm hello-world
```

优点：少一层转发，compose 行为与 Linux 服务器一致，M6 的"干净环境部署"验收更真实；
服务容器可以配置只读挂载、网络范围与PID/内存限制；各项按实际服务需求验证。

Docker daemon 的资源上限由 WSL 的 `.wslconfig` 控制。实测 Ubuntu 内可见
RAM 15 GB / 20 线程（宿主 31.8 GB / 20 线程），容器上限不得超出这个可见范围。

开发 Compose 从 PostgreSQL 单服务开始；向量库、队列、对象存储使用 profiles。下例是**待填版本的模板**，尖括号值不可直接执行，选择版本、验证后记录 digest。完整 DB role/迁移契约见 [repo-structure.md](repo-structure.md)。

```yaml
services:
  postgres:
    image: pgvector/pgvector:<已验证的pg16版本或digest>
    environment:
      POSTGRES_USER: bootstrap_admin
      POSTGRES_PASSWORD: ${POSTGRES_BOOTSTRAP_PASSWORD:?required}
      POSTGRES_DB: lpa
    ports: ["127.0.0.1:5432:5432"]
    volumes: ["pgdata:/var/lib/postgresql/data"]
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U bootstrap_admin -d lpa"]
      interval: 5s
      timeout: 3s
      retries: 20
    restart: unless-stopped
  qdrant:
    profiles: ["rag"]
    image: qdrant/qdrant:<已验证版本或digest>
    ports: ["127.0.0.1:6333:6333"]
    volumes: ["qdrantdata:/qdrant/storage"]
    restart: unless-stopped
volumes:
  pgdata:
  qdrantdata:
```

Qdrant readiness 使用外部探针检查该版本 `/readyz`，或构建带探针的镜像；不假设官方镜像内有 bash/curl。`pg_isready` 只表示服务能接连接，应用 readiness 还要检查 schema_version/迁移是否完成。PostgreSQL 初始化脚本只在空 volume 运行；角色与后续 schema 升级由独立迁移步骤管理。

`POSTGRES_USER` 初始化为超级用户，只给 bootstrap 工具使用。app_user/query_reader/audit_writer 密钥各自独立，服务不拿 bootstrap 凭据。开发端口绑定 127.0.0.1；部署内部数据库不映射宿主机端口。[官方镜像账号说明](https://hub.docker.com/_/postgres)

## 5. 网络：Ubuntu 内部回环，Windows 只访问前端

现在只有两条链路，且方向相反：**Ubuntu 内部全是回环，跨系统只有"Windows 浏览器 → 前端页面"这一条**。

### 5.1 Ubuntu 内部

```
Ubuntu 上的 Python 应用  ──►  127.0.0.1:11434   (Ollama)
Ubuntu 上的容器          ──►  postgres / qdrant 服务名
```

Ollama 默认只监听 `127.0.0.1`，这是**推荐状态**。如果 M2/M4 的容器里确实需要调 Ollama，
用下面两种方式之一，**不要**把 Ollama 改成监听 `0.0.0.0` 再开防火墙：

```yaml
# 方式一（推荐，单机开发）：容器共享宿主网络，直接 127.0.0.1:11434
services:
  agent-api:
    network_mode: host
    environment:
      OLLAMA_BASE_URL: http://127.0.0.1:11434
```

```yaml
# 方式二：显式声明宿主机，此时 Ollama 必须额外监听 docker0 地址
services:
  agent-api:
    extra_hosts:
      - "host.docker.internal:host-gateway"
    environment:
      OLLAMA_BASE_URL: http://host.docker.internal:11434
```

方式二的 `host.docker.internal` 解析到 `172.17.0.1`（docker0）；若 Ollama 仍只绑
`127.0.0.1` 则连不通，需要把 `OLLAMA_HOST` 改为 `172.17.0.1:11434`。
该地址只在本机 docker0 网桥上可达，不暴露到局域网，但**改了就要用
`ss -ltnp | grep 11434` 和一次真实 `curl` 各自确认**，不能凭本文件的示例值认定生效。

> 无论哪种方式，Ollama **不监听 `0.0.0.0`**，也不加任何对外放行规则。

### 5.2 Windows 访问前端（唯一跨系统链路）

最终交付物是一个**前端页面**，验收方式就是"Windows 上能用浏览器打开它"。
因此前端（以及 M6 的静态站点）必须监听所有网卡，而不是只绑回环：

```bash
# 前端与 API 监听 0.0.0.0:<port>，例如
uv run uvicorn services.agent_api.main:app --host 0.0.0.0 --port 8000
```

Windows 侧打开浏览器访问下列任一地址：

```text
http://172.26.9.67:8000      # Ubuntu 的 eth0 地址（实测；WSL 重建后会变）
http://localhost:8000         # WSL2 的 localhost 转发，多数情况可用
```

取当前 Ubuntu 地址：

```bash
hostname -I | awk '{print $1}'
```

约束与纪律：

- **只放行前端/API 端口**。数据库、Qdrant、Redis、Ollama 一律绑 `127.0.0.1`，
  不映射到对外网卡 —— 前端是唯一的对外入口。
- API 自身的鉴权（`API_KEY_HEADER`）不因为是"内网"而省略；
  M2 的越权用例必须在**从 Windows 访问**的同一条链路上验证。
- 前端绑 `0.0.0.0` 意味着同网段可访问。仅在可信网络下这样做，
  需要更严时改为绑定具体网卡地址或用反向代理加鉴权。
- 端口与地址的实际值必须在改完后用 `ss -ltnp` 与一次真实浏览器访问各自验证一次。

## 6. PyTorch / Blackwell（V5检索实验按需）

NVIDIA 驱动显示的 CUDA Version 是驱动支持上限，不证明 wheel 包含 sm_120 的代码。Ollama 与预编译 PyTorch 一般不需要 nvcc；自行编译扩展另行安装 Toolkit。

不要使用旧的 cu124 命令。选择支持 RTX 50 系的官方 wheel，固定 PyTorch 版本、CUDA 构建与依赖。**兼容起点示例**为 torch 2.7.1 + cu128，代表历史可用组合而非“最新版本”；实际通过后才锁定。当前安装也可按官网选支持 Blackwell 的更新稳定版，再重新验证，不能悄悄覆盖实验环境。

```bash
uv pip install "torch==2.7.1" --index-url https://download.pytorch.org/whl/cu128
python -c "import torch; assert torch.cuda.is_available(); x=torch.randn(256,256,device='cuda'); y=x@x; torch.cuda.synchronize(); print(torch.__version__, torch.version.cuda, torch.cuda.get_device_name(0), torch.cuda.get_device_capability(0), float(y.mean()))"
```

该一次性诊断命令之后必须把通过的依赖与源索引写入 pyproject/lock，防止下次 uv sync 替换 CUDA 构建。还要跑一对真实 reranker 输入；仅 `is_available()` 不足以验收。[PyTorch 2.7 Blackwell 支持](https://pytorch.org/blog/pytorch-2-7/)、[官方安装选择器](https://pytorch.org/get-started/locally/)

## 7. 密码 Provider 与资源边界

OpenSSL/GmSSL 源码仓库与文档同级，运行时采用受控安装前缀或验证过的系统库。记录 CLI、Python 包和实际 C 后端版本，不依据源码目录存在认定能力已可用。

固定 API 或参数数组调用 Provider，限制输入大小、超时和输出。模型只提交获授权的 file_id/certificate_id/key_id；服务端解析真实位置，密钥与解密明文不进入模型。算法不支持时明确拒绝，不静默切换为其他模式。

安装与能力验证任务见 [Provider 入门练习](06-CRYPTO-AGENT-SCOPE.md#10-后续可以照着操作的-provider-入门练习)，加解密、签名、证书与密钥掌握标准见同文件第3、5、6节。

## 8. 环境记录与待验证项

### 8.1 项目环境记录

以下记录来自2026年10月10日的只读检查，供Phase 0确定起点。开始学习时重新运行对应检查，记录当次版本与结果，不用记录表代替实际验收。

| 项目 | 已记录的状态 | 后续检查 |
|---|---|---|
| Ubuntu | Ubuntu 22.04.5 LTS，用户zsw | 当前发行版、用户、工作目录 |
| Python | 系统3.10.12；项目venv为3.12.13 | 新终端解释器与依赖锁 |
| Ollama | Ubuntu内服务，模型列表已有qwen3.5:4b | version、digest与真实请求 |
| 模型配置 | `.env.example`为127.0.0.1:11434和qwen3.5:4b | 当前Settings与本地配置一致 |
| OpenSSL CLI | 3.0.2 | 路径、实际版本、帮助与smoke |
| Python密码后端 | 尚未验证 | cryptography后端版本与选定功能 |
| GmSSL | 尚未验证 | C库、绑定、动态库加载与能力清单 |
| 项目基础 | 已有core配置与模型骨架；检查时无uv.lock和工具/Loop测试 | 按P0任务补依赖锁和首个测试 |
| Compose与应用运行 | 本轮未作运行验证 | 插件、迁移、服务readiness与应用smoke |

### 8.2 模型与资源记录

Phase 0只需qwen3.5:4b；9B在M5比较前准备。Embedding到M3引入，reranker按消融需求准备，27B属于可选配置。每次实验保存实际model digest、推理配置、空闲/峰值显存、冷/热加载状态，下载体积不能直接当显存占用。

### 8.3 环境验收记录方式

实现仓库的`docs/environment.md`保存当次命令、输出、版本、未验证项和必要降级说明；`scripts/selftest.py`检查骨架与配置契约。二者与文档不一致时先核对实际环境，再同步修正。学习从 [P0环境检查](../stages/V0-ENVIRONMENT.md#p0-01-检查已有环境) 开始。


## 9. 按交付验证环境，不以安装代替掌握

| 交付阶段 | 必须真实验证 | 不能据此声称的能力 |
|---|---|---|
| V0 | 新终端请求/测试/解释器/lock | 所有Provider均支持 |
| V1 | 真实只读工具与有限Loop，失败/超时可解释 | 已开放写动作/MCP |
| V2 | 迁移/角色/重启与JSON API，浏览器上传/执行/查询 | 完整SSE/审批/前端毕业 |
| V3 | 同工具直调/MCP对照、未知风险/断连拒绝 | 三职责或远程HTTP已验收 |
| V4 | 教学密码往返、固定审批、账本与故障恢复 | 全部证书/轮换工具齐全 |
| V5 | 三格式定位/授权/发布、Verifier/Memory/四组检索/SSE | 完整模型和frozen题库 |
| V6 | 清洁复现、完整专项/实验、安全、材料备份恢复 | 生产CA或合规认证 |

历史版本是日期快照，开始时重新测量。环境变更按02回归，运行/恢复依赖见09，个人深度以对应阶段的目标表为准。
