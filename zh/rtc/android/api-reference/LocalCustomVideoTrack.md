---
title: "LocalCustomVideoTrack"
description: "Android SMeeting 会议 SDK LocalCustomVideoTrack 接口参考"
---

## 说明

`LocalCustomVideoTrack` 用于向本地自定义视频轨道输入外部原始视频帧（YUV）。

轨道描述由创建该实例时的预设决定：
- `PreOptionCustomVideo.def`：默认自定义视频轨道（`TRACK_CUSTOM`）。
- `PreOptionCustomVideo.screen`：按屏幕共享描述发布（`TRACK_SHARE`）。

## LocalCustomVideoTrack 自身方法

### inputData(yuv, width, height, strideY, strideU, strideV, rotation, stamp)
```kotlin
fun inputData(
    yuv: ByteArray, width: Int, height: Int,
    strideY: Int, strideU: Int, strideV: Int,
    rotation: Int, stamp: Long
)
```
方法说明：输入一帧 YUV 原始视频数据。  
参数说明：
- `yuv`：`ByteArray`，YUV 原始帧数据。
- `width`：`Int`，视频宽度。
- `height`：`Int`，视频高度。
- `strideY`：`Int`，Y 平面步幅。
- `strideU`：`Int`，U 平面步幅。
- `strideV`：`Int`，V 平面步幅。
- `rotation`：`Int`，旋转角度。
- `stamp`：`Long`，帧时间戳。
返回值说明：无（`Unit`）。
