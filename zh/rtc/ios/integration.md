---
title: "集成方式"
description: "iOS SRTC 音视频 SDK 环境配置与 SDK 安装指南"
---

[RTCEngineKit](https://github.com/seastart/RTCEngineKit) 提供两种集成方式：您既可以通过CocoaPods自动集成我们的SDK，也可以通过手动下载SDK, 然后添加到您的项目中。

+ 编译语言：Objective-C
+ 编译环境：Xcode 11.0 及以上版本
+ 操作系统支持：iOS 10.0 及以上版本
+ SDK暂不支持模拟器编译
+ Enable Bitcode 配置 NO

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

