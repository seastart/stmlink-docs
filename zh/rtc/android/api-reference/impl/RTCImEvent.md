---
title: "RTCImEvent"
description: "Android SRTC 音视频 SDK RTCImEvent 接口参考"
---

## 说明

`RTCImEvent` 为即时通讯（IM）事件回调接口。

## 接口方法

### onImConnectSucceed(uid, sid)
```kotlin
fun onImConnectSucceed(uid: String, sid: String)
```
方法说明：IM 连接成功回调。  
参数说明：
- `uid`：`String`，当前用户 ID。
- `sid`：`String`，当前会话 ID。
返回值说明：无（`Unit`）。

### onImDisconnected(reason, statusCode, message)
```kotlin
fun onImDisconnected(reason: LeaveReason, statusCode: Int, message: String)
```
方法说明：IM 断开连接回调。  
参数说明：
- `reason`：`LeaveReason`，断开原因（枚举定义请参考 `LeaveReason` 文档）。
- `statusCode`：`Int`，状态码。
- `message`：`String`，状态描述。
返回值说明：无（`Unit`）。

### onImReconnecting()
```kotlin
fun onImReconnecting()
```
方法说明：IM 开始重连回调。  
参数说明：无。  
返回值说明：无（`Unit`）。

### onImReconnected()
```kotlin
fun onImReconnected()
```
方法说明：IM 重连成功回调。  
参数说明：无。  
返回值说明：无（`Unit`）。

### onImMessage(uid, sid, name, action, content)
```kotlin
fun onImMessage(uid: String, sid: String, name: String, action: String, content: String)
```
方法说明：接收 IM 消息回调。  
参数说明：
- `uid`：`String`，消息发送者用户 ID。
- `sid`：`String`，消息发送者会话 ID。
- `name`：`String`，发送者名称。
- `action`：`String`，消息动作标识。
- `content`：`String`，消息内容。
返回值说明：无（`Unit`）。
