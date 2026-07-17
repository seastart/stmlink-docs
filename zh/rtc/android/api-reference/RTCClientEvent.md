---
title: "RTCClientEvent"
description: "Android SRTC 音视频 SDK RTCClientEvent 接口参考"
---

## 说明

`RTCClientEvent` 为会控相关事件回调接口。

## 接口方法

### onJoinSucceed(channel, uid, whiteBoard)
```kotlin
fun onJoinSucceed(channel: String, uid: String, whiteBoard: String?)
```
方法说明：自己加入频道成功回调。  
参数说明：
- `channel`：`String`，频道标识。
- `uid`：`String`，当前用户 ID。
- `whiteBoard`：`String?`，白板相关信息，可为 `null`。
返回值说明：无（`Unit`）。

### onUserUpdate(channel, uid)
```kotlin
fun onUserUpdate(channel: String, uid: String)
```
方法说明：自己的用户信息更新回调。  
参数说明：
- `channel`：`String`，频道标识。
- `uid`：`String`，当前用户 ID。
返回值说明：无（`Unit`）。

### onMeMembershipChanged(channel, isMember)
```kotlin
fun onMeMembershipChanged(channel: String, isMember: Boolean)
```
方法说明：自己的观众/成员身份发生变化回调。观众升为正式成员（加入成员列表）时 `isMember = true`；正式成员被降为观众（移出成员列表）时 `isMember = false`。仅在身份**变化**时触发；入会时的初始身份请用 [`RTCEngine.isAudience`](/zh/rtc/android/api-reference/RTCEngine) 读取。  
参数说明：
- `channel`：`String`，频道标识。
- `isMember`：`Boolean`，`true` 表示当前为正式成员，`false` 表示当前为观众。
返回值说明：无（`Unit`）。

### onRemoteUserJoin(channel, uid)
```kotlin
fun onRemoteUserJoin(channel: String, uid: String)
```
方法说明：其他用户加入频道回调。  
参数说明：
- `channel`：`String`，频道标识。
- `uid`：`String`，远端用户 ID。
返回值说明：无（`Unit`）。

### onRemoteUserLeave(channel, userInfo, leaveReason)
```kotlin
fun onRemoteUserLeave(channel: String, userInfo: UserInfo, leaveReason: LeaveReason)
```
方法说明：其他用户离开频道回调。  
参数说明：
- `channel`：`String`，频道标识。
- `userInfo`：`UserInfo`，离会用户信息（对象字段请参考 `UserInfo` 文档）。
- `leaveReason`：`LeaveReason`，离会原因（枚举定义请参考 `LeaveReason` 文档）。
返回值说明：无（`Unit`）。

### onRemoteUserUpdate(channel, uid)
```kotlin
fun onRemoteUserUpdate(channel: String, uid: String)
```
方法说明：其他用户信息更新回调。  
参数说明：
- `channel`：`String`，频道标识。
- `uid`：`String`，远端用户 ID。
返回值说明：无（`Unit`）。

### onStreamTrackAdd(uid, channel, trackId, trackDesc)
```kotlin
fun onStreamTrackAdd(uid: String, channel: String, trackId: String, trackDesc: String)
```
方法说明：新增码流回调。  
参数说明：
- `uid`：`String`，所属用户 ID。
- `channel`：`String`，频道标识。
- `trackId`：`String`，轨道 ID。
- `trackDesc`：`String`，轨道描述。
返回值说明：无（`Unit`）。

### onStreamTrackUpdate(uid, channel, trackId, trackDesc)
```kotlin
fun onStreamTrackUpdate(uid: String, channel: String, trackId: String, trackDesc: String)
```
方法说明：码流更新回调。  
参数说明：
- `uid`：`String`，所属用户 ID。
- `channel`：`String`，频道标识。
- `trackId`：`String`，轨道 ID。
- `trackDesc`：`String`，轨道描述。
返回值说明：无（`Unit`）。

### onStreamTrackRemove(uid, channel, trackInfo)
```kotlin
fun onStreamTrackRemove(uid: String, channel: String, trackInfo: TrackInfo)
```
方法说明：码流移除回调。  
参数说明：
- `uid`：`String`，所属用户 ID。
- `channel`：`String`，频道标识。
- `trackInfo`：`TrackInfo`，被移除的轨道信息（对象字段请参考 `TrackInfo` 文档）。
返回值说明：无（`Unit`）。

### onChannelUpdate(channel, props)
```kotlin
fun onChannelUpdate(channel: String, props: String?)
```
方法说明：频道属性更新回调。  
参数说明：
- `channel`：`String`，频道标识。
- `props`：`String?`，频道属性 JSON 字符串，可为 `null`。
返回值说明：无（`Unit`）。

### onCustomMessage(uid, sid, name, action, content)
```kotlin
fun onCustomMessage(uid: String, sid: String, name: String, action: String, content: String)
```
方法说明：自定义消息回调。  
参数说明：
- `uid`：`String`，消息发送者用户 ID。
- `sid`：`String`，消息发送者会话 ID。
- `name`：`String`，发送者名称。
- `action`：`String`，消息动作标识。
- `content`：`String`，消息内容。
返回值说明：无（`Unit`）。

### onDisconnected(leaveReason, statusCode, message)
```kotlin
fun onDisconnected(leaveReason: LeaveReason, statusCode: Int, message: String)
```
方法说明：服务断开连接且不可恢复时回调（需要重新登录）。  
参数说明：
- `leaveReason`：`LeaveReason`，断开原因（枚举定义请参考 `LeaveReason` 文档）。
- `statusCode`：`Int`，状态码。
- `message`：`String`，状态描述。
返回值说明：无（`Unit`）。

### onReconnected()
```kotlin
fun onReconnected()
```
方法说明：服务重连成功回调。  
参数说明：无。  
返回值说明：无（`Unit`）。

### onReconnecting()
```kotlin
fun onReconnecting()
```
方法说明：服务断开后开始重连回调。  
参数说明：无。  
返回值说明：无（`Unit`）。

### onError(errorCode, message)
```kotlin
fun onError(errorCode: Int, message: String)
```
方法说明：频道级错误回调（例如频道未启动）。  
参数说明：
- `errorCode`：`Int`，错误码。
- `message`：`String`，错误描述。
返回值说明：无（`Unit`）。
