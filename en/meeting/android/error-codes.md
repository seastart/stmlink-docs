---
title: "Error codes"
description: "Where SMeeting Android SDK errors come from (Meeting SDK, SRTC SDK, librtc, server, HTTP), the full list of 202xxx MeetingErrorCode constants, passed-through RTC camera errors, and how your app should handle them. Read this when handling onFailure / onError."
---

One-shot Meeting results and Engine error events all return:

```kotlin
fun onFailure(errorCode: Int, message: String?)
fun onError(errorCode: Int, message: String?)
```

`message` is for development diagnostics only and is not guaranteed to be suitable for showing to users. Your app should maintain user-facing text and localization based on `errorCode`.

## Error sources

The error code is an open-ended `Int` and doesn't contain only errors produced by Meeting:

| Source | Range or form | How it's handled |
| --- | --- | --- |
| Meeting SDK | `202000`–`202999` | Defined by `MeetingErrorCode` |
| SRTC SDK | Usually `102xxx` | The underlying original error code is kept |
| librtc | Defined by the underlying layer | The original error code is kept |
| Meeting server | Server business codes | Valid business codes are kept |
| HTTP | HTTP status code or a Meeting local network error | Handle according to the actual source |

So don't force callback error codes into a closed enum, and don't assume every error can be found in `MeetingErrorCode`.

## MeetingErrorCode

Fully qualified class name: `cn.seastart.meeting.error.MeetingErrorCode`

### General errors (202000–202099)

| Constant | Value | Description |
| --- | --- | --- |
| `UNDEFINED_ERROR` | `202000` | Final fallback error that can't be further identified or classified |
| `SDK_NOT_INITIALIZED` | `202001` | The Meeting SDK has not finished initializing |
| `SDK_NOT_READY` | `202002` | The RTC engine or a runtime state that Meeting requires is not ready yet |
| `INVALID_PARAMETER` | `202003` | Invalid parameter passed to a Meeting public API |
| `INVALID_RESPONSE_DATA` | `202004` | A successful upstream response is missing a required field or has an invalid field format |
| `TOKEN_INVALID` | `202005` | Meeting determined locally that the token is invalid |
| `TOKEN_EXPIRED` | `202006` | Meeting determined locally that the token has expired |

### Session errors (202100–202199)

| Constant | Value | Description |
| --- | --- | --- |
| `SESSION_ALREADY_ACTIVE` | `202101` | Tried to enter a meeting again while a Session is already entering or active |
| `SESSION_NOT_ACTIVE` | `202102` | There is currently no usable active Session |
| `ENTER_MEETING_CANCELLED` | `202103` | The meeting entry flow was explicitly canceled |
| `WAITING_ROOM_CONTEXT_MISSING` | `202104` | No valid meeting context when exiting the waiting room |
| `AUDIENCE_OPERATION_FORBIDDEN` | `202105` | An audience member called a restricted capability such as opening a device, sharing, or publishing |
| `SESSION_OPERATION_CANCELLED` | `202106` | The meeting it belongs to started ending before an in-meeting asynchronous operation completed |

### Media errors (202200–202299)

| Constant | Value | Description |
| --- | --- | --- |
| `CAMERA_OPEN_FAILED` | `202201` | Meeting failed to open the camera and there is no original RTC code to pass through |
| `MIC_OPEN_FAILED` | `202202` | Meeting failed to open the mic and there is no original RTC code to pass through |
| `SCREEN_PERMISSION_DENIED` | `202203` | Android screen recording permission was denied |
| `SCREEN_TRACK_UNAVAILABLE` | `202204` | The screen sharing flow failed to create a valid track |
| `WHITEBOARD_REQUEST_CANCELLED` | `202205` | The whiteboard sharing request was canceled |
| `WHITEBOARD_URL_MISSING` | `202206` | The whiteboard API succeeded but the response has no URL |
| `CLOUD_RECORD_CAPTURE_DISABLED` | `202207` | A course recording track was started without enabling the client-side cloud recording capture configuration |
| `LOCAL_TRACK_UNAVAILABLE` | `202208` | A local media track that Meeting needs doesn't exist and there is no more specific error |
| `REMOTE_TRACK_UNAVAILABLE` | `202209` | A remote media track that Meeting needs to subscribe to doesn't exist |
| `LOCAL_DEVICE_OPERATION_CANCELLED` | `202210` | A local device operation was canceled by a newer open, close, or release action |
| `LOCAL_DEVICE_CAPABILITY_UNSUPPORTED` | `202211` | The current SRTC capture pipeline doesn't support the requested local device capability |
| `LOCAL_DEVICE_OPERATION_IN_PROGRESS` | `202212` | The previous open transaction on the same local device hasn't finished; that operation reports the final state |

### IM errors (202300–202349)

| Constant | Value | Description |
| --- | --- | --- |
| `IM_ENABLE_CANCELLED` | `202301` | The network flow for enabling IM was canceled |
| `IM_TOKEN_MISSING` | `202302` | The successful IM grant response is missing the IM token |

### HTTP errors (202350–202399)

| Constant | Value | Description |
| --- | --- | --- |
| `HTTP_CLIENT_NOT_INITIALIZED` | `202351` | Meeting's internal HTTP client is not initialized yet |
| `NETWORK_ERROR` | `202352` | Local network transport failure such as DNS, connection, or being offline |
| `REQUEST_TIMEOUT` | `202353` | Local HTTP request timed out |
| `REQUEST_CANCELLED` | `202354` | The HTTP request was canceled and needs to be converted into a failure callback |
| `EMPTY_RESPONSE_BODY` | `202355` | The HTTP request succeeded but the response body is empty |
| `RESPONSE_PARSE_FAILED` | `202356` | An HTTP response exists but can't be converted into a public business result |

## RTC camera errors (passed through as is)

The following errors come from RTC `2.0.33`, take effect with Meeting `2.0.37`, and are not part of `MeetingErrorCode`. After a switch fails, capture is not guaranteed to continue; if target validation fails, the original capture may be kept. The SDK doesn't fall back automatically—your app decides the recovery strategy.

| RTC constant | Value | Description |
| --- | --- | --- |
| `CAMERA_FIRST_FRAME_TIMEOUT` | `102239` | Timed out waiting for the camera's first frame |
| `CAMERA_FORMAT_UNAVAILABLE` | `102242` | No capture format available |
| `CAMERA_OPEN_TIMEOUT` | `102243` | Timed out opening the camera |
| `CAMERA_SESSION_TIMEOUT` | `102244` | Timed out creating the camera session |

## Recommended handling

```kotlin
override fun onFailure(errorCode: Int, message: String?) {
    logger.error("Meeting failed: code=$errorCode, message=$message")

    val userMessage = when (errorCode) {
        MeetingErrorCode.TOKEN_EXPIRED -> "Your login has expired. Please log in again."
        MeetingErrorCode.SESSION_ALREADY_ACTIVE -> "A meeting is already in progress"
        MeetingErrorCode.SCREEN_PERMISSION_DENIED -> "Screen recording permission was not granted"
        else -> "Operation failed. Please try again later."
    }
    showToast(userMessage)
}
```

You can log both `errorCode` and `message`; the UI should use only text your app maintains itself.
