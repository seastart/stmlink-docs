---
title: "RTCCameraDeviceEvent"
description: "Android Engine-global camera device events: camera list changes, physical disconnects, and capture runtime errors, registered with setRtcCameraDeviceEvent. Read when you need to react to camera hot-plugging or camera failures on Android."
---

Camera capture is shared by all channels, so device events are Engine-global events. Register them with `RTCEngine.setRtcCameraDeviceEvent(...)`; pass `null` to unbind. If you only care about some events, extend `RTCCameraDeviceSimpleEvent`.

```kotlin
interface RTCCameraDeviceEvent {
    fun onCameraDeviceListChanged(devices: List<CameraDeviceCapability>)
    fun onCameraDeviceDisconnected(cameraId: String)
    fun onCameraDeviceError(cameraId: String, errorCode: Int, message: String?)
}
```

| Callback | Description |
| --- | --- |
| `onCameraDeviceListChanged` | The list of cameras available on the system changed; the parameter is the full list after the change. |
| `onCameraDeviceDisconnected` | The specified Camera2 device was physically disconnected or is no longer available. |
| `onCameraDeviceError` | The specified device hit a runtime error during capture. |

This interface has been split out of `RTCMediaEvent`. It carries no channel parameter and isn't reported repeatedly when multiple channels publish the same camera track.
