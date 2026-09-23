---
title: "MeetingRoomEvent"
description: "接收当前会议的房间配置、连接、主持人、录制、共享、举手、讨论组与签到事件"
---

`MeetingRoomEvent` 承载当前会议的房间整体状态和连接生命周期，通过 `MeetingEngine.roomEvent` 注册。可继承 `MeetingRoomSimpleEvent` 按需覆写。

## 使用说明

+ 房间级事件描述整场会议的共享状态、配置和生命周期；指定成员的设备、权限或轨道变化由 `MeetingUserEvent` 分发。

+ 监听可在入会前赋值，以接收首次房间状态；离会后会被清除。
+ 回调保持实际来源线程。`onDisconnected()` 表示底层已经真实断开，主动调用 `exitMeeting()` 不保证产生该回调。

## 房间与连接

### onMeetingUpdated(meetingInfo)

```kotlin
fun onMeetingUpdated(meetingInfo: MeetingInfo?)
```

方法说明：当前会议房间信息刷新。

参数说明：

| 参数 | 说明 |
| --- | --- |
| `meetingInfo` | 更新后的房间快照；解析或生命周期边界下可能为 `null`。 |

返回值说明：无（`Unit`）。

### onDisconnected(reason, statusCode, message)

```kotlin
fun onDisconnected(reason: LeaveReason, statusCode: Int, message: String?)
```

方法说明：当前会议已真实断开。

参数说明：

| 参数 | 说明 |
| --- | --- |
| `reason` | SRTC 断开原因。 |
| `statusCode` | 底层状态码。 |
| `message` | 可空诊断信息。 |

返回值说明：无（`Unit`）。

### onReconnecting()

```kotlin
fun onReconnecting()
```

方法说明：当前会议连接开始自动重连。

参数说明：无。

返回值说明：无（`Unit`）。

### onReconnected()

```kotlin
fun onReconnected()
```

方法说明：当前会议连接自动重连成功。

参数说明：无。

返回值说明：无（`Unit`）。

## 房间配置

### onRoomCameraStateChanged(operatorUid, selfUnMuteCameraDisabled, disabled)

```kotlin
fun onRoomCameraStateChanged(
    operatorUid: String?,
    selfUnMuteCameraDisabled: Boolean,
    disabled: Boolean
)
```

方法说明：房间摄像头禁用与成员自行解除策略发生变化。

参数说明：

| 参数 | 说明 |
| --- | --- |
| `operatorUid` | 操作者 UID；系统事件时可能为 `null`。 |
| `selfUnMuteCameraDisabled` | 是否禁止成员自行解除禁画。 |
| `disabled` | 是否全体禁画。 |

返回值说明：无（`Unit`）。

### onRoomMicStateChanged(operatorUid, selfUnMuteMicDisabled, disabled)

```kotlin
fun onRoomMicStateChanged(
    operatorUid: String?,
    selfUnMuteMicDisabled: Boolean,
    disabled: Boolean
)
```

方法说明：房间麦克风禁用与成员自行解除策略发生变化。

参数说明：

| 参数 | 说明 |
| --- | --- |
| `operatorUid` | 可空操作者 UID。 |
| `selfUnMuteMicDisabled` | 是否禁止成员自行解除禁音。 |
| `disabled` | 是否全体禁音。 |

返回值说明：无（`Unit`）。

### onRoomChatDisabledChanged(operatorUid, disabled)

```kotlin
fun onRoomChatDisabledChanged(operatorUid: String?, disabled: Boolean)
```

方法说明：房间聊天禁用状态变化。

参数说明：

| 参数 | 说明 |
| --- | --- |
| `operatorUid` | 操作者 UID；系统事件时可能为 `null`。 |
| `disabled` | `true` 表示禁止房间成员聊天。 |

返回值说明：无（`Unit`）。

### onRoomScreenshotDisabledChanged(operatorUid, disabled)

```kotlin
fun onRoomScreenshotDisabledChanged(operatorUid: String?, disabled: Boolean)
```

方法说明：房间截屏禁用状态变化。

参数说明：

| 参数 | 说明 |
| --- | --- |
| `operatorUid` | 操作者 UID；系统事件时可能为 `null`。 |
| `disabled` | `true` 表示禁止房间成员截屏。 |

返回值说明：无（`Unit`）。

### onRoomWatermarkDisabledChanged(operatorUid, disabled)

```kotlin
fun onRoomWatermarkDisabledChanged(operatorUid: String?, disabled: Boolean)
```

方法说明：房间水印禁用状态变化。

参数说明：

| 参数 | 说明 |
| --- | --- |
| `operatorUid` | 操作者 UID；系统事件时可能为 `null`。 |
| `disabled` | `true` 表示禁用房间水印。 |

返回值说明：无（`Unit`）。

### onRoomLockedChanged(operatorUid, locked)

```kotlin
fun onRoomLockedChanged(operatorUid: String?, locked: Boolean)
```

方法说明：房间锁定状态变化。

参数说明：

| 参数 | 说明 |
| --- | --- |
| `operatorUid` | 操作者 UID；系统事件时可能为 `null`。 |
| `locked` | `true` 表示房间已经锁定。 |

返回值说明：无（`Unit`）。

### onWaitingRoomDisabledChanged(operatorUid, disabled)

```kotlin
fun onWaitingRoomDisabledChanged(operatorUid: String?, disabled: Boolean)
```

方法说明：等候室启停状态变化。

参数说明：

| 参数 | 说明 |
| --- | --- |
| `operatorUid` | 操作者 UID；系统事件时可能为 `null`。 |
| `disabled` | `true` 表示等候室已经禁用。 |

返回值说明：无（`Unit`）。

### onRoomHostMove(sourceUid, targetUid)

```kotlin
fun onRoomHostMove(sourceUid: String?, targetUid: String?)
```

方法说明：主持人身份从原成员转移到目标成员。

参数说明：

| 参数 | 说明 |
| --- | --- |
| `sourceUid` | 原主持人 UID，可能为 `null`。 |
| `targetUid` | 新主持人 UID，可能为 `null`。 |

返回值说明：无（`Unit`）。

## 录制、共享与举手

### onCloudRecordStatusChange(type, status, errorMessage)

```kotlin
fun onCloudRecordStatusChange(
    type: CloudRecordType,
    status: CloudRecordStatus,
    errorMessage: String
)
```

方法说明：云录制任务状态变化。

参数说明：

| 参数 | 说明 |
| --- | --- |
| `type` | 录制任务类型。 |
| `status` | 当前任务状态。 |
| `errorMessage` | 异常信息；无异常时通常为空字符串。 |

返回值说明：无（`Unit`）。

### onMcuAlarmReceived(operatorUid, alarm)

```kotlin
fun onMcuAlarmReceived(operatorUid: String, alarm: McuAlarm)
```

方法说明：收到 MCU 私发告警。

参数说明：

| 参数 | 说明 |
| --- | --- |
| `operatorUid` | 消息发送方 UID。 |
| `alarm` | 任务、网关、时间和摘要信息。 |

返回值说明：无（`Unit`）。

### onRoomShareStart(shareUid, shareType)

```kotlin
fun onRoomShareStart(shareUid: String?, shareType: ShareType)
```

方法说明：指定成员开始屏幕或白板共享。

参数说明：

| 参数 | 说明 |
| --- | --- |
| `shareUid` | 共享者 UID；无法确定时可能为 `null`。 |
| `shareType` | 开始的共享类型。 |

返回值说明：无（`Unit`）。

### onRoomShareStop(shareUid, shareType)

```kotlin
fun onRoomShareStop(shareUid: String?, shareType: ShareType)
```

方法说明：指定成员结束屏幕或白板共享。

参数说明：

| 参数 | 说明 |
| --- | --- |
| `shareUid` | 共享者 UID；无法确定时可能为 `null`。 |
| `shareType` | 结束的共享类型。 |

返回值说明：无（`Unit`）。

### onAdminRoomShareStop(shareUid, shareType)

```kotlin
fun onAdminRoomShareStop(shareUid: String, shareType: ShareType)
```

方法说明：主持人强制结束指定成员共享。

参数说明：

| 参数 | 说明 |
| --- | --- |
| `shareUid` | 被停止共享的成员 UID。 |
| `shareType` | 被停止的共享类型。 |

返回值说明：无（`Unit`）。

### onRoomHandUpChanged(operatorUid, enabled, handUpType)

```kotlin
fun onRoomHandUpChanged(
    operatorUid: String?,
    enabled: Boolean?,
    handUpType: HandUpType?
)
```

方法说明：房间成员举手状态变化。

参数说明：

| 参数 | 说明 |
| --- | --- |
| `operatorUid` | 可空成员 UID。 |
| `enabled` | `true` 举手，`false` 取消；无法解析时为 `null`。 |
| `handUpType` | 举手类型；无法解析时为 `null`。 |

返回值说明：无（`Unit`）。

## 讨论组与签到

### onAdminRoomStartSubMeeting(subMeetingId, subTitle, uids)

```kotlin
fun onAdminRoomStartSubMeeting(
    subMeetingId: String,
    subTitle: String,
    uids: List<String>
)
```

方法说明：主持人启动指定讨论组。

参数说明：

| 参数 | 说明 |
| --- | --- |
| `subMeetingId` | 启动的讨论组会议 ID。 |
| `subTitle` | 讨论组标题。 |
| `uids` | 分配到该讨论组的成员 UID 列表。 |

返回值说明：无（`Unit`）。

### onAdminRoomStopSubMeeting(mainMeetingId, subMeetingId, subTitle)

```kotlin
fun onAdminRoomStopSubMeeting(
    mainMeetingId: String,
    subMeetingId: String,
    subTitle: String
)
```

方法说明：主持人结束指定讨论组。

参数说明：

| 参数 | 说明 |
| --- | --- |
| `mainMeetingId` | 主会议 ID。 |
| `subMeetingId` | 结束的讨论组会议 ID。 |
| `subTitle` | 讨论组标题。 |

返回值说明：无（`Unit`）。

### onSignInActivity(hostName, epoch, beginAt, duration, endAt, description)

```kotlin
fun onSignInActivity(
    hostName: String,
    epoch: Int,
    beginAt: Long,
    duration: Int,
    endAt: Long,
    description: String
)
```

方法说明：收到会中签到活动开始消息。

参数说明：

| 参数 | 说明 |
| --- | --- |
| `hostName` | 发起人昵称。 |
| `epoch` | 签到轮次。 |
| `beginAt` | 开始时间，秒级时间戳。 |
| `duration` | 持续时长，单位分钟；`0` 表示不限时。 |
| `endAt` | 结束时间，秒级时间戳。 |
| `description` | 签到说明。 |

返回值说明：无（`Unit`）。

### onSignInFinish(hostName, epoch)

```kotlin
fun onSignInFinish(hostName: String, epoch: Int)
```

方法说明：收到会中签到活动结束消息。

参数说明：

| 参数 | 说明 |
| --- | --- |
| `hostName` | 结束活动的主持人昵称。 |
| `epoch` | 签到轮次。 |

返回值说明：无（`Unit`）。
