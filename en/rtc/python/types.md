---
title: "Types"
description: "Data types and enums of the SRTC Python SDK: every field of UserInfo, TrackInfo, ChannelInfo, ConnectionQuality, ActiveSpeaker, LayerSwitched, and CustomMsg, plus TrackKind, Codec, DeviceType, ConnectionState, DisconnectReason, and the composite stream constants."
---

All info classes are immutable `dataclass(frozen=True)` objects. What you get is a snapshot, and modifying it doesn't affect the SDK's internal state. For media frame types (`AudioFrame` / `VideoFrame` / `AudioFormat`), see [Audio and video data](/en/rtc/python/api-reference/audio).

---

## Info classes

### UserInfo

| Field | Type | Description |
| --- | --- | --- |
| `uid` | `str` | User ID |
| `name` | `str` | User name |
| `device_id` | `str` | Device ID |
| `version` | `str` | Client SDK version |
| `channel` | `str` | Name of the channel the user is in |
| `sid` | `str` | Session ID; different each time the same uid joins |
| `device_type` | `int` | Client type, a `DeviceType` enum value |
| `is_audience` | `bool` | Whether the user is in audience mode |
| `join_at` / `leave_at` / `updated_at` | `int` | Join / leave / update timestamps |
| `props` | `dict` | Custom user properties |
| `stream_tracks` | `tuple[TrackInfo, ...]` | Tracks the user has published |

### TrackInfo

| Field | Type | Description |
| --- | --- | --- |
| `id` | `str` | Track ID |
| `uid` | `str` | Publisher's uid |
| `desc` | `str` | Track description (specified by your app when publishing, such as `"mic"` or `"camera"`) |
| `kind` | `TrackKind` | `AUDIO` / `VIDEO` |
| `codec` | `int` | Encoding format, a `Codec` enum value |
| `width` / `height` / `fps` / `angle` | `int` | Video parameters |
| `bitrate` | `int` | Bitrate |
| `sample_rate` / `channel_count` | `int` | Audio parameters |
| `props` | `dict` | Custom track properties |

### ChannelInfo

| Field | Type | Description |
| --- | --- | --- |
| `app_id` | `str` | App ID |
| `channel` | `str` | Channel name |
| `created_at` / `updated_at` | `int` | Creation / update timestamps |
| `props` | `dict` | Custom channel properties |

### ConnectionQuality

Uplink and downlink network quality, updated about once per second.

| Field | Type | Description |
| --- | --- | --- |
| `ts` | `int` | When the report was generated (Unix milliseconds) |
| `pub` | `QualitySample` | Uplink (local → server) |
| `sub` | `QualitySample` | Downlink (server → local) |

`QualitySample`:

| Field | Type | Description |
| --- | --- | --- |
| `score` | `float` | Quality score, 0–100 |
| `level` | `str` | `excellent` / `good` / `poor` / `lost` |
| `mos` | `float` | 1.0–4.5 |
| `loss` | `float` | Packet loss rate, 0–1 |
| `rtt` / `jitter` | `float` | Round-trip time / jitter (milliseconds) |
| `bitrate` | `float` | Average bitrate (kbps) |
| `packets` / `bytes` | `int` | Packets / bytes in this statistics window |

### ActiveSpeaker

| Field | Type | Description |
| --- | --- | --- |
| `uid` | `str` | The speaker |
| `track_id` | `str` | Audio track ID |
| `level` | `float` | Volume, 0.0–1.0 |

### LayerSwitched

| Field | Type | Description |
| --- | --- | --- |
| `sub_key` | `str` | Subscription handle, in the form `"pub_uid:track_id"` |
| `from_track_id` / `to_track_id` | `str` | The layer served before / after the switch; `from_track_id` is empty on initial playback |
| `reason` | `str` | `bwe_down` / `bwe_up` / `track_refresh` / `track_upgrade` / `track_ended` / `client` |
| `latency_ms` | `int` | Time from initiation to completion of the switch |

### CustomMsg

An in-channel custom message, sent by your backend through [Server API · Send a custom message](/en/rtc/server-api/channel). The client SDK only receives messages and doesn't send them.

| Field | Type | Description |
| --- | --- | --- |
| `action` | `str` | Business action identifier |
| `uid` / `sid` | `str` | Sender |
| `channel` | `str` | Channel name |
| `is_private` | `bool` | `True` = sent to you point-to-point, `False` = channel broadcast |
| `content` | `Any` | Message content (parsed JSON) |

---

## Enums

### TrackKind

`AUDIO` = 0, `VIDEO` = 1.

### Codec

`H264`, `H265`, `VP8`, `VP9`, `AV1`, `OPUS`, `AAC`.

### DeviceType

`WINDOWS`(1), `ANDROID`(2), `IOS`(3), `LINUX`(4), `MACOS`(5), `WEBRTC`(6), `XCX`(7, WeChat Mini Program), `AGENTS`(80, server-side agent—the identity this SDK joins with). Other values are kept as-is as `int`.

### ConnectionState

`CONNECTING`(0), `CONNECTED`(1), `DISCONNECTED`(2), `RECONNECTING`(3).

### DisconnectReason

| Value | Meaning | Should you rejoin automatically? |
| --- | --- | --- |
| `SELF`(1) | Left voluntarily | — |
| `KICKED`(2) | Removed from the channel | No |
| `REPLACE`(3) | Replaced by another session with the same uid that joined elsewhere | No |
| `TIMEOUT`(4) | Heartbeat timed out | Yes, with a new token |
| `DESTROY`(5) | The channel was destroyed | No |
| `ERROR`(-1) | Left due to an error; see `error` in `on_disconnected` for details | Depends on the error |

---

## Constants

Used when subscribing to the channel's composite stream:

| Constant | Value | Purpose |
| --- | --- | --- |
| `MCU_PUBLISHER_UID` | `"__mcu__"` | Publisher uid of the composite stream |
| `TRACK_AMCU_ID` | `"__amcu__"` | track_id of the audio composite stream |
| `TRACK_MCU_ID` | `"__mcu__"` | track_id of the video composite stream |
