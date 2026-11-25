---
title: "回调事件接入指南"
description: "会议、成员、录制状态变化时 SMeeting 通知你的业务后端：怎么接、怎么验签、每个事件的字段结构"
---

回调让你的业务后端在不轮询的前提下感知会议侧的变化。注册地址用[设置事件通知](/zh/meeting/server-api/meet#设置事件通知)，
所有事件皆可不订阅，**未订阅的事件不会推送**。

## 请求形态

我们向你注册的 `cb_url` 发 POST 请求，事件名同时出现在查询参数与请求体里：

```text
POST {你的 cb_url}?event=user_enter
Content-Type: application/json; charset=utf-8
```

```json
{
  "app_id": "68b3ft51smhz0x5glscw9whm78bw57uu",
  "time": 1718250917,
  "event": "user_enter",
  "data": { "meeting_id": "sny038", "room_no": "803707296", "user_id": "1001" }
}
```

各事件的差异只在 `data`，外层三个字段恒定。`time` 是事件发生的秒级时间戳。

## 验签（务必做）

回调请求头带的签名**与调用服务端 API 时的算法完全一致**（见[概览](/zh/meeting/server-api/overview)），
只是方向相反：这次是我们用你的 `app_key` 签名，你来验。请求头为 `app_id` / `nonce` / `timestamp` / `signature`。

不验签意味着任何人只要知道你的回调地址就能伪造事件，**请不要跳过这一步**。

## 应答要求

+ HTTP 状态码必须为 `200`
+ 响应体必须是标准 JSON：`{"code": 0}`
+ 我们的请求超时为 **10 秒**，你的处理逻辑要在此之内返回（重活请异步化）

返回非 200、返回体不是 JSON、或 `code` 非 0，都会被记为一次失败。

## 事件一览

| 事件 | 何时触发 |
| --- | --- |
| `user_enter` | 用户进入会议 |
| `user_exit` | 用户离开会议 |
| `meeting_status_change` | 会议状态变化（未开始 / 进行中 / 已结束之间流转）|
| `mcu_status_change` | 录制或合流任务的状态变化 |
| `mcu_record_done` | 一个录像文件已就绪，可以取播放地址了（一次录制多个文件时推多条） |
| `mcu_alarm` | 录制任务出现异常，或推流任务持续失败 |
| `user_mic_state_change` | 用户打开或关闭麦克风 |
| `user_camera_state_change` | 用户打开或关闭摄像头 |
| `user_extra_screen_state_change` | 用户开始或停止推送额外屏幕（客户端推送的副屏） |
| `share_state_change` | 会议的共享状态变化（开始共享 / 结束共享） |
| `user_online` | 用户上线：真人客户端连上 IM，或设备（SIP / H.323 终端、国标监控）注册到设备网关，与是否在会无关 |
| `user_offline` | 用户下线：真人客户端 IM 断开，或设备注销 / 心跳超时 / 探测不可达，与是否在会无关 |

### `user_enter` — 用户进入会议

```json
{
  "meeting_id": "sny038",
  "room_no": "803707296",
  "user_id": "1001",
  "real_name": "张三",
  "nickname": "张三",
  "role": 1
}
```

`role`：`0` 普通成员、`1` 主持人、`2` 联席主持人。

同一个 `user_id` 在多端进会时，每一端都会触发一次。

### `user_exit` — 用户离开会议

比 `user_enter` 多两个字段：

```json
{ "meeting_id": "sny038", "user_id": "1001", "reason": 1, "online": 3 }
```

+ `reason`：`1` 主动离开、`2` 被踢、`3` 被顶号、`4` 心跳超时、`5` 会议销毁、`6` 身份变成观众、`7` 设备异常断开
+ `7` 只出现在经设备网关入会的 SIP / H323 终端上：终端信令或媒体超时、网络中断等**非正常挂断**；
  终端正常挂断仍是 `1`。据此可区分会议室终端是正常挂断还是异常掉线
+ `online` 是该用户离开**后**会中的在线人数，`0` 意味着人走空了

用 `online == 0` 判断「会议实际空了」比自己维护计数可靠。

### `meeting_status_change` — 会议状态变化

```json
{ "meeting_id": "sny038", "room_no": "803707296", "from_status": 1, "to_status": 2 }
```

状态取值：`1` 未开始、`2` 进行中、`3` 已结束。带上 `from_status` 是为了让你能区分
「正常开始」（1→2）与「异常重开」这类情况。

### `mcu_status_change` — 录制任务状态变化

```json
{
  "meeting_id": "sny038",
  "task_id": "sxjgwy",
  "task_type": 1,
  "task_status": 1,
  "err_desc": "",
  "began_at": 1718250917,
  "ended_at": 0,
  "record_count": 0,
  "total_duration": 0,
  "total_size": 0
}
```

+ `task_type` 按位组合，取值见[云录制与合流接入指南](/zh/meeting/server-api/guides/recording)
+ `task_status`：`0` 待开始、`1` 进行中、`2` 待结束、`3` 异常结束、`4` 正常结束
+ `err_desc` 只在 `task_status=3` 时有内容
+ `record_count` / `total_duration` / `total_size` 是本次录制产出的文件数、总时长（秒）、总字节

`0` 和 `2` 是过渡状态，业务侧一般只需要关心 `1`（开始了）、`3`（出错了）、`4`（结束了）。

**任务结束时这条事件里的 `record_count` 往往还是 0**：录像文件要等任务结束后才开始转码上传。
全部文件传完后会**再补发一条本事件**，那一条的计数才完整。

### `mcu_record_done` — 一个录像文件已就绪

```json
{
  "meeting_id": "sny038",
  "task_id": "sxjgwy",
  "record_id": "rc3p9w",
  "seq": 2,
  "is_last": false,
  "task_type": 1,
  "vod_size": 481920000,
  "duration": 3600,
  "offset_ms": 3600000,
  "began_at": 1718254517,
  "ended_at": 1718258117,
  "reason": 1
}
```

**这个事件才是取回放地址的正确时机。** 任务 `task_status` 变成 `4`（正常结束）时文件
往往还在转码上传，此时取地址可能拿不到东西。

**一场会议的一次录制会产出多个文件，本事件按文件推送。** 录制超过分片上限（默认 1 小时）
会按时长切段，录制中途中断后被续上也会另起一段。因此：

+ **取播放地址用 `record_id`，不是 `task_id`**，见[单个录像文件的点播地址](/zh/meeting/server-api/mcu#单个录像文件的点播地址)
+ `seq` 从 1 开始，按它排序即播放顺序；`offset_ms` 是相对整场录制开始的偏移（毫秒），做连播用
+ `reason`：`1` 按时长切段、`2` 中断后续录（**与上一片之间有时间空洞**）、`3` 结束收尾、`0` 未知
+ `is_last` 为 `true` 表示本次录制的文件已全部就绪

`duration` 是本片时长（秒），`vod_size` 是本片字节数。

<Tip>
  想一次拿到一场会议的全部可播地址，用
  [一场会议全部录像的点播地址](/zh/meeting/server-api/mcu#一场会议全部录像的点播地址)，
  它会把每一段都返回，按分片序号排好。
</Tip>

### `mcu_alarm` — 录制任务异常

```json
{
  "meeting_id": "sny038",
  "task_id": "sxjgwy",
  "title": "周会",
  "task_type": 1,
  "task_status": 1,
  "gw": "mcu-gw-01",
  "alarm_at": 1718250917,
  "alarm_brief": "推流中断"
}
```

`gw` 是任务所在的网关节点，排查时告诉我们这个值能快很多。注意告警**不代表任务已终止** ——
以 `mcu_status_change` 的 `task_status` 为准。

**推流任务持续失败也走这个事件**：`task_type` 为 `0` 表示推流告警，此时 `task_id` 是推流任务的 `push_id`，
不是录制任务，不要拿去调 `mcu/*` 接口；推流是否恢复以[推流任务列表](/zh/meeting/server-api/stream#推流任务列表)的 `status` 为准。
见[媒体输出接入指南](/zh/meeting/server-api/guides/media-output)。

### `user_mic_state_change` / `user_camera_state_change` / `user_extra_screen_state_change` — 用户媒体状态变化

三个事件共用同一个结构，按事件名看对应的状态字段，其余两个状态是推送时刻的快照：

```json
{
  "meeting_id": "sny038",
  "room_no": "803707296",
  "user_id": "1001",
  "real_name": "张三",
  "nickname": "张三",
  "avatar": "https://example.com/a.png",
  "role": 1,
  "device_type": 6,
  "join_at": 1718250900,
  "mic_state": 1,
  "camera_state": 2,
  "extra_screen_state": 2,
  "ts_ms": 1718250917123
}
```

+ `mic_state` / `camera_state` / `extra_screen_state`：`1` 开、`2` 关，取值与[会中人员列表](/zh/meeting/server-api/meet#查询会中人员列表)一致
+ 只在开关真正变化时推送：摄像头的大流、小流任一在发布都算开着，两路一起出现只推一次
+ 「额外屏幕」指客户端推送的额外屏幕（副屏，如远程评标场景每人常驻的第二路画面），每人各推各的、常驻，与会议共享（`share_state_change`）互不影响
+ SIP/H.323 终端的辅流共享不走本事件，它作为会议共享由 `share_state_change` 体现
+ 一次操作同时开关多个媒体时（例如进会同时开麦和摄像头），会分别推送，`ts_ms` 相同
+ 用户离会时**不再补发**关闭事件，以 `user_exit` 视为全部关闭
+ 状态以「是否在发布」为准：只在本地静音、仍在发布的麦克风不会触发关闭

### `share_state_change` — 会议共享状态变化

开始共享和结束共享都是这个事件，屏幕共享和白板共享都会推送：

```json
{
  "meeting_id": "sny038",
  "room_no": "803707296",
  "from_state": 0,
  "to_state": 1,
  "user_id": "1001",
  "nickname": "张三",
  "ts_ms": 1718250917123
}
```

+ `from_state` / `to_state`：`0` 无共享、`1` 屏幕、`2` 白板。`0→1/2` 是开始，`1/2→0` 是结束，`1↔2` 是切换共享类型
+ `user_id` 是开始或结束共享的那个人；结束时为原共享者
+ 共享者自己结束、主持人结束、主持人禁止共享、共享者离会，都会推送结束
+ 新共享者接管已掉线者的共享时，先推一条原共享者的结束，再推一条新共享者的开始
+ 申请到共享就推送「开始」，不等客户端真正推出屏幕画面
+ SIP/H.323 终端的辅流共享也是会议共享：终端本地按共享键发起时推送本事件（平台不能远程开启这类终端的共享），`user_id` 为该设备

### `user_online` / `user_offline` — 用户上线 / 下线

感知**会议外**的在线状态，真人和设备共用一个事件，用 `is_agent` 区分（进出会议看 `user_enter` / `user_exit`）。

本事件需要部署方开启后才会推送，需要时请联系我们。

真人上线：

```json
{ "user_id": "1001", "is_agent": false, "device_type": 3, "device_id": "aacc", "sid": "co63jg6g54hu3b0xhtie", "name": "", "contact": "" }
```

设备上线：

```json
{ "user_id": "_agent_sz8nk8", "is_agent": true, "device_type": 84, "device_id": "sz8nk8", "sid": "", "name": "大门监控", "contact": "34020000001320000001" }
```

`user_offline` 多两个字段：

```json
{ "user_id": "_agent_sz8nk8", "is_agent": true, "device_type": 84, "device_id": "sz8nk8", "sid": "", "name": "大门监控", "contact": "34020000001320000001", "reason": 4, "heartbeat_at": 1718250917 }
```

+ `is_agent`：`false` 真人，`true` 设备
+ `user_id`：真人为你的用户 ID；设备为 `_agent_` + 设备 ID，与设备入会后 `user_enter` 里的 `user_id` 一致
+ `device_type`：真人为 `1` Windows、`2` Android、`3` iOS、`4` Linux、`5` macOS、`6` WebRTC、`7` 微信小程序、`8` 鸿蒙；
  设备为 `82` SIP、`83` H323、`84` GB28181 监控
+ 真人**按端推送**：同一个 `user_id` 在多端登录时每一端各推一次，用 `sid` 区分是哪一端；要判断「这个人还在不在线」，
  请自己按 `user_id` 汇总各端状态
+ 设备按状态翻转只推一次，`name` / `contact` 只对设备有值（`contact` 为 SIP 用户名、H323 短号码、国标设备编号或 IP 直连地址）
+ `reason`：`1` 主动断开（设备为主动注销）、`2` 被踢、`3` 被顶号、`4` 心跳超时、`7` 探测不可达（仅 IP 直连设备）
+ `heartbeat_at` 只对设备有值，是最后一次心跳时间：心跳超时的离线**比真实断线晚 5~7 分钟**才推送，需要真实断线时刻时以它为准
+ 设备不归属某个应用，订阅了本事件的每个应用都会收到

## 幂等与重试

网络抖动可能导致同一事件送达多次，业务侧请按 `event` + 业务主键（`meeting_id`、`task_id`、
`user_id`）做幂等。不要用 `time` 去重 —— 同一秒内可以有多个同类事件。

媒体状态与共享状态事件不保证到达顺序（例如快速开关麦克风时，「关」可能先于「开」到达）。
请以 `ts_ms`（毫秒）最大的一条为准；三个媒体状态字段是推送时刻的完整快照，直接覆盖即可。
