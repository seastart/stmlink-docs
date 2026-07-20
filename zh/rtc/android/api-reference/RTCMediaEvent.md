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

> 本地预览帧回调已从 `RTCMediaEvent` 拆出，改由 [`RTCEngine.setRtcLocalVideoFrameEvent`](/zh/rtc/android/api-reference/RTCEngine)（`RTCLocalVideoFrameEvent`）提供，对应 `onLocalVideoFrame` / `onLocalVideoFrameSizeChanged`。原 `onPreviewFrame` / `onPreviewRealSize` 已移除。

### onMediaMetric(metric)
```kotlin
fun onMediaMetric(metric: MediaMetric.Metric)
```
方法说明：媒体性能指标回调，入会后每约 5 秒下发一份完整快照。  
参数说明：
- `metric`：`MediaMetric.Metric`，媒体性能指标对象。字段参见 [媒体质量](/zh/rtc/android/media-quality)。
返回值说明：无（`Unit`）。

### onNetworkQualityChanged(change)
```kotlin
fun onNetworkQualityChanged(change: NetworkQualityChange)
```
方法说明：网络质量档位变化回调。仅在质量等级发生跨档变化时触发（而非每个采样周期），内置非对称迟滞——等级下降（变差）立即回调，等级回升（变好）需连续多次采样确认后才回调；上行、下行各自独立触发，一次回调只表示一个方向的变化。适合驱动网络状态灯与弱网提示。  
参数说明：
- `change`：`NetworkQualityChange`，本次档位变化详情（方向、前后等级、趋势及触发时的完整质量报告）。字段参见 [类型定义](/zh/rtc/android/types)。
返回值说明：无（`Unit`）。

:::note
本回调在信令通道的后台线程触发，更新 UI 前请切换到主线程。用法与弱网处理示例见 [网络质量](/zh/rtc/android/network-quality)。
:::

### onVolumesReport(volumes)
```kotlin
fun onVolumesReport(volumes: MutableMap<UserTrackDesc, VolumeInfo>)
```
方法说明：音量信息回调。  
参数说明：
- `volumes`：`MutableMap<UserTrackDesc, VolumeInfo>`，音量映射（`UserTrackDesc` 与 `VolumeInfo` 字段参见 [类型定义](/zh/rtc/android/types)）。
返回值说明：无（`Unit`）。

### onActiveSpeakersChanged(speakers)
```kotlin
fun onActiveSpeakersChanged(speakers: List<ActiveSpeakerInfo>)
```
方法说明：活跃说话人状态变化回调。  
参数说明：
- `speakers`：`List<ActiveSpeakerInfo>`，当前活跃说话人列表（含 `uid`、`trackId` 与服务端量化后的音量强度 `level`）。字段参见 [类型定义](/zh/rtc/android/types)。
返回值说明：无（`Unit`）。

### onCameraDeviceListChanged(devices)
```kotlin
fun onCameraDeviceListChanged(devices: List<CameraDeviceCapability>)
```
方法说明：当前系统摄像头列表发生变化回调（如外接摄像头插拔）。  
参数说明：
- `devices`：`List<CameraDeviceCapability>`，最新的可用摄像头设备能力列表。字段参见 [类型定义](/zh/rtc/android/types)。
返回值说明：无（`Unit`）。

### onCameraDeviceDisconnected(cameraId)
```kotlin
fun onCameraDeviceDisconnected(cameraId: String)
```
方法说明：指定摄像头设备与系统物理断开或不再可用时回调。  
参数说明：
- `cameraId`：`String`，断开的 Camera2 摄像头 ID。
返回值说明：无（`Unit`）。

### onCameraDeviceError(cameraId, errorCode, message)
```kotlin
fun onCameraDeviceError(cameraId: String, errorCode: Int, message: String?)
```
方法说明：指定摄像头设备在采集过程中发生运行时错误时回调。  
参数说明：
- `cameraId`：`String`，发生错误的 Camera2 摄像头 ID。
- `errorCode`：`Int`，错误码。
- `message`：`String?`，错误信息描述，可为 `null`。
返回值说明：无（`Unit`）。
