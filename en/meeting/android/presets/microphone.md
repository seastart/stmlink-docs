---
title: "Mic presets"
description: "The PreOptionMic mic preset of the SMeeting Android SDK: MicCaptureOptions (AEC, ANS, AGC, sample rate) and AudioPublishOptions (codec, bitrate, DTX, RED) fields, plus the built-in PreOptionMic.def values. Read this when tuning mic capture or audio publishing."
---

This page describes the mic preset `PreOptionMic`. For the general preset structure (capture configuration + publish configuration), see [Camera presets](/en/meeting/android/presets/camera).

## PreOptionMic

Purpose: Mic track preset that combines audio capture parameters and audio publish parameters.

### Structure

`PreOptionMic(capture: MicCaptureOptions, publish: AudioPublishOptions)`

| Property | Type | Description |
| --- | --- | --- |
| capture | `MicCaptureOptions` | Mic capture configuration |
| publish | `AudioPublishOptions` | Mic audio publish configuration |

### Capture configuration MicCaptureOptions

Purpose: Configures mic capture parameters.

| Property | Type | Description |
| --- | --- | --- |
| deviceId | `String` | Device ID. |
| echoCancellation | `Boolean` | AEC echo cancellation. |
| noiseSuppression | `Boolean` | ANS noise suppression. |
| autoGainControl | `Boolean` | AGC automatic gain control. |
| channelCount | `Int` | Number of channels (currently mono only). |
| sampleRate | `Int` | Sample rate (usually 16000 / 48000). |
| sampleSize | `Int` | Bit depth (default 16). |
| latency | `Double` | Latency parameter. |

### Publish configuration AudioPublishOptions

Purpose: Configures audio track publish parameters.

| Property | Type | Description |
| --- | --- | --- |
| desc | `String` | Track description (default `TRACK_AUDIO`). |
| codec | `CodecType` | Codec (default `OPUS`). |
| maxBitrate | `Int` | Maximum bitrate. |
| dtx | `Boolean` | Audio discontinuous transmission. |
| red | `Boolean` | Redundant audio data. |
| props | `Any?` | Custom properties. |

### Built-in presets

Purpose: The SDK provides the default mic preset `PreOptionMic.def`.

```kotlin
capture: deviceId="MicCapDef", echoCancellation=true, noiseSuppression=true, autoGainControl=true,
         channelCount=1, sampleRate=48000, sampleSize=16, latency=0.0
publish: desc="mic"(TRACK_AUDIO), codec=OPUS, maxBitrate=32*1024, dtx=true, red=true, props=null
```
