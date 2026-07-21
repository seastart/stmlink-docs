---
title: "SignInManager"
description: "Android SMeeting 会议 SDK SignInManager 接口参考"
---

说明：`SignInManager` 是会中签到功能管理器，通过 `MeetingEngine.signInManager` 获取，用于发起/结束签到活动、用户签到、查询与导出签到记录。

## 签到方法

### listSignInActivities(callback)
```kotlin
fun listSignInActivities(callback: Callback<Data<SignInListBean>>)
```
方法说明：获取签到活动列表。  
参数说明：
- `callback`：`Callback<Data<SignInListBean>>`，异步结果回调，返回活动列表与服务器当前时间。
返回值说明：无（`Unit`）。

### createSignInActivity(dur, desc, callback)
```kotlin
fun createSignInActivity(dur: Int, desc: String, callback: Callback<Data<String>>?)
```
方法说明：创建签到活动。  
参数说明：
- `dur`：`Int`，活动持续时长（分钟），`0` 表示不限时。
- `desc`：`String`，活动描述。
- `callback`：`Callback<Data<String>>?`，异步结果回调。
返回值说明：无（`Unit`）。

### countSignInMembers(epoch, callback)
```kotlin
fun countSignInMembers(epoch: Int, callback: Callback<Data<SignInCountBean>>)
```
方法说明：统计指定轮次的签到人数。  
参数说明：
- `epoch`：`Int`，签到轮次（从 0 开始）。
- `callback`：`Callback<Data<SignInCountBean>>`，异步结果回调，返回实际签到人数。
返回值说明：无（`Unit`）。

### finishSignInActivity(callback)
```kotlin
fun finishSignInActivity(callback: Callback<Data<String>>?)
```
方法说明：结束当前签到活动。  
参数说明：
- `callback`：`Callback<Data<String>>?`，异步结果回调。
返回值说明：无（`Unit`）。

### getSignInDetail(epoch, callback)
```kotlin
fun getSignInDetail(epoch: Int, callback: Callback<Data<List<SignInRecordBean>>>)
```
方法说明：获取指定轮次的签到活动详情。  
参数说明：
- `epoch`：`Int`，签到轮次（从 0 开始）。
- `callback`：`Callback<Data<List<SignInRecordBean>>>`，异步结果回调，返回签到记录列表。
返回值说明：无（`Unit`）。

### signIn(callback)
```kotlin
fun signIn(callback: Callback<Data<String>>?)
```
方法说明：用户签到。  
参数说明：
- `callback`：`Callback<Data<String>>?`，异步结果回调。
返回值说明：无（`Unit`）。

### exportSignInDetail(epoch, callback)
```kotlin
fun exportSignInDetail(epoch: Int, callback: StreamCallback?)
```
方法说明：导出签到数据，返回原始流。  
参数说明：
- `epoch`：`Int`，签到轮次（从 0 开始）。
- `callback`：`StreamCallback?`，流式结果回调，返回导出文件的原始数据流。
返回值说明：无（`Unit`）。
