---
title: "Channel 与 Track"
description: "SRTC Swift SDK 中 Channel、Track 与渲染相关接口参考"
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
| `rtcTrack` | `LKRTCMediaStreamTrack?` | 底层 WebRTC 轨道 |
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
