---
title: "MeetingMicDeviceEvent"
description: "Receive changes to the process-wide shared mic input device list and invalidation of the current device through MeetingEngine.micDeviceEvent, before and during the meeting. Read this when you show a mic picker or handle unplugged devices."
---

`MeetingMicDeviceEvent` is an Engine-level mic device listener that isn't bound to a specific meeting, registered through `MeetingEngine.micDeviceEvent`. You can extend `MeetingMicDeviceSimpleEvent` and override only what you need.

## Usage notes

+ This event covers changes to the process-wide shared audio input devices; the same listener is used before and during the meeting.

+ Callbacks stay on the actual source thread of the device layer; switch to the main thread before updating the UI.
+ After the current device becomes invalid, SRTC may fall back to another input automatically; your app should refresh the UI based on the subsequent device list.

## Methods

### onMicDeviceListChanged(devices)

```kotlin
fun onMicDeviceListChanged(devices: List<MicDeviceCapability>)
```

Description: The full list of mic input devices available on the system changed.

Parameters:

| Parameter | Description |
| --- | --- |
| `devices` | The full device capability list after the change. |

Returns: None (`Unit`).

### onMicDeviceInvalid(deviceId, reason)

```kotlin
fun onMicDeviceInvalid(deviceId: String, reason: String)
```

Description: The mic device used for current capture became invalid; SRTC falls back to an available input according to its own policy.

Parameters:

| Parameter | Description |
| --- | --- |
| `deviceId` | ID of the device that became invalid. |
| `reason` | Invalidation reason provided by the underlying layer. |

Returns: None (`Unit`).
