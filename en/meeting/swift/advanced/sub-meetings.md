---
title: "Sub-meetings"
description: "Split a main meeting into sub-meetings with the SMeeting Swift SDK: create groups, assign and move members, start and stop them, switch meetings on the member side, and let groups ask the host for help. Read when building group discussions."
---

### Overview

Sub-meetings split one main meeting into several sub-meetings (groups). Members assigned to a group enter their own meeting, and return to the main meeting when the discussion ends.

+ The main meeting must be created in `MeetingMode.subMeeting` mode
+ The group orchestration APIs all have the `admin` prefix and are called by the host / a co-host
+ Group information is represented by `SubMeetingInfo`; `mainMeetingId` points to the main meeting, and `meetingId` is the group's own meeting ID

---

### Orchestrate groups

```swift
// Create several groups
try await meeting.adminCreateSubMeeting(mainMeetingId: mainId, titles: ["Group 1", "Group 2"])

// Query the group list
let groups = try await meeting.adminSubMeetingList(mainMeetingId: mainId)

// Rename a group
try await meeting.adminUpdateSubMeetingTitle(id: groups[0].id, title: "Product team")

// Assign members
try await meeting.adminUpdateSubMeetingUsers(
    id: groups[0].id,
    users: [(uid: "u1", name: "Alice"), (uid: "u2", name: "Bob")]
)

// Delete a group
try await meeting.adminDeleteSubMeeting(ids: [groups[1].id])
```

In each `SubMeetingInfo` returned by `adminSubMeetingList`, `users` are the assigned members, and `status` is the group's meeting status (`MeetingStatus`).

---

### Start and stop

```swift
// Start (you can start multiple groups at once)
try await meeting.adminStartSubMeeting(ids: [groupId1, groupId2])

// Stop
try await meeting.adminStopSubMeeting(ids: [groupId1, groupId2])
```

After receiving the corresponding event, the member side switches meetings on its own:

```swift
func meeting(_ meeting: SMeetingEngine, adminDidStartSubMeeting data: AdminStartSubMeetingEventData) {
    // data.meetingId meeting ID of the target group
    // data.title     group name
    // data.uids      members assigned to this group
    Task {
        await meeting.exitRoom()
        try await meeting.enterRoom(MeetingEnterReq(nickname: myNickname, meetingId: data.meetingId))
    }
}

func meeting(_ meeting: SMeetingEngine, adminDidStopSubMeeting data: AdminStopSubMeetingEventData) {
    // data.parent is the main meeting ID; after exiting the group, go back to the main meeting
    Task {
        await meeting.exitRoom()
        try await meeting.enterRoom(MeetingEnterReq(nickname: myNickname, meetingId: data.parent))
    }
}
```

> Switching meetings requires "exit the current meeting first, then enter the target meeting." The SDK doesn't switch for you automatically—when to switch and what to show the user during the switch are up to your app.

---

### Move members between groups

```swift
try await meeting.adminMoveSubMeetingUser(fromId: groupA, toId: groupB, userId: uid)
```

The moved member receives:

```swift
func meeting(_ meeting: SMeetingEngine, adminDidMoveSubMeetingUser data: AdminMoveSubMeetingUserEventData) {
    // data.fromMeetingId / data.fromMeetingTitle
    // data.toMeetingId   / data.toMeetingTitle
}
```

Likewise, your app needs to exit the old meeting and enter the new one itself.

---

### Groups ask the host for help

Members in a group can ask the main meeting for help:

```swift
try await meeting.userHelpSubMeeting()
```

If the host has enabled the out-of-meeting message path, they receive:

```swift
func meeting(_ meeting: SMeetingEngine, imUserHelpSubMeeting data: ImUserHelpSubMeetingEventData) {
    // data.base.uid / data.base.name the member asking for help
    // data.content.meetingId / data.content.title the group
    // data.content.parent main meeting ID
}
```

This notification goes through the out-of-meeting message path, so you must call `enableIm()` first; see [Out-of-meeting messages](/en/meeting/swift/advanced/im).

---

### Related pages

+ [Host controls](/en/meeting/swift/advanced/host-controls)
+ [Out-of-meeting messages](/en/meeting/swift/advanced/im)
+ [Events](/en/meeting/swift/events)
