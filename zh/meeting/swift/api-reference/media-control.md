---
title: "媒体控制"
description: "SMeeting Swift SDK 媒体控制接口参考：摄像头、麦克风、屏幕共享、远端订阅与播放"
---

本页接口都挂在 `SMeetingEngine` 上。使用说明见 [媒体控制](/zh/meeting/swift/advanced/media-control) 与 [视频渲染](/zh/meeting/swift/advanced/video-rendering)。

`NativeVideoView` 是 SDK 为渲染视图定义的别名，实际类型是 SRTC 的 `SRTCVideoRenderer`。

---

### 摄像头

#### `requestOpenCamera(view:deviceId:preset:byAdmin:adminUid:)`

打开摄像头：向会议申请 → 开始采集 → 发布。

```swift
let track = try await meeting.requestOpenCamera()
```

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | :---: | --- |
| `view` | `NativeVideoView?` | 否 | 本地预览视图。SwiftUI 传 `nil`，改用 `SRTCVideoView(track:)` |
| `deviceId` | `String?` | 否 | 指定摄像头，取自 `getDevices(kind: .videoInput)`；不传用默认设备 |
| `preset` | `CameraPreset` | 否 | 采集预设，默认 `.h720p` |
| `byAdmin` | `Bool` | 否 | 是否在响应主持人的开启邀请，默认 `false` |
| `adminUid` | `String?` | 否 | 发起邀请的主持人 ID，`byAdmin` 为 `true` 时必须一起传 |

**返回值：** `LocalCameraTrack`（可忽略，也可随时读 `meeting.cameraTrack`）

**可能抛出：**

+ `SMeetingError.unauthorized` —— 房间全体禁画且禁止自我解除，且你不是主持人 / 联席主持人
+ `SMeetingError.apiError(code:message:)`
+ 采集或发布失败时的底层错误（此时 SDK 已自动回滚，无需你再调 `closeCamera()`）

已经打开时重复调用不会重复起流；如果传入了不同的 `deviceId`，会切到目标设备。

---

#### `closeCamera()`

```swift
await meeting.closeCamera()
```

**返回值：** 无，不抛错。会取消发布、移除渲染视图、停止采集，并上报 `userCameraStateDidChange`。

---

#### `switchCamera(deviceId:)`

```swift
try await meeting.switchCamera()                     // iOS 前后摄互切
try await meeting.switchCamera(deviceId: deviceId)   // 切到指定设备
```

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | :---: | --- |
| `deviceId` | `String?` | 否 | 目标摄像头；不传时在 iOS 上做前后摄互切 |

**返回值：** 无

**可能抛出：** `SMeetingError.deviceError(_:)` —— 摄像头尚未开启

---

### 麦克风

#### `requestOpenMic(deviceId:preset:byAdmin:adminUid:)`

```swift
try await meeting.requestOpenMic()
```

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | :---: | --- |
| `deviceId` | `String?` | 否 | 指定麦克风，取自 `getDevices(kind: .audioInput)` |
| `preset` | `MicPreset` | 否 | 采集预设，默认 `.music` |
| `byAdmin` | `Bool` | 否 | 是否在响应主持人的开启邀请，默认 `false` |
| `adminUid` | `String?` | 否 | 发起邀请的主持人 ID |

**返回值：** 无

**可能抛出：**

+ `SMeetingError.unauthorized` —— 房间全体静音且禁止自我解除，且你不是主持人 / 联席主持人
+ `SMeetingError.apiError(code:message:)`
+ 采集或发布失败时的底层错误（SDK 会自动回滚）

---

#### `closeMic()`

```swift
await meeting.closeMic()
```

**返回值：** 无，不抛错。会取消发布、停止采集，并上报 `userMicStateDidChange`。

---

### 屏幕共享

#### `requestShare(shareType:preset:view:byAdmin:adminUid:)`

```swift
try await meeting.requestShare()
```

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | :---: | --- |
| `shareType` | `ShareType` | 否 | `.screen`（默认）或 `.whiteBoard` |
| `preset` | `ScreenPreset` | 否 | 采集预设，默认 `.h1080p` |
| `view` | `NativeVideoView?` | 否 | 本地预览视图 |
| `byAdmin` | `Bool` | 否 | 是否在响应主持人的开启邀请，默认 `false` |
| `adminUid` | `String?` | 否 | 发起邀请的主持人 ID |

**返回值：** 无

**可能抛出：**

+ `SMeetingError.unauthorized` —— 房间禁共享且你不是主持人 / 联席主持人
+ `SMeetingError.internalError(_:)` —— 本端已在共享
+ `SMeetingError.apiError(code:message:)`
+ 采集失败（例如用户拒绝屏幕录制授权）时的底层错误

`shareType` 为 `.whiteBoard` 时不创建媒体流，只广播共享状态并触发 `roomShareDidStart`。

---

#### `requestShare(source:preset:view:byAdmin:adminUid:)`

指定采集源的重载，**仅 macOS 12.3 及以上**。

```swift
let displays = try await ScreenCaptureSources.availableDisplays()
try await meeting.requestShare(source: displays[0])
```

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | :---: | --- |
| `source` | `ScreenCaptureSource` | 是 | `DisplaySource`（显示器）或 `WindowSource`（应用窗口） |
| `preset` | `ScreenPreset` | 否 | 采集预设，默认 `.h1080p` |
| `view` | `NativeVideoView?` | 否 | 本地预览视图 |
| `byAdmin` | `Bool` | 否 | 是否在响应主持人的开启邀请 |
| `adminUid` | `String?` | 否 | 发起邀请的主持人 ID |

**返回值：** 无

**可能抛出：** 同上一个重载。

---

#### `stopShare()`

```swift
await meeting.stopShare()
```

**返回值：** 无，不抛错。

---

### 远端视频

#### `subscribeRemoteVideoTrack(uid:trackDesc:)`

订阅远端视频轨道，不绑定渲染视图。

```swift
let track = try await meeting.subscribeRemoteVideoTrack(uid: uid, trackDesc: .cameraBig)
```

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | :---: | --- |
| `uid` | `String` | 是 | 远端成员 ID |
| `trackDesc` | `TrackDesc` | 是 | 轨道描述，例如 `.cameraBig`、`.screen` |

**返回值：** `RemoteVideoTrack`

**可能抛出：**

+ `SMeetingError.notInMeeting`
+ `SMeetingError.internalError(_:)` —— 该成员没有这一路轨道

---

#### `unsubscribeRemoteVideoTrack(uid:trackDesc:)`

无条件取消订阅，不考虑是否还有渲染视图在用。

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | :---: | --- |
| `uid` | `String` | 是 | 远端成员 ID |
| `trackDesc` | `TrackDesc` | 是 | 轨道描述 |

**返回值：** 无

**可能抛出：** `SMeetingError.notInMeeting`。轨道不存在时静默返回。

---

#### `startPlayRemoteVideo(view:uid:trackDesc:)`

订阅并把画面绑定到传入的渲染视图，适合 UIKit / AppKit。

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | :---: | --- |
| `view` | `NativeVideoView` | 是 | 已挂在视图层级上的渲染视图 |
| `uid` | `String` | 是 | 远端成员 ID |
| `trackDesc` | `TrackDesc` | 是 | 轨道描述 |

**返回值：** `RemoteVideoTrack`

**可能抛出：** 同 `subscribeRemoteVideoTrack(uid:trackDesc:)`

---

#### `stopPlayRemoteVideo(view:uid:trackDesc:)`

解绑渲染视图。**只有当这路轨道上已经没有任何渲染视图时**才会真正取消订阅。

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | :---: | --- |
| `view` | `NativeVideoView` | 是 | 要解绑的渲染视图 |
| `uid` | `String` | 是 | 远端成员 ID |
| `trackDesc` | `TrackDesc` | 是 | 轨道描述 |

**返回值：** 无

**可能抛出：** `SMeetingError.notInMeeting`

---

### 远端音频

进入会议时远端音频已自动订阅，以下接口用于需要精细控制的场景。

#### `subscribeRemoteAudioTrack(uid:trackDesc:)`

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | :---: | --- |
| `uid` | `String` | 是 | 远端成员 ID |
| `trackDesc` | `TrackDesc` | 否 | 默认 `.mic` |

**返回值：** 无

**可能抛出：** `SMeetingError.notInMeeting`、`SMeetingError.internalError(_:)`

#### `unsubscribeRemoteAudioTrack(uid:trackDesc:)`

参数同上。轨道不存在时静默返回。

#### `toggleRemoteAudioMute(_:)`

远端音频播放总开关，只切播放不改订阅关系。

```swift
meeting.toggleRemoteAudioMute(true)   // 静音
```

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | :---: | --- |
| `mute` | `Bool` | 是 | `true` 静音，`false` 恢复播放 |

**返回值：** 无，不抛错。

---

### 合屏画面（MCU）

#### `startPlayRemoteVideoMcu(view:uid:)`

订阅并播放服务端合成画面。需要服务端已配置合屏任务。

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | :---: | --- |
| `view` | `NativeVideoView` | 是 | 渲染视图 |
| `uid` | `String` | 是 | 合成画面对应的用户 ID |

**返回值：** `RemoteVideoTrack`

**可能抛出：** `SMeetingError.notInMeeting`、`SMeetingError.internalError(_:)`（未找到合成画面轨道）

#### `stopPlayRemoteVideoMcu(view:)`

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | :---: | --- |
| `view` | `NativeVideoView` | 是 | 之前传入的渲染视图 |

**返回值：** 无

---

### 相关页面

+ [媒体控制](/zh/meeting/swift/advanced/media-control)
+ [视频渲染](/zh/meeting/swift/advanced/video-rendering)
+ [屏幕共享](/zh/meeting/swift/advanced/screen-sharing)
