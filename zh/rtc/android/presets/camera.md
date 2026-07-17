---
title: "摄像头预设"
description: "Android SRTC 音视频 SDK 摄像头轨道预设 PreOptionCamera 与发布自定义参数 PublishCustomOptions"
---

本页说明摄像头轨道预设 `PreOptionCamera`，以及在发布阶段覆盖预设推送参数的 `PublishCustomOptions`。麦克风、屏幕共享预设分别见 [麦克风预设](/zh/rtc/android/presets/microphone)、[屏幕共享预设](/zh/rtc/android/presets/screen-sharing)。

## 通用说明

`PreOption*` 预设统一采用“采集配置 + 推送配置”结构：

- 采集配置：控制本地采集行为（分辨率、帧率、采样率、设备参数等）。
- 推送配置：控制发布行为（`desc`、`codec`、`maxBitrate`、联播参数等）。

## PreOptionCamera

作用说明：摄像头轨道预设，组合摄像头采集参数与视频推送参数。

### 结构定义

`PreOptionCamera(capture: CameraCaptureOptions, publish: VideoPublishOptions)`

| 属性名称 | 数据类型 | 说明 |
| --- | --- | --- |
| capture | `CameraCaptureOptions` | 摄像头采集配置 |
| publish | `VideoPublishOptions` | 摄像头视频推送配置 |

### 采集配置 CameraCaptureOptions

作用说明：配置摄像头采集端参数。

| 属性名称 | 数据类型 | 说明 |
| --- | --- | --- |
| deviceId | `String` | 设备 ID。 |
| position | `CamraPosition` | 手机摄像头位置：`FRONT` / `BACK` / `External`。 |
| facingMode | `CameraFacingMode` | WebRTC 朝向：`USER` / `ENVIRONMENT` / `LEFT` / `RIGHT`。 |
| width | `Int` | 采集宽度。 |
| height | `Int` | 采集高度。 |
| maxFps | `Int` | 最大采集帧率。 |

### 推送配置 VideoPublishOptions

作用说明：配置视频轨道发布参数。

| 属性名称 | 数据类型 | 说明 |
| --- | --- | --- |
| desc | `String` | 轨道描述（主流常用 `TRACK_MAIN`，辅流常用 `TRACK_SUB`）。 |
| codec | `CodecType` | 编码格式（常用 `H264`）。 |
| maxBitrate | `Int` | 最大码率。 |
| width | `Int` | 推送宽度。 |
| height | `Int` | 推送高度。 |
| maxFps | `Int` | 最大推送帧率。 |
| props | `Any?` | 自定义属性。 |
| simulcasts | `MutableList<VideoPublishOptions>?` | 联播/辅流配置（当前摄像头场景可配置 1 路辅流）。 |

### 内置预设

作用说明：SDK 提供分辨率分档预设。支持 `_1080P`、`_720P`、`_480P`、`_180P`（默认 `_480P`）。

```kotlin
// _1080P
capture: deviceId="cameraCapMain", position=FRONT, facingMode=USER, width=1920, height=1080, maxFps=30
publish(main): desc="camera_big"(TRACK_MAIN), codec=H264, maxBitrate=2000*1024, width=1920, height=1080, maxFps=25
publish(sub):  desc="camera_small"(TRACK_SUB), codec=H264, maxBitrate=128*1024, width=320, height=180, maxFps=25

// _720P
capture: deviceId="cameraCapMain", position=FRONT, facingMode=USER, width=1280, height=720, maxFps=30
publish(main): desc="camera_big"(TRACK_MAIN), codec=H264, maxBitrate=900*1024, width=1280, height=720, maxFps=25
publish(sub):  desc="camera_small"(TRACK_SUB), codec=H264, maxBitrate=128*1024, width=320, height=180, maxFps=25

// _480P
capture: deviceId="cameraCapMain", position=FRONT, facingMode=USER, width=640, height=480, maxFps=30
publish(main): desc="camera_big"(TRACK_MAIN), codec=H264, maxBitrate=512*1024, width=640, height=480, maxFps=25
publish(sub):  desc="camera_small"(TRACK_SUB), codec=H264, maxBitrate=128*1024, width=320, height=180, maxFps=25

// _180P
capture: deviceId="cameraCapMain", position=FRONT, facingMode=USER, width=320, height=180, maxFps=30
publish(main): desc="camera_big"(TRACK_MAIN), codec=H264, maxBitrate=128*1024, width=320, height=180, maxFps=25
publish(sub):  desc="camera_small"(TRACK_SUB), codec=H264, maxBitrate=128*1024, width=320, height=180, maxFps=25
```

## 发布自定义参数：PublishCustomOptions

作用说明：在 `publishLocalVideo` / `publishLocalAudio` 发布阶段覆盖预设中的推送参数，核心用于自定义轨道 `desc`。

### 字段说明

| 属性名称 | 数据类型 | 说明 |
| --- | --- | --- |
| desc | `String?` | 自定义轨道描述；`null` 表示不修改。 |
| props | `Any?` | 自定义附加属性；`null` 表示不修改。 |
| simulcasts | `MutableList<PublishCustomOptions>?` | 对联播/辅流参数进行覆盖；`null` 表示不修改。 |

### 使用建议

- 若只需改轨道描述，传入 `desc` 即可。
- 对摄像头主/辅流可分别通过 `simulcasts` 覆盖辅流参数。
- 对麦克风、屏幕共享、自定义视频流，通常只需主轨参数，不需要 `simulcasts`。
