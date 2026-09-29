---
title: "Audio routing"
description: "Manage Android audio output among speaker, earpiece, wired headsets, and Bluetooth headsets with AudioRouterManager: initialization order, setMode, auto-switch priorities, device callbacks, manual switching, and release. Read when your app controls or displays the output device."
---

`AudioRouterManager` manages audio routing among the speaker / earpiece / wired headset / Bluetooth headset in scenarios such as calls, conferencing, and voice chat.

## 1. Get `AudioRouterManager`

```kotlin
// Get the audio routing manager through rtcEngine
var audioRouterManager = rtcEngine.getAudioRouterManager()
```

`rtcEngine.getAudioRouterManager()` returns a singleton. The corresponding release method is:

```kotlin
rtcEngine.releaseAudioRouterManager()
audioRouterManager = null
```

---

## 2. Recommended initialization order

We recommend initializing in the following order when joining a channel / starting a call:

1. Get `AudioRouterManager`
2. Set the callback listener
3. Set the audio mode with `setMode(...)`
4. Set the auto-switch policy with `setAutoChangeAudioRouter(...)`
5. Call `init()` to start route monitoring

Full example:

```kotlin
// Imports omitted; the example assumes the relevant types are available

private var audioRouterManager: AudioRouterManager? = null

private fun initAudioRouterManager() {
    audioRouterManager = rtcEngine.getAudioRouterManager()

    // Note: the API name is setAudioRouterCalllback (Calllback has 3 l's)
    audioRouterManager?.setAudioRouterCalllback(object : AudioRouterCallback {
        override fun exitOutputDeviceChange(
            audioOutputDevices: HashMap<AudioRouterManager.AudioOutputDeviceType, AudioDeviceInfo?>
        ) {
            // The set of available output devices changed
            // For example: wired headset plugged in, Bluetooth headset connected, headset unplugged
        }

        override fun activeOutputDeviceChange(
            audioOutputDevice: Pair<AudioRouterManager.AudioOutputDeviceType, AudioDeviceInfo?>
        ) {
            // The output device actually in use changed
            // audioOutputDevice.first  is the device type
            // audioOutputDevice.second is the device info (available on Android 6.0+)
        }

        override fun onAudioBecomingNoisy() {
            // The system may produce noise after a route switch
            // For example, you can pause playback or lower the volume here
        }
    })

    // Set the mode again based on the scenario every time you switch app scenarios
    audioRouterManager?.setMode(AudioManager.MODE_IN_COMMUNICATION)

    // Enable auto-switching: speaker has priority over earpiece; Bluetooth headset has priority over wired headset
    audioRouterManager?.setAutoChangeAudioRouter(
        true,
        true,
        false
    )

    // Start route monitoring
    audioRouterManager?.init()
}
```

---

## 3. Using `setMode`

```kotlin
audioRouterManager?.setMode(AudioManager.MODE_IN_COMMUNICATION)
```

Supported modes are defined by `AudioManager`. Common values include:

- `AudioManager.MODE_NORMAL`
- `AudioManager.MODE_RINGTONE`
- `AudioManager.MODE_IN_CALL`
- `AudioManager.MODE_IN_COMMUNICATION`
- `AudioManager.MODE_CALL_SCREENING`
- `AudioManager.MODE_CALL_REDIRECT`
- `AudioManager.MODE_COMMUNICATION_REDIRECT`

### Notes

- The SDK requires `minSdk = 24`, so it actually takes the Android 6.0+ path.
- In the 6.0+ implementation, `init()` **doesn't set the audio mode automatically**; you must call `setMode(...)` yourself.
- We therefore recommend **setting the mode again before every scenario switch**, for example when switching between voice chat, conferencing, and media playback.

---

## 4. Auto-switch policy with `setAutoChangeAudioRouter`

### 4.1 Simple usage

```kotlin
audioRouterManager?.setAutoChangeAudioRouter(true)
```

Equivalent to:

```kotlin
audioRouterManager?.setAutoChangeAudioRouter(
    true,
    false,
    false
)
```

That is:

- Auto-switching is enabled
- **Earpiece has priority over speaker**
- **Bluetooth headset has priority over wired headset**

### 4.2 Full usage

```kotlin
audioRouterManager?.setAutoChangeAudioRouter(
    isAutoChange = true,
    isPrioritySpeaker = true,
    isPriorityWiredEarphone = false
)
```

Parameters:

- `isAutoChange`
  - `true`: audio routing is switched automatically internally
  - `false`: only monitor device changes without auto-switching; you call `switchAudioRouter(...)` manually
- `isPrioritySpeaker`
  - `true`: speaker has priority over earpiece
  - `false`: earpiece has priority over speaker
- `isPriorityWiredEarphone`
  - `true`: wired headset has priority over Bluetooth headset
  - `false`: Bluetooth headset has priority over wired headset

### 4.3 Auto-switch rules (based on the implementation)

Auto-switching generally follows these rules:

1. A newly connected device usually triggers a new route selection.
2. Category priority: **Bluetooth headset / wired headset > earpiece / speaker**.
3. Priority within a group can be customized with parameters:
   - Bluetooth headset vs. wired headset: controlled by `isPriorityWiredEarphone`
   - Earpiece vs. speaker: controlled by `isPrioritySpeaker`
4. When a device is removed, an available route is reselected from the remaining devices.

For example:

- Both a Bluetooth headset and a wired headset are present:
  - With `isPriorityWiredEarphone = false`, the Bluetooth headset is preferred
  - With `isPriorityWiredEarphone = true`, the wired headset is preferred
- No headset-type device is present:
  - With `isPrioritySpeaker = false`, the earpiece is preferred
  - With `isPrioritySpeaker = true`, the speaker is preferred

---

## 5. Callbacks

### 5.1 Available output devices changed

```kotlin
override fun exitOutputDeviceChange(
    audioOutputDevices: HashMap<AudioRouterManager.AudioOutputDeviceType, AudioDeviceInfo?>
) {
}
```

Indicates that the list of currently "selectable" audio output devices changed, for example:

- A Bluetooth headset connects / disconnects
- A wired headset is plugged in / unplugged
- The system's available output devices change

Available device types come from `AudioOutputDeviceType`:

- `SPEAKER`: speaker
- `EARPIECE`: earpiece
- `WIRED_EARPHONE`: wired headset
- `BLUETOOTH_HEADSET`: Bluetooth headset
- `UN_KNOW`: unknown / placeholder for automatic selection

> The SDK requires `minSdk = 24`, so `AudioDeviceInfo` here is usually available; it's declared nullable only for compatibility with lower versions.

### 5.2 Active output device changed

```kotlin
override fun activeOutputDeviceChange(
    audioOutputDevice: Pair<AudioRouterManager.AudioOutputDeviceType, AudioDeviceInfo?>
) {
}
```

Indicates that the output device actually in use changed. The "current speaker / Bluetooth / earpiece" state in your UI should usually be based on this callback.

### 5.3 Route change may produce noise

```kotlin
override fun onAudioBecomingNoisy() {
}
```

For example, when a headset is unplugged or A2DP disconnects, the system may switch to the loudspeaker. You can add safeguards here:

- Pause the player
- Lower the volume
- Show a prompt to the user

---

## 6. Get available devices and the active device

### 6.1 Get available output devices

```kotlin
val devices = audioRouterManager?.getExitAudioOutputDevices()
devices?.forEach { (type, info) ->
    val name = info?.productName?.toString() ?: type.name
}
```

### 6.2 Get the active output device

```kotlin
val activeDevice = audioRouterManager?.getActiveAudioOutputDevice()
val activeType = activeDevice?.first
val activeInfo = activeDevice?.second
```

### 6.3 Correct the Bluetooth name (optional)

On some devices, the Bluetooth name returned by `AudioDeviceInfo.getProductName()` may be inaccurate. In that case, use:

```kotlin
if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M) {
    AudioRouterManager.getValidBluetoothName(
        curName = activeInfo?.productName?.toString().orEmpty(),
        context = this
    ) { validName ->
        // validName is the corrected Bluetooth name
    }
}
```

> To get a more accurate Bluetooth device name, make sure the Bluetooth permissions are granted; on Android 12 and later, pay attention to the `BLUETOOTH_CONNECT` permission.

---

## 7. Switch routes manually

In most cases, this step is triggered by the user tapping a UI button.

```kotlin
audioRouterManager?.switchAudioRouter(selectType)
```

`selectType` is an `AudioOutputDeviceType` enum value, for example:

```kotlin
audioRouterManager?.switchAudioRouter(AudioRouterManager.AudioOutputDeviceType.SPEAKER)
audioRouterManager?.switchAudioRouter(AudioRouterManager.AudioOutputDeviceType.EARPIECE)
audioRouterManager?.switchAudioRouter(AudioRouterManager.AudioOutputDeviceType.WIRED_EARPHONE)
audioRouterManager?.switchAudioRouter(AudioRouterManager.AudioOutputDeviceType.BLUETOOTH_HEADSET)
```

### Special value: `UN_KNOW`

```kotlin
audioRouterManager?.switchAudioRouter(AudioRouterManager.AudioOutputDeviceType.UN_KNOW)
```

Passing `UN_KNOW` doesn't mean switching to an "unknown device"; it means: **reselect the most suitable route according to the current auto-selection policy**.

Suitable for:

- The user taps "Restore the system-recommended route"
- After plugging or unplugging a device, explicitly asking the SDK to recalculate the best device

---

## 8. Release resources

We recommend releasing through `rtcEngine`:

```kotlin
rtcEngine.releaseAudioRouterManager()
audioRouterManager = null
```

`releaseAudioRouterManager()` is internally equivalent to calling:

```kotlin
audioRouterManager.release(true)
```

This means release performs the following:

- Stops audio route monitoring
- Unregisters related broadcasts / callbacks
- Restores the audio mode to `AudioManager.MODE_NORMAL`
- Switches output back to the speaker

If you call directly:

```kotlin
audioRouterManager?.release(false)
```

Release then **doesn't restore the mode**.

---

## 9. Common device enums

```kotlin
AudioRouterManager.AudioOutputDeviceType.UN_KNOW
AudioRouterManager.AudioOutputDeviceType.SPEAKER
AudioRouterManager.AudioOutputDeviceType.EARPIECE
AudioRouterManager.AudioOutputDeviceType.WIRED_EARPHONE
AudioRouterManager.AudioOutputDeviceType.BLUETOOTH_HEADSET
```

Meanings:

- `UN_KNOW`: unknown / triggers automatic selection
- `SPEAKER`: speaker
- `EARPIECE`: earpiece
- `WIRED_EARPHONE`: wired headset
- `BLUETOOTH_HEADSET`: Bluetooth headset

---

## 10. Recommended practices

1. **Initialize when joining a channel and release when leaving**; don't recreate it on every button tap.
2. **Call `setMode(...)` every time you switch app scenarios**.
3. When the UI shows "which device is currently in use", rely on `activeOutputDeviceChange(...)` first.
4. When showing "which devices the user can choose", rely on `exitOutputDeviceChange(...)` or `getExitAudioOutputDevices()`.
5. When using Bluetooth devices, verify on a real device:
   - Connecting a Bluetooth headset
   - Disconnecting a Bluetooth headset
   - Plugging in / unplugging a wired headset
   - Manually switching among speaker / earpiece / Bluetooth
6. If your app has multiple audio playback/call states at the same time, focus on verifying actual behavior when switching between devices.

---

## 11. Complete initialization example

Initialize in the following order when entering the call screen:

```kotlin
audioRouterManager = rtcEngine.getAudioRouterManager()
audioRouterManager?.setAudioRouterCalllback(/* callback */)
audioRouterManager?.setMode(AudioManager.MODE_IN_COMMUNICATION)
audioRouterManager?.setAutoChangeAudioRouter(true, true, false)
audioRouterManager?.init()
```

You can use this directly as a reference for conferencing scenarios.
