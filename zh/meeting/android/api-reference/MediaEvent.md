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

### onActiveSpeakersChanged(speakers)
```kotlin
fun onActiveSpeakersChanged(speakers: List<ActiveSpeakerInfo>)
```
方法说明：活跃说话人状态变化回调。  
参数说明：
- `speakers`：`List<ActiveSpeakerInfo>`，当前活跃说话人列表。
返回值说明：无（`Unit`）。

### onCameraDeviceListChanged(devices)
```kotlin
fun onCameraDeviceListChanged(devices: List<CameraDeviceCapability>)
```
方法说明：当前系统摄像头列表发生变化回调。  
参数说明：
- `devices`：`List<CameraDeviceCapability>`，当前可用摄像头设备能力列表。
返回值说明：无（`Unit`）。

### onCameraDeviceDisconnected(cameraId)
```kotlin
fun onCameraDeviceDisconnected(cameraId: String)
```
方法说明：指定摄像头设备与系统物理断开或不再可用回调。  
参数说明：
- `cameraId`：`String`，摄像头设备 ID。
返回值说明：无（`Unit`）。

### onCameraDeviceError(cameraId, errorCode, message)
```kotlin
fun onCameraDeviceError(cameraId: String, errorCode: Int, message: String?)
```
方法说明：指定摄像头设备在采集过程中发生运行时错误回调。  
参数说明：
- `cameraId`：`String`，摄像头设备 ID。
- `errorCode`：`Int`，错误码。
- `message`：`String?`，错误描述。
返回值说明：无（`Unit`）。
