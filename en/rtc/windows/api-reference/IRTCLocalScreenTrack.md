---
title: "IRTCLocalScreenTrack"
description: "API reference for IRTCLocalScreenTrack, the Windows SRTC local screen sharing track: update capture options (RTCScreenCaptureOptions) and start or stop screen capture. Read when implementing screen sharing."
---



## Description
The local screen track object.



## Inheritance
[IRTCTrack](/en/rtc/windows/api-reference/IRTCTrack) -> [IRTCLocalVideoTrack](/en/rtc/windows/api-reference/IRTCLocalVideoTrack) ->IRTCLocalScreenTrack



## Methods
### Update capture options
```cpp
virtual StatusCode updateOptions(RTCScreenCaptureOptions* cap) = 0;
```

**Parameters**

| cap | Screen track capture options; see [RTCScreenCaptureOptions](/en/rtc/windows/types#screen-track-capture-options-rtcscreencaptureoptions) |
| --- | --- |


Note:

1\. After updating, we recommend also updating the publishing options; otherwise the previous publishing parameters are used.

2\. If capture is already running, you don't need to start it again.

### Start capture
```cpp
virtual StatusCode startCapture(RTCScreenCaptureOptions* cap = nullptr) = 0;
```

**Parameters**

| cap | Screen track capture options; see [RTCScreenCaptureOptions](/en/rtc/windows/types#screen-track-capture-options-rtcscreencaptureoptions) |
| --- | --- |




### Stop capture
```cpp
virtual StatusCode stopCapture() = 0;
```




