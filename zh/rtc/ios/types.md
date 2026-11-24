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
| [SRTCDeviceType](/zh/rtc/ios/types#srtcdevicetype) deviceType | 是 | 设备类型，默认 `SRTCDeviceTypeIOS` |
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
| NSMutableArray &lt;[RTCEngineStreamTrackModel](#rtcenginestreamtrackmodel) \*&gt; \*streamTracks | 否 | 码流轨道列表 |
| id props | 否 | 自定义属性 |


### RTCEngineStreamTrackModel
码流轨道信息

| **属性** | **必填** | **属性说明** |
| --- | :---: | --- |
| NSString *streamId | 是 | 码流标识 |
| NSString *desc | 是 | 码流描述 |
| [RTCStreamTrackKind](#rtcstreamtrackkind) kind | 是 | 码流种类 |
| [RTCCodecType](#rtccodectype) codecType | 是 | 编码类型 |
| int width | 是 | 分辨率宽 |
| int height | 是 | 分辨率高 |
| int fps | 是 | 视频帧率 |
| int bitrate | 是 | 视频码率，单位kbps |
| int angle | 是 | 视频角度 |
| int sampleRate | 否 | 音频采样率 |
| [RTCTrackIdentifierFlags](#rtctrackidentifierflags) track | 是 | 轨道号码 |
| `NSArray<NSString *> *fallbackIds` | 否 | 当前层可降级到的更低层轨道列表，仅用于支持 seastart 的引擎 |
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
| [RTCCodecType](#rtccodectype) audioEncode | 否 | 音频编码格式，默认AAC |
| [RTCAudioRoute](#rtcaudioroute) audioRoute | 否 | 无外设时的默认内置音频路由，支持扬声器或听筒，默认RTCAudioRouteSpeaker |
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
| [RTCNetworkQosShakeLevel](#rtcnetworkqosshakelevel) shakeLevel | 否 | 网络延时抗抖动等级，默认 RTCNetworkQosShakeLevelMedium |


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
| [RTCNetworkState](#rtcnetworkstate) state | 否 | 网络状况 |


### RTCSpeedTestConnectResult
测速连接状态结果

| **属性** | **必填** | **属性说明** |
| :--- | :---: | --- |
| NSInteger delay | 否 | 网络回环延迟 |
| BOOL internetConnect | 否 | 互联网连接情况，YES-正常 NO-异常 |
| BOOL streamConnect | 否 | 流媒体连接情况，YES-正常 NO-异常 |
| BOOL signalingConnect | 否 | 会控服务连接情况，YES-正常 NO-异常 |


### RTCNetworkCheckParams
会前网络检测参数（`3.3.0` 起），用于 [networkCheck:onItem:completion:](/zh/rtc/ios/api-reference/RTCEngineKit#会前网络检测相关接口函数)。`appId` + `serverUrl` 与 `token` 二选一；两者都传时以 `appId` + `serverUrl` 为准。

| **属性** | **必填** | **属性说明** |
| --- | :---: | --- |
| NSString *appId | 否 | 应用标识（app_id），与 `serverUrl` 一起传 |
| NSString *serverUrl | 否 | SDK 接口前缀，即令牌中的 `client_api`（如 `@"https://host/sdkapi"`），与 `appId` 一起传 |
| NSString *token | 否 | 任意一个本应用的 RTC 令牌（频道令牌 / 即时通讯令牌均可，不要求未过期）；`appId` / `serverUrl` 未传时从中解出 |
| NSInteger timeoutMs | 否 | 单项超时（毫秒），默认 3000，小于等于 0 时按默认值 |


### RTCNetworkCheckItem
会前网络检测单项结果（`3.3.0` 起）

| **属性** | **必填** | **属性说明** |
| --- | :---: | --- |
| [RTCNetworkCheckItemId](#rtcnetworkcheckitemid) itemId | 是 | 检测项标识 |
| [RTCNetworkCheckStatus](#rtcnetworkcheckstatus) status | 是 | 检测状态：`pass` / `warning` / `fail` / `skipped` / `unsupported` |
| [RTCNetworkCheckReason](#rtcnetworkcheckreason) reason | 是 | 机器可读的原因码，`pass` 时为空串 |
| NSString *message | 是 | 给人看的中文说明，App 可直接显示 |
| NSInteger costMs | 是 | 本项耗时（毫秒） |
| NSDictionary *data | 是 | 本项测量值，键名与其它端一致，见下表 |

`data` 的内容按检测项区分：

| **检测项** | **data** |
| --- | --- |
| `permission` | `{}` |
| `connectivity` | `{netType}`：`"wifi"` / `"cellular"` / `"ethernet"` / `"unknown"` |
| `mtu` | `{maxSize}`：能回显的最大探测包档位（字节），如 `1472`；全部不通时为 `0` |
| `dns` | `{hosts}`：各域名的解析结果数组，每个元素为 `{host, ips, costMs}` |
| `server` | `{api, signal, media}` 三个子检查，见下文 |

`server` 的每个子检查都是 `{ok, status, reason, rttMs}`：`ok` 表示是否连通；`status` 取 `"pass"` / `"fail"` / `"skipped"`；`reason` 为原因码，`pass` 时为空串；`rttMs` 为耗时（毫秒）。另外：

+ `api`：检测信息接口是否可达。失败时，收到 HTTP 响应则另带 `httpStatus`（HTTP 状态码）；HTTP 200 但业务码非 0 时另带 `code`（服务端业务错误码，如应用不存在或已停用）
+ `signal`：信令服务器是否连得上（先试 TCP/TLS，不通再试 WebSocket），另带 `via`：实际连通的方式 `"tcp"` 或 `"ws"`，不通时为空串
+ `media`：媒体服务器的 UDP 是否有应答

`toDictionary` 方法把单项结果转为字典（键名为 `id` / `status` / `reason` / `message` / `costMs` / `data`，与其它端一致），便于打日志或上报。


### RTCNetworkCheckResult
会前网络检测汇总结果（`3.3.0` 起）

| **属性** | **必填** | **属性说明** |
| --- | :---: | --- |
| [RTCNetworkCheckStatus](#rtcnetworkcheckstatus) status | 是 | 汇总状态：有 `fail` 即 `fail`；无 `fail` 但有 `warning` 即 `warning`；否则 `ok`（`skipped` / `unsupported` 不影响汇总） |
| `NSArray<RTCNetworkCheckItem *> *items` | 是 | 各项结果，固定 5 项、固定顺序：`permission`、`connectivity`、`mtu`、`dns`、`server` |
| NSInteger costMs | 是 | 总耗时（毫秒） |

`toDictionary` 方法把结果转为字典（键名为 `status` / `items` / `costMs`）。


### RTCNetworkCheckItemId
会前网络检测项标识（`3.3.0` 起，字符串常量，取值与其它端一致）

| **常量名** | **取值** | **检测内容** | **失败 / 告警时的原因码** |
| --- | --- | --- | --- |
| RTCNetworkCheckItemIdPermission | `permission` | 网络权限：蜂窝数据权限，仅当前不在 Wi-Fi / 有线网络下时才判失败 | `cellular_restricted` |
| RTCNetworkCheckItemIdConnectivity | `connectivity` | 系统网络连接状态 | `offline` |
| RTCNetworkCheckItemIdMtu | `mtu` | 向媒体服务器发不分片的 UDP 探测包（1200 / 1300 / 1400 / 1472 字节），取能回显的最大档 | `mtu_too_small`、`udp_blocked` |
| RTCNetworkCheckItemIdDns | `dns` | 解析接口、信令、媒体服务器的域名（IP 地址跳过） | `dns_failed` |
| RTCNetworkCheckItemIdServer | `server` | 接口 `api`、信令 `signal`、媒体 `media` 三个子检查 | `api_unreachable`、`signal_unreachable`、`udp_blocked`、`media_unavailable` |


### RTCNetworkCheckStatus
会前网络检测状态（`3.3.0` 起，字符串常量）。单项与汇总共用一套取值，汇总只会出现 `ok` / `warning` / `fail`。

| **常量名** | **取值** | **说明** |
| --- | --- | --- |
| RTCNetworkCheckStatusOk | `ok` | 汇总：全部正常 |
| RTCNetworkCheckStatusPass | `pass` | 单项：通过 |
| RTCNetworkCheckStatusWarning | `warning` | 单项 / 汇总：有隐患但可用 |
| RTCNetworkCheckStatusFail | `fail` | 单项 / 汇总：异常 |
| RTCNetworkCheckStatusSkipped | `skipped` | 单项：无需检测，如流媒体供应商不是 SeaStart 时不测 MTU |
| RTCNetworkCheckStatusUnsupported | `unsupported` | 单项：本平台不支持 |


### RTCNetworkCheckReason
会前网络检测原因码（`3.3.0` 起，字符串常量），通过时为空串

| **常量名** | **取值** | **说明** |
| --- | --- | --- |
| RTCNetworkCheckReasonNoPermission | `no_permission` | 未授予网络权限（iOS 不会出现，保留与其它端对齐） |
| RTCNetworkCheckReasonCellularRestricted | `cellular_restricted` | 蜂窝数据被系统设置限制，且当前不在 Wi-Fi / 有线网络下 |
| RTCNetworkCheckReasonOffline | `offline` | 当前没有网络连接 |
| RTCNetworkCheckReasonMtuTooSmall | `mtu_too_small` | 1200 字节的探测包都回不来，但 UDP 是通的（网络对大包有限制） |
| RTCNetworkCheckReasonUdpBlocked | `udp_blocked` | UDP 不通：媒体服务器无应答、探测包全部无回显 |
| RTCNetworkCheckReasonDnsFailed | `dns_failed` | 有域名解析失败 |
| RTCNetworkCheckReasonApiUnreachable | `api_unreachable` | 检测信息接口调用失败：服务器不可达，或服务端未升级、不支持会前网络检测 |
| RTCNetworkCheckReasonSignalUnreachable | `signal_unreachable` | 信令服务器连不上（TCP/TLS 与 WebSocket 都不通） |
| RTCNetworkCheckReasonVendorNotSupported | `vendor_not_supported` | 流媒体供应商不是 SeaStart，不做媒体 UDP / MTU 检测（`skipped` 时使用） |
| RTCNetworkCheckReasonMediaUnavailable | `media_unavailable` | 服务端没有可用的媒体节点（`server` 记 `fail`，`mtu` 记 `skipped`） |
| RTCNetworkCheckReasonServerInfoUnavailable | `server_info_unavailable` | 拿不到服务端检测信息，依赖它的 `mtu` 与信令、媒体检测记 `skipped` |
| RTCNetworkCheckReasonDfNotSupported | `df_not_supported` | 系统设不了不分片，`mtu` 记 `unsupported` |


### RTCStreamAudioModel
成员音频信息

| **属性** | **必填** | **属性说明** |
| --- | :---: | --- |
| NSString *userId | 否 | 用户标识，自`3.0.0`起可空 |
| int linkId | 是 | 连接标识(流媒体)，wangsu 流媒体下服务端不下发该值，恒为`0` |
| NSInteger power | 否 | 音频功率 |
| NSInteger db | 否 | 音频分贝值 |

> 注：识别讲话成员请直接使用`userId`，不要用`linkId`反查成员。`linkId`在 wangsu 流媒体下对所有成员恒为`0`，据此反查必然命中错误的人；SDK 自`3.1.2`起已在该链路下改用底层连接解析`userId`。


### RTCStreamSendModel
流媒体发送状态信息

| **属性** | **必填** | **属性说明** |
| --- | :---: | --- |
| int buffer | 否 | 上传缓冲包数 |
| int delay | 否 | 上传延迟 |
| int overflow | 否 | 溢出缓冲包数 |
| NSString *speed | 否 | 上传速率(单位kbps) |
| NSInteger status | 否 | 上传状态 |
| float loss_r | 否 | 补偿前丢包率 |
| float loss_c | 否 | 补偿后丢包率 |


### RTCStreamReceiveModel
流媒体接收状态信息

| **属性** | **必填** | **属性说明** |
| --- | :---: | --- |
| NSString *userId | 否 | 用户标识，自`3.0.0`起可空 |
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


### SRTCDeviceType
设备类型

| **枚举名** | **枚举值** | **说明** |
| --- | :---: | --- |
| SRTCDeviceTypeUnknown | `0` | 未知终端 |
| SRTCDeviceTypeWindows | `1` | Windows |
| SRTCDeviceTypeAndroid | `2` | Android |
| SRTCDeviceTypeIOS | `3` | iOS |
| SRTCDeviceTypeLinux | `4` | Linux |
| SRTCDeviceTypeMacOS | `5` | MacOS |
| SRTCDeviceTypeWebRTC | `6` | WebRTC |
| SRTCDeviceTypeRtmp | `7` | RTMP |
| SRTCDeviceTypeHarmonyOS | `8` | HarmonyOS |


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


### RTCStreamType
媒体流类型

| **枚举名** | **枚举值** | **说明** |
| --- | :---: | --- |
| RTCStreamTypeAudio | `0` | 音频流类型 |
| RTCStreamTypeVideo | `1` | 视频流类型 |


### RTCCodecType
编码类型

| **枚举名** | **枚举值** | **说明** |
| --- | :---: | --- |
| RTCCodecTypeUnknown | `0` | 未知类型 |
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


### RTCStreamQualityLevel
流媒体质量等级

| **枚举名** | **枚举值** | **说明** |
| --- | :---: | --- |
| RTCStreamQualityLevelUnknown | `0` | 未知 |
| RTCStreamQualityLevelExcellent | `1` | 优秀（`excellent`） |
| RTCStreamQualityLevelGood | `2` | 良好（`good`） |
| RTCStreamQualityLevelPoor | `3` | 较差（`poor`） |
| RTCStreamQualityLevelLost | `4` | 已断流（`lost`） |

