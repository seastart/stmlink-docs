---
title: "屏幕共享"
description: "SRTC Swift SDK 在 macOS 与 iOS 上的屏幕共享接入方式与平台差异"
---

### 平台差异

| 平台 | 支持情况 | 说明 |
| --- | --- | --- |
| macOS 12.3+ | 支持显示器 / 窗口共享 | 基于 `ScreenCaptureKit` |
| iOS | 支持应用内屏幕采集 | 不支持像 macOS 一样选择任意桌面窗口 |
| iOS 系统音频 | 不支持 | SDK 会忽略屏幕音频采集选项 |

---

### 基本用法

#### 默认创建屏幕共享轨道

```swift
let screenTrack = srtc.createLocalScreenTrack(preset: .h1080p)
try await screenTrack.startCapture()
try await channel.publishLocalTrack(screenTrack)
```

如果你不需要系统音频，这是最直接的接法。

---

### macOS：选择显示器或窗口

macOS 下，业务层需要先枚举采集源，再把用户选中的源传给 SDK：

```swift
import SRTC

@available(macOS 12.3, *)
func startScreenShare(srtc: SRTC, channel: Channel) async throws {
    let displays = try await ScreenCaptureSources.availableDisplays()
    let windows = try await ScreenCaptureSources.availableWindows()

    // 业务层自行展示选择 UI，这里以第一块显示器为例
    let selectedSource = displays.first

    let screenTrack = srtc.createLocalScreenTrack(
        source: selectedSource,
        preset: .h1080p
    )
    try await screenTrack.startCapture()
    try await channel.publishLocalTrack(screenTrack)
}
```

这里要注意一个设计边界：

+ SDK 负责“发现可共享的源”和“实际开始采集”
+ 业务层负责“如何把显示器 / 窗口列表展示给用户”

这样做的好处是 SDK 不绑定任何特定 UI 方案，SwiftUI、AppKit、TCA、MVVM 都能接入。

---

### macOS：同时采集系统音频

如果你要在屏幕共享时一起发送系统音频，可以传入 `audioPreset`：

```swift
let screenTrack = srtc.createLocalScreenTrack(
    source: selectedSource,
    preset: .h1080p,
    audioPreset: .default
)

try await screenTrack.startCapture()
try await channel.publishLocalTrack(screenTrack)
```

发布 `LocalScreenTrack` 时，如果它内部存在 `audioTrack`，SDK 会自动把屏幕音频一并走音频混音链路发送出去。

---

### iOS：应用内屏幕采集

iOS 下不需要传入 `source`：

```swift
let screenTrack = srtc.createLocalScreenTrack(preset: .h1080p)
try await screenTrack.startCapture()
try await channel.publishLocalTrack(screenTrack)
```

需要明确的是：

+ 这里是应用内采集模型，不是桌面级窗口选择模型
+ 即便传入 `audioPreset`，iOS 也不会采集系统音频

---

### 停止共享

```swift
try await channel.unpublishLocalTrack(screenTrack)
try await screenTrack.stopCapture()
```

建议遵循“先取消发布，再停止采集”的顺序，这样频道侧状态和本地硬件状态更一致。

---

### 常见问题

#### 为什么 macOS 必须先让用户选源？

因为桌面采集的本质是“用户授权共享哪一块屏幕或哪一个窗口”，SDK 无法替用户做出这个选择。

#### 为什么 iOS 不支持系统音频？

这是平台能力边界，不是 SDK 层面的简单开关。Swift SDK 在 iOS 上会明确忽略屏幕音频配置，而不是制造一个看起来支持、实际无效的接口。
