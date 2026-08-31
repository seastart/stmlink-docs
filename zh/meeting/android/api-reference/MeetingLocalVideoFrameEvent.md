---
title: "MeetingLocalVideoFrameEvent"
description: "接收本地视频 YUV 帧以及采集尺寸或摄像头方向变化"
---

`MeetingLocalVideoFrameEvent` 接收显式订阅的本地视频帧，通过 `MeetingEngine.localVideoFrameEvent` 注册。可继承 `MeetingLocalVideoFrameSimpleEvent` 按需覆写。

## 特殊说明

该事件跟随 Engine 的本地摄像头采集链路，不要求已经加入会议；赋 `null` 即停止向应用转发帧。

## 注意事项

回调保持 SRTC 视频采集线程，不得执行磁盘、网络或其他耗时操作。`yuv` 是为外部调用方复制的数据，可在控制内存占用的前提下保存。

## 接口方法

### onLocalVideoFrame(yuv, width, height, stamp, format, facing)

```kotlin
fun onLocalVideoFrame(
    yuv: ByteArray?,
    width: Int,
    height: Int,
    stamp: Long,
    format: Int,
    facing: Int
)
```

方法说明：返回一帧本地 YUV 视频数据。

参数说明：

+ `yuv`：可空 YUV 帧数据。
+ `width`：画面宽度，单位像素。
+ `height`：画面高度，单位像素。
+ `stamp`：帧时间戳。
+ `format`：SRTC 定义的像素格式值。
+ `facing`：摄像头方向值。

返回值说明：无（`Unit`）。

### onLocalVideoFrameSizeChanged(width, height, facing)

```kotlin
fun onLocalVideoFrameSizeChanged(width: Int, height: Int, facing: Int)
```

方法说明：本地视频采集尺寸或摄像头方向发生变化。

参数说明：

+ `width`：新的画面宽度。
+ `height`：新的画面高度。
+ `facing`：新的摄像头方向值。

返回值说明：无（`Unit`）。
