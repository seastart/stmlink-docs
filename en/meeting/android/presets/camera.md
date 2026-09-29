---
title: "Camera presets"
description: "The PreOptionCamera camera preset of the SMeeting Android SDK, the capture + publish structure (CameraCaptureOptions, VideoPublishOptions) shared by all presets, the known minBitrate limitation, and built-in 1080P/720P/480P/180P values. Read this when choosing camera resolution and bitrate."
---

This page describes the camera preset `PreOptionCamera` and defines the "capture configuration + publish configuration" structure shared by all presets. The mic, screen sharing, and custom video presets all reuse this page's `VideoPublishOptions` for their publish parameters.

## General notes

Purpose: `PreOption*` presets all use a "capture configuration + publish configuration" structure.

- Capture configuration: controls local capture behavior (resolution, frame rate, sample rate, device parameters, etc.).
- Publish configuration: controls publish behavior (`desc`, `codec`, `maxBitrate`, simulcast parameters, etc.).

In meetings, the camera preset is passed through `openCamera` / `openCameraAndPublish`, the mic preset through `openMic` / `openMicAndPublish`, and the screen sharing preset through `initScreenShare`. When `null` is passed for the camera, the default preset is used the first time, and the existing Track configuration is reused after that.

## PreOptionCamera

Purpose: Camera track preset that combines camera capture parameters and video publish parameters.

### Structure

`PreOptionCamera(capture: CameraCaptureOptions, publish: VideoPublishOptions)`

| Property | Type | Description |
| --- | --- | --- |
| capture | `CameraCaptureOptions` | Camera capture configuration |
| publish | `VideoPublishOptions` | Camera video publish configuration |

### Capture configuration CameraCaptureOptions

Purpose: Configures camera capture parameters.

| Property | Type | Description |
| --- | --- | --- |
| deviceId | `String` | Suggested device ID; the default empty string means none is specified. If it's unavailable at startup, the SDK automatically picks another device with the same facing first, then from all devices. |
| position | `CamraPosition` | Phone camera position: `FRONT` / `BACK` / `External`. |
| facingMode | `CameraFacingMode` | WebRTC facing: `USER` / `ENVIRONMENT` / `LEFT` / `RIGHT`. |
| width | `Int` | Capture width. |
| height | `Int` | Capture height. |
| maxFps | `Int` | Maximum capture frame rate. |

### Publish configuration VideoPublishOptions

Purpose: Configures video track publish parameters. All video presets other than the mic reuse this structure.

| Property | Type | Description |
| --- | --- | --- |
| desc | `String` | Track description (the high stream usually uses `TRACK_MAIN`, the low stream usually uses `TRACK_SUB`). |
| codec | `CodecType` | Codec (usually `H264`). |
| maxBitrate | `Int` | Maximum bitrate per stream in bps; set before publishing. |
| minBitrate | `Int?` | Minimum bitrate per stream (bps); `null` uses the engine's default lower bound. A non-null value should satisfy `0 <= minBitrate <= maxBitrate`. Each stream is configured independently and set before publishing; currently only supported by the SFU. |
| width | `Int` | Publish width. |
| height | `Int` | Publish height. |
| maxFps | `Int` | Maximum publish frame rate. |
| props | `Any?` | Custom properties. |
| simulcasts | `MutableList<VideoPublishOptions>?` | Simulcast / low stream configuration (currently one low stream can be configured for the camera). |

### Known minBitrate limitation

RTC `2.0.33` to `2.0.35` still have this limitation: `VideoPublishOptions.deepCopy()` doesn't copy `minBitrate`, so after copying, `minBitrate` becomes `null` for both the high and low streams. Meeting's parameter parsing and the RTC publish pipeline use deep copies, so the minimum bitrates in the table below are the values declared by the presets—you can't conclude from them that these versions actually publish with these lower bounds. This issue needs to be fixed and released in RTC before it can be verified; setting the field only on the app side can't get around the later deep copy.

### Built-in presets

Purpose: The following built-in values take effect from RTC `2.0.33` (introduced with Meeting `2.0.37`). Capture and publish frame rates are uniformly 15, an intentional adjustment in RTC; if you need another frame rate, pass it explicitly from your app. A new preset doesn't take effect while capture is already running; close and reopen the camera first.

The following presets are supported: `_1080P`, `_720P`, `_480P`, `_180P`.

```kotlin
// _1080P
capture: deviceId="", position=FRONT, facingMode=USER, width=1920, height=1080, maxFps=15
publish(main): desc="camera_big"(TRACK_MAIN), codec=H264, maxBitrate=5000*1024, minBitrate=2500*1024, width=1920, height=1080, maxFps=15
publish(sub):  desc="camera_small"(TRACK_SUB), codec=H264, maxBitrate=160*1024, minBitrate=80*1024, width=320, height=180, maxFps=15

// _720P
capture: deviceId="", position=FRONT, facingMode=USER, width=1280, height=720, maxFps=15
publish(main): desc="camera_big"(TRACK_MAIN), codec=H264, maxBitrate=2400*1024, minBitrate=1500*1024, width=1280, height=720, maxFps=15
publish(sub):  desc="camera_small"(TRACK_SUB), codec=H264, maxBitrate=160*1024, minBitrate=80*1024, width=320, height=180, maxFps=15

// _480P
capture: deviceId="", position=FRONT, facingMode=USER, width=640, height=480, maxFps=15
publish(main): desc="camera_big"(TRACK_MAIN), codec=H264, maxBitrate=800*1024, minBitrate=400*1024, width=640, height=480, maxFps=15
publish(sub):  desc="camera_small"(TRACK_SUB), codec=H264, maxBitrate=160*1024, minBitrate=80*1024, width=320, height=180, maxFps=15

// _180P
capture: deviceId="", position=FRONT, facingMode=USER, width=320, height=180, maxFps=15
publish(main): desc="camera_big"(TRACK_MAIN), codec=H264, maxBitrate=160*1024, minBitrate=80*1024, width=320, height=180, maxFps=15
publish(sub):  desc="camera_small"(TRACK_SUB), codec=H264, maxBitrate=160*1024, minBitrate=80*1024, width=320, height=180, maxFps=15
```
