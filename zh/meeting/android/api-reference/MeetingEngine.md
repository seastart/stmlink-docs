---
title: "MeetingEngine"
description: "Android SMeeting 会议 SDK MeetingEngine 接口参考"
---

说明：`MeetingEngine` 是 Meeting SDK 对外总入口，覆盖会前管理、入会会控、媒体能力与消息能力。

## 静态方法

### version()
```kotlin
fun version(): String
```
方法说明：版本信息  
参数说明：无。  
返回值说明：`String`，字符串结果。

### buildTime()
```kotlin
fun buildTime(): String
```
方法说明：构建时间  
参数说明：无。  
返回值说明：`String`，字符串结果。

### create()
```kotlin
fun create(app: Application): MeetingEngine
```
方法说明：创建 `MeetingEngine` 实例。  
参数说明：
- `app`：`Application`，应用上下文（建议传 `Application` 实例）。
返回值说明：`MeetingEngine`，`MeetingEngine` 实例。

## 核心属性

### infosManager（属性）
```kotlin
val infosManager: InfosManager
```
方法说明：信息管理类  
参数说明：无。  
返回值说明：`InfosManager`，属性值。

### imEvent（属性）
```kotlin
var imEvent: ImEvent?
```
方法说明：即时通讯回调  
参数说明：无。  
返回值说明：`ImEvent?`，属性值。

### roomEvent（属性）
```kotlin
var roomEvent: RoomEvent?
```
方法说明：房间事件回调  
参数说明：无。  
返回值说明：`RoomEvent?`，属性值。

### userEvent（属性）
```kotlin
var userEvent: UserEvent?
```
方法说明：用户事件回调  
参数说明：无。  
返回值说明：`UserEvent?`，属性值。

### roomMsgEvent（属性）
```kotlin
var roomMsgEvent: RoomMsgEvent?
```
方法说明：房间聊天事件回调  
参数说明：无。  
返回值说明：`RoomMsgEvent?`，属性值。

### mediaEvent（属性）
```kotlin
var mediaEvent: MediaEvent?
```
方法说明：媒体事件回调  
参数说明：无。  
返回值说明：`MediaEvent?`，属性值。

### enableClientCloudRecordCapture（属性）
```kotlin
var enableClientCloudRecordCapture: Boolean
```
方法说明：客户端是否负责云端录制数据采集  
参数说明：无。  
返回值说明：`Boolean`，属性值。

## 生命周期与配置

### getShareCustomVideoTrack()
```kotlin
fun getShareCustomVideoTrack(preOpt: PreOptionCustomVideo?): LocalCustomVideoTrack?
```
方法说明：获取用于云端录制的自定义视频轨，应用层可向该轨推送白板 YUV 数据  
参数说明：
- `preOpt`：`PreOptionCustomVideo?`，预设参数；为 `null` 时使用 SDK 默认预设。
返回值说明：`LocalCustomVideoTrack?`，本地自定义视频轨道；未就绪时返回 `null`。

### initSdk()
```kotlin
fun initSdk(meetToken: String, options: RTCMediaOptions?, listener: MeetingResultCallback?)
```
方法说明：初始化 sdk  
参数说明：
- `meetToken`：`String`，会议鉴权令牌，用于初始化 SDK 与后续会控请求。
- `options`：`RTCMediaOptions?`，流媒体参数配置；传 `null` 时使用默认媒体配置。
- `listener`：`MeetingResultCallback?`，结果回调，返回调用成功或失败信息。
返回值说明：无（`Unit`）。

### release()
```kotlin
fun release()
```
方法说明：销毁 MeetingEngine 实例  
参数说明：无。  
返回值说明：无（`Unit`）。

### updateMediaOptions()
```kotlin
fun updateMediaOptions(options: RTCMediaOptions)
```
方法说明：更新流媒体参数  
参数说明：
- `options`：`RTCMediaOptions`，流媒体参数配置；传 `null` 时使用默认媒体配置。
返回值说明：无（`Unit`）。

### getSelfInfo()
```kotlin
fun getSelfInfo(callback: Callback<Data<UserBean?>?>?)
```
方法说明：从后台获取自身用户信息  
参数说明：
- `callback`：`Callback<Data<UserBean?>?>?`，异步结果回调，返回接口执行结果或错误信息。
返回值说明：无（`Unit`）。

### getAgentList()
```kotlin
fun getAgentList(types: MutableList<AgentType>, keyword: String, page: Int, perPage: Int,
callback: Callback<Data2<List<AgentBean>>>)
```
方法说明：获取设备列表  
参数说明：
- `types`：`MutableList<AgentType>`，设备类型筛选列表。
- `keyword`：`String`，关键字，用于按名称或属性筛选结果。
- `page`：`Int`，分页页码（从 1 开始）。
- `perPage`：`Int`，每页数量。
- `callback`：`Callback<Data2<List<AgentBean>>>`，异步结果回调，返回接口执行结果或错误信息。
返回值说明：无（`Unit`）。

## IM 相关

### enableIm()
```kotlin
fun enableIm(callback: EnableImCallback)
```
方法说明：启动即时通讯  
参数说明：
- `callback`：`EnableImCallback`，异步结果回调，返回接口执行结果或错误信息。
返回值说明：无（`Unit`）。

### disableIm()
0
```kotlin
fun disableIm()
```
方法说明：关闭即时通讯  
参数说明：无。  
返回值说明：无（`Unit`）。

### callUser()
```kotlin
fun callUser(
targetUids: MutableList<String>,
callback: Callback<Data<String>>
)
```
方法说明：会议时呼叫人员  
参数说明：
- `targetUids`：`MutableList<String>`，被呼叫用户 UID 列表。
- `callback`：`Callback<Data<String>>`，异步结果回调，返回接口执行结果或错误信息。
返回值说明：无（`Unit`）。

## 会前会议管理

### createImmediateMeeting()
```kotlin
fun createImmediateMeeting(
title: String, option: CreateImmediateMeetingOption,
callback: Callback<Data<MeetingCreatedBean>>?
)
```
方法说明：创建即时会议房间  
参数说明：
- `title`：`String`，会议标题
- `option`：`CreateImmediateMeetingOption`，创建即时会议可选参数
- `callback`：`Callback<Data<MeetingCreatedBean>>?`，异步结果回调，返回接口执行结果或错误信息。
返回值说明：无（`Unit`）。

### createScheduleMeeting()
```kotlin
fun createScheduleMeeting(
title: String, planTime: Long, planDur: Int,
option: CreateScheduleMeetingOption,
callback: Callback<Data<MeetingCreatedBean>>?
)
```
方法说明：创建预约会议房间  
参数说明：
- `title`：`String`，会议标题
- `planTime`：`Long`，开始时间时间戳
- `planDur`：`Int`，会议时长
- `option`：`CreateScheduleMeetingOption`，创建预约会议可选参数
- `callback`：`Callback<Data<MeetingCreatedBean>>?`，异步结果回调，返回接口执行结果或错误信息。
返回值说明：无（`Unit`）。

### updateMeetingBeforeStart()
```kotlin
fun updateMeetingBeforeStart(
meetingId: String, option: UpdateMeetingOption,
callback: Callback<Data<String?>>
)
```
方法说明：会前更新会议  
参数说明：
- `meetingId`：`String`，会议id
- `option`：`UpdateMeetingOption`，修改会议可选参数
- `callback`：`Callback<Data<String?>>`，异步结果回调，返回接口执行结果或错误信息。
返回值说明：无（`Unit`）。

### getMeetingList()
```kotlin
fun getMeetingList(
page: Int, perPage: Int,
callback: Callback<Data2<List<MeetInfo>>>
)
```
方法说明：获取需要参加的会议列表  
参数说明：
- `page`：`Int`，分页页码（从 1 开始）。
- `perPage`：`Int`，每页数量。
- `callback`：`Callback<Data2<List<MeetInfo>>>`，异步结果回调，返回接口执行结果或错误信息。
返回值说明：无（`Unit`）。

### getHistoryMeetingList()
```kotlin
fun getHistoryMeetingList(
page: Int, perPage: Int,
callback: Callback<Data2<List<MeetInfo>>>
)
```
方法说明：获取历史会议列表  
参数说明：
- `page`：`Int`，分页页码（从 1 开始）。
- `perPage`：`Int`，每页数量。
- `callback`：`Callback<Data2<List<MeetInfo>>>`，异步结果回调，返回接口执行结果或错误信息。
返回值说明：无（`Unit`）。

### getMeetingDetail()
```kotlin
fun getMeetingDetail(
meetingId: String,
callback: Callback<Data<MeetDetail>>
)
```
方法说明：获取会议详情  
参数说明：
- `meetingId`：`String`，会议 ID。
- `callback`：`Callback<Data<MeetDetail>>`，异步结果回调，返回接口执行结果或错误信息。
返回值说明：无（`Unit`）。

### getMeetingDetailByRoomNo()
```kotlin
fun getMeetingDetailByRoomNo(
roomNo: String,
callback: Callback<Data<MeetDetail>>
)
```
方法说明：获取会议详情通过 roomNo  
参数说明：
- `roomNo`：`String`，会议房间号。
- `callback`：`Callback<Data<MeetDetail>>`，异步结果回调，返回接口执行结果或错误信息。
返回值说明：无（`Unit`）。

### cancelMeetingBeforeStart()
```kotlin
fun cancelMeetingBeforeStart(
meetingId: String,
callback: Callback<Data<String?>>
)
```
方法说明：会前取消会议  
参数说明：
- `meetingId`：`String`，会议 ID。
- `callback`：`Callback<Data<String?>>`，异步结果回调，返回接口执行结果或错误信息。
返回值说明：无（`Unit`）。

## 入会与离会

### enterMeeting()
```kotlin
fun enterMeeting(
activity: Activity, roomNo: String, password: String?, nick: String,
avatar: String, streamVendor: String, extendInfo: String?,
callback: EnterMeetingCallback
)
```
方法说明：进入会议  
参数说明：
- `activity`：`Activity`，activity
- `roomNo`：`String`，房间号
- `password`：`String?`，密码
- `nick`：`String`，入会名称
- `avatar`：`String`，用户头像 URL 或头像标识。
- `streamVendor`：`String`，流媒体厂商
- `extendInfo`：`String?`，扩展属性
- `callback`：`EnterMeetingCallback`，回调参数：`JoinRoomInfo`、`Room room`、`User me`、`List<User> members`。
返回值说明：无（`Unit`）。

### enterMeetingByMeetingId()
```kotlin
fun enterMeetingByMeetingId(
activity: Activity, meetingId: String, password: String?, nick: String,
avatar: String, streamVendor: String, extendInfo: String?,
callback: EnterMeetingCallback
)
```
方法说明：进入会议  
参数说明：
- `activity`：`Activity`，activity
- `meetingId`：`String`，会议id
- `password`：`String?`，密码
- `nick`：`String`，入会名称
- `avatar`：`String`，用户头像 URL 或头像标识。
- `streamVendor`：`String`，流媒体厂商
- `extendInfo`：`String?`，扩展属性
- `callback`：`EnterMeetingCallback`，回调参数：`JoinRoomInfo`、`Room room`、`User me`、`List<User> members`。
返回值说明：无（`Unit`）。

### exitMeeting()
```kotlin
fun exitMeeting()
```
方法说明：离开会议  
参数说明：无。  
返回值说明：无（`Unit`）。

### exitWaitingRoom()
```kotlin
fun exitWaitingRoom(callback: Callback<Data<String?>>?)
```
方法说明：退出等候室  
参数说明：
- `callback`：`Callback<Data<String?>>?`，结果回调
返回值说明：无（`Unit`）。

## 主持人会控

### adminDestroyMeeting()
```kotlin
fun adminDestroyMeeting(callback: Callback<Data<String?>>?)
```
方法说明：结束会议  
参数说明：
- `callback`：`Callback<Data<String?>>?`，回调
返回值说明：无（`Unit`）。

### adminUpdateConferee()
```kotlin
fun adminUpdateConferee(conferees: MutableList<String>, callback: Callback<Data<String?>>?)
```
方法说明：主持人更新受邀参会成员列表  
参数说明：
- `conferees`：`MutableList<String>`，受邀成员列表
- `callback`：`Callback<Data<String?>>?`，回调
返回值说明：无（`Unit`）。

### adminUpdateRoomCameraState()
```kotlin
fun adminUpdateRoomCameraState(
selfUnMuteCameraDisabled: Boolean, cameraDisabled: Boolean,
callback: Callback<Data<String?>>?
)
```
方法说明：主持人更新房间摄像头禁用状态  
参数说明：
- `selfUnMuteCameraDisabled`：`Boolean`，房间是否允许自我解除禁画状态，默认true，true-禁解除 false-不限制
- `cameraDisabled`：`Boolean`，房间视频禁用状态，默认false true-禁用 false-不禁用
- `callback`：`Callback<Data<String?>>?`，异步结果回调，返回接口执行结果或错误信息。
返回值说明：无（`Unit`）。

### adminUpdateRoomSelfUnmuteCameraDisabled()
```kotlin
fun adminUpdateRoomSelfUnmuteCameraDisabled(
selfUnMuteCameraDisabled: Boolean,
callback: Callback<Data<String?>>?
)
```
方法说明：更新房间摄像头允许自我解除  
参数说明：
- `selfUnMuteCameraDisabled`：`Boolean`，房间是否允许自我解除禁画状态，默认true，true-禁解除 false-不限制
- `callback`：`Callback<Data<String?>>?`，异步结果回调，返回接口执行结果或错误信息。
返回值说明：无（`Unit`）。

### adminUpdateRoomMicState()
```kotlin
fun adminUpdateRoomMicState(
selfUnMuteMicDisabled: Boolean,
micDisabled: Boolean,
callback: Callback<Data<String?>>?
)
```
方法说明：主持人更新房间麦克风禁用状态  
参数说明：
- `selfUnMuteMicDisabled`：`Boolean`，房间是否允许自我解除禁音状态 默认true，true-禁解除 false-不限制
- `micDisabled`：`Boolean`，房间音频禁用状态 默认false true-禁用 false-不禁用
- `callback`：`Callback<Data<String?>>?`，异步结果回调，返回接口执行结果或错误信息。
返回值说明：无（`Unit`）。

### adminUpdateRoomSelfUnmuteMicDisabled()
```kotlin
fun adminUpdateRoomSelfUnmuteMicDisabled(
selfUnMuteMicDisabled: Boolean,
callback: Callback<Data<String?>>?
)
```
方法说明：更新房间麦克风允许自我解除  
参数说明：
- `selfUnMuteMicDisabled`：`Boolean`，房间是否允许自我解除禁音状态 默认true，true-禁解除 false-不限制
- `callback`：`Callback<Data<String?>>?`，异步结果回调，返回接口执行结果或错误信息。
返回值说明：无（`Unit`）。

### adminUpdateRoomShareState()
```kotlin
fun adminUpdateRoomShareState(
shareDisabled: Boolean,
callback: Callback<Data<String?>>?
)
```
方法说明：更新房间共享状态  
参数说明：
- `shareDisabled`：`Boolean`，是否禁用房间共享能力。
- `callback`：`Callback<Data<String?>>?`，异步结果回调，返回接口执行结果或错误信息。
返回值说明：无（`Unit`）。

### adminUpdateRoomChatDisabled()
```kotlin
fun adminUpdateRoomChatDisabled(
chatDisabled: Boolean,
callback: Callback<Data<String?>>?
)
```
方法说明：主持人更新房间聊天禁用状态  
参数说明：
- `chatDisabled`：`Boolean`，房间文本消息禁用状态，默认false，true-禁用 false-不禁用
- `callback`：`Callback<Data<String?>>?`，回调
返回值说明：无（`Unit`）。

### adminUpdateRoomScreenshotDisabled()
```kotlin
fun adminUpdateRoomScreenshotDisabled(
screenshotDisabled: Boolean,
callback: Callback<Data<String?>>?
)
```
方法说明：主持人更新房间截屏功能禁用状态  
参数说明：
- `screenshotDisabled`：`Boolean`，截屏功能禁用状态 默认false true-禁用 false-不禁用
- `callback`：`Callback<Data<String?>>?`，异步结果回调，返回接口执行结果或错误信息。
返回值说明：无（`Unit`）。

### adminUpdateRoomWatermarkDisabled()
```kotlin
fun adminUpdateRoomWatermarkDisabled(
watermarkDisabled: Boolean,
callback: Callback<Data<String?>>?
)
```
方法说明：主持人更新房间水印功能禁用状态  
参数说明：
- `watermarkDisabled`：`Boolean`，水印禁用状态 默认false true-禁用 false-不禁用
- `callback`：`Callback<Data<String?>>?`，异步结果回调，返回接口执行结果或错误信息。
返回值说明：无（`Unit`）。

### adminUpdateRoomLocked()
```kotlin
fun adminUpdateRoomLocked(
locked: Boolean,
callback: Callback<Data<String?>>?
)
```
方法说明：主持人更新房间锁定状态  
参数说明：
- `locked`：`Boolean`，房间锁定状态，默认 false， true-开启 false-关闭
- `callback`：`Callback<Data<String?>>?`，异步结果回调，返回接口执行结果或错误信息。
返回值说明：无（`Unit`）。

### adminUpdateUserName()
```kotlin
fun adminUpdateUserName(
targetId: String, name: String,
callback: Callback<Data<String?>>?
)
```
方法说明：主持人更新用户名称  
参数说明：
- `targetId`：`String`，String  目标用户ID
- `name`：`String`，String  名称
- `callback`：`Callback<Data<String?>>?`，结果回调
返回值说明：无（`Unit`）。

### adminUpdateUserRole()
```kotlin
fun adminUpdateUserRole(
targetId: String, role: MemberRoleType,
callback: Callback<Data<String?>>?
)
```
方法说明：主持人更新用户角色身份  
参数说明：
- `targetId`：`String`，String  目标用户ID
- `role`：`MemberRoleType`，Int  角色 0普通成员 1主持人
- `callback`：`Callback<Data<String?>>?`，结果回调
返回值说明：无（`Unit`）。

### adminMoveHost()
```kotlin
fun adminMoveHost(targetId: String, callback: Callback<Data<String?>>?)
```
方法说明：主持人转移  
参数说明：
- `targetId`：`String`，String  目标用户ID
- `callback`：`Callback<Data<String?>>?`，结果回调
返回值说明：无（`Unit`）。

### adminUpdateUserDrawDisabled()
```kotlin
fun adminUpdateUserDrawDisabled(
targetId: String, drawDisabled: Boolean,
callback: Callback<Data<String?>>?
)
```
方法说明：主持人更新远端用户涂鸦禁用状态  
参数说明：
- `targetId`：`String`，String  目标用户ID
- `drawDisabled`：`Boolean`，涂鸦禁用状态，默认 true，true-禁用 false-不禁用
- `callback`：`Callback<Data<String?>>?`，结果回调
返回值说明：无（`Unit`）。

### adminUpdateUserChatDisabled()
```kotlin
fun adminUpdateUserChatDisabled(
targetId: String, chatDisabled: Boolean,
callback: Callback<Data<String?>>?
)
```
方法说明：主持人更新远端用户聊天禁用状态  
参数说明：
- `targetId`：`String`，String  目标用户ID
- `chatDisabled`：`Boolean`，聊天禁用状态，默认 false，true-禁用 false-不禁用
- `callback`：`Callback<Data<String?>>?`，结果回调
返回值说明：无（`Unit`）。

### adminRequestUserOpenCamera()
```kotlin
fun adminRequestUserOpenCamera(
targetId: String,
callback: Callback<Data<String?>>?
)
```
方法说明：主持人请求远端用户打开摄像头  
参数说明：
- `targetId`：`String`，String  目标用户ID
- `callback`：`Callback<Data<String?>>?`，结果回调
返回值说明：无（`Unit`）。

### adminCloseUserCamera()
```kotlin
fun adminCloseUserCamera(
targetId: String,
callback: Callback<Data<String?>>?
)
```
方法说明：主持人关闭远端用户摄像头  
参数说明：
- `targetId`：`String`，String  目标用户ID
- `callback`：`Callback<Data<String?>>?`，结果回调
返回值说明：无（`Unit`）。

### adminDisableUserCamera()
```kotlin
fun adminDisableUserCamera(
targetId: String, cameraDisabled: Boolean,
callback: Callback<Data<String?>>?
)
```
方法说明：主持人禁用远端用户摄像头(暂时不用)  
参数说明：
- `targetId`：`String`，目标用户 id
- `cameraDisabled`：`Boolean`，摄像头禁用状态，默认 false，true-禁用 false-不禁用
- `callback`：`Callback<Data<String?>>?`，结果回调
返回值说明：无（`Unit`）。

### adminRequestUserOpenMic()
```kotlin
fun adminRequestUserOpenMic(
targetId: String,
callback: Callback<Data<String?>>?
)
```
方法说明：主持人请求远端用户打开麦克风  
参数说明：
- `targetId`：`String`，String  目标用户ID
- `callback`：`Callback<Data<String?>>?`，结果回调
返回值说明：无（`Unit`）。

### adminCloseUserMic()
```kotlin
fun adminCloseUserMic(
targetId: String,
callback: Callback<Data<String?>>?
)
```
方法说明：主持人关闭远端用户麦克风  
参数说明：
- `targetId`：`String`，String  目标用户ID
- `callback`：`Callback<Data<String?>>?`，结果回调
返回值说明：无（`Unit`）。

### adminDisableUserMic()
```kotlin
fun adminDisableUserMic(
targetId: String, micDisabled: Boolean,
callback: Callback<Data<String?>>?
)
```
方法说明：主持人禁用远端用户麦克风(暂时不用)  
参数说明：
- `targetId`：`String`，目标用户 id
- `micDisabled`：`Boolean`，麦克风禁用状态，默认 false，true-禁用 false-不禁用
- `callback`：`Callback<Data<String?>>?`，结果回调
返回值说明：无（`Unit`）。

### adminRequestUserShare()
```kotlin
fun adminRequestUserShare(
targetId: String,
callback: Callback<Data<String?>>?
)
```
方法说明：主持人请求远端用户开始共享  
参数说明：
- `targetId`：`String`，目标用户 id
- `callback`：`Callback<Data<String?>>?`，结果回调
返回值说明：无（`Unit`）。

### adminStopRoomShare()
```kotlin
fun adminStopRoomShare(callback: Callback<Data<String?>>?)
```
方法说明：主持人停止房间共享  
参数说明：
- `callback`：`Callback<Data<String?>>?`，结果回调
返回值说明：无（`Unit`）。

### adminInviteAgent()
```kotlin
fun adminInviteAgent(agents: List<AgentRequestBean>, callback: Callback<Data<String?>>?)
```
方法说明：主持人邀请设备入会  
参数说明：
- `agents`：`List<AgentRequestBean>`，邀请设备请求列表
- `callback`：`Callback<Data<String?>>?`，结果回调
返回值说明：无（`Unit`）。

### adminKickUserOut()
```kotlin
fun adminKickUserOut(
targetId: String,
callback: Callback<Data<String?>>?
)
```
方法说明：主持人将远端用户踢出房间  
参数说明：
- `targetId`：`String`，String  目标用户ID
- `callback`：`Callback<Data<String?>>?`，结果回调
返回值说明：无（`Unit`）。

### adminConfirmHandUp()
```kotlin
fun adminConfirmHandUp(
targetId: String, code: HandUpType, approve: Boolean,
callback: Callback<Data<String?>>?
)
```
方法说明：主持人确认举手请求，同意或拒绝  
参数说明：
- `targetId`：`String`，String  目标用户ID
- `code`：`HandUpType`，举手类型，1:申请开音频 2:申请开视频 3:申请聊天 4:申请共享 5:申请涂鸦
- `approve`：`Boolean`，处理用户举手 true-同意 false-拒绝
- `callback`：`Callback<Data<String?>>?`，结果回调
返回值说明：无（`Unit`）。

### adminGetOnlineMembers()
```kotlin
fun adminGetOnlineMembers(meetingId: String?, page: Int, prePage: Int, callback: Callback<Data2<List<MemberBean>>> )
```
方法说明：主持人获取在线成员列表  
参数说明：
- `meetingId`：`String?`，String  会议id
- `page`：`Int`，Int  分页页码，从 1 开始
- `prePage`：`Int`，Int  每页数据量，最大1000，默认20
- `callback`：`Callback<Data2<List<MemberBean>>>`，结果回调
返回值说明：无（`Unit`）。

### adminUpdateRoomMCUMode()
```kotlin
fun adminUpdateRoomMCUMode()
```
方法说明：adminUpdateRoomMCUMode	更新房间MCU录制模式(后面做)  
参数说明：无。  
返回值说明：无（`Unit`）。

## 等候室与讨论组

### adminWaitingRoomDisabled()
```kotlin
fun adminWaitingRoomDisabled(
waitingRoomDisabled: Boolean,
callback: Callback<Data<String?>>?
)
```
方法说明：主持人启停等候室，默认关闭  
参数说明：
- `waitingRoomDisabled`：`Boolean`，是否禁用等待室 默认true true:禁用 false:不禁用
- `callback`：`Callback<Data<String?>>?`，结果回调
返回值说明：无（`Unit`）。

### adminMoveOutWaitingRoom()
```kotlin
fun adminMoveOutWaitingRoom(
uid: String?,
callback: Callback<Data<String?>>?
)
```
方法说明：主持人将成员从等候室移入会议  
参数说明：
- `uid`：`String?`，用户 UID；在等候室场景中为 `null` 时表示全部用户。
- `callback`：`Callback<Data<String?>>?`，结果回调
返回值说明：无（`Unit`）。

### adminMoveInWaitingRoom()
```kotlin
fun adminMoveInWaitingRoom(
uid: String,
nickName: String,
callback: Callback<Data<String?>>?
)
```
方法说明：主持人将成员从会议移入等候室  
参数说明：
- `uid`：`String`，目标用户 UID。
- `nickName`：`String`，用户显示名称。
- `callback`：`Callback<Data<String?>>?`，异步结果回调，返回接口执行结果或错误信息。
返回值说明：无（`Unit`）。

### adminGetWaitingRoomUsers()
```kotlin
fun adminGetWaitingRoomUsers(
callback: Callback<Data<List<WaitingRoomUserBean>>>
)
```
方法说明：主持人获取等候室用户列表  
参数说明：
- `callback`：`Callback<Data<List<WaitingRoomUserBean>>>`，结果回调
返回值说明：无（`Unit`）。

### createSubMeeting()
```kotlin
fun createSubMeeting(subMeetingTitles: MutableList<String>,
callback: Callback<Data<String?>>?
)
```
方法说明：创建讨论组  
参数说明：
- `subMeetingTitles`：`MutableList<String>`，子会议名称列表
- `callback`：`Callback<Data<String?>>?`，结果回调
返回值说明：无（`Unit`）。

### updateSubMeetingTitle()
```kotlin
fun updateSubMeetingTitle(
id: String, title: String, callback: Callback<Data<String?>>?
)
```
方法说明：更新讨论组标题  
参数说明：
- `id`：`String`，讨论组 id
- `title`：`String`，讨论组标题
- `callback`：`Callback<Data<String?>>?`，结果回调
返回值说明：无（`Unit`）。

### updateSubMeetingUsers()
```kotlin
fun updateSubMeetingUsers(
id: String, members: MutableList<MemberRequestBean>, callback: Callback<Data<String?>>?
)
```
方法说明：全量更新讨论组参与者  
参数说明：
- `id`：`String`，讨论组 id
- `members`：`MutableList<MemberRequestBean>`，讨论组参与者全量数据
- `callback`：`Callback<Data<String?>>?`，结果回调
返回值说明：无（`Unit`）。

### deleteSubMeeting()
```kotlin
fun deleteSubMeeting(
ids: MutableList<String>, callback: Callback<Data<String?>>?
)
```
方法说明：删除讨论组  
参数说明：
- `ids`：`MutableList<String>`，讨论组id列表
- `callback`：`Callback<Data<String?>>?`，结果回调
返回值说明：无（`Unit`）。

### getSubMeetingList()
```kotlin
fun getSubMeetingList(callback: Callback<Data<MutableList<SubMeetingBean>?>>)
```
方法说明：获取讨论组列表  
参数说明：
- `callback`：`Callback<Data<MutableList<SubMeetingBean>?>>`，结果回调
返回值说明：无（`Unit`）。

### startSubMeeting()
```kotlin
fun startSubMeeting(
ids: MutableList<String>,
callback: Callback<Data<String?>>?
)
```
方法说明：开始讨论组  
参数说明：
- `ids`：`MutableList<String>`，讨论组id列表
- `callback`：`Callback<Data<String?>>?`，异步结果回调，返回接口执行结果或错误信息。
返回值说明：无（`Unit`）。

### stopSubMeeting()
```kotlin
fun stopSubMeeting(
ids: MutableList<String>, callback: Callback<Data<String?>>?
)
```
方法说明：结束讨论组  
参数说明：
- `ids`：`MutableList<String>`，讨论组id列表
- `callback`：`Callback<Data<String?>>?`，结果回调
返回值说明：无（`Unit`）。

### moveSubMeetingUser()
```kotlin
fun moveSubMeetingUser(
fromId: String, toId: String?, uid: String,
callback: Callback<Data<String?>>?
)
```
方法说明：移动讨论组成员  
参数说明：
- `fromId`：`String`，来自哪个小组的id
- `toId`：`String?`，移动到哪个小组的id, 空表示主会场
- `uid`：`String`，移动用户的 uid
- `callback`：`Callback<Data<String?>>?`，结果回调
返回值说明：无（`Unit`）。

### updateEnterBeforeHostDisabled()
```kotlin
fun updateEnterBeforeHostDisabled(
meetingId: String, enterBeforeHostDisabled: Boolean,
callback: Callback<Data<String?>>?
)
```
方法说明：主持人更新在主持人前禁入会  
参数说明：
- `meetingId`：`String`，会议 id
- `enterBeforeHostDisabled`：`Boolean`，是否禁止在主持人之前进入会议
- `callback`：`Callback<Data<String?>>?`，结果回调
返回值说明：无（`Unit`）。

### helpSubMeeting()
```kotlin
fun helpSubMeeting(
meetingId: String, callback: Callback<Data<String?>>?
)
```
方法说明：讨论组请求帮助  
参数说明：
- `meetingId`：`String`，会议 ID。
- `callback`：`Callback<Data<String?>>?`，异步结果回调，返回接口执行结果或错误信息。
返回值说明：无（`Unit`）。

## 成员媒体控制

### updateName()
```kotlin
fun updateName(name: String, callback: Callback<Data<String?>>?)
```
方法说明：用户更新名称  
参数说明：
- `name`：`String`，姓名
- `callback`：`Callback<Data<String?>>?`，结果回调
返回值说明：无（`Unit`）。

### requestOpenCamera()
```kotlin
fun requestOpenCamera(
view: View?, preOpt: PreOptionCamera?, callback: Callback<Data<String?>>?
)
```
方法说明：用户请求打开摄像头  
参数说明：
- `view`：`View?`，预览画面渲染工具
- `preOpt`：`PreOptionCamera?`，打开摄像头预设参数
- `callback`：`Callback<Data<String?>>?`，结果回调
返回值说明：无（`Unit`）。

### closeCamera()
```kotlin
fun closeCamera()
```
方法说明：用户关闭摄像头  
参数说明：无。  
返回值说明：无（`Unit`）。

### switchCamera()
```kotlin
fun switchCamera(isFrontCamera: Boolean)
```
方法说明：切换前后置摄像头  
参数说明：
- `isFrontCamera`：`Boolean`，true: 前置；false：后置
返回值说明：无（`Unit`）。

### switchLight()
```kotlin
fun switchLight(open: Boolean)
```
方法说明：开关闪光灯  
参数说明：
- `open`：`Boolean`，true：打开；false：关闭
返回值说明：无（`Unit`）。

### addPreview()
```kotlin
fun addPreview(view: View)
```
方法说明：添加预览控件  
参数说明：
- `view`：`View`，View
返回值说明：无（`Unit`）。

### removePreview()
```kotlin
fun removePreview(view: View?)
```
方法说明：移除渲染控件  
参数说明：
- `view`：`View?`，如果 view 不为空，则移除指定控件；如果 view 为空，则移除所有控件
返回值说明：无（`Unit`）。

### replacePreView()
```kotlin
fun replacePreView(mViews: MutableList<View>)
```
方法说明：替换预览渲染控件  
参数说明：
- `mViews`：`MutableList<View>`，
返回值说明：无（`Unit`）。

### getAllPreview()
```kotlin
fun getAllPreview(): ArrayList<View>
```
方法说明：获取所有预览控件  
参数说明：无。  
返回值说明：`ArrayList<View>`，当前已绑定的本地预览视图列表。

### requestOpenMic()
```kotlin
fun requestOpenMic(preOpt: PreOptionMic?, callback: Callback<Data<String?>>?)
```
方法说明：用户请求打开麦克风  
参数说明：
- `preOpt`：`PreOptionMic?`，打开麦克风预设参数
- `callback`：`Callback<Data<String?>>?`，结果回调
返回值说明：无（`Unit`）。

### closeMic()
```kotlin
fun closeMic()
```
方法说明：用户关闭麦克风  
参数说明：无。  
返回值说明：无（`Unit`）。

## 屏幕共享与白板

### initScreenShare()
```kotlin
fun initScreenShare(
activity: Activity, notificationParam: ScreenNotificationOption?,
preOpt: PreOptionScreen?, event: ScreenShareEvent
)
```
方法说明：初始化屏幕共享  
参数说明：
- `activity`：`Activity`，活动
- `notificationParam`：`ScreenNotificationOption?`，通知栏参数，如果不启用通知栏，这个参数可以不设置
- `preOpt`：`PreOptionScreen?`，屏幕共享预设参数
- `event`：`ScreenShareEvent`，屏幕共享事件回调
返回值说明：无（`Unit`）。

### startScreenShare()
```kotlin
fun startScreenShare(hasBar: Boolean, listener: MeetingResultCallback?)
```
方法说明：开始屏幕共享  
参数说明：
- `hasBar`：`Boolean`，是否启用通知栏
- `listener`：`MeetingResultCallback?`，结果回调，返回调用成功或失败信息。
返回值说明：无（`Unit`）。

### stopScreenShare()
```kotlin
fun stopScreenShare()
```
方法说明：用户结束屏幕共享  
参数说明：无。  
返回值说明：无（`Unit`）。

### requestShareBoard()
```kotlin
fun requestShareBoard(callback: BoardShareCallback)
```
方法说明：用户请求共享白板  
参数说明：
- `callback`：`BoardShareCallback`，结果回调
返回值说明：无（`Unit`）。

### stopShareWhiteBoard()
```kotlin
fun stopShareWhiteBoard()
```
方法说明：用户请求停止共享白板  
参数说明：无。  
返回值说明：无（`Unit`）。

## 聊天与举手

### sendRoomChatMessage()
```kotlin
fun sendRoomChatMessage(
targetId: String?, msg: String, msgType: ChatMsgType,
callback: Callback<Data<String?>>?
)
```
方法说明：用户发送聊天消息，可单发和群发  
参数说明：
- `targetId`：`String?`，String  目标用户ID,传null发送为全体
- `msg`：`String`，String   消息
- `msgType`：`ChatMsgType`，Int   消息类型 1:文本(默认) 2:文件 3:图片 4:语音
- `callback`：`Callback<Data<String?>>?`，结果回调
返回值说明：无（`Unit`）。

### sendRoomCustomMessage()
```kotlin
fun sendRoomCustomMessage(
targetId: String?, msg: String,
callback: Callback<Data<String?>>?
)
```
方法说明：用户发送自定义消息，可单发和群发  
参数说明：
- `targetId`：`String?`，String?  目标用户ID,传null发送为全体
- `msg`：`String`，String?   消息内容
- `callback`：`Callback<Data<String?>>?`，结果回调
返回值说明：无（`Unit`）。

### getRoomChatMsgList()
```kotlin
fun getRoomChatMsgList(
page: Int, prePage: Int,
callback: Callback<Data2<List<ChatMsgBean?>>>
)
```
方法说明：获取聊天列表  
参数说明：
- `page`：`Int`，Int  页码
- `prePage`：`Int`，Int   每页个数
- `callback`：`Callback<Data2<List<ChatMsgBean?>>>`，结果回调
返回值说明：无（`Unit`）。

### requestHandUp()
```kotlin
fun requestHandUp(code: HandUpType, callback: Callback<Data<String?>>?)
```
方法说明：用户请求举手  
参数说明：
- `code`：`HandUpType`，举手申请类型 1:申请开音频 2:申请开视频 3:申请聊天 4:申请共享 5:申请涂鸦
- `callback`：`Callback<Data<String?>>?`，结果回调
返回值说明：无（`Unit`）。

### cancelHandUp()
```kotlin
fun cancelHandUp(code: HandUpType)
```
方法说明：用户取消举手  
参数说明：
- `code`：`HandUpType`，举手申请类型 1:申请开音频 2:申请开视频 3:申请聊天 4:申请共享 5:申请涂鸦
返回值说明：无（`Unit`）。

## 请求确认

### confirmOpenCameraAgree()
```kotlin
fun confirmOpenCameraAgree(
targetId: String, view: View?,
preOpt: PreOptionCamera?,
callback: Callback<Data<String?>>?)
```
方法说明：用户回复打开摄像头请求，同意  
参数说明：
- `targetId`：`String`，目标用户（主持人）id
- `view`：`View?`，渲染器控件
- `preOpt`：`PreOptionCamera?`，摄像头参数
- `callback`：`Callback<Data<String?>>?`，异步结果回调，返回接口执行结果或错误信息。
返回值说明：无（`Unit`）。

### confirmOpenCameraRefuse()
```kotlin
fun confirmOpenCameraRefuse(targetId: String, callback: Callback<Data<String?>>?)
```
方法说明：用户回复打开摄像头请求，拒绝  
参数说明：
- `targetId`：`String`，目标用户（主持人）id
- `callback`：`Callback<Data<String?>>?`，异步结果回调，返回接口执行结果或错误信息。
返回值说明：无（`Unit`）。

### confirmOpenMicAgree()
```kotlin
fun confirmOpenMicAgree(
targetId: String, preOpt: PreOptionMic?,
callback: Callback<Data<String?>>?
)
```
方法说明：用户回复打开麦克风请求， 同意  
参数说明：
- `targetId`：`String`，目标用户（主持人）id
- `preOpt`：`PreOptionMic?`，麦克风参数
- `callback`：`Callback<Data<String?>>?`，异步结果回调，返回接口执行结果或错误信息。
返回值说明：无（`Unit`）。

### confirmOpenMicRefuse()
```kotlin
fun confirmOpenMicRefuse(targetId: String, callback: Callback<Data<String?>>?)
```
方法说明：用户回复打开麦克风请求， 拒绝  
参数说明：
- `targetId`：`String`，目标用户（主持人）id
- `callback`：`Callback<Data<String?>>?`，结果回调
返回值说明：无（`Unit`）。

### confirmStartScreenShareAgree()
```kotlin
fun confirmStartScreenShareAgree(targetId: String, hasBar: Boolean, listener: MeetingResultCallback?)
```
方法说明：用户回复打开屏幕共享，同意  
参数说明：
- `targetId`：`String`，目标用户（主持人）id
- `hasBar`：`Boolean`，是否显示通知栏
- `listener`：`MeetingResultCallback?`，结果回调
返回值说明：无（`Unit`）。

### confirmStartScreenShareRefuse()
```kotlin
fun confirmStartScreenShareRefuse(targetId: String, callback: Callback<Data<String?>>?)
```
方法说明：用户回复打开屏幕共享，拒绝  
参数说明：
- `targetId`：`String`，
- `callback`：`Callback<Data<String?>>?`，异步结果回调，返回接口执行结果或错误信息。
返回值说明：无（`Unit`）。

### confirmStartWhiteBoardShareAgree()
```kotlin
fun confirmStartWhiteBoardShareAgree(targetId: String, callback: BoardShareCallback)
```
方法说明：用户回复打开白板共享，同意  
参数说明：
- `targetId`：`String`，
- `callback`：`BoardShareCallback`，
返回值说明：无（`Unit`）。

### confirmStartWhiteBoardShareRefuse()
```kotlin
fun confirmStartWhiteBoardShareRefuse(targetId: String, callback: Callback<Data<String?>>?)
```
方法说明：用户回复打开白板共享，拒绝  
参数说明：
- `targetId`：`String`，
- `callback`：`Callback<Data<String?>>?`，异步结果回调，返回接口执行结果或错误信息。
返回值说明：无（`Unit`）。

## 录制相关

### startCloudRecord()
```kotlin
fun startCloudRecord(layoutData: LayoutData?, callback: Callback<Data<String?>>?)
```
方法说明：开启云录制  
参数说明：
- `layoutData`：`LayoutData?`，云录制布局参数；传 `null` 时使用默认布局。
- `callback`：`Callback<Data<String?>>?`，异步结果回调，返回接口执行结果或错误信息。
返回值说明：无（`Unit`）。

### stopCloudRecord()
```kotlin
fun stopCloudRecord(callback: Callback<Data<String?>>?)
```
方法说明：停止云录制  
参数说明：
- `callback`：`Callback<Data<String?>>?`，异步结果回调，返回接口执行结果或错误信息。
返回值说明：无（`Unit`）。

### enableCourseRecordTrack()
```kotlin
fun enableCourseRecordTrack(track: LocalCustomVideoTrack, callback: CommonCallback?
```
方法说明：开启课程录制轨道  
参数说明：
- `track`：`LocalCustomVideoTrack`，用于课程录制发布的本地自定义视频轨道。
- `callback`：`CommonCallback?`，轨道发布完成回调
返回值说明：无（`Unit`）。

### disableCourseRecordTrack()
```kotlin
fun disableCourseRecordTrack()
```
方法说明：关闭课程录制轨道  
参数说明：无。  
返回值说明：无（`Unit`）。

## 音频与远端播放

### toggleRemoteAudioMute()
```kotlin
fun toggleRemoteAudioMute(mute: Boolean)
```
方法说明：切换远程音频的静音/取消静音状态  
参数说明：
- `mute`：`Boolean`，true：静音  false：取消静音
返回值说明：无（`Unit`）。

### getAudioRouterManager()
```kotlin
fun getAudioRouterManager(): AudioRouterManager?
```
方法说明：获取音频路由管理类  
参数说明：无。  
返回值说明：`AudioRouterManager?`，音频路由管理器实例；未初始化时返回 `null`。

### releaseAudioRouterManager()
```kotlin
fun releaseAudioRouterManager()
```
方法说明：释放音频路由管理类  
参数说明：无。  
返回值说明：无（`Unit`）。

### startPlayRemoteVideo()
```kotlin
fun startPlayRemoteVideo(
    uid: String,
    trackDesc: String,
    view: View? = null,
    event: RTCRemoteVideoEvent? = null
): RemoteVideoTrack?
```
方法说明：订阅视频流  
参数说明：
- `uid`：`String`，目标成员 UID。
- `trackDesc`：`String`，轨道描述（如 `camera_big`、`camera_small`、`screen`）。
- `view`：`View?`，视频渲染视图；传 `null` 时仅订阅不渲染。 默认值：`null`。
- `event`：`RTCRemoteVideoEvent?`，远端视频播放事件回调。 默认值：`null`。
返回值说明：`RemoteVideoTrack?`，远端视频轨道实例；未找到或未订阅时返回 `null`。

### stopPlayRemoteVideo()
```kotlin
fun stopPlayRemoteVideo(uid: String, trackDesc: String)
```
方法说明：取消订阅视频流  
参数说明：
- `uid`：`String`，目标成员 UID。
- `trackDesc`：`String`，轨道描述（如 `camera_big`、`camera_small`、`screen`）。
返回值说明：无（`Unit`）。

### getRemoteVideoTrack()
```kotlin
fun getRemoteVideoTrack(uid: String, trackDesc: String): RemoteVideoTrack?
```
方法说明：获取远端视频流的 VideoTrack  
参数说明：
- `uid`：`String`，目标成员 UID。
- `trackDesc`：`String`，轨道描述（如 `camera_big`、`camera_small`、`screen`）。
返回值说明：`RemoteVideoTrack?`，远端视频轨道实例；未找到或未订阅时返回 `null`。

### startPlayRemoteMixture()
```kotlin
fun startPlayRemoteMixture(
    view: View? = null,
    event: RTCRemoteVideoEvent? = null
): RemoteVideoTrack?
```
方法说明：开始播放远端合成流  
参数说明：
- `view`：`View?`，视频渲染视图；传 `null` 时仅订阅不渲染。
- `event`：`RTCRemoteVideoEvent?`，远端合成流播放事件回调。 默认值：`null`。
返回值说明：`RemoteVideoTrack?`，远端合成视频轨道实例；未找到时返回 `null`。

### stopPlayRemoteMixture()
```kotlin
fun stopPlayRemoteMixture()
```
方法说明：停止播放远端合成流  
参数说明：无。  
返回值说明：无（`Unit`）。

### getRemoteMixtureTrack()
```kotlin
fun getRemoteMixtureTrack(): RemoteVideoTrack?
```
方法说明：获取远端合成流的 VideoTrack  
参数说明：无。  
返回值说明：`RemoteVideoTrack?`，远端视频轨道实例；未找到或未订阅时返回 `null`。
