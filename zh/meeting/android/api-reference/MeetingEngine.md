---
title: "MeetingEngine"
description: "SMeeting Android SDK 全局入口，负责初始化、IM、设备、会前管理和发起入会"
---

`MeetingEngine` 与 SDK 生命周期一致，只承载全局、IM、设备和会前能力。入会成功后，请保存回调返回的 [MeetingSession](/zh/meeting/android/api-reference/MeetingSession)，所有会中调用都在该 Session 上完成。

## 创建与生命周期

```kotlin
val engine = MeetingEngine.create(application)

MeetingEngine.version()
MeetingEngine.buildTime()

engine.initSdk(meetToken, mediaOptions, callback)
engine.updateMediaOptions(mediaOptions)
engine.onAppForeground()
engine.onAppBackground()
engine.release()
```

`create()` 返回进程内共享实例。`release()` 会先关闭活动 Session，再释放 SDK 资源；释放后可重新调用 `create()`。

### activeSession

```kotlin
val activeSession: MeetingSession?
```

返回当前已成功入会且仍有效的 Session；没有活动会议时为 `null`。

## Engine 级事件

```kotlin
engine.setEngineEvent(event: MeetingEngineEvent?)
engine.setImEvent(event: MeetingImEvent?)
engine.setCameraDeviceEvent(event: MeetingCameraDeviceEvent?)
engine.setMicDeviceEvent(event: MeetingMicDeviceEvent?)
```

这些监听与 Engine 同生命周期，不属于某一场会议。事件说明见 [事件接口](/zh/meeting/android/api-reference/meeting-events)。

## IM 与设备

```kotlin
fun enableIm(callback: MeetingValueResultCallback<MeetingImConnection>)
fun disableIm()
fun getMicDevices(): List<MicDeviceCapability>
fun switchMicDevice(deviceId: String)
```

`enableIm()` 成功返回 `MeetingImConnection(uid, sid)`；失败使用 `onFail(errorCode, message)`。

## 会前接口

| 方法 | 说明 |
| --- | --- |
| `getSelfInfo(callback)` | 获取当前登录用户信息 |
| `getAgentList(types, keyword, page, perPage, callback)` | 查询可邀请的设备或用户 |
| `createImmediateMeeting(title, option, callback)` | 创建即时会议 |
| `createScheduleMeeting(title, planTime, planDur, option, callback)` | 创建预约会议 |
| `updateMeetingBeforeStart(meetingId, option, callback)` | 更新尚未开始的会议 |
| `getMeetingList(page, perPage, callback)` | 查询待开始或进行中的会议 |
| `getHistoryMeetingList(page, perPage, callback)` | 查询历史会议 |
| `getMeetingDetail(meetingId, callback)` | 按会议 ID 查询详情 |
| `getMeetingDetailByRoomNo(roomNo, callback)` | 按房间号查询详情 |
| `cancelMeetingBeforeStart(meetingId, callback)` | 取消尚未开始的会议 |

以上 HTTP 业务接口继续使用 `Callback<T>`，其服务端业务响应契约与 Meeting 一次性结果回调不同。

## 加入会议

### 按房间号加入

```kotlin
fun enterMeeting(
    activity: Activity,
    roomNo: String,
    password: String?,
    nick: String,
    avatar: String,
    streamVendor: String,
    isAudience: Boolean,
    extendInfo: String?,
    callback: MeetingValueResultCallback<MeetingSession>
)
```

### 按会议 ID 加入

```kotlin
fun enterMeetingByMeetingId(
    activity: Activity,
    meetingId: String,
    password: String?,
    nick: String,
    avatar: String,
    streamVendor: String,
    isAudience: Boolean,
    extendInfo: String?,
    callback: MeetingValueResultCallback<MeetingSession>
)
```

关键参数：

+ `streamVendor`：流媒体厂商标识，例如 `wangsucdn`。
+ `isAudience`：是否以观众身份入会；观众不能执行开设备、共享或发流等受限操作。
+ `extendInfo`：业务扩展 JSON；没有扩展信息时传 `null`。
+ `callback`：成功返回本次会议专属的 `MeetingSession`。同一个 Engine 同时只允许一个加入中或活动 Session。

位于等候室、尚未完成 RTC 入会时，可调用：

```kotlin
fun exitWaitingRoom(callback: Callback<Data<String?>>?)
```

## 错误处理

Meeting 一次性失败结果使用 `errorCode + message`。Meeting 自产错误为 `202xxx`，RTC、服务端和 HTTP 的有效错误码通常原样透传。`message` 只用于开发诊断，不应直接作为用户展示文案。详见 [错误码](/zh/meeting/android/error-codes)。
