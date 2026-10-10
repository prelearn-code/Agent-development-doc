# 01 - 分阶段环境搭建

> 2026-10-10 修订；同日按「全部在 Ubuntu 内实现」重写环境拓扑（§0）。
> 硬件与工具链数值为 2026-10-10 在 Ubuntu 内实测，替换旧文档的估算值与 Windows 侧记录。
> **安装命令不等于已验证完成**，每项须有实际验证输出。

## 0. 决策：全部在 Ubuntu 内实现，Windows 只作浏览器客户端

**结论：仓库、Ollama、Docker、数据库、向量库、API、前端全部运行在 Ubuntu 内；
Windows 不承担任何实现角色，只通过浏览器从网络访问前端页面。**

本机 Ubuntu 是 WSL2 里的 Ubuntu-22.04.5（内核 `6.6.87.2-microsoft-standard-WSL2`），
但它对项目而言就是**一台 Linux 主机**：所有进程、文件、容器、GPU 访问都在它内部完成。
除「用浏览器打开页面」以外，本指南不包含任何 Windows 侧的实现步骤。

这不是偏好，是 M1 的 sandbox 要求决定的。原验收文档要求隔离环境满足
"无网络、无秘密、非 root、只读根文件系统、限制 CPU/内存/PID/输出、
不挂载 Docker socket"，且**"不能降级为宿主机执行不可信代码"**。
这些是 Linux namespace/cgroup 原语，Windows 侧没有对等替代 ——
所以不仅 sandbox，整个实现栈都留在 Ubuntu 内最省事，也最接近 M6 的真实部署形态。

实测依据：

| 项 | 实测值 | 含义 |
|---|---|---|
| 发行版 | Ubuntu 22.04.5 LTS（WSL2） | 可用 |
| Ubuntu 内 Docker | **原生 29.1.3**，`/var/run/docker.sock` | 无需 Docker Desktop |
| Docker 能力 | `overlay2` + cgroup v2 + seccomp | sandbox 硬条件已满足 |
| Ubuntu 内 GPU | `nvidia-smi` 可见 RTX 5060 Ti，驱动 591.86 | GPU 直通已生效 |
| Ubuntu 内 Ollama | **0.32.15，systemd 服务 enabled 且运行中** | 已是 Ubuntu 服务 |
| uv | `~/.local/bin/uv`，0.11.12 | 已装 |
| Ubuntu 内 Node | v22.23.2 + pnpm 12.3.4 | M6 前端直接可用 |
| 磁盘 | `/` 1007 GB，可用 750 GB | 充足 |
| Ubuntu 用户 | `zsw`（非 root） | 符合最小权限 |

### 0.1 仓库放在 Ubuntu 的文件系统上

两个仓库同级摆放在 `/home/zsw/work/agent_development/`：

```
/home/zsw/work/agent_development/
├── Agent-development-doc/     ← 指南（静态 Markdown）
└── Agent-development-code/    ← 实现仓库
```

同级是硬要求：指南里的 `../Agent-development-code/` 相对链接否则会断。

**不要**把实现仓库放到 `/mnt/c`、`/mnt/d` 这类 Windows 挂载点：它们走 9P 协议，
venv、node_modules 这种大量小文件操作会慢数倍。实现仓库必须在 Ubuntu 的 ext4 上。

### 0.2 为什么 Ollama 也在 Ubuntu 内

旧方案把 Ollama 留在 Windows 宿主，Ubuntu 侧用宿主 IP 跨网络访问，代价是：
端口要监听 `0.0.0.0`、要开防火墙、宿主 IP 随 WSL 重建而变、多一层网络故障点。

现在 Ollama 已作为 **Ubuntu 内的 systemd 服务**运行（`/usr/local/bin/ollama`，
监听 `127.0.0.1:11434`），于是：

- 应用与 Ollama 之间是**本机回环**，不经过任何跨系统网络，`localhost` 可用。
- 宿主 IP 漂移问题消失，`.env` 不需要随环境改地址。
- Ollama **不再需要对外监听**，攻击面反而比旧方案小。

GPU 直通在 Ubuntu 内已实测可用，模型文件也在 Ubuntu 内
（`/usr/share/ollama/.ollama/models`，当前 20 GB），迁移成本已经付过了。

### 0.3 环境改变的纪律

环境变更后必须新建实验，不修改旧结果（§8）。上面每一项数值都要能被
`environment.lock.json` 复现；对不上的值以 lock 文件为准。

## 1. 分阶段引入

| 阶段 | 必需 | 可后置 |
|---|---|---|
| Phase 0 | Git、Python 3.12、uv、Ollama、qwen3.5:4b | qwen3.5:9b、Docker、数据库 |
| M1 | 首次运行不可信代码前完成 Docker Sandbox | GPU 直通容器 |
| M2 | Ubuntu 内 Docker + compose 插件、PostgreSQL + pgvector、Alembic | Redis、MinIO |
| M3 | Qdrant、bge-m3；reranker 后引入 | learned sparse |
| M4~M6 | Graph checkpointer、需要时 Redis worker、对象存储、Node（前端） | WebSocket、GPU sandbox |

Ubuntu 内的应用访问 `localhost`；容器内部访问 postgres/qdrant/redis 等服务名。
不要把服务名 URL 原样复制到 Ubuntu 宿主机，也不要把宿主机 URL 复制进容器。
Ollama 是唯一需要在容器里用 `host.docker.internal` 或 `network_mode: host` 访问的服务（§5）。

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

Ollama 已安装并注册为系统服务，**不是** Windows 程序：

```bash
# 状态与版本
systemctl status ollama --no-pager
ollama --version                     # 实测 0.32.15
curl -s http://127.0.0.1:11434/api/version

# 模型
ollama list
ollama pull qwen3.5:4b               # Phase 0 唯一必需模型（待拉取）
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
# 唯一缺口：compose 插件（实测 `docker compose` 仍是 unknown command）
sudo apt update && sudo apt install -y docker-compose-plugin
docker version
docker compose version
docker run --rm hello-world
```

优点：少一层转发，compose 行为与 Linux 服务器一致，M6 的"干净环境部署"验收更真实；
`read_only`、`--network none`、PID/内存限制等 M1 sandbox 原语直接可用。

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

## 6. PyTorch / Blackwell（M3 后段）

NVIDIA 驱动显示的 CUDA Version 是驱动支持上限，不证明 wheel 包含 sm_120 的代码。Ollama 与预编译 PyTorch 一般不需要 nvcc；自行编译扩展另行安装 Toolkit。

不要使用旧的 cu124 命令。选择支持 RTX 50 系的官方 wheel，固定 PyTorch 版本、CUDA 构建与依赖。**兼容起点示例**为 torch 2.7.1 + cu128，代表历史可用组合而非“最新版本”；实际通过后才锁定。当前安装也可按官网选支持 Blackwell 的更新稳定版，再重新验证，不能悄悄覆盖实验环境。

```bash
uv pip install "torch==2.7.1" --index-url https://download.pytorch.org/whl/cu128
python -c "import torch; assert torch.cuda.is_available(); x=torch.randn(256,256,device='cuda'); y=x@x; torch.cuda.synchronize(); print(torch.__version__, torch.version.cuda, torch.cuda.get_device_name(0), torch.cuda.get_device_capability(0), float(y.mean()))"
```

该一次性诊断命令之后必须把通过的依赖与源索引写入 pyproject/lock，防止下次 uv sync 替换 CUDA 构建。还要跑一对真实 reranker 输入；仅 `is_available()` 不足以验收。[PyTorch 2.7 Blackwell 支持](https://pytorch.org/blog/pytorch-2-7/)、[官方安装选择器](https://pytorch.org/get-started/locally/)

## 7. Sandbox 与降级

不可信代码只能在已验收的隔离环境；无 Docker 时 run_python 暂仅开放受信任模板，不允许任意脚本。Sandbox 的非 root、只读、无网络、无秘密、限制资源、超时清理和受控输出在 M1 验收，M5 扩展攻击测试。

GPU 不可用可用 CPU 4B 或 CPU reranker，明确标记后不能与 GPU baseline 混比。MinIO 可先用受控本地存储 adapter；Redis 尚未引入时只支持单进程执行，不声称具备持久化队列/多 worker 恢复。GPU 容器是选修。[Docker GPU 支持](https://docs.docker.com/desktop/features/gpu/)

## 8. 环境记录

保存 `environment.lock.json`：OS/内核/驱动/GPU、Python/uv/Ollama、package lock hash、容器 digest、模型 digest/量化、num_ctx/think/temperature/seed、并行度、embedding/rerank 部署方式、冷/热启动规则。环境改变必须建新实验，不修改旧结果。

### 8.1 2026-10-10 实测快照（Phase 0 起始，均在 Ubuntu 内取得）

| 项 | 实测值 |
|---|---|
| CPU / 线程 | i5-14600KF，`nproc` = 20 |
| RAM（Ubuntu 可见） | 15 GiB（宿主 31.8 GB，WSL 限额） |
| GPU | RTX 5060 Ti，16311 MiB；驱动 591.86 |
| GPU 空闲占用 | 2622 MiB（桌面常驻），**可用约 13.4 GB** |
| 内核 | 6.6.87.2-microsoft-standard-WSL2 |
| 发行版 | Ubuntu 22.04.5 LTS，`/` 1007 GB，可用 750 GB |
| 用户 | `zsw`（非 root） |
| Ubuntu 地址 | `172.26.9.67/20`（eth0；WSL 重建后会变） |
| Python（Ubuntu 系统） | 3.10.12（不够，用 uv 取 3.12） |
| uv | `/home/zsw/.local/bin/uv`，0.11.12 |
| Docker（Ubuntu 原生） | 29.1.3，`overlay2` + cgroup v2 + seccomp |
| docker compose | **缺失**，需 `docker-compose-plugin` |
| Ollama（Ubuntu systemd） | v0.32.15，**服务 enabled 且运行中**，`127.0.0.1:11434` |
| Ollama 模型目录 | `/usr/share/ollama/.ollama/models`，20 GB |
| Node / pnpm（Ubuntu） | v22.23.2 / 12.3.4 |

### 8.2 模型现状与风险

| 模型 | family | 参数 | 体积 | 判断 |
|---|---|---|---|---|
| **`qwen3.5:4b`** | qwen35 | 4.2B | 3.31 GB | **计划 Controller**，Q4_K_M，**待拉取** |
| `qwen3.5:9b` | qwen35 | 9.0B | 6.55 GB | 目标十一对照（同族同量化），M5 待拉取 |
| `qwen3.5:27b` | qwen35 | 26.9B | 17.48 GB | 可选配置 C；超出可用显存，必然 offload |
| `qwen3.8:27b-q4_K_M` | qwen35 | 27.3B | 16.52 GB | 与计划模型**不同版本**（3.8 ≠ 3.5） |
| `qwen3.8-agent-32k` | qwen35 | 27.3B | 16.52 GB | 自定义微调，**非**对照基线 |
| `qwen3-vl:4b` | qwen3vl | 4.4B | 3.07 GB | 旧独立视觉模型；`qwen3.5:4b` 已原生多模态，可淘汰 |

`qwen3.5:4b` 与 `qwen3.5:9b` **同族（qwen35）、同量化（Q4_K_M）、同 renderer/parser**，
满足目标十一"同族同量化比较"的前提；两者合计约 9.9 GB，可共存于 750 GB 磁盘。

**风险**：已装的 `qwen3.8` 系（16.52 GB）与计划的 `qwen3.5` 系**不同版本**，
不能用于 [00-ROADMAP.md](00-ROADMAP.md) 目标十一的 4B vs 9B 对比结论。
另外 `qwen3.5:27b`（17.48 GB）> 可用显存 13.4 GB，选它作可选配置 C 时必然 CPU offload，
其延迟不可与 4B/9B 组直接并列，必须单独标注。

### 8.3 Phase 0 未完成项

- [ ] 拉取 `qwen3.5:4b`（Phase 0 唯一必需模型）
- [ ] Ubuntu 侧 `docker-compose-plugin`
- [ ] `uv venv --python 3.12` + `uv sync --extra m1 --extra dev`
- [ ] 一个通过的最小请求测试（Phase 0 的验收判据）

> 已消除的旧缺口：Ollama CLI / 服务已在 Ubuntu 内就绪；不再需要 Windows 侧
> `OLLAMA_HOST` 与防火墙配置；不再需要查找宿主 IP。

### 8.4 应用仓库侧的同源记录

实现仓库内有 `docs/environment.md`（同一份数据的可读版）与
`scripts/selftest.py`（可执行契约）。**两处不一致时以本文件的实测表为准，
并同步修正实现仓库**——不能只改一处。
