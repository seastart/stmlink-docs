---
title: "屏幕共享预设"
description: "Android SMeeting 会议 SDK 屏幕共享预设 PreOptionScreen"
---

本页说明屏幕共享预设 `PreOptionScreen`。预设通用结构（采集配置 + 推送配置）见 [摄像头预设](/zh/meeting/android/presets/camera)。

## PreOptionScreen

作用说明：屏幕共享轨道预设，组合录屏采集参数与视频推送参数。

### 结构定义

`PreOptionScreen(capture: ScreenCaptureOptions, publish: VideoPublishOptions)`

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

作用说明：同视频发布参数结构（字段见 [摄像头预设](/zh/meeting/android/presets/camera)），默认 `desc` 为 `TRACK_SHARE`。

### 内置预设

作用说明：SDK 提供默认屏幕共享预设 `PreOptionScreen.def`。

```kotlin
capture: deviceId="screenCapDef", width=1920, height=1080, maxFps=10, maxBitrate=1024*1024
publish: desc="screen"(TRACK_SHARE), codec=H264, maxBitrate=1024*1024,
         width=1920, height=1080, maxFps=10, props=null, simulcasts=null
```
