---
title: "IRTCLocalMicTrack"
description: "API reference for IRTCLocalMicTrack, the Windows SRTC local microphone track: update capture options (RTCMicCaptureOptions) and start or stop microphone capture. Read when publishing microphone audio."
---

## Description
The local audio publishing object.



## Inheritance
[IRTCTrack](/en/rtc/windows/api-reference/IRTCTrack) -> [IRTCLocalAudioTrack](/en/rtc/windows/api-reference/IRTCLocalAudioTrack) ->IRTCLocalMicTrack







## Methods
### Update capture options
```cpp
virtual StatusCode updateOptions(RTCMicCaptureOptions* cap) = 0;
```

**Parameters**

| cap | Audio track capture options; see [RTCMicCaptureOptions](/en/rtc/windows/types#audio-track-capture-options-rtcmiccaptureoptions) |
| --- | --- |


Note:

1\. After updating, we recommend also updating the publishing options; otherwise the previous publishing parameters are used.

2\. If capture is already running, you don't need to start it again.



### Start capture
```cpp
virtual StatusCode startCapture(RTCMicCaptureOptions* cap = nullptr) = 0;
```

**Parameters**

| cap | Audio track capture options; see [RTCMicCaptureOptions](/en/rtc/windows/types#audio-track-capture-options-rtcmiccaptureoptions) |
| --- | --- |




### Stop capture
```cpp
virtual StatusCode stopCapture() = 0;
```



