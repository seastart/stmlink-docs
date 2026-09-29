---
title: "MeetingEngine"
description: "The single public entry point of the SMeeting Android SDK: initialization, pre-meeting management, entering and exiting meetings, meeting controls, local media, sharing, messages, remote subscription, cast codes, and virtual background. Look up any MeetingEngine method signature and behavior here."
---

`MeetingEngine` is the public business entry point of the SMeeting Android SDK, created with `MeetingEngine.create(application)`. It handles SDK initialization and release, pre-meeting management, entering and exiting meetings, in-meeting controls, local media, sharing, messages, and remote media subscription.

## Usage notes

+ Each call to `MeetingEngine.create(application)` creates one Engine instance. Your app should hold a single instance in one place within the process and call `release()` when it's no longer needed.
+ The current public API uses a single-meeting model: one Engine can have only one meeting that is being entered or active at a time; entering again returns `MeetingErrorCode.SESSION_ALREADY_ACTIVE`.
+ A successful entry returns [MeetingEnterInfo](/en/meeting/android/types#meetingenterinfo); in-meeting capabilities are then still called through the current `MeetingEngine`.
+ All asynchronous result callbacks stay on the thread they actually come from; the main thread is not guaranteed. Switch to the main thread before updating the UI.
+ The failure method of `MeetingResultCallback` / `MeetingValueResultCallback<T>` is `onFailure(errorCode, message)`. `message` is for diagnostics only and shouldn't be shown to users directly.
+ `roomEvent`, `userEvent`, `mediaEvent`, and `messageEvent` are bound to the current meeting and cleared when you exit the meeting; assign them again to receive events for the next meeting. Engine, IM, and device events share the Engine's lifecycle.

## Creation and version

### create(app)

```kotlin
fun create(app: Application): MeetingEngine
```

Description: Creates a `MeetingEngine` instance.

Parameters:

| Parameter | Description |
| --- | --- |
| `app` | `Application`, the application-level context. |

Returns: The newly created `MeetingEngine`.

### version()

```kotlin
fun version(): String
```

Description: Gets the Meeting SDK version number.

Parameters: None.

Returns: The version string written at build time, in the form `x.y.z`.

### buildTime()

```kotlin
fun buildTime(): String
```

Description: Gets the Meeting SDK build time.

Parameters: None.

Returns: The build time string.

## Manager properties

### infosManager

```kotlin
val infosManager: InfosManager
```

Description: Reads local snapshots of the current meeting, its members, and media tracks. This facade can be kept before the meeting; when you are not in a meeting, queries return null or empty collections. See [InfosManager](/en/meeting/android/api-reference/InfosManager).

### rollCallManager

```kotlin
val rollCallManager: RollCallManager
```

Description: The roll call management facade for the current meeting. When you are not in a meeting, asynchronous operations return `SESSION_NOT_ACTIVE` through the callback. See [RollCallManager](/en/meeting/android/api-reference/RollCallManager).

### signInManager

```kotlin
val signInManager: SignInManager
```

Description: The sign-in management facade for the current meeting. When you are not in a meeting, asynchronous operations return `SESSION_NOT_ACTIVE` through the callback. See [SignInManager](/en/meeting/android/api-reference/SignInManager).

## Event properties

Register a listener by assigning these properties directly; assign `null` to remove it. For each event's callback parameters and thread semantics, see the corresponding interface page.

| Property | Type | Scope |
| --- | --- | --- |
| `engineEvent` | `MeetingEngineEvent?` | Engine-wide runtime errors |
| `imEvent` | `MeetingImEvent?` | IM connection and business messages |
| `cameraDeviceEvent` | `MeetingCameraDeviceEvent?` | Process-wide shared camera device |
| `micDeviceEvent` | `MeetingMicDeviceEvent?` | Process-wide shared mic device |
| `localVideoFrameEvent` | `MeetingLocalVideoFrameEvent?` | Local captured video frames |
| `localAudioFrameEvent` | `MeetingLocalAudioFrameEvent?` | Local captured PCM frames |
| `screenCaptureEvent` | `MeetingScreenCaptureEvent?` | Local screen capture state |
| `roomEvent` | `MeetingRoomEvent?` | Room state and connection of the current meeting |
| `userEvent` | `MeetingUserEvent?` | Members, permissions, and tracks of the current meeting |
| `mediaEvent` | `MeetingMediaEvent?` | Media and quality statistics of the current meeting |
| `messageEvent` | `MeetingMessageEvent?` | Chat, system, and extension messages of the current meeting |

## Initialization and release

### initSdk(meetToken, options, callback)

```kotlin
fun initSdk(
    meetToken: String,
    options: RTCMediaOptions?,
    callback: MeetingResultCallback
)
```

Description: Initializes the service connection and the underlying SRTC SDK with a Meeting token. An invalid or expired token and local state errors are all returned through the result callback.

Parameters:

| Parameter | Description |
| --- | --- |
| `meetToken` | `String`, the initialization token issued by the Meeting server. |
| `options` | `RTCMediaOptions?`, the SRTC media configuration; pass `null` to use the default configuration. |
| `callback` | `MeetingResultCallback`, the single final-state callback for initialization. |

Returns: None (`Unit`).

### updateMediaOptions(options)

```kotlin
fun updateMediaOptions(options: RTCMediaOptions)
```

Description: Updates the underlying SRTC media parameters.

Parameters:

| Parameter | Description |
| --- | --- |
| `options` | `RTCMediaOptions`, the new media configuration. |

Returns: None (`Unit`).

### release()

```kotlin
fun release()
```

Description: Exits the current meeting, stops capture and subscriptions, closes IM, and releases Meeting and SRTC resources. The instance can't be used after release.

Parameters: None.

Returns: None (`Unit`).

## Media statistics and cloud recording capture

### getMetric()

```kotlin
fun getMetric(): MediaMetric.Metric?
```

Description: Gets the most recently sampled media quality snapshot of the current meeting; it doesn't actively trigger underlying statistics collection.

Parameters: None.

Returns: A thread-safe copy of `MediaMetric.Metric`; `null` when not in a meeting or before the first sample (about 5 seconds) has been produced. For the fields, see [Media quality](/en/meeting/android/media-quality).

### enableClientCloudRecordCapture

```kotlin
var enableClientCloudRecordCapture: Boolean
```

Description: Whether the client maintains the `TrackDesc.TRACK_SHARE` track used by cloud recording. When enabled, you can get the custom video track through `getShareCustomVideoTrack()`.

### getShareCustomVideoTrack(preOpt)

```kotlin
fun getShareCustomVideoTrack(preOpt: PreOptionCustomVideo?): LocalCustomVideoTrack?
```

Description: Gets or reuses the custom video track your app writes cloud recording video into. Your app must not publish or unpublish this track itself.

Parameters:

| Parameter | Description |
| --- | --- |
| `preOpt` | `PreOptionCustomVideo?`, custom video capture parameters; pass `null` to use the underlying default configuration. |

Returns: The cached or newly created `LocalCustomVideoTrack`; `null` when the underlying SRTC isn't ready yet or the track can't be created. `enableClientCloudRecordCapture` constrains the subsequent course recording publish flow; it doesn't prevent getting and writing to this track in advance.

## Current user info

### getSelfInfo(callback)

```kotlin
fun getSelfInfo(callback: MeetingValueResultCallback<UserBean>)
```

Description: Gets the currently logged-in user's info from the Meeting service.

Parameters:

| Parameter | Description |
| --- | --- |
| `callback` | Result callback that returns `UserBean` on success. |

Returns: None (the asynchronous result is delivered through the callback).

## Host member controls

### adminUpdateUserName(targetId, name, callback)

```kotlin
fun adminUpdateUserName(
    targetId: String,
    name: String,
    callback: MeetingResultCallback
)
```

Description: Changes the specified member's in-meeting display name.

Parameters:

| Parameter | Description |
| --- | --- |
| `targetId` | Target member UID. |
| `name` | New nickname. |
| `callback` | Update result callback. |

Returns: None (the asynchronous result is delivered through the callback).

### adminUpdateUserRole(targetId, role, callback)

```kotlin
fun adminUpdateUserRole(
    targetId: String,
    role: MemberRoleType,
    callback: MeetingResultCallback
)
```

Description: Changes the specified member's meeting role.

Parameters:

| Parameter | Description |
| --- | --- |
| `targetId` | Target member UID. |
| `role` | The new `MemberRoleType`. |
| `callback` | Update result callback. |

Returns: None (the asynchronous result is delivered through the callback).

### adminMoveHost(targetId, callback)

```kotlin
fun adminMoveHost(targetId: String, callback: MeetingResultCallback)
```

Description: Transfers the host role to the specified member.

Parameters:

| Parameter | Description |
| --- | --- |
| `targetId` | UID of the new host. |
| `callback` | Transfer result callback. |

Returns: None (the asynchronous result is delivered through the callback).

### adminUpdateUserDrawDisabled(targetId, drawDisabled, callback)

```kotlin
fun adminUpdateUserDrawDisabled(
    targetId: String,
    drawDisabled: Boolean,
    callback: MeetingResultCallback
)
```

Description: Updates the specified member's whiteboard drawing permission.

Parameters:

| Parameter | Description |
| --- | --- |
| `targetId` | Target member UID. |
| `drawDisabled` | `true` means drawing is disabled. |
| `callback` | Update result callback. |

Returns: None (the asynchronous result is delivered through the callback).

### adminUpdateUserChatDisabled(targetId, chatDisabled, callback)

```kotlin
fun adminUpdateUserChatDisabled(
    targetId: String,
    chatDisabled: Boolean,
    callback: MeetingResultCallback
)
```

Description: Updates the specified member's chat permission.

Parameters:

| Parameter | Description |
| --- | --- |
| `targetId` | Target member UID. |
| `chatDisabled` | `true` means chat is disabled. |
| `callback` | Update result callback. |

Returns: None (the asynchronous result is delivered through the callback).

### adminRequestUserOpenCamera(targetId, callback)

```kotlin
fun adminRequestUserOpenCamera(targetId: String, callback: MeetingResultCallback)
```

Description: Asks the specified member to turn on the camera; the member receives the request through `MeetingUserEvent.onRequestOpenCamera()`.

Parameters:

| Parameter | Description |
| --- | --- |
| `targetId` | Target member UID. |
| `callback` | Request submission result callback. |

Returns: None (the asynchronous result is delivered through the callback).

### adminCloseUserCamera(targetId, callback)

```kotlin
fun adminCloseUserCamera(targetId: String, callback: MeetingResultCallback)
```

Description: The host turns off the specified member's camera.

Parameters:

| Parameter | Description |
| --- | --- |
| `targetId` | Target member UID. |
| `callback` | Operation result callback. |

Returns: None (the asynchronous result is delivered through the callback).

### adminDisableUserCamera(targetId, cameraDisabled, callback)

```kotlin
fun adminDisableUserCamera(
    targetId: String,
    cameraDisabled: Boolean,
    callback: MeetingResultCallback
)
```

Description: Reserved API for disabling a member's camera.

Parameters:

| Parameter | Description |
| --- | --- |
| `targetId` | Target member UID. |
| `cameraDisabled` | Target disabled state. |
| `callback` | Result callback. |

Returns: None (the asynchronous result is delivered through the callback).

:::warning
This capability isn't implemented in the current version; don't rely on it for meeting controls. To turn off a camera immediately, use `adminCloseUserCamera()`.
:::

### adminRequestUserOpenMic(targetId, callback)

```kotlin
fun adminRequestUserOpenMic(targetId: String, callback: MeetingResultCallback)
```

Description: Asks the specified member to turn on the mic; the member receives the request through `MeetingUserEvent.onRequestOpenMic()`.

Parameters:

| Parameter | Description |
| --- | --- |
| `targetId` | Target member UID. |
| `callback` | Request submission result callback. |

Returns: None (the asynchronous result is delivered through the callback).

### adminCloseUserMic(targetId, callback)

```kotlin
fun adminCloseUserMic(targetId: String, callback: MeetingResultCallback)
```

Description: The host turns off the specified member's mic.

Parameters:

| Parameter | Description |
| --- | --- |
| `targetId` | Target member UID. |
| `callback` | Operation result callback. |

Returns: None (the asynchronous result is delivered through the callback).

### adminDisableUserMic(targetId, micDisabled, callback)

```kotlin
fun adminDisableUserMic(
    targetId: String,
    micDisabled: Boolean,
    callback: MeetingResultCallback
)
```

Description: Reserved API for disabling a member's mic.

Parameters:

| Parameter | Description |
| --- | --- |
| `targetId` | Target member UID. |
| `micDisabled` | Target disabled state. |
| `callback` | Result callback. |

Returns: None (the asynchronous result is delivered through the callback).

:::warning
This capability isn't implemented in the current version; don't rely on it for meeting controls. To turn off a mic immediately, use `adminCloseUserMic()`.
:::

### adminRequestUserShare(targetId, callback)

```kotlin
fun adminRequestUserShare(targetId: String, callback: MeetingResultCallback)
```

Description: Asks the specified member to start screen sharing.

Parameters:

| Parameter | Description |
| --- | --- |
| `targetId` | Target member UID. |
| `callback` | Request submission result callback. |

Returns: None (the asynchronous result is delivered through the callback).

### adminStopRoomShare(callback)

```kotlin
fun adminStopRoomShare(callback: MeetingResultCallback)
```

Description: Forcibly stops the screen or whiteboard sharing currently in progress in the room.

Parameters:

| Parameter | Description |
| --- | --- |
| `callback` | Stop sharing result callback. |

Returns: None (the asynchronous result is delivered through the callback).

### adminInviteAgent(agents, callback)

```kotlin
fun adminInviteAgent(
    agents: List<AgentRequestBean>,
    callback: MeetingResultCallback
)
```

Description: Invites external devices such as SIP, H.323, RTSP, and RTMP devices into the current meeting.

Parameters:

| Parameter | Description |
| --- | --- |
| `agents` | List of device types and contact identifiers. |
| `callback` | Invitation result callback. |

Returns: None (the asynchronous result is delivered through the callback).

### adminKickUserOut(targetId, callback)

```kotlin
fun adminKickUserOut(targetId: String, callback: MeetingResultCallback)
```

Description: Removes the specified member from the current meeting.

Parameters:

| Parameter | Description |
| --- | --- |
| `targetId` | Target member UID. |
| `callback` | Operation result callback. |

Returns: None (the asynchronous result is delivered through the callback).

### adminConfirmHandUp(targetId, code, approve, callback)

```kotlin
fun adminConfirmHandUp(
    targetId: String,
    code: HandUpType,
    approve: Boolean,
    callback: MeetingResultCallback
)
```

Description: Handles the specified member's raise-hand request.

Parameters:

| Parameter | Description |
| --- | --- |
| `targetId` | UID of the requesting member. |
| `code` | Raise-hand type. |
| `approve` | `true` approves, `false` declines. |
| `callback` | Handling result callback. |

Returns: None (the asynchronous result is delivered through the callback).

### adminGetOnlineMembers(meetingId, page, prePage, callback)

```kotlin
fun adminGetOnlineMembers(
    meetingId: String?,
    page: Int,
    prePage: Int,
    callback: MeetingValueResultCallback<MeetingPage<MemberBean>>
)
```

Description: Queries the online members of the specified meeting page by page.

Parameters:

| Parameter | Description |
| --- | --- |
| `meetingId` | Target meeting ID; pass `null` to use the current meeting. |
| `page` | Page number, starting from `1`. |
| `prePage` | Maximum number of items per page. The parameter name is a historical spelling and means the same as `perPage`. |
| `callback` | Callback that returns the paginated online members on success. |

Returns: None (the asynchronous result is delivered through the callback).

### adminUpdateRoomMCUMode()

```kotlin
fun adminUpdateRoomMCUMode()
```

Description: Reserved entry point for updating the room's MCU mode.

Parameters: None.

Returns: None (`Unit`).

:::warning
This API isn't implemented in the current version; calling it only logs a warning.
:::

## Waiting room

### adminWaitingRoomDisabled(waitingRoomDisabled, callback)

```kotlin
fun adminWaitingRoomDisabled(
    waitingRoomDisabled: Boolean,
    callback: MeetingResultCallback
)
```

Description: Enables or disables the current meeting's waiting room.

Parameters:

| Parameter | Description |
| --- | --- |
| `waitingRoomDisabled` | `true` disables the waiting room, `false` enables it. |
| `callback` | Update result callback. |

Returns: None (the asynchronous result is delivered through the callback).

### adminMoveOutWaitingRoom(uid, callback)

```kotlin
fun adminMoveOutWaitingRoom(uid: String?, callback: MeetingResultCallback)
```

Description: Admits waiting room members into the meeting.

Parameters:

| Parameter | Description |
| --- | --- |
| `uid` | Target member UID; pass `null` to handle all members in the waiting room. |
| `callback` | Operation result callback. |

Returns: None (the asynchronous result is delivered through the callback).

### adminMoveInWaitingRoom(uid, nickName, callback)

```kotlin
fun adminMoveInWaitingRoom(
    uid: String,
    nickName: String,
    callback: MeetingResultCallback
)
```

Description: Moves a current meeting member into the waiting room.

Parameters:

| Parameter | Description |
| --- | --- |
| `uid` | Target member UID. |
| `nickName` | Target member nickname. |
| `callback` | Operation result callback. |

Returns: None (the asynchronous result is delivered through the callback).

### adminGetWaitingRoomUsers(callback)

```kotlin
fun adminGetWaitingRoomUsers(
    callback: MeetingValueResultCallback<List<WaitingRoomUserBean>>
)
```

Description: Queries the members in the current meeting's waiting room.

Parameters:

| Parameter | Description |
| --- | --- |
| `callback` | Callback that returns the list of waiting room members on success. |

Returns: None (the asynchronous result is delivered through the callback).

## Sub-meetings

### createSubMeeting(subMeetingTitles, callback)

```kotlin
fun createSubMeeting(
    subMeetingTitles: MutableList<String>,
    callback: MeetingResultCallback
)
```

Description: Creates one or more sub-meetings under the current main meeting.

Parameters:

| Parameter | Description |
| --- | --- |
| `subMeetingTitles` | List of sub-meeting titles. |
| `callback` | Creation result callback. |

Returns: None (the asynchronous result is delivered through the callback).

### updateSubMeetingTitle(id, title, callback)

```kotlin
fun updateSubMeetingTitle(
    id: String,
    title: String,
    callback: MeetingResultCallback
)
```

Description: Changes the title of the specified sub-meeting.

Parameters:

| Parameter | Description |
| --- | --- |
| `id` | Sub-meeting record ID. |
| `title` | New title. |
| `callback` | Update result callback. |

Returns: None (the asynchronous result is delivered through the callback).

### updateSubMeetingUsers(id, members, callback)

```kotlin
fun updateSubMeetingUsers(
    id: String,
    members: MutableList<MemberRequestBean>,
    callback: MeetingResultCallback
)
```

Description: Replaces the members of the specified sub-meeting in full.

Parameters:

| Parameter | Description |
| --- | --- |
| `id` | Sub-meeting record ID. |
| `members` | List of target member UIDs and nicknames. |
| `callback` | Update result callback. |

Returns: None (the asynchronous result is delivered through the callback).

### deleteSubMeeting(ids, callback)

```kotlin
fun deleteSubMeeting(ids: MutableList<String>, callback: MeetingResultCallback)
```

Description: Deletes the specified sub-meetings.

Parameters:

| Parameter | Description |
| --- | --- |
| `ids` | List of sub-meeting record IDs. |
| `callback` | Deletion result callback. |

Returns: None (the asynchronous result is delivered through the callback).

### getSubMeetingList(callback)

```kotlin
fun getSubMeetingList(
    callback: MeetingValueResultCallback<List<SubMeetingBean>>
)
```

Description: Queries the list of sub-meetings under the current main meeting.

Parameters:

| Parameter | Description |
| --- | --- |
| `callback` | Callback that returns the list of sub-meetings on success. |

Returns: None (the asynchronous result is delivered through the callback).

### startSubMeeting(ids, callback)

```kotlin
fun startSubMeeting(ids: MutableList<String>, callback: MeetingResultCallback)
```

Description: Starts the specified sub-meetings.

Parameters:

| Parameter | Description |
| --- | --- |
| `ids` | List of sub-meeting record IDs. |
| `callback` | Start result callback. |

Returns: None (the asynchronous result is delivered through the callback).

### stopSubMeeting(ids, callback)

```kotlin
fun stopSubMeeting(ids: MutableList<String>, callback: MeetingResultCallback)
```

Description: Ends the specified sub-meetings.

Parameters:

| Parameter | Description |
| --- | --- |
| `ids` | List of sub-meeting record IDs. |
| `callback` | Stop result callback. |

Returns: None (the asynchronous result is delivered through the callback).

### moveSubMeetingUser(fromId, toId, uid, callback)

```kotlin
fun moveSubMeetingUser(
    fromId: String,
    toId: String?,
    uid: String,
    callback: MeetingResultCallback
)
```

Description: Moves members between the main meeting and sub-meetings.

Parameters:

| Parameter | Description |
| --- | --- |
| `fromId` | Source sub-meeting record ID. |
| `toId` | Target sub-meeting record ID; pass `null` to move back to the main meeting. |
| `uid` | Target member UID. |
| `callback` | Move result callback. |

Returns: None (the asynchronous result is delivered through the callback).

### updateEnterBeforeHostDisabled(meetingId, enterBeforeHostDisabled, callback)

```kotlin
fun updateEnterBeforeHostDisabled(
    meetingId: String,
    enterBeforeHostDisabled: Boolean,
    callback: MeetingResultCallback
)
```

Description: Updates whether members can enter the specified meeting before the host.

Parameters:

| Parameter | Description |
| --- | --- |
| `meetingId` | Meeting ID of the target main meeting or sub-meeting. |
| `enterBeforeHostDisabled` | `true` means entering before the host is not allowed. |
| `callback` | Update result callback. |

Returns: None (the asynchronous result is delivered through the callback).

### helpSubMeeting(meetingId, callback)

```kotlin
fun helpSubMeeting(meetingId: String, callback: MeetingResultCallback)
```

Description: Asks the host of the main meeting for help from a sub-meeting.

Parameters:

| Parameter | Description |
| --- | --- |
| `meetingId` | Meeting ID of the current sub-meeting. |
| `callback` | Request submission result callback. |

Returns: None (the asynchronous result is delivered through the callback).

## Current user's nickname

### updateName(name, callback)

```kotlin
fun updateName(name: String, callback: MeetingResultCallback)
```

Description: Changes the current user's in-meeting display name.

Parameters:

| Parameter | Description |
| --- | --- |
| `name` | New nickname. |
| `callback` | Update result callback. |

Returns: None (the asynchronous result is delivered through the callback).

## Users, IM, and calls

### getAgentList(types, keyword, page, perPage, callback)

```kotlin
fun getAgentList(
    types: MutableList<AgentType>,
    keyword: String,
    page: Int,
    perPage: Int,
    callback: MeetingValueResultCallback<MeetingPage<AgentBean>>
)
```

Description: Queries invitable contact devices page by page, by device type and keyword.

Parameters:

| Parameter | Description |
| --- | --- |
| `types` | List of `AgentType` values to query. |
| `keyword` | Filter keyword for the fields the server supports; pass an empty string for no filtering. |
| `page` | Page number, starting from `1`. |
| `perPage` | Maximum number of items per page. |
| `callback` | Result callback that returns `MeetingPage<AgentBean>` on success. |

Returns: None (the asynchronous result is delivered through the callback).

### enableIm(callback)

```kotlin
fun enableIm(callback: MeetingValueResultCallback<MeetingImConnection>)
```

Description: Requests an IM grant and establishes the connection. After the connection is established, ongoing state and messages are delivered through `imEvent`.

Parameters:

| Parameter | Description |
| --- | --- |
| `callback` | Result callback that returns `MeetingImConnection(uid, sid)` on success. |

Returns: None (the asynchronous result is delivered through the callback).

### disableIm()

```kotlin
fun disableIm()
```

Description: Explicitly closes IM. Closing it explicitly doesn't trigger `MeetingImEvent.onImDisconnected()`.

Parameters: None.

Returns: None (`Unit`).

### callUser(targetUids, callback)

```kotlin
fun callUser(targetUids: MutableList<String>, callback: MeetingResultCallback)
```

Description: Calls the specified users to enter the current meeting.

Parameters:

| Parameter | Description |
| --- | --- |
| `targetUids` | List of target user UIDs. |
| `callback` | Server submission result callback. |

Returns: None (the asynchronous result is delivered through the callback).

## Pre-meeting management

### createImmediateMeeting(title, option, callback)

```kotlin
fun createImmediateMeeting(
    title: String,
    option: CreateImmediateMeetingOption,
    callback: MeetingValueResultCallback<MeetingCreatedBean>
)
```

Description: Creates an instant meeting.

Parameters:

| Parameter | Description |
| --- | --- |
| `title` | Meeting title. |
| `option` | Optional parameters for the instant meeting. |
| `callback` | Callback that returns the meeting ID and room number on success. |

Returns: None (the asynchronous result is delivered through the callback).

### createScheduleMeeting(title, planTime, planDur, option, callback)

```kotlin
fun createScheduleMeeting(
    title: String,
    planTime: Long,
    planDur: Int,
    option: CreateScheduleMeetingOption,
    callback: MeetingValueResultCallback<MeetingCreatedBean>
)
```

Description: Creates a scheduled meeting.

Parameters:

| Parameter | Description |
| --- | --- |
| `title` | Meeting title. |
| `planTime` | Planned start time, a Unix timestamp in seconds. |
| `planDur` | Planned duration in minutes. |
| `option` | Optional parameters for the scheduled meeting. |
| `callback` | Callback that returns the meeting ID and room number on success. |

Returns: None (the asynchronous result is delivered through the callback).

### updateMeetingBeforeStart(meetingId, option, callback)

```kotlin
fun updateMeetingBeforeStart(
    meetingId: String,
    option: UpdateMeetingOption,
    callback: MeetingResultCallback
)
```

Description: Updates a meeting that hasn't started yet.

Parameters:

| Parameter | Description |
| --- | --- |
| `meetingId` | Target meeting ID. |
| `option` | Fields to update; nullable fields that aren't set are not updated. |
| `callback` | Update result callback. |

Returns: None (the asynchronous result is delivered through the callback).

### getMeetingList(page, perPage, callback)

```kotlin
fun getMeetingList(
    page: Int,
    perPage: Int,
    callback: MeetingValueResultCallback<MeetingPage<MeetInfo>>
)
```

Description: Queries the current user's upcoming or in-progress meetings page by page.

Parameters:

| Parameter | Description |
| --- | --- |
| `page` | Page number, starting from `1`. |
| `perPage` | Maximum number of items per page. |
| `callback` | Callback that returns the paginated meetings on success. |

Returns: None (the asynchronous result is delivered through the callback).

### getHistoryMeetingList(page, perPage, callback)

```kotlin
fun getHistoryMeetingList(
    page: Int,
    perPage: Int,
    callback: MeetingValueResultCallback<MeetingPage<MeetInfo>>
)
```

Description: Queries the current user's past meetings page by page.

Parameters:

| Parameter | Description |
| --- | --- |
| `page` | Page number, starting from `1`. |
| `perPage` | Maximum number of items per page. |
| `callback` | Callback that returns the paginated past meetings on success. |

Returns: None (the asynchronous result is delivered through the callback).

### getMeetingDetail(meetingId, callback)

```kotlin
fun getMeetingDetail(
    meetingId: String,
    callback: MeetingValueResultCallback<MeetDetail>
)
```

Description: Queries meeting details by meeting ID.

Parameters:

| Parameter | Description |
| --- | --- |
| `meetingId` | Target meeting ID. |
| `callback` | Result callback that returns `MeetDetail` on success. |

Returns: None (the asynchronous result is delivered through the callback).

### getMeetingDetailByRoomNo(roomNo, callback)

```kotlin
fun getMeetingDetailByRoomNo(
    roomNo: String,
    callback: MeetingValueResultCallback<MeetDetail>
)
```

Description: Queries meeting details by room number.

Parameters:

| Parameter | Description |
| --- | --- |
| `roomNo` | Target room number. |
| `callback` | Result callback that returns `MeetDetail` on success. |

Returns: None (the asynchronous result is delivered through the callback).

### cancelMeetingBeforeStart(meetingId, callback)

```kotlin
fun cancelMeetingBeforeStart(meetingId: String, callback: MeetingResultCallback)
```

Description: Cancels a meeting that hasn't started yet.

Parameters:

| Parameter | Description |
| --- | --- |
| `meetingId` | Target meeting ID. |
| `callback` | Cancellation result callback. |

Returns: None (the asynchronous result is delivered through the callback).

## Entering and exiting meetings

### enterMeeting(activity, roomNo, password, nick, avatar, streamVendor, isAudience, extendInfo, callback)

```kotlin
fun enterMeeting(
    activity: Activity,
    roomNo: String,
    password: String?,
    nick: String,
    avatar: String,
    streamVendor: String,
    isAudience: Boolean,
    extendInfo: String?,
    callback: MeetingValueResultCallback<MeetingEnterInfo>
)
```

Description: Queries the meeting details by room number, enters the meeting on the server, and joins the SRTC channel, returning a single final result.

Parameters:

| Parameter | Description |
| --- | --- |
| `activity` | The current `Activity`, required for the SRTC join. |
| `roomNo` | Target room number. |
| `password` | Meeting password; pass `null` if there is none. |
| `nick` | Nickname for this meeting entry. |
| `avatar` | Avatar URL or business avatar identifier; pass an empty string if there is none. |
| `streamVendor` | Streaming vendor identifier agreed with the server, such as `wangsucdn`. |
| `isAudience` | Whether to enter the meeting as audience; audience members can't open devices, share, or publish streams. |
| `extendInfo` | Business extension string; pass `null` if there is none. |
| `callback` | Result callback that returns `MeetingEnterInfo(meetingId, uid)` on success. |

Returns: None (the asynchronous result is delivered through the callback).

### enterMeetingByMeetingId(activity, meetingId, password, nick, avatar, streamVendor, isAudience, extendInfo, callback)

```kotlin
fun enterMeetingByMeetingId(
    activity: Activity,
    meetingId: String,
    password: String?,
    nick: String,
    avatar: String,
    streamVendor: String,
    isAudience: Boolean,
    extendInfo: String?,
    callback: MeetingValueResultCallback<MeetingEnterInfo>
)
```

Description: Enters a meeting by meeting ID; the flow and callback semantics are the same as `enterMeeting()`.

Parameters:

| Parameter | Description |
| --- | --- |
| `activity` | The current `Activity`, required for the SRTC join. |
| `meetingId` | Target meeting ID. |
| `password` | Meeting password; pass `null` if there is none. |
| `nick` | Nickname for this meeting entry. |
| `avatar` | Avatar URL or business avatar identifier. |
| `streamVendor` | Streaming vendor identifier agreed with the server. |
| `isAudience` | Whether to enter the meeting as audience. |
| `extendInfo` | Business extension string; pass `null` if there is none. |
| `callback` | Result callback that returns `MeetingEnterInfo` on success. |

Returns: None (the asynchronous result is delivered through the callback).

### exitWaitingRoom(callback)

```kotlin
fun exitWaitingRoom(callback: MeetingResultCallback)
```

Description: Exits the current waiting room before the SRTC join has completed.

Parameters:

| Parameter | Description |
| --- | --- |
| `callback` | Exit result callback; returns `WAITING_ROOM_CONTEXT_MISSING` when the waiting room context is missing. |

Returns: None (the asynchronous result is delivered through the callback).

### exitMeeting()

```kotlin
fun exitMeeting()
```

Description: Exits the current meeting and stops that meeting's capture, sharing, remote subscriptions, and further event dispatch. Safe to call repeatedly.

Parameters: None.

Returns: None (`Unit`).

## Host room controls

### adminDestroyMeeting(callback)

```kotlin
fun adminDestroyMeeting(callback: MeetingResultCallback)
```

Description: The host ends the current meeting.

Parameters:

| Parameter | Description |
| --- | --- |
| `callback` | End meeting result callback. |

Returns: None (the asynchronous result is delivered through the callback).

### adminUpdateConferee(conferees, callback)

```kotlin
fun adminUpdateConferee(
    conferees: MutableList<String>,
    callback: MeetingResultCallback
)
```

Description: Updates the current meeting's pre-meeting invitee UID list.

Parameters:

| Parameter | Description |
| --- | --- |
| `conferees` | Complete invitee UID list. |
| `callback` | Update result callback. |

Returns: None (the asynchronous result is delivered through the callback).

### adminUpdateRoomCameraState(selfUnMuteCameraDisabled, cameraDisabled, callback)

```kotlin
fun adminUpdateRoomCameraState(
    selfUnMuteCameraDisabled: Boolean,
    cameraDisabled: Boolean,
    callback: MeetingResultCallback
)
```

Description: Updates both the room-wide camera disabled state and the policy for whether members can turn it back on themselves.

Parameters:

| Parameter | Description |
| --- | --- |
| `selfUnMuteCameraDisabled` | `true` means members can't turn their cameras back on themselves. |
| `cameraDisabled` | `true` means cameras are disabled for everyone. |
| `callback` | Update result callback. |

Returns: None (the asynchronous result is delivered through the callback).

### adminUpdateRoomSelfUnmuteCameraDisabled(selfUnMuteCameraDisabled, callback)

```kotlin
fun adminUpdateRoomSelfUnmuteCameraDisabled(
    selfUnMuteCameraDisabled: Boolean,
    callback: MeetingResultCallback
)
```

Description: Updates only whether members can turn their cameras back on themselves.

Parameters:

| Parameter | Description |
| --- | --- |
| `selfUnMuteCameraDisabled` | `true` means members can't turn their cameras back on themselves. |
| `callback` | Update result callback. |

Returns: None (the asynchronous result is delivered through the callback).

### adminUpdateRoomMicState(selfUnMuteMicDisabled, micDisabled, callback)

```kotlin
fun adminUpdateRoomMicState(
    selfUnMuteMicDisabled: Boolean,
    micDisabled: Boolean,
    callback: MeetingResultCallback
)
```

Description: Updates both the room-wide mic disabled state and the policy for whether members can unmute themselves.

Parameters:

| Parameter | Description |
| --- | --- |
| `selfUnMuteMicDisabled` | `true` means members can't unmute themselves. |
| `micDisabled` | `true` means mics are disabled for everyone. |
| `callback` | Update result callback. |

Returns: None (the asynchronous result is delivered through the callback).

### adminUpdateRoomSelfUnmuteMicDisabled(selfUnMuteMicDisabled, callback)

```kotlin
fun adminUpdateRoomSelfUnmuteMicDisabled(
    selfUnMuteMicDisabled: Boolean,
    callback: MeetingResultCallback
)
```

Description: Updates only whether members can unmute themselves.

Parameters:

| Parameter | Description |
| --- | --- |
| `selfUnMuteMicDisabled` | `true` means members can't unmute themselves. |
| `callback` | Update result callback. |

Returns: None (the asynchronous result is delivered through the callback).

### adminUpdateRoomShareState(shareDisabled, callback)

```kotlin
fun adminUpdateRoomShareState(shareDisabled: Boolean, callback: MeetingResultCallback)
```

Description: Updates the room's sharing disabled state.

Parameters:

| Parameter | Description |
| --- | --- |
| `shareDisabled` | `true` means members can't start sharing. |
| `callback` | Update result callback. |

Returns: None (the asynchronous result is delivered through the callback).

### adminUpdateRoomChatDisabled(chatDisabled, callback)

```kotlin
fun adminUpdateRoomChatDisabled(chatDisabled: Boolean, callback: MeetingResultCallback)
```

Description: Updates the room's text chat disabled state.

Parameters:

| Parameter | Description |
| --- | --- |
| `chatDisabled` | `true` means chat is disabled. |
| `callback` | Update result callback. |

Returns: None (the asynchronous result is delivered through the callback).

### adminUpdateRoomScreenshotDisabled(screenshotDisabled, callback)

```kotlin
fun adminUpdateRoomScreenshotDisabled(
    screenshotDisabled: Boolean,
    callback: MeetingResultCallback
)
```

Description: Updates the room's screenshot disabled state; your app still needs to enforce the screenshot restriction on Android itself.

Parameters:

| Parameter | Description |
| --- | --- |
| `screenshotDisabled` | `true` means screenshots are disallowed at the business level. |
| `callback` | Update result callback. |

Returns: None (the asynchronous result is delivered through the callback).

### adminUpdateRoomWatermarkDisabled(watermarkDisabled, callback)

```kotlin
fun adminUpdateRoomWatermarkDisabled(
    watermarkDisabled: Boolean,
    callback: MeetingResultCallback
)
```

Description: Updates the room's watermark disabled state.

Parameters:

| Parameter | Description |
| --- | --- |
| `watermarkDisabled` | `true` means the watermark is disabled. |
| `callback` | Update result callback. |

Returns: None (the asynchronous result is delivered through the callback).

### adminUpdateRoomLocked(locked, callback)

```kotlin
fun adminUpdateRoomLocked(locked: Boolean, callback: MeetingResultCallback)
```

Description: Updates the room's locked state.

Parameters:

| Parameter | Description |
| --- | --- |
| `locked` | `true` means the room is locked. |
| `callback` | Update result callback. |

Returns: None (the asynchronous result is delivered through the callback).

## Local camera

### openCamera(view, preOption, callback)

```kotlin
fun openCamera(
    view: View?,
    preOption: PreOptionCamera?,
    callback: MeetingResultCallback
)
```

Description: Only starts local camera capture and preview, without requesting meeting permission or publishing video; can be called before the meeting once initialization succeeds.

If capture is already running or starting, the existing operation is reused and the new `preOption` doesn't take effect; to change parameters, call `closeCamera()` first. The device ID and facing in the start parameters are suggestions; if unavailable, RTC picks another automatically. If an in-flight start is canceled by a switch or close, the callback returns `LOCAL_DEVICE_OPERATION_CANCELLED`.

Parameters:

| Parameter | Description |
| --- | --- |
| `view` | Optional preview view; only the SRTC-specified `VcsPlayerGlTextureView` / `VcsPlayerGlSurfaceView` are supported. |
| `preOption` | Camera preset; pass `null` to reuse the existing Track configuration; the first time, the SRTC default 480P configuration is used. |
| `callback` | Result callback after physical capture has started stably. |

Returns: None (the asynchronous result is delivered through the callback).

### openCameraAndPublish(view, preOption, callback)

```kotlin
fun openCameraAndPublish(
    view: View?,
    preOption: PreOptionCamera?,
    callback: MeetingResultCallback
)
```

Description: Completes server-side authorization, camera capture, and SRTC publishing in the current meeting. A regular failure rolls back this publish and closes only the capture generation it belongs to, without stopping later switches or recoveries; if the capture is superseded by a newer switch, the callback returns `LOCAL_DEVICE_OPERATION_CANCELLED`, which ends only the old publish transaction and doesn't stop the new switch.

Parameters:

| Parameter | Description |
| --- | --- |
| `view` | Optional local preview view; same type restrictions as `openCamera()`. |
| `preOption` | Camera capture preset; pass `null` to use the default configuration. |
| `callback` | Result callback after authorization, capture, and publishing have all completed. |

Returns: None (the asynchronous result is delivered through the callback).

### closeCamera()

```kotlin
fun closeCamera()
```

Description: Unpublishes the camera in the current meeting and stops local capture; when not in a meeting, only stops local capture.

Parameters: None.

Returns: None (`Unit`).

### switchCamera(isFrontCamera)

```kotlin
fun switchCamera(isFrontCamera: Boolean)
fun switchCamera(isFrontCamera: Boolean, callback: MeetingResultCallback?)
```

Description: Tries devices only within the specified facing, using the first frame of the new video as the success criterion.

**Compatibility change (Meeting 2.0.37, RTC 2.0.33): after a failed switch, capture is not guaranteed to continue and there is no longer an automatic fallback; if target validation fails, the original capture may be kept.** Your app must roll back the UI and decide for itself whether to recover. If the Track has never been created, the intent is only saved and the callback reports success without opening the device; if the Track exists, the switch reopens capture even after `closeCamera()` (without publishing automatically). We recommend disabling the switch control while the camera is off.

When the request is canceled by a later switch or by `closeCamera()`, the callback returns `MeetingErrorCode.LOCAL_DEVICE_OPERATION_CANCELLED`. A cancellation represents a newer user intent—**don't recover in the cancellation callback**. SDK `release()` clears the waiters and no longer delivers cancellation callbacks.

Parameters:

| Parameter | Description |
| --- | --- |
| `isFrontCamera` | `true` uses the front camera, `false` uses the rear camera. |
| `callback` | `MeetingResultCallback?` for the overload with a callback, can be null; the first-frame success or failure result. |

Returns: None (`Unit`).

### getCameraDevices()

```kotlin
fun getCameraDevices(): List<CameraDeviceCapability>
```

Description: Gets a snapshot of the camera capabilities SRTC currently recognizes.

Parameters: None.

Returns: The list of camera device capabilities; an empty list when there is no available device.

### switchCameraDevice(cameraId)

```kotlin
fun switchCameraDevice(cameraId: String)
fun switchCameraDevice(cameraId: String, callback: MeetingResultCallback?)
```

Description: Tries only the specified Camera2 device ID, using the first frame as the success criterion; on failure it doesn't pick another device or fall back automatically. If no Track has been created, the intent is saved; if a Track exists, capture is reopened even if it has stopped. Cancellation and release behave the same as `switchCamera`.

For an exact recovery, call this method again with the `getCurrentCameraId()` snapshot taken **before the switch**; the suggestion semantics of `openCamera` can't guarantee a return to the original device.

Parameters:

| Parameter | Description |
| --- | --- |
| `cameraId` | Camera ID returned by `getCameraDevices()`. |
| `callback` | `MeetingResultCallback?` for the overload with a callback, can be null; the first-frame success or failure result. |

Returns: None (`Unit`).

### getCurrentCameraId()

```kotlin
fun getCurrentCameraId(): String
```

Returns the ID of the last camera that actually produced a first frame; returns an empty string when the SDK isn't ready, capture hasn't succeeded yet, or after release. The value is a historical record and **doesn't mean capture is in progress**; it may keep an old value during a switch, after a failure, after stopping, or after the device is unplugged.

### App-level exact recovery example

Start the switch on the UI thread. `cameraUiGeneration` is maintained by your app and incremented each time the camera is turned off, switched again, or the screen is destroyed; `cameraEnabled` indicates that your app still wants capture, preventing late callbacks from reopening the device. `runOnUiThread`, `updateCameraUi`, and `showCameraLost` are your app's own UI methods.

```kotlin
val generation = ++cameraUiGeneration
val previousId = engine.getCurrentCameraId() // Must be snapshotted before the switch
engine.switchCamera(targetFront, object : MeetingResultCallback {
    override fun onSuccess() = runOnUiThread {
        if (generation == cameraUiGeneration && cameraEnabled) updateCameraUi()
    }

    override fun onFailure(errorCode: Int, message: String?) = runOnUiThread {
        if (generation != cameraUiGeneration || !cameraEnabled) return@runOnUiThread
        if (errorCode == MeetingErrorCode.LOCAL_DEVICE_OPERATION_CANCELLED ||
            errorCode == MeetingErrorCode.SESSION_OPERATION_CANCELLED ||
            errorCode == MeetingErrorCode.LOCAL_DEVICE_OPERATION_IN_PROGRESS ||
            errorCode == MeetingErrorCode.SDK_NOT_READY) return@runOnUiThread
        // The UI facing is updated only on success, so on failure it still keeps the original state.
        if (previousId.isBlank()) {
            showCameraLost()
            return@runOnUiThread
        }
        engine.switchCameraDevice(previousId, object : MeetingResultCallback {
            override fun onSuccess() = Unit // The original device has been restored
            override fun onFailure(errorCode: Int, message: String?) = runOnUiThread {
                if (generation == cameraUiGeneration && cameraEnabled &&
                    errorCode != MeetingErrorCode.LOCAL_DEVICE_OPERATION_CANCELLED &&
                    errorCode != MeetingErrorCode.SDK_NOT_READY) showCameraLost()
            }
        })
    }
})
```

The first failure means the switch failed; only when the recovery request also fails does it mean the video can't be restored, and your app should stop publishing, close the device, and notify the user. For a complete example, see the demo's `CameraFragment`: it ignores repeated taps during switching and recovery, and calibrates the UI facing against the real device on final success.

### switchFrontCameraMirror(open)

```kotlin
fun switchFrontCameraMirror(open: Boolean)
```

Description: Sets front camera preview mirroring. It affects only the front camera; the state is cached and restored after capture restarts.

Parameters:

| Parameter | Description |
| --- | --- |
| `open` | `true` turns mirroring on, `false` turns it off. |

Returns: None (`Unit`).

### isFrontCameraMirrorOpen()

```kotlin
fun isFrontCameraMirrorOpen(): Boolean
```

Description: Queries the front camera preview mirroring state.

Parameters: None.

Returns: `true` means mirroring is on; currently on by default.

### addPreview(view)

```kotlin
fun addPreview(view: View): Boolean
```

Description: Binds a preview view to the current local camera track.

Parameters:

| Parameter | Description |
| --- | --- |
| `view` | A local video render view supported by SRTC. |

Returns: `true` means binding succeeded; `false` means the view type is invalid or the current track is unavailable.

### removePreview(view)

```kotlin
fun removePreview(view: View?)
```

Description: Removes a local camera preview view.

Parameters:

| Parameter | Description |
| --- | --- |
| `view` | The view to remove; pass `null` to remove all preview views. |

Returns: None (`Unit`).

### replacePreview(views)

```kotlin
fun replacePreview(views: List<View>)
```

Description: Replaces the local camera preview views wholesale with a new list.

Parameters:

| Parameter | Description |
| --- | --- |
| `views` | The new list of preview views; all views must be of a type SRTC supports. |

Returns: None (`Unit`).

### getAllPreview()

```kotlin
fun getAllPreview(): List<View>
```

Description: Gets all currently bound local preview views.

Parameters: None.

Returns: A snapshot of the preview views.

## Local mic

### openMic(preOption, callback)

```kotlin
fun openMic(preOption: PreOptionMic?, callback: MeetingResultCallback)
```

Description: Only starts local mic capture, without requesting meeting permission or publishing audio; can be called before the meeting once initialization succeeds.

Parameters:

| Parameter | Description |
| --- | --- |
| `preOption` | Mic preset; pass `null` to use the SRTC default configuration. |
| `callback` | Result callback after physical capture has started stably. |

Returns: None (the asynchronous result is delivered through the callback).

### openMicAndPublish(preOption, callback)

```kotlin
fun openMicAndPublish(
    preOption: PreOptionMic?,
    callback: MeetingResultCallback
)
```

Description: Completes server-side authorization, mic capture, and SRTC publishing in the current meeting. A failure rolls back this publish and closes capture.

Parameters:

| Parameter | Description |
| --- | --- |
| `preOption` | Mic capture preset; pass `null` to use the default configuration. |
| `callback` | Result callback after authorization, capture, and publishing have all completed. |

Returns: None (the asynchronous result is delivered through the callback).

### closeMic()

```kotlin
fun closeMic()
```

Description: Unpublishes the mic in the current meeting and stops local capture; when not in a meeting, only stops local capture.

Parameters: None.

Returns: None (`Unit`).

### getMicVolume()

```kotlin
fun getMicVolume(): Int?
```

Description: Gets the real-time mic volume during capture.

Parameters: None.

Returns: The volume in dBFS; `null` when not capturing.

### getMicDevices()

```kotlin
fun getMicDevices(): List<MicDeviceCapability>
```

Description: Gets a snapshot of the mic input device capabilities SRTC currently recognizes.

Parameters: None.

Returns: The list of mic device capabilities; an empty list when there is no available device.

### switchMicDevice(deviceId)

```kotlin
fun switchMicDevice(deviceId: String)
```

Description: Switches the mic input by device ID.

Parameters:

| Parameter | Description |
| --- | --- |
| `deviceId` | Device ID returned by `getMicDevices()`. |

Returns: None (`Unit`).

## Screen sharing

### initScreenShare(activity, notificationParam, preOpt)

```kotlin
fun initScreenShare(
    activity: Activity,
    notificationParam: ScreenNotificationOption?,
    preOpt: PreOptionScreen?
)
```

Description: Creates or reuses the local screen capture object. This method only initializes capture resources; it doesn't mean a screen track has been published to the meeting.

Parameters:

| Parameter | Description |
| --- | --- |
| `activity` | The `Activity` used to start the Android MediaProjection authorization. |
| `notificationParam` | Foreground service notification configuration; pass `null` if you don't use a notification. |
| `preOpt` | Screen capture preset; pass `null` to use the SRTC default configuration. |

Returns: None (`Unit`). Capture state is delivered through `screenCaptureEvent`.

### startScreenShare(hasBar, callback)

```kotlin
fun startScreenShare(hasBar: Boolean, callback: MeetingResultCallback)
```

Description: Runs the full flow of Android authorization, the Meeting sharing request, screen capture, and SRTC track publishing. Call `initScreenShare()` first.

Parameters:

| Parameter | Description |
| --- | --- |
| `hasBar` | Whether to enable the foreground service notification. |
| `callback` | Result callback after all steps have completed. |

Returns: None (the asynchronous result is delivered through the callback).

### stopScreenShare()

```kotlin
fun stopScreenShare()
```

Description: Stops the current user's screen sharing and coordinates the share track it has in common with course recording.

Parameters: None.

Returns: None (`Unit`).

### confirmStartScreenShareAgree(targetId, hasBar, callback)

```kotlin
fun confirmStartScreenShareAgree(
    targetId: String,
    hasBar: Boolean,
    callback: MeetingResultCallback
)
```

Description: Accepts the host's screen sharing request and goes on to complete authorization, capture, and publishing.

Parameters:

| Parameter | Description |
| --- | --- |
| `targetId` | UID of the host who sent the request. |
| `hasBar` | Whether to enable the foreground service notification. |
| `callback` | Result callback after server confirmation and local sharing have all completed. |

Returns: None (the asynchronous result is delivered through the callback).

### confirmStartScreenShareRefuse(targetId, callback)

```kotlin
fun confirmStartScreenShareRefuse(
    targetId: String,
    callback: MeetingResultCallback
)
```

Description: Declines the host's screen sharing request.

Parameters:

| Parameter | Description |
| --- | --- |
| `targetId` | UID of the host who sent the request. |
| `callback` | Server confirmation result callback. |

Returns: None (the asynchronous result is delivered through the callback).

## Whiteboard sharing

### requestShareBoard(callback)

```kotlin
fun requestShareBoard(callback: MeetingValueResultCallback<String>)
```

Description: Requests to start whiteboard sharing.

Parameters:

| Parameter | Description |
| --- | --- |
| `callback` | Result callback that returns the current meeting's whiteboard URL on success. |

Returns: None (the asynchronous result is delivered through the callback).

### stopShareWhiteBoard()

```kotlin
fun stopShareWhiteBoard()
fun stopShareWhiteBoard(callback: MeetingResultCallback)
```

Description: Stops the current user's whiteboard sharing; the overload with a callback returns after the server confirms the result.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| callback | `MeetingResultCallback` | Required for the overload with a callback | Result of the whiteboard stop request |

Returns: None (`Unit`).

### confirmStartWhiteBoardShareAgree(targetId, callback)

```kotlin
fun confirmStartWhiteBoardShareAgree(
    targetId: String,
    callback: MeetingValueResultCallback<String>
)
```

Description: Accepts the host's whiteboard sharing request.

Parameters:

| Parameter | Description |
| --- | --- |
| `targetId` | UID of the host who sent the request. |
| `callback` | Result callback that returns the whiteboard URL on success. |

Returns: None (the asynchronous result is delivered through the callback).

### confirmStartWhiteBoardShareRefuse(targetId, callback)

```kotlin
fun confirmStartWhiteBoardShareRefuse(
    targetId: String,
    callback: MeetingResultCallback
)
```

Description: Declines the host's whiteboard sharing request.

Parameters:

| Parameter | Description |
| --- | --- |
| `targetId` | UID of the host who sent the request. |
| `callback` | Server confirmation result callback. |

Returns: None (the asynchronous result is delivered through the callback).

## Room messages and raising hands

### sendRoomChatMessage(targetId, msg, msgType, callback)

```kotlin
fun sendRoomChatMessage(
    targetId: String?,
    msg: String,
    msgType: ChatMsgType,
    callback: MeetingResultCallback
)
```

Description: Sends a room chat message.

Parameters:

| Parameter | Description |
| --- | --- |
| `targetId` | Target member UID; pass `null` to send to everyone. |
| `msg` | Message content. |
| `msgType` | Chat type, such as text, file, image, or voice. |
| `callback` | Message submission result callback. |

Returns: None (the asynchronous result is delivered through the callback).

### sendRoomCustomMessage(targetId, msg, callback)

```kotlin
fun sendRoomCustomMessage(
    targetId: String?,
    msg: String,
    callback: MeetingResultCallback
)
```

Description: Sends an app-defined custom message; recipients handle extension messages through `MeetingMessageEvent.onExtensionMessage()`.

Parameters:

| Parameter | Description |
| --- | --- |
| `targetId` | Target member UID; pass `null` to send to everyone. |
| `msg` | Custom message content. |
| `callback` | Message submission result callback. |

Returns: None (the asynchronous result is delivered through the callback).

### getRoomChatMsgList(page, prePage, callback)

```kotlin
fun getRoomChatMsgList(
    page: Int,
    prePage: Int,
    callback: MeetingValueResultCallback<MeetingPage<ChatMsgBean>>
)
```

Description: Queries the current meeting's chat history page by page.

Parameters:

| Parameter | Description |
| --- | --- |
| `page` | Page number, starting from `1`. |
| `prePage` | Maximum number of items per page. The parameter name is a historical spelling and means the same as `perPage`. |
| `callback` | Callback that returns the paginated chat records on success. |

Returns: None (the asynchronous result is delivered through the callback).

### requestHandUp(code, callback)

```kotlin
fun requestHandUp(code: HandUpType, callback: MeetingResultCallback)
```

Description: Sends a raise-hand request of the specified type to the host.

Parameters:

| Parameter | Description |
| --- | --- |
| `code` | Raise-hand request type. |
| `callback` | Request submission result callback. |

Returns: None (the asynchronous result is delivered through the callback).

### cancelHandUp(code)

```kotlin
fun cancelHandUp(code: HandUpType)
```

Description: Cancels the current user's raise-hand request of the specified type.

Parameters:

| Parameter | Description |
| --- | --- |
| `code` | The raise-hand type to cancel. |

Returns: None (`Unit`).

## Replying to device requests

### confirmOpenCameraAgree(targetId, view, preOpt, callback)

```kotlin
fun confirmOpenCameraAgree(
    targetId: String,
    view: View?,
    preOpt: PreOptionCamera?,
    callback: MeetingResultCallback
)
```

Description: Accepts the host's request to turn on the camera and completes local capture and publishing.

Parameters:

| Parameter | Description |
| --- | --- |
| `targetId` | UID of the host who sent the request. |
| `view` | Optional local preview view. |
| `preOpt` | Camera capture preset; pass `null` to use the default configuration. |
| `callback` | Result callback for server confirmation, capture, and publishing. |

Returns: None (the asynchronous result is delivered through the callback).

### confirmOpenCameraRefuse(targetId, callback)

```kotlin
fun confirmOpenCameraRefuse(targetId: String, callback: MeetingResultCallback)
```

Description: Declines the host's request to turn on the camera.

Parameters:

| Parameter | Description |
| --- | --- |
| `targetId` | UID of the host who sent the request. |
| `callback` | Server confirmation result callback. |

Returns: None (the asynchronous result is delivered through the callback).

### confirmOpenMicAgree(targetId, preOpt, callback)

```kotlin
fun confirmOpenMicAgree(
    targetId: String,
    preOpt: PreOptionMic?,
    callback: MeetingResultCallback
)
```

Description: Accepts the host's request to turn on the mic and completes local capture and publishing.

Parameters:

| Parameter | Description |
| --- | --- |
| `targetId` | UID of the host who sent the request. |
| `preOpt` | Mic capture preset; pass `null` to use the default configuration. |
| `callback` | Result callback for server confirmation, capture, and publishing. |

Returns: None (the asynchronous result is delivered through the callback).

### confirmOpenMicRefuse(targetId, callback)

```kotlin
fun confirmOpenMicRefuse(targetId: String, callback: MeetingResultCallback)
```

Description: Declines the host's request to turn on the mic.

Parameters:

| Parameter | Description |
| --- | --- |
| `targetId` | UID of the host who sent the request. |
| `callback` | Server confirmation result callback. |

Returns: None (the asynchronous result is delivered through the callback).

## Cloud recording and course recording

### startCloudRecord(layoutData, callback)

```kotlin
fun startCloudRecord(
    layoutData: LayoutData?,
    callback: MeetingResultCallback
)
```

Description: Starts cloud video recording for the current meeting.

Parameters:

| Parameter | Description |
| --- | --- |
| `layoutData` | Optional recording layout; pass `null` to use the server's default layout. |
| `callback` | Start request result callback. The actual task status is delivered through `MeetingRoomEvent.onCloudRecordStatusChange()`. |

Returns: None (the asynchronous result is delivered through the callback).

### stopCloudRecord(callback)

```kotlin
fun stopCloudRecord(callback: MeetingResultCallback)
```

Description: Stops cloud video recording for the current meeting.

Parameters:

| Parameter | Description |
| --- | --- |
| `callback` | Stop request result callback. |

Returns: None (the asynchronous result is delivered through the callback).

### enableCourseRecordTrack(track, callback)

```kotlin
fun enableCourseRecordTrack(
    track: LocalCustomVideoTrack,
    callback: MeetingResultCallback
)
```

Description: Publishes a custom video track provided by your app as `TRACK_SHARE`, for course recording. This method only handles the media track; your app sends the recording business request separately.

Parameters:

| Parameter | Description |
| --- | --- |
| `track` | The `LocalCustomVideoTrack` your app keeps writing the course video into. |
| `callback` | Track publish result callback. |

Returns: None (the asynchronous result is delivered through the callback).

### disableCourseRecordTrack()

```kotlin
fun disableCourseRecordTrack()
```

Description: Unpublishes the course recording sharing track; it doesn't stop the server-side recording task on your app's behalf.

Parameters: None.

Returns: None (`Unit`).

## Audio routing and remote audio

### toggleRemoteAudioMute(mute)

```kotlin
fun toggleRemoteAudioMute(mute: Boolean)
```

Description: Mutes or resumes playback of the current meeting's remote mixed audio.

Parameters:

| Parameter | Description |
| --- | --- |
| `mute` | `true` mutes, `false` resumes playback. |

Returns: None (`Unit`).

### getAudioRouterManager()

```kotlin
fun getAudioRouterManager(): AudioRouterManager?
```

Description: Gets the SRTC Engine-level audio routing manager; repeated calls within the same lifecycle return the cached instance.

Parameters: None.

Returns: `AudioRouterManager?`; `null` when the SDK isn't ready. Callers must not call its `release()` directly.

### releaseAudioRouterManager()

```kotlin
fun releaseAudioRouterManager()
```

Description: The Meeting SDK releases and clears the cached audio routing manager. Safe to call repeatedly.

Parameters: None.

Returns: None (`Unit`).

## Remote member video

### startPlayRemoteVideo(uid, trackDesc, view, event, callback)

```kotlin
fun startPlayRemoteVideo(
    uid: String,
    trackDesc: String,
    view: View? = null,
    event: MeetingRemoteVideoEvent? = null,
    callback: MeetingValueResultCallback<RemoteVideoTrack>
)
```

Description: Subscribes to the specified member's video track. After SRTC confirms success, the corresponding `RemoteVideoTrack` control object is returned.

Parameters:

| Parameter | Description |
| --- | --- |
| `uid` | Remote member UID. |
| `trackDesc` | Track description, such as the description of the high or low camera stream, or the sharing stream. |
| `view` | Optional render view; must be `VcsPlayerGlTextureView` or `VcsPlayerGlSurfaceView`. |
| `event` | Optional listener for single-track receive and stutter state. |
| `callback` | Result callback that returns `RemoteVideoTrack` on success. |

Returns: None (the asynchronous result is delivered through the callback).

### stopPlayRemoteVideo(uid, trackDesc)

```kotlin
fun stopPlayRemoteVideo(uid: String, trackDesc: String)
```

Description: Unsubscribes from the specified member's video track.

Parameters:

| Parameter | Description |
| --- | --- |
| `uid` | The remote member UID used when subscribing. |
| `trackDesc` | The track description used when subscribing. |

Returns: None (`Unit`).

### getRemoteVideoTrack(uid, trackDesc)

```kotlin
fun getRemoteVideoTrack(uid: String, trackDesc: String): RemoteVideoTrack?
```

Description: Queries the specified remote video control track cached for the current meeting.

Parameters:

| Parameter | Description |
| --- | --- |
| `uid` | Remote member UID. |
| `trackDesc` | Track description. |

Returns: The matching `RemoteVideoTrack`; `null` when not in a meeting or the control track hasn't been created. For track rendering methods, see [SRTC RemoteVideoTrack](/en/rtc/android/api-reference/RemoteVideoTrack).

## Remote composite stream

### startPlayRemoteMixture(view, event, callback)

```kotlin
fun startPlayRemoteMixture(
    view: View? = null,
    event: MeetingRemoteVideoEvent? = null,
    callback: MeetingValueResultCallback<RemoteVideoTrack>
)
```

Description: Prepares the remote composite stream control track and submits the subscription request. SRTC currently doesn't provide a subscription result listener for the composite stream, so success only means the request was submitted, not that the first frame has been received.

Parameters:

| Parameter | Description |
| --- | --- |
| `view` | Optional composite stream render view. |
| `event` | Optional composite stream receive state listener. |
| `callback` | Returns the prepared `RemoteVideoTrack` control object on success. |

Returns: None (the asynchronous result is delivered through the callback).

### stopPlayRemoteMixture()

```kotlin
fun stopPlayRemoteMixture()
```

Description: Stops subscribing to the remote composite stream.

Parameters: None.

Returns: None (`Unit`).

### getRemoteMixtureTrack()

```kotlin
fun getRemoteMixtureTrack(): RemoteVideoTrack?
```

Description: Queries the remote composite stream control track cached for the current meeting.

Parameters: None.

Returns: `RemoteVideoTrack?`; `null` when not in a meeting or not yet created.

## Wangsu generic streams

:::warning
The APIs in this group apply only to the Wangsu (WS) media streaming engine, and you must already have entered the meeting. Calling them with a non-WS engine returns an underlying "not supported" error or a null control track.
:::

### subscribeWsVideoStream(streamName, uid, trackDesc, view, event, callback)

```kotlin
fun subscribeWsVideoStream(
    streamName: String,
    uid: String = streamName,
    trackDesc: String,
    view: View? = null,
    event: MeetingRemoteVideoEvent? = null,
    callback: MeetingValueResultCallback<RemoteVideoTrack>
)
```

Description: Subscribes to one Wangsu generic video stream by its full stream name, without depending on the meeting members' track lists.

Parameters:

| Parameter | Description |
| --- | --- |
| `streamName` | Full video stream name, such as `rtc_v_lesson_fknqb`. |
| `uid` | Render routing identifier; use the default `streamName` unless you have special needs. |
| `trackDesc` | Track description that distinguishes multiple generic streams. |
| `view` | Optional video render view. |
| `event` | Optional single-track receive state listener. |
| `callback` | Result callback that returns the video control track on success. |

Returns: None (the asynchronous result is delivered through the callback).

### subscribeWsAudioStream(streamName, uid, trackDesc, callback)

```kotlin
fun subscribeWsAudioStream(
    streamName: String,
    uid: String = streamName,
    trackDesc: String,
    callback: MeetingResultCallback
)
```

Description: Subscribes to one Wangsu generic audio stream by its full stream name; after success, the SDK plays it through the speaker automatically.

Parameters:

| Parameter | Description |
| --- | --- |
| `streamName` | Full audio stream name, such as `rtc_a_lesson_fknqb`. |
| `uid` | Audio routing identifier; use the default `streamName` unless you have special needs. |
| `trackDesc` | Track description that distinguishes multiple generic streams. |
| `callback` | SRTC subscription result callback. |

Returns: None (the asynchronous result is delivered through the callback).

### unsubscribeWsVideoStream(streamName, uid, trackDesc)

```kotlin
fun unsubscribeWsVideoStream(
    streamName: String,
    uid: String = streamName,
    trackDesc: String
)
```

Description: Unsubscribes from a Wangsu generic video stream. Control tracks are reclaimed together when you exit the meeting.

Parameters:

| Parameter | Description |
| --- | --- |
| `streamName` | The full stream name used when subscribing. |
| `uid` | The routing identifier used when subscribing. |
| `trackDesc` | The track description used when subscribing. |

Returns: None (`Unit`).

### unsubscribeWsAudioStream(streamName, uid, trackDesc)

```kotlin
fun unsubscribeWsAudioStream(
    streamName: String,
    uid: String = streamName,
    trackDesc: String
)
```

Description: Unsubscribes from a Wangsu generic audio stream.

Parameters:

| Parameter | Description |
| --- | --- |
| `streamName` | The full stream name used when subscribing. |
| `uid` | The routing identifier used when subscribing. |
| `trackDesc` | The track description used when subscribing. |

Returns: None (`Unit`).

### getWsVideoStreamTrack(uid, trackDesc)

```kotlin
fun getWsVideoStreamTrack(uid: String, trackDesc: String): RemoteVideoTrack?
```

Description: Gets or creates a Wangsu generic video stream control track; you can bind the render view before subscribing.

Parameters:

| Parameter | Description |
| --- | --- |
| `uid` | Video routing identifier. |
| `trackDesc` | Track description. |

Returns: `RemoteVideoTrack?`; `null` for audio streams, non-WS engines, or when not in a meeting.


## Cast codes

### registerCastCode(meetingId, callback)

```kotlin
fun registerCastCode(meetingId: String?, callback: MeetingValueResultCallback<CastCodeInfo>)
```

Registers or renews the current device's cast code and syncs the large screen's current meeting. Repeated calls from the same device return the same valid code and refresh its validity; call it immediately after entering or exiting a meeting, and renew it periodically while online as agreed with the server.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| meetingId | `String?` | Yes | Current meeting ID; pass null or an empty string when not in a meeting |
| callback | `MeetingValueResultCallback<CastCodeInfo>` | Yes | Returns the cast code and its remaining validity in seconds |

Returns: `Unit`; the business result is returned through the callback.

### unregisterCastCode(callback)

```kotlin
fun unregisterCastCode(callback: MeetingResultCallback)
```

Unregisters the current device's cast code, usually called before logging out or shutting down the device.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| callback | `MeetingResultCallback` | Yes | Unregistration result |

Returns: `Unit`; the result is returned through the callback.

### startCast(code, option, callback)

```kotlin
fun startCast(code: String, option: CastStartOption, callback: MeetingValueResultCallback<CastStartInfo>)
```

Consumes a cast code and gets the target meeting. The server consumes the cast code atomically, so it must not be reused even if entering the meeting fails afterward; your app enters the meeting based on the result and, when `canShare` is true, goes on to request sharing. When the large screen is already in a meeting, the server ignores the roles and ownership in option.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| code | `String` | Yes | Six-character uppercase cast code |
| option | `CastStartOption` | Yes | Roles and ownership of both parties when a new cast meeting is created; you can pass a default instance |
| callback | `MeetingValueResultCallback<CastStartInfo>` | Yes | Target meeting and sharing permission |

Returns: `Unit`; the business result is returned through the callback. For the related models, see the model types page; for ownership values, see the enums page.

## Virtual background

Supported since `2.0.39`. First initialize the SDK and install the person segmentation model, then set blur or a background image, and finally turn the effect on. After camera capture or a switch succeeds, or after a successful reconnection, the meeting layer reapplies the cached configuration; `release()` clears the cache and releases the underlying resources.

### installVirtualBackground(modelData)

```kotlin
fun installVirtualBackground(modelData: ByteArray): Int
```

Installs the virtual background module; no license key is required.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| modelData | `ByteArray` | Yes | Contents of the selfie_segmenter ONNX model read by your app; the meeting layer holds the array reference directly without copying it |

Returns: `0` on success; `MeetingErrorCode.SDK_NOT_READY` when the SDK isn't ready; other errors pass through RTC's `102xxx` error codes. Check the result before turning the effect on.

### uninstallVirtualBackground()

```kotlin
fun uninstallVirtualBackground()
```

Uninstalls the model and GPU resources, and clears the model, background image, mode, and on/off state cached by the meeting layer; nothing is reinstalled automatically afterward. No parameters; returns `Unit`.

### enabledVirtualBackground(enabled)

```kotlin
fun enabledVirtualBackground(enabled: Boolean): Int
```

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| enabled | `Boolean` | Yes | true turns it on; false turns it off and passes the original captured video through |

Returns: `0` on success; `MeetingErrorCode.SDK_NOT_READY` when the SDK isn't ready; other errors pass through the RTC return value. Turning the effect off doesn't uninstall the model.

### setVirtualBackgroundBlur(level)

```kotlin
fun setVirtualBackgroundBlur(level: Int)
```

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| level | `Int` | Yes | Blur strength 1–10, default 5; out-of-range values are clamped to the bounds |

Returns: `Unit`. Mutually exclusive with background image mode; whichever mode is set last takes effect. Setting the strength doesn't turn on the main switch automatically.

### setVirtualBackgroundImage(image)

```kotlin
fun setVirtualBackgroundImage(image: Bitmap?)
```

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| image | `android.graphics.Bitmap?` | Yes | Background image, cropped to cover without stretching; null cancels the image replacement and returns to passthrough |

Returns: `Unit`. Mutually exclusive with blur mode; whichever mode is set last takes effect. Your app must first decode the image URI or file into a Bitmap; the meeting layer caches this object for configuration replay, so don't recycle it while it's in use. Setting the image doesn't turn on the main switch automatically.

### setVirtualBackgroundInferenceInterval(interval)

```kotlin
fun setVirtualBackgroundInferenceInterval(interval: Int)
```

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| interval | `Int` | Yes | Run segmentation once every N frames, default 1; values less than 1 are treated as 1 |

Returns: `Unit`. For your app to configure according to device performance; we don't recommend exposing it directly to end users.

### setVirtualBackgroundMaskSync(on)

```kotlin
fun setVirtualBackgroundMaskSync(on: Boolean)
```

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| on | `Boolean` | Yes | Whether to enable mask alignment, default false |

Returns: `Unit`. Makes a difference only when the inference interval is greater than 1; it reduces mask misalignment trailing during fast motion.

### isVirtualBackgroundEnabled()

```kotlin
fun isVirtualBackgroundEnabled(): Boolean
```

No parameters. Returns: The RTC's current virtual background on/off state; falls back to the value cached by the meeting layer when RTC hasn't been created yet. This state doesn't mean model inference or the video effect has been verified to work.
