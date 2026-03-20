---
title: "RoomMsgEvent"
description: "Android SMeeting 会议 SDK RoomMsgEvent 接口参考"
---

说明：`RoomMsgEvent` 是房间消息事件回调接口，用于接收聊天消息与系统消息。

## 回调方法

### onReceiveChatMessage(operatorUid, message, chatMsgType)
```kotlin
fun onReceiveChatMessage(operatorUid: String, message: String, chatMsgType: ChatMsgType)
```
方法说明：收到聊天消息事件。  
参数说明：
- `operatorUid`：`String`，发送者 uid。
- `message`：`String`，消息内容。
- `chatMsgType`：`ChatMsgType`，消息类型。
返回值说明：无（`Unit`）。

### onReceiveSystemMessage(message, chatMsgType)
```kotlin
fun onReceiveSystemMessage(message: String, chatMsgType: ChatMsgType)
```
方法说明：收到系统消息事件。  
参数说明：
- `message`：`String`，消息内容。
- `chatMsgType`：`ChatMsgType`，消息类型。
返回值说明：无（`Unit`）。
