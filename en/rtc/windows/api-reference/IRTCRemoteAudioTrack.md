---
title: "IRTCRemoteAudioTrack"
description: "API reference for IRTCRemoteAudioTrack, the Windows SRTC remote audio mixing object: start audio output to a speaker (RTCAudioOutputOptions) and stop it. Read when playing remote audio."
---

## Description
The remote audio mixing object.



## Inheritance
[IRTCTrack](/en/rtc/windows/api-reference/IRTCTrack) ->IRTCRemoteAudioTrack





## Methods
### Start audio output
```cpp
virtual StatusCode startPlay(RTCAudioOutputOptions* opt = nullptr) = 0;
```

**Parameters**

| opt | Audio track output options; see [RTCAudioOutputOptions](/en/rtc/windows/types#audio-track-output-options-rtcaudiooutputoptions) |
| --- | --- |




### Stop audio output
```cpp
virtual StatusCode stopPlay() = 0;
```



