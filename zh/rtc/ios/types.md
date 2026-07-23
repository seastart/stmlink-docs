---
title: "类型定义"
description: "iOS SRTC 音视频 SDK 完整类型与结构体定义"
---

### RTCEngineConfig
初始化RTC配置参数

| **属性** | **必填** | **属性说明** |
| --- | :---: | --- |
| NSString *logPath | 否 | 日志文件路径 |
| BOOL enableLocalLog | 否 | 是否启用本地日志，默认 NO |


### RTCEngineUserModel
用户信息

| **属性** | **必填** | **属性说明** |
| --- | :---: | --- |
| NSString *appId | 是 | 应用标识 |
| NSString *userId | 是 | 用户标识 |
| NSString *sessionId | 是 | 会话标识 |
| NSString *name | 是 | 用户名称 |
| [RTCDeviceType](#YJ8zG) deviceType | 是 | 设备类型，默认 `RTCDeviceTypeIOS` |
| NSString *deviceId | 是 | 设备标识 |
| NSString *version | 是 | 组件版本号 |
| NSString *netid | 是 | 网络标识 |
| NSString *sgid | 是 | 分组标识 |
| NSString *channel | 是 | 频道名称 |
| int linkId | 是 | 连接标识(流媒体) |
| NSString *sessionKey | 是 | 会话令牌(流媒体) |
| NSString *uploadId | 是 | 流媒体服务标识 |
| BOOL isAudience | 是 | 是否为观众 |
| NSInteger joinAt | 否 | 加入时间 |
| NSInteger updatedAt | 否 | 更新时间 |
| NSInteger leaveAt | 否 | 离开时间 |
| NSMutableArray &lt;[RTCEngineStreamTrackModel](#o95yb) \*&gt; \*streamTracks | 否 | 码流轨道列表 |
| id props | 否 | 自定义属性 |


### RTCEngineStreamTrackModel
码流轨道信息

| **属性** | **必填** | **属性说明** |
| --- | :---: | --- |
| NSString *streamId | 是 | 码流标识 |
| NSString *desc | 是 | 码流描述 |
| [RTCStreamTrackKind](#Ysug3) kind | 是 | 码流种类 |
| [RTCCodecType](#bolP1) codecType | 是 | 编码类型 |
| int width | 是 | 分辨率宽 |
| int height | 是 | 分辨率高 |
| int fps | 是 | 视频帧率 |
| int bitrate | 是 | 视频码率，单位kbps |
| int angle | 是 | 视频角度 |
| int sampleRate | 否 | 音频采样率 |
| [RTCTrackIdentifierFlags](#QmrJ5) track | 是 | 轨道号码 |
| NSArray<NSString *> *fallbackIds | 否 | 当前层可降级到的更低层轨道列表，仅用于支持 seastart 的引擎 |
| BOOL variant | 否 | 是否为 simulcast 副层，仅用于支持 seastart 的引擎 |
| id props | 否 | 自定义属性 |


### RTCEngineChannelModel
频道信息

| **属性** | **必填** | **属性说明** |
| --- | :---: | --- |
| NSString *appId | 是 | 应用标识 |
| NSString *channel | 是 | 频道名称 |
| int linkId | 是 | 连接标识(流媒体) |
| int maxUser | 是 | 频道最大用户数 |
| int maxAudio | 是 | 频道音频最大转发数 |
| int maxPeer | 是 | 频道用户最大可转发数 |
| int maxVideo | 是 | 频道用户视频最大可转发数 |
| NSInteger createdAt | 否 | 创建时间 |
| NSInteger updatedAt | 否 | 更新时间 |
| id props | 否 | 自定义属性 |


### RTCEngineMediaConfig
流媒体配置参数

| **属性** | **必填** | **属性说明** |
| --- | :---: | --- |
| int aec | 否 | 回声消除AEC，默认12 |
| int agc | 否 | 自动增益控制AGC，默认16000 |
| int audioSampe | 否 | 音频采样率，默认48000 |
| [RTCCodecType](#bolP1) audioEncode | 否 | 音频编码格式，默认AAC |
| [RTCAudioRoute](#fcHdd) audioRoute | 否 | 无外设时的默认内置音频路由，支持扬声器或听筒，默认RTCAudioRouteSpeaker |
| int videoWidth | 否 | 分辨率宽，默认480 |
| int videoHeight | 否 | 分辨率高，默认640 |
| BOOL videoMirror | 否 | 视频镜像，默认YES |
| int fps | 否 | 视频帧率，默认25 |
| int bitrate | 否 | 视频码率，默认0.9*1024，单位kbps |


### RTCEngineNetworkQosParam
网络质量控制参数

| **属性** | **必填** | **属性说明** |
| --- | :---: | --- |
| int secondGear | 否 | 接收自适应延迟二档位，默认 500 |
| int thirdGear | 否 | 接收自适应延迟三档位，默认 1200 |
| float onAudioCycle | 否 | 获取云端音频数据信息周期，默认为500毫秒 |
| BOOL isHardwarede | 否 | 开启硬件解码 YES开启 NO关闭，默认 YES |
| BOOL isNetworkAdaptive | 否 | 开启网络自适应延迟 YES开启 NO关闭，默认 YES |
| BOOL isBitrateAdaptive | 否 | 开启码率自适应 YES开启 NO关闭，默认 YES |
| [RTCNetworkQosShakeLevel](#CVdPk) shakeLevel | 否 | 网络延时抗抖动等级，默认 RTCNetworkQosShakeLevelMedium |


### RTCEngineDebugParam
调试模式参数

| **属性** | **必填** | **属性说明** |
| :--- | :---: | --- |
| NSString *debugHost | 否 | 远程调试地址 |
| BOOL enableSaveVideo | 否 | 保存视频流，默认 NO |
| BOOL enableSaveAudioCapture | 否 | 保存采集音频流，默认 NO |
| BOOL enableSaveAudioReceive | 否 | 保存远程音频流，默认 NO |


### RTCSpeedTestParams
测速参数

| **属性** | **必填** | **属性说明** |
| --- | :---: | --- |
| int linkId | 是 | 连接标识(流媒体) |
| NSString *streamHost | 是 | 流媒体服务地址 |
| int streamPort | 是 | 流媒体服务端口 |
| int expectedUpBandwidth | 否 | 预期的上行带宽，默认 2000kbps，设置为0时不对上行做检测 |
| int expectedDownBandwidth | 否 | 预期的下行带宽，默认 2000kbps，设置为0时不对下行做检测 |
| int duration | 否 | 测试时长，默认 30s |


### RTCSpeedTestResult
测速结果

| **属性** | **必填** | **属性说明** |
| --- | :---: | --- |
| NSInteger recv | 否 | 接收/发送总包数 |
| NSInteger miss | 否 | 错序数 |
| NSInteger losf | 否 | 丢包数 |
| NSInteger speed | 否 | 速率/码率(kbps) |
| NSInteger delay | 否 | 网络延迟 |
| float dropRate | 否 | 丢包率 |
| [RTCNetworkState](#FhNet) state | 否 | 网络状况 |


### RTCSpeedTestConnectResult
测速连接状态结果

| **属性** | **必填** | **属性说明** |
| :--- | :---: | --- |
| NSInteger delay | 否 | 网络回环延迟 |
| BOOL internetConnect | 否 | 互联网连接情况，YES-正常 NO-异常 |
| BOOL streamConnect | 否 | 流媒体连接情况，YES-正常 NO-异常 |
| BOOL signalingConnect | 否 | 会控服务连接情况，YES-正常 NO-异常 |


### RTCStreamAudioModel
成员音频信息

| **属性** | **必填** | **属性说明** |
| --- | :---: | --- |
| NSString *userId | 是 | 用户标识 |
| int linkId | 是 | 连接标识(流媒体) |
| NSInteger power | 否 | 音频功率 |
| NSInteger db | 否 | 音频分贝值 |


### RTCStreamSendModel
流媒体发送状态信息

| **属性** | **必填** | **属性说明** |
| --- | :---: | --- |
| int buffer | 否 | 上传缓冲包数 |
| int delay | 否 | 上传延迟 |
| int overflow | 否 | 溢出缓冲包数 |
| NSString *speed | 否 | 上传速率(单位kps) |
| NSInteger status | 否 | 上传状态 |
| float loss_r | 否 | 补偿前丢包率 |
| float loss_c | 否 | 补偿后丢包率 |


### RTCStreamReceiveModel
流媒体接收状态信息

| **属性** | **必填** | **属性说明** |
| --- | :---: | --- |
| NSString *userId | 是 | 用户标识 |
| int linkId | 是 | 连接标识(流媒体) |
| int recv | 否 | 接收包数 |
| int comp | 否 | 补偿包数 |
| int losf | 否 | 总丢包数 |
| float lrl | 否 | 端到端丢包率 |
| float lrd | 否 | 服务器到端丢包率 |
| int audio | 否 | 音频包数 |
| int video | 否 | 视频包数 |


### RTCStreamQualitySampleModel
流媒体质量采样数据，仅用于支持 seastart 的引擎 

| **属性** | **必填** | **属性说明** |
| --- | :---: | --- |
| NSInteger score | 是 | 综合评分（0~100） |
| RTCStreamQualityLevel level | 是 | 质量等级 |
| double mos | 是 | 语音 MOS 值 |
| double loss | 是 | 丢包率（0~1） |
| double rtt | 是 | 往返时延（毫秒） |
| double jitter | 是 | 抖动（毫秒） |
| NSInteger packets | 是 | 包数量 |
| NSInteger bitrate | 是 | 比特率（bps） |
| NSInteger bytes | 是 | 字节数 |


### RTCEngineLogLevel
日志等级

| **枚举名** | **枚举值** | **说明** |
| --- | :---: | --- |
| RTCEngineLogLevelTrace | `0` | 所有日志 |
| RTCEngineLogLevelDebug | `1` | DEBUG、INFO、WARN、ERROR、CRITICAL 等级日志 |
| RTCEngineLogLevelInfo | `2` | INFO、WARN、ERROR、CRITICAL 等级日志 |
| RTCEngineLogLevelWarn | `3` | WARN、ERROR、CRITICAL 等级日志 |
| RTCEngineLogLevelError | `4` | ERROR、CRITICAL 等级日志 |
| RTCEngineLogLevelCritical | `5` | CRITICAL 等级日志 |
| RTCEngineLogLevelOff | `6` | 不记录任何日志 |


### RTCDeviceType
设备类型

| **枚举名** | **枚举值** | **说明** |
| --- | :---: | --- |
| RTCTerminalTypeUnknown | `0` | 未知终端 |
| RTCDeviceTypeWindows | `1` | Windows |
| RTCDeviceTypeAndroid | `2` | Android |
| RTCDeviceTypeIOS | `3` | iOS |
| RTCDeviceTypeLinux | `4` | Linux |
| RTCDeviceTypeMacOS | `5` | MacOS |
| RTCDeviceTypeWebRTC | `6` | WebRTC |
| RTCDeviceTypeRtmp | `7` | RTMP |


### RTCUserRole
成员角色

| **枚举名** | **枚举值** | **说明** |
| --- | :---: | --- |
| RTCUserRoleDefault | `0` | 普通成员 |
| RTCUserRoleAudience | `1` | 听众 |


### RTCMediaType
媒体类型

| **枚举名** | **枚举值** | **说明** |
| --- | :---: | --- |
| RTCMediaTypeData | `0` | 数据类型 |
| RTCMediaTypeVideo | `1` | 视频类型 |
| RTCMediaTypeAudio | `2` | 音频类型 |


### RTCCodecType
编码类型

| **枚举名** | **枚举值** | **说明** |
| --- | :---: | --- |
| RTCCodecTypeH264 | `0` | 未知类型 |
| RTCCodecTypeH264 | `0x1b` | H264 |
| RTCCodecTypeH265 | `0x24` | H265 |
| RTCCodecTypeAAC | `0x0f` | AAC |
| RTCCodecTypeOPUS | `0x5355504f` | OPUS |


### RTCChangeType
变更操作类型

| **枚举名** | **枚举值** | **说明** |
| --- | :---: | --- |
| RTCChangeTypeNone | `0` | 无操作 |
| RTCChangeTypeUpdate | `1` | 更新 |
| RTCChangeTypeAppend | `2` | 新增 |
| RTCChangeTypeRemove | `3` | 移除 |


### RTCLeaveReason
离开频道原因

| **枚举名** | **枚举值** | **说明** |
| --- | :---: | --- |
| RTCLeaveReasonError | `-1` | 发生错误 |
| RTCLeaveReasonNormal | `1` | 主动离开 |
| RTCLeaveReasonKickout | `2` | 被踢离开 |
| RTCLeaveReasonReplaced | `3` | 被顶号 |
| RTCLeaveReasonTimeout | `4` | 心跳超时离开 |
| RTCLeaveReasonDestroy | `5` | 频道销毁离开 |
| RTCLeaveReasonAudience | `6` | 身份变成观众 |


### RTCImDisconnectReason
即时通讯断开原因

| **枚举名** | **枚举值** | **说明** |
| --- | :---: | --- |
| RTCImDisconnectReasonError | `-1` | 发生错误 |
| RTCImDisconnectReasonNormal | `1` | 主动离开 |
| RTCImDisconnectReasonKickout | `2` | 被踢离开 |
| RTCImDisconnectReasonTimeout | `4` | 心跳超时离开 |


### RTCTrackIdentifierFlags
码流轨道标识

| **枚举名** | **枚举值** | **说明** |
| --- | :---: | --- |
| RTCTrackIdentifierFlags0 | `0` | 轨道0 |
| RTCTrackIdentifierFlags1 | `1` | 轨道1 |
| RTCTrackIdentifierFlags2 | `2` | 轨道2 |
| RTCTrackIdentifierFlags3 | `3` | 轨道3 |
| RTCTrackIdentifierFlags4 | `4` | 轨道4 |
| RTCTrackIdentifierFlags5 | `5` | 轨道5 |
| RTCTrackIdentifierFlags6 | `6` | 轨道6 |


### RTCNetworkState
网络状况

| **枚举名** | **枚举值** | **说明** |
| --- | :---: | --- |
| RTCNetworkStateNormal | `0` | 良好 |
| RTCNetworkStatePoor | `1` | 不佳 |
| RTCNetworkStateBad | `2` | 较差 |
| RTCNetworkStateVeryBad | `3` | 极差 |


### RTCScreenRecordStatus
屏幕共享状态

| **枚举名** | **枚举值** | **说明** |
| --- | :---: | --- |
| RTCScreenRecordStatusError | `-1` | 共享连接错误 |
| RTCScreenRecordStatusStop | `0` | 共享已经停止 |
| RTCScreenRecordStatusStart | `1` | 共享已经开始 |


### RTCAudioRoute
音频路由类型

| **枚举名** | **枚举值** | **说明** |
| --- | :---: | --- |
| RTCAudioRouteUnknown | `0` | 无效路由 |
| RTCAudioRouteSpeaker | `1` | 扬声器 |
| RTCAudioRouteReceiver | `2` | 听筒 |
| RTCAudioRouteBluetooth | `3` | 蓝牙耳机 |
| RTCAudioRouteHeadset | `4` | 有线耳机 |

### RTCEngineCameraDirection
摄像头方向

| **枚举名** | **枚举值** | **说明** |
| --- | :---: | --- |
| RTCEngineCameraDirectionFront | `1` | 前置摄像头 |
| RTCEngineCameraDirectionBack | `2` | 后置摄像头 |


### RTCNetworkQosShakeLevel
网络延时抗抖动等级

| **常量** | **枚举值** | **说明** |
| --- | :---: | --- |
| RTCNetworkQosShakeLevelUltraShort | `0` | 超短(0) 单向延迟120ms左右 这种模式下没有丢包补偿机制 并且编码关闭了B帧 一般不建议实际使用 |
| RTCNetworkQosShakeLevelShort | `1` | 短(1) 单向延迟200ms左右 单次丢包补偿 B帧为1 双向对讲环境下可以使用 |
| RTCNetworkQosShakeLevelMedium | `2` | 中(2) 单向延迟350ms左右 两次丢包补偿 B帧为1 双向对讲环境下推荐使用 |
| RTCNetworkQosShakeLevelLong | `3` | 长(3) 单向延迟600ms左右 三次丢包补偿 B帧为3 这种模式仅用于单向收看 双向对讲环境下不建议使用 该参数无法动态设置 |


### RTCUploadBitrateAdaptiveState
上行码率自适应状态

| **枚举名** | **枚举值** | **说明** |
| --- | :---: | --- |
| RTCUploadBitrateAdaptiveStateStart | `1000` | 码率自适应开始工作 |
| RTCUploadBitrateAdaptiveStateNormal | `0` | 码率恢复到最初设置 |
| RTCUploadBitrateAdaptiveStateHalf | `-1` | 码率变为原来的一半 |
| RTCUploadBitrateAdaptiveStateQuarter | `-2` | 码率变为原来的四分之一 |
| RTCUploadBitrateAdaptiveStateVeryBad | `-3` | 当前网络环境极差 |


### RTCDownBitrateAdaptiveState
下行码率自适应状态

| **枚举名** | **枚举值** | **说明** |
| --- | :---: | --- |
| RTCDownBitrateAdaptiveStateNormal | `0` | 正常 |
| RTCDownBitrateAdaptiveStatePoor | `-1` | 较差 |
| RTCDownBitrateAdaptiveStateBad | `-2` | 很差 |
| RTCDownBitrateAdaptiveStateVeryBad | `-3` | 极差 |
| RTCDownBitrateAdaptiveStateLose | `-4` | 链路离线 |


### RTCDownLossLevelState
下行平均丢包档位

| **枚举名** | **枚举值** | **说明** |
| --- | :---: | --- |
| RTCDownLossLevelStateInvalid | `-1` | 无效 |
| RTCDownLossLevelStateNormal | `0` | 正常 |
| RTCDownLossLevelStatePoor | `1` | 较差 |
| RTCDownLossLevelStateBad | `2` | 很差 |
| RTCDownLossLevelStateVeryBad | `3` | 极差 |


### RTCStreamTrackKind
码流轨道种类

| **枚举名** | **枚举值** | **说明** |
| --- | :---: | --- |
| RTCStreamTrackKindVideo | `video` | 视频类型 |
| RTCStreamTrackKindAudio | `audio` | 音频类型 |


### RTCLeaveChannelReason
离开频道原因

| **枚举名** | **枚举值** | **说明** |
| --- | :---: | --- |
| RTCLeaveChannelReasonNormal | `1` | 主动离开 |
| RTCLeaveChannelReasonKickout | `2` | 被踢离开 |
| RTCLeaveChannelReasonReplaced | `3` | 被顶号 |
| RTCLeaveChannelReasonTimeout | `4` | 心跳超时离开 |
| RTCLeaveChannelReasonDestroy | `5` | 频道销毁离开 |


### RTCStreamQualityLevel
流媒体质量等级

| **枚举名** | **枚举值** | **说明** |
| --- | :---: | --- |
| RTCStreamQualityLevelUnknown | `0` | 未知 |
| RTCStreamQualityLevelExcellent | `1` | 优秀（excellent） |
| RTCStreamQualityLevelGood | `2` | 良好（good） |
| RTCStreamQualityLevelPoor | `3` | 较差（poor） |
| RTCStreamQualityLevelLost | `4` | 已断流（lost） |


