---
title: "会中消息"
description: "SMeeting Swift SDK 的会中聊天消息、自定义消息发送与接收，以及禁言控制"
---

### 概述

会议内有两种消息，都只在会议期间有效：

| 类型 | 发送 | 接收事件 | 适用场景 |
| --- | --- | --- | --- |
| 聊天消息 | `sendRoomChatMessage(_:type:targetId:)` | `meeting(_:didReceiveChatMessage:)` | 面向用户展示的聊天内容 |
| 自定义消息 | `sendRoomCustomMessage(_:targetId:)` | `meeting(_:didReceiveCustomMessage:)` | 业务自定义信令，例如举牌、投票、状态同步 |

两者都支持群发和私聊：`targetId` 传 `nil` 时是群发，传某位成员的 `uid` 时是私聊。

> 未在会议中调用会抛出 `SMeetingError.notInMeeting`。

---

### 发送聊天消息

```swift
// 群发文本
try await meeting.sendRoomChatMessage("大家好")

// 私聊
try await meeting.sendRoomChatMessage("单独说一句", targetId: user.uid)

// 非文本消息：先把文件上传到你们的存储，再把地址作为消息内容发出去
try await meeting.sendRoomChatMessage(imageURL, type: .pic)
```

`ChatMsgType` 可选值：`.text`（默认）、`.file`、`.pic`、`.sound`。SDK 不负责文件本身的上传与下载，只负责传递这条消息内容，具体渲染由你的 UI 决定。

---

### 接收聊天消息

```swift
func meeting(_ meeting: SMeetingEngine, didReceiveChatMessage data: RoomChatMsgEventData) {
    // data.msgType 消息类型
    // data.msg     消息内容
    // data.uid     发送者（可能为 nil）
    // data.isPrivate 是否私聊
}
```

发送者昵称不在事件里，需要用 `uid` 去成员列表查：

```swift
let name = meeting.getUsersInfo()[data.uid ?? ""]?.name ?? data.uid ?? ""
```

如果你在发送成功后就立刻本地回显了这条消息，请用 `data.uid` 与 `meeting.currentUserId` 比较做一次去重，避免同一条消息显示两遍。

---

### 自定义消息

自定义消息的内容是一个字符串，通常放你自己的 JSON：

```swift
struct VotePayload: Codable {
    let action: String
    let optionId: String
}

let payload = VotePayload(action: "vote", optionId: "A")
let json = String(data: try JSONEncoder().encode(payload), encoding: .utf8) ?? ""
try await meeting.sendRoomCustomMessage(json)
```

接收：

```swift
func meeting(_ meeting: SMeetingEngine, didReceiveCustomMessage data: RoomCustomMsgEventData) {
    guard let json = data.msg.data(using: .utf8),
          let payload = try? JSONDecoder().decode(VotePayload.self, from: json) else { return }
    // 处理业务信令
}
```

> 自定义消息是给业务用的通道，SDK 自身的会议信令走独立链路，你的消息内容不会和 SDK 冲突。

---

### 禁言

禁言分房间级和成员级，都由主持人 / 联席主持人设置。

#### 房间级

```swift
try await meeting.adminUpdateRoomChatDisabled(true)
```

当前状态读 `RoomInfo.chatDisabled`，变化时收到：

```swift
func meeting(_ meeting: SMeetingEngine, roomChatDisabledDidChange data: RoomChatDisabledChangeEventData) {
    // data.chatDisabled、data.opUid
}
```

#### 成员级

```swift
try await meeting.adminUpdateUserChatDisabled(targetId: user.uid, chatDisabled: true)
```

当前状态读 `MeetingUserInfo.chatDisabled`，变化时收到：

```swift
func meeting(_ meeting: SMeetingEngine, userChatDisabledDidChange data: UserChatDisabledChangeEventData) {
    // data.uid、data.chatDisabled、data.opUid
}
```

建议在 UI 上根据这两个状态直接禁用输入框，而不是等发送失败再提示。

---

### 相关页面

+ [举手与开启请求](/zh/meeting/swift/advanced/handup)
+ [主持人管控](/zh/meeting/swift/advanced/host-controls)
+ [会议外消息](/zh/meeting/swift/advanced/im)
