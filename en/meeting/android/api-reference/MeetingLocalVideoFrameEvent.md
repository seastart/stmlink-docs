---
title: "MeetingLocalVideoFrameEvent"
description: "Receive local YUV video frames and capture size or camera facing changes through MeetingEngine.localVideoFrameEvent, with or without entering a meeting. Read this when you process or record local camera frames yourself."
---

`MeetingLocalVideoFrameEvent` receives explicitly subscribed local video frames and is registered through `MeetingEngine.localVideoFrameEvent`. You can extend `MeetingLocalVideoFrameSimpleEvent` and override only what you need.

## Usage notes

+ This event follows the Engine's local camera capture pipeline and doesn't require having entered a meeting; assigning `null` stops forwarding frames to your app.
+ Callbacks stay on the SRTC video capture thread; don't perform disk, network, or other time-consuming operations. `yuv` is data copied for the external caller, so you can keep it as long as you keep memory usage under control.

## Methods

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

Description: Delivers one frame of local YUV video data.

Parameters:

| Parameter | Description |
| --- | --- |
| `yuv` | Nullable YUV frame data. |
| `width` | Video width in pixels. |
| `height` | Video height in pixels. |
| `stamp` | Frame timestamp. |
| `format` | Pixel format value defined by SRTC. |
| `facing` | Camera facing value. |

Returns: None (`Unit`).

### onLocalVideoFrameSizeChanged(width, height, facing)

```kotlin
fun onLocalVideoFrameSizeChanged(width: Int, height: Int, facing: Int)
```

Description: The local video capture size or camera facing changed.

Parameters:

| Parameter | Description |
| --- | --- |
| `width` | New video width. |
| `height` | New video height. |
| `facing` | New camera facing value. |

Returns: None (`Unit`).
