---
title: "CustomVideoTrack"
description: "Android SRTC 音视频 SDK CustomVideoTrack 接口参考"
---

## 说明

`CustomVideoTrack` 用于推送外部已编码视频数据（如 H264/H265）。

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
