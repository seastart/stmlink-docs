---
title: "错误码"
description: "SMeeting 会议 错误码枚举与处理说明"
---

| **枚举名** | **枚举值** | **说明** |
| --- | :---: | --- |
| CodeTokenChanged | `2040` | 当前用户已在其它地登录 |
| HeaderMissingAppId | `2041` | 请求头中缺少app_id |
| HeaderInvalidAppId | `2042` | 请求头中的app_id无效 |
| HeaderInvalidSignature | `2043` | 请求头中的signature无效 |
| HeaderInvalidTimestamp | `2044` | 设备时间不准，请调整时间后继续操作 |
| HeaderInvalidMeetSid | `2045` | 请求头中的meet_sid无效 |
| HeaderMissingNonce | `2046` | 请求头中缺少nonce |
| HeaderMissingUserId | `2047` | 请求头中缺少user_id |
| MakeTokenFailed | `2050` | 生成Token失败 |
| Unauthorized | `2051` | 未获取授权 |
| AuthorizationExpired | `2052` | 授权过期 |
| InvalidCallback | `2053` | 回调配置无效 |
| MeetingError | `2100` | 会议内部错误 |
| MeetingNotFound | `2101` | 会议不存在 |
| MeetingNotStart | `2102` | 会议未开始 |
| MeetingEnded | `2103` | 会议已结束 |
| MeetingAlreadyShare | `2104` | 会中已经有人在共享 |
| MeetingNotSharing | `2105` | 会中不在共享状态 |
| MeetingLocked | `2106` | 会议已锁定 |
| MeetingKickout | `2107` | 已被踢出，无法入会 |
| MemberInOther | `2108` | 已经在其它会议中 |
| MemberInMeeting | `2109` | 已经在该会议中 |
| MemberNotInMeeting | `2110` | 不在该会议中 |
| TargetNotInMeeting | `2111` | 目标不在该会议中 |
| MicNotAllow | `2112` | 不允许开麦克风 |
| CameraNotAllow | `2113` | 不允许开摄像头 |
| ChatNotAllow | `2114` | 不允许聊天 |
| PasswordNotCorrect | `2115` | 密码错误 |
| MemberNotOnList | `2116` | 会议仅限受邀人加入,请联系主持人 |
| ShareNotAllow | `2117` | 不允许共享 |
| EnterWaitingRoom | `2118` | 加入会议失败，进入了等候室 |
| EnterBeforeHost | `2120` | 不能在主持人进入前加入会议 |
