---
title: "ErrorEvent"
description: "Android SMeeting 会议 SDK ErrorEvent 接口参考"
---

说明：`ErrorEvent` 是错误事件回调接口，用于上报 token 失效、会控或流媒体连接断开等错误。

## 回调方法

### onError(code, msg)
```kotlin
fun onError(code: Int, msg: String)
```
方法说明：错误事件回调。  
参数说明：
- `code`：`Int`，错误码（会议层错误码范围为 `[200000,300000)`）。
- `msg`：`String`，错误信息。
返回值说明：无（`Unit`）。
