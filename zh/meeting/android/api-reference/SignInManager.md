---
title: "SignInManager"
description: "会中签到管理器：创建与结束签到、成员签到、人数统计、记录查询和流式导出"
---

`SignInManager` 通过 `MeetingEngine.signInManager` 获取，所有操作都绑定 Engine 当前的单场会议。

## 特殊说明

+ 该属性是稳定门面，可以在会前保存；未入会时所有异步方法返回 `MeetingErrorCode.SESSION_NOT_ACTIVE`。

## 注意事项

+ 结果回调保持网络来源线程，不自动切换主线程。
+ `exportSignInDetail()` 返回一次性 `MeetingDownload`，读取完成或放弃时必须关闭。

## 接口方法

### listSignInActivities(callback)

```kotlin
fun listSignInActivities(
    callback: MeetingValueResultCallback<SignInListBean>
)
```

方法说明：获取当前会议的签到活动列表与服务端当前时间。

参数说明：

+ `callback`：成功返回 `SignInListBean` 的结果回调。

返回值说明：无（异步结果见回调）。

### createSignInActivity(dur, desc, callback)

```kotlin
fun createSignInActivity(
    dur: Int,
    desc: String,
    callback: MeetingResultCallback
)
```

方法说明：由主持人创建一轮签到活动。

参数说明：

+ `dur`：签到持续时长，单位分钟；`0` 表示不限时。
+ `desc`：签到说明。
+ `callback`：创建结果回调。

返回值说明：无（异步结果见回调）。

### countSignInMembers(epoch, callback)

```kotlin
fun countSignInMembers(
    epoch: Int,
    callback: MeetingValueResultCallback<SignInCountBean>
)
```

方法说明：统计指定签到轮次的实际签到人数。

参数说明：

+ `epoch`：签到轮次。
+ `callback`：成功返回 `SignInCountBean` 的结果回调。

返回值说明：无（异步结果见回调）。

### finishSignInActivity(callback)

```kotlin
fun finishSignInActivity(callback: MeetingResultCallback)
```

方法说明：结束当前进行中的签到活动。

参数说明：

+ `callback`：结束结果回调。

返回值说明：无（异步结果见回调）。

### getSignInDetail(epoch, callback)

```kotlin
fun getSignInDetail(
    epoch: Int,
    callback: MeetingValueResultCallback<List<SignInRecordBean>>
)
```

方法说明：查询指定签到轮次的成员记录。

参数说明：

+ `epoch`：签到轮次。
+ `callback`：成功返回签到记录列表的结果回调。

返回值说明：无（异步结果见回调）。

### signIn(callback)

```kotlin
fun signIn(callback: MeetingResultCallback)
```

方法说明：当前成员对正在进行的签到活动执行签到。

参数说明：

+ `callback`：签到结果回调。

返回值说明：无（异步结果见回调）。

### exportSignInDetail(epoch, callback)

```kotlin
fun exportSignInDetail(
    epoch: Int,
    callback: MeetingValueResultCallback<MeetingDownload>
)
```

方法说明：导出指定签到轮次或全部轮次的数据流。

参数说明：

+ `epoch`：签到轮次；`-1` 表示全部轮次。
+ `callback`：成功返回一次性 `MeetingDownload` 的结果回调。

返回值说明：无（异步结果见回调）。调用方应使用 `use { ... }` 或显式 `close()` 关闭下载流。
