---
title: "SMeetingEngine"
description: "SMeeting Swift SDK 主入口类接口参考：初始化、登录、会议管理、进出会议、状态查询与会中用户操作"
---

`SMeetingEngine` 是 SDK 的唯一对外入口。同一个 App 内只应创建一个实例并全局持有。

本页覆盖初始化、认证、会议管理、进出会议、状态查询、会中用户操作与会议外消息。媒体相关接口见 [媒体控制](/zh/meeting/swift/api-reference/media-control)，外设见 [外设](/zh/meeting/swift/api-reference/devices)，主持人与管理接口见 [会议管理](/zh/meeting/swift/api-reference/admin-actions)。

---

### 初始化

#### `init(logLevel:)`

创建 SDK 实例。

```swift
let meeting = SMeetingEngine(logLevel: .info)
```

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | :---: | --- |
| `logLevel` | `LogLevel` | 否 | 日志级别，默认 `.warning`。可选 `.verbose`、`.debug`、`.info`、`.warning`、`.error`、`.off` |

---

### 属性

#### `version`

```swift
let v = SMeetingEngine.version
```

SDK 版本号，类型 `String`，静态属性。

#### `srtc`

底层 RTC 实例，类型 `SRTCEngine`。当会议层接口不足以满足需求时的逃生口。

```swift
meeting.srtc.logLevel = .debug
```

> 请始终使用这个实例，不要自行创建第二个 SRTCEngine —— 会议与底层共享同一个实例，另起一个会导致状态分裂、消息通道重复、设备被抢占。

#### `delegates`

事件委托集合，类型 `MulticastDelegate<SMeetingDelegate>`。弱引用多播，支持多个观察者。

```swift
meeting.delegates.add(delegate: self)
meeting.delegates.remove(delegate: self)
```

#### `currentUserId`

当前登录用户的 ID，类型 `String?`，未登录时为 `nil`。

#### `isInRoom`

当前是否在会议中，类型 `Bool`。

#### `cameraTrack` / `screenTrack` / `mcuTrack`

本地摄像头轨道（`LocalCameraTrack?`）、本地屏幕共享轨道（`LocalScreenTrack?`）、远端合屏轨道（`RemoteVideoTrack?`）。未开启对应能力时为 `nil`。

---

### 认证

#### `login(token:)`

登录会议 SDK。登录后才能调用其余接口。

```swift
try await meeting.login(token: token)
```

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | :---: | --- |
| `token` | `String` | 是 | 业务后端签发的 meeting token |

**返回值：** 无

**可能抛出：**

+ `SMeetingError.tokenInvalid` —— token 格式无法解析
+ `SMeetingError.tokenExpired` —— token 已过期
+ `SMeetingError.apiError(code:message:)` —— 服务端拒绝登录
+ `SMeetingError.networkError(_:)`

---

#### `logout()`

退出登录。若仍在会议中会先自动退出会议，并停用会议外消息通道。

```swift
await meeting.logout()
```

**返回值：** 无，不抛错。

---

### 会议管理（会前）

以下接口只要求已登录，不要求在会议中。

#### `createRoom(_:)`

创建会议。

```swift
var req = MeetingCreateReq(title: "项目周会", meetingMode: .normal)
req.meetingType = .instant
let (roomNo, meetingId) = try await meeting.createRoom(req)
```

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | :---: | --- |
| `req` | `MeetingCreateReq` | 是 | 创建参数，字段见 [类型定义](/zh/meeting/swift/types#meetingcreatereq) |

**返回值：** `(roomNo: String, meetingId: String)`

**可能抛出：** `SMeetingError.notLoggedIn`、`SMeetingError.apiError(code:message:)`

> 不显式设置 `meetingType` 时按即时会议创建。

---

#### `updateRoom(meetingId:req:)`

修改会议（会前）。

```swift
try await meeting.updateRoom(meetingId: meetingId, req: req)
```

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | :---: | --- |
| `meetingId` | `String` | 是 | 要修改的会议 ID |
| `req` | `MeetingCreateReq` | 是 | 新的会议参数 |

**返回值：** 无

**可能抛出：** `SMeetingError.notLoggedIn`、`SMeetingError.apiError(code:message:)`

---

#### `cancelRoom(meetingId:)`

取消会议。

```swift
try await meeting.cancelRoom(meetingId: meetingId)
```

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | :---: | --- |
| `meetingId` | `String` | 是 | 会议 ID |

**返回值：** 无

**可能抛出：** `SMeetingError.notLoggedIn`、`SMeetingError.apiError(code:message:)`

---

#### `detailRoom(meetingId:roomNo:)`

获取会议详情，两个参数二选一。

```swift
let info = try await meeting.detailRoom(roomNo: "10000001")
```

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | :---: | --- |
| `meetingId` | `String?` | 否 | 会议 ID |
| `roomNo` | `String?` | 否 | 房间号 |

**返回值：** `MeetingInfo`

**可能抛出：** `SMeetingError.notLoggedIn`、`SMeetingError.apiError(code:message:)`

---

#### `attendeeRoom(page:)`

我需要参加的会议（未开始或进行中）。

```swift
let result = try await meeting.attendeeRoom()
```

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | :---: | --- |
| `page` | `PageParam` | 否 | 分页参数，默认第 1 页每页 20 条 |

**返回值：** `PageResult<MeetingInfo>`

**可能抛出：** `SMeetingError.notLoggedIn`、`SMeetingError.apiError(code:message:)`

---

#### `attendedRoom(page:)`

历史会议。参数与返回值同 `attendeeRoom(page:)`。

---

#### `roomParticipant(meetingId:page:perPage:)`

某场会议的参会人员记录。

```swift
let result = try await meeting.roomParticipant(meetingId: meetingId)
```

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | :---: | --- |
| `meetingId` | `String` | 是 | 会议 ID |
| `page` | `Int` | 否 | 页码，默认 `1` |
| `perPage` | `Int` | 否 | 每页条数，默认 `20` |

**返回值：** `PageResult<ParticipantInfo>`

**可能抛出：** `SMeetingError.notLoggedIn`、`SMeetingError.apiError(code:message:)`

---

### 进入 / 退出会议

#### `enterRoom(_:)`

进入会议。

```swift
var req = MeetingEnterReq(nickname: "张三", roomNo: "10000001")
req.password = "123456"
try await meeting.enterRoom(req)
```

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | :---: | --- |
| `req` | `MeetingEnterReq` | 是 | 入会参数，`meetingId` 与 `roomNo` 二选一 |

**返回值：** 无

**可能抛出：**

+ `SMeetingError.notLoggedIn`
+ `SMeetingError.alreadyInMeeting` —— 已经在会议中，需要先 `exitRoom()`
+ `SMeetingError.apiError(code:message:)` —— 密码错误、会议不存在、被限制入会等
+ 底层连接建立失败时抛出的错误

成功后 SDK 会自动订阅远端音频，视频按需订阅。

---

#### `exitRoom()`

退出当前会议，登录状态保留。

```swift
await meeting.exitRoom()
```

**返回值：** 无，不抛错。不在会议中时调用会被安全忽略。

---

### 状态查询

#### `getRoomInfo()`

**返回值：** `RoomInfo?`，未在会议中时为 `nil`。

#### `getWhiteBoard()`

**返回值：** `String?`，当前会议的白板地址，没有时为 `nil`。

#### `getUserInfo(_:)`

```swift
let user = try meeting.getUserInfo(uid)
```

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | :---: | --- |
| `uid` | `String` | 是 | 成员 ID |

**返回值：** `MeetingUserInfo`

**可能抛出：** `SMeetingError.notInMeeting`、`SMeetingError.internalError(_:)`（会议中没有这个成员）

#### `getUsersInfo()`

**返回值：** `[String: MeetingUserInfo]`，uid 到成员的映射，未在会议中时为空字典。

#### `getUsersInfoList()`

**返回值：** `[MeetingUserInfo]`，未在会议中时为空数组。

#### `getRemoteVideoTrack(uid:desc:)`

查询某位成员的某路视频轨道对象，**不发起订阅**。

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | :---: | --- |
| `uid` | `String` | 是 | 成员 ID |
| `desc` | `TrackDesc` | 否 | 轨道描述，默认 `.cameraBig` |

**返回值：** `Track?`，成员不存在或未发布该轨道时为 `nil`。

---

### 会中用户操作

以下接口都要求在会议中，否则抛出 `SMeetingError.notInMeeting`；服务端拒绝时抛出 `SMeetingError.apiError(code:message:)`。

#### `updateName(_:)`

修改自己的会中昵称。

```swift
try await meeting.updateName("新昵称")
```

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | :---: | --- |
| `name` | `String` | 是 | 新昵称 |

---

#### `sendRoomChatMessage(_:type:targetId:)`

发送会中聊天消息。

```swift
try await meeting.sendRoomChatMessage("大家好")
try await meeting.sendRoomChatMessage(url, type: .pic, targetId: uid)
```

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | :---: | --- |
| `msg` | `String` | 是 | 消息内容 |
| `type` | `ChatMsgType` | 否 | 消息类型，默认 `.text` |
| `targetId` | `String?` | 否 | 私聊目标成员；不传为群发 |

---

#### `sendRoomCustomMessage(_:targetId:)`

发送业务自定义消息。

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | :---: | --- |
| `content` | `String` | 是 | 消息内容，通常放业务 JSON |
| `targetId` | `String?` | 否 | 私聊目标成员；不传为群发 |

---

#### `requestHandup(_:)` / `cancelHandup(_:)`

举手申请与取消。

```swift
try await meeting.requestHandup(.mic)
try await meeting.cancelHandup(.mic)
```

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | :---: | --- |
| `code` | `HandupType` | 是 | `.mic` / `.camera` / `.chat` / `.share` |

---

#### `rejectOpenMic(adminUid:)` / `rejectOpenCamera(adminUid:)`

拒绝主持人的开麦 / 开摄像头邀请。

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | :---: | --- |
| `adminUid` | `String?` | 否 | 发起邀请的主持人 ID，取自对应事件的 `opUid` |

---

#### `rollCallAnswer(rollCallUserId:)`

点名应答。

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | :---: | --- |
| `rollCallUserId` | `String` | 是 | 直接传 `RollCallNamedEventData.id`。注意不是 `.sid`（那是发起点名的主持人 uid） |

**可能抛出：** `SMeetingError.notLoggedIn`、`SMeetingError.apiError(code:message:)`

---

### 会议外消息

#### `enableIm()`

启用会议外消息通道。

```swift
try await meeting.enableIm()
```

**返回值：** 无

**可能抛出：** `SMeetingError.notLoggedIn`、`SMeetingError.apiError(code:message:)`、连接建立失败时的底层错误

#### `disableIm()`

停用会议外消息通道。

```swift
await meeting.disableIm()
```

**返回值：** 无，不抛错。`logout()` 内部会自动调用。

---

### 相关页面

+ [媒体控制接口](/zh/meeting/swift/api-reference/media-control)
+ [外设接口](/zh/meeting/swift/api-reference/devices)
+ [会议管理接口](/zh/meeting/swift/api-reference/admin-actions)
+ [事件参考](/zh/meeting/swift/events)
+ [类型定义](/zh/meeting/swift/types)
