# V0 环境准备

本阶段基础预算**20h**；实现成果：新终端可复现环境、模型请求与首个测试。先读实现目标与当前切片，再执行详细任务；完成标准以实际证据为准。

## 实现目标与学习结果要求

建立一个可以从新终端恢复的Ubuntu开发环境，完成一次真实模型请求和首个确定性测试。已有软件先核对；这个阶段不安装全部服务，也不实现业务Loop。环境说明、版本记录和四仓库布局统一见README。

| 需要学习的技术 | 学习结果要求 | 独立实现与排错证据 |
|---|---|---|
| Ubuntu终端、路径、进程与权限 | 能定位实现仓库、解释cwd与绝对路径、识别进程/端口和文件权限 | 新终端复测；错误路径、权限不足或端口占用能分类 |
| Git与四仓库布局 | 理解工作区/暂存/提交/远端；确认文档、代码、OpenSSL和GmSSL同级 | 看一次diff并解释；未提交改动不被同步覆盖 |
| Python3.12、uv、venv、依赖锁 | 识别实际解释器、依赖声明和锁；从新终端恢复相同环境 | 保存解释器路径/版本与lock；定位装到另一Python的问题 |
| HTTP、JSON、Ollama非流式请求 | 独立发送一次请求，解释模型名、消息角色、状态码、响应内容与计量 | 保存脱敏请求/响应；连接错误、HTTP错误与解析错误分别验证 |
| 配置、日志、pytest与lint | 加载配置样例，写一个有真实断言的测试，运行检查并定位失败 | 命令/退出码/修复记录可定位；日志无秘密 |
| Provider能力与版本记录 | 区分OpenSSL系统CLI、库后端和GmSSL绑定，记录已验证与未验证能力 | 不把导入成功或目录存在当能力验证；版本与安装prefix单独记录 |

## 必须独立回答的关键问题

这些问题必须由你结合自己的实现作答，AI只审查。记录在代码仓库docs/progress.md，写清场景、自己的理由、真实证据与未覆盖边界；只背定义或复制AI答案不算通过。

| 编号 | 必须自己回答的问题 | 回答达到标准所需的说明或证据 |
|---|---|---|
| Q01 | 当前终端究竟位于哪个仓库？怎样证明没有误用另一个目录？ | 给出pwd、Git远端与解释器路径，并画四仓库层级 |
| Q02 | 文档、代码、OpenSSL和GmSSL为什么各自保留独立Git历史？ | 解释一次文档更新与一次库版本锁定的影响范围 |
| Q03 | 源码目录、构建目录、安装prefix与虚拟环境分别保存什么？ | 标出实际路径和后续删除/重建时会影响什么 |
| Q04 | 系统python3与项目python能是不同版本吗？你如何选择正确的那个？ | 展示实际版本、sys.executable与激活前后对照 |
| Q05 | uv依赖声明、uv.lock和venv分别解决什么问题？ | 说明新终端或新目录复现的操作顺序与失败位置 |
| Q06 | git pull前为什么检查工作区？已有自己的代码时如何保留？ | 解释未提交修改、提交与合并，不给出覆盖式同步 |
| Q07 | Ollama服务正常但请求失败，至少有哪些不同原因？ | 区分监听地址、端口、模型名、HTTP状态与请求字段 |
| Q08 | 普通JSON解析失败与网络请求失败怎么区分？ | 用两个受控错误说明捕获位置和记录内容 |
| Q09 | 一条普通模型请求的输入、输出和耗时计量分别在哪里？ | 标注真实请求/响应，不能只展示最终聊天文本 |
| Q10 | 配置值来自哪些位置？怎么证明加载的是你期望的配置？ | 说明默认值/环境变量/样例关系并提供脱敏检查 |
| Q11 | 一个测试运行了却没有断言，能证明什么？pytest没有找到测试如何处理？ | 指出测试入口、断言与真实失败，不把无测试当成功 |
| Q12 | 为什么日志和环境说明也可能泄露秘密？ | 列出自己记录中需要删去或脱敏的字段 |
| Q13 | OpenSSL CLI与Python密码包可能使用不同后端吗？ | 分别记录真实版本与能力检查，解释不可互相替代的证据 |
| Q14 | 为什么第一个Demo不需要先启动数据库、向量库和三个MCP Server？ | 按阶段说明每项依赖首次解决的问题 |
| Q15 | Windows代码入口检查与Ubuntu密码业务测试分别证明什么？ | 列出已验证/未验证，不能将静态检查当真实运算 |
| Q16 | 换一个终端后如何重新证明V0完成？ | 提供一套实际复测记录、失败对照与未验证清单 |

## 分步任务与技术掌握标准

先按当前切片实现最小输入输出，再补齐技术表。本阶段首次运行、正常/失败/权限、本人解释与独立修改分别验收；未实际运行不签收。

### Phase 0：Ubuntu 与最小工程地基（20h）

**进入条件**：V0开始；能使用Ubuntu终端，零基础按本阶段步骤操作，依赖细节查README环境说明。

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

GmSSL：选择官方 C 库及官方 GmSSL-Python 绑定，或者选定版本的官方 CLI。先阅读 [GmSSL 官方仓库](https://github.com/guanzhi/GmSSL) 与 [GmSSL-Python](https://github.com/GmSSL/GmSSL-Python)。不要因为导入名同为 `gmssl` 就直接装任意同名包；锁定来源、C 库和绑定版本。具体密码能力的范围见 [密码工具学习合同](V1-CORE-DEMO.md#crypto-3.1)。

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

## 本阶段的接口与实践细节

以下内容属于本阶段，按任务用到的部分查阅；涉及后续能力的字段仅作为扩展合同，当前切片不要求提前全部实现。

<a id="full-phase0"></a>
<a id="full-phase0-phase020h"></a>
#### Phase0（20h）

- [ ] 应用独立目录、Git、Python3.12/uv/venv、合法pyproject/lock。
- [ ] Ollama与qwen3.5:4b能完成最小请求，保存版本/digest与GPU/CPU实测状态。
- [ ] 配置样例、脱敏日志、测试与lint入口、实际工时记录。
- [ ] Phase0无需一次装4模型/启动4服务，核心验收通过，phase0-done。

## 本阶段签收清单

- [ ] 本阶段学习技术表逐项有本人解释、独立实现/修改和失败验证证据。
- [ ] Q01–Q16已由本人结合实现作答，证据与未覆盖边界记入docs/progress.md；AI仅审查。

- [ ] P0 01–05真实复测，版本/解释器/lock/请求/首测可定位。
- [ ] 本人能区分配置、连接、协议和模型错误，V0出口通过。

## 下一步

本阶段出口有证据后进入[V1阶段](V1-CORE-DEMO.md)。跨阶段未完标准登记补齐位置。
