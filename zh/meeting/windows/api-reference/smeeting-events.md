---
title: "事件回调"
description: "Windows SMeeting SDK 引擎级与会议级事件回调 C++ 接口参考"
---

回调分为**引擎级** `ISMeetingEngineEvent` 和**会议级** `ISMeetingChannelEvent`。

- 引擎级回调通过 `ISMeetingEngine::setEventHandler()` 绑定。
- 会议级回调通过 `ISMeetingChannel::setEventHandler()` 绑定，**必须在 `enter()` 之前设置**，否则入会过程中的事件会漏掉。

会议级回调不再带 `roomno` 首参；如果同一个 handler 服务多个 channel，可用 `channel->getChannelId()` 或 `channel->getRoom()` 区分。

---

## ISMeetingEngineEvent（引擎级）

### 设备事件

| 事件 | 参数 | 说明 |
| --- | --- | --- |
| onDeviceChange | DeviceType tp, bool isadd, std::string name | 设备插拔变化 |
| onDefDeviceChange | DeviceType tp, std::string name | 默认设备变化 |

### 网络探测事件

| 事件 | 参数 | 说明 |
| --- | --- | --- |
| onStreamProbeResult | int step, std::string result | 网络探测结果 |

### IM 事件

| 事件 | 参数 | 说明 |
| --- | --- | --- |
| onImEnabled | std::string uid, std::string sid | IM 已启用 |
| onImDisconnected | int reason, StatusCode code, std::string message | IM 断开 |
| onImReconnected | - | IM 重连成功 |
| onImReconnecting | - | IM 重连中 |
| onImCallMessage | std::string uid, std::string name, std::string content | 呼叫消息 |
| onMeetingStartMessage | std::string content | 会议开始消息 |

---

## ISMeetingChannelEvent（会议级）

### 连接状态事件

| 事件 | 参数 | 说明 |
| --- | --- | --- |
| onDisconnected | DisconnectReason, StatusCode, std::string | 断开连接 |
| onReconnected | - | 重连成功 |
| onReconnecting | - | 重连中 |

### 用户事件

| 事件 | 参数 | 说明 |
| --- | --- | --- |
| onUserEnter | std::string userdata | 用户进入 |
| onUserExit | std::string userdata, DisconnectReason reason | 用户离开 |
| onUserCameraStateChanged | std::string uid, CameraState newstate, bool by_admin, std::string op_uid | 用户摄像头状态变化 |
| onUserAudioStateChanged | std::string uid, MicState newstate, bool by_admin, std::string op_uid | 用户音频状态变化 |
| onUserNameChanged | std::string uid, std::string newname, bool by_admin, std::string op_uid | 用户名称变化 |
| onUserRoleChanged | std::string uid, Role newrole, bool by_admin, std::string op_uid | 用户角色变化 |
| onUserChatDisabledChanged | std::string uid, bool newstate, bool by_admin, std::string op_uid | 用户聊天权限变化 |
| onUserHandup | std::string uid, HandupType tp, UserHandupStep step | 用户举手 |

### 房间事件

| 事件 | 参数 | 说明 |
| --- | --- | --- |
| onRoomCameraStateChanged | std::string uid, bool self_unmute_camera_disabled, bool camera_disabled | 房间摄像头状态 |
| onRoomMicStateChanged | std::string uid, bool self_unmute_mic_disabled, bool mic_disabled | 房间麦克风状态 |
| onRoomChatDisabledChanged | std::string uid, bool newstatus | 房间聊天状态 |
| onRoomScreenshotDisabledChanged | std::string uid, bool newstatus | 房间截屏状态 |
| onRoomWaterMarkDisabledChanged | std::string uid, bool newstatus | 房间水印状态 |
| onRoomLockChanged | bool lock | 房间锁定状态 |
| onRoomShareStart | std::string uid, ShareType st | 共享开始 |
| onRoomShareStop | std::string uid, ShareType st, bool by_admin, std::string op_uid | 共享停止 |
| onRoomChatMessage | std::string uid, bool pri, ChatMsgType msg_type, std::string msg | 聊天消息 |
| onRoomCustomMessage | std::string uid, bool pri, std::string msg | 自定义消息 |
| onRoomMcuTaskChange | int task_type, int task_status | MCU 任务变化 |
| onRoomShareStateChange | bool share_state | 共享状态变化 |
| onRoomWaitRoomStateChange | bool new_st | 等候室状态变化 |

### 主持人控制事件

| 事件 | 参数 | 说明 |
| --- | --- | --- |
| onAdminRequestOpenMic | std::string uid | 请求打开麦克风 |
| onAdminRequestOpenCamera | std::string uid | 请求打开摄像头 |
| onAdminUpdateName | std::string uid, std::string name | 更新名称 |
| onAdminConfirmHandup | std::string uid, int code, bool approve | 确认举手 |
| onAdminMoveInWaitRoom | - | 移入等候室 |
| onAdminWaitRoomEnterRoomFinish | int code, std::string msg | 进入房间完成 |

### 设备事件

| 事件 | 参数 | 说明 |
| --- | --- | --- |
| onDeviceStatusChange | DeviceType tp, DeviceStatus status | 设备状态变化 |
| onShareTargetNotFind | - | 未找到共享目标 |

### 流媒体事件

| 事件 | 参数 | 说明 |
| --- | --- | --- |
| onStreamUpLevel | StreamNetLevel level | 上行网络质量 |
| onStreamDownLevel | std::string uid, StreamNetLevel level | 下行网络质量 |
| onStreamUpStat | std::string upstat | 上行统计 |
| onStreamDownStat | std::string downstat | 下行统计 |
| onStreamSpeakers | std::string Speakers | 发言者列表 |
| onFrameTimeOut | std::string uid, std::string track_id, std::string track_desc, int loading | 帧超时 |

### 签到事件

| 事件 | 参数 | 说明 |
| --- | --- | --- |
| onSigninActivity | std::string name, std::string desc, long long enddt | 签到活动 |
| onSigninFinish | std::string name | 签到完成 |
| onWaitRoomMemberEnter | std::string uid, std::string name | 等候室成员进入 |
| onWaitRoomMemberLeave | std::string uid, std::string name | 等候室成员离开 |

### 录制事件

| 事件 | 参数 | 说明 |
| --- | --- | --- |
| onRecordStatusChange | std::string k, int status, std::string msg | 录制状态变化 |

### 分组会议事件

| 事件 | 参数 | 说明 |
| --- | --- | --- |
| onAdminStartSubMeeting | std::string meeting_id, std::string title, std::string users | 启动分组会议 |
| onAdminStopSubMeeting | std::string parent_meeting_id | 停止分组会议 |
| onAdminMoveSubMeetingUser | std::string to_meeting_title, std::string to_meeting_id | 移动分组用户 |
| onUserHelpSubMeeting | std::string meeting_id, std::string title, std::string parent | 请求帮助 |
