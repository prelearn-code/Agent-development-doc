# V0 环境准备

本阶段基础预算**20h**；实现成果：新终端可复现环境、模型请求与首个测试。先读实现目标与当前切片，再执行详细任务；完成标准以实际证据为准。

| 入口问题 | 本阶段安排 |
|---|---|
| 从哪里开始 | 环境检查P0 01，已有环境也先核对 |
| 首次进入的任务 | P0 01、P0 02、P0 03、P0 04、P0 05；可能只实现本阶段范围，完整版完成位置见任务索引 |
| 完整技术目标卡 | Phase 0；跨阶段项目以后补齐，不将全表当当前前置 |
| 如何判断完成 | 正常/失败/权限与真实结果可核对，本人能解释、改需求和排错；本章出口清单全部有证据 |
| 按需参考 | [01-ENVIRONMENT.md](../reference/01-ENVIRONMENT.md)；[06-CRYPTO-AGENT-SCOPE.md](../reference/06-CRYPTO-AGENT-SCOPE.md) |

每个技术目标的第一张表说明能力深度，紧接的实践表说明具体练习；两者在此集中阅读。通用周计划/任务卡见[学习总览](../LEARNING-PATH.md)，原M1–M6查[任务索引](../reference/TASK-INDEX.md)。

## 真实起点与操作约定

### 2026 年 10 月 10 日只读核对结果

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
| 依赖锁 | 核对时未发现 `uv.lock` | Phase 0 生成并核对锁文件 |
| GmSSL | 尚未验证安装状态 | Phase 0 后段或 M1 按选定路线安装验证 |

这是一次起点记录，不代表已经完成 Phase 0。机器状态可能变化，学习开始时按下面命令重新检查。后续以 Ubuntu 工作目录为开发现场。

### 所有开发命令在 Ubuntu Bash 中执行

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

预期最后一行指向实现仓库的 `.venv/bin/python`，版本为 3.12.x。没有虚拟环境时先做 Phase 0 的环境任务。

已有仓库同步时先看 `git status`，工作区干净再 `git pull --ff-only`。有自己的修改时先决定提交、保留或合并，不执行覆盖式 reset，也不把 clone 命令运行到已存在的目录上。

### 先理解目录与接口的区别

当前骨架使用 `packages/core`、`tools`、`minimal_agent` 等目录；[repo-structure.md](../reference/repo-structure.md) 还给出了 `src/lpa` 的目标布局。第一天沿用现有骨架，**不要为了看起来整齐搬动全部文件**。后续V2/V4如果选择调整包布局，必须同步导入路径、打包配置、结构文档和 `selftest.py`。

特别注意顶级 `mcp/` 目录可能遮蔽第三方 SDK，`agent-api` 也不能直接当 Python 包名导入。落地时选择合法包名并验证 `import` 来源；指南中的业务模块名称表示职责，不保证当前已经存在对应命令入口。

### 如何判断学会了

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

“可后置内容”不纳入本阶段必过条件，也不要求先学完才能动手。表中的练习与阶段任务配合使用，按相应阶段的工时与业务验收指标执行。每行记录“待学 / 在做 / 已验证”及证据路径，不能用看完视频、阅读时长或主观掌握百分比替代结果。密码工具的具体掌握标准另见 [领域范围文档](../reference/06-CRYPTO-AGENT-SCOPE.md)。


### Phase 0：Ubuntu 与最小工程地基（20h）

**进入条件**：V0开始；能使用Ubuntu终端，零基础按本阶段步骤操作，依赖细节查环境参考。

**Agent目标**：建立可复现环境，分清环境故障、协议故障与模型问题。 对应详细任务：**P0 01–05**。

**技术点掌握程度标准**

| 技术点 | 能解释 | 独立做到 | 排错与边界 | 验收证据 | 后置内容 |
|---|---|---|---|---|---|
| Ubuntu/路径/权限 | cwd、绝对路径、用户权限、进程与端口 | 在ext4工作目录操作，确认四仓库同级，区分源码与安装前缀 | 文件缺失、权限不足、端口占用能分类 | 路径图与版本/端口记录 | 内核调优 |
| Git | 工作区、暂存、commit、branch与remote | 看diff、提交一次变化并检查远端分支 | 识别未提交改动与冲突，不覆盖未知修改 | 一次提交与自己的解释 | 复杂历史重写 |
| Python/uv/配置 | 解释器、venv、依赖声明、lock与环境变量 | 从新终端恢复固定依赖，配置样例不含秘密 | 找出装在另一Python、配置未加载的问题 | 解释器路径、lock与复测命令 | 发布Python包 |
| HTTP/JSON/Ollama | 请求、状态码、超时与响应字段 | 发一次真实非流式请求，读取消息/模型/计量 | 分开连接失败、HTTP失败、JSON失败与模型错误 | 脱敏原始请求响应 | 推理优化与全模型矩阵 |
| 测试/日志 | 输入、预期、断言与关联标识 | 跑首个确定性测试和lint，保存真实版本 | 能定位断言失败，不凭截图判通过 | 命令、退出码与修复记录 | GPU CI体系 |

**学习与实现顺序**：①P0 01检查已有环境；②P0 02固定依赖与lock；③P0 03真实模型请求；④P0 04配置与测试；⑤P0 05选择Provider路线。DB/向量库到对应阶段启动，不一次安装所有模型。

**必须独立回答**：为什么新终端可能使用另一解释器？连接失败和错误模型名有什么区别？源码目录为什么与安装前缀分开？

**独立练习**：换一个终端复测；使用错误端口和错误模型名分别观察报错，修正后保留对照。

**退出条件**：最小请求与测试真实通过；路径和版本可复现，Provider未验证能力明确记录；标记phase0-done，不要求容器GPU直通。

**目标**：从新终端能启动正确的 Python 环境、请求本机 Ollama、运行至少一个你理解的测试。预算 20h，暂不启动数据库、向量库和前端。

### 要学的内容

**技术点掌握程度标准**

| 技术点 | 本阶段必须能独立做到 | 练习与验收证据 | 可后置内容 |
|---|---|---|---|
| Ubuntu Bash、文件与权限 | 用 pwd/cd/ls 找到四个同级仓库；理解相对/绝对路径、读写执行权限；定位文件而不凭目录名猜测 | 从新终端进入实现仓库，记录目录与受控样本权限，解释源码目录与安装前缀区别 | 复杂 shell 脚本、内核与系统管理 |
| 进程、端口与日志 | 区分“进程存在”“端口监听”“请求可用”；能用进程/监听信息与日志定位服务未启动或地址错误 | 保存一次服务正常请求与一次错误地址的排查记录 | systemd 单元编写后置到部署；网络协议栈细节选修 |
| Git | 看懂 status/diff/log；知道本地改动、提交、远端的区别；能提交本人改动、使用阶段 tag，更新前先检查工作区 | 为环境记录做一次可解释的 diff 和提交，说明 pull --ff-only 的失败含义 | rebase、复杂冲突与 Git 内部对象 |
| Python、venv 与 uv/lock | 分清系统解释器和项目解释器；按阶段同步依赖；解释 pyproject 与 lock 的职责 | 新终端下记录解释器、包版本和 lock，定位一次错误解释器造成的导入失败 | 包发布、复杂多平台依赖解析 |
| HTTP 与 JSON | 解释方法、URL、header、body、状态码和超时；用 curl 发请求并定位 JSON 字段 | 保存 P0 03 原始请求/响应，指出 messages、content、结束标志；连接失败与 HTTP 错误分别记录 | HTTP/2、代理调优、复杂网络抓包 |
| pytest 入门 | 自己写一个确定性断言和一个预期异常；能运行指定测试、读失败位置，识别未收集测试 | P0 04 测试先因预期错误失败，再修复通过；保存测试文件与结果 | fixtures、参数化在 M1 学；插件开发选修 |
| Settings、环境变量与秘密 | 说明模板和本地配置差别；查出当前有效配置来源；识别不能提交的秘密字段 | 配置检查结果与提交 diff，无实际口令或密钥；演示一个缺少配置的明确错误 | 密钥托管与配置中心 |
| Provider 路线与版本 | 区分源码仓库、CLI、C 共享库和 Python 绑定；知道系统 OpenSSL 与 Python 后端可能不同 | P0 05 路线记录，列出已验证版本与尚未验证能力，不将“可导入”记为功能通过 | 此阶段不要求读密码库源码、实现算法或完成 CA |

停止学习这些概念的条件是能完成本阶段任务。Shell 脚本高级技巧、Docker 全套知识和深度模型原理可在后续按需学习。

### P0 01 检查已有环境

工作目录：实现仓库。逐条运行，遇到不存在的命令时记录缺口，不把命令输出错误忽略掉。

```bash
cd /home/zsw/work/agent_development/Agent-development-code
git status --short --branch
python3 --version
uv --version
openssl version
command -v gmssl || true
systemctl is-active ollama
curl --fail --show-error http://127.0.0.1:11434/api/version
ollama list
```

`gmssl` 暂时没有不阻塞最小环境验收；先完成 OpenSSL 只读业务。Ollama 连接失败先检查 service、11434 端口与日志，不改成 Windows 宿主 IP。

### P0 02 安装本阶段依赖并固定环境

已有 `.venv` 且版本正确时保留；缺失时才运行 `uv venv --python 3.12 .venv`。第一次生成锁文件与安装：

```bash
cd /home/zsw/work/agent_development/Agent-development-code
source .venv/bin/activate
python --version
uv sync --extra m1 --extra dev
python -c 'import pydantic, httpx; print(pydantic.__version__, httpx.__version__)'
python3 scripts/selftest.py
git status --short
```

生成并检查 `uv.lock`，后续复现使用 `uv sync --frozen --extra m1 --extra dev`。项目的 `dev` 当前是 optional extra，不能假设省略 `--extra dev` 就会安装它。阶段依赖逐步叠加，M2 起保留 m1，不能只同步 m2 后把前面的依赖移除。参见 [uv 依赖管理](https://docs.astral.sh/uv/concepts/projects/dependencies/)。

当前骨架没有业务测试；`selftest.py` 只验证结构与配置一致性。pytest 显示“没有收集到测试”不算通过。你要在 P0 04 写一个真正执行了断言的测试。

### P0 03 做最小模型请求

先确认 `ollama list` 有 `qwen3.5:4b`。没有时才 `ollama pull qwen3.5:4b`。以下只发送无秘密的练习内容，输出放在本地数据目录：

```bash
cd /home/zsw/work/agent_development/Agent-development-code
mkdir -p data/learning/phase0
curl --fail --show-error --max-time 180 \
  http://127.0.0.1:11434/api/chat \
  -H 'Content-Type: application/json' \
  -d '{"model":"qwen3.5:4b","messages":[{"role":"user","content":"用一句话说明文件摘要和文件加密的区别。"}],"stream":false,"think":false,"options":{"temperature":0,"num_ctx":8192}}' \
  -o data/learning/phase0/chat-response.json
python -m json.tool data/learning/phase0/chat-response.json
```

查看 `message.content`、`done`、模型名和实际返回的 token/耗时字段。不把回答当技术结论的权威来源，这里验收的是请求确实完成、JSON 能解析。记录实验参数；`think` 支持情况以实际模型信息和后端版本为准，参见 [Ollama Chat API](https://docs.ollama.com/api/chat)。

### P0 04 写首个测试与环境记录

先独立写一个不依赖模型的测试：加载测试 Settings，断言本机 Ollama 地址和模型配置正确；不要让测试依赖含真实口令的 `.env`。再写一个简单输入校验例子，非法输入得到你预期的错误。

运行入口：

```bash
cd /home/zsw/work/agent_development/Agent-development-code
source .venv/bin/activate
python -m pytest -q
python -m ruff check .
```

把真实版本、模型 ID/digest、CPU/GPU 路线、Python 路径、lock hash 和推理配置写入 `environment.lock.json`。摘要或随机 ID 不能替代模型完整 digest；CLI 只显示短 ID 时继续查询实际模型元数据，记录来源。环境记录不写口令或完整秘密配置。

### P0 05 确定 OpenSSL 和 GmSSL 路线

OpenSSL：只读证书操作可先用 CLI；Python 密码操作可用 `cryptography` 作为 OpenSSL-backed 适配入口。Python 包的 OpenSSL 后端和系统 `openssl` 命令不保证同版本，分别记录并验证。

GmSSL：选择官方 C 库及官方 GmSSL-Python 绑定，或者选定版本的官方 CLI。先阅读 [GmSSL 官方仓库](https://github.com/guanzhi/GmSSL) 与 [GmSSL-Python](https://github.com/GmSSL/GmSSL-Python)。不要因为导入名同为 `gmssl` 就直接装任意同名包；锁定来源、C 库和绑定版本。具体密码能力的范围见 [06-CRYPTO-AGENT-SCOPE.md](../reference/06-CRYPTO-AGENT-SCOPE.md)。

这一步只需确定方案并验证版本/帮助入口。不要第一天实现全部算法与证书签发。如果 GmSSL 编译成为阻塞，登记缺口，先用 OpenSSL 完成 Loop，按当前可用能力先推进；SM3在V1可用时补，安装确实阻塞则登记到V6补齐，不伪称GmSSL已验证。

### 本阶段验收指标

| 指标 | 通过条件 | 留存证据 |
|---|---|---|
| 环境一致性 | 新终端下 Python 指向 `.venv`，版本为 3.12.x | 版本与路径输出 |
| 模型连通 | 一次 `/api/chat` 返回可解析内容与结束标志 | 原始 JSON |
| 测试入口 | 至少一个已收集并执行的确定性测试通过 | pytest 结果与测试位置 |
| 配置 | Settings 与样例一致，模板与提交文件无真实秘密 | selftest 与 diff |
| 复现记录 | 有 lock、实际版本与模型配置 | 环境记录 |
| 理解 | 能解释为何不用系统 Python、为何 Ollama 用回环地址 | 自己的说明 |

全部通过后再创建 `phase0-done`。下一步V1的M1 01–02只读契约与证书适配。

> 上述2026年10月10日记录是历史快照。2026年10月12日Windows代码仓库已增加薄CLI入口和合同测试，真实工具/LLM/Loop仍待实现；Ubuntu仓库当前状态由本人同步后重新核对，历史的“未发现测试”不是今天的结论。


## 本阶段签收清单

- [ ] P0 01–05真实复测，版本/解释器/lock/请求/首测可定位。
- [ ] 本人能区分配置、连接、协议和模型错误，V0出口通过。

## 下一步

本阶段出口有证据后进入[V1阶段](V1-CORE-DEMO.md)。跨阶段未完标准登记补齐位置。
