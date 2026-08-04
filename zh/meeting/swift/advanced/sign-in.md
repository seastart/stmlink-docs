---
title: "签到与点名"
description: "SMeeting Swift SDK 的会中签到活动创建、签到、统计查询，以及点名事件与应答"
---

### 签到

签到是一次带时限的活动：主持人发起，成员在时限内点一下签到，主持人可以随时查看统计和名单。活动用 `epoch`（轮次）区分，一场会议可以发起多轮。

#### 发起与结束

```swift
// 发起一轮签到
// dur 单位为分钟，这里是 30 分钟
try await meeting.signInCreate(dur: 30, desc: "上午场签到")

// 提前结束当前这一轮
try await meeting.signInFinish()
```

`dur` 是签到活动的持续时长，**单位为分钟**；活动的实际起止时间以下面事件和列表里的 `beginAt` / `endAt` 为准。

#### 成员签到

```swift
try await meeting.signInSign()
```

#### 查询

```swift
// 本场会议的所有签到活动，now 是服务端当前时间，可用来算剩余倒计时
let (list, now) = try await meeting.signInList()

// 某一轮已签到人数
let count = try await meeting.signInCount(epoch: epoch)

// 某一轮的签到名单，可按昵称过滤
let details = try await meeting.signInDetail(epoch: epoch, nickname: nil)
```

`SignInfo` 字段：`uid`（发起人）、`beginAt`、`dur`、`endAt`、`desc`、`nums`（已签到人数）。
`SignDetailInfo` 字段：`id`、`epoch`、`nickname`、`role`、`userId`、`createdAt`。

#### 签到事件

```swift
func meeting(_ meeting: SMeetingEngine, signInActivity data: SignInActivityEventData) {
    // data.hostId / data.hostName 发起人
    // data.epoch  轮次
    // data.beginAt / data.dur / data.endAt 起止与时长
    // data.desc   签到说明
}

func meeting(_ meeting: SMeetingEngine, signInDidFinish data: SignInFinishEventData) {
    // data.hostId / data.hostName / data.epoch
}
```

典型做法：收到 `signInActivity` 时弹出签到按钮并按 `endAt` 倒计时，收到 `signInDidFinish` 时收起。

---

### 点名

被点名时会收到事件：

```swift
func meeting(_ meeting: SMeetingEngine, rollCallNamed data: RollCallNamedEventData) {
    // data.id   点名记录中对应本成员的标识，应答时原样回传
    // data.sid  发起本次点名的主持人 uid
    // data.time 服务端当前时间
}
```

应答时**直接把事件里的 `id` 传回去**：

```swift
func meeting(_ meeting: SMeetingEngine, rollCallNamed data: RollCallNamedEventData) {
    Task {
        try await meeting.rollCallAnswer(rollCallUserId: data.id)
    }
}
```

<Warning>
不要用 `data.sid` 当参数 —— 它是发起点名的主持人 uid，不是点名记录标识。
</Warning>

> 当前 Swift SDK 只提供成员侧的点名应答能力。发起点名、查询点名详情属于主持人侧流程，需要通过服务端接口完成。
>
> 点名还需要服务端部署了该功能，未启用的环境调用会返回接口不存在。

---

### 相关页面

+ [主持人管控](/zh/meeting/swift/advanced/host-controls)
+ [事件参考](/zh/meeting/swift/events)
