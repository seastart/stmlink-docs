---
title: "AI noise suppression (DeepFilterNet)"
description: "Enable AI noise suppression with adjustable strength on the microphone with the SRTCDeepFilterNet plugin: integration, on/off and strength control, handling unsupported devices and CPU overload, and how a custom capture processor declares that built-in noise suppression should be off."
---

### Overview

`SRTCDeepFilterNet` is an AI noise suppression plugin based on [DeepFilterNet3](https://github.com/Rikorose/DeepFilterNet). It uses the same algorithm, model, and parameters as the Web [DeepFilterNet noise suppression plugin](/en/rtc/web/advanced/deepfilternet), so it sounds the same on every platform. It implements the SDK's `AudioProcessor` interface and takes effect once set on `SRTCEngine.audioCaptureProcessor`, with **suppression strength adjustable at runtime** and a **temporary bypass**.

The plugin is an **optional product** in the `srtc-swift-sdk` package, available since `1.8.0` on both iOS and macOS. Apps that don't use AI noise suppression don't need it.

---

### Integration

Add the `SRTCDeepFilterNet` product to the same app target that depends on `SRTC`:

```swift
// Package.swift
dependencies: [
    .package(url: "https://github.com/seastart/srtc-swift-sdk.git", from: "1.8.0")
],
targets: [
    .target(
        name: "YourApp",
        dependencies: [
            .product(name: "SRTC", package: "srtc-swift-sdk"),
            .product(name: "SRTCDeepFilterNet", package: "srtc-swift-sdk")
        ]
    )
]
```

In an Xcode project, select `SRTCDeepFilterNet` under `File > Add Package Dependencies...`. The model is built into the plugin; you don't need to copy any extra resources.

<Warning>
Don't add `SRTCDeepFilterNet` to the Broadcast Upload Extension for screen sharing. It is for the app process only.
</Warning>

---

### Usage

```swift
import SRTC
import SRTCDeepFilterNet

final class CallViewController: UIViewController {
    let srtc = SRTCEngine()
    /// Must be held by your code: the SDK keeps only a weak reference to the processor
    private var denoiser: DeepFilterNetProcessor?

    func enableDenoise() {
        // 1. Hide the noise suppression switch on unsupported devices
        guard DeepFilterNetProcessor.isSupported else { return }
        do {
            // 2. Create the plugin; strength 0–100, default 50
            let denoiser = try DeepFilterNetProcessor(suppressionLevel: 50)
            // 3. If the CPU can't keep up during a call, the plugin pauses suppression and calls back on the main thread
            denoiser.onOverload = { [weak self] in
                self?.showToast("Device too slow; AI noise suppression paused")
            }
            self.denoiser = denoiser
            // 4. Takes effect as soon as it's set; you can set it before or after joining
            srtc.audioCaptureProcessor = denoiser
        } catch {
            // Device not supported: SRTCError.featureNotSupported (032)
            print("Failed to enable AI noise suppression: \(error)")
        }
    }

    func disableDenoise() {
        srtc.audioCaptureProcessor = nil   // Detach and restore the SDK's default audio processing
        denoiser = nil
    }
}
```

Adjust the strength or bypass temporarily at runtime without detaching:

```swift
denoiser?.setSuppressionLevel(80)  // 0–100; higher suppresses more
denoiser?.setEnabled(false)        // Bypass: audio passes through unchanged while the processor stays attached
denoiser?.setEnabled(true)         // Resume suppression and clear a pause caused by CPU overload
```

---

### API

| API | Description |
| --- | --- |
| `static var isSupported: Bool` | Whether the current device is supported. Check it before enabling, and hide the switch when unsupported |
| `init(suppressionLevel: Int = 50, modelURL: URL? = nil) throws` | Creates the plugin. `suppressionLevel` is the strength, 0–100; `modelURL` is normally omitted so the built-in model is used. Throws `SRTCError.featureNotSupported` on unsupported devices and `SRTCError.invalidArgument` if the model can't be found |
| `setSuppressionLevel(_:)` | Adjusts the strength (0–100) at runtime |
| `setEnabled(_:)` | Turns suppression on or off. With `false`, audio passes through unchanged; `true` resumes suppression and clears a pause caused by CPU overload |
| `var suppressionLevel: Int` | Current strength, read-only |
| `var isEnabled: Bool` | Current on/off state, read-only. An automatic overload pause doesn't change it |
| `var onOverload: (() -> Void)?` | Called when the CPU can't keep up during a call and suppression has been paused automatically. Runs on the main thread, once per pause |

---

### Unsupported devices and CPU overload

AI noise suppression needs a certain amount of CPU power. The SDK handles this in two layers:

+ **Before enabling**: a device is unsupported when `isSupported` is `false`, and the initializer throws `SRTCError.featureNotSupported` (low-order code `032`; `103032` on iOS, `105032` on macOS). All current Apple devices are supported, but we still recommend checking before enabling, in line with the other platforms.
+ **During a call**: if the device stays overloaded (for example, while running other heavy workloads), the plugin switches to bypass automatically so the call doesn't stutter, and calls `onOverload`. Tell the user something like "Device too slow; noise suppression paused" and let them decide whether to call `setEnabled(true)` to turn it back on.

---

### Notes

+ **Your code must hold the plugin instance.** `audioCaptureProcessor` is a weak reference; if you only write `srtc.audioCaptureProcessor = try DeepFilterNetProcessor()`, the instance is released immediately and suppression has no effect.
+ **When attached, the SDK turns off WebRTC's built-in software noise suppression** and restores it on detach, so two layers of suppression don't stack and muffle the voice. Echo cancellation and automatic gain control are unaffected.
+ **The system's voice processing stays on.** During calls on iOS / macOS, the system's own echo cancellation and noise suppression can't be turned off separately; AI noise suppression runs on top of it. Listen on your target devices before going live.
+ The model loads in the background (usually in under 1 second). Until it's loaded, audio passes through unchanged and capture isn't blocked.
+ It works only with 48 kHz capture. When capture drops to 8 kHz / 16 kHz (for example, Bluetooth headsets in call mode), it bypasses automatically and resumes when capture returns to 48 kHz.
+ There is only one `audioCaptureProcessor`, applied to all channels. To combine it with other processing such as voice changing, chain the calls inside your own processor.
+ License: DeepFilterNet itself is Apache-2.0/MIT; verify the license of the model weights yourself before distribution.

---

### Declaring 3A requirements in a custom processor

If your own `AudioProcessor` also needs the built-in processing turned off (for example, when integrating another noise suppression algorithm), additionally conform to `AudioProcessingDeclaring` to declare its requirements for WebRTC's built-in 3A. When it's set as `audioCaptureProcessor`, the SDK applies the declaration, and restores the defaults when the processor is replaced or cleared:

```swift
final class MyDenoiser: NSObject, AudioProcessor, AudioProcessingDeclaring {
    // false requires it off; nil leaves the SDK default unchanged
    let audioProcessing = AudioProcessingConstraints(noiseSuppression: false)

    func audioProcessingInitialize(sampleRate sampleRateHz: Int, channels: Int) {}
    func audioProcessingProcess(audioBuffer: AudioBuffer) { /* Process in place */ }
    func audioProcessingRelease() {}
}
```

`AudioProcessingConstraints` has the same meaning as the same-named type in the Web SDK; see [Types](/en/rtc/swift/types#audioprocessingconstraints) for its fields.
