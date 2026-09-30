---
title: "Virtual background"
description: "Virtual background in the SMeeting iOS (Objective-C) SDK: person segmentation for background blur or replacement, no license key needed. Covers why it's a device-level setting, why camera switches and reconnects need no re-apply, and two frame-rate parameters for low-end devices."
---

Virtual background performs person segmentation in the camera capture pipeline and replaces everything outside the person with blur or a specified image. It's an in-house component, and installing it doesn't require a license key.

<Note>
The APIs are on the global singleton `MeetingKit`, not on `MeetingKitRoom`—virtual background applies to the single shared camera capture pipeline in the process, so it's **a device-level setting that applies to all rooms at once**. When you're in multiple rooms at the same time, there's no way to "turn on virtual background for just one room."

Switching cameras during the meeting (`switchCamera`) and reconnecting after a disconnect both rebuild the capture pipeline, and the SDK automatically replays the whole current configuration, so **you don't need to re-apply anything at these points**.
</Note>

<Warning>
Starting with `2.1.0`, the minimum system requirement is **iOS 16.0**. Virtual background depends on `onnxruntime`; with CocoaPods, it's pulled in transitively by the `RTCEngineKit` podspec, so you don't need to declare it in your `Podfile`. For details, see [Quickstart](/en/meeting/ios/quickstart).
</Warning>

### Step 1: **Install the virtual background component**

We recommend installing it before you need virtual background, for example when entering the meeting page. Pass `nil` for `modelPath` to use the SDK's built-in person segmentation model.

```objectivec
/// Install the virtual background component
/// @param modelPath Path to the person segmentation model file; pass nil to use the built-in model
SEAError error = [[MeetingKit sharedInstance] installVirtualBackground:nil];
```

Return values:

| **Return value** | **Description** |
| --- | --- |
| SEAErrorOK | Installed successfully |
| SEAErrorConflict | The component is already installed; this call is discarded |
| SEAErrorNotFound | The model file doesn't exist; check `modelPath` |
| SEAErrorSystemError | Failed to create the inference session; this is a runtime environment problem |

### Step 2: **Set the background effect**

Background blur and background replacement are **mutually exclusive; the later call wins**. Both APIs are remembered even if called before installation and take effect automatically once installation completes, so you don't need to care about their order relative to `installVirtualBackground:`.

```objectivec
/// Set background blur
/// @param level Blur level, range 1–10, default 5 (out-of-range values are clamped to the boundary)
[[MeetingKit sharedInstance] setVirtualBackgroundBlur:5];

/// Set background replacement
/// @param image Background image, cropped to cover without stretching; pass nil to cancel replacement and go back to blur
[[MeetingKit sharedInstance] setVirtualBackgroundImage:[UIImage imageNamed:@"background"]];
```

### Step 3: **Turn virtual background on or off**

After installation, it's **off** by default and must be turned on explicitly. When off, frames pass straight through with zero overhead, and no inference runs.

```objectivec
/// Virtual background switch
/// @param enabled YES: on, NO: off
[[MeetingKit sharedInstance] enabledVirtualBackground:YES];

/// Get whether virtual background is on
BOOL enabled = [[MeetingKit sharedInstance] isVirtualBackgroundEnabled];
```

Calling the switch before the component is installed returns `SEAErrorConflict`. Turning it off clears the inter-frame state, so the next time it's turned on it converges again from the first frame and doesn't flash a stale mask.

### Step 4: **Keep the frame rate up on low-end devices (optional)**

By default, person segmentation runs on every frame. On low-end devices, you can increase the inference interval, trading mask reuse for frame rate; then turn on mask sync as needed to eliminate trailing artifacts.

```objectivec
/// Set the segmentation inference interval
/// @param interval Run segmentation every N frames (compositing still runs every frame); default 1
[[MeetingKit sharedInstance] setVirtualBackgroundInferenceInterval:2];

/// Set mask sync
/// @param enabled YES: on, NO: off; default NO
[[MeetingKit sharedInstance] setVirtualBackgroundMaskSync:YES];
```

| **Parameter** | **Default** | **Description** |
| --- | :---: | --- |
| inferenceInterval | `1` | Run segmentation every N frames; values below 1 are treated as 1. Increasing it lowers inference overhead, at the cost of the mask following more slowly during fast motion |
| maskSync | `NO` | When on, non-inference frames aren't recomposited, so the video and the mask always come from the same moment, eliminating misaligned trails when waving; the cost is that the video update rate drops to the mask rate |

<Note>
When `inferenceInterval` is `1`, turning `setVirtualBackgroundMaskSync:` on or off makes no difference at all—it only takes effect after you increase the inference interval.
</Note>

### Step 5: **Uninstall the virtual background component**

Uninstall it when no longer needed to release the inference session and related buffers.

```objectivec
/// Uninstall the virtual background component
[[MeetingKit sharedInstance] uninstallVirtualBackground];
```

### Consistency between local preview and the published stream

When virtual background is on, the local preview shows the processed video, which is the same data other members see; when it's off, the local preview goes back to the raw camera video. For full signatures and parameters, see [MeetingKit](/en/meeting/ios/api-reference/MeetingKit#virtual-background-apis).
