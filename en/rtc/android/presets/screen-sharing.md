---
title: "Screen sharing preset"
description: "Android screen sharing preset PreOptionScreen: capture options (ScreenCaptureOptions), publish options (VideoPublishOptions with TRACK_SHARE), and the default PreOptionScreen.def values. Read when configuring screen sharing resolution, frame rate, or bitrate."
---

This page describes the screen sharing preset `PreOptionScreen`. For the general preset structure (capture options + publish options), see [Camera preset](/en/rtc/android/presets/camera).

## PreOptionScreen

Purpose: The screen sharing track preset, combining screen capture parameters with video publish parameters.

### Structure

`PreOptionScreen(capture: ScreenCaptureOptions, publish: VideoPublishOptions)`

| Property | Data type | Description |
| --- | --- | --- |
| capture | `ScreenCaptureOptions` | Screen capture options |
| publish | `VideoPublishOptions` | Screen video publish options |

### Capture options ScreenCaptureOptions

Purpose: Configures screen capture parameters.

| Property | Data type | Description |
| --- | --- | --- |
| deviceId | `String` | Device ID. |
| width | `Int` | Capture width. |
| height | `Int` | Capture height. |
| maxFps | `Int` | Maximum capture frame rate. |
| maxBitrate | `Int` | Maximum capture bitrate. |

### Publish options VideoPublishOptions

Purpose: Same structure as the video publish parameters (for fields, see [Camera preset](/en/rtc/android/presets/camera)); the default `desc` is `TRACK_SHARE`.

### Built-in presets

Purpose: The SDK provides the default screen sharing preset `PreOptionScreen.def`.

```kotlin
capture: deviceId="screenCapDef", width=1920, height=1080, maxFps=15, maxBitrate=1024*1024
publish: desc="screen"(TRACK_SHARE), codec=H264, maxBitrate=1024*1024,
         width=1920, height=1080, maxFps=15, props=null, simulcasts=null
```
