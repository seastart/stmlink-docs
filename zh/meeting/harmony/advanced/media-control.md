---
title: "媒体控制"
description: "开麦开摄像头的完整流程、静音与关闭的区别、响应主持人请求、按需订阅控制带宽"
---

会议 SDK 把「后端授权 → 建轨道 → 采集 → 发布」收成一个调用。
本页讲用法与取舍，完整签名见[媒体控制接口](/zh/meeting/harmony/api-reference/media-control)。

---

### 开麦：三个动作，别混用

```typescript
await meeting.requestOpenMic();      // 开麦（建轨道 + 采集 + 发布）
meeting.setMicMuted(true);           // 静音（轨道还在）
await meeting.closeMic();            // 关麦（销毁轨道）
```

| 用户操作 | 该调什么 | 为什么 |
| --- | --- | --- |
| 点"静音 / 取消静音" | `setMicMuted` | 高频操作，瞬时生效，对端仍看到你在会中 |
| 点"关闭麦克风"（离开发言） | `closeMic` | 真正释放 |

<Warning>
**不要用 `closeMic` + `requestOpenMic` 来实现"静音"按钮。**

每次都要走一遍后端授权 + SDP 协商，用户会感到明显延迟；而且轨道消失会让对端的
成员列表状态跳变。
</Warning>

---

### 开麦可能被拒绝

`requestOpenMic` 里的 `request` 是实义的 —— 主持人开了全体静音时后端会拒绝。

```typescript
// ❌ 不好：点了才知道不能点
try {
  await meeting.requestOpenMic();
} catch (e) {
  toast('主持人已开启全体静音');
}

// ✅ 好：按房间状态提前禁用按钮
const room = meeting.getRoomInfo();
const canUnmute = room !== undefined &&
  (!room.micDisabled || !room.selfUnmuteMicDisabled);
```

状态变化监听 `onRoomMicStateChange`，两个字段的语义见
[会控](/zh/meeting/harmony/advanced/host-controls)。

---

### 响应主持人的请求

主持人调 `adminRequestUserOpenMic(uid)` 后，你收到：

```typescript
onAdminRequestOpenMic: (m, data) => {
  // data.opUid 是发起请求的主持人
  this.showConfirmDialog('主持人请你开麦', async () => {
    await m.requestOpenMic(undefined, true, data.opUid);
  });
}
```

<Note>
第二、三个参数（`byAdmin`、`adminUid`）告诉后端"这是响应请求而非自主开麦"。
**SDK 不会自动开** —— 必须先征求用户同意，这是隐私边界。
</Note>

摄像头同理，走 `onAdminRequestOpenCamera` + `requestOpenCamera(preset, true, opUid)`。

---

### 摄像头

```typescript
const cam = await meeting.requestOpenCamera(cameraPreset720p());
await meeting.closeCamera();
meeting.switchCamera();                       // 前后置
meeting.switchCameraDevice(deviceId);         // 指定设备
```

摄像头**没有** `setMuted` 这种"假关" —— 用户预期关摄像头就该真的关（指示灯熄灭）。

本地预览：

```typescript
if (this.meeting.cameraTrack !== undefined) {
  SRTCVideoView({
    track: this.meeting.cameraTrack,
    trackKey: this.meeting.cameraTrack.id
  }).width('100%').height(240)
}
```

<Note>
`switchCamera` / `switchCameraDevice` 是**原地换设备、不重建轨道**，
所以不需要重新发布 —— 比直接用 SRTC 少一层心智负担。
</Note>

---

### 按需订阅是控制带宽的主要手段

不要一进会就把所有人的视频都订上。跟着摄像头状态走：

```typescript
onUserCameraStateChange: async (m, data) => {
  if (data.cameraState === CameraState.on) {
    await m.subscribeRemoteVideoTrack(data.uid, TrackDesc.cameraSmall);
  } else {
    await m.unsubscribeRemoteVideoTrack(data.uid, TrackDesc.cameraSmall, 300);
  }
}
```

再加上**大小流选择**：

| 视图 | `trackDesc` |
| --- | --- |
| 宫格（多人小窗） | `cameraSmall` |
| 大窗 / 主讲人 | `cameraBig` |
| 共享画面 | `screen` |

<Warning>
20 人宫格全订 `cameraBig` 会把下行带宽打满，表现是所有画面一起卡。
宫格一律用 `cameraSmall`。
</Warning>

`MeetingUserInfo.trackDescs` 告诉你某个人有哪些流可订 —— 里面有 `screen`
就说明他在共享，比自己维护状态可靠。

---

### 远端音频：三种"关"

```typescript
meeting.toggleRemoteAudioMute(true);          // 关扬声器（全体，只停播放）
meeting.toggleUserAudioMute(uid, true);       // 本地静音某人（只停播放）
await meeting.unsubscribeRemoteAudioTrack(uid);  // 真退订（省带宽）
```

前两个只影响**本地播放**，带宽照旧消耗，但切回来是瞬时的。
回读状态用 `isUserAudioMuted(uid)` / `getMutedAudioUids()`。

---

### 屏幕共享

```typescript
await meeting.requestShare();          // 弹系统授权窗
await meeting.stopShare();
```

<Warning>
`requestShare()` 返回只代表已发起，**用户点同意之后才出帧**。
UI 上不要在 `await` 返回后立刻显示"正在共享"。

另外鸿蒙每次重启屏幕采集都要**重新授权**，没有"沿用上次授权"。
</Warning>

监听别人的共享：

```typescript
onRoomShareStart: async (m, data) => {
  await m.subscribeRemoteVideoTrack(data.uid, TrackDesc.screen);
},
onRoomShareStop: async (m, data) => {
  await m.unsubscribeRemoteVideoTrack(data.uid, TrackDesc.screen, 0);
}
```

详见[屏幕共享](/zh/meeting/harmony/advanced/screen-sharing)。

---

### 离会前的清理顺序

```typescript
await meeting.closeCamera();
await meeting.closeMic();
await meeting.stopShare();
await meeting.exitRoom();
```

<Warning>
先关媒体再离会。反过来的话采集可能还在跑一小段时间，
表现是"已经退会了但摄像头指示灯还亮着"。
</Warning>

---

### 相关阅读

+ [媒体控制接口](/zh/meeting/harmony/api-reference/media-control)
+ [视频渲染](/zh/meeting/harmony/advanced/video-rendering)
+ [会控](/zh/meeting/harmony/advanced/host-controls)
+ [SRTC 静音与停止发布](/zh/rtc/harmony/advanced/mute-vs-unpublish)
