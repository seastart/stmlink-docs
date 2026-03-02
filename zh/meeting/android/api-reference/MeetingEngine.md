Meeting SDK 对外总入口

### version()
获取 RTC-SDK 版本号

```kotlin
fun version(): String
```

返回值

| RTC-SDK 版本信息 |
| --- |


### buildTime()
获取 RTC-SDK 构建时间信息

```kotlin
fun buildTime(): String
```

返回值 

| RTC-SDK 构建时间，精确到年月日 |
| --- |


## 初始化方法 SDK
### create()
用于创建实例

```kotlin
fun create(app: Application): MeetingEngine
```

参数

| app | application |
| --- | --- |


返回值 

| MeetingEngine 实例 |
| --- |


### initSdk()
初始化 SDK

```kotlin
fun initSdk(
    meetToken: String, options: RTCMediaOptions?, listener: MeetingResultCallback?
)
```

参数

| meetToken | String 类型，会议 token |
| --- | --- |
| options | RTCMediaOptions 类型，流媒体参数，详见数据类型中的  [RTCMediaOptions](https://www.yuque.com/anyconf/eanoso/mzyftti7zsfhs417#UxRKh)，<font style="color:#DF2A3F;">如无特殊要求，无需设置 。</font> |
| listener | 结果回调，详见 [MeetingResultCallback](https://www.yuque.com/anyconf/eanoso/put57w0owgogyplo)  |


### release()
销毁 MeetingEngine 实例，回收资源

```kotlin
fun release()
```

### updateMediaOptions()
更新流媒体参数

```java
fun updateMediaOptions(options: RTCMediaOptions)
```

参数

| options | RTCMediaOptions 类型，流媒体参数，详见数据类型中的  [RTCMediaOptions](https://www.yuque.com/anyconf/eanoso/mzyftti7zsfhs417#UxRKh)，<font style="color:#DF2A3F;">如无特殊要求，无需设置 。</font> |
| --- | --- |


### imEvent
设置、获取即时通讯回调

```java
var imEvent: ImEvent?
```

参数

| imEvent | ImEvent 类型，即时通讯回调接口类，详见 [ImEvent](https://www.yuque.com/anyconf/smeeting/ggs9x6lrxqsv22bl) |
| --- | --- |


### roomEvent
设置、获取房间事件回调

```java
var roomEvent: RoomEvent?
```

参数

| roomEvent | RoomEvent 类型，房间事件回调接口类，详见 [RoomEvent](https://www.yuque.com/anyconf/smeeting/ng82546vo88bmi2x) |
| --- | --- |


### userEvent
设置、获取用户事件回调

```java
var userEvent: UserEvent?
```

参数

| userEvent | UserEvent 类型，房间事件回调接口类，详见 [UserEvent](https://www.yuque.com/anyconf/smeeting/iza0mgvknc2lp3h5) |
| --- | --- |


### roomMsgEvent
设置、获取房间聊天事件回调

```java
var roomMsgEvent: RoomMsgEvent?
```

参数

| roomMsgEvent | RoomMsgEvent 类型，房间事件回调接口类，详见 [RoomMsgEvent](https://www.yuque.com/anyconf/smeeting/kf5nrkn95wwzeb27) |
| --- | --- |


### mediaEvent
设置、获取媒体事件回调

```java
var mediaEvent: MediaEvent?
```

参数

| mediaEvent | MediaEvent 类型，房间事件回调接口类，详见 [MediaEvent](https://www.yuque.com/anyconf/smeeting/zdpf2iza4qdr27ak) |
| --- | --- |


### enableIm(）
启动即时通讯

```java
fun enableIm(callback: EnableImCallback)
```

参数

| callback | EnableImCallback 类型，启动即时通讯结果回调接口类 |
| --- | --- |


EnableImCallback 详细说明

| 接口名称 | 接口说明 | 返回值 |
| --- | --- | --- |
| onSucceed | 启动即时通讯成功 | uid：String 类型，成员的 uid<br/>sid：String 类型，成员的会话 id |
| onFail | 启动即时通讯失败 | code：错误码<br/>msg：错误信息 |


### disableIm()
关闭即时通讯

```java
fun disableIm()
```

## 会议外操作
### createImmediateMeeting()
创建即时会议

```java
fun createImmediateMeeting(
        title: String, option: CreateImmediateMeetingOption,
        callback: Callback<Data<MeetingCreatedBean>>?
)
```

参数

| title | String 类型，会议名称 |
| --- | --- |
| option | CreateImmediateMeetingOption 类型，创建即时会议的可选参数，详见 [CreateImmediateMeetingOption](https://www.yuque.com/anyconf/smeeting/mzyftti7zsfhs417#bZLl6) |
| callback | Callback 类型，详见 [Callback<T extends BaseBean>](https://www.yuque.com/anyconf/smeeting/dqkggccykfrgogq5)<br/>MeetingCreatedBean，会议创建成功结果信息，详见 [MeetingCreatedBean](https://www.yuque.com/anyconf/smeeting/mzyftti7zsfhs417#rgrtP) |


### createScheduleMeeting
创建预约会议

```java
fun createScheduleMeeting(
        title: String, planTime: Long, planDur: Int,
        option: CreateScheduleMeetingOption,
        callback: Callback<Data<MeetingCreatedBean>>?
)
```

参数

| title | String 类型，会议名称 |
| --- | --- |
| planTime | Long 类型，计划开始时间 |
| planDur | Int 类型，计划持续时间 |
| option | CreateImmediateMeetingOption 类型，详见 [CreateImmediateMeetingOption](https://www.yuque.com/anyconf/smeeting/mzyftti7zsfhs417#bZLl6) |
| callback | Callback 类型，详见 [Callback<T extends BaseBean>](https://www.yuque.com/anyconf/smeeting/dqkggccykfrgogq5)<br/>MeetingCreatedBean，会议创建成功结果信息，详见 [MeetingCreatedBean](https://www.yuque.com/anyconf/smeeting/mzyftti7zsfhs417#rgrtP) |


### updateMeetingBeforeStart()
会前更新会议参数

```kotlin
fun updateMeetingBeforeStart(
        meetingId: String, option: UpdateMeetingOption,
        callback: Callback<Data<String?>>
)
```

参数

| meetingId | String 类型，会议 id |
| --- | --- |
| option | UpdateMeetingOption 类型，更新会议参数，详见 [UpdateMeetingOption](https://www.yuque.com/anyconf/smeeting/mzyftti7zsfhs417#KbkQL) |
| callback | 结果回调，详见 [Callback<Data<T extends BaseBean>>](https://www.yuque.com/anyconf/eanoso/dqkggccykfrgogq5) |


### getMeetingList()
获取需要参加的会议列表

```kotlin
fun getMeetingList(
        page: Int, perPage: Int,
        callback: Callback<Data2<List<MeetInfo>>>
)
```

参数

| page | Int 类型，页码 |
| --- | --- |
| perPage | Int 类型，当前页的元素项数 |
| callback | 结果回调，详见 [Callback<Data<T extends BaseBean>>](https://www.yuque.com/anyconf/eanoso/dqkggccykfrgogq5)，    MeetInfo：会议信息，详见 [MeetInfo](https://www.yuque.com/anyconf/smeeting/mzyftti7zsfhs417#ZYzii) |


### getHistoryMeetingList
获取历史会议列表

```kotlin
fun getHistoryMeetingList(
        page: Int, perPage: Int,
        callback: Callback<Data2<List<MeetInfo>>>
)
```

参数

| page | Int 类型，页码 |
| --- | --- |
| perPage | Int 类型，当前页的元素项数 |
| callback | 结果回调，详见 [Callback<Data<T extends BaseBean>>](https://www.yuque.com/anyconf/eanoso/dqkggccykfrgogq5)<br/>MeetInfo：会议信息，详见 [MeetInfo](https://www.yuque.com/anyconf/smeeting/mzyftti7zsfhs417#ZYzii) |


### getMeetingDetail
获取会议详情

```kotlin
fun getMeetingDetail(
        meetingId: String,
        callback: Callback<Data<MeetDetail>>
)
```

参数

| meetingId | String 类型，会议 id |
| --- | --- |
| callback | 结果回调，详见 [Callback<Data<T extends BaseBean>>](https://www.yuque.com/anyconf/eanoso/dqkggccykfrgogq5)<br/>MeetDetail：会议详情，详见 [MeetDetail](https://www.yuque.com/anyconf/smeeting/mzyftti7zsfhs417#lAg3T) |


### getMeetingDetailByRoomNo
通过房间号获取会议详情

```kotlin
fun getMeetingDetailByRoomNo(
    roomNo: String,
    callback: Callback<Data<MeetDetail>>
)
```

参数

| roomNo | String 类型，房间号 |
| --- | --- |
| callback | 结果回调，详见 [Callback<Data<T extends BaseBean>>](https://www.yuque.com/anyconf/eanoso/dqkggccykfrgogq5)<br/>MeetDetail：会议详情，详见 [MeetDetail](https://www.yuque.com/anyconf/smeeting/mzyftti7zsfhs417#lAg3T) |


### cancelMeetingBeforeStart()
会前取消会议

```kotlin
fun cancelMeetingBeforeStart(
        meetingId: String,
        callback: Callback<Data<String?>>
)
```

参数

| meetingId | String 类型，会议 id |
| --- | --- |
| callback | 结果回调，详见 [Callback<Data<T extends BaseBean>>](https://www.yuque.com/anyconf/eanoso/dqkggccykfrgogq5) |


### enterMeeting()
进入会议

```kotlin
fun enterMeeting(
    activity: Activity, roomNo: String, password: String?, 
    nick: String,avatar: String, extendInfo: String?, 
    callback: EnterMeetingCallback
)
```

参数

| activity | Activity 类型，当前活动页 |
| --- | --- |
| roomNo | String 类型，房间号 |
| password | String 类型，密码 |
| nick | String 类型，昵称 |
| avatar | String 类型，头像地址 |
| extendInfo | String 类型，扩展信息 |
| callback | EnterMeetingCallback，结果回调 |


EnterMeetingCallback 说明

| 接口名称 | 接口说明 | 返回值 |
| --- | --- | --- |
| onSucceed | 入会成功 | meetingId：String 类型，会议 id<br/>uid：String 类型，成员 uid |
| onFail | 入会失败 | code：错误码<br/>msg：错误信息 |


### enterMeetingByMeetingId()
通过会议号进入会议

```kotlin
fun enterMeetingByMeetingId(
    activity: Activity, meetingId: String, password: String?, nick: String,
    avatar: String, extendInfo: String?, callback: EnterMeetingCallback
)
```

参数

| activity | Activity 类型，当前活动页 |
| --- | --- |
| meetingId | String 类型，会议号 |
| password | String 类型，密码 |
| nick | String 类型，昵称 |
| avatar | String 类型，头像地址 |
| extendInfo | String 类型，扩展信息 |
| callback | EnterMeetingCallback，结果回调 |


EnterMeetingCallback 说明

| 接口名称 | 接口说明 | 返回值 |
| --- | --- | --- |
| onSucceed | 入会成功 | meetingId：String 类型，会议 id<br/>uid：String 类型，成员 uid |
| onFail | 入会失败 | code：错误码<br/>msg：错误信息 |


### exitMeeting()
离开会议

```kotlin
fun exitMeeting() 
```

### exitWaitingRoom()
退出等候室

```kotlin
fun exitWaitingRoom(callback: Callback<Data<String?>>?)
```

参数

| callback | 结果回调，详见 [Callback<Data<T extends BaseBean>>](https://www.yuque.com/anyconf/eanoso/dqkggccykfrgogq5) |
| --- | --- |


## 主持人操作
### adminDestroyMeeting()
结束会议

```kotlin
fun adminDestroyMeeting(callback: Callback<Data<String?>>?)
```

参数

| callback | 结果回调，详见 [Callback<Data<T extends BaseBean>>](https://www.yuque.com/anyconf/eanoso/dqkggccykfrgogq5) |
| --- | --- |


### adminUpdateConferee()
主持人更新受邀参会成员列表

```kotlin
fun adminUpdateConferee(
    onferees: MutableList<String>, 
    callback: Callback<Data<String?>>?
)
```

参数

| onferees | MutableList<String> 类型，受邀成员列表，item 为 uid |
| --- | --- |
| callback | 结果回调，详见 [Callback<Data<T extends BaseBean>>](https://www.yuque.com/anyconf/eanoso/dqkggccykfrgogq5) |


### adminUpdateRoomCameraState()
主持人更新房间摄像头禁用状态

```kotlin
fun adminUpdateRoomCameraState(
    selfUnMuteCameraDisabled: Boolean, cameraDisabled: Boolean,
    callback: Callback<Data<String?>>?
)
```

参数

| selfUnMuteCameraDisabled | Boolean 类型，房间是否自我解除禁画状态<br/>默认true，true-禁解除 false-不限制 |
| --- | --- |
| cameraDisabled | Boolean 类型，房间视频禁用状态<br/>默认true true-禁止 false-不禁止 |
| callback | 结果回调，详见 [Callback<Data<T extends BaseBean>>](https://www.yuque.com/anyconf/eanoso/dqkggccykfrgogq5) |


### adminUpdateRoomSelfUnmuteCameraDisabled()
更新房间摄像头允许自我解除

```kotlin
fun adminUpdateRoomSelfUnmuteCameraDisabled(
    selfUnMuteCameraDisabled: Boolean,
    callback: Callback<Data<String?>>?
)
```

参数

| selfUnMuteCameraDisabled | Boolean 类型，房间是否允许自我解除禁画状态<br/>默认true，true-禁解除；false-不限制 |
| --- | --- |
| callback | 结果回调，详见 [Callback<Data<T extends BaseBean>>](https://www.yuque.com/anyconf/eanoso/dqkggccykfrgogq5) |


### adminUpdateRoomMicState()
主持人更新房间麦克风禁用状态

```kotlin
fun adminUpdateRoomMicState(
    selfUnMuteMicDisabled: Boolean,micDisabled: Boolean,
    callback: Callback<Data<String?>>?
)
```

参数

| selfUnMuteMicDisabled | Boolean 类型，房间允许自我解除禁音状态<br/>默认true，true-禁解除 false-不限制 |
| --- | --- |
| micDisabled | Boolean 类型，房间音频禁用状态<br/>默认true true-禁止 false-不禁止 |
| callback | 结果回调，详见 [Callback<Data<T extends BaseBean>>](https://www.yuque.com/anyconf/eanoso/dqkggccykfrgogq5) |


### adminUpdateRoomSelfUnmuteMicDisabled()
更新房间麦克风允许自我解除

```kotlin
fun adminUpdateRoomSelfUnmuteMicDisabled(
    selfUnMuteMicDisabled: Boolean,
    callback: Callback<Data<String?>>?
)
```

参数

| selfUnMuteMicDisabled | Boolean 类型，房间是否允许自我解除禁音状态<br/>默认true，true-禁解除 false-不限制 |
| --- | --- |
| callback | 结果回调，详见 [Callback<Data<T extends BaseBean>>](https://www.yuque.com/anyconf/eanoso/dqkggccykfrgogq5) |


### adminUpdateRoomState()
更新房间共享状态

```kotlin
fun adminUpdateRoomState(
    shareDisabled: Boolean,
    callback: Callback<Data<String?>>?
)
```

参数

| shareDisabled | Boolean 类型，房间共享禁用状态<br/>默认false，true-禁用 false-不禁用 |
| --- | --- |
| callback | 结果回调，详见 [Callback<Data<T extends BaseBean>>](https://www.yuque.com/anyconf/eanoso/dqkggccykfrgogq5) |


### adminUpdateRoomChatDisabled()
主持人更新房间聊天禁用状态

```kotlin
fun adminUpdateRoomChatDisabled(
    chatDisabled: Boolean,
    callback: Callback<Data<String?>>?
)
```

参数

| chatDisabled | Boolean 类型， 房间文本消息禁用状态。<br/>默认false，true-禁用；false-不禁用 |
| --- | --- |
| callback | 结果回调，详见 [Callback<Data<T extends BaseBean>>](https://www.yuque.com/anyconf/eanoso/dqkggccykfrgogq5) |


### adminUpdateRoomScreenshotDisabled()
主持人更新房间截屏功能禁用状态

```kotlin
fun adminUpdateRoomScreenshotDisabled(
    screenshotDisabled: Boolean,
    callback: Callback<Data<String?>>?
)
```

参数

| screenshotDisabled | Boolean 类型， 截屏功能禁用状态<br/>默认false，true-禁用；false-不禁用 |
| --- | --- |
| callback | 结果回调，详见 [Callback<Data<T extends BaseBean>>](https://www.yuque.com/anyconf/eanoso/dqkggccykfrgogq5) |


### adminUpdateRoomWatermarkDisabled()
主持人更新房间水印功能禁用状态

```kotlin
fun adminUpdateRoomWatermarkDisabled(
    watermarkDisabled: Boolean,
    callback: Callback<Data<String?>>?
)
```

参数

| watermarkDisabled | Boolean 类型， 水印禁用状态<br/>默认false，true-禁用；false-不禁用 |
| --- | --- |
| callback | 结果回调，详见 [Callback<Data<T extends BaseBean>>](https://www.yuque.com/anyconf/eanoso/dqkggccykfrgogq5) |


### adminUpdateRoomLocked()
主持人更新房间锁定状态

```kotlin
fun adminUpdateRoomLocked(
    locked: Boolean,
    callback: Callback<Data<String?>>?
)
```

参数

| locked | Boolean 类型， 房间锁定状态<br/>默认false，true-启用；false-不启用 |
| --- | --- |
| callback | 结果回调，详见 [Callback<Data<T extends BaseBean>>](https://www.yuque.com/anyconf/eanoso/dqkggccykfrgogq5) |


### adminUpdateUserName()
主持人更新用户名称

```kotlin
fun adminUpdateUserName(
    targetId: String, name: String,
    callback: Callback<Data<String?>>?
)
```

参数

| targetId | String 类型，目标用户 uid |
| --- | --- |
| name | String 类型，新昵称 |
| callback | 结果回调，详见 [Callback<Data<T extends BaseBean>>](https://www.yuque.com/anyconf/eanoso/dqkggccykfrgogq5) |


### adminUpdateUserRole()
主持人更新用户角色身份

```kotlin
fun adminUpdateUserRole(
    targetId: String, role: MemberRoleType,
    callback: Callback<Data<String?>>?
)
```

参数

| targetId | String 类型，目标用户 uid |
| --- | --- |
| role | MemberRoleType 类型，新的成员角色<br/>详见枚举类型中的 [MemberRoleType](https://www.yuque.com/anyconf/eanoso/sly78y2qziqggiwx#nFCVP) |
| callback | 结果回调，详见 [Callback<Data<T extends BaseBean>>](https://www.yuque.com/anyconf/eanoso/dqkggccykfrgogq5) |


### adminMoveHost()
主持人转移

```kotlin
fun adminMoveHost(targetId: String, callback: Callback<Data<String?>>?)
```

参数

| targetId | String 类型，目标用户 uid |
| --- | --- |
| callback | 结果回调，详见 [Callback<Data<T extends BaseBean>>](https://www.yuque.com/anyconf/eanoso/dqkggccykfrgogq5) |


### adminUpdateUserChatDisabled()
主持人更新远端用户聊天禁用状态

```kotlin
fun adminUpdateUserChatDisabled(
    targetId: String, chatDisabled: Boolean,
    callback: Callback<Data<String?>>?
)
```

参数

| targetId | String 类型，目标用户 uid |
| --- | --- |
| chatDisabled | Boolean 类型，聊天禁用状态<br/>默认 false，true-禁用 false-不禁用 |
| callback | 结果回调，详见 [Callback<Data<T extends BaseBean>>](https://www.yuque.com/anyconf/eanoso/dqkggccykfrgogq5) |


### adminRequestUserOpenCamera()
主持人请求远端用户打开摄像头

```kotlin
fun adminRequestUserOpenCamera(
    targetId: String,
    callback: Callback<Data<String?>>?
)
```

参数

| targetId | String 类型，目标用户 uid |
| --- | --- |
| callback | 结果回调，详见 [Callback<Data<T extends BaseBean>>](https://www.yuque.com/anyconf/eanoso/dqkggccykfrgogq5) |


### adminCloseUserCamera()
主持人关闭远端用户摄像头

```kotlin
fun adminCloseUserCamera(
    targetId: String,
    callback: Callback<Data<String?>>?
)
```

参数

| targetId | String 类型，目标用户 uid |
| --- | --- |
| callback | 结果回调，详见 [Callback<Data<T extends BaseBean>>](https://www.yuque.com/anyconf/eanoso/dqkggccykfrgogq5) |


### adminDisableUserCamera()
主持人禁用远端用户摄像头（暂未实现）

```kotlin
fun adminDisableUserCamera(
    targetId: String, cameraDisabled: Boolean,
    callback: Callback<Data<String?>>?
)
```

参数

| targetId | String 类型，目标用户 uid |
| --- | --- |
| cameraDisabled | Boolean 类型，摄像头禁用状态<br/>默认值 false，ture-禁用  false-不禁用 |
| callback | 结果回调，详见 [Callback<Data<T extends BaseBean>>](https://www.yuque.com/anyconf/eanoso/dqkggccykfrgogq5) |


### adminRequestUserOpenMic()
主持人请求远端用户打开麦克风

```kotlin
fun adminRequestUserOpenMic(
    targetId: String,
    callback: Callback<Data<String?>>?
)
```

参数

| targetId | String 类型，目标用户 uid |
| --- | --- |
| callback | 结果回调，详见 [Callback<Data<T extends BaseBean>>](https://www.yuque.com/anyconf/eanoso/dqkggccykfrgogq5) |


### adminCloseUserMic()
主持人关闭远端用户麦克风

```kotlin
fun adminCloseUserMic(
    targetId: String,
    callback: Callback<Data<String?>>?
)
```

参数

| targetId | String 类型，目标用户 uid |
| --- | --- |
| callback | 结果回调，详见 [Callback<Data<T extends BaseBean>>](https://www.yuque.com/anyconf/eanoso/dqkggccykfrgogq5) |


### adminDisableUserMic()
主持人禁用远端用户麦克风(暂未实现)

```kotlin
fun adminDisableUserMic(
    targetId: String, micDisabled: Boolean,
    callback: Callback<Data<String?>>?
)
```

参数

| targetId | String 类型，目标用户 uid |
| --- | --- |
| micDisabled | Boolean 类型，麦克风禁用状态<br/>默认值 false，true-禁用 false-不禁用 |
| callback | 结果回调，详见 [Callback<Data<T extends BaseBean>>](https://www.yuque.com/anyconf/eanoso/dqkggccykfrgogq5) |


### adminStopRoomShare()
主持人停止房间共享

```kotlin
fun adminStopRoomShare(callback: Callback<Data<String?>>?)
```

参数

| callback | 结果回调，详见 [Callback<Data<T extends BaseBean>>](https://www.yuque.com/anyconf/eanoso/dqkggccykfrgogq5) |
| --- | --- |


### adminInviteAgent()
主持人邀请设备入会

```kotlin
fun adminInviteAgent(agents: List<AgentRequestBean>, callback: Callback<Data<String?>>?)
```

参数

| agents | List<AgentRequestBean> 类型，邀请设备请求列表<br/>AgentRequestBean，邀请设备请求信息，详见 [AgentRequestBean](https://www.yuque.com/anyconf/smeeting/mzyftti7zsfhs417#RmlXb) |
| --- | --- |
| callback | 结果回调，详见 [Callback<Data<T extends BaseBean>>](https://www.yuque.com/anyconf/eanoso/dqkggccykfrgogq5) |


### adminKickUserOut()
主持人将远端用户踢出会议

```kotlin
fun adminKickUserOut(
    targetId: String,
    callback: Callback<Data<String?>>?
)
```

参数

| targetId | String 类型，目标用户 uid |
| --- | --- |
| callback | 结果回调，详见 [Callback<Data<T extends BaseBean>>](https://www.yuque.com/anyconf/eanoso/dqkggccykfrgogq5) |


### adminConfirmHandup()
主持人确认举手请求，同意或拒绝

```kotlin
fun adminConfirmHandup(
    targetId: String, 
    code: HandupType, 
    approve: Boolean,
    callback: Callback<Data<String?>>?
)
```

参数

| targetId | String 类型，目标用户 uid |
| --- | --- |
| code | HandupType 类型，举手申请类型，详见枚举类型中的 [HandupType](https://www.yuque.com/anyconf/eanoso/sly78y2qziqggiwx#lWByu) |
| approve | Boolean 类型，处理结果，true-同意，false-不同意 |
| callback | 结果回调，详见 [Callback<Data<T extends BaseBean>>](https://www.yuque.com/anyconf/eanoso/dqkggccykfrgogq5) |


### adminGetOnlineMembers()
主持人获取在线成员列表

```kotlin
fun adminGetOnlineMembers(
    meetingId: String?, page: Int, prePage: Int, 
    callback: Callback<Data2<List<MemberBean>>> 
)
```

参数

| meetingId | String 类型，会议 id |
| --- | --- |
| page | Int 类型，分页页码，从 1 开始 |
| prePage | Int 类型，每页数量，最大 1000，默认 20 |
| callback | 结果回调，详见 [Callback<Data<T extends BaseBean>>](https://www.yuque.com/anyconf/eanoso/dqkggccykfrgogq5)<br/>MemberBean：成员信息，详见 [MemberBean](https://www.yuque.com/anyconf/smeeting/mzyftti7zsfhs417#QbfVP) |


### adminWaitingRoomDisabled()
主持人启停等候室，默认关闭

```kotlin
fun adminWaitingRoomDisabled(
    waitingRoomDisabled: Boolean,
    callback: Callback<Data<String?>>?
)
```

参数

| waitingRoomDisabled | Boolean 类型，是否禁用等候室。ture：禁用；false：不禁用。默认为 false |
| --- | --- |
| callback | 结果回调，详见 [Callback<Data<T extends BaseBean>>](https://www.yuque.com/anyconf/eanoso/dqkggccykfrgogq5) |


### adminMoveOutWaitingRoom()
主持人将成员从等候室移入会议

```kotlin
fun adminMoveOutWaitingRoom(
    uid: String?,
    callback: Callback<Data<String?>>?
)
```

参数

| uid | String 类型，用户 id |
| --- | --- |
| callback | 结果回调，详见 [Callback<Data<T extends BaseBean>>](https://www.yuque.com/anyconf/eanoso/dqkggccykfrgogq5) |


### adminMoveInWaitingRoom(）
主持人将成员从会议移入等候室

```kotlin
fun adminMoveInWaitingRoom(
    uid: String,
    nickName: String,
    callback: Callback<Data<String?>>?
)
```

参数

| uid | String 类型，用户 id |
| --- | --- |
| nickName | String 类型，用户昵称 |
| callback | 结果回调，详见 [Callback<Data<T extends BaseBean>>](https://www.yuque.com/anyconf/eanoso/dqkggccykfrgogq5) |


### adminGetWaitingRoomUsers()
主持人获取等候室用户列表

```kotlin
fun adminGetWaitingRoomUsers(
    callback: Callback<Data<List<WaitingRoomUserBean>>>
)
```

参数

| callback | 结果回调，详见 [Callback<Data<T extends BaseBean>>](https://www.yuque.com/anyconf/eanoso/dqkggccykfrgogq5)<br/>WaitingRoomUserBean：等候室成员信息，详见 [WaitingRoomUserBean](https://www.yuque.com/anyconf/smeeting/mzyftti7zsfhs417#txWLy) |
| --- | --- |


### createSubMeeting()
创建子会议

```kotlin
fun createSubMeeting(
    subMeetingTitles: MutableList<String>,
    callback: Callback<Data<String?>>?
)
```

参数

| subMeetingTitles | MutableList 类型，子会议名称列表 |
| --- | --- |
| callback | 结果回调，详见 [Callback<Data<T extends BaseBean>>](https://www.yuque.com/anyconf/eanoso/dqkggccykfrgogq5)<br/>WaitingRoomUserBean：等候室成员信息，详见 [WaitingRoomUserBean](https://www.yuque.com/anyconf/smeeting/mzyftti7zsfhs417#txWLy) |


### updateSubMeetingTitle(）
更新子会议标题

```kotlin
fun updateSubMeetingTitle(
    id: String, title: String, 
    callback: Callback<Data<String?>>?
)
```

参数

| id | String 类型，子会议 id |
| --- | --- |
| callback | 结果回调，详见 [Callback<Data<T extends BaseBean>>](https://www.yuque.com/anyconf/eanoso/dqkggccykfrgogq5) |


### updateSubMeetingUsers()
全量更新子会议参与者

```kotlin
fun updateSubMeetingUsers(
    id: String, members: MutableList<MemberRequestBean>, 
    callback: Callback<Data<String?>>?
)
```

参数

| id | String 类型，子会议 id |
| --- | --- |
| members | MutableList 类型，成员列表 |
| callback | 结果回调，详见 [Callback<Data<T extends BaseBean>>](https://www.yuque.com/anyconf/eanoso/dqkggccykfrgogq5) |


### deleteSubMeeting()
删除子会议

```kotlin
fun deleteSubMeeting(
    ids: MutableList<String>, callback: Callback<Data<String?>>?
)
```

参数

| ids | MutableList 类型，子会议 id 列表 |
| --- | --- |
| callback | 结果回调，详见 [Callback<Data<T extends BaseBean>>](https://www.yuque.com/anyconf/eanoso/dqkggccykfrgogq5) |


### getSubMeetingList()
获取讨子会议列表

```kotlin
fun getSubMeetingList(callback: Callback<Data<MutableList<SubMeetingBean>?>>)
```

参数

| callback | 结果回调，详见 [Callback<Data<T extends BaseBean>>](https://www.yuque.com/anyconf/eanoso/dqkggccykfrgogq5)<br/>SubMeetingBean：子会议信息，[SubMeetingBean](https://www.yuque.com/anyconf/smeeting/mzyftti7zsfhs417#lyedF) |
| --- | --- |


### startSubMeeting()
开始子会议

```kotlin
fun startSubMeeting(
    ids: MutableList<String>,
    callback: Callback<Data<String?>>?
)
```

参数

| ids | MutableList 类型，子会议 id 列表 |
| --- | --- |
| callback | 结果回调，详见 [Callback<Data<T extends BaseBean>>](https://www.yuque.com/anyconf/eanoso/dqkggccykfrgogq5) |


### stopSubMeeting()
结束子会议

```kotlin
fun stopSubMeeting(
    ids: MutableList<String>, callback: Callback<Data<String?>>?
)
```

参数

| ids | MutableList 类型，子会议 id 列表 |
| --- | --- |
| callback | 结果回调，详见 [Callback<Data<T extends BaseBean>>](https://www.yuque.com/anyconf/eanoso/dqkggccykfrgogq5) |


### moveSubMeetingUser()
移动子会议成员

```kotlin
fun moveSubMeetingUser(
    fromId: String, toId: String, uid: String,
    callback: Callback<Data<String?>>?
)
```

参数

| fromId | String 类型，源子会议 id |
| --- | --- |
| toId | String 类型，目标子会议 id，null 表示主会场 |
| uid | String 类型，用户 id |
| callback | 结果回调，详见 [Callback<Data<T extends BaseBean>>](https://www.yuque.com/anyconf/eanoso/dqkggccykfrgogq5) |


### helpSubMeeting()
子会议请求帮助

```kotlin
fun helpSubMeeting(
    meetingId: String, callback: Callback<Data<String?>>?
)
```

参数

| meetingId | String 类型，会议 id |
| --- | --- |
| callback | 结果回调，详见 [Callback<Data<T extends BaseBean>>](https://www.yuque.com/anyconf/eanoso/dqkggccykfrgogq5) |


### updateEnterBeforeHostDisabled()
主持人更新在主持人前禁入会

```kotlin
fun updateEnterBeforeHostDisabled(
    meetingId: String, enterBeforeHostDisabled: Boolean,
    callback: Callback<Data<String?>>?
)
```

参数

| meetingId | String 类型，会议 id |
| --- | --- |
| enterBeforeHostDisabled | Boolean 类型，是否禁止在主持人之前进入会议，<br/>true：禁止；false：不禁止。默认 false |
| uid | String 类型，用户 id |
| callback | 结果回调，详见 [Callback<Data<T extends BaseBean>>](https://www.yuque.com/anyconf/eanoso/dqkggccykfrgogq5) |


## 用户操作
### updateName()
用户更新名称

```kotlin
fun updateName(name: String, callback: Callback<Data<String?>>?)
```

参数

| name | String 类型，新昵称 |
| --- | --- |
| callback | 结果回调，详见 [Callback<Data<T extends BaseBean>>](https://www.yuque.com/anyconf/eanoso/dqkggccykfrgogq5) |


### requestOpenCamera()
用户请求打开摄像头

```kotlin
fun requestOpenCamera(
    activity: Activity, 
    view: View?, 
    preOpt: PreOptionCamera?, 
    callback: Callback<Data<String?>>?
)
```

参数

| activity | Activity 类型，作为上下文使用 |
| --- | --- |
| view | View 类型，渲染器控件<br/>必须是 VcsPlayerGlTextureView 或 VcsPlayerGlSurfaceView 之一 |
| preOpt | PreOptionCamera 类型，打开摄像头预设值。<br/>目前有四个值：<br/>PreOptionCamera.get_1080P()、PreOptionCamera.get_720P()<br/>PreOptionCamera.get_480P()、PreOptionCamera.get_180P()<br/>预设值相关内容详见 [摄像头预设值说明](https://www.yuque.com/anyconf/eanoso/gw4l6xvp8ct5aco0) |
| callback | 结果回调，详见 [Callback<Data<T extends BaseBean>>](https://www.yuque.com/anyconf/eanoso/dqkggccykfrgogq5) |


### closeCamera()
用户关闭摄像头

```kotlin
fun closeCamera()
```

### switchCamera()
切换前后置摄像头

```kotlin
fun switchCamera(isFrontCamera: Boolean)
```

参数

| isFrontCamera | Boolean 类型，前后置摄像头，true-前置摄像头，false-后置摄像头 |
| --- | --- |
| callback | 结果回调，详见 [Callback<Data<T extends BaseBean>>](https://www.yuque.com/anyconf/eanoso/dqkggccykfrgogq5) |


### addPreview()
添加预览控件

```kotlin
fun addPreview(view: View)
```

参数

| view | View 类型，渲染器控件<br/>必须是 VcsPlayerGlTextureView 或 VcsPlayerGlSurfaceView 之一 |
| --- | --- |


### removePreview()
移除渲染控件

```kotlin
fun removePreview(view: View?)
```

参数

| view | View 类型，渲染器控件<br/>如果 view 不为空，则移除指定控件；如果 view 为空，则移除所有控件 |
| --- | --- |


### replacePreView()
替换预览渲染控件

```kotlin
fun replacePreView(mViews: MutableList<View>)
```

参数

| mViews | MutableList 类型，渲染器控件列表 |
| --- | --- |


### getAllPreview()
获取所有预览控件

```kotlin
fun getAllPreview(): ArrayList<View>
```

返回值

| 当前所有预览控件 |
| --- |


### requestOpenMic()
用户请求打开麦克风

```kotlin
fun requestOpenMic(preOpt: PreOptionMic?, callback: Callback<Data<String?>>?)
```

参数

| preOpt | PreOptionMic 类型，打开麦克风预设值。<br/>目前只有唯一值：PreOptionMic.def<br/>预设值相关内容详见 [麦克风预设值说明](https://www.yuque.com/anyconf/eanoso/cyi8zdiamn9dss8d) |
| --- | --- |
| callback | 结果回调，详见 [Callback<Data<T extends BaseBean>>](https://www.yuque.com/anyconf/eanoso/dqkggccykfrgogq5) |


### closeMic()
用户关闭麦克风

```kotlin
fun closeMic()
```

### initScreenShare()
用户初始化屏幕共享

```kotlin
fun initScreenShare(
    activity: Activity, notificationParam: ScreenManager.NotificationParam?,
    preOpt: PreOptionScreen?, event: ScreenManager.ScreenShareEvent
)
```

参数

| activity | Activity 类型，上下文环境 |
| --- | --- |
| notificationParam | NotificationParam 类型，通知栏参数<br/><font style="color:#DF2A3F;">如果不启用通知栏，这个参数可以不设置</font> |
| preOpt | PreOptionScreen 类型，打开屏幕共享预设值。<br/>目前只有唯一值：PreOptionScreen.def<br/>预设值相关内容详见 [屏幕共享预设值说明](https://www.yuque.com/anyconf/eanoso/ndfl7ceqhcfdyghd) |
| event | 录屏事件 |


ScreenShareEvent 接口说明

| 接口名称 | 接口说明 | 返回值 |
| --- | --- | --- |
| onScreenStateChanged | 屏幕录制状态改变 | eventId：Int 类型，事件id<br/>VCS_EVENT_TYPE.ScreenRecordError：屏幕录制出错<br/>VCS_EVENT_TYPE.ScreenRecordStart：屏幕录制开始<br/>VCS_EVENT_TYPE.ScreenRecordStop：屏幕录制结束<br/>args：String 类型，事件描述 |


### startScreenShare()
用户开始屏幕共享

```kotlin
fun startScreenShare(hasBar: Boolean, listener: MeetingResultCallback?)
```

参数

| hasBar | Boolean 类型，是否启用通知栏 |
| --- | --- |
| listener | 结果回调，详见 [MeetingResultCallback](https://www.yuque.com/anyconf/eanoso/put57w0owgogyplo) |


### stopScreenShare()
用户停止屏幕共享

```kotlin
fun stopScreenShare()
```

### requestShareBoard()
用户请求共享白板

```kotlin
fun requestShareBoard(callback: BoardShareCallback)
```

参数

| callback | 白板共享结果回调 |
| --- | --- |


BoardShareCallback 说明

| 接口名称 | 接口说明 | 返回值 |
| --- | --- | --- |
| onSucceed | 发起白板共享成功 | whiteBoard：String 类型，白板地址 ur |
| onFail | 发起白板共享失败 | code：Int 类型，错误码<br/>msg：String 类型，错误信息 |


### stopShareWhiteBoard()
停止白板共享

```kotlin
fun stopShareWhiteBoard()
```

### sendRoomChatMessage()
用户发送聊天消息，可单发和群发

```kotlin
fun sendRoomChatMessage(
    targetId: String?, msg: String, msgType: ChatMsgType,
    callback: Callback<Data<String?>>?
)
```

参数

| targetId | String 类型，目标用户 uid；<font style="color:#DF2A3F;">如果 为 null，表示发送给全体</font> |
| --- | --- |
| msg | String 类型，消息内容 |
| msgType | ChatMsgType 类型，消息类型，详见枚举类型中的 [ChatMsgType](https://www.yuque.com/anyconf/eanoso/sly78y2qziqggiwx#dmcbX) |
| callback | 结果回调，详见 [Callback<Data<T extends BaseBean>>](https://www.yuque.com/anyconf/eanoso/dqkggccykfrgogq5) |


### sendRoomCustomMessage()
用户发送自定义消息，可单发和群发

```kotlin
fun sendRoomCustomMessage(
    targetId: String?, msg: String,
    callback: Callback<Data<String?>>?
)
```

参数

| targetId | String 类型，目标用户 uid；<font style="color:#DF2A3F;">如果 为 null，表示发送给全体</font> |
| --- | --- |
| msg | String 类型，消息内容 |
| callback | 结果回调，详见 [Callback<Data<T extends BaseBean>>](https://www.yuque.com/anyconf/eanoso/dqkggccykfrgogq5) |


### getRoomChatMsgList()
获取聊天列表

```kotlin
fun getRoomChatMsgList(
    page: Int, prePage: Int,
    callback: Callback<Data2<List<ChatMsgBean?>>>
)
```

参数

| page | Int 类型，页码 |
| --- | --- |
| prePage | Int 类型，每页条数 |
| callback | 结果回调，详见 [Callback<Data<T extends BaseBean>>](https://www.yuque.com/anyconf/eanoso/dqkggccykfrgogq5) |


### requestHandup()
用户请求举手

```kotlin
fun requestHandup(code: HandupType, callback: Callback<Data<String?>>?)
```

参数

| code | HandupType 类型，举手申请类型，详见枚举类型中的 [HandupType](https://www.yuque.com/anyconf/eanoso/sly78y2qziqggiwx#dWRbl) |
| --- | --- |
| callback | 结果回调，详见 [Callback<Data<T extends BaseBean>>](https://www.yuque.com/anyconf/eanoso/dqkggccykfrgogq5) |


### cancelHandup()
用户取消举手

```kotlin
fun cancelHandup(code: HandupType)
```

参数

| code | HandupType 类型，举手申请类型，详见枚举类型中的 [HandupType](https://www.yuque.com/anyconf/eanoso/sly78y2qziqggiwx#dWRbl) |
| --- | --- |


### confirmOpenCameraAgree()
用户回复打开摄像头请求，同意

```kotlin
fun confirmOpenCameraAgree(
    targetId: String, 
    view: View?,
    preOpt: PreOptionCamera?,
    callback: Callback<Data<String?>>?
)
```

参数

| targetId | String 类型，目标用户 uid |
| --- | --- |
| view | View 类型，渲染器控件<br/>必须是 VcsPlayerGlTextureView 或 VcsPlayerGlSurfaceView 之一 |
| preOpt | PreOptionCamera 类型，打开摄像头预设值。<br/>目前有四个值：<br/>PreOptionCamera.get_1080P()、PreOptionCamera.get_720P()<br/>PreOptionCamera.get_480P()、PreOptionCamera.get_180P()<br/>预设值相关内容详见 [摄像头预设值说明](https://www.yuque.com/anyconf/eanoso/gw4l6xvp8ct5aco0) |
| callback | 结果回调，详见 [Callback<Data<T extends BaseBean>>](https://www.yuque.com/anyconf/eanoso/dqkggccykfrgogq5) |


### confirmOpenCameraRefuse()
用户回复打开摄像头请求，拒绝

```kotlin
fun confirmOpenCameraRefuse(targetId: String, callback: Callback<Data<String?>>?)
```

参数

| targetId | String 类型，目标用户 uid |
| --- | --- |
| callback | 结果回调，详见 [Callback<Data<T extends BaseBean>>](https://www.yuque.com/anyconf/eanoso/dqkggccykfrgogq5) |


### confirmOpenMicAgree()
用户回复打开麦克风请求， 同意

```kotlin
fun confirmOpenMicAgree(
    targetId: String, preOpt: PreOptionMic?,
    callback: Callback<Data<String?>>?
)
```

参数

| targetId | String 类型，目标用户 uid |
| --- | --- |
| preOpt | PreOptionMic 类型，打开麦克风预设值。<br/>目前只有唯一值：PreOptionMic.def<br/>预设值相关内容详见 [麦克风预设值说明](https://www.yuque.com/anyconf/eanoso/cyi8zdiamn9dss8d) |
| callback | 结果回调，详见 [Callback<Data<T extends BaseBean>>](https://www.yuque.com/anyconf/eanoso/dqkggccykfrgogq5) |


### confirmOpenMicRefuse()
用户回复打开麦克风请求， 拒绝

```kotlin
fun confirmOpenMicRefuse(targetId: String, callback: Callback<Data<String?>>?)
```

参数

| targetId | String 类型，目标用户 uid |
| --- | --- |
| callback | 结果回调，详见 [Callback<Data<T extends BaseBean>>](https://www.yuque.com/anyconf/eanoso/dqkggccykfrgogq5) |


### confirmStartScreenShareAgree()
用户回复打开屏幕共享，同意

```kotlin
fun confirmStartScreenShareAgree(
    targetId: String, 
    hasBar: Boolean, 
    listener: MeetingResultCallback?
)
```

参数

| targetId | String 类型，目标用户 uid |
| --- | --- |
| hasBar | 是否显示通知栏 |
| callback | 结果回调，详见 [Callback<Data<T extends BaseBean>>](https://www.yuque.com/anyconf/eanoso/dqkggccykfrgogq5) |


### confirmStartScreenShareRefuse()
用户回复打开屏幕共享，拒绝

```kotlin
fun confirmStartScreenShareRefuse(targetId: String, callback: Callback<Data<String?>>?)
```

参数

| targetId | String 类型，目标用户 uid |
| --- | --- |
| callback | 结果回调，详见 [Callback<Data<T extends BaseBean>>](https://www.yuque.com/anyconf/eanoso/dqkggccykfrgogq5) |


### confirmStartWhiteBoardShareAgree()
用户回复打开白板共享，同意

```kotlin
fun confirmStartWhiteBoardShareAgree(targetId: String, callback: BoardShareCallback)
```

参数

| targetId | String 类型，目标用户 uid |
| --- | --- |
| callback | 结果回调，详见 [Callback<Data<T extends BaseBean>>](https://www.yuque.com/anyconf/eanoso/dqkggccykfrgogq5) |


### confirmStartWhiteBoardShareRefuse()
用户回复打开白板共享，拒绝

```kotlin
fun confirmStartWhiteBoardShareRefuse(targetId: String, callback: Callback<Data<String?>>?)
```

参数

| targetId | String 类型，目标用户 uid |
| --- | --- |
| callback | 结果回调，详见 [Callback<Data<T extends BaseBean>>](https://www.yuque.com/anyconf/eanoso/dqkggccykfrgogq5) |


### startCloudRecord()
开启云录制

```kotlin
fun startCloudRecord(layoutData: LayoutData?, callback: Callback<Data<String?>>?)
```

参数

| layoutData | LayoutData 类型，布局信息，详见 LayoutData |
| --- | --- |
| callback | 结果回调，详见 [Callback<Data<T extends BaseBean>>](https://www.yuque.com/anyconf/eanoso/dqkggccykfrgogq5) |


### stopCloudRecord()
停止云录制

```kotlin
fun stopCloudRecord(callback: Callback<Data<String?>>?)
```

参数

| callback | 结果回调，详见 [Callback<Data<T extends BaseBean>>](https://www.yuque.com/anyconf/eanoso/dqkggccykfrgogq5) |
| --- | --- |


### toggleRemoteAudioMute()
切换远程音频的静音/取消静音状态

```kotlin
fun switchSpeaker(mute: Boolean)
```

参数

| mute | Boolean 类型，切换远程音频<br/>默认值 false， true：静音  false：取消静音 |
| --- | --- |


### getAudioRouterManager()
获取音频路由管理类

```kotlin
fun getAudioRouterManager(): AudioRouterManager?
```

返回值

| 返回音频路由管理类，通过 AudioRouterManager 可以实现对音频路由的控制，详见 [AudioRouterManager](https://www.yuque.com/anyconf/eanoso/zauf0xfgmiirhbmy) |
| --- |


### releaseAudioRouterManager()
释放音频路由管理类

```kotlin
fun releaseAudioRouterManager()
```

### startPlayRemoteVideo()
订阅远端视频流

```kotlin
fun startPlayRemoteVideo(
    uid: String, 
    trackDesc: String, 
    view: View? = null, 
    event: RTCRemoteVideoEvent? = null
): RemoteVideoTrack?
```

参数

| uid | String 类型，用户 uid |
| --- | --- |
| trackDesc | String 类型，轨道描述 |
| view | View 类型，渲染器控件<br/>必须是 VcsPlayerGlTextureView 或 VcsPlayerGlSurfaceView 之一 |
| event | RTCRemoteVideoEvent 类型，回调远端视频流状态 |


返回值

| RemoteVideoTrack 类型，远端视频流操作类，用于实现更细致的远端视频流操作，详见 [RemoteVideoTrack](https://www.yuque.com/anyconf/smeeting/rg94p3ilfbbagbbx) |
| --- |


RTCRemoteVideoEvent 接口说明

| 接口名称 | 接口说明 | 返回值 |
| --- | --- | --- |
| onReceiveStreamStatusChange | 流媒体接收远端流状态变更回调 | uid：String 类型，用户 id<br/>trackDesc：String 类型，轨道描述<br/>isChoke：Boolean 类型，流是否停止 |


### stopPlayRemoteVideo()
取消订阅视频流

```kotlin
fun stopPlayRemoteVideo(uid: String, trackDesc: String)
```

参数

| uid | String 类型，用户 uid |
| --- | --- |
| trackDesc | String 类型，轨道描述 |


### getRemoteVideoTrack()
获取远端视频流的 RemoteVideoTrack

```kotlin
fun getRemoteVideoTrack(uid: String, trackDesc: String): RemoteVideoTrack?
```

参数

| uid | String 类型，用户 uid |
| --- | --- |
| trackDesc | String 类型，轨道描述 |


返回值

| RemoteVideoTrack 类型，远端视频流操作类，用于实现更细致的远端视频流操作，详见 [RemoteVideoTrack](https://www.yuque.com/anyconf/smeeting/rg94p3ilfbbagbbx) |
| --- |


### startPlayRemoteMixture()
开始播放远端合成流

```kotlin
fun startPlayRemoteMixture(
    view: View? = null, event: RTCRemoteVideoEvent? = null
): RemoteVideoTrack?
```

参数

| view | View 类型，渲染器控件<br/>必须是 VcsPlayerGlTextureView 或 VcsPlayerGlSurfaceView 之一 |
| --- | --- |
| event | RTCRemoteVideoEvent 类型，回调远端视频流状态 |


返回值

| RemoteVideoTrack 类型，远端视频流操作类，用于实现更细致的远端视频流操作，详见 [RemoteVideoTrack](https://www.yuque.com/anyconf/smeeting/rg94p3ilfbbagbbx) |
| --- |


RTCRemoteVideoEvent 接口说明

| 接口名称 | 接口说明 | 返回值 |
| --- | --- | --- |
| onReceiveStreamStatusChange | 流媒体接收远端流状态变更回调 | uid：String 类型，用户 id<br/>trackDesc：String 类型，轨道描述<br/>isChoke：Boolean 类型，流是否停止 |


### stopPlayRemoteMixture()
停止播放远端合成流

```kotlin
fun stopPlayRemoteMixture()
```

### getRemoteMixtureTrack()
获取远端合成流的 RemoteVideoTrack

```kotlin
fun getRemoteMixtureTrack(): RemoteVideoTrack?
```

返回值

| RemoteVideoTrack 类型，远端视频流操作类，用于实现更细致的远端视频流操作，详见 [RemoteVideoTrack](https://www.yuque.com/anyconf/smeeting/rg94p3ilfbbagbbx) |
| --- |


## 其他
### getSelfInfo()
从后台获取自身用户信息

```kotlin
fun getSelfInfo(callback: Callback<Data<UserBean?>?>?)
```

参数

| callback | Callback 类型，详见 [Callback<T extends BaseBean>](https://www.yuque.com/anyconf/smeeting/dqkggccykfrgogq5)<br/>UserBean：用户信息，详见 [UserBean](https://www.yuque.com/anyconf/smeeting/mzyftti7zsfhs417#BlxfD) |
| --- | --- |


### getAgentList()
获取设备列表

```kotlin
fun getAgentList(
    types: MutableList<AgentType>, 
    keyword: String, page: Int, perPage: Int,
    callback: Callback<Data2<List<AgentBean>>>
)
```

参数

| types | MutableList<AgentType> 类型，需要获取的设备类型列表，<br/>枚举类型详见：[AgentType](https://www.yuque.com/anyconf/smeeting/sly78y2qziqggiwx#vcRSD) |
| --- | --- |
| keyword | String 类型，搜索关键字 |
| page | Int 类型，页号 |
| perPage | Int 类型，每页 item 个数 |
| callback | Callback 类型，详见 [Callback<T extends BaseBean>](https://www.yuque.com/anyconf/smeeting/dqkggccykfrgogq5)<br/>AgentBean，设备信息，详见 [AgentBean](https://www.yuque.com/anyconf/smeeting/mzyftti7zsfhs417#hAhBk) |


### callUser()
```kotlin
fun callUser(
    targetUids: MutableList<String>,
    callback: Callback<Data<String>>
)
```

参数

| targetUids | MutableList<String> 类型，目标用户的 uid 列表 |
| --- | --- |
| callback | Callback 类型，详见 [Callback<T extends BaseBean>](https://www.yuque.com/anyconf/smeeting/dqkggccykfrgogq5) |


