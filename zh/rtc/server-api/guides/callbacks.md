---
title: "回调事件接入指南"
description: "RTC 侧在频道/用户/录制状态变化时通知你的业务后端：怎么接、怎么验签、每个事件的字段结构"
---

回调让你的业务后端在不轮询的前提下感知 RTC 侧的变化。注册地址用[设置回调](/zh/rtc/server-api/channel#设置回调)，
所有事件皆可不订阅，**未订阅的事件不会推送**。

## 请求形态

我们向你注册的 `cb_url` 发 POST 请求，事件名同时出现在查询参数与请求体里：

```text
POST {你的 cb_url}?event=user_join
Content-Type: application/json; charset=utf-8
```

```json
{
  "app_id": "68b3ft51smhz0x5glscw9whm78bw57uu",
  "time": 1718250917,
  "event": "user_join",
  "data": { "channel": "fire", "uid": "1001" }
}
```

各事件的差异只在 `data`，外层三个字段恒定。`time` 是事件发生的秒级时间戳。

## 验签（务必做）

回调请求头带的签名**与调用 srvapi 时的签名算法完全一致**（见[概览](/zh/rtc/server-api/overview)），
只是方向相反：这次是我们用你的 `app_key` 签名，你来验。请求头为 `app_id` / `nonce` / `timestamp` / `signature`。

不验签意味着任何人只要知道你的回调地址就能伪造事件，**请不要跳过这一步**。

## 应答要求

+ HTTP 状态码必须为 `200`
+ 响应体必须是标准 JSON：`{"code": 0}`
+ 我们的请求超时为 **5 秒**，你的处理逻辑要在此之内返回（重活请异步化）

失败的判定与后果分两类：

| | 异步通知事件 | 同步调用事件 |
| --- | --- | --- |
| 你返回非 200 / 非 JSON / `code` 非 0 | 最多重试 5 次后放弃 | **本次操作被拒绝** |
| 用途 | 让你知道发生了什么 | 由你决定允不允许、补充数据 |

只有 `agent_join` 与 `agent_operate` 是同步调用，其余都是异步通知。

## 异步通知事件

### `channel_open` — 频道打开

```json
{ "channel": "fire" }
```

### `channel_destroy` — 频道销毁

```json
{ "channel": "fire", "reason": 2 }
```

`reason`：`1` 主动销毁（调了销毁接口）、`2` 在线人数为 0 自动销毁。

### `user_join` — 用户进入频道

```json
{ "channel": "fire", "uid": "1001" }
```

### `user_leave` — 用户离开频道

```json
{ "channel": "fire", "uid": "1001", "reason": 1, "online": 3 }
```

+ `reason`：`1` 主动离开、`2` 被踢、`3` 被顶号、`4` 心跳超时、`5` 频道销毁、`6` 身份变成观众
+ `online` 是该用户离开**后**会中的在线人数，`0` 意味着人走空了

### `im_connect` / `im_disconnect` — IM 设备上线 / 下线

```json
{ "uid": "1001", "sid": "co63jg6g54hu3b0xhtie", "device_type": 3, "device_id": "aacc" }
```

`im_disconnect` 多一个 `reason`，取值同 `user_leave`。

`device_type`：`0` 未知、`1` Windows、`2` Android、`3` iOS、`4` Linux、`5` macOS、`6` WebRTC、`7` 微信小程序。
`80` 起是服务端代理入会的号段（`81` MCU、`82` SIP、`83` H323、`84` GB28181、`85` RTSP、`86` RTMP、`87` 文件播放、`88` 流分发、`89` 语音转写）。

### `mcu_task` — 录制/合流/直播任务状态变化

```json
{
  "channel": "fire",
  "task_id": "sxjgwy",
  "task_type": 9,
  "task_status": 1,
  "err_desc": "",
  "began_at": 1718250917,
  "ended_at": 0,
  "record_count": 0,
  "total_duration": 0,
  "total_size": 0
}
```

+ `task_type` 按位组合，含义见[云录制与直播接入指南](/zh/rtc/server-api/guides/recording)
+ `task_status`：`0` 待开始、`1` 进行中、`2` 待结束、`3` 异常结束、`4` 正常结束
+ `err_desc` 仅在异常结束时有内容
+ `record_count` / `total_duration` / `total_size` 是本次录制产出的文件数、总时长（秒）、总字节

这是判断"录制到底跑起来没有"最可靠的信号——比启动接口返回成功更有意义。

**任务结束时这条事件里的 `record_count` 往往还是 0**：录像文件要等任务结束后才开始转码上传。
全部文件传完后我们会**再补发一条本事件**，那一条里的计数才是完整的，用它对账。

### `mcu_record` — 一个录像文件已完成

```json
{
  "channel": "fire",
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

**一次录制会产出多个文件，本事件按文件推送，一次任务推多条。** 两种情况会切出新文件：

+ 录制时长超过分片上限（默认 1 小时），转码时按时长滚动切段，片间时间连续
+ 录制中途底层因 30 秒无音视频流自动停止、随后被重新拉起，另起一段，**片间存在时间空洞**

所以：

+ **取播放地址必须用 `record_id`，不是 `task_id`** —— `task_id` 是任务的，一次任务下有多个
  `record_id`。调[获取录像文件播放地址](/zh/rtc/server-api/mcu#获取单个录像文件的播放地址)时传它
+ `seq` 从 1 开始，按它排序就是播放顺序
+ `offset_ms` 是这一片相对整场录制开始的偏移（毫秒），做多片连播的进度轴用它；
  `began_at`/`ended_at` 是墙钟时间，用来跟你自己业务的时间线对齐
+ `reason`：`1` 按时长切段、`2` 中断后续录（**与上一片之间有空洞**，连播会跳变，UI 上值得提示）、
  `3` 任务结束收尾、`0` 未知
+ `is_last` 为 `true` 表示本次录制的文件已全部产出，可以开始拼完整回放了

`vod_size` 单位字节，`duration` 单位秒。

<Tip>
  想一次拿到整场录制的全部可播地址，直接调
  [录像任务详情](/zh/rtc/server-api/mcu#录像任务详情)——它的 `records` 数组里
  每一段都带好了播放地址，比逐条取省事。
</Tip>

### `mcu_alarm` — 录制任务告警

```json
{
  "task_id": "sxjgwy",
  "task_type": 1,
  "task_status": 3,
  "channel": "fire",
  "title": "项目周会 2024-06-12",
  "room_no": "818595664",
  "gw": "mcu-gw-01",
  "alarm_at": 1718250917,
  "alarm_brief": "任务异常结束"
}
```

用于接你自己的告警系统。录制是持续计费的能力，异常中断如果没人知道，损失的是录像本身。

### `talkrec_task` — 语音录制任务状态变化

```json
{
  "channel": "fire",
  "task_id": "tk8kjx",
  "task_status": 1,
  "err_desc": ""
}
```

`task_status`：`0` 待开始、`1` 进行中、`3` 异常结束、`4` 正常结束（没有 mcu 的「待结束」态）。

语音录制的启动是异步的——调用接口只表示已受理，录音网关入会成功后才转为进行中，
所以这个事件是判断「录音到底跑起来没有」最可靠的信号。

### `talkrec_record` — 一段录音完成

```json
{
  "channel": "fire",
  "task_id": "tk8kjx",
  "record_id": "rc3p9w",
  "uid": "1001",
  "name": "张三",
  "vod_key": "talkrec/2024/06/12/rc3p9w.mp3",
  "vod_size": 51200,
  "duration_ms": 4200,
  "began_at": 1718250917,
  "ended_at": 1718250921,
  "end_reason": 1
}
```

与录像不同，语音录制**每闭合一段就回调一次**，一次任务会推很多条——按说话人分轨、
一次讲话一段。这是做实时字幕、对讲留痕、按人计时的数据源。

+ `record_id` 是取播放地址时用的段 ID，不是 `task_id`
+ `duration_ms` 单位毫秒（段通常只有几秒，秒级精度不够）
+ `end_reason` 闭段原因：`0` 未知、`1` 正常松手、`2` 超时切段、`3` 用户离开、`4` 任务停止、`5` 空闲兜底

`end_reason` 值得留意：`2` 说明这段被时长上限截断了（同一次讲话会拆成多段），
`5` 是服务端兜底闭段，频繁出现意味着静音判定没能正常收尾，值得查一下音频质量。

## 同步调用事件

这两个事件我们**等你的回答**再继续，因此你的处理必须快（5 秒超时）。

### `agent_join` — 设备请求进入频道

```json
{
  "type": 4,
  "no": "818595664",
  "is_audience": false,
  "uid": "gb_34020000001320000001",
  "name": "大门监控",
  "net": "内网",
  "sg": "",
  "extend_info": "{\"gw\":\"devgate-1\"}"
}
```

`type` 是代理类型：`1` MCU、`2` SIP、`3` H323、`4` GB28181 监控、`5` RTSP 拉流、`6` RTMP 拉流、`7` 文件播放、`8` 流分发、`9` 语音转写。
`no` 是设备要进入的目标房间号（你自己业务的会议号）。

你需要把它换成一个会话：用 `no` 找到对应频道，调[获取加入频道token](/zh/rtc/server-api/channel#获取加入频道token)拿到 `sid`，然后原样回给我们：

```json
{"code": 0, "data": "_agent_co63jg6g54hu3b0xhtie"}
```

返回 `code` 非 0 即拒绝该设备入会。若你的用户详情不需要扩展 `props`，且设备无条件可信，可以不订阅本事件。

<Warning>
  调[获取加入频道token](/zh/rtc/server-api/channel#获取加入频道token)时，**必须把本回调里收到的
  `extend_info` 原样放进该接口的 `props` 参数**（键名就用 `extend_info`，值是收到的那个字符串，
  不要解析改写）：

  ```json
  {
    "channel": "fire",
    "uid": "gb_34020000001320000001",
    "props": {
      "extend_info": "{\"gw\":\"devgate-1\"}",
      "其它你自己的字段": "……"
    }
  }
  ```

  这个字段里带着设备所属的网关标识，我们靠它把会中的设备关联回网关。**丢了它，这些依赖反向
  通知网关的能力会静默失效**：[踢人](/zh/rtc/server-api/channel#踢人)对设备不生效（设备会被网关
  当成断线，随后自动重新入会）、[开关设备视频](/zh/rtc/server-api/agent#开关设备视频)与
  [开关设备音频](/zh/rtc/server-api/agent#开关设备音频)调用失败。你自己的 `props` 字段照常放，
  二者不冲突。
</Warning>

### `agent_operate` — 会中设备被操作（开关麦、开关摄像头）

```json
{
  "channel": "fire",
  "uid": "gb_34020000001320000001",
  "by_admin": true,
  "op_uid": "1001",
  "op_type": "camera"
}
```

返回 `code` 非 0 即拒绝这次操作。不订阅本事件时自动同意所有设备的流媒体操作。

## 幂等与顺序

回调是**至少一次**投递，不保证顺序也不保证不重复：

+ 重试会带来重复投递，业务侧要按 `channel` + `uid` + `time` 之类的组合做幂等
+ 网络与队列会打乱顺序，不要依赖"先收到 join 再收到 leave"来维护状态机；需要权威状态时以查询接口为准
