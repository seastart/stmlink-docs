---
title: "Virtual background"
description: "Virtual background in the Objective-C SRTC SDK on iOS: person segmentation for background blur or replacement, no license key. Covers ordering with beauty filters, two frame-rate settings for low-end devices, measured per-frame time and CPU usage, and the required onnxruntime dependency."
---

Virtual background runs person segmentation in the camera capture pipeline and replaces everything outside the person with a blur or a specified image. It's an in-house component, and **unlike beauty filters, installing it doesn't require a license key**.

<Note>
Virtual background and beauty filters act on the same shared camera capture pipeline, so settings apply to all channel instances at once.

When both are on, the order is fixed: **beauty filter first, then virtual background**. Person segmentation takes the beautified image as input, so its edges match the final video.
</Note>

<Warning>
Virtual background depends on `onnxruntime`. The SDK keeps only its undefined symbols, which your app resolves at link time. With CocoaPods integration, the dependency is brought in automatically, and the minimum system requirement is iOS 16.0; see [Integration](/en/rtc/ios/integration) for details.
</Warning>

### Step 1: **Install the virtual background component**

We recommend installing it before you need virtual background, for example when the call screen opens. Pass `nil` for `modelPath` to use the SDK's built-in person segmentation model.

```objectivec
/// Install the virtual background component
/// @param modelPath path to the person segmentation model file; pass nil to use the built-in model
RTCEngineError error = [[RTCEngineKit sharedEngine] installVirtualBackground:nil];
```

Return values:

| **Return value** | **Description** |
| --- | --- |
| RTCEngineErrorOK | Installed successfully |
| RTCEngineErrorConflict | The component is already installed; this call is discarded |
| RTCEngineErrorNotFound | The model file doesn't exist; check `modelPath` |
| RTCEngineErrorSystemError | Failed to create the inference session; this is a runtime environment issue |

### Step 2: **Set the background effect**

Background blur and background replacement are **mutually exclusive; the later call wins**. Both APIs are also remembered if called before installing, and take effect automatically once installation completes, so you don't need to worry about their order relative to `installVirtualBackground:`.

```objectivec
/// Set background blur
/// @param level blur level, range 1–10, default 5 (out-of-range values are clamped to the bounds)
[[RTCEngineKit sharedEngine] setVirtualBackgroundBlur:5];

/// Set background replacement
/// @param image background image, scaled to cover (cropped, not stretched); pass nil to cancel replacement and go back to blur
[[RTCEngineKit sharedEngine] setVirtualBackgroundImage:[UIImage imageNamed:@"background"]];
```

### Step 3: **Turn virtual background on or off**

After installing, it's **off** by default and must be turned on explicitly. When off, it's a zero-overhead pass-through and runs no inference.

```objectivec
/// Virtual background switch
/// @param enabled YES: on; NO: off
[[RTCEngineKit sharedEngine] enabledVirtualBackground:YES];

/// Get whether virtual background is on
BOOL enabled = [[RTCEngineKit sharedEngine] isVirtualBackgroundEnabled];
```

Calling the switch when the component isn't installed returns `RTCEngineErrorConflict`. Turning it off clears the inter-frame state, so the next time it's turned on it converges again from the first frame and doesn't flash a stale mask.

### Step 4: **Keep frame rate on low-end devices (optional)**

By default, person segmentation runs on every frame. On low-end devices you can increase the inference interval and reuse masks to gain frame rate; then turn on mask sync as needed to eliminate trailing artifacts.

```objectivec
/// Set the segmentation inference interval
/// @param interval run segmentation once every N frames (compositing still runs every frame), default 1
[[RTCEngineKit sharedEngine] setVirtualBackgroundInferenceInterval:2];

/// Set mask sync
/// @param enabled YES: on; NO: off; default NO
[[RTCEngineKit sharedEngine] setVirtualBackgroundMaskSync:YES];
```

| **Parameter** | **Default** | **Description** |
| --- | :---: | --- |
| inferenceInterval | `1` | Run segmentation once every N frames; values less than 1 are treated as 1. Increasing it lowers inference cost, at the price of the mask following more slowly during fast motion |
| maskSync | `NO` | When on, non-inference frames aren't recomposited, so the video and the mask are always from the same moment, eliminating the misaligned trail when waving; the price is that the video update rate drops to the mask rate |

<Note>
When `inferenceInterval` is `1`, turning `setVirtualBackgroundMaskSync:` on or off makes no difference—it only takes effect after you increase the inference interval.
</Note>

### Performance cost

Starting with `3.1.1`, person segmentation always runs CPU inference and no longer uses CoreML. The model is only 256×256, and its operators can't be fully handled by CoreML, so the cost of shuttling data between the CPU and CoreML on every frame exceeds the compute saved—in testing, it's a net slowdown.

Measured on iPhone XS Max / iOS 18.7.9 (720p@25fps capture, average over 300 frames, `inferenceInterval` at the default `1`):

| **Metric** | **3.1.0** | **3.1.1** |
| --- | :---: | :---: |
| Total per-frame time | 53.17 ms | 20.61 ms |
| Of which person segmentation inference | 41.66 ms | 6.06 ms |
| `installVirtualBackground:` time | 1271 ms | 130 ms |
| Process CPU usage | 172% | 63% |
| Memory usage | 83 MB | 58.6 MB |

On `3.1.0`, 53 ms per frame already exceeds the 40 ms budget for 25 fps and drags the encoder into dropping frames; on `3.1.1`, running segmentation on every frame by default is enough for 25 fps on this device, so you usually don't need to increase `inferenceInterval`. For lower-end devices, we still recommend testing as in the previous section before deciding.

### Step 5: **Uninstall the virtual background component**

Uninstall it when no longer in use to release the inference session and related buffers.

```objectivec
/// Uninstall the virtual background component
[[RTCEngineKit sharedEngine] uninstallVirtualBackground];
```

It's uninstalled automatically when the engine is destroyed, so you don't need to call this again.

### Use with beauty filters

The two are installed and switched on or off independently, and you can turn on just one of them. When both are on, the processing order is fixed: beauty filter first, then virtual background.

```objectivec
/// Beauty filter: requires a license key
[[RTCEngineKit sharedEngine] installRenderModule:g_auth_package authDataSize:sizeof(g_auth_package) logLevel:RTCEngineLogLevelError];
/// Virtual background: no license key required
[[RTCEngineKit sharedEngine] installVirtualBackground:nil];
[[RTCEngineKit sharedEngine] enabledVirtualBackground:YES];
```

When either beauty filter or virtual background is on, the local preview shows the processed video; when both are off, the local preview goes back to the raw camera video. For beauty filter APIs, see [Beauty filter](/en/rtc/ios/advanced/beauty).
