---
title: "Media control"
description: "API reference for SMeeting Swift SDK media methods on SMeetingEngine: camera and microphone, screen sharing including the macOS source overload and iOS full-screen broadcast, view capture, remote video and audio subscription and playback, and the MCU composite. Look up parameters and throws here."
---

The APIs on this page are all on `SMeetingEngine`. For usage, see [Media control](/en/meeting/swift/advanced/media-control) and [Video rendering](/en/meeting/swift/advanced/video-rendering).

`NativeVideoView` is an alias the SDK defines for rendering views; the actual type is SRTC's `SRTCVideoRenderer`.

---

### Camera

#### `requestOpenCamera(view:deviceId:preset:byAdmin:adminUid:)`

Turns on the camera: asks the meeting for permission → starts capture → publishes.

```swift
let track = try await meeting.requestOpenCamera()
```

| Parameter | Type | Required | Description |
| --- | --- | :---: | --- |
| `view` | `NativeVideoView?` | No | Local preview view. In SwiftUI, pass `nil` and use `SRTCVideoView(track:)` instead |
| `deviceId` | `String?` | No | The camera to use, taken from `getDevices(kind: .videoInput)`; omit to use the default device |
| `preset` | `CameraPreset` | No | Capture preset, default `.h720p` |
| `byAdmin` | `Bool` | No | Whether this responds to the host's turn-on request, default `false` |
| `adminUid` | `String?` | No | ID of the host who sent the request; must be passed together when `byAdmin` is `true` |

**Returns:** `LocalCameraTrack` (you can ignore it, or read `meeting.cameraTrack` at any time)

**Throws:**

+ `SMeetingError.unauthorized`—the room has camera off for everyone with members not allowed to turn cameras back on themselves, and you're not the host / a co-host
+ `SMeetingError.apiError(code:message:)`
+ Underlying errors when capture or publishing fails (the SDK has already rolled back automatically, so you don't need to call `closeCamera()`)

Calling it again while the camera is already on doesn't start another stream; if you pass a different `deviceId`, it switches to the target device.

---

#### `closeCamera()`

```swift
await meeting.closeCamera()
```

**Returns:** None; doesn't throw. It unpublishes, removes the renderer views, stops capture, and reports `userCameraStateDidChange`.

---

#### `switchCamera(deviceId:)`

```swift
try await meeting.switchCamera()                     // iOS: switch between front and back cameras
try await meeting.switchCamera(deviceId: deviceId)   // Switch to a specified device
```

| Parameter | Type | Required | Description |
| --- | --- | :---: | --- |
| `deviceId` | `String?` | No | Target camera; when omitted on iOS, switches between the front and back cameras |

**Returns:** None

**Throws:** `SMeetingError.invalidState(_:)`—the camera isn't on yet (`deviceError` in 1.3.10 and earlier)

---

### Microphone

#### `requestOpenMic(deviceId:preset:byAdmin:adminUid:)`

```swift
try await meeting.requestOpenMic()
```

| Parameter | Type | Required | Description |
| --- | --- | :---: | --- |
| `deviceId` | `String?` | No | The microphone to use, taken from `getDevices(kind: .audioInput)` |
| `preset` | `MicPreset` | No | Capture preset, default `.music` |
| `byAdmin` | `Bool` | No | Whether this responds to the host's turn-on request, default `false` |
| `adminUid` | `String?` | No | ID of the host who sent the request |

**Returns:** None

**Throws:**

+ `SMeetingError.unauthorized`—the room has mute all on with members not allowed to unmute themselves, and you're not the host / a co-host
+ `SMeetingError.apiError(code:message:)`
+ Underlying errors when capture or publishing fails (the SDK rolls back automatically)

---

#### `closeMic()`

```swift
await meeting.closeMic()
```

**Returns:** None; doesn't throw. It unpublishes, stops capture, and reports `userMicStateDidChange`.

---

### Screen sharing

> **Change in 1.3.5**: the `messageOnly` parameter and its mode have been removed from `requestShare`. To broadcast only the sharing status, use `requestShare(shareType: .whiteBoard)`; screen sharing still performs normal media capture and publishing. Remove `messageOnly: true` from old code or switch to whiteboard sharing.

#### `requestShare(shareType:preset:view:byAdmin:adminUid:)`

```swift
try await meeting.requestShare()
```

| Parameter | Type | Required | Description |
| --- | --- | :---: | --- |
| `shareType` | `ShareType` | No | `.screen` (default) or `.whiteBoard` |
| `preset` | `ScreenPreset` | No | Capture preset, default `.h1080p` |
| `view` | `NativeVideoView?` | No | Local preview view |
| `byAdmin` | `Bool` | No | Whether this responds to the host's turn-on request, default `false` |
| `adminUid` | `String?` | No | ID of the host who sent the request |

**Returns:** None

**Throws:**

+ `SMeetingError.unauthorized`—the room has sharing disabled, and you're not the host / a co-host
+ `SMeetingError.invalidState(_:)`—you're already sharing
+ `SMeetingError.apiError(code:message:)`
+ Underlying errors when capture fails (for example, the user denied screen recording permission)

When `shareType` is `.whiteBoard`, no media stream is created; it only broadcasts the sharing status and triggers `roomShareDidStart`.

---

#### `requestShare(source:preset:view:byAdmin:adminUid:excludedWindowIds:excludesCurrentApplication:)`

An overload that specifies the capture source, **macOS 12.3 and later only**.

```swift
let displays = try await ScreenCaptureSources.availableDisplays()
try await meeting.requestShare(source: displays[0])

// Share the whole screen while cutting out in-meeting windows (otherwise testing on the same machine creates an infinite mirror)
let ids = NSApplication.shared.windows
    .filter { $0.isVisible && $0.windowNumber > 0 }
    .map { UInt32($0.windowNumber) }
try await meeting.requestShare(source: displays[0], excludedWindowIds: ids)
```

| Parameter | Type | Required | Description |
| --- | --- | :---: | --- |
| `source` | `ScreenCaptureSource` | Yes | `DisplaySource` (display) or `WindowSource` (app window) |
| `preset` | `ScreenPreset` | No | Capture preset, default `.h1080p` |
| `view` | `NativeVideoView?` | No | Local preview view |
| `byAdmin` | `Bool` | No | Whether this responds to the host's turn-on request |
| `adminUid` | `String?` | No | ID of the host who sent the request |
| `excludedWindowIds` | `[UInt32]` | No | Your own windows to cut out when sharing the whole screen, as `UInt32(NSWindow.windowNumber)`; meaningless when capturing a single window. Default `[]` |
| `excludesCurrentApplication` | `Bool` | No | Set to `true` to go back to the old behavior of "not sharing the app at all"; `excludedWindowIds` is then ignored. Default `false` |

**Returns:** None

**Throws:** Same as the previous overload.

<Warning>
Since 1.3.2 (SRTC 1.4.2), whole-screen sharing **includes your app's own windows by default**. The main in-meeting window is usually rendering remote video; if your UI has a sharing preview, or you're testing with two instances on the same machine, be sure to put these windows into `excludedWindowIds`; otherwise you get an infinite mirror.
</Warning>

---

#### `stopShare()`

```swift
await meeting.stopShare()
```

**Returns:** None; doesn't throw.

---

### View capture

The following APIs are available since **1.3.4**. The caller is responsible for rendering the view into `CVPixelBuffer`s and pushing frames continuously; the SDK only creates and publishes the video track, and doesn't grab frames from the view itself or save a local recording file.

#### `startViewCaptureShare()`

```swift
public func startViewCaptureShare() async throws -> LocalVideoTrack
```

**Parameters:** None.

**Returns:** The published `LocalVideoTrack`, with the track description `screen` and a degradation preference that maintains resolution. Calling it again returns the existing track.

**Throws:**

+ `SMeetingError.notInMeeting`—you haven't entered a meeting yet.
+ `SMeetingError.invalidState(_:)`—a screen sharing track already exists, including a broadcast listening track that's been prepared but not yet published.
+ Underlying track publishing errors.

This API publishes the media track directly, without going through `requestShare()`'s flow of asking the meeting backend and notifying the sharing status. The caller should manage the sharing status according to its own business logic and make sure view capture and screen sharing are mutually exclusive; to switch to screen sharing, stop view capture first.

#### `stopViewCaptureShare()`

```swift
public func stopViewCaptureShare() async
```

**Parameters:** None.

**Returns:** None; doesn't throw. It tries to unpublish and clears the track and its renderers, without turning off or unpublishing the microphone track. The caller should also stop pushing frames.

View capture must be ended through this API; `stopShare()` can't be used instead.

---

### iOS full-screen sharing

The following APIs are available on iOS only and are used to share the entire system screen (on iOS, `requestShare()` can capture only your own app's content). You must integrate a Broadcast Upload Extension first; for the full steps, see [Screen sharing](/en/meeting/swift/advanced/screen-sharing).

#### `prepareBroadcastShare(appGroup:preset:)`

```swift
try await meeting.prepareBroadcastShare(appGroup: "group.your.app")
```

| Parameter | Type | Required | Description |
| --- | --- | :---: | --- |
| `appGroup` | `String` | Yes | The App Group ID shared by the host app and the extension |
| `preset` | `ScreenPreset` | No | Capture preset, default `.h1080p` |

Sets up the listener for full-screen capture and waits for the user to start broadcasting from the system UI. **It doesn't notify the meeting backend or publish a track**—sharing hasn't started yet at this point. Just call it after entering the meeting; it returns idempotently if already listening or already sharing.

**Returns:** None

**Throws:** Underlying errors when the capture listener fails to be set up (for example, an incorrect App Group configuration).

---

#### `publishBroadcastShare(view:byAdmin:adminUid:)`

```swift
try await meeting.publishBroadcastShare()
```

| Parameter | Type | Required | Description |
| --- | --- | :---: | --- |
| `view` | `NativeVideoView?` | No | Local preview view, usually not needed |
| `byAdmin` | `Bool` | No | Whether this responds to the host's turn-on request, default `false` |
| `adminUid` | `String?` | No | ID of the host who sent the request |

Publishes the full-screen capture that's already producing frames to the meeting (backend + underlying SRTC channel). **Call it after receiving `shareBroadcastDidStart`**—that's the moment the user actually starts sharing. It returns idempotently if already published.

**Returns:** None

**Throws:**

+ `SMeetingError.invalidState(_:)`—`prepareBroadcastShare` hasn't been called yet
+ `SMeetingError.unauthorized`—the room has sharing disabled, and you're not the host / a co-host
+ `SMeetingError.apiError(code:message:)`

When publishing fails, the SDK rolls back the sharing status automatically.

---

#### `stopBroadcastListening()`

```swift
await meeting.stopBroadcastListening()
```

Stops listening for full-screen capture. Calling it while sharing is equivalent to `stopShare()`, and the listener won't be set up again automatically afterward. `exitRoom()` calls it automatically.

**Returns:** None; doesn't throw.

---

#### `requestShare(broadcastAppGroup:preset:view:byAdmin:adminUid:)`

```swift
try await meeting.requestShare(broadcastAppGroup: "group.your.app")
```

The one-step version: announces sharing to the meeting at the same time as setting up the listener.

<Warning>
The user may never tap the system pill, in which case the meeting is left with a sharing flag that has no video, and you have to withdraw it yourself with a timeout. **For meeting scenarios, use `prepareBroadcastShare` + `publishBroadcastShare`**; this overload is kept only for simple integrations that "don't care about the intermediate state."
</Warning>

---

#### `isShareBroadcastActive`

```swift
if meeting.isShareBroadcastActive { /* The screen is producing frames */ }
```

**Type:** `Bool` (read-only)

Whether iOS full-screen sharing is actually producing frames right now. After `prepareBroadcastShare`, this property stays `false` until the user taps "Start Broadcast" in the system pill. It's always `false` in in-app capture mode.

---

### Remote video

#### `subscribeRemoteVideoTrack(uid:trackDesc:)`

Subscribes to a remote video track without binding a renderer view.

```swift
let track = try await meeting.subscribeRemoteVideoTrack(uid: uid, trackDesc: .cameraBig)
```

| Parameter | Type | Required | Description |
| --- | --- | :---: | --- |
| `uid` | `String` | Yes | Remote member ID |
| `trackDesc` | `TrackDesc` | Yes | Track description, such as `.cameraBig` or `.screen` |

**Returns:** `RemoteVideoTrack`

**Throws:**

+ `SMeetingError.notInMeeting`
+ `SMeetingError.remoteTrackUnavailable(uid:desc:)`—the member doesn't have this track

---

#### `unsubscribeRemoteVideoTrack(uid:trackDesc:)`

Unsubscribes unconditionally, regardless of whether any renderer view is still using it.

| Parameter | Type | Required | Description |
| --- | --- | :---: | --- |
| `uid` | `String` | Yes | Remote member ID |
| `trackDesc` | `TrackDesc` | Yes | Track description |

**Returns:** None

**Throws:** `SMeetingError.notInMeeting`. Returns silently when the track doesn't exist.

---

#### `startPlayRemoteVideo(view:uid:trackDesc:)`

Subscribes and binds the video to the renderer view you pass in; suited to UIKit / AppKit.

| Parameter | Type | Required | Description |
| --- | --- | :---: | --- |
| `view` | `NativeVideoView` | Yes | A renderer view already attached to the view hierarchy |
| `uid` | `String` | Yes | Remote member ID |
| `trackDesc` | `TrackDesc` | Yes | Track description |

**Returns:** `RemoteVideoTrack`

**Throws:** Same as `subscribeRemoteVideoTrack(uid:trackDesc:)`

---

#### `stopPlayRemoteVideo(view:uid:trackDesc:)`

Unbinds the renderer view. It actually unsubscribes **only when the track no longer has any renderer view**.

| Parameter | Type | Required | Description |
| --- | --- | :---: | --- |
| `view` | `NativeVideoView` | Yes | The renderer view to unbind |
| `uid` | `String` | Yes | Remote member ID |
| `trackDesc` | `TrackDesc` | Yes | Track description |

**Returns:** None

**Throws:** `SMeetingError.notInMeeting`

---

### Remote audio

Remote audio is already subscribed automatically when you enter the meeting; the following APIs are for scenarios that need fine-grained control.

#### `subscribeRemoteAudioTrack(uid:trackDesc:)`

| Parameter | Type | Required | Description |
| --- | --- | :---: | --- |
| `uid` | `String` | Yes | Remote member ID |
| `trackDesc` | `TrackDesc` | No | Default `.mic` |

**Returns:** None

**Throws:** `SMeetingError.notInMeeting`, `SMeetingError.remoteTrackUnavailable(uid:desc:)` (the member doesn't have this track)

#### `unsubscribeRemoteAudioTrack(uid:trackDesc:)`

Same parameters as above. Returns silently when the track doesn't exist.

#### `toggleRemoteAudioMute(_:)`

The master switch for remote audio playback; it only toggles playback and doesn't change subscriptions.

```swift
meeting.toggleRemoteAudioMute(true)   // Mute
```

| Parameter | Type | Required | Description |
| --- | --- | :---: | --- |
| `mute` | `Bool` | Yes | `true` mutes, `false` resumes playback |

**Returns:** None; doesn't throw.

---

### Composite video (MCU)

#### `startPlayRemoteVideoMcu(view:uid:)`

Subscribes to and plays the server-side composite video. Requires the server to have a composite task set up.

| Parameter | Type | Required | Description |
| --- | --- | :---: | --- |
| `view` | `NativeVideoView` | Yes | Renderer view |
| `uid` | `String` | Yes | User ID corresponding to the composite video |

**Returns:** `RemoteVideoTrack`

**Throws:** `SMeetingError.notInMeeting`, `SMeetingError.remoteTrackUnavailable(uid:desc:)` (composite video track not found)

#### `stopPlayRemoteVideoMcu(view:)`

| Parameter | Type | Required | Description |
| --- | --- | :---: | --- |
| `view` | `NativeVideoView` | Yes | The renderer view passed in earlier |

**Returns:** None

---

### Related pages

+ [Media control](/en/meeting/swift/advanced/media-control)
+ [Video rendering](/en/meeting/swift/advanced/video-rendering)
+ [Screen sharing](/en/meeting/swift/advanced/screen-sharing)
