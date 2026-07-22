---
title: "设备管理"
description: "使用 DeviceManager 枚举设备、切换摄像头和音频路由，并处理热插拔和中断恢复"
---

### 概述

Swift SDK 把设备管理抽成了 `DeviceManager.shared`，这意味着设备枚举、热插拔监听和音频会话中断处理，不需要业务层自己从零拼平台差异。

常见需求包括：

+ 枚举摄像头、麦克风、扬声器
+ 用户手动切换设备
+ 监听设备插拔
+ iOS 来电 / Siri 中断后的恢复

---

### 枚举设备

#### 枚举摄像头

```swift
let cameras = DeviceManager.shared.cameras()
```

#### macOS：枚举麦克风和扬声器

```swift
let microphones = DeviceManager.shared.microphones()
let speakers = DeviceManager.shared.speakers()
```

#### iOS：枚举音频路由

```swift
let routes = DeviceManager.shared.audioRoutes()
```

> iOS 下这里更准确的说法是“音频路由”，因为蓝牙耳机、有线耳机、扬声器切换本质上是 `AVAudioSession` 路由切换，不是桌面系统那种独立输入 / 输出设备模型。

#### 通用查询

如果你想统一写一层设备选择 UI，也可以用：

```swift
let allDevices = DeviceManager.shared.getDevices()
let camerasOnly = DeviceManager.shared.getDevices(kind: .videoInput)
```

---

### 切换摄像头

对已创建的 `LocalCameraTrack`，可以直接切换指定设备：

```swift
try await cameraTrack.changeDeviceId(deviceId)
```

iOS 前后摄切换可以直接用：

```swift
try await cameraTrack.switchCamera()
```

这里的关键点是：切换动作发生在轨道对象内部，业务层不需要重新创建一个新的 `LocalCameraTrack`。

---

### 切换麦克风或音频路由

#### macOS

```swift
try micTrack.changeDeviceId(deviceId)
```

#### iOS

```swift
try micTrack.changeDeviceId(deviceId)
```

虽然调用形式一样，但语义不同：

+ macOS：切换输入设备
+ iOS：切换音频输入 / 输出路由，比如蓝牙耳机、听筒、扬声器

如果你要显式切到 iOS 扬声器，常见的 `deviceId` 会是 `"speaker"`。

---

### macOS 切换扬声器

macOS 的输出设备切换走 `DeviceManager`：

```swift
try DeviceManager.shared.setOutputDevice(deviceId)
```

这和麦克风切换分开，是因为输出设备不绑定在 `LocalMicTrack` 上，而是绑定在底层音频模块的输出链路上。

---

### 监听设备变化

通过 `DeviceManagerDelegate` 注册监听：

```swift
final class DeviceState: DeviceManagerDelegate {
    init() {
        DeviceManager.shared.delegates.add(delegate: self)
    }

    func deviceManager(_ manager: DeviceManager, didAddDevice device: DeviceInfo) {
        print("device added:", device.name)
    }

    func deviceManager(_ manager: DeviceManager, didRemoveDevice device: DeviceInfo) {
        print("device removed:", device.name)
    }
}
```

推荐做法是：

+ 回调里只刷新本地设备列表状态
+ UI 层根据新的设备列表自动更新下拉框或选择器

---

### SDK 已做的自动恢复

Swift SDK 在内部已经处理了几类常见恢复逻辑：

+ 正在使用的摄像头被拔出时，尝试切到可用摄像头
+ macOS 正在使用的麦克风被拔出时，尝试切回默认输入
+ iOS 音频会话被来电等中断后，按条件恢复
+ iOS 前后台切换时，摄像头采集可在回前台后恢复

这意味着业务层通常不需要自己重建一整套容错逻辑，但仍然建议：

+ 把错误信息展示给用户
+ 在设备列表变化后刷新 UI
+ 不要缓存过期的 `deviceId`

---

### 业务层推荐写法

可以参考 `rtc-swift` Demo 里的思路：

+ 页面初始化时调用 `refreshDeviceList()`
+ 保存当前选中的 `deviceId`
+ 设备变化后，如果原来的 `deviceId` 不存在了，自动回退到默认设备

这一点很重要，因为热插拔场景里“旧设备 ID 仍然留在本地状态里”是很多切换失败问题的根源。
