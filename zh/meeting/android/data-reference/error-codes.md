---
title: "错误码"
description: "Android SMeeting 会议 SDK 错误码枚举与处理说明"
---

### StatusCode
错误码

| **枚举名** | **枚举值**  | **说明** |
| --- |:--------:| --- |
| OK |   `0`    | 无错误 |
| **系统级错误码** |          | |
| SystemError | `100001` | 系统内部错误 |
| NotInitialized | `100002` | 未初始化 |
| MediaNotInitialized | `100003` | 媒体模块尚未初始化 |
| ProtocolParsingError | `100004` | 协议解析错误 |
| **通用错误码** |          | |
| Timeout | `100005` | 超时 |
| InvalidArgs | `100006` | 参数错误 |
| Conflict | `100007` | 重复操作冲突 |
| SdkTokenInvalid | `100008` | 令牌失效 |
| **网络错误码** |          | |
| NetError | `100009` | 网络错误 |
| MediaNetError | `100010` | 媒体网络错误 |
| DeviceNotfound | `100011` | 目标不存在 |
| **客户端错误码** |          | |
| LACK_PERMISSION | `102001` | 设备访问无权限 |
| ERROR_TRACK_TYPE | `102002` | track 不匹配 |
| SDK_NOT_INIT | `102201` | sdk未准备好 |
| CHANNEL_NOT_START | `102202` | 频道未开始 |
| STREAM_NOT_READY | `102203` | 流媒体未准备好 |
| USER_NOT_FIND | `102204` | 成员未找到 |
| TRACK_NOT_FIND | `102205` | 轨道未找到 |
| ERROR_PARAM_ILLEGAL | `102310` | 参数错误 |
| ERROR_OPERATION_CANCEL | `102311` | 操作抵消 |
| ERROR_OPERATION_IGNORE | `102312` | 操作忽略 |
| ERROR_ABOUT_SDP_OPERATION | `102313` | sdp 相关操作失败 |
| ERROR_SUBSCRIBE_REFUSE | `102314` | 服务器拒绝订阅 |
| ERROR_CODE_API_NOT_INITIALIZED | `202010` | api未初始化 |
| ERROR_NO_PERMISSION | `202040` | 无权限 |
| ERROR_NET | `202051` | 网络错误 |
| ERROR_PARAM_ILLEGAL | `202070` | 请求参数不合法 |
| ERROR_CANCEL_HTTP | `202071` | 请求被取消 |
| ERROR_CONCURRENT_LIMIT |  `1033`  | 并发已达上限 |
| ERROR_ENTER_MEETING_PWD_ERROR |  `2115`  | 加入会议密码错误 |
| ApiFailed |  `202000`  | 未归类的通用错误 |
| ApiDatabaseFailed |  `202001`  | 数据库错误或异常 |
| ApiRecordNotFound |  `202002`  | 数据记录未找到 |
| ApiRepeatFound |  `202003`  | 数据记录已存在 |
| ApiNotAuthorized |  `202004`  | 无权限 |
| ApiNotInitialized |  `202005`  | 未登录 |
| ApiTokenDisabled |  `202006`  | 令牌无效 |
| ApiTokenExpired |  `202007`  | 令牌已过期 |
| ApiNetworkFailed |  `202008`  | 网络错误或异常 |
| ApiNetworkTimeout |  `202009`  | 请求超时 |
| ApiInvalidParameter |  `202010`  | 请求参数不合法 |
| ApiInvalidReturnValue |  `202011`  | 返回参数不合法 |
| ApiMeetingOver |  `202012`  | 会议已结束 |
| DeviceOpenFail |  `202013`  | 打开设备失败 |
| CancelEnterRoom |  `202014`  | 取消进入房间 |
| CancelBoardShare |  `202015`  | 取消白板共享 |
| MissBoardUrl |  `202016`  | 缺少白板 URL |
| CancelEnableIm |  `202017`  | 取消启动即时通讯 |
