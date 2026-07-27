---
title: "核心概念"
description: "理解 SRTC Swift SDK 中 SRTC、Channel、Track、渲染器与设备管理的关系"
---

### 整体模型

Swift SDK 的对象模型可以概括为：

+ `SRTC`：SDK 主入口，负责入会和创建本地轨道
+ `Channel`：一次真实的频道连接，负责发布、订阅、用户列表和事件分发
+ `Track`：音频或视频流的抽象对象
+ `ChannelDelegate` / `TrackDelegate`：事件回调入口
+ `SRTCVideoView` / `VideoView` / `SRTCVideoRenderer`：视频渲染层

从第一性原理看，RTC 系统本质上是在同步三类状态：

+ 连接状态
+ 用户状态
+ 媒体轨道状态

Swift SDK 也是围绕这三类状态来设计 API，所以理解这套模型之后，绝大多数接口都会变得自然。

---

### SRTC 与 Channel

#### `SRTC`

`SRTC` 更像一个“工厂 + 会话入口”，你通常用它来做两件事：

+ `joinChannel(token:options:)`
+ `createLocalMicTrack(...)` / `createLocalCameraTrack(...)` / `createLocalScreenTrack(...)`

#### `Channel`

加入频道成功后，真正承载业务状态的是 `Channel`：

+ 发布本地轨道
+ 订阅远端轨道
+ 获取频道信息与用户信息
+ 监听用户进出、轨道变化、断线重连、自定义消息

可以把它理解为“已经完成鉴权和网络连接的一次 RTC 会话”。

---

### Track 体系

#### 本地轨道

| 类型 | 创建方式 | 说明 |
| --- | --- | --- |
| `LocalMicTrack` | `srtc.createLocalMicTrack(...)` | 麦克风采集 |
| `LocalCameraTrack` | `srtc.createLocalCameraTrack(...)` | 摄像头采集 |
| `LocalScreenTrack` | `srtc.createLocalScreenTrack(...)` | 屏幕共享 |
| `LocalAudioTrack` | `srtc.createLocalCustomAudioTrack(...)` | 自定义音频注入 |
| `LocalVideoTrack` | `srtc.createLocalCustomVideoTrack(...)` | 自定义视频帧注入 |

#### 远端轨道

| 类型 | 获取方式 | 说明 |
| --- | --- | --- |
| `RemoteAudioTrack` | `channel.getRemoteTrack(...)` | 远端单路音频 |
| `RemoteAudioMixTrack` | 远端音频轨道的一种 | 全频道混音流 |
| `RemoteVideoTrack` | `channel.getRemoteTrack(...)` | 远端视频 |

---

### 音频的 Mix 模式

Swift SDK 当前的一个关键实现点是：**本地音频默认采用混音模式发送**。

这意味着：

+ 麦克风、自定义音频、屏幕音频会先进入内部 `AudioMixer`
+ PeerConnection 中真正发送的是一条内部 `audio_mix` 音频轨道
+ 业务层仍然可以分别控制每个音频源的创建、静音、停止采集

这样设计的原因是：

+ 减少多路音频并发发布时的复杂度
+ 让自定义音频、麦克风、屏幕音频采用统一发送模型
+ 与已有的 rtc-js 架构保持一致

---

### 视频采集与发布

视频轨道的生命周期通常分成三步：

```swift
let track = srtc.createLocalCameraTrack(preset: .h720p)
try await track.startCapture()
try await channel.publishLocalTrack(track)
```

三步拆开的收益是：

+ 你可以先本地预览，再决定是否发布
+ 可以单独控制硬件采集与网络发送
+ 出现权限失败、设备切换失败时，状态更容易定位

---

### 视频渲染方式

SDK 提供三种常见渲染入口：

#### `SRTCVideoView`

SwiftUI 组件，最适合直接在页面里渲染：

```swift
SRTCVideoView(track: track)
    .frame(width: 320, height: 180)
```

#### `VideoView`

适合 UIKit / AppKit，使用 `bind(track:)` 管理绑定关系。

#### `SRTCVideoRenderer`

更底层的渲染视图，由轨道自己调用 `addRenderer(...)` / `removeRenderer(...)` 绑定。

---

### 设备管理

`DeviceManager.shared` 用于处理设备枚举和设备变化监听：

+ 枚举摄像头：`cameras()`
+ macOS 枚举麦克风 / 扬声器：`microphones()`、`speakers()`
+ iOS 枚举音频路由：`audioRoutes()`
+ 监听设备热插拔与音频会话中断：`DeviceManagerDelegate`

如果你的应用需要设备选择器，建议直接围绕 `DeviceManager` 建一层 UI，而不是自己重新写一套平台差异处理。

---

### 事件模型

频道级事件走 `ChannelDelegate`：

+ 加入成功
+ 重连 / 断开
+ 用户加入、离开、更新
+ 远端轨道新增、更新、移除
+ 自定义消息

轨道级事件走 `TrackDelegate`：

+ 轨道信息变化
+ 静音 / 取消静音
+ 采集结束
+ 底层 WebRTC 轨道绑定完成

详细事件清单见 [事件参考](/zh/rtc/swift/events)。

---

### 建议继续阅读

+ [静音与停止发布](/zh/rtc/swift/advanced/mute-vs-unpublish)
+ [设备管理](/zh/rtc/swift/advanced/device-management)
+ [屏幕共享](/zh/rtc/swift/advanced/screen-sharing)
+ [自定义推流](/zh/rtc/swift/advanced/custom-track)
