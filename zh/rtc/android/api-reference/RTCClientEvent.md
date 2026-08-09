---
title: "RTCClientEvent"
description: "单频道会控事件：入会结果、成员与轨道变化、自定义消息、断开和重连；所有已归属事件均携带频道 ID"
---

`RTCClientEvent` 承载一条频道的会控事件。首次监听器必须通过 `RTCEngine.join(..., clientEvent, ...)` 传入；入会成功后可用 `RTCChannel.setRtcClientEvent(...)` 替换或解绑。

只关心少量事件时，建议继承提供空实现的 `RTCClientSimpleEvent`。

## 入会结果

### onJoinSucceed(channel, uid, whiteBoard)

```kotlin
fun onJoinSucceed(channel: String, uid: String, whiteBoard: String?)
```

自己加入频道成功。`channel` 为频道 ID，`uid` 为当前用户 ID，`whiteBoard` 为可空的白板地址或信息。应以本回调作为真正入会成功的依据。

### onJoinFailed(channel, statusCode)

```kotlin
fun onJoinFailed(channel: String?, statusCode: Int)
```

自己加入频道失败。能够从 token 解出频道 ID 时 `channel` 有值，否则为 `null`；`statusCode` 见 [错误码](/zh/rtc/android/error-codes)。

## 成员事件

### onUserUpdate(channel, uid)

```kotlin
fun onUserUpdate(channel: String, uid: String)
```

自己的用户信息更新。

### onMeMembershipChanged(channel, isMember)

```kotlin
fun onMeMembershipChanged(channel: String, isMember: Boolean)
```

自己的观众 / 正式成员身份发生变化。`isMember = true` 表示升级为正式成员，`false` 表示降为观众；入会初始身份通过对应频道的 `isAudience()` 读取。

### onRemoteUserJoin(channel, uid)

```kotlin
fun onRemoteUserJoin(channel: String, uid: String)
```

远端用户加入频道。

### onRemoteUserLeave(channel, userInfo, leaveReason)

```kotlin
fun onRemoteUserLeave(
    channel: String,
    userInfo: UserInfo,
    leaveReason: LeaveReason
)
```

远端用户离开频道。`userInfo` 是离会用户的最后一份信息快照。

### onRemoteUserUpdate(channel, uid)

```kotlin
fun onRemoteUserUpdate(channel: String, uid: String)
```

远端用户信息更新。

## Track 与频道事件

### onStreamTrackAdd(uid, channel, trackId, trackDesc)

```kotlin
fun onStreamTrackAdd(
    uid: String,
    channel: String,
    trackId: String,
    trackDesc: String
)
```

远端 Track 新增。应使用同一频道对应的 `RTCChannel` 获取和订阅远端 Track。

### onStreamTrackUpdate(uid, channel, trackId, trackDesc)

```kotlin
fun onStreamTrackUpdate(
    uid: String,
    channel: String,
    trackId: String,
    trackDesc: String
)
```

远端 Track 信息更新。

### onStreamTrackRemove(uid, channel, trackInfo)

```kotlin
fun onStreamTrackRemove(
    uid: String,
    channel: String,
    trackInfo: TrackInfo
)
```

远端 Track 移除。`TrackInfo` 字段见 [类型定义](/zh/rtc/android/types)。

### onChannelUpdate(channel, props)

```kotlin
fun onChannelUpdate(channel: String, props: String?)
```

频道扩展属性更新，`props` 可能为 `null`。

### onCustomMessage(channel, uid, sid, name, action, content)

```kotlin
fun onCustomMessage(
    channel: String,
    uid: String,
    sid: String,
    name: String,
    action: String,
    content: String
)
```

收到频道内自定义消息。`channel` 为消息所属频道，其他参数依次为发送者用户 ID、会话 ID、名称、动作标识和消息内容。

## 连接事件

### onDisconnected(channel, leaveReason, statusCode, message)

```kotlin
fun onDisconnected(
    channel: String,
    leaveReason: LeaveReason,
    statusCode: Int,
    message: String
)
```

频道发生不可恢复断连。该频道需要重新 `join(...)`；其他频道不受影响。

### onReconnected(channel)

```kotlin
fun onReconnected(channel: String)
```

频道断线重连成功。

### onReconnecting(channel)

```kotlin
fun onReconnecting(channel: String)
```

频道连接断开并开始自动重连。

:::note
原 `RTCClientEvent.onError(...)` 已移除。Engine 阻断操作或全局错误统一由 [`RTCEngineEvent.onError(...)`](/zh/rtc/android/api-reference/RTCEngineEvent) 返回。
:::
