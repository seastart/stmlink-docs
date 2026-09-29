---
title: "Instance and channel"
description: "C SDK instance lifecycle (rtc_create / rtc_destroy and when it is safe to free callback context), joining and leaving channels, rtc_get_last_error, auto-subscribe, log level, and every callback registration function with its threading rules."
---

This page covers creating and destroying SDK instances, joining and leaving channels, and every callback registration function.

All functions are thread-safe.

---

## Logging

### rtc_set_log_level

```c
void rtc_set_log_level(int level);
```

Sets the global log level. It applies to the whole process; we recommend calling it before `rtc_create`.

| Parameter | Description |
| --- | --- |
| `level` | `RTC_LOG_DEBUG`(0) / `RTC_LOG_INFO`(1) / `RTC_LOG_WARN`(2) / `RTC_LOG_ERROR`(3); any other value is treated as `INFO` |

---

## Instance lifecycle

### rtc_create

```c
void* rtc_create();
```

Creates an SDK instance and returns the instance handle. Every channel-related function afterward takes this handle.

One handle corresponds to one channel connection. To connect to multiple channels at the same time, create multiple instances.

### rtc_destroy

```c
void rtc_destroy(void* handle);
```

Destroys the instance and releases its resources. **Starting with 0.0.11**, `rtc_destroy` waits for all running callbacks to return before it returns. After it returns, no further callbacks fire for this instance, and you can safely free the `context` you passed to the callbacks.

+ You may call `rtc_destroy` from within one of this instance's callbacks (including the disconnect callback). In that case it only waits for callbacks on other threads—**don't free the current callback's `context` until that callback returns**
+ If a callback does slow work (decoding, writing files), `rtc_destroy` waits correspondingly longer
+ Neither `rtc_leave_channel` nor replacing a callback with `rtc_set_*_callback` waits for running callbacks, so neither is a safe point to free `context`

<Warning>
**0.0.10 and earlier don't provide these guarantees**: callbacks may still be running when `rtc_destroy` returns, and calling `rtc_destroy` from the disconnect callback deadlocks. With these older versions, don't free `context` right after `rtc_destroy`, and don't destroy the instance in the disconnect callback; we recommend upgrading to 0.0.11.
</Warning>

<Warning>
You must call `rtc_destroy`; otherwise the instance's resources are not released. The handle can't be used after it's destroyed.
</Warning>

---

## Joining and leaving a channel

### rtc_join_channel

```c
int rtc_join_channel(void* handle, const char* token);
```

Joins a channel asynchronously and returns immediately. The actual connection result is reported through the connection state callback (`rtc_set_connection_callback`).

| Parameter | Description |
| --- | --- |
| `token` | Channel join token issued by the server; see [Server API · Get a channel join token](/en/rtc/server-api/channel) |

**Returns**

| Return value | Meaning |
| --- | --- |
| `RTC_OK` | The join request was initiated (doesn't mean the connection succeeded) |
| `RTC_INVALID_PARAM` | Invalid handle, or the token is an empty string |

### rtc_join_channel_sync

```c
int rtc_join_channel_sync(void* handle, const char* token, int timeout_ms);
```

Joins a channel synchronously, blocking until the connection succeeds, fails, or times out.

| Parameter | Description |
| --- | --- |
| `token` | Channel join token issued by the server |
| `timeout_ms` | Timeout in milliseconds. On timeout, this join attempt is fully aborted, leaving no background tasks behind |

**Returns**

| Return value | Meaning |
| --- | --- |
| `RTC_OK` | Joined successfully |
| `RTC_INVALID_PARAM` | Invalid handle, or the token is an empty string |
| `RTC_ERROR` | Join failed (token invalid, session already taken, rejected by the server, etc.); get the specific reason with `rtc_get_last_error` |
| `RTC_TIMEOUT` | Didn't complete before the timeout |

### rtc_get_last_error

```c
int rtc_get_last_error(void* handle, char* msg_buf, int buf_len);
```

Gets the error details of this instance's **most recent failed call** (since 0.0.9). Call it after join, subscribe, publish, or similar functions return `RTC_ERROR` / `RTC_TIMEOUT`.

| Parameter | Description |
| --- | --- |
| `msg_buf` / `buf_len` | Optional. If provided, the error reason is written into it (truncated if too long, always `\0`-terminated); pass `NULL, 0` if you don't need the reason |

**Returns:** The error code. `180xxx` is an SDK error, `≥1000` is a server error code, `-1` is an internal error with no specific code, and `0` means nothing was recorded.

```c
if (rtc_join_channel_sync(rtc, token, 10000) != RTC_OK) {
    char msg[256];
    int code = rtc_get_last_error(rtc, msg, sizeof(msg));
    fprintf(stderr, "join failed: %d %s\n", code, msg);    // e.g. 1033 concurrency limit reached
}
```

<Note>
Each instance keeps only the most recent error. When multiple threads call functions on the same instance concurrently, a later failure overwrites an earlier one.
</Note>

### rtc_leave_channel

```c
int rtc_leave_channel(void* handle);
```

Leaves the channel. The instance stays valid after leaving and can join again. When you're done with it for good, you still need to call `rtc_destroy`.

**Returns:** `RTC_OK` / `RTC_INVALID_PARAM` (invalid handle).

---

## Auto-subscribe

### rtc_set_auto_subscribe

```c
void rtc_set_auto_subscribe(void* handle, int auto_audio, int auto_video);
```

Sets whether to automatically subscribe to remote tracks. When on, every already-published and newly published track of the corresponding type in the channel is subscribed automatically, and all data goes through the track data callback.

| Parameter | Description |
| --- | --- |
| `auto_audio` | 1 = auto-subscribe to all audio, 0 = don't |
| `auto_video` | 1 = auto-subscribe to all video, 0 = don't |

<Warning>
Must be called **before** joining the channel. Setting it after joining has no effect on existing tracks.
</Warning>

<Tip>
If a user wants to "hear everyone," the right approach is `rtc_set_auto_subscribe(rtc, 1, 0)` to subscribe to everyone's audio and then mix it yourself. **Don't** subscribe to the audio composite stream—it includes your own voice and causes echo.
</Tip>

---

## Callback registration

Every callback carries your context through the `context` parameter; the SDK passes it back unchanged without interpreting it.

<Warning>
`context` must be a **real pointer** (or `NULL`). Don't cast small integers like `1` or `2` to pointers to use as IDs: the SDK stores it internally as a pointer, and a value below 4096 is treated as an invalid pointer and terminates the process immediately. If you need an ID, pass the address of memory that holds it.
</Warning>

<Warning>
**Callbacks run on internal SDK threads.** Keep three things in mind:

1. Different callbacks can fire concurrently, so protect shared state yourself
2. Don't do slow work in callbacks, or you'll block the SDK event loop; queue slow processing and hand it to your own threads
3. Pointers in callback parameters (`data`, `props`, `content_json`, `speakers`, etc.) are **only valid during the callback**; copy them right away if you need to keep them
</Warning>

### rtc_set_connection_callback

```c
typedef void (*rtc_connection_callback)(void* context, int state);
void rtc_set_connection_callback(void* handle, rtc_connection_callback callback, void* context);
```

Connection state changes. `state`: `0`=connecting, `1`=connected, `2`=disconnected, `3`=reconnecting.

### rtc_set_disconnected_callback

```c
typedef void (*rtc_disconnected_callback)(void* context, int reason, int code, const char* msg);
void rtc_set_disconnected_callback(void* handle, rtc_disconnected_callback callback, void* context);
```

Fires once when the instance finally leaves the channel (at the same moment as `state=2` in the connection state callback, and before it), with the disconnect reason (since 0.0.9).

| Parameter | Description |
| --- | --- |
| `reason` | Disconnect reason `RTC_DISCONNECT_*`; see [Types · Callback parameter enums](/en/rtc/capi/types#callback-parameter-enums) |
| `code` | The error code if there was an error (`180xxx` or a server `1xxx`; see [Error codes](/en/rtc/capi/error-codes)), otherwise `0` |
| `msg` | The error reason; `NULL` if there was no error. Only valid during the callback |

<Tip>
Use it to decide whether to rejoin automatically: don't rejoin automatically when removed from the channel (`KICKED`), replaced by another session with the same uid (`REPLACE`), or when the channel is destroyed (`DESTROY`); in cases such as a heartbeat timeout (`TIMEOUT`), you can rejoin with a newly issued token.
</Tip>

### rtc_set_user_event_callback

```c
typedef void (*rtc_user_event_callback)(void* context, const char* uid, int event_type);
void rtc_set_user_event_callback(void* handle, rtc_user_event_callback callback, void* context);
```

Users joining and leaving the channel. `event_type`: `0`=joined, `1`=left.

### rtc_set_track_event_callback

```c
typedef void (*rtc_track_event_callback)(void* context, const char* uid,
                                         rtc_track_info_t* track_info, int event_type);
void rtc_set_track_event_callback(void* handle, rtc_track_event_callback callback, void* context);
```

Remote tracks added, updated, or removed. `event_type`: `0`=added, `1`=updated, `2`=removed. With manual subscription, use this callback to discover tracks you can subscribe to.

### rtc_set_track_sample_callback

```c
typedef void (*rtc_track_sample_callback)(void* context,
                                          rtc_user_info_t* user_info,
                                          rtc_track_info_t* track_info,
                                          uint8_t* data, int len,
                                          int64_t timestamp, int64_t duration);
void rtc_set_track_sample_callback(void* handle, rtc_track_sample_callback callback, void* context);
```

Media data for subscribed tracks. Every subscribed track (including composite streams) comes out of this single callback; use `user_info->uid` + `track_info->track_id` to tell the sources apart.

`data` is a complete encoded frame (one frame for video, one encoded packet for audio). The pointer is only valid during the callback:

```c
uint8_t* saved = malloc(len);
memcpy(saved, data, len);   // Copy it if you need to keep it
```

### rtc_set_custom_msg_callback

```c
typedef void (*rtc_custom_msg_callback)(void* context, const rtc_custom_msg_t* msg);
void rtc_set_custom_msg_callback(void* handle, rtc_custom_msg_callback callback, void* context);
```

In-channel custom messages; see [Custom messages](/en/rtc/capi/advanced/custom-msg).

### SeaStart-only callbacks

The following three callbacks only fire when the channel uses the SeaStart engine; with other engines they're never called. See [SeaStart advanced features](/en/rtc/capi/advanced/seastart).

```c
void rtc_set_layer_switched_callback(void* handle, rtc_layer_switched_callback callback, void* context);
void rtc_set_connection_quality_callback(void* handle, rtc_connection_quality_callback callback, void* context);
void rtc_set_active_speakers_callback(void* handle, rtc_active_speakers_callback callback, void* context);
```

---

## Typical call order

```c
rtc_set_log_level(RTC_LOG_INFO);

void* rtc = rtc_create();

// 1) Register callbacks first
rtc_set_connection_callback(rtc, on_conn, ctx);
rtc_set_user_event_callback(rtc, on_user, ctx);
rtc_set_track_event_callback(rtc, on_track, ctx);
rtc_set_track_sample_callback(rtc, on_sample, ctx);

// 2) Then configure auto-subscribe
rtc_set_auto_subscribe(rtc, 1, 1);

// 3) Finally join the channel
rtc_join_channel_sync(rtc, token, 10000);

// ... application runs ...

rtc_leave_channel(rtc);
rtc_destroy(rtc);
```
