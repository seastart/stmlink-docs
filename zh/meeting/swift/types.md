---
title: "类型定义"
description: "SMeeting Swift SDK 的请求参数、会议与成员信息、事件数据和枚举类型定义"
---

本页整理 SDK 对外公开的类型。字段名一律给 Swift 侧的属性名。

---

### 请求参数

#### MeetingCreateReq

创建 / 修改会议的参数。构造：

```swift
var req = MeetingCreateReq(title: "项目周会", meetingMode: .normal)
req.meetingType = .appointment
req.planTime = Int(Date().timeIntervalSince1970) + 1800
req.planDur = 60
```

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `title` | `String` | 会议标题（构造时必填） |
| `meetingMode` | `MeetingMode` | 会议模式（构造时必填） |
| `roomNo` | `String?` | 自定义房间号，不传由服务端生成 |
| `content` | `String?` | 会议说明 |
| `meetingType` | `MeetingType?` | 会议类型，不传按即时会议处理 |
| `planTime` | `Int?` | 预约开始时间，秒级时间戳 |
| `planDur` | `Int?` | 会议时长，单位分钟 |
| `attendType` | `AttendType?` | 入会限制类型 |
| `password` | `String?` | 入会密码，密码入会时必填 |
| `conferee` | `[String]?` | 受邀成员 ID，仅邀请入会时必填 |
| `coHosts` | `[String]?` | 联席主持人 ID |
| `maximum` | `Int?` | 最大参会人数 |
| `endType` | `EndType?` | 会议结束方式 |
| `entryMutePolicy` | `EntryMutePolicy?` | 入会静音策略 |
| `watermarkDisabled` | `Bool?` | 是否关闭水印 |
| `screenshotDisabled` | `Bool?` | 是否禁止截屏 |
| `chatDisabled` | `Bool?` | 是否全体禁言 |
| `waitingRoomDisabled` | `Bool?` | 是否关闭等候室 |
| `enterBeforeHostDisabled` | `Bool?` | 是否禁止主持人前入会 |
| `autoRecord` | `Bool?` | 是否自动录制 |
| `layoutData` | `LayoutData?` | 合成布局 |
| `background` | `String?` | 背景图资源键 |
| `attachments` | `[Attachment]?` | 会议资料 |
| `extendInfo` | `String?` | 业务扩展字段，建议放 JSON 字符串 |

#### MeetingEnterReq

进入会议的参数。构造：

```swift
var req = MeetingEnterReq(nickname: "张三", roomNo: "10000001")
req.password = "123456"
```

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `nickname` | `String` | 会中昵称（构造时必填） |
| `meetingId` | `String?` | 会议 ID，与 `roomNo` 二选一 |
| `roomNo` | `String?` | 房间号，与 `meetingId` 二选一 |
| `password` | `String?` | 入会密码 |
| `avatar` | `String?` | 会中头像 |
| `streamVendor` | `MeetingStreamVendor?` | 流媒体供应商，不传按服务端配置 |
| `extendInfo` | `String?` | 业务扩展字段 |

#### PageParam

```swift
let page = PageParam(page: 1, perPage: 20)
```

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `page` | `Int` | 页码，默认 `1` |
| `perPage` | `Int` | 每页条数，默认 `20` |

#### ResourceListReq

```swift
var req = ResourceListReq(page: 1, perPage: 20)
req.meetingId = meetingId
```

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `page` / `perPage` | `Int` | 分页 |
| `parentId` | `String?` | 父目录 ID |
| `meetingId` | `String?` | 会议 ID |
| `resName` | `String?` | 资源名过滤 |
| `resType` | `String?` | 资源类型过滤 |

#### ResourceCreateReq

```swift
var req = ResourceCreateReq(resName: "会议材料.pdf", resType: "pdf")
req.resKey = key
```

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `resName` | `String` | 资源名（构造时必填） |
| `resType` | `String` | 资源类型（构造时必填） |
| `resKey` | `String?` | 资源键，来自 `presignedPutObject` |
| `meetingId` | `String?` | 归属会议 |
| `parentId` | `String?` | 父目录 ID |

#### 布局与录制参数

`McuStartReq`、`LayoutData`、`Watermark`、`Tag`、`Cell`、`DivList`、`Attachment` 都提供了构造器，可选参数带默认值；它们同时是 `Codable` 的，也可以用 `JSONDecoder` 从后端下发的 JSON 解出来。字段与 JSON 键的对照表见 [录制与合屏布局](/zh/meeting/swift/advanced/recording)。

---

### 会议与成员信息

#### RoomInfo

当前会议的房间信息，由 `getRoomInfo()` 返回。

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `id` | `String` | 会议 ID |
| `roomNo` | `String` | 房间号 |
| `parent` | `String` | 主会场会议 ID（分组讨论中的小组才有） |
| `title` | `String` | 会议标题 |
| `content` | `String` | 会议说明 |
| `meetingType` | `MeetingType` | 会议类型 |
| `meetingMode` | `MeetingMode` | 会议模式 |
| `planTime` / `planDur` | `Int` | 计划开始时间（秒级时间戳）/ 时长（分钟） |
| `entryMutePolicy` | `EntryMutePolicy` | 入会静音策略 |
| `micDisabled` | `Bool` | 全体静音 |
| `selfUnmuteMicDisabled` | `Bool` | 禁止自我解除静音 |
| `cameraDisabled` | `Bool` | 全体禁画 |
| `selfUnmuteCameraDisabled` | `Bool` | 禁止自我解除禁画 |
| `shareDisabled` | `Bool` | 禁止共享 |
| `chatDisabled` | `Bool` | 全体禁言 |
| `screenshotDisabled` | `Bool` | 禁止截屏 |
| `watermarkDisabled` | `Bool` | 关闭水印 |
| `waitingRoomDisabled` | `Bool` | 关闭等候室 |
| `enterBeforeHostDisabled` | `Bool` | 禁止主持人前入会 |
| `locked` | `Bool` | 会议已锁定 |
| `password` | `String` | 入会密码 |
| `shareState` | `Int` | 当前共享：`0` 无、`1` 屏幕、`2` 白板 |
| `shareUid` | `String` | 当前共享者 |
| `recordStatus` | `Int` | 录制状态 |
| `creator` | `String` | 创建者 |
| `hostUid` | `String` | 主持人 |
| `coHosts` | `[String]` | 联席主持人 |
| `appId` | `String` | 应用 ID |
| `extendInfo` | `String` | 业务扩展字段 |

#### MeetingUserInfo

会中成员信息，由 `getUserInfo(_:)` / `getUsersInfo()` / `getUsersInfoList()` 返回。

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `uid` | `String` | 成员 ID |
| `name` | `String` | 会中昵称 |
| `avatar` | `String` | 会中头像 |
| `role` | `Role` | 会中角色 |
| `micState` | `MicState` | 麦克风状态 |
| `cameraState` | `CameraState` | 摄像头状态 |
| `shareState` | `Int` | 共享状态：`0` 无、`1` 屏幕、`2` 白板 |
| `chatDisabled` | `Bool` | 是否被单独禁言 |
| `isKickout` | `Bool` | 是否已被移出 |
| `trackDescs` | `[String]` | 当前已发布的轨道描述列表 |
| `deviceType` | `String` | 设备类型 |
| `deviceId` | `String` | 设备 ID |
| `version` | `String` | 客户端 SDK 版本 |
| `joinAt` | `Int` | 进入时间 |
| `extendInfo` | `String` | 业务扩展字段 |

#### MeetingInfo

会议详情，由 `detailRoom(...)`、`attendeeRoom(...)`、`attendedRoom(...)` 返回。

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `id` | `String` | 会议 ID |
| `title` | `String` | 会议标题 |
| `roomNo` | `String` | 房间号 |
| `meetingType` | `MeetingType` | 会议类型 |
| `meetingMode` | `MeetingMode` | 会议模式 |
| `meetingStatus` | `MeetingStatus` | 会议状态 |
| `attendType` | `AttendType` | 入会限制类型 |
| `password` | `String` | 入会密码 |
| `conferee` | `[String]` | 受邀成员 |
| `coHosts` | `[String]?` | 联席主持人 |
| `creator` | `String` | 创建者 |
| `maximum` | `Int?` | 最大参会人数 |
| `endType` | `EndType?` | 结束方式 |
| `autoRecord` | `Bool` | 是否自动录制 |
| `layoutData` | `LayoutData?` | 合成布局 |
| `watermarkDisabled` / `screenshotDisabled` / `chatDisabled` | `Bool` | 对应开关 |
| `waitingRoomDisabled` / `enterBeforeHostDisabled` | `Bool` | 对应开关 |
| `planTime` / `planDur` | `Int` | 计划开始时间 / 时长 |
| `beginTime` / `endTime` | `Int` | 实际开始 / 结束时间 |
| `createdAt` | `Int` | 创建时间 |
| `extendInfo` | `String` | 业务扩展字段 |

#### ParticipantInfo

参会记录，由 `roomParticipant(...)` 返回。

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `id` | `String` | 记录 ID |
| `userId` | `String` | 成员 ID |
| `nickname` | `String` | 会中昵称 |
| `enterAt` / `exitAt` | `Int` | 进入 / 退出时间 |

#### OnlineMemberInfo

在线人员，由 `adminListOnlineMember(...)` 返回：`userId`、`nickname`、`deviceType`、`joinAt`。

#### NoEnterUserInfo

未入会人员，由 `meetNotEnter()` 返回：`id`、`nickname`、`mobile`、`avatar`、`role`、`relUid`。

#### WaitingRoomUserInfo

等候室成员，由 `adminWaitingRoomUsers()` 返回：`userId`、`name`、`avatar`、`at`。

#### SubMeetingInfo / SubMeetingUser

小组信息，由 `adminSubMeetingList(...)` 返回。

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `id` | `String` | 小组 ID，编排类接口用它 |
| `mainMeetingId` | `String` | 主会议 ID |
| `meetingId` | `String` | 小组自己的会议 ID，进入小组时用它 |
| `title` | `String` | 小组名称 |
| `users` | `[SubMeetingUser]` | 已分配成员，每项含 `uid`、`name` |
| `status` | `MeetingStatus` | 小组会议状态 |

#### AgentInfo

可邀请设备，由 `agentList(...)` 返回：`id`、`name`、`type`（`AgentType`）、`status`（`AgentStatus`）、`contact`、`remark`。

#### ResourceInfo

资源，由 `resourcesList(...)` 返回。

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `id` | `String` | 资源 ID |
| `isFolder` | `Bool` | 是否为目录 |
| `parentId` | `String` | 父目录 ID |
| `resName` / `resType` / `resKey` / `resSize` | `String` / `String` / `String` / `Int` | 名称、类型、存储键、大小 |
| `userId` / `meetingId` | `String` | 归属用户 / 会议 |
| `createdAt` / `updatedAt` | `String` | 创建 / 更新时间 |

#### SignInfo / SignDetailInfo

签到活动与签到明细。

| 类型 | 字段 |
| --- | --- |
| `SignInfo` | `uid`、`beginAt`、`dur`、`endAt`、`desc`、`nums` |
| `SignDetailInfo` | `id`、`epoch`、`nickname`、`role`、`userId`、`createdAt` |

#### McuRecordConfig / McuRecordDetail

| 类型 | 字段 |
| --- | --- |
| `McuRecordConfig` | `appId`、`layout`、`watermarkType`、`windowTagType`、`createdAt`、`updatedAt` |
| `McuRecordDetail` | `id`、`opUid`、`opName`、`channel`、`title`、`roomNo`、`taskStatus`、`errDesc`、`vodKey`、`vodSize`、`mcuAt`、`mcuDur`、`tags`、`createdAt`、`updatedAt` |

#### MeetingToken

登录 token 解析后的内容。你通常不需要用到它 —— token 由业务后端签发，直接传给 `login(token:)` 即可。如果需要在客户端提前判断 token 是否过期，可以：

```swift
let info = try MeetingToken.decode(from: token)
if info.isExpired { /* 重新向后端获取 */ }
```

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `appId` | `String` | 应用 ID |
| `userId` | `String` | 用户 ID |
| `nickname` | `String` | 昵称 |
| `expAt` | `Int` | 过期时间，秒级时间戳 |
| `isExpired` | `Bool` | 是否已过期 |

---

### 分页

#### PageResult

```swift
let result = try await meeting.attendeeRoom()
result.data      // [MeetingInfo]
result.meta      // MetaRes
```

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `data` | `[T]` | 数据列表 |
| `meta` | `MetaRes` | 分页信息 |

`MetaRes`：`totalCount`、`pageCount`、`currentPage`、`perPage`。

---

### 事件数据类型

#### 连接与成员

| 类型 | 字段 |
| --- | --- |
| `DisconnectEventData` | `reason: DisconnectReason`、`error: Error?` |
| `UserExitEventData` | `uid`、`reason: DisconnectReason` |
| `UserCameraStateChangeEventData` | `uid`、`cameraState`、`byAdmin`、`opUid` |
| `UserMicStateChangeEventData` | `uid`、`micState`、`byAdmin`、`opUid` |
| `UserNameChangeEventData` | `uid`、`nickname`、`byAdmin`、`opUid` |
| `UserRoleChangeEventData` | `uid`、`role`、`opUid` |
| `UserChatDisabledChangeEventData` | `uid`、`chatDisabled`、`opUid` |
| `UserHandupEventData` | `uid`、`type: HandupType`、`step: UserHandupStep` |

#### 房间状态

| 类型 | 字段 |
| --- | --- |
| `RoomMicStateChangeEventData` | `micDisabled`、`selfUnmuteMicDisabled`、`opUid` |
| `RoomCameraStateChangeEventData` | `cameraDisabled`、`selfUnmuteCameraDisabled`、`opUid` |
| `RoomShareStateChangeEventData` | `shareDisabled`、`opUid` |
| `RoomChatDisabledChangeEventData` | `chatDisabled`、`opUid` |
| `RoomScreenshotDisabledChangeEventData` | `screenshotDisabled`、`opUid` |
| `RoomWatermarkDisabledChangeEventData` | `watermarkDisabled`、`opUid` |
| `RoomLockedChangeEventData` | `locked`、`opUid` |
| `RoomShareStartEventData` | `uid`、`shareType: ShareType` |
| `RoomShareStopEventData` | `uid`、`shareType`、`byAdmin`、`opUid` |
| `RoomMcuTaskEventData` | `taskType: McuTaskType`、`taskStatus: McuTaskStatus`、`errDesc` |
| `RoomJoinFailedEventData` | `uid`、`name`、`errDesc`、`failedType` |

#### 消息

| 类型 | 字段 |
| --- | --- |
| `RoomChatMsgEventData` | `msgType: ChatMsgType`、`msg`、`uid: String?`、`isPrivate` |
| `RoomCustomMsgEventData` | `msg`、`uid: String?`、`isPrivate` |

#### 主持人指令与举手

| 类型 | 字段 |
| --- | --- |
| `AdminConfirmHandupEventData` | `type: HandupType`、`approve`、`opUid`、`targetId` |
| `AdminRequestOpenMicEventData` | `opUid` |
| `AdminRequestOpenCameraEventData` | `opUid` |

#### 等候室与分组讨论

| 类型 | 字段 |
| --- | --- |
| `UserEnterWaitingRoomEventData` | `uid`、`name`、`avatar` |
| `UserExitWaitingRoomEventData` | `uid`、`name`、`avatar` |
| `AdminUpdateWaitingRoomDisabledEventData` | `waitingRoomDisabled`、`opUid` |
| `AdminStartSubMeetingEventData` | `meetingId`、`title`、`uids` |
| `AdminStopSubMeetingEventData` | `parent` |
| `AdminMoveSubMeetingUserEventData` | `fromMeetingId`、`fromMeetingTitle`、`toMeetingId`、`toMeetingTitle` |

#### 签到、点名与外设

| 类型 | 字段 |
| --- | --- |
| `SignInActivityEventData` | `hostId`、`hostName`、`epoch`、`beginAt`、`dur`、`endAt`、`desc` |
| `SignInFinishEventData` | `hostId`、`hostName`、`epoch` |
| `RollCallNamedEventData` | `id`（点名记录标识，应答时回传）、`sid`（发起点名的主持人 uid）、`time` |
| `DeviceChangeEventData` | `device: DeviceInfo` |

#### 会议外消息

所有会议外消息事件数据都由 `base` 和 `content` 两部分组成。

| 类型 | 字段 |
| --- | --- |
| `ImBaseEventData` | `sid`、`uid`、`name`、`avatar: String?` |
| `ImCallCallingEventData` | `base`、`content: ImCallContent`（`roomNo`、`meetingId`、`title`） |
| `ImMeetingRemindEventData` | `base`、`content: ImMeetingRemindContent`（`roomNo`、`meetingId`、`title`、`creatorName`、`planDur`、`planTime`） |
| `ImAdminMoveOutWaitingRoomEventData` | `base`、`content: ImMoveOutWaitingRoomContent`（`parent`、`meetingId`、`title`） |
| `ImUserHelpSubMeetingEventData` | `base`、`content: ImHelpSubMeetingContent`（`parent`、`meetingId`、`title`） |
| `ImDisconnectEventData` | `reason: String?` |

---

### 枚举

#### TrackDesc

| 枚举值 | 原始值 | 说明 |
| --- | --- | --- |
| `mic` | `mic` | 麦克风音频 |
| `cameraBig` | `camera_big` | 摄像头大流 |
| `cameraSmall` | `camera_small` | 摄像头小流 |
| `screen` | `screen` | 屏幕共享 |

#### Role

| 枚举值 | 原始值 | 说明 |
| --- | --- | --- |
| `member` | `0` | 普通成员 |
| `host` | `1` | 主持人 |
| `coHost` | `2` | 联席主持人 |

#### MicState / CameraState

| 枚举值 | 原始值 | 说明 |
| --- | --- | --- |
| `on` | `1` | 开 |
| `off` | `2` | 关 |

#### ShareType

| 枚举值 | 原始值 | 说明 |
| --- | --- | --- |
| `screen` | `1` | 屏幕共享 |
| `whiteBoard` | `2` | 电子白板 |

#### HandupType

| 枚举值 | 原始值 | 说明 |
| --- | --- | --- |
| `mic` | `1` | 申请开麦克风 |
| `camera` | `2` | 申请开摄像头 |
| `chat` | `3` | 申请聊天 |
| `share` | `4` | 申请共享 |

#### UserHandupStep

| 枚举值 | 原始值 | 说明 |
| --- | --- | --- |
| `request` | `1` | 请求举手 |
| `cancel` | `2` | 取消举手 |
| `confirmOpen` | `3` | 确认打开设备 |
| `rejectOpen` | `4` | 拒绝打开设备 |

#### ChatMsgType

| 枚举值 | 原始值 | 说明 |
| --- | --- | --- |
| `text` | `1` | 文本 |
| `file` | `2` | 文件 |
| `pic` | `3` | 图片 |
| `sound` | `4` | 语音 |

#### MeetingType

| 枚举值 | 原始值 | 说明 |
| --- | --- | --- |
| `instant` | `1` | 即时会议 |
| `appointment` | `2` | 预约会议 |

#### MeetingMode

| 枚举值 | 原始值 | 说明 |
| --- | --- | --- |
| `normal` | `1` | 普通模式（非合成） |
| `mix` | `2` | 合成模式 |
| `voice` | `3` | 语音会议 |
| `training` | `4` | 培训会议 |
| `subMeeting` | `5` | 分会场（小组） |

#### MeetingStatus

| 枚举值 | 原始值 | 说明 |
| --- | --- | --- |
| `unStart` | `1` | 未开始 |
| `running` | `2` | 进行中 |
| `end` | `3` | 已结束 |

#### AttendType

| 枚举值 | 原始值 | 说明 |
| --- | --- | --- |
| `unLimit` | `1` | 无限制 |
| `password` | `2` | 密码进入 |
| `invite` | `3` | 仅邀请人员参会 |
| `passwordAndInvite` | `4` | 密码 + 仅邀请人员 |

#### EndType

| 枚举值 | 原始值 | 说明 |
| --- | --- | --- |
| `normal` | `0` | 正常（延迟）结束 |
| `force` | `1` | 强制结束 |

#### EntryMutePolicy

| 枚举值 | 原始值 | 说明 |
| --- | --- | --- |
| `silent` | `1` | 所有人入会默认静音 |
| `unRestrict` | `2` | 不限制，跟随客户端初始音频状态 |
| `silentAfter6` | `3` | 超过 6 人后入会默认静音 |

#### MeetingStreamVendor

| 枚举值 | 原始值 |
| --- | --- |
| `ook` | `ook` |
| `seastart` | `seastart` |
| `wangsuCDN` | `wangsucdn` |

不确定该填哪一个时不要传，让服务端按部署配置决定。

#### UserType

| 枚举值 | 原始值 | 说明 |
| --- | --- | --- |
| `normal` | `1` | 普通用户 |
| `sip` | `2` | SIP 用户 |
| `h323` | `3` | H.323 用户 |

#### McuTaskType

| 枚举值 | 原始值 | 说明 |
| --- | --- | --- |
| `record` | `1` | 录像模式 |
| `mix` | `2` | 合流模式 |
| `mixAndRecord` | `3` | 合流并录制 |

#### McuTaskStatus

| 枚举值 | 原始值 | 说明 |
| --- | --- | --- |
| `running` | `1` | 进行中 |
| `exception` | `2` | 异常结束 |
| `normal` | `3` | 正常结束 |

#### LayoutType

| 枚举值 | 原始值 | 说明 |
| --- | --- | --- |
| `auto` | `auto` | 自动布局 |
| `full` | `full` | 全屏 |
| `grids2` | `grids_2` | 二等分 |
| `grids3` | `grids_3` | 品字形 |
| `grids4` | `grids_4` | 四宫格 |
| `grids5` | `grids_5` | 五宫格 |
| `grids6` | `grids_6` | 六宫格 |
| `grids8` | `grids_8` | 八宫格 |
| `grids9` | `grids_9` | 九宫格 |
| `grids10` | `grids_10` | 十宫格 |
| `grids12` | `grids_12` | 十二宫格 |
| `grids16` | `grids_16` | 十六宫格 |
| `grids20` | `grids_20` | 二十宫格 |
| `grids25` | `grids_25` | 二十五宫格 |
| `right4` | `right_4` | 右侧小窗口 |
| `top4` | `top_4` | 顶部小窗口 |
| `br7` | `br_7` | 下 L 型布局 |
| `tl7` | `tl_7` | 上 L 型布局 |
| `tb8` | `tb_8` | 左右布局 |

#### AgentType

| 枚举值 | 原始值 | 说明 |
| --- | --- | --- |
| `sip` | `2` | SIP |
| `h323` | `3` | H.323 |
| `gb28181` | `4` | GB28181 |
| `rtsp` | `5` | RTSP 拉流 |
| `rtmp` | `6` | RTMP 拉流 |
| `filePlay` | `7` | 文件播放 |
| `tencentMeet` | `8` | 腾讯会议 |
| `ai` | `9` | AI |

#### AgentStatus

| 枚举值 | 原始值 | 说明 |
| --- | --- | --- |
| `idle` | `1` | 空闲 |
| `busy` | `2` | 忙碌 |
| `offline` | `3` | 离线 |

#### PresignedPutObjectType

| 枚举值 | 原始值 | 说明 |
| --- | --- | --- |
| `attach` | `attach` | 会议附件 |
| `background` | `background` | 背景图 |
| `user` | `user` | 用户资源 |

---

### 来自 SRTC 的类型

以下类型定义在底层 SRTC 模块，使用时需要 `import SRTC`：`LogLevel`、`CameraPreset`、`MicPreset`、`ScreenPreset`、`DeviceInfo`、`DisconnectReason`、`SRTCVideoView`、`SRTCVideoRenderer`、`ScreenCaptureSources`、`DisplaySource`、`WindowSource`、`LocalCameraTrack`、`LocalScreenTrack`、`RemoteVideoTrack`、`Track`。

`NativeVideoView` 是 SMeeting 为渲染视图定义的别名，实际类型是 `SRTCVideoRenderer`。

---

### 相关页面

+ [事件参考](/zh/meeting/swift/events)
+ [错误处理](/zh/meeting/swift/error-codes)
