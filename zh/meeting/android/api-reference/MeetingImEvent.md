---
title: "MeetingImEvent"
description: "接收 Meeting IM 连接、重连、原始消息、呼叫、会议提醒、等候室与讨论组求助事件"
---

`MeetingImEvent` 接收与 Engine 中 IM 连接同生命周期的持续状态和业务消息，通过 `MeetingEngine.imEvent` 注册。可继承 `MeetingImSimpleEvent` 按需覆写。

## 特殊说明

IM 连接独立于当前会议 Session；会议提醒、等候室和讨论组求助等会外消息也从该接口分发。

## 注意事项

+ 先调用 `enableIm()` 建立连接；`disableIm()` 或 `release()` 导致的主动断开不会触发 `onImDisconnected()`。
+ 回调保持 IM 实际来源线程，更新 UI 前应切换到主线程。

## 接口方法

### onImConnected(uid, sid)

```kotlin
fun onImConnected(uid: String, sid: String)
```

方法说明：IM 首次建立连接。

参数说明：

+ `uid`：当前用户 IM UID。
+ `sid`：本次 IM 会话标识。

返回值说明：无（`Unit`）。

### onImDisconnected(reason, statusCode, message)

```kotlin
fun onImDisconnected(reason: LeaveReason, statusCode: Int, message: String?)
```

方法说明：IM 非主动断开。

参数说明：

+ `reason`：SRTC 定义的断开原因。
+ `statusCode`：底层状态码。
+ `message`：可空诊断信息。

返回值说明：无（`Unit`）。

### onImReconnecting()

```kotlin
fun onImReconnecting()
```

方法说明：IM 断开后开始自动重连。

参数说明：无。

返回值说明：无（`Unit`）。

### onImReconnected()

```kotlin
fun onImReconnected()
```

方法说明：IM 自动重连成功。

参数说明：无。

返回值说明：无（`Unit`）。

### onImMessage(uid, sid, name, action, content)

```kotlin
fun onImMessage(
    uid: String,
    sid: String,
    name: String,
    action: String,
    content: String
)
```

方法说明：接收未被 Meeting 解析为专用业务事件的原始 IM 消息。

参数说明：

+ `uid`：发送者 UID。
+ `sid`：消息所属会话标识。
+ `name`：发送者昵称。
+ `action`：消息动作名。
+ `content`：原始消息内容。

返回值说明：无（`Unit`）。

### onCallReceived(uid, nickname, callingMsg)

```kotlin
fun onCallReceived(
    uid: String,
    nickname: String,
    callingMsg: ImContent.CallingMsg
)
```

方法说明：收到会议通话邀请。

参数说明：

+ `uid`：邀请方 UID。
+ `nickname`：邀请方昵称。
+ `callingMsg`：目标会议 ID、房间号与标题。

返回值说明：无（`Unit`）。

### onMeetingRemind(uid, meetingRemind)

```kotlin
fun onMeetingRemind(uid: String, meetingRemind: ImContent.MeetingRemind)
```

方法说明：收到预约会议提醒。

参数说明：

+ `uid`：消息发送方 UID。
+ `meetingRemind`：会议与创建者、计划时间信息。

返回值说明：无（`Unit`）。

### onMoveOutWaitingRoom(uid, moveOutWaitingRoom)

```kotlin
fun onMoveOutWaitingRoom(
    uid: String,
    moveOutWaitingRoom: ImContent.MoveOutWaitingRoom
)
```

方法说明：当前用户被主持人从等候室移入会议。

参数说明：

+ `uid`：消息发送方 UID。
+ `moveOutWaitingRoom`：目标会议 ID 与标题。

返回值说明：无（`Unit`）。

### onUserHelpSubMeeting(uid, userHelpSubMeeting)

```kotlin
fun onUserHelpSubMeeting(
    uid: String,
    userHelpSubMeeting: ImContent.UserHelpSubMeeting
)
```

方法说明：收到讨论组成员发出的求助消息。

参数说明：

+ `uid`：求助成员 UID。
+ `userHelpSubMeeting`：主会议、子会议和讨论组标题信息。

返回值说明：无（`Unit`）。
