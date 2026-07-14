---
title: "类型定义"
description: "iOS SMeeting 会议 SDK 完整类型与结构体定义"
---

## 结构体类型
### SEALogConfig
日志配置

| **属性名称** | **描述** |
| --- | --- |
| enableLocalLog | 【字段含义】是否启用全进程本地日志采集<br/>【推荐取值】默认值：YES；启用后日志同时写入本地文件并保留宿主 App 控制台输出。 |


### SEAMeetingParam
会议参数

该参数是创建房间与更新房间时的必传参数。

| **属性名称** | **描述** |
| --- | --- |
| roomId | 【字段含义】房间标识<br/>【推荐取值】云端生成<br/>【特别说明】创建房间时无需设置该字段，更新房间信息时，该字段为必传项。 |
| roomNo | 【字段含义】房间号码<br/>【推荐取值】云端生成<br/>【特别说明】创建和更新房间信息时无需设置改字段。 |
| title | 【字段含义】会议标题<br/>【推荐取值】创建房间时，该字段为必传项。<br/>【特别说明】可用于列表等会议显示标题使用，使用 UTF-8 编码。 |
| content | 【字段含义】会议说明<br/>【特别说明】可用于列表等会议显示说明使用，使用 UTF-8 编码。 |
| password | 【字段含义】会议密码<br/>【特别说明】创建房间时，如果设置了参会密码，用户加入会议时同样需要匹配密码才可以正确加入会议。 |
| meetingType | 【字段含义】会议类型<br/>【推荐取值】默认值：[SEAMeetingTypeInitiate](#WHxwQ) |
| beginTime | 【字段含义】会议开始时间<br/>【推荐取值】当会议类型为`预约会议`时，为必传项。<br/>【特别说明】开始时间 unix 时间戳 |
| endTime | 【字段含义】会议结束时间<br/>【推荐取值】当会议类型为`预约会议`时，为必传项。<br/>【特别说明】结束时间 unix 时间戳 |
| entryMutePolicy | 【字段含义】入会静音状态<br/>【推荐取值】默认值：[SEAMeetingMuteState3](#TRTMj) |
| watermarkDisabled | 【字段含义】房间水印禁用状态<br/>【推荐取值】默认值：YES |
| screenshotDisabled | 【字段含义】房间截屏禁用状态<br/>【推荐取值】默认值：NO |
| chatDisabled | 【字段含义】房间聊天禁用状态<br/>【推荐取值】默认值：NO |
| waitingRoomDisabled | 【字段含义】等候室是否禁用<br/>【推荐取值】默认值：YES |
| extendInfo | 【字段含义】扩展信息 |


### SEAMeetingEnterParam
加入会议参数

该参数是创建房间与更新房间时的必传参数。

| **属性名称** | **描述** |
| --- | --- |
| roomNo | 【字段含义】会议号码<br/>【推荐取值】一般为 9 位数字<br/>【特别说明】入会时，可以选择**会议号码**或**会议标识**任意一个进行加会操作。 |
| meetingId | 【字段含义】会议标识<br/>【推荐取值】一般为加密字符串<br/>【特别说明】入会时，可以选择**会议号码**或**会议标识**任意一个进行加会操作。 |
| password | 【字段含义】会议密码<br/>【特别说明】如果创建房间时设置了参会密码，加入会议时需要同样的匹配密码才可以正确加入会议。 |
| nickname | 【字段含义】参会昵称<br/>【推荐取值】该字段将作为会议中展示信息，使用 UTF-8 编码。 |
| avatar | 【字段含义】参会头像<br/>【推荐取值】该字段将作为会议中展示信息，使用 UTF-8 编码。 |
| extendInfo | 【字段含义】扩展信息 |
| isAudience | 【字段类型】BOOL<br/>【字段含义】是否以观众身份入会<br/>【推荐取值】默认值：NO；设置为 YES 时以观众身份入会。 |


### SEAUserModel
用户数据

| **属性名称** | **描述** |
| --- | --- |
| userId | 【字段含义】用户标识<br/>【特别说明】此字段为用户的全局唯一标识。 |
| name | 【字段含义】用户名称<br/>【特别说明】作为用户昵称使用，使用 UTF-8 编码。 |
| micState | 【字段含义】麦克风状态，请参见 [SEADeviceState](#kiwuX) 中的相关说明。 |
| cameraState | 【字段含义】摄像头状态，请参见 [SEADeviceState](#kiwuX) 中的相关说明。 |
| shareType | 【字段含义】共享状态，请参见 [SEAShareType](#Ww9uW) 中的相关说明。 |
| extend | 【字段含义】扩展属性<br/>【特别说明】用户的扩展数据属性，请参见 [SEAUserExtend](#o3005) 中的相关说明。 |


### SEAUserExtend
用户扩展数据

| **属性名称** | **描述** |
| --- | --- |
| role | 【字段含义】参会角色<br/>【特别说明】标识着用户的会中角色，请参见 [SEAUserRole](#QsCHa) 中的相关说明。 |
| avatar | 【字段含义】参会头像<br/>【特别说明】该参数由用户在加入房间接口中设置，使用 UTF-8 编码。 |
| isKickout | 【字段含义】是否被踢出 |
| chatDisabled | 【字段含义】聊天能力禁用状态，YES-禁用 NO-不禁用 |
| drawDisabled | 【字段含义】涂鸦能力禁用状态，YES-禁用 NO-不禁用 |
| extend | 【字段含义】扩展信息 |


### SEARoomModel
房间数据

| **属性名称** | **描述** |
| --- | --- |
| extend | 【字段含义】扩展属性<br/>【特别说明】房间的扩展数据属性，请参见 [SEARoomExtend](#DG1TX) 中的相关说明。 |


### SEARoomExtend
房间扩展数据

| **属性名称** | **描述** |
| --- | --- |
| meetingId | 【字段含义】会议标识 |
| roomNo | 【字段含义】房间号码 |
| title | 【字段含义】会议标题 |
| content | 【字段含义】会议说明 |
| meetingType | 【字段含义】会议类型<br/>【特别说明】标识会议类型，请参见 [SEAMeetingType](#WHxwQ) 中的相关说明。 |
| beginTime | 【字段含义】开始时间 |
| endTime | 【字段含义】结束时间 |
| entryMutePolicy | 【字段含义】入会静音状态<br/>【特别说明】当前会议参会静音状态，请参见 [SEAMeetingMuteState](#TRTMj) 中的相关说明。 |
| watermarkDisabled | 【字段含义】房间水印禁用状态，YES-禁用 NO-不禁用 |
| screenshotDisabled | 【字段含义】房间截屏禁用状态，YES-禁用 NO-不禁用 |
| chatDisabled | 【字段含义】聊天能力禁用状态，YES-禁用 NO-不禁用 |
| micDisabled | 【字段含义】麦克风禁用状态，YES-禁用 NO-不禁用 |
| cameraDisabled | 【字段含义】摄像头禁用状态，YES-禁用 NO-不禁用 |
| selfUnmuteMicDisabled | 【字段含义】是否禁止自我解除麦克风状态，YES-禁止 NO-不禁止 |
| selfUnmuteCameraDisabled | 【字段含义】是否禁止自我解除摄像头状态，YES-禁止 NO-不禁止 |
| shareDisabled | 【字段含义】共享能力禁用状态，YES-禁用 NO-不禁用 |
| waitingRoomDisabled | 【字段含义】等候室禁用状态，YES-禁用 NO-不禁用 |
| parentMid | 【字段含义】上级会议标识 |
| enterBeforeHostDisabled | 【字段含义】是否禁止在主持人之前入会，YES-禁止 NO-不禁止 |
| locked | 【字段含义】会议锁定状态，YES-开启 NO-关闭 |
| shareType | 【字段含义】共享类型<br/>【特别说明】标识当前会议共享类型，请参见 [SEAShareType](#Ww9uW) 中的相关说明。 |
| shareUid | 【字段含义】共享者标识<br/>【特别说明】标识当前会议正在共享者的用户标识 |
| creator | 【字段含义】创建者的用户标识 |
| hostUid | 【字段含义】主持人的用户标识 |
| unionHosts | 【字段含义】会议联席主持人用户标识列表 |
| signInActivityLists | 【字段含义】房间签到活动列表，详情参考：[SEASignInActivityModel]() |
| hasSignInActivity | 【字段含义】房间是否存在进行中的签到活动 |
| extend | 【字段含义】扩展信息 |


### SEAUserInfo
用户信息

| **属性名称** | **描述** |
| --- | --- |
| userId | 【字段含义】用户标识 |
| deviceId | 【字段含义】设备标识 |
| deviceType | 【字段含义】设备类型<br/>【特别说明】标识当前设备类型，请参见 [SEADeviceType](#xpfl9) 中的相关说明。 |
| expAt | 【字段含义】过期时间 |


### SEASectionModel
数据分页对象

| **属性名称** | **描述** |
| --- | --- |
| currentPage | 【字段含义】当前页码 |
| pageCount | 【字段含义】总页数 |
| perPage | 【字段含义】每页数据条数 |
| totalCount | 【字段含义】总数据条数 |


### SEAMeetingCreateModel
创建房间响应对象

| **属性名称** | **描述** |
| --- | --- |
| meetingId | 【字段含义】会议标识 |
| roomNo | 【字段含义】房间号码 |


### SEAChatModel
聊天消息对象

| **属性名称** | **描述** |
| --- | --- |
| messageId | 【字段含义】消息标识 |
| meetingId | 【字段含义】会议标识 |
| message | 【字段含义】消息内容 |
| messageType | 【字段含义】消息类型，详情参考：[SEAMessageType](#xlxGu) |
| senderId | 【字段含义】发送者标识 |
| senderName | 【字段含义】发送者昵称 |
| createdAt | 【字段含义】创建时间 |


### SEAChatListModel
聊天消息列表对象

| **属性名称** | **描述** |
| --- | --- |
| meta | 【字段含义】数据分页对象，详情参考：[SEASectionModel](#aObbp) |
| listData | 【字段含义】聊天消息对象列表，详情参考：[SEAChatModel](#dseM1) |


### SEAMeetingModel
会议信息对象，以下简单罗列部分属性，详情请参看 SDK 提供的头文件。

| **属性名称** | **描述** |
| --- | --- |
| meetingId | 【字段含义】会议标识 |
| roomNo | 【字段含义】会议号码 |
| title | 【字段含义】会议标题 |
| content | 【字段含义】会议说明 |
| conferee | 【字段含义】受邀成员标识列表 |
| creator | 【字段含义】创建者标识 |


### SEAMeetingListModel
会议列表对象

| **属性名称** | **描述** |
| --- | --- |
| meta | 【字段含义】数据分页对象，详情参考：[SEASectionModel](#aObbp) |
| listData | 【字段含义】会议信息对象列表，详情参考：[SEAMeetingModel](#NwAZR) |


### SEAMemberModel
参会成员对象

| **属性名称** | **描述** |
| --- | --- |
| recordId | 【字段含义】记录标识 |
| userId | 【字段含义】用户标识 |
| nickname | 【字段含义】用户昵称 |
| enterAt | 【字段含义】加入时间 |
| exitAt | 【字段含义】离开时间 |


### SEAMemberListModel
参会成员列表对象

| **属性名称** | **描述** |
| --- | --- |
| meta | 【字段含义】数据分页对象，详情参考：[SEASectionModel](#aObbp) |
| listData | 【字段含义】参会成员对象列表，详情参考：[SEAMemberModel](#LfPnO) |


### SEAStreamAudioModel
流媒体音频数据

| **属性名称** | **描述** |
| --- | --- |
| userId | 【字段含义】用户标识 |
| power | 【字段含义】音频功率 |
| db | 【字段含义】音频分贝值 |


### SEAStreamSendModel
流媒体发送状态数据

| **属性名称** | **描述** |
| --- | --- |
| buffer | 【字段含义】上传缓冲包数 |
| delay | 【字段含义】上传延迟 |
| overflow | 【字段含义】溢出缓冲包数 |
| speed | 【字段含义】上传速率<br/>【特别说明】单位为 kps |
| status | 【字段含义】上传状态 |
| loss_r | 【字段含义】补偿前丢包率 |
| loss_c | 【字段含义】补偿后丢包率 |


### SEAStreamReceiveModel
流媒体接收状态数据

| **属性名称** | **描述** |
| --- | --- |
| userId | 【字段含义】用户标识 |
| recv | 【字段含义】接收包数 |
| comp | 【字段含义】补偿包数 |
| losf | 【字段含义】总丢包数 |
| lrl | 【字段含义】端到端丢包率 |
| lrd | 【字段含义】服务器到端丢包率 |
| audio | 【字段含义】音频包数 |
| video | 【字段含义】视频包数 |


### SEAStreamQualityModel
流媒体质量监测数据

| **属性名称** | **描述** |
| --- | --- |
| score | 【字段含义】综合评分（0~100） |
| level | 【字段含义】质量等级 |
| mos | 【字段含义】语音 MOS 值 |
| loss | 【字段含义】丢包率（0~1） |
| rtt | 【字段含义】往返时延（毫秒） |
| jitter | 【字段含义】抖动（毫秒） |
| packets | 【字段含义】包数量 |
| bitrate | 【字段含义】比特率（bps） |
| bytes | 【字段含义】字节数 |


### SEAAgentModel
邀请设备对象

| **属性名称** | **描述** |
| --- | --- |
| deviceId | 【字段含义】设备ID |
| name | 【字段含义】设备名称 |
| type | 【字段含义】设备类型，请参见 [SEAAgentType](#rv0G4) 中的相关说明。 |
| status | 【字段含义】设备状态，请参见 [SEAAgentStatus](#rW3P0) 中的相关说明。 |
| contact | 【字段含义】设备标识 |
| remark | 【字段含义】设备备注 |
| connectParams | 【字段含义】连接参数 |


### SEAAgentListModel
邀请设备列表对象

| **属性名称** | **描述** |
| --- | --- |
| meta | 【字段含义】数据分页对象，详情参考：[SEASectionModel](#aObbp) |
| listData | 【字段含义】设备对象列表，详情参考：[SEAAgentModel](#YRsDA) |


### SEAInviteModel
邀请对象

| **属性名称** | **描述** |
| --- | --- |
| contact | 【字段含义】设备标识 |
| type | 【字段含义】设备类型，详情参考：[SEAAgentType](#rv0G4) |


### SEAConfereeModel
小组会议参会成员对象

| **属性名称** | **描述** |
| --- | --- |
| userId | 【字段含义】用户标识 |
| nickname | 【字段含义】用户昵称 |


### SEALayoutDataModel
布局数据对象

| **属性名称** | **描述** |
| --- | --- |
| layout | 【字段含义】布局类型，默认 auto |
| isPolling | 【字段含义】是否轮询，默认 NO |
| watermark | 【字段含义】布局水印，详情参考：[SEALayoutWatermarkModel](#ktKP5) |
| label | 【字段含义】布局标签，详情参考：[SEALayoutLabelModel](#PfK8y) |
| viewLists | 【字段含义】布局视图列表，即：逻辑块, 包含宫格与用户<br/>【特别说明】布局视图列表，请参见 [SEALayoutViewListModel](#Ww9uW) 中的相关说明。 |


### SEALayoutWatermarkModel
布局水印对象

| **属性名称** | **描述** |
| --- | --- |
| type | 【字段含义】水印类型，默认 1；1-无，2-单排，3-多排 |
| size | 【字段含义】字体大小，为0时，表示默认值 |
| color | 【字段含义】字体颜色，为空时，表示默认值 |
| olColor | 【字段含义】轮廓颜色，为空时，表示默认值 |
| olWidth | 【字段含义】轮廓线宽，为0时，表示默认值 |


### SEALayoutLabelModel
布局标签对象

| **属性名称** | **描述** |
| --- | --- |
| type | 【字段含义】标签类型，默认 LT；字母或组合：L-左，R-右，T-上，B-下 |
| size | 【字段含义】字体大小，为0时，表示默认值 |
| color | 【字段含义】字体颜色，为空时，表示默认值 |
| bgColor | 【字段含义】背景颜色，为空时，表示默认值 |


### SEALayoutViewListModel
布局视图列表对象，即：逻辑块, 包含宫格与用户

| **属性名称** | **描述** |
| --- | --- |
| itemLists | 【字段含义】视图列表单元格<br/>【特别说明】单元格列表，请参见 [SEALayoutViewListCellModel](#NpDKM) 中的相关说明。 |
| userIds | 【字段含义】成员标识列表 |


### SEALayoutViewListCellModel
布局视图列表单元格对象

| **属性名称** | **描述** |
| --- | --- |
| index | 【字段含义】格子序号<br/>【特别说明】排序规则按HTML中标签的顺序，默认 0 |
| bindShare | 【字段含义】是否优先绑定频道内的共享流，默认 NO |
| label | 【字段含义】单元格标签，详情参考：[SEALayoutLabelModel](#PfK8y) |


### SEACloudRecordParam
云录制参数

该参数是开启云录制时的必传参数。

| **属性名称** | **描述** |
| --- | --- |
| recordType | 【字段含义】录制类型<br/>【推荐取值】默认：[SEARecordTypeVideo](#QYWNw) |
| title | 【字段含义】录制文件标题 |
| layoutData | 【字段含义】录制布局<br/>【推荐取值】详情可参考：[SEALayoutDataModel](#SobrR) |


### SEACloudRecordDetailsModel
云录制详情对象

| **属性名称** | **描述** |
| --- | --- |
| taskId | 【字段含义】任务标识 |
| meetingId | 【字段含义】会议标识 |
| roomNo | 【字段含义】会议号码 |
| title | 【字段含义】录制文件标题 |
| opUid | 【字段含义】操作人标识 |
| opName | 【字段含义】操作人名称 |
| recordStatus | 【字段含义】云录制状态，详情参考：[SEARecordStatus](#XOsJa) |
| videoKey | 【字段含义】视频地址 |
| videoSize | 【字段含义】视频大小 |
| tags | 【字段含义】录制标签 |
| errorDesc | 【字段含义】错误描述 |
| createdAt | 【字段含义】创建时间 |
| updatedAt | 【字段含义】更新时间 |


### SEACloudRecordConfigModel
云录制配置对象

| **属性名称** | **描述** |
| --- | --- |
| layout | 【字段含义】布局类型 |
| watermarkType | 【字段含义】水印类型，1-无，2-单排，3-多排 |
| labelType | 【字段含义】标签类型，字母或组合：L-左，R-右，T-上，B-下 |
| createdAt | 【字段含义】创建时间 |
| updatedAt | 【字段含义】更新时间 |


### SEAMeetingRemindModel
会议即将开始提醒对象

| **属性名称** | **描述** |
| --- | --- |
| meetingId | 【字段含义】会议标识 |
| roomNo | 【字段含义】房间号码 |
| title | 【字段含义】会议标题 |
| creatorName | 【字段含义】创建者昵称 |
| planTime | 【字段含义】预约时间 |
| planDuration | 【字段含义】预约时长，单位：分钟 |


### SEAMediaConfig
流媒体配置参数

| **属性** | **必填** | **属性说明** |
| --- | :---: | --- |
| int aec | 否 | 回声消除AEC，默认 12 |
| int agc | 否 | 自动增益控制AGC，默认 16000 |
| int audioSampe | 否 | 音频采样率，默认 48000 |
| [SEACodecType](#bolP1) audioEncode | 否 | 音频编码格式，默认 AAC |
| [SEAAudioRoute](#HhTLs) audioRoute | 否 | 音频路由，默认 SEAAudioRouteReceiver |
| int videoWidth | 否 | 分辨率宽，默认 480 |
| int videoHeight | 否 | 分辨率高，默认 640 |
| BOOL videoMirror | 否 | 视频镜像，默认 YES |
| int fps | 否 | 视频帧率，默认 25 |
| int bitrate | 否 | 视频码率，默认 0.9*1024，单位kbps |


### SEANetworkQosParam
网络质量控制参数

| **属性** | **必填** | **属性说明** |
| --- | :---: | --- |
| int secondGear | 否 | 接收自适应延迟二档位，默认 500 |
| int thirdGear | 否 | 接收自适应延迟三档位，默认 1200 |
| float onAudioCycle | 否 | 获取云端音频数据信息周期，默认 500毫秒 |
| BOOL isHardwarede | 否 | 开启硬件解码 YES开启 NO关闭，默认 YES |
| BOOL isNetworkAdaptive | 否 | 开启网络自适应延迟 YES开启 NO关闭，默认 YES |
| BOOL isBitrateAdaptive | 否 | 开启码率自适应 YES开启 NO关闭，默认 YES |
| [SEANetworkQosShakeLevel](#CVdPk) shakeLevel | 否 | 网络延时抗抖动等级，默认 SEANetworkQosShakeLevelMedium |


### SEADebugParam
调试模式参数

| **属性** | **必填** | **属性说明** |
| :--- | :---: | --- |
| NSString *debugHost | 否 | 远程调试地址 |
| BOOL enableSaveVideo | 否 | 保存视频流，默认 NO |
| BOOL enableSaveAudioCapture | 否 | 保存采集音频流，默认 NO |
| BOOL enableSaveAudioReceive | 否 | 保存远程音频流，默认 NO |


### SEAWaitingRoomMemberModel
等候室成员对象

| **属性名称** | **描述** |
| --- | --- |
| userId | 【字段含义】用户标识 |
| nickname | 【字段含义】用户昵称 |
| enterAt | 【字段含义】加入时间 |


### SEAWaitingRoomMemberListModel
等候室成员列表对象

| **属性名称** | **描述** |
| --- | --- |
| listData | 【字段含义】等候室成员对象列表，详情参考：[SEAWaitingRoomMemberModel](#BomRa) |


### SEARoomSubMeetingModel
小组会议对象

| **属性名称** | **描述** |
| --- | --- |
| groupId | 【字段含义】小组标识 |
| meetingId | 【字段含义】小组会议标识 |
| parentMid | 【字段含义】主会议标识 |
| title | 【字段含义】小组会议名称 |
| meetingStatus | 【字段含义】小组会议状态，详情参考：[SEAMeetingStatus](#YzZHH) |
| conferee | 【字段含义】小组会议参会成员列表，详情参考：[SEAConfereeModel](#ipu1S) |


### SEARoomSubMeetingListModel
小组会议列表对象

| **属性名称** | **描述** |
| --- | --- |
| listData | 【字段含义】小组会议对象列表，详情参考：[SEARoomSubMeetingModel](#n9tEd) |


### SEAOnlineMemberModel
在线成员对象

| **属性名称** | **描述** |
| --- | --- |
| userId | 【字段含义】用户标识 |
| nickname | 【字段含义】用户昵称 |
| deviceType | 【字段含义】设备类型，详情参考：[SEADeviceType](#xpfl9) |
| joinAt | 【字段含义】加入时间 |


### SEAOnlineMemberListModel
在线成员列表对象

| **属性名称** | **描述** |
| --- | --- |
| meta | 【字段含义】数据分页对象，详情参考：[SEASectionModel](https://www.yuque.com/anyconf/smeeting/gkeau9oyh5vms80z#aObbp) |
| listData | 【字段含义】在线成员对象列表，详情参考：[SEAOnlineMemberModel](#DpBFV) |


### SEASignInActivityModel
签到活动项对象

| **属性名称** | **描述** |
| --- | --- |
| userId | 【字段含义】用户标识(创建者) |
| beginAt | 【字段含义】开始时间 |
| dur | 【字段含义】签到时长，单位：分钟，0为不限时 |
| endAt | 【字段含义】结束时间 |
| status | 【字段含义】活动状态，，详情参考：[SEASignInActivityState]() |
| desc | 【字段含义】签到描述 |
| nums | 【字段含义】签到人数 |


### SEASignInListModel
签到活动列表对象

| **属性名称** | **描述** |
| --- | --- |
| listData | 【字段含义】签到活动列表，详情参考：[SEASignInActivityModel](#DpBFV) |
| now | 【字段含义】当前服务器时间 |


### SEASignInCountModel
签到统计人数对象

| **属性名称** | **描述** |
| --- | --- |
| nums | 【字段含义】签到人数 |


### SEASignInDetailModel
签到详情项对象

| **属性名称** | **描述** |
| --- | --- |
| detailId | 【字段含义】记录标识 |
| userId | 【字段含义】用户标识 |
| nickname | 【字段含义】用户昵称 |
| role | 【字段含义】用户角色，请参见 [SEAUserRole](#QsCHa) 中的相关说明。 |
| epoch | 【字段含义】签到轮次 |
| createdAt | 【字段含义】签到时间 |


### SEASignInDetailListModel
签到活动详情列表对象

| **属性名称** | **描述** |
| --- | --- |
| listData | 【字段含义】签到详情列表，详情参考：[SEASignInDetailModel](#DpBFV) |


## 枚举类型
### SEADeviceType
设备类型

| **枚举类型** | **枚举值** | **描述** |
| --- | :---: | --- |
| SEADeviceTypeUnknown | `0` | 未知类型设备 |
| SEADeviceTypeWindows | `1` | Windows |
| SEADeviceTypeAndroid | `2` | Android |
| SEADeviceTypeIOS | `3` | iOS |
| SEADeviceTypeLinux | `4` | Linux |
| SEADeviceTypeMacOS | `5` | MacOS |
| SEADeviceTypeWebRTC | `6` | WebRTC |
| SEADeviceTypeWeChat | `7` | 微信小程序 |


### SEACodecType
编码类型

| **枚举名** | **枚举值** | **说明** |
| --- | :---: | --- |
| SEACodecTypeH264 | `0` | 未知类型 |
| SEACodecTypeH264 | `0x1b` | H264 |
| SEACodecTypeH265 | `0x24` | H265 |
| SEACodecTypeAAC | `0x0f` | AAC |
| SEACodecTypeOPUS | `0x5355504f` | OPUS |


### SEANetworkQosShakeLevel
网络延时抗抖动等级

| **常量** | **枚举值** | **说明** |
| --- | :---: | --- |
| SEANetworkQosShakeLevelUltraShort | `0` | 超短(0) 单向延迟120ms左右 这种模式下没有丢包补偿机制 并且编码关闭了B帧 一般不建议实际使用 |
| SEANetworkQosShakeLevelShort | `1` | 短(1) 单向延迟200ms左右 单次丢包补偿 B帧为1 双向对讲环境下可以使用 |
| SEANetworkQosShakeLevelMedium | `2` | 中(2) 单向延迟350ms左右 两次丢包补偿 B帧为1 双向对讲环境下推荐使用 |
| SEANetworkQosShakeLevelLong | `3` | 长(3) 单向延迟600ms左右 三次丢包补偿 B帧为3 这种模式仅用于单向收看 双向对讲环境下不建议使用 该参数无法动态设置 |


### SEAAudioRoute
音频路由类型

| **枚举类型** | **枚举值** | **描述** |
| --- | :---: | --- |
| SEAAudioRouteUnknown | `0` | 未知类型路由 |
| SEAAudioRouteSpeaker | `1` | 扬声器 |
| SEAAudioRouteReceiver | `2` | 听筒 |
| SEAAudioRouteBluetooth | `3` | 蓝牙耳机 |
| SEAAudioRouteHeadset | `4` | 有线耳机 |


### SEAVideoStreamType
视频流类型

| **枚举类型** | **枚举值** | **描述** |
| --- | :---: | --- |
| SEAVideoStreamTypeBig | `1` | 高清大画面，一般用来传输摄像头的视频数据 |
| SEAVideoStreamTypeSmall | `2` | 低清小画面，小画面和大画面的内容相同，但是分辨率和码率都比大画面低，因此清晰度也更低 |
| SEAVideoStreamTypeScreen | `3` | 屏幕共享流 |


### SEAScreenRecordStatus
屏幕采集状态

| **枚举类型** | **枚举值** | **描述** |
| --- | :---: | --- |
| SEAScreenRecordStatusNormal | `1000` | 默认状态 |
| SEAScreenRecordStatusError | `-1` | 连接错误 |
| SEAScreenRecordStatusStop | `0` | 录制停止 |
| SEAScreenRecordStatusStart | `1` | 录制开始 |


### SEAUserRole
用户角色

| **枚举类型** | **枚举值** | **描述** |
| --- | :---: | --- |
| SEAUserRoleNormal | `0` | 普通成员 |
| SEAUserRoleHost | `1` | 主持人 |
| SEAUserRoleUnionHost | `2` | 联席主持人 |


### SEAMeetingType
会议类型

| **枚举类型** | **枚举值** | **描述** |
| --- | :---: | --- |
| SEAMeetingTypeInitiate | `1` | 即时会议 |
| SEAMeetingTypeSchedule | `2` | 预约会议 |


### SEAMeetingMode
会议模式

| **枚举类型** | **枚举值** | **描述** |
| --- | :---: | --- |
| SEAMeetingModeNormal | `1` | 常规会议模式 |
| SEAMeetingModeMixture | `2` | 合成会议模式 |
| SEAMeetingModeVoice | `3` | 语音会议模式 |
| SEAMeetingModeTraining | `4` | 培训会议模式 |
| SEAMeetingModeGroups | `5` | 小组会议模式 |


### SEAMeetingStatus
会议状态

| **枚举类型** | **枚举值** | **描述** |
| --- | :---: | --- |
| SEAMeetingStatusNotStart | `1` | 未开始 |
| SEAMeetingStatusIng | `2` | 进行中 |
| SEAMeetingStatusEnded | `3` | 已结束 |


### SEAMeetingAttendType
参会类型

| **枚举类型** | **枚举值** | **描述** |
| --- | :---: | --- |
| SEAMeetingAttendTypeNormal | `1` | 无限制 |
| SEAMeetingAttendTypePassword | `2` | 密码参会 |
| SEAMeetingAttendTypeInitiate | `3` | 仅邀请人员参会 |


### SEAMeetingMuteState
会议静音状态

| **枚举类型** | **枚举值** | **描述** |
| --- | :---: | --- |
| SEAMeetingMuteState1 | `1` | 开启入会静音(所有人入会默认静音) |
| SEAMeetingMuteState2 | `2` | 关闭入会静音(跟随客户端初始音频状态) |
| SEAMeetingMuteState3 | `3` | 超6人静音(超过6人后入会静音) |


### SEADeviceState
设备状态

| **枚举类型** | **枚举值** | **描述** |
| --- | :---: | --- |
| SEADeviceStateOpen | `1` | 开启状态 |
| SEADeviceStateClosed | `2` | 关闭状态 |


### SEACameraDirection
摄像头方向

| **枚举类型** | **枚举值** | **描述** |
| --- | :---: | --- |
| SEACameraDirectionFront | `1` | 前置摄像头 |
| SEACameraDirectionBack | `2` | 后置摄像头 |


### SEAShareType
共享类型

| **枚举类型** | **枚举值** | **描述** |
| --- | :---: | --- |
| SEAShareTypeNormal | `0` | 默认类型 |
| SEAShareTypeScreen | `1` | 共享屏幕 |
| SEAShareTypeDrawing | `2` | 共享画板 |


### SEAMessageType
消息类型

| **枚举类型** | **枚举值** | **描述** |
| --- | :---: | --- |
| SEAMessageTypeText | `1` | 文本消息 |
| SEAMessageTypeFile | `2` | 文件消息 |
| SEAMessageTypePicture | `3` | 图片消息 |
| SEAMessageTypeVoice | `4` | 语音消息 |
| SEAMessageTypeCustom | `5` | 自定义消息 |


### SEAHandupType
举手申请类型

| **枚举类型** | **枚举值** | **描述** |
| --- | :---: | --- |
| SEAHandupTypeMic | `1` | 麦克风 |
| SEAHandupTypeCamera | `2` | 摄像头 |
| SEAHandupTypeChat | `3` | 聊天 |
| SEAHandupTypeShare | `4` | 共享 |
| SEAHandupTypeDraw | `5` | 涂鸦 |
| SEAHandupTypeOther | `6` | 其它 |


### SEALeaveReason
离开原因

| **枚举类型** | **枚举值** | **描述** |
| --- | :---: | --- |
| SEALeaveReasonNormal | `1` | 主动离开 |
| SEALeaveReasonKickout | `2` | 被踢离开 |
| SEALeaveReasonReplaced | `3` | 被顶号 |
| SEALeaveReasonTimeout | `4` | 心跳超时离开 |
| SEALeaveReasonDestroy | `5` | 频道销毁离开 |


### SEAChangeReason
音视频状态更改原因

| **枚举类型** | **枚举值** | **描述** |
| --- | :---: | --- |
| SEAChangeReasonBySelf | `0` | 自己操作 |
| SEAChangeReasonByAdmin | `1` | 主持人或联席主持人操作 |


### SEADownBitrateAdaptiveState
下行码率自适应状态

| **枚举类型** | **枚举值** | **描述** |
| --- | :---: | --- |
| SEADownBitrateAdaptiveStateNormal | `0` | 正常 |
| SEADownBitrateAdaptiveStatePoor | `-1` | 较差 |
| SEADownBitrateAdaptiveStateBad | `-2` | 很差 |
| SEADownBitrateAdaptiveStateVeryBad | `-3` | 极差 |
| SEADownBitrateAdaptiveStateLose | `-4` | 链路离线 |


### SEAUploadBitrateAdaptiveState
上行码率自适应状态

| **枚举类型** | **枚举值** | **描述** |
| --- | :---: | --- |
| SEAUploadBitrateAdaptiveStateStart | `1000` | 码率自适应开始工作 |
| SEAUploadBitrateAdaptiveStateNormal | `0` | 码率恢复到最初设置 |
| SEAUploadBitrateAdaptiveStateHalf | `-1` | 码率变为原来的一半 |
| SEAUploadBitrateAdaptiveStateQuarter | `-2` | 码率变为原来的四分之一 |
| SEAUploadBitrateAdaptiveStateVeryBad | `-3` | 当前网络环境极差 |


### SEADownLossLevelState
下行平均丢包档位

| **枚举类型** | **枚举值** | **描述** |
| --- | :---: | --- |
| SEADownLossLevelStateInvalid | `-1` | 无效 |
| SEADownLossLevelStateNormal | `0` | 正常 |
| SEADownLossLevelStatePoor | `1` | 较差 |
| SEADownLossLevelStateBad | `2` | 很差 |
| SEADownLossLevelStateVeryBad | `3` | 极差 |


### SEAImDisconnectReason
即时通讯断开原因

| **枚举类型** | **枚举值** | **描述** |
| --- | :---: | --- |
| SEAImDisconnectReasonError | `-1` | 发生错误 |
| SEAImDisconnectReasonNormal | `1` | 主动离开 |
| SEAImDisconnectReasonKickout | `2` | 被踢离开 |
| SEAImDisconnectReasonTimeout | `4` | 心跳超时离开 |


### SEAAgentType
邀请设备类型

| **枚举类型** | **枚举值** | **描述** |
| --- | :---: | --- |
| SEAAgentTypeSIP | `2` | SIP |
| SEAAgentTypeH323 | `3` | H323 |
| SEAAgentTypeGB28181 | `4` | GB28181 |
| SEAAgentTypeRTSP | `5` | RTSP拉流 |
| SEAAgentTypeRTMP | `6` | RTMP拉流 |
| SEAAgentTypeFile | `7` | 文件播放 |
| SEAAgentTypeTencent | `8` | 腾讯会议 |
| SEAAgentTypeAI | `9` | AI |


### SEAAgentStatus
邀请设备状态

| **枚举类型** | **枚举值** | **描述** |
| --- | :---: | --- |
| SEAAgentStatusUnknown | `0` | 未知 |
| SEAAgentStatusOnline | `1` | 在线 |
| SEAAgentStatusOffline | `2` | 离线 |


### SEARecordType
录制类型

| **枚举类型** | **枚举值** | **描述** |
| --- | :---: | --- |
| SEARecordTypeVideo | `1` | 录像模式 |
| SEARecordTypeMixture | `2` | 合流模式 |
| SEARecordTypeAll | `3` | 混合模式 |


### SEARecordStatus
录制状态

| **枚举类型** | **枚举值** | **描述** |
| --- | :---: | --- |
| SEARecordStatuUnknown | `-1` | 无任务 |
| SEARecordStatusNotStart | `0` | 未开始 |
| SEARecordStatusIng | `1` | 进行中 |
| SEARecordStatusNotEnded | `2` | 未结束 |
| SEARecordStatusError | `3` | 异常结束 |
| SEARecordStatusEnded | `4` | 正常结束 |


### SEACallRole
通话角色

| **枚举类型** | **枚举值** | **描述** |
| --- | :---: | --- |
| SEACallRoleNone | `0` | 未知类型 |
| SEACallRoleCall | `1` | 主叫(邀请方) |
| SEACallRoleCalled | `2` | 被叫(被邀请方) |


### SEACallStatus
通话状态

| **枚举类型** | **枚举值** | **描述** |
| --- | :---: | --- |
| SEACallStatusNone | `0` | 未知 |
| SEACallStatusAccept | `1` | 接听 |
| SEACallStatusReject | `2` | 拒绝 |
| SEACallStatusBusy | `3` | 忙线 |


### SEASignInActivityState
签到活动状态

| **枚举类型** | **枚举值** | **描述** |
| --- | :---: | --- |
| SEASignInActivityStateStarted | `1` | 进行中 |
| SEASignInActivityStateFinished | `2` | 已结束 |
