---
title: "In-meeting messages"
description: "Send and receive in-meeting chat messages and in-meeting custom messages with the SMeeting Swift SDK, both to everyone and privately, and disable chat for the room or for individual members. Read when adding chat or custom signaling to a meeting."
---

### Overview

There are two kinds of messages inside a meeting, and both work only during the meeting:

| Type | Send | Receive event | Use case |
| --- | --- | --- | --- |
| Chat message | `sendRoomChatMessage(_:type:targetId:)` | `meeting(_:didReceiveChatMessage:)` | Chat content shown to users |
| Custom message | `sendRoomCustomMessage(_:targetId:)` | `meeting(_:didReceiveCustomMessage:)` | Your own custom signaling, such as holding up a sign, voting, or state sync |

Both support sending to everyone and private messages: pass `nil` for `targetId` to send to everyone, or a member's `uid` to send privately.

> Calling them when not in a meeting throws `SMeetingError.notInMeeting`.

---

### Send chat messages

```swift
// Send text to everyone
try await meeting.sendRoomChatMessage("Hi everyone")

// Private message
try await meeting.sendRoomChatMessage("Just between us", targetId: user.uid)

// Non-text messages: upload the file to your own storage first, then send its URL as the message content
try await meeting.sendRoomChatMessage(imageURL, type: .pic)
```

`ChatMsgType` values: `.text` (default), `.file`, `.pic`, `.sound`. The SDK doesn't upload or download the file itself; it only delivers the message content, and how to render it is up to your UI.

---

### Receive chat messages

```swift
func meeting(_ meeting: SMeetingEngine, didReceiveChatMessage data: RoomChatMsgEventData) {
    // data.msgType   message type
    // data.msg       message content
    // data.uid       sender (may be nil)
    // data.isPrivate whether it's a private message
}
```

The sender's nickname isn't in the event; look it up in the member list with `uid`:

```swift
let name = meeting.getUsersInfo()[data.uid ?? ""]?.name ?? data.uid ?? ""
```

If you echo the message locally right after it's sent successfully, compare `data.uid` with `meeting.currentUserId` to deduplicate, so the same message isn't shown twice.

---

### Custom messages

The content of a custom message is a string, usually your own JSON:

```swift
struct VotePayload: Codable {
    let action: String
    let optionId: String
}

let payload = VotePayload(action: "vote", optionId: "A")
let json = String(data: try JSONEncoder().encode(payload), encoding: .utf8) ?? ""
try await meeting.sendRoomCustomMessage(json)
```

To receive:

```swift
func meeting(_ meeting: SMeetingEngine, didReceiveCustomMessage data: RoomCustomMsgEventData) {
    guard let json = data.msg.data(using: .utf8),
          let payload = try? JSONDecoder().decode(VotePayload.self, from: json) else { return }
    // Handle your signaling
}
```

> Custom messages are a path for your own use; the SDK's own meeting signaling goes over a separate path, so your message content never conflicts with the SDK.

---

### Disable chat

Chat can be disabled at the room level and at the member level, both set by the host / a co-host.

#### Room level

```swift
try await meeting.adminUpdateRoomChatDisabled(true)
```

Read the current state from `RoomInfo.chatDisabled`; when it changes, you receive:

```swift
func meeting(_ meeting: SMeetingEngine, roomChatDisabledDidChange data: RoomChatDisabledChangeEventData) {
    // data.chatDisabled, data.opUid
}
```

#### Member level

```swift
try await meeting.adminUpdateUserChatDisabled(targetId: user.uid, chatDisabled: true)
```

Read the current state from `MeetingUserInfo.chatDisabled`; when it changes, you receive:

```swift
func meeting(_ meeting: SMeetingEngine, userChatDisabledDidChange data: UserChatDisabledChangeEventData) {
    // data.uid, data.chatDisabled, data.opUid
}
```

We recommend disabling the input box in the UI directly based on these two states, rather than waiting for sending to fail and then showing a message.

---

### Related pages

+ [Raise hand and turn-on requests](/en/meeting/swift/advanced/handup)
+ [Host controls](/en/meeting/swift/advanced/host-controls)
+ [Out-of-meeting messages](/en/meeting/swift/advanced/im)
