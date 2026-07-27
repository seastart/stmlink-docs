---
title: "集成方式"
description: "SRTC Swift SDK 的环境要求、Swift Package Manager 集成方式与权限配置"
---

SRTC Swift SDK 是一套 `Swift Package` 形态的原生音视频 SDK，对外模块名为 `SRTC`，当前支持：

+ iOS 13.0 及以上
+ macOS 10.15 及以上
+ Xcode 15 及以上
+ Swift 5.9 及以上

注意：本节文档对应的是新的 `rtc-swift` 仓库和 `import SRTC` 接入方式；站点里原有的 [iOS SDK](/zh/rtc/ios/integration) 文档对应旧版 `RTCEngineKit`，两套 API 不能混用。

如果你要直接运行仓库里的 Demo，请额外注意：

+ `Example/SRTCDemo` 当前工程目标为 iOS 16.0 / macOS 13.0
+ 这属于 Demo 工程要求，不是 SDK 最低运行要求

---

### 通过 Swift Package Manager 集成

#### 本地路径引用

适合和 `rtc-swift` 仓库放在同一工作区联调：

```swift
// Package.swift
dependencies: [
    .package(path: "../rtc-swift")
],
targets: [
    .target(
        name: "YourApp",
        dependencies: [
            .product(name: "SRTC", package: "rtc-swift")
        ]
    )
]
```

#### Xcode 中添加 Package

如果你使用 Xcode 工程而不是纯 SPM 工程：

+ 打开 `File > Add Package Dependencies...`
+ 选择本地 `rtc-swift` 目录，或填写你们实际发布用的 Git 地址
+ 在目标 Target 中勾选 `SRTC`

> 如果后续会发布独立二进制仓库，请将这里的本地路径替换为你们正式的 Git 仓库地址。文档不预设一个尚未确认的线上仓库地址。

---

### 导入 SDK

```swift
import SRTC
```

SDK 依赖的 WebRTC 与 MQTT 组件会由 Swift Package Manager 自动解析，无需你手动再引入一层底层库。

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
