---
title: "类型定义"
description: "Python SDK 的数据类型与枚举：UserInfo、TrackInfo、ChannelInfo、ConnectionQuality、ActiveSpeaker、LayerSwitched、CustomMsg，以及 TrackKind、Codec、DeviceType、ConnectionState、DisconnectReason 和合成流常量的全部字段。"
---

所有信息类都是不可变的 `dataclass(frozen=True)`，拿到的是快照，修改不会影响 SDK 内部状态。媒体帧类型（`AudioFrame` / `VideoFrame` / `AudioFormat`）见 [音视频数据](/zh/rtc/python/api-reference/audio)。

---

## 信息类

### UserInfo

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `uid` | `str` | 用户 ID |
| `name` | `str` | 用户名 |
| `device_id` | `str` | 设备 ID |
| `version` | `str` | 客户端 SDK 版本 |
| `channel` | `str` | 所在频道名 |
| `sid` | `str` | 会话 ID，同一 uid 每次入会不同 |
| `device_type` | `int` | 终端类型，`DeviceType` 枚举值 |
| `is_audience` | `bool` | 是否观众 |
| `join_at` / `leave_at` / `updated_at` | `int` | 加入 / 离开 / 更新时间戳 |
| `props` | `dict` | 用户自定义属性 |
| `stream_tracks` | `tuple[TrackInfo, ...]` | 该用户已发布的轨道 |

### TrackInfo

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `id` | `str` | 轨道 ID |
| `uid` | `str` | 发布者 uid |
| `desc` | `str` | 轨道描述（发布时由业务指定，如 `"mic"`、`"camera"`） |
| `kind` | `TrackKind` | `AUDIO` / `VIDEO` |
| `codec` | `int` | 编码格式，`Codec` 枚举值 |
| `width` / `height` / `fps` / `angle` | `int` | 视频参数 |
| `bitrate` | `int` | 码率 |
| `sample_rate` / `channel_count` | `int` | 音频参数 |
| `props` | `dict` | 轨道自定义属性 |

### ChannelInfo

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `app_id` | `str` | 应用 ID |
| `channel` | `str` | 频道名 |
| `created_at` / `updated_at` | `int` | 创建 / 更新时间戳 |
| `props` | `dict` | 频道自定义属性 |

### ConnectionQuality

上下行网络质量，约每秒更新一次。

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `ts` | `int` | 报告生成时间（Unix 毫秒） |
| `pub` | `QualitySample` | 上行（本端 → 服务端） |
| `sub` | `QualitySample` | 下行（服务端 → 本端） |

`QualitySample`：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `score` | `float` | 质量分 0–100 |
| `level` | `str` | `excellent` / `good` / `poor` / `lost` |
| `mos` | `float` | 1.0–4.5 |
| `loss` | `float` | 丢包率 0–1 |
| `rtt` / `jitter` | `float` | 往返时延 / 抖动（毫秒） |
| `bitrate` | `float` | 平均码率（kbps） |
| `packets` / `bytes` | `int` | 本统计窗口的包数 / 字节数 |

### ActiveSpeaker

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `uid` | `str` | 说话人 |
| `track_id` | `str` | 音频轨道 ID |
| `level` | `float` | 音量 0.0–1.0 |

### LayerSwitched

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `sub_key` | `str` | 订阅句柄，形如 `"pub_uid:track_id"` |
| `from_track_id` / `to_track_id` | `str` | 切换前 / 后命中的层，首次起播时 `from_track_id` 为空 |
| `reason` | `str` | `bwe_down` / `bwe_up` / `track_refresh` / `track_upgrade` / `track_ended` / `client` |
| `latency_ms` | `int` | 从发起到切换完成的耗时 |

### CustomMsg

频道内自定义消息，由你的业务服务端通过 [服务端 API · 发送自定义消息](/zh/rtc/server-api/channel) 发出。客户端 SDK 只收不发。

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `action` | `str` | 业务动作标识 |
| `uid` / `sid` | `str` | 发送方 |
| `channel` | `str` | 频道名 |
| `is_private` | `bool` | `True` = 点对点发给你，`False` = 频道广播 |
| `content` | `Any` | 消息内容（已解析的 JSON） |

---

## 枚举

### TrackKind

`AUDIO` = 0，`VIDEO` = 1。

### Codec

`H264`、`H265`、`VP8`、`VP9`、`AV1`、`OPUS`、`AAC`。

### DeviceType

`WINDOWS`(1)、`ANDROID`(2)、`IOS`(3)、`LINUX`(4)、`MACOS`(5)、`WEBRTC`(6)、`XCX`(7，小程序)、`AGENTS`(80，服务端代理，本 SDK 入会时的身份)。其它值原样保留为 `int`。

### ConnectionState

`CONNECTING`(0)、`CONNECTED`(1)、`DISCONNECTED`(2)、`RECONNECTING`(3)。

### DisconnectReason

| 值 | 含义 | 是否应该自动重进 |
| --- | --- | --- |
| `SELF`(1) | 主动离开 | —— |
| `KICKED`(2) | 被踢出频道 | 否 |
| `REPLACE`(3) | 同一 uid 在别处入会，被顶号 | 否 |
| `TIMEOUT`(4) | 心跳超时 | 可以，用新 Token |
| `DESTROY`(5) | 频道被销毁 | 否 |
| `ERROR`(-1) | 出错离开，详情见 `on_disconnected` 的 `error` | 视错误而定 |

### ErrorCode

0.2.0 起。SDK 错误码的后三位（`IntEnum`，各端 SDK 统一），与 `SdkError.base_code` 比较，如 `e.base_code == srtc.ErrorCode.INVALID_ARGUMENT`。完整错误码 = `180` + 3 位补零的值，如 `INVALID_ARGUMENT`(31) 即 `180031`。

`UNKNOWN`(0)、`NOT_IN_CHANNEL`(1)、`TOKEN_EXPIRED`(2)、`TRACK_NOT_FOUND`(3)、`TOKEN_INVALID`(4)、`CONNECTION_FAILED`(6)、`CONNECTION_TIMEOUT`(7)、`SIGNALING_CONNECT_FAILED`(9)、`SIGNALING_SUBSCRIBE_FAILED`(10)、`MESSAGE_DECODE_FAILED`(11)、`WEBRTC_ERROR`(12)、`SDP_NEGOTIATION_FAILED`(13)、`TRANSPORT_NOT_READY`(14)、`PEER_CONNECTION_FAILED`(15)、`CODEC_NOT_SUPPORTED`(19)、`MAX_PUBLISH_LIMIT_REACHED`(20)、`ENGINE_DISCONNECTED`(23)、`INVALID_STATE`(24)、`INTERNAL_ERROR`(25)、`CANCELLED`(26)、`INVALID_ARGUMENT`(31)、`FEATURE_NOT_SUPPORTED`(32)、`MAX_SUBSCRIBE_LIMIT_REACHED`(34)、`PUBLISH_DESC_CONFLICT`(35)、`NOT_MCU_PUBLISHER`(40)、`USER_NOT_FOUND`(204)、`PUBLISH_FAILED`(300)、`SUBSCRIBE_FAILED`(301)、`PUBLISH_TIMEOUT`(302)、`SUBSCRIBE_TIMEOUT`(303)、`SUBSCRIBE_TRACK_NOT_FOUND`(304)。

各码含义见 [错误码](/zh/rtc/python/error-codes)。

---

## 常量

订阅频道合成流时使用：

| 常量 | 值 | 用途 |
| --- | --- | --- |
| `MCU_PUBLISHER_UID` | `"__mcu__"` | 合成流发布者 uid |
| `TRACK_AMCU_ID` | `"__amcu__"` | 音频合成流 track_id |
| `TRACK_MCU_ID` | `"__mcu__"` | 视频合成流 track_id |
