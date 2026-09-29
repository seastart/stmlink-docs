---
title: "Channel and Track"
description: "API reference for the SRTC Swift SDK's Channel session object and the local/remote track classes: publishing, subscribing, and looking up tracks on Channel; capture, mute, device, and renderer methods on each track type; and the SRTCVideoView / VideoView / SRTCVideoRenderer components."
---

### Channel

`Channel` represents an established channel session and is the core entry point for publishing, subscribing, messaging, and user state.

---

#### Properties

| Property | Type | Description |
| --- | --- | --- |
| `delegates` | `MulticastDelegate<ChannelDelegate>` | Registers channel event callbacks |
| `connectState` | `ConnectionState` | Current connection state |
| `channelInfo` | `ChannelInfo?` | Current channel info |
| `me` | `User?` | The current user |
| `streamVendor` | `StreamVendor` | The current media streaming engine vendor |

---

#### `getUsers()`

Gets info for all users currently in the channel.

```swift
let users = channel.getUsers()
```

**Returns:** `[String: UserInfo]`

---

#### `getUser(_:)`

Gets a user object by `uid`.

```swift
let user = channel.getUser("alice")
```

**Returns:** `User?`

---

#### `publishLocalTrack(_:)`

Publishes a local audio or video track.

```swift
try await channel.publishLocalTrack(micTrack)
try await channel.publishLocalTrack(cameraTrack)
```

Supported overloads:

+ `publishLocalTrack(_ track: LocalAudioTrack, options: AudioPublishOptions? = nil)`
+ `publishLocalTrack(_ track: LocalVideoTrack, options: VideoPublishOptions? = nil)`

Note:

+ Audio tracks go through the internal mixed sending model
+ If a `LocalScreenTrack` carries screen audio, its audio part is published automatically along with it

---

#### `unpublishLocalTrack(_:)`

Unpublishes a local audio or video track.

```swift
try await channel.unpublishLocalTrack(micTrack)
try await channel.unpublishLocalTrack(cameraTrack)
```

We recommend calling `stopCapture()` after unpublishing to release capture resources.

---

#### `subscribeRemoteAudioTrack(uid:trackId:)`

Subscribes to a remote audio track.

```swift
try await channel.subscribeRemoteAudioTrack(uid: uid, trackId: trackId)
```

---

#### `subscribeRemoteVideoTrack(uid:trackId:)`

Subscribes to a remote video track.

```swift
try await channel.subscribeRemoteVideoTrack(uid: uid, trackId: trackId)
```

---

#### `unsubscribeRemoteTrack(_:debounceMs:)`

Unsubscribes from a remote track.

```swift
try await channel.unsubscribeRemoteTrack(track)
```

| Parameter | Type | Required | Description |
| --- | --- | :---: | --- |
| `track` | `Track` | Yes | The remote track object |
| `debounceMs` | `Int` | No | Default `2000`; debounces frequent subscribe/unsubscribe toggling |

---

#### `getRemoteTrack(uid:trackId:)`

Gets a remote track object by user and track ID.

```swift
let track = channel.getRemoteTrack(uid: uid, trackId: trackId)
```

**Returns:** `Track?`

---

#### `getRemoteTrackByDesc(uid:desc:)`

Gets a remote track by `desc`.

```swift
let screenTrack = channel.getRemoteTrackByDesc(uid: uid, desc: "screen")
```

---

---

### Track base class

All tracks inherit from `Track` and share the following core properties:

| Property | Type | Description |
| --- | --- | --- |
| `id` | `String` | Track ID |
| `kind` | `TrackKind` | `audio` or `video` |
| `desc` | `String` | Track description, such as `mic`, `screen`, or `camera_big` |
| `info` | `TrackInfo` | Snapshot of the current track info |
| `uid` | `String?` | UID of the user the track belongs to |
| `delegates` | `MulticastDelegate<TrackDelegate>` | Track-level event callbacks |

Common methods:

+ `getInfo()`

---

### LocalMicTrack

#### Capture control

+ `startCapture(options:)`
+ `stopCapture()`
+ `restartCapture()`

#### User control

+ `mute()`
+ `unmute()`
+ `changeDeviceId(_:)`

Typical usage:

```swift
let micTrack = srtc.createLocalMicTrack(preset: .music)
try await micTrack.startCapture()
try await channel.publishLocalTrack(micTrack)
micTrack.mute()
micTrack.unmute()
```

---

### LocalCameraTrack

#### Capture control

+ `startCapture(options:)`
+ `stopCapture()`
+ `restartCapture()`

#### User control

+ `mute()`
+ `unmute()`
+ `changeDeviceId(_:)`
+ `switchCamera()`

#### Rendering

+ `addRenderer(_:)`
+ `removeRenderer(_:)`
+ `removeAllRenderers()`

---

### LocalScreenTrack

#### Capture control

+ `startCapture(options:)`
+ `stopCapture()`
+ `restartCapture()`

#### User control

+ `mute()`
+ `unmute()`

#### Screen audio

+ `audioTrack`
+ `setAudioTrack(_:)`
+ `getAudioTrack()`

#### Capture mode and state (iOS)

| Member | Type | Description |
| --- | --- | --- |
| `captureMode` | `ScreenCaptureMode` | Capture mode, decided at creation by `createLocalScreenTrack(mode:)`; ignored on macOS |
| `isCapturing` | `Bool` | Whether capture has started. With full-screen capture it means "listening is ready", not that there's video |
| `isBroadcastActive` | `Bool` | With full-screen capture, whether the extension is sending video, i.e. **whether the remote side can see video**; check this to display a "sharing" state |

---

### LocalAudioTrack

For custom audio input:

+ `mute()`
+ `unmute()`
+ `pushAudioBuffer(_:)`

This kind of track usually doesn't need `startCapture()`; instead, your app keeps injecting PCM data.

---

### LocalVideoTrack

For custom video input:

+ `addRenderer(_:)`
+ `removeRenderer(_:)`
+ `removeAllRenderers()`
+ `pushFrame(_:rotation:timestampNs:)`

If you have an external rendering pipeline, a canvas, a screen encoder, or an AI processing pipeline, this entry point is the better fit.

---

### RemoteAudioTrack

#### Playback control

+ `startPlay()`
+ `stopPlay()`
+ `isPlaying`

#### PCM data callback

+ `add(audioRenderer:)`
+ `remove(audioRenderer:)`

The `AudioRenderer` callback receives `AVAudioPCMBuffer` values, suitable for speech transcription, recording, or further analysis.

---

### RemoteVideoTrack

#### Rendering control

+ `addRenderer(_:)`
+ `removeRenderer(_:)`
+ `removeAllRenderers()`

Remote video is usually displayed after a successful subscription, through `SRTCVideoView(track:)` or `SRTCVideoRenderer`.

#### Receive status

+ `isReceiveTimedOut: Bool`

Whether this video has currently been judged to have timed out on receiving. The value matches the `timedOut` last reported by `channel(_:didChangeReceiveStreamStatus:)`, and is suited for **filling in the current state once** when a render view initializes or when the app returns from the background to the foreground, so the UI doesn't fall out of sync with reality by relying on events alone. For the everyday "loading" indicator, we still recommend driving it with events—see [Events](/en/rtc/swift/events) for details.

---

### Rendering components

#### `SRTCVideoView`

Preferred for SwiftUI:

```swift
SRTCVideoView(track: track)
    .frame(width: 320, height: 180)
```

#### `VideoView`

For UIKit / AppKit, use `bind(track:)` / `unbind()` to manage binding.

#### `SRTCVideoRenderer`

A lower-level rendering view, bound by the track explicitly calling `addRenderer(_:)`.
