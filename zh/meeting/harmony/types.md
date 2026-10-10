---
title: "类型定义"
description: "SMeeting HarmonyOS SDK 的枚举、数据模型与请求参数完整清单"
---

所有类型从 `smeeting` 直接导出：

```typescript
import { Role, MeetingUserInfo, RoomInfo, MeetingCreateReq } from 'smeeting';
```

媒体相关的类型（`Track`、`AudioRoute`、`DeviceInfo`、质量类型等）来自 `srtc`，
见 [SRTC 类型定义](/zh/rtc/harmony/types)。

---

## 枚举

### `Role`

| 成员 | 值 | 说明 |
| --- | --- | --- |
| `member` | `0` | 普通成员 |
| `host` | `1` | 主持人 |
| `coHost` | `2` | 联席主持人 |

所有 `admin*` 方法要求 `host` 或 `coHost`。

### `TrackDesc`

会议里的轨道按用途命名。

| 成员 | 值 | 说明 |
| --- | --- | --- |
| `mic` | `'mic'` | 麦克风 |
| `cameraBig` | `'camera_big'` | 摄像头大流 |
| `cameraSmall` | `'camera_small'` | 摄像头小流（宫格用） |
| `screen` | `'screen'` | 屏幕共享 |

### `MicState` / `CameraState`

| 枚举 | 成员 |
| --- | --- |
| `MicState` | `on = 1` / `off = 2` |
| `CameraState` | `on = 1` / `off = 2` |

<Note>
注意是 `1` / `2`，**不是** `0` / `1` —— 别用 `!state` 判断。
</Note>

### `ShareType`

| 成员 | 值 |
| --- | --- |
| `screen` | `1` |
| `whiteBoard` | `2` |

### `HandupType` / `UserHandupStep`

| 枚举 | 成员 |
| --- | --- |
| `HandupType` | `mic = 1` / `camera = 2` / `chat = 3` / `share = 4` |
| `UserHandupStep` | `request = 1` / `cancel = 2` / `confirmOpen = 3` / `rejectOpen = 4` |

### `ChatMsgType`

| 成员 | 值 |
| --- | --- |
| `text` | `1` |
| `file` | `2` |
| `pic` | `3` |
| `sound` | `4` |

### `ChatMessageInfo`

一条**历史**聊天消息，由 `chatMessageInfoFromJson(o)` 从后端 JSON 还原。

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `id` | `string` | 消息 ID |
| `msg` | `string` | 消息内容（后端字段名是 `msg`） |
| `senderId` | `string` | 发送者 ID |
| `senderName` | `string` | 发送者昵称 |
| `createdAt` | `string` | 创建时间。后端下发的是**字符串**，原样保留，不做隐式转换 |

<Note>
**这个结构里没有消息类型字段。** 实时事件里的 `ChatMsgType`（文本 / 文件 / 图片 / 语音）在历史消息里区分不出来，所以没有它 —— 不要凭空补一个默认值上去。

`createdAt` 保持字符串是有意的：后端给的格式没有约定，强转数字可能得到 `NaN`。
</Note>

### `MeetingType` / `MeetingStatus` / `MeetingMode`

| 枚举 | 成员 |
| --- | --- |
| `MeetingType` | `instant = 1`（即时）/ `appointment = 2`（预约） |
| `MeetingStatus` | `unStart = 1` / `running = 2` / `end = 3` |
| `MeetingMode` | `normal = 1` / `mix = 2` / `voice = 3` / `training = 4` / `subMeeting = 5` |

### `AttendType`

入会限制。

| 成员 | 值 | 说明 |
| --- | --- | --- |
| `unLimit` | `1` | 无限制 |
| `password` | `2` | 需要密码 |
| `invite` | `3` | 仅受邀 |
| `passwordAndInvite` | `4` | 密码 + 受邀 |

### `EntryMutePolicy`

入会静音策略。

| 成员 | 值 | 说明 |
| --- | --- | --- |
| `silent` | `1` | 入会静音 |
| `unRestrict` | `2` | 不限制 |
| `silentAfter6` | `3` | 超过 6 人后入会静音 |

### `EndType`

| 成员 | 值 | 说明 |
| --- | --- | --- |
| `normal` | `0` | 正常结束 |
| `force` | `1` | 强制结束 |

### `UserType`

| 成员 | 值 |
| --- | --- |
| `normal` | `1` |
| `sip` | `2` |
| `h323` | `3` |

### `LayoutType`

MCU 合流布局，共 20 种：

`auto`、`full`、`grids_2`、`grids_3`、`grids_4`、`grids_5`、`grids_6`、`grids_8`、
`grids_9`、`grids_10`、`grids_12`、`grids_16`、`grids_20`、`grids_25`、
`right_4`、`top_4`、`br_7`、`tl_7`、`tb_8`

### `McuTaskType` / `McuTaskStatus`

| 枚举 | 成员 |
| --- | --- |
| `McuTaskType` | `record = 1`（纯录制）/ `mix = 2`（纯混流）/ `mixAndRecord = 3`（混流 + 录制）/ `audio = 4`（录音）/ `live = 8`（直播流）/ `unknown = -1` |
| `McuTaskStatus` | `waitStart = 0`（待开始）/ `running = 1`（进行中）/ `waitEnd = 2`（待结束）/ `exception = 3`（异常结束，原因见 `errDesc`）/ `normal = 4`（正常结束）/ `unknown = -1` |

取值与服务端下发的 `task_type` / `task_status` 一致。`task_type` 由服务端按位组合，组合出的其它值（如 5、9）解码为 `unknown`。
`unknown` 是兜底：服务端下发了本版本 SDK 不认识的取值时用它，**只用于解码，不要拿来发请求**；需要原始值时看 `RoomMcuTaskEventData.taskTypeRaw` / `taskStatusRaw`。
`waitStart` / `waitEnd` 是指令已下发、底层任务尚未确认的临时过渡状态。

<Warning>
**1.1.0 起 `McuTaskStatus` 的数值改了**：1.0.0 及以前是 `exception = 2`、`normal = 3`，与服务端错位。成员名没变，按成员名比较的代码升级后即得正确语义；**直接拿数字比较的代码需要自查**。
</Warning>

### `AgentType` / `AgentStatus`

| 枚举 | 成员 |
| --- | --- |
| `AgentType` | `sip = 2` / `h323 = 3` / `gb28181 = 4` / `rtsp = 5` / `rtmp = 6` / `filePlay = 7` / `tencentMeet = 8` / `ai = 9` |
| `AgentStatus` | `unknown = 0` / `online = 1` / `offline = 2`（废弃别名 `idle = 1`、`busy = 2`） |

<Warning>
**1.2.0 起 `AgentStatus` 的取值改了**：1.1.0 及以前是 `idle = 1` / `busy = 2` / `offline = 3`，与服务端不符。服务端下发其它取值或缺失时为 `unknown`。**按数字比较的代码需要自查**（`offline` 从 `3` 变为 `2`）。
</Warning>

### `MeetingStreamVendor`

| 成员 | 值 |
| --- | --- |
| `ook` | `'ook'` |
| `seastart` | `'seastart'` |
| `wangsuCDN` | `'wangsucdn'` |

### `PresignedPutObjectType`

| 成员 | 值 | 说明 |
| --- | --- | --- |
| `attach` | `'attach'` | 会议附件 |
| `background` | `'background'` | 会议背景 |
| `user` | `'user'` | 用户资源 |

---

## 会中数据模型

### `RoomInfo`

当前房间状态。**判断"按钮能不能点"就靠它。**

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `appId` / `id` / `parent` / `roomNo` | `string` | 标识；`parent` 是主会议（子会议才有） |
| `title` / `content` | `string` | 标题与说明 |
| `meetingType` | `MeetingType` | 即时 / 预约 |
| `meetingMode` | `MeetingMode` | 会议模式 |
| `planTime` / `planDur` | `number` | 预约时间与时长 |
| `entryMutePolicy` | `EntryMutePolicy` | 入会静音策略 |
| `micDisabled` | `boolean` | **全体静音** |
| `selfUnmuteMicDisabled` | `boolean` | **成员能否自行解除静音** |
| `cameraDisabled` | `boolean` | 全体关摄像头 |
| `selfUnmuteCameraDisabled` | `boolean` | 成员能否自行开摄像头 |
| `shareDisabled` | `boolean` | 禁止共享 |
| `chatDisabled` | `boolean` | 禁止聊天 |
| `screenshotDisabled` | `boolean` | 禁止截图 |
| `watermarkDisabled` | `boolean` | 水印开关 |
| `waitingRoomDisabled` | `boolean` | 等候室开关 |
| `enterBeforeHostDisabled` | `boolean` | 是否禁止主持人前入会 |
| `locked` | `boolean` | 会议锁定 |
| `password` | `string` | 入会密码 |
| `shareState` | `number` | 共享状态 |
| `shareUid` | `string` | 正在共享的人 |
| `recordStatus` | `number` | 录制状态 |
| `creator` / `hostUid` | `string` | 创建者 / 当前主持人 |
| `coHosts` | `string[]` | 联席主持人列表 |
| `extendInfo` | `string` | 扩展字段 |

<Warning>
**`micDisabled` 与 `selfUnmuteMicDisabled` 必须一起看。**

| `micDisabled` | `selfUnmuteMicDisabled` | 效果 |
| --- | --- | --- |
| `false` | — | 自由发言 |
| `true` | `false` | 全体静音，可自行开麦 |
| `true` | `true` | 全体静音，只能举手 |

只看 `micDisabled` 会把"可自行解除"的情况误判成不能开麦。摄像头同理。
</Warning>

### `MeetingUserInfo`

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `uid` / `name` / `avatar` | `string` | 标识与展示 |
| `role` | `Role` | 角色 |
| `micState` | `MicState` | 麦克风状态 |
| `cameraState` | `CameraState` | 摄像头状态 |
| `shareState` | `number` | 共享状态 |
| `chatDisabled` | `boolean` | 是否被禁言 |
| `isKickout` | `boolean` | 是否已被移出 |
| `deviceType` / `deviceId` / `version` | `string` | 端信息 |
| `joinAt` | `number` | 入会时间 |
| `trackDescs` | `string[]` | 该成员当前发布的轨道描述 |
| `extendInfo` | `string` | 扩展字段 |

<Note>
`trackDescs` 告诉你这个人有哪些流可订 —— 里面有 `screen` 就说明他在共享。
比自己维护状态可靠。
</Note>

### `MeetingInfo`

会议详情（`detailRoom` / 列表接口返回）。

| 字段 | 类型 |
| --- | --- |
| `id` / `title` / `roomNo` / `password` | `string` |
| `attendType` | `AttendType` |
| `meetingType` / `meetingMode` | 枚举 |
| `meetingStatus` | `MeetingStatus` |
| `autoRecord` | `boolean` |
| `layoutData?` | `LayoutData` |
| `conferee` / `coHosts` | `string[]` |
| `maximum?` | `number` |
| `endType?` | `EndType` |
| `planTime` / `planDur` / `beginTime` / `endTime` / `createdAt` | `number` |
| `creator` / `extendInfo` | `string` |
| `watermarkDisabled` / `screenshotDisabled` / `chatDisabled` / `waitingRoomDisabled` / `enterBeforeHostDisabled` | `boolean` |

### `ParticipantInfo` / `OnlineMemberInfo` / `NoEnterUserInfo`

| 接口 | 字段 |
| --- | --- |
| `ParticipantInfo` | `id`、`userId`、`nickname`、`enterAt`、`exitAt` |
| `OnlineMemberInfo` | `userId`、`nickname`、`deviceType`、`joinAt` |
| `NoEnterUserInfo` | `id`、`nickname`、`mobile`、`avatar`、`role`、`relUid` |

---

## 布局与水印

### `LayoutData`

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `layout` | `LayoutType` | 布局类型 |
| `pollingDur?` | `number` | 轮播间隔 |
| `watermark?` | `Watermark` | 水印 |
| `tag?` | `Tag` | 标签 |
| `divList?` | `DivList[]` | 分区配置 |

### `Watermark`

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `type` | `number` | 水印类型 |
| `text` | `string` | 文字 |
| `size?` | `number` | 字号 |
| `color?` | `string` | 颜色 |
| `olColor?` / `olWidth?` | — | 描边颜色与宽度 |

### `Cell`

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `idx` | `number` | 格位序号 |
| `bindShare` | `boolean` | 是否绑定共享画面 |
| `tag` | `Tag` | 标签 |

---

## 等候室与子会议

| 接口 | 字段 |
| --- | --- |
| `WaitingRoomUserInfo` | `userId`、`name`、`avatar`、`at` |
| `SubMeetingUser` | `uid`、`name` |
| `SubMeetingInfo` | `id`、`mainMeetingId`、`meetingId`、`title`、`users: SubMeetingUser[]`、`status: MeetingStatus` |

---

## 录制与资源

| 接口 | 字段 |
| --- | --- |
| `McuRecordConfig` | `appId`、`layout: LayoutType`、`watermarkType`、`windowTagType`、`createdAt`、`updatedAt` |
| `ResourceInfo` | `id`、`userId`、`meetingId`、`parentId`、`isFolder`、`resType`、`resKey`、`resName`、`resSize`、`createdAt`、`updatedAt` |
| `Attachment` | `name`、`key` |
| `PresignedPutObjectResult` | `url`、`key`、`ext` |
| `McuRecordDetail` | `id`（任务 ID）、`opUid`、`opName`、`channel`、`title`、`roomNo`、`taskType?: McuTaskType`、`taskStatus: McuTaskStatus`、`errDesc`、`beganAt`、`endedAt`、`recordCount`、`totalDuration`、`totalSize`、`records?: McuRecordFile[]`、`tags`、`createdAt`、`updatedAt`、`now`；已废弃：`vodKey?`、`vodSize?`、`mcuAt?`、`mcuDur?` |
| `McuRecordFile` | `recordId`、`taskId`、`channel`、`seq`、`vodSize`、`duration`、`beganAt`、`endedAt`、`offsetMs`、`reason`、`addr`（预签名播放地址，有效期 2 小时）、`createdAt` |

`McuRecordDetail` 是某场会议录制任务的明细，`McuRecordFile` 是任务产出的一个录制文件分片（按 `seq` 排序即播放顺序）。
`vodKey` / `vodSize` / `mcuAt` / `mcuDur` 自 1.1.0 起废弃并改为可选（新服务端不再返回 `vodKey` / `vodSize`），分别改用 `records`、`totalSize`、`beganAt`、`totalDuration`。
任务状态缺失或不认识时 `taskStatus` 为 `unknown`；老服务端不返回 `task_type` 时 `taskType` 为 `undefined`。

---

## 签到

| 接口 | 字段 |
| --- | --- |
| `SignInfo` | `uid`、`beginAt`、`dur`、`endAt`、`desc`、`nums`、`hostName`（可选，发起人昵称；服务端暂未返回，取不到时按 `uid` 找会中成员） |
| `SignDetailInfo` | `id`、`epoch`、`nickname`、`role: Role`、`userId`、`createdAt` |
| `SignInListResult` | 签到列表结果 |

---

## 第三方接入

| 接口 | 字段 |
| --- | --- |
| `AgentInfo` | `id`、`name`、`type: AgentType`、`status: AgentStatus`、`contact`、`remark`、`connParams?: JsonObject`（服务端 `conn_params`，1.2.0 起）、`connSubjects: Map<string, string>`（GB28181 通道表，国标设备按「设备编号:通道编号」邀请，1.2.0 起） |
| `AgentInvite` | `type: AgentType`、`contact` |

---

## 请求参数

### `MeetingCreateReq`

| 字段 | 类型 | 必填 |
| --- | --- | --- |
| `title` | `string` | **是** |
| `meetingMode` | `MeetingMode` | **是** |
| `roomNo?` / `content?` / `password?` / `extendInfo?` | `string` | 否 |
| `attendType?` | `AttendType` | 否 |
| `meetingType?` | `MeetingType` | 否 |
| `conferee?` / `coHosts?` | `string[]` | 否 |
| `maximum?` | `number` | 否 |
| `endType?` | `EndType` | 否 |
| `planTime?` / `planDur?` | `number` | 否，预约会议用 |
| `entryMutePolicy?` | `EntryMutePolicy` | 否 |
| `watermarkDisabled?` / `screenshotDisabled?` / `chatDisabled?` / `waitingRoomDisabled?` / `enterBeforeHostDisabled?` | `boolean` | 否 |
| `layoutData?` | `LayoutData` | 否 |
| `autoRecord?` | `boolean` | 否 |
| `background?` | `string` | 否 |
| `attachments?` | `Attachment[]` | 否 |

`newMeetingCreateReq()` 给一份带默认值的请求体。

### `MeetingEnterReq`

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `nickname` | `string` | **必填** |
| `meetingId?` | `string` | 与 `roomNo` **二选一** |
| `roomNo?` | `string` | 与 `meetingId` 二选一 |
| `password?` | `string` | 会议有密码时必填 |
| `avatar?` | `string` | 会中头像 |
| `extendInfo?` | `string` | 扩展字段 |
| `streamVendor?` | `MeetingStreamVendor` | 指定流媒体引擎 |

### 其它请求体

| 接口 | 字段 |
| --- | --- |
| `PageParam` | `page`、`perPage`（`defaultPageParam()` 给默认值） |
| `ResourceListReq` | `page`、`perPage`、`parentId?`、`meetingId?`、`resName?`、`resType?` |
| `ResourceCreateReq` | `resName`、`resType`、`meetingId?`、`parentId?`、`resKey?` |
| `McuStartReq` | `taskType`、`title`、`userName`、`layoutData` |

序列化辅助函数：`meetingCreateReqToJson`、`meetingEnterReqToJson`、
`pageParamToJson`、`resourceListReqToJson`、`resourceCreateReqToJson`、
`mcuStartReqToJson`。

---

## Token

```typescript
decodeMeetingToken(token: string): MeetingToken
isMeetingTokenExpired(token: MeetingToken): boolean
```

Token 由**业务后端**签发，SDK 只负责解析与过期判断。

---

## 工具函数

枚举的字符串 / 数字互转：

`handupTypeFromValue`、`shareTypeFromValue`、`roleFromValue`、
`chatMsgTypeFromValue`、`meetingTypeFromValue`、`meetingStatusFromValue`、
`attendTypeFromValue`、`endTypeFromValue`、`entryMutePolicyFromValue`、
`meetingModeFromValue`、`mcuTaskTypeFromValue`、`mcuTaskStatusFromValue`、
`layoutTypeFromValue`、`agentTypeFromValue`、`agentStatusFromValue`

数据解析与属性读取：

`emptyRoomInfo`、`roomInfoFromProps`、`cloneMeetingUserInfo`、`meetingInfoFromJson`、
`layoutDataToJson`、`attachmentToJson`、
`propString`、`propNumber`、`propBool`、`propStringArray`

---

### 相关阅读

+ [核心概念](/zh/meeting/harmony/key-concepts)
+ [事件参考](/zh/meeting/harmony/events)
+ [SRTC 类型定义](/zh/rtc/harmony/types) —— 媒体相关类型
