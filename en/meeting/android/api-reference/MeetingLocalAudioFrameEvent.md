---
title: "MeetingLocalAudioFrameEvent"
description: "Receive local mic PCM frames with their sample rate, channel count, and audio format through MeetingEngine.localAudioFrameEvent, with or without entering a meeting. Read this when you process local mic audio yourself."
---

`MeetingLocalAudioFrameEvent` receives explicitly subscribed local PCM frames and is registered through `MeetingEngine.localAudioFrameEvent`. You can extend `MeetingLocalAudioFrameSimpleEvent` and override only what you need.

## Usage notes

+ This event follows the Engine's local mic capture pipeline and doesn't require having entered a meeting; assigning `null` stops forwarding frames to your app.
+ Callbacks stay on the SRTC audio capture thread; don't perform time-consuming operations. Callbacks keep coming only while the ADM is recording.

## Methods

### onLocalAudioFrame(pcm, sampleRate, channelCount, audioFormat)

```kotlin
fun onLocalAudioFrame(
    pcm: ByteArray?,
    sampleRate: Int,
    channelCount: Int,
    audioFormat: Int
)
```

Description: Delivers one frame of local PCM audio data and its sampling parameters.

Parameters:

| Parameter | Description |
| --- | --- |
| `pcm` | Nullable PCM frame data. |
| `sampleRate` | Sample rate in Hz. |
| `channelCount` | Number of channels. |
| `audioFormat` | Audio sample format value defined by SRTC. |

Returns: None (`Unit`).
