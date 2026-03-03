---
title: "MeetingResultCallback"
description: "Android SMeeting 会议 SDK MeetingResultCallback 接口参考"
---

通用回调，一般在函数中使用

### onSuccess()
操作成功

```java
fun onSuccess()
```kotlin

### onFail()
操作失败

```java
fun onFail(code: Int, errorMsg: String?, showMsg: String?)
```

参数

| code | Int 类型，错误码 |
| --- | --- |
| errorMsg | String 类型，内部用于查看的错误信息 |
| showMsg | String 类型，对外显示的错误信息 |


