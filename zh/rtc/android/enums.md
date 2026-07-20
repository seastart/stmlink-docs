---
title: "枚举类型"
description: "Android SRTC 音视频 SDK 枚举值定义"
---

### CodecType

| 枚举名 | 值 | 说明 |
| --- | --- | --- |
| unknow | 0 | 未知编码类型 |
| H264 | 0x1b | H264 编码 |
| H265 | 0x24 | H265 编码 |
| AAC | 0x0f | AAC 编码 |
| VP8 | 0x38 | VP8 编码 |
| VP9 | 0x39 | VP9 编码 |
| AV1 | 0x3a | AV1 编码 |
| OPUS | 0x5355504f | OPUS 编码 |

### DeviceType

| 枚举名 | 值 | 说明 |
| --- | --- | --- |
| Unknown | 0 | 未知设备类型 |
| Windows | 1 | Windows 设备 |
| Android | 2 | Android 设备 |
| iOS | 3 | iOS 设备 |
| Linux | 4 | Linux 设备 |
| MacOS | 5 | macOS 设备 |
| WebRTC | 6 | WebRTC 设备 |
| Rtmp | 7 | RTMP 设备 |

### LeaveReason

| 枚举名 | 值 | 说明 |
| --- | --- | --- |
| Error | -1 | 出错离开 |
| Unknown | 0 | 原因未知 |
| VoluntarilyLeave | 1 | 主动离开 |
| KickOut | 2 | 被踢出 |
| BeReplaced | 3 | 被顶号 |
| HeartbeatTimeout | 4 | 心跳超时 |
| ChannelDestroy | 5 | 频道销毁 |
| BecomeAudience | 6 | 成为观众 |

### TrackKind

| 枚举名 | 值 | 说明 |
| --- | --- | --- |
| VIDEO | "video" | 视频轨道 |
| AUDIO | "audio" | 音频轨道 |

### TrackDesc

| 枚举名 | 值 | 说明 |
| --- | --- | --- |
| TRACK_MAIN | "camera_big" | 主摄像头大流 |
| TRACK_SUB | "camera_small" | 摄像头小流 |
| TRACK_SHARE | "screen" | 屏幕共享流 |
| TRACK_AUDIO | "mic" | 麦克风音频流 |
| TRACK_CUSTOM | "custom" | 自定义流 |
| TRACK_UN_KNOW | "unknow" | 未知轨道描述 |

### MediaDownLevel

| 枚举名 | 值 | 说明 |
| --- | --- | --- |
| UnKnown | 1000 | 未知数据 |
| Normal | 0 | 下行质量正常 |
| Poor | -1 | 下行质量较差 |
| Bad | -2 | 下行质量很差 |
| VeryBad | -3 | 下行质量极差 |

### MediaDownLossLevel

| 枚举名 | 值 | 说明 |
| --- | --- | --- |
| Invalid | -1 | 无效值 |
| Normal | 0 | 丢包情况正常 |
| Poor | 1 | 丢包情况较差 |
| Bad | 2 | 丢包情况很差 |
| VeryBad | 3 | 丢包情况极差 |

### QualityDirection

网络质量变化方向，用于 [`NetworkQualityChange`](/zh/rtc/android/types)。

| 枚举名 | 值 | 说明 |
| --- | --- | --- |
| UPLINK | 无显式值 | 本端到服务端的上行。 |
| DOWNLINK | 无显式值 | 服务端到本端的下行。 |

### QualityTrend

网络质量变化趋势，用于 [`NetworkQualityChange`](/zh/rtc/android/types)。

| 枚举名 | 值 | 说明 |
| --- | --- | --- |
| INITIAL | 无显式值 | 首次建立档位（非跨档，用于初始化 UI）。 |
| DEGRADED | 无显式值 | 档位变差（立即回调）。 |
| RECOVERED | 无显式值 | 档位变好（已通过连续确认）。 |

### RemoteStreamStatus

| 枚举名 | 值 | 说明 |
| --- | --- | --- |
| NOT_SUBSCRIBED | "not_subscribed" | 未订阅 |
| STREAM_NORMAL | "stream_normal" | 流状态正常 |
| STREAM_CHOKE | "stream_choke" | 流状态阻塞 |

### StreamVendor

| 枚举名 | 值 | 说明 |
| --- | --- | --- |
| FY | "seastart" | 风远服务 |
| OOK | "ook" | 网仕服务 |
| WS | "wangsucdn" | 网宿 CDN |

### AudioOutputDeviceType

| 枚举名 | 值 | 说明 |
| --- | --- | --- |
| UN_KNOW | 无显式值 | 未知输出设备 |
| SPEAKER | 无显式值 | 扬声器 |
| EARPIECE | 无显式值 | 听筒 |
| WIRED_EARPHONE | 无显式值 | 有线耳机 |
| BLUETOOTH_HEADSET | 无显式值 | 蓝牙耳机 |

### ScreenRecordState

| 枚举名 | 值 | 说明 |
| --- | --- | --- |
| START | "start" | 开始录屏。 |
| STOP | "stop" | 停止录屏。 |
| ERROR | "error" | 录屏出错。 |
| AUDIO_ERROR | "audio_error" | 录屏音频出错。 |

### CameraCaptureOptions.CamraPosition

| 枚举名 | 值 | 说明 |
| --- | --- | --- |
| FRONT | "FRONT" | 前置摄像头。 |
| BACK | "BACK" | 后置摄像头。 |
| External | "external" | 外接摄像头。 |

