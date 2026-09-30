---
title: "IRTCCustomAudioTrack"
description: "API reference for IRTCCustomAudioTrack, the Windows SRTC custom audio track: push your own encoded audio frames (such as AAC or Opus) with pushAudioFrame. Read when publishing audio from a source other than a microphone."
---

## Description
The custom audio track interface, used to push custom audio data streams.

## Inheritance
[IRTCTrack](/en/rtc/windows/api-reference/IRTCTrack) -> IRTCCustomAudioTrack

## Methods

### Push an audio frame
```cpp
virtual StatusCode pushAudioFrame(int stmtype, unsigned char* buf, int buf_len, long ts) = 0;
```

**Parameters**

| Parameter | Type | Description |
| --- | --- | --- |
| stmtype | int | Stream type (an encoding type such as AAC or Opus) |
| buf | unsigned char* | Audio frame data buffer |
| buf_len | int | Length of the data buffer |
| ts | long | Timestamp |

**Returns**

| Return value | Description |
| --- | --- |
| StatusCode | Status code of the operation result |

**Example**

```cpp
// Push an Opus audio frame
IRTCCustomAudioTrack* track = nullptr;
channel->getCustomAudioTrack("my_custom_audio", &track);  // channel is an IRTCChannel* that has joined
track->pushAudioFrame(0x5355504F, audioData, audioSize, timestamp);
```
