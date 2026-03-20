---
title: "枚举类型"
description: "Android SMeeting 会议 SDK 枚举值定义"
---

### AgentStatus

| 枚举名 | 值 | 说明 |
| --- | --- | --- |
| Unknow | 0 | 未知 |
| Online | 1 | 在线 |
| Offline | 2 | 离线 |

### AgentType

| 枚举名 | 值 | 说明 |
| --- | --- | --- |
| SIP | 2 | SIP |
| H323 | 3 | H323 |
| GB28181 | 4 | GB28181 |
| RTSP | 5 | RTSP 拉流 |
| RTMP | 6 | RTMP 拉流 |
| FILE | 7 | 文件播放 |
| TENCENT | 8 | 腾讯会议 |
| AI | 9 | AI |

### AttendType

| 枚举名 | 值 | 说明 |
| --- | --- | --- |
| ATTEND_NOT_LIMIT | 1 | 无限制（默认） |
| ATTEND_BY_PWD | 2 | 密码进入 |
| ATTEND_ONLY_INVITE | 3 | 仅邀请人员参会 |

### ChangeReason

| 枚举名 | 值 | 说明 |
| --- | --- | --- |
| ChangeReasonBySelf | 0 | 自己操作 |
| ChangeReasonByAdmin | 1 | 主持人或联席主持人操作 |

### ChatMsgType

| 枚举名 | 值 | 说明 |
| --- | --- | --- |
| UnKnown | 0 | 未知（保底类型） |
| Text | 1 | 文本消息 |
| File | 2 | 文件消息 |
| Picture | 3 | 图片消息 |
| Voice | 4 | 语音消息 |
| Custom | 5 | 自定义消息 |

### CloudRecordStatus

| 枚举名 | 值 | 说明 |
| --- | --- | --- |
| Status_Not_Start | 0 | 未开始 |
| Status_Ing | 1 | 进行中 |
| Status_Not_End | 2 | 待结束 |
| Status_Error | 3 | 异常结束 |
| Status_Ended | 4 | 正常结束 |

### CloudRecordType

| 枚举名 | 值 | 说明 |
| --- | --- | --- |
| Mode_Video | 1 | 录像模式 |
| Mode_Mixture | 2 | 合流模式 |
| Mode_All | 3 | 混合模式 |

### DeviceState

| 枚举名 | 值 | 说明 |
| --- | --- | --- |
| Open | 1 | 开启 |
| Closed | 2 | 关闭 |

### DisconnectedImReason

| 枚举名 | 值 | 说明 |
| --- | --- | --- |
| Unknown | 0 | 未知 |
| KickOut | 2 | 被踢出 |
| BeReplaced | 3 | 被顶号 |
| HeartbeatTimeout | 4 | 心跳超时 |

### HandUpType

| 枚举名 | 值 | 说明 |
| --- | --- | --- |
| UnKnown | 0 | 未知（保底类型） |
| OpenMic | 1 | 申请开音频 |
| OpenCamera | 2 | 申请开视频 |
| Chat | 3 | 申请聊天 |
| Share | 4 | 申请共享 |
| Draw | 5 | 申请白板涂鸦 |

### LeaveMeetingReason

| 枚举名 | 值 | 说明 |
| --- | --- | --- |
| Unknown | 0 | 未知 |
| KickOut | 2 | 被踢出 |
| BeReplaced | 3 | 被顶号 |
| HeartbeatTimeout | 4 | 心跳超时 |
| ChannelDestroy | 5 | 频道销毁 |

### McuAlarmStatus

| 枚举名 | 值 | 说明 |
| --- | --- | --- |
| PendingStart | 0 | 待开始 |
| InProgress | 1 | 进行中 |
| PendingEnd | 2 | 待结束 |
| AbnormalEnd | 3 | 异常结束 |
| Finished | 4 | 已结束 |

### MeetingMode

| 枚举名 | 值 | 说明 |
| --- | --- | --- |
| Normal | 1 | 普通会议模式 |
| Mixture | 2 | 合成会议模式 |
| Voice | 3 | 语音会议 |
| Training | 4 | 培训模式 |
| SubMeet | 5 | 子会议 |

### MeetingStatus

| 枚举名 | 值 | 说明 |
| --- | --- | --- |
| STATUS_UNKNOW | -1 | 未知 |
| STATUS_PRE | 1 | 未开始 |
| STATUS_ING | 2 | 进行中 |
| STATUS_END | 3 | 已结束 |

### MeetingType

| 枚举名 | 值 | 说明 |
| --- | --- | --- |
| Immediate | 1 | 即时会议 |
| Schedule | 2 | 预约会议 |

### MemberRoleType

| 枚举名 | 值 | 说明 |
| --- | --- | --- |
| Normal | 0 | 普通成员 |
| Host | 1 | 主持人 |
| UnionHost | 2 | 联席主持人 |

### MuteState

| 枚举名 | 值 | 说明 |
| --- | --- | --- |
| MuteState1 | 1 | 开启入会静音（所有人入会默认静音） |
| MuteState2 | 2 | 关闭入会静音（跟随客户端初始音频状态） |
| MuteState3 | 3 | 超 6 人静音（超过 6 人后入会静音） |

### ShareType

| 枚举名 | 值 | 说明 |
| --- | --- | --- |
| Normal | 0 | 正常状态无共享 |
| ScreenShare | 1 | 屏幕共享 |
| WhiteBoardShare | 2 | 白板共享 |

### SubMeetingStatus

| 枚举名 | 值 | 说明 |
| --- | --- | --- |
| STATUS_UNKNOW | -1 | 未知 |
| STATUS_PRE | 1 | 未开始 |
| STATUS_ING | 2 | 进行中 |
| STATUS_END | 3 | 已结束 |

### UserType

| 枚举名 | 值 | 说明 |
| --- | --- | --- |
| Normal | 1 | 普通成员 |
| SIP | 2 | SIP 设备 |
| H323 | 3 | H323 设备 |
