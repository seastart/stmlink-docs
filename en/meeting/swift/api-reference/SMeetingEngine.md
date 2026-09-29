---
title: "SMeetingEngine"
description: "API reference for SMeetingEngine, the single entry point of the SMeeting Swift SDK: initialization, properties, login and logout, creating and querying meetings, entering and exiting, state queries, member actions, out-of-meeting messages, and virtual background. Look up signatures and throws here."
---

`SMeetingEngine` is the SDK's only public entry point. Create only one instance per app and hold it globally.

This page covers initialization, authentication, meeting management, entering and exiting meetings, state queries, in-meeting member actions, and out-of-meeting messages. For media APIs, see [Media control](/en/meeting/swift/api-reference/media-control); for devices, see [Devices](/en/meeting/swift/api-reference/devices); for host and management APIs, see [Meeting management](/en/meeting/swift/api-reference/admin-actions).

---

### Initialization

#### `init(logLevel:)`

Creates an SDK instance.

```swift
let meeting = SMeetingEngine(logLevel: .info)
```

| Parameter | Type | Required | Description |
| --- | --- | :---: | --- |
| `logLevel` | `LogLevel` | No | Log level, default `.warning`. Options: `.verbose`, `.debug`, `.info`, `.warning`, `.error`, `.off` |

---

### Properties

#### `version`

```swift
let v = SMeetingEngine.version
```

The SDK version number, of type `String`; a static property.

#### `srtc`

The underlying RTC instance, of type `SRTCEngine`. An escape hatch for when the meeting layer's APIs aren't enough.

```swift
meeting.srtc.logLevel = .debug
```

> Always use this instance; don't create a second SRTCEngine yourself—the meeting and the underlying layer share the same instance, and creating another one leads to split state, duplicate message connections, and devices being taken over.

#### `delegates`

The collection of event delegates, of type `MulticastDelegate<SMeetingDelegate>`. A weak-reference multicast that supports multiple observers.

```swift
meeting.delegates.add(delegate: self)
meeting.delegates.remove(delegate: self)
```

#### `currentUserId`

The ID of the currently logged-in user, of type `String?`; `nil` when not logged in.

#### `isInRoom`

Whether you're currently in a meeting, of type `Bool`.

#### `cameraTrack` / `screenTrack` / `mcuTrack`

The local camera track (`LocalCameraTrack?`), the local screen sharing track (`LocalScreenTrack?`), and the remote composite track (`RemoteVideoTrack?`). Each is `nil` when the corresponding capability isn't on.

---

### Authentication

#### `login(token:)`

Logs in to the conferencing SDK. You can call the other APIs only after logging in.

```swift
try await meeting.login(token: token)
```

| Parameter | Type | Required | Description |
| --- | --- | :---: | --- |
| `token` | `String` | Yes | The meeting token issued by your backend |

**Returns:** None

**Throws:**

+ `SMeetingError.tokenInvalid`—the token format can't be parsed
+ `SMeetingError.tokenExpired`—the token has expired
+ `SMeetingError.apiError(code:message:)`—the server rejected the login
+ `SMeetingError.networkError(_:)`

---

#### `logout()`

Logs out. If still in a meeting, it first exits the meeting automatically, and it disables the out-of-meeting message path.

```swift
await meeting.logout()
```

**Returns:** None; doesn't throw.

---

### Meeting management (before the meeting)

The following APIs require only login, not being in a meeting.

#### `createRoom(_:)`

Creates a meeting.

```swift
var req = MeetingCreateReq(title: "Weekly project sync", meetingMode: .normal)
req.meetingType = .instant
let (roomNo, meetingId) = try await meeting.createRoom(req)
```

| Parameter | Type | Required | Description |
| --- | --- | :---: | --- |
| `req` | `MeetingCreateReq` | Yes | Creation parameters; for fields, see [Types](/en/meeting/swift/types#meetingcreatereq) |

**Returns:** `(roomNo: String, meetingId: String)`

**Throws:** `SMeetingError.notLoggedIn`, `SMeetingError.apiError(code:message:)`

> If `meetingType` isn't set explicitly, an instant meeting is created.

---

#### `updateRoom(meetingId:req:)`

Updates a meeting (before the meeting).

```swift
try await meeting.updateRoom(meetingId: meetingId, req: req)
```

| Parameter | Type | Required | Description |
| --- | --- | :---: | --- |
| `meetingId` | `String` | Yes | ID of the meeting to update |
| `req` | `MeetingCreateReq` | Yes | The new meeting parameters |

**Returns:** None

**Throws:** `SMeetingError.notLoggedIn`, `SMeetingError.apiError(code:message:)`

---

#### `cancelRoom(meetingId:)`

Cancels a meeting.

```swift
try await meeting.cancelRoom(meetingId: meetingId)
```

| Parameter | Type | Required | Description |
| --- | --- | :---: | --- |
| `meetingId` | `String` | Yes | Meeting ID |

**Returns:** None

**Throws:** `SMeetingError.notLoggedIn`, `SMeetingError.apiError(code:message:)`

---

#### `detailRoom(meetingId:roomNo:)`

Gets meeting details; provide one of the two parameters.

```swift
let info = try await meeting.detailRoom(roomNo: "10000001")
```

| Parameter | Type | Required | Description |
| --- | --- | :---: | --- |
| `meetingId` | `String?` | No | Meeting ID |
| `roomNo` | `String?` | No | Room number |

**Returns:** `MeetingInfo`

**Throws:** `SMeetingError.notLoggedIn`, `SMeetingError.apiError(code:message:)`

---

#### `attendeeRoom(page:)`

Meetings you need to attend (not started yet or in progress).

```swift
let result = try await meeting.attendeeRoom()
```

| Parameter | Type | Required | Description |
| --- | --- | :---: | --- |
| `page` | `PageParam` | No | Pagination parameters; defaults to page 1 with 20 items per page |

**Returns:** `PageResult<MeetingInfo>`

**Throws:** `SMeetingError.notLoggedIn`, `SMeetingError.apiError(code:message:)`

---

#### `attendedRoom(page:)`

Past meetings. Parameters and return value are the same as `attendeeRoom(page:)`.

---

#### `roomParticipant(meetingId:page:perPage:)`

Attendance records of a meeting.

```swift
let result = try await meeting.roomParticipant(meetingId: meetingId)
```

| Parameter | Type | Required | Description |
| --- | --- | :---: | --- |
| `meetingId` | `String` | Yes | Meeting ID |
| `page` | `Int` | No | Page number, default `1` |
| `perPage` | `Int` | No | Items per page, default `20` |

**Returns:** `PageResult<ParticipantInfo>`

**Throws:** `SMeetingError.notLoggedIn`, `SMeetingError.apiError(code:message:)`

---

### Enter / exit a meeting

#### `enterRoom(_:)`

Enters a meeting.

```swift
var req = MeetingEnterReq(nickname: "Alice", roomNo: "10000001")
req.password = "123456"
try await meeting.enterRoom(req)
```

| Parameter | Type | Required | Description |
| --- | --- | :---: | --- |
| `req` | `MeetingEnterReq` | Yes | Parameters for entering the meeting; provide either `meetingId` or `roomNo` |

**Returns:** None

**Throws:**

+ `SMeetingError.notLoggedIn`
+ `SMeetingError.alreadyInMeeting`—already in a meeting; call `exitRoom()` first
+ `SMeetingError.apiError(code:message:)`—wrong password, meeting doesn't exist, entry restricted, and so on
+ Errors thrown when the underlying connection fails to be set up

On success, the SDK subscribes to remote audio automatically; video is subscribed on demand.

---

#### `exitRoom()`

Exits the current meeting; the login state is kept.

```swift
await meeting.exitRoom()
```

**Returns:** None; doesn't throw. Calling it when not in a meeting is safely ignored.

---

### State queries

#### `getRoomInfo()`

**Returns:** `RoomInfo?`; `nil` when not in a meeting.

#### `getWhiteBoard()`

**Returns:** `String?`, the whiteboard URL of the current meeting; `nil` if there is none.

#### `getUserInfo(_:)`

```swift
let user = try meeting.getUserInfo(uid)
```

| Parameter | Type | Required | Description |
| --- | --- | :---: | --- |
| `uid` | `String` | Yes | Member ID |

**Returns:** `MeetingUserInfo`

**Throws:** `SMeetingError.notInMeeting`, `SMeetingError.internalError(_:)` (no such member in the meeting)

#### `getUsersInfo()`

**Returns:** `[String: MeetingUserInfo]`, a map from uid to member; an empty dictionary when not in a meeting.

#### `getUsersInfoList()`

**Returns:** `[MeetingUserInfo]`; an empty array when not in a meeting.

#### `getRemoteVideoTrack(uid:desc:)`

Looks up the track object of a given video track of a member, **without subscribing**.

| Parameter | Type | Required | Description |
| --- | --- | :---: | --- |
| `uid` | `String` | Yes | Member ID |
| `desc` | `TrackDesc` | No | Track description, default `.cameraBig` |

**Returns:** `Track?`; `nil` when the member doesn't exist or hasn't published that track.

---

### In-meeting member actions

The following APIs all require being in a meeting; otherwise they throw `SMeetingError.notInMeeting`. When the server rejects the call, they throw `SMeetingError.apiError(code:message:)`.

#### `updateName(_:)`

Changes your own in-meeting display name.

```swift
try await meeting.updateName("New nickname")
```

| Parameter | Type | Required | Description |
| --- | --- | :---: | --- |
| `name` | `String` | Yes | New nickname |

---

#### `sendRoomChatMessage(_:type:targetId:)`

Sends an in-meeting chat message.

```swift
try await meeting.sendRoomChatMessage("Hi everyone")
try await meeting.sendRoomChatMessage(url, type: .pic, targetId: uid)
```

| Parameter | Type | Required | Description |
| --- | --- | :---: | --- |
| `msg` | `String` | Yes | Message content |
| `type` | `ChatMsgType` | No | Message type, default `.text` |
| `targetId` | `String?` | No | Target member for a private message; omit to send to everyone |

---

#### `sendRoomCustomMessage(_:targetId:)`

Sends a custom message of your own.

| Parameter | Type | Required | Description |
| --- | --- | :---: | --- |
| `content` | `String` | Yes | Message content, usually your own JSON |
| `targetId` | `String?` | No | Target member for a private message; omit to send to everyone |

---

#### `requestHandup(_:)` / `cancelHandup(_:)`

Raises a hand or cancels it.

```swift
try await meeting.requestHandup(.mic)
try await meeting.cancelHandup(.mic)
```

| Parameter | Type | Required | Description |
| --- | --- | :---: | --- |
| `code` | `HandupType` | Yes | `.mic` / `.camera` / `.chat` / `.share` |

---

#### `rejectOpenMic(adminUid:)` / `rejectOpenCamera(adminUid:)`

Declines the host's request to turn on the microphone / camera.

| Parameter | Type | Required | Description |
| --- | --- | :---: | --- |
| `adminUid` | `String?` | No | ID of the host who sent the request, taken from `opUid` of the corresponding event |

---

#### `rollCallAnswer(rollCallUserId:)`

Answers a roll call.

| Parameter | Type | Required | Description |
| --- | --- | :---: | --- |
| `rollCallUserId` | `String` | Yes | Pass `RollCallNamedEventData.id` directly. Note that it's not `.sid` (that's the uid of the host who started the roll call) |

**Throws:** `SMeetingError.notLoggedIn`, `SMeetingError.apiError(code:message:)`

---

### Out-of-meeting messages

#### `enableIm()`

Enables the out-of-meeting message path.

```swift
try await meeting.enableIm()
```

**Returns:** None

**Throws:** `SMeetingError.notLoggedIn`, `SMeetingError.apiError(code:message:)`, and underlying errors when the connection fails to be set up

#### `disableIm()`

Disables the out-of-meeting message path.

```swift
await meeting.disableIm()
```

**Returns:** None; doesn't throw. `logout()` calls it internally.

---

### Virtual background

This is a **device-level setting** (it applies to the single shared camera capture pipeline in the process), and it applies to all meetings at once. After switching cameras, turning the camera off and on again, or reconnecting after a disconnect during the meeting, your app doesn't need to apply it again. For usage and tuning, see [Virtual background](/en/meeting/swift/advanced/virtual-background).

| Member | Signature | Description |
| --- | --- | --- |
| Install | `installVirtualBackground(modelPath: String? = nil) throws` | Loads the model + creates the inference session, taking hundreds of milliseconds; don't call it on the main thread / capture thread; `nil` uses the built-in model |
| Uninstall | `uninstallVirtualBackground()` | Releases the inference session and buffers; doesn't clear effect parameters |
| Master switch | `enableVirtualBackground(_ enabled: Bool) throws` | When off, frames pass straight through with zero overhead and no inference runs |
| Switch state | `isVirtualBackgroundEnabled: Bool` | Read-only |
| Background blur | `setVirtualBackgroundBlur(level: Int)` | `level` ranges from 1 to 10, default 5; out-of-range values are clamped to the boundary |
| Background replacement | `setVirtualBackgroundImage(_ image: SRTCNativeImage?)` | Cropped to cover without stretching; `nil` falls back to blur |
| Inference interval | `setVirtualBackgroundInferenceInterval(_ interval: Int)` | Runs segmentation every N frames (compositing still runs every frame); default 1 |
| Mask sync | `setVirtualBackgroundMaskSync(_ enabled: Bool)` | Default `false`; when `interval` is 1, the switch makes no difference |
| Instance | `virtualBackground: SRTCVirtualBackground` | Read-only state and dropped-frame count for diagnostics |

**Throws:** `SRTCError.virtualBackgroundAlreadyInstalled`, `.virtualBackgroundNotInstalled`, `.virtualBackgroundModelNotFound(String)`, `.virtualBackgroundSessionFailed(String)`

This group forwards to the audio and video layer, and the meeting layer doesn't keep a separate copy of the state, so it's equivalent to calling through `meeting.srtc` directly; we recommend using the meeting layer's methods.

---

### Related pages

+ [Virtual background](/en/meeting/swift/advanced/virtual-background)
+ [Media control APIs](/en/meeting/swift/api-reference/media-control)
+ [Device APIs](/en/meeting/swift/api-reference/devices)
+ [Meeting management APIs](/en/meeting/swift/api-reference/admin-actions)
+ [Events](/en/meeting/swift/events)
+ [Types](/en/meeting/swift/types)
