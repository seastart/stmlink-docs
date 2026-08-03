---
title: "MeetingResultCallback"
description: "会控类操作的成功/失败回调，不返回数据"
---

说明：`MeetingResultCallback` 是通用操作结果回调接口，用于反馈调用成功或失败。

## 回调方法

### onSuccess()
```kotlin
fun onSuccess()
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
