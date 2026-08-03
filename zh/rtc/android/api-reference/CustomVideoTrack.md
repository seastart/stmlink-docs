---
title: "CustomVideoTrack"
description: "推送外部已编码视频数据（H264 / H265）的自定义轨道"
---

## 说明

`CustomVideoTrack` 用于推送外部**已编码**视频数据（如 H264/H265），通过 [`RTCEngine.getCustomVideoTrack`](/zh/rtc/android/api-reference/RTCEngine) 获取。

> ⚠️ **不要与 [`LocalCustomVideoTrack`](/zh/rtc/android/api-reference/LocalCustomVideoTrack) 混用**：后者通过 `getLocalCustomVideoTrack(preOpt)` 获取，推送的是**未编码的原始 YUV 帧**，并且走 `publishLocalVideo` / `unPublishLocalVideo` 发布。两者都有 `inputData`，但参数与语义完全不同：本类是 `inputData(stamp, data, angle)`，`LocalCustomVideoTrack` 是 `inputData(yuv, width, height, strideY, strideU, strideV, rotation, stamp)`。若外部数据尚未编码，请使用 `LocalCustomVideoTrack`。

## CustomVideoTrack 自身方法

### startCustomVideo(option, listener)
```kotlin
fun startCustomVideo(option: CustomVideoOptions, listener: RTCResultListener?)
```
方法说明：开始推送自定义编码视频流。  
参数说明：
- `option`：`CustomVideoOptions`，自定义视频参数。
- `listener`：`RTCResultListener?`，开始推流结果回调，可为 `null`。
返回值说明：无（`Unit`）。

### stopCustomVideo(listener)
```kotlin
fun stopCustomVideo(listener: RTCResultListener?)
```
方法说明：停止推送自定义编码视频流。  
参数说明：
- `listener`：`RTCResultListener?`，停止推流结果回调，可为 `null`。
返回值说明：无（`Unit`）。

### inputData(stamp, data, angle)
```kotlin
fun inputData(stamp: Long, data: ByteArray, angle: Int)
```
方法说明：输入已编码视频帧数据。  
参数说明：
- `stamp`：`Long`，帧时间戳。
- `data`：`ByteArray`，编码后视频数据。
- `angle`：`Int`，当前帧角度（0/90/180/270）。
返回值说明：无（`Unit`）。
