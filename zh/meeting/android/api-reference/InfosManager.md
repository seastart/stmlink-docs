---
title: "InfosManager"
description: "读取当前会议、成员与 SRTC 轨道的本地状态快照"
---

`InfosManager` 是当前会议的只读信息查询入口，通过 `MeetingEngine.infosManager` 获取。它提供会议信息、成员信息和媒体轨道信息，不发起网络请求，也不修改会议状态。

## 使用说明

+ `MeetingEngine` 始终返回同一个 `InfosManager` 门面，应用可以长期持有；每次查询都会读取 Engine 当前已加入的会议，不会继续暴露上一场会议的数据。
+ 查询结果来自 SDK 本地缓存，可能与刚发起但服务端尚未确认的操作存在短暂时间差。需要感知状态变化时，应同时监听对应的 `MeetingRoomEvent` 或 `MeetingUserEvent`。
+ 没有已加入的会议时，可空属性和对象查询返回 `null`，列表查询返回空列表，布尔查询返回 `false`。
+ 观众不属于正式成员列表。当前用户以观众身份入会时，`isAudience()` 返回 `true`，但 `getMeInfo()` 可能返回 `null`。
+ 返回的模型和列表用于表示查询时的状态快照，不应依赖修改这些对象来更新 SDK 或服务端会议状态。

## 属性

### meUid

```kotlin
val meUid: String?
```

属性说明：当前用户在 SRTC 频道中的 UID；尚未完成入会或已经离会时为 `null`。

### meetingId

```kotlin
val meetingId: String?
```

属性说明：当前会议 ID；尚未完成入会或已经离会时为 `null`。

### whiteBoard

```kotlin
val whiteBoard: String?
```

属性说明：当前会议的白板地址；未入会、已经离会或会议没有白板地址时为 `null`。

## 接口方法

### getMeetingInfo()

```kotlin
fun getMeetingInfo(): MeetingInfo?
```

方法说明：读取当前会议的房间配置和共享、录制等状态快照。

参数说明：无。

返回值说明：当前会议的 [MeetingInfo](/zh/meeting/android/types#meetinginfo)；没有已加入的会议或房间属性无法解析时返回 `null`。

### getMeInfo()

```kotlin
fun getMeInfo(): MemberInfo?
```

方法说明：读取当前用户的正式会议成员信息，包括角色、设备状态和成员权限。

参数说明：无。

返回值说明：当前用户的 [MemberInfo](/zh/meeting/android/types#memberinfo)；未入会、当前用户为观众或成员属性无法解析时返回 `null`。

### isAudience()

```kotlin
fun isAudience(): Boolean
```

方法说明：判断当前用户是否以观众身份加入会议。

参数说明：无。

返回值说明：`true` 表示当前是观众；未入会或当前是正式成员时返回 `false`。

### getMembersInfo()

```kotlin
fun getMembersInfo(): MutableList<MemberInfo>
```

方法说明：读取当前会议的正式成员列表，包括作为正式成员入会的当前用户，不包含观众。

参数说明：无。

返回值说明：成员信息快照列表；未入会、会议内没有正式成员或成员属性均无法解析时返回空列表。

### getMemberByUid(uid)

```kotlin
fun getMemberByUid(uid: String): MemberInfo?
```

方法说明：根据 UID 读取指定正式成员的信息。

参数说明：

| 参数 | 说明 |
| --- | --- |
| `uid` | 目标成员在当前会议中的 UID |

返回值说明：匹配的 `MemberInfo`；未入会或成员不存在时返回 `null`。

### isExistMember(uid)

```kotlin
fun isExistMember(uid: String): Boolean
```

方法说明：判断指定 UID 是否存在于当前会议的正式成员列表中。

参数说明：

| 参数 | 说明 |
| --- | --- |
| `uid` | 目标成员在当前会议中的 UID |

返回值说明：成员存在时返回 `true`；未入会或成员不存在时返回 `false`。

### getTrackInfos(uid)

```kotlin
fun getTrackInfos(uid: String): MutableList<TrackInfo>
```

方法说明：读取指定用户当前公开的全部 SRTC 媒体轨道信息。

参数说明：

| 参数 | 说明 |
| --- | --- |
| `uid` | 目标用户在当前会议中的 UID |

返回值说明：SRTC `TrackInfo` 快照列表；未入会、用户不存在或用户没有公开轨道时返回空列表。模型字段见 [SRTC Android 模型类型](/zh/rtc/android/types)。

### getTrackInfoByTrackDesc(uid, trackDesc)

```kotlin
fun getTrackInfoByTrackDesc(uid: String, trackDesc: String): TrackInfo?
```

方法说明：根据用户 UID 和轨道描述读取一条 SRTC 媒体轨道。

参数说明：

| 参数 | 说明 |
| --- | --- |
| `uid` | 目标用户在当前会议中的 UID |
| `trackDesc` | 轨道描述，例如摄像头主流 `TRACK_MAIN`、麦克风 `TRACK_AUDIO` 或共享流 `TRACK_SHARE` 对应的字符串值 |

返回值说明：匹配的 `TrackInfo`；未入会或没有匹配轨道时返回 `null`。轨道描述定义见 [SRTC Android 枚举类型](/zh/rtc/android/enums)。

### getTrackInfoByTrackId(uid, trackId)

```kotlin
fun getTrackInfoByTrackId(uid: String, trackId: String): TrackInfo?
```

方法说明：根据用户 UID 和 SRTC 轨道 ID 读取一条媒体轨道。

参数说明：

| 参数 | 说明 |
| --- | --- |
| `uid` | 目标用户在当前会议中的 UID |
| `trackId` | SRTC 为目标轨道分配的唯一 ID |

返回值说明：匹配的 `TrackInfo`；未入会或没有匹配轨道时返回 `null`。
