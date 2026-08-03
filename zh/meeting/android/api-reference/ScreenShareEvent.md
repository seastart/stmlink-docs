---
title: "ScreenShareEvent"
description: "Android 录屏共享的状态变化回调（授权、开始、停止）"
---

说明：`ScreenShareEvent` 是录屏共享状态回调接口。

## 回调方法

### onScreenStateChanged(state, args)
```kotlin
fun onScreenStateChanged(state: ScreenRecordState, args: String?)
```
方法说明：录屏状态变化回调。  
参数说明：
- `state`：`ScreenRecordState`，录屏状态。
- `args`：`String?`，附加参数。
返回值说明：无（`Unit`）。
