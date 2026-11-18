---
title: "AI 降噪（DeepFilterNet）"
description: "在会议里给麦克风开启 AI 降噪：引入 cn.seastart.rtc:denoise 插件，用 MeetingEngine.setAudioCaptureProcessor 挂载，以及设备不支持、算力不足和自定义采集处理器的处理方式"
---

会议层通过 `MeetingEngine.setAudioCaptureProcessor` 挂载麦克风采集处理器，自 `2.0.43` 起提供。最常见的用法是挂 SRTC 的 AI 降噪插件 `cn.seastart.rtc:denoise`：它基于 DeepFilterNet3，与 Web、iOS 端使用同一份算法和模型，支持运行时调整降噪强度与临时旁路。

插件是独立的可选依赖，不用 AI 降噪的 App 不需要引入。插件自身的接口、强度、过载与设备判断的细节见 SRTC 文档 [AI 降噪（DeepFilterNet）](/zh/rtc/android/advanced/deepfilternet)，本页只讲会议层怎么接。

## 1. 添加依赖

```groovy
dependencies {
    implementation 'cn.seastart.meeting:meeting:2.0.43'
    implementation 'cn.seastart.rtc:denoise:0.1.0'
}
```

- Meeting `2.0.43` 传递依赖 RTC `2.0.39`，插件要求 RTC `2.0.39` 及以上，两者版本是配套的。
- 插件支持 `arm64-v8a` 和 `armeabi-v7a`，模型已内置，不需要额外拷贝资源。

## 2. 开启与关闭

```kotlin
import cn.seastart.rtc.denoise.DeepFilterNetProcessor
import cn.seastart.rtc.denoise.DenoiseNotSupportedException

private var denoiser: DeepFilterNetProcessor? = null

fun enableDenoise(context: Context, meetingEngine: MeetingEngine) {
    // 1. 不支持的设备直接隐藏降噪开关
    if (!DeepFilterNetProcessor.isSupported()) return
    try {
        // 2. 创建插件，强度 0–100，默认 50
        val processor = DeepFilterNetProcessor(context, suppressionLevel = 50)
        // 3. 运行中算力不足时插件自动暂停降噪，并在主线程回调
        processor.overloadListener = DeepFilterNetProcessor.OverloadListener {
            showToast("设备性能不足，AI 降噪已暂停")
        }
        // 4. 挂上即生效；initSdk 前后、入会前后都可以调用
        meetingEngine.setAudioCaptureProcessor(processor)
        denoiser = processor
    } catch (e: DenoiseNotSupportedException) {
        // 设备不支持：e.code == 102032
    }
}

fun disableDenoise(meetingEngine: MeetingEngine) {
    meetingEngine.setAudioCaptureProcessor(null)   // 卸载，恢复系统与 SDK 自带的降噪
    denoiser = null
}
```

运行时调整强度或临时旁路，直接调插件，不需要重新挂载：

```kotlin
denoiser?.setSuppressionLevel(80)  // 0–100，越大压制越强
denoiser?.setEnabled(false)        // 旁路：音频原样通过，处理器仍挂着
denoiser?.setEnabled(true)         // 恢复降噪，同时清除算力不足导致的暂停
```

## 3. 会议层的行为

- **设置会一直保留**：挂上后对之后的所有会议生效；`release()` 后再 `initSdk()`，SDK 会自动重新挂上，不需要业务重复设置。不再需要时传 `null`。
- **SDK 持有强引用**：替换或传 `null` 清除时，SDK 会调用旧处理器的 `release()`，旧实例之后不能再用；要重新开启就新建一个。
- **挂载时自动关闭系统与 WebRTC 自带的降噪**，卸载后恢复，避免两道降噪叠加让人声发闷；回声消除、自动增益不受影响。切换时麦克风采集会重建一次，声音有不到半秒的空档。只想临时关闭降噪时用插件的 `setEnabled(false)`，不会重建采集。
- 本端音量（说话人电平）反映的是降噪前的音量。

## 4. 设备不支持与算力不足

- **开启前**：只有低性能小核的设备（常见于部分电视、盒子和入门机型）不支持，`isSupported()` 返回 `false`，构造函数抛 `DenoiseNotSupportedException`（`102032`）。建议先判断再展示开关。
- **运行中**：设备持续过载时插件自动转入旁路、保证通话不卡顿，并回调 `overloadListener`。建议提示用户，由用户决定是否调用 `setEnabled(true)` 重新开启。

## 5. 自定义采集处理器

`setAudioCaptureProcessor` 接受任何实现 RTC `AudioCaptureProcessor` 接口的处理器，变声、自研降噪都可以挂，接口约定见 SRTC 文档 [自定义采集处理器](/zh/rtc/android/advanced/deepfilternet#6-自定义采集处理器)。同一时刻只能挂一个处理器。
