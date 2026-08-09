---
title: "RTCMicDeviceEvent"
description: "Engine 全局麦克风输入设备事件，通知输入设备列表变化及当前采集设备失效"
---

麦克风采集由所有频道共享，因此输入设备事件属于 Engine 全局事件。通过 `RTCEngine.setRtcMicDeviceEvent(...)` 注册；传 `null` 解绑。只关心部分事件时可继承 `RTCMicDeviceSimpleEvent`。

## onMicDeviceListChanged(devices)

```kotlin
fun onMicDeviceListChanged(devices: List<MicDeviceCapability>)
```

系统可用麦克风输入设备发生变化，例如有线耳机、蓝牙或 USB 麦克风插拔。参数为变化后的完整设备列表。

## onMicDeviceInvalid(deviceId, reason)

```kotlin
fun onMicDeviceInvalid(deviceId: String, reason: String)
```

当前正在采集的输入设备失效。SDK 会尝试回落到系统默认输入并重建采集；`deviceId` 为本次设备句柄，`reason` 为失效原因。

输入设备字段见 [类型定义](/zh/rtc/android/types)，主动查询和切换见 [LocalMicTrack](/zh/rtc/android/api-reference/LocalMicTrack)。
