---
title: "Events"
description: "Full list of Web SDK events and when they fire: in-channel events via onNotifyChannelEvent (channel and connection, remote users and tracks, tracks and devices, network quality and active speakers) and out-of-channel IM events via onNotifyImEvent, with string values and data types."
---

### In-channel events (onNotifyChannelEvent)

Register a callback with `srtc.onNotifyChannelEvent`; we recommend setting it before `join`:

```typescript
srtc.onNotifyChannelEvent = (evt: ChannelEvent) => {
  switch (evt.type) {
    case ChannelEventType.USER_JOIN:
      // evt.data
      break;
    case ChannelEventType.TRACK_PIP_ENTER:
      // evt.data
      break;
  }
};
```

`ChannelEvent` and `ImEvent` are both discriminated unions at the type level: when you branch with `switch (evt.type)`, `evt.data` is automatically narrowed to the data structure for that event type. If you only use them for type annotations in TypeScript, we recommend importing them with `import type`.

---

#### Channel and connection

| Event constant | String value | When it fires | `data` type |
| --- | --- | --- | --- |
| `JOIN_SUCCEED` | `'join_succeed'` | Joined the channel successfully for the first time | `ChannelInfo` |
| `CHANNEL_UPDATE` | `'channel_update'` | The channel's custom properties `props` were updated | `ChannelInfo` |
| `ME_UPDATE` | `'me_update'` | Your own user info was updated by the server | `UserInfo` |
| `RECONNECTING` | `'reconnecting'` | Network fluctuation; automatic reconnection started | None |
| `RECONNECTED` | `'reconnected'` | Automatic reconnection succeeded | None |
| `DISCONNECTED` | `'disconnected'` | Forcibly removed from the channel, or an unrecoverable error occurred | `DisconnectEventData` |
| `CUSTOM_MSG` | `'custom_msg'` | Received an in-channel custom message | `CustomMsgData` |

---

#### Remote users and tracks

| Event constant | String value | When it fires | `data` type |
| --- | --- | --- | --- |
| `USER_JOIN` | `'user_join'` | A remote user joined the channel | `UserInfo` |
| `USER_UPDATE` | `'user_update'` | A remote user's info was updated | `UserInfo` |
| `USER_LEAVE` | `'user_leave'` | A remote user left the channel | `UserLeaveEventData` |
| `USER_TRACK_ADD` | `'user_track_add'` | A remote user published a new track | `{ user: UserInfo, track: TrackInfo }` |
| `USER_TRACK_UPDATE` | `'user_track_update'` | A remote user updated track info | `{ user: UserInfo, track: TrackInfo }` |
| `USER_TRACK_REMOVE` | `'user_track_remove'` | A remote user unpublished a track | `{ user: UserInfo, track: TrackInfo }` |

> When a remote user leaves, the SDK automatically unsubscribes from all of that user's tracks; on `USER_TRACK_REMOVE`, it automatically unsubscribes from the corresponding track.

---

#### Tracks and devices

| Event constant | String value | When it fires | `data` type |
| --- | --- | --- | --- |
| `TRACK_MUTED` | `'track_muted'` | A track paused sending data | `BaseTrack` |
| `TRACK_UNMUTED` | `'track_unmuted'` | A track resumed sending data | `BaseTrack` |
| `TRACK_ENDED` | `'track_ended'` | A track stopped, e.g., a device was unplugged or the user clicked the browser's "Stop sharing" | `BaseTrack` |
| `TRACK_AUTOPLAY_FAIL` | `'track_autoplay_fail'` | The browser blocked autoplay; call `startPlay` again after a user gesture | `BaseTrack` |
| `TRACK_PIP_ENTER` | `'track_pip_enter'` | A video track entered picture-in-picture mode | `BaseTrack` |
| `TRACK_PIP_EXIT` | `'track_pip_exit'` | A video track exited picture-in-picture mode | `BaseTrack` |
| `TRACK_POPOUT_OPEN` | `'track_popout_open'` | A video track popped out to a separate window | `BaseTrack` |
| `TRACK_POPOUT_CLOSE` | `'track_popout_close'` | A video track closed its separate window | `BaseTrack` |
| `DEVICE_ADD` | `'device_add'` | A device was plugged in | `MediaDeviceInfo` |
| `DEVICE_REMOVE` | `'device_remove'` | A device was unplugged | `MediaDeviceInfo` |

---

#### Network quality and active speakers

| Event constant | String value | When it fires | `data` type |
| --- | --- | --- | --- |
| `CONNECTION_QUALITY_CHANGED` | `'connection_quality_changed'` | The connection quality level changed | `ConnectionQualityEventData` |
| `CPU_CONSTRAINED` | `'cpu_constrained'` | The sender is persistently CPU-limited | `QualityEvaluation` |
| `BANDWIDTH_CONSTRAINED` | `'bandwidth_constrained'` | The sender is persistently bandwidth-limited | `QualityEvaluation` |
| `ACTIVE_SPEAKERS_CHANGED` | `'active_speakers_changed'` | The current active speaker list changed; only supported by the SeaStart SFU | `ActiveSpeakersEventData` |

`data.speakers` of `ACTIVE_SPEAKERS_CHANGED` is a full snapshot of the users currently speaking, sorted by `level` from high to low; when nobody is speaking it's an empty array. Your app can overwrite the UI state directly, without merging increments yourself.

---

### Out-of-channel message events (onNotifyImEvent)

Register a callback with `srtc.onNotifyImEvent`; call `srtc.enableIm(token)` first:

```typescript
srtc.onNotifyImEvent = (evt: ImEvent) => {
  switch (evt.type) {
    case ImEventType.IM_MSG:
      // evt.data
      break;
  }
};
```

| Event constant | String value | When it fires | `data` type |
| --- | --- | --- | --- |
| `ENABLE_SUCCEED` | `'enable_succeed'` | IM connected successfully for the first time | None |
| `IM_MSG` | `'im_msg'` | Received an IM message | `ImMsgData` |
| `RECONNECTING` | `'reconnecting'` | IM connection dropped; reconnection started | None |
| `RECONNECTED` | `'reconnected'` | IM reconnected successfully | None |
| `DISCONNECTED` | `'disconnected'` | IM was forcibly disconnected | `ImDisconnectEventData` |
