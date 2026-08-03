---
title: "屏幕共享"
description: "SMeeting Swift SDK 的屏幕共享接入：默认采集、macOS 指定共享源、白板共享与共享事件"
---

### 概述

会议里的共享由 `ShareType` 区分两类：

| 类型 | 说明 | 是否产生媒体流 |
| --- | --- | --- |
| `.screen` | 屏幕共享 | 是 |
| `.whiteBoard` | 电子白板 | 否，只广播共享状态 |

同一时刻一个会议只有一位成员在共享，共享者是谁可以读 `RoomInfo.shareUid`，当前共享类型读 `RoomInfo.shareState`。

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
func startShare(meeting: SMeeting) async throws {
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

白板的具体交互由你在自己的容器里承载，SDK 只负责同步「现在谁在共享白板」这一状态。

---

### 共享事件

| 事件 | 触发时机 |
| --- | --- |
| `meeting(_:roomShareDidStart:)` | 有人开始共享（含自己） |
| `meeting(_:roomShareDidStop:)` | 共享结束 |
| `meeting(_:roomShareStateDidChange:)` | 主持人开启 / 关闭了「房间禁共享」 |

```swift
func meeting(_ meeting: SMeeting, roomShareDidStart data: RoomShareStartEventData) {
    // data.uid 共享者，data.shareType 共享类型
}

func meeting(_ meeting: SMeeting, roomShareDidStop data: RoomShareStopEventData) {
    // data.byAdmin 为 true 表示被主持人强制结束，data.opUid 为操作者
}
```

屏幕共享的 `roomShareDidStart` 会在「共享广播」和「远端画面就绪」两个条件都满足后才上报，因此收到这个事件时可以立即渲染共享画面，不需要额外做延时重试。

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
