---
title: "分组讨论"
description: "SMeeting Swift SDK 的子会议（分组讨论）创建、分配成员、开始结束与成员端响应"
---

### 概述

分组讨论把一场主会议拆成若干个子会议（小组），成员被分配到小组后进入各自的会议，讨论结束再回到主会场。

+ 主会议需要以 `MeetingMode.subMeeting` 模式创建
+ 小组的编排接口都带 `admin` 前缀，由主持人 / 联席主持人调用
+ 小组信息用 `SubMeetingInfo` 表示，`mainMeetingId` 指向主会议，`meetingId` 是这个小组自己的会议 ID

---

### 编排小组

```swift
// 创建若干小组
try await meeting.adminCreateSubMeeting(mainMeetingId: mainId, titles: ["第一组", "第二组"])

// 查询小组列表
let groups = try await meeting.adminSubMeetingList(mainMeetingId: mainId)

// 改小组名
try await meeting.adminUpdateSubMeetingTitle(id: groups[0].id, title: "产品组")

// 分配成员
try await meeting.adminUpdateSubMeetingUsers(
    id: groups[0].id,
    users: [(uid: "u1", name: "张三"), (uid: "u2", name: "李四")]
)

// 删除小组
try await meeting.adminDeleteSubMeeting(ids: [groups[1].id])
```

`adminSubMeetingList` 返回的每个 `SubMeetingInfo` 里 `users` 是已分配成员，`status` 是小组的会议状态（`MeetingStatus`）。

---

### 开始与结束

```swift
// 开始（可一次开多个小组）
try await meeting.adminStartSubMeeting(ids: [groupId1, groupId2])

// 结束
try await meeting.adminStopSubMeeting(ids: [groupId1, groupId2])
```

成员端收到对应事件后自行完成会议切换：

```swift
func meeting(_ meeting: SMeeting, adminDidStartSubMeeting data: AdminStartSubMeetingEventData) {
    // data.meetingId 目标小组会议 ID
    // data.title     小组名称
    // data.uids      被分配到这个小组的成员
    Task {
        await meeting.exitRoom()
        try await meeting.enterRoom(MeetingEnterReq(nickname: myNickname, meetingId: data.meetingId))
    }
}

func meeting(_ meeting: SMeeting, adminDidStopSubMeeting data: AdminStopSubMeetingEventData) {
    // data.parent 主会议 ID，退出小组后回到主会场
    Task {
        await meeting.exitRoom()
        try await meeting.enterRoom(MeetingEnterReq(nickname: myNickname, meetingId: data.parent))
    }
}
```

> 会议切换需要「先退出当前会议，再进入目标会议」。SDK 不会自动帮你换场 —— 什么时候切、切换过程中给用户什么提示，由你的业务决定。

---

### 小组间调整成员

```swift
try await meeting.adminMoveSubMeetingUser(fromId: groupA, toId: groupB, userId: uid)
```

被移动的成员收到：

```swift
func meeting(_ meeting: SMeeting, adminDidMoveSubMeetingUser data: AdminMoveSubMeetingUserEventData) {
    // data.fromMeetingId / data.fromMeetingTitle
    // data.toMeetingId   / data.toMeetingTitle
}
```

同样需要业务侧自行完成退出旧会议、进入新会议。

---

### 小组请求主持人协助

小组内的成员可以向主会场求助：

```swift
try await meeting.userHelpSubMeeting()
```

主持人如果启用了会议外消息通道，会收到：

```swift
func meeting(_ meeting: SMeeting, imUserHelpSubMeeting data: ImUserHelpSubMeetingEventData) {
    // data.base.uid / data.base.name 求助者
    // data.content.meetingId / data.content.title 小组
    // data.content.parent 主会议 ID
}
```

这条通知走的是会议外消息通道，需要先调用 `enableIm()`，见 [会议外消息](/zh/meeting/swift/advanced/im)。

---

### 相关页面

+ [主持人管控](/zh/meeting/swift/advanced/host-controls)
+ [会议外消息](/zh/meeting/swift/advanced/im)
+ [事件参考](/zh/meeting/swift/events)
