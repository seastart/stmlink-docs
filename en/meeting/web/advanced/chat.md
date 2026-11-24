---
title: "In-meeting chat and file messages"
description: "Group and private in-meeting chat, sending chat files (presignedPutObject for a signed URL → PUT the file yourself → sendRoomChatMessage with the key), the JSON format of file messages, receiving and downloading (presignedGetObject), and fetching history with roomChatMsgList"
---

### Overview

In-meeting chat has a single send API, `sendRoomChatMessage`, used for text, files, images, and voice alike.

**The SDK doesn't transfer files.** `ChatMsgType.File` / `Pic` / `Sound` only tag the message type; `msg` is always a string,
and neither the SDK nor the server parses it. So sending a file takes three steps:

1. `presignedPutObject(PresignedPutObjectType.Chat, ...)` to get a signed upload URL
2. `PUT` the file to that URL yourself (the SDK doesn't do this step)
3. Serialize the file info into a JSON string and send it with `sendRoomChatMessage(msg, ChatMsgType.File)`

The receiver parses the JSON, and when downloading calls `presignedGetObject(key)` to get a download URL.

---

### Send a text message

```typescript
import { ChatMsgType } from '@seastart/smeeting-web-sdk';

// Send to everyone in the room
await smeeting.sendRoomChatMessage('Hello everyone');

// Private message: pass the other user's uid as the third argument
await smeeting.sendRoomChatMessage('Just for you', ChatMsgType.Text, targetUid);
```

```typescript
sendRoomChatMessage(msg: string, msgType?: ChatMsgType, targetId?: string): Promise<void>
```

| Parameter | Description |
| --- | --- |
| `msg` | Message content, **always a string**; file-type messages pass a JSON string |
| `msgType` | `ChatMsgType`, defaults to `Text` (1); `File` = 2, `Pic` = 3, `Sound` = 4 |
| `targetId` | Recipient uid; set it for a private message, omit it to send to everyone |

Must be called while in a meeting, otherwise it fails with "not in meeting". The server rejects it when chat is disabled for the meeting or for you.

---

### Send a file message

```typescript
import { ChatMsgType, PresignedPutObjectType } from '@seastart/smeeting-web-sdk';

async function sendChatFile(file: File) {
  const meetingId = smeeting.getRoomInfo()?.id;
  if (!meetingId) throw new Error('Not in a meeting');

  // 1. Get a signed upload URL. ext is the extension without the dot and sets the file suffix in storage
  const ext = file.name.includes('.') ? file.name.split('.').pop()!.toLowerCase() : '';
  const put = await smeeting.presignedPutObject(PresignedPutObjectType.Chat, meetingId, ext);
  // put.url  Upload URL (signed, valid for 2 hours)
  // put.key  Key of the file in storage; this is what the message carries
  // put.ext  Extension

  // 2. PUT the file yourself, with the file binary as the body
  const rsp = await fetch(put.url, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/octet-stream' },
    body: file,
  });
  if (!rsp.ok) throw new Error(`Upload failed: ${rsp.status}`);

  // 3. Send the message: msg is a JSON string of the file info
  const msg = JSON.stringify({
    key: put.key,          // Required; the receiver uses it to get a download URL
    name: file.name,       // Original file name, for display and save-as
    size: formatSize(file.size), // Display size, e.g. "1.2 MB"
  });
  await smeeting.sendRoomChatMessage(msg, ChatMsgType.File);
}
```

To show upload progress, replace step 2 with `XMLHttpRequest` or axios `onUploadProgress`; the URL and method stay the same.

#### `presignedPutObject`

```typescript
presignedPutObject(type: PresignedPutObjectType, meetingId: string, ext: string): Promise<{ url: string, key: string, ext: string }>
```

| Parameter | Description |
| --- | --- |
| `type` | Resource category; pass `PresignedPutObjectType.Chat` for chat files |
| `meetingId` | Current meeting ID (`getRoomInfo().id`) |
| `ext` | Extension without the dot, such as `pdf` or `png`; pass an empty string if there is none |

Values of `PresignedPutObjectType`:

| Value | Purpose |
| --- | --- |
| `Attach` (`'attach'`) | Meeting attachment |
| `Background` (`'background'`) | Meeting background image |
| `User` (`'user'`) | User resource |
| `Chat` (`'chat'`) | Chat file |

<Warning>
When the deployment has file features turned off, `presignedPutObject` fails right away with `2125` (file features disabled);
hide the send-file entry in chat in that case. The SDK doesn't limit file size; enforce a per-file limit in your app.
</Warning>

#### `msg` format of file messages

The structure of `msg` is agreed between you and your own clients; the SDK doesn't validate it. We recommend matching the official Web demo:

```json
{
  "key": "chat/2611/meeting-xxxx/a1b2c3d4e5f6.pdf",
  "name": "requirements.pdf",
  "size": "1.2 MB"
}
```

| Field | Type | Description |
| --- | --- | --- |
| `key` | string | The `key` returned by `presignedPutObject`. **Don't send the `url`**: the upload URL is signed and expires |
| `name` | string | Original file name |
| `size` | string | Display file size |

Add your own fields if you need more (such as image dimensions or voice duration); receivers just ignore fields they don't recognize.

<Note>
All your clients (Web / Android / iOS, etc.) must use the same `msg` structure; otherwise the other side receives the message but can't parse the file out of it.
</Note>

---

### Receive messages

```typescript
import { RoomEvent, RoomEventType, ChatMsgType, RoomChatMsgEventData } from '@seastart/smeeting-web-sdk';

smeeting.onNotifyRoomEvent = (event: RoomEvent) => {
  if (event.type !== RoomEventType.ROOM_CHAT_MSG) return;
  const data = event.data as RoomChatMsgEventData;

  if (data.msg_type === ChatMsgType.File) {
    const file = JSON.parse(data.msg); // { key, name, size }
    showFileMessage(data.uid, file, data.private);
  } else {
    showTextMessage(data.uid, data.msg, data.private);
  }
};
```

`RoomChatMsgEventData`:

```typescript
interface RoomChatMsgEventData {
    /** Message type */
    msg_type: ChatMsgType;
    /** Message content; a JSON string for file-type messages */
    msg: string;
    /** Sender uid */
    uid?: string;
    /** Whether it's a private message */
    private: boolean;
}
```

Messages you send also come back through this event (`uid` equals your own), so don't append them to the UI a second time.

---

### Download a file

```typescript
async function downloadChatFile(file: { key: string, name: string }) {
  // Exchange the key for a signed download URL (valid for 2 hours; get a new one each time, don't cache it)
  const { url } = await smeeting.presignedGetObject(file.key);

  // <a download> ignores the file name on cross-origin URLs, so fetch it as a blob first to keep the original name
  const blob = await (await fetch(url)).blob();
  const blobUrl = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = blobUrl;
  a.download = file.name;
  a.click();
  URL.revokeObjectURL(blobUrl);
}
```

```typescript
presignedGetObject(resKey?: string, id?: string): Promise<{ url: string }>
```

Chat files only have a `key`, so pass just the first argument; `id` is for meeting materials (the resource ID returned by `resourcesList`).

---

### Fetch message history

People who join later don't see earlier events; use `roomChatMsgList` to fetch them:

```typescript
const { data, _meta } = await smeeting.roomChatMsgList(meetingId, 1, 50);
for (const m of data) {
  const content = m.msg_type === ChatMsgType.File ? JSON.parse(m.msg) : m.msg;
  // m.sender_id / m.sender_name / m.created_at (timestamp in seconds)
}
```

```typescript
roomChatMsgList(meetingId: string, page: number, perPage: number): Promise<{ data: ChatMsgInfo[], _meta: MetaRes }>
```

`ChatMsgInfo`:

```typescript
interface ChatMsgInfo {
    /** Message id */
    id: string;
    /** Meeting ID */
    meeting_id: string;
    /** Message content (a JSON string for files / images, etc.) */
    msg: string;
    /** Message type */
    msg_type: ChatMsgType;
    /** Sender id */
    sender_id: string;
    /** Sender name */
    sender_name: string;
    /** Creation time (timestamp in seconds) */
    created_at: number;
}
```

---

### Related reading

+ [SMeeting API](/en/meeting/web/api-reference/SMeeting)
+ [Events](/en/meeting/web/events) — `ROOM_CHAT_MSG` and chat-disabled state changes
+ [Types](/en/meeting/web/types) — `ChatMsgType`, `PresignedPutObjectType`
