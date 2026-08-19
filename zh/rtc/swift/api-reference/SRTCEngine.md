---
title: "SRTCEngine"
description: "Swift 音视频 SDK 的主入口：加入频道、创建本地轨道、配置日志与音频处理器"
---

`SRTCEngine` 是 Swift SDK 的主入口，负责加入频道、离开频道、创建本地轨道以及配置日志和音频处理器。

---

### 初始化

#### `init()`

创建一个 SDK 实例，并完成底层 WebRTC 初始化。

```swift
let srtc = SRTCEngine()
```

---

### 属性

#### `logLevel`

设置 SDK 日志级别。

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | :---: | --- |
| `logLevel` | `LogLevel` | 否 | 可选值包括 `debug`、`info`、`warning`、`error` |

示例：

```swift
srtc.logLevel = .debug
```

#### `audioCaptureProcessor`

麦克风采集后的音频处理器，可用于变声、降噪等处理。

#### `audioRenderProcessor`

远端音频播放前处理器，可用于播放侧音频增强。

#### `channels`

已加入且仍存活的频道列表（`[Channel]`），按加入先后排序。空数组表示不在任何频道中。

#### `defaultChannel`

默认频道（`Channel?`）：最早加入且仍存活的那个，它离会后顺延到下一个。无参的
`leaveChannel()` 作用于它。详见[多频道](/zh/rtc/swift/advanced/multi-channel)。

---

### 方法

#### `joinChannel(token:options:)`

加入频道并返回 `Channel` 实例。可多次调用以同时加入多个频道，各频道的发布、订阅、成员与
事件互不干扰，仅当**同一频道名**已加入（或正在加入中）时抛 `alreadyJoined`。

```swift
let channel = try await srtc.joinChannel(
    token: token,
    options: JoinOptions(autoSubscribeAudio: true)
)
```

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | :---: | --- |
| `token` | `String` | 是 | Base64 编码的频道 Token |
| `options` | `JoinOptions` | 否 | 加入选项，默认 `JoinOptions()` |

**返回值：** `Channel`

**可能抛出：**

+ `SRTCError.alreadyJoined`
+ `SRTCError.tokenExpired`
+ `SRTCError.tokenInvalid`
+ 其他网络、信令、流媒体连接错误

---

#### `leaveChannel()`

离开默认频道（最早加入且仍存活的那个）。

```swift
await srtc.leaveChannel()
```

如果当前没有已加入的频道，调用会被安全忽略。

#### `leaveChannel(_:)`

离开指定频道，等价于 `channel.leave()`，其它频道不受影响。多频道下建议用这个版本，
避免「默认频道顺延」带来的歧义。

```swift
await srtc.leaveChannel(groupChannel)
```

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | :---: | --- |
| `channel` | `Channel` | 是 | 要离开的频道 |

---

#### `createLocalMicTrack(preset:)`

创建本地麦克风轨道。

```swift
let micTrack = srtc.createLocalMicTrack(preset: .music)
```

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | :---: | --- |
| `preset` | `MicPreset` | 否 | 默认 `.music` |

**返回值：** `LocalMicTrack`

---

#### `createLocalCameraTrack(preset:)`

创建本地摄像头轨道。

```swift
let cameraTrack = srtc.createLocalCameraTrack(preset: .h720p)
```

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | :---: | --- |
| `preset` | `CameraPreset` | 否 | 默认 `.h720p` |

**返回值：** `LocalCameraTrack`

---

#### `createLocalScreenTrack(preset:audioPreset:mode:)`

创建本地屏幕共享轨道。

```swift
let screenTrack = srtc.createLocalScreenTrack(
    preset: .h1080p,
    audioPreset: .default
)

// iOS 全屏采集（需先集成 Broadcast Upload Extension）
let fullScreen = srtc.createLocalScreenTrack(
    preset: .h720p,
    mode: .broadcast(appGroup: "group.your.app.group")
)
```

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | :---: | --- |
| `preset` | `ScreenPreset` | 否 | 屏幕共享视频预设，默认 `.h1080p` |
| `audioPreset` | `ScreenAudioPreset?` | 否 | macOS 下可用于开启屏幕音频 |
| `mode` | `ScreenCaptureMode` | 否 | 仅 iOS 有效，默认 `.inApp`（应用内采集）；`.broadcast(appGroup:)` 为全屏采集，见[屏幕共享](/zh/rtc/swift/advanced/screen-sharing) |

**返回值：** `LocalScreenTrack`

<Note>
iOS 全屏采集下 `startCapture()` 成功只代表 SDK 开始监听，画面要等用户从系统 UI 发起广播后
才会传输，真正的开始 / 结束通过 `TrackDelegate.screenBroadcastDidStart` /
`screenBroadcastDidFinish(_:reason:)` 通知。
</Note>

#### `createLocalScreenTrack(source:preset:audioPreset:)`

macOS 12.3+ 专用重载，用于指定显示器或窗口源。

```swift
let track = srtc.createLocalScreenTrack(
    source: selectedSource,
    preset: .h1080p,
    audioPreset: .default
)
```

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | :---: | --- |
| `source` | `ScreenCaptureSource?` | 否 | `DisplaySource` 或 `WindowSource`，为空时默认主显示器 |
| `preset` | `ScreenPreset` | 否 | 默认 `.h1080p` |
| `audioPreset` | `ScreenAudioPreset?` | 否 | 是否采集系统音频 |

**返回值：** `LocalScreenTrack`

---

#### `createLocalCustomVideoTrack(desc:)`

创建自定义视频轨道，适合外部推帧场景。

```swift
let customVideoTrack = srtc.createLocalCustomVideoTrack(desc: "canvas")
```

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | :---: | --- |
| `desc` | `String` | 否 | 轨道描述，默认 `"custom"` |

**返回值：** `LocalVideoTrack`

调用后可通过 `pushFrame(...)` 注入 `CVPixelBuffer`。

---

#### `createLocalCustomAudioTrack(desc:)`

创建自定义音频轨道，适合外部 PCM 输入场景。

```swift
let customAudioTrack = srtc.createLocalCustomAudioTrack(desc: "bgm")
```

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | :---: | --- |
| `desc` | `String` | 否 | 轨道描述，默认 `"custom"` |

**返回值：** `LocalAudioTrack`

调用后可通过 `pushAudioBuffer(...)` 注入 `AVAudioPCMBuffer`。

---

### 相关页面

+ [核心概念](/zh/rtc/swift/key-concepts)
+ [Channel 与 Track](/zh/rtc/swift/api-reference/media-tracks)
+ [事件参考](/zh/rtc/swift/events)
