---
title: "InfosManager"
description: "读取当前会议、成员与 SRTC 轨道的本地状态快照，不发起网络请求"
---

`InfosManager` 是当前会议的信息中心，通过 `MeetingEngine.infosManager` 获取。它只读取 SDK 已缓存的会议、成员和轨道状态，不会发起网络请求。

## 特殊说明

+ Engine 暴露的是稳定门面，可以在会前保存；未入会时属性返回 `null`，列表方法返回空集合。

## 注意事项

+ 返回值是当前本地快照，可能与刚刚发起但服务端尚未确认的操作存在短暂时间差。
+ 观众不在正式成员列表中，`isAudience()` 用于判断当前身份。

## 属性

### meUid

```kotlin
val meUid: String?
```

属性说明：当前用户在 SRTC 频道中的 UID；尚未完成入会时为 `null`。

### meetingId

```kotlin
val meetingId: String?
```

属性说明：当前会议 ID；未入会时为 `null`。

### whiteBoard

```kotlin
val whiteBoard: String?
```

属性说明：当前会议的白板地址；未入会或会议没有白板地址时为 `null`。

## 接口方法

### getMeetingInfo()

```kotlin
fun getMeetingInfo(): MeetingInfo?
```

方法说明：获取当前房间信息快照。

参数说明：无。

返回值说明：`MeetingInfo?`；未入会时为 `null`。

### getMeInfo()

```kotlin
fun getMeInfo(): MemberInfo?
```

方法说明：获取当前用户的会议成员信息。

参数说明：无。

返回值说明：`MemberInfo?`；未入会或当前以观众身份加入时可能为 `null`。

### isAudience()

```kotlin
fun isAudience(): Boolean
```

方法说明：判断当前是否以观众身份入会。

参数说明：无。

返回值说明：`true` 表示观众；观众可接收成员和音视频信息，但不能开设备、共享或发流。

### getMembersInfo()

```kotlin
fun getMembersInfo(): MutableList<MemberInfo>
```

方法说明：获取当前会议的正式成员列表，包含当前用户但不包含观众。

参数说明：无。

返回值说明：成员信息快照；未入会时为空列表。

### getMemberByUid(uid)

```kotlin
fun getMemberByUid(uid: String): MemberInfo?
```

方法说明：按 UID 查询成员信息。

参数说明：

+ `uid`：目标成员 UID。

返回值说明：匹配的 `MemberInfo`；未找到时为 `null`。

### isExistMember(uid)

```kotlin
fun isExistMember(uid: String): Boolean
```

方法说明：判断指定 UID 是否存在于当前正式成员列表。

参数说明：

+ `uid`：目标成员 UID。

返回值说明：存在时为 `true`。

### getTrackInfos(uid)

```kotlin
fun getTrackInfos(uid: String): MutableList<TrackInfo>
```

方法说明：获取指定用户当前公开的全部 SRTC 轨道信息。

参数说明：

+ `uid`：目标用户 UID。

返回值说明：`TrackInfo` 快照列表；未找到用户或轨道时为空列表。

### getTrackInfoByTrackDesc(uid, trackDesc)

```kotlin
fun getTrackInfoByTrackDesc(uid: String, trackDesc: String): TrackInfo?
```

方法说明：按用户 UID 和轨道描述查询轨道。

参数说明：

+ `uid`：目标用户 UID。
+ `trackDesc`：轨道描述，例如摄像头主流或共享流描述。

返回值说明：匹配的 `TrackInfo`；未找到时为 `null`。

### getTrackInfoByTrackId(uid, trackId)

```kotlin
fun getTrackInfoByTrackId(uid: String, trackId: String): TrackInfo?
```

方法说明：按用户 UID 和 SRTC 轨道 ID 查询轨道。

参数说明：

+ `uid`：目标用户 UID。
+ `trackId`：目标轨道 ID。

返回值说明：匹配的 `TrackInfo`；未找到时为 `null`。
