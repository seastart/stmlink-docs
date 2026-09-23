---
title: "集成方式"
description: "iOS SRTC 音视频 SDK 环境配置与 SDK 安装指南"
---

[RTCEngineKit](https://github.com/seastart/RTCEngineKit) 提供两种集成方式：您既可以通过CocoaPods自动集成我们的SDK，也可以通过手动下载SDK, 然后添加到您的项目中。

+ 编译语言：Objective-C
+ 编译环境：Xcode 11.0 及以上版本
+ 操作系统支持：iOS 16.0 及以上版本（`3.1.0` 起，此前为 iOS 10.0）
+ SDK暂不支持模拟器编译
+ Enable Bitcode 配置 NO

<Warning>
`3.1.0` 起 SDK 内置虚拟背景，最低系统要求由 iOS 10.0 提升到 **iOS 16.0**，接入工程的 `IPHONEOS_DEPLOYMENT_TARGET` 与 `Podfile` 的 `platform :ios` 都需要不低于 16.0，否则依赖无法参与解析。
</Warning>

<Note>
**苹果平台有两套 SRTC SDK，先确认你要用哪一套。** 本章是 Objective-C 的 `RTCEngineKit`；另有一套 Swift 原生 SDK（`import SRTC`，Swift Package 形态，同时支持 iOS 与 macOS），见 [Swift SDK](/zh/rtc/swift/integration)。

**新项目建议用 Swift SDK。** 两套 API 不能混用，也不要在同一工程里同时引入。
</Note>

## 手动集成(不建议)


+ 根据需要，获取对应版本的 [RTCEngineKit](https://github.com/seastart/RTCEngineKit)，得到`RTCEngineKit.framework`并导入工程中。
+ 添加`RTCEngineKit`依赖的系统库

```objectivec
VideoToolbox.framework
AudioToolbox.framework
AVFoundation.framework
CoreFoundation.framework
CoreMedia.framework
CoreVideo.framework
Foundation.framework
QuartzCore.framework
Metal.framework
CoreML.framework
MetalPerformanceShaders.framework
Security.framework
OpenGLES.framework
Accelerate.framework
CoreGraphics.framework
SystemConfiguration.framework
ReplayKit.framework
libc++.tbd
libiconv.tbd
libz.tbd
```

+ 额外引入 `onnxruntime.xcframework`（`1.24.x`）。虚拟背景的推理引擎不随 `RTCEngineKit.framework` 打包，SDK 内部只保留其未定义符号，由 App 在链接期解决；缺少该库会在链接期报 `_OrtGetApiBase` 等符号未定义。可从 [ONNX Runtime Releases](https://github.com/microsoft/onnxruntime/releases) 获取 iOS 包，或改用下方的 CocoaPods 集成自动带入。

+ 在需要使用`RTCEngineKit`的地方 `#import <RTCEngineKit/RTCEngineKit.h>`

## 自动集成(建议)


在 `Podfile` 文件中加入`RTCEngineKit`

```objectivec
pod 'RTCEngineKit'
```

安装

```objectivec
pod install
```

如找不到该库请尝试同时更新本地源

```objectivec
pod install --repo-update
```

如果无法安装SDK最新版本，运行以下命令更新本地的CocoaPods仓库列表

```objectivec
pod repo update
```

