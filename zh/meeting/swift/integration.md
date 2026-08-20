---
title: "集成方式"
description: "SMeeting Swift SDK 的环境要求、Swift Package Manager 集成方式与权限配置"
---

SMeeting Swift SDK 是一套 `Swift Package` 形态的会议 SDK，对外模块名为 `SMeeting`，当前支持：

+ iOS 13.0 及以上
+ macOS 10.15 及以上
+ Xcode 15 及以上
+ Swift 5.9 及以上

SMeeting 构建在 SRTC 音视频能力之上：会议层负责房间、会议、参会成员、主持人管控等业务语义，底层的音视频采集、编解码、渲染仍由 SRTC 提供。引入 `SMeeting` 时，SRTC 会作为依赖被一并解析，你不需要单独再加一次。

<Note>
**苹果平台有两套 SMeeting SDK，先确认你要用哪一套。** 本章是 Swift 原生 SDK（`import SMeeting`，Swift Package 形态，同时支持 iOS 与 macOS）；另有一套 Objective-C 的 `MeetingKit`（CocoaPods 分发，仅 iOS），见 [iOS SDK](/zh/meeting/ios/quickstart)。

**新项目建议用本章的 Swift SDK。** 两套 API 不能混用，也不要在同一工程里同时引入。
</Note>

---

### 通过 Swift Package Manager 集成

SDK 以预编译 XCFramework 形式分发，包含 iOS 真机、iOS 模拟器、macOS 三个平台切片。

会议层构建在音视频层之上，但你只需要声明一个依赖 —— 底层的 SRTC 与 WebRTC 会被 SPM 自动解析。

#### 在 Package.swift 中声明

```swift
// Package.swift
dependencies: [
    .package(url: "https://github.com/seastart/smeeting-swift-sdk.git", from: "1.2.0"),
],
targets: [
    .target(
        name: "YourApp",
        dependencies: [
            .product(name: "SMeeting", package: "smeeting-swift-sdk"),
        ]
    ),
]
```

#### 在 Xcode 工程中添加

如果你使用 Xcode 工程而不是纯 SPM 工程：

+ 打开 `File > Add Package Dependencies...`
+ 填入 `https://github.com/seastart/smeeting-swift-sdk.git`
+ 在目标 Target 中勾选 `SMeeting`

#### 例外：iOS 全屏共享需要再加一条依赖

只有要做 **iOS 全屏屏幕共享**（共享整个系统屏幕，而非仅本 App 画面）时才需要这一步。它的扩展侧要链接 `SRTCBroadcastKit` —— 那是音视频层 `srtc-swift-sdk` 的第二个产物（不含 WebRTC），而 SwiftPM 不允许使用传递依赖的产品，所以要显式再声明一次：

```swift
dependencies: [
    .package(url: "https://github.com/seastart/smeeting-swift-sdk.git", from: "1.2.0"),
    // 版本必须与 SMeeting 内部锁定的 SRTC 版本一致
    .package(url: "https://github.com/seastart/srtc-swift-sdk.git", exact: "1.3.0"),
],
```

<Warning>
`SRTCBroadcastKit` **只能加到 Broadcast Upload Extension 的 target 上**，不要同时加到 App target —— App 侧的 `SRTC` 里已经静态含有同一份代码，重复链接会让一个进程里出现两份同名类型。反过来让扩展去链 `SMeeting` / `SRTC` 同样不行：那会把 WebRTC 拉进只有 50MB 内存上限的扩展进程。

完整接入步骤见 [屏幕共享](/zh/meeting/swift/advanced/screen-sharing)。
</Warning>

SMeeting 每个版本锁定的 SRTC 版本是固定的（用 `exact:` 钉住，保证是我们测过的组合），可以在 [更新日志](/zh/meeting/swift/changelog) 里查到对应关系。

---

### 导入 SDK

```swift
import SMeeting
```

会议相关的类型（`SMeetingEngine`、`MeetingCreateReq`、`MeetingUserInfo`、`SMeetingDelegate` 等）都在 `SMeeting` 模块里。

以下几类类型来自底层 SRTC 模块，用到时需要额外引入：

```swift
import SRTC
```

| 场景 | 涉及类型 |
| --- | --- |
| 渲染视频画面 | `SRTCVideoView`、`SRTCVideoRenderer` |
| 指定采集参数 | `CameraPreset`、`MicPreset`、`ScreenPreset` |
| 设置日志级别 | `LogLevel` |
| 枚举外设 | `DeviceInfo` |
| macOS 选择共享源 | `ScreenCaptureSources`、`DisplaySource`、`WindowSource` |
| iOS 全屏共享 | `SRTCBroadcastPicker`（唤起系统广播选择器） |
| iOS 音频路由 | `AudioRoute`、`AudioRouteTarget`、`AudioRouteInfo`、`AudioCallState` |
| 通话质量事件 | `QualityReport`、`ConnectionQualityChange`、`ActiveSpeakersSnapshot`、`LayerSwitchedInfo` |
| 断开原因 | `DisconnectReason` |

---

### 权限配置

#### iOS

在 `Info.plist` 中补充：

```xml
<key>NSCameraUsageDescription</key>
<string>需要访问摄像头以进行视频会议</string>
<key>NSMicrophoneUsageDescription</key>
<string>需要访问麦克风以进行语音会议</string>
```

建议同时声明后台音频能力，避免 App 切到后台时音频被系统挂起：

```xml
<key>UIBackgroundModes</key>
<array>
    <string>audio</string>
</array>
```

<Note>
iOS 上**入会时就会申请麦克风权限**，即使成员只打算旁听；入会期间状态栏也会显示橙色麦克风指示点。这是音频路由可控的前提，与 Zoom、腾讯会议等 App 一致，原因见 [音频路由](/zh/meeting/swift/advanced/audio-routing)。所以 `NSMicrophoneUsageDescription` 是必填项，缺了会崩溃。
</Note>

#### macOS

在 `Info.plist` 中补充：

```xml
<key>NSCameraUsageDescription</key>
<string>需要访问摄像头以进行视频会议</string>
<key>NSMicrophoneUsageDescription</key>
<string>需要访问麦克风以进行语音会议</string>
<key>NSScreenCaptureUsageDescription</key>
<string>需要录制屏幕以进行屏幕共享</string>
```

如果你要使用屏幕共享，还需要注意：

+ macOS 上选择显示器或应用窗口共享需要用户在系统弹窗中授权
+ 指定共享源的接口要求 macOS 12.3 及以上，详见 [屏幕共享](/zh/meeting/swift/advanced/screen-sharing)

---

### 最小接入检查清单

+ 已将 `SMeeting` 添加到目标依赖
+ 已配置摄像头 / 麦克风（以及屏幕录制）权限文案
+ 业务后端已能签发登录 SDK 所需的 meeting token
+ UI 层已准备好本地画面区域和远端画面区域

完成以上步骤后，可以继续阅读 [快速开始](/zh/meeting/swift/quickstart)。
