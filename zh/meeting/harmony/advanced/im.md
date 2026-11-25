---
title: "IM 通道"
description: "会议 IM 的四类事件、base + content 结构、呼叫与会议提醒、连接状态"
---

IM 是会议 SDK 里独立于会议内聊天的一条通道，用于**会议之外**的通知：
被呼叫入会、会议提醒、等候室与子会议的通知。

<Note>
不需要手动开启 —— 登录后 SDK 自动维护 IM 连接。会议**内**的聊天走
`sendRoomChatMessage` / `onChatMessage`，见
[聊天与自定义消息](/zh/meeting/harmony/advanced/messaging)。
</Note>

---

### 统一的两段结构

所有 IM 业务事件都是「`base` + `content`」：

```typescript
onImCallCalling: (m, data) => {
  // data.base    谁发的
  // data.content 业务内容，类型按事件不同
}
```

`ImBaseEventData`：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `sid` | `string` | 会话 ID |
| `uid` | `string` | 发送者 |
| `name` | `string` | 发送者昵称 |
| `avatar?` | `string` | 头像 |

---

### 被呼叫入会

主持人调 `adminCallUsers([uid])` 时，对方收到：

```typescript
onImCallCalling: (m, data) => {
  // data.content: ImCallContent
  //   roomNo / meetingId / title / forceJoin（1.9.0 起）
  this.showIncomingCall(data.base.name, data.content.title, async () => {
    await m.enterRoom({
      nickname: myNickname,
      meetingId: data.content.meetingId
    });
  });
}
```

`content` 里直接给了 `meetingId` 和 `roomNo`，接受呼叫就是拿它去 `enterRoom`。

**强制入会**（1.9.0 起）：服务端调 `meet-admin/call-users` 带 `force_join=true` 发起的呼叫，`content.forceJoin` 为 `true`（缺省 `false`），
发送者昵称固定为「管理员」。约定的处理方式是不弹接听页、直接入会：

- 已经在 `meetingId` 这场会议里：忽略。
- 正在别的会议里（含等候室、正在入会中）：先 `exitRoom()` 只退出自己（不结束会议、不弹确认），再进入目标会议。
- 被叫人在 30 分钟内凭这次呼叫入会免密码（服务端处理），`enterRoom` 不用传密码；强制呼叫还不受会议锁定、等候室、「主持人入会前不允许他人加入」限制，普通呼叫这些规则照旧。见[邀请入会与移出](/zh/meeting/server-api/guides/invite-and-kickout#能进哪些受限会议)。
- 短时间内同一 `meetingId` 的强制呼叫可能重复到达，建议 10 秒内只处理第一次。
- App 在后台时发本地通知，用户点通知或回到前台再入会。鸿蒙退到后台约 3 秒进程即被冻结，冻结后收不到呼叫。

<Note>
这是**会议外**的事件 —— 用户此时不在任何会议里，所以要在 App 全局
（而不是会议页）监听它。通常在登录后就注册一个全局 delegate。
</Note>

---

### 会议提醒

主持人调 `adminMeetRemind(uids)` 时：

```typescript
onImMeetingRemind: (m, data) => {
  // data.content: ImMeetingRemindContent
  //   roomNo / meetingId / title / creatorName / creatorId（1.4.0 起）/ planTime / planDur
  this.showReminder(
    data.content.title,
    data.content.creatorName,
    data.content.planTime,
    data.content.planDur
  );
}
```

比呼叫多了创建者与预约时间，适合做"会议即将开始"的通知。

---

### 等候室与子会议通知

这两个共用 `ImSubMeetingContent`（`parent` / `meetingId` / `title`）：

```typescript
// 被移出等候室（也就是被放行或被拒）
onImAdminMoveOutWaitingRoom: (m, data) => {
  // data.content.meetingId / title
}

// 子会议里有成员求助（主持人收到）
onImUserHelpSubMeeting: (m, data) => {
  // data.base.name 谁在求助
  // data.content.parent 主会议 ID，meetingId 子会议 ID
  this.showHelpRequest(data.base.name, data.content.title);
}
```

---

### 连接状态

```typescript
onImReconnecting: (m) => { /* 无参数 */ },
onImReconnected: (m) => { /* 无参数 */ },
onImDisconnected: (m, data) => {
  // data.reason?: string
}
```

<Note>
IM 断开**不影响会议本身** —— 会议的媒体和信令走另一条通道。
所以 `onImDisconnected` 只该影响"能不能收到会外通知"这类 UI，
不要据此提示"会议已断开"。
</Note>

---

### 注册在哪里

IM 事件和会议事件在**同一个** `SMeetingDelegate` 接口上，但生效范围不同：

```typescript
// App 级：登录后就注册，用于接呼叫和提醒
class GlobalMeetingObserver implements SMeetingDelegate {
  onImCallCalling = (m, data) => { /* 全局弹窗 */ };
  onImMeetingRemind = (m, data) => { /* 通知栏 */ };
}

// 会议页级：进会时注册，出会时摘除
const roomDelegate: SMeetingDelegate = {
  onUserEnter: (m, u) => { /* ... */ },
  onImUserHelpSubMeeting: (m, data) => { /* 只在会中有意义 */ }
};
```

<Warning>
两份 delegate 都要**成对 `add` / `remove`**。App 级那份的生命周期跟着登录状态走：
`logout()` 之后就该摘掉，否则下次登录会有重复回调。
</Warning>

---

### 相关阅读

+ [事件参考](/zh/meeting/harmony/events)
+ [子会议](/zh/meeting/harmony/advanced/sub-meetings)
+ [等候室](/zh/meeting/harmony/advanced/waiting-room)
