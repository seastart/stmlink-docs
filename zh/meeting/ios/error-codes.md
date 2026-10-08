---
title: "错误码"
description: "iOS SMeeting 会议 SDK 错误码枚举与处理说明"
---

`SEAError` 是失败回调 `SEAFailedBlock` 的 `code`，也是 `onError`、`onImDisconnected` 等回调的 `errCode` 类型。`0`（`SEAErrorOK`）代表成功，非 0 都是错误。

<Note>
本页取值自 **2.2.0** 起生效。2.2.0 起会议层自身的错误改用 `203` 段、透传的 RTC 层错误码随 `RTCEngineKit 3.2.0` 重排，2.1.0 及以前的旧码与新码对照见 [更新日志](/zh/meeting/ios/changelog)。各端共用的编号规则见 [错误码规则与总表](/zh/meeting/error-codes)。
</Note>

### 取值规则

| 类别 | 取值 | 来源 | `message` |
| --- | --- | --- | --- |
| 后端业务码 | `1000`–`99999` | 后端返回，SDK 原样透传 | 后端返回的 `msg`，语言随 `language` |
| 会议层客户端码 | `203xxx` | MeetingKit 自身产生，iOS 前缀 `203` + 统一码表低 3 位，与 Swift SDK 同号同义 | 英文 |
| RTC 层透传码 | `103xxx` | RTCEngineKit 产生，与 `RTCEngineError` 同值，会议层不重新包装 | 英文，并带上 RTC 码 |

+ **判断错误类型只看 `code`**，不要按 `message` 做分支，也不要把 `message` 直接展示给终端用户；需要给用户看的提示请按 `code` 自行映射
+ 会议层与 RTC 层的低 3 位是两套独立的表，`203004`（无权限）与 `103004`（令牌不合法）含义不同，请比较完整的 6 位码
+ `language` 只影响会议层请求后端时的 `Accept-Language`，即后端业务码的文案语言，见 [MeetingKit.language](/zh/meeting/ios/api-reference/MeetingKit#language)；RTC 层自身的请求暂不带语言

### SEAError

#### 会议层客户端错误码

| **枚举名** | **枚举值** | **说明** |
| --- | :---: | --- |
| SEAErrorOK | `0` | 无错误 |
| SEAErrorMeetingNotLoggedIn | `203001` | 未登录会议 SDK（本端暂未产生，保留与各端对齐） |
| SEAErrorMeetingTokenExpired | `203002` | Token 已过期（本端暂未产生，保留与各端对齐） |
| SEAErrorMeetingNotInMeeting | `203003` | 不在会议中（本端暂未产生，保留与各端对齐） |
| SEAErrorMeetingUnauthorized | `203004` | 无权限，如该接口仅主持人或联席主持人可调用 |
| SEAErrorNotAuthorized | `203004` | 已废弃，`SEAErrorMeetingUnauthorized` 的同值别名（旧值 `103005`） |
| SEAErrorMeetingTokenInvalid | `203005` | Token 格式无效，会议令牌解不开 |
| SEAErrorMeetingAlreadyInMeeting | `203006` | 已在会议中，请先退出（房间实例正在加入或已加入） |
| SEAErrorMeetingNetworkError | `203007` | 网络错误：连不上、HTTP 非 200 等，HTTP 状态见 `message` |
| SEAErrorMeetingDeviceError | `203008` | 设备错误（保留；采集与权限失败透传 RTC 层的码） |
| SEAErrorMeetingInternalError | `203009` | SDK 内部错误，如下载文件落盘失败 |
| SEAErrorMeetingUserNotFound | `203010` | 会议中没有该成员（本端暂未产生，保留与各端对齐） |
| SEAErrorMeetingInvalidState | `203011` | 当前状态不允许该操作，如房间实例已销毁 |
| SEAErrorMeetingInvalidArgument | `203012` | 参数非法（本端暂未产生，保留与各端对齐） |
| SEAErrorMeetingRemoteTrackUnavailable | `203209` | 远端轨道不可用：成员在会议中，但没有要订阅的这路视频 |
| SEAErrorMeetingRequestTimeout | `203353` | 请求超时 |
| SEAErrorMeetingRequestCancelled | `203354` | 请求被取消 |
| SEAErrorMeetingEmptyResponseBody | `203355` | 响应体为空 |
| SEAErrorMeetingResponseParseFailed | `203356` | 响应解析失败：不是 JSON 对象、缺 `code` 字段或结构不符 |

<Warning>
`SEAErrorNotAuthorized` 与 `SEAErrorMediaNotInitialized` 已废弃，分别与 `SEAErrorMeetingUnauthorized`、`SEAErrorNotInitialized` 同值。`switch` 中同时写一对同值常量会报重复 `case`；引用废弃常量会产生废弃告警，开启 `-Werror` 的工程会编译失败，请改用新名字。
</Warning>

#### RTC 层透传错误码

取值与 `RTCEngineKit` 的 `RTCEngineError` 一致，详见 [SRTC iOS 错误码](/zh/rtc/ios/error-codes)。括号内为 2.1.0 及以前的旧值。

| **枚举名** | **枚举值** | **说明** |
| --- | :---: | --- |
| SEAErrorNotJoinedChannel | `103001` | 未加入频道（旧 `103002`） |
| SEAErrorStreamNotFound | `103003` | 码流不存在（旧 `103004`） |
| SEAErrorSdkTokenInvalid | `103004` | 令牌不合法（旧 `100008`） |
| SEAErrorConflict | `103005` | 重复操作冲突（旧 `100007`） |
| SEAErrorNetError | `103006` | RTC 层网络错误，含 HTTP 非 200（旧 `100009`）。会议层的网络失败不再使用本码，见 `203007` |
| SEAErrorTimeout | `103007` | 超时（旧 `100005`） |
| SEAErrorProtocolParsingError | `103011` | 协议解析错误（旧 `100004`） |
| SEAErrorMediaNetError | `103012` | 媒体网络错误（旧 `100010`） |
| SEAErrorNotInitialized | `103024` | 未初始化 / 当前状态不允许（旧 `100002`） |
| SEAErrorMediaNotInitialized | `103024` | 已废弃，`SEAErrorNotInitialized` 的同值别名（旧 `100003`） |
| SEAErrorSystemError | `103025` | 系统内部错误（旧 `100001`） |
| SEAErrorUserCancelled | `103026` | 用户取消（旧 `100012`） |
| SEAErrorVirtualBackgroundAlreadyInstalled | `103027` | 虚拟背景已装载（旧版以 `100007` 返回） |
| SEAErrorVirtualBackgroundNotInstalled | `103028` | 虚拟背景未装载（旧版以 `100007` 返回） |
| SEAErrorVirtualBackgroundModelNotFound | `103029` | 虚拟背景模型不存在或无效（旧版以 `100011` 返回） |
| SEAErrorVirtualBackgroundSessionFailed | `103030` | 虚拟背景推理会话创建失败（旧版以 `100001` 返回） |
| SEAErrorInvalidArgs | `103031` | 参数错误（旧 `100006`） |
| SEAErrorDeviceNoAuthorized | `103042` | 设备访问无权限，无法区分摄像头 / 麦克风时使用（旧 `103001`）；当前不再返回，改报 `103231` / `103251` |
| SEAErrorForbidden | `103043` | 操作不被允许（旧 `103003`） |
| SEAErrorSwitchAudioRouteFail | `103044` | 音频路由切换失败（旧 `103005`） |
| SEAErrorNotFound | `103204` | 频道内没有该用户（旧 `100011`） |
| SEAErrorCameraNoAuthorized | `103231` | 无摄像头权限（旧版以 `103001` 返回） |
| SEAErrorMicNoAuthorized | `103251` | 无麦克风权限（旧版以 `103001` 返回） |

#### 后端业务码

后端返回、SDK 原样透传，`message` 为后端返回的 `msg`，语言随 `language`。完整清单与含义以 [服务端 API 错误码](/zh/meeting/server-api/error-codes) 为准。

<Note>
2.2.0 起 SDK 不再自己产生 `SEAErrorApiTokenDisabled`（`10042`）、`SEAErrorApiRepeatFound`（`10003`）等码来表示本地错误，这些常量只在后端真的返回该码时出现。
</Note>

| **枚举名** | **枚举值** | **说明** |
| --- | :---: | --- |
| SEAErrorRtcApiHeaderNotAppId | `1001` | 请求头中缺少APPID |
| SEAErrorRtcApiHeaderInvalidAppId | `1002` | 请求头中的APPID无效 |
| SEAErrorRtcApiHeaderInvalidSignature | `1003` | 请求头中的签名无效 |
| SEAErrorRtcApiHeaderInvalidTimestamp | `1004` | 请求头中的时间戳无效 |
| SEAErrorApiHeaderInvalidSession | `1005` | 请求头中的会话标识无效 |
| SEAErrorRtcApiHeaderNotNonce | `1006` | 请求头中缺少随机标识 |
| SEAErrorRtcApiInvalidApplication | `1011` | 应用无效 |
| SEAErrorRtcApiInvalidServiceGroup | `1012` | 服务组无效 |
| SEAErrorRtcApiInvalidService | `1013` | 服务无效 |
| SEAErrorRtcApiInvalidScene | `1014` | 应用场景无效 |
| SEAErrorRtcApiInvalidConfigure | `1015` | 回调配置无效 |
| SEAErrorRtcApiChannelTokenFailed | `1020` | 生成 Channel Token 失败 |
| SEAErrorRtcApiChannelTokenOccupied | `1021` | Channel Token 已被使用 |
| SEAErrorRtcApiSessionNotFound | `1022` | 该会话不在频道中 |
| SEAErrorRtcApiMemberNotFound | `1023` | 成员不在频道中 |
| SEAErrorRtcApiChannelNotOpen | `1024` | 频道未开启 |
| SEAErrorRtcApiChannelOpen | `1025` | 频道已开启 |
| SEAErrorRtcApiImTokenFailed | `1030` | 生成 Im Token 失败 |
| SEAErrorRtcApiImTokenOccupied | `1031` | Im Token 已被使用 |
| SEAErrorRtcApiSessionOffline | `1032` | 该会话不在线 |
| SEAErrorRtcApiInsufficientConcurrency | `1033` | 并发已达上限 |
| SEAErrorRtcApiNotFoundMcuTask | `1040` | 未找到MCU任务 |
| SEAErrorRtcApiRecordTaskUnfinished | `1041` | 录像任务还未结束 |
| SEAErrorRtcApiRecordTaskNotFile | `1042` | 录像任务还未生成录像文件 |
| SEAErrorRtcApiMcuLayoutFailed | `1043` | MCU的布局数据出错 |
| SEAErrorRtcApiMcuTaskStoped | `1044` | MCU任务已经停止 |
| SEAErrorMeetingApiRemoteLogin | `2040` | 当前用户已在其它地登录 |
| SEAErrorMeetingApiHeaderNotAppId | `2041` | 请求头中缺少APPID |
| SEAErrorMeetingApiHeaderInvalidAppId | `2042` | 请求头中的APPID无效 |
| SEAErrorMeetingApiHeaderInvalidSignature | `2043` | 请求头中的签名无效 |
| SEAErrorMeetingApiHeaderInvalidTimestamp | `2044` | 请求头中的时间戳无效 |
| SEAErrorMeetingApiHeaderInvalidSession | `2045` | 请求头中的会议会话标识无效 |
| SEAErrorMeetingApiHeaderNotNonce | `2046` | 请求头中缺少随机标识 |
| SEAErrorMeetingApiHeaderNotUserId | `2047` | 请求头中缺少用户标识 |
| SEAErrorMeetingApiTokenFailed | `2050` | 生成 Token 失败 |
| SEAErrorMeetingApiNotAuthorized | `2051` | 未获取授权 |
| SEAErrorMeetingApiTokenExpired | `2052` | 授权过期 |
| SEAErrorMeetingApiFailed | `2100` | 会议内部错误 |
| SEAErrorMeetingApiNotFound | `2101` | 会议不存在 |
| SEAErrorMeetingApiNotStarted | `2102` | 会议未开始 |
| SEAErrorMeetingApiFinished | `2103` | 会议已结束 |
| SEAErrorMeetingApiSomeoneSharing | `2104` | 会中已经有人在共享 |
| SEAErrorMeetingApiNotSharing | `2105` | 会中不在共享状态 |
| SEAErrorMeetingApiLocked | `2106` | 会议已被锁定 |
| SEAErrorMeetingApiKickedout | `2107` | 已被踢出，无法入会 |
| SEAErrorMeetingApiAtOtherMeeting | `2108` | 已经在其它会议中 |
| SEAErrorMeetingApiAlreadyExisted | `2109` | 已经在该会议中 |
| SEAErrorMeetingApiNotMeeting | `2110` | 不在该会议中 |
| SEAErrorMeetingApiMemberNotFound | `2111` | 目标不在该会议中 |
| SEAErrorMeetingApiMicDisabled | `2112` | 不允许开麦克风 |
| SEAErrorMeetingApiCameraDisabled | `2113` | 不允许开摄像头 |
| SEAErrorMeetingApiChatDisabled | `2114` | 不允许聊天 |
| SEAErrorMeetingApiPasswordFailed | `2115` | 密码错误 |
| SEAErrorMeetingApiByInviteOnly | `2116` | 会议仅限受邀人加入,请联系主持人 |
| SEAErrorMeetingApiWaitingRoomEnable | `2118` | 会议开启等候室，需要管理员确认后入会 |
| SEAErrorMeetingApiEnterBeforeHostDisabled | `2120` | 会议禁止在主持人之前加入 |
| SEAErrorApiFailed | `10000` | 未归类的通用错误 |
| SEAErrorApiDatabaseFailed | `10001` | 数据库错误或异常 |
| SEAErrorApiRecordNotFound | `10002` | 数据记录未找到 |
| SEAErrorApiRepeatFound | `10003` | 数据记录已存在 |
| SEAErrorApiNotAuthorized | `10040` | ⽆权限 |
| SEAErrorApiNotInitialized | `10041` | 未登录 |
| SEAErrorApiTokenDisabled | `10042` | 令牌⽆效 |
| SEAErrorApiTokenExpired | `10043` | 令牌已过期 |
| SEAErrorApiNetworkFailed | `10051` | ⽹络错误或异常 |
| SEAErrorApiNetworkTimeout | `10055` | 请求超时 |
| SEAErrorApiInvalidParameter | `10070` | 请求参数不合法 |
