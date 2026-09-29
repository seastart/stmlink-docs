---
title: "Audio routing (iOS)"
description: "Use AudioRouteSession in the SRTC Swift SDK to control whether iOS audio plays from the speaker or the receiver: the persistent vs. temporary route layers, why external devices can't be switched to, why joining requests microphone permission, and route change and interruption callbacks."
---

### Overview

On iOS, "where sound comes out" is managed by `AudioRouteSession.shared`. It exists only on iOS—macOS uses an independent input / output hardware device model and goes through `setOutputDevice(_:)` in [Device management](/en/rtc/swift/advanced/device-management).

This API is designed after the common practice of mainstream RTC SDKs (Agora, Tencent TRTC, LiveKit). There are three principles to understand first; otherwise it's easy to write code that "sets the route but has no effect".

---

### Principle 1: you can only switch between the speaker and the receiver

`AudioRouteTarget` has only two values:

```swift
public enum AudioRouteTarget {
    case speaker    // Speaker (speakerphone)
    case earpiece   // Receiver
}
```

**The SDK doesn't provide an API to "switch to Bluetooth headphones / wired headphones".** This isn't a missing feature but an iOS platform limitation: the system has no reliable way for an app to target a specific external device (you can't choose among several connected devices, and switching between A2DP and HFP is decided by the system based on the session category). Agora, TRTC, and LiveKit don't have such an API either.

External devices behave as follows:

+ **When plugged in, the system switches to them automatically**; when several devices are connected at once, the most recently connected one wins
+ **When unplugged**, the SDK falls back to the route you set
+ When you need to let the user choose Bluetooth / AirPlay themselves, use the system-provided `AVRoutePickerView`

<Warning>
While Bluetooth or wired headphones are in use, `setAudioRoute(.speaker)` **has no effect**, and audio still comes out of the external device. iOS doesn't allow taking output back from an external device to the built-in speaker. This matches the behavior of Agora and other SDKs; the SDK doesn't throw an error for this, it only logs it. Check the actual result with `currentRoute`—don't assume that a successful call means the route has switched.
</Warning>

---

### Principle 2: persistent and temporary settings are two layers

| Layer | API | When it applies | Description |
| :--- | :--- | :--- | :--- |
| Persistent | `defaultAudioRoute` | Set before joining, stays in effect | Equivalent to Agora's `setDefaultAudioRouteToSpeakerphone` |
| Temporary | `setAudioRoute(_:)` | Called after joining | Equivalent to Agora's `setEnableSpeakerphone` |

The priority is **temporary > persistent**. After an external device is unplugged, the SDK falls back according to this priority.

#### Persistent setting: decide the default behavior before joining

```swift
// Voice call scenario: use the receiver by default
AudioRouteSession.shared.defaultAudioRoute = .earpiece

// Video conferencing scenario: use speakerphone by default
AudioRouteSession.shared.defaultAudioRoute = .speaker
```

<Tip>
If you don't need to "let the user switch temporarily during a call", **this one setting is all you need**. Set it once, and fallback after plugging or unplugging headphones follows it from then on.
</Tip>

#### Temporary setting: switch during a call

```swift
// The user tapped the speakerphone button
AudioRouteSession.shared.setAudioRoute(.speaker)

// The user tapped the receiver button
AudioRouteSession.shared.setAudioRoute(.earpiece)

// Drop the temporary choice and go back to defaultAudioRoute
AudioRouteSession.shared.clearAudioRouteOverride()
```

The temporary setting gets cleared by system behavior (plugging or unplugging an external device, a system call, and so on). This is by design, not a bug.

---

### Principle 3: joining sets up the audio path

**When you join a channel, the SDK sets up the call audio path and keeps it until you leave**, whether or not you turn on the microphone. Turning the microphone on or off only decides "whether to publish"; it doesn't affect whether underlying audio capture is running.

This leads to two consequences that you must tell your product team and users about in advance:

<Warning>
**Joining a channel requests microphone permission**, even if the user only intends to listen. Make sure `Info.plist` contains `NSMicrophoneUsageDescription`; otherwise the app crashes.

**While in a channel, the iOS status bar shows an orange microphone indicator dot.** Audio capture really is running. This matches the behavior of meeting apps such as Zoom and Tencent Meeting—the SDK isn't secretly recording.
</Warning>

Why must it work this way? Because on iOS, when the audio session isn't in VoIP call mode, **route control as a whole is unreliable**—receiver output exists only under the `.playAndRecord` session category, and testing on real devices showed that upgrading the category on demand doesn't take effect. Tencent TRTC's documentation records the same phenomenon: with the microphone off it uses the media audio path, and in that state you can't set speaker or receiver output.

If the user denies microphone permission, the SDK degrades to playback-only mode: **the user can still hear others**, but the receiver route isn't available—only the speaker.

We recommend also declaring the background audio capability in `Info.plist`, so the system doesn't suspend audio when the app goes to the background:

```xml
<key>UIBackgroundModes</key>
<array>
    <string>audio</string>
</array>
```

---

### Query the current state

`currentRoute` is a **read-only five-state** type that includes external devices the SDK can't switch to but must report accurately:

```swift
let session = AudioRouteSession.shared

session.currentRoute           // .speaker / .receiver / .bluetooth / .headset / .unknown
session.currentRoute.isExternal // Whether audio is going through Bluetooth or wired headphones
session.effectiveRouteTarget   // The target currently in effect = temporary override ?? persistent default
session.routeOverride          // Temporary override; nil means none
session.isBluetoothAvailable   // Whether Bluetooth headphones are connected
session.isHeadsetAvailable     // Whether wired headphones are connected
session.isEngaged              // Whether the audio path is set up (in a channel / capturing)
```

<Note>
Distinguish between `currentRoute` (where sound **actually** comes out, five states) and `effectiveRouteTarget` (the target you **requested**, two states). With headphones plugged in, the former is `.bluetooth` while the latter may still be `.speaker`—this isn't a contradiction; external devices take priority. Your UI should display `currentRoute`.
</Note>

---

### Stop the audio unit during local-only playback

For scenarios like recorded live classes: the user is in the channel but is only playing a recording, with **no call audio to send or receive at all**. The VoIP voice processing unit (VPIO) still holds the audio session and lowers `AVPlayer` playback volume significantly. Stop the audio unit, hand the system audio session back to the local player, and the volume returns to normal.

```swift
let session = AudioRouteSession.shared

// Before starting playback of the recording: stop the audio unit
session.setAudioModuleEnabled(false)

// After the recording finishes playing: hand it back to automatic management by the media engine
session.setAudioModuleEnabled(true)

session.isAudioModuleEnabled   // Whether it's currently managed automatically by the media engine (default true)
```

<Warning>
**While it's disabled, call audio can't be received or sent.** You must set it back to `true` after the recording finishes; otherwise the rest of the session is silent—and the symptom of no sound looks exactly like "the other side hasn't turned on their microphone", so check this first when troubleshooting.
</Warning>

<Note>
In one case you don't need to clean up yourself: each time the audio path is occupied for the **first** time (joining / starting capture), it's automatically reset to `true`, so a manually disabled state from a previous session doesn't leak across sessions. This matches the behavior of the older `RTCEngineKit`, which set `enabledAudioModule:YES` on joining.

This switch is only for scenarios where "the whole session needs no call audio". If you only want to mute yourself or someone else, use `LocalMicTrack.mute()` or unsubscribe—don't stop the audio unit.
</Note>

---

### Listen for route changes

```swift
final class RouteObserver: AudioRouteSessionDelegate {
    init() {
        AudioRouteSession.shared.delegates.add(delegate: self)
    }

    func audioRouteSession(
        _ session: AudioRouteSession,
        didChangeRoute route: AudioRoute,
        from previousRoute: AudioRoute,
        reason: AVAudioSession.RouteChangeReason
    ) {
        // Already called back on the main thread; you can update the UI directly
        print("Route changed: \(previousRoute.displayName) → \(route.displayName)")
    }

    func audioRouteSessionWasInterrupted(_ session: AudioRouteSession) {
        // Incoming call / Siri / another app took over
    }

    func audioRouteSessionDidRecoverFromInterruption(_ session: AudioRouteSession) {
        // Fires only after the interruption has really been recovered (may be delayed, see below)
    }

    func audioRouteSession(_ session: AudioRouteSession, didChangeCallState callState: AudioCallState) {
        // System call state: .incoming / .connected / .disconnected, etc.
    }
}
```

All callbacks run on the main thread, and the protocol provides default empty implementations, so implement only the ones you care about.

The `reason` parameter deserves attention because it distinguishes the source of the change: `.oldDeviceUnavailable` means unplugged, `.newDeviceAvailable` means plugged in, and `.override` means the app overrode it actively. When troubleshooting route issues, this is often more valuable than the result itself.

---

### Interruptions and incoming system calls

The SDK uses CallKit to detect system call state, and interruption recovery isn't a one-shot action:

+ When an audio interruption ends, if the system phone call hasn't actually hung up yet, it **doesn't** recover immediately—reactivating the audio session at that point is guaranteed to fail
+ The recovery condition is "the system call has ended" and "the app is in the foreground"; if not met, it stays in a pending-recovery state
+ It retries automatically when the app returns to the foreground, and a few seconds after the call ends
+ `audioRouteSessionDidRecoverFromInterruption` fires only after recovery actually succeeds

You usually don't need to handle this timing yourself; just refresh the UI in the recovery callback.

---

### Relationship with DeviceManager

The iOS audio methods on `DeviceManager` are a thin wrapper over this API, with semantics aligned with Agora's `setEnableSpeakerphone`:

```swift
try DeviceManager.shared.setSpeakerOutputPreferred(true)   // Equivalent to setAudioRoute(.speaker)
try DeviceManager.shared.setSpeakerOutputPreferred(false)  // Equivalent to setAudioRoute(.earpiece)
DeviceManager.shared.isSpeakerOutputPreferred              // Whether speaker output is currently in use
```

<Note>
`DeviceManager.audioInputs()` and `setAudioInputDevice(_:)` are low-level APIs at the **input port** level. They're a separate matter from "where sound comes out", and they don't take part in the fallback policy described on this page. To control where output goes, use `AudioRouteSession`.
</Note>

---

### Complete example

```swift
import SRTC

final class CallAudioController: AudioRouteSessionDelegate {
    private let session = AudioRouteSession.shared

    /// Call before joining: decide the default behavior
    func prepare(isVideoCall: Bool) {
        session.defaultAudioRoute = isVideoCall ? .speaker : .earpiece
        session.delegates.add(delegate: self)
    }

    /// Speakerphone button
    func toggleSpeaker() {
        let next: AudioRouteTarget = session.currentRoute == .speaker ? .earpiece : .speaker
        session.setAudioRoute(next)

        // Switching has no effect while an external device is in use; tell the user accordingly
        if session.currentRoute.isExternal {
            showToast("Currently using \(session.currentRoute.displayName). Switch in Control Center")
        }
    }

    func audioRouteSession(
        _ session: AudioRouteSession,
        didChangeRoute route: AudioRoute,
        from previousRoute: AudioRoute,
        reason: AVAudioSession.RouteChangeReason
    ) {
        updateSpeakerButton(isOn: route == .speaker, isEnabled: !route.isExternal)
    }
}
```

---

### FAQ

**Switching has no effect**

Check in this order:

1. Whether audio is currently going through an external device (`currentRoute.isExternal`)—in that case switching to the speaker has no effect anyway
2. Whether you've joined or started capture (`isEngaged`)—before the audio path is set up, the setting is only recorded and applied once the path is set up
3. Whether microphone permission was denied—if denied, the session is degraded and the receiver isn't available

**Why microphone permission is needed even without turning on the microphone**

See "Principle 3". Receiver output exists only under a session category that can record—this is an iOS platform limitation.

**An orange dot appears in the status bar after joining**

This is expected. Audio capture really is running, consistent with other meeting apps.

**Route switching has no effect on the Simulator**

The Simulator has no receiver or Bluetooth routes, and `availableInputs` isn't realistic either. **Audio routing must be verified on a real device.**
