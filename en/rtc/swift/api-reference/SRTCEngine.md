---
title: "SRTCEngine"
description: "API reference for SRTCEngine, the main entry point of the SRTC Swift SDK: joining and leaving one or more channels, creating microphone, camera, screen, and custom tracks, log level, audio processors, default video processors, and the virtual background methods."
---

`SRTCEngine` is the main entry point of the Swift SDK. It's responsible for joining channels, leaving channels, creating local tracks, and configuring logging and audio processors.

---

### Initialization

#### `init()`

Creates an SDK instance and completes the underlying WebRTC initialization.

```swift
let srtc = SRTCEngine()
```

---

### Properties

#### `logLevel`

Sets the SDK log level.

| Parameter | Type | Required | Description |
| --- | --- | :---: | --- |
| `logLevel` | `LogLevel` | No | Possible values include `debug`, `info`, `warning`, and `error` |

Example:

```swift
srtc.logLevel = .debug
```

#### `audioCaptureProcessor`

Audio processor applied after microphone capture, usable for voice changing, noise suppression, and similar processing.

#### `audioRenderProcessor`

Processor applied to remote audio before playback, usable for playback-side audio enhancement.

#### `channels`

The list of channels that have been joined and are still live (`[Channel]`), ordered by join time. An empty array means you're not in any channel.

#### `defaultChannel`

The default channel (`Channel?`): the earliest-joined one that's still live; once you leave it, the next one takes its place. The no-argument
`leaveChannel()` applies to it. See [Multi-channel](/en/rtc/swift/advanced/multi-channel) for details.

---

### Methods

#### `joinChannel(token:options:)`

Joins a channel and returns a `Channel` instance. You can call it multiple times to join several channels at once; each channel's publishing, subscriptions, users, and
events are independent of each other. It throws `alreadyJoined` only when **the same channel name** has already been joined (or a join is in progress).

```swift
let channel = try await srtc.joinChannel(
    token: token,
    options: JoinOptions(autoSubscribeAudio: true)
)
```

| Parameter | Type | Required | Description |
| --- | --- | :---: | --- |
| `token` | `String` | Yes | Base64-encoded channel token |
| `options` | `JoinOptions` | No | Join options; default `JoinOptions()` |

**Returns:** `Channel`

**Throws:**

+ `SRTCError.alreadyJoined`
+ `SRTCError.tokenExpired`
+ `SRTCError.tokenInvalid`
+ Other network, signaling, and media streaming connection errors

---

#### `leaveChannel()`

Leaves the default channel (the earliest-joined one that's still live).

```swift
await srtc.leaveChannel()
```

If no channel is currently joined, the call is safely ignored.

#### `leaveChannel(_:)`

Leaves the specified channel, equivalent to `channel.leave()`; other channels aren't affected. With multiple channels we recommend this version,
to avoid ambiguity from "the default channel moving to the next one".

```swift
await srtc.leaveChannel(groupChannel)
```

| Parameter | Type | Required | Description |
| --- | --- | :---: | --- |
| `channel` | `Channel` | Yes | The channel to leave |

---

#### `createLocalMicTrack(preset:)`

Creates a local microphone track.

```swift
let micTrack = srtc.createLocalMicTrack(preset: .music)
```

| Parameter | Type | Required | Description |
| --- | --- | :---: | --- |
| `preset` | `MicPreset` | No | Default `.music` |

**Returns:** `LocalMicTrack`

---

#### `createLocalCameraTrack(preset:)`

Creates a local camera track.

```swift
let cameraTrack = srtc.createLocalCameraTrack(preset: .h720p)
```

| Parameter | Type | Required | Description |
| --- | --- | :---: | --- |
| `preset` | `CameraPreset` | No | Default `.h720p` |

**Returns:** `LocalCameraTrack`

---

#### `createLocalScreenTrack(preset:audioPreset:mode:)`

Creates a local screen-sharing track.

```swift
let screenTrack = srtc.createLocalScreenTrack(
    preset: .h1080p,
    audioPreset: .default
)

// iOS full-screen capture (requires integrating a Broadcast Upload Extension first)
let fullScreen = srtc.createLocalScreenTrack(
    preset: .h720p,
    mode: .broadcast(appGroup: "group.your.app.group")
)
```

| Parameter | Type | Required | Description |
| --- | --- | :---: | --- |
| `preset` | `ScreenPreset` | No | Screen-sharing video preset; default `.h1080p` |
| `audioPreset` | `ScreenAudioPreset?` | No | On macOS, can be used to enable screen audio |
| `mode` | `ScreenCaptureMode` | No | iOS only; default `.inApp` (in-app capture); `.broadcast(appGroup:)` is full-screen capture—see [Screen sharing](/en/rtc/swift/advanced/screen-sharing) |

**Returns:** `LocalScreenTrack`

<Note>
With iOS full-screen capture, a successful `startCapture()` only means the SDK has started listening; video is transmitted only after the user starts the broadcast from the system UI.
The actual start / end is notified through `TrackDelegate.screenBroadcastDidStart` /
`screenBroadcastDidFinish(_:reason:)`.
</Note>

#### `createLocalScreenTrack(source:preset:audioPreset:excludedWindowIds:excludesCurrentApplication:)`

Overload for macOS 12.3+ only, used to specify a display or window source.

```swift
let track = srtc.createLocalScreenTrack(
    source: selectedSource,
    preset: .h1080p,
    audioPreset: .default
)

// Share the full display while cutting out your own windows that render this shared content
let previewWindowIds = NSApplication.shared.windows
    .filter { $0.isVisible && $0.identifier?.rawValue == "meeting-room" }
    .map { UInt32($0.windowNumber) }
let shared = srtc.createLocalScreenTrack(
    source: display,
    excludedWindowIds: previewWindowIds
)
```

| Parameter | Type | Required | Description |
| --- | --- | :---: | --- |
| `source` | `ScreenCaptureSource?` | No | `DisplaySource` or `WindowSource`; defaults to the main display when empty |
| `preset` | `ScreenPreset` | No | Default `.h1080p` |
| `audioPreset` | `ScreenAudioPreset?` | No | Whether to capture system audio |
| `excludedWindowIds` | `[UInt32]` | No | Your own windows to cut out when sharing a full display, as `UInt32(NSWindow.windowNumber)`; meaningless when capturing a single window. Default `[]` |
| `excludesCurrentApplication` | `Bool` | No | Set to `true` to go back to the old behavior of excluding the entire app from the capture; `excludedWindowIds` is then ignored. Default `false` |

**Returns:** `LocalScreenTrack`

<Warning>
Since 1.4.2, full-display sharing **includes your own app's windows by default**. Put every window that renders this shared content into `excludedWindowIds`; otherwise you get an infinite mirror. The window list is snapshotted once at `startCapture()`, and windows opened afterward all appear in the capture.
</Warning>

---

#### `createLocalCustomVideoTrack(desc:)`

Creates a custom video track, for scenarios where frames are pushed from outside.

```swift
let customVideoTrack = srtc.createLocalCustomVideoTrack(desc: "canvas")
```

| Parameter | Type | Required | Description |
| --- | --- | :---: | --- |
| `desc` | `String` | No | Track description; default `"custom"` |

**Returns:** `LocalVideoTrack`

After calling it, you can inject `CVPixelBuffer` values through `pushFrame(...)`.

---

#### `createLocalCustomAudioTrack(desc:)`

Creates a custom audio track, for scenarios with external PCM input.

```swift
let customAudioTrack = srtc.createLocalCustomAudioTrack(desc: "bgm")
```

| Parameter | Type | Required | Description |
| --- | --- | :---: | --- |
| `desc` | `String` | No | Track description; default `"custom"` |

**Returns:** `LocalAudioTrack`

After calling it, you can inject `AVAudioPCMBuffer` values through `pushAudioBuffer(...)`.

---

### Video preprocessing

#### `defaultVideoProcessors`

The default video processor pipeline. Configure it once here, and **every camera track created afterward picks it up automatically**.

```swift
srtc.defaultVideoProcessors = [myProcessor]
```

| Parameter | Type | Required | Description |
| --- | --- | :---: | --- |
| `defaultVideoProcessors` | `[VideoProcessor]` | No | Empty by default |

A camera track is created anew every time the camera is turned on (turning the camera off destroys it), so if you set processors only on the track, the effect is gone the next time the camera is turned on—this property exists for exactly that reason. It affects only tracks created **afterward** and doesn't apply retroactively to existing tracks; custom video tracks aren't affected (frames on that path are pushed by you via `pushFrame`, so you decide whether they go through processors).

---

### Virtual background

The following methods forward to `SRTCVirtualBackground.shared`, with a single process-wide state. Once enabled, it **automatically applies to all camera tracks**, and you don't need to add anything to `videoProcessors`. For usage and tuning, see [Virtual background](/en/rtc/swift/advanced/virtual-background).

| Member | Signature | Description |
| --- | --- | --- |
| Install | `installVirtualBackground(modelPath: String? = nil) throws` | Loads the model + creates the inference session, taking hundreds of milliseconds; don't call it on the main thread / capture thread; `nil` uses the built-in model |
| Uninstall | `uninstallVirtualBackground()` | Releases the inference session and buffers; doesn't clear effect parameters |
| Master switch | `enableVirtualBackground(_ enabled: Bool) throws` | When off, it's a zero-overhead pass-through with no inference |
| Switch state | `isVirtualBackgroundEnabled: Bool` | Read-only |
| Background blur | `setVirtualBackgroundBlur(level: Int)` | `level` ranges 1–10, default 5; out-of-range values are clamped to the bounds |
| Background replacement | `setVirtualBackgroundImage(_ image: SRTCNativeImage?)` | Scaled to cover (cropped, not stretched); `nil` falls back to blur. There's also a `CGImage` overload |
| Inference interval | `setVirtualBackgroundInferenceInterval(_ interval: Int)` | Segmentation runs once every N frames (compositing still runs every frame); default 1 |
| Mask sync | `setVirtualBackgroundMaskSync(_ enabled: Bool)` | Default `false`; makes no difference when `interval` is 1 |
| Instance | `virtualBackground: SRTCVirtualBackground` | For diagnostics: `droppedFrameCount`, `isInstalled`, `effect`, `inferenceIntervalMs`, and more |

**Throws:** `SRTCError.virtualBackgroundAlreadyInstalled`, `.virtualBackgroundNotInstalled`, `.virtualBackgroundModelNotFound(String)`, `.virtualBackgroundSessionFailed(String)`

Background blur and background replacement are mutually exclusive, and the later call wins; both are also remembered if called before installing, and take effect automatically once installation completes.

---

### Related pages

+ [Key concepts](/en/rtc/swift/key-concepts)
+ [Virtual background](/en/rtc/swift/advanced/virtual-background)
+ [Channel and Track](/en/rtc/swift/api-reference/media-tracks)
+ [Events](/en/rtc/swift/events)
