---
title: "Video rendering"
description: "Render local video, remote video, and the server-side MCU composite in SwiftUI and UIKit / AppKit with the SMeeting Swift SDK, and decide when to subscribe to remote video. Read when building the meeting's video grid or managing subscriptions yourself."
---

### Overview

Meeting video comes in three kinds, each with its own entry point:

| Video | SwiftUI | UIKit / AppKit |
| --- | --- | --- |
| Local camera / sharing | `SRTCVideoView(track:)` | Pass an `SRTCVideoRenderer` when turning it on |
| Remote camera / sharing | `SMeetingRemoteVideoView` | `startPlayRemoteVideo(view:uid:trackDesc:)` |
| Server-side composite (MCU) | Get `meeting.mcuTrack` and pass it to `SRTCVideoView` | `startPlayRemoteVideoMcu(view:uid:)` |

Local video **doesn't need a subscription**; just render the track directly. Remote video **must be subscribed first** before it has any data.

---

### Local video

#### SwiftUI

Don't pass `view` when turning on the camera; afterward, pass the track directly to `SRTCVideoView`:

```swift
try await meeting.requestOpenCamera()

if let cameraTrack = meeting.cameraTrack {
    SRTCVideoView(track: cameraTrack)
        .frame(height: 180)
}
```

Screen sharing works the same way, using `meeting.screenTrack`:

```swift
if let screenTrack = meeting.screenTrack {
    SRTCVideoView(track: screenTrack)
}
```

> `SMeetingEngine` is not an `ObservableObject`, so `cameraTrack` / `screenTrack` changing from `nil` to a value doesn't trigger a SwiftUI refresh by itself. Keep a "camera is on" flag in your own `@Published` state and let it drive view updates.

#### UIKit / AppKit

Pass the preview view when turning on the camera:

```swift
let renderer = SRTCVideoRenderer(frame: previewFrame)
containerView.addSubview(renderer)

try await meeting.requestOpenCamera(view: renderer)
```

> The `view` you pass must be an object that is actually attached to the view hierarchy. Passing a temporarily created local variable that hasn't been added to any superview leaves the rendering pipeline running with nothing to show.

---

### Remote video (SwiftUI)

`SMeetingRemoteVideoView` is the recommended entry point for SwiftUI. It handles the entire subscription lifecycle: it subscribes by `uid + trackDesc` when the view appears and unsubscribes when the view disappears.

```swift
SMeetingRemoteVideoView(
    meeting: meeting,
    uid: user.uid,
    trackDesc: .cameraBig
)
.frame(height: 180)
```

To view someone's screen sharing, change `trackDesc` to `.screen`:

```swift
SMeetingRemoteVideoView(meeting: meeting, uid: user.uid, trackDesc: .screen)
```

What the component guarantees:

+ Rendering the same `(uid, trackDesc)` in multiple places doesn't make them knock out each other's subscriptions
+ When a layout change recreates the view (the old instance disappears and a new one appears), no extra unsubscribe + resubscribe happens, so the video doesn't flicker
+ The subscription result and the arrival of the underlying media don't happen at the same moment; the component binds automatically once the data actually arrives, so you don't need delays or retries

A typical usage is rendering a grid from the member list:

```swift
ForEach(users, id: \.uid) { user in
    if user.uid == meeting.currentUserId {
        if let track = meeting.cameraTrack {
            SRTCVideoView(track: track)
        }
    } else if user.shareState == ShareType.screen.rawValue {
        SMeetingRemoteVideoView(meeting: meeting, uid: user.uid, trackDesc: .screen)
    } else if user.cameraState == .on {
        SMeetingRemoteVideoView(meeting: meeting, uid: user.uid, trackDesc: .cameraBig)
    }
}
```

---

### Remote video (UIKit / AppKit)

If you already hold an `SRTCVideoRenderer` attached to the view hierarchy, use this pair of convenience methods:

```swift
let renderer = SRTCVideoRenderer(frame: frame)
containerView.addSubview(renderer)

try await meeting.startPlayRemoteVideo(
    view: renderer,
    uid: remoteUid,
    trackDesc: .cameraBig
)

// When no longer needed
try await meeting.stopPlayRemoteVideo(
    view: renderer,
    uid: remoteUid,
    trackDesc: .cameraBig
)
```

`stopPlayRemoteVideo` removes only the one renderer view you pass in; it actually unsubscribes only when the track no longer has any renderer view. So when the same video is shown in several windows, closing one of them doesn't affect the others.

---

### Control subscriptions yourself

When you need to separate subscription timing from rendering timing (for example, pre-subscribe and then decide the layout), use the core APIs:

```swift
let track = try await meeting.subscribeRemoteVideoTrack(uid: remoteUid, trackDesc: .cameraBig)

// SwiftUI: SRTCVideoView(track: track)
// UIKit / AppKit: track.addRenderer(renderer)

try await meeting.unsubscribeRemoteVideoTrack(uid: remoteUid, trackDesc: .cameraBig)
```

Note that `unsubscribeRemoteVideoTrack` **unsubscribes unconditionally**, regardless of whether any renderer view is still using it. When rendering the same video in multiple places, use `SMeetingRemoteVideoView` or `stopPlayRemoteVideo`.

To just check whether a given track of a given member exists (without subscribing), use:

```swift
let track = meeting.getRemoteVideoTrack(uid: remoteUid, desc: .cameraBig)
```

---

### When to subscribe

Remote video is **subscribed on demand**; the SDK doesn't subscribe to everyone automatically for you. Base the decision on member state and events:

+ `MeetingUserInfo.cameraState == .on` → this member has camera video
+ `MeetingUserInfo.shareState == ShareType.screen.rawValue` → this member is sharing their screen
+ Refresh the layout when you receive `userCameraStateDidChange` or `roomShareDidStart` / `roomShareDidStop`

With `SMeetingRemoteVideoView`, you only need to make the views appear / disappear along with these states, and the subscriptions follow automatically.

---

### Server-side composite video (MCU)

When the meeting has a server-side composite task running, you can pull a single composite video instead of subscribing to members one by one:

```swift
let track = try await meeting.startPlayRemoteVideoMcu(view: renderer, uid: mcuUid)
// You can also get this track at any time through meeting.mcuTrack

try await meeting.stopPlayRemoteVideoMcu(view: renderer)
```

The composite video requires the server to set up the composite task first; the layout is controlled by `adminUpdateLayout(_:)`. See [Recording and composite layout](/en/meeting/swift/advanced/recording).

---

### Related pages

+ [Media control](/en/meeting/swift/advanced/media-control)
+ [Screen sharing](/en/meeting/swift/advanced/screen-sharing)
+ [API reference - SMeetingRemoteVideoView](/en/meeting/swift/api-reference/SMeetingRemoteVideoView)
