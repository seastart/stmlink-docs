---
title: "设备与音频路由接口"
description: "SMeetingEngine 上的设备枚举、热插拔监听与音频输出路由接口"
---

会议 SDK 在引擎上直接包了一层设备与路由接口，不用再去碰底层的
`DeviceManager` / `AudioRouteSession`。

---

## 设备枚举

```typescript
getDevices(kind?: DeviceKind): Promise<DeviceInfo[]>
cachedDevices(kind?: DeviceKind): DeviceInfo[]
```

| 方法 | 说明 |
| --- | --- |
| `getDevices(kind?)` | 查询设备，可按类别过滤 |
| `cachedDevices(kind?)` | 读缓存，**不触发系统查询** |

`DeviceKind`：`audioInput` / `audioOutput` / `videoInput`。

<Note>
做设备下拉框用 `cachedDevices()` —— 它不会每次渲染都去问系统。
配合热插拔事件刷新即可。
</Note>

`DeviceInfo` 字段：`deviceId`、`name`、`kind`、`isDefault`。

---

## 热插拔监听

```typescript
startDeviceMonitoring(): void
stopDeviceMonitoring(): void
```

事件走 `SMeetingDelegate` 里的 `onDeviceAdd` / `onDeviceRemove`
（第二个参数直接是 `DeviceInfo`）：

```typescript
const delegate: SMeetingDelegate = {
  onDeviceAdd: (meeting, device: DeviceInfo) => {
    this.devices = meeting.cachedDevices();     // 建新数组再整体赋值
  },
  onDeviceRemove: (meeting, device: DeviceInfo) => {
    this.devices = meeting.cachedDevices();
  }
};

meeting.delegates.add(delegate);
meeting.startDeviceMonitoring();

// 页面退出
meeting.stopDeviceMonitoring();
meeting.delegates.remove(delegate);
```

<Warning>
ArkTS 的 `@Observed` / `@State` **只观测第一层属性的赋值**。设备列表这类数组
永远用「建新数组再整体赋值」，不要 `push` / `splice` 原数组 —— 那样 UI 不会刷新。
</Warning>

---

## 切换摄像头

```typescript
switchCamera(cameraId?: string): void
switchCameraDevice(deviceId: string): void
```

| 方法 | 说明 |
| --- | --- |
| `switchCamera()` | 不传参数就是前后置切换 |
| `switchCameraDevice(deviceId)` | 切到指定设备 |

```typescript
const cams = await meeting.getDevices(DeviceKind.videoInput);
meeting.switchCameraDevice(cams[1].deviceId);
```

<Note>
这两个是**原地换设备、不重建轨道**，所以不需要重新发布 —— 比直接用 SRTC 的
`changeDeviceId` 少一层心智负担。
</Note>

---

## 音频输出路由

### 两种设置，优先级不同

| | 接口 | 生效范围 |
| --- | --- | --- |
| **持久设置** | `defaultAudioRoute`（读写属性） | 长期有效，外设拔出后按它回落 |
| **临时设置** | `setAudioRoute(target)` | 本次通话中，**优先级更高** |

```typescript
import { AudioRouteTarget } from 'srtc';

// 入会前：视频会议默认外放
meeting.defaultAudioRoute = AudioRouteTarget.speaker;

// 通话中用户点了听筒
meeting.setAudioRoute(AudioRouteTarget.earpiece);

// 撤销临时设置，回到持久设置
meeting.clearAudioRouteOverride();
```

### 状态查询

| 属性 / 方法 | 类型 | 说明 |
| --- | --- | --- |
| `currentAudioRoute` | `AudioRoute` | **实际**在用的路由（五态，含蓝牙 / 有线） |
| `effectiveAudioRouteTarget` | `AudioRouteTarget` | 当前生效的目标（两态） |
| `audioRouteOverride` | `AudioRouteTarget \| undefined` | 有临时设置时非空 |
| `defaultAudioRoute` | `AudioRouteTarget` | 持久设置 |
| `isExternalAudioRouteActive` | `boolean` | 蓝牙 / 有线是否在用 |
| `availableAudioRoutes()` | `AudioRouteInfo[]` | 可用路由清单 |

<Note>
**判断"免提"按钮的选中态用 `effectiveAudioRouteTarget`**，不是 `defaultAudioRoute` ——
后者在有临时设置时不代表当前状态。
</Note>

### 为什么可切换目标只有两个

```
AudioRoute        speaker / earpiece / bluetooth / wired / other   ← 只读，五态
AudioRouteTarget  speaker / earpiece                               ← 可切换，两态
```

**外接设备由系统接管。** SDK 能上报"你现在走蓝牙"，但不能主动切到某个具体外设 ——
那是系统的职责。

<Warning>
**收到 `onAudioRouteChange` 时不要在回调里再切回去。**

用户插耳机 → 系统切到 `wired` → 你的回调里又 `setAudioRoute(speaker)` →
系统再切回……声音会在两个设备间反复跳。正确做法是更新 UI，把选择权交给用户。
</Warning>

### 扬声器快捷开关

```typescript
setSpeakerOutputEnabled(enabled: boolean): void
```

等价于在 `speaker` 与 `earpiece` 之间切，用于"免提"按钮。

---

## 系统通话状态

来电会抢走音频通道。监听 `onCallStateChange`：

```typescript
onCallStateChange: (meeting, data) => {
  // data.state / data.previousState，类型 AudioCallState
}
```

`AudioCallState`：`unknown` / `dialing` / `incoming` / `connected` / `disconnected`。

+ `incoming` / `connected`：提示"通话中已静音"
+ `disconnected`：恢复

---

### 相关阅读

+ [音频路由](/zh/meeting/harmony/advanced/audio-routing) —— 完整场景与坑
+ [设备管理](/zh/meeting/harmony/advanced/device-management)
+ [媒体控制接口](/zh/meeting/harmony/api-reference/media-control)
