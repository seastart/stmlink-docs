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

#### `language`

SDK language, of type `String?` (such as `"en"` or `"zh-CN"`). Defaults to `nil`, which follows the system language. Available since 1.4.0.

This is the same process-wide setting as the SRTC layer's language: requests from both the meeting layer and the RTC layer to the backend carry `Accept-Language`, and **the messages of backend business errors (codes ≥ 1000)** come back in Chinese or English accordingly. The SDK's own errors (`SMeetingError.message` / `SRTCError.message`) are always in English and aren't affected. Set it before `login`; changing it later takes effect immediately for subsequent requests.

```swift
meeting.language = "en"
```

#### `currentLanguage`

The language actually in effect, of type `String`, read-only: `language` if it's set, otherwise the system's preferred language, or `"zh"` if that can't be determined. Available since 1.4.0.

For error codes and how to handle them, see [Error handling](/en/meeting/swift/error-codes).

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

#### `isCameraOpened`

Whether the camera is open as the **meeting camera**, of type `Bool`, read-only. Available since 1.9.0.

During a preview-only `requestOpenCamera(publish: false)`, `cameraTrack` isn't `nil` but this property is `false`. Use it to tell "opened for preview" apart from "actually on in the meeting", and decide whether to call `closeCamera()` when closing the preview:

```swift
// Closing the settings page preview: close only a preview-only camera; leave the meeting camera alone
if !meeting.isCameraOpened {
    await meeting.closeCamera()
}
```

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

**Returns:** `MeetingInfo`. The detail response has no creation time, so `createdAt` is `0`; since 1.5.0 it also carries `entryMutePolicy` and `content` (`nil` when the backend doesn't return them). See [Types](/en/meeting/swift/types#meetinginfo) for fields

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
  + `code == SMeetingError.waitingRoomCode` (`2118`): moved into the waiting room; `code == SMeetingError.enterBeforeHostCode` (`2120`): must wait for the host to join. Neither is a failure—show a waiting page; see [Waiting room](/en/meeting/swift/advanced/waiting-room) (constants since 1.14.0)
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

**Throws:** `SMeetingError.notInMeeting`, `SMeetingError.userNotFound(_:)` (no such member in the meeting)

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

After it succeeds, `meeting(_:imDidConnect:)` fires once. Subsequent out-of-meeting messages are dispatched by action to `imCallCalling` / `imMeetingRemind` / `imAdminMoveOutWaitingRoom` / `imUserHelpSubMeeting`, and every message also fires `imDidReceiveMessage` as is; see [Out-of-meeting messages](/en/meeting/swift/advanced/im). In 1.4.1 and earlier these events were never actually dispatched; fixed in 1.5.0.

**Returns:** None

**Throws:** `SMeetingError.notLoggedIn`, `SMeetingError.apiError(code:message:)`, and underlying errors when the connection fails to be set up

#### `disableIm()`

Disables the out-of-meeting message path.

```swift
await meeting.disableIm()
```

**Returns:** None; doesn't throw. `logout()` calls it internally. Disabling it yourself doesn't fire `meeting(_:imDidDisconnect:)`.

---

### Pre-call network check

Available since 1.11.0, requires SRTC 1.10.0. **Call it before joining**; you don't need to join a meeting or connect to RTC. It has the same name and parameters as SRTC's
[`networkCheck`](/en/rtc/swift/api-reference/SRTCEngine#pre-call-network-check):
SRTC runs the five checks `permission` → `connectivity` → `mtu` → `dns` → `server` and its results are converted to meeting-layer types as is.
The meeting layer only adds one subcheck, `meetingApi` (JSON key `meeting_api`, whether the meeting API is reachable), to the `data` of the `server` item, and recomputes the overall status accordingly.
When everything is normal it takes about 1–5 seconds.

#### `networkCheck(timeoutMs:onItem:)`

Use this when logged in: the RTC `app_id` and server address come from the login information (from the IM token if `enableIm()` has been called; otherwise derived from the meeting API address), so you don't pass any.

```swift
let result = try await meeting.networkCheck { item in
    // Main thread, called item by item in the order permission → connectivity → mtu → dns → server
    print(item.id, item.status, item.message)
}
if result.status == .fail {
    // Each item's message is a Chinese description you can show to users directly
}
```

| Parameter | Type | Required | Description |
| --- | --- | :---: | --- |
| `timeoutMs` | `Int` | No | Per-item timeout in milliseconds, default `3000`; also used as the request timeout of `meeting_api` |
| `onItem` | `(@Sendable (MeetingNetworkCheckItem) -> Void)?` | No | Called once per completed item, on the main thread; the `server` item is reported only after `meeting_api` is merged in |

**Returns:** [`MeetingNetworkCheckResult`](/en/meeting/swift/types#meetingnetworkcheckresult) (`async throws`)

**Throws:** `SMeetingError.notLoggedIn` (not logged in), `SRTCError.invalidArgument` (the RTC address can't be derived; use the overload below that takes explicit parameters), `.alreadyJoined` (a check is already running), `.cancelled` (cancelled)

#### `networkCheck(appId:serverUrl:timeoutMs:onItem:)`

Use this when not logged in: pass the RTC app ID and server address explicitly. Everything else is the same as above.

| Parameter | Type | Required | Description |
| --- | --- | :---: | --- |
| `appId` | `String` | Yes | App ID |
| `serverUrl` | `String` | Yes | The **RTC** server address, that is, `client_api` in the RTC / IM token (such as `https://host/client/`), not the meeting API address |
| `timeoutMs` | `Int` | No | Same as above |
| `onItem` | `(@Sendable (MeetingNetworkCheckItem) -> Void)?` | No | Same as above |

When logged in, `meeting_api` probes the meeting API used for login; when not logged in, the meeting API address is derived from `serverUrl`, and if it can't be derived, `meeting_api` is `skipped` (`server_info_unavailable`).

#### `networkCheck(token:timeoutMs:onItem:)`

A shortcut when you already have an RTC channel token or IM token: only its `app_id` and `client_api` are used, not for authentication, so **an expired token also works**. Throws `SRTCError.invalidArgument` if the token can't be decoded.

#### `cancelNetworkCheck()`

Cancels the check running on this instance; the running `networkCheck` then throws `SRTCError.cancelled`. Does nothing if no check is running.

#### Rules and errors

+ **How `meeting_api` is judged**: it makes one signed call to a read-only meeting API, and **any HTTP response counts as reachable**; a network error or timeout counts as unreachable, in which case `server` is `fail` with `reason` `meeting_api_unreachable`. If `server` has already failed because of an SRTC subcheck, SRTC's `reason` is kept.
+ **Duration**: `meeting_api` runs in parallel with the SRTC checks, so it doesn't add to the total duration.
+ What the other items check, their reason codes, and platform limitations are the same as in SRTC; see [SRTC types](/en/rtc/swift/types#networkcheckitemid).

| Error | Low code | When |
| --- | :---: | --- |
| `SRTCError.alreadyJoined` | `005` | A check is already running (only one at a time) |
| `SRTCError.cancelled` | `026` | Cancelled by `cancelNetworkCheck()` or by the caller's task |
| `SRTCError.invalidArgument` | `031` | Empty parameters, a token that can't be decoded, or logged in but the RTC address can't be derived |
| `SMeetingError.notLoggedIn` | `001` | Not logged in, using the overload without parameters |

The first three are SRTC-layer errors passed through, with the same codes as when you call SRTC directly; only "not logged in" uses the meeting layer's `SMeetingError`.

---

### Virtual background

**iOS only**: starting with `1.7.0`, these members don't exist on macOS; wrap code shared by both platforms in `#if os(iOS)`. This is a **device-level setting** (it applies to the single shared camera capture pipeline in the process), and it applies to all meetings at once. After switching cameras, turning the camera off and on again, or reconnecting after a disconnect during the meeting, your app doesn't need to apply it again. For usage and tuning, see [Virtual background](/en/meeting/swift/advanced/virtual-background).

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

This group forwards to the audio and video layer, and the meeting layer doesn't keep a separate copy of the state.

---

### Audio and video processing

The following APIs are available since 1.9.0. They forward to the same-named SRTC APIs, and the meeting layer doesn't keep a separate copy of the state.

#### `audioCaptureProcessor`

The microphone capture processor, of type `AudioProcessor?`; `nil` clears it. The most common use is attaching the SRTC AI noise suppression plugin; see [AI noise suppression (DeepFilterNet)](/en/meeting/swift/advanced/deepfilternet).

```swift
let processor = try DeepFilterNetProcessor()
self.denoiser = processor                    // Kept by your code
meeting.audioCaptureProcessor = processor
```

+ **The SDK holds the processor weakly**: keep your own reference to the processor; otherwise it's released immediately and processing silently stops working.
+ Global; only one can be attached at a time, and you can set it at any time before or after entering a meeting.
+ When the processor conforms to `AudioProcessingDeclaring` (for example, the noise suppression plugin declares that built-in noise suppression should be off), the SDK turns off the corresponding WebRTC software processing as declared and restores it when cleared.

#### `defaultVideoProcessors`

Engine-level default video processors (beauty filters and so on), of type `[VideoProcessor]`. They apply automatically to camera tracks created **from then on**.

```swift
meeting.defaultVideoProcessors = [beautyProcessor]
```

A new camera track is created every time the camera is turned on, so processors attached only to `cameraTrack?.videoProcessors` are gone the next time; put "set it once" processors here.

---

### Related pages

+ [Virtual background](/en/meeting/swift/advanced/virtual-background)
+ [Media control APIs](/en/meeting/swift/api-reference/media-control)
+ [Device APIs](/en/meeting/swift/api-reference/devices)
+ [Meeting management APIs](/en/meeting/swift/api-reference/admin-actions)
+ [Events](/en/meeting/swift/events)
+ [Types](/en/meeting/swift/types)
