会中信息管理类，通过该类的实例，可以获取到会议信息、成员信息、轨道信息

### meUid
获取自己的 uid

```kotlin
val meUid: String?
```

### meetingId
获取会议的 id

```kotlin
val meetingId: String?
```

### whiteBoard
白板地址

```kotlin
val whiteBoard: String?
```

### meetingIdForWaitingRoom
为了等候室存储的 meetingId

```kotlin
val meetingIdForWaitingRoom: String?
```

### getMeetingInfo()
获取房间信息

```java
fun getMeetingInfo(): MeetingInfo?
```

返回值

| 会议信息，详见数据类型中的 [MeetingInfo](https://www.yuque.com/anyconf/eanoso/mzyftti7zsfhs417#NkjUb) |
| --- |


### getMeInfo()
获取自己的用户信息

```java
fun getMeInfo(): MemberInfo?
```

返回值

| 自己的信息，详见数据类型中的 [MemberInfo](https://www.yuque.com/anyconf/eanoso/mzyftti7zsfhs417#CoQJN) |
| --- |


### getMembersInfo()
获取所有成员的用户信息，包括自己的用户信息

```java
fun getMembersInfo(): MutableList<MemberInfo>
```

返回值

| 成员信息集合，详见数据类型中的 [MemberInfo](https://www.yuque.com/anyconf/eanoso/mzyftti7zsfhs417#CoQJN) |
| --- |


### getMemberByUid()
获取指定 uid 的成员的用户信息

```java
fun getMemberByUid(uid: String): MemberInfo?
```

参数

| uid | String 类型，成员 uid |
| --- | --- |


返回值

| 成员信息集合，详见数据类型中的 [MemberInfo](https://www.yuque.com/anyconf/eanoso/mzyftti7zsfhs417#CoQJN) |
| --- |


### isExistMember()
是否存在指定成员

```java
fun isExistMember(uid: String): Boolean
```

参数

| uid | String 类型，成员 uid |
| --- | --- |


返回值

| Boolean 类型，是否存在指定 uid 的成员 |
| --- |


### getTrackInfos()
获取指定 uid 的 trackInfo 列表

```java
fun getTrackInfos(uid: String): MutableList<TrackInfo>
```

参数

| uid | String 类型，成员 uid |
| --- | --- |


返回值

| 轨道集合，TrackInfo，轨道信息，详见数据类型中的 [TrackInfo](https://www.yuque.com/anyconf/eanoso/mzyftti7zsfhs417#NhiSN) |
| --- |


### getTrackInfoByTrackDesc()
获取指定 uid、trackDesc 的 trackInfo

```java
fun getTrackInfoByTrackDesc(uid: String, trackDesc: String): TrackInfo?
```

参数

| uid | String 类型，成员 uid |
| --- | --- |
| trackDesc | String 类型，轨道描述 |


返回值

| 轨道信息，详见数据类型中的 [TrackInfo](https://www.yuque.com/anyconf/eanoso/mzyftti7zsfhs417#NhiSN) |
| --- |


### getTrackInfoByTrackId()
获取指定 uid、trackId 的 trackInfo

```java
fun getTrackInfoByTrackId(uid: String, trackId: String): TrackInfo?
```

参数

| uid | String 类型，成员 uid |
| --- | --- |
| trackId | String 类型，轨道 id |


返回值

| 轨道信息，详见数据类型中的 [TrackInfo](https://www.yuque.com/anyconf/eanoso/mzyftti7zsfhs417#NhiSN) |
| --- |


