---
title: "MeetingMediaEvent"
description: "接收当前会议的媒体连接、远端原始帧、媒体统计、音量、活跃说话人与网络质量变化"
---

`MeetingMediaEvent` 承载当前会议的媒体事件，通过 `MeetingEngine.mediaEvent` 注册。可继承 `MeetingMediaSimpleEvent` 按需覆写。

## 使用说明

+ 该接口同时包含连接状态、原始远端帧和聚合质量统计；单条远端视频的接收状态应使用 `MeetingRemoteVideoEvent`。

+ `onRemoteVideoFrame()` 在 SRTC 媒体线程回调，不得阻塞。
+ 媒体统计通常约每 5 秒产生一次；弱网档位变化优先使用 `onNetworkQualityChanged()`。
+ 该监听在离会时清除，下一场会议需要重新赋值。

## 接口方法

### onMediaConnected()

```kotlin
fun onMediaConnected()
```

方法说明：当前会议的 SRTC 流媒体服务器连接成功。

参数说明：无。

返回值说明：无（`Unit`）。

### onRemoteVideoFrame(uid, trackDesc, y, u, v, width, height, format, angle)

```kotlin
fun onRemoteVideoFrame(
    uid: String,
    trackDesc: String,
    y: ByteArray?,
    u: ByteArray?,
    v: ByteArray?,
    width: Int,
    height: Int,
    format: Int,
    angle: Int
)
```

方法说明：收到一帧远端视频原始数据。

参数说明：

| 参数 | 说明 |
| --- | --- |
| `uid` | 远端用户 UID。 |
| `trackDesc` | 远端轨道描述。 |
| `y` | 可空 Y 图像分量。 |
| `u` | 可空 U 图像分量。 |
| `v` | 可空 V 图像分量。 |
| `width` | 画面宽度，单位像素。 |
| `height` | 画面高度，单位像素。 |
| `format` | SRTC 定义的像素格式值。 |
| `angle` | 画面旋转角度。 |

返回值说明：无（`Unit`）。

### onMediaMetric(metric)

```kotlin
fun onMediaMetric(metric: MediaMetric.Metric)
```

方法说明：返回当前会议的媒体性能指标快照。

参数说明：

| 参数 | 说明 |
| --- | --- |
| `metric` | 发送、接收、网络与服务端质量统计，字段见[媒体质量](/zh/meeting/android/media-quality)。 |

返回值说明：无（`Unit`）。

### onVolumesReport(volumes)

```kotlin
fun onVolumesReport(volumes: MutableMap<UserTrackDesc, VolumeInfo>)
```

方法说明：返回当前会议各用户轨道的音量快照。

参数说明：

| 参数 | 说明 |
| --- | --- |
| `volumes` | 以 `UserTrackDesc` 标识用户轨道的音量映射。 |

返回值说明：无（`Unit`）。

### onActiveSpeakersChanged(speakers)

```kotlin
fun onActiveSpeakersChanged(speakers: List<ActiveSpeakerInfo>)
```

方法说明：当前会议的活跃说话人列表发生变化。

参数说明：

| 参数 | 说明 |
| --- | --- |
| `speakers` | 按 SRTC 规则排序的活跃说话人快照。 |

返回值说明：无（`Unit`）。

### onNetworkQualityChanged(change)

```kotlin
fun onNetworkQualityChanged(change: NetworkQualityChange)
```

方法说明：当前会议的上行或下行网络质量跨档变化。

参数说明：

| 参数 | 说明 |
| --- | --- |
| `change` | 方向、旧等级、新等级和变化趋势等信息。 |

返回值说明：无（`Unit`）。数据类型见 [SRTC 类型](/zh/rtc/android/types)，等级见 [SRTC 枚举](/zh/rtc/android/enums)。
