---
title: "MeetingMessageEvent"
description: "接收当前会议的成员聊天、系统消息与应用扩展消息"
---

`MeetingMessageEvent` 接收当前会议的消息，通过 `MeetingEngine.messageEvent` 注册。可继承 `MeetingMessageSimpleEvent` 按需覆写。

## 特殊说明

聊天消息、系统消息和应用扩展消息共用当前会议的消息通道，但保留独立回调，应用应按业务类型分别处理。

## 注意事项

该监听在离会时清除。聊天消息与应用扩展信令语义不同：聊天用于用户内容，扩展消息用于应用自定义动作和数据。

## 接口方法

### onReceiveChatMessage(operatorUid, message, chatMessageType)

```kotlin
fun onReceiveChatMessage(
    operatorUid: String,
    message: String,
    chatMessageType: ChatMsgType
)
```

方法说明：收到成员发送的房间聊天消息。

参数说明：

+ `operatorUid`：发送成员 UID。
+ `message`：消息内容。
+ `chatMessageType`：文本、文件、图片或语音等聊天类型。

返回值说明：无（`Unit`）。

### onReceiveSystemMessage(message, chatMessageType)

```kotlin
fun onReceiveSystemMessage(
    message: String,
    chatMessageType: ChatMsgType
)
```

方法说明：收到房间系统消息。

参数说明：

+ `message`：系统消息内容。
+ `chatMessageType`：消息类型。

返回值说明：无（`Unit`）。

### onExtensionMessage(uid, nickname, action, content)

```kotlin
fun onExtensionMessage(
    uid: String?,
    nickname: String?,
    action: String,
    content: String
)
```

方法说明：收到以应用扩展前缀命名的会中自定义消息。

参数说明：

+ `uid`：可空发送者 UID。
+ `nickname`：可空发送者昵称。
+ `action`：应用自定义动作名。
+ `content`：应用自定义内容。

返回值说明：无（`Unit`）。
