---
title: "RoomEvent"
description: "Android SMeeting 会议 SDK RoomEvent 接口参考"
---

说明：`RoomEvent` 是房间级事件回调接口，用于接收会控能力变化、共享状态、子会议与重连等事件。

## 回调方法

### onRoomCameraStateChanged(operatorUid, selfUnMuteCameraDisabled, disabled)
```kotlin
fun onRoomCameraStateChanged(operatorUid: String, selfUnMuteCameraDisabled: Boolean, disabled: Boolean)
```
方法说明：房间内所有用户摄像头状态能力改变事件。  
参数说明：
- `operatorUid`：`String`，操作者 uid。
- `selfUnMuteCameraDisabled`：`Boolean`，是否允许自我解除禁画状态。
- `disabled`：`Boolean`，房间视频禁用状态。
返回值说明：无（`Unit`）。

### onRoomMicStateChanged(operatorUid, selfUnMuteMicDisabled, disabled)
```kotlin
fun onRoomMicStateChanged(operatorUid: String, selfUnMuteMicDisabled: Boolean, disabled: Boolean)
```
方法说明：房间内所有用户麦克风状态能力改变事件。  
参数说明：
- `operatorUid`：`String`，操作者 uid。
- `selfUnMuteMicDisabled`：`Boolean`，是否允许自我解除禁音状态。
- `disabled`：`Boolean`，房间音频禁用状态。
返回值说明：无（`Unit`）。

### onRoomChatDisabledChanged(operatorUid, disabled)
```kotlin
fun onRoomChatDisabledChanged(operatorUid: String, disabled: Boolean)
```
方法说明：房间内用户发送文本消息被禁用事件。  
参数说明：
- `operatorUid`：`String`，操作者 uid。
- `disabled`：`Boolean`，房间文本消息禁用状态。
返回值说明：无（`Unit`）。

### onRoomScreenshotDisabledChanged(operatorUid, disabled)
```kotlin
fun onRoomScreenshotDisabledChanged(operatorUid: String, disabled: Boolean)
```
方法说明：房间内截屏能力变化事件。  
参数说明：
- `operatorUid`：`String`，操作者 uid。
- `disabled`：`Boolean`，房间截屏禁用状态。
返回值说明：无（`Unit`）。

### onRoomWatermarkDisabledChanged(operatorUid, disabled)
```kotlin
fun onRoomWatermarkDisabledChanged(operatorUid: String, disabled: Boolean)
```
方法说明：房间内水印能力变化事件。  
参数说明：
- `operatorUid`：`String`，操作者 uid。
- `disabled`：`Boolean`，房间水印禁用状态。
返回值说明：无（`Unit`）。

### onRoomLockedChanged(operatorUid, locked)
```kotlin
fun onRoomLockedChanged(operatorUid: String, locked: Boolean)
```
方法说明：房间锁定状态变化事件。  
参数说明：
- `operatorUid`：`String`，操作者 uid。
- `locked`：`Boolean`，锁定状态。
返回值说明：无（`Unit`）。

### onWaitingRoomDisabledChanged(operatorUid, disabled)
```kotlin
fun onWaitingRoomDisabledChanged(operatorUid: String, disabled: Boolean)
```
方法说明：等候室禁用状态变化事件。  
参数说明：
- `operatorUid`：`String`，操作者 uid。
- `disabled`：`Boolean`，等候室禁用状态。
返回值说明：无（`Unit`）。

### onRoomHostMove(sourceUid, targetUid)
```kotlin
fun onRoomHostMove(sourceUid: String, targetUid: String)
```
方法说明：主持人转移事件。  
参数说明：
- `sourceUid`：`String`，原主持人 uid。
- `targetUid`：`String`，新主持人 uid。
返回值说明：无（`Unit`）。

### onCloudRecordStatusChange(type, status, errMsg)
```kotlin
fun onCloudRecordStatusChange(type: CloudRecordType, status: CloudRecordStatus, errMsg: String)
```
方法说明：云录制状态改变事件。  
参数说明：
- `type`：`CloudRecordType`，云录制类型。
- `status`：`CloudRecordStatus`，云录制状态。
- `errMsg`：`String`，错误信息。
返回值说明：无（`Unit`）。

### onMcuAlarmReceived(operatorUid, alarm)
```kotlin
fun onMcuAlarmReceived(operatorUid: String, alarm: McuAlarm)
```
方法说明：MCU 告警（私发）事件。  
参数说明：
- `operatorUid`：`String`，发送者 uid。
- `alarm`：`McuAlarm`，告警信息。
返回值说明：无（`Unit`）。

### onRoomShareStart(shareUid, shareType)
```kotlin
fun onRoomShareStart(shareUid: String, shareType: ShareType)
```
方法说明：共享开始事件（屏幕共享、共享白板）。  
参数说明：
- `shareUid`：`String`，共享者 uid。
- `shareType`：`ShareType`，共享类型。
返回值说明：无（`Unit`）。

### onRoomShareStop(shareUid, shareType)
```kotlin
fun onRoomShareStop(shareUid: String, shareType: ShareType)
```
方法说明：共享结束事件。  
参数说明：
- `shareUid`：`String`，共享者 uid。
- `shareType`：`ShareType`，共享类型。
返回值说明：无（`Unit`）。

### onAdminRoomShareStop(shareUid, shareType)
```kotlin
fun onAdminRoomShareStop(shareUid: String, shareType: ShareType)
```
方法说明：主持人结束共享事件。  
参数说明：
- `shareUid`：`String`，共享者 uid。
- `shareType`：`ShareType`，共享类型。
返回值说明：无（`Unit`）。

### onRoomHandUpChanged(operatorUid, enable, handupType)
```kotlin
fun onRoomHandUpChanged(operatorUid: String, enable: Boolean, handupType: HandUpType)
```
方法说明：房间内举手状态变化事件。  
参数说明：
- `operatorUid`：`String`，操作者 uid。
- `enable`：`Boolean`，举手状态（申请/取消）。
- `handupType`：`HandUpType`，举手申请类型。
返回值说明：无（`Unit`）。

### onAdminRoomStartSubMeeting(subMeetingId, subTitle, uids)
```kotlin
fun onAdminRoomStartSubMeeting(subMeetingId: String, subTitle: String, uids: List<String>)
```
方法说明：主持人开始子会议事件。  
参数说明：
- `subMeetingId`：`String`，子会议 id。
- `subTitle`：`String`，子会议标题。
- `uids`：`List<String>`，子会议中包含的成员 uid 列表。
返回值说明：无（`Unit`）。

### onAdminRoomStopSubMeeting(mainMeetingId, subMeetingId, subTitle)
```kotlin
fun onAdminRoomStopSubMeeting(mainMeetingId: String, subMeetingId: String, subTitle: String)
```
方法说明：主持人停止子会议事件（主会场成员收到）。  
参数说明：
- `mainMeetingId`：`String`，主会议 id。
- `subMeetingId`：`String`，子会议 id。
- `subTitle`：`String`，子会议标题。
返回值说明：无（`Unit`）。

### onError(errorCode, errMsg)
```kotlin
fun onError(errorCode: Int, errMsg: String)
```
方法说明：错误事件回调。  
参数说明：
- `errorCode`：`Int`，错误码。
- `errMsg`：`String`，错误信息。
返回值说明：无（`Unit`）。

### onReconnecting()
```kotlin
fun onReconnecting()
```
方法说明：开始重连事件。  
参数说明：无。  
返回值说明：无（`Unit`）。

### onReconnected()
```kotlin
fun onReconnected()
```
方法说明：重连成功事件。  
参数说明：无。  
返回值说明：无（`Unit`）。
