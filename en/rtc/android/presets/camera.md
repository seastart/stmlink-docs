---
title: "Camera preset"
description: "Android camera track preset PreOptionCamera: capture options (CameraCaptureOptions), publish options (VideoPublishOptions), the built-in 1080p/720p/480p/180p presets, and PublishCustomOptions for overriding publish parameters. Read when choosing or tuning camera resolution, frame rate, or bitrate."
---

This page describes the camera track preset `PreOptionCamera`, and `PublishCustomOptions`, which overrides the preset's publish parameters at publish time. For microphone and screen sharing presets, see [Microphone preset](/en/rtc/android/presets/microphone) and [Screen sharing preset](/en/rtc/android/presets/screen-sharing).

## General notes

All `PreOption*` presets share a "capture options + publish options" structure:

- Capture options: control local capture behavior (resolution, frame rate, sample rate, device parameters, and so on).
- Publish options: control publishing behavior (`desc`, `codec`, `maxBitrate`, simulcast parameters, and so on).

## PreOptionCamera

Purpose: The camera track preset, combining camera capture parameters with video publish parameters.

### Structure

`PreOptionCamera(capture: CameraCaptureOptions, publish: VideoPublishOptions)`

| Property | Data type | Description |
| --- | --- | --- |
| capture | `CameraCaptureOptions` | Camera capture options |
| publish | `VideoPublishOptions` | Camera video publish options |

### Capture options CameraCaptureOptions

Purpose: Configures camera capture parameters.

| Property | Data type | Description |
| --- | --- | --- |
| deviceId | `String` | The suggested camera device ID, taken from `CameraDeviceCapability.cameraId` returned by [`RTCEngine.getCameraDevices`](/en/rtc/android/api-reference/RTCEngine). An empty string means no device is specified and the SDK chooses one. |
| position | `CamraPosition` | Phone camera position: `FRONT` / `BACK` / `External`. |
| facingMode | `CameraFacingMode` | WebRTC facing mode: `USER` / `ENVIRONMENT` / `LEFT` / `RIGHT`. |
| width | `Int` | Capture width. |
| height | `Int` | Capture height. |
| maxFps | `Int` | Maximum capture frame rate. |

### Publish options VideoPublishOptions

Purpose: Configures video track publish parameters.

| Property | Data type | Description |
| --- | --- | --- |
| desc | `String` | Track description (the high stream usually uses `TRACK_MAIN`, the low stream usually uses `TRACK_SUB`). |
| codec | `CodecType` | Codec (usually `H264`). |
| maxBitrate | `Int` | Maximum bitrate in bps. |
| minBitrate | `Int?` | Minimum bitrate in bps. `null` uses the engine's default lower bound; when non-null, it must satisfy `0 <= minBitrate <= maxBitrate`. Currently supported only by the SFU engine. |
| width | `Int` | Publish width. |
| height | `Int` | Publish height. |
| maxFps | `Int` | Maximum publish frame rate. |
| props | `Any?` | Custom properties. |
| simulcasts | `MutableList<VideoPublishOptions>?` | Simulcast / low stream configuration (in the camera scenario, you can currently configure 1 low stream). |

### Built-in presets

Purpose: The SDK provides presets by resolution tier: `_1080P`, `_720P`, `_480P`, and `_180P` (default `_480P`).

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

## Custom publish parameters: PublishCustomOptions

Purpose: Overrides the preset's publish parameters at publish time in `publishLocalVideo` / `publishLocalAudio`, mainly to customize the track `desc`.

### Fields

| Property | Data type | Description |
| --- | --- | --- |
| desc | `String?` | Custom track description; `null` leaves it unchanged. |
| props | `Any?` | Custom additional properties; `null` leaves them unchanged. |
| simulcasts | `MutableList<PublishCustomOptions>?` | Overrides simulcast / low stream parameters; `null` leaves them unchanged. |

### Recommendations

- If you only need to change the track description, pass `desc`.
- For the camera's high / low streams, you can override the low stream parameters through `simulcasts`.
- Microphone, screen sharing, and custom video tracks usually need only the main track parameters, not `simulcasts`.
