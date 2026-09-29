---
title: "Microphone preset"
description: "Android microphone track preset PreOptionMic: capture options (MicCaptureOptions for AEC, noise suppression, AGC, sample rate), publish options (AudioPublishOptions for codec, bitrate, DTX, RED), and the default PreOptionMic.def values. Read when configuring microphone capture or audio publishing."
---

This page describes the microphone track preset `PreOptionMic`. For the general preset structure (capture options + publish options), see [Camera preset](/en/rtc/android/presets/camera).

## PreOptionMic

Purpose: The microphone track preset, combining audio capture parameters with audio publish parameters.

### Structure

`PreOptionMic(capture: MicCaptureOptions, publish: AudioPublishOptions)`

| Property | Data type | Description |
| --- | --- | --- |
| capture | `MicCaptureOptions` | Microphone capture options |
| publish | `AudioPublishOptions` | Microphone audio publish options |

### Capture options MicCaptureOptions

Purpose: Configures microphone capture parameters.

| Property | Data type | Description |
| --- | --- | --- |
| deviceId | `String` | Device ID. |
| echoCancellation | `Boolean` | AEC (acoustic echo cancellation). |
| noiseSuppression | `Boolean` | ANS (noise suppression). |
| autoGainControl | `Boolean` | AGC (automatic gain control). |
| channelCount | `Int` | Number of audio channels (currently mono only). |
| sampleRate | `Int` | Sample rate (usually 16000 / 48000). |
| sampleSize | `Int` | Bit depth (default 16). |
| latency | `Double` | Latency parameter. |

### Publish options AudioPublishOptions

Purpose: Configures audio track publish parameters.

| Property | Data type | Description |
| --- | --- | --- |
| desc | `String` | Track description (default `TRACK_AUDIO`). |
| codec | `CodecType` | Codec (default `OPUS`). |
| maxBitrate | `Int` | Maximum bitrate. |
| dtx | `Boolean` | Audio discontinuous transmission. |
| red | `Boolean` | Redundant audio data. |
| props | `Any?` | Custom properties. |

### Built-in presets

Purpose: The SDK provides the default microphone preset `PreOptionMic.def`.

```kotlin
capture: deviceId="MicCapDef", echoCancellation=true, noiseSuppression=true, autoGainControl=true,
         channelCount=1, sampleRate=48000, sampleSize=16, latency=0.0
publish: desc="mic"(TRACK_AUDIO), codec=OPUS, maxBitrate=32*1024, dtx=true, red=true, props=null
```
