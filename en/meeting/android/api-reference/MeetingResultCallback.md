---
title: "Meeting result callbacks"
description: "The contract of MeetingResultCallback and MeetingValueResultCallback<T>: success and failure, callback threads, and error codes. Read this when handling the one-shot result of any asynchronous SMeeting Android API."
---

The Meeting SDK uses two kinds of one-shot result callbacks: `MeetingResultCallback` when there is no business return value, and `MeetingValueResultCallback<T>` when success needs to return an object.

## Usage notes

+ Each asynchronous call returns exactly one final state; it never both succeeds and fails.
+ Errors produced by Meeting itself are `202xxx`; valid error codes from SRTC, the server, or HTTP are passed through as is.

+ Callbacks stay on the thread they actually come from; the main thread is not guaranteed.
+ Messages for Meeting-produced errors are empty; RTC and backend messages pass through unchanged and may be null or empty. Provide localized text when no message is available.

## MeetingResultCallback

### onSuccess()

```kotlin
fun onSuccess()
```

Description: The operation completed successfully without a business value.

Parameters: None.

Returns: None (`Unit`).

### onFailure(errorCode, message)

```kotlin
fun onFailure(errorCode: Int, message: String?)
```

Description: The operation failed.

Parameters:

| Parameter | Description |
| --- | --- |
| `errorCode` | Open-ended integer error code from the actual error source. |
| `message` | Messages for Meeting-produced errors are empty; RTC and backend messages pass through unchanged and may be null or empty. Provide localized text when no message is available. |

Returns: None (`Unit`).

## MeetingValueResultCallback&lt;T&gt;

### onSuccess(value)

```kotlin
fun onSuccess(value: T)
```

Description: The operation completed successfully and returns a business value.

Parameters:

| Parameter | Description |
| --- | --- |
| `value` | The business object declared by the method signature, such as `MeetingEnterInfo`, `MeetingPage<T>`, or `RemoteVideoTrack`. |

Returns: None (`Unit`).

### onFailure(errorCode, message)

```kotlin
fun onFailure(errorCode: Int, message: String?)
```

Description: The operation failed; same semantics as `MeetingResultCallback.onFailure()`.

Parameters:

| Parameter | Description |
| --- | --- |
| `errorCode` | The actual error code. |
| `message` | Messages for Meeting-produced errors are empty; RTC and backend messages pass through unchanged and may be null or empty. Provide localized text when no message is available. |

Returns: None (`Unit`). See [Error codes](/en/meeting/android/error-codes).
