---
title: "Virtual background"
description: "Virtual background in the SMeeting Swift SDK: person segmentation for background blur or replacement, no license key needed. Covers why it's a device-level setting, why camera switches and restarts need no re-apply, two frame-rate parameters for low-end devices, and the 1.3.0 OS requirements."
---

Virtual background performs person segmentation in the camera capture pipeline and replaces everything outside the person with blur or a specified image. It's an in-house component, and installing it **doesn't require a license key**.

<Note>
The APIs are on `SMeetingEngine`, but the state is **device-level**: virtual background applies to the single shared camera capture pipeline in the process, so the setting applies to all meetings and channels at once. When you're in multiple rooms at the same time, there's no way to "turn on virtual background for just one room."

During the meeting, **you don't need to re-apply anything after switching cameras, turning the camera off and on again, or reconnecting after a disconnect**—the capture pipeline reads the effect for every frame, so rebuilding the track doesn't lose it.
</Note>

<Warning>
Starting with `1.3.0`, the minimum system requirements are raised to **iOS 16.0 / macOS 14.0** (previously iOS 13 / macOS 10.15). Projects below this minimum can't resolve 1.3.0 or later. For details, see [Integration](/en/meeting/swift/integration).

The inference runtime `onnxruntime` is statically linked into the audio and video layer's `SRTC.xcframework`, so you don't need to declare any extra dependencies.
</Warning>

---

### Step 1: **Install the virtual background component**

We recommend installing it before you need virtual background, for example when entering the meeting page. Pass `nil` for `modelPath` to use the SDK's built-in person segmentation model.

```swift
/// Installing loads the model and creates an inference session, taking hundreds of milliseconds—don't call it on the main thread or the capture thread
Task.detached(priority: .userInitiated) {
    do {
        try meeting.installVirtualBackground()       // Pass nil for modelPath to use the built-in model
    } catch {
        print("Failed to install virtual background:", error.localizedDescription)
    }
}
```

Errors thrown (`SRTCError` from the audio and video layer):

| **Error** | **Description** |
| --- | --- |
| `virtualBackgroundAlreadyInstalled` | The component is already installed; this call is discarded |
| `virtualBackgroundModelNotFound(String)` | The model file doesn't exist; check `modelPath` |
| `virtualBackgroundSessionFailed(String)` | Failed to create the inference session; this is a runtime environment problem |

---

### Step 2: **Set the background effect**

Background blur and background replacement are **mutually exclusive; the later call wins**. Both APIs are remembered even if called before installation and take effect automatically once installation completes, so you don't need to care about their order relative to `installVirtualBackground()`.

```swift
/// Set background blur; level ranges from 1 to 10, default 5 (out-of-range values are clamped to the boundary)
meeting.setVirtualBackgroundBlur(level: 5)

/// Set background replacement, cropped to cover without stretching; pass nil to cancel replacement and go back to blur
meeting.setVirtualBackgroundImage(SRTCNativeImage(named: "background"))
```

`SRTCNativeImage` is an alias for the platform's native image type (`UIImage` on iOS, `NSImage` on macOS).

---

### Step 3: **Turn virtual background on or off**

After installation, it's **off** by default and must be turned on explicitly. When off, frames pass straight through with zero overhead, and no inference runs.

```swift
try meeting.enableVirtualBackground(true)

/// Query whether it's on
let enabled = meeting.isVirtualBackgroundEnabled
```

Calling the switch before the component is installed throws `virtualBackgroundNotInstalled`. Turning it off clears the inter-frame state, so the next time it's turned on it converges again from the first frame and doesn't flash a stale mask.

<Note>
Virtual background is local preprocessing and has nothing to do with meeting state: **you can set it before or after entering the meeting**, and it isn't affected by permission actions such as the host muting you or turning off your camera. Settings made while the camera is off are also remembered, and you see the effect once the camera is on.
</Note>

---

### Step 4: **Keep the frame rate up on low-end devices (optional)**

By default, person segmentation runs on every frame. On low-end devices, you can increase the inference interval, trading mask reuse for frame rate; then turn on mask sync as needed to eliminate trailing artifacts.

```swift
/// Run segmentation every N frames (compositing still runs every frame); default 1
meeting.setVirtualBackgroundInferenceInterval(2)

/// Mask sync; default false
meeting.setVirtualBackgroundMaskSync(true)
```

| **Parameter** | **Default** | **Description** |
| --- | :---: | --- |
| `inferenceInterval` | `1` | Run segmentation every N frames; values below 1 are treated as 1. Increasing it lowers inference overhead, at the cost of the mask following more slowly during fast motion |
| `maskSync` | `false` | When on, non-inference frames aren't recomposited, so the video and the mask always come from the same moment, eliminating misaligned trails when waving; the cost is that the video update rate drops to the mask rate |

<Note>
When `inferenceInterval` is `1`, turning `setVirtualBackgroundMaskSync(_:)` on or off makes no difference at all—it only takes effect after you increase the inference interval.
</Note>

---

### Step 5: **Uninstall the virtual background component**

Uninstall it when no longer needed to release the inference session and related buffers. Effect parameters you've set aren't cleared and still apply after the next installation.

```swift
meeting.uninstallVirtualBackground()
```

---

### Frames are dropped on errors, so the real background never flashes

When segmentation fails or the output buffer pool is exhausted, the SDK **drops that frame** instead of sending the unprocessed raw camera frame—which would flash your real background to other members. The cost is a brief stutter in the video others see.

The dropped-frame count and read-only state are on `meeting.virtualBackground` (`droppedFrameCount`, `isInstalled`, `isEnabled`, `effect`, `blurLevel`), which you can use to populate panel controls with the SDK's actual state:

```swift
print(meeting.virtualBackground.droppedFrameCount)
```

---

### Consistency between local preview and the published stream

When virtual background is on, the local preview shows the processed video, which is the same data other members see; when it's off, the local preview goes back to the raw camera video.

For lower-level usage (attaching virtual background to a custom video track, clearing inter-frame state when you take over capture yourself), see [Virtual background](/en/rtc/swift/advanced/virtual-background) in the audio and video layer.

---

### Related pages

+ [Integration](/en/meeting/swift/integration)—system requirements and integration steps
+ [SMeetingEngine](/en/meeting/swift/api-reference/SMeetingEngine#virtual-background)—full signatures and parameters
+ [Virtual background in the audio and video layer](/en/rtc/swift/advanced/virtual-background)—diagnostics and custom track usage
