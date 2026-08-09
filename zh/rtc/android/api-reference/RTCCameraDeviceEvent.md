---
title: "RTCCameraDeviceEvent"
description: "Engine 全局摄像头设备事件，通知设备列表变化、物理断开和采集运行时错误"
---

摄像头采集由所有频道共享，因此设备事件属于 Engine 全局事件。通过 `RTCEngine.setRtcCameraDeviceEvent(...)` 注册；传 `null` 解绑。只关心部分事件时可继承 `RTCCameraDeviceSimpleEvent`。

```kotlin
interface RTCCameraDeviceEvent {
    fun onCameraDeviceListChanged(devices: List<CameraDeviceCapability>)
    fun onCameraDeviceDisconnected(cameraId: String)
    fun onCameraDeviceError(cameraId: String, errorCode: Int, message: String?)
}
```

| 回调 | 说明 |
| --- | --- |
| `onCameraDeviceListChanged` | 系统可用摄像头列表发生变化，参数为变化后的完整列表。 |
| `onCameraDeviceDisconnected` | 指定 Camera2 设备物理断开或不再可用。 |
| `onCameraDeviceError` | 指定设备在采集期间发生运行时错误。 |

该接口已从 `RTCMediaEvent` 中独立出来，不携带频道参数，也不会因多个频道发布同一摄像头 Track 而重复回调。
