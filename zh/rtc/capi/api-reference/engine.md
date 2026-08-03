---
title: "实例与频道"
description: "SRTC C SDK 实例生命周期、加入/离开频道、日志级别与各类回调的注册接口"
---

本页覆盖 SDK 实例的创建销毁、频道进出，以及全部回调的注册接口。

所有接口都是线程安全的。

---

## 日志

### rtc_set_log_level

```c
void rtc_set_log_level(int level);
```

设置全局日志级别，进程级生效，建议在 `rtc_create` 之前调用。

| 参数 | 说明 |
| --- | --- |
| `level` | `RTC_LOG_DEBUG`(0) / `RTC_LOG_INFO`(1) / `RTC_LOG_WARN`(2) / `RTC_LOG_ERROR`(3)，传入其它值按 `INFO` 处理 |

---

## 实例生命周期

### rtc_create

```c
void* rtc_create();
```

创建一个 SDK 实例，返回实例句柄。后续所有频道相关接口都要传这个句柄。

一个句柄对应一个频道连接。需要同时连多个频道时，创建多个实例即可。

### rtc_destroy

```c
void rtc_destroy(void* handle);
```

销毁实例并释放资源。SDK 保证 `rtc_destroy` 返回后不会再触发任何回调，因此可以安全地在它之后释放你传给回调的 `context`。

<Warning>
必须调用 `rtc_destroy`，否则实例资源不会释放。销毁后该句柄不可再使用。
</Warning>

---

## 加入与离开频道

### rtc_join_channel

```c
int rtc_join_channel(void* handle, const char* token);
```

异步加入频道，立即返回。真正的连接结果通过连接状态回调（`rtc_set_connection_callback`）通知。

| 参数 | 说明 |
| --- | --- |
| `token` | 服务端签发的加入频道 Token，见 [服务端 API · 获取加入频道 token](/zh/rtc/server-api/channel) |

**返回值**

| 返回值 | 含义 |
| --- | --- |
| `RTC_OK` | 已发起加入请求（不代表已连接成功） |
| `RTC_INVALID_PARAM` | 句柄无效，或 token 为空字符串 |

### rtc_join_channel_sync

```c
int rtc_join_channel_sync(void* handle, const char* token, int timeout_ms);
```

同步加入频道，阻塞直到连接成功、失败或超时。

| 参数 | 说明 |
| --- | --- |
| `token` | 服务端签发的加入频道 Token |
| `timeout_ms` | 超时时间（毫秒）。超时后本次加入流程会被完整中止，不会留下后台任务 |

**返回值**

| 返回值 | 含义 |
| --- | --- |
| `RTC_OK` | 加入成功 |
| `RTC_INVALID_PARAM` | 句柄无效，或 token 为空字符串 |
| `RTC_ERROR` | 加入失败（Token 失效、会话被占用、服务端拒绝等） |
| `RTC_TIMEOUT` | 超时未完成 |

### rtc_leave_channel

```c
int rtc_leave_channel(void* handle);
```

离开频道。离开后实例仍然有效，可以再次加入。彻底不用时还需调用 `rtc_destroy`。

**返回值**：`RTC_OK` / `RTC_INVALID_PARAM`（句柄无效）。

---

## 自动订阅

### rtc_set_auto_subscribe

```c
void rtc_set_auto_subscribe(void* handle, int auto_audio, int auto_video);
```

设置是否自动订阅远端轨道。开启后，频道内所有已发布和新发布的对应类型轨道都会被自动订上，数据统一走轨道数据回调。

| 参数 | 说明 |
| --- | --- |
| `auto_audio` | 1 = 自动订阅所有音频，0 = 不自动订阅 |
| `auto_video` | 1 = 自动订阅所有视频，0 = 不自动订阅 |

<Warning>
必须在加入频道**之前**调用，入会后再设置不会对已有轨道生效。
</Warning>

<Tip>
参与者想"听全场"，正确做法是 `rtc_set_auto_subscribe(rtc, 1, 0)` 订阅所有人的音频后在业务侧自行混音，**不要**去订阅音频合成流 —— 合成流包含自己的声音，会产生回声。
</Tip>

---

## 回调注册

所有回调都通过 `context` 参数携带业务上下文，SDK 原样回传，不做任何解释。

<Warning>
**回调执行在 SDK 内部线程上**，注意三点：

1. 不同回调可能并发触发，业务侧要自己做并发保护
2. 回调里不要做耗时操作，否则会阻塞 SDK 事件循环；耗时处理请入队后交给自己的线程
3. 回调参数中的指针（`data`、`props`、`content_json`、`speakers` 等）**只在回调期间有效**，需要留存必须立即拷贝
</Warning>

### rtc_set_connection_callback

```c
typedef void (*rtc_connection_callback)(void* context, int state);
void rtc_set_connection_callback(void* handle, rtc_connection_callback callback, void* context);
```

连接状态变化。`state`：`0`=连接中，`1`=已连接，`2`=已断开，`3`=重连中。

### rtc_set_user_event_callback

```c
typedef void (*rtc_user_event_callback)(void* context, const char* uid, int event_type);
void rtc_set_user_event_callback(void* handle, rtc_user_event_callback callback, void* context);
```

用户进出频道。`event_type`：`0`=加入，`1`=离开。

### rtc_set_track_event_callback

```c
typedef void (*rtc_track_event_callback)(void* context, const char* uid,
                                         rtc_track_info_t* track_info, int event_type);
void rtc_set_track_event_callback(void* handle, rtc_track_event_callback callback, void* context);
```

远端轨道的增删改。`event_type`：`0`=新增，`1`=更新，`2`=移除。手动订阅时用这个回调发现可订阅的轨道。

### rtc_set_track_sample_callback

```c
typedef void (*rtc_track_sample_callback)(void* context,
                                          rtc_user_info_t* user_info,
                                          rtc_track_info_t* track_info,
                                          uint8_t* data, int len,
                                          int64_t timestamp, int64_t duration);
void rtc_set_track_sample_callback(void* handle, rtc_track_sample_callback callback, void* context);
```

已订阅轨道的媒体数据。所有订阅的轨道（含合成流）都从这一个回调出来，用 `user_info->uid` + `track_info->track_id` 区分来源。

`data` 是完整的编码帧（视频为一帧，音频为一个编码包），指针仅在回调期间有效：

```c
uint8_t* saved = malloc(len);
memcpy(saved, data, len);   // 需要留存必须拷贝
```

### rtc_set_custom_msg_callback

```c
typedef void (*rtc_custom_msg_callback)(void* context, const rtc_custom_msg_t* msg);
void rtc_set_custom_msg_callback(void* handle, rtc_custom_msg_callback callback, void* context);
```

频道内自定义消息，详见 [自定义消息](/zh/rtc/capi/advanced/custom-msg)。

### SeaStart 专属回调

以下三个回调仅在频道使用 SeaStart 引擎时触发，其它引擎下不会回调。详见 [SeaStart 进阶能力](/zh/rtc/capi/advanced/seastart)。

```c
void rtc_set_layer_switched_callback(void* handle, rtc_layer_switched_callback callback, void* context);
void rtc_set_connection_quality_callback(void* handle, rtc_connection_quality_callback callback, void* context);
void rtc_set_active_speakers_callback(void* handle, rtc_active_speakers_callback callback, void* context);
```

---

## 典型调用顺序

```c
rtc_set_log_level(RTC_LOG_INFO);

void* rtc = rtc_create();

// 1) 先注册回调
rtc_set_connection_callback(rtc, on_conn, ctx);
rtc_set_user_event_callback(rtc, on_user, ctx);
rtc_set_track_event_callback(rtc, on_track, ctx);
rtc_set_track_sample_callback(rtc, on_sample, ctx);

// 2) 再配置自动订阅
rtc_set_auto_subscribe(rtc, 1, 1);

// 3) 最后加入频道
rtc_join_channel_sync(rtc, token, 10000);

// ... 业务运行 ...

rtc_leave_channel(rtc);
rtc_destroy(rtc);
```
