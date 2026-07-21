---
title: "EnableImCallback"
description: "Android SMeeting 会议 SDK EnableImCallback 接口参考"
---

说明：`EnableImCallback` 是启动即时通讯结果回调接口。

## 回调方法

### onSucceed(uid, sid)
```kotlin
fun onSucceed(uid: String, sid: String)
```
方法说明：启动即时通讯成功回调。  
参数说明：
- `uid`：`String`，当前用户 uid。
- `sid`：`String`，当前会话 sid。
返回值说明：无（`Unit`）。

### onFail(code, msg)
```kotlin
fun onFail(code: Int, msg: String)
```
方法说明：启动即时通讯失败回调。  
参数说明：
- `code`：`Int`，错误码。
- `msg`：`String`，错误信息。
返回值说明：无（`Unit`）。
