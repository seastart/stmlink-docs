---
title: "Model types"
description: "Configuration, result, meeting, member, roll call, sign-in, IM, recording layout, and casting models used directly by the public APIs of SMeeting Android, with every field. Read this when you build options or read results, events, and snapshots."
---

This page lists only the Meeting models directly exposed by `MeetingEngine`, the public managers, events, and result callbacks. `TrackInfo`, `RemoteVideoTrack`, device capabilities, media statistics, and similar types come from the transitive SRTC dependency; see [SRTC Android model types](/en/rtc/android/types).

## Configuration models

### CreateImmediateMeetingOption

Optional parameters for creating an instant meeting. All fields default to `null`; the server applies its default rules to unset items.

| Property | Type | Description |
| --- | --- | --- |
| `roomNo` | `String?` | Custom room number |
| `content` | `String?` | Meeting description |
| `attendType` | `AttendType?` | Entry method |
| `conferees` | `MutableList<String>?` | Invitee UID list |
| `password` | `String?` | Meeting password |
| `mode` | `MeetingMode?` | Meeting mode |
| `planTime` | `Long?` | Optional planned start time, Unix timestamp in seconds |
| `planDur` | `Int?` | Optional planned duration in minutes |
| `autoRecord` | `Boolean?` | Whether to record automatically |
| `entryMutePolicy` | `MuteState?` | Mute-on-entry policy |
| `watermarkDisabled` | `Boolean?` | Whether the watermark is disabled |
| `screenshotDisabled` | `Boolean?` | Whether screenshots are disabled |
| `chatDisabled` | `Boolean?` | Whether chat is disabled |
| `waitingRoomDisabled` | `Boolean?` | Whether the waiting room is disabled |
| `enterBeforeHostDisabled` | `Boolean?` | Whether entering before the host is prohibited |
| `extendInfo` | `String?` | App-defined extension string |

### CreateScheduleMeetingOption

Optional parameters for creating a scheduled meeting. `planTime` and `planDur` are passed as separate parameters of `createScheduleMeeting()`, so this type doesn't define them again.

| Property | Type | Description |
| --- | --- | --- |
| `roomNo` | `String?` | Custom room number |
| `content` | `String?` | Meeting description |
| `attendType` | `AttendType?` | Entry method |
| `conferees` | `MutableList<String>?` | Invitee UID list |
| `password` | `String?` | Meeting password |
| `mode` | `MeetingMode?` | Meeting mode |
| `autoRecord` | `Boolean?` | Whether to record automatically |
| `entryMutePolicy` | `MuteState?` | Mute-on-entry policy |
| `watermarkDisabled` | `Boolean?` | Whether the watermark is disabled |
| `screenshotDisabled` | `Boolean?` | Whether screenshots are disabled |
| `chatDisabled` | `Boolean?` | Whether chat is disabled |
| `waitingRoomDisabled` | `Boolean?` | Whether the waiting room is disabled |
| `enterBeforeHostDisabled` | `Boolean?` | Whether entering before the host is prohibited |
| `extendInfo` | `String?` | App-defined extension string |

### UpdateMeetingOption

Optional fields for updating a meeting before it starts. Fields left as `null` aren't updated.

| Property | Type | Description |
| --- | --- | --- |
| `title` | `String?` | New meeting title |
| `content` | `String?` | New meeting description |
| `attendType` | `AttendType?` | Entry method |
| `conferees` | `MutableList<String>?` | Invitee UID list |
| `password` | `String?` | Meeting password |
| `mode` | `MeetingMode?` | Meeting mode |
| `planTime` | `Long?` | Planned start time, Unix timestamp in seconds |
| `planDur` | `Int?` | Planned duration in minutes |
| `autoRecord` | `Boolean?` | Whether to record automatically |
| `entryMutePolicy` | `MuteState?` | Mute-on-entry policy |
| `watermarkDisabled` | `Boolean?` | Whether the watermark is disabled |
| `screenshotDisabled` | `Boolean?` | Whether screenshots are disabled |
| `chatDisabled` | `Boolean?` | Whether chat is disabled |
| `waitingRoomDisabled` | `Boolean?` | Whether the waiting room is disabled |
| `enterBeforeHostDisabled` | `Boolean?` | Whether entering before the host is prohibited |
| `extendInfo` | `String?` | App-defined extension string |

### ScreenNotificationOption

Notification configuration for the Android screen capture foreground service.

| Property | Type | Description |
| --- | --- | --- |
| `smallIcon` | `Int` | Resource ID of the small notification icon |
| `title` | `String?` | Notification title |
| `desc` | `String?` | Notification description |
| `buttonText` | `String?` | Text of the notification action button |

## Common results

### MeetingPage&lt;T&gt;

Stable pagination result used by public APIs; the server's `_meta` wrapper isn't exposed.

| Property | Type | Description |
| --- | --- | --- |
| `items` | `List<T>` | Business data on the current page |
| `totalCount` | `Int` | Total number of items |
| `pageCount` | `Int` | Total number of pages |
| `currentPage` | `Int` | Current page number, starting from 1 |
| `perPage` | `Int` | Maximum number of items per page |

### MeetingDownload

One-shot data stream returned after a file download succeeds; implements `Closeable`.

| Property / method | Type | Description |
| --- | --- | --- |
| `fileName` | `String?` | Server file name; `null` when the response doesn't carry one |
| `inputStream` | `InputStream` | One-shot data stream bound to the current response |
| `close()` | `Unit` | Closes the data stream and the underlying network response; can be called repeatedly |

```kotlin
download.use { result ->
    result.inputStream.copyTo(outputStream)
}
```

### MeetingEnterInfo

Meeting identity information returned after successfully entering the meeting. It only represents the result and is not a session control object.

| Property | Type | Description |
| --- | --- | --- |
| `meetingId` | `String` | ID of the meeting you entered |
| `uid` | `String` | The current user's UID in the meeting |

### MeetingImConnection

Connection identifiers after the IM connection is established.

| Property | Type | Description |
| --- | --- | --- |
| `uid` | `String` | The current user's IM UID |
| `sid` | `String` | Current IM session identifier |

## Current meeting state

### MeetingInfo

Snapshot of the current room, converted from the SRTC channel properties.

| Property | Type | Description |
| --- | --- | --- |
| `id` | `String` | Meeting ID |
| `roomNo` | `String` | Room number |
| `title` | `String` | Meeting title |
| `content` | `String?` | Meeting description |
| `meetingType` | `MeetingType` | Instant or scheduled meeting |
| `meetingMode` | `MeetingMode` | Meeting mode |
| `planTime` | `Long` | Planned start time, Unix timestamp in seconds |
| `planDur` | `Long` | Planned duration in minutes |
| `entryMutePolicy` | `MuteState` | Mute-on-entry policy |
| `watermarkDisabled` | `Boolean` | Whether the watermark is disabled |
| `screenshotDisabled` | `Boolean` | Whether screenshots are disabled |
| `chatDisabled` | `Boolean` | Whether chat is disabled |
| `micDisabled` | `Boolean` | Whether mute all is on |
| `cameraDisabled` | `Boolean` | Whether camera off for everyone is on |
| `selfUnmuteMicDisabled` | `Boolean` | Whether members are prevented from unmuting themselves |
| `selfUnmuteCameraDisabled` | `Boolean` | Whether members are prevented from turning their cameras back on themselves |
| `shareDisabled` | `Boolean` | Whether sharing is prohibited |
| `locked` | `Boolean` | Whether the room is locked |
| `waitingRoomDisabled` | `Boolean` | Whether the waiting room is disabled |
| `enterBeforeHostDisabled` | `Boolean` | Whether entering before the host is prohibited |
| `shareState` | `ShareType` | Current sharing type |
| `recordStatus` | `CloudRecordStatus` | Current cloud recording status |
| `parent` | `String` | Main meeting ID; usually an empty string for the main meeting |
| `shareUid` | `String?` | UID of the current sharer |
| `creator` | `String` | Creator UID |
| `hostUid` | `String` | Host UID |
| `coHosts` | `MutableList<String>` | Co-host UID list |
| `extendInfo` | `JsonElement?` | Parsed business extension JSON |

### MemberInfo

Snapshot of a member in the current meeting.

| Property | Type | Description |
| --- | --- | --- |
| `uid` | `String?` | Member UID |
| `name` | `String?` | In-meeting display name |
| `deviceType` | `DeviceType` | SRTC device type |
| `deviceId` | `String?` | Unique device identifier |
| `version` | `String?` | SDK version of the remote side |
| `joinAt` | `Long` | Time of entering the meeting |
| `role` | `MemberRoleType` | In-meeting role |
| `avatar` | `String?` | Avatar |
| `micState` | `DeviceState` | Mic state |
| `cameraState` | `DeviceState` | Camera state |
| `shareState` | `ShareType` | Sharing state |
| `drawDisabled` | `Boolean` | Whether whiteboard drawing is prohibited |
| `chatDisabled` | `Boolean` | Whether chat is prohibited |
| `extendInfo` | `JsonElement?` | Parsed business extension JSON |

### McuAlarm

| Property | Type | Description |
| --- | --- | --- |
| `taskId` | `String` | MCU task ID |
| `taskStatus` | `McuAlarmStatus` | MCU task status |
| `gw` | `String` | Gateway where the alarm occurred |
| `alarmAt` | `Long` | Alarm timestamp |
| `alarmBrief` | `String` | Alarm summary |

## Pre-meeting models

### UserBean

| Property | Type | Description |
| --- | --- | --- |
| `deviceId` | `String` | Unique ID of the current device |
| `deviceType` | `DeviceType` | SRTC device type |
| `expAt` | `Long` | User authorization expiration time |
| `uid` | `String` | Meeting user ID |

### MeetingCreatedBean

| Property | Type | Description |
| --- | --- | --- |
| `meetingId` | `String` | ID of the newly created meeting |
| `roomNo` | `String` | Room number of the newly created meeting |

### MeetInfo

Meeting list item. For the Java type, read properties through getters.

| Property | Type | Description |
| --- | --- | --- |
| `id` | `String` | Meeting ID |
| `title` | `String` | Meeting title |
| `roomNo` | `String` | Room number |
| `attendType` | `AttendType` | Entry method |
| `meetingStatus` | `MeetingStatus` | Meeting status |
| `meetingType` | `MeetingType` | Meeting type |
| `planTime` | `Long` | Planned start time, Unix timestamp in seconds |
| `planDur` | `Int` | Planned duration in minutes |
| `beginTime` | `Long` | Actual start time, Unix timestamp in seconds |
| `endTime` | `Long` | Actual end time, Unix timestamp in seconds |
| `creator` | `String` | Creator UID |
| `conferee` | `ArrayList<String>` | Invitee UID list |
| `createdAt` | `Long` | Creation time, Unix timestamp in seconds |

### MeetDetail

| Property | Type | Description |
| --- | --- | --- |
| `id` | `String` | Meeting ID |
| `roomNo` | `String` | Room number |
| `title` | `String` | Meeting title |
| `content` | `String` | Meeting description |
| `creator` | `String` | Creator UID |
| `attendType` | `AttendType` | Entry method |
| `password` | `String` | Meeting password |
| `meetingStatus` | `MeetingStatus` | Meeting status |
| `meetingType` | `MeetingType` | Meeting type |
| `meetingMode` | `MeetingMode` | Meeting mode |
| `autoRecord` | `Boolean?` | Whether to record automatically |
| `planTime` | `Long?` | Planned start time, Unix timestamp in seconds |
| `planDur` | `Int?` | Planned duration in minutes |
| `beginTime` | `Long?` | Actual start time, Unix timestamp in seconds |
| `endTime` | `Long?` | Actual end time, Unix timestamp in seconds |
| `onlineNum` | `Int?` | Number of people online |
| `entryMutePolicy` | `MuteState` | Mute-on-entry policy |
| `watermarkDisabled` | `Boolean?` | Whether the watermark is disabled |
| `screenshotDisabled` | `Boolean?` | Whether screenshots are disabled |
| `chatDisabled` | `Boolean?` | Whether chat is disabled |
| `locked` | `Boolean?` | Whether the meeting is locked |
| `shareState` | `Int?` | Raw sharing state value |
| `micDisabled` | `Boolean?` | Whether mute all is on |
| `cameraDisabled` | `Boolean?` | Whether camera off for everyone is on |
| `selfUnmuteMicDisabled` | `Boolean?` | Whether members are prevented from unmuting themselves |
| `selfUnmuteCameraDisabled` | `Boolean?` | Whether members are prevented from turning their cameras back on themselves |
| `waitingRoomDisabled` | `Boolean?` | Whether the waiting room is disabled |
| `enterBeforeHostDisabled` | `Boolean?` | Whether entering before the host is prohibited |
| `conferee` | `List<String>` | Invitee UID list |
| `extendInfo` | `String?` | Custom meeting extension info, that is, the `extend_info` passed when the meeting was created or updated, as a JSON string. Empty if not set. Available since `2.0.47` |

## Device and invitation models

### AgentRequestBean

| Property | Type | Description |
| --- | --- | --- |
| `type` | `AgentType` | External device type |
| `contact` | `String` | Device contact identifier or stream pull URL |

### AgentBean

| Property | Type | Description |
| --- | --- | --- |
| `id` | `String` | Device ID |
| `name` | `String` | Device name |
| `type` | `AgentType` | Device type |
| `status` | `AgentStatus` | Online status |
| `contact` | `String` | Device contact identifier |
| `remark` | `String?` | Remarks |
| `connParams` | `AgentBean.ConnParams?` | Connection parameters |

### AgentBean.ConnParams

| Property | Type | Description |
| --- | --- | --- |
| `subjects` | `MutableMap<String, String>?` | Channel or subject mapping |

## Members, waiting room, and sub-meetings

### MemberBean

| Property | Type | Description |
| --- | --- | --- |
| `uid` | `String` | User UID |
| `nickname` | `String` | User nickname |
| `deviceType` | `Int?` | Raw device type value |
| `joinAt` | `Long?` | Time of entering the meeting |

### MemberRequestBean

| Property | Type | Description |
| --- | --- | --- |
| `uid` | `String` | User UID |
| `name` | `String` | User nickname |

### WaitingRoomUserBean

| Property | Type | Description |
| --- | --- | --- |
| `uid` | `String` | UID of the user in the waiting room |
| `nickName` | `String` | User nickname |
| `at` | `Long` | Timestamp of entering the waiting room |

### SubMeetingBean

| Property | Type | Description |
| --- | --- | --- |
| `id` | `String` | Sub-meeting record ID |
| `mainMeetingId` | `String` | Main meeting ID |
| `meetingId` | `String` | Sub-meeting ID |
| `status` | `SubMeetingStatus` | Sub-meeting status |
| `title` | `String` | Sub-meeting title |
| `users` | `MutableList<MemberBean>?` | Assigned member list |

## Roll call models

### RollCallBean

| Property | Type | Description |
| --- | --- | --- |
| `id` | `String` | Roll call activity ID |
| `title` | `String` | Roll call title |
| `method` | `Int` | `1` automatic, `2` manual |
| `meetingTitle` | `String` | Meeting title |
| `total` | `Int` | Number of people in the roll call |
| `status` | `Int` | `1` in progress, `2` ended |
| `createdAt` | `Long` | Creation time, Unix timestamp in seconds |

### RollCallDetailBean

| Property | Type | Description |
| --- | --- | --- |
| `id` | `String` | Roll call activity ID |
| `title` | `String` | Roll call title |
| `method` | `Int` | `1` automatic, `2` manual |
| `meetingTitle` | `String` | Meeting title |
| `total` | `Int` | Number of people in the roll call |
| `status` | `Int` | `1` in progress, `2` ended |
| `users` | `List<RollCallUserBean>?` | Roll call members and their response status |
| `createdAt` | `Long` | Creation time, Unix timestamp in seconds |

### RollCallUserBean

| Property | Type | Description |
| --- | --- | --- |
| `id` | `String` | Roll call user record ID; the call and answer APIs use this value |
| `userId` | `String` | Meeting user UID |
| `userName` | `String` | User nickname |
| `rollCallAt` | `Long` | Call time; `0` means not called yet |
| `answerAt` | `Long` | Answer time; `0` means not answered yet |
| `status` | `Int` | `0` not called, `1` called but not answered, `2` answered |

## Sign-in models

### SignInActivityBean

| Property | Type | Description |
| --- | --- | --- |
| `uid` | `String` | Initiator UID |
| `beginAt` | `Long` | Start time, Unix timestamp in seconds |
| `dur` | `Int` | Duration in minutes; `0` means no time limit |
| `endAt` | `Long` | End time; `0` when there is no time limit and the activity hasn't ended |
| `desc` | `String` | Activity description |
| `nums` | `Int` | Number of people signed in; may be `0` before the activity ends |

### SignInListBean

| Property | Type | Description |
| --- | --- | --- |
| `list` | `List<SignInActivityBean>?` | Sign-in activity list |
| `now` | `Long` | Current server time |

### SignInCountBean

| Property | Type | Description |
| --- | --- | --- |
| `nums` | `Int` | Actual number of people signed in |

### SignInRecordBean

| Property | Type | Description |
| --- | --- | --- |
| `id` | `String` | Sign-in record ID |
| `userId` | `String` | User UID |
| `nickname` | `String` | In-meeting display name |
| `role` | `Int` | Raw in-meeting role value |
| `epoch` | `Int` | Sign-in round, starting from `0` |
| `createdAt` | `String` | Sign-in time string |

## Message and IM models

### ChatMsgBean

| Property | Type | Description |
| --- | --- | --- |
| `id` | `String` | Message ID |
| `meetingId` | `String` | Meeting ID |
| `senderId` | `String` | Sender UID |
| `senderName` | `String` | Sender nickname |
| `msgType` | `Int?` | Raw message type value |
| `msg` | `String` | Message content |
| `createdAt` | `Int?` | Creation time in milliseconds |

### ImContent.CallingMsg

| Property | Type | Description |
| --- | --- | --- |
| `roomNo` | `String` | Room number |
| `meetingId` | `String` | Meeting ID |
| `title` | `String` | Meeting title |
| `forceJoin` | `Boolean` | Defaults to false; true means the server requires the large screen to enter the specified meeting without manual confirmation |

### ImContent.MeetingRemind

| Property | Type | Description |
| --- | --- | --- |
| `meetingId` | `String` | Meeting ID |
| `title` | `String` | Meeting title |
| `roomNo` | `String` | Room number |
| `creatorUid` | `String` | Creator UID |
| `creatorName` | `String` | Creator nickname |
| `planTime` | `Long` | Planned start time |
| `planDur` | `Int` | Planned duration in minutes |

### ImContent.MoveOutWaitingRoom

| Property | Type | Description |
| --- | --- | --- |
| `meetingId` | `String` | Target meeting ID |
| `title` | `String` | Target meeting title |

### ImContent.UserHelpSubMeeting

| Property | Type | Description |
| --- | --- | --- |
| `parent` | `String` | Main meeting ID |
| `meetingId` | `String` | Sub-meeting ID |
| `title` | `String` | Sub-meeting title |

## Cloud recording layout

### LayoutData

| Property | Type | Description |
| --- | --- | --- |
| `layout` | `String` | Layout type; defaults to `auto` |
| `pollingDur` | `Int` | Rotation duration in seconds |
| `watermark` | `LayoutData.Watermark?` | Watermark configuration |
| `tag` | `LayoutData.Tag?` | Default label configuration |
| `divList` | `List<LayoutData.Div>?` | List of logical blocks |

### LayoutData.Watermark

| Property | Type | Description |
| --- | --- | --- |
| `type` | `Int` | `0` default, `1` none, `2` single row, `3` multiple rows |
| `text` | `String` | Specified content; an empty string means the meeting title is used automatically |
| `size` | `Int` | Font size; `0` uses the default |
| `color` | `String` | Font color; an empty string uses the default |
| `olColor` | `String` | Outline color; an empty string uses the default |
| `olWidth` | `Int` | Outline width; `0` uses the default |

### LayoutData.Tag

| Property | Type | Description |
| --- | --- | --- |
| `type` | `String` | Label position, using `L` / `R` / `T` / `B` or a combination |
| `text` | `String` | Specified content; an empty string means the in-meeting display name is used automatically |
| `size` | `Int` | Font size; `0` uses the default |
| `color` | `String` | Font color |
| `bgColor` | `String` | Background color |

### LayoutData.Div

| Property | Type | Description |
| --- | --- | --- |
| `cell` | `List<LayoutData.Cell>` | List of grid cells |
| `uids` | `List<String>` | List of bound user UIDs |

### LayoutData.Cell

| Property | Type | Description |
| --- | --- | --- |
| `idx` | `Int` | Cell index |
| `bindShare` | `Boolean` | Whether to prefer binding the shared stream in the meeting |
| `tag` | `LayoutData.Tag` | Label configuration |


## Casting models

### CastCodeInfo

| Property | Type | Default | Description |
| --- | --- | --- | --- |
| code | `String` | `""` | Current six-digit cast code; empty in the unregister response |
| expireIn | `Int` | `0` | Remaining validity in seconds |

### CastStartInfo

| Property | Type | Default | Description |
| --- | --- | --- | --- |
| meetingId | `String` | `""` | Unique identifier of the target meeting |
| roomNo | `String` | `""` | Room number of the target meeting |
| canShare | `Boolean` | `false` | Whether this casting device is allowed to continue sharing |

### CastStartOption

Used when creating a new casting meeting; all fields are ignored by the server when the large screen is already in a meeting. null uses the server defaults.

| Property | Type | Default | Description |
| --- | --- | --- | --- |
| selfRole | `MemberRoleType?` | `null` | Role of the casting initiator |
| screenRole | `MemberRoleType?` | `null` | Role of the large screen that registered the cast code |
| owner | `CastMeetingOwner?` | `null` | Ownership policy for the new meeting |

## Presigned resource models

### PresignedPutObjectInfo

Success result of [`presignedPutObject`](/en/meeting/android/api-reference/MeetingEngine#presignedputobject-type-meetingid-ext-callback), available since `2.0.46`.

| Property | Type | Default | Description |
| --- | --- | --- | --- |
| url | `String` | `""` | Presigned upload URL; valid for a limited time and only for this PUT. Don't pass or persist it |
| key | `String` | `""` | Resource key; pass it to others after the upload succeeds, and use it with `presignedGetObject` to get a download URL |
| ext | `String` | `""` | File extension confirmed by the server, without the dot |

## Network check models

Available since `2.0.45`, used by the [pre-call network check](/en/meeting/android/api-reference/MeetingEngine#pre-call-network-check). Fields and values match the [SRTC Android network check types](/en/rtc/android/types#networkcheckoptions), but these are the meeting layer's own types.

### NetworkCheckOption

Full class name: `cn.seastart.meeting.options.NetworkCheckOption`. All fields are optional; after `initSdk`, just pass the default instance. Before initialization, provide the server information in one of two ways: `appId` + `serverUrl`, or a `token` from which both can be extracted. Precedence: explicit fields > `token` > the Meeting token from initialization. The check itself doesn't use the token for authentication.

| Property | Type | Default | Description |
| --- | --- | --- | --- |
| appId | `String?` | `null` | App ID |
| serverUrl | `String?` | `null` | Server API prefix; either RTC's `client_api` (such as `https://host/client/`) or Meeting's `client_api` (such as `https://host/meeting/client`) works |
| token | `String?` | `null` | Meeting token or RTC token, used only to extract `appId` and `serverUrl` |
| timeoutMs | `Int` | `3000` | Per-item timeout in milliseconds; values of 0 or less use the default |

### NetworkCheckItem

Full class name: `cn.seastart.meeting.info.NetworkCheckItem`. Result of a single check item.

| Property | Type | Description |
| --- | --- | --- |
| id | `String` | Check item; see `NetworkCheckItemId` |
| status | `String` | Check status: `pass` / `warning` / `fail` / `skipped` / `unsupported`; see `NetworkCheckStatus` |
| reason | `String` | Machine-readable reason code, empty for `pass`; see `NetworkCheckReason` |
| message | `String` | Chinese description that can be shown to users directly |
| costMs | `Long` | Time spent on this item, in milliseconds |
| data | `Map<String, Any?>` | Measured values for this item, such as `netType` for `connectivity` and `maxSize` for `mtu`; `server` contains four sub-checks, `api`, `signal`, `media`, and `meeting_api`, each with `ok`, `status`, `reason`, and `rttMs` |

### NetworkCheckResult

Full class name: `cn.seastart.meeting.info.NetworkCheckResult`. Overall check result.

| Property | Type | Description |
| --- | --- | --- |
| status | `String` | Overall status: `fail` if any item fails; otherwise `warning` if any item warns; otherwise `ok` |
| items | `List<NetworkCheckItem>` | Always 5 items, in the order `permission`, `connectivity`, `mtu`, `dns`, `server` |
| costMs | `Long` | Total time, in milliseconds |

### Network check constants

All in the `cn.seastart.meeting.enumerate` package.

`NetworkCheckItemId` (check items):

| Constant | Value | Description |
| --- | --- | --- |
| `PERMISSION` | `permission` | Network permission |
| `CONNECTIVITY` | `connectivity` | Network connection |
| `MTU` | `mtu` | Maximum transmission unit |
| `DNS` | `dns` | DNS resolution |
| `SERVER` | `server` | Server connectivity (API / signaling / media / meeting service) |

`NetworkCheckStatus` (check status):

| Constant | Value | Description |
| --- | --- | --- |
| `OK` | `ok` | Overall: everything is normal |
| `PASS` | `pass` | Item: passed |
| `WARNING` | `warning` | At risk but usable |
| `FAIL` | `fail` | Failed |
| `SKIPPED` | `skipped` | Item: no check needed |
| `UNSUPPORTED` | `unsupported` | Item: not supported on the current device |

`NetworkCheckReason` (reason codes):

| Constant | Value | Description |
| --- | --- | --- |
| `NO_PERMISSION` | `no_permission` | Network permission not granted |
| `CELLULAR_RESTRICTED` | `cellular_restricted` | The system restricts background or cellular data |
| `OFFLINE` | `offline` | No network connection |
| `MTU_TOO_SMALL` | `mtu_too_small` | 1200-byte probe packets don't get through, but the media server is reachable |
| `UDP_BLOCKED` | `udp_blocked` | Media UDP is blocked |
| `DNS_FAILED` | `dns_failed` | DNS resolution failed |
| `API_UNREACHABLE` | `api_unreachable` | The check information API is unreachable (including when the server doesn't support the pre-call network check) |
| `SERVER_INFO_UNAVAILABLE` | `server_info_unavailable` | Server check information is unavailable; checks that depend on it are `skipped` |
| `SIGNAL_UNREACHABLE` | `signal_unreachable` | The signaling server is unreachable |
| `VENDOR_NOT_SUPPORTED` | `vendor_not_supported` | Media checks aren't needed for the current streaming engine |
| `MEDIA_UNAVAILABLE` | `media_unavailable` | The server has no available media node |
| `DF_NOT_SUPPORTED` | `df_not_supported` | The system doesn't allow setting Don't Fragment, so the MTU check isn't available |
| `MEETING_API_UNREACHABLE` | `meeting_api_unreachable` | The meeting service is unreachable |
