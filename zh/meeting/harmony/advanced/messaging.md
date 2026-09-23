---
title: "聊天与自定义消息"
description: "群发与私聊、四种消息类型、自定义消息、禁言控制"
---

### 发消息

```typescript
sendRoomChatMessage(msg: string, type?: ChatMsgType, targetId?: string): Promise<void>
```

```typescript
// 群发文本
await meeting.sendRoomChatMessage('大家好');

// 私聊
await meeting.sendRoomChatMessage('单独说一句', ChatMsgType.text, targetUid);

// 发图片（自己先上传，这里发的是元信息）
await meeting.sendRoomChatMessage(
  JSON.stringify({ url: uploadedUrl, w: 800, h: 600 }),
  ChatMsgType.pic
);
```

| 参数 | 说明 |
| --- | --- |
| `msg` | 消息内容，**始终是字符串** |
| `type` | `ChatMsgType`，默认 `text` |
| `targetId` | 传了就是私聊，不传是群发 |

`ChatMsgType`：`text = 1` / `file = 2` / `pic = 3` / `sound = 4`。

<Note>
**SDK 不传文件。** `file` / `pic` / `sound` 类型只是给消息打个标记，
实际内容要你自己上传（可以用 SDK 的预签名接口，见
[资源与附件](/zh/meeting/harmony/advanced/resources)），然后把 URL 或元信息
序列化成字符串发出去。

也就是说 `msg` 的结构由你和自己的客户端约定，SDK 不解析它。
</Note>

---

### 收消息

```typescript
onChatMessage: (m, data) => {
  // data.msgType: ChatMsgType
  // data.msg: string
  // data.uid?: string       发送者
  // data.isPrivate: boolean 是否私聊
  if (data.msgType === ChatMsgType.text) {
    this.messages = [...this.messages, data];
  } else if (data.msgType === ChatMsgType.pic) {
    const meta = JSON.parse(data.msg) as Record<string, Object>;
    // 按自己的约定解析
  }
}
```

<Warning>
`data.uid` 是**可选**的 —— 系统消息可能没有发送者。渲染前判空。
</Warning>

---

### 自定义消息

跟聊天分开的一条通道，用于业务自己的信令（比如投票、白板同步指令）：

```typescript
onCustomMessage: (m, data) => {
  // data.msg / data.uid? / data.isPrivate
  const payload = JSON.parse(data.msg) as Record<string, Object>;
}
```

<Note>
自定义消息**只有接收事件，没有发送接口** —— 发送由业务后端负责。
与 SRTC 的 `onCustomMessage` 是同一个设计。

需要客户端之间互发业务信令时，用 `sendRoomChatMessage` 配一个自定的
`ChatMsgType` 语义，或者走自己的后端。
</Note>

---

### 禁言

```typescript
// 全体禁言
await meeting.adminUpdateRoomChatDisabled(true);

// 单独禁言某人
await meeting.adminUpdateUserChatDisabled(uid, true);
```

对应事件：

```typescript
onRoomChatDisabledChange: (m, data) => {
  // data.chatDisabled / data.opUid
  this.chatEnabled = !data.chatDisabled;
},
onUserChatDisabledChange: (m, data) => {
  // data.uid / data.chatDisabled / data.opUid
  if (data.uid === this.myUid) {
    this.chatEnabled = !data.chatDisabled;
  }
}
```

<Note>
输入框的可用性要**同时**看两个来源：房间级 `RoomInfo.chatDisabled` 和
自己的 `MeetingUserInfo.chatDisabled`。任一为 `true` 就该禁用。

```typescript
const room = meeting.getRoomInfo();
const me = meeting.getUserInfo(this.myUid);
const canChat = room !== undefined && !room.chatDisabled && !me.chatDisabled;
```
</Note>

被禁言时也可以举手申请（`HandupType.chat`），见[举手](/zh/meeting/harmony/advanced/handup)。

---

### 一个最小的聊天面板

```typescript
@State messages: RoomChatMsgEventData[] = [];
@State canChat: boolean = true;

private delegate: SMeetingDelegate = {
  onChatMessage: (m, data) => {
    this.messages = [...this.messages, data];      // 建新数组
  },
  onRoomChatDisabledChange: (m, data) => {
    this.refreshCanChat(m);
  },
  onUserChatDisabledChange: (m, data) => {
    if (data.uid === this.myUid) {
      this.refreshCanChat(m);
    }
  }
};
```

<Warning>
ArkTS 的 `@State` 只观测第一层赋值 —— 消息列表永远用「建新数组再整体赋值」，
`this.messages.push(...)` 不会刷新 UI。

消息多了要注意截断（比如只留最近 200 条），否则每次都整体重建大数组会卡。
</Warning>

---

### 相关阅读

+ [SMeetingEngine](/zh/meeting/harmony/api-reference/SMeetingEngine)
+ [资源与附件](/zh/meeting/harmony/advanced/resources) —— 文件上传
+ [事件参考](/zh/meeting/harmony/events)
