---
title: "RoomMsgEvent"
description: "Android SMeeting 会议 SDK RoomMsgEvent 接口参考"
---

房间内消息监听接口

### onReceiveChatMessage()
收到聊天消息事件

```java
void onReceiveChatMessage(String operatorUid, String message, ChatMsgType chatMsgType);
```kotlin

参数

| operatorUid | String 类型，发送者 uid |
| --- | --- |
| message | String 类型，消息内容 |
| chatMsgType | ChatMsgType 类型， 消息类型，详见枚举类型中的 [ChatMsgType](https://www.yuque.com/anyconf/eanoso/sly78y2qziqggiwx) |


### onReceiveSystemMessage()
收到的系统消息事件

```java
void onReceiveSystemMessage(String message, ChatMsgType chatMsgType);
```

参数

| message | String 类型，消息内容 |
| --- | --- |
| chatMsgType | String 类型，消息类型，详见枚举类型中的 [ChatMsgType](https://www.yuque.com/anyconf/eanoso/sly78y2qziqggiwx#dmcbX) |


