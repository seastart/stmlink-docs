---
title: "屏幕共享"
description: "SMeeting Swift SDK 的屏幕共享接入：默认采集、macOS 指定共享源、iOS 全屏共享（Broadcast Upload Extension）、白板共享与共享事件"
---

### 概述

会议里的共享由 `ShareType` 区分两类：

| 类型 | 说明 | 是否产生媒体流 |
| --- | --- | --- |
| `.screen` | 屏幕共享 | 是 |
| `.whiteBoard` | 电子白板 | 否，只广播共享状态 |

同一时刻一个会议只有一位成员在共享，共享者是谁可以读 `RoomInfo.shareUid`，当前共享类型读 `RoomInfo.shareState`。

屏幕共享在 iOS 上有两条采集路径，能采到的范围完全不同，接入前先确认要哪一条：

| 路径 | 接口 | 能采到什么 | 集成成本 |
| --- | --- | --- | --- |
| 应用内采集 | `requestShare()` | **只有本 App 的画面** | 无 |
| 全屏采集 | `prepareBroadcastShare(appGroup:)` + `publishBroadcastShare()` | 整个系统屏幕 | 需额外集成一个扩展 target |

macOS 只有一条路径，`requestShare()` 即整屏 / 指定窗口采集。

---

### 开始共享

#### 默认采集

```swift
try await meeting.requestShare()
```

等价于 `requestShare(shareType: .screen, preset: .h1080p)`，macOS 上采集主显示器。`preset` 取值来自 SRTC 的 `ScreenPreset`：`.h720p`、`.h1080p`（默认）。

#### macOS：让用户选择显示器或窗口

macOS 12.3 及以上支持指定采集源。业务层先枚举，展示选择 UI，再把用户选中的源传进来：

```swift
import SMeeting
import SRTC

@available(macOS 12.3, *)
func startShare(meeting: SMeetingEngine) async throws {
    let displays = try await ScreenCaptureSources.availableDisplays()
    let windows = try await ScreenCaptureSources.availableWindows()

    // 这里以第一块显示器为例，实际应由用户在你的 UI 上选择
    guard let source = displays.first else { return }

    try await meeting.requestShare(source: source)
}
```

`source` 接受 `DisplaySource`（显示器）或 `WindowSource`（应用窗口）。

> SDK 负责「发现可共享的源」和「开始采集」，「怎么把源列表展示给用户」由你决定，这样 SDK 不绑定任何 UI 方案。

#### 本地预览

如果你在 UIKit / AppKit 下需要本地预览共享画面，可以传入 `view`；SwiftUI 下不传，改用 `SRTCVideoView(track: meeting.screenTrack)`。

---

### iOS：全屏共享

`requestShare()` 在 iOS 上走的是应用内采集，**只能采到本 App 的画面**。要共享整个系统屏幕，必须走 ReplayKit 的 Broadcast Upload Extension —— 这是 iOS 的系统约束，任何 SDK 都绕不过去。

#### 一、集成扩展 target

新建一个 Broadcast Upload Extension target，**只链接 `SRTCBroadcastKit`**，principal class 继承 `SRTCBroadcastSampleHandler`：

```swift
import SRTCBroadcastKit

class SampleHandler: SRTCBroadcastSampleHandler {}
```

`SRTCBroadcastKit` 是音视频层 `srtc-swift-sdk` 的产物，而 SwiftPM 不允许使用传递依赖的产品，所以要在工程里**再加一条依赖**，版本与 SMeeting 内部锁定的 SRTC 版本保持一致（见 [集成方式](/zh/meeting/swift/integration)）：

```swift
.package(url: "https://github.com/seastart/srtc-swift-sdk.git", exact: "1.3.0"),
```

<Warning>
**只把 `SRTCBroadcastKit` 加到扩展 target 上。** 加到 App target 会让一个进程里出现两份同名类型（App 侧的 `SRTC` 里已经静态含有同一份代码）；反过来让扩展去链 `SMeeting` / `SRTC`，会把 WebRTC 拉进只有 **50MB** 内存上限的扩展进程，基本必被系统杀掉。
</Warning>

#### 二、配置 App Group

App 与扩展配同一个 App Group，并在**扩展的 `Info.plist`** 写 `SRTCAppGroupIdentifier`。三处必须完全一致：App 的 entitlement、扩展的 entitlement、扩展的 `Info.plist`。

App Group 还要在开发者后台注册，两份描述文件都得带上该 capability，否则签名阶段就会报 `Provisioning profile doesn't include the App Groups capability`。

#### 三、入会后挂监听，用户从系统 UI 发起

全屏采集只能由用户从系统 UI 发起，所以链路是「先挂监听 → 用户点系统胶囊 → 真的出帧了才对会议宣布共享」：

```swift
// 入会后：只挂监听，不通知会议后端 —— 此刻共享还没开始
try await meeting.prepareBroadcastShare(appGroup: "group.your.app")

// 共享按钮：把 SRTCBroadcastPicker 透明盖在自己画的按钮上，点一下直接进系统弹窗
myShareButton.overlay {
    SRTCBroadcastPicker(preferredExtension: "com.your.app.broadcast", title: "")
}

// 用户点了「开始直播」，扩展开始出帧 —— 这时才对会议宣布共享
func meeting(_ meeting: SMeetingEngine, shareBroadcastDidStart data: ShareBroadcastStartEventData) {
    Task { try? await meeting.publishBroadcastShare() }
}
```

举手申请共享、被主持人同意后再开始的场景，把 `publishBroadcastShare(byAdmin: true, adminUid:)` 传上对应参数即可，与 `requestShare` 的语义一致。

<Warning>
**不要在用户点按钮时就调 `requestShare`。** 用户在系统弹窗里点「取消」是没有任何回调的，那样会议里会挂着一个永远没有画面的共享标记，只能靠你自己超时撤回。

一步到位的 `requestShare(broadcastAppGroup:)` 仍然保留，但它在**监听就绪的那一刻**就宣布共享，只适合不关心中间态的简单集成。会议类场景请用 `prepareBroadcastShare` + `publishBroadcastShare`。
</Warning>

因为共享按钮本体就是系统的 `SRTCBroadcastPicker`，界面上**不需要**「等待用户开启共享」这类中间态提示页。

#### 四、状态与收尾

| 状态 | 判断方式 |
| --- | --- |
| 已挂监听、用户还没开播 | `prepareBroadcastShare` 已成功，且 `isShareBroadcastActive == false` |
| 正在出帧 | 收到 `shareBroadcastDidStart` |
| 已结束 | 收到 `shareBroadcastDidFinish(reason:)` |

用户从系统胶囊停止广播时，SDK 会**自动收尾**（停止发布 + 通知会议后端）并重新挂上监听，业务侧不需要再调 `stopShare()`、也不用重新 prepare，只需刷新 UI。用户可以直接再共享一次。

不再需要共享能力时调 `stopBroadcastListening()`；`exitRoom()` 会自动拆掉监听，不需要手动处理。

<Note>
**模拟器跑不通全屏采集，必须真机**（依赖真实签名与 App Group）。扩展进程的日志不在 Xcode 控制台里，用 Console.app 按 subsystem `com.srtc.broadcast` 过滤。

iOS 全屏共享**不采集系统音频** —— 扩展侧能拿到音频帧，但当前宿主侧的 iOS 音频链路接不通，协议里是预留位。共享内容只有画面。
</Note>

底层帧传输、背压与内存约束见 [SRTC · 屏幕共享](/zh/rtc/swift/advanced/screen-sharing)。

---

### 停止共享

```swift
await meeting.stopShare()
```

`stopShare()` 会通知会议、停止发布并停止采集，不抛错。

主持人也可以强制结束当前正在进行的共享：

```swift
try await meeting.adminStopRoomShare()
```

被强制停止的一方不需要做任何处理，SDK 会自动停流，并上报 `roomShareDidStop`（`byAdmin` 为 `true`）。

---

### 白板共享

白板不产生媒体流，`requestShare(shareType: .whiteBoard)` 只是把共享状态广播出去：

```swift
try await meeting.requestShare(shareType: .whiteBoard)
```

白板页面地址进入会议后即可读取：

```swift
let url = meeting.getWhiteBoard()
```

拿到的是一个拼好授权码的完整 URL，用 `WKWebView` 加载即可。白板的具体交互由你在自己的容器里承载，SDK 只负责同步「现在谁在共享白板」这一状态。

中途入会的人收不到 `roomShareDidStart`，需要自己补一次判断：`RoomInfo.shareState == 2` 就说明会议里已经有人在共享白板。

白板页面的 URL 参数、宿主 JS 接口、生命周期与销毁时机见 [SRTC · 电子白板](/zh/rtc/whiteboard)。

---

### 共享事件

| 事件 | 触发时机 |
| --- | --- |
| `meeting(_:roomShareDidStart:)` | 有人开始共享（含自己） |
| `meeting(_:roomShareDidStop:)` | 共享结束 |
| `meeting(_:roomShareStateDidChange:)` | 主持人开启 / 关闭了「房间禁共享」 |
| `meeting(_:shareBroadcastDidStart:)` | 仅 iOS 全屏共享：扩展真的开始出帧 |
| `meeting(_:shareBroadcastDidFinish:)` | 仅 iOS 全屏共享：出帧结束（用户停掉广播 / 扩展被系统结束） |

```swift
func meeting(_ meeting: SMeetingEngine, roomShareDidStart data: RoomShareStartEventData) {
    // data.uid 共享者，data.shareType 共享类型
}

func meeting(_ meeting: SMeetingEngine, roomShareDidStop data: RoomShareStopEventData) {
    // data.byAdmin 为 true 表示被主持人强制结束，data.opUid 为操作者
}
```

屏幕共享的 `roomShareDidStart` **以 RTC 媒体轨道为准**：远端 screen 轨道到达即上报，因此收到这个事件时可以立即渲染共享画面，不需要额外做延时重试。共享广播消息与媒体轨道是两条独立通道、到达顺序不保证，SDK 已在三条路径上做了去重与兜底，同一次共享只会上报一次。

`shareBroadcastDidStart` / `shareBroadcastDidFinish` 只在 **iOS 全屏共享**、且只在**共享方自己**这一端触发，用于区分「监听已挂上」和「真的有画面了」。其他成员只关心 `roomShareDidStart` / `roomShareDidStop` 即可，不需要分辨对端用的是哪条采集路径。

---

### 常见拒绝原因

| 情况 | 结果 |
| --- | --- |
| 主持人开启了「房间禁共享」，且你不是主持人 / 联席主持人 | 抛出 `SMeetingError.unauthorized` |
| 本端已经在共享 | 抛出 `SMeetingError.internalError` |
| 用户在系统弹窗中拒绝了屏幕录制授权 | 采集失败，SDK 会自动回滚共享状态并把错误抛给你 |

---

### 相关页面

+ [视频渲染](/zh/meeting/swift/advanced/video-rendering)
+ [媒体控制](/zh/meeting/swift/advanced/media-control)
+ [主持人管控](/zh/meeting/swift/advanced/host-controls)
