---
title: "设备管理"
description: "枚举摄像头与麦克风、切换设备、热插拔监听与设备选择器"
---

会议 SDK 在引擎上包了一层设备接口。音频**输出路由**是另一套，
见[音频路由](/zh/meeting/harmony/advanced/audio-routing)。

---

### 枚举

```typescript
import { DeviceKind, DeviceInfo } from 'srtc';

const cams: DeviceInfo[] = await meeting.getDevices(DeviceKind.videoInput);
const mics: DeviceInfo[] = await meeting.getDevices(DeviceKind.audioInput);
const all: DeviceInfo[] = await meeting.getDevices();

// 读缓存，不触发系统查询
const cached: DeviceInfo[] = meeting.cachedDevices(DeviceKind.videoInput);
```

`DeviceInfo` 字段：`deviceId`、`name`、`kind`、`isDefault`。

<Note>
**做设备下拉框用 `cachedDevices()`** —— 它不会每次渲染都去问系统。
配合热插拔事件刷新即可。
</Note>

---

### 切换摄像头

```typescript
meeting.switchCamera();                       // 前后置切换
meeting.switchCameraDevice(deviceId);         // 切到指定设备
```

<Note>
这两个是**原地换设备、不重建轨道**，所以不需要重新发布 ——
比直接用底层 SRTC 的 `changeDeviceId` 少一层心智负担
（那边换设备会换底层轨道，已发布的必须重新发布）。
</Note>

---

### 热插拔

```typescript
const delegate: SMeetingDelegate = {
  onDeviceAdd: (m, device: DeviceInfo) => {
    this.devices = m.cachedDevices();          // 建新数组赋值
    if (device.kind === DeviceKind.audioInput) {
      toast(`已接入 ${device.name}`);
    }
  },
  onDeviceRemove: (m, device: DeviceInfo) => {
    this.devices = m.cachedDevices();
  }
};

aboutToAppear(): void {
  this.meeting.delegates.add(delegate);
  this.meeting.startDeviceMonitoring();
}

aboutToDisappear(): void {
  this.meeting.stopDeviceMonitoring();
  this.meeting.delegates.remove(delegate);
}
```

<Warning>
`onDeviceAdd` / `onDeviceRemove` 的第二个参数**直接是 `DeviceInfo`**，
不是像其它事件那样的 `xxxEventData` 包装对象。
</Warning>

<Warning>
ArkTS 的 `@State` 只观测第一层赋值 —— 设备列表永远用「建新数组再整体赋值」，
不要 `push` / `splice` 原数组。
</Warning>

---

### 一个最小的设备选择器

```typescript
@State cams: DeviceInfo[] = [];
@State currentCamId: string = '';

async loadDevices(): Promise<void> {
  this.cams = await this.meeting.getDevices(DeviceKind.videoInput);
}

build() {
  Column() {
    ForEach(this.cams, (d: DeviceInfo) => {
      Row() {
        Text(d.name)
        if (d.isDefault) {
          Text('（默认）').fontSize(12)
        }
      }
      .onClick(() => {
        this.meeting.switchCameraDevice(d.deviceId);
        this.currentCamId = d.deviceId;
      })
    }, (d: DeviceInfo) => d.deviceId)
  }
}
```

---

### 实测的设备形态

一台 HUAWEI nova 12 Pro（HarmonyOS 6.1）上：

```
cameras: 2   后置 device/0（默认）、前置 device/1
mics:    1   Microphone (2)（默认）
speakers: 2
```

<Note>
**系统默认摄像头是后置。** 视频会议通常要显式用前置 ——
`requestOpenCamera()` 用的默认预设已经是前置（`CameraPosition.front`），
但如果你自己构造采集参数就要注意。
</Note>

<Warning>
**采集分辨率受设备档位限制，档位表因机型而异。** 底层会把请求宽高吸附到最近的档位，
所以实际尺寸可能与预设不同。读 `cameraTrack.captureWidth` / `captureHeight`
拿实际值。

这也是必须在 `UIAbility.onCreate` 里调 `SRTC.init(this.context)` 的原因 ——
没有 Context 就查不到档位表，分辨率会退化为"由底层自行吸附"。
</Warning>

---

### 权限

摄像头与麦克风是 `user_grant` 权限，除了在 `module.json5` 声明，
还必须在运行时申请：

```typescript
import { abilityAccessCtrl, common, Permissions } from '@kit.AbilityKit';

const perms: Permissions[] = [
  'ohos.permission.CAMERA',
  'ohos.permission.MICROPHONE'
];
await abilityAccessCtrl.createAtManager()
  .requestPermissionsFromUser(getContext(this) as common.UIAbilityContext, perms);
```

权限没给时 `requestOpenMic` / `requestOpenCamera` 会失败，
底层抛的是 `SRTCError` 的 `captureError`（`108018`）。

---

### 相关阅读

+ [设备与音频路由接口](/zh/meeting/harmony/api-reference/devices)
+ [音频路由](/zh/meeting/harmony/advanced/audio-routing)
+ [SRTC 设备管理](/zh/rtc/harmony/advanced/device-management) —— 底层接口
