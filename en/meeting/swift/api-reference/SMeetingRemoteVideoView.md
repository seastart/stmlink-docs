---
title: "SMeetingRemoteVideoView"
description: "SMeetingRemoteVideoView, the SwiftUI component that renders a remote member's video and subscribes and unsubscribes automatically as the view appears and disappears: initializer parameters, behavior guarantees, and when to use other entry points instead. Read when rendering remote video in SwiftUI."
---

`SMeetingRemoteVideoView` is the SwiftUI component that renders a remote member's video. It ties "subscribe / unsubscribe" to the "view lifecycle": you just let the view appear and disappear, and the subscription follows along.

Availability: iOS 13.0+ / macOS 10.15+.

---

### `init(meeting:uid:trackDesc:)`

```swift
SMeetingRemoteVideoView(
    meeting: meeting,
    uid: user.uid,
    trackDesc: .cameraBig
)
.frame(height: 180)
```

| Parameter | Type | Required | Description |
| --- | --- | :---: | --- |
| `meeting` | `SMeetingEngine` | Yes | The SDK instance |
| `uid` | `String` | Yes | ID of the remote member to render |
| `trackDesc` | `TrackDesc` | Yes | Track description: pass `.cameraBig` for the camera and `.screen` for screen sharing |

**Returns:** A SwiftUI `View`

---

### Behavior guarantees

+ When the view appears, it subscribes by `(uid, trackDesc)`; when the view disappears, it unsubscribes
+ When `uid` or `trackDesc` changes, it automatically unsubscribes from the old one and subscribes to the new one, so you don't need to add `id(...)` to force the view to be rebuilt
+ When a layout change rebuilds the view (the old instance disappears and a new one appears right after), no redundant unsubscribe + resubscribe happens, and the video doesn't flicker or drop
+ When the same video is rendered in several places at once, closing one of them doesn't affect the others
+ Subscription completing and the underlying media arriving don't happen at the same moment; the component completes the binding automatically once the data actually arrives, so you don't need to add delays or retries
+ A failed subscription doesn't crash; the view stays blank, and the reason for the failure is written to the SDK log

---

### When not to use it

In the following cases, use a different entry point:

| Scenario | Use |
| --- | --- |
| Rendering your own camera / sharing | `SRTCVideoView(track: meeting.cameraTrack)` |
| UIKit / AppKit | `startPlayRemoteVideo(view:uid:trackDesc:)` |
| You need to separate when you subscribe from when you render | `subscribeRemoteVideoTrack(uid:trackDesc:)` |

---

### Related pages

+ [Video rendering](/en/meeting/swift/advanced/video-rendering)
+ [Media control API](/en/meeting/swift/api-reference/media-control)
