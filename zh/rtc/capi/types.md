---
title: "类型定义"
description: "SRTC C SDK 的结构体、编码常量、枚举取值与回调签名一览"
---

本页汇总 `librtc.h` 中对外暴露的数据结构与常量。

---

## 数据结构

### rtc_track_info_t

轨道信息。出现在轨道事件回调、轨道数据回调，以及用户信息的 `stream_tracks` 数组里。

```c
typedef struct {
    char track_id[64];
    char uid[64];
    char desc[64];
    int kind;
    int codec;
    int width;
    int height;
    int fps;
    int angle;
    int bitrate;
    int sample_rate;
    int channel_count;
    const char* props;
} rtc_track_info_t;
```

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `track_id` | `char[64]` | 轨道 ID |
| `uid` | `char[64]` | 所属用户 uid |
| `desc` | `char[64]` | 轨道描述，如 `camera` / `screen` / `microphone` |
| `kind` | `int` | `0`=音频，`1`=视频 |
| `codec` | `int` | 编码格式，取值见下方[编码格式](#编码格式) |
| `width` / `height` | `int` | 视频分辨率 |
| `fps` | `int` | 帧率 |
| `angle` | `int` | 视频角度 |
| `bitrate` | `int` | 码率（bps） |
| `sample_rate` | `int` | 音频采样率 |
| `channel_count` | `int` | 音频声道数 |
| `props` | `const char*` | 自定义业务属性，JSON 字符串；可能为 `NULL` |

### rtc_user_info_t

用户信息。由 `rtc_get_user_info` / `rtc_get_users_info` 返回，也出现在轨道数据回调里。

```c
typedef struct {
    char uid[64];
    char name[128];
    char device_id[128];
    char version[64];
    char channel[128];
    char sid[128];
    const char* props;
    int device_type;
    int is_audience;
    int64_t join_at;
    int64_t leave_at;
    int64_t updated_at;
    int64_t link_id;
    rtc_track_info_t* stream_tracks;
    int stream_track_count;
} rtc_user_info_t;
```

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `uid` | `char[64]` | 用户 ID |
| `name` | `char[128]` | 用户名 |
| `device_id` | `char[128]` | 设备 ID |
| `version` | `char[64]` | 客户端 SDK 版本 |
| `channel` | `char[128]` | 所在频道名 |
| `sid` | `char[128]` | 会话 ID |
| `props` | `const char*` | 自定义业务属性，JSON 字符串；可能为 `NULL` |
| `device_type` | `int` | 设备类型 |
| `is_audience` | `int` | `1`=观众（不出现在他人成员列表里），`0`=普通用户 |
| `join_at` / `leave_at` / `updated_at` | `int64_t` | 加入 / 离开 / 更新时间戳 |
| `link_id` | `int64_t` | 连接 ID |
| `stream_tracks` | `rtc_track_info_t*` | 该用户已发布的轨道数组 |
| `stream_track_count` | `int` | 轨道数量 |

<Warning>
`props` 和 `stream_tracks` 是 SDK 动态分配的，查询接口返回的 `rtc_user_info_t` 必须用 `rtc_free_user_info` / `rtc_free_users_info` 释放。详见 [用户信息查询](/zh/rtc/capi/api-reference/users)。
</Warning>

### rtc_publish_options_t

发布选项，见 [发布与推流](/zh/rtc/capi/api-reference/publish)。

```c
typedef struct {
    char desc[64];         // 轨道描述（必填，不能为空串）
    int width;             // 视频宽度（视频必填）
    int height;            // 视频高度（视频必填）
    int fps;               // 帧率（视频必填）
    int sample_rate;       // 采样率（音频必填）
    int channel_count;     // 声道数（音频必填）
    int angle;             // 视频角度（可选）
    int bitrate;           // 码率 bps（可选）
    const char* props;     // 自定义属性，JSON 字符串（可选）
} rtc_publish_options_t;
```

### SeaStart 相关结构体

`rtc_layer_switched_t`、`rtc_quality_sample_t`、`rtc_connection_quality_t`、`rtc_active_speaker_t` 见 [SeaStart 进阶能力](/zh/rtc/capi/advanced/seastart)。

### rtc_custom_msg_t

见 [自定义消息](/zh/rtc/capi/advanced/custom-msg)。

---

## 常量

### 编码格式

```c
#define RTC_CODEC_H264  0x1b        // H264 视频
#define RTC_CODEC_H265  0x24        // H265 视频
#define RTC_CODEC_VP8   0x38        // VP8 视频
#define RTC_CODEC_VP9   0x39        // VP9 视频
#define RTC_CODEC_AV1   0x3a        // AV1 视频
#define RTC_CODEC_AAC   0x0f        // AAC 音频
#define RTC_CODEC_OPUS  0x5355504f  // OPUS 音频
```

头文件里还提供了一个内联辅助函数，用于把 codec 转成可读字符串：

```c
static inline const char* rtc_codec_to_string(int codec);
// 未知取值返回 "UNKNOWN"
```

### 日志级别

```c
#define RTC_LOG_DEBUG  0
#define RTC_LOG_INFO   1
#define RTC_LOG_WARN   2
#define RTC_LOG_ERROR  3
```

### 合成流保留标识

```c
#define RTC_MCU_PUBLISHER_UID "__mcu__"   // 合成流发布者 uid
#define RTC_TRACK_AMCU_ID     "__amcu__"  // 音频合成流 trackId
#define RTC_TRACK_MCU_ID      "__mcu__"   // 视频合成流 trackId
```

---

## 回调参数枚举

这些取值以 `int` 形式出现在回调参数里，头文件中没有对应的宏。

**连接状态**（`rtc_connection_callback` 的 `state`）

| 值 | 含义 |
| --- | --- |
| `0` | connecting，连接中 |
| `1` | connected，已连接 |
| `2` | disconnected，已断开 |
| `3` | reconnecting，重连中 |

**用户事件**（`rtc_user_event_callback` 的 `event_type`）

| 值 | 含义 |
| --- | --- |
| `0` | join，加入 |
| `1` | leave，离开 |

**轨道事件**（`rtc_track_event_callback` 的 `event_type`）

| 值 | 含义 |
| --- | --- |
| `0` | add，新增 |
| `1` | update，更新 |
| `2` | remove，移除 |

**轨道类型**（`rtc_track_info_t.kind`）

| 值 | 含义 |
| --- | --- |
| `0` | 音频 |
| `1` | 视频 |

---

## 回调签名一览

```c
typedef void (*rtc_connection_callback)(void* context, int state);

typedef void (*rtc_user_event_callback)(void* context, const char* uid, int event_type);

typedef void (*rtc_track_event_callback)(void* context, const char* uid,
                                         rtc_track_info_t* track_info, int event_type);

typedef void (*rtc_track_sample_callback)(void* context,
                                          rtc_user_info_t* user_info,
                                          rtc_track_info_t* track_info,
                                          uint8_t* data, int len,
                                          int64_t timestamp, int64_t duration);

typedef void (*rtc_layer_switched_callback)(void* context, const rtc_layer_switched_t* data);

typedef void (*rtc_connection_quality_callback)(void* context, const rtc_connection_quality_t* q);

typedef void (*rtc_active_speakers_callback)(void* context, int64_t ts,
                                             const rtc_active_speaker_t* speakers,
                                             int speakers_count);

typedef void (*rtc_custom_msg_callback)(void* context, const rtc_custom_msg_t* msg);

typedef void (*rtc_keyframe_request_callback)(void* context, const char* track_id);
```
