---
title: "设备检测（会前 / 会中预览）"
description: "在入会前或会中做摄像头、麦克风、扬声器检测：枚举设备、requestOpenCamera 的 publish = false 只预览不推流、isCameraOpened 判断要不要关、麦克风音量只能在会中发布后读、扬声器走音频路由"
---

### 概述

入会前的设备检测页、会中的设置页，都需要「打开设备看一眼，但不推给其他人」。各项检测在鸿蒙会议层的做法：

| 检测项 | 做法 | 支持情况 |
| --- | --- | --- |
| 设备列表 | `getDevices(kind)` | 支持 |
| 摄像头预览 | `requestOpenCamera(preset, false, undefined, false)` | 会前会中都支持（1.6.0 起） |
| 麦克风音量 | `getLocalAudioLevel()` | 只能在会中开麦（已发布）后读 |
| 扬声器 | 外放 / 听筒切换，测试音由业务自己播 | 不能指定任意输出设备 |

---

### 设备列表

```typescript
import { DeviceKind, DeviceInfo } from 'srtc';

const cams: DeviceInfo[] = await meeting.getDevices(DeviceKind.videoInput);
const mics: DeviceInfo[] = await meeting.getDevices(DeviceKind.audioInput);
```

摄像头没有插拔事件，进检测页时重新调一次 `getDevices()`。详见[外设管理](/zh/meeting/harmony/advanced/device-management)。

---

### 摄像头预览

```typescript
import { cameraPreset720p, SRTCVideoView } from 'srtc';

// 只采集预览：不请求会控、不发布、不发摄像头状态事件，会中打开也不会推给其他人
const track = await meeting.requestOpenCamera(cameraPreset720p(), false, undefined, false);

// 渲染：SRTCVideoView({ track: meeting.cameraTrack, trackKey: track.id })

// 离开检测页：只关预览打开的；会中摄像头本来就开着（isCameraOpened）就别关
if (!meeting.isCameraOpened) {
  await meeting.closeCamera();
}
```

+ 摄像头已作为会议摄像头打开时，`publish = false` 直接返回正在用的轨，预览看到的就是正在发布的画面
+ 预览之后要正式开摄像头，调 `requestOpenCamera()`（默认 `publish = true`），会发布同一条轨、不重新采集
+ 主持人关摄像头 / 全员禁用不影响只预览的轨
+ 切设备用 `switchCameraDevice(deviceId)`，预览轨同样生效

---

### 麦克风音量

`getLocalAudioLevel()` 读的是发送统计，**只有会中开麦（轨道已发布）后才有值**，未开麦 / 不在会中返回 `undefined`。
所以鸿蒙会议层目前做不了「会前只采集不发布地测麦」，`requestOpenMic` 也没有 `publish` 参数。

```typescript
// 会中：开麦后按 ≤10Hz 轮询
await meeting.requestOpenMic();
const level: number | undefined = await meeting.getLocalAudioLevel();   // 0~1，线性
```

---

### 扬声器

鸿蒙不支持指定任意输出设备，只能在外放与听筒之间切换（`setSpeakerOutputEnabled` / 音频路由），蓝牙等外设交给系统。
试听测试音需要业务自己用系统播放器播一段音频。详见[音频路由](/zh/meeting/harmony/advanced/audio-routing)。

---

### 相关阅读

+ [媒体控制](/zh/meeting/harmony/advanced/media-control)
+ [媒体控制接口](/zh/meeting/harmony/api-reference/media-control)
