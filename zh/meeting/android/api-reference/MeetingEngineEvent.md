---
title: "MeetingEngineEvent"
description: "接收无法归属到单次调用或当前会议的 Meeting Engine 全局运行错误"
---

`MeetingEngineEvent` 接收与 `MeetingEngine` 同生命周期的全局错误，通过 `MeetingEngine.engineEvent` 注册。只关心部分事件时可继承 `MeetingEngineSimpleEvent`。

## 使用说明

+ 该事件不绑定具体会议，适合承载无法归属到某次调用或当前会议的持续运行错误。

+ 初始化等一次性操作失败只通过对应结果回调返回，不会在这里重复通知。
+ 回调保持实际来源线程；SRTC 等上游有效错误码原样透传，Meeting 自产错误使用 `202xxx`。

## 接口方法

### onError(errorCode, message)

```kotlin
fun onError(errorCode: Int, message: String?)
```

方法说明：SRTC Engine 或 Meeting 全局运行过程发生错误。

参数说明：

| 参数 | 说明 |
| --- | --- |
| `errorCode` | 开放错误码空间中的实际错误码。 |
| `message` | 可空诊断信息，不属于 UI 文案契约。 |

返回值说明：无（`Unit`）。
