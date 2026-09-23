---
title: "MeetingMicDeviceEvent"
description: "接收进程共享麦克风输入设备列表变化与当前设备失效事件"
---

`MeetingMicDeviceEvent` 是不绑定具体会议的 Engine 级麦克风设备监听，通过 `MeetingEngine.micDeviceEvent` 注册。可继承 `MeetingMicDeviceSimpleEvent` 按需覆写。

## 使用说明

+ 该事件覆盖进程共享的音频输入设备变化，会前和会中使用同一监听。

+ 回调保持设备层实际来源线程，更新 UI 前应切换到主线程。
+ 当前设备失效后 SRTC 可能自动回落到其他输入，应用应结合后续设备列表刷新界面。

## 接口方法

### onMicDeviceListChanged(devices)

```kotlin
fun onMicDeviceListChanged(devices: List<MicDeviceCapability>)
```

方法说明：系统可用麦克风输入设备完整列表发生变化。

参数说明：

| 参数 | 说明 |
| --- | --- |
| `devices` | 变化后的完整设备能力列表。 |

返回值说明：无（`Unit`）。

### onMicDeviceInvalid(deviceId, reason)

```kotlin
fun onMicDeviceInvalid(deviceId: String, reason: String)
```

方法说明：当前采集使用的麦克风设备失效，SRTC 将按自身策略回落到可用输入。

参数说明：

| 参数 | 说明 |
| --- | --- |
| `deviceId` | 失效设备 ID。 |
| `reason` | 底层提供的失效原因。 |

返回值说明：无（`Unit`）。
