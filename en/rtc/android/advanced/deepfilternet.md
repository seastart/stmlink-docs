---
title: "AI noise suppression (DeepFilterNet)"
description: "Enable AI noise suppression with adjustable strength on the microphone with the optional cn.seastart.rtc:denoise plugin: adding the dependency, on/off and strength control, handling unsupported devices and CPU overload, and using a custom AudioCaptureProcessor."
---

`cn.seastart.rtc:denoise` is an AI noise suppression plugin based on [DeepFilterNet3](https://github.com/Rikorose/DeepFilterNet). It uses the same algorithm, model, and parameters as the Web [DeepFilterNet noise suppression plugin](/en/rtc/web/advanced/deepfilternet), so it sounds the same on every platform. It implements the SDK's `AudioCaptureProcessor` interface and takes effect once attached with `RTCEngine.setAudioCaptureProcessor`, with **suppression strength adjustable at runtime** and a **temporary bypass**.

The plugin is a separate, optional dependency, available since RTC `2.0.39`. Apps that don't use AI noise suppression don't need it.

## 1. Add the dependency

```groovy
dependencies {
    implementation 'cn.seastart.rtc:rtc:2.0.39'
    implementation 'cn.seastart.rtc:denoise:0.1.0'
}
```

- The plugin depends transitively on `cn.seastart.rtc:rtc` and requires RTC `2.0.39` or later.
- The plugin supports `arm64-v8a` and `armeabi-v7a`, the same as the SDK.
- The model is built into the plugin; you don't need to copy any extra resources.

## 2. Enable and disable

```kotlin
import cn.seastart.rtc.denoise.DeepFilterNetProcessor
import cn.seastart.rtc.denoise.DenoiseNotSupportedException

private var denoiser: DeepFilterNetProcessor? = null

fun enableDenoise(context: Context, rtcEngine: RTCEngine) {
    // 1. Hide the noise suppression switch on unsupported devices
    if (!DeepFilterNetProcessor.isSupported()) return
    try {
        // 2. Create the plugin; strength 0–100, default 50
        val processor = DeepFilterNetProcessor(context, suppressionLevel = 50)
        // 3. If the CPU can't keep up during a call, the plugin pauses suppression and calls back on the main thread
        processor.overloadListener = DeepFilterNetProcessor.OverloadListener {
            showToast("Device too slow; AI noise suppression paused")
        }
        // 4. Takes effect as soon as it's attached, before or after joining; Engine-level, applies to all channels
        rtcEngine.setAudioCaptureProcessor(processor)
        denoiser = processor
    } catch (e: DenoiseNotSupportedException) {
        // Device not supported: e.code == RtcErrorCode.FEATURE_NOT_SUPPORTED (102032)
    }
}

fun disableDenoise(rtcEngine: RTCEngine) {
    rtcEngine.setAudioCaptureProcessor(null)   // Detach and restore the system's and SDK's built-in noise suppression
    denoiser = null
}
```

Adjust the strength or bypass temporarily at runtime without detaching:

```kotlin
denoiser?.setSuppressionLevel(80)  // 0–100; higher suppresses more
denoiser?.setEnabled(false)        // Bypass: audio passes through unchanged while the processor stays attached
denoiser?.setEnabled(true)         // Resume suppression and clear a pause caused by CPU overload
```

## 3. API

| API | Description |
| --- | --- |
| `DeepFilterNetProcessor.isSupported(): Boolean` | Static method: whether the current device is supported. Check it before enabling, and hide the switch when unsupported |
| `DeepFilterNetProcessor(context, suppressionLevel = 50)` | Creates the plugin; `suppressionLevel` is the strength, 0–100. Throws `DenoiseNotSupportedException` on unsupported devices |
| `setSuppressionLevel(value: Int)` | Adjusts the strength (0–100) at runtime |
| `setEnabled(value: Boolean)` | Turns suppression on or off. With `false`, audio passes through unchanged; `true` resumes suppression and clears a pause caused by CPU overload |
| `suppressionLevel: Int` | Current strength, read-only |
| `isEnabled: Boolean` | Current on/off state, read-only. An automatic overload pause doesn't change it |
| `overloadListener: OverloadListener?` | Called when the CPU can't keep up during a call and suppression has been paused automatically. Runs on the main thread, once per pause |
| `DenoiseNotSupportedException.code` | Always `RtcErrorCode.FEATURE_NOT_SUPPORTED` (`102032`) |

## 4. Unsupported devices and CPU overload

AI noise suppression needs a certain amount of CPU power. The SDK handles this in two layers:

- **Before enabling**: only devices with low-performance little cores (common in some TVs, set-top boxes, and entry-level phones) are unsupported. On them `isSupported()` returns `false` and the constructor throws `DenoiseNotSupportedException` (`102032`). Check first and only then show the switch, rather than reporting an error after the user taps it.
- **During a call**: if the device stays overloaded (for example, while running other heavy workloads), the plugin switches to bypass automatically so the call doesn't stutter, and calls `overloadListener`. Tell the user something like "Device too slow; noise suppression paused" and let them decide whether to call `setEnabled(true)` to turn it back on.

## 5. Notes

- **When attached, the SDK turns off the system's and WebRTC's built-in noise suppression** and restores it on detach, so two layers of suppression don't stack and muffle the voice. Echo cancellation and automatic gain control are unaffected. This switch rebuilds microphone capture once, leaving a gap of less than half a second. To turn suppression off temporarily, use `setEnabled(false)`, which doesn't rebuild capture.
- The model loads in the background (usually in under 1 second). Until it's loaded, audio passes through unchanged and capture isn't blocked.
- It works only with 48 kHz mono capture; other capture formats pass through unchanged.
- Local volume (`getVolume`, speaker levels) reflects the volume before noise suppression.
- `setAudioCaptureProcessor` holds only one processor, applied to all channels; `releaseSDK()` doesn't clear it.
- License: DeepFilterNet itself is Apache-2.0/MIT; verify the license of the model weights yourself before distribution.

## 6. Custom capture processors

The `AudioCaptureProcessor` interface the plugin implements can also be used to plug in your own audio algorithms (noise suppression, voice changing, and so on). The processor processes each PCM frame in place on the SDK capture thread; the processed data is then distributed to all channels, and the local audio frame callback also receives the processed data.

```kotlin
class MyProcessor : AudioCaptureProcessor {
    // Optional: require built-in noise suppression off; return null to leave it unchanged
    override val audioProcessing = AudioProcessingConstraints(noiseSuppression = false)

    override fun initialize(sampleRate: Int, channelCount: Int) {
        // Called when the capture format is determined (including rebuilds after device switches or route changes); return quickly
    }

    override fun process(data: ByteArray, offset: Int, length: Int) {
        // Process data[offset, offset + length) in place: 16-bit little-endian PCM, 48 kHz mono 10 ms (960 bytes) by default
        // Called every 10 ms and must return within a few milliseconds; the buffer is reused after return, so don't keep data
    }

    override fun release() {
        // Called when the processor is replaced or cleared; process isn't called afterward
    }
}

rtcEngine.setAudioCaptureProcessor(MyProcessor())
```

- Exceptions thrown from `process` are caught and logged by the SDK, and that frame is sent unchanged.
- `AudioProcessingConstraints` has the same meaning as the same-named type in the Web and Swift SDKs. Android currently handles only `noiseSuppression`; `echoCancellation` and `autoGainControl` keep the SDK defaults.
- For interface details, see [RTCEngine.setAudioCaptureProcessor](/en/rtc/android/api-reference/RTCEngine#setaudiocaptureprocessor-processor) and [Types](/en/rtc/android/types#audiocaptureprocessor).
