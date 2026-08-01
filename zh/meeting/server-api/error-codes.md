---
title: "错误码"
description: "服务端 API 响应体中 code 的取值"
---

{/* 本页错误码由后端源码自动生成，请勿手工编辑 —— 改动会在下次同步时被覆盖。
    内容一律改 meeting-backend 的源码，写法见那边 README 的「对外接口文档（srvapi）」一节。 */}

响应体的 `code` 为 `0` 表示成功，非 0 表示失败，此时 `msg` 是可读的错误描述。
业务侧请**按 `code` 判断**，不要匹配 `msg` 文案 —— 文案会随版本调整，码不会。

## 业务错误码

| 错误码 | 枚举名 | 说明 |
| --- | --- | --- |
| `2040` | CodeTokenChanged | 当前用户已在其它地登录 |
| `2041` | HeaderMissingAppId | 请求头中缺少app_id |
| `2042` | HeaderInvalidAppId | 请求头中的app_id无效 |
| `2043` | HeaderInvalidSignature | 请求头中的signature无效 |
| `2044` | HeaderInvalidTimestamp | 设备时间不准，请调整时间后继续操作 |
| `2045` | HeaderInvalidMeetSid | 请求头中的meet_sid无效 |
| `2046` | HeaderMissingNonce | 请求头中缺少nonce |
| `2047` | HeaderMissingUserId | 请求头中缺少user_id |
| `2050` | MakeTokenFailed | 生成Token失败 |
| `2051` | Unauthorized | 未获取授权 |
| `2052` | AuthorizationExpired | 授权过期 |
| `2053` | InvalidCallback | 回调配置无效 |
| `2100` | MeetingError | 会议内部错误 |
| `2101` | MeetingNotFound | 会议不存在 |
| `2102` | MeetingNotStart | 会议未开始 |
| `2103` | MeetingEnded | 会议已结束 |
| `2104` | MeetingAlreadyShare | 会中已经有人在共享 |
| `2105` | MeetingNotSharing | 会中不在共享状态 |
| `2106` | MeetingLocked | 会议已锁定 |
| `2107` | MeetingKickout | 已被踢出，无法入会 |
| `2108` | MemberInOther | 已经在其它会议中 |
| `2109` | MemberInMeeting | 已经在该会议中 |
| `2110` | MemberNotInMeeting | 不在该会议中 |
| `2111` | TargetNotInMeeting | 目标不在该会议中 |
| `2112` | MicNotAllow | 不允许开麦克风 |
| `2113` | CameraNotAllow | 不允许开摄像头 |
| `2114` | ChatNotAllow | 不允许聊天 |
| `2115` | PasswordNotCorrect | 密码错误 |
| `2116` | MemberNotOnList | 会议仅限受邀人加入,请联系主持人 |
| `2117` | ShareNotAllow | 不允许共享 |
| `2118` | EnterWaitingRoom | 加入会议失败，进入了等候室 |
| `2120` | EnterBeforeHost | 不能在主持人进入前加入会议 |

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
