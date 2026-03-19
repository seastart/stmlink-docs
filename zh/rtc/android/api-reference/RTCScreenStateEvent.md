---
title: "RTCScreenStateEvent"
description: "Android SRTC 音视频 SDK RTCScreenStateEvent 接口参考"
---

## 说明

`RTCScreenStateEvent` 为录屏状态回调接口。

## 接口方法

### onScreenRecordStateChanged(state, args)
```kotlin
fun onScreenRecordStateChanged(state: ScreenRecordState, args: String?)
```
方法说明：录屏状态变化回调。  
参数说明：
- `state`：`ScreenRecordState`，录屏状态（枚举定义请参考 `ScreenRecordState` 文档）。
- `args`：`String?`，扩展信息，可为 `null`。
返回值说明：无（`Unit`）。
