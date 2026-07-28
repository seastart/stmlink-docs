---
title: "开关设备视频"
examples:
  channel: fire
  uid: _agent_co63jg6g54hu3b0xhtie
  enabled: true
---

开关设备的摄像头。设备不像普通客户端那样能自己操作，只能由服务端下发。

`uid` 是设备在频道里的用户 ID（带 `_agent_` 前缀，从「在线/离线成员列表」或 `user_join` 回调拿）。

若你订阅了 `agent_operate` 回调，本次操作会先征询你的业务后端，返回非 0 表示拒绝。不订阅则默认允许。
