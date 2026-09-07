---
title: "设备管理"
description: "用 DeviceManager 枚举摄像头与麦克风、切换设备、处理热插拔"
---

`DeviceManager.shared` 是单例，管**输入设备的枚举与选择**。
音频**输出路由**（扬声器 / 听筒 / 蓝牙）是另一套，见[音频路由](/zh/rtc/harmony/advanced/audio-routing)。

---

### 枚举设备

```typescript
import { DeviceManager, DeviceInfo, DeviceKind } from 'srtc';

const dm: DeviceManager = DeviceManager.shared;

const cameras: DeviceInfo[] = await dm.cameras();
const mics: DeviceInfo[] = await dm.microphones();
const speakers: DeviceInfo[] = dm.speakers();          // 注意：同步方法
const all: DeviceInfo[] = await dm.getDevices();       // 也可按 kind 过滤
```

| 方法 | 返回 | 说明 |
| --- | --- | --- |
| `cameras()` | `Promise<DeviceInfo[]>` | 摄像头 |
| `microphones()` / `audioInputs()` | `Promise<DeviceInfo[]>` | 麦克风 |
| `speakers()` | `DeviceInfo[]` | 扬声器，**同步** |
| `getDevices(kind?)` | `Promise<DeviceInfo[]>` | 全部或按类别 |
| `refreshDevices()` | `Promise<DeviceInfo[]>` | 强制刷新缓存 |
| `cachedDevices(kind?)` | `DeviceInfo[]` | 读缓存，不触发查询 |

`DeviceInfo` 的字段：`deviceId`、`name`、`kind`、`isDefault`。

<Note>
UI 上做设备下拉框时用 `cachedDevices()` 更合适 —— 它不会每次渲染都去查系统。
配合下面的热插拔事件刷新缓存即可。
</Note>

---

### 切换摄像头

```typescript
// 前后置切换
camera.switchCamera();

// 切到指定设备
const cameras = await DeviceManager.shared.cameras();
camera.changeDeviceId(cameras[1].deviceId);
```

枚举出来的 `deviceId` 可以直接喂回采集参数，这条回路是设备切换能力的地基：

```typescript
import { defaultCameraCaptureOptions, CameraCaptureOptions } from 'srtc';

const opts: CameraCaptureOptions = defaultCameraCaptureOptions();
opts.deviceId = cameras[0].deviceId;
await camera.startCapture(opts);
```

---

### 切换麦克风

有两条路：

```typescript
// 1) 轨道级：切这一条轨道的输入设备
await channel.unpublishLocalAudioTrack(mic);
await mic.changeDeviceId(newDeviceId);
await channel.publishLocalAudioTrack(mic);

// 2) 全局偏好：影响之后创建的音频轨道
await DeviceManager.shared.setAudioInputDevice(newDeviceId);
const current = DeviceManager.shared.preferredAudioInputDeviceId;
DeviceManager.shared.clearAudioInputDevice();     // 回到系统默认
```

<Warning>
`changeDeviceId()` 会换一条底层轨道，**已发布的轨道必须重新发布**，
否则对端收到的还是旧设备的音频。详见[静音与停止发布](/zh/rtc/harmony/advanced/mute-vs-unpublish)。
</Warning>

---

### 输出设备

```typescript
DeviceManager.shared.setOutputDevice(deviceId);
DeviceManager.shared.setSpeakerOutputPreferred(true);          // true=扬声器，false=听筒
const onSpeaker = DeviceManager.shared.isSpeakerOutputPreferred;
```

<Note>
`setSpeakerOutputPreferred(true/false)` 与 `AudioRouteSession` 的
`defaultAudioRoute` 管的是同一件事的不同层次。做通话类 UI 建议统一用
`AudioRouteSession` —— 它区分"持久设置"与"通话中临时切换"，语义更清晰。
</Note>

---

### 热插拔

```typescript
import { DeviceManagerDelegate, DeviceInfo } from 'srtc';

const observer: DeviceManagerDelegate = {
  onDeviceAdd: (device: DeviceInfo) => {
    console.info(`接入 ${device.kind}: ${device.name}`);
  },
  onDeviceRemove: (device: DeviceInfo) => {
    console.info(`移除 ${device.kind}: ${device.name}`);
  }
};

DeviceManager.shared.delegates.add(observer);
DeviceManager.shared.startMonitoring();

// 页面退出时
DeviceManager.shared.stopMonitoring();
DeviceManager.shared.delegates.remove(observer);
```

`isMonitoring` 可以回读监听状态。

<Warning>
**`delegates` 是强引用，必须成对 `add` / `remove`。**

`DeviceManager.shared` 是**全局单例**，注册在它上面的 delegate 不摘除就是永久泄漏 ——
页面早就销毁了，回调还在往一个不该存在的对象上打。
</Warning>

比较两次枚举结果的差异可以用现成的工具函数：

```typescript
import { deviceListEquals, deviceListDiff } from 'srtc';

if (!deviceListEquals(prev, next)) {
  const diff = deviceListDiff(prev, next);
}
```

---

### 实测的设备形态

在一台 HUAWEI nova 12 Pro（HarmonyOS 6.1）上：

```
cameras count=2
  camera[0] id=device/0 name=Build_in Back (device/0)  kind=videoInput default=true
  camera[1] id=device/1 name=Build_in Front (device/1) kind=videoInput default=false
microphones count=1
  mic[0] id=2 name=Microphone (2) kind=audioInput default=true
speakers count=2
```

<Note>
**默认摄像头是后置。** 做视频通话通常要显式指定前置 ——
用 `CameraPosition.front`（`defaultCameraCaptureOptions()` 已经是前置），
或按 `deviceId` 指定。
</Note>

---

### 相关阅读

+ [音频路由](/zh/rtc/harmony/advanced/audio-routing) —— 输出路由是另一套
+ [静音与停止发布](/zh/rtc/harmony/advanced/mute-vs-unpublish)
+ [类型定义](/zh/rtc/harmony/types)
