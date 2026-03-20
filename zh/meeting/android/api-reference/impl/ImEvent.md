---
title: "ImEvent"
description: "Android SMeeting 会议 SDK ImEvent 接口参考"
---

说明：`ImEvent` 是即时通讯事件回调接口，用于接收 IM 连接状态、错误与业务消息事件。

## 回调方法

### onImDisconnected(reason)
```kotlin
fun onImDisconnected(reason: DisconnectedImReason)
```
方法说明：即时通讯断开连接回调。  
参数说明：
- `reason`：`DisconnectedImReason`，即时通讯断开原因。
返回值说明：无（`Unit`）。

### onError(errorCode, errorMsg)
```kotlin
fun onError(errorCode: Int, errorMsg: String)
```
方法说明：即时通讯出现不可恢复错误回调。  
参数说明：
- `errorCode`：`Int`，错误码。
- `errorMsg`：`String`，错误信息。
返回值说明：无（`Unit`）。

### onImReconnecting()
```kotlin
fun onImReconnecting()
```
方法说明：即时通讯断开后正在重连回调。  
参数说明：无。  
返回值说明：无（`Unit`）。

### onImReconnected()
```kotlin
fun onImReconnected()
```
方法说明：即时通讯重连成功回调。  
参数说明：无。  
返回值说明：无（`Unit`）。

### onImMessage(uid, sid, name, action, content)
```kotlin
fun onImMessage(uid: String, sid: String, name: String, action: String, content: String)
```
方法说明：即时通讯接收消息回调。  
参数说明：
- `uid`：`String`，发送者 uid。
- `sid`：`String`，发送者 sid。
- `name`：`String`，发送者昵称。
- `action`：`String`，消息标识。
- `content`：`String`，消息内容。
返回值说明：无（`Unit`）。

### onCallReceived(uid, nickname, callingMsg)
```kotlin
fun onCallReceived(uid: String, nickname: String, callingMsg: ImContent.CallingMsg)
```
方法说明：通话请求回调。  
参数说明：
- `uid`：`String`，发送者 uid。
- `nickname`：`String`，发送者昵称。
- `callingMsg`：`ImContent.CallingMsg`，通话请求消息体。
返回值说明：无（`Unit`）。

### onMeetingRemind(uid, meetingRemind)
```kotlin
fun onMeetingRemind(uid: String, meetingRemind: ImContent.MeetingRemind)
```
方法说明：会议提醒回调。  
参数说明：
- `uid`：`String`，发送者 uid。
- `meetingRemind`：`ImContent.MeetingRemind`，会议提醒消息体。
返回值说明：无（`Unit`）。

### onMoveOutWaitingRoom(uid, moveOutWaitingRoom)
```kotlin
fun onMoveOutWaitingRoom(uid: String, moveOutWaitingRoom: ImContent.MoveOutWaitingRoom)
```
方法说明：成员被从等候室移入会议回调。  
参数说明：
- `uid`：`String`，发送者 uid。
- `moveOutWaitingRoom`：`ImContent.MoveOutWaitingRoom`，等候室移入会议消息体。
返回值说明：无（`Unit`）。

### onUserHelpSubMeeting(uid, userHelpSubMeeting)
```kotlin
fun onUserHelpSubMeeting(uid: String, userHelpSubMeeting: ImContent.UserHelpSubMeeting)
```
方法说明：小组请求帮助回调。  
参数说明：
- `uid`：`String`，发送者 uid。
- `userHelpSubMeeting`：`ImContent.UserHelpSubMeeting`，小组请求帮助消息体。
返回值说明：无（`Unit`）。
