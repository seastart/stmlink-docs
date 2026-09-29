---
title: "RTCClientEvent"
description: "Android per-channel control events: join results, user and track changes, channel property updates, in-channel custom messages, disconnects, and reconnection. Every event that belongs to a channel carries the channel ID. Read when handling channel callbacks on Android."
---

`RTCClientEvent` carries the channel control events of one channel. The first listener must be passed through `RTCEngine.join(..., clientEvent, ...)`; after the join succeeds, you can replace or unbind it with `RTCChannel.setRtcClientEvent(...)`.

If you only care about a few events, extend `RTCClientSimpleEvent`, which provides empty implementations.

## Join results

### onJoinSucceed(channel, uid, whiteBoard)

```kotlin
fun onJoinSucceed(channel: String, uid: String, whiteBoard: String?)
```

You joined the channel successfully. `channel` is the channel ID, `uid` is the current user ID, and `whiteBoard` is the nullable whiteboard URL or info. Treat this callback as the signal that the join actually succeeded.

### onJoinFailed(channel, statusCode)

```kotlin
fun onJoinFailed(channel: String?, statusCode: Int)
```

You failed to join the channel. `channel` has a value when the channel ID can be parsed from the token, otherwise it's `null`; for `statusCode`, see [Error codes](/en/rtc/android/error-codes).

## User events

### onUserUpdate(channel, uid)

```kotlin
fun onUserUpdate(channel: String, uid: String)
```

Your own user info was updated.

### onMeMembershipChanged(channel, isMember)

```kotlin
fun onMeMembershipChanged(channel: String, isMember: Boolean)
```

Your role changed between audience and full member. `isMember = true` means you were promoted to a full member, and `false` means you were demoted to audience; read your initial role at join time with `isAudience()` on the corresponding channel.

### onRemoteUserJoin(channel, uid)

```kotlin
fun onRemoteUserJoin(channel: String, uid: String)
```

A remote user joined the channel.

### onRemoteUserLeave(channel, userInfo, leaveReason)

```kotlin
fun onRemoteUserLeave(
    channel: String,
    userInfo: UserInfo,
    leaveReason: LeaveReason
)
```

A remote user left the channel. `userInfo` is the last snapshot of the leaving user's info.

### onRemoteUserUpdate(channel, uid)

```kotlin
fun onRemoteUserUpdate(channel: String, uid: String)
```

A remote user's info was updated.

## Track and channel events

### onStreamTrackAdd(uid, channel, trackId, trackDesc)

```kotlin
fun onStreamTrackAdd(
    uid: String,
    channel: String,
    trackId: String,
    trackDesc: String
)
```

A remote track was added. Use the `RTCChannel` of the same channel to get and subscribe to the remote track.

### onStreamTrackUpdate(uid, channel, trackId, trackDesc)

```kotlin
fun onStreamTrackUpdate(
    uid: String,
    channel: String,
    trackId: String,
    trackDesc: String
)
```

A remote track's info was updated.

### onStreamTrackRemove(uid, channel, trackInfo)

```kotlin
fun onStreamTrackRemove(
    uid: String,
    channel: String,
    trackInfo: TrackInfo
)
```

A remote track was removed. For `TrackInfo` fields, see [Types](/en/rtc/android/types).

### onChannelUpdate(channel, props)

```kotlin
fun onChannelUpdate(channel: String, props: String?)
```

Channel properties were updated; `props` may be `null`.

### onCustomMessage(channel, uid, sid, name, action, content)

```kotlin
fun onCustomMessage(
    channel: String,
    uid: String,
    sid: String,
    name: String,
    action: String,
    content: String
)
```

An in-channel custom message was received. `channel` is the channel the message belongs to; the other parameters are, in order, the sender's user ID, session ID, name, action identifier, and message content.

## Connection events

### onDisconnected(channel, leaveReason, statusCode, message)

```kotlin
fun onDisconnected(
    channel: String,
    leaveReason: LeaveReason,
    statusCode: Int,
    message: String
)
```

An unrecoverable disconnect occurred in the channel. You need to call `join(...)` again for this channel; other channels aren't affected.

### onReconnected(channel)

```kotlin
fun onReconnected(channel: String)
```

The channel reconnected successfully after a disconnect.

### onReconnecting(channel)

```kotlin
fun onReconnecting(channel: String)
```

The channel connection dropped and automatic reconnection started.

:::note
The former `RTCClientEvent.onError(...)` has been removed. Engine-blocking operations and global errors are all reported by [`RTCEngineEvent.onError(...)`](/en/rtc/android/api-reference/RTCEngineEvent).
:::
