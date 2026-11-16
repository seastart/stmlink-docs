---
title: "AI 降噪（DeepFilterNet）"
description: "用 SRTCDeepFilterNet 插件给麦克风开启可调强度的 AI 降噪：集成、开关、强度调节、设备不支持与算力不足的处理，以及自定义采集处理器如何声明关闭自带降噪"
---

### 概述

`SRTCDeepFilterNet` 是基于 [DeepFilterNet3](https://github.com/Rikorose/DeepFilterNet) 的 AI 降噪插件，与 Web 的 [DeepFilterNet 降噪插件](/zh/rtc/web/advanced/deepfilternet) 使用同一份算法、模型和参数，各端听感一致。它实现了 SDK 的 `AudioProcessor` 接口，挂到 `SRTCEngine.audioCaptureProcessor` 上即生效，支持**运行时调整降噪强度**与**临时旁路**。

插件是 `srtc-swift-sdk` 包里的**可选产品**，自 `1.8.0` 起提供，iOS 与 macOS 都可用。不用 AI 降噪的 App 不需要引入它。

---

### 集成

在依赖 `SRTC` 的同一个 App target 上再加 `SRTCDeepFilterNet` 产品：

```swift
// Package.swift
dependencies: [
    .package(url: "https://github.com/seastart/srtc-swift-sdk.git", from: "1.8.0")
],
targets: [
    .target(
        name: "YourApp",
        dependencies: [
            .product(name: "SRTC", package: "srtc-swift-sdk"),
            .product(name: "SRTCDeepFilterNet", package: "srtc-swift-sdk")
        ]
    )
]
```

Xcode 工程在 `File > Add Package Dependencies...` 里勾选 `SRTCDeepFilterNet` 即可。模型已内置在插件里，不需要额外拷贝资源。

<Warning>
不要把 `SRTCDeepFilterNet` 加到屏幕共享的 Broadcast Upload Extension 上，它只用于 App 进程。
</Warning>

---

### 使用

```swift
import SRTC
import SRTCDeepFilterNet

final class CallViewController: UIViewController {
    let srtc = SRTCEngine()
    /// 必须由业务持有：SDK 对处理器是弱引用
    private var denoiser: DeepFilterNetProcessor?

    func enableDenoise() {
        // 1. 不支持的设备直接隐藏降噪开关
        guard DeepFilterNetProcessor.isSupported else { return }
        do {
            // 2. 创建插件，强度 0–100，默认 50
            let denoiser = try DeepFilterNetProcessor(suppressionLevel: 50)
            // 3. 运行中算力不足时插件自动暂停降噪，并在主线程回调
            denoiser.onOverload = { [weak self] in
                self?.showToast("设备性能不足，AI 降噪已暂停")
            }
            self.denoiser = denoiser
            // 4. 挂上即生效，入会前后都可以设置
            srtc.audioCaptureProcessor = denoiser
        } catch {
            // 设备不支持：SRTCError.featureNotSupported（032）
            print("AI 降噪开启失败：\(error)")
        }
    }

    func disableDenoise() {
        srtc.audioCaptureProcessor = nil   // 卸载，恢复 SDK 默认的音频处理
        denoiser = nil
    }
}
```

运行时调整强度或临时旁路，不需要重新挂载：

```swift
denoiser?.setSuppressionLevel(80)  // 0–100，越大压制越强
denoiser?.setEnabled(false)        // 旁路：音频原样通过，处理器仍挂着
denoiser?.setEnabled(true)         // 恢复降噪，同时清除算力不足导致的暂停
```

---

### 接口

| 接口 | 说明 |
| --- | --- |
| `static var isSupported: Bool` | 当前设备是否支持。开启前判断，不支持时直接隐藏降噪开关 |
| `init(suppressionLevel: Int = 50, modelURL: URL? = nil) throws` | 创建插件。`suppressionLevel` 为强度 0–100；`modelURL` 一般不传，使用内置模型。设备不支持时抛 `SRTCError.featureNotSupported`，找不到模型时抛 `SRTCError.invalidArgument` |
| `setSuppressionLevel(_:)` | 运行时调整强度 0–100 |
| `setEnabled(_:)` | 开关降噪。`false` 时音频原样通过；`true` 恢复降噪并清除算力不足导致的暂停 |
| `var suppressionLevel: Int` | 当前强度，只读 |
| `var isEnabled: Bool` | 当前开关状态，只读。算力不足自动暂停不会改变它 |
| `var onOverload: (() -> Void)?` | 运行中算力不足、降噪已自动暂停时回调，在主线程执行，每次暂停只回调一次 |

---

### 设备不支持与算力不足

AI 降噪需要一定的 CPU 算力，SDK 分两层处理：

+ **开启前**：`isSupported` 为 `false` 的设备不支持，构造函数会抛 `SRTCError.featureNotSupported`（错误码低位 `032`，iOS 为 `103032`、macOS 为 `105032`）。目前的苹果设备都支持，建议仍按跨端统一的写法先判断再开启。
+ **运行中**：设备持续过载（例如同时在跑其它重负载任务）时，插件会自动转入旁路、保证通话不卡顿，并回调 `onOverload`。建议提示用户「设备性能不足，降噪已暂停」，由用户决定是否调用 `setEnabled(true)` 重新开启。

---

### 注意事项

+ **业务必须持有插件实例**。`audioCaptureProcessor` 是弱引用，只写 `srtc.audioCaptureProcessor = try DeepFilterNetProcessor()` 的话，实例会被立即释放，降噪不生效。
+ **挂载时 SDK 会自动关闭 WebRTC 自带的软件降噪**，卸载后恢复，避免两道降噪叠加让人声发闷；回声消除、自动增益不受影响。
+ **系统的语音处理仍然生效**。iOS / macOS 通话时系统自带的回声消除与降噪无法单独关闭，AI 降噪叠加在它之上。正式上线前建议在目标设备上试听确认效果。
+ 模型在后台加载（通常不到 1 秒），加载完成前音频原样通过，不会卡住采集。
+ 只在 48kHz 采集下工作。蓝牙耳机通话模式等把采集降到 8kHz / 16kHz 时自动旁路，回到 48kHz 后恢复。
+ `audioCaptureProcessor` 全局只有一个，作用于所有频道。需要同时做变声等其它处理时，请在自己的处理器里串联调用。
+ 许可：DeepFilterNet 本体为 Apache-2.0/MIT；模型权重的授权请在分发前自行核实。

---

### 自定义处理器声明 3A 要求

自己实现的 `AudioProcessor` 若也需要关闭自带处理（例如接入其它降噪算法），可以额外遵循 `AudioProcessingDeclaring`，声明对 WebRTC 自带 3A 的要求。设为 `audioCaptureProcessor` 时 SDK 按声明调整，换掉或清空处理器时恢复：

```swift
final class MyDenoiser: NSObject, AudioProcessor, AudioProcessingDeclaring {
    // false 表示要求关闭；nil 表示不干预，沿用 SDK 默认配置
    let audioProcessing = AudioProcessingConstraints(noiseSuppression: false)

    func audioProcessingInitialize(sampleRate sampleRateHz: Int, channels: Int) {}
    func audioProcessingProcess(audioBuffer: AudioBuffer) { /* 原地处理 */ }
    func audioProcessingRelease() {}
}
```

`AudioProcessingConstraints` 与 Web SDK 的同名类型含义一致，字段见 [类型定义](/zh/rtc/swift/types#audioprocessingconstraints)。
