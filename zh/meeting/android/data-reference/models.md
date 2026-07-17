---
title: "模型类型"
description: "Android SMeeting 会议 SDK 数据模型与参数定义"
---

### CreateImmediateMeetingOption

| 属性名称 | 数据类型 | 说明 |
| --- | --- | --- |
| roomNo | String? | 房间号 |
| content | String? | 会议说明 |
| attendType | AttendType? | 入会方式类型 |
| conferees | `MutableList<String>?` | 参会成员 uid 列表 |
| password | String? | 密码 |
| mode | MeetingMode? | 会议模式 |
| planTime | Long? | 开始时间时间戳 |
| planDur | Int? | 会议时长 |
| autoRecord | Boolean? | 是否开启自动录制 |
| entryMutePolicy | MuteState? | 入会静音状态 |
| watermarkDisabled | Boolean? | 水印是否禁用 |
| screenshotDisabled | Boolean? | 截屏是否禁用 |
| chatDisabled | Boolean? | 聊天是否禁用 |
| waitingRoomDisabled | Boolean? | 等候室是否禁用 |
| enterBeforeHostDisabled | Boolean? | 是否禁止在主持人前入会 |
| extendInfo | String? | 自定义扩展字段 |

### CreateScheduleMeetingOption

| 属性名称 | 数据类型 | 说明 |
| --- | --- | --- |
| roomNo | String? | 房间号 |
| content | String? | 会议说明 |
| attendType | AttendType? | 入会方式类型 |
| conferees | `MutableList<String>?` | 参会成员 uid 列表 |
| password | String? | 密码 |
| mode | MeetingMode? | 会议模式 |
| autoRecord | Boolean? | 是否开启自动录制 |
| entryMutePolicy | MuteState? | 入会静音状态 |
| watermarkDisabled | Boolean? | 水印是否禁用 |
| screenshotDisabled | Boolean? | 截屏是否禁用 |
| chatDisabled | Boolean? | 聊天是否禁用 |
| waitingRoomDisabled | Boolean? | 等候室是否禁用 |
| enterBeforeHostDisabled | Boolean? | 是否禁止在主持人前入会 |
| extendInfo | String? | 自定义扩展字段 |

### UpdateMeetingOption

| 属性名称 | 数据类型 | 说明 |
| --- | --- | --- |
| title | String? | 会议标题 |
| content | String? | 会议说明 |
| attendType | AttendType? | 入会方式类型 |
| conferees | `MutableList<String>?` | 参会成员 uid 列表 |
| password | String? | 密码 |
| mode | MeetingMode? | 会议模式 |
| planTime | Long? | 开始时间时间戳 |
| planDur | Int? | 会议时长 |
| autoRecord | Boolean? | 是否开启自动录制 |
| entryMutePolicy | MuteState? | 入会静音状态 |
| watermarkDisabled | Boolean? | 水印是否禁用 |
| screenshotDisabled | Boolean? | 截屏是否禁用 |
| chatDisabled | Boolean? | 聊天是否禁用 |
| waitingRoomDisabled | Boolean? | 等候室是否禁用 |
| enterBeforeHostDisabled | Boolean? | 是否允许主持人前入会（源码注释为“是否允许进入会”） |
| extendInfo | String? | 自定义扩展字段 |

### ScreenNotificationOption

| 属性名称 | 数据类型 | 说明 |
| --- | --- | --- |
| smallIcon | Int | 通知小图标资源 ID |
| title | String? | 通知标题 |
| desc | String? | 通知描述 |
| buttonText | String? | 按钮文案 |

### MeetingInfo

| 属性名称 | 数据类型 | 说明 |
| --- | --- | --- |
| id | String | 会议 ID |
| roomNo | String | 房间号 |
| title | String | 会议标题 |
| content | String? | 会议说明 |
| meetingType | MeetingType | 会议类型（由 `_meetingType` 映射） |
| meetingMode | MeetingMode | 会议模式（由 `_meetingMode` 映射） |
| planTime | Long | 预约时间 |
| planDur | Long | 预约时长 |
| entryMutePolicy | MuteState | 入会静音策略（由 `_entryMutePolicy` 映射） |
| watermarkDisabled | Boolean | 水印禁用状态 |
| screenshotDisabled | Boolean | 截屏禁用状态 |
| chatDisabled | Boolean | 聊天禁用状态 |
| micDisabled | Boolean | 麦克风禁用状态 |
| cameraDisabled | Boolean | 摄像头禁用状态 |
| selfUnmuteMicDisabled | Boolean | 是否禁止自我解除禁音 |
| selfUnmuteCameraDisabled | Boolean | 是否禁止自我解除禁画 |
| shareDisabled | Boolean | 共享禁用状态 |
| locked | Boolean | 房间锁定状态 |
| waitingRoomDisabled | Boolean | 等候室禁用状态 |
| enterBeforeHostDisabled | Boolean | 禁止在主持人前入会状态 |
| shareState | ShareType | 共享状态（由 `_shareState` 映射） |
| recordStatus | CloudRecordStatus | 录制状态（由 `_recordStatus` 映射） |
| parent | String | 主会议 ID（子会议场景） |
| shareUid | String? | 共享者 uid |
| creator | String | 创建者 uid |
| hostUid | String | 主持人 uid |
| coHosts | `MutableList<String>` | 联席主持人 uid 列表 |
| extendInfo | JsonElement? | 自定义扩展（由 `_extendInfo` 映射） |

### MemberInfo

| 属性名称 | 数据类型 | 说明 |
| --- | --- | --- |
| uid | String? | 三方平台用户 ID |
| name | String? | 用户名 |
| deviceType | DeviceType | 设备类型（由 `_deviceType` 映射） |
| deviceId | String? | 终端唯一编号 |
| version | String? | SDK 版本号 |
| joinAt | Long | 加入时间 |
| role | MemberRoleType | 会中角色（由 `_role` 映射） |
| avatar | String? | 会中头像 |
| micState | DeviceState | 麦克风状态（由 `_micState` 映射） |
| cameraState | DeviceState | 摄像头状态（由 `_cameraState` 映射） |
| shareState | ShareType | 共享状态（由 `_shareState` 映射） |
| drawDisabled | Boolean | 白板涂鸦禁用状态 |
| chatDisabled | Boolean | 聊天禁用状态 |
| extendInfo | JsonElement? | 自定义扩展（由 `_extendInfo` 映射） |

### McuAlarm

| 属性名称 | 数据类型 | 说明 |
| --- | --- | --- |
| taskId | String | MCU 任务 ID |
| taskStatus | McuAlarmStatus | MCU 任务状态（由 `_taskStatus` 映射） |
| gw | String | 告警所在网关 |
| alarmAt | Long | 告警时间戳 |
| alarmBrief | String | 告警摘要信息 |

### ImContent.CallingMsg

| 属性名称 | 数据类型 | 说明 |
| --- | --- | --- |
| roomNo | String | 房间号 |
| meetingId | String | 会议 ID |
| title | String | 会议标题 |

### ImContent.MeetingRemind

| 属性名称 | 数据类型 | 说明 |
| --- | --- | --- |
| meetingId | String | 会议 ID |
| title | String | 会议标题 |
| roomNo | String | 会议号 |
| creatorUid | String | 创建者 uid |
| creatorName | String | 创建者昵称 |
| planTime | Long | 预计开始时间 |
| planDur | Int | 预计持续时长 |

### ImContent.MoveOutWaitingRoom

| 属性名称 | 数据类型 | 说明 |
| --- | --- | --- |
| meetingId | String | 会议 ID |
| title | String | 会议名称 |

### ImContent.UserHelpSubMeeting

| 属性名称 | 数据类型 | 说明 |
| --- | --- | --- |
| parent | String | 主会场会议 ID |
| meetingId | String | 分会场会议 ID |
| title | String | 分会场名称 |

### BaseBean

| 属性名称 | 数据类型 | 说明 |
| --- | --- | --- |
| code | Int | 业务状态码 |
| msg | String | 响应消息 |

### `Data<T>`

| 属性名称 | 数据类型 | 说明 |
| --- | --- | --- |
| code | Int | 继承自 `BaseBean` 的业务状态码 |
| msg | String | 继承自 `BaseBean` 的响应消息 |
| data | T | 业务数据 |

### `Data2<T>`

| 属性名称 | 数据类型 | 说明 |
| --- | --- | --- |
| code | Int | 继承自 `BaseBean` 的业务状态码 |
| msg | String | 继承自 `BaseBean` 的响应消息 |
| data | T | 业务数据 |
| _meta | MetaBean | 分页信息 |

### MetaBean

| 属性名称 | 数据类型 | 说明 |
| --- | --- | --- |
| totalCount | Int | 总条目数 |
| pageCount | Int | 总页数 |
| currentPage | Int | 当前页号（从 1 开始） |
| perPage | Int | 每页最大条目数 |

### LoginBean

| 属性名称 | 数据类型 | 说明 |
| --- | --- | --- |
| meet_sid | String | 会议会话标识 |
| exp_at | Long | 过期时间戳 |

### UserBean

| 属性名称 | 数据类型 | 说明 |
| --- | --- | --- |
| deviceId | String | 设备唯一 ID |
| deviceType | DeviceType | 设备类型（由整型字段映射） |
| expAt | Long | 过期时间 |
| uid | String | 参会用户 ID |

### MeetingCreatedBean

| 属性名称 | 数据类型 | 说明 |
| --- | --- | --- |
| meetingId | String | 会议 ID |
| roomNo | String | 会议号 |

### MeetInfo

| 属性名称 | 数据类型 | 说明 |
| --- | --- | --- |
| id | String | 会议 ID |
| title | String | 会议标题 |
| roomNo | String | 房间号 |
| password | String | 会议密码 |
| attendType | AttendType | 入会方式类型 |
| meetingStatus | MeetingStatus | 会议状态 |
| meetingType | MeetingType | 会议类型 |
| planTime | Long | 计划开始时间（秒） |
| planDur | Int | 计划持续时长（分钟） |
| beginTime | Long | 实际开始时间（秒） |
| endTime | Long | 实际结束时间（秒） |
| creator | String | 创建者 uid |
| conferee | `ArrayList<String>` | 会前邀请成员 uid 列表 |
| createdAt | Long | 创建时间（秒） |

### MeetDetail

| 属性名称 | 数据类型 | 说明 |
| --- | --- | --- |
| id | String | 会议 ID |
| roomNo | String | 房间号 |
| title | String | 会议标题 |
| content | String | 会议说明 |
| creator | String | 创建者 uid |
| attendType | AttendType | 入会方式类型 |
| password | String | 入会密码 |
| meetingStatus | MeetingStatus | 会议状态 |
| meetingType | MeetingType | 会议类型 |
| meetingMode | MeetingMode | 会议模式 |
| autoRecord | Boolean | 是否自动录制 |
| planTime | Long | 计划开始时间（秒） |
| planDur | Int | 计划持续时长（分钟） |
| beginTime | Long | 实际开始时间（秒） |
| endTime | Long | 实际结束时间（秒） |
| onlineNum | Int | 在线人数 |
| entryMutePolicy | MuteState | 入会静音策略 |
| watermarkDisabled | Boolean | 水印禁用状态 |
| screenshotDisabled | Boolean | 截屏禁用状态 |
| chatDisabled | Boolean | 聊天禁用状态 |
| locked | Boolean | 房间锁定状态 |
| shareState | Int | 共享状态值 |
| micDisabled | Boolean | 麦克风禁用状态 |
| cameraDisabled | Boolean | 摄像头禁用状态 |
| selfUnmuteMicDisabled | Boolean | 是否允许自我解除禁音 |
| selfUnmuteCameraDisabled | Boolean | 是否允许自我解除禁画 |
| waitingRoomDisabled | Boolean | 等候室禁用状态 |
| enterBeforeHostDisabled | Boolean | 是否禁止主持人前入会 |
| conferee | `List<String>` | 会前邀请成员 uid 列表 |

### MemberBean

| 属性名称 | 数据类型 | 说明 |
| --- | --- | --- |
| uid | String | 用户 ID（兼容 `user_id` / `uid`） |
| nickname | String | 用户昵称（兼容 `nickname` / `name`） |
| deviceType | Int? | 设备类型值 |
| joinAt | Long? | 加入时间 |

### MemberRequestBean

| 属性名称 | 数据类型 | 说明 |
| --- | --- | --- |
| uid | String | 用户 ID |
| name | String | 用户昵称 |

### WaitingRoomUserBean

| 属性名称 | 数据类型 | 说明 |
| --- | --- | --- |
| uid | String | 用户 ID |
| nickName | String | 用户昵称 |
| at | Long | 成员进入时间戳 |

### SubMeetingBean

| 属性名称 | 数据类型 | 说明 |
| --- | --- | --- |
| id | String | 小组 ID |
| mainMeetingId | String | 主会议 ID |
| meetingId | String | 子会议 ID |
| status | SubMeetingStatus | 子会议状态（由 `_status` 映射） |
| title | String | 小组名称 |
| users | `MutableList<MemberBean>?` | 用户列表 |

### AgentRequestBean

| 属性名称 | 数据类型 | 说明 |
| --- | --- | --- |
| type | AgentType | 设备类型 |
| contact | String | 设备标识 |

### AgentBean

| 属性名称 | 数据类型 | 说明 |
| --- | --- | --- |
| id | String | 设备 ID |
| name | String | 设备名称 |
| type | AgentType | 设备类型（由 `_type` 映射） |
| status | AgentStatus | 设备状态（由 `_status` 映射） |
| contact | String | 设备标识 |
| remark | String? | 备注 |
| connParams | AgentBean.ConnParams? | 连接参数 |

### AgentBean.ConnParams

| 属性名称 | 数据类型 | 说明 |
| --- | --- | --- |
| subjects | `MutableMap<String, String>?` | 通道列表映射 |

### ChatMsgBean

| 属性名称 | 数据类型 | 说明 |
| --- | --- | --- |
| id | String | 消息 ID |
| meetingId | String | 会议 ID |
| senderId | String | 发送者 ID |
| senderName | String | 发送者昵称 |
| msgType | Int | 消息类型（1 文本，2 文件，3 图片，4 语音） |
| msg | String | 消息内容 |
| createdAt | Int | 创建时间（毫秒） |

### LayoutData

| 属性名称 | 数据类型 | 说明 |
| --- | --- | --- |
| layout | String | 布局类型，默认 `auto` |
| pollingDur | Int | 轮询时长（秒） |
| watermark | LayoutData.Watermark? | 水印配置 |
| tag | LayoutData.Tag? | 默认标签配置 |
| divList | `List<LayoutData.Div>?` | 逻辑块列表 |

### LayoutData.Watermark

| 属性名称 | 数据类型 | 说明 |
| --- | --- | --- |
| type | Int | 水印类型（0 默认，1 无，2 单排，3 多排） |
| text | String | 指定内容（空表示自动） |
| size | Int | 字体大小（0 表示默认） |
| color | String | 字体颜色（空表示默认） |
| olColor | String | 轮廓颜色（空表示默认） |
| olWidth | Int | 轮廓线宽（0 表示默认） |

### LayoutData.Tag

| 属性名称 | 数据类型 | 说明 |
| --- | --- | --- |
| type | String | 标签位置类型（如 L/R/T/B 组合） |
| text | String | 指定内容（空表示自动） |
| size | Int | 字体大小（0 表示默认） |
| color | String | 字体颜色（空表示默认） |
| bgColor | String | 背景颜色（空表示默认） |

### LayoutData.Div

| 属性名称 | 数据类型 | 说明 |
| --- | --- | --- |
| cell | `List<LayoutData.Cell>` | 宫格列表 |
| uids | `List<String>` | 用户 ID 列表 |

### LayoutData.Cell

| 属性名称 | 数据类型 | 说明 |
| --- | --- | --- |
| idx | Int | 格子序号 |
| bindShare | Boolean | 是否优化绑定频道内共享流 |
| tag | LayoutData.Tag | 标签配置 |
