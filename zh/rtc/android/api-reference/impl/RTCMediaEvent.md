---
title: "RTCMediaEvent"
description: "Android SRTC 音视频 SDK RTCMediaEvent 接口参考"
---

## 说明

`RTCMediaEvent` 为媒体层事件回调接口。

## 接口方法

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
- `uid`：`String`，远端用户 ID。
- `trackDesc`：`String`，轨道描述。
- `y`：`ByteArray?`，Y 分量数据。
- `u`：`ByteArray?`，U 分量数据。
- `v`：`ByteArray?`，V 分量数据。
- `width`：`Int`，帧宽度。
- `height`：`Int`，帧高度。
- `format`：`Int`，像素格式标识。
- `angle`：`Int`，帧角度。
返回值说明：无（`Unit`）。

### onPreviewFrame(yuv, width, height, stamp, format, facing)
```kotlin
fun onPreviewFrame(
    yuv: ByteArray?,
    width: Int,
    height: Int,
    stamp: Long,
    format: Int,
    facing: Int
)
```
方法说明：本地预览视频帧回调。  
参数说明：
- `yuv`：`ByteArray?`，YUV 数据。
- `width`：`Int`，帧宽度。
- `height`：`Int`，帧高度。
- `stamp`：`Long`，时间戳。
- `format`：`Int`，像素格式标识。
- `facing`：`Int`，摄像头朝向标识。
返回值说明：无（`Unit`）。

### onPreviewRealSize(width, height, facing)
```kotlin
fun onPreviewRealSize(width: Int, height: Int, facing: Int)
```
方法说明：本地预览尺寸变化回调。  
参数说明：
- `width`：`Int`，画面宽度。
- `height`：`Int`，画面高度。
- `facing`：`Int`，摄像头朝向标识。
返回值说明：无（`Unit`）。

### onMediaMetric(metric)
```kotlin
fun onMediaMetric(metric: MediaMetric.Metric)
```
方法说明：媒体性能指标回调。  
参数说明：
- `metric`：`MediaMetric.Metric`，媒体性能指标对象（对象字段请参考 `MediaMetric` 文档）。
返回值说明：无（`Unit`）。

### onVolumesReport(volumes)
```kotlin
fun onVolumesReport(volumes: MutableMap<UserTrackDesc, VolumeInfo>)
```
方法说明：音量信息回调。  
参数说明：
- `volumes`：`MutableMap<UserTrackDesc, VolumeInfo>`，音量映射（对象字段请分别参考 `UserTrackDesc` 与 `VolumeInfo` 文档）。
返回值说明：无（`Unit`）。
