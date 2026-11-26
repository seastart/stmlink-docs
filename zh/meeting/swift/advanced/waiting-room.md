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

### 入会被转入等候室

会议开启了等候室时，非主持人 `enterRoom` 会抛 `apiError`，`code` 为 `2118`（常量 `SMeetingError.waitingRoomCode`，1.14.0 起）。此时服务端已把本人记入候场名单，App 应进入等待页，而不是当作失败处理。主持人放行后收到会议外消息 `meeting(_:imAdminMoveOutWaitingRoom:)`，再重新 `enterRoom` 即可。

---

### 等待主持人入会

会议开启了「主持人入会前禁止加入」、且主持人 / 联席主持人 / 创建者都未入会时，`enterRoom` 抛 `apiError`，`code` 为 `2120`（常量 `SMeetingError.enterBeforeHostCode`，1.14.0 起）。服务端已把本人记入等主持人名单，App 应进入「等待主持人」页。

```swift
do {
    try await meeting.enterRoom(req)
} catch let error as SMeetingError where error.code == SMeetingError.enterBeforeHostCode {
    showWaitingPage(mode: .waitingHost)      // 等主持人
} catch let error as SMeetingError where error.code == SMeetingError.waitingRoomCode {
    showWaitingPage(mode: .waitingRoom)      // 等候室
}
```

等待期间通过会议外消息得知进展（需要先 `enableIm()`，见 [会议外消息](/zh/meeting/swift/advanced/im#等待页消息)）：

```swift
// 主持人 / 联席主持人 / 创建者任一入会
func meeting(_ meeting: SMeetingEngine, imHostEntered data: ImHostEnteredEventData) {
    guard data.content.meetingId == waitingMeetingId else { return }
    // 带原密码重新 enterRoom
}

// 会议结束或取消（等主持人、等候室两种等待页都会收到）
func meeting(_ meeting: SMeetingEngine, imWaitingMeetingEnd data: ImWaitingMeetingEndEventData) {
    guard data.content.meetingId == waitingMeetingId else { return }
    // 提示「会议已结束」，离开等待页
}
```

+ 服务端的检查顺序是密码 → `2120` → `2118`：两个开关都开时，先等主持人；主持人到了重新入会，再拿到 `2118` 转入等候室
+ 同一账号可能先后在等不同的会议，收到消息后请按 `meetingId` / `roomNo` 判断是不是当前等待的那场

---

### 成员主动离开等候

在等候室或等主持人的成员如果不想继续等待：

```swift
try await meeting.exitWaitingRoom(roomNo: roomNo)
```

`meetingId` 与 `roomNo` 二选一填写。这个接口只需要登录，不要求在会议中。它同时把本人移出候场名单和等主持人名单，两种等待页离开时都调用它。

---

### 相关页面

+ [主持人管控](/zh/meeting/swift/advanced/host-controls)
+ [会议外消息](/zh/meeting/swift/advanced/im)
+ [错误处理](/zh/meeting/swift/error-codes)
+ [事件参考](/zh/meeting/swift/events)
