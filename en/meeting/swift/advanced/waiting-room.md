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

### Moved into the waiting room on entry

When the meeting has the waiting room on, `enterRoom` for a non-host throws `apiError` with `code` `2118` (constant `SMeetingError.waitingRoomCode`, since 1.14.0). The server has already put the user on the waiting list, so the app should show a waiting page instead of treating it as a failure. After the host admits the user, the out-of-meeting message `meeting(_:imAdminMoveOutWaitingRoom:)` arrives; then call `enterRoom` again.

---

### Wait for the host to join

When the meeting has "no one may join before the host" turned on and none of the host / co-host / creator has joined, `enterRoom` throws `apiError` with `code` `2120` (constant `SMeetingError.enterBeforeHostCode`, since 1.14.0). The server has already put the user on the waiting-for-host list, so the app should show a "waiting for the host" page.

```swift
do {
    try await meeting.enterRoom(req)
} catch let error as SMeetingError where error.code == SMeetingError.enterBeforeHostCode {
    showWaitingPage(mode: .waitingHost)      // waiting for the host
} catch let error as SMeetingError where error.code == SMeetingError.waitingRoomCode {
    showWaitingPage(mode: .waitingRoom)      // waiting room
}
```

While waiting, progress arrives as out-of-meeting messages (call `enableIm()` first; see [Out-of-meeting messages](/en/meeting/swift/advanced/im#waiting-page-messages)):

```swift
// Any of the host / co-host / creator joined
func meeting(_ meeting: SMeetingEngine, imHostEntered data: ImHostEnteredEventData) {
    guard data.content.meetingId == waitingMeetingId else { return }
    // Call enterRoom again with the original password
}

// The meeting ended or was cancelled (received on both kinds of waiting page)
func meeting(_ meeting: SMeetingEngine, imWaitingMeetingEnd data: ImWaitingMeetingEndEventData) {
    guard data.content.meetingId == waitingMeetingId else { return }
    // Show "The meeting has ended" and leave the waiting page
}
```

+ The server checks in the order password → `2120` → `2118`: when both switches are on, the user first waits for the host; re-entering after the host joins then returns `2118` and moves the user into the waiting room
+ The same account may wait for different meetings one after another, so check `meetingId` / `roomNo` to tell whether a message is for the meeting currently being waited for

---

### Members stop waiting on their own

If a member in the waiting room or waiting for the host doesn't want to keep waiting:

```swift
try await meeting.exitWaitingRoom(roomNo: roomNo)
```

Provide either `meetingId` or `roomNo`. This API only requires login, not being in a meeting. It removes the user from both the waiting list and the waiting-for-host list, so call it when leaving either kind of waiting page.

---

### Related pages

+ [Host controls](/en/meeting/swift/advanced/host-controls)
+ [Out-of-meeting messages](/en/meeting/swift/advanced/im)
+ [Error handling](/en/meeting/swift/error-codes)
+ [Events](/en/meeting/swift/events)
