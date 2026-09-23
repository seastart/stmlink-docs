---
title: "音频路由"
description: "扬声器与听筒切换、持久设置与临时设置的优先级、蓝牙与有线耳机、系统来电"
---

会议 SDK 在引擎上直接提供了音频路由接口，不用去碰底层的 `AudioRouteSession`。

---

### 两种设置，优先级不同

| | 接口 | 生效范围 | 典型用法 |
| --- | --- | --- | --- |
| **持久设置** | `defaultAudioRoute`（读写属性） | 长期有效，外设拔出后按它回落 | 入会前定默认走扬声器还是听筒 |
| **临时设置** | `setAudioRoute(target)` | 本次通话，**优先级更高** | 用户在通话中点了"免提" |

```typescript
import { AudioRouteTarget } from 'srtc';

// 入会前：视频会议默认外放，纯语音默认听筒
meeting.defaultAudioRoute = isVideoMeeting
  ? AudioRouteTarget.speaker
  : AudioRouteTarget.earpiece;

// 通话中的免提按钮
function toggleSpeaker(): void {
  const on = meeting.effectiveAudioRouteTarget === AudioRouteTarget.speaker;
  meeting.setAudioRoute(on ? AudioRouteTarget.earpiece : AudioRouteTarget.speaker);
}

// 撤销临时设置
meeting.clearAudioRouteOverride();
```

<Warning>
**免提按钮的选中态要用 `effectiveAudioRouteTarget`，不是 `defaultAudioRoute`。**

后者是持久设置，在有临时设置时不代表当前状态 —— 用它会导致按钮显示与实际不符。
</Warning>

也有个快捷方法：

```typescript
meeting.setSpeakerOutputEnabled(true);   // 等价于切到 speaker
```

---

### 状态查询

| 属性 / 方法 | 类型 | 说明 |
| --- | --- | --- |
| `currentAudioRoute` | `AudioRoute` | **实际**在用的路由（五态） |
| `effectiveAudioRouteTarget` | `AudioRouteTarget` | 当前生效的目标（两态） |
| `audioRouteOverride` | `AudioRouteTarget \| undefined` | 有临时设置时非空 |
| `isExternalAudioRouteActive` | `boolean` | 蓝牙 / 有线是否在用 |
| `availableAudioRoutes()` | `AudioRouteInfo[]` | 可用路由清单 |

---

### 为什么可切换目标只有两个

```
AudioRoute        speaker / earpiece / bluetooth / wired / other   ← 只读，五态
AudioRouteTarget  speaker / earpiece                               ← 可切换，两态
```

**外接设备由系统接管。** SDK 能上报"你现在走蓝牙"，但**不能主动切到某个具体外设** ——
那是系统的职责。

```typescript
if (meeting.isExternalAudioRouteActive) {
  // 蓝牙或有线在用，此时切扬声器/听筒的请求会被系统覆盖
  // UI 上应该把免提按钮置灰，并提示"正在使用耳机"
}
```

---

### 监听变化

```typescript
onAudioRouteChange: (m, data) => {
  // data.route / data.previousRoute，类型 AudioRoute
  this.speakerOn = m.effectiveAudioRouteTarget === AudioRouteTarget.speaker;
  this.usingHeadset = m.isExternalAudioRouteActive;
}
```

<Warning>
**不要在回调里再切回去。**

用户插耳机 → 系统切到 `wired` → 你的回调里又 `setAudioRoute(speaker)` →
系统再切回 `wired`……声音会在两个设备间反复跳。

正确做法是更新 UI，把选择权交给用户。
</Warning>

`audioRouteName(route)` 可以拿到可读名字，直接用于 UI 展示。

---

### 系统来电

来电会抢走音频通道，此时会议音频被系统中断：

```typescript
onCallStateChange: (m, data) => {
  // data.state / data.previousState，类型 AudioCallState
  switch (data.state) {
    case AudioCallState.incoming:
    case AudioCallState.connected:
      this.banner = '系统通话中，会议音频已暂停';
      break;
    case AudioCallState.disconnected:
      this.banner = undefined;
      break;
  }
}
```

`AudioCallState`：`unknown` / `dialing` / `incoming` / `connected` / `disconnected`。

<Note>
SDK 不会自动帮你静音或退会 —— 只上报状态。要不要提示、要不要暂停业务逻辑，
由你决定。
</Note>

---

### 会议场景的典型配置

```typescript
aboutToAppear(): void {
  this.meeting.delegates.add(this.delegate);
  // 视频会议默认外放
  this.meeting.defaultAudioRoute = AudioRouteTarget.speaker;
  this.syncAudioUi();
}

private syncAudioUi(): void {
  this.speakerOn = this.meeting.effectiveAudioRouteTarget === AudioRouteTarget.speaker;
  this.usingHeadset = this.meeting.isExternalAudioRouteActive;
}
```

进会后**先同步一次 UI**，之后靠 `onAudioRouteChange` 更新 ——
只依赖事件的话进会瞬间的按钮状态是错的。

---

### 相关阅读

+ [设备与音频路由接口](/zh/meeting/harmony/api-reference/devices)
+ [设备管理](/zh/meeting/harmony/advanced/device-management)
+ [SRTC 音频路由](/zh/rtc/harmony/advanced/audio-routing) —— 底层接口
