---
title: "等候室"
description: "SMeeting Swift SDK 的等候室开关、候场成员管理与相关事件"
---

### 概述

等候室让成员进入会议前先在候场区等待，由主持人逐个放行。

+ 是否启用读 `RoomInfo.waitingRoomDisabled`（`true` 表示**关闭**等候室）
+ 创建会议时可以通过 `MeetingCreateReq.waitingRoomDisabled` 预设
+ 会中由主持人 / 联席主持人调整

---

### 开关等候室

```swift
// 关闭等候室（成员直接进入会议）
try await meeting.adminUpdateWaitingRoomDisabled(true)

// 启用等候室
try await meeting.adminUpdateWaitingRoomDisabled(false)
```

状态变化时所有成员收到：

```swift
func meeting(_ meeting: SMeetingEngine, waitingRoomDisabledDidChange data: AdminUpdateWaitingRoomDisabledEventData) {
    // data.waitingRoomDisabled、data.opUid
}
```

---

### 查看候场成员

```swift
let users = try await meeting.adminWaitingRoomUsers()
```

返回 `[WaitingRoomUserInfo]`，含 `userId`、`name`、`avatar`、`at`（进入等候室时间）。

有人进出等候室时会有事件通知，主持人可以据此增量刷新列表：

```swift
func meeting(_ meeting: SMeetingEngine, userDidEnterWaitingRoom data: UserEnterWaitingRoomEventData) {
    // data.uid、data.name、data.avatar
}

func meeting(_ meeting: SMeetingEngine, userDidExitWaitingRoom data: UserExitWaitingRoomEventData) {
    // data.uid、data.name、data.avatar
}
```

---

### 放行与移入

```swift
// 从等候室放进会议
try await meeting.adminMoveOutWaitingRoom(userId: uid, nickname: name)

// 全部放行：两个参数都不传
try await meeting.adminMoveOutWaitingRoom()

// 把会议中的成员移回等候室
try await meeting.adminMoveInWaitingRoom(userId: uid, nickname: name)
```

被移回等候室的成员会收到：

```swift
func meetingDidMoveToWaitingRoom(_ meeting: SMeetingEngine) {
    // 切换到等候界面
}
```

---

### 成员主动离开等候室

在等候室里的成员如果不想继续等待：

```swift
try await meeting.exitWaitingRoom(roomNo: roomNo)
```

`meetingId` 与 `roomNo` 二选一填写。这个接口只需要登录，不要求在会议中。

---

### 相关页面

+ [主持人管控](/zh/meeting/swift/advanced/host-controls)
+ [事件参考](/zh/meeting/swift/events)
