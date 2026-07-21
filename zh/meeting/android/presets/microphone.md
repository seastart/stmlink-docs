---
title: "麦克风预设"
description: "Android SMeeting 会议 SDK 麦克风预设 PreOptionMic"
---

本页说明麦克风预设 `PreOptionMic`。预设通用结构（采集配置 + 推送配置）见 [摄像头预设](/zh/meeting/android/presets/camera)。

## PreOptionMic

作用说明：麦克风轨道预设，组合音频采集参数与音频推送参数。

### 结构定义

`PreOptionMic(capture: MicCaptureOptions, publish: AudioPublishOptions)`

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

作用说明：SDK 提供默认麦克风预设 `PreOptionMic.def`。

```kotlin
capture: deviceId="MicCapDef", echoCancellation=true, noiseSuppression=true, autoGainControl=true,
         channelCount=1, sampleRate=48000, sampleSize=16, latency=0.0
publish: desc="mic"(TRACK_AUDIO), codec=OPUS, maxBitrate=32*1024, dtx=true, red=true, props=null
```
