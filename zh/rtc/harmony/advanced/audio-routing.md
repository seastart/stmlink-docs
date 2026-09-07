---
title: "音频路由"
description: "用 AudioRouteSession 管理扬声器与听筒切换、处理蓝牙与有线耳机、监听系统通话状态"
---

`AudioRouteSession.shared` 管**音频输出走哪儿**。输入设备的枚举与选择是另一套
（[设备管理](/zh/rtc/harmony/advanced/device-management)）。

---

### 两种设置，优先级不同

这是这套 API 最需要先理解的一点：

| | 接口 | 生效范围 | 典型用法 |
| --- | --- | --- | --- |
| **持久设置** | `defaultAudioRoute` | 长期有效，外设拔出后按它回落 | 入会前定"这个场景默认走扬声器还是听筒" |
| **临时设置** | `setAudioRoute(target)` | 本次通话中，**优先级更高** | 用户在通话中点了"免提" |

```typescript
import { AudioRouteSession, AudioRouteTarget } from 'srtc';

const session = AudioRouteSession.shared;
session.start();

// 持久：视频会议默认外放
session.defaultAudioRoute = AudioRouteTarget.speaker;

// 临时：用户点了听筒
session.setAudioRoute(AudioRouteTarget.earpiece);

// 撤销临时设置，回到持久设置
session.clearAudioRouteOverride();
```

回读状态：

| 属性 | 类型 | 说明 |
| --- | --- | --- |
| `currentRoute` | `AudioRoute` | **实际**在用的路由（五态，含蓝牙 / 有线） |
| `effectiveRouteTarget` | `AudioRouteTarget` | 当前生效的目标（两态） |
| `routeOverride` | `AudioRouteTarget \| undefined` | 有临时设置时非空 |
| `defaultAudioRoute` | `AudioRouteTarget` | 持久设置 |

---

### 为什么 `AudioRoute` 有五态、`AudioRouteTarget` 只有两态

```
AudioRoute       speaker / earpiece / bluetooth / wired / other   ← 只读，五态
AudioRouteTarget speaker / earpiece                               ← 可切换，两态
```

因为**外接设备由系统接管**。SDK 能上报"你现在走的是蓝牙"，但**不能主动切到某个具体外设** ——
那是系统的职责，抢不过也不该抢。

```typescript
if (session.isExternalRouteActive) {
  // 蓝牙或有线耳机在用，此时切扬声器/听筒的请求会被系统覆盖
}
session.isSpeakerActive;        // 当前是否外放
session.isHeadsetAvailable;     // 有线耳机是否可用
session.isBluetoothAvailable;   // 蓝牙是否可用
session.availableRoutes();      // AudioRouteInfo[]，可用路由清单
```

<Warning>
**收到 `onAudioRouteChange` 时不要在回调里再切回去。**

用户插上耳机 → 系统切到 `wired` → 你的回调里又 `setAudioRoute(speaker)` →
系统再切回 `wired`……这样会打起来，表现是声音在两个设备间反复跳。

正确做法是：更新 UI 指示，把选择权交给用户。
</Warning>

---

### 监听变化

```typescript
import { AudioRouteSessionDelegate, AudioRoute, AudioCallState, audioRouteName } from 'srtc';

const observer: AudioRouteSessionDelegate = {
  onAudioRouteChange: (route: AudioRoute, previous: AudioRoute) => {
    console.info(`路由: ${audioRouteName(previous)} → ${audioRouteName(route)}`);
    // 刷新 UI 上的"免提"按钮状态
  },
  onCallStateChange: (state: AudioCallState, previous: AudioCallState) => {
    // 系统通话（来电等）状态变化
  }
};

AudioRouteSession.shared.delegates.add(observer);
AudioRouteSession.shared.start();

// 页面退出时
AudioRouteSession.shared.stop();
AudioRouteSession.shared.delegates.remove(observer);
```

`isObserving` 可以回读监听状态，`refreshCurrentRoute()` 主动刷一次当前路由。

<Warning>
**`delegates` 是强引用，而 `AudioRouteSession.shared` 是全局单例。**

注册后不摘除就是永久泄漏 —— 页面早已销毁，回调还在往一个不该存在的对象上打。
必须在 `aboutToDisappear` 里 `remove`。
</Warning>

---

### 系统通话状态

`AudioCallState` 有五个值：`unknown` / `dialing` / `incoming` / `connected` / `disconnected`。

来电会抢走音频通道，此时 RTC 的音频会被系统中断。业务侧通常需要：

+ `incoming` / `connected`：暂停或提示"通话中已静音"
+ `disconnected`：恢复

```typescript
session.callState;                     // 主动查询
audioCallStateName(session.callState); // 可读名字
```

---

### 会议场景的典型配置

```typescript
// 入会前：视频会议默认外放，语音通话默认听筒
session.defaultAudioRoute = isVideoCall
  ? AudioRouteTarget.speaker
  : AudioRouteTarget.earpiece;
session.start();

// 通话中的"免提"按钮
function toggleSpeaker(): void {
  const on = session.effectiveRouteTarget === AudioRouteTarget.speaker;
  session.setAudioRoute(on ? AudioRouteTarget.earpiece : AudioRouteTarget.speaker);
}
```

判断按钮的选中态用 `effectiveRouteTarget`（当前生效的目标），
而不是 `defaultAudioRoute`（持久设置）—— 后者在有临时设置时不代表当前状态。

---

### 相关阅读

+ [设备管理](/zh/rtc/harmony/advanced/device-management)
+ [事件参考](/zh/rtc/harmony/events)
+ [类型定义](/zh/rtc/harmony/types)
