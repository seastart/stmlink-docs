---
title: "RTCMediaEvent"
description: "单频道媒体事件：媒体连接、远端视频帧、质量统计、音量和活跃说话人；每个回调均携带频道 ID"
---

`RTCMediaEvent` 承载一条频道的媒体事件。`RTCEngine.setRtcMediaEvent(...)` 设置默认频道监听器；额外频道使用 `RTCChannel.setRtcMediaEvent(...)`。只关心少量事件时，建议继承 `RTCMediaSimpleEvent`。

所有回调的第一个参数都是 `channel: String`，用于在多频道场景中明确事件归属。

## 接口方法

### onMediaConnected(channel)

```kotlin
fun onMediaConnected(channel: String)
```

本频道的流媒体服务器连接成功。

### onRemoteVideoFrame(channel, uid, trackDesc, y, u, v, width, height, format, angle)

```kotlin
fun onRemoteVideoFrame(
    channel: String,
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

收到本频道的一帧远端视频。`uid` 和 `trackDesc` 定位远端 Track；`y`、`u`、`v` 为图像分量，`width` / `height` 为尺寸，`format` 为像素格式，`angle` 为旋转角度。

### onMediaMetric(channel, metric)

```kotlin
fun onMediaMetric(channel: String, metric: MediaMetric.Metric)
```

本频道的媒体性能指标快照，入会后约每 5 秒回调一次。字段见 [媒体质量](/zh/rtc/android/media-quality)。

### onNetworkQualityChanged(channel, change)

```kotlin
fun onNetworkQualityChanged(
    channel: String,
    change: NetworkQualityChange
)
```

本频道网络质量发生跨档变化。等级变差立即回调，变好需要连续采样确认；上、下行独立触发。回调运行在 SDK 后台线程，更新 UI 前请切换到主线程。用法见 [网络质量](/zh/rtc/android/network-quality)。

### onVolumesReport(channel, volumes)

```kotlin
fun onVolumesReport(
    channel: String,
    volumes: MutableMap<UserTrackDesc, VolumeInfo>
)
```

本频道的音量信息。

### onActiveSpeakersChanged(channel, speakers)

```kotlin
fun onActiveSpeakersChanged(
    channel: String,
    speakers: List<ActiveSpeakerInfo>
)
```

本频道的活跃说话人列表发生变化。

:::note
摄像头设备增删和运行时错误是 Engine 全局事件，已从 `RTCMediaEvent` 移至 [`RTCCameraDeviceEvent`](/zh/rtc/android/api-reference/RTCCameraDeviceEvent)，不会因多频道而重复回调。本地视频帧与本地音频帧也分别使用独立监听器。
:::
