---
title: "MeetingRemoteVideoEvent"
description: "Receive the receive and stutter state of a single remote video, composite stream, or Wangsu video stream, registered through the event parameter of startPlayRemoteVideo(), startPlayRemoteMixture(), or subscribeWsVideoStream(). Read this when you show per-video stutter indicators."
---

`MeetingRemoteVideoEvent` listens to a single remote video control track and is registered through the `event` parameter of `startPlayRemoteVideo()`, `startPlayRemoteMixture()`, or `subscribeWsVideoStream()`. You can extend `MeetingRemoteVideoSimpleEvent`.

## Usage notes

+ This listener is bound to a single subscribe call rather than registered globally through a `MeetingEngine` property; different remote tracks can use different listener instances.

+ Events stay on the actual SRTC callback thread and aren't switched to the main thread.
+ Meeting hides the underlying channel parameter and filters out late events from a previous meeting.
+ For a composite stream, a successful subscription only means the request has been submitted; use this event together with the rendering result to tell whether video is actually received.

## Methods

### onReceiveStreamStatusChange(uid, trackDesc, isChoke)

```kotlin
fun onReceiveStreamStatusChange(
    uid: String,
    trackDesc: String,
    isChoke: Boolean
)
```

Description: The receive or stutter state of the remote video stream changed.

Parameters:

| Parameter | Description |
| --- | --- |
| `uid` | The remote user or render route identifier used when subscribing. |
| `trackDesc` | The track description used when subscribing. |
| `isChoke` | `true` means reception is currently stuttering, `false` means it's back to normal. |

Returns: None (`Unit`).
