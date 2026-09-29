---
title: "Waiting room"
description: "Turn the waiting room on or off with the SMeeting Swift SDK, list waiting members, admit them or move members back, let members exit the waiting room on their own, and handle the related events. Read when your meetings need the host to admit members one by one."
---

### Overview

The waiting room makes members wait in a holding area before entering the meeting, and the host admits them one by one.

+ To check whether it's enabled, read `RoomInfo.waitingRoomDisabled` (`true` means the waiting room is **off**)
+ You can preset it with `MeetingCreateReq.waitingRoomDisabled` when creating the meeting
+ During the meeting, the host / a co-host can change it

---

### Turn the waiting room on or off

```swift
// Turn off the waiting room (members enter the meeting directly)
try await meeting.adminUpdateWaitingRoomDisabled(true)

// Turn on the waiting room
try await meeting.adminUpdateWaitingRoomDisabled(false)
```

When the state changes, all members receive:

```swift
func meeting(_ meeting: SMeetingEngine, waitingRoomDisabledDidChange data: AdminUpdateWaitingRoomDisabledEventData) {
    // data.waitingRoomDisabled, data.opUid
}
```

---

### View waiting members

```swift
let users = try await meeting.adminWaitingRoomUsers()
```

Returns `[WaitingRoomUserInfo]`, including `userId`, `name`, `avatar`, and `at` (the time they entered the waiting room).

Events notify you when someone enters or exits the waiting room, so the host can refresh the list incrementally:

```swift
func meeting(_ meeting: SMeetingEngine, userDidEnterWaitingRoom data: UserEnterWaitingRoomEventData) {
    // data.uid, data.name, data.avatar
}

func meeting(_ meeting: SMeetingEngine, userDidExitWaitingRoom data: UserExitWaitingRoomEventData) {
    // data.uid, data.name, data.avatar
}
```

---

### Admit and move back

```swift
// Admit from the waiting room into the meeting
try await meeting.adminMoveOutWaitingRoom(userId: uid, nickname: name)

// Admit everyone: omit both parameters
try await meeting.adminMoveOutWaitingRoom()

// Move a member in the meeting back to the waiting room
try await meeting.adminMoveInWaitingRoom(userId: uid, nickname: name)
```

A member moved back to the waiting room receives:

```swift
func meetingDidMoveToWaitingRoom(_ meeting: SMeetingEngine) {
    // Switch to the waiting screen
}
```

---

### Members exit the waiting room on their own

If a member in the waiting room doesn't want to keep waiting:

```swift
try await meeting.exitWaitingRoom(roomNo: roomNo)
```

Provide either `meetingId` or `roomNo`. This API only requires login, not being in a meeting.

---

### Related pages

+ [Host controls](/en/meeting/swift/advanced/host-controls)
+ [Events](/en/meeting/swift/events)
