---
title: "MediaEvent"
description: "Android SMeeting 会议 SDK MediaEvent 接口参考"
---

说明：`MediaEvent` 是流媒体事件回调接口，用于接收媒体连接、音视频帧与统计信息事件。

## 回调方法

### onMediaConnected()
```kotlin
fun onMediaConnected()
```
方法说明：流媒体服务器连接成功回调。  
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
方法说明：远端视频帧回调。  
参数说明：
- `uid`：`String`，用户 uid。
- `trackDesc`：`String`，轨道描述。
- `y`：`ByteArray?`，Y 分量数据。
- `u`：`ByteArray?`，U 分量数据。
- `v`：`ByteArray?`，V 分量数据。
- `width`：`Int`，画面宽度。
- `height`：`Int`，画面高度。
- `format`：`Int`，图像格式标识。
- `angle`：`Int`，画面旋转角度。
返回值说明：无（`Unit`）。

### onPreviewFrame(yuv, width, height, stamp, format, facing)
```kotlin
fun onPreviewFrame(yuv: ByteArray?, width: Int, height: Int, stamp: Long, format: Int, facing: Int)
```
方法说明：本地预览视频帧回调。  
参数说明：
- `yuv`：`ByteArray?`，视频帧数据。
- `width`：`Int`，视频帧宽度。
- `height`：`Int`，视频帧高度。
- `stamp`：`Long`，时间戳。
- `format`：`Int`，视频帧格式。
- `facing`：`Int`，摄像头方向标识。
返回值说明：无（`Unit`）。

### onPreviewRealSize(width, height, facing)
```kotlin
fun onPreviewRealSize(width: Int, height: Int, facing: Int)
```
方法说明：本地视频流尺寸变化回调。  
参数说明：
- `width`：`Int`，画面宽度。
- `height`：`Int`，画面高度。
- `facing`：`Int`，摄像头方向标识。
返回值说明：无（`Unit`）。

### onMediaMetric(metric)
```kotlin
fun onMediaMetric(metric: MediaMetric.Metric)
```
方法说明：媒体性能指标回调。  
参数说明：
- `metric`：`MediaMetric.Metric`，媒体性能指标数据。
返回值说明：无（`Unit`）。

### onVolumesReport(volumes)
```kotlin
fun onVolumesReport(volumes: MutableMap<UserTrackDesc, VolumeInfo>)
```
方法说明：音量信息回调。  
参数说明：
- `volumes`：`MutableMap<UserTrackDesc, VolumeInfo>`，音量数据映射。
返回值说明：无（`Unit`）。
