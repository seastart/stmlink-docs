---
title: "RTCLocalAudioFrameEvent"
description: "获取共享麦克风采集产生的本地 PCM 帧，用于本地录制、落盘或应用层音频处理"
---

通过 `RTCEngine.setRtcLocalAudioFrameEvent(...)` 注册本地 PCM 回调，传 `null` 解绑。该回调属于 Engine 共享采集层，不携带频道 ID，SDK 内部推流也不依赖此监听器。

## onLocalAudioFrame(pcm, sampleRate, channelCount, audioFormat)

```kotlin
fun onLocalAudioFrame(
    pcm: ByteArray?,
    sampleRate: Int,
    channelCount: Int,
    audioFormat: Int
)
```

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `pcm` | `ByteArray?` | SDK 为应用单独复制的 PCM 数据，通常为 16-bit 小端。 |
| `sampleRate` | `Int` | 采样率，单位 Hz，例如 `48000`。 |
| `channelCount` | `Int` | 声道数，`1` 为单声道，`2` 为立体声。 |
| `audioFormat` | `Int` | 与 `android.media.AudioFormat.ENCODING_*` 一致的采样格式。 |

:::warning
注册监听器本身不会打开麦克风。必须调用 `LocalMicTrack.startCapture(...)`，成功后才会产生 PCM 回调；调用 `stopCapture()` 后停止。应用不应在回调线程执行耗时 I/O，可复制或投递数据后异步处理。
:::

```kotlin
rtcEngine.setRtcLocalAudioFrameEvent(object : RTCLocalAudioFrameEvent {
    override fun onLocalAudioFrame(
        pcm: ByteArray?,
        sampleRate: Int,
        channelCount: Int,
        audioFormat: Int
    ) {
        // 投递到应用自己的工作线程
    }
})

val micTrack = rtcEngine.getLocalMicTrack(PreOptionMic.def)
micTrack.startCapture(null)
```
