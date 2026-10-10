# 01 - 分阶段环境搭建

> 2026-10-10 修订；同日补充 WSL 决策与实测记录（§2）。硬件与工具链数值为 2026-10-10 实测，
> 替换旧文档的估算值。**安装命令不等于已验证完成**，每项须有实际验证输出。

## 0. 决策：开发环境用 WSL Ubuntu（2026-10-10 实测后确定）

**结论：仓库与 Docker 都在 WSL Ubuntu-22.04 内；Ollama 保留在 Windows 原生。**

这不是偏好，是 M1 的 sandbox 要求决定的。原验收文档要求隔离环境满足
"无网络、无秘密、非 root、只读根文件系统、限制 CPU/内存/PID/输出、
不挂载 Docker socket"，且**"不能降级为宿主机执行不可信代码"**。
这些是 Linux namespace/cgroup 原语，Windows 侧没有对等替代。

实测依据：

| 项 | 实测值 | 含义 |
|---|---|---|
| WSL 发行版 | Ubuntu-22.04.5 LTS，运行中 | 可用 |
| WSL 内 Docker | **原生 29.1.3**，`/var/run/docker.sock` | 无需 Docker Desktop |
| Docker 能力 | `overlay2` + **cgroup v2** + seccomp + runc 1.3.3 | sandbox 硬条件已满足 |
| GPU 直通 | WSL 内 `nvidia-smi -L` 可见 RTX 5060 Ti | 需要时可用 |
| uv | `/home/zsw/.local/bin/uv` | 已装 |
| WSL 磁盘 | `/` 1007 GB，可用 750 GB | 充足 |
| WSL 用户 | `zsw`（非 root） | 符合最小权限 |

### 0.1 仓库必须放在 WSL 的 ext4 上

`/mnt/d/...` 走 9P 协议，venv、node_modules 这类大量小文件操作会慢数倍。
仓库路径用 `~/projects/Agent-development-code`，**不要**放 `/mnt/d`。

指南包是静态 Markdown，留在 `D:\work\Agent-development-doc` 即可，
从 WSL 按 `/mnt/d/work/Agent-development-doc` 读取（只读不影响性能）。

### 0.2 为什么 Ollama 留在 Windows

GPU 直通已生效、模型已下载（其中一个 16.52 GB），迁移需重拉或用 `ollama cp` 搬运，
收益不足。代价是 WSL 内必须走**宿主 IP** 而非 `localhost`（见 §5）。

若后续 WSL→Windows 网络持续不稳，再考虑把 Ollama 移入 WSL ——
GPU 直通已实测可用，这条退路是通的，但要重新拉模型并重测显存占用。

### 0.3 环境改变的纪律

环境变更后必须新建实验，不修改旧结果（§8）。上面每一项数值都要能被
`environment.lock.json` 复现；对不上的值以 lock 文件为准。

## 1. 分阶段引入

| 阶段 | 必需 | 可后置 |
|---|---|---|
| Phase 0 | Git、Python 3.12、uv、Ollama、qwen3:4b | 8B/14B、Docker、数据库 |
| M1 | 首次运行不可信代码前完成 Docker Sandbox | GPU 直通容器 |
| M2 | WSL 内 Docker + compose 插件、PostgreSQL + pgvector、Alembic | Redis、MinIO |
| M3 | Qdrant、bge-m3；reranker 后引入 | learned sparse |
| M4~M6 | Graph checkpointer、需要时 Redis worker、对象存储、Node | WebSocket、GPU sandbox |

宿主机应用访问 localhost；容器内部访问 postgres/qdrant/redis 等服务名。不要把宿主机 URL 原样复制进容器。
**例外**：Ollama 在 Windows 宿主，WSL 应用与容器都访问**宿主 IP**，不是 localhost（§5）。

## 2. Python 与目录

按 §0 的决策：指南留在 `D:\work\Agent-development-doc`（静态文档，Windows 侧编辑即可），
应用建在 **WSL 内** `~/projects/Agent-development-code`。命令从应用根目录运行。

**WSL 系统自带 Python 3.10.12，不满足项目的 3.12 要求。用 uv 提供，不要 `apt install`**
（Ubuntu 22.04 默认源没有 3.12，加 deadsnakes PPA 会污染系统环境）：

```bash
# WSL 内执行
uv venv --python 3.12 .venv          # uv 自动下载 cpython-3.12.13，无需 root
source .venv/bin/activate
python -c "import sys; print(sys.executable, sys.prefix)"   # 必须指向 .venv
```

Windows 侧的历史解释器路径 `D:\evm\python3.12.8\python.exe` **已不再是项目依赖**；
仅在需要 Windows 原生跑脚本时使用。

先创建合法 pyproject（至少 name/version/requires-python），按里程碑加入依赖；
提交 uv.lock，正式启动 `uv sync --frozen`。开发依赖 pytest/pytest-asyncio/ruff/mypy；
M1 加 pydantic/httpx/pydantic-settings，M2 加 fastapi/uvicorn/sqlalchemy/asyncpg/alembic，
M3 再加 qdrant-client/pymupdf/BM25/分词器，M4 加 mcp/langgraph/checkpoint-postgres。
不能靠无上界的最低版本声明保证 API 稳定，实际版本锁定后保存兼容 smoke Trace。

> 应用仓库已按上述分组写好 `pyproject.toml`（`m1`/`m2`/`m3`/`m4`/`ml`/`dev` extras），
> 并带有纯标准库的自检脚本 `scripts/selftest.py`（校验目录布局、`.env.example` 与
> `Settings` 字段双向一致、密钥扫描、分层反向依赖）。**在 `uv sync` 之前就能跑**。

## 3. Ollama

```powershell
winget install --id Ollama.Ollama -e
Invoke-RestMethod http://127.0.0.1:11434/api/version
ollama pull qwen3:4b
ollama run qwen3:4b "用一句话说明工具调用"
ollama ps
```

M3 拉 bge-m3，M5 按需拉 8B/14B。模型名可变，实验记录实际 digest、量化、template、上下文参数；权重体积不能直接当推理峰值显存。

| 变量 | 起点 | 注意 |
|---|---|---|
| OLLAMA_HOST | 127.0.0.1:11434 | 默认仅本机 |
| OLLAMA_MODELS | D:\ollama-models | 按磁盘空间选择 |
| OLLAMA_MAX_LOADED_MODELS | 1 | 限 Ollama 管理的模型，不限制 PyTorch |
| OLLAMA_NUM_PARALLEL | 1 | baseline 固定串行 |
| OLLAMA_KEEP_ALIVE | 5m | embedding 与 controller 切换可能导致重复加载 |
| OLLAMA_FLASH_ATTENTION | 1 | 核对实际版本支持 |
| OLLAMA_KV_CACHE_TYPE | q8_0 | 和上下文长度一起固定与记录 |

如果全部 embedding/controller 共用单模型槽，不声称两者都处于 warm 状态。可选择 CPU embedding、单独部署、预计算用于检索质量实验，或接受换模并计入端到端延迟。生成与 Judge 分批运行，避免每题来回换模型。

原生 `/api/chat` 的流是 NDJSON；应用 `/chat` 给前端的流是 SSE，两层分别适配。[Ollama streaming](https://docs.ollama.com/api/streaming)、[tool calling](https://docs.ollama.com/capabilities/tool-calling)

## 4. Docker：两条路线（2026-10-10 实测后修订）

本机实测：**WSL 内已有原生 Docker engine 29.1.3**（`overlay2` + cgroup v2 + seccomp），
Windows 侧**未安装** Docker Desktop。因此走**路线 A**。

### 路线 A（本机采用）：WSL 内原生 Docker engine

```bash
# 唯一缺口：compose 插件
sudo apt update && sudo apt install -y docker-compose-plugin
docker version
docker compose version
docker run --rm hello-world
```

优点：少一层转发，compose 行为与 Linux 服务器一致，M6 的"干净环境部署"验收更真实；
`read_only`、`--network none`、PID/内存限制等 M1 sandbox 原语直接可用。
代价：容器无法直接读写 Windows 文件系统路径，需要在 WSL 内准备挂载目录。

Docker daemon 的 cgroup 上限由 WSL 的 `.wslconfig` 控制（用户目录），
示例 `memory=12GB`、`processors=8`，调整后需按 WSL 要求重启。
不是所有版本都能在 Docker Desktop 里设置 WSL 内存 —— 路线 A 下该设置项不适用。
[Docker WSL 指南](https://docs.docker.com/desktop/features/wsl/best-practices/)

### 路线 B（备选）：Docker Desktop + WSL2 集成

```powershell
winget install --id Docker.DockerDesktop -e
```

仅在前述条件不成立时使用（例如需要与 Windows 文件系统深度集成、
或本机没有可用 WSL 发行版）。开启 WSL2 backend 和所需发行版集成。

**两条路线的差异会影响后续配置**：

| 项 | 路线 A（原生） | 路线 B（Desktop） |
|---|---|---|
| 容器访问宿主 Ollama | 宿主 IP，需 `extra_hosts` | 通常可用 `host.docker.internal` |
| compose 端口绑定行为 | 与 Linux 一致 | 经 Desktop 转发 |
| GPU 直通 | WSL 原生，`nvidia-smi` 已验证可见 | Desktop 设置项 |
| Windows 路径挂载 | 不直接支持 | 支持 |

**本机验证记录**：`docker info` 报 `StorageDriver=overlay2 CgroupVersion=2`，
seccomp 启用，runc 1.3.3。WSL 内 `nvidia-smi -L` 可见 RTX 5060 Ti。

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

## 5. 容器访问宿主机 Ollama

**本机采用路线 A（WSL 原生 Docker），因此 `host.docker.internal` 不自动存在**，
与路线 B 的写法不同。

WSL 默认 NAT 模式下有两条独立链路，都要打通：

```
WSL 内的 Python 应用  ──► 宿主 IP:11434
Docker 容器          ──► 宿主 IP:11434（需 extra_hosts 或直接写 IP）
```

取宿主 IP（WSL 重建后会变，需重新确认）：

```bash
ip route show default | awk '{print $3}'      # 实测 172.26.0.1
```

Windows 侧必须让 Ollama 监听非回环地址，否则两条链路都不通：

```powershell
[Environment]::SetEnvironmentVariable('OLLAMA_HOST','0.0.0.0:11434','User')
# 重启 Ollama 后确认监听
netstat -ano | Select-String '11434'
```

compose 里显式声明宿主（路线 A 必需）：

```yaml
services:
  agent-api:
    extra_hosts:
      - "host.docker.internal:host-gateway"
    environment:
      OLLAMA_BASE_URL: http://host.docker.internal:11434
```

**防火墙规则必须限制来源，不能只按 Private profile 放行**：
绑定 `0.0.0.0` 后，任何能路由到该端口的客户端都能调用 Ollama。
至少限定到 WSL 所在网段（本机 NAT 网关为 `172.26.0.0/20` 一类），
并避免在公共网络配置下生效：

```powershell
New-NetFirewallRule -DisplayName "Ollama for WSL" -Direction Inbound `
  -Protocol TCP -LocalPort 11434 -Action Allow `
  -RemoteAddress 172.26.0.0/20 -Profile Private
```

需要外部访问时增加鉴权代理；Ollama 不直接暴露到互联网。
[Ollama FAQ](https://docs.ollama.com/faq)

> 端口与网段的实际值必须在改完后用 `netstat` 与 `curl` 各自验证一次，
> 不能只凭本文件的示例值认定已生效。

## 6. PyTorch / Blackwell（M3 后段）

NVIDIA 驱动显示的 CUDA Version 是驱动支持上限，不证明 wheel 包含 sm_120 的代码。Ollama 与预编译 PyTorch 一般不需要 nvcc；自行编译扩展另行安装 Toolkit。

不要使用旧的 cu124 命令。选择支持 RTX 50 系的官方 wheel，固定 PyTorch 版本、CUDA 构建与依赖。**兼容起点示例**为 torch 2.7.1 + cu128，代表历史可用组合而非“最新版本”；Windows/Python 与 FlagEmbedding 集成实际通过后才锁定。当前安装也可按官网选支持 Blackwell 的更新稳定版，再重新验证，不能悄悄覆盖实验环境。

```powershell
uv pip install "torch==2.7.1" --index-url https://download.pytorch.org/whl/cu128
python -c "import torch; assert torch.cuda.is_available(); x=torch.randn(256,256,device='cuda'); y=x@x; torch.cuda.synchronize(); print(torch.__version__, torch.version.cuda, torch.cuda.get_device_name(0), torch.cuda.get_device_capability(0), float(y.mean()))"
```

该一次性诊断命令之后必须把通过的依赖与源索引写入 pyproject/lock，防止下次 uv sync 替换 CUDA 构建。还要跑一对真实 reranker 输入；仅 `is_available()` 不足以验收。[PyTorch 2.7 Blackwell 支持](https://pytorch.org/blog/pytorch-2-7/)、[官方安装选择器](https://pytorch.org/get-started/locally/)

## 7. Sandbox 与降级

不可信代码只能在已验收的隔离环境；无 Docker 时 run_python 暂仅开放受信任模板，不允许任意脚本。Sandbox 的非 root、只读、无网络、无秘密、限制资源、超时清理和受控输出在 M1 验收，M5 扩展攻击测试。

GPU 不可用可用 CPU 4B 或 CPU reranker，明确标记后不能与 GPU baseline 混比。MinIO 可先用受控本地存储 adapter；Redis 尚未引入时只支持单进程执行，不声称具备持久化队列/多 worker 恢复。GPU 容器是选修；Docker Desktop WSL2 与发行版自行运行 Docker engine 的安装流程分别处理。[Docker GPU 支持](https://docs.docker.com/desktop/features/gpu/)

## 8. 环境记录

保存 `environment.lock.json`：OS/WSL/驱动/GPU、Python/uv/Ollama、package lock hash、容器 digest、模型 digest/量化、num_ctx/think/temperature/seed、并行度、embedding/rerank 部署方式、冷/热启动规则。环境改变必须建新实验，不修改旧结果。

### 8.1 2026-10-10 实测快照（Phase 0 起始）

| 项 | 实测值 |
|---|---|
| CPU / RAM | i5-14600KF，14 核 / 20 线程；31.8 GB |
| GPU | RTX 5060 Ti，16311 MiB；驱动 591.86 |
| GPU 空闲占用 | 2483 MiB（桌面常驻），**可用约 13.5 GB** |
| WSL | Ubuntu-22.04.5 LTS，`/` 可用 750 GB，用户 `zsw` |
| WSL 网络 | **NAT 模式**，宿主网关 `172.26.0.1` |
| Python（WSL 系统） | 3.10.12（不够，用 uv 取 3.12） |
| uv | `/home/zsw/.local/bin/uv` |
| Docker（WSL 原生） | 29.1.3，`overlay2` + cgroup v2 + seccomp |
| docker compose | **缺失**，需 `docker-compose-plugin` |
| Ollama（Windows 原生） | API v0.32.15 运行中；**CLI 不在 PATH** |
| GPU 直通（WSL 内） | `nvidia-smi -L` 可见 RTX 5060 Ti |

### 8.2 模型现状与风险

| 模型 | family | 参数 | 体积 | 判断 |
|---|---|---|---|---|
| `qwen3.8:27b-q4_K_M` | qwen35 | 27.3B | 16.52 GB | 与计划模型**不同代** |
| `qwen3.8-agent-32k` | qwen35 | 27.3B | 16.52 GB | 自定义微调，**非**对照基线 |
| `qwen3-vl:4b` | qwen3vl | 4.4B | 3.07 GB | 视觉模型，不能当 Controller |

**风险**：27B 权重 16.52 GB > 可用显存 13.5 GB，必然 CPU offload；
且与 `qwen3:4b/8b` 不同代，**不能用于 §13 的 4B vs 8B 对比结论**。

### 8.3 Phase 0 未完成项

- [ ] 拉取 `qwen3:4b`（Phase 0 唯一必需模型）
- [ ] Ollama CLI 可用（`winget install Ollama.Ollama` 会一并补上）
- [ ] Windows 侧 `OLLAMA_HOST=0.0.0.0:11434` + 限制来源的防火墙规则
- [ ] WSL 侧 `docker-compose-plugin`
- [ ] `uv venv --python 3.12` + `uv sync --extra m1 --extra dev`
- [ ] 一个通过的最小请求测试（Phase 0 的验收判据）

### 8.4 应用仓库侧的同源记录

实现仓库内有 `docs/environment.md`（同一份数据的可读版）与
`scripts/selftest.py`（可执行契约）。**两处不一致时以本文件的实测表为准，
并同步修正实现仓库**——不能只改一处。
