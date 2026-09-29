---
title: "MeetingEngineEvent"
description: "Receive global Meeting Engine runtime errors that can't be attributed to a single call or the current meeting, registered through MeetingEngine.engineEvent. Read this when handling ongoing SDK-level errors."
---

`MeetingEngineEvent` receives global errors that share the `MeetingEngine` lifecycle and is registered through `MeetingEngine.engineEvent`. If you only care about some of the events, extend `MeetingEngineSimpleEvent`.

## Usage notes

+ This event isn't bound to a specific meeting; it's meant for ongoing runtime errors that can't be attributed to a particular call or the current meeting.

+ Failures of one-shot operations such as initialization are returned only through the corresponding result callback and aren't reported here again.
+ Callbacks stay on the actual source thread; valid error codes from upstream layers such as SRTC are passed through as is, and errors produced by Meeting itself use `202xxx`.

## Methods

### onError(errorCode, message)

```kotlin
fun onError(errorCode: Int, message: String?)
```

Description: A global runtime error occurred in the SRTC Engine or Meeting.

Parameters:

| Parameter | Description |
| --- | --- |
| `errorCode` | The actual error code in the open-ended error code space. |
| `message` | Nullable diagnostic information; not part of the UI text contract. |

Returns: None (`Unit`).
