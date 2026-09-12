---
title: "签到"
description: "发起签到、成员签到、查询统计与明细"
---

签到用于确认成员实际在场。一场会议可以发起多轮，每轮用 `epoch` 区分。

---

### 主持人：发起与结束

```typescript
// 发起一轮签到，持续 120 秒
await meeting.signInCreate(120, '第一次签到');

// 提前结束
await meeting.signInFinish();
```

| 参数 | 说明 |
| --- | --- |
| `dur` | 持续秒数 |
| `desc` | 说明文字，会展示给成员 |

---

### 成员：签到

```typescript
await meeting.signInSign();
```

不需要任何参数 —— 当前是哪一轮由服务端决定。

---

### 事件

发起时所有人收到：

```typescript
onSignInActivity: (m, data) => {
  // data.hostId / hostName   谁发起的
  // data.epoch               这一轮的标识
  // data.beginAt / endAt     起止时间戳
  // data.dur                 持续秒数
  // data.desc                说明
  this.currentEpoch = data.epoch;
  this.showSignInDialog(data.desc, data.endAt);
}
```

结束时：

```typescript
onSignInFinish: (m, data) => {
  // data.hostId / hostName / epoch
  this.dismissSignInDialog();
}
```

<Note>
`epoch` 是查询统计的必需参数，从 `onSignInActivity` 里拿并存下来 ——
签到结束后还要用它查结果。
</Note>

<Warning>
倒计时用 `endAt`（绝对时间戳）算，不要用 `dur` 自己在本地倒数 ——
后者会因为事件到达延迟而偏移，成员看到的剩余时间和实际不一致。
</Warning>

---

### 查询

```typescript
// 本场会议的签到轮次列表
const list: SignInListResult = await meeting.signInList();

// 某一轮的签到人数
const count: number = await meeting.signInCount(epoch);

// 某一轮的明细，可按昵称过滤
const details: SignDetailInfo[] = await meeting.signInDetail(epoch, '张');
```

| 接口 | 字段 |
| --- | --- |
| `SignInfo` | `uid`、`beginAt`、`dur`、`endAt`、`desc`、`nums`（签到人数） |
| `SignDetailInfo` | `id`、`epoch`、`nickname`、`role`、`userId`、`createdAt` |

<Note>
`signInDetail` 只返回**已签到**的人。要算"谁没签"，得拿它和
`getUsersInfoList()`（当前在会成员）做差集。
</Note>

---

### 一个最小的签到流程

主持人侧：

```typescript
@State epoch: number = 0;
@State signedCount: number = 0;

async startSignIn(): Promise<void> {
  await this.meeting.signInCreate(120, '请签到');
  // epoch 从 onSignInActivity 事件里拿，不是这个调用的返回值
}

private delegate: SMeetingDelegate = {
  onSignInActivity: (m, data) => {
    this.epoch = data.epoch;
    this.pollCount();
  },
  onSignInFinish: async (m, data) => {
    this.signedCount = await m.signInCount(data.epoch);
    const details = await m.signInDetail(data.epoch);
    // 与在会成员做差集，算出未签到的人
    const signed = new Set(details.map((d: SignDetailInfo) => d.userId));
    this.notSigned = m.getUsersInfoList()
      .filter((u: MeetingUserInfo) => !signed.has(u.uid));
  }
};
```

成员侧：

```typescript
onSignInActivity: (m, data) => {
  this.showDialog(data.desc, data.endAt, async () => {
    await m.signInSign();
    toast('签到成功');
  });
}
```

<Warning>
`signInCreate` **不返回 `epoch`** —— 它走事件下发。所以主持人自己也要监听
`onSignInActivity` 才能拿到本轮标识，不能指望调用的返回值。
</Warning>

---

### 相关阅读

+ [会控接口](/zh/meeting/harmony/api-reference/admin-actions)
+ [事件参考](/zh/meeting/harmony/events)
+ [类型定义](/zh/meeting/harmony/types)
