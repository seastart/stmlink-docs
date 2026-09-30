---
title: "Integration"
description: "Add the Objective-C SRTC SDK (RTCEngineKit) to an iOS app: system requirements (iOS 16.0 since 3.1.0, no simulator, Bitcode off), manual framework integration with required system libraries and onnxruntime, or CocoaPods. Read before the iOS quickstart."
---

[RTCEngineKit](https://github.com/seastart/RTCEngineKit) offers two integration methods: you can integrate the SDK automatically with CocoaPods, or download the SDK manually and add it to your project.

+ Language: Objective-C
+ Build environment: Xcode 14.0 or later
+ Supported OS: iOS 16.0 or later (since `3.1.0`; previously iOS 10.0)
+ The SDK doesn't support building for the simulator
+ Set Enable Bitcode to NO

<Warning>
Starting with `3.1.0`, the SDK includes virtual background, and the minimum system requirement was raised from iOS 10.0 to **iOS 16.0**. Both `IPHONEOS_DEPLOYMENT_TARGET` in your project and `platform :ios` in your `Podfile` must be 16.0 or later; otherwise the dependency can't be resolved.
</Warning>

<Note>
**There are two SRTC SDKs for Apple platforms—confirm which one you need first.** This page covers the Objective-C `RTCEngineKit`; there is also a native Swift SDK (`import SRTC`, distributed as a Swift Package, supporting both iOS and macOS)—see [Swift SDK](/en/rtc/swift/integration).

**For new projects, we recommend the Swift SDK.** The two APIs can't be mixed, and don't include both in the same project.
</Note>

## Manual integration (not recommended)


+ Get the version of [RTCEngineKit](https://github.com/seastart/RTCEngineKit) you need, then import the resulting `RTCEngineKit.framework` into your project.
+ Add the system libraries that `RTCEngineKit` depends on

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

+ Also add `onnxruntime.xcframework` (`1.24.x`). The inference engine for virtual background isn't bundled in `RTCEngineKit.framework`; the SDK keeps only its undefined symbols, which your app resolves at link time. Without this library, linking fails with undefined symbols such as `_OrtGetApiBase`. You can get the iOS package from [ONNX Runtime Releases](https://github.com/microsoft/onnxruntime/releases), or use the CocoaPods integration below, which brings it in automatically.

+ Add `#import <RTCEngineKit/RTCEngineKit.h>` wherever you use `RTCEngineKit`

## Automatic integration (recommended)


Add `RTCEngineKit` to your `Podfile`

```objectivec
pod 'RTCEngineKit'
```

Install

```objectivec
pod install
```

If the library can't be found, try updating the local spec repo at the same time

```objectivec
pod install --repo-update
```

If you can't install the latest SDK version, run the following command to update your local CocoaPods repo list

```objectivec
pod repo update
```

