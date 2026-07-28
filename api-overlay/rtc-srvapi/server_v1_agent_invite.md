---
title: "邀请设备入会"
examples:
  no: fire
  agents: [{"type": 4, "contact": "50010700001320000001", "nickname": "嘉宾席摄像头"}]
descriptions:
  no: 目标房间号。RTC 层应用填频道名，Meeting 层应用填会议号
---

把设备拉进频道。可以一次邀请多台。

+ `agents[].type` 与 `contact` 从「设备列表」取；`nickname` 是会中显示名，留空则用设备的显示名
+ `no` 对 RTC 层应用就是频道名；如果你用的是 SMeeting 会议层，填会议号
+ 设备入会是**异步**的：本接口返回成功只表示邀请已下发，设备实际上线要等 `user_join` 回调（设备的 `uid` 带 `_agent_` 前缀）

设备侧接受邀请前会触发 `agent_join` 回调。若你订阅了该事件，需要按要求返回 `sid`，否则设备无法入会——详见「设置回调」。

邀请一个已在该频道的设备不会重复拉入。
