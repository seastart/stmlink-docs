---
title: "Audio routing (iOS)"
description: "Control whether meeting audio plays from the speaker or the earpiece on iOS with the SMeeting Swift SDK: the persistent default and temporary override layers, why external devices can't be switched to, and why entering a meeting requests microphone permission. Read when adding a speaker button."
---

### Overview

On iOS, "where the sound comes out" is controlled by a set of audio routing APIs on `SMeetingEngine`, available on iOS only—macOS uses a separate model of input / output hardware devices, through `setAudioOutput(deviceId:)` in [Device management](/en/meeting/swift/advanced/device-management).

These APIs are a thin wrapper around the underlying SRTC `AudioRouteSession` and don't cache state a second time, so the meeting layer and the underlying layer never end up with two drifting copies of the state. The design follows the common practice of mainstream RTC SDKs (Agora, Tencent TRTC, LiveKit). There are three principles you need to understand first; otherwise it's easy to write code that "sets it but it doesn't take effect."

For a full description of the underlying mechanism, see [SRTC · Audio routing](/en/rtc/swift/advanced/audio-routing); this page only covers how to use it at the meeting layer.

---

### Principle 1: you can only switch between the speaker and the earpiece

`AudioRouteTarget` has only two values—`.speaker` (speaker / speakerphone) and `.earpiece` (earpiece).

**The SDK doesn't provide an API to "switch to Bluetooth headphones / a wired headset."** This isn't a missing feature but an iOS platform limitation: the system has no reliable way for an app to specify a particular external device. Agora, TRTC, and LiveKit don't have such APIs either.

External devices behave like this: when plugged in, the system switches to them automatically; when unplugged, the SDK falls back to the route you set. When you need to let the user actively choose Bluetooth / AirPlay, use the system-provided `AVRoutePickerView`.

<Warning>
While Bluetooth headphones or a wired headset are in use, `setAudioRoute(.speaker)` **doesn't take effect**, and audio still comes out of the external device. iOS doesn't allow taking the output back from an external device to the built-in speaker; the SDK doesn't throw in this case and only writes a log. Use `currentAudioRoute` to check the actual result instead of assuming a successful call means the route has switched; when `isExternalAudioRouteActive` is `true`, gray out the "speakerphone" button.
</Warning>

---

### Principle 2: persistent and temporary settings are two separate layers

| Layer | API | When it applies | Corresponding Agora API |
| :--- | :--- | :--- | :--- |
| Persistent | `defaultAudioRoute` | Set before entering the meeting, stays in effect long-term | `setDefaultAudioRouteToSpeakerphone` |
| Temporary | `setAudioRoute(_:)` | Called after entering the meeting | `setEnableSpeakerphone` |

The priority is **temporary > persistent**. After an external device is unplugged, the SDK falls back according to this priority.

```swift
// Before entering the meeting: use the speakerphone by default for meetings
meeting.defaultAudioRoute = .speaker

// During the meeting: the user tapped the earpiece button
meeting.setAudioRoute(.earpiece)

// Drop the temporary choice and go back to defaultAudioRoute
meeting.clearAudioRouteOverride()
```

<Tip>
If you don't need to "let the user switch temporarily during the meeting," **`defaultAudioRoute` alone is enough**. It maps to a category option of `AVAudioSession`, which is Apple's proper way to express "speakerphone by default," and it's much more reliable than overriding once after activation.
</Tip>

Temporary settings get overridden by system behavior (plugging or unplugging external devices, system phone calls, and so on). This is by design, not a bug.

---

### Principle 3: entering a meeting sets up the call audio path

**When you enter a meeting, the SDK sets up the call audio path and keeps it until you exit**, whether or not you turn on the microphone. Turning the microphone on or off only decides "whether to publish"; it doesn't affect whether the underlying audio capture is running.

<Warning>
**Entering a meeting requests microphone permission**, even if the member only intends to listen. Make sure `Info.plist` contains `NSMicrophoneUsageDescription`; otherwise the app crashes.

**While in the meeting, the iOS status bar shows the orange microphone indicator.** Audio capture really is running; this matches the behavior of meeting apps such as Zoom and Tencent Meeting, and it doesn't mean the SDK is secretly recording.
</Warning>

Why does it have to work this way? On iOS, earpiece output only exists under the recording-capable session category (`.playAndRecord`), and testing on real devices shows that "play only normally, then upgrade temporarily when the earpiece is needed" doesn't switch over—keeping the call path resident is the prerequisite for controllable routing.

If the user denies microphone permission, the SDK downgrades to playback-only mode: **you can still hear other members**, but the earpiece route isn't available, only the speakerphone.

We recommend also declaring the background audio capability in `Info.plist`, so the system doesn't suspend audio when the app goes to the background:

```xml
<key>UIBackgroundModes</key>
<array>
    <string>audio</string>
</array>
```

---

### Query the current state

```swift
meeting.currentAudioRoute           // Actual system route (five states, including Bluetooth / wired)
meeting.effectiveAudioRouteTarget   // Currently effective target = temporary override ?? persistent default (two states)
meeting.audioRouteOverride          // Temporary override; nil means none
meeting.isExternalAudioRouteActive  // Whether audio is on Bluetooth headphones or a wired headset
meeting.isAudioSessionActive        // Whether the call audio path is set up (should be true after entering the meeting)
meeting.audioCallState              // System call state (as observed through CallKit)
meeting.availableAudioRoutes()      // Snapshot of system audio ports, for diagnostics / display
```

<Note>
Distinguish `currentAudioRoute` (where the sound **actually** comes out, five states) from `effectiveAudioRouteTarget` (the target you **asked for**, two states). With headphones plugged in, the former is `.bluetooth` while the latter may still be `.speaker`—this isn't a contradiction; external devices take priority. What you show the user in the UI is `currentAudioRoute`.

`availableAudioRoutes()` returns a snapshot of ports, **not a list for the user to choose from**—the only controllable targets are the earpiece and the speakerphone.
</Note>

---

### Stop the audio unit for local-only playback

Scenarios like recorded video classes: the person is in the meeting but is only playing a recorded video, and **there's no call audio to send or receive at all**. The VoIP voice processing unit still holds the audio session and pushes the playback volume of `AVPlayer` down considerably. Stop the audio unit, the system audio session is handed back to the local player, and the volume returns to normal.

```swift
meeting.setAudioModuleEnabled(false)   // Before starting to play the recording
meeting.setAudioModuleEnabled(true)    // After the recording finishes playing
meeting.isAudioModuleEnabled           // Whether it's currently managed automatically by the media streaming engine (default true)
```

<Warning>
**While it's disabled, call audio can't be received or sent.** You must set it back to `true` after the recording finishes; otherwise the rest of the meeting is silent—it looks exactly like "no one has turned on their microphone," so check this first when troubleshooting.
</Warning>

<Note>
You don't need to clean up yourself when entering a meeting again: every time you enter a meeting, it's automatically reset to `true`, so a manually disabled state from the previous meeting doesn't leak into the next one.

This switch is only for scenarios where "the whole meeting needs no call audio." If you just want to mute yourself or someone else, use the microphone switch or unsubscribe; don't stop the audio unit. This is a thin wrapper around the underlying `AudioRouteSession.setAudioModuleEnabled(_:)`; see [SRTC · Audio routing](/en/rtc/swift/advanced/audio-routing).
</Note>

---

### Listen for route changes

```swift
extension MeetingController: SMeetingDelegate {

    func meeting(_ meeting: SMeetingEngine, audioRouteDidChange data: AudioRouteChangeEventData) {
        // Already called back on the main thread, so you can update the UI directly
        updateSpeakerButton(
            isOn: data.route == .speaker,
            isEnabled: !meeting.isExternalAudioRouteActive
        )
    }

    func meetingAudioRouteDidRecoverFromInterruption(_ meeting: SMeetingEngine) {
        // Fires once after an incoming call / Siri interruption has actually recovered; just refresh the UI
    }
}
```

`AudioRouteChangeEventData` carries `route` (after the change), `previousRoute` (before the change), and `reason` (the reason given by the system: `.oldDeviceUnavailable` means unplugged, `.newDeviceAvailable` means plugged in, `.override` means the app actively overrode it). When troubleshooting routing problems, `reason` is often more valuable than the result itself.

Audio routing events **don't depend on meeting state**; the SDK starts reporting them once the instance is created, so pre-meeting device check pages can use them too.

<Note>
Interruption recovery isn't a one-shot thing: when an audio interruption ends but the system phone call hasn't actually hung up yet, reactivation is bound to fail. The SDK waits until "the system call has ended" and "the app is in the foreground" before retrying, and fires `meetingAudioRouteDidRecoverFromInterruption` only after recovery actually succeeds. Your app doesn't need to handle this timing itself.
</Note>

---

### Relationship with setSpeakerOutputEnabled

`setSpeakerOutputEnabled(_:)` in [Device management](/en/meeting/swift/advanced/device-management) and `setAudioRoute(_:)` on this page are **two ways of writing the same mechanism**; both map to the system's `overrideOutputAudioPort`:

```swift
try meeting.setSpeakerOutputEnabled(true)   // Equivalent to setAudioRoute(.speaker)
try meeting.setSpeakerOutputEnabled(false)  // Equivalent to setAudioRoute(.earpiece)
```

To express "speakerphone by default long-term," use `defaultAudioRoute`. Don't build a third set of state of your own on top of these two.

---

### FAQ

**The switch doesn't take effect**

Check in this order:

1. Whether audio is currently on an external device (`isExternalAudioRouteActive`)—in that case, switching to the speaker has no effect anyway
2. Whether you've entered the meeting (`isAudioSessionActive`)—before the audio path is set up, the setting is only recorded and applied once the path is set up
3. Whether microphone permission was denied—if denied, the session is downgraded and the earpiece isn't available

**Why microphone permission is needed even without turning on the microphone**

See "Principle 3." Earpiece output exists only under the recording-capable session category; this is an iOS platform limitation.

**Route switching doesn't work in the simulator**

The simulator has no earpiece or Bluetooth routes, and its port list isn't real. **Audio routing must be verified on a real device.**

---

### Related pages

+ [Device management](/en/meeting/swift/advanced/device-management)
+ [Media control](/en/meeting/swift/advanced/media-control)
+ [SRTC · Audio routing](/en/rtc/swift/advanced/audio-routing)
