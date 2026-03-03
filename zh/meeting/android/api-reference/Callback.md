---
title: "Callback"
description: "Android SMeeting 会议 SDK Callback 接口参考"
---

结果回调，一般用于 HTTP 请求的结果回调

### onStart()
请求开始

```kotlin
public void onStart()
```kotlin

### onCancel()
请求取消

```kotlin
public void onCancel()
```

### onSuccess()
请求成功

```kotlin
public void onSuccess(T data)
```kotlin

参数

| data | 请求结果 |
| --- | --- |


### onFailed()
请求失败

```kotlin
public void onFailed(int code, String msg)
```

参数

| code | Int 类型，错误码 |
| --- | --- |
| msg | String 类型，错误信息 |


