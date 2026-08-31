---
title: "模型类型"
description: "SMeeting Android 2.0.35 公开接口直接使用的配置、结果、会议、成员、点名、签到、IM 与录制布局模型"
---

本页只列出 `MeetingEngine`、公开 manager、事件和结果回调直接暴露的 Meeting 模型。`RTCMediaOptions`、`TrackInfo`、`RemoteVideoTrack`、设备能力和媒体统计等来自传递依赖 SRTC，详见 [SRTC Android 模型类型](/zh/rtc/android/types)。

## 配置模型

### CreateImmediateMeetingOption

创建即时会议的可选参数。所有字段都有默认 `null`，服务端按缺省规则处理未设置项。

| 属性 | 类型 | 说明 |
| --- | --- | --- |
| `roomNo` | `String?` | 自定义房间号 |
| `content` | `String?` | 会议说明 |
| `attendType` | `AttendType?` | 入会方式 |
| `conferees` | `MutableList<String>?` | 受邀成员 UID 列表 |
| `password` | `String?` | 入会密码 |
| `mode` | `MeetingMode?` | 会议模式 |
| `planTime` | `Long?` | 可选计划开始时间，秒级时间戳 |
| `planDur` | `Int?` | 可选计划时长，单位分钟 |
| `autoRecord` | `Boolean?` | 是否自动录制 |
| `entryMutePolicy` | `MuteState?` | 入会静音策略 |
| `watermarkDisabled` | `Boolean?` | 是否禁用水印 |
| `screenshotDisabled` | `Boolean?` | 是否禁用截屏 |
| `chatDisabled` | `Boolean?` | 是否禁用聊天 |
| `waitingRoomDisabled` | `Boolean?` | 是否禁用等候室 |
| `enterBeforeHostDisabled` | `Boolean?` | 是否禁止主持人前入会 |
| `extendInfo` | `String?` | 应用自定义扩展字符串 |

### CreateScheduleMeetingOption

创建预约会议的可选参数。`planTime` 与 `planDur` 由 `createScheduleMeeting()` 的独立参数传入，因此本类型不重复定义。

| 属性 | 类型 | 说明 |
| --- | --- | --- |
| `roomNo` | `String?` | 自定义房间号 |
| `content` | `String?` | 会议说明 |
| `attendType` | `AttendType?` | 入会方式 |
| `conferees` | `MutableList<String>?` | 受邀成员 UID 列表 |
| `password` | `String?` | 入会密码 |
| `mode` | `MeetingMode?` | 会议模式 |
| `autoRecord` | `Boolean?` | 是否自动录制 |
| `entryMutePolicy` | `MuteState?` | 入会静音策略 |
| `watermarkDisabled` | `Boolean?` | 是否禁用水印 |
| `screenshotDisabled` | `Boolean?` | 是否禁用截屏 |
| `chatDisabled` | `Boolean?` | 是否禁用聊天 |
| `waitingRoomDisabled` | `Boolean?` | 是否禁用等候室 |
| `enterBeforeHostDisabled` | `Boolean?` | 是否禁止主持人前入会 |
| `extendInfo` | `String?` | 应用自定义扩展字符串 |

### UpdateMeetingOption

会前更新会议的可选字段。保持 `null` 的字段不参与更新。

| 属性 | 类型 | 说明 |
| --- | --- | --- |
| `title` | `String?` | 新会议标题 |
| `content` | `String?` | 新会议说明 |
| `attendType` | `AttendType?` | 入会方式 |
| `conferees` | `MutableList<String>?` | 受邀成员 UID 列表 |
| `password` | `String?` | 入会密码 |
| `mode` | `MeetingMode?` | 会议模式 |
| `planTime` | `Long?` | 计划开始时间，秒级时间戳 |
| `planDur` | `Int?` | 计划时长，单位分钟 |
| `autoRecord` | `Boolean?` | 是否自动录制 |
| `entryMutePolicy` | `MuteState?` | 入会静音策略 |
| `watermarkDisabled` | `Boolean?` | 是否禁用水印 |
| `screenshotDisabled` | `Boolean?` | 是否禁用截屏 |
| `chatDisabled` | `Boolean?` | 是否禁用聊天 |
| `waitingRoomDisabled` | `Boolean?` | 是否禁用等候室 |
| `enterBeforeHostDisabled` | `Boolean?` | 是否禁止主持人前入会 |
| `extendInfo` | `String?` | 应用自定义扩展字符串 |

### ScreenNotificationOption

Android 屏幕采集前台服务通知配置。

| 属性 | 类型 | 说明 |
| --- | --- | --- |
| `smallIcon` | `Int` | 通知栏小图标资源 ID |
| `title` | `String?` | 通知标题 |
| `desc` | `String?` | 通知描述 |
| `buttonText` | `String?` | 通知操作按钮文案 |

## 通用结果

### MeetingPage&lt;T&gt;

公共接口使用的稳定分页结果，不暴露服务端 `_meta` 包装。

| 属性 | 类型 | 说明 |
| --- | --- | --- |
| `items` | `List<T>` | 当前页业务数据 |
| `totalCount` | `Int` | 全部条目数 |
| `pageCount` | `Int` | 全部页数 |
| `currentPage` | `Int` | 当前页码，从 1 开始 |
| `perPage` | `Int` | 每页最大条目数 |

### MeetingDownload

文件下载成功后返回的一次性数据流，实现 `Closeable`。

| 属性 / 方法 | 类型 | 说明 |
| --- | --- | --- |
| `fileName` | `String?` | 服务端文件名；响应未携带时为 `null` |
| `inputStream` | `InputStream` | 与当前响应绑定的一次性数据流 |
| `close()` | `Unit` | 关闭数据流与底层网络响应；可重复调用 |

```kotlin
download.use { result ->
    result.inputStream.copyTo(outputStream)
}
```

### MeetingEnterInfo

入会成功后返回的会议身份信息，只表示结果，不是会话控制对象。

| 属性 | 类型 | 说明 |
| --- | --- | --- |
| `meetingId` | `String` | 当前加入的会议 ID |
| `uid` | `String` | 当前用户在会议中的 UID |

### MeetingImConnection

IM 建链成功后的连接标识。

| 属性 | 类型 | 说明 |
| --- | --- | --- |
| `uid` | `String` | 当前用户 IM UID |
| `sid` | `String` | 当前 IM 会话标识 |

## 当前会议状态

### MeetingInfo

SRTC 频道属性转换得到的当前房间快照。

| 属性 | 类型 | 说明 |
| --- | --- | --- |
| `id` | `String` | 会议 ID |
| `roomNo` | `String` | 房间号 |
| `title` | `String` | 会议标题 |
| `content` | `String?` | 会议说明 |
| `meetingType` | `MeetingType` | 即时或预约会议 |
| `meetingMode` | `MeetingMode` | 会议模式 |
| `planTime` | `Long` | 计划开始时间，秒级时间戳 |
| `planDur` | `Long` | 计划时长，单位分钟 |
| `entryMutePolicy` | `MuteState` | 入会静音策略 |
| `watermarkDisabled` | `Boolean` | 是否禁用水印 |
| `screenshotDisabled` | `Boolean` | 是否禁用截屏 |
| `chatDisabled` | `Boolean` | 是否禁用聊天 |
| `micDisabled` | `Boolean` | 是否全体禁音 |
| `cameraDisabled` | `Boolean` | 是否全体禁画 |
| `selfUnmuteMicDisabled` | `Boolean` | 是否禁止成员自行解除禁音 |
| `selfUnmuteCameraDisabled` | `Boolean` | 是否禁止成员自行解除禁画 |
| `shareDisabled` | `Boolean` | 是否禁止共享 |
| `locked` | `Boolean` | 房间是否锁定 |
| `waitingRoomDisabled` | `Boolean` | 是否禁用等候室 |
| `enterBeforeHostDisabled` | `Boolean` | 是否禁止主持人前入会 |
| `shareState` | `ShareType` | 当前共享类型 |
| `recordStatus` | `CloudRecordStatus` | 当前云录制状态 |
| `parent` | `String` | 主会议 ID；主会场通常为空字符串 |
| `shareUid` | `String?` | 当前共享者 UID |
| `creator` | `String` | 创建者 UID |
| `hostUid` | `String` | 主持人 UID |
| `coHosts` | `MutableList<String>` | 联席主持人 UID 列表 |
| `extendInfo` | `JsonElement?` | 解析后的业务扩展 JSON |

### MemberInfo

当前会议成员快照。

| 属性 | 类型 | 说明 |
| --- | --- | --- |
| `uid` | `String?` | 成员 UID |
| `name` | `String?` | 会中昵称 |
| `deviceType` | `DeviceType` | SRTC 设备类型 |
| `deviceId` | `String?` | 终端唯一编号 |
| `version` | `String?` | 对端 SDK 版本 |
| `joinAt` | `Long` | 加入时间 |
| `role` | `MemberRoleType` | 会中角色 |
| `avatar` | `String?` | 头像 |
| `micState` | `DeviceState` | 麦克风状态 |
| `cameraState` | `DeviceState` | 摄像头状态 |
| `shareState` | `ShareType` | 共享状态 |
| `drawDisabled` | `Boolean` | 是否禁止白板涂鸦 |
| `chatDisabled` | `Boolean` | 是否禁止聊天 |
| `extendInfo` | `JsonElement?` | 解析后的业务扩展 JSON |

### McuAlarm

| 属性 | 类型 | 说明 |
| --- | --- | --- |
| `taskId` | `String` | MCU 任务 ID |
| `taskStatus` | `McuAlarmStatus` | MCU 任务状态 |
| `gw` | `String` | 告警所在网关 |
| `alarmAt` | `Long` | 告警时间戳 |
| `alarmBrief` | `String` | 告警摘要 |

## 会前会议模型

### UserBean

| 属性 | 类型 | 说明 |
| --- | --- | --- |
| `deviceId` | `String` | 当前终端唯一 ID |
| `deviceType` | `DeviceType` | SRTC 设备类型 |
| `expAt` | `Long` | 用户授权过期时间 |
| `uid` | `String` | 参会用户 ID |

### MeetingCreatedBean

| 属性 | 类型 | 说明 |
| --- | --- | --- |
| `meetingId` | `String` | 新建会议 ID |
| `roomNo` | `String` | 新建会议房间号 |

### MeetInfo

会议列表项。Java 类型通过 getter 读取属性。

| 属性 | 类型 | 说明 |
| --- | --- | --- |
| `id` | `String` | 会议 ID |
| `title` | `String` | 会议标题 |
| `roomNo` | `String` | 房间号 |
| `attendType` | `AttendType` | 入会方式 |
| `meetingStatus` | `MeetingStatus` | 会议状态 |
| `meetingType` | `MeetingType` | 会议类型 |
| `planTime` | `Long` | 计划开始时间，秒级时间戳 |
| `planDur` | `Int` | 计划时长，单位分钟 |
| `beginTime` | `Long` | 实际开始时间，秒级时间戳 |
| `endTime` | `Long` | 实际结束时间，秒级时间戳 |
| `creator` | `String` | 创建者 UID |
| `conferee` | `ArrayList<String>` | 受邀成员 UID 列表 |
| `createdAt` | `Long` | 创建时间，秒级时间戳 |

### MeetDetail

| 属性 | 类型 | 说明 |
| --- | --- | --- |
| `id` | `String` | 会议 ID |
| `roomNo` | `String` | 房间号 |
| `title` | `String` | 会议标题 |
| `content` | `String` | 会议说明 |
| `creator` | `String` | 创建者 UID |
| `attendType` | `AttendType` | 入会方式 |
| `password` | `String` | 入会密码 |
| `meetingStatus` | `MeetingStatus` | 会议状态 |
| `meetingType` | `MeetingType` | 会议类型 |
| `meetingMode` | `MeetingMode` | 会议模式 |
| `autoRecord` | `Boolean?` | 是否自动录制 |
| `planTime` | `Long?` | 计划开始时间，秒级时间戳 |
| `planDur` | `Int?` | 计划时长，单位分钟 |
| `beginTime` | `Long?` | 实际开始时间，秒级时间戳 |
| `endTime` | `Long?` | 实际结束时间，秒级时间戳 |
| `onlineNum` | `Int?` | 在线人数 |
| `entryMutePolicy` | `MuteState` | 入会静音策略 |
| `watermarkDisabled` | `Boolean?` | 是否禁用水印 |
| `screenshotDisabled` | `Boolean?` | 是否禁用截屏 |
| `chatDisabled` | `Boolean?` | 是否禁用聊天 |
| `locked` | `Boolean?` | 是否锁定 |
| `shareState` | `Int?` | 原始共享状态值 |
| `micDisabled` | `Boolean?` | 是否全体禁音 |
| `cameraDisabled` | `Boolean?` | 是否全体禁画 |
| `selfUnmuteMicDisabled` | `Boolean?` | 是否禁止自行解除禁音 |
| `selfUnmuteCameraDisabled` | `Boolean?` | 是否禁止自行解除禁画 |
| `waitingRoomDisabled` | `Boolean?` | 是否禁用等候室 |
| `enterBeforeHostDisabled` | `Boolean?` | 是否禁止主持人前入会 |
| `conferee` | `List<String>` | 受邀成员 UID 列表 |

## 设备与邀请模型

### AgentRequestBean

| 属性 | 类型 | 说明 |
| --- | --- | --- |
| `type` | `AgentType` | 外部设备类型 |
| `contact` | `String` | 设备联系标识或拉流地址 |

### AgentBean

| 属性 | 类型 | 说明 |
| --- | --- | --- |
| `id` | `String` | 设备 ID |
| `name` | `String` | 设备名称 |
| `type` | `AgentType` | 设备类型 |
| `status` | `AgentStatus` | 在线状态 |
| `contact` | `String` | 设备联系标识 |
| `remark` | `String?` | 备注 |
| `connParams` | `AgentBean.ConnParams?` | 连接参数 |

### AgentBean.ConnParams

| 属性 | 类型 | 说明 |
| --- | --- | --- |
| `subjects` | `MutableMap<String, String>?` | 通道或主题映射 |

## 成员、等候室与讨论组

### MemberBean

| 属性 | 类型 | 说明 |
| --- | --- | --- |
| `uid` | `String` | 用户 UID |
| `nickname` | `String` | 用户昵称 |
| `deviceType` | `Int?` | 原始设备类型值 |
| `joinAt` | `Long?` | 加入时间 |

### MemberRequestBean

| 属性 | 类型 | 说明 |
| --- | --- | --- |
| `uid` | `String` | 用户 UID |
| `name` | `String` | 用户昵称 |

### WaitingRoomUserBean

| 属性 | 类型 | 说明 |
| --- | --- | --- |
| `uid` | `String` | 等候室用户 UID |
| `nickName` | `String` | 用户昵称 |
| `at` | `Long` | 进入等候室时间戳 |

### SubMeetingBean

| 属性 | 类型 | 说明 |
| --- | --- | --- |
| `id` | `String` | 讨论组记录 ID |
| `mainMeetingId` | `String` | 主会议 ID |
| `meetingId` | `String` | 子会议 ID |
| `status` | `SubMeetingStatus` | 子会议状态 |
| `title` | `String` | 讨论组标题 |
| `users` | `MutableList<MemberBean>?` | 分配成员列表 |

## 点名模型

### RollCallBean

| 属性 | 类型 | 说明 |
| --- | --- | --- |
| `id` | `String` | 点名活动 ID |
| `title` | `String` | 点名标题 |
| `method` | `Int` | `1` 自动，`2` 手动 |
| `meetingTitle` | `String` | 会议标题 |
| `total` | `Int` | 点名人数 |
| `status` | `Int` | `1` 进行中，`2` 已结束 |
| `createdAt` | `Long` | 创建时间，秒级时间戳 |

### RollCallDetailBean

| 属性 | 类型 | 说明 |
| --- | --- | --- |
| `id` | `String` | 点名活动 ID |
| `title` | `String` | 点名标题 |
| `method` | `Int` | `1` 自动，`2` 手动 |
| `meetingTitle` | `String` | 会议标题 |
| `total` | `Int` | 点名人数 |
| `status` | `Int` | `1` 进行中，`2` 已结束 |
| `users` | `List<RollCallUserBean>?` | 点名成员及应答状态 |
| `createdAt` | `Long` | 创建时间，秒级时间戳 |

### RollCallUserBean

| 属性 | 类型 | 说明 |
| --- | --- | --- |
| `id` | `String` | 点名用户记录 ID，呼叫和应答接口使用此值 |
| `userId` | `String` | 会议用户 UID |
| `userName` | `String` | 用户昵称 |
| `rollCallAt` | `Long` | 呼叫时间；`0` 表示未呼叫 |
| `answerAt` | `Long` | 应答时间；`0` 表示未应答 |
| `status` | `Int` | `0` 未点名，`1` 已点名未应答，`2` 已应答 |

## 签到模型

### SignInActivityBean

| 属性 | 类型 | 说明 |
| --- | --- | --- |
| `uid` | `String` | 发起者 UID |
| `beginAt` | `Long` | 开始时间，秒级时间戳 |
| `dur` | `Int` | 时长，单位分钟；`0` 不限时 |
| `endAt` | `Long` | 结束时间；不限时且未结束时为 `0` |
| `desc` | `String` | 活动说明 |
| `nums` | `Int` | 签到人数；活动未结束时可能为 `0` |

### SignInListBean

| 属性 | 类型 | 说明 |
| --- | --- | --- |
| `list` | `List<SignInActivityBean>?` | 签到活动列表 |
| `now` | `Long` | 当前服务端时间 |

### SignInCountBean

| 属性 | 类型 | 说明 |
| --- | --- | --- |
| `nums` | `Int` | 实际签到人数 |

### SignInRecordBean

| 属性 | 类型 | 说明 |
| --- | --- | --- |
| `id` | `String` | 签到记录 ID |
| `userId` | `String` | 用户 UID |
| `nickname` | `String` | 会中昵称 |
| `role` | `Int` | 原始会中角色值 |
| `epoch` | `Int` | 签到轮次，从 `0` 开始 |
| `createdAt` | `String` | 签到时间字符串 |

## 消息与 IM 模型

### ChatMsgBean

| 属性 | 类型 | 说明 |
| --- | --- | --- |
| `id` | `String` | 消息 ID |
| `meetingId` | `String` | 会议 ID |
| `senderId` | `String` | 发送者 UID |
| `senderName` | `String` | 发送者昵称 |
| `msgType` | `Int?` | 原始消息类型值 |
| `msg` | `String` | 消息内容 |
| `createdAt` | `Int?` | 创建时间，单位毫秒 |

### ImContent.CallingMsg

| 属性 | 类型 | 说明 |
| --- | --- | --- |
| `roomNo` | `String` | 房间号 |
| `meetingId` | `String` | 会议 ID |
| `title` | `String` | 会议标题 |

### ImContent.MeetingRemind

| 属性 | 类型 | 说明 |
| --- | --- | --- |
| `meetingId` | `String` | 会议 ID |
| `title` | `String` | 会议标题 |
| `roomNo` | `String` | 房间号 |
| `creatorUid` | `String` | 创建者 UID |
| `creatorName` | `String` | 创建者昵称 |
| `planTime` | `Long` | 计划开始时间 |
| `planDur` | `Int` | 计划时长，单位分钟 |

### ImContent.MoveOutWaitingRoom

| 属性 | 类型 | 说明 |
| --- | --- | --- |
| `meetingId` | `String` | 目标会议 ID |
| `title` | `String` | 目标会议标题 |

### ImContent.UserHelpSubMeeting

| 属性 | 类型 | 说明 |
| --- | --- | --- |
| `parent` | `String` | 主会议 ID |
| `meetingId` | `String` | 子会议 ID |
| `title` | `String` | 讨论组标题 |

## 云录制布局

### LayoutData

| 属性 | 类型 | 说明 |
| --- | --- | --- |
| `layout` | `String` | 布局类型，默认 `auto` |
| `pollingDur` | `Int` | 轮询时长，单位秒 |
| `watermark` | `LayoutData.Watermark?` | 水印配置 |
| `tag` | `LayoutData.Tag?` | 默认标签配置 |
| `divList` | `List<LayoutData.Div>?` | 逻辑块列表 |

### LayoutData.Watermark

| 属性 | 类型 | 说明 |
| --- | --- | --- |
| `type` | `Int` | `0` 默认，`1` 无，`2` 单排，`3` 多排 |
| `text` | `String` | 指定内容；空字符串表示自动使用会议标题 |
| `size` | `Int` | 字体大小；`0` 使用默认值 |
| `color` | `String` | 字体颜色；空字符串使用默认值 |
| `olColor` | `String` | 轮廓颜色；空字符串使用默认值 |
| `olWidth` | `Int` | 轮廓线宽；`0` 使用默认值 |

### LayoutData.Tag

| 属性 | 类型 | 说明 |
| --- | --- | --- |
| `type` | `String` | 标签位置，使用 `L` / `R` / `T` / `B` 或组合 |
| `text` | `String` | 指定内容；空字符串表示自动使用会中名称 |
| `size` | `Int` | 字体大小；`0` 使用默认值 |
| `color` | `String` | 字体颜色 |
| `bgColor` | `String` | 背景颜色 |

### LayoutData.Div

| 属性 | 类型 | 说明 |
| --- | --- | --- |
| `cell` | `List<LayoutData.Cell>` | 宫格列表 |
| `uids` | `List<String>` | 绑定用户 UID 列表 |

### LayoutData.Cell

| 属性 | 类型 | 说明 |
| --- | --- | --- |
| `idx` | `Int` | 格子序号 |
| `bindShare` | `Boolean` | 是否优先绑定频道内共享流 |
| `tag` | `LayoutData.Tag` | 标签配置 |
