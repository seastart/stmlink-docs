---
title: "错误码"
description: "Python SDK 的 SdkError：code 的三类取值（SDK 自身 180xxx、服务端 1xxx 原样透传、-1 内部错误）与 base_code / ErrorCode，常见错误的原因与排查、入会失败时的处理建议，以及用 set_language 设置服务端错误文案的语言。"
---

接口失败时抛出 `srtc.SdkError`，带以下字段：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `code` | `int` | 错误码 |
| `msg` | `str` | 错误原因。SDK 自身错误为英文；服务端错误的语言见下文 [语言](#语言) |
| `base_code` | `int` | 0.2.0 起。SDK 错误码的后三位（各端 SDK 统一），可与 `srtc.ErrorCode` 比较；服务端错误码返回自身 |

```python
try:
    ch = await srtc.Channel.join(token)
except srtc.SdkError as e:
    print(e.code, e.msg)
    if e.base_code == srtc.ErrorCode.TOKEN_INVALID:
        ...  # Token 不合法，检查签发
```

请按 `code` / `base_code` 判断错误类型，不要按 `msg` 文案判断。

`code` 分三类：

| 取值 | 来源 | 说明 |
| --- | --- | --- |
| `180xxx` | SDK 自身 | 与 [C SDK · 错误码](/zh/rtc/capi/error-codes#日志里的-180xxx：sdk-层错误) 同一套，服务端接入方式共用 `180` 前缀，后三位各端 SDK 统一（编号规则见 [错误码规则](/zh/rtc/error-codes)） |
| `≥1000`（如 `1033`） | 服务端 | 业务层面的拒绝原因，SDK 原样透传，完整清单见 [服务端 API · 错误码](/zh/rtc/server-api/error-codes) |
| `-1` | SDK 内部 | 没有具体错误码的内部错误，正常不应出现，看 `msg` |

<Warning>
0.2.0 起错误码全面重排（如参数错误由 `180900` 改为 `180031`，"无权发布合成流"由 `180004` 改为 `180040`），下表按 0.2.0 及以后的版本列出。旧码与新码的对照见 [更新日志 · 0.2.0](/zh/rtc/python/changelog)。
</Warning>

---

## 常见错误

| 码 | `ErrorCode` | 含义 | 常见原因与处理 |
| --- | --- | --- | --- |
| `180001` | `NOT_IN_CHANNEL` | 不在频道内 | 频道已断开（`ch.closed` 为 `True`）后又调了会中接口 |
| `180002` | `TOKEN_EXPIRED` | Token 已过期 | Token 超时未使用。**每次 `join` 都要新签发** |
| `180003` | `TRACK_NOT_FOUND` | 流轨道不存在 | 订阅的 uid / track_id 写错，或对方已取消发布 |
| `180004` | `TOKEN_INVALID` | Token 不合法 | Token 解析失败或内容不完整，检查是否完整传入、是否为本环境签发 |
| `180006` | `CONNECTION_FAILED` | 连接失败 | 网络请求失败或 HTTP 非 200，检查网络与服务地址 |
| `180007` | `CONNECTION_TIMEOUT` | 连接超时 | `join` 在 `timeout` 内未完成 |
| `180014` | `TRANSPORT_NOT_READY` | 传输未就绪 | 频道正在重连，**稍后重试**即可 |
| `180025` | `INTERNAL_ERROR` | SDK 内部错误 | 如创建本地音频轨道失败。请带上日志联系我们 |
| `180031` | `INVALID_ARGUMENT` | 参数非法 | 参数取值不对，如声道数不是 1 或 2、轨道类型不符 |
| `180040` | `NOT_MCU_PUBLISHER` | 无权发布合成流 | 发布合成流要求以 `__mcu__` 身份接入 |
| `180300` / `180301` | `PUBLISH_FAILED` / `SUBSCRIBE_FAILED` | 发布 / 订阅失败 | 媒体协商未通过，检查网络 |
| `180302` / `180303` | `PUBLISH_TIMEOUT` / `SUBSCRIBE_TIMEOUT` | 发布 / 订阅协商超时 | 服务端媒体端口不可达，检查防火墙 |
| `1021` | —— | Token 已被使用 | 同一个 Token 用了两次 |
| `1032` | —— | 该会话不在线 | 复用了已离开频道的 Token |
| `1033` | —— | 并发已达上限 | 应用的并发授权额度已用完，扩容授权或等待其他会话结束 |
| `1034` / `1035` | —— | 无可用节点 / 节点满载 | 服务端媒体节点繁忙。SDK 在**重连**时会自动退避重试；**首次入会**失败需要你稍后重试 |

`srtc.ErrorCode` 的完整取值与各码含义见 [C SDK · 错误码](/zh/rtc/capi/error-codes#日志里的-180xxx：sdk-层错误)（`ErrorCode` 的值即错误码后三位）。

<Tip>
入会失败时，按错误码区分处理：`1021` / `1032` / `180002` / `180004` 是 Token 问题，重试前要**重新签发 Token**；`1034` / `1035` / `180006` 是暂时性的，稍后用新 Token 重试即可；`1033` 是授权额度问题，重试没有用。
</Tip>

---

## 语言

服务端错误（`code` ≥1000）的 `msg` 由服务端生成，语言可以设置（0.2.0 起）：

```python
import srtc

srtc.set_language("en")      # 如 "en"、"zh-CN"；传 None 或空串恢复为跟随系统语言
```

+ 进程级生效，随时可调，可以在创建 `Channel` 之前调用
+ 不调用时跟随系统语言：依次取环境变量 `LC_ALL`、`LC_MESSAGES`、`LANG` 中第一个非空的值；为 `C` / `POSIX` 或都未设置时，服务端按中文返回
+ 只影响服务端错误的文案；SDK 自身错误（`180xxx`）始终是英文

---

## 日志

SDK 使用 Python 标准 `logging`，logger 名为 `srtc`：

```python
import logging

logging.basicConfig(level=logging.INFO)
logging.getLogger("srtc").setLevel(logging.DEBUG)     # 排查问题时打开
```

原生内核（信令、媒体连接）的日志直接输出到进程的标准输出 / 标准错误，不经过 `logging`。
