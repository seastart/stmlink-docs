---
title: "Channel 与 Track"
description: "Channel 会话对象与本地/远端轨道类：发布、订阅、渲染与采集控制"
---

### Channel

`Channel` 表示一次已建立的频道会话，是发布、订阅、消息和用户状态的核心入口。

---

#### 属性

| 属性名 | 类型 | 说明 |
| --- | --- | --- |
| `delegates` | `MulticastDelegate<ChannelDelegate>` | 注册频道事件回调 |
| `connectState` | `ConnectionState` | 当前连接状态 |
| `channelInfo` | `ChannelInfo?` | 当前频道信息 |
| `me` | `User?` | 当前用户 |
| `streamVendor` | `StreamVendor` | 当前流媒体引擎供应商 |

---

#### `getUsers()`

获取当前频道内所有用户信息。

```swift
let users = channel.getUsers()
```

**返回值：** `[String: UserInfo]`

---

#### `getUser(_:)`

按 `uid` 获取用户对象。

```swift
let user = channel.getUser("alice")
```

**返回值：** `User?`

---

#### `publishLocalTrack(_:)`

发布本地音频或视频轨道。

```swift
try await channel.publishLocalTrack(micTrack)
try await channel.publishLocalTrack(cameraTrack)
```

支持的重载：

+ `publishLocalTrack(_ track: LocalAudioTrack, options: AudioPublishOptions? = nil)`
+ `publishLocalTrack(_ track: LocalVideoTrack, options: VideoPublishOptions? = nil)`

注意：

+ 音频轨道会走内部混音发送模型
+ `LocalScreenTrack` 如果带有屏幕音频，会自动一并发布音频部分

---

#### `unpublishLocalTrack(_:)`

取消发布本地音频或视频轨道。

```swift
try await channel.unpublishLocalTrack(micTrack)
try await channel.unpublishLocalTrack(cameraTrack)
```

建议业务层在取消发布后，再调用 `stopCapture()` 释放采集资源。

---

#### `subscribeRemoteAudioTrack(uid:trackId:)`

订阅远端音频轨道。

```swift
try await channel.subscribeRemoteAudioTrack(uid: uid, trackId: trackId)
```

---

#### `subscribeRemoteVideoTrack(uid:trackId:)`

订阅远端视频轨道。

```swift
try await channel.subscribeRemoteVideoTrack(uid: uid, trackId: trackId)
```

---

#### `subscribeRemoteVideoMcuTrack()`

订阅频道级 MCU 合成视频（1.5.3 起）。服务端合成任务把频道内的画面合成一路，以保留身份 `__mcu__` 发布，
**这个身份不在频道成员列表里**，所以不能用 `subscribeRemoteVideoTrack(uid:trackId:)`，要用本方法。

```swift
let mcu = try await channel.subscribeRemoteVideoMcuTrack()
mcu.addRenderer(renderer)          // 或交给 SRTCVideoView(track: mcu)

try await channel.unsubscribeRemoteVideoMcuTrack()
```

**返回值：** `RemoteVideoMcuTrack`（继承 `RemoteVideoTrack`），重复调用返回同一对象；当前订阅中的轨道也可通过 `channel.remoteVideoMcuTrack` 取到。

<Note>
合成任务没开时 SFU 找不到这一路，SDK 会重试几秒后放弃（不抛错，也不出画面）。合成任务比订阅晚起来的场景，在任务开始运行后再调一次即可，调用是幂等的。
收流超时 / 恢复照常经 `didChangeReceiveStreamStatus` 上报，`uid` 为 `RemoteVideoMcuTrack.publisherUid`（`"__mcu__"`）。
</Note>

---

#### `unsubscribeRemoteTrack(_:debounceMs:)`

取消订阅远端轨道。

```swift
try await channel.unsubscribeRemoteTrack(track)
```

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | :---: | --- |
| `track` | `Track` | 是 | 远端轨道对象 |
| `debounceMs` | `Int` | 否 | 默认 `2000`，用于降低频繁订阅抖动 |

---

#### `getRemoteTrack(uid:trackId:)`

按用户和轨道 ID 取回远端轨道对象。

```swift
let track = channel.getRemoteTrack(uid: uid, trackId: trackId)
```

**返回值：** `Track?`

---

#### `getRemoteTrackByDesc(uid:desc:)`

按 `desc` 获取远端轨道。

```swift
let screenTrack = channel.getRemoteTrackByDesc(uid: uid, desc: "screen")
```

---

---

### Track 基类

所有轨道都继承自 `Track`，共享以下核心属性：

| 属性名 | 类型 | 说明 |
| --- | --- | --- |
| `id` | `String` | 轨道 ID |
| `kind` | `TrackKind` | `audio` 或 `video` |
| `desc` | `String` | 轨道描述，如 `mic`、`screen`、`camera_big` |
| `info` | `TrackInfo` | 当前轨道信息快照 |
| `uid` | `String?` | 轨道所属用户 UID |
| `delegates` | `MulticastDelegate<TrackDelegate>` | 轨道级事件回调 |

通用方法：

+ `getInfo()`

---

### LocalMicTrack

#### 采集控制

+ `startCapture(options:)`
+ `stopCapture()`
+ `restartCapture()`

#### 用户控制

+ `mute()`
+ `unmute()`
+ `changeDeviceId(_:)`

典型用法：

```swift
let micTrack = srtc.createLocalMicTrack(preset: .music)
try await micTrack.startCapture()
try await channel.publishLocalTrack(micTrack)
micTrack.mute()
micTrack.unmute()
```

---

### LocalCameraTrack

#### 采集控制

+ `startCapture(options:)`
+ `stopCapture()`
+ `restartCapture()`

#### 用户控制

+ `mute()`
+ `unmute()`
+ `changeDeviceId(_:)`
+ `switchCamera()`

#### 渲染相关

+ `addRenderer(_:)`
+ `removeRenderer(_:)`
+ `removeAllRenderers()`

---

### LocalScreenTrack

#### 采集控制

+ `startCapture(options:)`
+ `stopCapture()`
+ `restartCapture()`

#### 用户控制

+ `mute()`
+ `unmute()`

#### 屏幕音频

+ `audioTrack`
+ `setAudioTrack(_:)`
+ `getAudioTrack()`

#### 采集方式与状态（iOS）

| 成员 | 类型 | 说明 |
| --- | --- | --- |
| `captureMode` | `ScreenCaptureMode` | 采集方式，创建时由 `createLocalScreenTrack(mode:)` 决定；macOS 忽略 |
| `isCapturing` | `Bool` | 是否已开始采集。全屏采集下它表示「监听就绪」，并不代表有画面 |
| `isBroadcastActive` | `Bool` | 全屏采集下扩展是否正在推流，即**对端能否看到画面**；展示「共享中」状态应看这个 |

---

### LocalAudioTrack

适用于自定义音频输入：

+ `mute()`
+ `unmute()`
+ `pushAudioBuffer(_:)`

这类轨道通常不需要 `startCapture()`，而是由业务层持续注入 PCM 数据。

---

### LocalVideoTrack

适用于自定义视频输入：

+ `addRenderer(_:)`
+ `removeRenderer(_:)`
+ `removeAllRenderers()`
+ `pushFrame(_:rotation:timestampNs:)`

如果你有外部渲染管线、Canvas、屏幕编码器或 AI 处理链路，这个入口更合适。

---

### RemoteAudioTrack

#### 播放控制

+ `startPlay()`
+ `stopPlay()`
+ `isPlaying`

#### PCM 数据回调

+ `add(audioRenderer:)`
+ `remove(audioRenderer:)`

`AudioRenderer` 回调会拿到 `AVAudioPCMBuffer`，适合做语音转写、录制或二次分析。

---

### RemoteVideoTrack

#### 渲染控制

+ `addRenderer(_:)`
+ `removeRenderer(_:)`
+ `removeAllRenderers()`

远端视频通常在订阅成功后，通过 `SRTCVideoView(track:)` 或 `SRTCVideoRenderer` 展示。

#### 收流状态

+ `isReceiveTimedOut: Bool`

这一路视频当前是否已判定收流超时。值与 `channel(_:didChangeReceiveStreamStatus:)` 最近一次上报的 `timedOut` 一致，适合在渲染视图初始化、或从后台回到前台时**补一次当前状态**，避免只靠事件导致 UI 与实际不同步。日常的「加载中」指示仍建议由事件驱动，详见[事件参考](/zh/rtc/swift/events)。

---

### 渲染组件

#### `SRTCVideoView`

SwiftUI 场景优先使用：

```swift
SRTCVideoView(track: track)
    .frame(width: 320, height: 180)
```

#### `VideoView`

UIKit / AppKit 场景下使用 `bind(track:)` / `unbind()` 管理绑定关系。

#### `SRTCVideoRenderer`

更底层的渲染视图，由轨道显式调用 `addRenderer(_:)` 绑定。
