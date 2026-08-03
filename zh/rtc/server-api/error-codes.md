---
title: "错误码"
description: "服务端 API 响应体中 code 的取值"
---

{/* 本页错误码由后端源码自动生成，请勿手工编辑 —— 改动会在下次同步时被覆盖。
    内容一律改 rtc-backend 的源码，写法见那边 README 的「对外接口文档（srvapi）」一节。 */}

响应体的 `code` 为 `0` 表示成功，非 0 表示失败，此时 `msg` 是可读的错误描述。
业务侧请**按 `code` 判断**，不要匹配 `msg` 文案 —— 文案会随版本调整，码不会。

## 业务错误码

| 错误码 | 枚举名 | 说明 |
| --- | --- | --- |
| `1001` | HeaderMissingAppId | 请求头中缺少app_id |
| `1002` | HeaderInvalidAppId | 请求头中的app_id无效 |
| `1003` | HeaderInvalidSignature | 请求头中的signature无效 |
| `1004` | HeaderInvalidTimestamp | 请求头中的timestamp无效 |
| `1005` | HeaderInvalidSid | 请求头中的sid无效 |
| `1006` | HeaderMissingNonce | 请求头中缺少nonce |
| `1011` | InvalidApp | 应用无效 |
| `1012` | InvalidSrvGroup | 服务组无效 |
| `1013` | InvalidServer | 服务无效 |
| `1014` | InvalidScene | 应用场景无效 |
| `1015` | InvalidCallback | 回调配置无效 |
| `1020` | GrantChannelTokenFailed | 生成Channel Token失败 |
| `1021` | ChannelTokenUsed | channel token已被使用 |
| `1022` | SidNotInChannel | 该会话不在频道中 |
| `1023` | UserNotInChannel | 成员不在频道中 |
| `1024` | ChannelNotOpen | 频道未开启 |
| `1025` | ChannelOpened | 频道已开启 |
| `1027` | GrantWbTokenFailed | 生成白板Token失败 |
| `1028` | InvalidChannelName | 频道名不符合规范 |
| `1029` | InvalidUid | uid不符合规范 |
| `1030` | GrantImTokenFailed | 生成IM Token失败 |
| `1031` | ImTokenUsed | IM Token已被使用 |
| `1032` | SidNotFound | 该会话不在线 |
| `1033` | ConcurrentLimit | 并发已达上限 |
| `1040` | McuTaskNotFound | 未找到MCU任务 |
| `1041` | McuRecordNotStop | 录像任务还未结束 |
| `1042` | McuRecordNoVod | 录像任务还未生成录像文件 |
| `1043` | McuLayoutDataErr | MCU的布局数据出错 |
| `1044` | McuTaskIsEnd | MCU任务已经停止 |
| `1050` | TalkrecTaskNotFound | 未找到语音录制任务 |
| `1051` | TalkrecRecordNotFound | 未找到语音录制段 |
| `1052` | TalkrecRecordNoVod | 语音录制段还未生成录音文件 |
| `1053` | TalkrecGatewayNotFound | 没有可用的语音录制网关 |

## 框架通用错误码

所有接口都可能返回这一组，其中 `10070` 最常见 —— 参数没通过校验（必填、长度、字符集、取值范围）时返回它，具体哪个参数看 `msg`。

| 错误码 | 枚举名 | 说明 |
| --- | --- | --- |
| `10000` | CodeUnSpecial | 通用未指定错误 |
| `10001` | CodeDatabaseException | 数据库错误 |
| `10002` | CodeDataRecordNotFound | 数据记录未找到 |
| `10003` | CodeDataRecordExists | 数据记录已存在 |
| `10040` | CodeUnAuthorized | 权限不足 |
| `10041` | CodeAuthFailed | 未登录 |
| `10042` | CodeTokenInvalid | token无效 |
| `10043` | CodeTokenExpired | token已过期 |
| `10051` | CodeNetError | 网络错误 |
| `10055` | CodeRequestTimeout | 请求超时 |
| `10070` | CodeInvalidParams | 请求参数不合法 |
