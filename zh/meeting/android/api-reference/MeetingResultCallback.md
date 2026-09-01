---
title: "Meeting 结果回调"
description: "MeetingResultCallback 与 MeetingValueResultCallback 的成功、失败、线程和错误码契约"
---

Meeting SDK 使用两类一次性结果回调：无业务返回值时使用 `MeetingResultCallback`，成功需要返回对象时使用 `MeetingValueResultCallback<T>`。

## 使用说明

+ 每次异步调用只返回一个最终状态，不会同时成功和失败。
+ Meeting 自产错误为 `202xxx`；SRTC、服务端或 HTTP 的有效错误码原样透传。

+ 回调保持实际来源线程，不保证主线程。
+ `message` 面向开发诊断，不属于稳定的用户展示文案契约。

## MeetingResultCallback

### onSuccess()

```kotlin
fun onSuccess()
```

方法说明：不携带业务值的操作成功完成。

参数说明：无。

返回值说明：无（`Unit`）。

### onFailure(errorCode, message)

```kotlin
fun onFailure(errorCode: Int, message: String?)
```

方法说明：操作失败。

参数说明：

| 参数 | 说明 |
| --- | --- |
| `errorCode` | 实际错误来源的开放整数错误码。 |
| `message` | 可空诊断信息，仅用于日志和排障。 |

返回值说明：无（`Unit`）。

## MeetingValueResultCallback&lt;T&gt;

### onSuccess(value)

```kotlin
fun onSuccess(value: T)
```

方法说明：操作成功完成并返回业务值。

参数说明：

| 参数 | 说明 |
| --- | --- |
| `value` | 方法签名声明的业务对象，例如 `MeetingEnterInfo`、`MeetingPage<T>` 或 `RemoteVideoTrack`。 |

返回值说明：无（`Unit`）。

### onFailure(errorCode, message)

```kotlin
fun onFailure(errorCode: Int, message: String?)
```

方法说明：操作失败，语义与 `MeetingResultCallback.onFailure()` 相同。

参数说明：

| 参数 | 说明 |
| --- | --- |
| `errorCode` | 实际错误码。 |
| `message` | 可空诊断信息。 |

返回值说明：无（`Unit`）。详见[错误码](/zh/meeting/android/error-codes)。
