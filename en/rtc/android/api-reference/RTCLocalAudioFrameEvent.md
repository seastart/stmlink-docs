---
title: "RTCLocalAudioFrameEvent"
description: "Android callback that delivers local PCM frames from shared microphone capture, for local recording, writing to disk, or app-level audio processing: parameters, threading, and the requirement to start LocalMicTrack capture. Read when you need raw local microphone audio on Android."
---

Register the local PCM callback with `RTCEngine.setRtcLocalAudioFrameEvent(...)`; pass `null` to unbind. The callback belongs to the Engine's shared capture layer and carries no channel ID; in multi-channel scenarios, each physically captured frame is delivered only once, and the SDK's own publishing doesn't depend on this listener.

## onLocalAudioFrame(pcm, sampleRate, channelCount, audioFormat)

```kotlin
fun onLocalAudioFrame(
    pcm: ByteArray?,
    sampleRate: Int,
    channelCount: Int,
    audioFormat: Int
)
```

| Parameter | Type | Description |
| --- | --- | --- |
| `pcm` | `ByteArray?` | PCM data copied by the SDK for the app, usually 16-bit little-endian. |
| `sampleRate` | `Int` | Sample rate in Hz, for example `48000`. |
| `channelCount` | `Int` | Number of audio channels; `1` is mono, `2` is stereo. |
| `audioFormat` | `Int` | Sample format, consistent with `android.media.AudioFormat.ENCODING_*`. |

:::warning
Registering the listener doesn't open the microphone by itself. You must call `LocalMicTrack.startCapture(...)`; PCM callbacks start only after it succeeds, and stop after you call `stopCapture()`.

Callbacks run serially on the SDK's audio dispatch thread and aren't guaranteed to be on the main thread. The PCM is a separate copy for the app, so modifying it doesn't affect the SDK's uplink, and time-consuming processing doesn't block the uplink either; however, when the side queue stays full, older app callback frames are dropped first. For recording or writing to disk, still hand frames off quickly to your app's own work queue.
:::

```kotlin
rtcEngine.setRtcLocalAudioFrameEvent(object : RTCLocalAudioFrameEvent {
    override fun onLocalAudioFrame(
        pcm: ByteArray?,
        sampleRate: Int,
        channelCount: Int,
        audioFormat: Int
    ) {
        // Hand off quickly to the app's own recording or processing queue
    }
})

val micTrack = rtcEngine.getLocalMicTrack(PreOptionMic.def)
micTrack.startCapture(null)
```
