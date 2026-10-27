---
title: "Error codes"
description: "Android SRTC error codes: mapped librtc StatusCode values, SDK error domains, callback messages, the 2.0.35-to-2.0.36 code mapping, and RtcErrorCatalog. Read when handling Android SDK errors or upgrading."
---

Error codes defined by the Android SRTC SDK fall into two categories:

+ `StatusCode`: Android error codes mapped from local librtc status codes.
+ `cn.seastart.rtc.error`: `102xxx` error codes with unified semantics produced by the Android SDK itself.

Callback error codes use `Int`. Local librtc errors are mapped to Android `102xxx` codes; backend business codes retain their original values. HTTP library and media streaming vendor errors may still have other values, so handle unknown error codes as a fallback.

## Error message `message`

Starting with 2.0.36, `RTCClientEvent.onJoinFailed(...)` and `RTCResultListener.onFail(...)` include a `message: String` parameter. When a backend error has a message available, `message` may contain the text returned by the backend. Use [`RTCEngine.setLanguage(...)`](/en/rtc/android/api-reference/RTCEngine) to set the request language; the actual message depends on the backend response. With `RtcLanguage.SYSTEM`, requests follow the system language.

SDK-produced errors and local librtc errors have an empty `message`; diagnostic details are only used in logs. Backend error codes and messages pass through unchanged based on their source, not their numeric range. A non-null String callback converts a null backend message to an empty string without generating text. Your app can map codes to localized text when no message is available.

Non-2xx HTTP responses retain their original status code and status message. Without an HTTP status code, request timeouts return `102007`, ordinary network failures return `102006`, and parsing failures, a missing `code`, or an empty response return `102011`, all with empty messages. Request cancellation still uses the cancellation callback.

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

`NotInitialized` and `MediaNotInitialized` share `102024`; `NotFound` and `RtcErrorCode.USER_NOT_FOUND` share `102204`.

## Unified error codes in 2.0.38: `RtcErrorCode`

Starting with 2.0.38, the seven domain-specific error code objects are replaced by `cn.seastart.rtc.error.RtcErrorCode`. All 40 constants are listed below. Update constant references and localized mappings when upgrading.

| Constant | Value | Description |
| --- | ---: | --- |
| `NOT_IN_CHANNEL` | `102001` | Not in the channel, or the channel has not started |
| `TRACK_NOT_FOUND` | `102003` | Track not found |
| `TOKEN_INVALID` | `102004` | Token is invalid |
| `ALREADY_JOINED` | `102005` | Already joined, or a conflicting operation is in progress |
| `CONNECTION_FAILED` | `102006` | Connection failed |
| `CONNECTION_TIMEOUT` | `102007` | Connection timed out |
| `MESSAGE_DECODE_FAILED` | `102011` | Failed to decode signaling message or response |
| `WEBRTC_ERROR` | `102012` | WebRTC or media network error |
| `SDP_NEGOTIATION_FAILED` | `102013` | SDP negotiation failed |
| `TRANSPORT_NOT_READY` | `102014` | Transport is not ready, retry later |
| `CAPTURE_FAILED` | `102018` | Capture failed (device busy, open failure or runtime error) |
| `DEVICE_NOT_FOUND` | `102021` | Device not found |
| `ENGINE_NOT_SUPPORTED` | `102022` | Operation not supported by the current stream engine |
| `ENGINE_DISCONNECTED` | `102023` | Native client or channel is closed |
| `INVALID_STATE` | `102024` | Operation not allowed in the current state |
| `INTERNAL_ERROR` | `102025` | SDK internal error |
| `CANCELLED` | `102026` | Operation canceled |
| `VIRTUAL_BACKGROUND_NOT_INSTALLED` | `102028` | Virtual background module is not installed |
| `VIRTUAL_BACKGROUND_MODEL_NOT_FOUND` | `102029` | Virtual background model not found or invalid |
| `INVALID_ARGUMENT` | `102031` | Invalid argument |
| `SCREEN_SHARE_DENIED` | `102039` | Screen share denied by user or system |
| `PERMISSION_DENIED` | `102042` | Device permission denied |
| `FORBIDDEN` | `102043` | Operation not allowed for the current role |
| `USER_NOT_FOUND` | `102204` | User not found in the channel |
| `CHANNEL_JOIN_NATIVE_EXCEPTION` | `102209` | Native join call threw an exception |
| `CHANNEL_RESOURCE_CREATE_FAILED` | `102212` | Failed to create channel resources |
| `CHANNEL_JOIN_DISCONNECTED` | `102213` | Disconnected while joining without a valid status code |
| `CAMERA_PERMISSION_DENIED` | `102231` | Camera permission denied |
| `CAMERA_SESSION_FAILED` | `102233` | Failed to create camera capture session |
| `CAMERA_REQUEST_FAILED` | `102234` | Camera capture request failed |
| `CAMERA_DISCONNECTED` | `102235` | Camera disconnected by the system |
| `CAMERA_FIRST_FRAME_TIMEOUT` | `102239` | Camera produced no first frame before timeout |
| `CAMERA_FORMAT_UNAVAILABLE` | `102242` | No usable capture format on the camera |
| `CAMERA_OPEN_TIMEOUT` | `102243` | Camera open timed out |
| `CAMERA_SESSION_TIMEOUT` | `102244` | Camera session configuration timed out |
| `MIC_PERMISSION_DENIED` | `102251` | Microphone (RECORD_AUDIO) permission denied |
| `MIC_FORMAT_UNSUPPORTED` | `102255` | Microphone capture format not supported |
| `SCREEN_CAPTURE_REQUEST_REJECTED` | `102270` | Screen capture request rejected in the current state |
| `SUBSCRIBE_FAILED` | `102301` | Subscription failed or refused by server |
| `OPERATION_IGNORED` | `102312` | Duplicate operation ignored |

### Migrating from 2.0.37

The permission meaning of the old `102001` moves to `102042`; the new `102001` means not in the channel. Do not reuse hard-coded messages for the old value. All new constants below belong to `RtcErrorCode`.

| Old constant | Old code | New constant | New code |
| --- | ---: | --- | ---: |
| `RtcCameraErrorCode.LEGACY_LACK_PERMISSION` | `102001` | `PERMISSION_DENIED` | `102042` |
| `RtcChannelErrorCode.TRACK_TYPE_INVALID` | `102002` | `INVALID_ARGUMENT` | `102031` |
| `RtcCommonErrorCode.SDK_NOT_INIT` | `102201` | `INVALID_STATE` | `102024` |
| `RtcChannelErrorCode.CHANNEL_NOT_START` | `102202` | `NOT_IN_CHANNEL` | `102001` |
| `RtcCommonErrorCode.STREAM_NOT_READY` | `102203` | `TRANSPORT_NOT_READY` | `102014` |
| `RtcErrorCode.USER_NOT_FOUND` | `102204` | `USER_NOT_FOUND` | `102204` |
| `RtcChannelErrorCode.TRACK_NOT_FOUND` | `102205` | `TRACK_NOT_FOUND` | `102003` |
| `RtcChannelErrorCode.STREAM_VENDOR_NOT_SUPPORTED` | `102206` | `ENGINE_NOT_SUPPORTED` | `102022` |
| `RtcChannelErrorCode.FORBIDDEN_FOR_AUDIENCE` | `102207` | `FORBIDDEN` | `102043` |
| `RtcChannelErrorCode.CHANNEL_ALREADY_EXISTS` | `102208` | `ALREADY_JOINED` | `102005` |
| `RtcChannelErrorCode.CHANNEL_JOIN_NATIVE_EXCEPTION` | `102209` | `CHANNEL_JOIN_NATIVE_EXCEPTION` | `102209` |
| `RtcChannelErrorCode.CHANNEL_JOIN_PAYLOAD_INVALID` | `102210` | `MESSAGE_DECODE_FAILED` | `102011` |
| `RtcChannelErrorCode.CHANNEL_INFO_INVALID` | `102211` | `MESSAGE_DECODE_FAILED` | `102011` |
| `RtcChannelErrorCode.CHANNEL_RESOURCE_CREATE_FAILED` | `102212` | `CHANNEL_RESOURCE_CREATE_FAILED` | `102212` |
| `RtcChannelErrorCode.CHANNEL_JOIN_DISCONNECTED_WITHOUT_STATUS` | `102213` | `CHANNEL_JOIN_DISCONNECTED` | `102213` |
| `RtcCommonErrorCode.NATIVE_CLIENT_CLOSED` | `102214` | `ENGINE_DISCONNECTED` | `102023` |
| `RtcChannelErrorCode.NATIVE_CHANNEL_CLOSED` | `102215` | `ENGINE_DISCONNECTED` | `102023` |
| `RtcCameraErrorCode.CAMERA_DEVICE_NOT_FOUND` | `102230` | `DEVICE_NOT_FOUND` | `102021` |
| `RtcCameraErrorCode.CAMERA_PERMISSION_DENIED` | `102231` | `CAMERA_PERMISSION_DENIED` | `102231` |
| `RtcCameraErrorCode.CAMERA_OPEN_FAILED` | `102232` | `CAPTURE_FAILED` | `102018` |
| `RtcCameraErrorCode.CAMERA_SESSION_FAILED` | `102233` | `CAMERA_SESSION_FAILED` | `102233` |
| `RtcCameraErrorCode.CAMERA_REQUEST_FAILED` | `102234` | `CAMERA_REQUEST_FAILED` | `102234` |
| `RtcCameraErrorCode.CAMERA_DISCONNECTED` | `102235` | `CAMERA_DISCONNECTED` | `102235` |
| `RtcCameraErrorCode.CAMERA_RUNTIME_ERROR` | `102236` | `CAPTURE_FAILED` | `102018` |
| `RtcCameraErrorCode.CAMERA_STATE_INVALID` | `102237` | `INVALID_STATE` | `102024` |
| `RtcCameraErrorCode.CAMERA_FIRST_FRAME_TIMEOUT` | `102239` | `CAMERA_FIRST_FRAME_TIMEOUT` | `102239` |
| `RtcCameraErrorCode.VIRTUAL_BACKGROUND_MODEL_INVALID` | `102240` | `VIRTUAL_BACKGROUND_MODEL_NOT_FOUND` | `102029` |
| `RtcCameraErrorCode.VIRTUAL_BACKGROUND_NOT_INSTALL` | `102241` | `VIRTUAL_BACKGROUND_NOT_INSTALLED` | `102028` |
| `RtcCameraErrorCode.CAMERA_FORMAT_UNAVAILABLE` | `102242` | `CAMERA_FORMAT_UNAVAILABLE` | `102242` |
| `RtcCameraErrorCode.CAMERA_OPEN_TIMEOUT` | `102243` | `CAMERA_OPEN_TIMEOUT` | `102243` |
| `RtcCameraErrorCode.CAMERA_SESSION_TIMEOUT` | `102244` | `CAMERA_SESSION_TIMEOUT` | `102244` |
| `RtcMicErrorCode.MIC_DEVICE_NOT_FOUND` | `102250` | `DEVICE_NOT_FOUND` | `102021` |
| `RtcMicErrorCode.MIC_PERMISSION_DENIED` | `102251` | `MIC_PERMISSION_DENIED` | `102251` |
| `RtcMicErrorCode.MIC_OPEN_FAILED` | `102252` | `CAPTURE_FAILED` | `102018` |
| `RtcMicErrorCode.MIC_READ_FAILED` | `102253` | `CAPTURE_FAILED` | `102018` |
| `RtcMicErrorCode.MIC_STATE_INVALID` | `102254` | `INVALID_STATE` | `102024` |
| `RtcMicErrorCode.MIC_FORMAT_UNSUPPORTED` | `102255` | `MIC_FORMAT_UNSUPPORTED` | `102255` |
| `RtcScreenErrorCode.SCREEN_CAPTURE_OPERATION_REJECTED` | `102270` | `SCREEN_CAPTURE_REQUEST_REJECTED` | `102270` |
| `RtcStreamErrorCode.ERROR_PARAM_ILLEGAL` | `102310` | `INVALID_ARGUMENT` | `102031` |
| `RtcStreamErrorCode.ERROR_OPERATION_CANCEL` | `102311` | `CANCELLED` | `102026` |
| `RtcStreamErrorCode.ERROR_OPERATION_IGNORE` | `102312` | `OPERATION_IGNORED` | `102312` |
| `RtcStreamErrorCode.ERROR_ABOUT_SDP_OPERATION` | `102313` | `SDP_NEGOTIATION_FAILED` | `102013` |
| `RtcStreamErrorCode.ERROR_SUBSCRIBE_REFUSE` | `102314` | `SUBSCRIBE_FAILED` | `102301` |
| `RtcHttpErrorCode.HTTP_NOT_INITIALIZED` | `102350` | `INVALID_STATE` | `102024` |
| `RtcHttpErrorCode.HTTP_INVALID_ARGUMENT` | `102351` | `INVALID_ARGUMENT` | `102031` |
| `RtcHttpErrorCode.HTTP_NETWORK_ERROR` | `102352` | `CONNECTION_FAILED` | `102006` |
| `RtcHttpErrorCode.HTTP_RESPONSE_INVALID` | `102353` | `MESSAGE_DECODE_FAILED` | `102011` |

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
| `defaultMessage` | `String` | Default description for diagnostics only; not returned as the message for SDK-produced errors. |
| `recoverable` | `Boolean` | Whether the caller can recover by retrying or correcting the state. |

`RtcErrorCatalog.all` returns descriptors for all errors produced by the current SDK. `RtcErrorModule` domains and their reserved ranges:

| Domain | Code range |
| --- | --- |
| `COMMON` | `102000..102099` |
| `CHANNEL` | `102200..102229` |
| `CAMERA` | `102230..102249` |
| `MIC` | `102250..102269` |
| `SCREEN` | `102270..102299` |
| `STREAM` | `102300..102349` |

Call `RtcErrorModule.owns(code)` to check whether an SDK-produced error falls within that domain's reserved range; this is not the same as checking whether the error is formally defined in `RtcErrorCatalog`.

## Callback handling recommendations

+ `RTCClientEvent.onJoinFailed(channel, statusCode, message)`: handle join failures.
+ `RTCResultListener.onFail(code, message)`: handle failures of specific asynchronous operations.
+ `RTCEngineEvent.onError(channelId, errorCode, message)`: handle blocking errors from Engine operations, and global errors.
+ `RTCClientEvent.onDisconnected(channel, leaveReason, statusCode, message)`: handle unrecoverable channel disconnects.

When logging errors, keep the channel ID, the raw numeric value, and the runtime `message` together. Don't rely only on enums or `RtcErrorCatalog`; otherwise new upstream errors the SDK doesn't recognize yet will be lost.
