---
title: "UserEvent"
description: "Android SMeeting 会议 SDK UserEvent 接口参考"
---

说明：`UserEvent` 是房间内用户事件回调接口，用于接收成员进退会、角色与设备状态变化及会控请求事件。

## 回调方法

### onExitRoom(reason)
```kotlin
fun onExitRoom(reason: LeaveMeetingReason)
```
方法说明：离开会议事件回调。  
参数说明：
- `reason`：`LeaveMeetingReason`，离会原因。
返回值说明：无（`Unit`）。

### onUserEnter(uid)
```kotlin
fun onUserEnter(uid: String)
```
方法说明：远端用户进房事件。  
参数说明：
- `uid`：`String`，远端用户 uid。
返回值说明：无（`Unit`）。

### onUserExit(userInfo)
```kotlin
fun onUserExit(userInfo: UserInfo)
```
方法说明：远端用户离开房间事件。  
参数说明：
- `userInfo`：`UserInfo`，离会用户信息。
返回值说明：无（`Unit`）。

### onUserNameChanged(targetUid, nick)
```kotlin
fun onUserNameChanged(targetUid: String, nick: String)
```
方法说明：用户昵称变化事件（所有成员收到）。  
参数说明：
- `targetUid`：`String`，目标用户 uid。
- `nick`：`String`，新昵称。
返回值说明：无（`Unit`）。

### onUserRoleChanged(targetUid, roleType)
```kotlin
fun onUserRoleChanged(targetUid: String, roleType: MemberRoleType)
```
方法说明：用户角色变化事件。  
参数说明：
- `targetUid`：`String`，目标用户 uid。
- `roleType`：`MemberRoleType`，成员角色类型。
返回值说明：无（`Unit`）。

### onUserCameraStateChanged(targetUid, cameraState, reason)
```kotlin
fun onUserCameraStateChanged(targetUid: String, cameraState: DeviceState, reason: ChangeReason)
```
方法说明：用户摄像头状态变化事件。  
参数说明：
- `targetUid`：`String`，目标用户 uid。
- `cameraState`：`DeviceState`，摄像头状态。
- `reason`：`ChangeReason`，状态变更原因。
返回值说明：无（`Unit`）。

### onUserMicStateChanged(targetUid, micState, reason)
```kotlin
fun onUserMicStateChanged(targetUid: String, micState: DeviceState, reason: ChangeReason)
```
方法说明：用户麦克风状态变化事件。  
参数说明：
- `targetUid`：`String`，目标用户 uid。
- `micState`：`DeviceState`，麦克风状态。
- `reason`：`ChangeReason`，状态变更原因。
返回值说明：无（`Unit`）。

### onUserDrawDisabledChange(operatorUid, targetUid, disabled)
```kotlin
fun onUserDrawDisabledChange(operatorUid: String, targetUid: String, disabled: Boolean)
```
方法说明：用户涂鸦禁用状态变化事件。  
参数说明：
- `operatorUid`：`String`，操作者 uid。
- `targetUid`：`String`，目标用户 uid。
- `disabled`：`Boolean`，禁用状态。
返回值说明：无（`Unit`）。

### onUserChatDisabledChange(operatorUid, disabled)
```kotlin
fun onUserChatDisabledChange(operatorUid: String, disabled: Boolean)
```
方法说明：用户聊天能力禁用状态变化事件。  
参数说明：
- `operatorUid`：`String`，操作者 uid。
- `disabled`：`Boolean`，禁用状态。
返回值说明：无（`Unit`）。

### onHandUpConfirm(operatorUid, targetUid, approve, handupType)
```kotlin
fun onHandUpConfirm(operatorUid: String, targetUid: String, approve: Boolean, handupType: HandUpType)
```
方法说明：举手处理结果回调。  
参数说明：
- `operatorUid`：`String`，处理人 uid。
- `targetUid`：`String`，被处理人 uid。
- `approve`：`Boolean`，处理结果。
- `handupType`：`HandUpType`，申请类型。
返回值说明：无（`Unit`）。

### onRequestOpenCamera(operatorUid)
```kotlin
fun onRequestOpenCamera(operatorUid: String)
```
方法说明：请求打开摄像头事件。  
参数说明：
- `operatorUid`：`String`，请求者 uid。
返回值说明：无（`Unit`）。

### onRequestOpenMic(operatorUid)
```kotlin
fun onRequestOpenMic(operatorUid: String)
```
方法说明：请求打开麦克风事件。  
参数说明：
- `operatorUid`：`String`，请求者 uid。
返回值说明：无（`Unit`）。

### onRequestStartShare(operatorUid)
```kotlin
fun onRequestStartShare(operatorUid: String)
```
方法说明：请求开始屏幕共享事件。  
参数说明：
- `operatorUid`：`String`，请求者 uid。
返回值说明：无（`Unit`）。

### onUserConfirmOpenCamera(operatorUid, approve)
```kotlin
fun onUserConfirmOpenCamera(operatorUid: String, approve: Boolean)
```
方法说明：用户回复打开摄像头请求事件。  
参数说明：
- `operatorUid`：`String`，响应者 uid。
- `approve`：`Boolean`，是否同意。
返回值说明：无（`Unit`）。

### onUserConfirmOpenMic(operatorUid, approve)
```kotlin
fun onUserConfirmOpenMic(operatorUid: String, approve: Boolean)
```
方法说明：用户回复打开麦克风请求事件。  
参数说明：
- `operatorUid`：`String`，响应者 uid。
- `approve`：`Boolean`，是否同意。
返回值说明：无（`Unit`）。

### onMoveInWaitingRoom(operatorUid, nickName)
```kotlin
fun onMoveInWaitingRoom(operatorUid: String, nickName: String)
```
方法说明：用户被从会议移入等候室事件。  
参数说明：
- `operatorUid`：`String`，操作者 uid。
- `nickName`：`String`，相关用户昵称。
返回值说明：无（`Unit`）。

### onUserEnterWaitingRoom(uid, nickName)
```kotlin
fun onUserEnterWaitingRoom(uid: String, nickName: String)
```
方法说明：用户进入等候室事件（仅主持人收到）。  
参数说明：
- `uid`：`String`，用户 uid。
- `nickName`：`String`，用户昵称。
返回值说明：无（`Unit`）。

### onUserExitWaitingRoom(uid, nickName)
```kotlin
fun onUserExitWaitingRoom(uid: String, nickName: String)
```
方法说明：用户离开等候室事件（仅主持人收到）。  
参数说明：
- `uid`：`String`，用户 uid。
- `nickName`：`String`，用户昵称。
返回值说明：无（`Unit`）。

### onRequestMoveToMainMeetOrSubMeet(targetMeetingId, targetMeetingTitle)
```kotlin
fun onRequestMoveToMainMeetOrSubMeet(targetMeetingId: String, targetMeetingTitle: String)
```
方法说明：主持人将成员移动到主会场或子会场事件。  
参数说明：
- `targetMeetingId`：`String`，目标会议 id。
- `targetMeetingTitle`：`String`，目标会议标题。
返回值说明：无（`Unit`）。
