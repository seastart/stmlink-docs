---
title: "MeetingCameraDeviceEvent"
description: "接收进程共享摄像头列表变化、设备断开与运行错误"
---

`MeetingCameraDeviceEvent` 是不绑定具体会议的 Engine 级摄像头设备监听，通过 `MeetingEngine.cameraDeviceEvent` 注册。可继承 `MeetingCameraDeviceSimpleEvent` 按需覆写。

## 使用说明

+ 该事件覆盖进程共享的 Camera2 设备变化，会前和会中使用同一监听。

+ 回调保持设备层实际来源线程，更新 UI 前应切换到主线程。
+ 列表变化回调提供变化后的完整列表，不是增量列表。

## 接口方法

### onCameraDeviceListChanged(devices)

```kotlin
fun onCameraDeviceListChanged(devices: List<CameraDeviceCapability>)
```

方法说明：系统可用摄像头完整列表发生变化。

参数说明：

| 参数 | 说明 |
| --- | --- |
| `devices` | 变化后的完整摄像头能力列表。 |

返回值说明：无（`Unit`）。

### onCameraDeviceDisconnected(cameraId)

```kotlin
fun onCameraDeviceDisconnected(cameraId: String)
```

方法说明：指定摄像头与系统物理断开或不再可用。

参数说明：

| 参数 | 说明 |
| --- | --- |
| `cameraId` | 失效的 Camera2 设备 ID。 |

返回值说明：无（`Unit`）。

### onCameraDeviceError(cameraId, errorCode, message)

```kotlin
fun onCameraDeviceError(
    cameraId: String,
    errorCode: Int,
    message: String?
)
```

方法说明：指定摄像头在采集过程中发生运行错误。

参数说明：

| 参数 | 说明 |
| --- | --- |
| `cameraId` | 发生错误的设备 ID。 |
| `errorCode` | SRTC 或系统来源错误码。 |
| `message` | 可空诊断信息。 |

返回值说明：无（`Unit`）。
