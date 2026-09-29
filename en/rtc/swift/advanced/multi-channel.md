---
title: "Multi-channel"
description: "Join multiple channels at once with the SRTC Swift SDK: joining and leaving each Channel, how engine-level tracks are reused across channels, when capture is released, the hard constraint on publishing audio to multiple channels, and per-channel events."
---

One `SRTCEngine` can join multiple channels at the same time. Typical scenarios are use cases like "main session + group discussions" that need to listen to
two streams at once, or publishing one camera to two channels at the same time.

### Join and leave

`joinChannel` can be called multiple times, and each call returns an independent `Channel`:

```swift
let main = try await srtc.joinChannel(token: mainToken)
let group = try await srtc.joinChannel(token: groupToken)

srtc.channels          // [main, group], ordered by join time
srtc.defaultChannel    // main (the earliest-joined one that's still live)
```

Joining the same channel name twice throws `SRTCError.alreadyJoined`—this also applies while a join is in progress, so you never get two
`Channel` objects pointing to the same channel.

We recommend specifying explicitly which channel to leave:

```swift
await group.leave()            // Or srtc.leaveChannel(group)
await srtc.leaveChannel()      // The no-argument version applies to defaultChannel
```

The no-argument version of `leaveChannel()` applies only to the default channel; after you leave the default channel, the next one takes its place. Single-channel users
never notice this rule, but with multiple channels we recommend not relying on it and naming the channel to leave directly.

Publishing, subscribing, the user list, event callbacks, and leaving all happen on each `Channel` independently, without interfering with each other.

---

### Tracks are engine-level objects and can be published to multiple channels

Tracks created with `createLocalXxxTrack` belong to the engine rather than to a particular channel, so the same track can be published to multiple channels:

```swift
let camera = srtc.createLocalCameraTrack(preset: .h720p)
try await camera.startCapture()

try await main.publishLocalTrack(camera)
try await group.publishLocalTrack(camera)   // One capture, sent separately by each channel
```

This captures only once and encodes separately per channel, without opening the camera twice.

**Capture release follows "the last releaser is responsible"**: when you unpublish or leave one of the channels, as long as the track is still
published by another live channel, the SDK doesn't stop capture; only when the last holder releases it does it actually
`stopCapture()`. So in the code below, `main`'s video isn't interrupted after leaving `group`:

```swift
await group.leave()      // camera is still published by main → capture continues
await main.leave()        // Last holder → capture stops automatically
```

Screen sharing works the same way. iOS full-screen capture (Broadcast Extension) is itself exclusive at the process level: one screen track corresponds to
one broadcast, and publishing it to multiple channels still uses only one capture.

---

### Hard constraint on publishing audio to multiple channels

<Warning>
When multiple channels **publish** audio at the same time, the set of audio sources published in each channel must be **exactly the same**; otherwise
`publishLocalTrack` throws `SRTCError.invalidState`.
</Warning>

The reason lies in the audio pipeline: the whole process has only one audio device module and one mix, so the audio tracks of all channels get **the same
mixed result**. If channel A publishes only the microphone while channel B publishes the microphone + screen audio, then this global mix contains
the screen audio, and A's subscribers also hear what B is sharing—something A has no way to anticipate from the API semantics. This is cross-channel
audio leakage, so the SDK blocks it at the publishing entry point.

Identical sets give predictable behavior: both channels send the same content. So the most common usage is allowed:

```swift
let mic = srtc.createLocalMicTrack()
try await mic.startCapture()

try await main.publishLocalTrack(mic)
try await group.publishLocalTrack(mic)     // ✅ The audio source set of both channels is {mic}
```

But the following is rejected:

```swift
try await main.publishLocalTrack(mic)                    // {mic}
try await group.publishLocalTrack(mic)                   // {mic}
try await group.publishLocalTrack(screenTrack)           // ❌ group becomes {mic, screen_audio}
// SRTCError.invalidState: the audio sources published in each channel must be exactly the same
```

Either have both channels publish the same audio sources, or unpublish audio in the other channel first.

**The subscribing side has no restrictions**: any channel can subscribe to remote audio normally. Downlink audio is mixed by WebRTC itself and is unrelated to the constraint above.

---

### Events

Each `Channel` has its own delegate list; delegates registered on a channel receive only that channel's events:

```swift
main.delegates.add(delegate: mainHandler)
group.delegates.add(delegate: groupHandler)
```

Track-level events (`TrackDelegate`) are registered on the track, so a track shared across channels only needs to be registered once.

---

### FAQ

#### Does multi-channel open the camera / microphone multiple times?

No. Capture is engine-level; multiple channels share the same capture, and the hardware is opened only once.

#### After leaving one channel, the other channel's video goes black?

Normally this doesn't happen—capture release is handled by "the last releaser". If it does happen, check whether you created a separate track for each of the two channels
(which means two captures, unrelated to each other) instead of reusing the same one.

#### Can two channels send different audio?

Not currently, for the reason explained in the mixing constraint above. If your scenario needs this capability, contact us; it depends on support for a direct publishing path.
