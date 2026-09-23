---
title: "会控"
description: "主持人权限、房间级开关的两字段语义、对成员的媒体操作与主持人移交"
---

会控接口全部要求 `Role.host` 或 `Role.coHost`，否则抛 `unauthorized`（`208004`）。

<Note>
**按角色隐藏 / 禁用按钮，不要靠捕获 `unauthorized`。**
当前角色从 `meeting.getUserInfo(myUid).role` 读，变化监听 `onUserRoleChange`。
</Note>

---

### 房间开关都是「两个字段一组」

麦克风与摄像头这两组最容易写错：

```typescript
// 全体静音，且成员不可自行解除
await meeting.adminUpdateRoomMicState(true, true);

// 全体静音，但成员可以自己开麦
await meeting.adminUpdateRoomMicState(false, true);

// 解除全体静音
await meeting.adminUpdateRoomMicState(false, false);
```

<Warning>
**第一个参数是 `selfUnmuteMicDisabled`（能不能自己解除），第二个才是 `micDisabled`（是否静音）。**

参数顺序反直觉，很容易记错。摄像头的 `adminUpdateRoomCameraState` 同理。
</Warning>

读状态时也要两个一起看：

| `micDisabled` | `selfUnmuteMicDisabled` | 成员的"开麦"按钮 |
| --- | --- | --- |
| `false` | — | 可用 |
| `true` | `false` | 可用（自行解除） |
| `true` | `true` | **禁用**，只能举手 |

```typescript
const room = meeting.getRoomInfo();
const canUnmute = room !== undefined &&
  (!room.micDisabled || !room.selfUnmuteMicDisabled);
```

---

### 其余单开关

```typescript
await meeting.adminUpdateRoomShareState(true);          // 禁止共享
await meeting.adminUpdateRoomChatDisabled(true);        // 禁止聊天
await meeting.adminUpdateRoomScreenshotDisabled(true);  // 禁止截图
await meeting.adminUpdateRoomWatermarkDisabled(false);  // 开启水印
await meeting.adminUpdateRoomLocked(true);              // 锁定会议
await meeting.adminUpdateEnterBeforeHostDisabled(true); // 禁止主持人前入会
```

变化通过对应的 `onRoom*Change` 事件广播给所有人，事件里带 `opUid`（谁操作的）。

<Note>
**锁定会议（`locked`）后新成员无法加入**，但已在会中的不受影响。
被拒绝的成员收到的是 `onRoomJoinFailed`（不是抛错），所以入会失败处理要
同时写 `try/catch` 与那个事件。
</Note>

---

### 对成员的操作

```typescript
await meeting.adminUpdateUserName(uid, '新昵称');
await meeting.adminUpdateUserRole(uid, Role.coHost);   // 设为联席主持人
await meeting.adminUpdateUserChatDisabled(uid, true);  // 单独禁言
await meeting.adminKickUserOut(uid, true);             // 移出并禁止再入
```

### 「请求开」与「直接关」不对称

```typescript
// 请求对方开麦 —— 对方会收到 onAdminRequestOpenMic，需要他同意
await meeting.adminRequestUserOpenMic(uid);

// 直接关掉对方的麦 —— 不需要同意
await meeting.adminCloseUserMic(uid);
```

<Note>
这是**有意的隐私边界**：主持人可以关别人的麦克风和摄像头，但**不能替别人打开**。
成员侧收到请求应当弹窗，同意后调 `requestOpenMic(preset, true, adminUid)`。
</Note>

强制停止当前共享（不指定 uid，停的是正在共享的那个人）：

```typescript
await meeting.adminStopRoomShare();
```

---

### 移交主持人

```typescript
await meeting.adminMoveHost(targetUid);
```

<Warning>
**调用后你自己变成普通成员**，所有会控按钮应当立即失效。
不要假设调用成功后还能继续会控 —— 监听 `onUserRoleChange` 更新 UI。
</Warning>

---

### 一个最小的会控面板

```typescript
@State room?: RoomInfo = undefined;
@State myRole: Role = Role.member;

private delegate: SMeetingDelegate = {
  onRoomMicStateChange: (m, data) => {
    this.room = m.getRoomInfo();      // 整体重取，别改局部字段
  },
  onRoomLockedChange: (m, data) => {
    this.room = m.getRoomInfo();
  },
  onUserRoleChange: (m, data) => {
    if (data.uid === this.myUid) {
      this.myRole = data.role;
    }
  }
};

aboutToAppear(): void {
  this.meeting.delegates.add(this.delegate);
  this.room = this.meeting.getRoomInfo();   // 先读一次初始化
  this.myRole = this.meeting.getUserInfo(this.myUid).role;
}
```

<Note>
进会后**先读一次 `getRoomInfo()` 初始化 UI**，之后靠事件增量更新。
只依赖事件会导致进会瞬间的状态是空的。
</Note>

`isHost` 的判断：

```typescript
const isHost: boolean = this.myRole === Role.host || this.myRole === Role.coHost;
```

---

### 相关阅读

+ [会控接口](/zh/meeting/harmony/api-reference/admin-actions) —— 完整签名
+ [举手](/zh/meeting/harmony/advanced/handup)
+ [等候室](/zh/meeting/harmony/advanced/waiting-room)
+ [事件参考](/zh/meeting/harmony/events)
