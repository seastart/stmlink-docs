---
title: "Integration"
description: "Requirements (iOS 16 / macOS 14, Xcode 15, Swift 5.9), adding the SMeeting Swift SDK with Swift Package Manager, the extra SRTCBroadcastKit dependency for iOS full-screen sharing, which types need import SRTC, and Info.plist permissions. Read this before writing any meeting code on iOS or macOS."
---

The SMeeting Swift SDK is a conferencing SDK delivered as a `Swift Package`, with the public module name `SMeeting`. It currently supports:

+ iOS 16.0 and later
+ macOS 14.0 and later
+ Xcode 15 and later
+ Swift 5.9 and later

<Warning>
**Starting with `1.3.0`, the minimum OS versions were raised from iOS 13 / macOS 10.15 to iOS 16 / macOS 14.** Projects below these minimums can't resolve 1.3.0 or later (you get a dependency resolution failure, not a compile error); projects that still need to support older systems should stay on `1.2.1`.

The minimums come from the virtual background inference runtime in the audio and video layer—SwiftPM's `platforms:` is package-wide, and a dependent package can only be equal to or higher than its dependency. For details, see [Virtual background](/en/meeting/swift/advanced/virtual-background).
</Warning>

SMeeting is built on top of SRTC's audio and video capabilities: the meeting layer handles business semantics such as rooms, meetings, members, and host controls, while the underlying audio and video capture, encoding and decoding, and rendering are still provided by SRTC. When you add `SMeeting`, SRTC is resolved along with it as a dependency, so you don't need to add it separately.

<Note>
**There are two SMeeting SDKs for Apple platforms—first confirm which one you need.** This section covers the native Swift SDK (`import SMeeting`, delivered as a Swift Package, supporting both iOS and macOS); there is also an Objective-C `MeetingKit` (distributed via CocoaPods, iOS only), see [iOS SDK](/en/meeting/ios/quickstart).

**For new projects, we recommend the Swift SDK in this section.** The two APIs can't be mixed, and you shouldn't add both to the same project.
</Note>

---

### Integrate with Swift Package Manager

The SDK is distributed as a precompiled XCFramework containing three platform slices: iOS device, iOS simulator, and macOS.

The meeting layer is built on top of the audio and video layer, but you only need to declare one dependency—SPM resolves the underlying SRTC and WebRTC automatically.

#### Declare it in Package.swift

```swift
// Package.swift
dependencies: [
    .package(url: "https://github.com/seastart/smeeting-swift-sdk.git", from: "1.3.8"),
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

#### Add it in an Xcode project

If you use an Xcode project rather than a pure SPM project:

+ Open `File > Add Package Dependencies...`
+ Enter `https://github.com/seastart/smeeting-swift-sdk.git`
+ Check `SMeeting` for your target

#### Exception: iOS full-screen sharing needs one more dependency

You need this step only for **iOS full-screen screen sharing** (sharing the entire system screen, not just your app's content). The extension must link `SRTCBroadcastKit`—the second product of the audio and video layer's `srtc-swift-sdk` (it doesn't include WebRTC)—and because SwiftPM doesn't allow using products of transitive dependencies, you must declare it explicitly:

```swift
dependencies: [
    .package(url: "https://github.com/seastart/smeeting-swift-sdk.git", from: "1.3.8"),
    // The version must match the SRTC version pinned inside SMeeting
    .package(url: "https://github.com/seastart/srtc-swift-sdk.git", exact: "1.4.7"),
],
```

<Warning>
**Add `SRTCBroadcastKit` only to the Broadcast Upload Extension target**, not to the app target as well—`SRTC` on the app side already statically contains the same code, and linking it twice puts two copies of the same types into one process. The reverse doesn't work either: linking `SMeeting` / `SRTC` into the extension pulls WebRTC into an extension process that has a 50 MB memory limit.

For the full integration steps, see [Screen sharing](/en/meeting/swift/advanced/screen-sharing).
</Warning>

Each SMeeting version pins a fixed SRTC version (pinned with `exact:` to guarantee a combination we have tested); you can find the mapping in the [Changelog](/en/meeting/swift/changelog).

---

### Import the SDK

```swift
import SMeeting
```

Meeting-related types (`SMeetingEngine`, `MeetingCreateReq`, `MeetingUserInfo`, `SMeetingDelegate`, etc.) are all in the `SMeeting` module.

The following types come from the underlying SRTC module and require an extra import when you use them:

```swift
import SRTC
```

| Scenario | Types |
| --- | --- |
| Render video | `SRTCVideoView`, `SRTCVideoRenderer` |
| Specify capture parameters | `CameraPreset`, `MicPreset`, `ScreenPreset` |
| Set the log level | `LogLevel` |
| Enumerate devices | `DeviceInfo` |
| Choose a sharing source on macOS | `ScreenCaptureSources`, `DisplaySource`, `WindowSource` |
| Full-screen sharing on iOS | `SRTCBroadcastPicker` (brings up the system broadcast picker) |
| Audio routing on iOS | `AudioRoute`, `AudioRouteTarget`, `AudioRouteInfo`, `AudioCallState` |
| Virtual background | `SRTCNativeImage` (the background image, an alias of `UIImage` / `NSImage`), `SRTCVirtualBackgroundEffect` |
| Call quality events | `QualityReport`, `ConnectionQualityChange`, `ActiveSpeakersSnapshot`, `LayerSwitchedInfo` |
| Disconnect reason | `DisconnectReason` |

---

### Permissions

#### iOS

Add the following to `Info.plist`:

```xml
<key>NSCameraUsageDescription</key>
<string>Camera access is required for video meetings</string>
<key>NSMicrophoneUsageDescription</key>
<string>Microphone access is required for voice meetings</string>
```

We recommend also declaring the background audio capability, so the system doesn't suspend audio when the app goes to the background:

```xml
<key>UIBackgroundModes</key>
<array>
    <string>audio</string>
</array>
```

<Note>
On iOS, **the SDK requests microphone permission when you enter the meeting**, even if the member only intends to listen; the orange microphone indicator also shows in the status bar while in the meeting. This is a prerequisite for controllable audio routing and matches apps such as Zoom and Tencent Meeting; for the reason, see [Audio routing](/en/meeting/swift/advanced/audio-routing). So `NSMicrophoneUsageDescription` is required—the app crashes without it.
</Note>

#### macOS

Add the following to `Info.plist`:

```xml
<key>NSCameraUsageDescription</key>
<string>Camera access is required for video meetings</string>
<key>NSMicrophoneUsageDescription</key>
<string>Microphone access is required for voice meetings</string>
<key>NSScreenCaptureUsageDescription</key>
<string>Screen recording is required for screen sharing</string>
```

If you use screen sharing, also note:

+ On macOS, sharing a display or an app window requires the user to grant permission in a system prompt
+ The APIs that specify a sharing source require macOS 12.3 or later; for details, see [Screen sharing](/en/meeting/swift/advanced/screen-sharing)

---

### Minimum integration checklist

+ `SMeeting` has been added to your target's dependencies
+ Usage descriptions for camera / microphone (and screen recording) permissions are configured
+ Your backend can issue the meeting token needed to log in to the SDK
+ Your UI has areas ready for local video and remote video

Once you've completed these steps, continue with the [Quickstart](/en/meeting/swift/quickstart).
