---
title: "LocalMicTrack"
description: "Android shared microphone capture track: explicitly start and stop capture independently of any channel, read the volume, enumerate and switch input devices, receive local PCM, and publish to one or more channels. Read when working with microphone audio on Android."
---

`LocalMicTrack` is created by `RTCEngine.getLocalMicTrack(...)`. Microphone capture is decoupled from joining a channel and publishing audio: the app must explicitly call `startCapture(...)` to open the shared microphone, then publish through `RTCEngine` or `RTCChannel.publishLocalAudio(...)`.

The same `LocalMicTrack` can be published to multiple channels. Unpublishing from one channel doesn't stop capture; `stopCapture()` closes the shared data source and affects every channel still using the track.

## startCapture(listener)

```kotlin
fun startCapture(listener: RTCResultListener?)
```

Opens microphone capture. Repeated calls with the same parameters are idempotent. After it succeeds, you can read the volume, receive local PCM callbacks, or publish to a channel.

| Parameter | Type | Description |
| --- | --- | --- |
| `listener` | `RTCResultListener?` | The start result; can be `null`. For failure codes, see [Error codes](/en/rtc/android/error-codes). |

## stopCapture()

```kotlin
fun stopCapture()
```

Closes shared microphone capture. Calling it when capture hasn't started is idempotent.

## getVolume()

```kotlin
fun getVolume(): Int
```

Returns the real-time microphone volume in dBFS, roughly in the range `[-60, 0]`; returns the implementation's silence value when not capturing.

## switchMicDevice(deviceId)

```kotlin
fun switchMicDevice(deviceId: String)
```

Switches the microphone input device. `deviceId` comes from `getMicDevices()` and is valid only while the device stays connected; switching during capture rebuilds the recording pipeline.

## getMicDevices()

```kotlin
fun getMicDevices(): List<MicDeviceCapability>
```

Returns the capabilities of the microphone input devices currently available on the system. For fields, see [Types](/en/rtc/android/types). `getMicDevices()` and `switchMicDevice(...)` on the Engine are convenience entry points to the same shared capture module.

## Local PCM callback

```kotlin
rtcEngine.setRtcLocalAudioFrameEvent(object : RTCLocalAudioFrameEvent {
    override fun onLocalAudioFrame(
        pcm: ByteArray?,
        sampleRate: Int,
        channelCount: Int,
        audioFormat: Int
    ) {
        // Don't perform time-consuming I/O on the callback thread
    }
})

val micTrack = rtcEngine.getLocalMicTrack(PreOptionMic.def)
micTrack.startCapture(listener)
```

Registering the frame listener alone doesn't open the microphone. For full parameters, see [RTCLocalAudioFrameEvent](/en/rtc/android/api-reference/RTCLocalAudioFrameEvent).
