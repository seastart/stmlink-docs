---
title: "摄像头预设"
description: "Android SMeeting 会议 SDK 摄像头预设 PreOptionCamera"
---

本页说明摄像头预设 `PreOptionCamera`，并统一定义各类预设通用的“采集配置 + 推送配置”结构。麦克风、屏幕共享、自定义视频流预设在推送参数上均复用本页的 `VideoPublishOptions`。

## 通用说明

作用说明：`PreOption*` 预设统一采用“采集配置 + 推送配置”结构。

- 采集配置：控制本地采集行为（分辨率、帧率、采样率、设备参数等）。
- 推送配置：控制发布行为（`desc`、`codec`、`maxBitrate`、联播参数等）。

会议场景下，摄像头、麦克风预设通过 `requestOpenCamera` / `requestOpenMic` 传入，屏幕共享预设通过 `initScreenShare` 传入。传 `null` 时使用 SDK 默认预设。

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

作用说明：配置视频轨道发布参数。麦克风以外的视频类预设均复用该结构。

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

作用说明：SDK 提供分辨率分档预设。

支持以下预设：`_1080P`、`_720P`、`_480P`、`_180P`。

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
