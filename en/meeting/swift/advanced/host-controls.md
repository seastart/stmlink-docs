---
title: "Host controls"
description: "What the host and co-hosts can do with the SMeeting Swift SDK: room-level controls such as mute all, camera off for everyone, and locking the meeting, member management, invitee reminders and calls, and inviting SIP / H.323 / GB28181 devices into the meeting. Read when building a host panel."
---

### Overview

APIs with the `admin` prefix require the host (`.host`) or co-host (`.coHost`) role; regular members who call them get a permission error from the server. Check before calling:

```swift
let me = try? meeting.getUserInfo(meeting.currentUserId ?? "")
let isAdmin = me?.role == .host || me?.role == .coHost
```

Once a control action takes effect, **all members** receive the corresponding room / member state event. You don't need to change state manually on the initiating side; just refresh in the event handlers.

---

### Room-level controls

| API | Purpose | Room field | Change event |
| --- | --- | --- | --- |
| `adminUpdateRoomMicState(selfUnmuteMicDisabled:micDisabled:)` | Mute all | `micDisabled` / `selfUnmuteMicDisabled` | `roomMicStateDidChange` |
| `adminUpdateRoomCameraState(selfUnmuteCameraDisabled:cameraDisabled:)` | Camera off for everyone | `cameraDisabled` / `selfUnmuteCameraDisabled` | `roomCameraStateDidChange` |
| `adminUpdateRoomShareState(shareDisabled:)` | Disable sharing | `shareDisabled` | `roomShareStateDidChange` |
| `adminUpdateRoomChatDisabled(_:)` | Disable chat for everyone | `chatDisabled` | `roomChatDisabledDidChange` |
| `adminUpdateRoomScreenshotDisabled(_:)` | Disable screenshots | `screenshotDisabled` | `roomScreenshotDisabledDidChange` |
| `adminUpdateRoomWatermarkDisabled(_:)` | Turn off the watermark | `watermarkDisabled` | `roomWatermarkDisabledDidChange` |
| `adminUpdateRoomLocked(_:)` | Lock the meeting | `locked` | `roomLockedDidChange` |
| `adminUpdateEnterBeforeHostDisabled(_:)` | Disallow entering before the host | `enterBeforeHostDisabled` | No separate event |
| `adminStopRoomShare()` | Force the current sharing to end | `shareState` | `roomShareDidStop` |
| `adminDestroyRoom()` | End the whole meeting | — | Members receive `didDisconnect` |

#### The two switches of mute all

`micDisabled` and `selfUnmuteMicDisabled` mean different things, and together they determine the members' experience:

```swift
// Mute all, and don't allow members to unmute themselves
try await meeting.adminUpdateRoomMicState(selfUnmuteMicDisabled: true, micDisabled: true)

// Mute all, but allow members to unmute themselves
try await meeting.adminUpdateRoomMicState(selfUnmuteMicDisabled: false, micDisabled: true)

// Turn off mute all
try await meeting.adminUpdateRoomMicState(selfUnmuteMicDisabled: false, micDisabled: false)
```

When "mute all" is turned on, the microphones of non-host members are turned off automatically. Whether members can then turn their microphones back on themselves depends on `selfUnmuteMicDisabled`. The camera follows the same rules.

#### End the meeting

```swift
try await meeting.adminDestroyRoom()
```

All members are disconnected, and the member side learns about it through `meeting(_:didDisconnect:)`. The initiator also needs to take its own UI back out of the meeting.

---

### Member management

```swift
// Change a member's in-meeting display name
try await meeting.adminUpdateUserName(targetId: uid, nickname: "Alice")

// Make a co-host / revoke
try await meeting.adminUpdateUserRole(targetId: uid, role: .coHost)
try await meeting.adminUpdateUserRole(targetId: uid, role: .member)

// Transfer host (after the transfer, you become a regular member)
try await meeting.adminMoveHost(targetId: uid)

// Disable chat for an individual member
try await meeting.adminUpdateUserChatDisabled(targetId: uid, chatDisabled: true)

// Prevent drawing
try await meeting.adminUpdateUserDrawDisabled(targetId: uid, drawDisable: true)

// Remove from the meeting; joinDisabled set to true also prevents entering again
try await meeting.adminKickUserOut(targetId: uid, joinDisabled: true)
```

The corresponding member state events: `userNameDidChange`, `userRoleDidChange`, `userChatDisabledDidChange`, `userDrawDisabledDidChange` (since 1.3.6). A removed member learns about it through `didDisconnect`.

Read the current drawing permission from `MeetingUserInfo.drawDisabled`; when it changes, you receive:

```swift
func meeting(_ meeting: SMeetingEngine, userDrawDisabledDidChange data: UserDrawDisabledChangeEventData) {
    // data.uid, data.drawDisabled, data.opUid
}
```

For turning off a member's microphone / camera and asking members to turn them on, see [Raise hand and turn-on requests](/en/meeting/swift/advanced/handup).

---

### Change your own in-meeting display name

This action doesn't require the host role:

```swift
try await meeting.updateName("New nickname")
```

---

### Invitee management

#### Update the invitee list

```swift
try await meeting.adminUpdateConferee(meetingId: meetingId, conferee: [uid1, uid2])
```

#### Find out who hasn't entered yet

```swift
let notEntered = try await meeting.meetNotEnter()
```

Returns `[NoEnterUserInfo]`, including nickname, phone number, avatar, role, and more.

#### Remind invitees to enter

```swift
try await meeting.adminMeetRemind(uids: [uid1, uid2], useSms: true)
```

When `useSms` is `true`, an SMS reminder is sent as well.

#### In-meeting calls

```swift
try await meeting.adminCallUsers(conferee: [uid1, uid2])
```

If the called users have enabled out-of-meeting messages, they receive the `imCallCalling` event; see [Out-of-meeting messages](/en/meeting/swift/advanced/im).

#### Online member list

```swift
let page = try await meeting.adminListOnlineMember(page: 1, perPage: 20)
```

---

### Invite devices into the meeting

Meetings support bringing external devices into the meeting, such as SIP, H.323, GB28181, RTSP / RTMP pull streams, and file playback.

First, query the available devices:

```swift
let devices = try await meeting.agentList(type: [.sip, .h323], name: "Meeting room")
```

Then send the invitation:

```swift
try await meeting.adminInviteAgent(
    agents: [(type: .sip, contact: "sip:1001@example.com")],
    no: roomNo
)
```

For `AgentType` values, see [Types](/en/meeting/swift/types#agenttype). Read a device's current busy / idle status from `AgentInfo.status`.

---

### Related pages

+ [Raise hand and turn-on requests](/en/meeting/swift/advanced/handup)
+ [Waiting room](/en/meeting/swift/advanced/waiting-room)
+ [Sub-meetings](/en/meeting/swift/advanced/sub-meetings)
+ [API reference - Meeting management](/en/meeting/swift/api-reference/admin-actions)
