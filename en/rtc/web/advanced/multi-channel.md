---
title: "Multi-channel"
description: "Join multiple channels at once with the Web SDK: using the Channel object returned by join, isolating events per channel, the default-channel rule for single-channel code, publishing one captured track to several channels, and how capture is released on leave."
---

### Overview

The Web SDK lets one SRTC instance **join multiple channels at the same time**. A typical scenario: while sending and receiving audio and video in a main call channel, also join a voice intercom channel to send and receive intercom audio separately.

```typescript
const meeting = await srtc.join(meetingToken);   // Main call channel
const intercom = await srtc.join(intercomToken); // Intercom channel, running in parallel

await meeting.publishLocalTrack(cameraTrack);
await intercom.publishLocalTrack(micTrack);

await intercom.leave();   // Leave the intercom; the main call is unaffected
```

The return value of `join` is the channel handle (the Channel object). Publishing, subscribing, querying users, listening for events, and leaving all happen on it, and multiple channels don't interfere with each other.

### Channel object

The channel-level methods on the Channel object have **exactly the same semantics** as the methods of the same name on the `srtc` instance (for parameters and return values, see the [SRTC API reference](/en/rtc/web/api-reference/SRTC)); the only difference is that the target changes from "the current channel" to this specific channel:

| Category | Methods |
| --- | --- |
| Info queries | `getInfo()`, `getUsersInfo(map)` |
| Publishing | `publishLocalTrack(track, opt?)`, `unpublishLocalTrack(track)`, `getPublishInfo(track)` |
| Subscribing | `subscribeRemoteAudioMixTrack` / `subscribeRemoteAudioTrack` / `subscribeRemoteVideoTrack` / `subscribeRemoteVideoMcuTrack` / `unsubscribeRemoteTrack` |
| Quality statistics | `getStreamMetric()`, `getNetworkStats()`, `getConnectionQuality()` |
| Events | `onNotifyEvent` callback property, `on()` / `once()` / `off()` typed listeners |
| Leaving | `leave()` |

The Channel object can only be created by `srtc.join()`; `new` isn't allowed.

### Per-channel event isolation

Each channel's events are emitted on its own Channel object. Use either approach:

```typescript
// Option 1: callback property (the same discriminated union as srtc.onNotifyChannelEvent)
intercom.onNotifyEvent = (evt) => {
  switch (evt.type) {
    case ChannelEventType.USER_TRACK_ADD:
      // Only receives events from the intercom channel
      break;
  }
};

// Option 2: typed listener for a single event
meeting.on(ChannelEventType.CONNECTION_QUALITY_CHANGED, (evt) => { ... });
```

`srtc.onNotifyChannelEvent` still works: it receives channel events of the **default channel** (see the next section), plus device-level events unrelated to any channel, such as devices being plugged in or unplugged. In multi-channel apps, we recommend handling all channel events through `channel.onNotifyEvent` and leaving `srtc.onNotifyChannelEvent` for device-level events only.

### Single-channel compatibility: the default channel rule

The channel-level methods on the `srtc` instance (`publishLocalTrack`, `subscribe*`, `getChannelInfo`, `leave`, etc.) internally act on the **default channel**—the earliest-joined channel that you're still in; when you leave it, the next one takes over.

When you join only one channel, the default channel is always that channel, so all existing single-channel code behaves the same. Once you join multiple channels, we recommend no longer relying on these convenience methods and using each Channel object explicitly, to avoid ambiguity from the default channel moving to the next one.

### Publishing one captured track to multiple channels

The same local track can be published to multiple channels at once. There's only one capture, while encoding and publishing are independent per channel:

```typescript
const mic = srtc.createLocalMicTrack();
await meeting.publishLocalTrack(mic);
await intercom.publishLocalTrack(mic);
```

Once published to multiple channels, the track has **separate track info in each channel** (the track id assigned by the server, encoding parameters, and so on all differ). In that case:

- `track.getInfo()` **throws**—it can't answer "the info in which channel";
- Use `channel.getPublishInfo(track)` instead to query the track description in a given channel;
- When published to only one channel, `track.getInfo()` behaves as before, so no changes are needed.

```typescript
const infoInMeeting = meeting.getPublishInfo(mic);   // Track id etc. in the main call channel
const infoInIntercom = intercom.getPublishInfo(mic); // A separate copy in the intercom channel
```

### Releasing capture resources

When you leave, the SDK releases capture based on "whether any channel is still using it":

- `leave()` on one channel: only stops capture of local tracks that "were published in that channel and are no longer published in any channel"; tracks still published by other channels keep capturing and publishing.
- Leaving the last channel: releases all local tracks created by the SRTC instance (the same behavior as in the single-channel era).

So in the example above, `intercom.leave()` doesn't stop the mic capture (the main call is still using it); capture stops only after you leave both channels.

### Releasing the instance

When you no longer need the SRTC instance (the SPA route changes, the component unmounts, or you're about to recreate the instance), call `srtc.destroy()` to leave all channels, disable IM, and remove global listeners in one go. See [destroy](/en/rtc/web/api-reference/SRTC#destroy).
