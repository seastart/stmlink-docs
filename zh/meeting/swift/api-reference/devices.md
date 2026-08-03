---
title: "外设"
description: "SMeeting Swift SDK 外设接口参考：设备枚举、麦克风切换与音频输出控制"
---

本页接口都挂在 `SMeeting` 上，**不要求在会议中**，登录后即可调用。使用说明见 [外设管理](/zh/meeting/swift/advanced/device-management)。

---

#### `getDevices(kind:)`

枚举系统设备。

```swift
let cameras = meeting.getDevices(kind: .videoInput)
```

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | :---: | --- |
| `kind` | `DeviceInfo.DeviceKind?` | 否 | 设备类型过滤：`.videoInput` / `.audioInput` / `.audioOutput`；不传返回全部 |

**返回值：** `[DeviceInfo]`，不抛错。

平台差异：

+ macOS 音频列表中包含一个指向系统默认输入 / 输出的虚拟设备
+ iOS 的音频输入返回的是可用输入路由（蓝牙、有线耳机、内置麦克风等）
+ iOS 不支持枚举音频输出，`kind: .audioOutput` 在 iOS 上返回空数组

---

#### `switchMic(deviceId:)`

切换麦克风输入。

```swift
try meeting.switchMic(deviceId: deviceId)
```

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | :---: | --- |
| `deviceId` | `String` | 是 | 目标设备 ID，取自 `getDevices(kind: .audioInput)` |

**返回值：** 无

**可能抛出：** 设备切换失败时抛出底层错误。

行为按当前状态自适应：

| 状态 | 行为 |
| --- | --- |
| 已开麦 | 切换正在采集的输入设备 |
| 未开麦（iOS） | 预选音频输入路由 |
| 未开麦（macOS） | 直接返回，不做任何事，也不报错 |

---

#### `setAudioOutput(deviceId:)`

选择音频输出设备。**仅 macOS 可用**。

```swift
try meeting.setAudioOutput(deviceId: deviceId)
```

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | :---: | --- |
| `deviceId` | `String` | 是 | 目标输出设备 ID，取自 `getDevices(kind: .audioOutput)` |

**返回值：** 无

**可能抛出：** 设备切换失败时抛出底层错误。

---

#### `setSpeakerOutputEnabled(_:)`

切换外放。**仅 iOS 可用**。

```swift
try meeting.setSpeakerOutputEnabled(true)
```

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | :---: | --- |
| `enabled` | `Bool` | 是 | `true` 强制外放；`false` 回到系统默认输出 |

**返回值：** 无

**可能抛出：** 设置失败时抛出底层错误。

---

### 设备事件

设备插拔通过 `SMeetingDelegate` 上报，见 [事件参考](/zh/meeting/swift/events#外设事件)：

+ `meeting(_:didAddDevice:)`
+ `meeting(_:didRemoveDevice:)`

---

### 相关页面

+ [外设管理](/zh/meeting/swift/advanced/device-management)
+ [媒体控制接口](/zh/meeting/swift/api-reference/media-control)
