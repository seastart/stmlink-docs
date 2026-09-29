---
title: "MeetingMessageEvent"
description: "Receive the current meeting's member chat messages, system messages, and app extension messages through MeetingEngine.messageEvent. Read this when you build in-meeting chat or exchange in-meeting custom messages."
---

`MeetingMessageEvent` receives messages in the current meeting and is registered through `MeetingEngine.messageEvent`. You can extend `MeetingMessageSimpleEvent` and override only what you need.

## Usage notes

+ Chat messages, system messages, and app extension messages share the current meeting's message channel but keep separate callbacks; your app should handle them separately by business type.
+ This listener is cleared when you exit the meeting; reassign it for the next meeting.
+ Chat messages are for user content and extension messages are for app-defined actions and data; don't mix them.

## Methods

### onReceiveChatMessage(operatorUid, message, chatMessageType)

```kotlin
fun onReceiveChatMessage(
    operatorUid: String,
    message: String,
    chatMessageType: ChatMsgType
)
```

Description: Received a room chat message sent by a member.

Parameters:

| Parameter | Description |
| --- | --- |
| `operatorUid` | Sender member UID. |
| `message` | Message content. |
| `chatMessageType` | Chat type such as text, file, image, or voice. |

Returns: None (`Unit`).

### onReceiveSystemMessage(message, chatMessageType)

```kotlin
fun onReceiveSystemMessage(
    message: String,
    chatMessageType: ChatMsgType
)
```

Description: Received a room system message.

Parameters:

| Parameter | Description |
| --- | --- |
| `message` | System message content. |
| `chatMessageType` | Message type. |

Returns: None (`Unit`).

### onExtensionMessage(uid, nickname, action, content)

```kotlin
fun onExtensionMessage(
    uid: String?,
    nickname: String?,
    action: String,
    content: String
)
```

Description: Received an in-meeting custom message whose name uses the app extension prefix.

Parameters:

| Parameter | Description |
| --- | --- |
| `uid` | Nullable sender UID. |
| `nickname` | Nullable sender nickname. |
| `action` | App-defined action name. |
| `content` | App-defined content. |

Returns: None (`Unit`).
