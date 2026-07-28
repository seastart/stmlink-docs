---
examples:
  scene: ""
  events: ["user_join", "user_leave", "channel_destroy"]
  cb_url: https://your-domain.com/server/v1/callback/rtc
---

注册回调地址，RTC 侧在频道/用户状态变化时通知你的业务后端。所有事件皆可不订阅；未订阅的事件不会推送。

### 回调响应要求

+ HTTP 状态码必须为 `200`
+ 响应体为标准 JSON，示例：`{"code": 0}`
+ **异步通知事件**：若 `code` 不为 0，最多重试 5 次（间隔 10 秒）
+ **同步调用事件**：必须按业务要求回复，`code` 不为 0 表示拒绝本次操作

### 事件列表

`events` 字段可选的值如下。

**`im_connect`** — IM 设备上线（异步通知）

```json
{
  "uid": "string",        // 用户ID
  "sid": "string",        // 会话ID
  "device_type": 0,       // 设备类型
  "device_id": "string"   // 设备唯一ID
}
```

**`im_disconnect`** — IM 设备下线断开（异步通知）

```json
{
  "uid": "string",
  "sid": "string",
  "device_type": 0,
  "device_id": "string",
  "reason": 0             // 离开原因
}
```

**`user_join`** — 用户进入频道（异步通知）

```json
{
  "channel": "string",
  "uid": "string"
}
```

**`user_leave`** — 用户离开频道（异步通知）

```json
{
  "channel": "string",
  "uid": "string",
  "reason": 0,            // 离开原因
  "online": 0             // 离开后会中在线人数
}
```

**`channel_open`** — 频道打开（异步通知）

```json
{ "channel": "string" }
```

**`channel_destroy`** — 频道销毁（异步通知）

```json
{
  "channel": "string",
  "reason": 0             // 销毁原因
}
```

**`agent_join`** — 设备进入频道（**同步调用**）

若用户详情无需扩展 `props` 字段，且设备无条件可信，可以不订阅此事件。

```json
{
  "type": 0,               // 代理类型
  "no": "string",          // 目标房间号
  "is_audience": true,     // 是否观众
  "uid": "string",         // 设备的用户ID
  "name": "string",        // 频道中的昵称
  "net": "string",         // 网络线路
  "sg": "string",          // 服务分组
  "extend_info": "string"  // 扩展信息
}
```

须回复会话 ID，即调用「获取加入频道token」（`/server/v1/channel/grant`）后拿到的 `sid`：

```json
{"code": 0, "data": "_agent_co63jg6g54hu3b0xhtie"}
```

**`agent_operate`** — 会中设备操作（开关麦、开关摄像头）（**同步调用**）

不订阅此事件时，将自动同意设备的流媒体操作。

```json
{
  "channel": "string",   // 设备所在频道
  "uid": "string",       // 设备的用户ID
  "by_admin": true,      // 是否响应主持人操作
  "op_uid": "string",    // 主持人UID
  "op_type": "string"    // 子操作类型
}
```

回复的 `code` 不为 0 时将拒绝设备的流媒体操作。
