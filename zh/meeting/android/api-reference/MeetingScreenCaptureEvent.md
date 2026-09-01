---
title: "MeetingScreenCaptureEvent"
description: "接收 Android 本地屏幕采集状态，不等同于服务端屏幕共享业务状态"
---

`MeetingScreenCaptureEvent` 接收本地屏幕采集对象的持续状态，通过 `MeetingEngine.screenCaptureEvent` 注册。可继承 `MeetingScreenCaptureSimpleEvent` 按需覆写。

## 使用说明

+ 本事件只描述 Android MediaProjection / SRTC 本地采集状态。会议里谁开始或停止共享，应监听 `MeetingRoomEvent.onRoomShareStart()` / `onRoomShareStop()`。
+ 回调保持屏幕采集链路的实际来源线程；收到终止或错误状态后，应用应同步清理共享 UI 和持有的 MediaProjection 资源。

## 接口方法

### onScreenCaptureStateChanged(state, message)

```kotlin
fun onScreenCaptureStateChanged(
    state: ScreenCaptureState,
    message: String?
)
```

方法说明：本地屏幕采集状态发生变化。

参数说明：

| 参数 | 说明 |
| --- | --- |
| `state` | SRTC 定义的屏幕采集状态，见 [SRTC 枚举](/zh/rtc/android/enums#screencapturestate)。 |
| `message` | 可空附加诊断信息。 |

返回值说明：无（`Unit`）。回调保持屏幕采集来源线程。
