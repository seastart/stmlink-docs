---
title: "Custom video preset"
description: "Android custom video preset PreOptionCustomVideo for LocalCustomVideoTrack: capture options that describe the external frame source, publish options, and the built-in def (TRACK_CUSTOM) and screen (TRACK_SHARE) presets. Read when publishing external YUV frames on Android."
---

This page describes the custom video preset `PreOptionCustomVideo`, used by the [`LocalCustomVideoTrack`](/en/rtc/android/api-reference/LocalCustomVideoTrack) obtained from [`RTCEngine.getLocalCustomVideoTrack`](/en/rtc/android/api-reference/RTCEngine) (which pushes external raw YUV frames into a published track). For the general preset structure (capture options + publish options) and `PublishCustomOptions` used at publish time, see [Camera preset](/en/rtc/android/presets/camera).

## PreOptionCustomVideo

Purpose: The custom video track preset, combining custom capture parameters with video publish parameters.

### Structure

`PreOptionCustomVideo(capture: CustomVideoCaptureOptions, publish: VideoPublishOptions)`

| Property | Data type | Description |
| --- | --- | --- |
| capture | `CustomVideoCaptureOptions` | Custom video capture-side parameters. |
| publish | `VideoPublishOptions` | Custom video publish parameters. |

### Capture options CustomVideoCaptureOptions

Purpose: Declares the specifications of the external frame source, which the SDK uses as a reference when creating the published track. The SDK doesn't capture custom video itself; your app feeds the actual frames through `LocalCustomVideoTrack.inputData`.

| Property | Data type | Description |
| --- | --- | --- |
| width | `Int` | Capture width. |
| height | `Int` | Capture height. |
| maxFps | `Int` | Capture frame rate. |
| maxBitrate | `Int` | Capture bitrate. |

### Publish options VideoPublishOptions

Purpose: Same structure as the video publish parameters (for fields, see [Camera preset](/en/rtc/android/presets/camera)).

- The default custom video preset uses `desc = TRACK_CUSTOM` (`"custom"`)
- The screen scenario preset uses `desc = TRACK_SHARE` (`"screen"`)
- Custom video doesn't use simulcast; `simulcasts` is always `null`

### Built-in presets

Purpose: The SDK provides two custom video presets, `PreOptionCustomVideo.def` and `PreOptionCustomVideo.screen`.

```kotlin
// def — default custom stream, track description custom
capture: width=1920, height=1080, maxFps=10, maxBitrate=1024*1024
publish: desc="custom"(TRACK_CUSTOM), codec=H264, maxBitrate=1024*1024,
         width=1920, height=1080, maxFps=10, props=null, simulcasts=null

// screen — publishes external video with the screen sharing track description
capture: width=1920, height=1080, maxFps=10, maxBitrate=1024*1024
publish: desc="screen"(TRACK_SHARE), codec=H264, maxBitrate=1024*1024,
         width=1920, height=1080, maxFps=10, props=null, simulcasts=null
```

### Recommendations

- Keep the frame resolution you push consistent with `publish.width` / `publish.height` to avoid extra scaling overhead; don't exceed `maxFps`.
- To appear as "sharing" to remote users, use `PreOptionCustomVideo.screen`, or override `desc` with `PublishCustomOptions(desc = TrackDesc.TRACK_SHARE.value)` in `publishLocalVideo`.
- The SDK caches the track instance as a singleton; getting it again overwrites the old `preOpt` with the new one, so republish after switching presets.
- For the full publishing flow, see [Custom tracks](/en/rtc/android/advanced/custom-track).
