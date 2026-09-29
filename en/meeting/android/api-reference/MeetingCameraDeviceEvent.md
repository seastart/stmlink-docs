---
title: "MeetingCameraDeviceEvent"
description: "Receive changes to the process-wide shared camera list, device disconnections, and runtime errors through MeetingEngine.cameraDeviceEvent, before and during the meeting. Read this when you show a camera picker or handle camera failures."
---

`MeetingCameraDeviceEvent` is an Engine-level camera device listener that isn't bound to a specific meeting, registered through `MeetingEngine.cameraDeviceEvent`. You can extend `MeetingCameraDeviceSimpleEvent` and override only what you need.

## Usage notes

+ This event covers changes to the process-wide shared Camera2 devices; the same listener is used before and during the meeting.

+ Callbacks stay on the actual source thread of the device layer; switch to the main thread before updating the UI.
+ The list-change callback provides the full list after the change, not an incremental list.

## Methods

### onCameraDeviceListChanged(devices)

```kotlin
fun onCameraDeviceListChanged(devices: List<CameraDeviceCapability>)
```

Description: The full list of cameras available on the system changed.

Parameters:

| Parameter | Description |
| --- | --- |
| `devices` | The full camera capability list after the change. |

Returns: None (`Unit`).

### onCameraDeviceDisconnected(cameraId)

```kotlin
fun onCameraDeviceDisconnected(cameraId: String)
```

Description: The specified camera was physically disconnected from the system or is no longer available.

Parameters:

| Parameter | Description |
| --- | --- |
| `cameraId` | The Camera2 device ID that became invalid. |

Returns: None (`Unit`).

### onCameraDeviceError(cameraId, errorCode, message)

```kotlin
fun onCameraDeviceError(
    cameraId: String,
    errorCode: Int,
    message: String?
)
```

Description: The specified camera hit a runtime error during capture.

Parameters:

| Parameter | Description |
| --- | --- |
| `cameraId` | ID of the device where the error occurred. |
| `errorCode` | Error code from SRTC or the system. |
| `message` | Nullable diagnostic information. |

Returns: None (`Unit`).
