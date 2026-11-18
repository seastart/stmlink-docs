---
title: "AI noise suppression (DeepFilterNet)"
description: "Turn on AI noise suppression for the microphone in meetings: add the cn.seastart.rtc:denoise plugin, attach it with MeetingEngine.setAudioCaptureProcessor, and handle unsupported devices, CPU overload, and custom capture processors"
---

The meeting layer attaches microphone capture processors through `MeetingEngine.setAudioCaptureProcessor`, available since `2.0.43`. The most common use is attaching the SRTC AI noise suppression plugin `cn.seastart.rtc:denoise`. It is based on DeepFilterNet3, uses the same algorithm and model as the Web and iOS SDKs, and lets you adjust the suppression strength and bypass it at runtime.

The plugin is a separate, optional dependency; apps that don't use AI noise suppression don't need it. For the plugin's own API, strength, overload handling, and device checks, see the SRTC page [AI noise suppression (DeepFilterNet)](/en/rtc/android/advanced/deepfilternet). This page only covers how to wire it into a meeting.

## 1. Add the dependency

```groovy
dependencies {
    implementation 'cn.seastart.meeting:meeting:2.0.43'
    implementation 'cn.seastart.rtc:denoise:0.1.0'
}
```

- Meeting `2.0.43` transitively depends on RTC `2.0.39`, and the plugin requires RTC `2.0.39` or later, so the two versions match.
- The plugin supports `arm64-v8a` and `armeabi-v7a`. The model is bundled, so you don't need to copy any extra assets.

## 2. Enable and disable

```kotlin
import cn.seastart.rtc.denoise.DeepFilterNetProcessor
import cn.seastart.rtc.denoise.DenoiseNotSupportedException

private var denoiser: DeepFilterNetProcessor? = null

fun enableDenoise(context: Context, meetingEngine: MeetingEngine) {
    // 1. Hide the noise suppression switch on unsupported devices
    if (!DeepFilterNetProcessor.isSupported()) return
    try {
        // 2. Create the plugin; strength 0–100, default 50
        val processor = DeepFilterNetProcessor(context, suppressionLevel = 50)
        // 3. If the CPU can't keep up, the plugin pauses noise suppression and calls back on the main thread
        processor.overloadListener = DeepFilterNetProcessor.OverloadListener {
            showToast("Device too slow, AI noise suppression paused")
        }
        // 4. Takes effect immediately; can be called before or after initSdk, in or out of a meeting
        meetingEngine.setAudioCaptureProcessor(processor)
        denoiser = processor
    } catch (e: DenoiseNotSupportedException) {
        // Device not supported: e.code == 102032
    }
}

fun disableDenoise(meetingEngine: MeetingEngine) {
    meetingEngine.setAudioCaptureProcessor(null)   // Detach and restore the built-in noise suppression of the system and SDK
    denoiser = null
}
```

To adjust the strength or bypass temporarily, call the plugin directly; no need to attach it again:

```kotlin
denoiser?.setSuppressionLevel(80)  // 0–100; higher means stronger suppression
denoiser?.setEnabled(false)        // Bypass: audio passes through unchanged, processor stays attached
denoiser?.setEnabled(true)         // Resume noise suppression and clear any pause caused by CPU overload
```

## 3. Meeting-layer behavior

- **The setting persists**: once attached, it applies to all later meetings. After `release()` and another `initSdk()`, the SDK attaches it again automatically, so you don't need to set it again. Pass `null` when you no longer need it.
- **The SDK holds a strong reference**: when you replace it or clear it with `null`, the SDK calls `release()` on the old processor, and the old instance can't be used again. Create a new one to turn it back on.
- **Attaching turns off the built-in noise suppression of the system and WebRTC**, and detaching restores it, so the two don't stack and muffle voices. Echo cancellation and automatic gain control are not affected. Switching restarts microphone capture once, leaving a gap of under half a second. To turn noise suppression off temporarily, use the plugin's `setEnabled(false)`, which doesn't restart capture.
- The local volume (speaker level) reflects the volume before noise suppression.

## 4. Unsupported devices and CPU overload

- **Before enabling**: only devices with low-performance little cores (common on some TVs, set-top boxes, and entry-level phones) are unsupported. `isSupported()` returns `false`, and the constructor throws `DenoiseNotSupportedException` (`102032`). Check first, then show the switch.
- **While running**: when the device stays overloaded, the plugin switches to bypass automatically to keep the call smooth and calls `overloadListener`. Let the user know and let them decide whether to call `setEnabled(true)` to turn it back on.

## 5. Custom capture processors

`setAudioCaptureProcessor` accepts any processor that implements the RTC `AudioCaptureProcessor` interface, such as a voice changer or your own noise suppression. For the interface contract, see the SRTC section [Custom capture processors](/en/rtc/android/advanced/deepfilternet#6-custom-capture-processors). Only one processor can be attached at a time.
