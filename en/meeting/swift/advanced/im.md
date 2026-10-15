---
title: "Out-of-meeting messages"
description: "The out-of-meeting message (IM) path of the SMeeting Swift SDK: enable and disable it after login, receive calls, meeting reminders, waiting room admissions, and sub-meeting help requests before entering a meeting, and track its connection state. Read when users need notifications outside a meeting."
---

### Overview

Out-of-meeting messages (IM) are a **notification path independent of the meeting**. They solve problems like "how does a user get notified before entering a meeting":

+ Someone in a meeting is calling you
+ A scheduled meeting is about to start
+ You've been admitted from the waiting room
+ A sub-meeting you're responsible for is asking for help

In-meeting chat messages don't go through this path—those are [In-meeting messages](/en/meeting/swift/advanced/messaging), which work only during the meeting.

---

### Enable and disable

```swift
// You can enable it right after logging in; you don't need to be in a meeting
try await meeting.enableIm()

// When no longer needed
await meeting.disableIm()
```

Key points:

+ You must call `login(token:)` first; calling it before logging in throws `SMeetingError.notLoggedIn`
+ `logout()` disables this path internally, so you don't need to call it again in your logout flow
+ Once set up, the path stays up regardless of whether you're in a meeting
+ After `enableIm()` succeeds, `meeting(_:imDidConnect:)` fires once with the local `uid` and IM session `sid` (since 1.5.0)
+ Calling `disableIm()` yourself doesn't fire `imDidDisconnect`

<Note>
In 1.4.1 and earlier, `enableIm()` only established the path; the call, reminder, waiting room admission, and sub-meeting help events below, as well as the reconnect / disconnect callbacks, were never actually dispatched. Integrations that rely on these events need to upgrade to 1.5.0.
</Note>

The typical place to enable it is right after a successful login:

```swift
try await meeting.login(token: token)
meeting.delegates.add(delegate: self)
try await meeting.enableIm()
```

---

### Events

The four business events below each carry a `base` (`ImBaseEventData`) and a `content`:

| `ImBaseEventData` field | Description |
| --- | --- |
| `sid` | Session ID |
| `uid` | Sender's user ID |
| `name` | Sender's nickname |
| `avatar` | Sender's avatar |

#### Someone is calling you

```swift
func meeting(_ meeting: SMeetingEngine, imCallCalling data: ImCallCallingEventData) {
    // data.base.name caller
    // data.content.roomNo / data.content.meetingId / data.content.title
    // Show the incoming call UI; after the user answers, call enterRoom to enter
}
```

#### Meeting reminders

```swift
func meeting(_ meeting: SMeetingEngine, imMeetingRemind data: ImMeetingRemindEventData) {
    // data.content.title / creatorName / planTime / planDur
    // data.content.creatorId creator's user ID (since 1.5.0)
}
```

`planTime` is a Unix timestamp in seconds, and `planDur` is in minutes.

#### Admitted from the waiting room

```swift
func meeting(_ meeting: SMeetingEngine, imAdminMoveOutWaitingRoom data: ImAdminMoveOutWaitingRoomEventData) {
    // data.content.meetingId is the target meeting, which you can enter
}
```

#### A sub-meeting asks for help

```swift
func meeting(_ meeting: SMeetingEngine, imUserHelpSubMeeting data: ImUserHelpSubMeetingEventData) {
    // data.content.meetingId / title the sub-meeting asking for help
    // data.content.parent main meeting ID
}
```

#### Raw messages

Every out-of-meeting message first fires `imDidReceiveMessage` as is; actions the SDK recognizes are additionally dispatched to the named events above (since 1.5.0). Business-defined actions are only available here:

```swift
func meeting(_ meeting: SMeetingEngine, imDidReceiveMessage data: ImMessageEventData) {
    // data.action  message command, such as call_calling
    // data.content message content, usually a JSON string you parse yourself
    // data.sid / data.uid / data.name sender
}
```

A known message triggers both the raw and the named callback, so don't handle it in both places.

---

### Connection state

This path has its own connection state events; don't confuse them with the meeting's reconnection events:

| Event | Description |
| --- | --- |
| `meeting(_:imDidConnect:)` | Fires once after `enableIm()` succeeds; `data.uid` / `data.sid` are the local user ID and IM session ID (since 1.5.0) |
| `meetingImIsReconnecting(_:)` | The message path starts reconnecting |
| `meetingImDidReconnect(_:)` | The message path reconnected successfully (doesn't fire `imDidConnect` again) |
| `meeting(_:imDidDisconnect:)` | The message path is disconnected passively (kicked, heartbeat timeout, backend error); `data.reason` describes the reason |

Since 1.5.0, `ImDisconnectEventData` also carries a structured reason:

| Field | Type | Description |
| --- | --- | --- |
| `reason` | `String?` | Text description: the error description if there is an error, otherwise the name of `disconnectReason` |
| `disconnectReason` | `ImDisconnectReason` | Disconnect reason (defined in SRTC; requires `import SRTC`) |
| `errorCode` | `Int?` | Code of the error that caused the disconnect; `nil` if there is none |
| `errorMessage` | `String?` | Description of the error that caused the disconnect; `nil` if there is none |

After a passive disconnect the path is no longer usable; call `enableIm()` again if needed.

The corresponding connection events for the meeting itself are `meetingIsReconnecting(_:)` / `meetingDidReconnect(_:)` / `meeting(_:didDisconnect:)`.

---

### Related pages

+ [In-meeting messages](/en/meeting/swift/advanced/messaging)
+ [Waiting room](/en/meeting/swift/advanced/waiting-room)
+ [Sub-meetings](/en/meeting/swift/advanced/sub-meetings)
