---
title: "LocalMicTrack"
description: "共享麦克风采集轨道，支持脱离频道显式启停采集、读取音量、枚举和切换输入设备，并发布到一个或多个频道"
---

`LocalMicTrack` 由 `RTCEngine.getLocalMicTrack(...)` 创建。麦克风采集、频道加入和音频发布已经解耦：应用必须显式调用 `startCapture(...)` 打开共享麦克风，再通过 `RTCEngine` 或 `RTCChannel.publishLocalAudio(...)` 发布。

同一个 `LocalMicTrack` 可以发布到多个频道。取消某个频道的发布不会停止采集；`stopCapture()` 会关闭共享数据源并影响所有仍在使用该 Track 的频道。

## startCapture(listener)

```kotlin
fun startCapture(listener: RTCResultListener?)
```

打开麦克风采集。相同参数下重复调用保持幂等；成功后可读取音量、接收本地 PCM 回调或发布到频道。

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `listener` | `RTCResultListener?` | 启动结果，可为 `null`；失败码见 [错误码](/zh/rtc/android/error-codes)。 |

## stopCapture()

```kotlin
fun stopCapture()
```

关闭共享麦克风采集。未启动时调用保持幂等。

## getVolume()

```kotlin
fun getVolume(): Int
```

返回实时麦克风音量，单位为 dBFS，范围约为 `[-60, 0]`；未采集时返回实现的静音值。

## switchMicDevice(deviceId)

```kotlin
fun switchMicDevice(deviceId: String)
```

切换麦克风输入设备。`deviceId` 来自 `getMicDevices()`，只在本次设备连接期间有效；采集中切换会重建录音链路。

## getMicDevices()

```kotlin
fun getMicDevices(): List<MicDeviceCapability>
```

返回当前系统可用的麦克风输入设备能力列表。字段见 [类型定义](/zh/rtc/android/types)。Engine 上的 `getMicDevices()` 与 `switchMicDevice(...)` 是同一共享采集模块的便捷入口。

## 本地 PCM 回调

```kotlin
rtcEngine.setRtcLocalAudioFrameEvent(object : RTCLocalAudioFrameEvent {
    override fun onLocalAudioFrame(
        pcm: ByteArray?,
        sampleRate: Int,
        channelCount: Int,
        audioFormat: Int
    ) {
        // 不要在回调线程执行耗时 I/O
    }
})

val micTrack = rtcEngine.getLocalMicTrack(PreOptionMic.def)
micTrack.startCapture(listener)
```

仅注册帧监听器不会自动打开麦克风。完整参数见 [RTCLocalAudioFrameEvent](/zh/rtc/android/api-reference/RTCLocalAudioFrameEvent)。
