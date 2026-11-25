---
title: "聊天与文件消息"
description: "会中群聊 / 私聊、发送聊天文件（presignedPutObject 换签名地址 → 自己 PUT 上传 → sendRoomChatMessage 发 key）、文件消息的 JSON 格式、收消息与下载（presignedGetObject）、拉历史消息 roomChatMsgList"
---

### 概述

会中聊天只有一个发送接口 `sendRoomChatMessage`，文本、文件、图片、语音都走它。

**SDK 不传文件。** `ChatMsgType.File` / `Pic` / `Sound` 只是给消息打个类型标记，`msg` 始终是字符串，
SDK 和服务端都不解析它。所以发文件是三步：

1. `presignedPutObject(PresignedPutObjectType.Chat, ...)` 换一个带签名的上传地址
2. 自己把文件 `PUT` 到这个地址（SDK 不做这一步）
3. 把文件信息序列化成 JSON 字符串，用 `sendRoomChatMessage(msg, ChatMsgType.File)` 发出去

接收方收到后解析 JSON，下载时再用 `presignedGetObject(key)` 换下载地址。

---

### 发文本消息

```typescript
import { ChatMsgType } from '@seastart/smeeting-web-sdk';

// 群发（全房间可见）
await smeeting.sendRoomChatMessage('大家好');

// 私聊：第三个参数传对方 uid
await smeeting.sendRoomChatMessage('单独说一句', ChatMsgType.Text, targetUid);
```

```typescript
sendRoomChatMessage(msg: string, msgType?: ChatMsgType, targetId?: string): Promise<void>
```

| 参数 | 说明 |
| --- | --- |
| `msg` | 消息内容，**始终是字符串**；文件类消息传 JSON 字符串 |
| `msgType` | `ChatMsgType`，默认 `Text`（1）；`File` = 2、`Pic` = 3、`Sound` = 4 |
| `targetId` | 接收者 uid，传了是私聊，不传是群发 |

必须在会中调用，否则报「不在会议中」。会议或本人被禁言时服务端会拒绝。

---

### 发文件消息

```typescript
import { ChatMsgType, PresignedPutObjectType } from '@seastart/smeeting-web-sdk';

async function sendChatFile(file: File) {
  const meetingId = smeeting.getRoomInfo()?.id;
  if (!meetingId) throw new Error('不在会议中');

  // 1. 换预签名上传地址。ext 是不带点的扩展名，决定存储里的文件后缀；必填，没有扩展名时传 bin
  const ext = (file.name.includes('.') ? file.name.split('.').pop()!.toLowerCase() : '') || 'bin';
  const put = await smeeting.presignedPutObject(PresignedPutObjectType.Chat, meetingId, ext);
  // put.url  上传地址（带签名，2 小时内有效）
  // put.key  文件在存储里的 key，消息里发的就是它
  // put.ext  扩展名

  // 2. 自己把文件 PUT 上去，body 直接放文件二进制
  const rsp = await fetch(put.url, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/octet-stream' },
    body: file,
  });
  if (!rsp.ok) throw new Error(`上传失败: ${rsp.status}`);

  // 3. 发消息：msg 是文件信息的 JSON 字符串
  const msg = JSON.stringify({
    key: put.key,          // 必填，接收方凭它换下载地址
    name: file.name,       // 原始文件名，用于展示和下载另存
    size: formatSize(file.size), // 展示用的大小，如 "1.20MB"（官方 Demo 的格式：两位小数、不带空格，不足 1KB 显示整数字节如 "512B"）
  });
  await smeeting.sendRoomChatMessage(msg, ChatMsgType.File);
}
```

要显示上传进度，第 2 步换成 `XMLHttpRequest` 或 axios 的 `onUploadProgress` 即可，地址和方法不变。

#### `presignedPutObject`

```typescript
presignedPutObject(type: PresignedPutObjectType, meetingId: string, ext: string): Promise<{ url: string, key: string, ext: string }>
```

| 参数 | 说明 |
| --- | --- |
| `type` | 资源类别，聊天文件传 `PresignedPutObjectType.Chat` |
| `meetingId` | 当前会议 ID（`getRoomInfo().id`） |
| `ext` | 扩展名，不带点，如 `pdf`、`png`；**必填**，不能传空串，没有扩展名的文件传 `bin` 之类即可（原始文件名放在消息的 `name` 里） |

`PresignedPutObjectType` 的取值：

| 值 | 用途 |
| --- | --- |
| `Attach`（`'attach'`） | 会议附件 |
| `Background`（`'background'`） | 会议背景图 |
| `User`（`'user'`） | 用户资源 |
| `Chat`（`'chat'`） | 聊天文件 |

<Warning>
部署关闭了文件功能时，`presignedPutObject` 直接报错 `2125`（文件功能已关闭），
此时应隐藏聊天里的发文件入口。SDK 不限制文件大小，单个文件上限请在业务侧自己控制。
</Warning>

#### 文件消息的 `msg` 格式

`msg` 的结构由你和自己的各端客户端约定，SDK 不校验。推荐与官方 Web Demo 保持一致：

```json
{
  "key": "chat/2611/meeting-xxxx/a1b2c3d4e5f6.pdf",
  "name": "需求文档.pdf",
  "size": "1.20MB"
}
```

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `key` | string | `presignedPutObject` 返回的 `key`，**不要发 `url`**：上传地址带签名且会过期 |
| `name` | string | 原始文件名 |
| `size` | string | 展示用的文件大小，官方 Demo 格式为两位小数加单位、不带空格，如 `1.20MB`、`42.40KB`，不足 1KB 为 `512B` |

需要更多信息（如图片宽高、语音时长）可以自己加字段，接收方忽略不认识的字段即可。

<Note>
所有接入端（Web / Android / iOS 等）必须用同一种 `msg` 结构，否则对方能收到消息但解析不出文件。
</Note>

---

### 收消息

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

`RoomChatMsgEventData`：

```typescript
interface RoomChatMsgEventData {
    /** 消息类型 */
    msg_type: ChatMsgType;
    /** 消息内容，文件类消息是 JSON 字符串 */
    msg: string;
    /** 发送者 uid */
    uid?: string;
    /** 是否私聊 */
    private: boolean;
}
```

自己发出的消息也会通过这个事件回来（`uid` 等于自己），界面上不要再重复追加一条。

---

### 下载文件

```typescript
async function downloadChatFile(file: { key: string, name: string }) {
  // 用 key 换带签名的下载地址（2 小时内有效，用时再换，不要缓存）
  const { url } = await smeeting.presignedGetObject(file.key);

  // 跨域地址上 <a download> 的文件名不生效，先取成 blob 再另存，才能用原始文件名
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

传 `key`（第一个参数）即可。`id` 参数目前服务端不支持，请始终传 `resKey`。

---

### 拉历史消息

后入会的人看不到之前的事件，用 `roomChatMsgList` 补拉：

```typescript
const { data, _meta } = await smeeting.roomChatMsgList(meetingId, 1, 50);
for (const m of data) {
  const content = m.msg_type === ChatMsgType.File ? JSON.parse(m.msg) : m.msg;
  // m.sender_id / m.sender_name / m.created_at（秒级时间戳）
}
```

```typescript
roomChatMsgList(meetingId: string, page: number, perPage: number): Promise<{ data: ChatMsgInfo[], _meta: MetaRes }>
```

`ChatMsgInfo`：

```typescript
interface ChatMsgInfo {
    /** 消息 id */
    id: string;
    /** 会议 ID */
    meeting_id: string;
    /** 消息内容（文件 / 图片等为 JSON 字符串） */
    msg: string;
    /** 消息类型 */
    msg_type: ChatMsgType;
    /** 发送者 id */
    sender_id: string;
    /** 发送者名称 */
    sender_name: string;
    /** 创建时间（秒级时间戳） */
    created_at: number;
}
```

---

### 相关阅读

+ [SMeeting 接口](/zh/meeting/web/api-reference/SMeeting)
+ [事件](/zh/meeting/web/events) —— `ROOM_CHAT_MSG`、禁言状态变化
+ [类型定义](/zh/meeting/web/types) —— `ChatMsgType`、`PresignedPutObjectType`
