# 01. 环境准备（20h）

> 完成这一段，你能做到：**新开一个终端，三分钟内恢复出正确的解释器、依赖、模型和密码工具，并用一条真实请求证明它们都通。**

这一段不写业务代码。它的产出是一份**可复现的环境记录**——后面每一段出问题，你都要靠它区分"环境坏了"还是"代码坏了"。

---

## 在流程中的位置

[FLOW.md](../FLOW.md) 里所有环节的前置。这一段不通，后面每一步的失败都无法归因。

前置：无。解锁：02 段需要的模型请求、OpenSSL 调用、pytest 入口。

---

## 要写的代码

这一段**几乎不写代码**，主要是确认和记录：

| 文件 | 职责 | 现状 |
|---|---|---|
| `.venv/` | 项目解释器（Python 3.12） | 已有 |
| `uv.lock` | 依赖锁 | 已有 |
| `tests/test_crypto_config.py` 等 | 现有测试 | 已有 |
| `environment.lock.json` | **环境快照**（这一步的主要产出） | 需新建 |
| `data/learning/v0/chat-response.json` | 一次裸模型请求的原始响应 | 需新建 |
| `tests/test_env_contract.py` | 断言默认配置正确 | 需自己写 |

---

## 核心概念

### 1. 系统 Python 和项目 Python 是两个东西

Ubuntu 22.04 自带 **3.10.12**，项目要 **3.12**。用 `uv venv --python 3.12` 让它自己下载，**不要** `apt install`（源里没有 3.12，加 deadsnakes PPA 会污染系统）。

判断你现在用的是哪个：

```bash
python -c 'import sys; print(sys.executable, sys.version)'
```

必须指向 `.../Agent-development-code/.venv/bin/python`。不指向就是没激活，或者装了两次。

### 2. `pyproject.toml` / `uv.lock` / `.venv` 三者分工

| 文件 | 是什么 | 类比 |
|---|---|---|
| `pyproject.toml` | **声明**需要哪些包、什么版本范围 | 购物清单 |
| `uv.lock` | **锁定**每个包的确切版本 + hash | 小票，能精确复现 |
| `.venv/` | **实际安装**出来的目录 | 冰箱里的东西 |

复现用 `uv sync --frozen`：只按 lock 装，不改 lock。不带 `--frozen` 会重新解析，可能拿到新版本。

`dev` 是 optional extra，**省略 `--extra dev` 就不会装** pytest/ruff/mypy。完整同步：

```bash
uv sync --extra m1 --extra dev
```

### 3. Ollama 是 Ubuntu 的 systemd 服务，走回环

`127.0.0.1:11434`。不要改成 `0.0.0.0`，也不要改到 Windows 宿主 IP——容器需要访问时用 `network_mode: host`。

`qwen3.5:4b` 要求 Ollama ≥ 0.30.0（本机 0.32.15）。它是**统一多模态**模型（文本+图像，256K 上下文，原生 tools 与 thinking），所以不需要单独部署视觉模型。

出厂采样参数是 `temperature=1 / top_p=0.95 / top_k=20 / presence_penalty=1.5`。**记录它们**，和消融实验的配置分开报告。

### 4. 源码目录 / 构建目录 / 安装 prefix 是三件事

| 概念 | 本例 | 删掉会怎样 |
|---|---|---|
| 源码 | `../GmSSL/` | 重新 clone 即可 |
| 构建 | `../GmSSL/build/` | 重新 cmake 即可 |
| 安装 prefix | `../.local/gmssl/` | **运行时立刻崩**（配置指向这里） |
| 虚拟环境 | `Agent-development-code/.venv/` | 重新 `uv sync` |

配置里 `GMSSL_BIN` 默认是 `../.local/gmssl/bin/gmssl`，不是源码目录。

### 5. 五种"失败"要分得开

后面每一段都会遇到，现在先建立分类习惯：

| 现象 | 是环境问题吗 | 先查 |
|---|---|---|
| `ModuleNotFoundError` | 是 | 解释器路径、extras 装没装 |
| `Connection refused` | 是 | `systemctl is-active ollama`、端口 |
| `404 model not found` | 是（配置） | `ollama list` 里的真名 |
| HTTP 500 / 响应字段缺失 | 不一定 | 服务端日志、请求体 |
| 模型答得不对 | **不是** | 这条不属于环境 |

---

## 分步实现

### 步骤 1 核对起点

```bash
cd /home/zsw/work/agent_development/Agent-development-code
pwd
git status --short --branch
python3 --version
uv --version
openssl version
command -v gmssl || true
systemctl is-active ollama
curl --fail --show-error http://127.0.0.1:11434/api/version
ollama list
```

**预期**（本机实测，2026-10-10）：

```text
/home/zsw/work/agent_development/Agent-development-code
## main...origin/main
Python 3.12.13          ← 注意：这是 uv 管理的，不是系统的 3.10.12
uv 0.11.12
OpenSSL 3.0.2 15 Mar 2022
active
{"version":"0.32.15"}
qwen3.5:4b  3.3 GB
```

**`gmssl` 不在 PATH 是正常的**，不阻塞。实际二进制在 `../.local/gmssl/bin/gmssl`。但**必须在环境记录里写下这个缺口**，不要当成"没这回事"。

### 步骤 2 恢复依赖

```bash
source .venv/bin/activate
python -c 'import sys; print(sys.executable)'
uv sync --frozen --extra m1 --extra dev
python -c 'import pydantic, httpx; print(pydantic.__version__, httpx.__version__)'
uv lock --check
```

**预期**：`pydantic 2.14.1 | httpx 0.28.1`，`uv lock --check` 输出 `Resolved N packages` 且退出 0。

如果 `uv lock --check` 失败，说明 `pyproject.toml` 和 `uv.lock` 不一致——先查是谁改的，不要直接 `uv lock` 覆盖。

### 步骤 3 一次裸模型请求（不经过任何项目代码）

```bash
mkdir -p data/learning/v0
curl --fail --show-error --max-time 180 \
  http://127.0.0.1:11434/api/chat \
  -H 'Content-Type: application/json' \
  -d '{"model":"qwen3.5:4b","messages":[{"role":"user","content":"用一句话说明文件摘要和文件加密的区别。"}],"stream":false,"think":false,"options":{"temperature":0,"num_ctx":8192}}' \
  -o data/learning/v0/chat-response.json
python -m json.tool data/learning/v0/chat-response.json
```

**为什么必须用 curl 而不是项目入口**：这一步验证的是"模型服务本身通不通"。经过项目代码就多了一层，出问题时你分不清是模型的问题还是代码的问题。

**要能指出响应里这几个字段**：`message.content`（回答）、`message.role`、`done`（是否结束）、模型名、以及 token/耗时计量字段（如 `prompt_eval_count` / `eval_count` / `total_duration`）。

注意 `think:false` 的作用：固定它，否则 token 消耗无法跨配置比较。

### 步骤 4 写一个自己理解的测试

要求：**不依赖模型、不依赖 `.env`**，断言默认配置正确。

```python
# tests/test_env_contract.py
from packages.core.config import Settings


def test_defaults_point_to_local_ollama_and_model() -> None:
    s = Settings(_env_file=None)          # 不读 .env，测的是代码默认值
    assert s.OLLAMA_BASE_URL == "http://127.0.0.1:11434"
    assert s.CONTROLLER_MODEL == "qwen3.5:4b"
    assert s.LLM_NUM_CTX == 8192
    assert s.LLM_THINK is False
```

先让它**失败一次**（比如故意把 `8192` 写成 `8193`），看 pytest 报什么，再改回来。没经历过一次红，你不会用这个入口排错。

```bash
python -m pytest tests/test_env_contract.py -q
python -m pytest -q
python -m ruff check .
```

> `ruff check .` 当前有 5 个基线告警，全在 `packages/core/models.py`（UP035/UP017/UP046/UP037×2）。**记录下来**，不要为了清零去改契约文件。

### 步骤 5 写 `environment.lock.json`

这是本段最重要的产出。文档不写死格式，但必须包含：

```json
{
  "recorded_at": "2026-10-10",
  "os": {"distro": "Ubuntu 22.04.5 LTS", "kernel": "6.6.87.2-microsoft-standard-WSL2"},
  "python": {"executable": "/home/zsw/.../.venv/bin/python", "version": "3.12.13"},
  "uv": {"version": "0.11.12"},
  "lock": {"file": "uv.lock", "sha256": "<自己算>"},
  "ollama": {"version": "0.32.15", "endpoint": "http://127.0.0.1:11434"},
  "model": {"name": "qwen3.5:4b", "digest": "<完整 sha256，不是短 ID>", "size_bytes": 0, "quantization": "Q4_K_M"},
  "sampling": {"temperature": 1, "top_p": 0.95, "top_k": 20, "presence_penalty": 1.5},
  "openssl": {"path": "/bin/openssl", "version": "3.0.2"},
  "gmssl": {"path": "../.local/gmssl/bin/gmssl", "version": "3.3.0-dev.1183", "in_path": false},
  "gpu": {"model": "RTX 5060 Ti", "driver": "591.86"},
  "known_gaps": ["gmssl 不在 PATH", "packages/core/models.py 有 5 个 ruff 告警"]
}
```

取模型完整 digest：

```bash
ollama show qwen3.5:4b --modelfile | head -5
# 或
curl -s http://127.0.0.1:11434/api/tags | python -m json.tool | grep -A2 qwen3.5:4b
```

**为什么必须记完整 digest**：`ollama list` 只显示短 ID，而模型可以被覆盖重拉。现在不记，以后就无法证明你当时的实验用的是哪份权重。

算 lock hash：

```bash
sha256sum uv.lock
```

---

## 常见坑

1. **新终端忘了 activate。** 报错信息一模一样，但解释器是系统的 3.10.12。先跑 `python -c 'import sys;print(sys.executable)'`。
2. **省略 `--extra dev` 导致 pytest 找不到。** `dev` 是 optional extra，不会自动装。
3. **`uv sync` 不带 `--frozen` 悄悄升级了依赖。** 复现时必须带。
4. **把 `gmssl` 不在 PATH 当成"没装"。** 二进制在 `../.local/gmssl/bin/`，配置里指向那里就行。
5. **模型回答不好就去调 temperature。** 这一段验收的是"请求完成且 JSON 可解析"，回答质量不归这一段管。
6. **`data/learning/` 是 git 忽略的。** 环境记录的原始 JSON 放这里，不要把大文件提交。
7. **拿 `ollama list` 的短 ID 当 digest。** 短 ID 会碰撞、会被覆盖。

---

## 自检问题

1. 当前终端位于哪个仓库？怎样用三条命令证明没有误用另一个目录？
2. 系统 `python3` 和项目 `python` 版本不同，你怎么选对的那个？激活前后 `sys.executable` 分别是什么？
3. `pyproject.toml`、`uv.lock`、`.venv` 各解决什么问题？换台机器复现的顺序是什么？
4. Ollama 服务正常但请求失败，至少能列出几种不同原因？分别怎么查？
5. `gmssl` 不在 PATH，为什么后续功能还能用它？配置里的哪个字段决定了这一点？

---

## 本人记录

> 每段结束时补。写自己的话，不抄。

```text
日期：
实际工时：
环境是否与基线一致（不一致的项）：
卡住过的地方 & 怎么解决的：
还没理解的：
下次入口：
```
