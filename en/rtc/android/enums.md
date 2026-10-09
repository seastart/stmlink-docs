---
title: "Enums"
description: "Android SRTC SDK enum values, including RtcLanguage, codec, device, track, quality, vendor, audio output, and screen capture enums. Read when you need the values and meanings of Android SDK enums."
---

### RtcLanguage

Used by `RTCEngine.setLanguage(...)` to set the language for subsequent channel and IM backend requests.

| Enum name | Language tag | Description |
| --- | --- | --- |
| `SYSTEM` | `null` | Follow the system language. |
| `ZH_CN` | `zh-CN` | Simplified Chinese. |
| `EN` | `en` | English. |

### CodecType

| Enum name | Value | Description |
| --- | --- | --- |
| unknow | 0 | Unknown codec type |
| H264 | 0x1b | H264 codec |
| H265 | 0x24 | H265 codec |
| AAC | 0x0f | AAC codec |
| VP8 | 0x38 | VP8 codec |
| VP9 | 0x39 | VP9 codec |
| AV1 | 0x3a | AV1 codec |
| OPUS | 0x5355504f | OPUS codec |

### DeviceType

| Enum name | Value | Description |
| --- | --- | --- |
| Unknown | 0 | Unknown device type |
| Windows | 1 | Windows device |
| Android | 2 | Android device |
| iOS | 3 | iOS device |
| Linux | 4 | Linux device |
| MacOS | 5 | macOS device |
| WebRTC | 6 | WebRTC device |
| Rtmp | 7 | RTMP device |

### LeaveReason

| Enum name | Value | Description |
| --- | --- | --- |
| Error | -1 | Left due to an error |
| Unknown | 0 | Unknown reason |
| VoluntarilyLeave | 1 | Left voluntarily |
| KickOut | 2 | Removed from the channel |
| BeReplaced | 3 | Replaced by another session with the same uid |
| HeartbeatTimeout | 4 | Heartbeat timed out |
| ChannelDestroy | 5 | Channel destroyed |
| BecomeAudience | 6 | Became audience |

### TrackKind

| Enum name | Value | Description |
| --- | --- | --- |
| VIDEO | "video" | Video track |
| AUDIO | "audio" | Audio track |

### TrackDesc

| Enum name | Value | Description |
| --- | --- | --- |
| TRACK_MAIN | "camera_big" | Main camera high stream |
| TRACK_SUB | "camera_small" | Camera low stream |
| TRACK_SHARE | "screen" | Screen sharing stream |
| TRACK_AUDIO | "mic" | Microphone audio stream |
| TRACK_CUSTOM | "custom" | Custom stream |
| TRACK_UN_KNOW | "unknow" | Unknown track description |

### QualityDirection

The direction of a network quality change, used in [`NetworkQualityChange`](/en/rtc/android/types).

| Enum name | Value | Description |
| --- | --- | --- |
| UPLINK | No explicit value | Uplink from this client to the server. |
| DOWNLINK | No explicit value | Downlink from the server to this client. |

### QualityTrend

The trend of a network quality change, used in [`NetworkQualityChange`](/en/rtc/android/types).

| Enum name | Value | Description |
| --- | --- | --- |
| INITIAL | No explicit value | The level is established for the first time (used to initialize the UI). |
| DEGRADED | No explicit value | The level got worse than last time. |
| RECOVERED | No explicit value | The level got better than last time. |
| STABLE | No explicit value | The level is the same as last time, or this level can't be recognized. |

### StreamVendor

| Enum name | Value | Description |
| --- | --- | --- |
| FY | "seastart" | FY (Freewind) service |
| WS | "wangsucdn" | Wangsu CDN |

### AudioOutputDeviceType

| Enum name | Value | Description |
| --- | --- | --- |
| UN_KNOW | No explicit value | Unknown output device |
| SPEAKER | No explicit value | Speaker |
| EARPIECE | No explicit value | Earpiece |
| WIRED_EARPHONE | No explicit value | Wired headset |
| BLUETOOTH_HEADSET | No explicit value | Bluetooth headset |

### ScreenCaptureState

| Enum name | Value | Description |
| --- | --- | --- |
| START | "start" | Screen capture has started. |
| STOP | "stop" | Screen capture has stopped. |
| ERROR | "error" | Screen capture failed to start or failed while running. |

### CameraCaptureOptions.CamraPosition

| Enum name | Value | Description |
| --- | --- | --- |
| FRONT | "FRONT" | Front camera. |
| BACK | "BACK" | Rear camera. |
| External | "external" | External camera. |
