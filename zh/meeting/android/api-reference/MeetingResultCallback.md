---
title: "MeetingResultCallback"
description: "Meeting SDK 一次性操作结果回调，统一使用 errorCode 与开发诊断 message"
---

Meeting SDK 的一次性异步结果分为无返回值和有返回值两种。两种接口的失败契约一致，均不提供 `showMsg`。

## MeetingResultCallback

用于成功时不需要返回数据的操作。

```kotlin
interface MeetingResultCallback {
    fun onSuccess()
    fun onFail(errorCode: Int, message: String?)
}
```

## MeetingValueResultCallback&lt;T&gt;

用于成功时需要返回对象的操作，例如入会成功后返回 `MeetingSession`。

```kotlin
interface MeetingValueResultCallback<T> {
    fun onSuccess(value: T)
    fun onFail(errorCode: Int, message: String?)
}
```

## 失败参数

+ `errorCode`：Meeting 自产错误使用 `202xxx`；RTC、librtc、服务端或 HTTP 的有效错误码可能原样透传。
+ `message`：面向开发者的诊断信息，可能为空，不保证适合直接展示给用户。

应用应根据 `errorCode` 维护用户展示文案和国际化。错误来源和 Meeting 自产错误常量见 [错误码](/zh/meeting/android/error-codes)。
