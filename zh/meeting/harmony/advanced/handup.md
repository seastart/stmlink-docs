---
title: "举手"
description: "四种举手类型、状态流转、主持人处理与 UI 状态同步"
---

全体静音且不允许自行解除时，成员通过举手申请发言。举手还可以用于摄像头、聊天、共享。

---

### 四种类型

`HandupType` 决定举手申请的是什么：

| 值 | 申请 |
| --- | --- |
| `mic = 1` | 开麦 |
| `camera = 2` | 开摄像头 |
| `chat = 3` | 发言（聊天） |
| `share = 4` | 共享 |

---

### 状态流转

`UserHandupStep` 是流转步骤：

| 值 | 含义 | 谁触发 |
| --- | --- | --- |
| `request = 1` | 举手 | 成员 |
| `cancel = 2` | 取消举手 | 成员 |
| `confirmOpen = 3` | 同意 | 主持人 |
| `rejectOpen = 4` | 拒绝 | 主持人 |

所有变化都通过 `onUserHandup` 广播：

```typescript
onUserHandup: (m, data) => {
  // data.uid / data.type: HandupType / data.step: UserHandupStep
  switch (data.step) {
    case UserHandupStep.request:
      this.raised = [...this.raised, data];          // 建新数组
      break;
    case UserHandupStep.cancel:
    case UserHandupStep.confirmOpen:
    case UserHandupStep.rejectOpen:
      this.raised = this.raised.filter((h) => h.uid !== data.uid);
      break;
  }
}
```

<Note>
`onUserHandup` 是广播给**所有人**的，包含举手者自己 ——
所以成员侧也能用它来同步自己的举手状态，不必本地猜。
</Note>

---

### 主持人处理

```typescript
// 同意
await meeting.adminConfirmHandup(targetUid, true, HandupType.mic);

// 拒绝
await meeting.adminConfirmHandup(targetUid, false, HandupType.mic);
```

处理结果另有一条事件（给所有人）：

```typescript
onAdminConfirmHandup: (m, data) => {
  // data.type / data.approve / data.targetId / data.opUid
  if (data.targetId === this.myUid) {
    if (data.approve) {
      toast('主持人已同意，可以开麦了');
    } else {
      toast('主持人拒绝了你的申请');
    }
  }
}
```

<Warning>
**同意举手不等于替对方开麦。**

`adminConfirmHandup(uid, true, HandupType.mic)` 只是授予权限，
成员侧还要自己调 `requestOpenMic()`。这与
`adminRequestUserOpenMic` 一样，SDK 不会替用户打开麦克风。
</Warning>

---

### 成员侧的按钮逻辑

举手按钮该不该显示，取决于房间开关：

```typescript
const room = meeting.getRoomInfo();
const canUnmuteSelf = room !== undefined &&
  (!room.micDisabled || !room.selfUnmuteMicDisabled);

// 能自己开麦 → 显示"开麦"；不能 → 显示"举手"
```

| `micDisabled` | `selfUnmuteMicDisabled` | 按钮 |
| --- | --- | --- |
| `false` | — | 开麦 |
| `true` | `false` | 开麦（自行解除） |
| `true` | `true` | **举手** |

两个字段的完整语义见[会控](/zh/meeting/harmony/advanced/host-controls)。

---

### 一个最小的举手列表

```typescript
@State raised: UserHandupEventData[] = [];

build() {
  Column() {
    ForEach(this.raised, (h: UserHandupEventData) => {
      Row({ space: 8 }) {
        Text(this.meeting.getUserInfo(h.uid).name)
        Text(this.typeLabel(h.type)).fontSize(12)
        Button('同意').onClick(async () => {
          await this.meeting.adminConfirmHandup(h.uid, true, h.type);
        })
        Button('拒绝').onClick(async () => {
          await this.meeting.adminConfirmHandup(h.uid, false, h.type);
        })
      }
    }, (h: UserHandupEventData) => `${h.uid}-${h.type as number}`)
  }
}

private typeLabel(t: HandupType): string {
  switch (t) {
    case HandupType.mic: return '申请发言';
    case HandupType.camera: return '申请开摄像头';
    case HandupType.chat: return '申请聊天';
    case HandupType.share: return '申请共享';
    default: return '申请';
  }
}
```

<Note>
`ForEach` 的 key 要**同时包含 uid 和 type** —— 同一个人可以同时申请开麦和开摄像头，
只用 uid 会撞。
</Note>

<Warning>
ArkTS 的 `@State` 只观测第一层赋值，举手列表这类数组永远用「建新数组再整体赋值」，
不要 `push` / `splice`。
</Warning>

---

### 相关阅读

+ [会控](/zh/meeting/harmony/advanced/host-controls)
+ [媒体控制](/zh/meeting/harmony/advanced/media-control)
+ [事件参考](/zh/meeting/harmony/events)
