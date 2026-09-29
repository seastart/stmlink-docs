---
title: "MeetingScreenCaptureEvent"
description: "Receive the Android local screen capture state (MediaProjection / SRTC) through MeetingEngine.screenCaptureEvent. It is not the server-side screen sharing state; read this when you need to clean up sharing UI after capture stops or fails."
---

`MeetingScreenCaptureEvent` receives the ongoing state of the local screen capture object and is registered through `MeetingEngine.screenCaptureEvent`. You can extend `MeetingScreenCaptureSimpleEvent` and override only what you need.

## Usage notes

+ This event only describes the Android MediaProjection / SRTC local capture state. To know who starts or stops sharing in the meeting, listen to `MeetingRoomEvent.onRoomShareStart()` / `onRoomShareStop()`.
+ Callbacks stay on the actual source thread of the screen capture pipeline; after receiving a terminated or error state, your app should clean up the sharing UI and any MediaProjection resources it holds accordingly.

## Methods

### onScreenCaptureStateChanged(state, message)

```kotlin
fun onScreenCaptureStateChanged(
    state: ScreenCaptureState,
    message: String?
)
```

Description: The local screen capture state changed.

Parameters:

| Parameter | Description |
| --- | --- |
| `state` | Screen capture state defined by SRTC; see [SRTC enums](/en/rtc/android/enums#screencapturestate). |
| `message` | Nullable additional diagnostic information. |

Returns: None (`Unit`). The callback stays on the screen capture source thread.
