---
title: "Media control"
description: "Turn the camera, microphone, and speaker on and off in the SMeeting Swift SDK, switch devices and presets, respond to the host's turn-on requests, and see how room policies like mute all block turning media on. Read when building in-meeting media buttons."
---

### Overview

Media control in a meeting has three parts:

+ **Local capture and publishing**: camera, microphone, screen sharing
+ **Remote playback**: the master switch for remote audio, remote video subscription
+ **Room policies**: mute all / camera off for everyone / sharing disabled set by the host directly decide whether you can turn media on

The naming follows one clear rule: **turn-on APIs include `request`, turn-off APIs don't**.

| Action | Turn on | Turn off |
| --- | --- | --- |
| Microphone | `requestOpenMic(...)` | `closeMic()` |
| Camera | `requestOpenCamera(...)` | `closeCamera()` |
| Sharing | `requestShare(...)` | `stopShare()` |

The turn-on APIs are marked `throws` (they can be rejected by room policies or fail to capture); the turn-off APIs never throw, so you can call them directly.

---

### Microphone

#### Turn on and off

```swift
try await meeting.requestOpenMic()
await meeting.closeMic()
```

`requestOpenMic` does the following in order: asks the meeting for permission to turn on the microphone → starts local microphone capture → publishes to the meeting → emits the `userMicStateDidChange` event.

#### Specify a device and audio preset

```swift
try await meeting.requestOpenMic(
    deviceId: selectedMicId,   // From getDevices(kind: .audioInput)
    preset: .music
)
```

If the microphone is already on and you call it again with a different `deviceId`, the SDK switches directly to the target device instead of ignoring the call.

`preset` takes values from SRTC's `MicPreset`: `.speech`, `.music` (default), `.musicStereo`, `.musicHighQuality`, `.musicHighQualityStereo`.

---

### Camera

#### Turn on and off

```swift
let track = try await meeting.requestOpenCamera()
await meeting.closeCamera()
```

`requestOpenCamera` returns a `LocalCameraTrack`; you can also get it at any time through `meeting.cameraTrack` (`nil` when the camera is off).

#### Parameters

```swift
try await meeting.requestOpenCamera(
    view: nil,                 // Pass nil in SwiftUI
    deviceId: selectedCameraId,
    preset: .h720p
)
```

+ `view` is needed only in UIKit / AppKit, and it must be an `SRTCVideoRenderer` that is **already attached to the view hierarchy**. In SwiftUI, always pass `nil` and hand `meeting.cameraTrack` to `SRTCVideoView(track:)`
+ `preset` takes values from SRTC's `CameraPreset`: `.h180p`, `.h360p`, `.h720p` (default), `.h1080p`

#### Replace the preview view (UIKit / AppKit, 1.3.8+)

```swift
meeting.updateLocalCameraView(newPreviewView)
```

UIKit hosts often destroy and recreate the view that hosts the preview when the layout changes (rebuilding the grid, switching between the first screen and the video wall). Once the view is recreated, the renderer is still attached to the old view, and the local video goes black. `updateLocalCameraView(_:)` moves the renderer to the new view **without interrupting capture**, so you don't need to turn the camera off and on again.

Calling `requestOpenCamera(view:)` while the camera is already on also moves the renderer to the newly passed view (since 1.3.8; before that, the new view was silently ignored).

#### Switch cameras

```swift
// iOS: switch between front and back cameras
try await meeting.switchCamera()

// Specify a device (multiple cameras on desktop)
try await meeting.switchCamera(deviceId: deviceId)
```

Calling it while the camera is off throws `SMeetingError.deviceError`.

---

### How room policies affect turning media on

The host can set room-level media policies that directly decide whether regular members can turn media on themselves:

| Room field | Meaning |
| --- | --- |
| `RoomInfo.micDisabled` | Mute all is on for the room |
| `RoomInfo.selfUnmuteMicDisabled` | Members aren't allowed to unmute themselves |
| `RoomInfo.cameraDisabled` | Camera off for everyone is on for the room |
| `RoomInfo.selfUnmuteCameraDisabled` | Members aren't allowed to turn their cameras back on themselves |
| `RoomInfo.shareDisabled` | Sharing is disabled for the room |

When "mute all" and "members aren't allowed to unmute themselves" are both `true`, and you're not the host / a co-host, `requestOpenMic()` throws `SMeetingError.unauthorized`. The same applies to the camera.

We recommend reflecting this state in the UI in advance, rather than letting users tap the button and then get an error:

```swift
let info = meeting.getRoomInfo()
let canUnmuteSelf = !(info?.micDisabled == true && info?.selfUnmuteMicDisabled == true) || isAdmin
```

In addition, when the host turns on "mute all" during the meeting, the SDK automatically turns off the microphones of non-host members and reports `userMicStateDidChange` once (with `byAdmin` set to `true`). The same applies to the camera.

---

### Respond to the host's turn-on requests

The host can ask a member to turn on their microphone or camera, and the member receives an event:

```swift
func meeting(_ meeting: SMeetingEngine, adminDidRequestOpenMic data: AdminRequestOpenMicEventData) {
    // data.opUid is the host who sent the request
}
```

To accept, pass `byAdmin` together with `adminUid` to the turn-on API:

```swift
try await meeting.requestOpenMic(byAdmin: true, adminUid: data.opUid)
try await meeting.requestOpenCamera(byAdmin: true, adminUid: data.opUid)
```

To decline, call the corresponding reject API:

```swift
try await meeting.rejectOpenMic(adminUid: data.opUid)
try await meeting.rejectOpenCamera(adminUid: data.opUid)
```

> If you pass `byAdmin: true`, you must also pass `adminUid`; otherwise the call doesn't carry the "respond to the request" semantics.

The host can also directly turn off a member's microphone / camera. The affected member doesn't need to handle anything: the SDK stops the stream automatically and reports `userMicStateDidChange` / `userCameraStateDidChange` (with `byAdmin` set to `true` and `opUid` set to the operator).

---

### Remote audio

Remote audio is subscribed automatically when you enter the meeting, so you usually need only a "speaker switch":

```swift
meeting.toggleRemoteAudioMute(true)   // Mute: stop playing remote audio
meeting.toggleRemoteAudioMute(false)  // Resume playback
```

This method only toggles playback and doesn't unsubscribe, so switching back and forth has no renegotiation cost.

If you really need fine-grained, per-member control over subscriptions (for example, to listen to only a few streams), use:

```swift
try await meeting.subscribeRemoteAudioTrack(uid: uid)
try await meeting.unsubscribeRemoteAudioTrack(uid: uid)
```

---

### Clean up before exiting the meeting

`exitRoom()` exits the meeting, but we recommend turning off local capture explicitly so that the UI state and the hardware state are both reset:

```swift
await meeting.closeCamera()
await meeting.closeMic()
await meeting.stopShare()
await meeting.exitRoom()
```

---

### Related pages

+ [Device management](/en/meeting/swift/advanced/device-management)
+ [Video rendering](/en/meeting/swift/advanced/video-rendering)
+ [Screen sharing](/en/meeting/swift/advanced/screen-sharing)
+ [API reference - Media control](/en/meeting/swift/api-reference/media-control)
