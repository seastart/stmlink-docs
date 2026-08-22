---
title: "枚举类型与数据结构"
description: "Windows SMeeting SDK C++ 枚举类型与数据结构参考"
---

## 枚举类型

### StatusCode

| 值 | 名称 | 说明 |
| --- | --- | --- |
| 0 | OK | 成功 |
| 100001 | SystemError | 系统错误 |
| 100002 | NotInitialized | 未初始化 |
| 100003 | MediaNotInitialized | 媒体未初始化 |
| 100004 | ProtocolParsingError | 协议解析错误 |
| 100005 | Timeout | 超时 |
| 100006 | InvalidArgs | 参数无效 |
| 100007 | Conflict | 冲突 |
| 100008 | SdkTokenInvalid | Token 无效 |
| 100009 | NetError | 网络错误 |
| 100010 | MediaNetError | 媒体网络错误 |
| 100011 | NotFound | 未找到 |
| 101000 | SDKFail | SDK 失败 |
| 101001 | DeviceFail | 设备失败 |
| 101002 | DeviceNoFind | 设备未找到 |
| 101003 | UserNotFound | 用户未找到 |
| 101004 | NotDevPrivate | 无设备权限 |
| 101005 | InvalidOperation | 无效操作 |
| 101006 | NotSupport | 不支持 |
| 101007 | DealBeQuick | 操作过快 |
| 101008 | MoudelNotSupport | 模式不支持 |
| 101009 | BeforeSetting | 需要先设置 |
| 101100 | ChannelJoinError | 频道加入错误 |
| 101101 | ChannelJoinTimeOut | 频道加入超时 |
| 101200 | StreamJoinError | 流加入错误 |
| 101201 | StreamJoinConflict | 流加入冲突 |
| 101202 | VideoCapturerError | 视频采集器错误 |
| 101203 | NotFindStreamTrack | 未找到流轨道 |
| 101204 | ExceedingSpecifiedQuantity | 超出指定数量 |
| 201000 | SDKMeetingFail | SDK 会议失败 |
| 201001 | MeetingStatusReject | 会议状态拒绝 |
| 201002 | MeetingHostFail | 主持人失败 |

### DisconnectReason

| 值 | 名称 | 说明 |
| --- | --- | --- |
| -1 | Error | 错误 |
| 1 | Self | 主动离开 |
| 2 | Kicked | 被踢出 |
| 3 | Replace | 被替换 |
| 4 | Timeout | 超时离开 |
| 5 | Destroy | 被销毁 |

### ChatMsgType

| 值 | 名称 | 说明 |
| --- | --- | --- |
| 1 | Text | 文本 |
| 2 | File | 文件 |
| 3 | Pic | 图片 |
| 4 | Sound | 声音 |

### HandupType

| 值 | 名称 | 说明 |
| --- | --- | --- |
| 1 | Mic | 举手麦克风 |
| 2 | Camera | 举手摄像头 |
| 3 | Chat | 举手聊天 |

### UserHandupStep

| 值 | 名称 | 说明 |
| --- | --- | --- |
| 1 | Request | 请求 |
| 2 | Cancel | 取消 |
| 3 | ConfirmOpen | 确认打开 |
| 4 | RejectOpen | 拒绝打开 |

### CameraState

| 值 | 名称 | 说明 |
| --- | --- | --- |
| 1 | On | 开启 |
| 2 | Off | 关闭 |

### MicState

| 值 | 名称 | 说明 |
| --- | --- | --- |
| 1 | On | 开启 |
| 2 | Off | 关闭 |

### ShareType

| 值 | 名称 | 说明 |
| --- | --- | --- |
| 0 | Normal | 普通 |
| 1 | Screen | 屏幕 |
| 2 | WhiteBoard | 白板 |

### Role

| 值 | 名称 | 说明 |
| --- | --- | --- |
| 0 | Member | 普通成员 |
| 1 | Host | 主持人 |
| 2 | CoHost | 联合主持人 |

### DeviceType

| 值 | 名称 | 说明 |
| --- | --- | --- |
| 1 | Mic | 麦克风 |
| 2 | Speaker | 扬声器 |
| 3 | Camera | 摄像头 |

### DeviceStatus

| 值 | 名称 | 说明 |
| --- | --- | --- |
| 2 | NoFail | 正常 |
| 1 | Fail | 异常 |

### StreamNetLevel

| 值 | 名称 | 说明 |
| --- | --- | --- |
| 0 | Good | 好 |
| -1 | NotGood | 一般 |
| -2 | Terrible | 差 |
| -3 | Catastrophic | 灾难性 |

---

## 数据结构

### SMeetingCreateMeetingModel

会议室创建模型：

| 字段 | 类型 | 说明 | 默认值 |
| --- | --- | --- | --- |
| room_no | std::string | 房间号 | - |
| title | std::string | 会议标题 | - |
| content | std::string | 会议内容 | - |
| password | std::string | 密码 | - |
| meeting_type | int | 会议类型 (1:临时 2:预约) | 1 |
| meeting_mode | int | 会议模式 (1:普通 2:合成 3:培训 4:培训 5:小组) | 1 |
| plan_time | long long | 计划时间 (Unix 时间戳) | 0 |
| plan_dur | int | 计划时长 | 0 |
| conferee | `std::vector<std::string>` | 与会者列表 | - |
| co_host | `std::vector<std::string>` | 联合主持人列表 | - |
| maximum | int | 最大人数 | 0 |
| end_type | int | 结束类型 (0:延长 1:强制结束) | 1 |
| entry_mute_policy | int | 入场静音策略 (1:强制 2:关闭 3:超 6 人静音) | 3 |
| watermark_disabled | bool | 是否禁用水印 | true |
| screenshot_disabled | bool | 是否禁用截屏 | false |
| chat_disabled | bool | 是否禁用聊天 | false |
| auto_record | bool | 是否自动录制 | true |
| attend_type | int | 参会类型 (1:允许 3:禁止) | 1 |
| waiting_room_disabled | bool | 是否禁用等候室 | true |
| enter_before_host_disabled | bool | 是否禁止主持人前进入 | false |
| parent | std::string | 父会议 ID | - |
| extend_info | std::string | 扩展信息 | - |

### SMeetingMeetingAttachments

会议附件：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| name | std::string | 名称 |
| key | std::string | 键 |

### SMeetingResourcesModel

资源模型：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| meeting_id | std::string | 会议 ID |
| parent_id | std::string | 父资源 ID |
| res_type | std::string | 资源类型 |
| res_key | std::string | 资源键 |
| res_name | std::string | 资源名称 |

### CustomPublishTrack

自定义发布轨道：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| desc | std::string | 描述 |
| width | int | 宽度 |
| height | int | 高度 |
| fps | int | 帧率 |
| bitrate | int | 比特率 |
| encode | int | 编码 |
