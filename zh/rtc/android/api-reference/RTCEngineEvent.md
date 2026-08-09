---
title: "RTCEngineEvent"
description: "与 RTCEngine 同生命周期的全局错误入口，用于接收阻断操作和无法归入单个频道业务事件的错误"
---

`RTCEngineEvent` 在 `RTCEngine.create(...)` 时传入，与 Engine 生命周期一致。它只承载 Engine 级错误；入会结果、成员、Track 和频道连接事件仍由对应频道的 `RTCClientEvent` 派发。

只需按需覆写时，可以继承 `RTCEngineSimpleEvent`。

## onError(channelId, errorCode, message)

```kotlin
fun onError(
    channelId: String?,
    errorCode: Int,
    message: String?
)
```

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `channelId` | `String?` | 错误所属频道；无法定位到具体频道时为 `null`。 |
| `errorCode` | `Int` | 原始错误码，可能来自 librtc、SDK 自产错误、后端或流媒体厂商。 |
| `message` | `String?` | 运行时错误现场信息，没有可用信息时为 `null`。 |

示例：

```kotlin
val engineEvent = object : RTCEngineSimpleEvent() {
    override fun onError(channelId: String?, errorCode: Int, message: String?) {
        val descriptor = RtcErrorCatalog.find(errorCode)
        Log.e(
            "SRTC",
            "channel=$channelId code=$errorCode name=${descriptor?.name} message=$message"
        )
    }
}
```

原 `RTCClientEvent.onError(...)` 与中间包装类型 `RTCEngineError` 已移除。错误码归属见 [错误码](/zh/rtc/android/error-codes)。
