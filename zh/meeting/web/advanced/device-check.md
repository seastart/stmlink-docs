---
title: "设备检测（会前 / 会中预览）"
description: "在入会前或会中做摄像头、麦克风、扬声器检测：getDevices 枚举设备，requestOpenCamera / requestOpenMic 传 publish: false 只采集不推流，getVolume 读麦克风音量，isCameraOpened / isMicOpened 判断要不要关，扬声器用 <audio> + setSinkId 试听"
---

### 概述

入会前的设备检测页、会中的设置页，都需要「打开设备看一眼、听一下，但不推给其他人」。各项检测在 Web 会议层的做法：

| 检测项 | 做法 |
| --- | --- |
| 设备列表 | `getDevices(kind)` |
| 摄像头预览 | `requestOpenCamera(container, deviceId, preset, false, undefined, false)`（`publish: false`） |
| 麦克风音量 | `requestOpenMic(deviceId, preset, false, undefined, false)` 返回的轨道 `getVolume()` |
| 扬声器试听 | SDK 不提供接口，用 `<audio>` + `setSinkId` 自己播放测试音 |

`publish: false` 自 `0.3.5` 起提供：只采集、只预览，不请求会控、不发布、不发状态事件，会前会中都可以调用；主持人关闭设备、全员禁用也不影响只预览的轨。

---

### 设备列表

```typescript
const cameras = await meeting.getDevices("videoinput");
const microphones = await meeting.getDevices("audioinput");
const speakers = await meeting.getDevices("audiooutput");
```

浏览器在授权前不返回设备名称，所以设备名称为空时 SDK 会先申请一次摄像头 / 麦克风权限；不想触发授权弹窗时第二个参数传 `false`。

---

### 摄像头预览

```typescript
// 打开预览：最后一个参数 publish 传 false
const camTrack = await meeting.requestOpenCamera(previewEl, cameraId, undefined, false, undefined, false);

// 换摄像头：再调一次，传新的 deviceId
await meeting.requestOpenCamera(previewEl, newCameraId, undefined, false, undefined, false);

// 关闭预览
if (!meeting.isCameraOpened()) {
  await meeting.closeCamera();           // 只预览的才关
} else {
  camTrack.removePlayView(previewEl);    // 会议摄像头开着：只移除自己加的预览容器
}
```

+ **预览后决定开摄像头**：以默认的 `publish: true` 再调一次 `requestOpenCamera()`，会请求会控并发布**同一条轨**，不重新采集。
+ **会议摄像头已开着时打开预览**：`publish: false` 直接返回正在用的轨，并把传入的 `container` 追加为预览，不会再开一路采集。
+ **入会前用默认参数打开的摄像头**：入会后再调用一次 `requestOpenCamera()` 会补发布到会议。

---

### 麦克风音量

```typescript
const micTrack = await meeting.requestOpenMic(micId, undefined, false, undefined, false);

const timer = setInterval(() => {
  volumeBar.style.width = `${micTrack.getVolume()}%`;   // getVolume() 返回 0~100
}, 100);

// 检测结束
clearInterval(timer);
if (!meeting.isMicOpened()) {
  await meeting.closeMic();
}
```

+ 用 [`setAudioProcessor()`](/zh/meeting/web/advanced/deepfilternet) 设置的处理器（如 AI 降噪）在只采集时同样会挂上，可以直接听到、看到降噪后的效果。
+ 预览后决定开麦、会议麦克风已开着、入会前打开等情况，规则与摄像头相同；用 `isMicOpened()` 判断关不关。

---

### 扬声器试听

SDK 不提供播放测试音的接口，用浏览器的 `<audio>` 播放，并用 `setSinkId` 指定输出设备（部分浏览器不支持 `setSinkId`，此时只能用系统默认输出）：

```typescript
const audio = new Audio("/assets/test-tone.mp3");
if ("setSinkId" in audio) {
  await (audio as any).setSinkId(speakerId);
}
await audio.play();
```

选定的扬声器在会中播放远端声音时，通过 `toggleRemoteAudioMute(false, { deviceId: speakerId })` 生效。

---

### 相关页面

+ [SMeeting 接口](/zh/meeting/web/api-reference/SMeeting)
+ [AI 降噪](/zh/meeting/web/advanced/deepfilternet)
