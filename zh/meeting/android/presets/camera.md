---
title: "摄像头预设"
description: "Android SMeeting 会议 SDK 摄像头预设 PreOptionCamera"
---

本页说明摄像头预设 `PreOptionCamera`，并统一定义各类预设通用的“采集配置 + 推送配置”结构。麦克风、屏幕共享、自定义视频流预设在推送参数上均复用本页的 `VideoPublishOptions`。

## 通用说明

作用说明：`PreOption*` 预设统一采用“采集配置 + 推送配置”结构。

- 采集配置：控制本地采集行为（分辨率、帧率、采样率、设备参数等）。
- 推送配置：控制发布行为（`desc`、`codec`、`maxBitrate`、联播参数等）。

会议场景下，摄像头预设通过 `openCamera` / `openCameraAndPublish` 传入，麦克风预设通过 `openMic` / `openMicAndPublish` 传入，屏幕共享预设通过 `initScreenShare` 传入。摄像头传 `null` 时首次使用默认预设，后续复用现有 Track 配置。

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
| deviceId | `String` | 建议设备 ID，默认空串表示不指定；启动时不可用会在同方向、再到全部设备中自动改选。 |
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
| maxBitrate | `Int` | 单路最大码率，单位 bps，发布前设置。 |
| minBitrate | `Int?` | 单路最小码率（bps），`null` 使用引擎默认下限；非空应满足 `0 <= minBitrate <= maxBitrate`。各路独立配置，发布前设置，目前仅 SFU 支持。 |
| width | `Int` | 推送宽度。 |
| height | `Int` | 推送高度。 |
| maxFps | `Int` | 最大推送帧率。 |
| props | `Any?` | 自定义属性。 |
| simulcasts | `MutableList<VideoPublishOptions>?` | 联播/辅流配置（当前摄像头场景可配置 1 路辅流）。 |

### 当前 RTC 版本的 minBitrate 限制

当前 RTC `2.0.33` 仍有此限制：`VideoPublishOptions.deepCopy()` 未复制 `minBitrate`，大小流经过复制后均会变为 `null`。Meeting 参数解析和 RTC 发布链路会使用深拷贝，因此下表中的最小码率是预设声明值，不能据此认定该版本已按此下限发布。此问题需 RTC 修复并发布后再验证；仅在应用侧设置该字段不能绕过后续深拷贝。

### 内置预设

作用说明：以下为 RTC `2.0.33` 的内置值，随 Meeting `2.0.37` 生效。采集与推送帧率统一为 15，是 RTC 有意调整；需要其它帧率时由应用显式传参。已采集时新预设不生效，需先关闭再打开。

支持以下预设：`_1080P`、`_720P`、`_480P`、`_180P`。

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
