---
title: "ExtensionMessageEvent"
description: "接收会中自定义业务消息（给程序看的信令，不是聊天消息）"
---

说明：`ExtensionMessageEvent` 是扩展消息回调接口，用于接收自定义业务扩展消息。通过 `MeetingSession.setExtensionMessageEvent(...)` 设置。

## 回调方法

### onExtensionMessage(uid, nickName, action, content)
```kotlin
fun onExtensionMessage(uid: String?, nickName: String?, action: String, content: String)
```
方法说明：收到扩展消息回调。  
参数说明：
- `uid`：`String?`，发送者用户 ID。
- `nickName`：`String?`，发送者昵称。
- `action`：`String`，消息类型。
- `content`：`String`，消息内容。
返回值说明：无（`Unit`）。
