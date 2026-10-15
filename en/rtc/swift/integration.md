---
title: "Integration"
description: "Add the SRTC Swift SDK to an iOS or macOS app: system requirements (iOS 16 / macOS 14 since 1.4.0), Swift Package Manager setup in Package.swift or Xcode, when to use SRTCBroadcastKit, camera and microphone permissions, and a minimal integration checklist. Read before the Swift quickstart."
---

The SRTC Swift SDK is a native audio and video SDK distributed as a `Swift Package`, with the public module name `SRTC`. It currently supports:

+ iOS 16.0 and later
+ macOS 14.0 and later
+ Xcode 15 and later
+ Swift 5.9 and later

<Warning>
**Starting with `1.4.0`, the minimum system versions were raised from iOS 13 / macOS 10.15 to iOS 16 / macOS 14.** Projects below these minimums can't resolve version 1.4.0 or later (you get a dependency resolution failure, not a compile error); projects that still need to support older systems should stay on `1.3.3`.

The minimums are dictated by the inference runtime used for virtual background. SwiftPM's `platforms:` applies to the whole package and has no per-target minimum, so there's no way to apply this requirement to virtual background alone.
</Warning>

<Note>
**There are two SRTC SDKs for Apple platforms—confirm which one you need first.** This section covers the native Swift SDK (`import SRTC`, distributed as a Swift Package, supporting both iOS and macOS); there is also an Objective-C `RTCEngineKit` (distributed via CocoaPods, iOS only)—see [iOS SDK](/en/rtc/ios/integration).

**For new projects, we recommend the Swift SDK described here.** The two APIs can't be mixed, and don't include both in the same project.
</Note>

---

### Integrate with Swift Package Manager

The SDK is distributed as a prebuilt XCFramework containing slices for three platforms: iOS devices, the iOS Simulator, and macOS.

#### Declare it in Package.swift

```swift
// Package.swift
dependencies: [
    .package(url: "https://github.com/seastart/srtc-swift-sdk.git", from: "1.5.2")
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

#### Add it in Xcode

If you use an Xcode project instead of a pure SPM project:

+ Open `File > Add Package Dependencies...`
+ Enter `https://github.com/seastart/srtc-swift-sdk.git`
+ Select `SRTC` for your target

#### SRTCBroadcastKit (only for full-screen screen sharing on iOS)

The same package also contains an `SRTCBroadcastKit` product. It is used only by the Broadcast Upload Extension for iOS screen sharing;
regular integrations don't need it. For integration steps, see [Screen sharing](/en/rtc/swift/advanced/screen-sharing).

<Warning>
Add `SRTCBroadcastKit` only to the extension target—**don't** add it to the app target; the extension target also must **not**
depend on `SRTC`. The extension process has a 50 MB memory limit, and linking WebRTC gets it killed by the system; meanwhile, `SRTC` on the app side already
contains the same code, and linking it twice puts two copies of the same types in one process.
</Warning>

---

### Import the SDK

```swift
import SRTC
```

The underlying WebRTC and signaling components are resolved automatically by Swift Package Manager; you don't need to add another layer manually.

---

### Configure permissions

#### iOS

Add the following to `Info.plist`:

```xml
<key>NSCameraUsageDescription</key>
<string>Camera access is required for video calls</string>
<key>NSMicrophoneUsageDescription</key>
<string>Microphone access is required for voice calls</string>
```

#### macOS

The app's `Info.plist` also needs:

```xml
<key>NSCameraUsageDescription</key>
<string>Camera access is required for video calls</string>
<key>NSMicrophoneUsageDescription</key>
<string>Microphone access is required for voice calls</string>
```

If you use screen sharing, also note:

+ macOS screen sharing is based on `ScreenCaptureKit`
+ Sharing a window or display requires the user to grant permission in a system prompt
+ Capturing system audio requires newer system capabilities—see [Screen sharing](/en/rtc/swift/advanced/screen-sharing)

---

### Minimal integration checklist

+ `SRTC` has been added to your target's dependencies
+ Camera / microphone permission strings are configured
+ Your backend can already issue the token needed to join a channel
+ Your UI has a local preview area and a remote video area ready

After completing the steps above, continue with [Quickstart](/en/rtc/swift/quickstart).
