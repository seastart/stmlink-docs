---
title: "AI 降噪（DeepFilterNet）"
description: "在会议里给麦克风开启 AI 降噪：加 srtc-swift-sdk 的 SRTCDeepFilterNet 产品，赋给 SMeetingEngine.audioCaptureProcessor，以及处理器的持有、设备不支持、算力不足和自定义采集处理器"
---

### 概述

会议层通过 `SMeetingEngine.audioCaptureProcessor` 挂载麦克风采集处理器，自 `1.9.0` 起提供。最常见的用法是挂 SRTC 的 AI 降噪插件 `SRTCDeepFilterNet`：它基于 DeepFilterNet3，与 Web、Android 端使用同一份算法和模型，支持运行时调整降噪强度与临时旁路。

插件是独立的可选产品，不用 AI 降噪的 App 不需要引入。插件自身的接口、强度、过载与设备判断的细节见 SRTC 文档 [AI 降噪（DeepFilterNet）](/zh/rtc/swift/advanced/deepfilternet)，本页只讲会议层怎么接。

---

### 集成

插件在 `srtc-swift-sdk` 分发仓里，需要在工程里再声明一条 `srtc-swift-sdk` 依赖，版本用 `exact:` 锁到与 SMeeting 配套的 SRTC 版本（SMeeting 1.11.0 配 SRTC `1.10.0`），并把 `SRTCDeepFilterNet` 挂到 App target：

```swift
dependencies: [
    .package(url: "https://github.com/seastart/smeeting-swift-sdk.git", from: "1.14.0"),
    .package(url: "https://github.com/seastart/srtc-swift-sdk.git", exact: "1.10.0"),
],
targets: [
    .target(
        name: "YourApp",
        dependencies: [
            .product(name: "SMeeting", package: "smeeting-swift-sdk"),
            .product(name: "SRTCDeepFilterNet", package: "srtc-swift-sdk"),
        ]
    ),
]
```

Xcode 工程同理：在 Package Dependencies 里加 `srtc-swift-sdk`，规则选 Exact Version `1.10.0`，只给 App target 勾选 `SRTCDeepFilterNet`。

<Warning>
`srtc-swift-sdk` 的版本必须与 SMeeting 锁定的 SRTC 版本一致，否则依赖解析直接失败。升级 SMeeting 时一并检查这条依赖。屏幕共享扩展 target 不要挂这个产品。
</Warning>

---

### 使用

```swift
import SMeeting
import SRTCDeepFilterNet

final class MeetingService {
    let meeting = SMeetingEngine()
    /// SDK 对处理器是弱引用，必须由业务持有，否则会被立即释放、降噪静默失效
    private var denoiser: DeepFilterNetProcessor?

    func enableDenoise() {
        // 1. 不支持的设备直接隐藏降噪开关
        guard DeepFilterNetProcessor.isSupported else { return }
        do {
            // 2. 创建插件，强度 0–100，默认 50
            let processor = try DeepFilterNetProcessor(suppressionLevel: 50)
            // 3. 运行中算力不足时插件自动暂停降噪，并在主线程回调
            processor.onOverload = {
                print("设备性能不足，AI 降噪已暂停")
            }
            // 4. 挂上即生效；入会前后都可以设置
            meeting.audioCaptureProcessor = processor
            denoiser = processor
        } catch {
            // 设备不支持：SRTCError.featureNotSupported（低位 032）
        }
    }

    func disableDenoise() {
        meeting.audioCaptureProcessor = nil   // 卸载
        denoiser = nil
    }
}
```

运行时调整强度或临时旁路，直接调插件，不需要重新挂载：

```swift
denoiser?.setSuppressionLevel(80)  // 0–100，越大压制越强
denoiser?.setEnabled(false)        // 旁路：音频原样通过，处理器仍挂着
denoiser?.setEnabled(true)         // 恢复降噪，同时清除算力不足导致的暂停
```

---

### 会议层的行为

+ **SDK 对处理器是弱引用**：业务方要自己持有处理器对象（上例的 `denoiser`），否则它会被立即释放，降噪静默失效。
+ **全局生效**：同一时刻只能挂一个处理器，挂一次对之后的会议都有效，不需要每次入会重挂。
+ **挂载时按插件的声明关闭 WebRTC 自带的软件降噪**，卸载后恢复，避免两道降噪叠加让人声发闷。iOS / macOS 系统自带的语音处理（回声消除等）始终保留。
+ 本端音量（说话人电平）反映的是降噪前的音量。

---

### 设备不支持与算力不足

+ **开启前**：`isSupported` 为 `false` 的设备不支持，构造函数抛 `SRTCError.featureNotSupported`（错误码低位 `032`，iOS 为 `103032`、macOS 为 `105032`）。目前的苹果设备都支持，建议仍按跨端统一的写法先判断再开启。
+ **运行中**：设备持续过载时插件自动转入旁路、保证通话不卡顿，并回调 `onOverload`。建议提示用户，由用户决定是否调用 `setEnabled(true)` 重新开启。

---

### 自定义采集处理器

`audioCaptureProcessor` 接受任何遵循 SRTC `AudioProcessor` 协议的处理器，变声、自研降噪都可以挂；需要关闭某项自带处理时遵循 `AudioProcessingDeclaring` 声明，约定见 SRTC 文档 [自定义处理器声明 3A 要求](/zh/rtc/swift/advanced/deepfilternet#自定义处理器声明-3a-要求)。

---

### 相关页面

+ [SRTC：AI 降噪（DeepFilterNet）](/zh/rtc/swift/advanced/deepfilternet)
+ [SMeetingEngine 接口](/zh/meeting/swift/api-reference/SMeetingEngine)
