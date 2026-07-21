---
title: "Callback"
description: "Android SMeeting 会议 SDK Callback 接口参考"
---

说明：`Callback<T extends BaseBean>` 是通用请求结果回调抽象类，实现 `ApiImpl<T>`，用于承接请求生命周期与结果状态。

## 回调方法

### onStart()
```kotlin
override fun onStart()
```
方法说明：请求开始回调。  
参数说明：无。  
返回值说明：无（`Unit`）。

### onCancel()
```kotlin
override fun onCancel()
```
方法说明：请求取消回调。  
参数说明：无。  
返回值说明：无（`Unit`）。

### onSuccess(data)
```kotlin
override fun onSuccess(data: T)
```
方法说明：请求成功回调。  
参数说明：
- `data`：`T`，请求成功返回的数据对象（`T` 需继承 `BaseBean`）。
返回值说明：无（`Unit`）。

### onFailed(code, errorMsg, showMsg)
```kotlin
override fun onFailed(code: Int, errorMsg: String, showMsg: String)
```
方法说明：请求失败回调。  
参数说明：
- `code`：`Int`，错误码。
- `errorMsg`：`String`，技术错误信息（通常用于日志或排查）。
- `showMsg`：`String`，面向用户的提示信息。
返回值说明：无（`Unit`）。
