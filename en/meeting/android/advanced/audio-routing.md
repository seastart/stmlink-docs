---
title: "Audio routing"
description: "Manage audio output routing (speaker, earpiece, wired headset, Bluetooth headset) in the SMeeting Android SDK: get AudioRouterManager from MeetingEngine, set the mode and auto-switch policy, handle device callbacks, switch routes manually, and release it."
---

Audio routing is managed by `AudioRouterManager`, and it behaves the same as in SRTC. In SMeeting you get and release it through `MeetingEngine`:

```kotlin
var audioRouterManager = meetingEngine.getAudioRouterManager()

meetingEngine.releaseAudioRouterManager()
audioRouterManager = null
```

The `AudioRouterManager` type itself still comes from the RTC package: `cn.seastart.rtc.media.audioRouter.AudioRouterManager`.

---

## 1. Get `AudioRouterManager`

In SMeeting, get it through the current `MeetingEngine`:

```kotlin
var audioRouterManager = meetingEngine.getAudioRouterManager()
```

The corresponding release call:

```kotlin
meetingEngine.releaseAudioRouterManager()
audioRouterManager = null
```

### Notes

- `getAudioRouterManager()` returns a nullable type; handle null in your app.
- In the current `meetingSDK` implementation, this method passes through to the underlying RTC engine.
- We recommend holding it in one place on the **meeting screen / call screen**, rather than getting and initializing it again on every button tap.

---

## 2. Recommended initialization order

Based on the `meetingSDK` demo, we recommend initializing in the following order after entering the meeting screen:

1. Get the manager with `meetingEngine.getAudioRouterManager()`
2. Set the callback listener with `setAudioRouterCalllback(...)`
3. Set the audio mode with `setMode(...)`
4. Set the auto-switch policy with `setAutoChangeAudioRouter(...)`
5. Call `init()` to start route monitoring

Full example:

```kotlin
// Imports are omitted in the following example

private var audioRouterManager: AudioRouterManager? = null

private fun initAudioRouterManager(meetingEngine: MeetingEngine) {
    audioRouterManager = meetingEngine.getAudioRouterManager()

    // Note: the API name is setAudioRouterCalllback (Calllback has 3 l's)
    audioRouterManager?.setAudioRouterCalllback(object :
        AudioRouterManager.AudioRouterCallback {

        override fun exitOutputDeviceChange(
            audioOutputDevices: HashMap<AudioRouterManager.AudioOutputDeviceType?, AudioDeviceInfo?>
        ) {
            // The list of currently available output devices changed
            // For example: a wired headset was plugged in, a Bluetooth headset connected, a headset was unplugged
        }

        override fun activeOutputDeviceChange(
            audioOutputDevice: Pair<AudioRouterManager.AudioOutputDeviceType, AudioDeviceInfo?>
        ) {
            // The output device actually in effect changed
        }

        override fun onAudioBecomingNoisy() {
            // When a headset disconnects and similar, the system may switch to the speaker
        }
    })

    // The demo's meeting scenario currently uses MODE_IN_COMMUNICATION
    audioRouterManager?.setMode(AudioManager.MODE_IN_COMMUNICATION)

    // The demo's actual policy: speaker over earpiece; Bluetooth over wired headset
    audioRouterManager?.setAutoChangeAudioRouter(true, true, false)

    // Start route monitoring
    audioRouterManager?.init()
}
```

This matches the current implementation in the demo's `MeetingActivity.kt`:

```kotlin
audioRouterManager = MeetingEngineHelper.getInstance().session.getAudioRouterManager()
audioRouterManager?.setAudioRouterCalllback(/* callback */)
audioRouterManager?.setMode(AudioManager.MODE_IN_COMMUNICATION)
audioRouterManager?.setAutoChangeAudioRouter(true, true, false)
audioRouterManager?.init()
```

---

## 3. Using `setMode`

Recommended for meeting / call scenarios:

```kotlin
audioRouterManager?.setMode(AudioManager.MODE_IN_COMMUNICATION)
```

For the common modes, refer to `AudioManager`, for example:

- `AudioManager.MODE_NORMAL`
- `AudioManager.MODE_RINGTONE`
- `AudioManager.MODE_IN_CALL`
- `AudioManager.MODE_IN_COMMUNICATION`

### Notes

- The current project's `minSdk = 24`.
- In the current integration, we recommend that your app **set the mode explicitly** rather than rely on the default.
- If your app has different audio scenarios such as meetings, playback, and voice chat, we recommend calling `setMode(...)` again when switching scenarios.

---

## 4. `setAutoChangeAudioRouter` auto-switch policy

### 4.1 Basic usage

```kotlin
audioRouterManager?.setAutoChangeAudioRouter(true)
```

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
  - `true`: the route is switched automatically internally
  - `false`: device changes are only monitored; your app switches manually
- `isPrioritySpeaker`
  - `true`: the speaker has higher priority than the earpiece
  - `false`: the earpiece has higher priority than the speaker
- `isPriorityWiredEarphone`
  - `true`: a wired headset has higher priority than a Bluetooth headset
  - `false`: a Bluetooth headset has higher priority than a wired headset

### 4.3 Policy used in the current demo

`MeetingActivity.kt` uses:

```kotlin
audioRouterManager?.setAutoChangeAudioRouter(true, true, false)
```

This means:

- Auto-switching is on
- The speaker takes priority over the earpiece
- A Bluetooth headset takes priority over a wired headset

This suits meeting scenarios that play audio out loud.

---

## 5. Callbacks

### 5.1 Available output devices changed

```kotlin
override fun exitOutputDeviceChange(
    audioOutputDevices: HashMap<AudioRouterManager.AudioOutputDeviceType?, AudioDeviceInfo?>
) {
}
```

Indicates that the current "list of selectable devices" has changed, for example:

- A Bluetooth headset connected / disconnected
- A wired headset was plugged in / unplugged
- The system's output device capabilities changed

### 5.2 Active output device changed

```kotlin
override fun activeOutputDeviceChange(
    audioOutputDevice: Pair<AudioRouterManager.AudioOutputDeviceType, AudioDeviceInfo?>
) {
}
```

Indicates that the audio output device actually in effect has changed.

If your UI shows "currently using the speaker / earpiece / Bluetooth headset," we recommend relying on this callback first.

### 5.3 A route change may cause noise

```kotlin
override fun onAudioBecomingNoisy() {
}
```

Typical scenarios:

- A headset was unplugged
- A Bluetooth headset disconnected
- The system automatically switched from the headset to the speaker

At this point you can apply some safeguards in your app, such as:

- Lowering the volume
- Pausing playback
- Notifying the user

---

## 6. Get the available devices and the active device

### 6.1 Get the currently available output devices

```kotlin
val devices = audioRouterManager?.getExitAudioOutputDevices()
devices?.forEach { (type, info) ->
    val name = info?.productName?.toString() ?: type?.name.orEmpty()
}
```

### 6.2 Get the currently active output device

```kotlin
val activeDevice = audioRouterManager?.getActiveAudioOutputDevice()
val activeType = activeDevice?.first
val activeInfo = activeDevice?.second
```

### 6.3 Correct the Bluetooth name (optional)

```kotlin
AudioRouterManager.getValidBluetoothName(
    curName = activeInfo?.productName?.toString().orEmpty(),
    context = this
) { validName ->
    // validName is the corrected Bluetooth name
}
```

> To get a more accurate Bluetooth name, handle Bluetooth permissions according to the OS version; on Android 12 and later you usually need to take care of `BLUETOOTH_CONNECT`.

---

## 7. Switch routes manually

Your app can switch actively when the user taps the UI:

```kotlin
audioRouterManager?.switchAudioRouter(selectType)
```

Here `selectType` is an `AudioOutputDeviceType`, for example:

```kotlin
audioRouterManager?.switchAudioRouter(AudioRouterManager.AudioOutputDeviceType.SPEAKER)
audioRouterManager?.switchAudioRouter(AudioRouterManager.AudioOutputDeviceType.EARPIECE)
audioRouterManager?.switchAudioRouter(AudioRouterManager.AudioOutputDeviceType.WIRED_EARPHONE)
audioRouterManager?.switchAudioRouter(AudioRouterManager.AudioOutputDeviceType.BLUETOOTH_HEADSET)
```

The current demo reads the list of available devices and then shows a dialog for the user to choose from:

```kotlin
val audioOutputDevices = audioRouterManager?.exitAudioOutputDevices
// Build the options from the device list
audioRouterManager?.switchAudioRouter(selectType)
```

### Special value: `UN_KNOW`

```kotlin
audioRouterManager?.switchAudioRouter(AudioRouterManager.AudioOutputDeviceType.UN_KNOW)
```

This doesn't mean switching to an "unknown device"; it means:

**Choose the most suitable output route again according to the current automatic routing policy.**

Suitable for scenarios such as:

- Restoring the default recommended route
- Explicitly asking the SDK to choose a route again after a device is plugged in or unplugged

---

## 8. Release resources

We recommend calling this when the meeting screen exits / is destroyed:

```kotlin
meetingEngine.releaseAudioRouterManager()
audioRouterManager = null
```

What the current demo actually does:

```kotlin
private fun releaseAudioRouterManager() {
    MeetingEngineHelper.getInstance().session.releaseAudioRouterManager()
    audioRouterManager = null
}

override fun onDestroy() {
    super.onDestroy()
    releaseAudioRouterManager()
}
```

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

- `UN_KNOW`: unknown / triggers automatic re-routing
- `SPEAKER`: speaker
- `EARPIECE`: earpiece
- `WIRED_EARPHONE`: wired headset
- `BLUETOOTH_HEADSET`: Bluetooth headset

---

## 10. Recommended practices

1. **Integrate through the APIs exposed by `MeetingEngine`**; don't depend on the underlying `rtcEngine` directly in your app.
2. **Initialize when entering the meeting screen and release when leaving it**, to avoid repeatedly calling `init()` / `release()` from a single button tap.
3. **Set `setMode(...)` again every time you switch your app's audio scenario**.
4. When showing "the device currently in use," rely on `activeOutputDeviceChange(...)`.
5. When showing "the list of currently selectable devices," rely on `exitOutputDeviceChange(...)` or `getExitAudioOutputDevices()`.
6. We recommend fully verifying switching among Bluetooth / wired headset / speaker / earpiece on real devices.
7. `AudioRouterManager` is an Engine-level cached object; callers shouldn't call its `release()` directly—always use `meetingEngine.releaseAudioRouterManager()`.
