---
title: "RTCImEvent"
description: "Android SRTC 音视频 SDK RTCImEvent 接口参考"
---

即时通讯事件回调监听

### onImConnectSucceed()
im 连接成功

```kotlin
fun onImConnectSucceed(uid: String, sid: String)
```kotlin

参数

| uid | 用户标识 |
| --- | --- |
| sid | 会话标识 |


### onImDisconnected()
im 断开连接

```kotlin
fun onImDisconnected(reason: LeaveReason, statusCode: Int, message: String)
```

参数

| reason | im 断连原因 |
| --- | --- |
| statusCode | 状态码 |
| message | 状态描述 |


LeaveReason 详细说明参见 [LeaveReason枚举](https://www.yuque.com/anyconf/rtcengine/co4luv4dhreapv0g#Qczyz)

### onImReconnecting()
im 开始重连

```kotlin
fun onImReconnecting()
```kotlin

### onImReconnected()
im 重新连接成功

```kotlin
fun onImReconnected()
```

### onImMessage()
im 接收消息

```kotlin
fun onImMessage(uid: String, sid: String, name: String, action: String, content: String)
```kotlin

参数

| uid | 用户标识 |
| --- | --- |
| sid | 会话标识 |
| name | 用户昵称 |
| action | 消息标识 |
| content | 消息内容 |


