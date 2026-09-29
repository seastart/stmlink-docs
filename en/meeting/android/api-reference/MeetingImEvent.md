---
title: "MeetingImEvent"
description: "Receive Meeting IM connection, reconnection, raw message, call, meeting reminder, waiting room, and sub-meeting help events, registered through MeetingEngine.imEvent. Read this when you use enableIm() for out-of-meeting messages."
---

`MeetingImEvent` receives ongoing state and business messages that share the lifecycle of the IM connection in the Engine, and is registered through `MeetingEngine.imEvent`. You can extend `MeetingImSimpleEvent` and override only what you need.

## Usage notes

+ The IM connection is independent of the current meeting; out-of-meeting messages such as meeting reminders, waiting room moves, and sub-meeting help requests are also dispatched through this interface.

+ Call `enableIm()` first to establish the connection; an intentional disconnect caused by `disableIm()` or `release()` doesn't trigger `onImDisconnected()`.
+ Callbacks stay on the actual IM source thread; switch to the main thread before updating the UI.

## Methods

### onImConnected(uid, sid)

```kotlin
fun onImConnected(uid: String, sid: String)
```

Description: IM established its connection for the first time.

Parameters:

| Parameter | Description |
| --- | --- |
| `uid` | The current user's IM UID. |
| `sid` | Identifier of this IM session. |

Returns: None (`Unit`).

### onImDisconnected(reason, statusCode, message)

```kotlin
fun onImDisconnected(reason: LeaveReason, statusCode: Int, message: String?)
```

Description: IM disconnected unintentionally.

Parameters:

| Parameter | Description |
| --- | --- |
| `reason` | Disconnect reason defined by SRTC. |
| `statusCode` | Underlying status code. |
| `message` | Nullable diagnostic information. |

Returns: None (`Unit`).

### onImReconnecting()

```kotlin
fun onImReconnecting()
```

Description: IM started reconnecting automatically after a disconnect.

Parameters: None.

Returns: None (`Unit`).

### onImReconnected()

```kotlin
fun onImReconnected()
```

Description: IM reconnected automatically.

Parameters: None.

Returns: None (`Unit`).

### onImMessage(uid, sid, name, action, content)

```kotlin
fun onImMessage(
    uid: String,
    sid: String,
    name: String,
    action: String,
    content: String
)
```

Description: Receives a raw IM message that Meeting didn't parse into a dedicated business event.

Parameters:

| Parameter | Description |
| --- | --- |
| `uid` | Sender UID. |
| `sid` | Identifier of the session the message belongs to. |
| `name` | Sender nickname. |
| `action` | Message action name. |
| `content` | Raw message content. |

Returns: None (`Unit`).

### onCallReceived(uid, nickname, callingMsg)

```kotlin
fun onCallReceived(
    uid: String,
    nickname: String,
    callingMsg: ImContent.CallingMsg
)
```

Description: Received a meeting call invitation.

Parameters:

| Parameter | Description |
| --- | --- |
| `uid` | Inviter UID. |
| `nickname` | Inviter nickname. |
| `callingMsg` | Target meeting ID, room number, and title. |

Returns: None (`Unit`).

### onMeetingRemind(uid, meetingRemind)

```kotlin
fun onMeetingRemind(uid: String, meetingRemind: ImContent.MeetingRemind)
```

Description: Received a scheduled meeting reminder.

Parameters:

| Parameter | Description |
| --- | --- |
| `uid` | Message sender UID. |
| `meetingRemind` | Meeting, creator, and planned time information. |

Returns: None (`Unit`).

### onMoveOutWaitingRoom(uid, moveOutWaitingRoom)

```kotlin
fun onMoveOutWaitingRoom(
    uid: String,
    moveOutWaitingRoom: ImContent.MoveOutWaitingRoom
)
```

Description: The host moved the current user from the waiting room into the meeting.

Parameters:

| Parameter | Description |
| --- | --- |
| `uid` | Message sender UID. |
| `moveOutWaitingRoom` | Target meeting ID and title. |

Returns: None (`Unit`).

### onUserHelpSubMeeting(uid, userHelpSubMeeting)

```kotlin
fun onUserHelpSubMeeting(
    uid: String,
    userHelpSubMeeting: ImContent.UserHelpSubMeeting
)
```

Description: Received a help request from a sub-meeting member.

Parameters:

| Parameter | Description |
| --- | --- |
| `uid` | UID of the member asking for help. |
| `userHelpSubMeeting` | Main meeting and sub-meeting information, including the sub-meeting title. |

Returns: None (`Unit`).
