---
title: "外设管理"
description: "SMeeting Swift SDK 中摄像头、麦克风、扬声器的枚举与切换，以及设备插拔事件处理"
---

### 概述

外设相关的接口都挂在 `SMeetingEngine` 上，你不需要自己去处理 iOS 与 macOS 的平台差异：

| 能力 | 接口 | 平台 |
| --- | --- | --- |
| 枚举设备 | `getDevices(kind:)` | 通用 |
| 切换摄像头 | `switchCamera(deviceId:)` | 通用 |
| 切换麦克风 | `switchMic(deviceId:)` | 通用 |
| 选择音频输出设备 | `setAudioOutput(deviceId:)` | 仅 macOS |
| 切换外放开关 | `setSpeakerOutputEnabled(_:)` | 仅 iOS |

设备能力**不依赖会议状态**：登录后（甚至进入会议前）就可以枚举设备、监听插拔，方便你做「入会前设备检测」页面。

---

### 枚举设备

```swift
let cameras = meeting.getDevices(kind: .videoInput)
let microphones = meeting.getDevices(kind: .audioInput)
let speakers = meeting.getDevices(kind: .audioOutput)

let all = meeting.getDevices()   // 不传 kind 返回全部
```

返回的 `DeviceInfo` 包含 `deviceId`、`name`、`kind`、`isDefault`。

平台差异需要留意：

+ **macOS**：音频列表里会出现一个指向系统默认输入 / 输出的虚拟设备
+ **iOS 音频输入**：返回的是可用的音频输入路由（蓝牙、有线耳机、内置麦克风等）
+ **iOS 音频输出**：系统不提供枚举能力，`kind: .audioOutput` 在 iOS 上返回空数组 —— iOS 的输出控制是一个「是否外放」的布尔开关，见下文

---

### 切换摄像头

```swift
// 指定设备
try await meeting.switchCamera(deviceId: deviceId)

// iOS 前后摄互切
try await meeting.switchCamera()
```

摄像头未打开时调用会抛出 `SMeetingError.deviceError`。如果用户是在**未开摄像头**时先在下拉框里选好设备，建议把选择先记在业务状态里，等 `requestOpenCamera(deviceId:)` 时一起传进去。

---

### 切换麦克风

```swift
try meeting.switchMic(deviceId: deviceId)
```

这个方法不抛「未开麦」的错误，它按当前状态自适应：

+ **已开麦**：切换正在采集的输入设备
+ **未开麦（iOS）**：预选音频输入路由，例如入会前先选好蓝牙耳机
+ **未开麦（macOS）**：录音链路尚未启动，调用直接返回，不做任何事也不报错

---

### 音频输出

输出侧两个平台的能力模型不同，因此接口也拆开了。

#### macOS：选择输出设备

```swift
try meeting.setAudioOutput(deviceId: deviceId)
```

用于在内置扬声器、USB 声卡、蓝牙音箱等硬件之间选择。

#### iOS：外放开关

```swift
try meeting.setSpeakerOutputEnabled(true)   // 强制外放
try meeting.setSpeakerOutputEnabled(false)  // 回到系统默认输出（听筒 / 蓝牙 / 有线耳机）
```

iOS 上蓝牙、AirPlay 等具体输出路由由用户通过系统控制中心或 `AVRoutePickerView` 选择，应用无法直接指定。

要设定「长期默认走外放」，或需要读取当前实际路由、监听路由变化，用 [音频路由](/zh/meeting/swift/advanced/audio-routing) 那一套接口 —— `setSpeakerOutputEnabled(_:)` 与其中的 `setAudioRoute(_:)` 是同一机制的两种写法。

#### 与「扬声器静音」的区别

这两件事是正交的，不要混用：

| 目的 | 接口 |
| --- | --- |
| 要不要听到远端声音 | `toggleRemoteAudioMute(_:)` |
| 从哪个硬件出声 | `setAudioOutput(deviceId:)` / `setSpeakerOutputEnabled(_:)` |

---

### 监听设备插拔

设备变化通过 `SMeetingDelegate` 上报：

```swift
func meeting(_ meeting: SMeetingEngine, didAddDevice data: DeviceChangeEventData) {
    refreshDeviceList()
}

func meeting(_ meeting: SMeetingEngine, didRemoveDevice data: DeviceChangeEventData) {
    refreshDeviceList()
}
```

iOS 上耳机插拔、蓝牙连接 / 断开这类音频路由变化，也会以「设备」的形式通过这两个事件上报。

推荐做法：

+ 回调里只刷新设备列表状态，UI 层按新列表自动更新选择器
+ 当前选中的 `deviceId` 如果已经从列表里消失，回退到默认设备

```swift
func refreshDeviceList() {
    cameras = meeting.getDevices(kind: .videoInput)
    if let id = selectedCameraId, !cameras.contains(where: { $0.deviceId == id }) {
        selectedCameraId = nil    // 回退到默认
    }
}
```

> 正在使用的设备被拔出时，SDK 会自行降级到可用设备，你不需要重建整套容错逻辑，但仍应刷新 UI，避免界面上还显示着一个已经不存在的设备。

---

### 相关页面

+ [媒体控制](/zh/meeting/swift/advanced/media-control)
+ [接口文档 - 外设](/zh/meeting/swift/api-reference/devices)
