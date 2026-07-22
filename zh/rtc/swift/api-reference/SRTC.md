---
title: "SRTC"
description: "SRTC Swift SDK 主入口类接口参考"
---

`SRTC` 是 Swift SDK 的主入口，负责加入频道、离开频道、创建本地轨道以及配置日志和音频处理器。

---

### 初始化

#### `init()`

创建一个 SDK 实例，并完成底层 WebRTC 初始化。

```swift
let srtc = SRTC()
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

---

### 方法

#### `joinChannel(token:options:)`

加入频道并返回 `Channel` 实例。

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

离开当前频道。

```swift
await srtc.leaveChannel()
```

如果当前没有已加入的频道，调用会被安全忽略。

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

#### `createLocalScreenTrack(preset:audioPreset:)`

创建本地屏幕共享轨道。

```swift
let screenTrack = srtc.createLocalScreenTrack(
    preset: .h1080p,
    audioPreset: .default
)
```

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | :---: | --- |
| `preset` | `ScreenPreset` | 否 | 屏幕共享视频预设，默认 `.h1080p` |
| `audioPreset` | `ScreenAudioPreset?` | 否 | macOS 下可用于开启屏幕音频 |

**返回值：** `LocalScreenTrack`

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
