---
title: "Key concepts"
description: "The SRTC Swift SDK object model: SRTCEngine vs. Channel, local and remote track types, the default audio mix mode, create/capture/publish steps for video, the three rendering options, DeviceManager, and the ChannelDelegate / TrackDelegate event model. Read before using the Swift API reference."
---

### Overall model

The Swift SDK's object model can be summarized as:

+ `SRTCEngine`: the main SDK entry point, responsible for joining channels and creating local tracks
+ `Channel`: an actual channel connection, responsible for publishing, subscribing, the user list, and event dispatch
+ `Track`: the abstraction of an audio or video stream
+ `ChannelDelegate` / `TrackDelegate`: entry points for event callbacks
+ `SRTCVideoView` / `VideoView` / `SRTCVideoRenderer`: the video rendering layer

At its core, an RTC system synchronizes three kinds of state:

+ Connection state
+ User state
+ Media track state

The Swift SDK's API is designed around these three kinds of state, so once you understand this model, most APIs become intuitive.

---

### SRTCEngine and Channel

#### `SRTCEngine`

`SRTCEngine` works more like a "factory + entry point for joining". You typically use it for two things:

+ `joinChannel(token:options:)`
+ `createLocalMicTrack(...)` / `createLocalCameraTrack(...)` / `createLocalScreenTrack(...)`

#### `Channel`

After you join a channel, `Channel` is what actually holds the channel's state:

+ Publish local tracks
+ Subscribe to remote tracks
+ Get channel info and user info
+ Listen for users joining and leaving, track changes, disconnects and reconnects, and custom messages

Think of it as "an RTC session that has completed authentication and network connection".

`joinChannel` can be called multiple times—one engine can join multiple channels at the same time, and each channel's publishing, subscriptions, users, and events
are independent of each other; `srtc.channels` is the list of currently live channels. **Tracks belong to the engine, not to a channel**: the same capture track
can be published to multiple channels, capture happens only once, and cleanup is handled by the last releaser. Publishing **audio** to multiple channels at the same time has one
hard constraint (the set of audio sources must be the same in every channel)—see [Multi-channel](/en/rtc/swift/advanced/multi-channel).

---

### Track system

#### Local tracks

| Type | How to create | Description |
| --- | --- | --- |
| `LocalMicTrack` | `srtc.createLocalMicTrack(...)` | Microphone capture |
| `LocalCameraTrack` | `srtc.createLocalCameraTrack(...)` | Camera capture |
| `LocalScreenTrack` | `srtc.createLocalScreenTrack(...)` | Screen sharing |
| `LocalAudioTrack` | `srtc.createLocalCustomAudioTrack(...)` | Custom audio injection |
| `LocalVideoTrack` | `srtc.createLocalCustomVideoTrack(...)` | Custom video frame injection |

#### Remote tracks

| Type | How to get | Description |
| --- | --- | --- |
| `RemoteAudioTrack` | `channel.getRemoteTrack(...)` | A single remote audio track |
| `RemoteAudioMixTrack` | A kind of remote audio track | Channel-wide mixed audio track |
| `RemoteVideoTrack` | `channel.getRemoteTrack(...)` | Remote video |

---

### Audio mix mode

A key implementation detail of the current Swift SDK: **local audio is sent in mix mode by default**.

This means:

+ The microphone, custom audio, and screen audio first go into the internal `AudioMixer`
+ What the PeerConnection actually sends is a single internal `audio_mix` audio track
+ Your code can still control creation, muting, and stopping capture of each audio source separately

The reasons for this design:

+ It reduces the complexity of publishing multiple audio tracks concurrently
+ Custom audio, the microphone, and screen audio share one sending model
+ It stays consistent with the existing rtc-js architecture

---

### Video capture and publishing

A video track's lifecycle usually has three steps:

```swift
let track = srtc.createLocalCameraTrack(preset: .h720p)
try await track.startCapture()
try await channel.publishLocalTrack(track)
```

Separating the three steps gives you these benefits:

+ You can preview locally first, then decide whether to publish
+ You can control hardware capture and network sending independently
+ When a permission failure or device switch failure occurs, the state is easier to pinpoint

---

### Video rendering

The SDK provides three common rendering entry points:

#### `SRTCVideoView`

A SwiftUI component, best for rendering directly in a view:

```swift
SRTCVideoView(track: track)
    .frame(width: 320, height: 180)
```

#### `VideoView`

For UIKit / AppKit; use `bind(track:)` to manage binding.

#### `SRTCVideoRenderer`

A lower-level rendering view, bound by the track itself calling `addRenderer(...)` / `removeRenderer(...)`.

---

### Device management

`DeviceManager.shared` handles device enumeration and device change monitoring:

+ Enumerate cameras: `cameras()`
+ Enumerate microphones / speakers on macOS: `microphones()`, `speakers()`
+ Enumerate audio routes on iOS: `audioRoutes()`
+ Monitor device hot-plugging and audio session interruptions: `DeviceManagerDelegate`

If your app needs a device picker, build a UI layer directly on top of `DeviceManager` rather than writing your own platform-specific handling.

---

### Event model

Channel-level events go through `ChannelDelegate`:

+ Join succeeded
+ Reconnect / disconnect
+ User joined, left, or updated
+ Remote track added, updated, or removed
+ Custom messages

Track-level events go through `TrackDelegate`:

+ Track info changes
+ Mute / unmute
+ Capture ended
+ Underlying WebRTC track binding completed

For the full event list, see [Events](/en/rtc/swift/events).

---

### Further reading

+ [Mute vs. unpublish](/en/rtc/swift/advanced/mute-vs-unpublish)
+ [Device management](/en/rtc/swift/advanced/device-management)
+ [Screen sharing](/en/rtc/swift/advanced/screen-sharing)
+ [Multi-channel](/en/rtc/swift/advanced/multi-channel)
+ [Custom tracks](/en/rtc/swift/advanced/custom-track)
