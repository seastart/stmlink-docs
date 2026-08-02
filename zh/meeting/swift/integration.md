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

---

### 通过 Swift Package Manager 集成

我们会提供给你两个 Swift Package 目录：会议层的 `meeting-swift` 和它依赖的音视频层 `rtc-swift`。

<Warning>
**两个目录必须并列放在同一层级。** `meeting-swift` 是以相对路径 `../rtc-swift` 引用音视频层的，目录结构不对会导致 SPM 解析失败：

```text
your-workspace/
├── meeting-swift/   ← 会议层
├── rtc-swift/       ← 音视频层，必须与 meeting-swift 同级
└── YourApp/         ← 你的工程
```

`rtc-swift` 自身依赖的 WebRTC、MQTT 等第三方库托管在公网，由 SPM 自动拉取，你不需要手动处理。
</Warning>

#### 在 Package.swift 中声明

```swift
// Package.swift
dependencies: [
    .package(path: "../meeting-swift"),
],
targets: [
    .target(
        name: "YourApp",
        dependencies: [
            // package 填包的标识，取本地目录最后一段名字
            .product(name: "SMeeting", package: "meeting-swift"),
        ]
    ),
]
```

#### 在 Xcode 工程中添加

如果你使用 Xcode 工程而不是纯 SPM 工程：

+ 打开 `File > Add Local Package...`
+ 选择本地的 `meeting-swift` 目录
+ 在目标 Target 中勾选 `SMeeting`

---

### 导入 SDK

```swift
import SMeeting
```

会议相关的类型（`SMeeting`、`MeetingCreateReq`、`MeetingUserInfo`、`SMeetingDelegate` 等）都在 `SMeeting` 模块里。

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
