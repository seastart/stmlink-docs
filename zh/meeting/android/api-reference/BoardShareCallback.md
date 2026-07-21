---
title: "BoardShareCallback"
description: "Android SMeeting 会议 SDK BoardShareCallback 接口参考"
---

说明：`BoardShareCallback` 是白板共享结果回调接口，用于反馈发起白板共享的成功或失败。

## 回调方法

### onSucceed(whiteBoard)
```kotlin
fun onSucceed(whiteBoard: String)
```
方法说明：发起白板共享成功回调。  
参数说明：
- `whiteBoard`：`String`，白板共享信息。
返回值说明：无（`Unit`）。

### onFail(code, errorMsg, showMsg)
```kotlin
fun onFail(code: Int, errorMsg: String?, showMsg: String?)
```
方法说明：发起白板共享失败回调。  
参数说明：
- `code`：`Int`，错误码。
- `errorMsg`：`String?`，技术错误信息。
- `showMsg`：`String?`，面向用户的提示信息。
返回值说明：无（`Unit`）。
