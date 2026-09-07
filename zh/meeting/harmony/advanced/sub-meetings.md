---
title: "子会议"
description: "创建与分组、启停子会议、跨组移动成员、成员求助"
---

子会议（分组讨论）把主会议的成员拆到若干独立房间。

---

### 主持人：建组与分人

```typescript
// 一次建多个组
await meeting.adminCreateSubMeeting(mainMeetingId, ['第一组', '第二组', '第三组']);

// 查看现有子会议
const subs: SubMeetingInfo[] = await meeting.adminSubMeetingList(mainMeetingId);

// 改标题
await meeting.adminUpdateSubMeetingTitle(subs[0].id, '产品组');

// 分配成员
await meeting.adminUpdateSubMeetingUsers(subs[0].id, [
  { uid: 'u1', name: '张三' },
  { uid: 'u2', name: '李四' }
]);

// 删除
await meeting.adminDeleteSubMeeting([subs[2].id]);
```

`SubMeetingInfo` 字段：`id`、`mainMeetingId`、`meetingId`、`title`、
`users: SubMeetingUser[]`、`status: MeetingStatus`。

<Note>
注意 `id` 与 `meetingId` 是两个字段：`id` 是子会议配置的标识（传给
`adminUpdateSubMeetingTitle` 等），`meetingId` 是它作为一个会议的 ID。
</Note>

---

### 启停

```typescript
await meeting.adminStartSubMeeting([id1, id2]);   // 可以只启部分组
await meeting.adminStopSubMeeting([id1, id2]);
```

启动后成员收到：

```typescript
onAdminStartSubMeeting: (m, data) => {
  // data.meetingId / title / uids
  if (data.uids.includes(this.myUid)) {
    this.promptJoinSub(data.meetingId, data.title);
  }
}

onAdminStopSubMeeting: (m, data) => {
  // data.parent 是主会议 ID —— 回到主会议
  this.returnToMain(data.parent);
}
```

<Note>
`onAdminStartSubMeeting` 的 `uids` 是**这个组的成员名单** ——
要先判断自己在不在里面，事件是广播给所有人的。
</Note>

---

### 跨组移动成员

```typescript
await meeting.adminMoveSubMeetingUser(fromSubId, toSubId, userId);
```

被移动的成员收到：

```typescript
onAdminMoveSubMeetingUser: (m, data) => {
  // 两侧的 ID 和标题都有，可以直接做提示
  toast(`你已被移动到「${data.toMeetingTitle}」`);
}
```

事件带了 `fromMeetingId` / `fromMeetingTitle` / `toMeetingId` / `toMeetingTitle`
四个字段，不用自己去查名字。

---

### 成员求助

在子会议里成员可以叫主持人：

```typescript
await meeting.userHelpSubMeeting();      // 成员调，不需要权限
```

主持人收到的是一条 IM 事件：

```typescript
onImUserHelpSubMeeting: (m, data) => {
  // data.base.uid / name / avatar —— 谁在求助
  // data.content 里是子会议信息
  this.showHelpRequest(data.base.name, data.content);
}
```

<Note>
求助走的是 IM 通道（`onImUserHelpSubMeeting`），不是会议事件 ——
所以带的是「`base` + `content`」两段结构。
</Note>

---

### 会议模式

`MeetingMode` 里有一档 `subMeeting = 5`。创建会议时指定它表示这是个带分组讨论的会议。

从 `getRoomInfo().meetingMode` 或 `MeetingInfo.meetingMode` 读当前模式。

`RoomInfo.parent` 非空说明**当前就在某个子会议里**，值是主会议 ID ——
用它判断要不要显示"返回主会议"按钮。

---

### 状态流转要小心

进出子会议是一次真正的**离会 + 入会**，所以：

<Warning>
+ 媒体状态不会自动带过去 —— 进子会议后要重新 `requestOpenMic` / `requestOpenCamera`
+ 订阅关系全部失效，画面要重新订
+ 会控开关是子会议自己的一套，不继承主会议

UI 状态机要把"切换子会议"当成一次完整的会议切换来处理，不要复用旧状态。
</Warning>

---

### 相关阅读

+ [会控接口](/zh/meeting/harmony/api-reference/admin-actions)
+ [IM](/zh/meeting/harmony/advanced/im)
+ [事件参考](/zh/meeting/harmony/events)
