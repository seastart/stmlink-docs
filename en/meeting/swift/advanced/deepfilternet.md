---
title: "AI noise suppression (DeepFilterNet)"
description: "Turn on AI noise suppression for the microphone in meetings: add the SRTCDeepFilterNet product of srtc-swift-sdk, assign it to SMeetingEngine.audioCaptureProcessor, and handle processor ownership, unsupported devices, CPU overload, and custom capture processors"
---

### Overview

The meeting layer attaches microphone capture processors through `SMeetingEngine.audioCaptureProcessor`, available since `1.9.0`. The most common use is attaching the SRTC AI noise suppression plugin `SRTCDeepFilterNet`. It is based on DeepFilterNet3, uses the same algorithm and model as the Web and Android SDKs, and lets you adjust the suppression strength and bypass it at runtime.

The plugin is a separate, optional product; apps that don't use AI noise suppression don't need it. For the plugin's own API, strength, overload handling, and device checks, see the SRTC page [AI noise suppression (DeepFilterNet)](/en/rtc/swift/advanced/deepfilternet). This page only covers how to wire it into a meeting.

---

### Integration

The plugin lives in the `srtc-swift-sdk` distribution repository, so declare an additional `srtc-swift-sdk` dependency in your project, pinned with `exact:` to the SRTC version that matches SMeeting (SMeeting 1.10.0 pairs with SRTC `1.9.0`), and add `SRTCDeepFilterNet` to your App target:

```swift
dependencies: [
    .package(url: "https://github.com/seastart/smeeting-swift-sdk.git", from: "1.10.0"),
    .package(url: "https://github.com/seastart/srtc-swift-sdk.git", exact: "1.9.0"),
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

The same applies to Xcode projects: add `srtc-swift-sdk` under Package Dependencies, choose the Exact Version rule with `1.9.0`, and check `SRTCDeepFilterNet` only for the App target.

<Warning>
The `srtc-swift-sdk` version must match the SRTC version that SMeeting pins; otherwise dependency resolution fails. Check this dependency whenever you upgrade SMeeting. Don't add this product to the screen sharing extension target.
</Warning>

---

### Usage

```swift
import SMeeting
import SRTCDeepFilterNet

final class MeetingService {
    let meeting = SMeetingEngine()
    /// The SDK holds the processor weakly, so you must keep it; otherwise it's released immediately and noise suppression silently stops working
    private var denoiser: DeepFilterNetProcessor?

    func enableDenoise() {
        // 1. On unsupported devices, just hide the noise suppression switch
        guard DeepFilterNetProcessor.isSupported else { return }
        do {
            // 2. Create the plugin; strength 0–100, default 50
            let processor = try DeepFilterNetProcessor(suppressionLevel: 50)
            // 3. If the CPU can't keep up, the plugin pauses noise suppression automatically and calls back on the main thread
            processor.onOverload = {
                print("Not enough CPU, AI noise suppression paused")
            }
            // 4. Takes effect once attached; you can set it before or after entering the meeting
            meeting.audioCaptureProcessor = processor
            denoiser = processor
        } catch {
            // Device not supported: SRTCError.featureNotSupported (low-order code 032)
        }
    }

    func disableDenoise() {
        meeting.audioCaptureProcessor = nil   // Detach
        denoiser = nil
    }
}
```

To adjust the strength or bypass it temporarily at runtime, call the plugin directly; no need to reattach it:

```swift
denoiser?.setSuppressionLevel(80)  // 0–100; higher suppresses more
denoiser?.setEnabled(false)        // Bypass: audio passes through unchanged, the processor stays attached
denoiser?.setEnabled(true)         // Resume noise suppression and clear any pause caused by CPU overload
```

---

### Meeting-layer behavior

+ **The SDK holds the processor weakly**: keep your own reference to the processor (`denoiser` above); otherwise it's released immediately and noise suppression silently stops working.
+ **Global**: only one processor can be attached at a time. Attach it once and it applies to later meetings too; you don't need to reattach it every time you enter a meeting.
+ **When attached, the WebRTC built-in software noise suppression is turned off as the plugin declares**, and restored when detached, so two layers of noise suppression don't stack up and muffle the voice. The voice processing built into iOS / macOS (echo cancellation and so on) always stays on.
+ Your local volume (speaker level) reflects the volume before noise suppression.

---

### Unsupported devices and CPU overload

+ **Before enabling**: a device is unsupported when `isSupported` is `false`, and the initializer throws `SRTCError.featureNotSupported` (low-order code `032`; `103032` on iOS, `105032` on macOS). All current Apple devices are supported, but we still recommend checking before enabling, in line with the other platforms.
+ **While running**: if the device stays overloaded, the plugin switches to bypass automatically to keep the call smooth and calls `onOverload`. We recommend telling the user and letting them decide whether to call `setEnabled(true)` to turn it back on.

---

### Custom capture processors

`audioCaptureProcessor` accepts any processor that conforms to the SRTC `AudioProcessor` protocol, so you can attach voice changers or your own noise suppression. To turn off a built-in processing step, conform to `AudioProcessingDeclaring` and declare it; see the SRTC page [Declaring 3A requirements in a custom processor](/en/rtc/swift/advanced/deepfilternet#declaring-3a-requirements-in-a-custom-processor).

---

### Related pages

+ [SRTC: AI noise suppression (DeepFilterNet)](/en/rtc/swift/advanced/deepfilternet)
+ [SMeetingEngine API](/en/meeting/swift/api-reference/SMeetingEngine)
