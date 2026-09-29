---
title: "Device management"
description: "Enumerate and switch cameras, microphones, and speakers in the SMeeting Swift SDK, choose audio output on macOS or toggle the speakerphone on iOS, and handle device plug and unplug events. Read when building a device picker or a pre-meeting device check page."
---

### Overview

The device APIs are all on `SMeetingEngine`, so you don't need to handle the platform differences between iOS and macOS yourself:

| Capability | API | Platform |
| --- | --- | --- |
| Enumerate devices | `getDevices(kind:)` | All |
| Switch cameras | `switchCamera(deviceId:)` | All |
| Switch microphones | `switchMic(deviceId:)` | All |
| Choose the audio output device | `setAudioOutput(deviceId:)` | macOS only |
| Toggle the speakerphone | `setSpeakerOutputEnabled(_:)` | iOS only |

Device capabilities **don't depend on meeting state**: after logging in (even before entering a meeting), you can enumerate devices and listen for plug and unplug events, which makes it easy to build a "pre-meeting device check" page.

---

### Enumerate devices

```swift
let cameras = meeting.getDevices(kind: .videoInput)
let microphones = meeting.getDevices(kind: .audioInput)
let speakers = meeting.getDevices(kind: .audioOutput)

let all = meeting.getDevices()   // Returns all devices when kind is omitted
```

The returned `DeviceInfo` contains `deviceId`, `name`, `kind`, and `isDefault`.

Watch out for platform differences:

+ **macOS**: the audio lists include a virtual device that points to the system default input / output
+ **iOS audio input**: returns the available audio input routes (Bluetooth, wired headset, built-in microphone, and so on)
+ **iOS audio output**: the system doesn't provide enumeration, so `kind: .audioOutput` returns an empty array on iOS—output control on iOS is a Boolean "speakerphone or not" switch; see below

---

### Switch cameras

```swift
// Specify a device
try await meeting.switchCamera(deviceId: deviceId)

// iOS: switch between front and back cameras
try await meeting.switchCamera()
```

Calling it while the camera is off throws `SMeetingError.deviceError`. If the user picks a device in a dropdown **before turning on the camera**, we recommend storing the choice in your app state first and passing it in when you call `requestOpenCamera(deviceId:)`.

---

### Switch microphones

```swift
try meeting.switchMic(deviceId: deviceId)
```

This method doesn't throw a "microphone not on" error; it adapts to the current state:

+ **Microphone on**: switches the input device being captured
+ **Microphone off (iOS)**: preselects the audio input route, for example choosing Bluetooth headphones before entering the meeting
+ **Microphone off (macOS)**: the recording pipeline hasn't started yet, so the call returns directly without doing anything or reporting an error

---

### Audio output

The two platforms have different capability models on the output side, so the APIs are split as well.

#### macOS: choose the output device

```swift
try meeting.setAudioOutput(deviceId: deviceId)
```

Use it to choose among hardware such as the built-in speakers, USB sound cards, and Bluetooth speakers.

#### iOS: speakerphone switch

```swift
try meeting.setSpeakerOutputEnabled(true)   // Force the speakerphone
try meeting.setSpeakerOutputEnabled(false)  // Go back to the system default output (earpiece / Bluetooth / wired headset)
```

On iOS, specific output routes such as Bluetooth and AirPlay are chosen by the user through Control Center or `AVRoutePickerView`; apps can't specify them directly.

To set "use the speakerphone by default long-term," or to read the actual current route and listen for route changes, use the APIs in [Audio routing](/en/meeting/swift/advanced/audio-routing)—`setSpeakerOutputEnabled(_:)` and `setAudioRoute(_:)` there are two ways of writing the same mechanism.

#### How it differs from "speaker mute"

These two things are orthogonal; don't mix them up:

| Purpose | API |
| --- | --- |
| Whether to hear remote audio | `toggleRemoteAudioMute(_:)` |
| Which hardware plays the sound | `setAudioOutput(deviceId:)` / `setSpeakerOutputEnabled(_:)` |

---

### Listen for device plug and unplug events

Device changes are reported through `SMeetingDelegate`:

```swift
func meeting(_ meeting: SMeetingEngine, didAddDevice data: DeviceChangeEventData) {
    refreshDeviceList()
}

func meeting(_ meeting: SMeetingEngine, didRemoveDevice data: DeviceChangeEventData) {
    refreshDeviceList()
}
```

On iOS, audio route changes such as plugging in or unplugging a headset and connecting / disconnecting Bluetooth are also reported as "devices" through these two events.

Recommended practice:

+ In the callbacks, only refresh the device list state, and let the UI layer update the pickers from the new list automatically
+ If the currently selected `deviceId` has disappeared from the list, fall back to the default device

```swift
func refreshDeviceList() {
    cameras = meeting.getDevices(kind: .videoInput)
    if let id = selectedCameraId, !cameras.contains(where: { $0.deviceId == id }) {
        selectedCameraId = nil    // Fall back to the default
    }
}
```

> When a device in use is unplugged, the SDK falls back to an available device on its own, so you don't need to build a whole fault-tolerance layer. You should still refresh the UI, though, so it doesn't keep showing a device that no longer exists.

---

### Related pages

+ [Media control](/en/meeting/swift/advanced/media-control)
+ [API reference - Devices](/en/meeting/swift/api-reference/devices)
