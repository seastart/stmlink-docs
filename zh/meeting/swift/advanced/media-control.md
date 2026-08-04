---
title: "媒体控制"
description: "SMeeting Swift SDK 中摄像头、麦克风、扬声器的开关与切换，以及房间媒体策略的影响"
---

### 概述

会议里的媒体控制分成三块：

+ **本端采集与发布**：摄像头、麦克风、屏幕共享
+ **远端播放**：远端音频总开关、远端视频订阅
+ **房间策略**：主持人设置的全体静音 / 全体禁画 / 禁共享会直接影响你能不能开

命名上有一条明确规律：**开启侧带 `request`，关闭侧不带**。

| 动作 | 开启 | 关闭 |
| --- | --- | --- |
| 麦克风 | `requestOpenMic(...)` | `closeMic()` |
| 摄像头 | `requestOpenCamera(...)` | `closeCamera()` |
| 共享 | `requestShare(...)` | `stopShare()` |

开启侧是 `throws` 的（可能被房间策略拒绝、可能采集失败），关闭侧不会抛错，可以放心直接调。

---

### 麦克风

#### 打开与关闭

```swift
try await meeting.requestOpenMic()
await meeting.closeMic()
```

`requestOpenMic` 做的事情依次是：向会议申请开麦 → 起本地麦克风采集 → 发布到会议 → 抛出 `userMicStateDidChange` 事件。

#### 指定设备与音质预设

```swift
try await meeting.requestOpenMic(
    deviceId: selectedMicId,   // 来自 getDevices(kind: .audioInput)
    preset: .music
)
```

如果麦克风已经打开，再次调用并传入不同的 `deviceId`，SDK 会直接切到目标设备而不是忽略这次调用。

`preset` 取值来自 SRTC 的 `MicPreset`：`.speech`、`.music`（默认）、`.musicStereo`、`.musicHighQuality`、`.musicHighQualityStereo`。

---

### 摄像头

#### 打开与关闭

```swift
let track = try await meeting.requestOpenCamera()
await meeting.closeCamera()
```

`requestOpenCamera` 返回 `LocalCameraTrack`，也可以随时通过 `meeting.cameraTrack` 拿到（未开启时为 `nil`）。

#### 参数说明

```swift
try await meeting.requestOpenCamera(
    view: nil,                 // SwiftUI 传 nil
    deviceId: selectedCameraId,
    preset: .h720p
)
```

+ `view` 只在 UIKit / AppKit 场景需要传，且必须是一个**已经挂在视图层级上**的 `SRTCVideoRenderer`。SwiftUI 场景一律传 `nil`，把 `meeting.cameraTrack` 交给 `SRTCVideoView(track:)` 即可
+ `preset` 取值来自 SRTC 的 `CameraPreset`：`.h180p`、`.h360p`、`.h720p`（默认）、`.h1080p`

#### 切换摄像头

```swift
// iOS：前后摄互切
try await meeting.switchCamera()

// 指定设备（桌面端多摄像头）
try await meeting.switchCamera(deviceId: deviceId)
```

摄像头未打开时调用会抛出 `SMeetingError.deviceError`。

---

### 房间策略对开启的影响

主持人可以设置房间级的媒体策略，它们会直接决定普通成员能否自行开启：

| 房间字段 | 含义 |
| --- | --- |
| `RoomInfo.micDisabled` | 房间全体静音 |
| `RoomInfo.selfUnmuteMicDisabled` | 禁止成员自我解除静音 |
| `RoomInfo.cameraDisabled` | 房间全体禁画 |
| `RoomInfo.selfUnmuteCameraDisabled` | 禁止成员自我解除禁画 |
| `RoomInfo.shareDisabled` | 房间禁共享 |

当「全体静音」且「禁止自我解除」同时为 `true`，且你不是主持人 / 联席主持人时，`requestOpenMic()` 会抛出 `SMeetingError.unauthorized`。摄像头同理。

建议在 UI 上提前反映这个状态，而不是让用户点了按钮才收到报错：

```swift
let info = meeting.getRoomInfo()
let canUnmuteSelf = !(info?.micDisabled == true && info?.selfUnmuteMicDisabled == true) || isAdmin
```

此外，当主持人在会中打开「全体静音」时，非主持人成员的麦克风会被 SDK 自动关闭，并上报一次 `userMicStateDidChange`（`byAdmin` 为 `true`）。摄像头同理。

---

### 响应主持人的开启邀请

主持人可以邀请某位成员开麦或开摄像头，成员端会收到事件：

```swift
func meeting(_ meeting: SMeetingEngine, adminDidRequestOpenMic data: AdminRequestOpenMicEventData) {
    // data.opUid 是发起邀请的主持人
}
```

同意时，把 `byAdmin` 与 `adminUid` 一起传给开启接口：

```swift
try await meeting.requestOpenMic(byAdmin: true, adminUid: data.opUid)
try await meeting.requestOpenCamera(byAdmin: true, adminUid: data.opUid)
```

拒绝时调用对应的拒绝接口：

```swift
try await meeting.rejectOpenMic(adminUid: data.opUid)
try await meeting.rejectOpenCamera(adminUid: data.opUid)
```

> 传了 `byAdmin: true` 就必须同时传 `adminUid`，否则这次调用不会带上「响应邀请」的语义。

主持人也可以直接关闭某位成员的麦克风 / 摄像头，被关闭方不需要处理，SDK 会自动停流并上报 `userMicStateDidChange` / `userCameraStateDidChange`（`byAdmin` 为 `true`，`opUid` 为操作者）。

---

### 远端音频

远端音频在进入会议时会自动订阅，你通常只需要一个「扬声器开关」：

```swift
meeting.toggleRemoteAudioMute(true)   // 静音，不再播放远端声音
meeting.toggleRemoteAudioMute(false)  // 恢复播放
```

这个方法只切播放开关，不会退订，因此来回切换没有重新协商的代价。

如果你确实需要按成员精细控制订阅关系（例如只听某几路），可以用：

```swift
try await meeting.subscribeRemoteAudioTrack(uid: uid)
try await meeting.unsubscribeRemoteAudioTrack(uid: uid)
```

---

### 退会前的清理

`exitRoom()` 会离开会议，但本地采集建议由你显式关掉，让 UI 状态和硬件状态同时归位：

```swift
await meeting.closeCamera()
await meeting.closeMic()
await meeting.stopShare()
await meeting.exitRoom()
```

---

### 相关页面

+ [外设管理](/zh/meeting/swift/advanced/device-management)
+ [视频渲染](/zh/meeting/swift/advanced/video-rendering)
+ [屏幕共享](/zh/meeting/swift/advanced/screen-sharing)
+ [接口文档 - 媒体控制](/zh/meeting/swift/api-reference/media-control)
