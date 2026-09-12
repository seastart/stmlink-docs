---
title: "快速开始"
description: "在 HarmonyOS 应用中用 SMeeting 完成登录、创建会议、入会、开麦开摄像头的最小流程"
---

本文用最小代码跑通一次会议：登录 → 创建或加入会议 → 开麦 → 开摄像头 → 离会。

开始之前请先完成 [集成方式](/zh/meeting/harmony/integration) 中的两个 HAR 引入、权限配置与 `SRTC.init`。

---

### 调用序列总览

```
登录        meeting.login(token)              ← token 由业务后端签发
            meeting.delegates.add(delegate)
            meeting.attendeeRoom()            ← 拉"即将开始"列表

即时会议    meeting.createRoom(req) → [roomNo, meetingId]
            meeting.enterRoom({ nickname, meetingId })
房间号入会  meeting.enterRoom({ nickname, roomNo, password })

开麦        meeting.requestOpenMic()          ← 内含"后端授权 → 建轨道 → 采集 → 发布"
开摄像头    meeting.requestOpenCamera()       ← 预览用 meeting.cameraTrack
共享        meeting.requestShare()            ← 弹系统授权窗，同意后出帧

聊天        meeting.sendRoomChatMessage(msg)   ← 可选 type / targetId（私聊）
会控        meeting.adminUpdateRoomMicState / adminKickUserOut / ...

离会        meeting.closeCamera() / closeMic() / stopShare() → meeting.exitRoom()
登出        meeting.logout() → meeting.delegates.remove(delegate)
```

<Note>
`requestOpenMic` / `requestOpenCamera` 是**一体化**接口：内部完成"向会议后端申请授权 → 创建本地轨道 → 启动采集 → 发布到频道"。你不需要像直接使用 SRTC 那样自己拼这四步。
</Note>

---

### 第一步：创建引擎并登录

Token 由**你的业务后端**签发，SDK 不负责发号。

```typescript
import { SMeetingEngine } from 'smeeting';
import { LogLevel } from 'srtc';

const meeting: SMeetingEngine = new SMeetingEngine(LogLevel.info);

await meeting.login(token);
```

---

### 第二步：监听会议事件

```typescript
import { SMeetingDelegate } from 'smeeting';

const delegate: SMeetingDelegate = {
  onUserEnter: (m, user) => {
    console.info(`${user.name} 进入会议`);
  },
  onUserExit: (m, data) => {
    console.info(`${data.uid} 离开会议，原因 ${data.reason}`);
  },
  onUserMicStateChange: (m, data) => {
    // data.uid / data.micState / data.byAdmin
    // 刷新成员列表上的麦克风图标
  },
  onUserCameraStateChange: (m, data) => {
    // data.uid / data.cameraState —— 按需订阅或取消订阅画面
  },
  onRoomMicStateChange: (m, data) => {
    // data.micDisabled 全体静音；data.selfUnmuteMicDisabled 是否允许自行解除
  },
  onChatMessage: (m, data) => {
    console.info(`${data.uid}: ${data.msg}`);
  },
  onDisconnected: (m, data) => {
    console.warn(`会议连接断开：${data.reason}`);
  },
  onRoomJoinFailed: (m, data) => {
    console.error(`入会失败：${data.errDesc}`);
  }
};

meeting.delegates.add(delegate);
```

<Note>
所有回调的**第一个参数都是引擎实例**，第二个参数是该事件的数据对象（`onUserEnter` 例外，第二个参数直接是 `MeetingUserInfo`）。数据对象的字段见各事件的类型定义。
</Note>

<Warning>
**`delegates` 是强引用，必须成对 `add` / `remove`。**

ArkTS 没有弱引用，也没有 `deinit`。注册后不摘除会导致监听者永不回收，而且离开页面后仍然收到回调。通常在组件的 `aboutToAppear` / `aboutToDisappear` 里配对处理。
</Warning>

---

### 第三步：创建或加入会议

#### 创建即时会议

```typescript
import { MeetingCreateReq } from 'smeeting';

const req: MeetingCreateReq = { title: '产品评审' };
const result: string[] = await meeting.createRoom(req);
const roomNo: string = result[0];
const meetingId: string = result[1];

await meeting.enterRoom({ nickname: '张三', meetingId: meetingId });
```

#### 用房间号加入

```typescript
await meeting.enterRoom({
  nickname: '张三',
  roomNo: '123456',
  password: '1234'   // 会议有密码时必填
});
```

`meetingId` 与 `roomNo` 二选一，`nickname` 必填。

---

### 第四步：开麦与开摄像头

```typescript
// 开麦
await meeting.requestOpenMic();
// 关麦
await meeting.closeMic();

// 通话中临时静音（不重建轨道）
meeting.setMicMuted(true);
```

```typescript
// 开摄像头，返回本地轨道用于预览
const camera = await meeting.requestOpenCamera();
// 关摄像头
await meeting.closeCamera();
// 切换前后置
meeting.switchCamera();
```

<Note>
主持人开启全体静音后，`requestOpenMic` 会被后端拒绝。这类限制通过 `onRoomMicStateChange` 事件下发，UI 上应当据此禁用按钮，而不是等调用失败。
</Note>

---

### 第五步：渲染画面

渲染组件来自 `srtc`。

#### 本地预览

```typescript
import { SRTCVideoView } from 'srtc';

if (this.cameraTrack !== undefined) {
  SRTCVideoView({ track: this.cameraTrack, trackKey: this.cameraTrack.id })
    .width('100%')
    .height(240)
}
```

本地摄像头轨道也可以直接从引擎上取：`meeting.cameraTrack` / `meeting.screenTrack` / `meeting.micTrack`。

#### 订阅并渲染远端

```typescript
import { Track } from 'srtc';

// 订阅某个成员的画面
await meeting.subscribeRemoteVideoTrack(uid);

// 取到轨道交给组件
const remote: Track | undefined = meeting.getRemoteVideoTrack(uid);
```

多路画面用 `ForEach`，key 带上成员 uid：

```typescript
ForEach(this.tiles, (tile: Tile) => {
  SRTCVideoView({
    track: meeting.getRemoteVideoTrack(tile.uid),
    trackKey: tile.uid
  })
}, (tile: Tile) => tile.uid)
```

<Warning>
**`track` 是普通成员变量，不能声明成 `@Prop`。**

ArkTS 的 `@Prop` 对复杂类型做深拷贝，且拷贝过程中会丢失类型 —— `Track` 拷过来会变成没有方法的普通对象，结果是画面黑屏、事件也收不到。轨道要**按引用**传入，换轨道靠组件重建。
</Warning>

---

### 第六步：屏幕共享

```typescript
await meeting.requestShare();
await meeting.stopShare();
```

`requestShare` 会弹出系统授权窗，用户同意之后才开始出帧。

---

### 第七步：离会与清理

```typescript
await meeting.closeCamera();
await meeting.closeMic();
await meeting.stopShare();
await meeting.exitRoom();

await meeting.logout();
meeting.delegates.remove(delegate);
meeting.dispose();
```

<Warning>
`dispose()` 必须调用 —— 它会摘掉挂在全局单例上的监听。ArkTS 没有析构函数，漏掉会导致页面永不回收、摄像头指示灯一直亮。
</Warning>

---

### 自测建议

+ **发布与订阅必须在真机上验证**：视频预设都用 H264，而 H264 只有硬编、没有软编兜底，模拟器上编码器建不出来。
+ **不要以"看到画面"作为通过标准**：缺少 H264 硬编能力的设备会静默退回 VP8，表现为和其它端互通不上。

---

### 下一步

+ [集成方式](/zh/meeting/harmony/integration) —— 环境要求与权限配置
+ [更新日志](/zh/meeting/harmony/changelog) —— 版本变更记录
