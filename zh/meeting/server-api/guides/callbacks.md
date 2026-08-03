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
| `mcu_status_change` | 录制、合流或直播任务的状态变化 |
| `mcu_record_done` | 录像文件转码完成，可以取播放地址了 |
| `mcu_alarm` | 录制任务出现异常 |

### `user_enter` — 用户进入会议

```json
{
  "meeting_id": "sny038",
  "room_no": "803707296",
  "user_id": "1001",
  "account": "13345678903",
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

+ `reason`：`1` 主动离开、`2` 被踢、`3` 被顶号、`4` 心跳超时、`5` 会议销毁、`6` 身份变成观众
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
  "err_desc": ""
}
```

+ `task_type` 按位组合，取值见[云录制与直播接入指南](/zh/meeting/server-api/guides/recording)
+ `task_status`：`0` 待开始、`1` 进行中、`2` 待结束、`3` 异常结束、`4` 正常结束
+ `err_desc` 只在 `task_status=3` 时有内容

`0` 和 `2` 是过渡状态，业务侧一般只需要关心 `1`（开始了）、`3`（出错了）、`4`（结束了）。

### `mcu_record_done` — 录像转码完成

```json
{
  "meeting_id": "sny038",
  "task_id": "sxjgwy",
  "task_type": 1,
  "vod_key": "xxx/xxx.mp4",
  "vod_size": 10485760,
  "mcu_dur": 3600
}
```

**这个事件才是取回放地址的正确时机。** 任务 `task_status` 变成 `4`（正常结束）时转码
往往还没做完，此时调[录像播放地址](/zh/meeting/server-api/mcu#单个录像的点播地址)可能拿不到东西。

`mcu_dur` 是录像时长（秒），`vod_size` 是文件字节数。

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

## 幂等与重试

网络抖动可能导致同一事件送达多次，业务侧请按 `event` + 业务主键（`meeting_id`、`task_id`、
`user_id`）做幂等。不要用 `time` 去重 —— 同一秒内可以有多个同类事件。
