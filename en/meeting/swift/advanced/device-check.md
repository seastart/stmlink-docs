---
title: "Device checks (pre-meeting / in-meeting preview)"
description: "Check the camera, microphone, and speaker before or during a meeting: list devices, preview without publishing via requestOpenCamera(publish: false), use isCameraOpened to decide whether to close, and the limits and workarounds for mic level and speaker tests on Apple platforms"
---

### Overview

A pre-meeting device check page and an in-meeting settings page both need to "turn the device on to take a look without sending it to anyone". How each check works on the Swift meeting layer:

| Check | How | Support |
| --- | --- | --- |
| Device list | `getDevices(kind:)` | iOS / macOS |
| Camera preview | `requestOpenCamera(publish: false)` | iOS / macOS, before and during a meeting, since 1.9.0 |
| Mic level | After opening the mic in a meeting, read your own entry in `activeSpeakersDidChange` | **Testing the mic outside a meeting or capture-only isn't supported yet**; see below |
| Speaker test | On macOS, choose the device with `setAudioOutput(deviceId:)`; play the test sound yourself | The SDK has no speaker test API |

---

### Device list

```swift
let cameras = meeting.getDevices(kind: .videoInput)
let microphones = meeting.getDevices(kind: .audioInput)
let speakers = meeting.getDevices(kind: .audioOutput)
```

For device hot-plugging and switching, see [Device management](/en/meeting/swift/advanced/device-management).

---

### Camera preview

With `publish: false`, `requestOpenCamera` only captures and previews: it doesn't ask the meeting for permission, doesn't publish, and doesn't fire camera state events, and you can call it before or during a meeting. The host turning off your camera or disabling cameras for everyone doesn't affect a preview-only track.

```swift
// Open the preview (pass view in UIKit / AppKit; in SwiftUI pass nil and render with SRTCVideoView(track:))
let track = try await meeting.requestOpenCamera(
    view: previewView,
    deviceId: selectedCameraId,
    publish: false
)

// The user picked another camera on the check page: call it again with the new deviceId
try await meeting.requestOpenCamera(view: previewView, deviceId: newCameraId, publish: false)

// Close the preview: close only a preview-only camera; leave the meeting camera alone
if !meeting.isCameraOpened {
    await meeting.closeCamera()
}
```

What happens in each combination:

+ **Deciding to turn the camera on after previewing**: call `requestOpenCamera()` again with the default `publish: true`. It asks the meeting for permission and publishes **the same track**, without restarting capture, so the picture doesn't flicker.
+ **Opening a preview while the meeting camera is already on**: `publish: false` just returns the track in use and doesn't start another capture. `isCameraOpened` is then `true`, so don't call `closeCamera()` when closing the preview.
+ **A camera opened with default parameters before entering a meeting**: calling `requestOpenCamera()` again after entering publishes it to the meeting.

---

### Mic level

`requestOpenMic` on the Swift meeting layer has **no** `publish: false`, so testing the mic outside a meeting or capture-only without publishing isn't supported yet. This is a limit of the audio pipeline on Apple platforms: the microphone stays muted until it is published, and the recording pipeline outside a meeting doesn't start until you enter one, so no valid level can be read.

After opening the mic in a meeting, you can show your own level from your entry (`isLocal == true`) in the active speaker event:

```swift
func meeting(_ meeting: SMeetingEngine, activeSpeakersDidChange snapshot: ActiveSpeakersSnapshot) {
    let myLevel = snapshot.speakers.first(where: { $0.isLocal })?.level ?? 0
    micLevelView.update(myLevel)   // 0–1
}
```

If a pre-meeting check page really needs a mic test, capture a short sample yourself with the system `AVAudioRecorder` / `AVAudioEngine` to read the level, and release it before entering the meeting.

---

### Speaker test

The SDK has no API for playing a test sound; play it yourself with `AVAudioPlayer`:

+ **macOS**: first select the output device to test with `try meeting.setAudioOutput(deviceId:)`, then play the test sound.
+ **iOS**: the output route is decided by the system. Use `setSpeakerOutputEnabled(_:)` to switch between the speaker and the earpiece, and leave external devices such as Bluetooth to the system route picker; see [Audio routing](/en/meeting/swift/advanced/audio-routing).

---

### Related pages

+ [Device management](/en/meeting/swift/advanced/device-management)
+ [Media control API](/en/meeting/swift/api-reference/media-control)
