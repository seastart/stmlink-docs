---
title: "设备接入指南"
description: "SIP / H323 话机、国标监控、RTSP 流怎么登记进来，再拉进频道"
---

设备接入解决的是「不跑我们 SDK 的东西也要进会」：会议室里的 SIP 话机、墙上的国标摄像头、
一路 RTSP 流。它们由**设备网关**代理入会，在频道里表现为一个普通成员（`uid` 带 `_agent_` 前缀）。

单个接口的参数与返回结构见[设备接入](/zh/rtc/server-api/agent)。

## 三步接入

```
1. 拿网关            POST /server/v1/agent/list-gw?type=regsip   → gw
2. 登记设备          POST /server/v1/agent/create?type=regsip    → 设备 ID
3. 拉进频道          POST /server/v1/agent/invite                → 等 user_join 回调
```

设备不是直连 RTC，而是挂在某个网关上，由网关负责信令与媒体转换。所以**第 1 步不能跳过**——
`gw` 填错会导致设备无法上线。

## 六种接入方式

`type` 是 **URL 查询参数**（`?type=regsip`），不在请求体里。[新增设备](/zh/rtc/server-api/agent#新增设备)与
[修改设备](/zh/rtc/server-api/agent#修改设备)的请求体字段随它变化：

| `type` | 说明 | 特有必填字段 |
| --- | --- | --- |
| `ipsip` | SIP 话机，IP 直连 | `uri`（`ip:port`）|
| `regsip` | SIP 话机，注册模式 | `username`（不能含 `:`）、`auth_pwd` |
| `iph323` | H323 终端，IP 直连 | `uri`（`ip:port`）|
| `regh323` | H323 终端，注册模式 | `username`（**只能是数字短号**）、`auth_pwd` |
| `gb28181` | 国标监控设备 | `sip_no`（18–20 位数字）、`auth_pwd`，可选 `subjects` |
| `rtsp` | RTSP 拉流 | `uri`（必须以 `rtsp` 开头），可选 `transport_type`（`UDP` 默认 / `TCP`）|

所有方式都必填 `display_name`（显示名称）和 `gw`（设备网关），`remark` 可选。
`rtsp` 之外的方式还需要注意：注册模式要求设备主动向网关注册，IP 直连则由我们去连设备，
选哪种取决于设备所在网络能不能被我们访问到。

修改设备时 `type` **必须与设备登记时一致**，不能借此把 SIP 设备改成 RTSP；
要换接入方式请删除后重新登记。

## 国标设备的通道

一台国标设备（NVR、球机）下面可能挂多个摄像头通道，每个通道在会中是一路独立画面。
`subjects` 是「通道编号 → 通道名称」的键值对：

```json
{"50010700001320000001": "嘉宾席", "50010700001320000002": "观众席"}
```

三种维护方式，效果相同：

+ 登记设备时用 `subjects` 一次性批量传入
+ 之后用[设置国标设备的一个通道](/zh/rtc/server-api/agent#设置国标设备的一个通道)逐个添加或改名
+ 编号懒得自己拼 → 先调[生成国标设备的通道编号](/zh/rtc/server-api/agent#生成国标设备的通道编号)按规范生成，再登记

同理，设备本身的 `sip_no` 也可以用[生成国标设备的 SIP 编号](/zh/rtc/server-api/agent#生成国标设备的-sip-编号)拿到。
两个"生成"接口都**只返回编号、不落库**，拿到后还得自己去登记。

要让国标摄像头能注册上来，设备端得填"上级平台"信息（SIP 编号、域、IP、端口）——
这些值从[设备网关平台信息列表](/zh/rtc/server-api/agent#设备网关平台信息列表)取。

## 邀请与会中操作

[邀请设备入会](/zh/rtc/server-api/agent#邀请设备入会)的 `agents[].type` 与 `contact` 从
[设备列表](/zh/rtc/server-api/agent#设备列表)取；国标设备的每个通道各占一条，`contact` 就是通道编号。

**入会是异步的**：接口返回成功只表示邀请已下发，设备真正上线要等 `user_join` 回调。
如果你订阅了 `agent_join` 回调，还必须在回调里返回 `sid`，否则设备进不来——见[回调事件接入指南](/zh/rtc/server-api/guides/callbacks)。

设备不能自己开关麦克风和摄像头，只能由服务端下发：
[开关设备视频](/zh/rtc/server-api/agent#开关设备视频) / [开关设备音频](/zh/rtc/server-api/agent#开关设备音频)。
`uid` 用设备在频道里的用户 ID（带 `_agent_` 前缀，从成员列表或 `user_join` 回调拿），
不传 `uid` 则对该频道内所有设备生效。

订阅了 `agent_operate` 回调时，这两个操作会先征询你的业务后端，返回非 0 即拒绝。

## 设备类型编号

`list-invite` 与 `invite` 用的是数字类型，与 `type` 字符串不是一套：

| 数字 | 含义 | 对应的 `type` |
| --- | --- | --- |
| 2 | SIP | `ipsip` / `regsip` |
| 3 | H323 | `iph323` / `regh323` |
| 4 | GB28181 监控 | `gb28181` |
| 5 | RTSP 拉流 | `rtsp` |

会中成员的 `device_type` 是第三套编号（`80` 起的代理号段），见[回调事件接入指南](/zh/rtc/server-api/guides/callbacks)。
