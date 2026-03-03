---
title: "错误码"
description: "iOS SMeeting 会议 SDK 错误码枚举与处理说明"
---

### SEAError
错误码

| **枚举名** | **枚举值** | **说明** |
| --- | :---: | --- |
| SEAErrorOK | `0` | 无错误 |
| **API 错误码** | | |
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
| **系统级错误码** | | |
| SEAErrorSystemError | `100001` | 系统内部错误 |
| SEAErrorNotInitialized | `100002` | 未初始化 |
| SEAErrorMediaNotInitialized | `100003` | 媒体模块尚未初始化 |
| SEAErrorProtocolParsingError | `100004` | 协议解析错误 |
| **通用错误码** | | |
| SEAErrorTimeout | `100005` | 超时 |
| SEAErrorInvalidArgs | `100006` | 参数错误 |
| SEAErrorConflict | `100007` | 重复操作冲突 |
| SEAErrorSdkTokenInvalid | `100008` | 令牌失效 |
| **网络错误码** | | |
| SEAErrorNetError | `100009` | 网络错误 |
| SEAErrorMediaNetError | `100010` | 媒体网络错误 |
| SEAErrorNotFound | `100011` | 目标不存在 |
| **客户端错误码** | | |
| SEAErrorDeviceNoAuthorized | `103001` | 设备访问无权限 |
| SEAErrorNotJoinedChannel | `103002` | 未加入频道 |
| SEAErrorForbidden | `103003` | 操作不被允许 |
| SEAErrorStreamNotFound | `103004` | 码流不存在 |
| SEAErrorNotAuthorized | `103005` | 没有权限执行操作 |


