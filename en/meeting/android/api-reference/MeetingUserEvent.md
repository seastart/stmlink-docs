---
title: "MeetingUserEvent"
description: "Receive the current meeting's member enter/exit, role and permission, device state, request and reply, waiting room, meeting move, and track change events through MeetingEngine.userEvent. Read this when you maintain the member list or decide what to subscribe to."
---

`MeetingUserEvent` carries the current meeting's member, member permission, and member track events and is registered through `MeetingEngine.userEvent`. You can extend `MeetingUserSimpleEvent` and override only what you need.

## Usage notes

+ Event parameters mainly provide the UID of the member that changed and the incremental state; when you need a full member or track snapshot, query it through `MeetingEngine.infosManager`.

+ You can assign the listener before entering the meeting; it is cleared after you exit the meeting.
+ `onUserEnter()` only provides the UID; when you need full information, query it through `MeetingEngine.infosManager.getMemberByUid(uid)`.
+ The audience isn't included in the full member list; identity changes are reported through `onMeMembershipChanged()`.

## Member lifecycle

### onExitRoom(reason)

```kotlin
fun onExitRoom(reason: LeaveMeetingReason)
```

Description: The current user exited the meeting because they were removed, replaced, timed out on heartbeat, or the channel was destroyed, among other reasons.

Parameters:

| Parameter | Description |
| --- | --- |
| `reason` | Exit reason as mapped by Meeting. |

Returns: None (`Unit`).

### onUserEnter(uid)

```kotlin
fun onUserEnter(uid: String)
```

Description: A remote user entered the current meeting.

Parameters:

| Parameter | Description |
| --- | --- |
| `uid` | UID of the user who just entered. |

Returns: None (`Unit`).

### onUserExit(memberInfo)

```kotlin
fun onUserExit(memberInfo: MemberInfo)
```

Description: A remote user exited the current meeting.

Parameters:

| Parameter | Description |
| --- | --- |
| `memberInfo` | The last available Meeting member snapshot of the user who exited. |

Returns: None (`Unit`).

### onMemberUpdated(memberInfo)

```kotlin
fun onMemberUpdated(memberInfo: MemberInfo)
```

Description: The Meeting information of the specified member was refreshed.

Parameters:

| Parameter | Description |
| --- | --- |
| `memberInfo` | The updated member snapshot. |

Returns: None (`Unit`).

### onUserNameChanged(targetUid, nickname)

```kotlin
fun onUserNameChanged(targetUid: String, nickname: String)
```

Description: A member's nickname changed.

Parameters:

| Parameter | Description |
| --- | --- |
| `targetUid` | Target member UID. |
| `nickname` | The member's new nickname. |

Returns: None (`Unit`).

### onUserRoleChanged(targetUid, roleType)

```kotlin
fun onUserRoleChanged(targetUid: String, roleType: MemberRoleType)
```

Description: A member's role changed.

Parameters:

| Parameter | Description |
| --- | --- |
| `targetUid` | Target member UID. |
| `roleType` | The member's new role. |

Returns: None (`Unit`).

### onMeMembershipChanged(isMember)

```kotlin
fun onMeMembershipChanged(isMember: Boolean)
```

Description: The current user's identity changed between full member and audience.

Parameters:

| Parameter | Description |
| --- | --- |
| `isMember` | `true` means full member, `false` means audience. |

Returns: None (`Unit`).

## Devices and permissions

### onUserCameraStateChanged(targetUid, cameraState, reason)

```kotlin
fun onUserCameraStateChanged(
    targetUid: String,
    cameraState: DeviceState,
    reason: ChangeReason
)
```

Description: A member's camera state changed.

Parameters:

| Parameter | Description |
| --- | --- |
| `targetUid` | Target member UID. |
| `cameraState` | Open or closed state. |
| `reason` | Whether the member or the host made the change. |

Returns: None (`Unit`).

### onUserMicStateChanged(targetUid, micState, reason)

```kotlin
fun onUserMicStateChanged(
    targetUid: String,
    micState: DeviceState,
    reason: ChangeReason
)
```

Description: A member's mic state changed.

Parameters:

| Parameter | Description |
| --- | --- |
| `targetUid` | Target member UID. |
| `micState` | Mic open or closed state. |
| `reason` | Whether the member or the host made the change. |

Returns: None (`Unit`).

### onUserDrawDisabledChange(operatorUid, targetUid, disabled)

```kotlin
fun onUserDrawDisabledChange(
    operatorUid: String?,
    targetUid: String?,
    disabled: Boolean?
)
```

Description: The specified member's whiteboard drawing permission changed.

Parameters:

| Parameter | Description |
| --- | --- |
| `operatorUid` | Nullable operator UID. |
| `targetUid` | Nullable target member UID. |
| `disabled` | `true` disables drawing; `null` when it can't be parsed. |

Returns: None (`Unit`).

### onUserChatDisabledChange(operatorUid, disabled)

```kotlin
fun onUserChatDisabledChange(operatorUid: String?, disabled: Boolean)
```

Description: The current member's chat permission changed.

Parameters:

| Parameter | Description |
| --- | --- |
| `operatorUid` | Operator UID; may be `null` for system events. |
| `disabled` | `true` means the current member is not allowed to chat. |

Returns: None (`Unit`).

### onHandUpConfirm(operatorUid, targetUid, approved, handUpType)

```kotlin
fun onHandUpConfirm(
    operatorUid: String?,
    targetUid: String,
    approved: Boolean,
    handUpType: HandUpType
)
```

Description: The host handled the specified member's raise hand request.

Parameters:

| Parameter | Description |
| --- | --- |
| `operatorUid` | Nullable host UID. |
| `targetUid` | UID of the requesting member. |
| `approved` | `true` approves, `false` rejects. |
| `handUpType` | Raise hand request type. |

Returns: None (`Unit`).

## Host requests and member replies

### onRequestOpenCamera(operatorUid)

```kotlin
fun onRequestOpenCamera(operatorUid: String?)
```

Description: The current user received a request to turn on the camera.

Parameters:

| Parameter | Description |
| --- | --- |
| `operatorUid` | Requester UID; may be `null` when it can't be determined. |

Returns: None (`Unit`). Reply with `confirmOpenCameraAgree()` / `confirmOpenCameraRefuse()`.

### onRequestOpenMic(operatorUid)

```kotlin
fun onRequestOpenMic(operatorUid: String?)
```

Description: The current user received a request to turn on the mic.

Parameters:

| Parameter | Description |
| --- | --- |
| `operatorUid` | Requester UID; may be `null` when it can't be determined. |

Returns: None (`Unit`). Reply with `confirmOpenMicAgree()` / `confirmOpenMicRefuse()`.

### onRequestStartShare(operatorUid)

```kotlin
fun onRequestStartShare(operatorUid: String?)
```

Description: The current user received a request to start screen sharing.

Parameters:

| Parameter | Description |
| --- | --- |
| `operatorUid` | Requester UID; may be `null` when it can't be determined. |

Returns: None (`Unit`). Reply with `confirmStartScreenShareAgree()` / `confirmStartScreenShareRefuse()`.

### onUserConfirmOpenCamera(operatorUid, approved)

```kotlin
fun onUserConfirmOpenCamera(operatorUid: String, approved: Boolean)
```

Description: The target member replied to the request to turn on the camera.

Parameters:

| Parameter | Description |
| --- | --- |
| `operatorUid` | UID of the member who replied to the request. |
| `approved` | `true` means they agreed to turn on the camera, `false` means they declined. |

Returns: None (`Unit`).

### onUserConfirmOpenMic(operatorUid, approved)

```kotlin
fun onUserConfirmOpenMic(operatorUid: String, approved: Boolean)
```

Description: The target member replied to the request to turn on the mic.

Parameters:

| Parameter | Description |
| --- | --- |
| `operatorUid` | UID of the member who replied to the request. |
| `approved` | `true` means they agreed to turn on the mic, `false` means they declined. |

Returns: None (`Unit`).

## Waiting room and meeting moves

### onMoveInWaitingRoom(operatorUid, nickname)

```kotlin
fun onMoveInWaitingRoom(operatorUid: String?, nickname: String?)
```

Description: The current user was moved into the waiting room.

Parameters:

| Parameter | Description |
| --- | --- |
| `operatorUid` | Operator UID; may be `null` for system operations. |
| `nickname` | Operator nickname; may be `null` when it can't be determined. |

Returns: None (`Unit`).

### onUserEnterWaitingRoom(uid, nickname)

```kotlin
fun onUserEnterWaitingRoom(uid: String, nickname: String)
```

Description: A user entered the waiting room.

Parameters:

| Parameter | Description |
| --- | --- |
| `uid` | UID of the user who entered the waiting room. |
| `nickname` | User nickname. |

Returns: None (`Unit`).

### onUserExitWaitingRoom(uid, nickname)

```kotlin
fun onUserExitWaitingRoom(uid: String, nickname: String)
```

Description: A user exited the waiting room.

Parameters:

| Parameter | Description |
| --- | --- |
| `uid` | UID of the user who exited the waiting room. |
| `nickname` | User nickname. |

Returns: None (`Unit`).

### onRequestMoveToMainMeetOrSubMeet(targetMeetingId, targetMeetingTitle)

```kotlin
fun onRequestMoveToMainMeetOrSubMeet(
    targetMeetingId: String?,
    targetMeetingTitle: String?
)
```

Description: The current user was asked to move to the main meeting or the specified sub-meeting.

Parameters:

| Parameter | Description |
| --- | --- |
| `targetMeetingId` | Nullable target meeting ID. |
| `targetMeetingTitle` | Nullable target meeting title. |

Returns: None (`Unit`).

## Track changes

### onTrackAdded(uid, trackInfo)

```kotlin
fun onTrackAdded(uid: String, trackInfo: TrackInfo)
```

Description: A remote member added a media track.

Parameters:

| Parameter | Description |
| --- | --- |
| `uid` | UID of the member who added the track. |
| `trackInfo` | Information about the added track. |

Returns: None (`Unit`).

### onTrackUpdated(uid, trackInfo)

```kotlin
fun onTrackUpdated(uid: String, trackInfo: TrackInfo)
```

Description: The information of one of a remote member's media tracks was updated.

Parameters:

| Parameter | Description |
| --- | --- |
| `uid` | UID of the member whose track was updated. |
| `trackInfo` | The updated track information. |

Returns: None (`Unit`).

### onTrackRemoved(uid, trackInfo)

```kotlin
fun onTrackRemoved(uid: String, trackInfo: TrackInfo)
```

Description: A remote member removed a media track.

Parameters:

| Parameter | Description |
| --- | --- |
| `uid` | UID of the member who removed the track. |
| `trackInfo` | The last available snapshot of the removed track. |

Returns: None (`Unit`).
