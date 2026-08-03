---
title: "自定义视频流预设"
description: "Android SRTC 音视频 SDK 自定义视频流预设 PreOptionCustomVideo"
---

本页说明自定义视频流预设 `PreOptionCustomVideo`，用于 [`RTCEngine.getLocalCustomVideoTrack`](/zh/rtc/android/api-reference/RTCEngine) 获取的 [`LocalCustomVideoTrack`](/zh/rtc/android/api-reference/LocalCustomVideoTrack)（向已发布轨道推送外部原始 YUV 帧）。预设通用结构（采集配置 + 推送配置）与发布阶段的 `PublishCustomOptions` 见 [摄像头预设](/zh/rtc/android/presets/camera)。

## PreOptionCustomVideo

作用说明：自定义视频轨道预设，组合自定义采集参数与视频推送参数。

### 结构定义

`PreOptionCustomVideo(capture: CustomVideoCaptureOptions, publish: VideoPublishOptions)`

| 属性名称 | 数据类型 | 说明 |
| --- | --- | --- |
| capture | `CustomVideoCaptureOptions` | 自定义视频采集侧参数。 |
| publish | `VideoPublishOptions` | 自定义视频推送参数。 |

### 采集配置 CustomVideoCaptureOptions

作用说明：声明外部帧源的规格，供 SDK 建立发布轨道时参考。SDK 本身不采集自定义视频，实际帧由业务侧通过 `LocalCustomVideoTrack.inputData` 送入。

| 属性名称 | 数据类型 | 说明 |
| --- | --- | --- |
| width | `Int` | 采集宽度。 |
| height | `Int` | 采集高度。 |
| maxFps | `Int` | 采集帧率。 |
| maxBitrate | `Int` | 采集码率。 |

### 推送配置 VideoPublishOptions

作用说明：同视频发布参数结构（字段见 [摄像头预设](/zh/rtc/android/presets/camera)）。

- 默认自定义视频预设使用 `desc = TRACK_CUSTOM`（`"custom"`）
- 屏幕场景预设使用 `desc = TRACK_SHARE`（`"screen"`）
- 自定义视频不使用联播，`simulcasts` 固定为 `null`

### 内置预设

作用说明：SDK 提供两种自定义视频预设 `PreOptionCustomVideo.def`、`PreOptionCustomVideo.screen`。

```kotlin
// def —— 默认自定义流，轨道描述 custom
capture: width=1920, height=1080, maxFps=10, maxBitrate=1024*1024
publish: desc="custom"(TRACK_CUSTOM), codec=H264, maxBitrate=1024*1024,
         width=1920, height=1080, maxFps=10, props=null, simulcasts=null

// screen —— 以屏幕共享轨道描述发布外部画面
capture: width=1920, height=1080, maxFps=10, maxBitrate=1024*1024
publish: desc="screen"(TRACK_SHARE), codec=H264, maxBitrate=1024*1024,
         width=1920, height=1080, maxFps=10, props=null, simulcasts=null
```

### 使用建议

- 送帧分辨率与 `publish.width` / `publish.height` 保持一致，避免额外缩放开销；帧率不要超过 `maxFps`。
- 需要以“共享”身份出现在远端时用 `PreOptionCustomVideo.screen`，或在 `publishLocalVideo` 时通过 `PublishCustomOptions(desc = TrackDesc.TRACK_SHARE.value)` 覆盖 `desc`。
- 轨道实例在 SDK 内按单例缓存，重复获取会用新的 `preOpt` 覆盖旧值，切换预设后需重新发布。
- 完整推流流程见 [自定义推流](/zh/rtc/android/advanced/custom-track)。
