---
title: "错误码"
description: "SRTC C SDK 接口返回值的取值、含义与排查建议"
---

C 接口用返回值表达结果。返回 `int` 的接口统一使用下面 5 个取值，`RTC_OK` 为 `0`，失败一律为负数。

```c
#define RTC_OK              0   // 成功
#define RTC_ERROR          -1   // 一般错误
#define RTC_INVALID_PARAM  -2   // 参数无效
#define RTC_NOT_CONNECTED  -3   // 未连接
#define RTC_TIMEOUT        -4   // 超时
```

---

## 取值说明

| 常量 | 值 | 含义 | 常见原因与排查方向 |
| --- | --- | --- | --- |
| `RTC_OK` | `0` | 成功 | —— |
| `RTC_ERROR` | `-1` | 一般错误 | 服务端拒绝、底层协商失败、Token 会话失效、身份不满足要求（如非 `__mcu__` 身份发布合成流）。**开 DEBUG 日志看具体原因** |
| `RTC_INVALID_PARAM` | `-2` | 参数无效 | 实例/轨道句柄无效或已销毁、必填指针传了 `NULL`、Token 为空串、对非视频轨道请求关键帧 |
| `RTC_NOT_CONNECTED` | `-3` | 未连接 | 还没成功加入频道就调了需要连接的接口；`rtc_get_connection_quality` 下还表示"尚未收到第一帧质量数据" |
| `RTC_TIMEOUT` | `-4` | 超时 | 仅 `rtc_join_channel_sync` 返回。Token 过期、网络不通、服务端不可达 |

<Note>
`RTC_ERROR` 是一个笼统的失败码，本身不携带具体原因。定位问题时请先调高日志级别：

```c
rtc_set_log_level(RTC_LOG_DEBUG);
```

SDK 会把服务端返回的业务错误打到日志里。
</Note>

---

## 与服务端业务错误码的关系

C 接口的这 5 个码只描述"调用层面"的结果。真正的业务失败原因来自服务端，会以业务错误码的形式出现在日志中，例如：

| 服务端码 | 说明 | 在 C 侧的表现 |
| --- | --- | --- |
| `1021` | channel token 已被使用 | `rtc_join_channel_sync` 返回 `RTC_ERROR` |
| `1032` | 该会话不在线 | `rtc_join_channel_sync` 返回 `RTC_ERROR` |

完整清单见 [服务端 API · 错误码](/zh/rtc/server-api/error-codes)。

<Warning>
Token 与一次会话绑定，进程离开频道后该会话即失效。复用同一个 Token 起第二个进程会拿到 `1032`（在 C 侧表现为 `RTC_ERROR`）—— 每个进程都要单独签发 Token。
</Warning>

---

## 返回值检查建议

所有返回 `int` 的接口都应检查返回值。加入频道这类关键路径失败时必须走清理流程，避免句柄泄漏：

```c
void* rtc = rtc_create();

int ret = rtc_join_channel_sync(rtc, token, 10000);
if (ret != RTC_OK) {
    fprintf(stderr, "join failed: %d\n", ret);
    rtc_destroy(rtc);        // 失败也要销毁实例
    return -1;
}
```

`rtc_create` / `rtc_create_local_track` 返回的是指针，失败时为 `NULL`，判空即可。
