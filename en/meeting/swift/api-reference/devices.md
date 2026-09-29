---
title: "Devices"
description: "SMeeting Swift SDK device API reference: enumerate cameras, microphones, and speakers, switch the microphone, choose the audio output on macOS, control speakerphone and audio routing on iOS, and the related device and routing events. Read when building device selection or audio output controls."
---

The APIs on this page are all on `SMeetingEngine`. They **don't require being in a meeting**—you can call them once logged in. For usage guidance, see [Device management](/en/meeting/swift/advanced/device-management).

---

#### `getDevices(kind:)`

Enumerates system devices.

```swift
let cameras = meeting.getDevices(kind: .videoInput)
```

| Parameter | Type | Required | Description |
| --- | --- | :---: | --- |
| `kind` | `DeviceInfo.DeviceKind?` | No | Device type filter: `.videoInput` / `.audioInput` / `.audioOutput`; omit it to return all devices |

**Returns:** `[DeviceInfo]`; doesn't throw.

Platform differences:

+ On macOS, the audio lists include a virtual device that points to the system default input / output
+ On iOS, audio input returns the available input routes (Bluetooth, wired headset, built-in microphone, etc.)
+ iOS doesn't support enumerating audio outputs; `kind: .audioOutput` returns an empty array on iOS

---

#### `switchMic(deviceId:)`

Switches the microphone input.

```swift
try meeting.switchMic(deviceId: deviceId)
```

| Parameter | Type | Required | Description |
| --- | --- | :---: | --- |
| `deviceId` | `String` | Yes | Target device ID, taken from `getDevices(kind: .audioInput)` |

**Returns:** None

**Throws:** An underlying error when switching the device fails.

The behavior adapts to the current state:

| State | Behavior |
| --- | --- |
| Microphone on | Switches the input device being captured |
| Microphone off (iOS) | Preselects the audio input route |
| Microphone off (macOS) | Returns immediately without doing anything, and doesn't throw |

---

#### `setAudioOutput(deviceId:)`

Selects the audio output device. **macOS only**.

```swift
try meeting.setAudioOutput(deviceId: deviceId)
```

| Parameter | Type | Required | Description |
| --- | --- | :---: | --- |
| `deviceId` | `String` | Yes | Target output device ID, taken from `getDevices(kind: .audioOutput)` |

**Returns:** None

**Throws:** An underlying error when switching the device fails.

---

#### `setSpeakerOutputEnabled(_:)`

Toggles speakerphone. **iOS only**.

```swift
try meeting.setSpeakerOutputEnabled(true)
```

| Parameter | Type | Required | Description |
| --- | --- | :---: | --- |
| `enabled` | `Bool` | Yes | `true` forces speakerphone; `false` returns to the system default output |

**Returns:** None

**Throws:** An underlying error when the setting fails.

This and `setAudioRoute(_:)` below are two ways of using the same mechanism—don't mix them and end up with two sets of state.

---

### Audio routing (iOS)

The following APIs are **iOS only** and control whether sound comes out of the speaker or the earpiece. These are the only two targets you can switch to—Bluetooth / wired headsets are taken over by the system; for the reason, see [Audio routing](/en/meeting/swift/advanced/audio-routing).

#### `defaultAudioRoute`

```swift
meeting.defaultAudioRoute = .speaker
```

**Type:** `AudioRouteTarget` (read-write)

The persistent default output route. It's most reliable to set it **before entering the meeting**, and it stays in effect long term. It has lower priority than the temporary override from `setAudioRoute(_:)`.

---

#### `setAudioRoute(_:)`

```swift
meeting.setAudioRoute(.earpiece)
```

| Parameter | Type | Required | Description |
| --- | --- | :---: | --- |
| `target` | `AudioRouteTarget` | Yes | `.speaker` (speakerphone) or `.earpiece` (earpiece) |

Temporarily switches the output route during the meeting, with higher priority than `defaultAudioRoute`. **Doesn't throw**: while an external device (Bluetooth / wired) is in use, switching to `.speaker` is skipped by the underlying layer and logged—the operation has no effect on iOS in that case anyway. Use `currentAudioRoute` to check the actual result.

---

#### `clearAudioRouteOverride()`

```swift
meeting.clearAudioRouteOverride()
```

Removes the temporary override and falls back to `defaultAudioRoute`.

---

#### Read-only state

| Member | Type | Description |
| --- | --- | --- |
| `currentAudioRoute` | `AudioRoute` | The system's actual output route (five states, including Bluetooth / wired); this is what your UI should display |
| `effectiveAudioRouteTarget` | `AudioRouteTarget` | The target currently in effect = temporary override ?? persistent default |
| `audioRouteOverride` | `AudioRouteTarget?` | The current temporary override; `nil` means there is none |
| `isExternalAudioRouteActive` | `Bool` | Whether audio is going through a Bluetooth / wired headset; when `true`, gray out the "switch to speaker" button |
| `isAudioSessionActive` | `Bool` | Whether the call audio path has been set up (should be `true` after entering the meeting) |
| `audioCallState` | `AudioCallState` | System call state (as observed through CallKit) |
| `availableAudioRoutes()` | `[AudioRouteInfo]` | A snapshot of ports, **for diagnostics / display**; not a list for users to choose from |

Route changes and recovery from interruptions are reported through `meeting(_:audioRouteDidChange:)` and `meetingAudioRouteDidRecoverFromInterruption(_:)`; see [Events](/en/meeting/swift/events#audio-routing-events-ios).

---

### Device events

Device plug and unplug events are reported through `SMeetingDelegate`; see [Events](/en/meeting/swift/events#device-events):

+ `meeting(_:didAddDevice:)`
+ `meeting(_:didRemoveDevice:)`

---

### Related pages

+ [Device management](/en/meeting/swift/advanced/device-management)
+ [Audio routing](/en/meeting/swift/advanced/audio-routing)
+ [Media control APIs](/en/meeting/swift/api-reference/media-control)
