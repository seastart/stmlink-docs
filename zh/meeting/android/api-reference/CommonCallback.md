---
title: "CommonCallback"
description: "Android SMeeting 会议 SDK CommonCallback 接口参考"
---

说明：`CommonCallback` 是通用结果回调接口，用于反馈操作成功或失败。

## 回调方法

### onSucceed()
```kotlin
fun onSucceed()
```
方法说明：操作成功回调。  
参数说明：无。  
返回值说明：无（`Unit`）。

### onFail(code, errorMsg, showMsg)
```kotlin
fun onFail(code: Int, errorMsg: String?, showMsg: String?)
```
方法说明：操作失败回调。  
参数说明：
- `code`：`Int`，错误码。
- `errorMsg`：`String?`，技术错误信息。
- `showMsg`：`String?`，面向用户的提示信息。
返回值说明：无（`Unit`）。
