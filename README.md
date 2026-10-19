# 密码工具 Agent 全栈开发

用 OpenSSL / GmSSL 的**确定性密码工具**，走一遍 AI Agent 的完整开发链路：

```text
用户提问 → 模型提议工具调用 → 程序授权 → 固定程序执行
        → 真实结果回传 → 持久化 → 前端展示
```

目标不是"跑起来一个 demo"，而是**能说清每个环节由谁负责、代码写在哪、在哪一步会失败**。具体形式不重要，机制要清楚。

---

## 文档怎么读

| 你想知道 | 读这个 |
|---|---|
| **全流程长什么样**（先读这个） | [FLOW.md](FLOW.md) |
| 现在该做哪一段 | [ROADMAP.md](ROADMAP.md) |
| 接口契约（ToolResult / ToolSpec / 执行顺序） | [CONTRACTS.md](CONTRACTS.md) |
| 开始写代码 | [stages/01-ENV.md](stages/01-ENV.md) 起，按序 |
| 卡住了 | [TROUBLESHOOT.md](TROUBLESHOOT.md) |
| openssl / gmssl 具体参数 | [reference/](reference/)，**当字典查，不要通读** |

`stages/` 下每份文档结构一致：

```text
在流程中的位置 → 要写的代码 → 核心概念（≤5 条）
→ 分步实现（带可运行命令）→ 常见坑 → 自检问题（3–5 道）
```

---

## 十段路径

| # | 阶段 | 工时 | 做完能做什么 |
|---|---|---:|---|
| 01 | 环境准备 | 20h | 新终端能复现，模型能应答 |
| 02 | 最小 Demo | 20h | 摘要工具跑通，手写 Loop 转起来 |
| 03 | 授权层 | 10h | 模型参数不可信，执行前就拒绝 |
| 04 | 协议与预算 | 35h | 四类失败分得开，预算撞得上，流能切块 |
| 05 | 持久化 | 40h | Run / 审计 / 动作意图落盘 |
| 06 | 审批与写操作 | 55h | action_hash 绑定、账本、崩溃恢复 |
| 07 | MCP | 12h | 同一业务，直调与协议调用结果一致 |
| 08 | 知识能力 | 105h | RAG / 引用 / Memory / 检索实验 |
| 09 | 前端 | 15h | 浏览器看到真实服务端状态 |
| 10 | 评测与交付 | 138h | 固定数据、实验、部署、恢复 |

**前四段（85h）做完，你就理解了这个 Agent 的全部机制。** 后面是在同一套机制上加持久化、审批、协议、检索和界面。

---

## 环境

全部在 Ubuntu 内运行，Windows 只用来开浏览器。

**四个仓库必须同级**（文档里的相对链接依赖这个布局）：

```text
/home/zsw/work/agent_development/
├── Agent-development-doc/      ← 本仓库（只有 Markdown）
├── Agent-development-code/     ← 实现
├── openssl/                    ← 官方源码
└── GmSSL/                      ← 官方源码
```

实测基线（2026-10-10 记录，**开工前重新核对**）：

| 项 | 实测值 |
|---|---|
| 发行版 | Ubuntu 22.04.5 LTS（WSL2，内核 6.6.87.2） |
| 用户 | `zsw`（非 root） |
| Python | 系统 3.10.12；项目 venv **3.12.13**（用 uv 提供，不要 apt install） |
| uv | 0.11.12 |
| Ollama | 0.32.15，systemd 服务，回环 `127.0.0.1:11434` |
| 模型 | `qwen3.5:4b`（3.3 GB，要求 Ollama ≥ 0.30.0） |
| OpenSSL CLI | 3.0.2（`/bin/openssl`） |
| GmSSL CLI | 3.3.0-dev.1183（`../.local/gmssl/bin/gmssl`） |
| GPU | RTX 5060 Ti，驱动 591.86 |

**不要**把仓库放在 `/mnt/c` 或 `/mnt/d`：9P 协议下 venv / node_modules 会慢数倍。

### 每次新开终端

```bash
cd /home/zsw/work/agent_development/Agent-development-code
git status --short --branch
source .venv/bin/activate
python -c 'import sys; print(sys.executable)'   # 必须指向 .venv/bin/python
```

### 检查入口

```bash
python3 scripts/selftest.py --stage <当前阶段> --strict   # 布局 / 配置 / 分层
python -m pytest -q                                      # 行为测试
python -m ruff check .                                   # 风格
```

> **已知基线缺口**：`packages/core/models.py` 有 5 个 ruff UP 系列告警。新增改动不要扩大它，但也别为了清零去动契约文件。

---

## 五条不会变的原则

1. **模型不执行任何东西。** 它只产生 `tool_calls` 这段 JSON。真正的动作在 `executor` 批准之后由 `subprocess` 完成。
2. **只有一个执行出口。** 所有工具调用走 `tools/executor.py`。绕过它直接调 handler、拼命令、读文件都是错的。
3. **秘密在服务端停住。** 真实路径、key version、口令、解密明文不进模型上下文、不进 ToolResult、不进日志。
4. **只读先于写。** 只读链路稳定之前不开放写操作；写操作必须有审批和账本。
5. **证据优先于说法。** "能跑"要有命令、输出、对照；"理解了"要能画出来并改一个需求。

---

## 与旧版文档的关系

旧版按 `V0`–`V6` 分七个阶段，每阶段 16–22 道必答题、多张重复的技术标准表（同一张表全库出现 40 次）。本次重构成 `01`–`10` 十段：

- 每段只讲一段，不再把多个"目标"塞进同一文档
- 技术标准表从 40 张压到每段一张（或并入核心概念）
- 必答题从约 140 道降到每段 3–5 道
- 前端从第 3 段移到第 9 段（形式放后面）
- CLI 手册移到 `reference/`，不在首读路径

旧文档在 git 历史里：

```bash
git log --diff-filter=D --oneline -- stages/V1-CORE-DEMO.md
git show <commit>^:stages/V1-CORE-DEMO.md | less
```

---

## 文档维护

- 本仓库只有 Markdown。
- 环境记录、阶段学习记录、决策记录写进对应阶段文档末尾的「本人记录」小节，不在代码仓库另建 `docs/`。
- 改文档前先看 `git status`，工作区干净再动。
- 不在本仓库放密钥、解密产物、真实工作资料或模型权重。
