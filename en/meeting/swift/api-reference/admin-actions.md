---
title: "Meeting management"
description: "SMeeting Swift SDK management API reference: room controls, member management, invitees and devices, waiting room, sub-meetings, layout and recording, resources, and sign-in, plus the shared login / in-meeting preconditions and error rules. Read when implementing host controls."
---

The APIs on this page are all on `SMeetingEngine`.

---

### Error conventions

The APIs on this page follow two shared rules for throwing errors, which aren't repeated for each API below:

| Precondition | Thrown when not met |
| --- | --- |
| Requires being logged in | `SMeetingError.notLoggedIn` |
| Requires being in a meeting | `SMeetingError.notInMeeting` |

When the server rejects a request, the SDK always throws `SMeetingError.apiError(code:message:)`, where `code` and `message` come from the server. APIs with the `admin` prefix require the host (`.host`) or co-host (`.coHost`) role; regular members who call them get a permission error in the form of `apiError`.

APIs that return a value throw a decoding error when the data returned by the server can't be parsed.

---

### Room controls

The following APIs all require **being in a meeting**, and none of them return a value.

#### `adminDestroyRoom()`

Ends the entire meeting; all members are disconnected.

#### `adminUpdateRoomMicState(selfUnmuteMicDisabled:micDisabled:)`

Sets mute all for the room.

| Parameter | Type | Required | Description |
| --- | --- | :---: | --- |
| `selfUnmuteMicDisabled` | `Bool` | Yes | Whether to prevent members from unmuting themselves |
| `micDisabled` | `Bool?` | No | Whether to mute all; omit it to leave this setting unchanged |

#### `adminUpdateRoomCameraState(selfUnmuteCameraDisabled:cameraDisabled:)`

Sets camera off for everyone for the room.

| Parameter | Type | Required | Description |
| --- | --- | :---: | --- |
| `selfUnmuteCameraDisabled` | `Bool` | Yes | Whether to prevent members from turning their cameras back on themselves |
| `cameraDisabled` | `Bool?` | No | Whether to turn on camera off for everyone; omit it to leave this setting unchanged |

#### `adminUpdateRoomShareState(shareDisabled:)`

| Parameter | Type | Required | Description |
| --- | --- | :---: | --- |
| `shareDisabled` | `Bool` | Yes | Whether to prevent members from sharing |

#### `adminUpdateRoomChatDisabled(_:)`

| Parameter | Type | Required | Description |
| --- | --- | :---: | --- |
| `chatDisabled` | `Bool` | Yes | Whether to disable chat for everyone |

#### `adminUpdateRoomScreenshotDisabled(_:)`

| Parameter | Type | Required | Description |
| --- | --- | :---: | --- |
| `screenshotDisabled` | `Bool` | Yes | Whether to prevent screenshots |

#### `adminUpdateRoomWatermarkDisabled(_:)`

| Parameter | Type | Required | Description |
| --- | --- | :---: | --- |
| `watermarkDisabled` | `Bool` | Yes | Whether to turn off the watermark |

#### `adminUpdateRoomLocked(_:)`

| Parameter | Type | Required | Description |
| --- | --- | :---: | --- |
| `locked` | `Bool` | Yes | Whether to lock the meeting (once locked, new members can't enter) |

#### `adminUpdateEnterBeforeHostDisabled(_:)`

| Parameter | Type | Required | Description |
| --- | --- | :---: | --- |
| `disabled` | `Bool` | Yes | Whether to prevent entering the meeting before the host arrives |

#### `adminStopRoomShare()`

Forcibly ends the sharing currently in progress.

---

### Member management

The following APIs all require **being in a meeting**, and none of them return a value.

#### `adminUpdateUserName(targetId:nickname:)`

| Parameter | Type | Required | Description |
| --- | --- | :---: | --- |
| `targetId` | `String` | Yes | Target member ID |
| `nickname` | `String` | Yes | New in-meeting display name |

#### `adminUpdateUserRole(targetId:role:)`

| Parameter | Type | Required | Description |
| --- | --- | :---: | --- |
| `targetId` | `String` | Yes | Target member ID |
| `role` | `Role` | Yes | `.member` / `.coHost` |

#### `adminUpdateUserChatDisabled(targetId:chatDisabled:)`

| Parameter | Type | Required | Description |
| --- | --- | :---: | --- |
| `targetId` | `String` | Yes | Target member ID |
| `chatDisabled` | `Bool` | Yes | Whether to disable chat for this member |

#### `adminUpdateUserDrawDisabled(targetId:drawDisable:)`

| Parameter | Type | Required | Description |
| --- | --- | :---: | --- |
| `targetId` | `String` | Yes | Target member ID |
| `drawDisable` | `Bool` | Yes | Whether to prevent this member from drawing |

Read the current state from `MeetingUserInfo.drawDisabled`; when it changes, all members receive `meeting(_:userDrawDisabledDidChange:)` (available since 1.3.6).

#### `adminMoveHost(targetId:)`

Transfers the host role.

| Parameter | Type | Required | Description |
| --- | --- | :---: | --- |
| `targetId` | `String` | Yes | ID of the new host |

#### `adminRequestUserOpenMic(targetId:)` / `adminRequestUserOpenCamera(targetId:)`

Asks a member to turn on their microphone / camera.

| Parameter | Type | Required | Description |
| --- | --- | :---: | --- |
| `targetId` | `String` | Yes | Target member ID |

#### `adminCloseUserMic(targetId:)` / `adminCloseUserCamera(targetId:)`

Turns off a member's microphone / camera directly.

| Parameter | Type | Required | Description |
| --- | --- | :---: | --- |
| `targetId` | `String` | Yes | Target member ID |

#### `adminKickUserOut(targetId:joinDisabled:)`

| Parameter | Type | Required | Description |
| --- | --- | :---: | --- |
| `targetId` | `String` | Yes | Target member ID |
| `joinDisabled` | `Bool` | No | Whether to also prevent the member from entering the meeting again; defaults to `false` |

#### `adminConfirmHandup(targetId:approve:code:)`

Approves or rejects a raise-hand request.

| Parameter | Type | Required | Description |
| --- | --- | :---: | --- |
| `targetId` | `String` | Yes | ID of the member who raised their hand |
| `approve` | `Bool` | Yes | Whether to approve |
| `code` | `HandupType` | Yes | Raise-hand type |

---

### Invitees and devices

#### `adminUpdateConferee(meetingId:conferee:)`

Updates the invitee list. **Requires being logged in.**

| Parameter | Type | Required | Description |
| --- | --- | :---: | --- |
| `meetingId` | `String` | Yes | Meeting ID |
| `conferee` | `[String]` | Yes | List of invitee IDs |

**Returns:** None

#### `adminCallUsers(conferee:)`

Calls people during the meeting. **Requires being in a meeting.**

| Parameter | Type | Required | Description |
| --- | --- | :---: | --- |
| `conferee` | `[String]` | Yes | IDs of the invitees to call |

**Returns:** None

#### `meetNotEnter()`

Queries the invitees who haven't entered the meeting yet. **Requires being in a meeting.**

**Returns:** `[NoEnterUserInfo]`

#### `adminMeetRemind(uids:useSms:)`

Reminds people to enter the meeting. **Requires being in a meeting.**

| Parameter | Type | Required | Description |
| --- | --- | :---: | --- |
| `uids` | `[String]` | Yes | IDs of the invitees to remind |
| `useSms` | `Bool` | No | Whether to also send an SMS; defaults to `false` |

**Returns:** None

#### `adminListOnlineMember(page:perPage:)`

Lists online members. **Requires being in a meeting.**

| Parameter | Type | Required | Description |
| --- | --- | :---: | --- |
| `page` | `Int` | No | Page number; defaults to `1` |
| `perPage` | `Int` | No | Items per page; defaults to `20` |

**Returns:** `PageResult<OnlineMemberInfo>`

#### `agentList(type:name:page:perPage:)`

Lists the devices that can be invited. **Requires being logged in.**

| Parameter | Type | Required | Description |
| --- | --- | :---: | --- |
| `type` | `[AgentType]` | Yes | Device type filter |
| `name` | `String` | No | Name filter; defaults to an empty string (no filtering) |
| `page` | `Int` | No | Page number; defaults to `1` |
| `perPage` | `Int` | No | Items per page; defaults to `20` |

**Returns:** `PageResult<AgentInfo>`

#### `adminInviteAgent(agents:no:)`

Invites devices to the meeting. **Requires being logged in.**

| Parameter | Type | Required | Description |
| --- | --- | :---: | --- |
| `agents` | `[(type: AgentType, contact: String)]` | Yes | Device types and contact addresses |
| `no` | `String` | Yes | Room number of the meeting |

**Returns:** None

---

### Waiting room

#### `adminUpdateWaitingRoomDisabled(_:)`

**Requires being in a meeting.**

| Parameter | Type | Required | Description |
| --- | --- | :---: | --- |
| `disabled` | `Bool` | Yes | `true` turns the waiting room off; `false` turns it on |

**Returns:** None

#### `adminWaitingRoomUsers()`

**Requires being in a meeting.**

**Returns:** `[WaitingRoomUserInfo]`

#### `adminMoveInWaitingRoom(userId:nickname:)`

Moves a member in the meeting back to the waiting room. **Requires being in a meeting.**

| Parameter | Type | Required | Description |
| --- | --- | :---: | --- |
| `userId` | `String` | Yes | Member ID |
| `nickname` | `String` | Yes | Member's nickname |

**Returns:** None

#### `adminMoveOutWaitingRoom(userId:nickname:)`

Admits a member from the waiting room into the meeting. Omit both parameters to admit everyone. **Requires being in a meeting.**

| Parameter | Type | Required | Description |
| --- | --- | :---: | --- |
| `userId` | `String?` | No | Member ID |
| `nickname` | `String?` | No | Member's nickname |

**Returns:** None

#### `exitWaitingRoom(meetingId:roomNo:)`

The member exits the waiting room on their own; provide either of the two parameters. **Requires being logged in.**

| Parameter | Type | Required | Description |
| --- | --- | :---: | --- |
| `meetingId` | `String?` | No | Meeting ID |
| `roomNo` | `String?` | No | Room number |

**Returns:** None

---

### Sub-meetings

Except for `userHelpSubMeeting()`, the following APIs **only require being logged in**.

#### `adminCreateSubMeeting(mainMeetingId:titles:)`

| Parameter | Type | Required | Description |
| --- | --- | :---: | --- |
| `mainMeetingId` | `String` | Yes | Main meeting ID |
| `titles` | `[String]` | Yes | List of titles of the sub-meetings to create |

**Returns:** None

#### `adminSubMeetingList(mainMeetingId:)`

| Parameter | Type | Required | Description |
| --- | --- | :---: | --- |
| `mainMeetingId` | `String` | Yes | Main meeting ID |

**Returns:** `[SubMeetingInfo]`

#### `adminUpdateSubMeetingTitle(id:title:)`

| Parameter | Type | Required | Description |
| --- | --- | :---: | --- |
| `id` | `String` | Yes | Sub-meeting ID |
| `title` | `String` | Yes | New title |

**Returns:** None

#### `adminUpdateSubMeetingUsers(id:users:)`

| Parameter | Type | Required | Description |
| --- | --- | :---: | --- |
| `id` | `String` | Yes | Sub-meeting ID |
| `users` | `[(uid: String, name: String)]` | Yes | Members assigned to this sub-meeting |

**Returns:** None

#### `adminDeleteSubMeeting(ids:)`

| Parameter | Type | Required | Description |
| --- | --- | :---: | --- |
| `ids` | `[String]` | Yes | List of sub-meeting IDs |

**Returns:** None

#### `adminStartSubMeeting(ids:)` / `adminStopSubMeeting(ids:)`

| Parameter | Type | Required | Description |
| --- | --- | :---: | --- |
| `ids` | `[String]` | Yes | List of sub-meeting IDs |

**Returns:** None

#### `adminMoveSubMeetingUser(fromId:toId:userId:)`

| Parameter | Type | Required | Description |
| --- | --- | :---: | --- |
| `fromId` | `String` | Yes | Source sub-meeting ID |
| `toId` | `String` | Yes | Target sub-meeting ID |
| `userId` | `String` | Yes | Member ID |

**Returns:** None

#### `userHelpSubMeeting()`

A member in a sub-meeting asks the main meeting for help. **Requires being in a meeting.**

**Returns:** None

---

### Layout and recording

#### `adminUpdateLayout(_:)`

Updates the layout of a composite meeting. **Requires being in a meeting.**

| Parameter | Type | Required | Description |
| --- | --- | :---: | --- |
| `layoutData` | `LayoutData` | Yes | Layout configuration; for the fields, see [Recording and composite layout](/en/meeting/swift/advanced/recording) |

**Returns:** None

#### `mcuStart(meetingId:req:)`

Starts a recording / stream mixing task. **Requires being logged in.**

| Parameter | Type | Required | Description |
| --- | --- | :---: | --- |
| `meetingId` | `String` | Yes | Meeting ID |
| `req` | `McuStartReq` | Yes | Task parameters |

**Returns:** None

#### `mcuStop(meetingId:taskType:)`

**Requires being logged in.**

| Parameter | Type | Required | Description |
| --- | --- | :---: | --- |
| `meetingId` | `String` | Yes | Meeting ID |
| `taskType` | `McuTaskType` | Yes | Type of the task to stop |

**Returns:** None

#### `mcuRecordConfig()`

**Requires being logged in.**

**Returns:** `McuRecordConfig`

#### `mcuRecordDetail(meetingId:)`

**Requires being logged in.**

| Parameter | Type | Required | Description |
| --- | --- | :---: | --- |
| `meetingId` | `String` | Yes | Meeting ID |

**Returns:** `McuRecordDetail`

---

### Resources

The following APIs all **only require being logged in**.

#### `presignedPutObject(type:meetingId:ext:)`

Gets an upload URL.

| Parameter | Type | Required | Description |
| --- | --- | :---: | --- |
| `type` | `PresignedPutObjectType` | Yes | `.attach` / `.background` / `.user` |
| `meetingId` | `String` | Yes | Meeting ID |
| `ext` | `String` | Yes | File extension, for example `pdf` |

**Returns:** `(url: String, key: String, ext: String)`

#### `presignedGetObject(id:resKey:)`

Gets a download URL; provide either of the two parameters.

| Parameter | Type | Required | Description |
| --- | --- | :---: | --- |
| `id` | `String?` | No | Resource ID |
| `resKey` | `String?` | No | Resource key |

**Returns:** `String` (a signed download URL)

#### `resourcesList(req:)`

| Parameter | Type | Required | Description |
| --- | --- | :---: | --- |
| `req` | `ResourceListReq` | Yes | Query conditions |

**Returns:** `PageResult<ResourceInfo>`

#### `resourcesCreate(req:)`

Registers a resource.

| Parameter | Type | Required | Description |
| --- | --- | :---: | --- |
| `req` | `ResourceCreateReq` | Yes | Resource information |

**Returns:** None

---

### Sign-in

The following APIs all **require being in a meeting** and act on the current meeting.

#### `signInCreate(dur:desc:)`

Starts a round of sign-in.

| Parameter | Type | Required | Description |
| --- | --- | :---: | --- |
| `dur` | `Int` | Yes | How long the sign-in lasts, in **minutes** |
| `desc` | `String` | Yes | Sign-in description |

**Returns:** None

#### `signInFinish()`

Ends the current round of sign-in early.

**Returns:** None

#### `signInSign()`

The member signs in.

**Returns:** None

#### `signInList()`

**Returns:** `(list: [SignInfo]?, now: Int)`, where `now` is the server's current time

#### `signInCount(epoch:)`

| Parameter | Type | Required | Description |
| --- | --- | :---: | --- |
| `epoch` | `Int` | Yes | Sign-in round |

**Returns:** `Int` (the number of members who have signed in)

#### `signInDetail(epoch:nickname:)`

| Parameter | Type | Required | Description |
| --- | --- | :---: | --- |
| `epoch` | `Int` | Yes | Sign-in round |
| `nickname` | `String?` | No | Filter by nickname |

**Returns:** `[SignDetailInfo]`

---

### Related pages

+ [Host controls](/en/meeting/swift/advanced/host-controls)
+ [Waiting room](/en/meeting/swift/advanced/waiting-room)
+ [Sub-meetings](/en/meeting/swift/advanced/sub-meetings)
+ [Recording and composite layout](/en/meeting/swift/advanced/recording)
+ [Meeting materials](/en/meeting/swift/advanced/resources)
+ [Sign-in and roll call](/en/meeting/swift/advanced/sign-in)
