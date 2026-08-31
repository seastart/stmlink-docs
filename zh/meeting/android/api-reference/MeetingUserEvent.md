---
title: "MeetingUserEvent"
description: "接收当前会议成员进出、角色与权限、设备状态、请求确认、等候室、会场移动和轨道变化"
---

`MeetingUserEvent` 承载当前会议的成员、成员权限和成员轨道事件，通过 `MeetingEngine.userEvent` 注册。可继承 `MeetingUserSimpleEvent` 按需覆写。

## 特殊说明

事件参数优先提供发生变化的成员 UID 和增量状态；需要完整成员或轨道快照时通过 `MeetingEngine.infosManager` 查询。

## 注意事项

+ 监听可在入会前赋值，离会后会被清除。
+ `onUserEnter()` 只提供 UID；需要完整信息时再通过 `MeetingEngine.infosManager.getMemberByUid(uid)` 查询。
+ 观众不进入正式成员列表，身份变化通过 `onMeMembershipChanged()` 通知。

## 成员生命周期

### onExitRoom(reason)

```kotlin
fun onExitRoom(reason: LeaveMeetingReason)
```

方法说明：当前用户因被踢、被替换、心跳超时或频道销毁等原因退出会议。

参数说明：

+ `reason`：Meeting 映射后的离会原因。

返回值说明：无（`Unit`）。

### onUserEnter(uid)

```kotlin
fun onUserEnter(uid: String)
```

方法说明：远端用户进入当前会议。

参数说明：

+ `uid`：新进入用户 UID。

返回值说明：无（`Unit`）。

### onUserExit(memberInfo)

```kotlin
fun onUserExit(memberInfo: MemberInfo)
```

方法说明：远端用户离开当前会议。

参数说明：

+ `memberInfo`：离开用户最后一次可用的 Meeting 成员快照。

返回值说明：无（`Unit`）。

### onMemberUpdated(memberInfo)

```kotlin
fun onMemberUpdated(memberInfo: MemberInfo)
```

方法说明：指定成员的 Meeting 信息刷新。

参数说明：

+ `memberInfo`：更新后的成员快照。

返回值说明：无（`Unit`）。

### onUserNameChanged(targetUid, nickname)

```kotlin
fun onUserNameChanged(targetUid: String, nickname: String)
```

方法说明：成员昵称变化。

参数说明：`targetUid` 为目标成员 UID，`nickname` 为新昵称。

返回值说明：无（`Unit`）。

### onUserRoleChanged(targetUid, roleType)

```kotlin
fun onUserRoleChanged(targetUid: String, roleType: MemberRoleType)
```

方法说明：成员角色变化。

参数说明：`targetUid` 为目标成员 UID，`roleType` 为新角色。

返回值说明：无（`Unit`）。

### onMeMembershipChanged(isMember)

```kotlin
fun onMeMembershipChanged(isMember: Boolean)
```

方法说明：当前用户的正式成员或观众身份变化。

参数说明：

+ `isMember`：`true` 表示正式成员，`false` 表示观众。

返回值说明：无（`Unit`）。

## 设备与权限

### onUserCameraStateChanged(targetUid, cameraState, reason)

```kotlin
fun onUserCameraStateChanged(
    targetUid: String,
    cameraState: DeviceState,
    reason: ChangeReason
)
```

方法说明：成员摄像头状态变化。

参数说明：

+ `targetUid`：目标成员 UID。
+ `cameraState`：打开或关闭状态。
+ `reason`：成员自行操作或主持人操作。

返回值说明：无（`Unit`）。

### onUserMicStateChanged(targetUid, micState, reason)

```kotlin
fun onUserMicStateChanged(
    targetUid: String,
    micState: DeviceState,
    reason: ChangeReason
)
```

方法说明：成员麦克风状态变化。

参数说明：`targetUid` 为目标成员 UID，`micState` 为打开或关闭状态，`reason` 为变化原因。

返回值说明：无（`Unit`）。

### onUserDrawDisabledChange(operatorUid, targetUid, disabled)

```kotlin
fun onUserDrawDisabledChange(
    operatorUid: String?,
    targetUid: String?,
    disabled: Boolean?
)
```

方法说明：指定成员的白板涂鸦权限变化。

参数说明：

+ `operatorUid`：可空操作者 UID。
+ `targetUid`：可空目标成员 UID。
+ `disabled`：`true` 禁止涂鸦；无法解析时为 `null`。

返回值说明：无（`Unit`）。

### onUserChatDisabledChange(operatorUid, disabled)

```kotlin
fun onUserChatDisabledChange(operatorUid: String?, disabled: Boolean)
```

方法说明：当前成员聊天权限变化。

参数说明：`operatorUid` 为可空操作者 UID；`disabled=true` 表示禁止聊天。

返回值说明：无（`Unit`）。

### onHandUpConfirm(operatorUid, targetUid, approved, handUpType)

```kotlin
fun onHandUpConfirm(
    operatorUid: String?,
    targetUid: String,
    approved: Boolean,
    handUpType: HandUpType
)
```

方法说明：主持人处理了指定成员的举手申请。

参数说明：

+ `operatorUid`：可空主持人 UID。
+ `targetUid`：申请成员 UID。
+ `approved`：`true` 同意，`false` 拒绝。
+ `handUpType`：举手申请类型。

返回值说明：无（`Unit`）。

## 主持人请求与成员回复

### onRequestOpenCamera(operatorUid)

```kotlin
fun onRequestOpenCamera(operatorUid: String?)
```

方法说明：当前用户收到打开摄像头请求。

参数说明：`operatorUid` 为可空请求方 UID。

返回值说明：无（`Unit`）。使用 `confirmOpenCameraAgree()` / `confirmOpenCameraRefuse()` 回复。

### onRequestOpenMic(operatorUid)

```kotlin
fun onRequestOpenMic(operatorUid: String?)
```

方法说明：当前用户收到打开麦克风请求。

参数说明：`operatorUid` 为可空请求方 UID。

返回值说明：无（`Unit`）。使用 `confirmOpenMicAgree()` / `confirmOpenMicRefuse()` 回复。

### onRequestStartShare(operatorUid)

```kotlin
fun onRequestStartShare(operatorUid: String?)
```

方法说明：当前用户收到开始屏幕共享请求。

参数说明：`operatorUid` 为可空请求方 UID。

返回值说明：无（`Unit`）。使用 `confirmStartScreenShareAgree()` / `confirmStartScreenShareRefuse()` 回复。

### onUserConfirmOpenCamera(operatorUid, approved)

```kotlin
fun onUserConfirmOpenCamera(operatorUid: String, approved: Boolean)
```

方法说明：目标成员回复了打开摄像头请求。

参数说明：`operatorUid` 为回复成员 UID；`approved` 表示是否同意。

返回值说明：无（`Unit`）。

### onUserConfirmOpenMic(operatorUid, approved)

```kotlin
fun onUserConfirmOpenMic(operatorUid: String, approved: Boolean)
```

方法说明：目标成员回复了打开麦克风请求。

参数说明：`operatorUid` 为回复成员 UID；`approved` 表示是否同意。

返回值说明：无（`Unit`）。

## 等候室与会场移动

### onMoveInWaitingRoom(operatorUid, nickname)

```kotlin
fun onMoveInWaitingRoom(operatorUid: String?, nickname: String?)
```

方法说明：当前用户被移入等候室。

参数说明：`operatorUid` 为可空操作者 UID；`nickname` 为可空操作者昵称。

返回值说明：无（`Unit`）。

### onUserEnterWaitingRoom(uid, nickname)

```kotlin
fun onUserEnterWaitingRoom(uid: String, nickname: String)
```

方法说明：等候室中有用户进入。

参数说明：`uid` 为用户 UID，`nickname` 为昵称。

返回值说明：无（`Unit`）。

### onUserExitWaitingRoom(uid, nickname)

```kotlin
fun onUserExitWaitingRoom(uid: String, nickname: String)
```

方法说明：等候室中有用户离开。

参数说明：`uid` 为用户 UID，`nickname` 为昵称。

返回值说明：无（`Unit`）。

### onRequestMoveToMainMeetOrSubMeet(targetMeetingId, targetMeetingTitle)

```kotlin
fun onRequestMoveToMainMeetOrSubMeet(
    targetMeetingId: String?,
    targetMeetingTitle: String?
)
```

方法说明：当前用户被请求移动到主会场或指定讨论组。

参数说明：

+ `targetMeetingId`：可空目标会议 ID。
+ `targetMeetingTitle`：可空目标会议标题。

返回值说明：无（`Unit`）。

## 轨道变化

### onTrackAdded(uid, trackInfo)

```kotlin
fun onTrackAdded(uid: String, trackInfo: TrackInfo)
```

方法说明：远端成员新增一条媒体轨道。

参数说明：`uid` 为成员 UID，`trackInfo` 为新增轨道信息。

返回值说明：无（`Unit`）。

### onTrackUpdated(uid, trackInfo)

```kotlin
fun onTrackUpdated(uid: String, trackInfo: TrackInfo)
```

方法说明：远端成员的一条媒体轨道信息更新。

参数说明：`uid` 为成员 UID，`trackInfo` 为更新后的轨道信息。

返回值说明：无（`Unit`）。

### onTrackRemoved(uid, trackInfo)

```kotlin
fun onTrackRemoved(uid: String, trackInfo: TrackInfo)
```

方法说明：远端成员移除一条媒体轨道。

参数说明：`uid` 为成员 UID，`trackInfo` 为被移除轨道的最后快照。

返回值说明：无（`Unit`）。
