---
title: "设备列表"
examples:
  type: [2, 4]
  keyword: 会议室
  page: 1
  per-page: 10
descriptions:
  type: 设备类型列表，2 SIP、3 H323、4 GB28181、5 RTSP
---

分页查询可邀请的设备列表，通常用于在你的界面上给用户挑设备。

+ `type` 必填且为数组，按类型筛选：`2` SIP、`3` H323、`4` GB28181、`5` RTSP
+ `keyword` 模糊匹配显示名与设备标识；也可用 `name` / `contact` 精确筛选
+ 国标设备的每个**通道**会各占一条，`contact` 是通道编号

响应里的 `contact`（设备标识）就是「邀请设备入会」要传的值。
