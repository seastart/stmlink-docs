---
title: "AI 降噪（DeepFilterNet）"
description: "用可选插件 cn.seastart.rtc:denoise 给麦克风开启可调强度的 AI 降噪：依赖引入、开关与强度调节、设备不支持与算力不足的处理，以及自定义采集处理器 AudioCaptureProcessor 的用法"
---

`cn.seastart.rtc:denoise` 是基于 [DeepFilterNet3](https://github.com/Rikorose/DeepFilterNet) 的 AI 降噪插件，与 Web 的 [DeepFilterNet 降噪插件](/zh/rtc/web/advanced/deepfilternet) 使用同一份算法、模型和参数，各端听感一致。它实现了 SDK 的 `AudioCaptureProcessor` 接口，通过 `RTCEngine.setAudioCaptureProcessor` 挂载即生效，支持**运行时调整降噪强度**与**临时旁路**。

插件是独立的可选依赖，自 RTC `2.0.39` 起提供。不用 AI 降噪的 App 不需要引入它。

## 1. 添加依赖

```groovy
dependencies {
    implementation 'cn.seastart.rtc:rtc:2.0.39'
    implementation 'cn.seastart.rtc:denoise:0.1.0'
}
```

- 插件会传递依赖 `cn.seastart.rtc:rtc`，要求 RTC `2.0.39` 及以上。
- 插件支持 `arm64-v8a` 和 `armeabi-v7a`，与 SDK 一致。
- 模型已内置在插件里，不需要额外拷贝资源。

## 2. 开启与关闭

```kotlin
import cn.seastart.rtc.denoise.DeepFilterNetProcessor
import cn.seastart.rtc.denoise.DenoiseNotSupportedException

private var denoiser: DeepFilterNetProcessor? = null

fun enableDenoise(context: Context, rtcEngine: RTCEngine) {
    // 1. 不支持的设备直接隐藏降噪开关
    if (!DeepFilterNetProcessor.isSupported()) return
    try {
        // 2. 创建插件，强度 0–100，默认 50
        val processor = DeepFilterNetProcessor(context, suppressionLevel = 50)
        // 3. 运行中算力不足时插件自动暂停降噪，并在主线程回调
        processor.overloadListener = DeepFilterNetProcessor.OverloadListener {
            showToast("设备性能不足，AI 降噪已暂停")
        }
        // 4. 挂上即生效，入会前后都可以调用；Engine 级生效，作用于所有频道
        rtcEngine.setAudioCaptureProcessor(processor)
        denoiser = processor
    } catch (e: DenoiseNotSupportedException) {
        // 设备不支持：e.code == RtcErrorCode.FEATURE_NOT_SUPPORTED（102032）
    }
}

fun disableDenoise(rtcEngine: RTCEngine) {
    rtcEngine.setAudioCaptureProcessor(null)   // 卸载，恢复系统与 SDK 自带的降噪
    denoiser = null
}
```

运行时调整强度或临时旁路，不需要重新挂载：

```kotlin
denoiser?.setSuppressionLevel(80)  // 0–100，越大压制越强
denoiser?.setEnabled(false)        // 旁路：音频原样通过，处理器仍挂着
denoiser?.setEnabled(true)         // 恢复降噪，同时清除算力不足导致的暂停
```

## 3. 接口

| 接口 | 说明 |
| --- | --- |
| `DeepFilterNetProcessor.isSupported(): Boolean` | 静态方法，当前设备是否支持。开启前判断，不支持时直接隐藏降噪开关 |
| `DeepFilterNetProcessor(context, suppressionLevel = 50)` | 创建插件，`suppressionLevel` 为强度 0–100。设备不支持时抛 `DenoiseNotSupportedException` |
| `setSuppressionLevel(value: Int)` | 运行时调整强度 0–100 |
| `setEnabled(value: Boolean)` | 开关降噪。`false` 时音频原样通过；`true` 恢复降噪并清除算力不足导致的暂停 |
| `suppressionLevel: Int` | 当前强度，只读 |
| `isEnabled: Boolean` | 当前开关状态，只读。算力不足自动暂停不会改变它 |
| `overloadListener: OverloadListener?` | 运行中算力不足、降噪已自动暂停时回调，在主线程执行，每次暂停只回调一次 |
| `DenoiseNotSupportedException.code` | 固定为 `RtcErrorCode.FEATURE_NOT_SUPPORTED`（`102032`） |

## 4. 设备不支持与算力不足

AI 降噪需要一定的 CPU 算力，SDK 分两层处理：

- **开启前**：只有低性能小核的设备（常见于部分电视、盒子和入门机型）不支持，`isSupported()` 返回 `false`，构造函数抛 `DenoiseNotSupportedException`（`102032`）。建议先判断再展示开关，而不是让用户点了才报错。
- **运行中**：设备持续过载（例如同时在跑其它重负载任务）时，插件会自动转入旁路、保证通话不卡顿，并回调 `overloadListener`。建议提示用户「设备性能不足，降噪已暂停」，由用户决定是否调用 `setEnabled(true)` 重新开启。

## 5. 注意事项

- **挂载时 SDK 会自动关闭系统与 WebRTC 自带的降噪**，卸载后恢复，避免两道降噪叠加让人声发闷；回声消除、自动增益不受影响。这次切换会让麦克风采集重建一次，声音有不到半秒的空档。只想临时关闭降噪时用 `setEnabled(false)`，不会重建采集。
- 模型在后台加载（通常不到 1 秒），加载完成前音频原样通过，不会卡住采集。
- 只在 48kHz 单声道采集下工作，其它采集格式原样通过。
- 本端音量（`getVolume`、说话人电平）反映的是降噪前的音量。
- `setAudioCaptureProcessor` 全局只有一个处理器，作用于所有频道；`releaseSDK()` 不会清除它。
- 许可：DeepFilterNet 本体为 Apache-2.0/MIT；模型权重的授权请在分发前自行核实。

## 6. 自定义采集处理器

插件实现的 `AudioCaptureProcessor` 接口也可以用来接入自己的音频算法（降噪、变声等）。处理器在 SDK 采集线程上原地处理每一帧 PCM，处理后的数据再分发给所有频道，本地音频帧回调拿到的也是处理后的数据。

```kotlin
class MyProcessor : AudioCaptureProcessor {
    // 可选：要求关闭自带降噪；返回 null 表示不干预
    override val audioProcessing = AudioProcessingConstraints(noiseSuppression = false)

    override fun initialize(sampleRate: Int, channelCount: Int) {
        // 采集格式确定时调用（含设备切换、路由变化后的重建），须快速返回
    }

    override fun process(data: ByteArray, offset: Int, length: Int) {
        // 原地处理 data[offset, offset + length)：16bit 小端 PCM，默认 48kHz 单声道 10ms（960 字节）
        // 每 10ms 调用一次，须在几毫秒内返回；返回后缓冲会被复用，不要持有 data
    }

    override fun release() {
        // 处理器被替换或清空时调用，之后不会再收到 process
    }
}

rtcEngine.setAudioCaptureProcessor(MyProcessor())
```

- `process` 抛出的异常会被 SDK 捕获并记录，该帧按原样发送。
- `AudioProcessingConstraints` 与 Web、Swift SDK 的同名类型含义一致；Android 目前只处理 `noiseSuppression`，`echoCancellation`、`autoGainControl` 保持 SDK 默认。
- 接口细节见 [RTCEngine.setAudioCaptureProcessor](/zh/rtc/android/api-reference/RTCEngine#setaudiocaptureprocessor-processor) 与 [类型定义](/zh/rtc/android/types#audiocaptureprocessor)。
