---
title: "Custom video presets"
description: "The PreOptionCustomVideo custom video preset of the SMeeting Android SDK (def and screen), its capture and publish fields, and PublishCustomOptions for overriding desc, props, and simulcasts at publish time. Read this when publishing custom video tracks such as whiteboard or course recording."
---

This page describes the custom video preset `PreOptionCustomVideo` and the publish-time custom parameters `PublishCustomOptions`. In meetings, whiteboard/sharing data capture for cloud recording (`getShareCustomVideoTrack`, `enableCourseRecordTrack`) uses a custom video track. For the general preset structure (capture configuration + publish configuration), see [Camera presets](/en/meeting/android/presets/camera).

## PreOptionCustomVideo

Purpose: Custom video track preset that combines custom capture parameters and video publish parameters.

### Structure

`PreOptionCustomVideo(capture: CustomVideoCaptureOptions, publish: VideoPublishOptions)`

| Property | Type | Description |
| --- | --- | --- |
| capture | `CustomVideoCaptureOptions` | Custom video capture-side parameters. |
| publish | `VideoPublishOptions` | Custom video publish parameters. |

### Capture configuration CustomVideoCaptureOptions

Purpose: Configures custom video capture parameters.

| Property | Type | Description |
| --- | --- | --- |
| width | `Int` | Capture width. |
| height | `Int` | Capture height. |
| maxFps | `Int` | Capture frame rate. |
| maxBitrate | `Int` | Capture bitrate. |

### Publish configuration VideoPublishOptions

Purpose: Same structure as the video publish parameters (for fields, see [Camera presets](/en/meeting/android/presets/camera)).

- The default custom video preset uses `desc = TRACK_CUSTOM`
- The screen preset uses `desc = TRACK_SHARE`

### Built-in presets

Purpose: The SDK provides two custom video presets, `PreOptionCustomVideo.def` and `PreOptionCustomVideo.screen`.

```kotlin
// def
capture: width=1920, height=1080, maxFps=10, maxBitrate=1024*1024
publish: desc="custom"(TRACK_CUSTOM), codec=H264, maxBitrate=1024*1024,
         width=1920, height=1080, maxFps=10, props=null, simulcasts=null

// screen
capture: width=1920, height=1080, maxFps=10, maxBitrate=1024*1024
publish: desc="screen"(TRACK_SHARE), codec=H264, maxBitrate=1024*1024,
         width=1920, height=1080, maxFps=10, props=null, simulcasts=null
```

## Publish-time custom parameters: PublishCustomOptions

Purpose: Overrides the preset's publish parameters at publish time, mainly used to customize the track `desc`.

### Fields

| Property | Type | Description |
| --- | --- | --- |
| desc | `String?` | Custom track description; `null` means no change. |
| props | `Any?` | Custom additional properties; `null` means no change. |
| simulcasts | `MutableList<PublishCustomOptions>?` | Overrides the simulcast / low stream parameters; `null` means no change. |

### Recommendations

- If you only need to change the track description, just pass `desc`.
- For the camera's high and low streams (`TRACK_MAIN` / `TRACK_SUB`), you can override the low stream parameters separately through `simulcasts`.
- For the mic, screen sharing, and custom video, you usually only need the main track parameters and don't need `simulcasts`.
