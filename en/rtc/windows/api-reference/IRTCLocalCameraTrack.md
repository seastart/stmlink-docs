---
title: "IRTCLocalCameraTrack"
description: "API reference for IRTCLocalCameraTrack, the Windows SRTC local camera track: update capture options (RTCCameraCaptureOptions) and start or stop camera capture. Read when publishing camera video."
---



## Description
The local video publishing object.



## Inheritance
[IRTCTrack](/en/rtc/windows/api-reference/IRTCTrack) -> [IRTCLocalVideoTrack](/en/rtc/windows/api-reference/IRTCLocalVideoTrack) ->IRTCLocalCameraTrack



## Methods
### Update capture options
```cpp
virtual StatusCode updateOptions(RTCCameraCaptureOptions* cap) = 0;
```

**Parameters**

| cap | Video track capture options; see [RTCCameraCaptureOptions](/en/rtc/windows/types#video-track-capture-options-rtccameracaptureoptions) |
| --- | --- |


Note:

1\. After updating, we recommend also updating the publishing options; otherwise the previous publishing parameters are used.

2\. If capture is already running, you don't need to start it again.



### Start capture
```cpp
virtual StatusCode startCapture(RTCCameraCaptureOptions* cap = nullptr) = 0;
```

**Parameters**

| cap | Video track capture options; see [RTCCameraCaptureOptions](/en/rtc/windows/types#video-track-capture-options-rtccameracaptureoptions) |
| --- | --- |




### Stop capture
```cpp
virtual StatusCode stopCapture() = 0;
```




