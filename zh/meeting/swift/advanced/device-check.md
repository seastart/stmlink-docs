---
title: "设备检测（会前 / 会中预览）"
description: "在入会前或会中做摄像头、麦克风、扬声器检测：枚举设备、requestOpenCamera(publish: false) 只预览不推流、isCameraOpened 判断要不要关、麦克风音量与扬声器试听在苹果平台上的限制与做法"
---

### 概述

入会前的设备检测页、会中的设置页，都需要「打开设备看一眼，但不推给其他人」。各项检测在 Swift 会议层的做法：

| 检测项 | 做法 | 支持情况 |
| --- | --- | --- |
| 设备列表 | `getDevices(kind:)` | iOS / macOS |
| 摄像头预览 | `requestOpenCamera(publish: false)` | iOS / macOS，会前会中都可用，自 1.9.0 起 |
| 麦克风音量 | 会中开麦后看 `activeSpeakersDidChange` 里自己那一条 | **暂不支持会外 / 只采集测麦**，原因见下 |
| 扬声器试听 | macOS 用 `setAudioOutput(deviceId:)` 选设备，测试音由业务自己播放 | SDK 不提供试听接口 |

---

### 设备列表

```swift
let cameras = meeting.getDevices(kind: .videoInput)
let microphones = meeting.getDevices(kind: .audioInput)
let speakers = meeting.getDevices(kind: .audioOutput)
```

设备插拔、切换设备见 [外设管理](/zh/meeting/swift/advanced/device-management)。

---

### 摄像头预览

`requestOpenCamera` 传 `publish: false` 时只采集、只预览：不请求会控、不发布、不发摄像头状态事件，会前会中都可以调用。主持人关闭摄像头、全员禁画也不影响只预览的轨。

```swift
// 打开预览（UIKit / AppKit 传 view；SwiftUI 传 nil，再用 SRTCVideoView(track:) 渲染）
let track = try await meeting.requestOpenCamera(
    view: previewView,
    deviceId: selectedCameraId,
    publish: false
)

// 用户在检测页里换了摄像头：再调一次，传新的 deviceId
try await meeting.requestOpenCamera(view: previewView, deviceId: newCameraId, publish: false)

// 关闭预览：只预览的才关，会议摄像头开着时不动
if !meeting.isCameraOpened {
    await meeting.closeCamera()
}
```

几种组合的结果：

+ **预览后决定开摄像头**：以默认的 `publish: true` 再调一次 `requestOpenCamera()`，会请求会控并发布**同一条轨**，不重新采集，画面不闪。
+ **会议摄像头已开着时打开预览**：`publish: false` 直接返回正在用的轨，不会再开一路采集；这时 `isCameraOpened` 为 `true`，关预览时不要调 `closeCamera()`。
+ **会前用默认参数打开的摄像头**：入会后再调用一次 `requestOpenCamera()` 会补发布到会议。

---

### 麦克风音量

Swift 会议层的 `requestOpenMic` **没有** `publish: false`，暂不支持会外或只采集不发布的测麦。这是苹果平台音频链路的限制：麦克风在发布前一直处于静音，会外的录音链路也要入会后才启动，此时读不到有效的音量。

会中开麦之后，可以用活跃说话人事件里自己那一条（`isLocal == true`）显示本端音量：

```swift
func meeting(_ meeting: SMeetingEngine, activeSpeakersDidChange snapshot: ActiveSpeakersSnapshot) {
    let myLevel = snapshot.speakers.first(where: { $0.isLocal })?.level ?? 0
    micLevelView.update(myLevel)   // 0~1
}
```

会前检测页如果一定要测麦，可以用系统 `AVAudioRecorder` / `AVAudioEngine` 自己采一段读电平，测完释放后再入会。

---

### 扬声器试听

SDK 不提供播放测试音的接口，测试音由业务自己用 `AVAudioPlayer` 播放：

+ **macOS**：先 `try meeting.setAudioOutput(deviceId:)` 选中要测的输出设备，再播放测试音。
+ **iOS**：输出路由由系统决定，可用 `setSpeakerOutputEnabled(_:)` 在外放与听筒之间切换，蓝牙等外设交给系统路由选择器，见 [音频路由](/zh/meeting/swift/advanced/audio-routing)。

---

### 相关页面

+ [外设管理](/zh/meeting/swift/advanced/device-management)
+ [音视频控制接口](/zh/meeting/swift/api-reference/media-control)
