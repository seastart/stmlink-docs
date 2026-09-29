---
title: "Mute vs. unpublish"
description: "Compare the lightweight enableLocalTrack / disableLocalTrack (mute) with the heavyweight publishLocalTrack / unpublishLocalTrack in the Web SDK: underlying behavior, remote events, latency, and which to use for mute buttons, stopping screen sharing, and turning off the camera."
---

### Overview

There are two operations of different granularity for controlling local audio and video publishing. Picking the wrong one causes unnecessary resource waste or broken behavior:

| | `enableLocalTrack` / `disableLocalTrack` | `unpublishLocalTrack` / `publishLocalTrack` |
| --- | --- | --- |
| Acts on | A published track | The whole publishing pipeline |
| Underlying behavior | Pauses/resumes sending media data; the connection stays up | Destroys/rebuilds the publishing path |
| Effect on remote users | Remote users receive the `TRACK_MUTED` / `TRACK_UNMUTED` event | Remote users receive the `USER_TRACK_REMOVE` / `USER_TRACK_ADD` event |
| Time taken | Very fast (< 10 ms) | Slower (requires renegotiation, ~100 ms+) |
| Typical scenario | Temporarily mute, temporarily turn off video | Stop publishing entirely (e.g., leaving the stage) |

---

### enableLocalTrack / disableLocalTrack

These two methods only control **sending of media data**; the underlying WebRTC connection stays up. They suit scenarios where you need to toggle mute/unmute quickly.

```typescript
import { SRTC, LocalMicTrack, MicPresets } from '@seastart/srtc-web-sdk';

const srtc = new SRTC();
// Assume you have joined the channel and localMicTrack is published
let localMicTrack: LocalMicTrack;

// Create and publish the microphone track
localMicTrack = srtc.createLocalMicTrack(MicPresets.music);
await localMicTrack.startCapture();
await srtc.publishLocalTrack(localMicTrack);

// ── Temporarily mute (capture continues, publishing isn't torn down) ──────────
await srtc.disableLocalTrack(localMicTrack);
// Remote users receive the ChannelEventType.TRACK_MUTED event

// ── Unmute ────────────────────────────────────────────────────────────────────
await srtc.enableLocalTrack(localMicTrack);
// Remote users receive the ChannelEventType.TRACK_UNMUTED event
```

> **Note:** After `disableLocalTrack`, microphone capture continues (the indicator stays on); it just stops pushing data to the channel.
> If you want to stop capture entirely to release the microphone, use `unpublishLocalTrack` + `stopCapture`.

---

### unpublishLocalTrack / publishLocalTrack

Stops/restarts publishing entirely, which fires the `USER_TRACK_REMOVE` / `USER_TRACK_ADD` events on the remote side. Suitable for scenarios such as a user leaving the stage or "Stop sharing" during a call.

```typescript
// ── Unpublish (stop publishing entirely) ──────────────────────────────────────
await srtc.unpublishLocalTrack(localMicTrack);
localMicTrack.stopCapture();
localMicTrack = undefined;

// ── Publish again (requires creating the track again) ─────────────────────────
localMicTrack = srtc.createLocalMicTrack(MicPresets.music);
await localMicTrack.startCapture();
await srtc.publishLocalTrack(localMicTrack);
```

<Warning>
Before publishing again, make sure the previous track with the same `desc` has finished `unpublishLocalTrack`—within one channel only one track per `desc` may be published, and publishing the same `desc` again with a different track throws.

In particular, don't let "microphone off" and "microphone on" actions interleave: if another "microphone on" is started during the await window of the previous `publishLocalTrack`, two microphone tracks publish at the same time, and you only keep a reference to the one created later. The one published first can't be unpublished and its capture can't be stopped, so the remote side keeps hearing audio. Add a serial queue or a button loading state to such entry points.
</Warning>

---

### Recommendations

+ **Microphone mute button in a call** → use `disableLocalTrack` / `enableLocalTrack` for fast response and a smooth experience
+ **Stop screen sharing** → use `unpublishLocalTrack` + `stopCapture` to release resources entirely
+ **Temporarily turn off the camera (video goes black)** → use `disableLocalTrack`
+ **Turn off the camera entirely (release the device)** → use `unpublishLocalTrack` + `stopCapture`
