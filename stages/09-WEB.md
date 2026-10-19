# 09. 前端（15h）

> 完成这一段，你能做到：**在浏览器里做完一件事，并且页面显示的状态是服务端的真实状态，不是你猜的。**

前端放在倒数第二段是刻意的：**形式在机制之后。** 你已经有了清晰的 API 和事件契约，前端只是它的一个消费者。

---

## 在流程中的位置

[FLOW.md](../FLOW.md) 最后一段：`DB 状态 / 事件 → 浏览器快照与 SSE`。

前置：08 段（要消费 SSE 和引用）。解锁：10 段的综合验收（要在页面上跑完业务）。

---

## 要写的代码

| 路径 | 职责 | 现状 |
|---|---|---|
| `web/src/` | React + TypeScript 应用 | ❌ 空目录 |
| `services/agent_api/` | 已提供 API 与事件 | ✅ 05/06/08 段完成 |

依赖：Node v22.23.2 + pnpm 12.3.4。`uv sync` 不管前端，要用 pnpm 单独装。

---

## 核心概念

### 1. 状态分三层，不要混

| 层 | 内容 | 来源 | 什么时候变 |
|---|---|---|---|
| **本地状态** | 输入框、选中的 tab、展开的行 | 用户操作 | 立刻 |
| **服务器快照** | Run 状态、pending 审批、最终答案 | `GET /runs/{id}` | 刷新、重连、动作后 |
| **流事件增量** | 新的 step、token、tool_result | SSE | 实时追加 |

**规则：服务器快照永远优先。** 事件只负责"追加"，不负责"修正"。

具体做法：每次收到事件后，若事件表明状态可能变了（如 `approval_required`），**重新拉一次 snapshot**，不要靠前端自己推。

### 2. 九个通用区块

```text
Chat          对话
Session       会话列表
Upload        文件上传
Knowledge     知识库文档
Steps         步骤时间线
ToolCalls     工具调用与结果
Sources       引用与验证状态
Approval      审批面板
RunHistory    Run 历史
```

不必一次全做。**先做 Chat + Steps + ToolCalls + Approval**，这四个能撑起一次完整业务。

### 3. 审批面板只提交三个字段

```json
{"approval_id": "...", "action_hash": "...", "decision": "approved"}
```

**不提交**：风险等级、角色、参数、用户 ID。这些全部由服务端从数据库读。

面板**必须显示**（否则用户不知道自己在批准什么）：

```text
工具名（canonical）
规范参数（只读）
影响资源 + 版本
风险等级 + 策略版本
action_hash
有效期
发起者
当前执行状态
```

### 4. 断线 ≠ 取消

```text
用户关掉浏览器      → 服务端 Run 按 disconnect_policy 处理
前端 abort() 请求    → 只是本地停止读取，服务端不知道
服务端 cancel        → 需要显式 POST /runs/{id}/cancel
```

三件事完全不同。**关闭本地 reader 不代表服务端停止。**

`disconnect_policy` 两档：

| 值 | 含义 | 用在哪 |
|---|---|---|
| `cancel` | 断线即取消 | 05 段简单同步任务 |
| `detach` | 断线后继续跑 | 06 段审批等待、后台任务 |

### 5. 刷新 = 查原 Run，不是重新 POST

```text
❌ 刷新 → POST /chat → 又跑一遍
✅ 刷新 → GET /runs/{run_id} + GET /runs/{run_id}/events?after={last_event_id}
```

判断依据：URL 里有没有 `run_id`。有就查，没有才新建。

**不同 tab 看同一个 Run 不应该触发第二次执行。**

### 6. 切换 Run 必须清干净

```text
切 Run 时：
  ① abort 旧的 reader / AbortController
  ② 清空旧事件的累积状态
  ③ 重置 last_event_id
  ④ 拉新 Run 的 snapshot
```

漏了任何一步，就会出现"新 Run 里冒出旧 Run 的事件"——**串流**。

### 7. 验证状态如实显示

```text
passed     → 显示"已通过"
failed     → 显示失败原因
not_run    → 显示"未验证"，不能显示成通过
unknown    → 显示"未检查到"
```

`draft` 是草稿，`final` 才是最终答案。**`not_run` 不能伪装成已验证。**

---

## 分步实现

### 步骤 1 打通最小页面

```text
登录（API key）→ 上传文件 → 提问 → 看到步骤和工具调用 → 看到答案
```

先只用非流式 JSON，不要一上来就 SSE。

验证：`GET /health/live` 和 `/health/ready` 都在页面上有反馈。

### 步骤 2 接 SSE

用 `fetch` + 手动读流，不用原生 `EventSource`：

```ts
const resp = await fetch(`/runs/${runId}/events`, {
  headers: { "X-API-Key": key },
  signal: ac.signal,
});
const reader = resp.body!.getReader();
// 按 \n\n 分帧，处理 UTF-8 跨块
```

原生 `EventSource` **不支持自定义鉴权头**，只能把 key 塞 URL（会进日志），所以不用它。

### 步骤 3 审批面板

从 `approval_required` 事件或 snapshot 里拿 `pending` 审批，渲染出上面那 8 项，用户点了之后 POST。

验证四件事：

- 批准后状态变化
- 拒绝后不产生 artifact
- 过期后再点被拒
- 刷新页面能重建 pending 面板

### 步骤 4 刷新与重连

```text
① 页面加载 → 从 URL 取 run_id
② GET /runs/{id} → 恢复快照
③ 从 snapshot.last_event_id 开始拉事件
④ 去重（按 event_id）
```

验证：执行中刷新，页面能恢复；不产生第二个 Run。

### 步骤 5 Windows 浏览器访问

前端和 API 必须绑 `0.0.0.0`（或至少不是 `127.0.0.1`），否则 Windows 访问不到。

```bash
ss -ltnp | grep -E '5173|8000'     # 确认监听地址
```

注意：**Ubuntu 内的 `127.0.0.1` ≠ Windows 的 `127.0.0.1`**。前端若要从浏览器直连 Ollama，是连不通的——Ollama 只绑回环。所以模型调用必须经后端。

---

## 常见坑

1. **用原生 `EventSource`。** 无法带鉴权头，只能把 key 塞 URL。
2. **前端自己推导状态。** 收到 `step` 就以为完成了。状态以 snapshot 为准。
3. **断线当取消。** 关掉页面，服务端可能还在跑（`detach`）。
4. **刷新重新 POST。** 创建第二个 Run，第二个副作用。
5. **切 Run 不清理 reader。** 串流。
6. **审批面板只发 `decision`。** 不带 `action_hash`，无法校验批准的是不是同一件事。
7. **`not_run` 显示成通过。** 用户会以为验证过了。
8. **把 API key 放 `localStorage` 或 URL。** 前者被 XSS 拿，后者进日志。
9. **前端隐藏按钮当权限。** 后端必须同样校验。
10. **容器里用 `127.0.0.1` 连宿主 Ollama。** 容器自己的回环不是宿主。

---

## 自检问题

1. 本地状态、服务器快照、流事件三层分别管什么？举一个"只靠事件会出错"的例子。
2. 审批面板为什么必须显示 `action_hash` 和规范参数？只提交 `decision` 会怎样？
3. 关闭浏览器标签页、前端 `abort()`、服务端 `cancel` 是三件事——分别发生了什么？
4. 刷新页面为什么不能重新 POST？你的页面怎么知道该查哪个 Run？
5. `effect` 清理或 `AbortController` 中断，能证明后端已停止吗？给出你核对的方式。

---

## 本人记录

```text
日期：
实际工时：
页面截图/操作路径：
一次完整业务的 Run 记录：
审批面板显示的字段：
断线/刷新/切 Run 的实际行为：
还没理解的：
```
