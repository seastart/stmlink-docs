---
title: "MeetingLocalAudioFrameEvent"
description: "接收本地麦克风 PCM 帧及其采样率、声道数和音频格式"
---

`MeetingLocalAudioFrameEvent` 接收显式订阅的本地 PCM 帧，通过 `MeetingEngine.localAudioFrameEvent` 注册。可继承 `MeetingLocalAudioFrameSimpleEvent` 按需覆写。

## 使用说明

+ 该事件跟随 Engine 的本地麦克风采集链路，不要求已经加入会议；赋 `null` 即停止向应用转发帧。
+ 回调保持 SRTC 音频采集线程，不得执行耗时操作。只有 ADM 正在录音时才会持续回调。

## 接口方法

### onLocalAudioFrame(pcm, sampleRate, channelCount, audioFormat)

```kotlin
fun onLocalAudioFrame(
    pcm: ByteArray?,
    sampleRate: Int,
    channelCount: Int,
    audioFormat: Int
)
```

方法说明：返回一帧本地 PCM 音频数据及采样参数。

参数说明：

| 参数 | 说明 |
| --- | --- |
| `pcm` | 可空 PCM 帧数据。 |
| `sampleRate` | 采样率，单位 Hz。 |
| `channelCount` | 声道数。 |
| `audioFormat` | SRTC 定义的音频样本格式值。 |

返回值说明：无（`Unit`）。
