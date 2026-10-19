# 卡住时先查什么

原则：**先缩小到一个输入、一个工具、一个预期结果**，再动手。不要一次贴整个项目求助。

保存四样东西再开始排查：最小复现命令、实际报文、版本、已尝试的步骤。

---

## 按现象查

| 现象 | 先检查 | 下一步 | 相关阶段 |
|---|---|---|---|
| `ModuleNotFoundError` | 解释器路径、extras 装没装、当前目录 | `python -c 'import sys;print(sys.executable)'` | 01 |
| `pytest` 说没有测试 | 文件名、`testpaths`、是否真写了断言 | 写一个会失败的断言先看红 | 01 |
| `uv lock --check` 失败 | `pyproject.toml` 与 `uv.lock` 谁改的 | 查 git diff，不要直接覆盖 | 01 |
| Ollama 连不上 | `systemctl is-active ollama`、11434、回环地址 | 修服务，不要改到 Windows 宿主 IP | 01 |
| `404 model not found` | `ollama list` 里的真名 | 改 `CONTROLLER_MODEL` | 01 |
| 工具一直不被选 | 原始 `tools` schema、实际 `tool_calls`、问题是否真的需要工具 | 一次只暴露 1–2 个只读工具 | 02 |
| 模型编了个摘要 | 和独立 `openssl dgst` 对照 | 不一致就是没执行 | 02 |
| 工具参数缺字段 | `required` / 类型 / 资源 ID | 执行前拒绝，缺参数时澄清 | 03 |
| 越权没被拦住 | `resolve()` 是否在比较之前、是否用 `is_relative_to` | 用 `startswith` 会被 `/data_evil` 绕过 | 03 |
| 模型还在调已摘掉的工具 | `tools/list` 里还有没有它 | 注册代码没删干净 | 03 |
| 上下文爆掉 | `LLM_NUM_CTX` 有没有人读、history 有没有截断 | 截断要成对丢 assistant+tool | 04 |
| 后端报 400 孤儿 tool 消息 | 截断时把 `tool_calls` 和 `role:tool` 拆散了 | 成对丢 | 04 |
| 超时后进程还在 | `terminate()` / `wait()` / `kill()` 有没有真的调 | `wait_for` 只取消协程 | 04 |
| NDJSON 解析出乱码 | UTF-8 跨块、半行 | 用 `IncrementalDecoder` | 04 |
| 全部请求莫名超时 | 事务跨了模型请求 | 缩短事务边界 | 05 |
| 并发重传建了两个 Run | `UNIQUE(user_id, client_request_id)` 有没有 | 加约束 | 05 |
| `ready` 通过但业务失败 | `ready` 有没有真查依赖 | 分开 `live` 和 `ready` | 05 |
| 密文解不开 | key/version、nonce、AAD、tag、格式版本 | 用语料外工具核对，不让模型猜密钥 | 06 |
| 认证失败却生成了输出 | 是否先认证再创建文件 | 顺序错了 | 06 |
| 审批后资源变了还能执行 | `action_hash` 有没有绑资源版本 | 重新提议 | 06 |
| 双击批准执行了两次 | 服务端有没有 CAS/单次消费 | 按钮禁用不算 | 06 |
| 重启后动作跑了两遍 | 有没有写 intent、有没有查账本 | 标 unknown，别重跑 | 06 |
| MCP 协议解析失败 | stdout 里有没有 `print` | 日志走 stderr | 07 |
| `import mcp` 拿到自己的目录 | 项目里有没有顶级 `mcp/` | 改名 `mcp_integration` | 07 |
| 绕过 Agent 能越权 | Server 侧有没有复查 | 客户端不是信任边界 | 07 |
| 检索结果缺了很多 | ACL 是不是在检索之后才过滤 | 必须在候选之前 | 08 |
| 引用点不到原文 | locator 是真实页区间还是编的 | MD/TXT 不能有页码 | 08 |
| 指标好看但不真实 | `Q-` 有没有进 Recall 分母 | 单独报拒答率 | 08 |
| 事件收到了但查不到状态 | 事件是不是先发后落库 | 同一事务提交后再发 | 08 |
| 重连后有两个 Run | 重连时是不是重新 POST 了 | 用 snapshot + after 游标 | 08/09 |
| 前端串流（旧 Run 事件冒进新 Run） | 切 Run 有没有 abort + 清 last_event_id | 四步都要做 | 09 |
| 页面说成功但资源没变 | API snapshot、工具真实结果 | 页面只显示服务端状态 | 09 |
| 前端报失败但后端在做 | 本地 `abort()` ≠ 服务端取消 | 查 Run 状态 | 09 |
| 容器连不上宿主 Ollama | 容器自己的 `127.0.0.1` 不是宿主 | 用 `network_mode: host` 或显式地址 | 09 |
| 报告数字对不上 | hash 是不是同一套、有没有跳过 case | 缺失/重复/超时都不能静默 | 10 |
| 恢复后密钥用不了 | keystore blob 恢复了吗 | 只恢复 DB 不够 | 10 |

---

## 排错顺序（按层往下走，不要跳）

```text
① 前端展示        页面显示的是 snapshot 还是自己推的？
② API 身份与 Run  run_id 对不对？身份是谁？状态是什么？
③ 模型原始报文    实际 request/response 是什么？（脱敏后看）
④ registry / schema  工具名和参数形状对不对？
⑤ policy / approval 授权和审批在哪一步被拒的？
⑥ 动作账本        intent 写了没？状态是什么？unknown 还是 failed？
⑦ Provider 产物   子进程真的跑了吗？命令数组是什么？
⑧ Claim / Citation 引用对得上吗？
⑨ Verifier       哪个检查失败了？
```

**看到"模型答得不对"就先去换模型，几乎总是错的。** 从 ① 往下走一遍，比换模型快得多。

---

## 一次卡住的最小流程

```text
1. 缩小   能用一个命令复现吗？能缩短到一个工具吗？
2. 保存   命令、实际输出、版本、已试过的步骤
3. 分类   是环境 / 协议 / 授权 / 密码 / 模型 哪一类？
4. 定位   按上面九层往下，找到第一个不对的层
5. 修一层 一次只改一处，改完立刻回归
6. 记录   写进该阶段文档的「本人记录」
```

---

## 几个不需要排错的"假问题"

| 现象 | 为什么不是问题 |
|---|---|
| 模型两次回答措辞不同 | 采样有随机性。比协议和行为，不比文本 |
| `selftest` 过了但 ruff 有告警 | 两个检查管不同的事。基线告警已登记 |
| `gmssl` 不在 PATH | 配置里指向 `../.local/gmssl/bin/gmssl` |
| `live` 通过但业务跑不动 | `live` 只证明进程活着 |
| 空结果是 `success=True` | 合法语义："查了，没有" |
