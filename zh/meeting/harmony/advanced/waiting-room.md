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

这个方法**不需要主持人权限**。1.10.0 起它同时把本人移出等主持人名单，
等候室与[等待主持人](#等待主持人入会)两种等待页离开时都调用它。

被放行时不会有专门的事件 —— 走的是正常的入会流程，你会收到
`onUserEnter` 等会中事件。

---

### 入会时就被拦在等候室

会议开启了等候室时，非主持人 `enterRoom()` 会抛 `apiError`，`code` 为 `2118`
（常量 `MeetingServerErrorCode.enterWaitingRoom`，1.10.0 起）。此时服务端已把本人记入候场名单，
App 应进入等待页，而不是当作入会失败。主持人放行后收到会议外消息 `onImAdminMoveOutWaitingRoom`，
再重新 `enterRoom()` 即可（见 [IM 通道](/zh/meeting/harmony/advanced/im#等候室与子会议通知)）。

---

### 等待主持人入会

1.10.0 起。会议开启了「主持人入会前禁止加入」、且主持人 / 联席主持人 / 创建者都未入会时，
`enterRoom()` 抛 `apiError`，`code` 为 `2120`（常量 `MeetingServerErrorCode.enterBeforeHost`）。
服务端已把本人记入等主持人名单，App 应进入「等待主持人」页。

```typescript
import { MeetingServerErrorCode, SMeetingError, SMeetingErrorKind } from 'smeeting';

try {
  await meeting.enterRoom(req);
} catch (e) {
  const err = e as SMeetingError;
  if (err.kind === SMeetingErrorKind.apiError && err.code === MeetingServerErrorCode.enterBeforeHost) {
    this.showWaitingPage('waitingHost');   // 等主持人
  } else if (err.kind === SMeetingErrorKind.apiError && err.code === MeetingServerErrorCode.enterWaitingRoom) {
    this.showWaitingPage('waitingRoom');   // 等候室
  } else {
    throw e;
  }
}
```

等待期间通过会议外 IM 消息得知进展（登录后 SDK 自动维护 IM 连接，见 [IM 通道](/zh/meeting/harmony/advanced/im#等待页通知)）：

```typescript
// 主持人 / 联席主持人 / 创建者任一入会
onImHostEntered: (m, data) => {
  if (data.content.meetingId !== this.waitingMeetingId) {
    return;
  }
  // 带原密码重新 enterRoom
},

// 会议结束或取消（等主持人、等候室两种等待页都会收到）
onImWaitingMeetingEnd: (m, data) => {
  if (data.content.meetingId !== this.waitingMeetingId) {
    return;
  }
  // 提示「会议已结束」，离开等待页
}
```

+ 服务端的检查顺序是密码 → `2120` → `2118`：两个开关都开时，先等主持人；主持人到了重新入会，再拿到 `2118` 转入等候室
+ 同一账号可能先后在等不同的会议，收到消息后请按 `meetingId` / `roomNo` 判断是不是当前等待的那场

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
