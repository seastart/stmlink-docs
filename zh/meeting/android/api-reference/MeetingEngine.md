---
title: "MeetingEngine"
description: "SMeeting Android SDK 的唯一公开入口，覆盖初始化、会前业务、入会、会控、本地媒体、共享、消息与远端订阅"
---

`MeetingEngine` 是 SMeeting Android SDK 的公开业务入口，通过 `MeetingEngine.create(application)` 创建。它负责 SDK 初始化与释放、会前会议管理、入会与离会、会中控制、本地媒体、共享、消息和远端媒体订阅。

## 使用说明

+ `MeetingEngine.create(application)` 每次创建一个 Engine 实例。应用应在进程内集中持有一个实例，并在不再使用时调用 `release()`。
+ 当前公开 API 采用单会议模型：同一 Engine 同时只能有一场加入中或活动会议；重复入会返回 `MeetingErrorCode.SESSION_ALREADY_ACTIVE`。
+ 入会成功返回 [MeetingEnterInfo](/zh/meeting/android/types#meetingenterinfo)，后续会中能力继续通过当前 `MeetingEngine` 调用。
+ 所有异步结果回调保持实际来源线程，不保证主线程；更新 UI 前应切换到主线程。
+ `MeetingResultCallback` / `MeetingValueResultCallback<T>` 的失败方法是 `onFailure(errorCode, message)`。`message` 仅用于诊断，不应直接展示给用户。
+ `roomEvent`、`userEvent`、`mediaEvent`、`messageEvent` 会绑定当前会议并在离会时清除；需要接收下一场会议事件时应重新赋值。Engine、IM 和设备事件与 Engine 生命周期一致。

## 创建与版本

### create(app)

```kotlin
fun create(app: Application): MeetingEngine
```

方法说明：创建一个 `MeetingEngine` 实例。

参数说明：

| 参数 | 说明 |
| --- | --- |
| `app` | `Application`，应用级上下文。 |

返回值说明：新建的 `MeetingEngine`。

### version()

```kotlin
fun version(): String
```

方法说明：获取 Meeting SDK 版本号。

参数说明：无。

返回值说明：构建时写入的版本字符串，例如 `2.0.35`。

### buildTime()

```kotlin
fun buildTime(): String
```

方法说明：获取 Meeting SDK 构建时间。

参数说明：无。

返回值说明：构建时间字符串。

## 管理器属性

### infosManager

```kotlin
val infosManager: InfosManager
```

属性说明：读取当前会议、成员和媒体轨道的本地快照。该门面可在会前保存；未入会时查询返回空值或空集合。详见 [InfosManager](/zh/meeting/android/api-reference/InfosManager)。

### rollCallManager

```kotlin
val rollCallManager: RollCallManager
```

属性说明：当前会议的点名管理门面。未入会时，异步操作通过回调返回 `SESSION_NOT_ACTIVE`。详见 [RollCallManager](/zh/meeting/android/api-reference/RollCallManager)。

### signInManager

```kotlin
val signInManager: SignInManager
```

属性说明：当前会议的签到管理门面。未入会时，异步操作通过回调返回 `SESSION_NOT_ACTIVE`。详见 [SignInManager](/zh/meeting/android/api-reference/SignInManager)。

## 事件属性

以下属性通过直接赋值注册监听，赋 `null` 取消监听。每个事件的回调参数与线程语义见对应接口页。

| 属性 | 类型 | 作用域 |
| --- | --- | --- |
| `engineEvent` | `MeetingEngineEvent?` | Engine 全局运行错误 |
| `imEvent` | `MeetingImEvent?` | IM 连接与业务消息 |
| `cameraDeviceEvent` | `MeetingCameraDeviceEvent?` | 进程共享摄像头设备 |
| `micDeviceEvent` | `MeetingMicDeviceEvent?` | 进程共享麦克风设备 |
| `localVideoFrameEvent` | `MeetingLocalVideoFrameEvent?` | 本地视频采集帧 |
| `localAudioFrameEvent` | `MeetingLocalAudioFrameEvent?` | 本地 PCM 采集帧 |
| `screenCaptureEvent` | `MeetingScreenCaptureEvent?` | 本地屏幕采集状态 |
| `roomEvent` | `MeetingRoomEvent?` | 当前会议房间状态与连接 |
| `userEvent` | `MeetingUserEvent?` | 当前会议成员、权限与轨道 |
| `mediaEvent` | `MeetingMediaEvent?` | 当前会议媒体与质量统计 |
| `messageEvent` | `MeetingMessageEvent?` | 当前会议聊天、系统与扩展消息 |

## 初始化与释放

### initSdk(meetToken, options, callback)

```kotlin
fun initSdk(
    meetToken: String,
    options: RTCMediaOptions?,
    callback: MeetingResultCallback
)
```

方法说明：使用 Meeting token 初始化服务连接与底层 SRTC SDK。无效或过期 token、本地状态错误均通过结果回调返回。

参数说明：

| 参数 | 说明 |
| --- | --- |
| `meetToken` | `String`，Meeting 服务端签发的初始化 token。 |
| `options` | `RTCMediaOptions?`，SRTC 媒体配置；传 `null` 使用默认配置。 |
| `callback` | `MeetingResultCallback`，初始化唯一终态回调。 |

返回值说明：无（`Unit`）。

### updateMediaOptions(options)

```kotlin
fun updateMediaOptions(options: RTCMediaOptions)
```

方法说明：更新底层 SRTC 媒体参数。

参数说明：

| 参数 | 说明 |
| --- | --- |
| `options` | `RTCMediaOptions`，新的媒体配置。 |

返回值说明：无（`Unit`）。

### release()

```kotlin
fun release()
```

方法说明：离开当前会议、停止采集与订阅、关闭 IM，并释放 Meeting 和 SRTC 资源。释放后的实例不可继续使用。

参数说明：无。

返回值说明：无（`Unit`）。

## 媒体统计与云录制采集

### getMetric()

```kotlin
fun getMetric(): MediaMetric.Metric?
```

方法说明：获取当前会议最近一次采样的媒体质量快照；不会主动触发底层统计采集。

参数说明：无。

返回值说明：线程安全的 `MediaMetric.Metric` 副本；未入会或首个约 5 秒采样尚未产生时为 `null`。字段见[媒体质量](/zh/meeting/android/media-quality)。

### enableClientCloudRecordCapture

```kotlin
var enableClientCloudRecordCapture: Boolean
```

属性说明：是否由客户端维护云录制使用的 `TrackDesc.TRACK_SHARE` 轨道。开启后可通过 `getShareCustomVideoTrack()` 获取自定义视频轨。

### getShareCustomVideoTrack(preOpt)

```kotlin
fun getShareCustomVideoTrack(preOpt: PreOptionCustomVideo?): LocalCustomVideoTrack?
```

方法说明：获取或复用供应用写入云录制画面的自定义视频轨。应用不得自行发布或取消发布该轨道。

参数说明：

| 参数 | 说明 |
| --- | --- |
| `preOpt` | `PreOptionCustomVideo?`，自定义视频采集参数；传 `null` 使用底层默认配置。 |

返回值说明：缓存或新建的 `LocalCustomVideoTrack`；底层 SRTC 尚未就绪或无法创建轨道时为 `null`。`enableClientCloudRecordCapture` 约束的是后续课程录制发布流程，不阻止提前取得并写入该轨道。

## 当前用户信息

### getSelfInfo(callback)

```kotlin
fun getSelfInfo(callback: MeetingValueResultCallback<UserBean>)
```

方法说明：从 Meeting 服务获取当前登录用户信息。

参数说明：

| 参数 | 说明 |
| --- | --- |
| `callback` | 成功返回 `UserBean` 的结果回调。 |

返回值说明：无（异步结果见回调）。

## 主持人成员控制

### adminUpdateUserName(targetId, name, callback)

```kotlin
fun adminUpdateUserName(
    targetId: String,
    name: String,
    callback: MeetingResultCallback
)
```

方法说明：修改指定成员的会中昵称。

参数说明：

| 参数 | 说明 |
| --- | --- |
| `targetId` | 目标成员 UID。 |
| `name` | 新昵称。 |
| `callback` | 更新结果回调。 |

返回值说明：无（异步结果见回调）。

### adminUpdateUserRole(targetId, role, callback)

```kotlin
fun adminUpdateUserRole(
    targetId: String,
    role: MemberRoleType,
    callback: MeetingResultCallback
)
```

方法说明：修改指定成员的会议角色。

参数说明：

| 参数 | 说明 |
| --- | --- |
| `targetId` | 目标成员 UID。 |
| `role` | 新的 `MemberRoleType`。 |
| `callback` | 更新结果回调。 |

返回值说明：无（异步结果见回调）。

### adminMoveHost(targetId, callback)

```kotlin
fun adminMoveHost(targetId: String, callback: MeetingResultCallback)
```

方法说明：把主持人身份移交给指定成员。

参数说明：

| 参数 | 说明 |
| --- | --- |
| `targetId` | 新主持人的 UID。 |
| `callback` | 移交结果回调。 |

返回值说明：无（异步结果见回调）。

### adminUpdateUserDrawDisabled(targetId, drawDisabled, callback)

```kotlin
fun adminUpdateUserDrawDisabled(
    targetId: String,
    drawDisabled: Boolean,
    callback: MeetingResultCallback
)
```

方法说明：更新指定成员的白板涂鸦权限。

参数说明：

| 参数 | 说明 |
| --- | --- |
| `targetId` | 目标成员 UID。 |
| `drawDisabled` | `true` 表示禁止涂鸦。 |
| `callback` | 更新结果回调。 |

返回值说明：无（异步结果见回调）。

### adminUpdateUserChatDisabled(targetId, chatDisabled, callback)

```kotlin
fun adminUpdateUserChatDisabled(
    targetId: String,
    chatDisabled: Boolean,
    callback: MeetingResultCallback
)
```

方法说明：更新指定成员的聊天权限。

参数说明：

| 参数 | 说明 |
| --- | --- |
| `targetId` | 目标成员 UID。 |
| `chatDisabled` | `true` 表示禁止聊天。 |
| `callback` | 更新结果回调。 |

返回值说明：无（异步结果见回调）。

### adminRequestUserOpenCamera(targetId, callback)

```kotlin
fun adminRequestUserOpenCamera(targetId: String, callback: MeetingResultCallback)
```

方法说明：请求指定成员打开摄像头；对方通过 `MeetingUserEvent.onRequestOpenCamera()` 接收请求。

参数说明：

| 参数 | 说明 |
| --- | --- |
| `targetId` | 目标成员 UID。 |
| `callback` | 请求提交结果回调。 |

返回值说明：无（异步结果见回调）。

### adminCloseUserCamera(targetId, callback)

```kotlin
fun adminCloseUserCamera(targetId: String, callback: MeetingResultCallback)
```

方法说明：由主持人关闭指定成员摄像头。

参数说明：

| 参数 | 说明 |
| --- | --- |
| `targetId` | 目标成员 UID。 |
| `callback` | 操作结果回调。 |

返回值说明：无（异步结果见回调）。

### adminDisableUserCamera(targetId, cameraDisabled, callback)

```kotlin
fun adminDisableUserCamera(
    targetId: String,
    cameraDisabled: Boolean,
    callback: MeetingResultCallback
)
```

方法说明：预留的成员摄像头禁用接口。

参数说明：

| 参数 | 说明 |
| --- | --- |
| `targetId` | 目标成员 UID。 |
| `cameraDisabled` | 目标禁用状态。 |
| `callback` | 结果回调。 |

返回值说明：无（异步结果见回调）。

:::warning
当前版本尚未实现该能力，不应依赖它完成会控；需要立即关闭摄像头时使用 `adminCloseUserCamera()`。
:::

### adminRequestUserOpenMic(targetId, callback)

```kotlin
fun adminRequestUserOpenMic(targetId: String, callback: MeetingResultCallback)
```

方法说明：请求指定成员打开麦克风；对方通过 `MeetingUserEvent.onRequestOpenMic()` 接收请求。

参数说明：

| 参数 | 说明 |
| --- | --- |
| `targetId` | 目标成员 UID。 |
| `callback` | 请求提交结果回调。 |

返回值说明：无（异步结果见回调）。

### adminCloseUserMic(targetId, callback)

```kotlin
fun adminCloseUserMic(targetId: String, callback: MeetingResultCallback)
```

方法说明：由主持人关闭指定成员麦克风。

参数说明：

| 参数 | 说明 |
| --- | --- |
| `targetId` | 目标成员 UID。 |
| `callback` | 操作结果回调。 |

返回值说明：无（异步结果见回调）。

### adminDisableUserMic(targetId, micDisabled, callback)

```kotlin
fun adminDisableUserMic(
    targetId: String,
    micDisabled: Boolean,
    callback: MeetingResultCallback
)
```

方法说明：预留的成员麦克风禁用接口。

参数说明：

| 参数 | 说明 |
| --- | --- |
| `targetId` | 目标成员 UID。 |
| `micDisabled` | 目标禁用状态。 |
| `callback` | 结果回调。 |

返回值说明：无（异步结果见回调）。

:::warning
当前版本尚未实现该能力，不应依赖它完成会控；需要立即关闭麦克风时使用 `adminCloseUserMic()`。
:::

### adminRequestUserShare(targetId, callback)

```kotlin
fun adminRequestUserShare(targetId: String, callback: MeetingResultCallback)
```

方法说明：请求指定成员开始屏幕共享。

参数说明：

| 参数 | 说明 |
| --- | --- |
| `targetId` | 目标成员 UID。 |
| `callback` | 请求提交结果回调。 |

返回值说明：无（异步结果见回调）。

### adminStopRoomShare(callback)

```kotlin
fun adminStopRoomShare(callback: MeetingResultCallback)
```

方法说明：强制停止当前房间正在进行的屏幕或白板共享。

参数说明：

| 参数 | 说明 |
| --- | --- |
| `callback` | 停止共享结果回调。 |

返回值说明：无（异步结果见回调）。

### adminInviteAgent(agents, callback)

```kotlin
fun adminInviteAgent(
    agents: List<AgentRequestBean>,
    callback: MeetingResultCallback
)
```

方法说明：邀请 SIP、H323、RTSP、RTMP 等外部设备进入当前会议。

参数说明：

| 参数 | 说明 |
| --- | --- |
| `agents` | 设备类型和联系标识列表。 |
| `callback` | 邀请结果回调。 |

返回值说明：无（异步结果见回调）。

### adminKickUserOut(targetId, callback)

```kotlin
fun adminKickUserOut(targetId: String, callback: MeetingResultCallback)
```

方法说明：将指定成员移出当前会议。

参数说明：

| 参数 | 说明 |
| --- | --- |
| `targetId` | 目标成员 UID。 |
| `callback` | 操作结果回调。 |

返回值说明：无（异步结果见回调）。

### adminConfirmHandUp(targetId, code, approve, callback)

```kotlin
fun adminConfirmHandUp(
    targetId: String,
    code: HandUpType,
    approve: Boolean,
    callback: MeetingResultCallback
)
```

方法说明：处理指定成员的举手申请。

参数说明：

| 参数 | 说明 |
| --- | --- |
| `targetId` | 申请成员 UID。 |
| `code` | 举手类型。 |
| `approve` | `true` 同意，`false` 拒绝。 |
| `callback` | 处理结果回调。 |

返回值说明：无（异步结果见回调）。

### adminGetOnlineMembers(meetingId, page, prePage, callback)

```kotlin
fun adminGetOnlineMembers(
    meetingId: String?,
    page: Int,
    prePage: Int,
    callback: MeetingValueResultCallback<MeetingPage<MemberBean>>
)
```

方法说明：分页查询指定会议的在线成员。

参数说明：

| 参数 | 说明 |
| --- | --- |
| `meetingId` | 目标会议 ID；传 `null` 使用当前会议。 |
| `page` | 页码，从 `1` 开始。 |
| `prePage` | 每页最大条目数。参数名为历史拼写，含义等同 `perPage`。 |
| `callback` | 成功返回在线成员分页结果的回调。 |

返回值说明：无（异步结果见回调）。

### adminUpdateRoomMCUMode()

```kotlin
fun adminUpdateRoomMCUMode()
```

方法说明：预留的房间 MCU 模式更新入口。

参数说明：无。

返回值说明：无（`Unit`）。

:::warning
当前版本尚未实现该接口，调用只记录警告日志。
:::

## 等候室

### adminWaitingRoomDisabled(waitingRoomDisabled, callback)

```kotlin
fun adminWaitingRoomDisabled(
    waitingRoomDisabled: Boolean,
    callback: MeetingResultCallback
)
```

方法说明：启用或禁用当前会议的等候室。

参数说明：

| 参数 | 说明 |
| --- | --- |
| `waitingRoomDisabled` | `true` 禁用等候室，`false` 启用等候室。 |
| `callback` | 更新结果回调。 |

返回值说明：无（异步结果见回调）。

### adminMoveOutWaitingRoom(uid, callback)

```kotlin
fun adminMoveOutWaitingRoom(uid: String?, callback: MeetingResultCallback)
```

方法说明：将等候室成员移入会议。

参数说明：

| 参数 | 说明 |
| --- | --- |
| `uid` | 目标成员 UID；传 `null` 表示处理等候室中的全部成员。 |
| `callback` | 操作结果回调。 |

返回值说明：无（异步结果见回调）。

### adminMoveInWaitingRoom(uid, nickName, callback)

```kotlin
fun adminMoveInWaitingRoom(
    uid: String,
    nickName: String,
    callback: MeetingResultCallback
)
```

方法说明：将当前会议成员移入等候室。

参数说明：

| 参数 | 说明 |
| --- | --- |
| `uid` | 目标成员 UID。 |
| `nickName` | 目标成员昵称。 |
| `callback` | 操作结果回调。 |

返回值说明：无（异步结果见回调）。

### adminGetWaitingRoomUsers(callback)

```kotlin
fun adminGetWaitingRoomUsers(
    callback: MeetingValueResultCallback<List<WaitingRoomUserBean>>
)
```

方法说明：查询当前会议等候室成员。

参数说明：

| 参数 | 说明 |
| --- | --- |
| `callback` | 成功返回等候室成员列表的回调。 |

返回值说明：无（异步结果见回调）。

## 讨论组

### createSubMeeting(subMeetingTitles, callback)

```kotlin
fun createSubMeeting(
    subMeetingTitles: MutableList<String>,
    callback: MeetingResultCallback
)
```

方法说明：在当前主会议下创建一个或多个讨论组。

参数说明：

| 参数 | 说明 |
| --- | --- |
| `subMeetingTitles` | 讨论组标题列表。 |
| `callback` | 创建结果回调。 |

返回值说明：无（异步结果见回调）。

### updateSubMeetingTitle(id, title, callback)

```kotlin
fun updateSubMeetingTitle(
    id: String,
    title: String,
    callback: MeetingResultCallback
)
```

方法说明：修改指定讨论组标题。

参数说明：

| 参数 | 说明 |
| --- | --- |
| `id` | 讨论组记录 ID。 |
| `title` | 新标题。 |
| `callback` | 更新结果回调。 |

返回值说明：无（异步结果见回调）。

### updateSubMeetingUsers(id, members, callback)

```kotlin
fun updateSubMeetingUsers(
    id: String,
    members: MutableList<MemberRequestBean>,
    callback: MeetingResultCallback
)
```

方法说明：全量更新指定讨论组成员。

参数说明：

| 参数 | 说明 |
| --- | --- |
| `id` | 讨论组记录 ID。 |
| `members` | 目标成员 UID 和昵称列表。 |
| `callback` | 更新结果回调。 |

返回值说明：无（异步结果见回调）。

### deleteSubMeeting(ids, callback)

```kotlin
fun deleteSubMeeting(ids: MutableList<String>, callback: MeetingResultCallback)
```

方法说明：删除指定讨论组。

参数说明：

| 参数 | 说明 |
| --- | --- |
| `ids` | 讨论组记录 ID 列表。 |
| `callback` | 删除结果回调。 |

返回值说明：无（异步结果见回调）。

### getSubMeetingList(callback)

```kotlin
fun getSubMeetingList(
    callback: MeetingValueResultCallback<List<SubMeetingBean>>
)
```

方法说明：查询当前主会议下的讨论组列表。

参数说明：

| 参数 | 说明 |
| --- | --- |
| `callback` | 成功返回讨论组列表的回调。 |

返回值说明：无（异步结果见回调）。

### startSubMeeting(ids, callback)

```kotlin
fun startSubMeeting(ids: MutableList<String>, callback: MeetingResultCallback)
```

方法说明：启动指定讨论组。

参数说明：

| 参数 | 说明 |
| --- | --- |
| `ids` | 讨论组记录 ID 列表。 |
| `callback` | 启动结果回调。 |

返回值说明：无（异步结果见回调）。

### stopSubMeeting(ids, callback)

```kotlin
fun stopSubMeeting(ids: MutableList<String>, callback: MeetingResultCallback)
```

方法说明：结束指定讨论组。

参数说明：

| 参数 | 说明 |
| --- | --- |
| `ids` | 讨论组记录 ID 列表。 |
| `callback` | 停止结果回调。 |

返回值说明：无（异步结果见回调）。

### moveSubMeetingUser(fromId, toId, uid, callback)

```kotlin
fun moveSubMeetingUser(
    fromId: String,
    toId: String?,
    uid: String,
    callback: MeetingResultCallback
)
```

方法说明：在主会场和讨论组之间移动成员。

参数说明：

| 参数 | 说明 |
| --- | --- |
| `fromId` | 来源讨论组记录 ID。 |
| `toId` | 目标讨论组记录 ID；传 `null` 表示移回主会场。 |
| `uid` | 目标成员 UID。 |
| `callback` | 移动结果回调。 |

返回值说明：无（异步结果见回调）。

### updateEnterBeforeHostDisabled(meetingId, enterBeforeHostDisabled, callback)

```kotlin
fun updateEnterBeforeHostDisabled(
    meetingId: String,
    enterBeforeHostDisabled: Boolean,
    callback: MeetingResultCallback
)
```

方法说明：更新指定会议能否在主持人进入前入会。

参数说明：

| 参数 | 说明 |
| --- | --- |
| `meetingId` | 目标主会议或讨论组会议 ID。 |
| `enterBeforeHostDisabled` | `true` 表示禁止主持人前入会。 |
| `callback` | 更新结果回调。 |

返回值说明：无（异步结果见回调）。

### helpSubMeeting(meetingId, callback)

```kotlin
fun helpSubMeeting(meetingId: String, callback: MeetingResultCallback)
```

方法说明：从讨论组向主会场主持人发起求助。

参数说明：

| 参数 | 说明 |
| --- | --- |
| `meetingId` | 当前讨论组会议 ID。 |
| `callback` | 请求提交结果回调。 |

返回值说明：无（异步结果见回调）。

## 当前用户昵称

### updateName(name, callback)

```kotlin
fun updateName(name: String, callback: MeetingResultCallback)
```

方法说明：修改当前用户的会中昵称。

参数说明：

| 参数 | 说明 |
| --- | --- |
| `name` | 新昵称。 |
| `callback` | 更新结果回调。 |

返回值说明：无（异步结果见回调）。

## 用户、IM 与呼叫

### getAgentList(types, keyword, page, perPage, callback)

```kotlin
fun getAgentList(
    types: MutableList<AgentType>,
    keyword: String,
    page: Int,
    perPage: Int,
    callback: MeetingValueResultCallback<MeetingPage<AgentBean>>
)
```

方法说明：按设备类型和关键字分页查询可邀请的联系人设备。

参数说明：

| 参数 | 说明 |
| --- | --- |
| `types` | 要查询的 `AgentType` 列表。 |
| `keyword` | 服务端支持字段的过滤关键字；不筛选时传空字符串。 |
| `page` | 页码，从 `1` 开始。 |
| `perPage` | 每页最大条目数。 |
| `callback` | 成功返回 `MeetingPage<AgentBean>` 的结果回调。 |

返回值说明：无（异步结果见回调）。

### enableIm(callback)

```kotlin
fun enableIm(callback: MeetingValueResultCallback<MeetingImConnection>)
```

方法说明：申请 IM 授权并建立连接。连接建立后持续状态和消息通过 `imEvent` 通知。

参数说明：

| 参数 | 说明 |
| --- | --- |
| `callback` | 成功返回 `MeetingImConnection(uid, sid)` 的结果回调。 |

返回值说明：无（异步结果见回调）。

### disableIm()

```kotlin
fun disableIm()
```

方法说明：主动关闭 IM。主动关闭不会触发 `MeetingImEvent.onImDisconnected()`。

参数说明：无。

返回值说明：无（`Unit`）。

### callUser(targetUids, callback)

```kotlin
fun callUser(targetUids: MutableList<String>, callback: MeetingResultCallback)
```

方法说明：呼叫指定用户加入当前会议。

参数说明：

| 参数 | 说明 |
| --- | --- |
| `targetUids` | 目标用户 UID 列表。 |
| `callback` | 服务端提交结果回调。 |

返回值说明：无（异步结果见回调）。

## 会前会议管理

### createImmediateMeeting(title, option, callback)

```kotlin
fun createImmediateMeeting(
    title: String,
    option: CreateImmediateMeetingOption,
    callback: MeetingValueResultCallback<MeetingCreatedBean>
)
```

方法说明：创建即时会议。

参数说明：

| 参数 | 说明 |
| --- | --- |
| `title` | 会议标题。 |
| `option` | 即时会议可选参数。 |
| `callback` | 成功返回会议 ID 与房间号的回调。 |

返回值说明：无（异步结果见回调）。

### createScheduleMeeting(title, planTime, planDur, option, callback)

```kotlin
fun createScheduleMeeting(
    title: String,
    planTime: Long,
    planDur: Int,
    option: CreateScheduleMeetingOption,
    callback: MeetingValueResultCallback<MeetingCreatedBean>
)
```

方法说明：创建预约会议。

参数说明：

| 参数 | 说明 |
| --- | --- |
| `title` | 会议标题。 |
| `planTime` | 计划开始时间，秒级 Unix 时间戳。 |
| `planDur` | 计划时长，单位分钟。 |
| `option` | 预约会议可选参数。 |
| `callback` | 成功返回会议 ID 与房间号的回调。 |

返回值说明：无（异步结果见回调）。

### updateMeetingBeforeStart(meetingId, option, callback)

```kotlin
fun updateMeetingBeforeStart(
    meetingId: String,
    option: UpdateMeetingOption,
    callback: MeetingResultCallback
)
```

方法说明：更新尚未开始的会议。

参数说明：

| 参数 | 说明 |
| --- | --- |
| `meetingId` | 目标会议 ID。 |
| `option` | 要更新的字段；未设置的可空字段不参与更新。 |
| `callback` | 更新结果回调。 |

返回值说明：无（异步结果见回调）。

### getMeetingList(page, perPage, callback)

```kotlin
fun getMeetingList(
    page: Int,
    perPage: Int,
    callback: MeetingValueResultCallback<MeetingPage<MeetInfo>>
)
```

方法说明：分页查询当前用户待开始或进行中的会议。

参数说明：

| 参数 | 说明 |
| --- | --- |
| `page` | 页码，从 `1` 开始。 |
| `perPage` | 每页最大条目数。 |
| `callback` | 成功返回会议分页结果的回调。 |

返回值说明：无（异步结果见回调）。

### getHistoryMeetingList(page, perPage, callback)

```kotlin
fun getHistoryMeetingList(
    page: Int,
    perPage: Int,
    callback: MeetingValueResultCallback<MeetingPage<MeetInfo>>
)
```

方法说明：分页查询当前用户的历史会议。

参数说明：

| 参数 | 说明 |
| --- | --- |
| `page` | 页码，从 `1` 开始。 |
| `perPage` | 每页最大条目数。 |
| `callback` | 成功返回历史会议分页结果的回调。 |

返回值说明：无（异步结果见回调）。

### getMeetingDetail(meetingId, callback)

```kotlin
fun getMeetingDetail(
    meetingId: String,
    callback: MeetingValueResultCallback<MeetDetail>
)
```

方法说明：按会议 ID 查询会议详情。

参数说明：

| 参数 | 说明 |
| --- | --- |
| `meetingId` | 目标会议 ID。 |
| `callback` | 成功返回 `MeetDetail` 的结果回调。 |

返回值说明：无（异步结果见回调）。

### getMeetingDetailByRoomNo(roomNo, callback)

```kotlin
fun getMeetingDetailByRoomNo(
    roomNo: String,
    callback: MeetingValueResultCallback<MeetDetail>
)
```

方法说明：按房间号查询会议详情。

参数说明：

| 参数 | 说明 |
| --- | --- |
| `roomNo` | 目标房间号。 |
| `callback` | 成功返回 `MeetDetail` 的结果回调。 |

返回值说明：无（异步结果见回调）。

### cancelMeetingBeforeStart(meetingId, callback)

```kotlin
fun cancelMeetingBeforeStart(meetingId: String, callback: MeetingResultCallback)
```

方法说明：取消尚未开始的会议。

参数说明：

| 参数 | 说明 |
| --- | --- |
| `meetingId` | 目标会议 ID。 |
| `callback` | 取消结果回调。 |

返回值说明：无（异步结果见回调）。

## 入会与离会

### enterMeeting(activity, roomNo, password, nick, avatar, streamVendor, isAudience, extendInfo, callback)

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
    callback: MeetingValueResultCallback<MeetingEnterInfo>
)
```

方法说明：按房间号完成详情查询、服务端入会和 SRTC 加入频道，并只返回一个最终结果。

参数说明：

| 参数 | 说明 |
| --- | --- |
| `activity` | SRTC 入会所需的当前 `Activity`。 |
| `roomNo` | 目标房间号。 |
| `password` | 入会密码；无密码时传 `null`。 |
| `nick` | 本次入会昵称。 |
| `avatar` | 头像地址或业务头像标识；没有时传空字符串。 |
| `streamVendor` | 服务端约定的流媒体厂商标识，例如 `wangsucdn`。 |
| `isAudience` | 是否以观众身份入会；观众不能开设备、共享或发流。 |
| `extendInfo` | 业务扩展字符串；没有时传 `null`。 |
| `callback` | 成功返回 `MeetingEnterInfo(meetingId, uid)` 的结果回调。 |

返回值说明：无（异步结果见回调）。

### enterMeetingByMeetingId(activity, meetingId, password, nick, avatar, streamVendor, isAudience, extendInfo, callback)

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
    callback: MeetingValueResultCallback<MeetingEnterInfo>
)
```

方法说明：按会议 ID 入会，流程和回调语义与 `enterMeeting()` 相同。

参数说明：

| 参数 | 说明 |
| --- | --- |
| `activity` | SRTC 入会所需的当前 `Activity`。 |
| `meetingId` | 目标会议 ID。 |
| `password` | 入会密码；无密码时传 `null`。 |
| `nick` | 本次入会昵称。 |
| `avatar` | 头像地址或业务头像标识。 |
| `streamVendor` | 服务端约定的流媒体厂商标识。 |
| `isAudience` | 是否以观众身份入会。 |
| `extendInfo` | 业务扩展字符串；没有时传 `null`。 |
| `callback` | 成功返回 `MeetingEnterInfo` 的结果回调。 |

返回值说明：无（异步结果见回调）。

### exitWaitingRoom(callback)

```kotlin
fun exitWaitingRoom(callback: MeetingResultCallback)
```

方法说明：在尚未完成 SRTC 入会时退出当前等候室。

参数说明：

| 参数 | 说明 |
| --- | --- |
| `callback` | 退出结果回调；缺少等候室上下文时返回 `WAITING_ROOM_CONTEXT_MISSING`。 |

返回值说明：无（异步结果见回调）。

### exitMeeting()

```kotlin
fun exitMeeting()
```

方法说明：离开当前会议，并停止该会议的采集、共享、远端订阅和后续事件分发。重复调用安全。

参数说明：无。

返回值说明：无（`Unit`）。

## 主持人房间控制

### adminDestroyMeeting(callback)

```kotlin
fun adminDestroyMeeting(callback: MeetingResultCallback)
```

方法说明：由主持人结束当前会议。

参数说明：

| 参数 | 说明 |
| --- | --- |
| `callback` | 结束会议结果回调。 |

返回值说明：无（异步结果见回调）。

### adminUpdateConferee(conferees, callback)

```kotlin
fun adminUpdateConferee(
    conferees: MutableList<String>,
    callback: MeetingResultCallback
)
```

方法说明：更新当前会议的会前受邀成员 UID 列表。

参数说明：

| 参数 | 说明 |
| --- | --- |
| `conferees` | 完整受邀成员 UID 列表。 |
| `callback` | 更新结果回调。 |

返回值说明：无（异步结果见回调）。

### adminUpdateRoomCameraState(selfUnMuteCameraDisabled, cameraDisabled, callback)

```kotlin
fun adminUpdateRoomCameraState(
    selfUnMuteCameraDisabled: Boolean,
    cameraDisabled: Boolean,
    callback: MeetingResultCallback
)
```

方法说明：同时更新房间全体摄像头禁用状态与成员自行解除策略。

参数说明：

| 参数 | 说明 |
| --- | --- |
| `selfUnMuteCameraDisabled` | `true` 表示成员不能自行解除禁画。 |
| `cameraDisabled` | `true` 表示全体摄像头禁用。 |
| `callback` | 更新结果回调。 |

返回值说明：无（异步结果见回调）。

### adminUpdateRoomSelfUnmuteCameraDisabled(selfUnMuteCameraDisabled, callback)

```kotlin
fun adminUpdateRoomSelfUnmuteCameraDisabled(
    selfUnMuteCameraDisabled: Boolean,
    callback: MeetingResultCallback
)
```

方法说明：只更新成员能否自行解除摄像头禁用。

参数说明：

| 参数 | 说明 |
| --- | --- |
| `selfUnMuteCameraDisabled` | `true` 表示禁止自行解除。 |
| `callback` | 更新结果回调。 |

返回值说明：无（异步结果见回调）。

### adminUpdateRoomMicState(selfUnMuteMicDisabled, micDisabled, callback)

```kotlin
fun adminUpdateRoomMicState(
    selfUnMuteMicDisabled: Boolean,
    micDisabled: Boolean,
    callback: MeetingResultCallback
)
```

方法说明：同时更新房间全体麦克风禁用状态与成员自行解除策略。

参数说明：

| 参数 | 说明 |
| --- | --- |
| `selfUnMuteMicDisabled` | `true` 表示成员不能自行解除禁音。 |
| `micDisabled` | `true` 表示全体麦克风禁用。 |
| `callback` | 更新结果回调。 |

返回值说明：无（异步结果见回调）。

### adminUpdateRoomSelfUnmuteMicDisabled(selfUnMuteMicDisabled, callback)

```kotlin
fun adminUpdateRoomSelfUnmuteMicDisabled(
    selfUnMuteMicDisabled: Boolean,
    callback: MeetingResultCallback
)
```

方法说明：只更新成员能否自行解除麦克风禁用。

参数说明：

| 参数 | 说明 |
| --- | --- |
| `selfUnMuteMicDisabled` | `true` 表示禁止自行解除。 |
| `callback` | 更新结果回调。 |

返回值说明：无（异步结果见回调）。

### adminUpdateRoomShareState(shareDisabled, callback)

```kotlin
fun adminUpdateRoomShareState(shareDisabled: Boolean, callback: MeetingResultCallback)
```

方法说明：更新房间共享禁用状态。

参数说明：

| 参数 | 说明 |
| --- | --- |
| `shareDisabled` | `true` 表示禁止成员发起共享。 |
| `callback` | 更新结果回调。 |

返回值说明：无（异步结果见回调）。

### adminUpdateRoomChatDisabled(chatDisabled, callback)

```kotlin
fun adminUpdateRoomChatDisabled(chatDisabled: Boolean, callback: MeetingResultCallback)
```

方法说明：更新房间文本聊天禁用状态。

参数说明：

| 参数 | 说明 |
| --- | --- |
| `chatDisabled` | `true` 表示禁用聊天。 |
| `callback` | 更新结果回调。 |

返回值说明：无（异步结果见回调）。

### adminUpdateRoomScreenshotDisabled(screenshotDisabled, callback)

```kotlin
fun adminUpdateRoomScreenshotDisabled(
    screenshotDisabled: Boolean,
    callback: MeetingResultCallback
)
```

方法说明：更新房间截屏禁用状态；应用仍需自行执行 Android 端的截屏限制。

参数说明：

| 参数 | 说明 |
| --- | --- |
| `screenshotDisabled` | `true` 表示业务上禁止截屏。 |
| `callback` | 更新结果回调。 |

返回值说明：无（异步结果见回调）。

### adminUpdateRoomWatermarkDisabled(watermarkDisabled, callback)

```kotlin
fun adminUpdateRoomWatermarkDisabled(
    watermarkDisabled: Boolean,
    callback: MeetingResultCallback
)
```

方法说明：更新房间水印禁用状态。

参数说明：

| 参数 | 说明 |
| --- | --- |
| `watermarkDisabled` | `true` 表示禁用水印。 |
| `callback` | 更新结果回调。 |

返回值说明：无（异步结果见回调）。

### adminUpdateRoomLocked(locked, callback)

```kotlin
fun adminUpdateRoomLocked(locked: Boolean, callback: MeetingResultCallback)
```

方法说明：更新房间锁定状态。

参数说明：

| 参数 | 说明 |
| --- | --- |
| `locked` | `true` 表示锁定房间。 |
| `callback` | 更新结果回调。 |

返回值说明：无（异步结果见回调）。

## 本地摄像头

### openCamera(view, preOption, callback)

```kotlin
fun openCamera(
    view: View?,
    preOption: PreOptionCamera?,
    callback: MeetingResultCallback
)
```

方法说明：只开启本地摄像头采集和预览，不请求会议权限，也不发布视频；初始化成功后可在会前调用。

参数说明：

| 参数 | 说明 |
| --- | --- |
| `view` | 可选预览控件；仅支持 SRTC 指定的 `VcsPlayerGlTextureView` / `VcsPlayerGlSurfaceView`。 |
| `preOption` | 摄像头预设；传 `null` 使用 SRTC 默认 480P 配置。 |
| `callback` | 物理采集稳定开启后的结果回调。 |

返回值说明：无（异步结果见回调）。

### openCameraAndPublish(view, preOption, callback)

```kotlin
fun openCameraAndPublish(
    view: View?,
    preOption: PreOptionCamera?,
    callback: MeetingResultCallback
)
```

方法说明：在当前会议中完成服务端授权、摄像头采集和 SRTC 发布。任一步失败都会回滚本次发布并关闭采集。

参数说明：

| 参数 | 说明 |
| --- | --- |
| `view` | 可选本地预览控件，类型限制同 `openCamera()`。 |
| `preOption` | 摄像头采集预设；传 `null` 使用默认配置。 |
| `callback` | 授权、采集和发布全部完成后的结果回调。 |

返回值说明：无（异步结果见回调）。

### closeCamera()

```kotlin
fun closeCamera()
```

方法说明：取消当前会议中的摄像头发布并停止本地采集；未入会时只停止本地采集。

参数说明：无。

返回值说明：无（`Unit`）。

### switchCamera(isFrontCamera)

```kotlin
fun switchCamera(isFrontCamera: Boolean)
```

方法说明：在前后置摄像头之间切换。

参数说明：

| 参数 | 说明 |
| --- | --- |
| `isFrontCamera` | `true` 使用前置摄像头，`false` 使用后置摄像头。 |

返回值说明：无（`Unit`）。

### getCameraDevices()

```kotlin
fun getCameraDevices(): List<CameraDeviceCapability>
```

方法说明：获取 SRTC 当前识别到的摄像头能力快照。

参数说明：无。

返回值说明：摄像头设备能力列表；没有可用设备时为空列表。

### switchCameraDevice(cameraId)

```kotlin
fun switchCameraDevice(cameraId: String)
```

方法说明：按 Camera2 设备 ID 切换摄像头输入。

参数说明：

| 参数 | 说明 |
| --- | --- |
| `cameraId` | `getCameraDevices()` 返回的摄像头 ID。 |

返回值说明：无（`Unit`）。

### switchFrontCameraMirror(open)

```kotlin
fun switchFrontCameraMirror(open: Boolean)
```

方法说明：设置前置摄像头预览镜像。只影响前置摄像头，状态会缓存并在重新采集后恢复。

参数说明：

| 参数 | 说明 |
| --- | --- |
| `open` | `true` 开启镜像，`false` 关闭镜像。 |

返回值说明：无（`Unit`）。

### isFrontCameraMirrorOpen()

```kotlin
fun isFrontCameraMirrorOpen(): Boolean
```

方法说明：查询前置摄像头预览镜像状态。

参数说明：无。

返回值说明：`true` 表示镜像已开启；当前默认开启。

### addPreview(view)

```kotlin
fun addPreview(view: View): Boolean
```

方法说明：把一个预览控件绑定到当前本地摄像头轨道。

参数说明：

| 参数 | 说明 |
| --- | --- |
| `view` | SRTC 支持的本地视频渲染控件。 |

返回值说明：`true` 表示绑定成功，`false` 表示控件类型无效或当前轨道不可用。

### removePreview(view)

```kotlin
fun removePreview(view: View?)
```

方法说明：移除本地摄像头预览控件。

参数说明：

| 参数 | 说明 |
| --- | --- |
| `view` | 要移除的控件；传 `null` 移除全部预览控件。 |

返回值说明：无（`Unit`）。

### replacePreview(views)

```kotlin
fun replacePreview(views: List<View>)
```

方法说明：用新列表整体替换本地摄像头预览控件。

参数说明：

| 参数 | 说明 |
| --- | --- |
| `views` | 新的预览控件列表，所有控件都必须是 SRTC 支持的类型。 |

返回值说明：无（`Unit`）。

### getAllPreview()

```kotlin
fun getAllPreview(): List<View>
```

方法说明：获取当前绑定的全部本地预览控件。

参数说明：无。

返回值说明：预览控件快照。

## 本地麦克风

### openMic(preOption, callback)

```kotlin
fun openMic(preOption: PreOptionMic?, callback: MeetingResultCallback)
```

方法说明：只开启本地麦克风采集，不请求会议权限，也不发布音频；初始化成功后可在会前调用。

参数说明：

| 参数 | 说明 |
| --- | --- |
| `preOption` | 麦克风预设；传 `null` 使用 SRTC 默认配置。 |
| `callback` | 物理采集稳定开启后的结果回调。 |

返回值说明：无（异步结果见回调）。

### openMicAndPublish(preOption, callback)

```kotlin
fun openMicAndPublish(
    preOption: PreOptionMic?,
    callback: MeetingResultCallback
)
```

方法说明：在当前会议中完成服务端授权、麦克风采集和 SRTC 发布。失败会回滚本次发布并关闭采集。

参数说明：

| 参数 | 说明 |
| --- | --- |
| `preOption` | 麦克风采集预设；传 `null` 使用默认配置。 |
| `callback` | 授权、采集和发布全部完成后的结果回调。 |

返回值说明：无（异步结果见回调）。

### closeMic()

```kotlin
fun closeMic()
```

方法说明：取消当前会议中的麦克风发布并停止本地采集；未入会时只停止本地采集。

参数说明：无。

返回值说明：无（`Unit`）。

### getMicVolume()

```kotlin
fun getMicVolume(): Int?
```

方法说明：获取采集中的实时麦克风音量。

参数说明：无。

返回值说明：dBFS 音量值；未采集时为 `null`。

### getMicDevices()

```kotlin
fun getMicDevices(): List<MicDeviceCapability>
```

方法说明：获取 SRTC 当前识别到的麦克风输入设备能力快照。

参数说明：无。

返回值说明：麦克风设备能力列表；没有可用设备时为空列表。

### switchMicDevice(deviceId)

```kotlin
fun switchMicDevice(deviceId: String)
```

方法说明：按设备 ID 切换麦克风输入。

参数说明：

| 参数 | 说明 |
| --- | --- |
| `deviceId` | `getMicDevices()` 返回的设备 ID。 |

返回值说明：无（`Unit`）。

## 屏幕共享

### initScreenShare(activity, notificationParam, preOpt)

```kotlin
fun initScreenShare(
    activity: Activity,
    notificationParam: ScreenNotificationOption?,
    preOpt: PreOptionScreen?
)
```

方法说明：创建或复用本地屏幕采集对象。该方法只初始化采集资源，不代表已向会议发布屏幕轨道。

参数说明：

| 参数 | 说明 |
| --- | --- |
| `activity` | 用于发起 Android MediaProjection 授权的 `Activity`。 |
| `notificationParam` | 前台服务通知配置；不使用通知栏时可传 `null`。 |
| `preOpt` | 屏幕采集预设；传 `null` 使用 SRTC 默认配置。 |

返回值说明：无（`Unit`）。采集状态通过 `screenCaptureEvent` 返回。

### startScreenShare(hasBar, callback)

```kotlin
fun startScreenShare(hasBar: Boolean, callback: MeetingResultCallback)
```

方法说明：执行 Android 授权、Meeting 共享请求、屏幕采集和 SRTC 轨道发布的完整流程。调用前应先执行 `initScreenShare()`。

参数说明：

| 参数 | 说明 |
| --- | --- |
| `hasBar` | 是否启用前台服务通知栏。 |
| `callback` | 全部步骤完成后的结果回调。 |

返回值说明：无（异步结果见回调）。

### stopScreenShare()

```kotlin
fun stopScreenShare()
```

方法说明：停止当前用户的屏幕共享，并协调与课程录制共用的共享轨道。

参数说明：无。

返回值说明：无（`Unit`）。

### confirmStartScreenShareAgree(targetId, hasBar, callback)

```kotlin
fun confirmStartScreenShareAgree(
    targetId: String,
    hasBar: Boolean,
    callback: MeetingResultCallback
)
```

方法说明：同意主持人的屏幕共享请求，并继续完成授权、采集和发布。

参数说明：

| 参数 | 说明 |
| --- | --- |
| `targetId` | 发起请求的主持人 UID。 |
| `hasBar` | 是否启用前台服务通知栏。 |
| `callback` | 服务端确认和本地共享全部完成后的结果回调。 |

返回值说明：无（异步结果见回调）。

### confirmStartScreenShareRefuse(targetId, callback)

```kotlin
fun confirmStartScreenShareRefuse(
    targetId: String,
    callback: MeetingResultCallback
)
```

方法说明：拒绝主持人的屏幕共享请求。

参数说明：

| 参数 | 说明 |
| --- | --- |
| `targetId` | 发起请求的主持人 UID。 |
| `callback` | 服务端确认结果回调。 |

返回值说明：无（异步结果见回调）。

## 白板共享

### requestShareBoard(callback)

```kotlin
fun requestShareBoard(callback: MeetingValueResultCallback<String>)
```

方法说明：请求开始白板共享。

参数说明：

| 参数 | 说明 |
| --- | --- |
| `callback` | 成功返回当前会议白板地址的结果回调。 |

返回值说明：无（异步结果见回调）。

### stopShareWhiteBoard()

```kotlin
fun stopShareWhiteBoard()
```

方法说明：停止当前用户的白板共享。

参数说明：无。

返回值说明：无（`Unit`）。

### confirmStartWhiteBoardShareAgree(targetId, callback)

```kotlin
fun confirmStartWhiteBoardShareAgree(
    targetId: String,
    callback: MeetingValueResultCallback<String>
)
```

方法说明：同意主持人的白板共享请求。

参数说明：

| 参数 | 说明 |
| --- | --- |
| `targetId` | 发起请求的主持人 UID。 |
| `callback` | 成功返回白板地址的结果回调。 |

返回值说明：无（异步结果见回调）。

### confirmStartWhiteBoardShareRefuse(targetId, callback)

```kotlin
fun confirmStartWhiteBoardShareRefuse(
    targetId: String,
    callback: MeetingResultCallback
)
```

方法说明：拒绝主持人的白板共享请求。

参数说明：

| 参数 | 说明 |
| --- | --- |
| `targetId` | 发起请求的主持人 UID。 |
| `callback` | 服务端确认结果回调。 |

返回值说明：无（异步结果见回调）。

## 房间消息与举手

### sendRoomChatMessage(targetId, msg, msgType, callback)

```kotlin
fun sendRoomChatMessage(
    targetId: String?,
    msg: String,
    msgType: ChatMsgType,
    callback: MeetingResultCallback
)
```

方法说明：发送房间聊天消息。

参数说明：

| 参数 | 说明 |
| --- | --- |
| `targetId` | 目标成员 UID；传 `null` 群发。 |
| `msg` | 消息内容。 |
| `msgType` | 文本、文件、图片或语音等聊天类型。 |
| `callback` | 消息提交结果回调。 |

返回值说明：无（异步结果见回调）。

### sendRoomCustomMessage(targetId, msg, callback)

```kotlin
fun sendRoomCustomMessage(
    targetId: String?,
    msg: String,
    callback: MeetingResultCallback
)
```

方法说明：发送应用自定义消息；接收方通过 `MeetingMessageEvent.onExtensionMessage()` 处理扩展消息。

参数说明：

| 参数 | 说明 |
| --- | --- |
| `targetId` | 目标成员 UID；传 `null` 群发。 |
| `msg` | 自定义消息内容。 |
| `callback` | 消息提交结果回调。 |

返回值说明：无（异步结果见回调）。

### getRoomChatMsgList(page, prePage, callback)

```kotlin
fun getRoomChatMsgList(
    page: Int,
    prePage: Int,
    callback: MeetingValueResultCallback<MeetingPage<ChatMsgBean>>
)
```

方法说明：分页查询当前会议聊天历史。

参数说明：

| 参数 | 说明 |
| --- | --- |
| `page` | 页码，从 `1` 开始。 |
| `prePage` | 每页最大条目数。参数名为历史拼写，含义等同 `perPage`。 |
| `callback` | 成功返回聊天记录分页结果的回调。 |

返回值说明：无（异步结果见回调）。

### requestHandUp(code, callback)

```kotlin
fun requestHandUp(code: HandUpType, callback: MeetingResultCallback)
```

方法说明：向主持人发起指定类型的举手申请。

参数说明：

| 参数 | 说明 |
| --- | --- |
| `code` | 举手申请类型。 |
| `callback` | 请求提交结果回调。 |

返回值说明：无（异步结果见回调）。

### cancelHandUp(code)

```kotlin
fun cancelHandUp(code: HandUpType)
```

方法说明：取消当前用户指定类型的举手申请。

参数说明：

| 参数 | 说明 |
| --- | --- |
| `code` | 要取消的举手类型。 |

返回值说明：无（`Unit`）。

## 设备开启请求回复

### confirmOpenCameraAgree(targetId, view, preOpt, callback)

```kotlin
fun confirmOpenCameraAgree(
    targetId: String,
    view: View?,
    preOpt: PreOptionCamera?,
    callback: MeetingResultCallback
)
```

方法说明：同意主持人打开摄像头的请求，并完成本地采集和发布。

参数说明：

| 参数 | 说明 |
| --- | --- |
| `targetId` | 发起请求的主持人 UID。 |
| `view` | 可选本地预览控件。 |
| `preOpt` | 摄像头采集预设；传 `null` 使用默认配置。 |
| `callback` | 服务端确认、采集与发布的结果回调。 |

返回值说明：无（异步结果见回调）。

### confirmOpenCameraRefuse(targetId, callback)

```kotlin
fun confirmOpenCameraRefuse(targetId: String, callback: MeetingResultCallback)
```

方法说明：拒绝主持人打开摄像头的请求。

参数说明：

| 参数 | 说明 |
| --- | --- |
| `targetId` | 发起请求的主持人 UID。 |
| `callback` | 服务端确认结果回调。 |

返回值说明：无（异步结果见回调）。

### confirmOpenMicAgree(targetId, preOpt, callback)

```kotlin
fun confirmOpenMicAgree(
    targetId: String,
    preOpt: PreOptionMic?,
    callback: MeetingResultCallback
)
```

方法说明：同意主持人打开麦克风的请求，并完成本地采集和发布。

参数说明：

| 参数 | 说明 |
| --- | --- |
| `targetId` | 发起请求的主持人 UID。 |
| `preOpt` | 麦克风采集预设；传 `null` 使用默认配置。 |
| `callback` | 服务端确认、采集与发布的结果回调。 |

返回值说明：无（异步结果见回调）。

### confirmOpenMicRefuse(targetId, callback)

```kotlin
fun confirmOpenMicRefuse(targetId: String, callback: MeetingResultCallback)
```

方法说明：拒绝主持人打开麦克风的请求。

参数说明：

| 参数 | 说明 |
| --- | --- |
| `targetId` | 发起请求的主持人 UID。 |
| `callback` | 服务端确认结果回调。 |

返回值说明：无（异步结果见回调）。

## 云录制与课程录制

### startCloudRecord(layoutData, callback)

```kotlin
fun startCloudRecord(
    layoutData: LayoutData?,
    callback: MeetingResultCallback
)
```

方法说明：启动当前会议的云端视频录制。

参数说明：

| 参数 | 说明 |
| --- | --- |
| `layoutData` | 可选录制布局；传 `null` 使用服务端默认布局。 |
| `callback` | 启动请求结果回调。实际任务状态通过 `MeetingRoomEvent.onCloudRecordStatusChange()` 通知。 |

返回值说明：无（异步结果见回调）。

### stopCloudRecord(callback)

```kotlin
fun stopCloudRecord(callback: MeetingResultCallback)
```

方法说明：停止当前会议的云端视频录制。

参数说明：

| 参数 | 说明 |
| --- | --- |
| `callback` | 停止请求结果回调。 |

返回值说明：无（异步结果见回调）。

### enableCourseRecordTrack(track, callback)

```kotlin
fun enableCourseRecordTrack(
    track: LocalCustomVideoTrack,
    callback: MeetingResultCallback
)
```

方法说明：把应用提供的自定义视频轨作为 `TRACK_SHARE` 发布，用于课程录制。该方法只处理媒体轨道，录制业务请求由应用另行发起。

参数说明：

| 参数 | 说明 |
| --- | --- |
| `track` | 应用持续写入课程画面的 `LocalCustomVideoTrack`。 |
| `callback` | 轨道发布结果回调。 |

返回值说明：无（异步结果见回调）。

### disableCourseRecordTrack()

```kotlin
fun disableCourseRecordTrack()
```

方法说明：取消课程录制共享轨发布；不会代替应用停止服务端录制任务。

参数说明：无。

返回值说明：无（`Unit`）。

## 音频路由与远端音频

### toggleRemoteAudioMute(mute)

```kotlin
fun toggleRemoteAudioMute(mute: Boolean)
```

方法说明：静音或恢复当前会议的远端合流音频播放。

参数说明：

| 参数 | 说明 |
| --- | --- |
| `mute` | `true` 静音，`false` 恢复播放。 |

返回值说明：无（`Unit`）。

### getAudioRouterManager()

```kotlin
fun getAudioRouterManager(): AudioRouterManager?
```

方法说明：获取 SRTC Engine 级音频路由管理器；同一生命周期重复调用返回缓存实例。

参数说明：无。

返回值说明：`AudioRouterManager?`；SDK 未就绪时为 `null`。调用方不得直接调用其 `release()`。

### releaseAudioRouterManager()

```kotlin
fun releaseAudioRouterManager()
```

方法说明：由 Meeting SDK 释放并清除缓存的音频路由管理器。重复调用安全。

参数说明：无。

返回值说明：无（`Unit`）。

## 远端成员视频

### startPlayRemoteVideo(uid, trackDesc, view, event, callback)

```kotlin
fun startPlayRemoteVideo(
    uid: String,
    trackDesc: String,
    view: View? = null,
    event: MeetingRemoteVideoEvent? = null,
    callback: MeetingValueResultCallback<RemoteVideoTrack>
)
```

方法说明：订阅指定成员的视频轨。SRTC 确认成功后返回对应的 `RemoteVideoTrack` 控制对象。

参数说明：

| 参数 | 说明 |
| --- | --- |
| `uid` | 远端成员 UID。 |
| `trackDesc` | 轨道描述，例如摄像头主流、辅流或共享流描述。 |
| `view` | 可选渲染控件；必须是 `VcsPlayerGlTextureView` 或 `VcsPlayerGlSurfaceView`。 |
| `event` | 可选的单轨接收与卡顿状态监听。 |
| `callback` | 成功返回 `RemoteVideoTrack` 的结果回调。 |

返回值说明：无（异步结果见回调）。

### stopPlayRemoteVideo(uid, trackDesc)

```kotlin
fun stopPlayRemoteVideo(uid: String, trackDesc: String)
```

方法说明：取消订阅指定成员的视频轨。

参数说明：

| 参数 | 说明 |
| --- | --- |
| `uid` | 订阅时使用的远端成员 UID。 |
| `trackDesc` | 订阅时使用的轨道描述。 |

返回值说明：无（`Unit`）。

### getRemoteVideoTrack(uid, trackDesc)

```kotlin
fun getRemoteVideoTrack(uid: String, trackDesc: String): RemoteVideoTrack?
```

方法说明：查询当前会议已缓存的指定远端视频控制轨。

参数说明：

| 参数 | 说明 |
| --- | --- |
| `uid` | 远端成员 UID。 |
| `trackDesc` | 轨道描述。 |

返回值说明：匹配的 `RemoteVideoTrack`；未入会或未创建控制轨时为 `null`。轨道渲染方法见 [SRTC RemoteVideoTrack](/zh/rtc/android/api-reference/RemoteVideoTrack)。

## 远端合成流

### startPlayRemoteMixture(view, event, callback)

```kotlin
fun startPlayRemoteMixture(
    view: View? = null,
    event: MeetingRemoteVideoEvent? = null,
    callback: MeetingValueResultCallback<RemoteVideoTrack>
)
```

方法说明：准备远端合成流控制轨并提交订阅请求。SRTC 当前没有为合成流提供订阅结果监听，因此成功只表示请求已提交，不表示已收到首帧。

参数说明：

| 参数 | 说明 |
| --- | --- |
| `view` | 可选合成流渲染控件。 |
| `event` | 可选的合成流接收状态监听。 |
| `callback` | 成功返回已准备的 `RemoteVideoTrack` 控制对象。 |

返回值说明：无（异步结果见回调）。

### stopPlayRemoteMixture()

```kotlin
fun stopPlayRemoteMixture()
```

方法说明：停止订阅远端合成流。

参数说明：无。

返回值说明：无（`Unit`）。

### getRemoteMixtureTrack()

```kotlin
fun getRemoteMixtureTrack(): RemoteVideoTrack?
```

方法说明：查询当前会议已缓存的远端合成流控制轨。

参数说明：无。

返回值说明：`RemoteVideoTrack?`；未入会或尚未创建时为 `null`。

## 网宿通用流

:::warning
本组接口只适用于网宿（WS）流媒体引擎，且必须已经入会。非 WS 引擎调用会返回底层不支持错误或空控制轨。
:::

### subscribeWsVideoStream(streamName, uid, trackDesc, view, event, callback)

```kotlin
fun subscribeWsVideoStream(
    streamName: String,
    uid: String = streamName,
    trackDesc: String,
    view: View? = null,
    event: MeetingRemoteVideoEvent? = null,
    callback: MeetingValueResultCallback<RemoteVideoTrack>
)
```

方法说明：按完整流名订阅一路网宿视频通用流，不依赖会议成员轨道列表。

参数说明：

| 参数 | 说明 |
| --- | --- |
| `streamName` | 完整视频流名，例如 `rtc_v_lesson_fknqb`。 |
| `uid` | 渲染路由标识；无特殊需求时使用默认的 `streamName`。 |
| `trackDesc` | 区分多路通用流的轨道描述。 |
| `view` | 可选视频渲染控件。 |
| `event` | 可选的单轨接收状态监听。 |
| `callback` | 成功返回视频控制轨的结果回调。 |

返回值说明：无（异步结果见回调）。

### subscribeWsAudioStream(streamName, uid, trackDesc, callback)

```kotlin
fun subscribeWsAudioStream(
    streamName: String,
    uid: String = streamName,
    trackDesc: String,
    callback: MeetingResultCallback
)
```

方法说明：按完整流名订阅一路网宿音频通用流，成功后由 SDK 自动外放。

参数说明：

| 参数 | 说明 |
| --- | --- |
| `streamName` | 完整音频流名，例如 `rtc_a_lesson_fknqb`。 |
| `uid` | 音频路由标识；无特殊需求时使用默认的 `streamName`。 |
| `trackDesc` | 区分多路通用流的轨道描述。 |
| `callback` | SRTC 订阅结果回调。 |

返回值说明：无（异步结果见回调）。

### unsubscribeWsVideoStream(streamName, uid, trackDesc)

```kotlin
fun unsubscribeWsVideoStream(
    streamName: String,
    uid: String = streamName,
    trackDesc: String
)
```

方法说明：取消网宿视频通用流订阅。控制轨会在离会时统一回收。

参数说明：

| 参数 | 说明 |
| --- | --- |
| `streamName` | 订阅时使用的完整流名。 |
| `uid` | 订阅时使用的路由标识。 |
| `trackDesc` | 订阅时使用的轨道描述。 |

返回值说明：无（`Unit`）。

### unsubscribeWsAudioStream(streamName, uid, trackDesc)

```kotlin
fun unsubscribeWsAudioStream(
    streamName: String,
    uid: String = streamName,
    trackDesc: String
)
```

方法说明：取消网宿音频通用流订阅。

参数说明：

| 参数 | 说明 |
| --- | --- |
| `streamName` | 订阅时使用的完整流名。 |
| `uid` | 订阅时使用的路由标识。 |
| `trackDesc` | 订阅时使用的轨道描述。 |

返回值说明：无（`Unit`）。

### getWsVideoStreamTrack(uid, trackDesc)

```kotlin
fun getWsVideoStreamTrack(uid: String, trackDesc: String): RemoteVideoTrack?
```

方法说明：获取或创建网宿视频通用流控制轨，可在订阅前先绑定渲染控件。

参数说明：

| 参数 | 说明 |
| --- | --- |
| `uid` | 视频路由标识。 |
| `trackDesc` | 轨道描述。 |

返回值说明：`RemoteVideoTrack?`；音频流、非 WS 引擎或未入会时为 `null`。
