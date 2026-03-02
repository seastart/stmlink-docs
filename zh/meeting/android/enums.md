### ChatMsgType
聊天消息类型

| 枚举名 | 值 | 说明 |
| --- | --- | --- |
| unknow | 0 | 未知 |
| Text | 1 | 文本消息 |
| File | 2 | 文件消息 |
| Picture | 3 | 图片消息 |
| Voice | 4 | 语音消息 |
| Custom | 5 | 自定义消息 |


### ShareType
共享类型

| 枚举名 | 值 | 说明 |
| --- | --- | --- |
| Normal | 0 | 正常状态无共享 |
| ScreenShare | 1 | 屏幕共享 |
| WhiteBoardShare | 2 | 白板共享 |


### HandupType
举手申请类型

| 枚举名 | 值 | 说明 |
| --- | --- | --- |
| UnKnown | 0 | 未知 |
| OpenMic | 1 | 申请开音频 |
| OpenCamera | 2 | 申请开视频 |
| Chat | 3 | 申请聊天 |


### LeaveReason
| 枚举名 | 值 | 说明 |
| --- | --- | --- |
| UnKnown | 0 | 未知 |
| OpenMic | 1 | 申请开音频 |
| OpenCamera | 2 | 申请开视频 |
| Chat | 3 | 申请聊天 |


### LeaveMeetingReason
离开会议的原因

| 枚举名 | 值 | 说明 |
| --- | --- | --- |
| UnKnown | 0 | 未知 |
| KickOut | 2 | 被踢出 |
| BeReplaced | 3 | 被顶号 |
| HeartbeatTimeout | 4 | 心跳超时 |
| ChannelDestroy | 5 | 频道销毁 |


### DeviceState
设备状态

| 枚举名 | 值 | 说明 |
| --- | --- | --- |
| Open | 1 | 未知 |
| Closed | 2 | 被踢出 |


### ChangeReason
状态变化原因

| 枚举名 | 值 | 说明 |
| --- | --- | --- |
| ChangeReasonBySelf | 0 | 自己操作 |
| ChangeReasonByAdmin | 1 | 主持人或联席主持人操作 |


### HandupType
举手申请类型

| 枚举名 | 值 | 说明 |
| --- | --- | --- |
| UnKnown | 0 | 未知 |
| OpenMic | 1 | 申请开音频 |
| OpenCamera | 2 | 申请开视频 |
| Chat | 3 | 申请聊天 |


### DeviceType
设备枚举类型

| 枚举名 | 值 |
| --- | --- |
| unknow | 0 |
| Windows | 1 |
| Android | 2 |
| iOS | 3 |
| Linux | 4 |
| MacOS | 5 |
| WebRTC | 6 |
| Rtmp | 7 |


### MemberRoleType
成员角色类型

| 枚举名 | 值 | 说明 |
| --- | --- | --- |
| Normal | 0 | 普通成员 |
| Host | 1 | 主持人 |
| UnionHost | 2 | 联席主持人 |


### UserType
成员类型

| 枚举名 | 值 | 说明 |
| --- | --- | --- |
| Normal | 1 | 普通成员 |
| SIP | 2 | SIP 设备 |
| H323 | 3 | H323 设备 |


### MeetingType
会议类型

| 枚举名 | 值 | 说明 |
| --- | --- | --- |
| Initiate | 1 | 即时会议 |
| Schedule | 2 | 预约会议 |


### MeetingMode
会议模式

| 枚举名 | 值 | 说明 |
| --- | --- | --- |
| Normal | 1 | 普通会议模式 |
| Mixture | 2 | 合成会议模式 |


### MuteState
入会静音状态

| 枚举名 | 值 | 说明 |
| --- | --- | --- |
| MuteState1 | 1 | 开启入会静音(所有人入会默认静音) |
| MuteState2 | 2 | 关闭入会静音(跟随客户端初始音频状态) |
| MuteState3 | 3 | 超6人静音(超过6人后入会静音) |


### AgentType
| 枚举名 | 值 | 说明 |
| --- | --- | --- |
| SIP | 2 |  |
| H323 | 3 |  |
| GB28181 | 4 |  |
| RTSP | 5 |  |
| RTMP | 6 |  |
| FILE | 7 |  |
| TENCENT | 8 |  |
| AI | 9 |  |


### AgentStatus
| 枚举名 | 值 | 说明 |
| --- | --- | --- |
| Unknown | 0 | 未知理由 |
| Online | 1 | 在线 |
| Offline | 2 | 离线 |


### DisconnectedImReason
| 枚举名 | 值 | 说明 |
| --- | --- | --- |
| Unknown | 0 | 未知理由 |
| KickOut | 2 | 被踢出 |
| BeReplaced | 3 | 被顶号 |
| HeartbeatTimeout | 4 | 心跳超时 |




