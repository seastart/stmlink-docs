---
title: "事件参考"
description: "SMeeting Swift SDK 中 SMeetingDelegate 的全部事件、触发时机与数据类型"
---

### 注册与注销

所有会议事件都通过 `SMeetingDelegate` 上报：

```swift
final class MeetingController: SMeetingDelegate {
    init(meeting: SMeetingEngine) {
        meeting.delegates.add(delegate: self)
    }

    func meeting(_ meeting: SMeetingEngine, userDidEnter user: MeetingUserInfo) {
        print("成员进入:", user.name)
    }
}
```

要点：

+ `delegates` 是**弱引用多播**，可以注册多个观察者，SDK 不会因为注册而延长你的对象生命周期
+ 协议里所有方法都有默认空实现，只实现关心的事件即可
+ 不再需要时调用 `meeting.delegates.remove(delegate:)`
+ 回调统一在**主线程**派发，可以直接更新 UI

如果你的观察者是 `@MainActor` 类型，协议方法需要声明为 `nonisolated`，再在里面回到主 actor 上下文：

```swift
extension MeetingController: SMeetingDelegate {
    nonisolated func meeting(_ meeting: SMeetingEngine, userDidExit data: UserExitEventData) {
        DispatchQueue.main.async { self.users = meeting.getUsersInfoList() }
    }
}
```

---

### 连接事件

| 方法 | 触发时机 | 数据类型 |
| --- | --- | --- |
| `meetingIsReconnecting(_:)` | 会议连接中断，开始自动重连 | 无 |
| `meetingDidReconnect(_:)` | 重连成功 | 无 |
| `meeting(_:didDisconnect:)` | 自己被断开：主动退会、被移出、会议结束、超时等 | `DisconnectEventData` |

`DisconnectEventData` 的 `reason` 是 `DisconnectReason`，可据此区分是自己走的还是被动断开；`error` 在异常断开时携带底层错误。

---

### 成员事件

| 方法 | 触发时机 | 数据类型 |
| --- | --- | --- |
| `meeting(_:userDidEnter:)` | 其他成员进入会议 | `MeetingUserInfo` |
| `meeting(_:userDidExit:)` | 成员离开会议 | `UserExitEventData` |
| `meeting(_:userCameraStateDidChange:)` | 任一成员（含自己）摄像头开 / 关 | `UserCameraStateChangeEventData` |
| `meeting(_:userMicStateDidChange:)` | 任一成员（含自己）麦克风开 / 关 | `UserMicStateChangeEventData` |
| `meeting(_:userNameDidChange:)` | 成员会中昵称变化 | `UserNameChangeEventData` |
| `meeting(_:userRoleDidChange:)` | 成员角色变化，含主持人转移 | `UserRoleChangeEventData` |
| `meeting(_:userChatDisabledDidChange:)` | 成员被单独禁言 / 解除 | `UserChatDisabledChangeEventData` |
| `meeting(_:userDidHandup:)` | 成员举手、取消举手，或响应了主持人的开启邀请 | `UserHandupEventData` |

媒体状态事件里的 `byAdmin` 为 `true` 时表示这次变化是主持人操作导致的，`opUid` 是操作者。你可以据此给用户一个「已被主持人关闭麦克风」这类提示。

`UserHandupEventData.step` 区分是哪一步：`.request` 举手、`.cancel` 取消、`.confirmOpen` 同意邀请、`.rejectOpen` 拒绝邀请。

---

### 房间状态事件

| 方法 | 触发时机 | 数据类型 |
| --- | --- | --- |
| `meeting(_:roomMicStateDidChange:)` | 全体静音设置变化 | `RoomMicStateChangeEventData` |
| `meeting(_:roomCameraStateDidChange:)` | 全体禁画设置变化 | `RoomCameraStateChangeEventData` |
| `meeting(_:roomShareStateDidChange:)` | 禁止共享设置变化 | `RoomShareStateChangeEventData` |
| `meeting(_:roomChatDisabledDidChange:)` | 全体禁言设置变化 | `RoomChatDisabledChangeEventData` |
| `meeting(_:roomScreenshotDisabledDidChange:)` | 禁止截屏设置变化 | `RoomScreenshotDisabledChangeEventData` |
| `meeting(_:roomWatermarkDisabledDidChange:)` | 水印开关变化 | `RoomWatermarkDisabledChangeEventData` |
| `meeting(_:roomLockedDidChange:)` | 会议锁定状态变化 | `RoomLockedChangeEventData` |
| `meeting(_:roomShareDidStart:)` | 有人开始共享（屏幕或白板） | `RoomShareStartEventData` |
| `meeting(_:roomShareDidStop:)` | 共享结束 | `RoomShareStopEventData` |
| `meeting(_:roomMcuTask:)` | 录制 / 合流任务状态变化 | `RoomMcuTaskEventData` |
| `meeting(_:roomJoinDidFail:)` | 有成员入会失败 | `RoomJoinFailedEventData` |

屏幕共享的 `roomShareDidStart` 会在共享广播和远端画面两个条件都满足后才上报，收到时可以直接渲染共享画面。

当主持人开启「全体静音」或「全体禁画」时，非主持人成员的本地设备会被 SDK 自动关闭，并额外上报一次对应的成员媒体状态事件。

---

### 消息事件

| 方法 | 触发时机 | 数据类型 |
| --- | --- | --- |
| `meeting(_:didReceiveChatMessage:)` | 收到会中聊天消息 | `RoomChatMsgEventData` |
| `meeting(_:didReceiveCustomMessage:)` | 收到业务自定义消息 | `RoomCustomMsgEventData` |

两者都有 `isPrivate` 标记是否为私聊，`uid` 是发送者。

---

### 主持人指令事件

| 方法 | 触发时机 | 数据类型 |
| --- | --- | --- |
| `meeting(_:adminDidConfirmHandup:)` | 主持人处理了举手申请 | `AdminConfirmHandupEventData` |
| `meeting(_:adminDidRequestOpenMic:)` | 主持人邀请你开麦 | `AdminRequestOpenMicEventData` |
| `meeting(_:adminDidRequestOpenCamera:)` | 主持人邀请你开摄像头 | `AdminRequestOpenCameraEventData` |

处理方式见 [举手与开启请求](/zh/meeting/swift/advanced/handup)。

---

### 等候室事件

| 方法 | 触发时机 | 数据类型 |
| --- | --- | --- |
| `meeting(_:userDidEnterWaitingRoom:)` | 有人进入等候室 | `UserEnterWaitingRoomEventData` |
| `meeting(_:userDidExitWaitingRoom:)` | 有人离开等候室 | `UserExitWaitingRoomEventData` |
| `meeting(_:waitingRoomDisabledDidChange:)` | 等候室开关变化 | `AdminUpdateWaitingRoomDisabledEventData` |
| `meetingDidMoveToWaitingRoom(_:)` | 自己被主持人移回等候室 | 无 |

---

### 分组讨论事件

| 方法 | 触发时机 | 数据类型 |
| --- | --- | --- |
| `meeting(_:adminDidStartSubMeeting:)` | 主持人开始了分组讨论 | `AdminStartSubMeetingEventData` |
| `meeting(_:adminDidStopSubMeeting:)` | 主持人结束了分组讨论 | `AdminStopSubMeetingEventData` |
| `meeting(_:adminDidMoveSubMeetingUser:)` | 你被移动到另一个小组 | `AdminMoveSubMeetingUserEventData` |

这三个事件都需要你自行完成「退出当前会议、进入目标会议」的切换。

---

### 签到与点名事件

| 方法 | 触发时机 | 数据类型 |
| --- | --- | --- |
| `meeting(_:signInActivity:)` | 主持人发起了一轮签到 | `SignInActivityEventData` |
| `meeting(_:signInDidFinish:)` | 签到活动结束 | `SignInFinishEventData` |
| `meeting(_:rollCallNamed:)` | 你被点名 | `RollCallNamedEventData` |

---

### 外设事件

| 方法 | 触发时机 | 数据类型 |
| --- | --- | --- |
| `meeting(_:didAddDevice:)` | 系统接入了摄像头 / 麦克风 / 扬声器，或 iOS 音频路由新增 | `DeviceChangeEventData` |
| `meeting(_:didRemoveDevice:)` | 设备被移除 | `DeviceChangeEventData` |

外设事件**不依赖会议状态**，SDK 实例创建后就开始上报，可用于入会前的设备检测页面。

---

### 会议外消息事件

需要先调用 `enableIm()`，见 [会议外消息](/zh/meeting/swift/advanced/im)。

| 方法 | 触发时机 | 数据类型 |
| --- | --- | --- |
| `meeting(_:imCallCalling:)` | 有人在会议里呼叫你 | `ImCallCallingEventData` |
| `meeting(_:imMeetingRemind:)` | 会议开始提醒 | `ImMeetingRemindEventData` |
| `meeting(_:imAdminMoveOutWaitingRoom:)` | 你被放行出等候室 | `ImAdminMoveOutWaitingRoomEventData` |
| `meeting(_:imUserHelpSubMeeting:)` | 有小组请求协助 | `ImUserHelpSubMeetingEventData` |
| `meetingImIsReconnecting(_:)` | 会议外消息通道开始重连 | 无 |
| `meetingImDidReconnect(_:)` | 会议外消息通道重连成功 | 无 |
| `meeting(_:imDidDisconnect:)` | 会议外消息通道断开 | `ImDisconnectEventData` |

这几个连接事件与前面的会议连接事件是两条独立通道，不要混用。

---

### 事件标识枚举

SDK 另外公开了两个枚举，列出各事件的字符串标识：

+ `RoomEventType` —— 会议内事件标识，例如 `user_enter`、`room_share_start`
+ `ImEventType` —— 会议外消息事件标识，例如 `call_calling`

Swift 侧的事件分发走上面的 `SMeetingDelegate` 方法，这两个枚举在正常接入中用不到，只在你需要做日志埋点或与其它端对齐事件命名时才有用。

---

### 相关页面

+ [核心概念](/zh/meeting/swift/key-concepts)
+ [类型定义](/zh/meeting/swift/types)
+ [错误处理](/zh/meeting/swift/error-codes)
