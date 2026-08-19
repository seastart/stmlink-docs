---
title: "集成方式"
description: "SRTC Swift SDK 的环境要求、Swift Package Manager 集成方式与权限配置"
---

SRTC Swift SDK 是一套 `Swift Package` 形态的原生音视频 SDK，对外模块名为 `SRTC`，当前支持：

+ iOS 13.0 及以上
+ macOS 10.15 及以上
+ Xcode 15 及以上
+ Swift 5.9 及以上

<Note>
**苹果平台有两套 SRTC SDK，先确认你要用哪一套。** 本章是 Swift 原生 SDK（`import SRTC`，Swift Package 形态，同时支持 iOS 与 macOS）；另有一套 Objective-C 的 `RTCEngineKit`（CocoaPods 分发，仅 iOS），见 [iOS SDK](/zh/rtc/ios/integration)。

**新项目建议用本章的 Swift SDK。** 两套 API 不能混用，也不要在同一工程里同时引入。
</Note>

---

### 通过 Swift Package Manager 集成

SDK 以预编译 XCFramework 形式分发，包含 iOS 真机、iOS 模拟器、macOS 三个平台切片。

#### 在 Package.swift 中声明

```swift
// Package.swift
dependencies: [
    .package(url: "https://github.com/seastart/srtc-swift-sdk.git", from: "1.2.0")
],
targets: [
    .target(
        name: "YourApp",
        dependencies: [
            .product(name: "SRTC", package: "srtc-swift-sdk")
        ]
    )
]
```

#### 在 Xcode 中添加

如果你使用 Xcode 工程而不是纯 SPM 工程：

+ 打开 `File > Add Package Dependencies...`
+ 填入 `https://github.com/seastart/srtc-swift-sdk.git`
+ 在目标 Target 中勾选 `SRTC`

#### SRTCBroadcastKit（iOS 全屏屏幕共享才需要）

同一个包里还有一个 `SRTCBroadcastKit` 产品，只给 iOS 屏幕共享的 Broadcast Upload Extension
使用，普通接入不需要它。集成步骤见[屏幕共享](/zh/rtc/swift/advanced/screen-sharing)。

<Warning>
`SRTCBroadcastKit` 只勾选到扩展 target，**不要**勾到 App target；扩展 target 也**不要**
依赖 `SRTC`。扩展进程内存上限 50MB，链上 WebRTC 会被系统杀掉；而 App 侧的 `SRTC` 里已经
含有同一份代码，重复链接会让一个进程里出现两份同名类型。
</Warning>

---

### 导入 SDK

```swift
import SRTC
```

底层的 WebRTC 与信令组件由 Swift Package Manager 自动解析，你不需要手动再引入一层。

---

### 权限配置

#### iOS

在 `Info.plist` 中补充：

```xml
<key>NSCameraUsageDescription</key>
<string>需要访问摄像头以进行视频通话</string>
<key>NSMicrophoneUsageDescription</key>
<string>需要访问麦克风以进行语音通话</string>
```

#### macOS

在应用的 `Info.plist` 中同样需要补充：

```xml
<key>NSCameraUsageDescription</key>
<string>需要访问摄像头以进行视频通话</string>
<key>NSMicrophoneUsageDescription</key>
<string>需要访问麦克风以进行语音通话</string>
```

如果你要使用屏幕共享，还需要注意：

+ macOS 屏幕共享基于 `ScreenCaptureKit`
+ 选择窗口或显示器共享需要用户在系统弹窗中授权
+ 采集系统音频需要较新的系统能力，见 [屏幕共享](/zh/rtc/swift/advanced/screen-sharing)

---

### 最小接入检查清单

+ 已将 `SRTC` 添加到目标依赖
+ 已配置摄像头 / 麦克风权限文案
+ 业务后端已能签发加入频道所需的 Token
+ UI 层已准备好一个本地预览区域和一个远端视频区域

完成以上步骤后，可以继续阅读 [快速开始](/zh/rtc/swift/quickstart)。
