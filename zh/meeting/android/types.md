---
title: "类型定义"
description: "Android SMeeting 会议 SDK 完整类型与结构体定义"
---

### CreateImmediateMeetingOption
创建即时会议参数

| 属性名称 | 数据类型 | 说明 |
| --- | --- | --- |
| roomNo | String | 房间号 |
| content | String | 会议说明 |
| attendType | AttendType | 入会方式类型，默认 `ATTEND_NOT_LIMIT<br/>`ATTEND_NOT_LIMIT：无限制，值为 1 <br/>ATTEND_BY_PWD：密码进入，值为 2 <br/>ATTEND_ONLY_INVITE：仅邀请人员参会，值为 3 |
| conferees | `MutableList<String>` | 参会成员列表 |
| password | String | 密码 |
| mode | MeetingMode | 会议模式 |
| planTime | Long | 开始时间时间戳 |
| planDur | Int | 会议时长 |
| autoRecord | Boolean | 是否开启自动录制 |
| entryMutePolicy | MuteState | 入会静音状态 默认 `MuteState1<br/>`详见 [MuteState](https://www.yuque.com/anyconf/smeeting/sly78y2qziqggiwx#alagF) |
| watermarkDisabled | Boolean | 水印状态 默认false <br/>true:禁用 <br/>false:不禁用 |
| screenshotDisabled | Boolean | 截屏状态 默认false <br/>true：禁用 <br/>false:不禁用 |
| chatDisabled | Boolean | 聊天模式 默认false <br/>true:禁用 <br/>false:不禁用 |
| extendInfo | String | 自定义扩展字段 |


### UpdateMeetingOption
更新会议参数

| 属性名称 | 数据类型 | 说明 |
| --- | --- | --- |
| title | String | 会议标题 |
| content | String | 会议说明 |
| attendType | AttendType | 入会方式类型，默认 `ATTEND_NOT_LIMIT<br/>`ATTEND_NOT_LIMIT：无限制，值为 1 <br/>ATTEND_BY_PWD：密码进入，值为 2 <br/>ATTEND_ONLY_INVITE：仅邀请人员参会，值为 3 |
| conferees | `MutableList<String>` | 参会成员列表 |
| password | String | 密码 |
| mode | MeetingMode | 会议模式 |
| planTime | Long | 开始时间时间戳 |
| planDur | Int | 会议时长 |
| autoRecord | Boolean | 是否开启自动录制 |
| entryMutePolicy | MuteState | 入会静音状态 默认 `MuteState1<br/>`详见：[MuteState](https://www.yuque.com/anyconf/smeeting/sly78y2qziqggiwx#alagF) |
| watermarkDisabled | Boolean | 水印状态 默认false <br/>true:禁用 <br/>false:不禁用 |
| screenshotDisabled | Boolean | 截屏状态 默认false <br/>true：禁用 <br/>false:不禁用 |
| chatDisabled | Boolean | 聊天模式 默认false <br/>true:禁用 <br/>false:不禁用 |
| extendInfo | String | 自定义扩展字段 |


### RTCMediaOptions
流媒体全局配置参数

| 属性名称 | 数据类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| audioChannels | Int  | 1 | 音频采样通道 |
| audioSamplerate | Int  | 48000 | 音频采样率 |
| audioBitrate | Int  |  32 * 1024 | 音频码率 |
| audioCodec | CodecType 枚举类型 | CodecType.OPUS | 音频编码格式 |
| videoWidthMain | Int  | 640 | 视频分辨率宽度 |
| videoHeightMain | Int  | 480 | 视频分辨率高度 |
| videoBitrateMain | Int  | 512 * 1024 | 视频码率 |
| fpsMain | Int  | 25 | 视频帧率 |
| sft | Boolean  | true | 是否使用移频 |
| agc | Int  | 10000 | 音频 agc |
| aec | Int  | 12 | 音频 aec |
| xdelay | Boolean  | true | 是否开启延时自适应 |
| xbitrate | Int  |  5 | 码率自适应 |
| defFrontCamera | Boolean  | false | 默认打开的摄像头位置：前置 / 后置 |
| defMcuTrack | Int  | 0 | mcu默认轨道 |
| plc | Int  | 2 | 延迟抖动 |
| hwDecoder | Boolean  | true | 是否优先硬解码 |
| hwEncoder | Boolean  | true | 是否优先硬编码 |
| isDaulStream | Boolean  | true | 是否双流 |
| statInterval | Int  | 1000 | 网络统计间隔 ms |
| statAudioInterval | Int  | 500 | 音频统计间隔 ms |


### MeetingCreatedBean
会议创建成功结果信息

| 属性名称 | 数据类型 | 说明 |
| --- | --- | --- |
| meetingId | String | 会议 id |
| roomNo | String | 会议号 |


### AgentRequestBean
邀请设备请求信息

| 属性名称 | 数据类型 | 说明 |
| --- | --- | --- |
| type | AgentType | 设备类型，详见 [AgentType](https://www.yuque.com/anyconf/smeeting/sly78y2qziqggiwx#vcRSD) |
| contact | String | 设备标识 |


### MeetInfo
会议信息

| 属性名称 | 数据类型 | 说明 |
| --- | --- | --- |
| id | String | 会议ID |
| title | String | 会议标题 |
| roomNo | String | 房间号 |
| password | String | 会议密码 |
| attendType | AttendType | 入会方式类型，默认 `ATTEND_NOT_LIMIT<br/>`ATTEND_NOT_LIMIT：无限制，值为 1 <br/>ATTEND_BY_PWD：密码进入，值为 2 <br/>ATTEND_ONLY_INVITE：仅邀请人员参会，值为 3 |
| meetingStatus | MeetingStatus | 会议状态，<br/>STATUS_UNKNOW：未知，值为 -1<br/>STATUS_PRE：未开始，值为 1<br/>STATUS_ING：进行中，值为 2<br/>STATUS_END：结束，值为 3 |
| meetingType | MeetingType | 会议类型，详见 [MeetingType](https://www.yuque.com/anyconf/smeeting/sly78y2qziqggiwx#XPYPA) |
| planTime | Long | 预计开始时间 |
| planDur | Int | 预计持续时间 |
| beginTime | Long | 开始时间 |
| endTime | Long | 结束时间 |
| creator | String | 创建者ID |
| conferee | `ArrayList<String>` | 会前邀请参加的成员列表，value 为成员 uid |
| createAt | Long | 创建时间，单位 秒 |


### MeetDetail
会议详情

| 属性名称 | 数据类型 | 说明 |
| --- | --- | --- |
| id | String | 会议ID |
| roomNo | String | 房间号 |
| title | String | 会议标题 |
| content | String | 会议说明 |
| password | String | 入会密码 |
| creator | String | 创建者ID |
| attendType | AttendType | 入会方式类型，默认 `ATTEND_NOT_LIMIT<br/>`ATTEND_NOT_LIMIT：无限制，值为 1 <br/>ATTEND_BY_PWD：密码进入，值为 2 <br/>ATTEND_ONLY_INVITE：仅邀请人员参会，值为 3 |
| meetingStatus | MeetingStatus | 会议状态，<br/>STATUS_UNKNOW：未知，值为 -1<br/>STATUS_PRE：未开始，值为 1<br/>STATUS_ING：进行中，值为 2<br/>STATUS_END：结束，值为 3 |
| meetingType | MeetingType | 会议类型，详见 [MeetingType](https://www.yuque.com/anyconf/smeeting/sly78y2qziqggiwx#XPYPA) |
| meetingMode | MeetingMode | 会议模式，详见 [MeetingMode](https://www.yuque.com/anyconf/smeeting/sly78y2qziqggiwx#avINM) |
| autoRecord | Boolean | 自动录制状态 |
| planTime | Long | 预计开始时间 |
| planDur | Int | 预计持续时间 |
| beginTime | Long | 开始时间 |
| endTime | Long | 结束时间 |
| onlineNum | Int | 在线人数 |
| entryMutePolicy | MuteState | 入会静音状态，详见 [MuteState](https://www.yuque.com/anyconf/smeeting/sly78y2qziqggiwx#alagF) |
| watermarkDisabled | Boolean | 水印禁用状态 |
| screenshotDisabled | Boolean | 截屏禁用状态 |
| chatDisabled | Boolean | 聊天禁用状态 |
| locked | Boolean | 锁定状态 |
| shareState | ShareType | 共享状态，详见枚举类型中的 [ShareType](https://www.yuque.com/anyconf/eanoso/sly78y2qziqggiwx#TA7zJ) |
| micDisabled | Boolean | 麦克风禁用状态 |
| cameraDisabled | Boolean | 摄像头禁用状态 |
| selfUnmuteMicDisabled | Boolean | 房间是否允许自我解除禁音状态 |
| selfUnmuteCameraDisabled | Boolean | 房间是否允许自我解除禁画状态 |
| conferee | `ArrayList<String>` | 会前邀请参加的成员列表，value 为成员 uid |


### SubMeetingBean
子会议信息

| 属性名称 | 数据类型 | 说明 |
| --- | --- | --- |
| id | String | 子会议 id |
| mainMeetingId | String | 主会议的会议 id |
| meetingId | String | 子会议关联的会议 id |
| status | SubMeetingStatus | 子会议状态：<br/>    STATUS_PRE：未开始<br/>    STATUS_ING：进行中<br/>    STATUS_END：已结束 |
| title | String | 小组名称 |
| users | MutableList | 用户列表   MemberBean：成员信息，详见 [MemebrBean](#QbfVP) |


### UserBean
用户信息

| 属性名称 | 数据类型 | 说明 |
| --- | --- | --- |
| device_id | String | 设备唯一id |
| device_type | Int | 设备类型，详见 [DeviceType](https://www.yuque.com/anyconf/smeeting/sly78y2qziqggiwx#IiY5L) |
| exp_at | Long | 过期时间,默认7天 |
| user_id | String | 参会用户ID |


### MemberBean
成员信息

| 属性名称 | 数据类型 | 说明 |
| --- | --- | --- |
| uid | String | 用户 id |
| nickname | String | 用户昵称 |
| deviceType | Int | 设备类型，详见 [DeviceType](https://www.yuque.com/anyconf/smeeting/sly78y2qziqggiwx#IiY5L) |
| joinAt | Long | 加入时间（后端使用，前端不必在意） |


### WaitingRoomUserBean
等候室成员信息

| 属性名称 | 数据类型 | 说明 |
| --- | --- | --- |
| uid | String | 用户 id |
| nickname | String | 用户昵称 |


### MeetingInfo
会议信息

| 属性名称 | 数据类型 | 说明 |
| --- | --- | --- |
| id | String | 会议ID |
| roomNo | String | 房间号 |
| title | String | 会议标题 |
| content | String | 会议说明 |
| meetingType | Int | 会议类型 |
| beginTime | Long | 开始时间 |
| endTime | Long | 结束时间 |
| entryMutePolicy | Int | 入会静音选项 |
| watermarkDisabled | Boolean | 关水印设置 |
| screenshotDisabled | Boolean | 禁截屏设置 |
| chatDisabled | Boolean | 禁聊设置 |
| micDisabled | Boolean | 静音设置 |
| cameraDisabled | Boolean | 禁画设置 |
| selfUnmuteMicDisabled | Boolean | 禁自我解除静音 |
| selfUnmuteCameraDisabled | Boolean | 禁自我解除禁画 |
| locked | Boolean | 房间锁定状态 |
| shareState | ShareType | 共享状态，详见枚举类型中的 [ShareType](https://www.yuque.com/anyconf/eanoso/sly78y2qziqggiwx#TA7zJ) |
| shareUid | String | 共享者ID |
| creator | String | 创建者ID |
| hostUid | String | 主持人 |
| coHosts | `MutableList<String>` | 主持人ID列表 |
| extendInfo | JsonElement | 自定义扩展 |


### MemberInfo
成员信息

| 属性名称 | 数据类型 | 说明 |
| --- | --- | --- |
| uid | String | 三方平台用户ID |
| name | String | 用户名 |
| deviceType | Int | 设备类型，详见枚举类型中的 [DeviceType](https://www.yuque.com/anyconf/eanoso/sly78y2qziqggiwx#IiY5L) |
| deviceId | String | 终端唯一编号 |
| version | String | sdk版本号 |
| joinAt | Long | 加入时间 |
| role | MemberRoleType | 会中角色，详见枚举类型中的 [MemberRoleType](https://www.yuque.com/anyconf/eanoso/sly78y2qziqggiwx#nFCVP) |
| avatar | String | 会中头像 |
| micState | DeviceState | 麦克风状态，详见枚举类型中的 [DeviceState](https://www.yuque.com/anyconf/eanoso/sly78y2qziqggiwx#hT40E) |
| cameraState | DeviceState | 摄像头状态，详见枚举类型中的 [DeviceState](https://www.yuque.com/anyconf/eanoso/sly78y2qziqggiwx#hT40E) |
| shareState | ShareType | 共享状态，详见枚举类型中的 [ShareType](https://www.yuque.com/anyconf/eanoso/sly78y2qziqggiwx#TA7zJ) |
| chatDisabled | Boolean | 禁聊设置 |
| extendInfo | JsonElement | 自定义扩展 |


### TrackInfo
轨道信息

| 属性名称 | 数据类型 | 说明 |
| --- | --- | --- |
| id | String | 轨道 id |
| desc | String | 轨道描述 |
| kind | String | 轨道类型：video / audio |
| codec | Int | 编码类型：<br/>unknow：0<br/>H264：0x1b<br/>H265：0x24<br/>AAC：0x0f<br/>OPUS：0x5355504f |
| width | Int | 视频宽度 |
| height | Int  | 视频高度 |
| fps | Int  | 视频帧率 |
| angle | Int  | angle |
| bitrate | Int | bitrate |
| sample_rate | Int | 音频采样率 |
| track | Int | 轨道号 （0-6） |
| props | JsonElement | 自定义属性 |


### AgentBean
设备信息

| 属性名称 | 数据类型 | 说明 |
| --- | --- | --- |
| id | String | 设备 ID |
| name | Int | 设备名称 |
| type | AgentType | 设备类型，[AgentType](https://www.yuque.com/anyconf/smeeting/sly78y2qziqggiwx#vcRSD) |
| status | AgentStatus | 设备状态，[AgentStatus](https://www.yuque.com/anyconf/smeeting/sly78y2qziqggiwx#I4j9W) |
| contact | String | 设备标识 |
| remark | String | 备注 |














































