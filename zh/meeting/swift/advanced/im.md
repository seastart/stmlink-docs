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
+ `enableIm()` 成功后会触发一次 `meeting(_:imDidConnect:)`，带本端 `uid` 与 IM 会话 `sid`（1.5.0 起）
+ 主动调用 `disableIm()` 不会触发 `imDidDisconnect`

<Note>
1.4.1 及以前，`enableIm()` 只建立了通道，下面的呼叫、提醒、等候室放行、小组求助事件以及重连 / 断开回调实际都不会派发。依赖这些事件的接入需要升级到 1.5.0。
</Note>

典型接入位置是登录成功之后：

```swift
try await meeting.login(token: token)
meeting.delegates.add(delegate: self)
try await meeting.enableIm()
```

---

### 事件

下面四个业务事件都带一个 `base`（`ImBaseEventData`）和一个 `content`：

| `ImBaseEventData` 字段 | 说明 |
| --- | --- |
| `sid` | 会话 ID |
| `uid` | 发送者用户 ID |
| `name` | 发送者昵称 |
| `avatar` | 发送者头像 |

#### 有人呼叫你

```swift
func meeting(_ meeting: SMeetingEngine, imCallCalling data: ImCallCallingEventData) {
    // data.base.name 呼叫者
    // data.content.roomNo / data.content.meetingId / data.content.title
    // 展示来电界面，用户接听后调用 enterRoom 进入
}
```

#### 会议提醒

```swift
func meeting(_ meeting: SMeetingEngine, imMeetingRemind data: ImMeetingRemindEventData) {
    // data.content.title / creatorName / planTime / planDur
    // data.content.creatorId 创建者用户 ID（1.5.0 起）
}
```

`planTime` 为秒级时间戳，`planDur` 单位为分钟。

#### 被放行出等候室

```swift
func meeting(_ meeting: SMeetingEngine, imAdminMoveOutWaitingRoom data: ImAdminMoveOutWaitingRoomEventData) {
    // data.content.meetingId 目标会议，可据此进入
}
```

#### 小组请求协助

```swift
func meeting(_ meeting: SMeetingEngine, imUserHelpSubMeeting data: ImUserHelpSubMeetingEventData) {
    // data.content.meetingId / title 求助的小组
    // data.content.parent 主会议 ID
}
```

#### 原始消息

每条会议外消息都会先原样触发一次 `imDidReceiveMessage`，SDK 认识的 action 再额外派发到上面的具名事件（1.5.0 起）。业务自定义的 action 只能从这里拿到：

```swift
func meeting(_ meeting: SMeetingEngine, imDidReceiveMessage data: ImMessageEventData) {
    // data.action  消息命令，例如 call_calling
    // data.content 消息内容，通常是 JSON 字符串，需要自行解析
    // data.sid / data.uid / data.name 发送者
}
```

同一条已知消息会先后收到原始与具名两次回调，不要两边都处理。

---

### 连接状态

这条通道有自己独立的连接状态事件，不要和会议的重连事件混淆：

| 事件 | 说明 |
| --- | --- |
| `meeting(_:imDidConnect:)` | `enableIm()` 成功后触发一次，`data.uid` / `data.sid` 为本端用户 ID 与 IM 会话 ID（1.5.0 起） |
| `meetingImIsReconnecting(_:)` | 消息通道开始重连 |
| `meetingImDidReconnect(_:)` | 消息通道重连成功（不会再触发 `imDidConnect`） |
| `meeting(_:imDidDisconnect:)` | 消息通道被动断开（被踢、心跳超时、后端报错），`data.reason` 为原因描述 |

`ImDisconnectEventData` 自 1.5.0 起另带结构化原因：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `reason` | `String?` | 原因的文字描述：有错误时为错误描述，否则为 `disconnectReason` 的名字 |
| `disconnectReason` | `ImDisconnectReason` | 断开原因（定义在 SRTC，需要 `import SRTC`） |
| `errorCode` | `Int?` | 导致断开的错误码，无错误为 `nil` |
| `errorMessage` | `String?` | 导致断开的错误描述，无错误为 `nil` |

被动断开后通道已失效，需要时重新调用 `enableIm()`。

对应会议本身的连接事件是 `meetingIsReconnecting(_:)` / `meetingDidReconnect(_:)` / `meeting(_:didDisconnect:)`。

---

### 相关页面

+ [会中消息](/zh/meeting/swift/advanced/messaging)
+ [等候室](/zh/meeting/swift/advanced/waiting-room)
+ [分组讨论](/zh/meeting/swift/advanced/sub-meetings)
