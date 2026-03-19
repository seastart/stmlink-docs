---
title: "轨道预设配置总览"
description: "Android SRTC 音视频 SDK 轨道 options（摄像头、麦克风、屏幕共享、自定义视频流）说明"
---

本文档汇总 `cn.seastart.rtc.track.options` 目录下与轨道预设相关的核心类型，按摄像头、麦克风、屏幕共享、自定义视频流四条主线说明采集配置与推送配置，并补充 `PublishCustomOptions` 在发布阶段的自定义能力。

## 通用说明

作用说明：`PreOption*` 预设统一采用“采集配置 + 推送配置”结构。

- 采集配置：控制本地采集行为（分辨率、帧率、采样率、设备参数等）。
- 推送配置：控制发布行为（`desc`、`codec`、`maxBitrate`、联播参数等）。

## 摄像头：PreOptionCamera

作用说明：摄像头轨道预设，组合摄像头采集参数与视频推送参数。

### 结构定义

`PreOptionCamera(capture: CameraCaptureOptions, publish: VideoPublishOptions)`

### 属性说明

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

## 麦克风：PreOptionMic

作用说明：麦克风轨道预设，组合音频采集参数与音频推送参数。

### 结构定义

`PreOptionMic(capture: MicCaptureOptions, publish: AudioPublishOptions)`

### 属性说明

| 属性名称 | 数据类型 | 说明 |
| --- | --- | --- |
| capture | `MicCaptureOptions` | 麦克风采集配置 |
| publish | `AudioPublishOptions` | 麦克风音频推送配置 |

### 采集配置 MicCaptureOptions

作用说明：配置麦克风采集端参数。

| 属性名称 | 数据类型 | 说明 |
| --- | --- | --- |
| deviceId | `String` | 设备 ID。 |
| echoCancellation | `Boolean` | AEC 回声消除。 |
| noiseSuppression | `Boolean` | ANS 降噪。 |
| autoGainControl | `Boolean` | AGC 自动增益。 |
| channelCount | `Int` | 声道数（当前仅单声道）。 |
| sampleRate | `Int` | 采样率（常用 16000 / 48000）。 |
| sampleSize | `Int` | 位深（默认 16）。 |
| latency | `Double` | 延迟参数。 |

### 推送配置 AudioPublishOptions

作用说明：配置音频轨道发布参数。

| 属性名称 | 数据类型 | 说明 |
| --- | --- | --- |
| desc | `String` | 轨道描述（默认 `TRACK_AUDIO`）。 |
| codec | `CodecType` | 编码格式（默认 `OPUS`）。 |
| maxBitrate | `Int` | 最大码率。 |
| dtx | `Boolean` | 音频不连续传输。 |
| red | `Boolean` | 冗余音频数据。 |
| props | `Any?` | 自定义属性。 |

### 内置预设

作用说明：SDK 提供默认麦克风预设。

支持预设：`PreOptionMic.def`。

```kotlin
capture: deviceId="MicCapDef", echoCancellation=true, noiseSuppression=true, autoGainControl=true,
         channelCount=1, sampleRate=48000, sampleSize=16, latency=0.0
publish: desc="mic"(TRACK_AUDIO), codec=OPUS, maxBitrate=32*1024, dtx=true, red=true, props=null
```

## 屏幕共享：PreOptionScreen

作用说明：屏幕共享轨道预设，组合录屏采集参数与视频推送参数。

### 结构定义

`PreOptionScreen(capture: ScreenCaptureOptions, publish: VideoPublishOptions)`

### 属性说明

| 属性名称 | 数据类型 | 说明 |
| --- | --- | --- |
| capture | `ScreenCaptureOptions` | 屏幕采集配置 |
| publish | `VideoPublishOptions` | 屏幕视频推送配置 |

### 采集配置 ScreenCaptureOptions

作用说明：配置录屏采集端参数。

| 属性名称 | 数据类型 | 说明 |
| --- | --- | --- |
| deviceId | `String` | 设备 ID。 |
| width | `Int` | 采集宽度。 |
| height | `Int` | 采集高度。 |
| maxFps | `Int` | 最大采集帧率。 |
| maxBitrate | `Int` | 最大采集码率。 |

### 推送配置 VideoPublishOptions

作用说明：同视频发布参数结构，默认 `desc` 为 `TRACK_SHARE`。

### 内置预设

作用说明：SDK 提供默认屏幕共享预设。

支持预设：`PreOptionScreen.def`。

```kotlin
capture: deviceId="screenCapDef", width=1920, height=1080, maxFps=10, maxBitrate=1024*1024
publish: desc="screen"(TRACK_SHARE), codec=H264, maxBitrate=1024*1024,
         width=1920, height=1080, maxFps=10, props=null, simulcasts=null
```

## 自定义视频流：PreOptionCustomVideo

作用说明：自定义视频轨道预设，组合自定义采集参数与视频推送参数。

### 结构定义

`PreOptionCustomVideo(capture: CustomVideoCaptureOptions, publish: VideoPublishOptions)`

### 属性说明

| 属性名称 | 数据类型 | 说明 |
| --- | --- | --- |
| capture | `CustomVideoCaptureOptions` | 自定义视频采集侧参数。 |
| publish | `VideoPublishOptions` | 自定义视频推送参数。 |

### 采集配置 CustomVideoCaptureOptions

作用说明：配置自定义视频采集端参数。

| 属性名称 | 数据类型 | 说明 |
| --- | --- | --- |
| width | `Int` | 采集宽度。 |
| height | `Int` | 采集高度。 |
| maxFps | `Int` | 采集帧率。 |
| maxBitrate | `Int` | 采集码率。 |

### 推送配置 VideoPublishOptions

作用说明：同视频发布参数结构。

- 默认自定义视频预设使用 `desc = TRACK_CUSTOM`
- 屏幕场景预设使用 `desc = TRACK_SHARE`

### 内置预设

作用说明：SDK 提供两种自定义视频预设。

支持预设：`PreOptionCustomVideo.def`、`PreOptionCustomVideo.screen`。

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

## 发布自定义参数：PublishCustomOptions

作用说明：发布阶段覆盖预设中的推送参数，核心用于自定义轨道 `desc`。

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
