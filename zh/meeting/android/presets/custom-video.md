---
title: "自定义视频流预设"
description: "Android SMeeting 会议 SDK 自定义视频流预设 PreOptionCustomVideo 与 PublishCustomOptions"
---

本页说明自定义视频流预设 `PreOptionCustomVideo` 及发布阶段的自定义参数 `PublishCustomOptions`。会议场景中，云端录制的白板/共享数据采集（`getShareCustomVideoTrack`、`enableCourseRecordTrack`）会用到自定义视频轨。预设通用结构（采集配置 + 推送配置）见 [摄像头预设](/zh/meeting/android/presets/camera)。

## PreOptionCustomVideo

作用说明：自定义视频轨道预设，组合自定义采集参数与视频推送参数。

### 结构定义

`PreOptionCustomVideo(capture: CustomVideoCaptureOptions, publish: VideoPublishOptions)`

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

作用说明：同视频发布参数结构（字段见 [摄像头预设](/zh/meeting/android/presets/camera)）。

- 默认自定义视频预设使用 `desc = TRACK_CUSTOM`
- 屏幕场景预设使用 `desc = TRACK_SHARE`

### 内置预设

作用说明：SDK 提供两种自定义视频预设 `PreOptionCustomVideo.def`、`PreOptionCustomVideo.screen`。

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
