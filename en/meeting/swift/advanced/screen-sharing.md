---
title: "Screen sharing"
description: "Screen sharing in the SMeeting Swift SDK: default capture, choosing a display or window on macOS, iOS full-screen sharing through a Broadcast Upload Extension, whiteboard sharing, sharing events, and common rejection causes. Read when adding a share button to your meeting UI."
---

### Overview

Sharing in a meeting comes in two types, distinguished by `ShareType`:

| Type | Description | Produces a media stream |
| --- | --- | --- |
| `.screen` | Screen sharing | Yes |
| `.whiteBoard` | Whiteboard | No, it only broadcasts the sharing status |

Only one member in a meeting can share at a time. To find out who is sharing, read `RoomInfo.shareUid`; for the current sharing type, read `RoomInfo.shareState`.

On iOS, screen sharing has two capture paths that capture completely different scopes. Decide which one you need before integrating:

| Path | API | What it captures | Integration cost |
| --- | --- | --- | --- |
| In-app capture | `requestShare()` | **Only your own app's content** | None |
| Full-screen capture | `prepareBroadcastShare(appGroup:)` + `publishBroadcastShare()` | The entire system screen | Requires integrating an extra extension target |

macOS has only one path: `requestShare()` captures the whole screen / a specified window.

---

### Start sharing

#### Default capture

```swift
try await meeting.requestShare()
```

This is equivalent to `requestShare(shareType: .screen, preset: .h1080p)`, and on macOS it captures the main display. `preset` takes values from SRTC's `ScreenPreset`: `.h720p`, `.h1080p` (default).

#### macOS: let the user choose a display or window

macOS 12.3 and later support specifying the capture source. Your app enumerates the sources first, shows a selection UI, and then passes in the source the user chose:

```swift
import SMeeting
import SRTC

@available(macOS 12.3, *)
func startShare(meeting: SMeetingEngine) async throws {
    let displays = try await ScreenCaptureSources.availableDisplays()
    let windows = try await ScreenCaptureSources.availableWindows()

    // This example uses the first display; in practice, the user should choose in your UI
    guard let source = displays.first else { return }

    try await meeting.requestShare(source: source)
}
```

`source` accepts a `DisplaySource` (display) or a `WindowSource` (app window).

> The SDK handles "discovering shareable sources" and "starting capture"; how to present the source list to the user is up to you, so the SDK isn't tied to any particular UI.

#### macOS: exclude in-meeting windows when sharing the whole screen

When sharing an **entire display**, the video **includes your app's own windows** by default (consistent with Zoom / Tencent Meeting). But the main in-meeting window is usually rendering remote video, and if it happens to be rendering your own shared stream (testing with two instances on the same machine, or a sharing preview in your UI), you get an infinite mirror. Pass the IDs of these windows to cut them out one by one:

```swift
let ids = NSApplication.shared.windows
    .filter { $0.isVisible && $0.windowNumber > 0 }
    .map { UInt32($0.windowNumber) }

try await meeting.requestShare(source: source, excludedWindowIds: ids)
```

+ The values are `UInt32(NSWindow.windowNumber)`; they only matter when sharing an entire display and are ignored when capturing a single window
+ The list is snapshotted once when capture starts; windows opened afterward always appear in the video
+ If you really want the old behavior of "not sharing the app at all," set `excludesCurrentApplication` to `true`; `excludedWindowIds` is then ignored

<Warning>
This is a **behavior change** in 1.3.2 (SRTC 1.4.2): previously, all windows of the process were cut out of the whole-screen video, so others couldn't see your in-meeting windows. The new behavior is more natural when sharing across machines (others can see your meeting UI); products that depend on the old behavior must explicitly set `excludesCurrentApplication: true` after upgrading.
</Warning>

#### Local preview

If you need a local preview of the shared content in UIKit / AppKit, pass `view`; in SwiftUI, don't pass it and use `SRTCVideoView(track: meeting.screenTrack)` instead.

---

### iOS: full-screen sharing

On iOS, `requestShare()` uses in-app capture and **can capture only your own app's content**. To share the entire system screen, you must use a ReplayKit Broadcast Upload Extension—this is an iOS system constraint that no SDK can get around.

#### 1. Integrate the extension target

Create a Broadcast Upload Extension target that **links only `SRTCBroadcastKit`**, with its principal class inheriting from `SRTCBroadcastSampleHandler`:

```swift
import SRTCBroadcastKit

class SampleHandler: SRTCBroadcastSampleHandler {}
```

`SRTCBroadcastKit` is a product of the audio and video layer's `srtc-swift-sdk`, and SwiftPM doesn't allow using products of transitive dependencies, so you must **add one more dependency** to your project, with a version matching the SRTC version pinned inside SMeeting (see [Integration](/en/meeting/swift/integration)):

```swift
.package(url: "https://github.com/seastart/srtc-swift-sdk.git", exact: "1.5.2"),
```

<Warning>
**Add `SRTCBroadcastKit` only to the extension target.** Adding it to the app target puts two copies of the same types into one process (`SRTC` on the app side already statically contains the same code). Conversely, linking `SMeeting` / `SRTC` into the extension pulls WebRTC into an extension process that has only a **50 MB** memory limit, and the system will almost certainly kill it.
</Warning>

#### 2. Configure the App Group

Configure the same App Group for the app and the extension, and set `SRTCAppGroupIdentifier` in the **extension's `Info.plist`**. These three places must match exactly: the app's entitlement, the extension's entitlement, and the extension's `Info.plist`.

The App Group must also be registered in the developer portal, and both provisioning profiles must include that capability; otherwise signing fails with `Provisioning profile doesn't include the App Groups capability`.

#### 3. Set up the listener after entering the meeting, and let the user start from the system UI

Full-screen capture can only be started by the user from the system UI, so the flow is "set up the listener first → the user taps the system pill → announce sharing to the meeting only once frames actually arrive":

```swift
// After entering the meeting: only set up the listener, don't notify the meeting backend—sharing hasn't started yet
try await meeting.prepareBroadcastShare(appGroup: "group.your.app")

// Share button: overlay SRTCBroadcastPicker transparently on your own button, so one tap opens the system dialog directly
myShareButton.overlay {
    SRTCBroadcastPicker(preferredExtension: "com.your.app.broadcast", title: "")
}

// The user tapped "Start Broadcast" and the extension starts producing frames—only now announce sharing to the meeting
func meeting(_ meeting: SMeetingEngine, shareBroadcastDidStart data: ShareBroadcastStartEventData) {
    Task { try? await meeting.publishBroadcastShare() }
}
```

For the scenario where a member raises a hand to request sharing and starts only after the host approves, pass the corresponding parameters to `publishBroadcastShare(byAdmin: true, adminUid:)`; the semantics are the same as for `requestShare`.

<Warning>
**Don't call `requestShare` as soon as the user taps the button.** There's no callback at all when the user taps "Cancel" in the system dialog, so the meeting would be left with a sharing flag that never has any video, and you'd have to withdraw it yourself with a timeout.

The one-step `requestShare(broadcastAppGroup:)` is still available, but it announces sharing **the moment the listener is ready**, so it only suits simple integrations that don't care about the intermediate state. For meeting scenarios, use `prepareBroadcastShare` + `publishBroadcastShare`.
</Warning>

Because the share button itself is the system `SRTCBroadcastPicker`, your UI **doesn't need** an intermediate prompt page such as "waiting for the user to start sharing."

#### 4. State and cleanup

| State | How to tell |
| --- | --- |
| Listener set up, user hasn't started broadcasting yet | `prepareBroadcastShare` succeeded, and `isShareBroadcastActive == false` |
| Producing frames | `shareBroadcastDidStart` received |
| Ended | `shareBroadcastDidFinish(reason:)` received |

When the user stops broadcasting from the system pill, the SDK **cleans up automatically** (unpublishes + notifies the meeting backend) and sets up the listener again. Your app doesn't need to call `stopShare()` or prepare again; just refresh the UI. The user can share again right away.

Call `stopBroadcastListening()` when you no longer need the sharing capability; `exitRoom()` tears down the listener automatically, so you don't need to handle it manually.

<Note>
**Full-screen capture doesn't work in the simulator; you must use a real device** (it depends on real signing and the App Group). Logs from the extension process don't appear in the Xcode console; use Console.app and filter by the subsystem `com.srtc.broadcast`.

iOS full-screen sharing **doesn't capture system audio**—the extension side can get audio frames, but the current iOS audio path on the host side isn't connected, and the protocol only reserves a slot for it. Shared content is video only.
</Note>

For the underlying frame transport, backpressure, and memory constraints, see [SRTC · Screen sharing](/en/rtc/swift/advanced/screen-sharing).

---

### Stop sharing

```swift
await meeting.stopShare()
```

`stopShare()` notifies the meeting, unpublishes, and stops capture; it doesn't throw.

The host can also force the current sharing to end:

```swift
try await meeting.adminStopRoomShare()
```

The member whose sharing is stopped doesn't need to do anything: the SDK stops the stream automatically and reports `roomShareDidStop` (with `byAdmin` set to `true`).

---

### Whiteboard sharing

A whiteboard doesn't produce a media stream; `requestShare(shareType: .whiteBoard)` only broadcasts the sharing status:

```swift
try await meeting.requestShare(shareType: .whiteBoard)
```

You can read the whiteboard page URL once you've entered the meeting:

```swift
let url = meeting.getWhiteBoard()
```

What you get is a complete URL with the auth code already included; just load it with `WKWebView`. You host the whiteboard's actual interaction in your own container; the SDK only synchronizes the state of "who is currently sharing the whiteboard."

Members who enter mid-meeting don't receive `roomShareDidStart`, so they need to check once themselves: `RoomInfo.shareState == 2` means someone in the meeting is already sharing the whiteboard.

For the whiteboard page's URL parameters, host JS APIs, lifecycle, and when it's destroyed, see [SRTC · Whiteboard](/en/rtc/whiteboard).

---

### Sharing events

| Event | When it fires |
| --- | --- |
| `meeting(_:roomShareDidStart:)` | Someone starts sharing (including yourself) |
| `meeting(_:roomShareDidStop:)` | Sharing ends |
| `meeting(_:roomShareStateDidChange:)` | The host turned "sharing disabled for the room" on / off |
| `meeting(_:shareBroadcastDidStart:)` | iOS full-screen sharing only: the extension actually starts producing frames |
| `meeting(_:shareBroadcastDidFinish:)` | iOS full-screen sharing only: frame production ends (the user stopped broadcasting / the system ended the extension) |

```swift
func meeting(_ meeting: SMeetingEngine, roomShareDidStart data: RoomShareStartEventData) {
    // data.uid is the sharer, data.shareType is the sharing type
}

func meeting(_ meeting: SMeetingEngine, roomShareDidStop data: RoomShareStopEventData) {
    // data.byAdmin being true means the host forced it to end; data.opUid is the operator
}
```

For screen sharing, `roomShareDidStart` **is driven by the RTC media track**: it's reported as soon as the remote screen track arrives, so when you receive this event you can render the shared video immediately without extra delays or retries. The sharing broadcast message and the media track are two independent paths with no guaranteed arrival order; the SDK deduplicates and adds fallbacks across three paths, so each sharing session is reported only once.

`shareBroadcastDidStart` / `shareBroadcastDidFinish` fire only for **iOS full-screen sharing**, and only on **the sharer's own** side, to distinguish "the listener is set up" from "there's actually video." Other members only need to care about `roomShareDidStart` / `roomShareDidStop`; they don't need to tell which capture path the sharer is using.

---

### Common rejection causes

| Situation | Result |
| --- | --- |
| The host turned on "sharing disabled for the room," and you're not the host / a co-host | Throws `SMeetingError.unauthorized` |
| You're already sharing | Throws `SMeetingError.invalidState` |
| The user denied screen recording permission in the system dialog | Capture fails; the SDK rolls back the sharing status automatically and throws the error to you |

---

### Related pages

+ [Video rendering](/en/meeting/swift/advanced/video-rendering)
+ [Media control](/en/meeting/swift/advanced/media-control)
+ [Host controls](/en/meeting/swift/advanced/host-controls)
