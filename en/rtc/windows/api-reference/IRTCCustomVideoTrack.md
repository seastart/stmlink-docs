---
title: "IRTCCustomVideoTrack"
description: "API reference for IRTCCustomVideoTrack, the Windows SRTC custom video track: push your own encoded video frames (such as H.264 or H.265) with pushVideoFrame. Read when publishing video from a source other than a camera or screen."
---

## Description
The custom video track interface, used to push custom video data streams.

## Inheritance
[IRTCTrack](/en/rtc/windows/api-reference/IRTCTrack) -> IRTCCustomVideoTrack

## Methods

### Push a video frame
```cpp
virtual StatusCode pushVideoFrame(int stmtype, unsigned char* buf, int buf_len, int frmtype, long ts) = 0;
```

**Parameters**

| Parameter | Type | Description |
| --- | --- | --- |
| stmtype | int | Stream type (an encoding type such as H.264 or H.265) |
| buf | unsigned char* | Video frame data buffer |
| buf_len | int | Length of the data buffer |
| frmtype | int | Frame type (such as key frame or P-frame) |
| ts | long | Timestamp |

**Returns**

| Return value | Description |
| --- | --- |
| StatusCode | Status code of the operation result |

**Example**

```cpp
// Push an H.264 key frame
IRTCCustomVideoTrack* track = nullptr;
channel->getCustomVideoTrack("my_custom_track", &track);  // channel is an IRTCChannel* that has joined
track->pushVideoFrame(0x1b, frameData, frameSize, 1, timestamp);
```
