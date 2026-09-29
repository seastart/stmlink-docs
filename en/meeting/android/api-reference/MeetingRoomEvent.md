---
title: "MeetingRoomEvent"
description: "Receive the current meeting's room configuration, connection, host, recording, sharing, raise hand, sub-meeting, and sign-in events through MeetingEngine.roomEvent. Read this when you track meeting-wide state or handle disconnects and reconnects."
---

`MeetingRoomEvent` carries the overall room state and connection lifecycle of the current meeting and is registered through `MeetingEngine.roomEvent`. You can extend `MeetingRoomSimpleEvent` and override only what you need.

## Usage notes

+ Room-level events describe the shared state, configuration, and lifecycle of the whole meeting; device, permission, or track changes of a specific member are dispatched by `MeetingUserEvent`.

+ You can assign the listener before entering the meeting to receive the initial room state; it is cleared after you exit the meeting.
+ Callbacks stay on the actual source thread. `onDisconnected()` means the underlying connection is actually disconnected; calling `exitMeeting()` yourself isn't guaranteed to produce this callback.

## Room and connection

### onMeetingUpdated(meetingInfo)

```kotlin
fun onMeetingUpdated(meetingInfo: MeetingInfo?)
```

Description: The current meeting's room information was refreshed.

Parameters:

| Parameter | Description |
| --- | --- |
| `meetingInfo` | The updated room snapshot; may be `null` at parsing or lifecycle boundaries. |

Returns: None (`Unit`).

### onDisconnected(reason, statusCode, message)

```kotlin
fun onDisconnected(reason: LeaveReason, statusCode: Int, message: String?)
```

Description: The current meeting is actually disconnected.

Parameters:

| Parameter | Description |
| --- | --- |
| `reason` | SRTC disconnect reason. |
| `statusCode` | Underlying status code. |
| `message` | Nullable diagnostic information. |

Returns: None (`Unit`).

### onReconnecting()

```kotlin
fun onReconnecting()
```

Description: The current meeting connection started reconnecting automatically.

Parameters: None.

Returns: None (`Unit`).

### onReconnected()

```kotlin
fun onReconnected()
```

Description: The current meeting connection reconnected automatically.

Parameters: None.

Returns: None (`Unit`).

## Room configuration

### onRoomCameraStateChanged(operatorUid, selfUnMuteCameraDisabled, disabled)

```kotlin
fun onRoomCameraStateChanged(
    operatorUid: String?,
    selfUnMuteCameraDisabled: Boolean,
    disabled: Boolean
)
```

Description: The room's camera-off setting or the policy on whether members can turn their cameras back on themselves changed.

Parameters:

| Parameter | Description |
| --- | --- |
| `operatorUid` | Operator UID; may be `null` for system events. |
| `selfUnMuteCameraDisabled` | Whether members are prevented from turning their cameras back on themselves. |
| `disabled` | Whether camera off for everyone is on. |

Returns: None (`Unit`).

### onRoomMicStateChanged(operatorUid, selfUnMuteMicDisabled, disabled)

```kotlin
fun onRoomMicStateChanged(
    operatorUid: String?,
    selfUnMuteMicDisabled: Boolean,
    disabled: Boolean
)
```

Description: The room's mic mute setting or the policy on whether members can unmute themselves changed.

Parameters:

| Parameter | Description |
| --- | --- |
| `operatorUid` | Nullable operator UID. |
| `selfUnMuteMicDisabled` | Whether members are prevented from unmuting themselves. |
| `disabled` | Whether mute all is on. |

Returns: None (`Unit`).

### onRoomChatDisabledChanged(operatorUid, disabled)

```kotlin
fun onRoomChatDisabledChanged(operatorUid: String?, disabled: Boolean)
```

Description: The room's chat-disabled state changed.

Parameters:

| Parameter | Description |
| --- | --- |
| `operatorUid` | Operator UID; may be `null` for system events. |
| `disabled` | `true` means room members are not allowed to chat. |

Returns: None (`Unit`).

### onRoomScreenshotDisabledChanged(operatorUid, disabled)

```kotlin
fun onRoomScreenshotDisabledChanged(operatorUid: String?, disabled: Boolean)
```

Description: The room's screenshot-disabled state changed.

Parameters:

| Parameter | Description |
| --- | --- |
| `operatorUid` | Operator UID; may be `null` for system events. |
| `disabled` | `true` means room members are not allowed to take screenshots. |

Returns: None (`Unit`).

### onRoomWatermarkDisabledChanged(operatorUid, disabled)

```kotlin
fun onRoomWatermarkDisabledChanged(operatorUid: String?, disabled: Boolean)
```

Description: The room's watermark-disabled state changed.

Parameters:

| Parameter | Description |
| --- | --- |
| `operatorUid` | Operator UID; may be `null` for system events. |
| `disabled` | `true` means the room watermark is disabled. |

Returns: None (`Unit`).

### onRoomLockedChanged(operatorUid, locked)

```kotlin
fun onRoomLockedChanged(operatorUid: String?, locked: Boolean)
```

Description: The room's locked state changed.

Parameters:

| Parameter | Description |
| --- | --- |
| `operatorUid` | Operator UID; may be `null` for system events. |
| `locked` | `true` means the room is locked. |

Returns: None (`Unit`).

### onWaitingRoomDisabledChanged(operatorUid, disabled)

```kotlin
fun onWaitingRoomDisabledChanged(operatorUid: String?, disabled: Boolean)
```

Description: The waiting room was enabled or disabled.

Parameters:

| Parameter | Description |
| --- | --- |
| `operatorUid` | Operator UID; may be `null` for system events. |
| `disabled` | `true` means the waiting room is disabled. |

Returns: None (`Unit`).

### onRoomHostMove(sourceUid, targetUid)

```kotlin
fun onRoomHostMove(sourceUid: String?, targetUid: String?)
```

Description: The host role was transferred from the original member to the target member.

Parameters:

| Parameter | Description |
| --- | --- |
| `sourceUid` | Original host UID; may be `null`. |
| `targetUid` | New host UID; may be `null`. |

Returns: None (`Unit`).

## Recording, sharing, and raise hand

### onCloudRecordStatusChange(type, status, errorMessage)

```kotlin
fun onCloudRecordStatusChange(
    type: CloudRecordType,
    status: CloudRecordStatus,
    errorMessage: String
)
```

Description: The status of a cloud recording task changed.

Parameters:

| Parameter | Description |
| --- | --- |
| `type` | Recording task type. |
| `status` | Current task status. |
| `errorMessage` | Error information; usually an empty string when there is no error. |

Returns: None (`Unit`).

### onMcuAlarmReceived(operatorUid, alarm)

```kotlin
fun onMcuAlarmReceived(operatorUid: String, alarm: McuAlarm)
```

Description: Received an MCU alarm sent privately to this user.

Parameters:

| Parameter | Description |
| --- | --- |
| `operatorUid` | Message sender UID. |
| `alarm` | Task, gateway, time, and summary information. |

Returns: None (`Unit`).

### onRoomShareStart(shareUid, shareType)

```kotlin
fun onRoomShareStart(shareUid: String?, shareType: ShareType)
```

Description: The specified member started screen or whiteboard sharing.

Parameters:

| Parameter | Description |
| --- | --- |
| `shareUid` | Sharer UID; may be `null` when it can't be determined. |
| `shareType` | The type of sharing that started. |

Returns: None (`Unit`).

### onRoomShareStop(shareUid, shareType)

```kotlin
fun onRoomShareStop(shareUid: String?, shareType: ShareType)
```

Description: The specified member stopped screen or whiteboard sharing.

Parameters:

| Parameter | Description |
| --- | --- |
| `shareUid` | Sharer UID; may be `null` when it can't be determined. |
| `shareType` | The type of sharing that stopped. |

Returns: None (`Unit`).

### onAdminRoomShareStop(shareUid, shareType)

```kotlin
fun onAdminRoomShareStop(shareUid: String, shareType: ShareType)
```

Description: The host forcibly stopped the specified member's sharing.

Parameters:

| Parameter | Description |
| --- | --- |
| `shareUid` | UID of the member whose sharing was stopped. |
| `shareType` | The type of sharing that was stopped. |

Returns: None (`Unit`).

### onRoomHandUpChanged(operatorUid, enabled, handUpType)

```kotlin
fun onRoomHandUpChanged(
    operatorUid: String?,
    enabled: Boolean?,
    handUpType: HandUpType?
)
```

Description: A room member's raise hand state changed.

Parameters:

| Parameter | Description |
| --- | --- |
| `operatorUid` | Nullable member UID. |
| `enabled` | `true` raises the hand, `false` lowers it; `null` when it can't be parsed. |
| `handUpType` | Raise hand type; `null` when it can't be parsed. |

Returns: None (`Unit`).

## Sub-meetings and sign-in

### onAdminRoomStartSubMeeting(subMeetingId, subTitle, uids)

```kotlin
fun onAdminRoomStartSubMeeting(
    subMeetingId: String,
    subTitle: String,
    uids: List<String>
)
```

Description: The host started the specified sub-meeting.

Parameters:

| Parameter | Description |
| --- | --- |
| `subMeetingId` | Meeting ID of the sub-meeting that started. |
| `subTitle` | Sub-meeting title. |
| `uids` | UIDs of the members assigned to this sub-meeting. |

Returns: None (`Unit`).

### onAdminRoomStopSubMeeting(mainMeetingId, subMeetingId, subTitle)

```kotlin
fun onAdminRoomStopSubMeeting(
    mainMeetingId: String,
    subMeetingId: String,
    subTitle: String
)
```

Description: The host ended the specified sub-meeting.

Parameters:

| Parameter | Description |
| --- | --- |
| `mainMeetingId` | Main meeting ID. |
| `subMeetingId` | Meeting ID of the sub-meeting that ended. |
| `subTitle` | Sub-meeting title. |

Returns: None (`Unit`).

### onSignInActivity(hostName, epoch, beginAt, duration, endAt, description)

```kotlin
fun onSignInActivity(
    hostName: String,
    epoch: Int,
    beginAt: Long,
    duration: Int,
    endAt: Long,
    description: String
)
```

Description: Received a message that an in-meeting sign-in activity started.

Parameters:

| Parameter | Description |
| --- | --- |
| `hostName` | Initiator nickname. |
| `epoch` | Sign-in round. |
| `beginAt` | Start time, Unix timestamp in seconds. |
| `duration` | Duration in minutes; `0` means no time limit. |
| `endAt` | End time, Unix timestamp in seconds. |
| `description` | Sign-in description. |

Returns: None (`Unit`).

### onSignInFinish(hostName, epoch)

```kotlin
fun onSignInFinish(hostName: String, epoch: Int)
```

Description: Received a message that an in-meeting sign-in activity ended.

Parameters:

| Parameter | Description |
| --- | --- |
| `hostName` | Nickname of the host who ended the activity. |
| `epoch` | Sign-in round. |

Returns: None (`Unit`).
