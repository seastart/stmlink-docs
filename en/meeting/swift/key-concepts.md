---
title: "Key concepts"
description: "How the SMeeting Swift SDK is organized: the SMeetingEngine entry point, the meeting lifecycle, meeting ID vs. room number, RoomInfo / MeetingUserInfo snapshots, roles, TrackDesc, media control naming, audio vs. video subscription, and SMeetingDelegate events. Read before building meeting features."
---

### Overall model

The object model of the SMeeting Swift SDK is compact:

+ `SMeetingEngine`: the only public class; login, meeting management, entering and exiting meetings, media control, and host operations are all on it
+ `RoomInfo`: room-level state of the current meeting (title, mute all / camera off for everyone, lock, sharing status, etc.)
+ `MeetingUserInfo`: the state of one member in the meeting (nickname, role, microphone, camera, sharing)
+ `SMeetingDelegate`: the callback entry point for all meeting events
+ `SMeetingRemoteVideoView` / `SRTCVideoView`: the entry points for video rendering

At its core, the conferencing SDK synchronizes three kinds of state: **meeting state**, **member state**, and **media state**. The SDK's APIs and events are organized around these three kinds of state; once you understand this, most of the APIs become intuitive.

---

### Terminology: meeting layer vs. RTC layer

SMeeting is built on top of SRTC, and the two layers use different terms; mixing them up will keep tripping you up when reading the APIs:

| Concept | Meeting layer (SMeeting) | RTC layer (SRTC) |
| --- | --- | --- |
| Space | room / meeting | channel |
| Entry / exit | enter / exit | join / leave |
| Members | member | channel user |

In the SMeeting APIs, you only see meeting-semantic names such as `enterRoom` / `exitRoom` / `createRoom`.

---

### Meeting lifecycle

A complete integration unfolds in the following order:

```text
login  →  Before the meeting (create / query / update meetings)  →  enterRoom  →  In the meeting  →  exitRoom  →  logout
```

| Stage | Typical APIs | Description |
| --- | --- | --- |
| Log in | `login(token:)` | The token is issued by your backend; you can call the other APIs only after logging in |
| Before the meeting | `createRoom(_:)`, `updateRoom(meetingId:req:)`, `cancelRoom(meetingId:)`, `detailRoom(meetingId:roomNo:)`, `attendeeRoom(page:)`, `attendedRoom(page:)` | Requires only login, not being in a meeting |
| Enter | `enterRoom(_:)` | On success, the SDK sets up meeting state internally and starts reporting events |
| In the meeting | Media control, messages, host controls, and more | Calling these when not in a meeting throws `SMeetingError.notInMeeting` |
| Exit | `exitRoom()` | Exits only the current meeting; the login state is kept |
| Log out | `logout()` | If still in a meeting, exits the meeting first automatically |

To check whether you're currently in a meeting, use `meeting.isInRoom`.

---

### Meeting ID and room number

The two identifiers often appear together but mean different things:

| Identifier | Source | Purpose |
| --- | --- | --- |
| `meetingId` | Return value of `createRoom`, meeting list / details | The unique ID of the meeting; used by most meeting management APIs |
| `roomNo` | Return value of `createRoom`, meeting details | The user-facing meeting number, used for sharing and inviting others to enter the meeting |

In `MeetingEnterReq`, provide either `meetingId` or `roomNo`.

---

### Meeting type and meeting mode

Creating a meeting involves two orthogonal dimensions:

+ `MeetingType`: `.instant` instant meeting / `.appointment` scheduled meeting. A scheduled meeting also requires `planTime` (timestamp in seconds) and `planDur` (minutes)
+ `MeetingMode`: `.normal` normal, `.mix` composite, `.voice` voice meeting, `.training` training, `.subMeeting` sub-meeting

Entry restrictions are controlled by `AttendType`: password-protected entry also requires `password`, and invitation-only entry also requires `conferee`.

---

### In-meeting state: RoomInfo and MeetingUserInfo

After you enter a meeting, the SDK continuously maintains a snapshot of the in-meeting state that you can read at any time:

```swift
let roomInfo = meeting.getRoomInfo()          // Current room info; nil when not in a meeting
let users = meeting.getUsersInfoList()        // All members (array)
let usersMap = meeting.getUsersInfo()         // All members (uid → member)
let me = try meeting.getUserInfo(meeting.currentUserId ?? "")
```

This snapshot is **read-only**: state changes are notified through `SMeetingDelegate` events, and you just read it again in the event callback. Don't cache stale member objects.

Frequently used fields in `MeetingUserInfo`:

| Field | Type | Description |
| --- | --- | --- |
| `micState` | `MicState` | `.on` / `.off` |
| `cameraState` | `CameraState` | `.on` / `.off` |
| `shareState` | `Int` | `0` no sharing, `1` screen sharing, `2` whiteboard; can be compared with the `rawValue` of `ShareType` |
| `role` | `Role` | `.member` / `.host` / `.coHost` |
| `chatDisabled` | `Bool` | Whether chat is disabled for this member individually |
| `drawDisabled` | `Bool` | Whether the member is prevented from drawing |

---

### Roles and permissions

| Role | Description |
| --- | --- |
| `.host` | Host, with full meeting control permissions |
| `.coHost` | Co-host, sharing most meeting control permissions with the host |
| `.member` | Regular member |

To check whether you have meeting control permissions, read your own `MeetingUserInfo.role`:

```swift
let me = try? meeting.getUserInfo(meeting.currentUserId ?? "")
let isAdmin = me?.role == .host || me?.role == .coHost
```

APIs with the `admin` prefix succeed only when called by the host / a co-host; regular members who call them get a permission error from the server.

---

### Track descriptions: TrackDesc

Every media stream in a meeting has a fixed description, used to locate the target when subscribing to remote video:

| Enum value | Raw value | Description |
| --- | --- | --- |
| `.mic` | `mic` | Microphone audio |
| `.cameraBig` | `camera_big` | Camera high stream |
| `.cameraSmall` | `camera_small` | Camera low stream |
| `.screen` | `screen` | Screen sharing |

To see which tracks a member is currently publishing, read `MeetingUserInfo.trackDescs`.

---

### Naming rules for media control

+ **Turning on** uses `requestOpenMic` / `requestOpenCamera` / `requestShare`—they include `request` because these actions first ask the meeting for permission (subject to room policies such as mute all, camera off for everyone, and sharing disabled) and then start the local stream
+ **Turning off** uses `closeMic` / `closeCamera` / `stopShare`—they stop the local stream directly, with no request step, and never throw

When you're responding to the host's invitation to turn on your microphone / camera, pass `byAdmin: true` and `adminUid` to the turn-on API; the SDK then takes the "confirm the host's request" path instead of "request on your own."

---

### Video rendering entry points

| Scenario | Recommended entry point |
| --- | --- |
| Local video in SwiftUI | `SRTCVideoView(track: meeting.cameraTrack)` |
| Remote video in SwiftUI | `SMeetingRemoteVideoView(meeting:uid:trackDesc:)` |
| Remote video in UIKit / AppKit | `startPlayRemoteVideo(view:uid:trackDesc:)` / `stopPlayRemoteVideo(view:uid:trackDesc:)` |
| Controlling subscription yourself | `subscribeRemoteVideoTrack(uid:trackDesc:)` / `unsubscribeRemoteVideoTrack(uid:trackDesc:)` |

For details, see [Video rendering](/en/meeting/swift/advanced/video-rendering).

---

### Audio subscription semantics

Remote audio and remote video are handled differently:

+ **Audio**: subscribed automatically after you enter the meeting; you don't need to subscribe member by member. The speaker (remote audio playback) switch is `toggleRemoteAudioMute(_:)`—it only toggles playback and doesn't touch subscriptions
+ **Video**: subscribed on demand. In a large meeting, subscribing to everyone's video makes bandwidth and decoding costs uncontrollable, so you decide which streams the current layout needs to pull

---

### Event model

All meeting events are reported through `SMeetingDelegate`. To register:

```swift
meeting.delegates.add(delegate: self)
// When no longer needed
meeting.delegates.remove(delegate: self)
```

Key points:

+ `delegates` is a **weak-reference multicast**, so you can register multiple observers; registering doesn't extend your object's lifetime
+ Every method in the protocol has a default empty implementation, so you only implement the events you care about
+ Event callbacks are always dispatched on the **main thread**, so you can update the UI directly

If your observer is a `@MainActor` type (for example, a SwiftUI `ObservableObject`), declare the protocol methods as `nonisolated`, then hop back to the main actor context inside them:

```swift
@MainActor
final class MeetingController: ObservableObject {
    @Published var users: [MeetingUserInfo] = []
}

extension MeetingController: SMeetingDelegate {
    nonisolated func meeting(_ meeting: SMeetingEngine, userDidEnter user: MeetingUserInfo) {
        DispatchQueue.main.async { self.users = meeting.getUsersInfoList() }
    }
}
```

Events fall roughly into these groups: connection events, member events, room state events, message events, raise hand and host commands, waiting room, sub-meetings, sign-in and roll call, device events, and out-of-meeting messages (IM). For the full list, see [Events](/en/meeting/swift/events).

---

### Out-of-meeting messages (IM)

`enableIm()` sets up a message path independent of the meeting, used to receive notifications such as calls and meeting reminders **when you haven't entered a meeting**. It is separate from in-meeting chat messages: in-meeting chat goes through `sendRoomChatMessage` and works only inside the meeting.

See [Out-of-meeting messages](/en/meeting/swift/advanced/im).

---

### Underlying RTC capabilities

When the meeting layer's high-level APIs aren't enough (for example, you need raw frame processing or custom encoding parameters that only SRTC provides), you can access the underlying instance through `meeting.srtc`.

```swift
meeting.srtc.logLevel = .debug
```

> Always use `meeting.srtc`; don't create another SRTCEngine instance yourself. The meeting and the underlying layer share the same instance, and creating another one leads to split state, duplicate message connections, and devices being taken over.

---

### Further reading

+ [Media control](/en/meeting/swift/advanced/media-control)
+ [Video rendering](/en/meeting/swift/advanced/video-rendering)
+ [Screen sharing](/en/meeting/swift/advanced/screen-sharing)
+ [Host controls](/en/meeting/swift/advanced/host-controls)
+ [Types](/en/meeting/swift/types)
