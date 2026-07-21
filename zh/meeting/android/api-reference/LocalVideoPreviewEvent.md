---
title: "LocalVideoPreviewEvent"
description: "Android SMeeting 会议 SDK LocalVideoPreviewEvent 接口参考"
---

说明：`LocalVideoPreviewEvent` 是本地视频帧回调接口，用于接收本地采集的视频帧数据与尺寸/方向变化。通过 `MeetingEngine.localVideoPreviewEvent` 设置，适用于自渲染或对本地画面做二次处理的场景。

## 回调方法

### onVideoFrame(yuv, width, height, stamp, format, facing)
```kotlin
fun onVideoFrame(yuv: ByteArray?, width: Int, height: Int, stamp: Long, format: Int, facing: Int)
```
方法说明：本地视频帧回调。传出的 `yuv` 是 SDK 为外部应用单独拷贝的数据，应用层可以自行缓存或处理。  
参数说明：
- `yuv`：`ByteArray?`，视频帧数据。
- `width`：`Int`，视频帧宽度。
- `height`：`Int`，视频帧高度。
- `stamp`：`Long`，时间戳。
- `format`：`Int`，视频帧格式标识。
- `facing`：`Int`，摄像头方向标识。
返回值说明：无（`Unit`）。

### onFrameSizeChanged(width, height, facing)
```kotlin
fun onFrameSizeChanged(width: Int, height: Int, facing: Int)
```
方法说明：本地视频帧尺寸或摄像头方向变化回调。  
参数说明：
- `width`：`Int`，画面宽度。
- `height`：`Int`，画面高度。
- `facing`：`Int`，摄像头方向标识。
返回值说明：无（`Unit`）。
