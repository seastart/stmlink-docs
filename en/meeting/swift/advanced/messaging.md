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

// Non-text messages: msg is still a string; see the next section for file messages
try await meeting.sendRoomChatMessage(content, type: .file)
```

`ChatMsgType` values: `.text` (default), `.file`, `.pic`, `.sound`. The SDK doesn't upload or download the file itself; it only delivers the message content, and how to render it is up to your UI.

---

### Send file messages

Since 1.12.0, `PresignedPutObjectType.chat` lets you upload chat files straight to the meeting's object storage. It takes three steps:

1. Call `presignedPutObject(type: .chat, ...)` to get a signed upload URL
2. `PUT` the file to that URL yourself (the SDK doesn't do this step)
3. Serialize `{key, name, size}` into a JSON string and send it with `sendRoomChatMessage(_:type: .file)`

```swift
func sendChatFile(fileURL: URL) async throws {
    guard let meetingId = meeting.getRoomInfo()?.id else { return }
    let data = try Data(contentsOf: fileURL)

    // 1. Get an upload URL. ext has no leading dot and is required; pass bin when there is no extension
    let ext = fileURL.pathExtension.isEmpty ? "bin" : fileURL.pathExtension.lowercased()
    let object = try await meeting.presignedPutObject(type: .chat, meetingId: meetingId, ext: ext)

    // 2. PUT the file yourself, with the raw file bytes as the body
    var request = URLRequest(url: URL(string: object.url)!)
    request.httpMethod = "PUT"
    request.setValue("application/octet-stream", forHTTPHeaderField: "Content-Type")
    let (_, response) = try await URLSession.shared.upload(for: request, from: data)
    guard (response as? HTTPURLResponse)?.statusCode == 200 else { throw URLError(.badServerResponse) }

    // 3. Send the message: the content is a JSON string of the file info
    let payload: [String: String] = [
        "key": object.key,                 // Required; the receiver uses it to get a download URL
        "name": fileURL.lastPathComponent, // Original file name, for display and saving
        "size": "1.20MB",                  // Display size; official Demo format: two decimals, no space, whole bytes below 1KB such as "512B"
    ]
    let content = String(data: try JSONSerialization.data(withJSONObject: payload), encoding: .utf8)!
    try await meeting.sendRoomChatMessage(content, type: .file)
}
```

The receiver parses the JSON in `msg` and, when downloading, gets a URL from the `key` on demand:

```swift
let url = try await meeting.presignedGetObject(resKey: key)
```

`{key, name, size}` is the format used by the official Web Demo and Swift Demo. The SDK doesn't validate it, so you can also agree on your own format across your clients.

> When the deployment has file features turned off, `presignedPutObject` throws error code `2125` (file features are disabled); hide the send-file entry in that case. The SDK doesn't limit file size, so enforce a per-file limit in your app.

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
