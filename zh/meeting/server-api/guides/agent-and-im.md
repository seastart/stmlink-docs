---
title: "设备接入与 IM"
description: "SMeeting 的设备接入与 IM 接口直接沿用 SRTC 的同名接口，本页说明怎么调"
---

SIP / H323 / GB28181 等设备的接入，以及会议外的 IM 消息，SMeeting 没有另做一套 ——
请求会原样转发给底层的 SRTC，参数与返回结构完全一致。

所以这两类接口的文档就是 SRTC 那两页：

<Columns cols={2}>
  <Card title="设备接入" href="/zh/rtc/server-api/agent">
    设备的增删改查、网关列表、邀请入会、会中开关设备音视频、切换设备画面
  </Card>
  <Card title="IM 消息" href="/zh/rtc/server-api/im">
    会议外的即时消息、IM 授权与设备在线管理
  </Card>
</Columns>

### 调用时的两点差别

**域名用 SMeeting 的**。接口路径（`/server/v1/agent/...`、`/server/v1/im/...`）和参数
都不变，只是发给 SMeeting 的地址，不用再单独对接 SRTC 的域名。

**签名也用 SMeeting 的 app_id / app_key**，签名方法见[概览](/zh/meeting/server-api/overview)。
转发时鉴权已经在 SMeeting 这一层做完了。

### 设备入会时目标房间填什么

邀请设备入会（`/server/v1/agent/invite`）的 `no` 参数，在 SMeeting 里**填会议房间号 `room_no`**，
不是 `meeting_id`。设备入会时 SMeeting 按房间号找到该房间当前的这一场会议，再把设备拉进去；
填 `meeting_id` 会因为找不到会议而入会失败。

```json
{
  "agents": [
    { "type": 4, "contact": "37070000082008000001:34020000001320000001" }
  ],
  "no": "021890611"
}
```

`agents` 里每台设备的 `type` 与 `contact` 从[设备列表](/zh/rtc/server-api/agent)取，国标设备的
`contact` 格式是 `设备编号:通道编号`，各字段说明见[邀请设备入会](/zh/rtc/server-api/agent#邀请设备入会)。

每台设备还可以带四个可选开关，决定入会后先发什么、放不放会议声音：`camera_enabled`（发摄像头画面，默认 `true`）、
`mic_enabled`（设备麦克风的声音进会，默认 `true`）、`share_enabled`（直接共享画面，默认 `false`）、
`speaker_enabled`（会议声音从设备喇叭放出，SIP/H.323 默认 `true`，国标默认取设备网关配置、一般为 `false`）。

+ 它们**仍受会议的禁止策略约束**：会议禁了摄像头 / 麦克风 / 共享，传 `true` 也开不了
+ `share_enabled` 只对 RTSP / 国标等拉流设备生效：入会时按会议的共享互斥规则申请共享，放行则主画面作为共享发布；**被拒（如已有人在共享）则退回作为普通摄像头画面**
+ SIP/H.323 设备不支持 `share_enabled: true`：只要有一台这样传，整个邀请返回错误码 `1037`。终端要共享请在终端上按共享键
+ `speaker_enabled` 与 `mic_enabled` 成对，一个管下行一个管上行：SIP/H.323 传 `false` 时终端听不到会议声音；国标传 `true` 时设备网关向设备发起 GB28181 语音广播（需网关开启广播、设备支持并接了喇叭 / 音柱）；RTSP 等拉流设备忽略。详见 SRTC [设备接入指南的「设备喇叭」](/zh/rtc/server-api/guides/agents#设备喇叭)
+ 会中再开关设备喇叭，直接调 SRTC 的[开关设备喇叭](/zh/rtc/server-api/agent#开关设备喇叭)（与开关设备音视频一样经 SMeeting 转发，`channel` / `uid` 填法见下节）

### 会中操作设备时频道和用户 ID 填什么

开关设备音视频与喇叭、发按键、[切换设备看到的画面](/zh/rtc/server-api/agent#切换设备看到的画面)这几个接口
针对的是已经在会里的设备，参数里的 `channel` 在 SMeeting 里**填会议 ID `meeting_id`**（不是房间号），
`uid` 填设备在会中的用户 ID（带 `_agent_` 前缀，从参会人列表或成员入会回调拿）。

切换设备画面时，`sub_uid` 直接填要看的那位参会人的 `user_id`：

```json
{
  "channel": "<meeting_id>",
  "uid": "_agent_co63jg6g54hu3b0xhtie",
  "sub_uid": "1001",
  "sub_tdesc": "camera_big"
}
```

### 让设备共享画面

在 SMeeting 里让设备共享，请用会议层的[主持人请求用户共享](/zh/meeting/server-api/meet-admin#主持人请求用户共享)，
`target_id` 填设备在会中的用户 ID：

+ 只适用于 RTSP / 国标等**拉流设备**（只有一路画面）：设备无需确认，服务端直接让它开始共享，主画面**切成**共享，摄像头画面随之撤下；结束共享后切回摄像头画面
+ **SIP/H.323 终端不支持远程开启共享**，目标是这类终端时返回错误码 `2126`。终端要共享请在终端上按共享键发辅流（摄像头画面照旧），同样作为会议共享
+ 它和普通成员的共享互斥（已有人在共享返回 `2104`），共享状态、`share_state_change` 回调都会照常更新
+ 结束用[主持人结束共享](/zh/meeting/server-api/meet-admin#主持人结束共享)，会同时让设备停止发送共享画面

不要直接调 SRTC 的[开关设备共享](/zh/rtc/server-api/agent#开关设备共享)：它只让设备发出 / 撤销画面，不做互斥，
也不会更新会议的共享状态。终端本地按共享键发起的共享、拉流设备带 `share_enabled` 入会时的共享，
SMeeting 都会自动按同样的互斥规则放行或拒绝，无需你处理。
