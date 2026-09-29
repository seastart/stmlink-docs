---
title: "Virtual background"
description: "Virtual background in the SRTC Swift SDK: person segmentation for background blur or replacement, no license key. Why enabling it once covers all camera tracks, why camera switches need no extra work, two frame-rate settings for low-end devices, and the iOS 16 / macOS 14 minimum since 1.4.0."
---

Virtual background runs person segmentation in the camera capture pipeline and replaces everything outside the person with a blur or a specified image. It's an in-house component, and installing it **doesn't require a license key**.

<Note>
The API lives on `SRTCEngine`, but there's **a single process-wide state** (internally it's `SRTCVirtualBackground.shared`): an inference session takes tens of MB and installing takes hundreds of milliseconds, so multiple engine instances and multiple channels share the same configuration. There's no way to "enable virtual background for only one channel".

Once enabled, it **automatically applies to all camera tracks**, including those created after enabling it (`createLocalCameraTrack` attaches it automatically). You don't need to add anything to `videoProcessors`.

**You don't need to do anything after switching between the front and back cameras or switching camera devices**: the SDK clears the inter-frame state internally and keeps it in effect.
</Note>

<Warning>
Starting with `1.4.0`, the minimum system requirements were raised to **iOS 16.0 / macOS 14.0** (previously iOS 13 / macOS 10.15). Projects below these minimums can't resolve version 1.4.0 or later—see [Integration](/en/rtc/swift/integration) for details.

The inference runtime `onnxruntime` is **statically linked** into `SRTC.xcframework`, so you don't need to declare any extra dependency or embed anything.
</Warning>

---

### Step 1: **Install the virtual background component**

We recommend installing it before you need virtual background, for example when the call screen opens. Pass `nil` for `modelPath` to use the SDK's built-in person segmentation model.

```swift
/// Installing loads the model and creates an inference session, taking hundreds of milliseconds — don't call it on the main thread or the capture thread
Task.detached(priority: .userInitiated) {
    do {
        try srtc.installVirtualBackground()          // Pass nil for modelPath to use the built-in model
    } catch {
        print("Failed to install virtual background:", error.localizedDescription)
    }
}
```

Errors thrown:

| **Error** | **Description** |
| --- | --- |
| `virtualBackgroundAlreadyInstalled` | The component is already installed; this call is discarded |
| `virtualBackgroundModelNotFound(String)` | The model file doesn't exist; check `modelPath` |
| `virtualBackgroundSessionFailed(String)` | Failed to create the inference session; this is a runtime environment issue |

---

### Step 2: **Set the background effect**

Background blur and background replacement are **mutually exclusive; the later call wins**. Both APIs are also remembered if called before installing, and take effect automatically once installation completes, so you don't need to worry about their order relative to `installVirtualBackground()`.

```swift
/// Set background blur; level ranges 1–10, default 5 (out-of-range values are clamped to the bounds)
srtc.setVirtualBackgroundBlur(level: 5)

/// Set background replacement, scaled to cover (cropped, not stretched); pass nil to cancel replacement and go back to blur
srtc.setVirtualBackgroundImage(SRTCNativeImage(named: "background"))
```

`SRTCNativeImage` is an alias for the platform's native image type (`UIImage` on iOS, `NSImage` on macOS), and there's also an overload that accepts a `CGImage`.

---

### Step 3: **Turn virtual background on or off**

After installing, it's **off** by default and must be turned on explicitly. When off, it's a zero-overhead pass-through: the capture pipeline never calls the processor, runs no inference, and does no compositing.

```swift
try srtc.enableVirtualBackground(true)

/// Query whether it's on
let enabled = srtc.isVirtualBackgroundEnabled
```

Calling the switch when the component isn't installed throws `virtualBackgroundNotInstalled`. Turning it off clears the inter-frame state, so the next time it's turned on it converges again from the first frame and doesn't flash a stale mask.

---

### Step 4: **Keep frame rate on low-end devices (optional)**

By default, person segmentation runs on every frame. On low-end devices you can increase the inference interval and reuse masks to gain frame rate; then turn on mask sync as needed to eliminate trailing artifacts.

```swift
/// Run segmentation once every N frames (compositing still runs every frame), default 1
srtc.setVirtualBackgroundInferenceInterval(2)

/// Mask sync, default false
srtc.setVirtualBackgroundMaskSync(true)
```

| **Parameter** | **Default** | **Description** |
| --- | :---: | --- |
| `inferenceInterval` | `1` | Run segmentation once every N frames; values less than 1 are treated as 1. Increasing it lowers inference cost, at the price of the mask following more slowly during fast motion |
| `maskSync` | `false` | When on, non-inference frames aren't recomposited, so the video and the mask are always from the same moment, eliminating the misaligned trail when waving; the price is that the video update rate drops to the mask rate |

<Note>
When `inferenceInterval` is `1`, turning `setVirtualBackgroundMaskSync(_:)` on or off makes no difference—every frame is then inferred on the current frame and composited right away, so it's already aligned. It only takes effect after you increase the inference interval.
</Note>

When the frame rate is unstable, throttling by frame count can't control the actual inference frequency, so you can throttle by time instead (`inferenceIntervalMs`; both apply at the same time):

```swift
srtc.virtualBackground.inferenceIntervalMs = 66   // Inference at most ~15 times per second
```

---

### Step 5: **Uninstall the virtual background component**

Uninstall it when no longer in use to release the inference session and related buffers. Effect parameters you've set aren't cleared and still apply after the next install.

```swift
srtc.uninstallVirtualBackground()
```

---

### Frames are dropped on errors, never flashing the real background

When segmentation fails or the output buffer pool is exhausted, the SDK **drops that frame** rather than sending the unprocessed raw camera frame—that would flash the real background to the remote side, which for virtual background is a privacy incident. The price is that the remote side sees a brief stall.

You can read the dropped-frame count directly. If it keeps growing, segmentation is failing continuously, or something downstream in your processor chain is holding output buffers across frames:

```swift
print(srtc.virtualBackground.droppedFrameCount)
```

`srtc.virtualBackground` also provides read-only state such as `isInstalled`, `isEnabled`, `effect`, and `blurLevel`, for aligning your UI with the SDK's real state (for example, restoring control values when a panel is reopened).

---

### Screen sharing and custom video tracks

Virtual background applies automatically only to camera tracks. Screen sharing and custom video tracks **don't** go through virtual background by default—to add the effect to them, put this instance into that track's `videoProcessors` manually (it's a `VideoProcessor` itself):

```swift
customTrack.videoProcessors = [srtc.virtualBackground]
```

When you take over capture yourself (`LocalVideoTrack` + a custom capturer), clear the inter-frame state manually once after rebuilding the capture pipeline; otherwise temporal smoothing still holds the mask from the old frames:

```swift
srtc.virtualBackground.reset()      // Only clears inter-frame state; configuration is unaffected
```

Camera tracks don't need this step; the SDK already calls it during device switching.

---

### Consistency between local preview and published video

While virtual background is on, the local preview shows the processed video, the same data the remote side sees (the preview goes through `track.addRenderer()`, which renders frames after the processors). When it's off, the local preview goes back to the raw camera video.

---

### Performance cost

Person segmentation always runs CPU inference, without CoreML: the model is only 256×256, and its operators can't be fully handled by CoreML, so the cost of shuttling data between the CPU and CoreML on every frame exceeds the compute saved—in testing, it's a net slowdown.

The algorithm is implemented from the same source as the Objective-C version (the same person segmentation + mask post-processing). For the order of magnitude of per-frame time, refer to the measured data in [Virtual background in the iOS SDK](/zh/rtc/ios/advanced/virtual-background#性能开销) (Chinese). Run a round of tests on a real device with the default parameters (segmentation every frame) first, and increase the inference interval as in Step 4 only if it exceeds your frame budget.

---

### Related pages

+ [Integration](/en/rtc/swift/integration) — system requirements and integration steps
+ [Error codes](/en/rtc/swift/error-codes) — virtual-background-related values of `SRTCError`
+ [Custom tracks](/en/rtc/swift/advanced/custom-track) — the processor chain when you take over capture yourself
