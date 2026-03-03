---
title: "RTCClientEvent"
description: "Android SRTC 音视频 SDK RTCClientEvent 接口参考"
---

会控事件监听接口

### onJoinSucceed()
自己加入频道成功回调

```kotlin
fun onJoinSucceed(channel: String, uid: String, whiteBoard: String?)
```kotlin

参数

| channel | String 类型，频道号 |
| --- | --- |
| uid | String 类型，用户 id |
| whiteBoard | String 类型， 电子白板地址 |


### onUserUpdate()
自己的信息更新回调

```kotlin
fun onUserUpdate(channel: String, uid: String)
```

参数

| channel | String 类型，频道号 |
| --- | --- |
| uid | String 类型，用户 id |


### onRemoteUserJoin()
远端用户加入频道回调

```kotlin
fun onRemoteUserJoin(channel: String, uid: String)
```kotlin

参数

| channel | String 类型，频道号 |
| --- | --- |
| uid | String 类型，用户 id |


### onRemoteUserLeave()
远端用户离开频道回调

```kotlin
fun onRemoteUserLeave(channel: String, userInfo: UserInfo, leaveReason: LeaveReason)
```

参数

| channel | String 类型，频道号 |
| --- | --- |
| userInfo | [UserInfo ](https://www.yuque.com/anyconf/rtcengine/linzbg#KHDlE)类型，用户信息 |
| leaveReason | LeaveReason 枚举类型，离开原因 |


LeaveReason 属性说明

| Error(-1) | 因为出错离开 |
| --- | --- |
| Unknown(0) | 原因未知 |
| VoluntarilyLeave(1) | 主动离开 |
| KickOut(2) | 被踢出 |
| BeReplaced(3) | 被顶号 |
| HeartbeatTimeout(4) | 心跳超时 |
| ChannelDestroy(5) | 频道销毁 |


### onRemoteUserUpdate()
用户信息更新回调

```kotlin
fun onRemoteUserUpdate(channel: String, uid: String)
```kotlin

参数

| channel | String 类型，频道号 |
| --- | --- |
| uid | String 类型，用户 id |


### onStreamTrackAdd()
码流增加回调

```kotlin
fun onStreamTrackAdd(uid: String, channel: String, trackId: String, trackDesc: String)
```

参数

| uid | String 类型，成员的 uid |
| --- | --- |
| channel | String 类型，频道号 |
| trackId | String 类型，轨道 id |
| trackDesc | String 类型，轨道描述 |


### onStreamTrackUpdate()
码流更新回调

```kotlin
fun onStreamTrackUpdate(uid: String, channel: String, trackId: String, trackDesc: String)
```kotlin

参数

| uid | String 类型，成员的 uid |
| --- | --- |
| channel | String 类型，频道号 |
| trackId | String 类型，轨道 id |
| trackDesc | String 类型，轨道描述 |


### onStreamTrackRemove()
码流移除回调

```kotlin
fun onStreamTrackRemove(uid: String, channel: String, trackInfo: TrackInfo)
```

参数

| uid | String 类型，成员的 uid |
| --- | --- |
| channel | String 类型，频道号 |
| trackInfo | [TrackInfo](https://www.yuque.com/anyconf/rtcengine/linzbg#YnYlM) 类型，轨道信息 |


### onChannelUpdate()
频道更新回调

```kotlin
fun onChannelUpdate(channel: String, props: String?)
```kotlin

参数

| channel | String 类型，频道号 |
| --- | --- |
| props | String 类型，扩展信息 |


### onCustomMessage()
返回自定义消息

```kotlin
fun onCustomMessage(uid: String, action: String, content: String)
```

参数

| channel | String 类型，频道号 |
| --- | --- |
| action | String 类型，消息标识 |
| content | String 类型，消息内容 |


### onDisconnected()
断开连接回调，发生不可恢复的错误，这个事件触发需要重新登录

```kotlin
fun onDisconnected(leaveReason: LeaveReason, statusCode: Int, message: String)
```kotlin

参数

| leaveReason | LeaveReason 枚举类型，断开连接的原因 |
| --- | --- |
| statusCode | String 类型，发生错误时的状态码 |
| message | String 类型，消息内容 |


LeaveReason 属性说明

| Error(-1) | 因为出错离开 |
| --- | --- |
| Unknown(0) | 原因未知 |
| VoluntarilyLeave(1) | 主动离开 |
| KickOut(2) | 被踢出 |
| BeReplaced(3) | 被顶号 |
| HeartbeatTimeout(4) | 心跳超时 |
| ChannelDestroy(5) | 频道销毁 |


### onReconnected()
断线重连成功

```kotlin
fun onReconnected()
```

### onReconnecting()
服务断开并触发重连

```kotlin
fun onReconnecting()
```kotlin

