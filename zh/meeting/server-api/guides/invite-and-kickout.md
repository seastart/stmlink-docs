---
title: "邀请入会与移出"
description: "从你的业务后端把人员（App / Web 用户）或会议室终端、监控等设备拉进会议、强制入会、移出会议，以及怎么知道邀请失败了：人员与设备两条路的接口、参数和限制对照"
---

平台侧把人拉进会议有两条路：**人员**（登录了 App / Web 的用户）用会议层的
[会议时呼叫人员入会](/zh/meeting/server-api/meet-admin#会议时呼叫人员入会)（`call-users`），
**设备**（SIP / H.323 终端、国标监控、RTSP 等）用经 SMeeting 转发的
[邀请设备入会](/zh/rtc/server-api/agent#邀请设备入会)（`agent/invite`）。移出则两者共用一个接口。

## 对照表

| | 人员 | 设备 |
| --- | --- | --- |
| 邀请接口 | `POST /server/v1/meet-admin/call-users` | `POST /server/v1/agent/invite` |
| 会议怎么填 | `room_no` 或 `meeting_id` 二选一 | `no` 填会议房间号 `room_no`（不是 `meeting_id`） |
| 对方要不要确认 | 要：被叫人的各端弹出来电，接听后入会 | 不用：设备网关直接呼叫或拉流。SIP / H.323 终端是否自动应答，看终端自己的设置 |
| 强制入会 | 传 `force_join=true`：不弹来电，直接入会；正在别的会里会先退出再进 | 总是强制：设备已在别的会里会直接切到这场，终端不挂断 |
| 能进的受限会议 | 见下文「能进哪些受限会议」 | 见下文「能进哪些受限会议」 |
| 移出 | [主持人踢人](/zh/meeting/server-api/meet-admin#主持人踢人)（`kickout-user`），`target_id` 填用户 ID | 同一个接口，`target_id` 填设备的会中 ID（带 `_agent_` 前缀） |
| 失败怎么知道 | 返回值 `offline_user_ids` 列出不在线的人；没接、拒接用「60 秒内没收到 `user_enter` 回调」判断 | [`device_invite_failed` 回调](/zh/meeting/server-api/guides/callbacks#device_invite_failed-—-设备邀请失败) |

## 邀请人员：call-users

```json
{
  "room_no": "021890611",
  "conferee_details": [{ "user_id": "1001" }, { "user_id": "1002" }],
  "is_additional": true,
  "force_join": true
}
```

+ 被叫人会被同步进参会人员（白名单），并收到一条呼叫；`is_additional=true` 表示追加，不覆盖原有的参会人员
+ 被叫人要**登录着**某一端 App / Web（即时通讯在线）才收得到呼叫
+ 返回 `data.offline_user_ids`：呼叫当时即时通讯不在线、一定收不到这次呼叫的人。都在线时为空数组；
  在线状态暂时查不到时按在线处理，不会误报

```json
{ "code": 0, "data": { "offline_user_ids": ["1002"] } }
```

### 强制入会（force_join）

`force_join=true` 时，我们的 App（STM Link 等）收到呼叫后：

+ 不弹来电页，提示一句后直接入会；入会时的昵称、摄像头 / 麦克风开关沿用 App 的入会设置
+ 正在别的会议里（含等候室、正在入会）：先离开当前会议再进这场。离开只退出自己，即使是主持人也不结束会议，也不弹确认框
+ 已经在这场会议里：忽略
+ 入会失败（如会议已结束）按普通入会失败提示，不重试

不传或传 `false` 时，保持普通的来电页（接听 / 拒绝，60 秒超时）。

## 邀请设备：agent/invite

设备邀请经 SMeeting 原样转发到 SRTC，参数与签名的填法见[设备接入与 IM](/zh/meeting/server-api/guides/agent-and-im#设备入会时目标房间填什么)，
字段说明见 SRTC 的[邀请设备入会](/zh/rtc/server-api/agent#邀请设备入会)。

```json
{
  "agents": [{ "type": 2, "contact": "192.168.0.18:5060" }],
  "no": "021890611"
}
```

+ 设备不用确认。设备网关呼叫 SIP / H.323 终端，终端配置了自动应答就直接入会，否则要有人在终端上接听；国标、RTSP 等拉流设备直接拉流入会
+ 设备已经在别的会议里时，会直接切到这场会议，通话不中断、终端不挂断
+ 接口返回成功只代表邀请已下发给设备网关，**不代表设备已入会**。入会成功看 `user_enter` 回调，失败看 `device_invite_failed` 回调

## 能进哪些受限会议

邀请会放过会议的部分入会限制，被邀请方不用输密码、不会卡在等候室：

| 入会限制 | 设备（平台邀请） | 人员，`force_join=true` | 人员，普通呼叫 |
| --- | --- | --- | --- |
| 会议密码 | 放过 | 放过 | 放过 |
| 参会人员白名单 | 放过 | 放过（呼叫时已加入白名单） | 放过（呼叫时已加入白名单） |
| 会议锁定 | 放过 | 放过 | 照常拦截 |
| 等候室 | 放过（直接进会） | 放过（直接进会） | 照常进等候室 |
| 主持人入会前不允许他人加入 | 放过 | 放过 | 照常拦截 |

+ 人员的放行**有效期 30 分钟**：要凭这次呼叫在 30 分钟内入会，超时后按普通入会处理；同一人被再次呼叫时以最新一次为准
+ **设备自己呼入**（终端拨会议号进来）不算平台邀请，仍走正常的入会校验
+ 会议已结束、被拉黑（踢人时带了 `join_disabled`）等其它规则不受影响

## 移出：kickout-user

人员和设备都用[主持人踢人](/zh/meeting/server-api/meet-admin#主持人踢人)：

```json
{
  "room_no": "021890611",
  "target_id": "_agent_co63jg6g54hu3b0xhtie",
  "join_disabled": true
}
```

+ `target_id`：人员填用户 ID；设备填它在会中的用户 ID，以 `_agent_` 开头，从[会中人员列表](/zh/meeting/server-api/meet#查询会中人员列表)或 `user_enter` 回调拿
+ `join_disabled=true`：拉黑，本场会议不能再进；`remove_conferee=true`：同时从参会人员里移除
+ 目标已不在会中时直接返回成功

## 邀请失败怎么知道

### 人员

| 情况 | 怎么判断 |
| --- | --- |
| 不在线，收不到呼叫 | `call-users` 返回的 `offline_user_ids` |
| 收到了但没接、拒接，或强制入会失败 | 呼叫后 **60 秒内没收到该用户的 `user_enter` 回调** |

### 设备

订阅 [`device_invite_failed` 回调](/zh/meeting/server-api/guides/callbacks#device_invite_failed-—-设备邀请失败)：终端忙、拒接、无应答、呼不通、拉流失败、入会被拒时推送，
带失败原因 `reason` 与原始说明 `msg`。

<Warning>
  这个回调需要三方面都就位才会推送：

  + **设备网关新版本**：老版本的设备网关不上报邀请失败
  + **部署方开启**：在 SMeeting 服务端配置的 `rtc.callback_events` 里追加 `agent_invite_failed`（默认不开）
  + **你订阅**：[设置事件通知](/zh/meeting/server-api/meet#设置事件通知)时 `events` 里带上 `device_invite_failed`

  只对平台邀请的设备推送，设备自己呼入失败不推。
</Warning>

## 限制

+ **App 不在线拉不进来**：人员必须登录着某一端（即时通讯在线）才能收到呼叫，强制入会也一样；不在线的人列在 `offline_user_ids` 里
+ **手机 App 在后台时**：系统允许时直接拉到前台入会；不允许时只能先弹本地通知，用户 60 秒内点通知或回到前台才入会，超过 60 秒丢弃这次呼叫
+ **自己用 SDK 做界面的**：上面「强制入会」的行为是我们 App 的处理，SDK 只把标记带给你。要在收到呼叫事件时自行读取 `force_join`，
  按上面的方式处理（不弹来电、先退出当前会议再入会）；不处理的话，强制呼叫在你的 App 里就和普通呼叫一样。各端从以下版本起能拿到这个字段：

| 端 | 版本 | 字段 |
| --- | --- | --- |
| Web | 0.2.0 起 | `call_calling` 事件的 `content.force_join`，见[事件](/zh/meeting/web/events#会外消息事件) |
| Android | 2.0.37 起 | `ImContent.CallingMsg.forceJoin`，见[类型](/zh/meeting/android/types#imcontent-callingmsg) |
| iOS（Objective-C） | 2.5.0 起 | `onCallReceived:nickname:roomNo:title:meetingId:forceJoin:`，见[MeetingKitIMDelegate](/zh/meeting/ios/api-reference/MeetingKitIMDelegate#oncallreceivednicknameroomnotitlemeetingidforcejoin) |
| Swift | 1.13.0 起 | `ImCallContent.forceJoin`，见[会议外消息](/zh/meeting/swift/advanced/im#有人呼叫你) |
| 鸿蒙 | 1.9.0 起 | `ImCallContent.forceJoin`，见[IM 与呼叫](/zh/meeting/harmony/advanced/im#被呼叫入会) |
| Windows | 暂不支持 | — |
