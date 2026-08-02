---
title: "会议外消息"
description: "SMeeting Swift SDK 的会议外消息通道：启用与停用、呼叫与会议提醒等事件"
---

### 概述

会议外消息（IM）是一条**独立于会议的通知通道**。它解决的是「用户还没进会议时怎么被通知到」这类问题：

+ 有人在会议里呼叫你
+ 预约会议快开始了
+ 你在等候室里被放行了
+ 你负责的讨论小组请求协助

会中的聊天消息不走这条通道 —— 那是 [会中消息](/zh/meeting/swift/advanced/messaging)，只在会议期间有效。

---

### 启用与停用

```swift
// 登录之后即可启用，不需要在会议中
try await meeting.enableIm()

// 不再需要时
await meeting.disableIm()
```

要点：

+ 必须先 `login(token:)`，未登录调用会抛出 `SMeetingError.notLoggedIn`
+ `logout()` 内部会自动停用这条通道，你不需要在登出流程里重复调用
+ 通道建立后一直保持，与是否在会议中无关

典型接入位置是登录成功之后：

```swift
try await meeting.login(token: token)
meeting.delegates.add(delegate: self)
try await meeting.enableIm()
```

---

### 事件

所有会议外消息事件都带一个 `base`（`ImBaseEventData`）和一个 `content`：

| `ImBaseEventData` 字段 | 说明 |
| --- | --- |
| `sid` | 会话 ID |
| `uid` | 发送者用户 ID |
| `name` | 发送者昵称 |
| `avatar` | 发送者头像 |

#### 有人呼叫你

```swift
func meeting(_ meeting: SMeeting, imCallCalling data: ImCallCallingEventData) {
    // data.base.name 呼叫者
    // data.content.roomNo / data.content.meetingId / data.content.title
    // 展示来电界面，用户接听后调用 enterRoom 进入
}
```

#### 会议提醒

```swift
func meeting(_ meeting: SMeeting, imMeetingRemind data: ImMeetingRemindEventData) {
    // data.content.title / creatorName / planTime / planDur
}
```

#### 被放行出等候室

```swift
func meeting(_ meeting: SMeeting, imAdminMoveOutWaitingRoom data: ImAdminMoveOutWaitingRoomEventData) {
    // data.content.meetingId 目标会议，可据此进入
}
```

#### 小组请求协助

```swift
func meeting(_ meeting: SMeeting, imUserHelpSubMeeting data: ImUserHelpSubMeetingEventData) {
    // data.content.meetingId / title 求助的小组
    // data.content.parent 主会议 ID
}
```

---

### 连接状态

这条通道有自己独立的连接状态事件，不要和会议的重连事件混淆：

| 事件 | 说明 |
| --- | --- |
| `meetingImIsReconnecting(_:)` | 消息通道开始重连 |
| `meetingImDidReconnect(_:)` | 消息通道重连成功 |
| `meeting(_:imDidDisconnect:)` | 消息通道断开，`data.reason` 为原因描述 |

对应会议本身的连接事件是 `meetingIsReconnecting(_:)` / `meetingDidReconnect(_:)` / `meeting(_:didDisconnect:)`。

---

### 相关页面

+ [会中消息](/zh/meeting/swift/advanced/messaging)
+ [等候室](/zh/meeting/swift/advanced/waiting-room)
+ [分组讨论](/zh/meeting/swift/advanced/sub-meetings)
