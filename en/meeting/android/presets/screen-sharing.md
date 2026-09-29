---
title: "Screen sharing presets"
description: "The PreOptionScreen screen sharing preset of the SMeeting Android SDK: ScreenCaptureOptions fields, the VideoPublishOptions publish configuration with TRACK_SHARE, and the built-in PreOptionScreen.def values. Read this when tuning screen sharing resolution, frame rate, or bitrate."
---

This page describes the screen sharing preset `PreOptionScreen`. For the general preset structure (capture configuration + publish configuration), see [Camera presets](/en/meeting/android/presets/camera).

## PreOptionScreen

Purpose: Screen sharing track preset that combines screen recording capture parameters and video publish parameters.

### Structure

`PreOptionScreen(capture: ScreenCaptureOptions, publish: VideoPublishOptions)`

| Property | Type | Description |
| --- | --- | --- |
| capture | `ScreenCaptureOptions` | Screen capture configuration |
| publish | `VideoPublishOptions` | Screen video publish configuration |

### Capture configuration ScreenCaptureOptions

Purpose: Configures screen recording capture parameters.

| Property | Type | Description |
| --- | --- | --- |
| deviceId | `String` | Device ID. |
| width | `Int` | Capture width. |
| height | `Int` | Capture height. |
| maxFps | `Int` | Maximum capture frame rate. |
| maxBitrate | `Int` | Maximum capture bitrate. |

### Publish configuration VideoPublishOptions

Purpose: Same structure as the video publish parameters (for fields, see [Camera presets](/en/meeting/android/presets/camera)); the default `desc` is `TRACK_SHARE`.

### Built-in presets

Purpose: The SDK provides the default screen sharing preset `PreOptionScreen.def`.

```kotlin
capture: deviceId="screenCapDef", width=1920, height=1080, maxFps=10, maxBitrate=1024*1024
publish: desc="screen"(TRACK_SHARE), codec=H264, maxBitrate=1024*1024,
         width=1920, height=1080, maxFps=10, props=null, simulcasts=null
```
