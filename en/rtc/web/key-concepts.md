---
title: "Key concepts"
description: "Core model of the SRTC Web SDK: the SRTC instance and the Channel returned by join, tokens, the track class hierarchy and how each track is created, the local track lifecycle, channel and IM event callbacks, and audience mode. Read before writing code beyond the quickstart."
---

### SRTC instance

Create an instance with `new SRTC(initParams)`; almost all operations are exposed through this instance.

+ One instance can call `join` multiple times to join several channels at once; each `join` returns that channel's Channel object
+ In-channel events are delivered through the `srtc.onNotifyChannelEvent` callback; with multiple channels, use each channel's `channel.onNotifyEvent` to tell them apart. See [Multi-channel](/en/rtc/web/advanced/multi-channel)

```typescript
import { SRTC, LogLevel, LogTarget } from '@seastart/srtc-web-sdk';

const srtc = new SRTC({
  logLevel: LogLevel.DEBUG,   // DEBUG is recommended during development
  logTarget: LogTarget.CONSOLE,
});
```

---

### Channel and token

A **channel** is the container for a multi-user audio and video session, uniquely identified by its channel name. Users who join the same channel can send and receive audio and video streams with each other.

A **token** is the credential for joining a channel. Your server issues it through the STMLink server API, and it carries the channel name, user ID, permissions, and other information. Every join requires a valid token.

```typescript
// After getting the token from your backend, call join; it returns a Channel object
const channel = await srtc.join(token);
console.log(channel.getInfo().channel); // Channel name
```

You can perform channel-level operations such as publishing, subscribing, and leaving directly on the **Channel object** returned by `join`. Single-channel apps don't need to care about it—the `srtc` instance keeps all channel-level methods (internally acting on the current channel); you only need it to specify the target when you join multiple channels at once. See [Multi-channel](/en/rtc/web/advanced/multi-channel).

After joining, you can get channel and user information at any time with these methods:

```typescript
// Get the current channel's info
const channelInfo = srtc.getChannelInfo();

// Get info for a user in the channel
const userInfo = srtc.getUserInfo(uid);

// Get all users in the channel (as a map)
const usersMap = srtc.getUsersInfo(true);   // Record<uid, UserInfo>

// Get all users in the channel (as an array)
const usersArr = srtc.getUsersInfo(false);  // UserInfo[]
```

---

### Track system

A track is the smallest unit of audio and video data; each audio or video stream is a track.

#### Class hierarchy

```text
BaseTrack
├── LocalAudioTrack          ← Local audio base class (custom audio stream)
│   └── LocalMicTrack        ← Microphone stream
├── LocalVideoTrack          ← Local video base class (custom video stream)
│   ├── LocalCameraTrack     ← Camera stream
│   └── LocalScreenTrack     ← Screen sharing stream
├── RemoteAudioTrack         ← Single remote audio stream
│   └── RemoteAudioMixTrack  ← Remote channel-wide mixed audio stream
└── RemoteVideoTrack         ← Remote video stream
```

#### Track types

| Track type | How to create | Description |
| --- | --- | --- |
| `LocalMicTrack` | `srtc.createLocalMicTrack()` | Microphone capture, supports switching devices |
| `LocalCameraTrack` | `srtc.createLocalCameraTrack()` | Camera capture, supports switching devices |
| `LocalScreenTrack` | `srtc.createLocalScreenTrack()` | Screen sharing, can capture system audio at the same time |
| `LocalAudioTrack` | `srtc.createLocalCustomAudioTrack(msTrack)` | Custom audio, pass in a `MediaStreamTrack` |
| `LocalVideoTrack` | `srtc.createLocalCustomVideoTrack(msTrack)` | Custom video, pass in a `MediaStreamTrack` |
| `RemoteAudioMixTrack` | `srtc.subscribeRemoteAudioMixTrack()` | Channel-wide mixed audio; in most scenarios this is the only audio you need to subscribe to |
| `RemoteAudioTrack` | `srtc.subscribeRemoteAudioTrack(uid, id)` | Subscribe to a single audio track of a given user |
| `RemoteVideoTrack` | `srtc.subscribeRemoteVideoTrack(uid, id)` | Subscribe to a given user's video |

#### Local track lifecycle

```text
createLocalXxxTrack()
  → startCapture()        // Start capture (requests camera/microphone permission)
  → publishLocalTrack()   // Publish to the channel (other users can subscribe)
  → unpublishLocalTrack() // Unpublish (other users can't see it, but local capture continues)
  → stopCapture()         // Stop capture and release the device
```

---

### Event system

SRTC provides two sets of event callbacks:

#### In-channel events (onNotifyChannelEvent)

Listen for channel connection state, remote users joining and leaving, remote track changes, local device state, and more:

```typescript
srtc.onNotifyChannelEvent = (evt: ChannelEvent) => {
  switch (evt.type) {
    case ChannelEventType.USER_JOIN:
      // A remote user joined; evt.data is UserInfo
      break;
    case ChannelEventType.USER_TRACK_ADD:
      // A remote user published a new track; evt.data is { user: UserInfo, track: TrackInfo }
      break;
    // ... for more events, see "Events"
  }
};
```

#### Out-of-channel message events (onNotifyImEvent)

Listen for IM messages (call `srtc.enableIm(token)` first to enable IM):

```typescript
srtc.onNotifyImEvent = (evt: ImEvent) => {
  if (evt.type === ImEventType.IM_MSG) {
    // evt.data is ImMsgData
  }
};
```

For the full event list, see [Events](/en/rtc/web/events).

---

### Audience mode (is_audience)

When `UserInfo.is_audience` is `true`, the user has joined the channel as an audience member:

+ Audience members only receive audio and video streams and **can't publish** local tracks
+ Whether a user joins as audience is decided when the server issues the token
+ Use the `ChannelEventType.ME_UPDATE` event to detect changes to your own audience status
