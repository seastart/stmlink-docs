---
title: "设备接入与 IM"
description: "SMeeting 的设备接入与 IM 接口直接沿用 SRTC 的同名接口，本页说明怎么调"
---

SIP / H323 / GB28181 等设备的接入，以及会议外的 IM 消息，SMeeting 没有另做一套 ——
请求会原样转发给底层的 SRTC，参数与返回结构完全一致。

所以这两类接口的文档就是 SRTC 那两页：

<Columns cols={2}>
  <Card title="设备接入" href="/zh/rtc/server-api/agent">
    设备的增删改查、网关列表、邀请入会、会中开关设备音视频
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
