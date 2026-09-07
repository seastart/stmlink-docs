---
title: "屏幕共享"
description: "发起共享、订阅别人的共享画面、白板共享、以及授权窗相关的坑"
---

HarmonyOS 的屏幕采集是**同进程**的，不需要像 iOS 那样单独做扩展进程，
也没有 50MB 内存上限的约束。

---

### 发起共享

```typescript
import { ShareType, screenPreset1080p } from 'smeeting';

await meeting.requestShare();                                  // 默认屏幕共享
await meeting.requestShare(ShareType.screen, screenPreset1080p());
await meeting.stopShare();
```

`ShareType` 有两种：`screen`（屏幕）与 `whiteBoard`（白板）。

在 `module.json5` 里要声明权限：

```json5
{ "name": "ohos.permission.CAPTURE_SCREEN", "reason": "$string:screen_reason" }
```

<Warning>
**`requestShare()` 返回只代表已发起，不代表已出帧。**

系统会弹窗让用户确认，**用户点同意之后才真正出帧**。UI 上不要在 `await` 返回后
立刻显示"正在共享" —— 等 `onRoomShareStart`（自己也会收到）更可靠。
</Warning>

<Warning>
**每次重启共享都会再弹一次授权窗。**

鸿蒙的 `AVScreenCapture` 拿不到"沿用上次授权"这种待遇。所以不要为了改参数而
反复 `stopShare` + `requestShare`，用户会看到弹窗接连出现。
</Warning>

---

### 会控可能禁止共享

```typescript
const room = meeting.getRoomInfo();
const canShare = room !== undefined && !room.shareDisabled;
```

主持人调 `adminUpdateRoomShareState(true)` 会禁止所有人共享，
变化走 `onRoomShareStateChange`。按它禁用按钮，别等调用失败。

主持人还能强制停止**当前正在进行的**共享：

```typescript
await meeting.adminStopRoomShare();
```

被停的人收到 `onRoomShareStop`，其中 `byAdmin` 为 `true`、`opUid` 是操作者 ——
可以据此提示"你的共享已被主持人停止"。

---

### 订阅别人的共享

```typescript
onRoomShareStart: async (m, data) => {
  // data.uid / data.shareType
  if (data.shareType === ShareType.screen) {
    await m.subscribeRemoteVideoTrack(data.uid, TrackDesc.screen);
    this.sharingUid = data.uid;
  }
},
onRoomShareStop: async (m, data) => {
  await m.unsubscribeRemoteVideoTrack(data.uid, TrackDesc.screen, 0);
  this.sharingUid = undefined;
}
```

渲染：

```typescript
if (this.sharingUid !== undefined) {
  SMeetingRemoteVideoView({
    meeting: this.meeting,
    uid: this.sharingUid,
    trackDesc: TrackDesc.screen
  }).width('100%').height('100%')
}
```

<Note>
`MeetingUserInfo.trackDescs` 里有 `screen` 就说明这个人在共享 ——
进会时用它初始化（可能有人在你进会之前就开始共享了），之后靠事件更新。

只依赖 `onRoomShareStart` 会漏掉这种情况。
</Note>

也可以从 `RoomInfo.shareUid` / `RoomInfo.shareState` 读当前共享状态。

---

### 白板

`ShareType.whiteBoard` 走的是同一套发起流程，但内容不是视频流 ——
白板地址从 `meeting.getWhiteBoard()` 取，用 Web 组件加载。

```typescript
const url: string | undefined = meeting.getWhiteBoard();
```

<Note>
白板与屏幕共享**互斥**（同一时刻只能有一个共享）。切换前要先 `stopShare()`。
</Note>

---

### 共享时的布局

共享开始后通常要把画面切到大窗。如果用 MCU 合流，可以让某个格位绑定共享：

```typescript
const layoutData: LayoutData = {
  layout: LayoutType.right4,
  divList: [/* Cell.bindShare = true 的格位 */]
};
await meeting.adminUpdateLayout(layoutData);
```

见[录制与 MCU](/zh/meeting/harmony/advanced/recording)。

---

### 系统音频

会议 SDK 的 `requestShare` 目前不带系统音频参数。需要连系统声音一起共享时，
走底层 SRTC 的接口：

```typescript
const screen = meeting.srtc.createLocalScreenTrack(
  screenPreset1080p(), screenAudioPresetDefault());
```

细节与坑（`excludesCurrentProcessAudio` 防回环等）见
[SRTC 屏幕共享](/zh/rtc/harmony/advanced/screen-sharing)。

---

### 排查清单

| 现象 | 先查什么 |
| --- | --- |
| 报错信息为空 | 见 SRTC 那页的 `targetId` 那条坑 |
| 一直不出帧 | 用户是不是没点授权窗 |
| 按钮点了没反应 | `RoomInfo.shareDisabled` 是不是 `true` |
| 别人看不到共享 | 视频轨是否发布成功；对端有没有订 `TrackDesc.screen` |
| 授权窗反复弹 | 是不是在循环里重启共享 |

---

### 相关阅读

+ [SRTC 屏幕共享](/zh/rtc/harmony/advanced/screen-sharing) —— 底层细节与全部坑
+ [媒体控制](/zh/meeting/harmony/advanced/media-control)
+ [录制与 MCU](/zh/meeting/harmony/advanced/recording)
