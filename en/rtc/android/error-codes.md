---
title: "Error codes"
description: "Android SRTC error codes: mapped librtc StatusCode values, SDK error domains, callback messages, the 2.0.35-to-2.0.36 code mapping, and RtcErrorCatalog. Read when handling Android SDK errors or upgrading."
---

Error codes defined by the Android SRTC SDK fall into two categories:

+ `StatusCode`: Android error codes mapped from local librtc status codes.
+ `cn.seastart.rtc.error`: domain-specific `102xxx` error codes produced by the Android SDK itself.

Callback error codes use `Int`. Local librtc errors are mapped to Android `102xxx` codes; backend business codes retain their original values. HTTP library and media streaming vendor errors may still have other values, so handle unknown error codes as a fallback.

## Error message `message`

Starting with 2.0.36, `RTCClientEvent.onJoinFailed(...)` and `RTCResultListener.onFail(...)` include a `message: String` parameter. When a backend error has a message available, `message` may contain the text returned by the backend. Use [`RTCEngine.setLanguage(...)`](/en/rtc/android/api-reference/RTCEngine) to set the request language; the actual message depends on the backend response. With `RtcLanguage.SYSTEM`, requests follow the system language.

For errors produced by the SDK, local librtc errors, and failures to subscribe to remote tracks or Wangsu general streams, `message` is an empty string in these callbacks. Handle failures by error code; if you need to display a reason, provide a localized message for that code.

The `message` parameter of `RTCEngineEvent.onError(...)` is nullable. See [RTCEngineEvent](/en/rtc/android/api-reference/RTCEngineEvent).

## librtc status codes `StatusCode`

The table compares public enum values in 2.0.35 and 2.0.36. The new values apply starting with 2.0.36. If your app uses hard-coded old values, update them; prefer referencing enum constants.

| Enum name | 2.0.35 | 2.0.36 onward | Description |
| --- | ---: | ---: | --- |
| `OK` | `0` | `0` | Success. |
| `SystemError` | `100001` | `102025` | Internal system error. |
| `NotInitialized` | `100002` | `102024` | The native client isn't initialized. |
| `MediaNotInitialized` | `100003` | `102024` | The media module isn't initialized yet. |
| `ProtocolParsingError` | `100004` | `102011` | Protocol parsing error. |
| `Timeout` | `100005` | `102007` | The operation timed out. |
| `InvalidArgs` | `100006` | `102031` | Invalid arguments. |
| `Conflict` | `100007` | `102005` | Conflicting operation. |
| `SdkTokenInvalid` | `100008` | `102004` | The SDK token is invalid or has expired. |
| `NetError` | `100009` | `102006` | Signaling network error. |
| `MediaNetError` | `100010` | `102012` | Media network error. |
| `NotFound` | `100011` | `102204` | The target resource doesn't exist. |
| `UserCancelled` | `100012` | `102026` | The user canceled the operation. |

`NotInitialized` and `MediaNotInitialized` share `102024`; `NotFound` and `RtcChannelErrorCode.USER_NOT_FOUND` share `102204`.

## SDK common and channel errors

### `RtcCommonErrorCode`

| Constant | Value | Description |
| --- | ---: | --- |
| `SDK_NOT_INIT` | `102201` | The RTC SDK isn't initialized yet. |
| `STREAM_NOT_READY` | `102203` | The media streaming resource the operation depends on isn't ready yet. |
| `NATIVE_CLIENT_CLOSED` | `102214` | The native client held by the Kotlin layer has been closed. |

### `RtcChannelErrorCode`

| Constant | Value | Description |
| --- | ---: | --- |
| `TRACK_TYPE_INVALID` | `102002` | An unsupported track type was passed when publishing or unpublishing. |
| `CHANNEL_NOT_START` | `102202` | The target channel hasn't been joined successfully. |
| `USER_NOT_FOUND` | `102204` | The target user doesn't exist. |
| `TRACK_NOT_FOUND` | `102205` | The target track doesn't exist. |
| `STREAM_VENDOR_NOT_SUPPORTED` | `102206` | The current media streaming engine doesn't support this operation. |
| `FORBIDDEN_FOR_AUDIENCE` | `102207` | Audience users aren't allowed to publish local tracks. |
| `CHANNEL_ALREADY_EXISTS` | `102208` | The same channel already exists in the current Engine. |
| `CHANNEL_JOIN_NATIVE_EXCEPTION` | `102209` | An exception occurred while calling native join. |
| `CHANNEL_JOIN_PAYLOAD_INVALID` | `102210` | The data in the native join success callback can't be parsed. |
| `CHANNEL_INFO_INVALID` | `102211` | The native channel info is empty or invalid. |
| `CHANNEL_RESOURCE_CREATE_FAILED` | `102212` | Failed to create the channel objects or media streaming resources. |
| `CHANNEL_JOIN_DISCONNECTED_WITHOUT_STATUS` | `102213` | Disconnected while joining, and native provided no valid status code. |
| `NATIVE_CHANNEL_CLOSED` | `102215` | The native channel held by the Kotlin layer has been closed. |

## Capture errors

### `RtcCameraErrorCode`

| Constant | Value | Description |
| --- | ---: | --- |
| `LEGACY_LACK_PERMISSION` | `102001` | Kept for compatibility with the previously published permission error value; no longer used for new permission checks. |
| `CAMERA_DEVICE_NOT_FOUND` | `102230` | No available camera was found. |
| `CAMERA_PERMISSION_DENIED` | `102231` | The app doesn't have camera permission. |
| `CAMERA_OPEN_FAILED` | `102232` | Failed to open the camera. |
| `CAMERA_SESSION_FAILED` | `102233` | Failed to create the camera capture session. |
| `CAMERA_REQUEST_FAILED` | `102234` | Failed to send the camera capture request. |
| `CAMERA_DISCONNECTED` | `102235` | The camera disconnected while running. |
| `CAMERA_RUNTIME_ERROR` | `102236` | Camera runtime system error. |
| `CAMERA_STATE_INVALID` | `102237` | The operation violates the camera state machine constraints. |
| `CAMERA_FIRST_FRAME_TIMEOUT` | `102239` | The camera session started, but produced no first frame within the timeout. |
| `VIRTUAL_BACKGROUND_MODEL_INVALID` | `102240` | The virtual background person segmentation model is empty or invalid. |
| `VIRTUAL_BACKGROUND_NOT_INSTALL` | `102241` | The virtual background module isn't installed; call `installVirtualBackground` first. |
| `CAMERA_FORMAT_UNAVAILABLE` | `102242` | Camera devices exist in scope, but no capture format is available. |
| `CAMERA_OPEN_TIMEOUT` | `102243` | Opening the camera device timed out; it neither succeeded nor reported an error within the deadline. |
| `CAMERA_SESSION_TIMEOUT` | `102244` | The device opened, but configuring the capture session or sending the capture request timed out. |

### `RtcMicErrorCode`

| Constant | Value | Description |
| --- | ---: | --- |
| `MIC_DEVICE_NOT_FOUND` | `102250` | The requested microphone device wasn't found. |
| `MIC_PERMISSION_DENIED` | `102251` | The app doesn't have audio recording permission. |
| `MIC_OPEN_FAILED` | `102252` | Failed to open or start the microphone. |
| `MIC_READ_FAILED` | `102253` | The SDK detected that microphone reads failed or stalled. |
| `MIC_STATE_INVALID` | `102254` | The operation violates the microphone state machine constraints. |
| `MIC_FORMAT_UNSUPPORTED` | `102255` | The requested microphone capture format isn't supported. |

### `RtcScreenErrorCode`

| Constant | Value | Description |
| --- | ---: | --- |
| `SCREEN_CAPTURE_OPERATION_REJECTED` | `102270` | The current SDK state can't accept a new screen capture start request. |

## Media streaming and HTTP errors

### `RtcStreamErrorCode`

| Constant | Value | Description |
| --- | ---: | --- |
| `ERROR_PARAM_ILLEGAL` | `102310` | Invalid media streaming configuration parameters. |
| `ERROR_OPERATION_CANCEL` | `102311` | Pending operations in opposite directions canceled each other out. |
| `ERROR_OPERATION_IGNORE` | `102312` | A duplicate operation was ignored. |
| `ERROR_ABOUT_SDP_OPERATION` | `102313` | SDP creation, setting, or negotiation failed. |
| `ERROR_SUBSCRIBE_REFUSE` | `102314` | The RTC server rejected the subscription request. |

### `RtcHttpErrorCode`

| Constant | Value | Description |
| --- | ---: | --- |
| `HTTP_NOT_INITIALIZED` | `102350` | RTC HTTP capability isn't initialized yet. |
| `HTTP_INVALID_ARGUMENT` | `102351` | The SDK detected invalid HTTP request parameters. |
| `HTTP_NETWORK_ERROR` | `102352` | The HTTP request failed and there's no upstream error code to pass through. |
| `HTTP_RESPONSE_INVALID` | `102353` | The HTTP response is empty or can't be parsed. |

## Error catalog lookup

`RtcErrorCatalog.find(code)` looks up SDK-defined error descriptions by numeric value alone; it cannot identify an error's source. It returns `null` for unknown codes. `StatusCode.NotFound` and the SDK's `USER_NOT_FOUND` both have value `102204`, so looking up that value returns `USER_NOT_FOUND`.

```kotlin
val descriptor: RtcErrorDescriptor? = RtcErrorCatalog.find(errorCode)

descriptor?.let {
    Log.e(
        "SRTC",
        "code=${it.code} name=${it.name} module=${it.module} " +
            "recoverable=${it.recoverable} message=${it.defaultMessage}"
    )
}
```

`RtcErrorDescriptor` fields:

| Field | Type | Description |
| --- | --- | --- |
| `code` | `Int` | Stable six-digit SDK error code. |
| `name` | `String` | Stable English name, suitable for logging and monitoring. |
| `module` | `RtcErrorModule` | The domain the error belongs to. |
| `defaultMessage` | `String` | Default description without runtime context. |
| `recoverable` | `Boolean` | Whether the caller can recover by retrying or correcting the state. |

`RtcErrorCatalog.all` returns descriptors for all errors produced by the current SDK. `RtcErrorModule` domains and their reserved ranges:

| Domain | Code range |
| --- | --- |
| `LEGACY` | `102000..102099` |
| `COMMON` | `102200..102229` |
| `CHANNEL` | `102200..102229` |
| `CAMERA` | `102230..102249` |
| `MIC` | `102250..102269` |
| `SCREEN` | `102270..102289` |
| `STREAM` | `102300..102349` |
| `HTTP` | `102350..102379` |

`COMMON` and `CHANNEL` currently share a historical range, but each specific error code is globally unique.
Call `RtcErrorModule.owns(code)` to check whether an SDK-produced error falls within that domain's reserved range; this is not the same as checking whether the error is formally defined in `RtcErrorCatalog`.

## Callback handling recommendations

+ `RTCClientEvent.onJoinFailed(channel, statusCode, message)`: handle join failures.
+ `RTCResultListener.onFail(code, message)`: handle failures of specific asynchronous operations.
+ `RTCEngineEvent.onError(channelId, errorCode, message)`: handle blocking errors from Engine operations, and global errors.
+ `RTCClientEvent.onDisconnected(channel, leaveReason, statusCode, message)`: handle unrecoverable channel disconnects.

When logging errors, keep the channel ID, the raw numeric value, and the runtime `message` together. Don't rely only on enums or `RtcErrorCatalog`; otherwise new upstream errors the SDK doesn't recognize yet will be lost.
