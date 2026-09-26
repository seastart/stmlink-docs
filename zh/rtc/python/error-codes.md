---
title: "错误码"
description: "Python SDK 的 SdkError：code 的三类取值（SDK 自身 180xxx、服务端 1xxx 原样透传、-1 内部错误），常见错误的原因与排查，以及入会失败时的处理建议。"
---

接口失败时抛出 `srtc.SdkError`，带两个字段：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `code` | `int` | 错误码 |
| `msg` | `str` | 错误原因 |

```python
try:
    ch = await srtc.Channel.join(token)
except srtc.SdkError as e:
    print(e.code, e.msg)
```

`code` 分三类：

| 取值 | 来源 | 说明 |
| --- | --- | --- |
| `180xxx` | SDK 自身 | 与 [C SDK · 错误码](/zh/rtc/capi/error-codes#日志里的-180xxx：sdk-层错误) 同一套，服务端接入方式共用 `180` 前缀 |
| `≥1000`（如 `1033`） | 服务端 | 业务层面的拒绝原因，SDK 原样透传，完整清单见 [服务端 API · 错误码](/zh/rtc/server-api/error-codes) |
| `-1` | SDK 内部 | 没有具体错误码的失败（如 Token 格式不对、网络不通），看 `msg` |

---

## 常见错误

| 码 | 含义 | 常见原因与处理 |
| --- | --- | --- |
| `180001` | 不在频道内 | 频道已断开（`ch.closed` 为 `True`）后又调了会中接口 |
| `180002` | Token 已过期 | Token 超时未使用。**每次 `join` 都要新签发** |
| `180003` | 流轨道不存在 | 订阅的 uid / track_id 写错，或对方已取消发布 |
| `180300` / `180301` | 发布 / 订阅失败 | 媒体协商未通过，检查网络 |
| `180302` / `180303` | 发布 / 订阅协商超时 | 服务端媒体端口不可达，检查防火墙 |
| `1021` | Token 已被使用 | 同一个 Token 用了两次 |
| `1032` | 该会话不在线 | 复用了已离开频道的 Token |
| `1033` | 并发已达上限 | 应用的并发授权额度已用完，扩容授权或等待其他会话结束 |
| `1034` / `1035` | 无可用节点 / 节点满载 | 服务端媒体节点繁忙。SDK 在**重连**时会自动退避重试；**首次入会**失败需要你稍后重试 |

<Tip>
入会失败时，按错误码区分处理：`1021` / `1032` / `180002` 是 Token 问题，重试前要**重新签发 Token**；`1034` / `1035` 是暂时性的，稍后用新 Token 重试即可；`1033` 是授权额度问题，重试没有用。
</Tip>

---

## 日志

SDK 使用 Python 标准 `logging`，logger 名为 `srtc`：

```python
import logging

logging.basicConfig(level=logging.INFO)
logging.getLogger("srtc").setLevel(logging.DEBUG)     # 排查问题时打开
```

原生内核（信令、媒体连接）的日志直接输出到进程的标准输出 / 标准错误，不经过 `logging`。
