---
title: "InfosManager"
description: "Android SMeeting 会议 SDK InfosManager 接口参考"
---

说明：`InfosManager` 是会中信息管理器，用于读取当前会议、成员与轨道的本地状态快照。

## 核心属性

### meUid（属性）
```kotlin
val meUid: String?
```
方法说明：当前登录成员的 UID。  
参数说明：无。  
返回值说明：`String?`，当前用户 UID；未入会或未就绪时为 `null`。

### meetingId（属性）
```kotlin
val meetingId: String?
```
方法说明：当前会议 ID。  
参数说明：无。  
返回值说明：`String?`，当前会议 ID；未入会时为 `null`。

### whiteBoard（属性）
```kotlin
val whiteBoard: String?
```
方法说明：当前会议白板地址。  
参数说明：无。  
返回值说明：`String?`，白板 URL/地址；未配置时为 `null`。

### meetingIdForWaitingRoom（属性）
```kotlin
val meetingIdForWaitingRoom: String?
```
方法说明：等候室场景下缓存的会议 ID。  
参数说明：无。  
返回值说明：`String?`，等候室关联会议 ID；无数据时为 `null`。

## 会议信息

### getMeetingInfo()
```kotlin
fun getMeetingInfo(): MeetingInfo?
```
方法说明：获取当前会议信息。  
参数说明：无。  
返回值说明：`MeetingInfo?`，会议信息对象；无会议上下文时返回 `null`。

## 成员信息

### getMeInfo()
```kotlin
fun getMeInfo(): MemberInfo?
```
方法说明：获取当前用户成员信息。  
参数说明：无。  
返回值说明：`MemberInfo?`，当前成员信息；未入会或数据未同步时返回 `null`。

### getMembersInfo()
```kotlin
fun getMembersInfo(): MutableList<MemberInfo>
```
方法说明：获取当前会议全部成员信息（包含自己）。  
参数说明：无。  
返回值说明：`MutableList<MemberInfo>`，成员信息列表；无成员时返回空列表。

### getMemberByUid(uid)
```kotlin
fun getMemberByUid(uid: String): MemberInfo?
```
方法说明：按用户 UID 获取成员信息。  
参数说明：
- `uid`：`String`，目标成员 UID。
返回值说明：`MemberInfo?`，目标成员信息；未找到时返回 `null`。

### isExistMember(uid)
```kotlin
fun isExistMember(uid: String): Boolean
```
方法说明：判断指定 UID 的成员是否存在于当前会议。  
参数说明：
- `uid`：`String`，目标成员 UID。
返回值说明：`Boolean`，`true` 表示存在，`false` 表示不存在。

## 轨道信息

### getTrackInfos(uid)
```kotlin
fun getTrackInfos(uid: String): MutableList<TrackInfo>
```
方法说明：获取指定成员的全部轨道信息。  
参数说明：
- `uid`：`String`，目标成员 UID。
返回值说明：`MutableList<TrackInfo>`，该成员轨道列表；无轨道时返回空列表。

### getTrackInfoByTrackDesc(uid, trackDesc)
```kotlin
fun getTrackInfoByTrackDesc(uid: String, trackDesc: String): TrackInfo?
```
方法说明：按成员 UID 与轨道描述查询轨道信息。  
参数说明：
- `uid`：`String`，目标成员 UID。
- `trackDesc`：`String`，轨道描述（如 `camera_big`、`camera_small`、`screen`、`mic`）。
返回值说明：`TrackInfo?`，匹配到的轨道信息；未找到时返回 `null`。

### getTrackInfoByTrackId(uid, trackId)
```kotlin
fun getTrackInfoByTrackId(uid: String, trackId: String): TrackInfo?
```
方法说明：按成员 UID 与轨道 ID 查询轨道信息。  
参数说明：
- `uid`：`String`，目标成员 UID。
- `trackId`：`String`，轨道 ID。
返回值说明：`TrackInfo?`，匹配到的轨道信息；未找到时返回 `null`。


