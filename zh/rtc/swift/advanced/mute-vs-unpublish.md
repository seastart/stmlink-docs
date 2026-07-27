---
title: "静音与停止发布"
description: "Swift SDK 中 mute / unmute 与 unpublish / stopCapture 的区别和选择建议"
---

### 概述

Swift SDK 里常见的一个误区是：把“静音”和“停止发布”当成同一件事。

从第一性原理看，它们控制的是两层不同的状态：

+ `mute / unmute` 控制的是“这条轨道现在是否输出媒体数据”
+ `unpublishLocalTrack` 控制的是“这条轨道是否还属于频道里的已发布轨道”

因此两者的结果、恢复成本和对远端的影响都不同。

---

### 两种操作的区别

| 操作 | 控制层级 | 是否保留 Track 对象 | 是否需要重新 publish | 适合场景 |
| --- | --- | --- | --- | --- |
| `mute()` / `unmute()` | 轨道输出层 | 是 | 否 | 临时静音、临时关画面 |
| `unpublishLocalTrack(...)` | 频道发布层 | 通常否 | 是 | 彻底停止推流、离开舞台 |

但在 Swift SDK 里，不同轨道的 `mute()` 语义还有一层差异。

---

### 麦克风轨道：`mute()` 是轻操作

`LocalMicTrack` 的 `mute()` 不会销毁轨道对象，也不会要求你重新发布。

典型流程：

```swift
let micTrack = srtc.createLocalMicTrack(preset: .music)
try await micTrack.startCapture()
try await channel.publishLocalTrack(micTrack)

// 临时静音
micTrack.mute()

// 恢复
micTrack.unmute()
```

这种方式适合：

+ 会议里的“静音/取消静音”按钮
+ 主持人短暂闭麦
+ 需要快速切换、尽量不打断音频会话的场景

原因是当前 Swift SDK 的本地音频走内部混音模型，`LocalMicTrack` 的静音本质上是把麦克风这一路从混音输出里静掉，而不是把整条发布链路拆掉。

---

### 摄像头和屏幕共享：`mute()` 仍保留发布关系，但会停采

`LocalCameraTrack` 和 `LocalScreenTrack` 的 `mute()` / `unmute()` 是 `async` 的，这是一个重要信号：它们不是纯内存标记，而是会涉及采集生命周期。

```swift
let cameraTrack = srtc.createLocalCameraTrack(preset: .h720p)
try await cameraTrack.startCapture()
try await channel.publishLocalTrack(cameraTrack)

// 临时关闭画面
try await cameraTrack.mute()

// 恢复画面
try await cameraTrack.unmute()
```

这里的关键点是：

+ 轨道对象还在
+ 不需要重新 `publishLocalTrack(...)`
+ 但采集会停止，恢复时会重新启动采集

所以它适合：

+ 用户暂时关闭摄像头，但界面上仍保留“这一路视频轨道”
+ 屏幕共享暂时暂停，再继续共享同一路内容

---

### `unpublishLocalTrack(...)` 是发布层面的移除

如果你希望远端从频道视角上不再看到这一路轨道，应该用取消发布：

```swift
try await channel.unpublishLocalTrack(cameraTrack)
try await cameraTrack.stopCapture()
```

重新恢复时，通常建议重新创建或重新采集后再发布：

```swift
let newCameraTrack = srtc.createLocalCameraTrack(preset: .h720p)
try await newCameraTrack.startCapture()
try await channel.publishLocalTrack(newCameraTrack)
```

这适合：

+ 用户真正退出上麦 / 退出视频位
+ 停止屏幕共享并释放这一路轨道
+ 业务上需要让远端用户列表中的轨道信息被移除

---

### 选择建议

#### 麦克风按钮

+ 常规静音按钮：优先用 `mute()` / `unmute()`
+ 用户离开频道前清理：直接调用 `srtc.leaveChannel()`，SDK 内部自动停止采集和取消发布

#### 摄像头按钮

+ 临时关画面、稍后还会恢复：用 `mute()` / `unmute()`
+ 真正关闭摄像头并让远端移除该轨道：用 `unpublishLocalTrack(...)` + `stopCapture()`

#### 屏幕共享按钮

+ 短暂停止共享后继续当前会话：可以用 `mute()` / `unmute()`
+ 结束共享并清理资源：用 `unpublishLocalTrack(...)` + `stopCapture()`

---

### 一个实用判断标准

如果你的目标是“用户稍后恢复时，不希望重新走完整的发布流程”，优先考虑 `mute()`。

如果你的目标是“让频道里的这条流彻底消失”，优先考虑 `unpublishLocalTrack(...)`。
