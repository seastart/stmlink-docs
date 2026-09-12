---
title: "等候室"
description: "开启等候室、放行成员、成员被移入等候室时的处理"
---

等候室让主持人先审核再放人进会。

---

### 主持人侧

```typescript
// 开启 / 关闭
await meeting.adminUpdateWaitingRoomDisabled(false);   // false = 启用等候室

// 查看等候中的人
const users: WaitingRoomUserInfo[] = await meeting.adminWaitingRoomUsers();

// 放行某人
await meeting.adminMoveOutWaitingRoom(userId, nickname);

// 放行全部（不传参数）
await meeting.adminMoveOutWaitingRoom();

// 把会中的人移回等候室
await meeting.adminMoveInWaitingRoom(userId, nickname);
```

<Warning>
参数名是 `waitingRoomDisabled` —— **`false` 才是"启用等候室"**。
布尔的方向容易搞反，写的时候对着字段名读一遍。
</Warning>

`WaitingRoomUserInfo` 字段：`userId`、`name`、`avatar`、`at`（进入时间）。

### 监听等候室变化

```typescript
const delegate: SMeetingDelegate = {
  onUserEnterWaitingRoom: (m, data) => {
    // data.uid / name / avatar —— 有人在门外等
    this.waiting = [...this.waiting, data];        // 建新数组
    this.showBadge(this.waiting.length);
  },
  onUserExitWaitingRoom: (m, data) => {
    this.waiting = this.waiting.filter((u) => u.uid !== data.uid);
  },
  onWaitingRoomDisabledChange: (m, data) => {
    // data.waitingRoomDisabled / opUid
  }
};
```

<Note>
`onUserEnterWaitingRoom` / `onUserExitWaitingRoom` 只有**主持人侧**会收到。
普通成员感知不到别人在等候室。
</Note>

---

### 成员侧

被移入等候室时收到一个**无参数**的事件：

```typescript
onMoveToWaitingRoom: (m) => {
  // 已经被移出会议主房间
  this.stage = 'waiting';
  this.stopRenderingMeeting();     // 停止渲染会议内容
}
```

<Warning>
收到 `onMoveToWaitingRoom` 意味着你**已经不在会议主房间里了**。
UI 必须切到等候页，并停止渲染会议画面 —— 继续渲染会显示已失效的旧帧。
</Warning>

成员可以主动退出等候：

```typescript
await meeting.exitWaitingRoom(meetingId, roomNo);
```

这个方法**不需要主持人权限**。

被放行时不会有专门的事件 —— 走的是正常的入会流程，你会收到
`onUserEnter` 等会中事件。

---

### 入会时就被拦在等候室

启用等候室后，`enterRoom()` **不会抛错**，而是走事件：

```typescript
onRoomJoinFailed: (m, data) => {
  // data.failedType 会指出原因
  console.info(`未直接入会: ${data.errDesc}`);
}
```

<Warning>
所以入会流程的 UI 状态机不能假设「`enterRoom` 成功 = 已在会中」。
要等 `onUserEnter`（自己）或读 `getRoomInfo()` 才算真进去了。
</Warning>

---

### 一个最小的等候室面板

```typescript
@State waiting: WaitingRoomUserInfo[] = [];

aboutToAppear(): void {
  this.meeting.delegates.add(this.delegate);
  if (this.isHost) {
    this.meeting.adminWaitingRoomUsers().then((us) => { this.waiting = us; });
  }
}

build() {
  Column() {
    ForEach(this.waiting, (u: WaitingRoomUserInfo) => {
      Row() {
        Text(u.name)
        Button('放行').onClick(async () => {
          await this.meeting.adminMoveOutWaitingRoom(u.userId, u.name);
        })
      }
    }, (u: WaitingRoomUserInfo) => u.userId)

    if (this.waiting.length > 1) {
      Button('全部放行').onClick(async () => {
        await this.meeting.adminMoveOutWaitingRoom();
      })
    }
  }
}
```

进面板时**先查一次** `adminWaitingRoomUsers()` 初始化，之后靠事件增量更新 ——
只依赖事件会漏掉进面板之前已经在等的人。

---

### 相关阅读

+ [会控](/zh/meeting/harmony/advanced/host-controls)
+ [会控接口](/zh/meeting/harmony/api-reference/admin-actions)
+ [事件参考](/zh/meeting/harmony/events)
