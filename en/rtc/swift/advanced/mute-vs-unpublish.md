---
title: "Mute vs. unpublish"
description: "The difference between mute / unmute and unpublish / stopCapture in the SRTC Swift SDK: which layer each controls, how microphone, camera, and screen tracks behave on mute, and which to use for microphone, camera, and screen-sharing buttons."
---

### Overview

A common misconception in the Swift SDK is treating "mute" and "unpublish" as the same thing.

From first principles, they control two different layers of state:

+ `mute / unmute` controls "whether this track is outputting media data right now"
+ `unpublishLocalTrack` controls "whether this track is still one of the published tracks in the channel"

So the two differ in their result, their cost to restore, and their effect on remote users.

---

### How the two operations differ

| Operation | Layer controlled | Keeps the Track object | Requires publishing again | Use cases |
| --- | --- | --- | --- | --- |
| `mute()` / `unmute()` | Track output layer | Yes | No | Temporarily mute, temporarily turn off video |
| `unpublishLocalTrack(...)` | Channel publishing layer | Usually no | Yes | Stop publishing entirely, leave the stage |

In the Swift SDK, however, `mute()` has a further difference in meaning depending on the track type.

---

### Microphone track: `mute()` is a lightweight operation

`mute()` on a `LocalMicTrack` doesn't destroy the track object and doesn't require you to publish again.

Typical flow:

```swift
let micTrack = srtc.createLocalMicTrack(preset: .music)
try await micTrack.startCapture()
try await channel.publishLocalTrack(micTrack)

// Temporarily mute
micTrack.mute()

// Restore
micTrack.unmute()
```

This approach suits:

+ A "mute / unmute" button in a meeting app
+ A host briefly muting their microphone
+ Scenarios that need fast toggling without interrupting the audio session as much as possible

The reason is that local audio in the current Swift SDK goes through an internal mixing model. Muting a `LocalMicTrack` essentially silences the microphone input in the mixed output, rather than tearing down the whole publishing pipeline.

---

### Camera and screen sharing: `mute()` keeps the track published but stops capture

`mute()` / `unmute()` on `LocalCameraTrack` and `LocalScreenTrack` are `async`, which is an important signal: they aren't a pure in-memory flag, but involve the capture lifecycle.

```swift
let cameraTrack = srtc.createLocalCameraTrack(preset: .h720p)
try await cameraTrack.startCapture()
try await channel.publishLocalTrack(cameraTrack)

// Temporarily turn off video
try await cameraTrack.mute()

// Restore video
try await cameraTrack.unmute()
```

The key points here:

+ The track object still exists
+ You don't need to call `publishLocalTrack(...)` again
+ But capture stops, and it restarts when you restore

So it suits:

+ The user temporarily turns off the camera, but the UI still keeps "this video track"
+ Screen sharing is paused temporarily and then resumes sharing the same content

---

### `unpublishLocalTrack(...)` removes the track at the publishing layer

If you want remote users to no longer see this track from the channel's point of view, unpublish it:

```swift
try await channel.unpublishLocalTrack(cameraTrack)
try await cameraTrack.stopCapture()
```

To restore it, we usually recommend creating the track again or restarting capture, then publishing:

```swift
let newCameraTrack = srtc.createLocalCameraTrack(preset: .h720p)
try await newCameraTrack.startCapture()
try await channel.publishLocalTrack(newCameraTrack)
```

This suits:

+ The user actually leaves the speaker slot / video slot
+ Stopping screen sharing and releasing that track
+ Your business logic needs the track info removed from remote users' user lists

---

### Recommendations

#### Microphone button

+ Regular mute button: prefer `mute()` / `unmute()`
+ Cleanup before the user leaves the channel: call `srtc.leaveChannel()` directly; the SDK stops capture and unpublishes internally

#### Camera button

+ Temporarily turn off video and restore it later: use `mute()` / `unmute()`
+ Fully turn off the camera and have remote users remove the track: use `unpublishLocalTrack(...)` + `stopCapture()`

#### Screen-sharing button

+ Stop sharing briefly and then continue the current session: you can use `mute()` / `unmute()`
+ End sharing and clean up resources: use `unpublishLocalTrack(...)` + `stopCapture()`

---

### A practical rule of thumb

If you don't want to go through the full publishing flow again when the user turns it back on, prefer `mute()`.

If your goal is "make this stream disappear from the channel entirely", prefer `unpublishLocalTrack(...)`.
