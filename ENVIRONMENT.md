# 环境复现（另一台设备）

> 目标：在新机器上，只靠**四个仓库的克隆 + 本文命令**，复现出与基线一致、能跑通测试和一次真实模型请求的环境。
> 本文只回答"装什么、装成什么样、怎么证明装对了"。为什么这样设计，见 [stages/01-ENV.md](stages/01-ENV.md)。

**读者**：人或 AI。步骤按顺序执行，每一步都有"预期输出"，对不上就停下按 [第 11 节](#11-失败对照表) 查。

---

## 0. 先确认三件事

### 0.1 目录布局：四个仓库必须同级

```text
<项目根>/
├── Agent-development-doc/      ← 文档（纯 Markdown）
├── Agent-development-code/     ← 实现（Python）
├── GmSSL/                      ← 官方源码（要编译）
├── openssl/                    ← 官方源码（只做参考，不编译）
└── .local/gmssl/               ← 生成物：GmSSL 安装 prefix（本文第 5 步产生）
```

这个布局是硬约束，原因有两个：

1. 文档里的相对链接是 `../Agent-development-code/...`；
2. `packages/core/config.py` 里 `GMSSL_BIN` 的默认值是 `../.local/gmssl/bin/gmssl`，按**代码仓库根目录**解析相对路径。

所以**项目根放哪都行**（本文用 `/home/zsw/work/agent_development`），只要四个仓库和 `.local/` 的相对位置不变。换机器不用改任何配置。

### 0.2 在 WSL 里做，且不要放在 `/mnt/c`

基线是 Ubuntu 22.04 的 WSL2。**不要**把仓库放在 `/mnt/c`、`/mnt/d`：9P 文件系统下 `uv sync` 和 pytest 会慢数倍，还可能出现权限位丢失（`keys/` 要求 `0700`）。

Ollama 依赖 systemd。WSL2 默认没开 systemd 时，第 6 节的 `systemctl` 全部会失败，所以先确认 `/etc/wsl.conf` 里有：

```ini
[boot]
systemd=true
```

改完在 Windows 侧 `wsl --shutdown` 再进，`systemctl --version` 有输出才算生效。

### 0.3 是否需要 GPU

不强制。`qwen3.5:4b` 在 CPU 上也能跑，只是慢。基线机器是 RTX 5060 Ti（驱动 610.88）。没有 GPU 时把 `LLM_TIMEOUT_S` 调大即可。

---

## 1. 一键流程

放在这里方便复制；每一步的说明和预期输出在后面各节。

```bash
# 0) 项目根（可改，之后所有相对路径自动跟随）
export ROOT=/home/zsw/work/agent_development
mkdir -p "$ROOT" && cd "$ROOT"

# 1) 克隆四个仓库（第 2 节）
git clone https://github.com/prelearn-code/Agent-development-doc.git
git clone https://github.com/prelearn-code/Agent-development-code.git
git clone https://github.com/guanzhi/GmSSL.git
git clone https://github.com/openssl/openssl.git

# 2) 系统依赖（第 3 节）
sudo apt-get update && sudo apt-get install -y build-essential cmake git curl

# 3) uv + Python 3.12 + 依赖（第 4 节）
curl -LsSf https://astral.sh/uv/install.sh | sh
cd Agent-development-code
uv python install 3.12
uv sync --frozen --extra m1 --extra dev \
  --index-url https://pypi.tuna.tsinghua.edu.cn/simple   # 国内镜像；能直连 pypi 就删掉这行

# 4) 编译安装 GmSSL 到 ../.local/gmssl（第 5 节）
cd ../GmSSL
cmake -S . -B build -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_INSTALL_PREFIX="$ROOT/.local/gmssl"
cmake --build build -j"$(nproc)"
cmake --install build

# 5) Ollama + 模型（第 6 节）
curl -fsSL https://ollama.com/install.sh | sh
ollama pull qwen3.5:4b

# 6) 验收（第 9 节）
cd ../Agent-development-code
.venv/bin/python scripts/selftest.py --stage V1 --strict
.venv/bin/python -m pytest
```

---

## 2. 克隆四个仓库（并对齐版本）

```bash
cd "$ROOT"
git clone https://github.com/prelearn-code/Agent-development-doc.git
git clone https://github.com/prelearn-code/Agent-development-code.git
git clone https://github.com/guanzhi/GmSSL.git
git clone https://github.com/openssl/openssl.git
```

**写本文时的版本锚点**（要严格对齐就逐个 checkout；只跑通不追平可以不 pin）：

| 仓库 | 分支 | commit | 说明 |
|---|---|---|---|
| `Agent-development-code` | `main` | `5fbcedf61dbd78fcc1749a9a8b830b4936716dbe` | 实现；`uv.lock` 必须与它同期 |
| `Agent-development-doc` | `main` | `b8ed4c1812e1f9e728fca29ddf25f53b8b0e1459` | 文档 |
| `GmSSL` | `master` | `24ae482701a7b124826c382fffc55c19f76d475d` | 决定 `gmssl version` 显示的 `3.3.0-dev.1183` |
| `openssl` | `master` | `122db7eb076bf0625df87b91bcc2dccfaccc4900` | 仅源码参考，**不编译**；实际用的是系统 `/bin/openssl` |

```bash
git -C Agent-development-code checkout 5fbcedf61dbd78fcc1749a9a8b830b4936716dbe
git -C Agent-development-doc  checkout b8ed4c1812e1f9e728fca29ddf25f53b8b0e1459
git -C GmSSL                  checkout 24ae482701a7b124826c382fffc55c19f76d475d
git -C openssl                checkout 122db7eb076bf0625df87b91bcc2dccfaccc4900
```

> 仓库体积参考：`openssl/.git` 约 389 MB（`openssl` 的 `cloudflare-quiche`、`pyca-cryptography` 等空目录是未初始化的 submodule，**正常**，不要删）。

**验收**：

```bash
for r in Agent-development-{code,doc} GmSSL openssl; do
  echo "== $r"; git -C "$r" status --short --branch; git -C "$r" rev-parse HEAD
done
```

预期：四个仓库 `status` 无改动（GmSSL/openssl 落后上游若干 commit 是正常的，只表示没更新）。

---

## 3. 系统依赖

基线：Ubuntu 22.04.5 LTS，内核 `6.6.87.2-microsoft-standard-WSL2`，普通用户 `zsw`（有 sudo）。

```bash
sudo apt-get update
sudo apt-get install -y build-essential cmake git curl ca-certificates
```

| 包 | 基线版本 | 用途 |
|---|---|---|
| `build-essential` / gcc | 11.4.0 | 编译 GmSSL |
| `cmake` | 3.22.1 | 配置 GmSSL |
| `git` | 任意近版 | 克隆 |
| `curl` | 任意近版 | 装 uv / 验证 Ollama |

**不要**用 apt 装 Python 3.12（22.04 源里没有），也不要加 deadsnakes PPA——Python 由 uv 提供（第 4 节）。

**不要**用 apt 装 OpenSSL 开发包来"升级"系统 OpenSSL：项目用的就是 `/bin/openssl` 3.0.2。

**验收**：

```bash
cmake --version | head -1   # cmake version 3.22.1
gcc --version | head -1     # gcc (Ubuntu 11.4.0-...) 11.4.0
```

---

## 4. Python：uv + 3.12 + 项目依赖

### 4.1 装 uv

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
source "$HOME/.local/bin/env" 2>/dev/null || export PATH="$HOME/.local/bin:$PATH"
uv --version
```

基线 `uv 0.11.12`（`/home/zsw/.local/bin/uv`）。版本不严格，但太老的 uv 可能读不了当前 `uv.lock` 的格式；对不上就升到 0.11.x。

### 4.2 配镜像（国内网络必做）

`uv.toml` 的键是**顶层**的，不是 `[global]`（`[global]` 是 pip.conf 的写法，uv 会直接报 `unknown field 'global'`——本机旧配置就有这个问题，导致 uv 仍然去连 `pypi.org` 并超时）：

```bash
mkdir -p ~/.config/uv
cat > ~/.config/uv/uv.toml <<'EOF'
index-url = "https://pypi.tuna.tsinghua.edu.cn/simple"
EOF
```

等价写法：命令行 `--index-url https://pypi.tuna.tsinghua.edu.cn/simple`，或环境变量 `UV_INDEX_URL=...`。三者优先级：命令行 > 环境变量 > `uv.toml`。

### 4.3 建 venv 并同步依赖

```bash
cd "$ROOT/Agent-development-code"
uv python install 3.12          # 下载 uv 管理的 CPython；不装也行，uv sync 会自己下
uv sync --frozen --extra m1 --extra dev
```

三个关键点：

- **`--frozen`**：只按 `uv.lock` 装，不改 lock。复现必须带。
- **`--extra m1 --extra dev`**：`pydantic` 在 `m1`，`pytest/ruff/mypy` 在 `dev`。可选依赖**不会**自动装，漏了就报 `ModuleNotFoundError`。
- **`--index-url` 必须能被 uv 读到**：`uv sync` 会当场构建本项目（hatchling 构建后端），断网或走错索引会失败在 `No solution found when resolving: hatchling`。

同步后 `Agent-development-code/.venv/` 出现，`python` 指向 3.12。

**验收**：

```bash
.venv/bin/python -c 'import sys; print(sys.version)'        # 3.12.13 (...)
.venv/bin/python -c 'import pydantic, httpx, mcp, numpy; print(pydantic.__version__, httpx.__version__, numpy.__version__)'
# 2.14.1 0.28.1 2.5.4
uv lock --check                                              # Resolved 164 packages
```

> 不要用系统 `python3`（3.10.12）跑项目：`requires-python >= 3.12`，泛型语法和 `tomllib` 行为都不同。

### 4.4 配置文件 `.env`（可以跳过）

`.env` **不存在时全部走代码默认值**，基线机器上就没有 `.env`。要覆盖任何一项才创建：

```bash
cp .env.example .env      # 只填需要改的键，其余留空
```

- 键名必须与 `packages/core/config.py` 的 `Settings` 字段一致——`scripts/selftest.py` 会做**双向**比对（37 个键），少一个或多一个都会报"配置对齐"失败。
- 环境变量优先于 `.env`；改完要重启 Agent/MCP 进程。
- `.env` 已被 `.gitignore` 排除，**不要**提交，也不要把真实密钥写进去。

---

## 5. 编译安装 GmSSL 到 `../.local/gmssl`

`Agent-development-code` 调用的不是源码，而是**安装 prefix** 里的 `gmssl`：

```text
源码 ../GmSSL/          → 重新 clone 即可
构建 ../GmSSL/build/    → 重新 cmake 即可（本文结束可以删）
安装 ../.local/gmssl/   → 运行时立刻崩，配置指向这里
```

```bash
cd "$ROOT/GmSSL"
cmake -S . -B build -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_INSTALL_PREFIX="$ROOT/.local/gmssl"
cmake --build build -j"$(nproc)"
cmake --install build
```

- 必须用 `Release`（基线 `CMAKE_BUILD_TYPE=Release`，`BUILD_SHARED_LIBS=ON`）。
- `CMAKE_INSTALL_PREFIX` **必须是绝对路径**，且等于 `<项目根>/.local/gmssl`，否则 `GMSSL_BIN` 的默认相对路径找不到它。
- 其余 `ENABLE_*` 全部用 GmSSL 默认值即可（x86_64 下默认开 `ENABLE_SM2_AMD64`、`ENABLE_SM3_SSE`、`ENABLE_SM4_AVX2`）。**不要**改 `ENABLE_SM4_AESNI` 之类的加速开关——基线的 `sm2sign/sm2verify` 行为按默认配置验证过。
- 这里只构建库和 CLI，不跑 GmSSL 自带的 TLS 测试（那会额外产生 `build/` 里几十个 `.log`，与项目无关）。

**验收**：

```bash
"$ROOT/.local/gmssl/bin/gmssl" version
# GmSSL 3.3.0-dev.1183
ls "$ROOT/.local/gmssl/lib"
# libgmssl.so  libgmssl.so.3  libgmssl.so.3.3
```

`gmssl` **不在 PATH 是设计如此**，不要做 `ln -s /usr/local/bin/gmssl`。配置里 `GMSSL_BIN=../.local/gmssl/bin/gmssl` 负责定位。

> `gmssl version` 显示的 `dev.1183` 来自 `git describe`，只跟 checkout 的 commit 有关；不 pin commit 就可能是别的数字，不影响功能。

---

## 6. Ollama 与模型

Ollama 是**同机 systemd 服务**，应用通过回环 `127.0.0.1:11434` 访问。不要改成 `0.0.0.0` 或宿主 IP。

```bash
curl -fsSL https://ollama.com/install.sh | sh   # 装最新版；基线时为 0.32.15，qwen3.5 要求 >= 0.30.0
sudo systemctl enable --now ollama
ollama pull qwen3.5:4b
```

**验收**：

```bash
systemctl is-active ollama                                   # active
curl -s http://127.0.0.1:11434/api/version                   # {"version":"0.32.15"}
ollama list                                                  # qwen3.5:4b  3.3 GB
curl -s http://127.0.0.1:11434/api/tags | python3 -m json.tool | grep -A1 digest
```

完整 digest（基线，记下来用于对照权重）：

```text
qwen3.5:4b  d8b0f5e9760cd1682034f292d7ef72ec46f432149be0df7574bf2d6e92e38c04
size_bytes  3324173934        quantization  Q4_K_M
```

补充说明：

- 基线机器还装了 `qwen3.8:27b-q4_K_M`、`qwen3.8-agent-32k`、`qwen3-vl:4b`，**与本项目无关**，不用装。
- 拉不到 `qwen3.5:4b` 时（模型名不在公共库/需要权限），换一个支持 tools 的模型并改 `.env` 的 `CONTROLLER_MODEL`；此时"模型 digest 与基线一致"这一项验收会失败，属预期，记录差异即可。
- 模型文件在 `/usr/share/ollama/.ollama/models`（基线全量 23 GB），**不存在于项目目录**，不要试图复制。

---

## 7. OpenSSL：用系统自带的

```bash
openssl version     # OpenSSL 3.0.2 15 Mar 2022
command -v openssl  # /bin/openssl（Ubuntu 22.04 上 /usr/bin/openssl 是它的同源链接）
```

- 项目配置 `OPENSSL_BIN=/bin/openssl`，**只调用 CLI**，不链接 libcrypto。
- `openssl/` 仓库是**源码参考**，给 [reference/CLI-OPENSSL-HELP.md](reference/CLI-OPENSSL-HELP.md) 查手册用。**不编译它**，也不需要。
- 如果换了发行版（例如 24.04 自带 3.0.13），把 `.env` 里的 `OPENSSL_BIN` 指向实际路径，并在验收记录里写明版本差异。摘要类工具的输出只依赖算法，不依赖 3.0.x 小版本。

---

## 8. 本地运行数据（新克隆默认没有）

`data/` 和 `keys/` 被 `.gitignore` 排除，**克隆下来是空的**。测试会跳过依赖数据的用例，Agent 也无法演示。

```bash
cd "$ROOT/Agent-development-code"
mkdir -p data/file_002
cat > data/file_002/data.md <<'EOF'
# 教学样例

这是用于环境验收的样例文件。它的 SHA-256 由 OpenSSL CLI 计算，签名由 GmSSL 完成。
EOF
```

- `data/<file_id>/`：输入与密码产物，服务端按 `file_id` 解析，模型不能传路径。
- `keys/<key_id>/`：教学密钥，目录权限必须 `0700`，`key_id` 形如 `sm2_<32位十六进制>`。
- 跑完一次真实签名/加解密后，`file_001` 会多出 `ciphertext.der`、`decrypted.bin` 等产物（基线机器上有）。
- 这两个目录里的东西**不要**从旧机器复制，也不要提交；它们是要被重新生成的证据。

---

## 9. 验收：一条条核对

在 `Agent-development-code` 目录、激活 venv 后执行（或直接用 `.venv/bin/python` 前缀）：

| # | 命令 | 基线预期输出 |
|---|---|---|
| 1 | `python -c 'import sys;print(sys.version)'` | `3.12.13 (main, ...) [Clang 22.1.3]` |
| 2 | `uv lock --check` | `Resolved 164 packages` |
| 3 | `python -m ruff check .` | `All checks passed!` |
| 4 | `python scripts/selftest.py --stage V1 --strict` | `SUMMARY checks=10 fails=0 warns=0` |
| 5 | `python -m pytest` | `174 passed, 6 skipped in ~4.2s` |
| 6 | `../.local/gmssl/bin/gmssl version` | `GmSSL 3.3.0-dev.1183` |
| 7 | `/bin/openssl version` | `OpenSSL 3.0.2 15 Mar 2022` |
| 8 | `curl -s http://127.0.0.1:11434/api/version` | `{"version":"0.32.15"}` |
| 9 | `DSH_LIVE_TEST=1 python -m pytest -s tests/test_live_flow.py` | `6 passed`（真实模型 + MCP；默认 6 个用例是 skipped） |

第 5 步的 6 个 `skipped` **就是**第 9 步那 6 个 live 用例（默认跳过，需 `DSH_LIVE_TEST=1`）。

第 9 条是关键：它真的把问题发给 `qwen3.5:4b`、真的通过 stdio MCP 调 GmSSL/OpenSSL。跑它之前确认第 8 节的数据已建好，否则 `test_success_digest_matches_hashlib` 会因缺 `data/file_002/data.md` 跳过。基线里它长这样（节选）：

```text
[live] 问题：计算教学文件 file_002 里那个文件的 SHA-256 摘要
{
  "status": "completed",
  "run_id": "...",
  "answer": "... 摘要为 <64 位十六进制> ...",
  "evidence": [{"tool_name": "sha256_file", "ok": true, "result": {"digest_hex": "..."}}]
}
```

### 9.1 最小人工验收（不用 pytest）

```bash
.venv/bin/python -m packages.app status
# {"entry": "python -m packages.app", "entry_ready": true, ..., "network_requests": 0}

.venv/bin/python -m packages.app run --question '计算教学文件 file_002 里那个文件的 SHA-256 摘要'
# {"status": "completed", "run_id": "...", "answer": "...", "evidence": [...]}
```

`run` 返回 `status=completed`，且 `evidence[0].result.digest_hex` 等于下面这行，环境就算通了：

```bash
sha256sum data/file_002/data.md
```

---

## 10. 什么该复制、什么必须重新生成

**只复制/克隆四个仓库**（并且只克隆到 `main`/`master` 的提交）：

| 复制 | 说明 |
|---|---|
| 四个仓库的源码（含 `.git`） | 唯一事实来源 |
| `.env`（如果有） | 只在改过默认配置时需要；**不要**带真实密钥 |

**下面这些一律重新生成，不要从旧机器拷**：

| 生成物 | 生成方式 | 体积参考 |
|---|---|---|
| `.local/gmssl/` | 本文第 5 节 | 3.1 MB |
| `GmSSL/build/` | 本文第 5 节（可删） | 18 MB |
| `Agent-development-code/.venv/` | 本文第 4.3 节 | 191 MB |
| `__pycache__/`、`.pytest_cache/`、`.mypy_cache/`、`.ruff_cache/`、`.coverage`、`dist/` | 跑测试/打包自动产生 | 数 MB |
| `data/`、`keys/` | 本文第 8 节 + 跑一次 Demo | 200 KB 起 |
| Ollama 模型 | `ollama pull` | 3.3 GB（全量 23 GB） |

判断标准很简单：**`git status --ignored` 里出现的，都是生成物。**

---

## 11. 失败对照表

| 现象 | 是环境问题吗 | 处理 |
|---|---|---|
| `ModuleNotFoundError: pydantic` / `pytest` 找不到 | 是 | 漏了 `--extra`；`uv sync --frozen --extra m1 --extra dev` |
| `No solution found when resolving: hatchling` + `pypi.org` 超时 | 是 | 索引没配好；`--index-url` 镜像，或修 `~/.config/uv/uv.toml`（顶层 `index-url`，**不是** `[global]`） |
| `uv lock --check` 失败 | 是（配置） | `pyproject.toml` 与 `uv.lock` 不一致；查谁改的，别用 `uv lock` 覆盖 |
| `FileNotFoundError: .../.local/gmssl/bin/gmssl` | 是 | 第 5 节没做，或 install prefix 不是 `<项目根>/.local/gmssl` |
| `gmssl version` 不是 `3.3.0-dev.1183` | 是（版本） | GmSSL commit 不同；不影响功能，记录差异 |
| `Connection refused` 连 `127.0.0.1:11434` | 是 | `sudo systemctl start ollama`；`ss -ltnp \| grep 11434` |
| `404 model not found` | 是（配置） | `ollama list` 看真名；改 `CONTROLLER_MODEL` |
| `cmake: command not found` | 是 | 第 3 节 |
| pytest 慢到几十秒 / 权限位异常 | 是（布局） | 仓库放进了 `/mnt/c`；挪到 Linux 文件系统 |
| 模型答得不对 / 工具没被调用 | **不是** | 属行为问题，查 [TROUBLESHOOT.md](TROUBLESHOOT.md) 与对应阶段文档 |
| live 用例全 skip | 是（数据） | 第 8 节没建 `data/file_002/data.md`，或没设 `DSH_LIVE_TEST=1` |
| selftest 报"配置对齐"失败 | 是 | 改过 `Settings` 但没同步 `.env.example`，或反之 |

---

## 12. 已知缺口与基线差异

**设计上的缺口（不是错误）**：

1. `gmssl` 不在 `PATH`。定位由 `GMSSL_BIN` 负责；`command -v gmssl` 无输出是正常的。
2. `openssl/` 仓库未编译。只用系统 `/bin/openssl` 3.0.2。
3. `data/`、`keys/` 不入库，新克隆必须按第 8 节自建。

**与 [README.md](README.md) 里 2026-10-10 基线表的差异（以本文为准）**：

| 项 | README 旧记录 | 2026-10-29 实测 |
|---|---|---|
| GPU 驱动 | 591.86 | **610.88** |
| `ruff check .` | `packages/core/models.py` 有 5 个 UP 告警 | **`All checks passed!`**（已修，不再有基线告警） |
| 测试总数 | 未记 | **174 passed, 6 skipped** |

**没在本文验收范围内的**：V2 之后的数据库（Postgres）、向量库（Qdrant）、前端、Compose。它们由 [ROADMAP.md](ROADMAP.md) 对应阶段引入，各自的依赖在 `pyproject.toml` 的 `m2`/`m3`/`m4` extra 里，**这段环境不需要装**。

---

## 13. 给 AI 的执行提示

把下面这段连同四个仓库地址丢给另一台设备上的 AI：

```text
任务：在本机复现 /home/<user>/work/agent_development 下的开发环境。

1. 先读 Agent-development-doc/ENVIRONMENT.md，按第 2→9 节顺序执行。
2. 四个仓库必须同级，项目根自定（下文记作 ROOT）；布局和相对路径不能改。
3. 每个"验收"小节都要真的运行命令，并把真实输出贴出来；
   与基线不一致的项写进最后的差异清单，不要静默跳过。
4. 失败时先查 ENVIRONMENT.md 第 11 节，再查 Agent-development-doc/TROUBLESHOOT.md；
   不要为了"让它通过"去改测试、改 lock、放宽配置。
5. 约束：不要 apt install python3.12；不要生成 /usr/local/bin/gmssl 软链；
   不要从别的机器拷贝 .venv / .local / data / keys / 模型权重。
6. 完成后报告：
   - 四个仓库的 commit
   - 第 9 节 9 条验收的真实输出
   - 与基线的差异（版本号、模型 digest、跳过项）
   - 卡住过的地方和解决办法

仓库：
  https://github.com/prelearn-code/Agent-development-code.git
  https://github.com/prelearn-code/Agent-development-doc.git
  https://github.com/guanzhi/GmSSL.git
  https://github.com/openssl/openssl.git
```

---

## 附：基线环境快照（2026-10-29 实测）

```text
发行版      Ubuntu 22.04.5 LTS（WSL2，内核 6.6.87.2-microsoft-standard-WSL2）
用户        zsw（uid 1000，非 root，sudo 组）
系统 Python 3.10.12
uv          0.11.12（~/.local/bin/uv）
项目 Python 3.12.13（uv 管理：~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu）
cmake       3.22.1
gcc         11.4.0
OpenSSL     /bin/openssl 3.0.2
GmSSL       .local/gmssl/bin/gmssl 3.3.0-dev.1183（libgmssl.so.3）
Ollama      0.32.15（/usr/local/bin/ollama，systemd，127.0.0.1:11434）
模型        qwen3.5:4b  d8b0f5e9…  Q4_K_M  3324173934 B
GPU         RTX 5060 Ti  驱动 610.88
磁盘        /home 1007 G（已用 149 G）
```
