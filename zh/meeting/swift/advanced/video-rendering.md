---
title: "视频渲染"
description: "在 SwiftUI 与 UIKit / AppKit 中渲染 SMeeting 的本端画面、远端画面与合屏画面"
---

### 概述

会议画面分三类，入口各不相同：

| 画面 | SwiftUI | UIKit / AppKit |
| --- | --- | --- |
| 本端摄像头 / 共享 | `SRTCVideoView(track:)` | 打开时传入 `SRTCVideoRenderer` |
| 远端摄像头 / 共享 | `SMeetingRemoteVideoView` | `startPlayRemoteVideo(view:uid:trackDesc:)` |
| 服务端合屏（MCU） | 取 `meeting.mcuTrack` 后交给 `SRTCVideoView` | `startPlayRemoteVideoMcu(view:uid:)` |

本端画面**不需要订阅**，直接拿轨道渲染即可；远端画面**必须先订阅**才有数据。

---

### 本端画面

#### SwiftUI

打开摄像头时不要传 `view`，之后直接把轨道交给 `SRTCVideoView`：

```swift
try await meeting.requestOpenCamera()

if let cameraTrack = meeting.cameraTrack {
    SRTCVideoView(track: cameraTrack)
        .frame(height: 180)
}
```

屏幕共享同理，取 `meeting.screenTrack`：

```swift
if let screenTrack = meeting.screenTrack {
    SRTCVideoView(track: screenTrack)
}
```

> `SMeetingEngine` 不是 `ObservableObject`，`cameraTrack` / `screenTrack` 从 `nil` 变成有值不会自己触发 SwiftUI 刷新。请在自己的 `@Published` 状态里记一个「摄像头已开」标记，由它驱动视图更新。

#### UIKit / AppKit

在打开摄像头时把预览视图传进去：

```swift
let renderer = SRTCVideoRenderer(frame: previewFrame)
containerView.addSubview(renderer)

try await meeting.requestOpenCamera(view: renderer)
```

> 传进来的 `view` 必须是真实挂在视图层级上的对象。传一个临时创建、没有加入任何父视图的局部变量，会导致渲染链路空转。

---

### 远端画面（SwiftUI）

`SMeetingRemoteVideoView` 是 SwiftUI 场景的推荐入口，它负责整个订阅生命周期：视图出现时按 `uid + trackDesc` 订阅，视图消失时退订。

```swift
SMeetingRemoteVideoView(
    meeting: meeting,
    uid: user.uid,
    trackDesc: .cameraBig
)
.frame(height: 180)
```

看某人的屏幕共享，把 `trackDesc` 换成 `.screen`：

```swift
SMeetingRemoteVideoView(meeting: meeting, uid: user.uid, trackDesc: .screen)
```

组件对你的保证：

+ 同一个 `(uid, trackDesc)` 在多处渲染时不会互相踢掉订阅
+ 布局切换导致视图重建（旧实例消失、新实例出现）时不会产生一次多余的退订 + 重订，画面不会闪断
+ 订阅返回与底层媒体到达不是同一时刻，组件会在数据真正到达后自动完成绑定，你不需要做延时或重试

典型用法是按成员列表渲染宫格：

```swift
ForEach(users, id: \.uid) { user in
    if user.uid == meeting.currentUserId {
        if let track = meeting.cameraTrack {
            SRTCVideoView(track: track)
        }
    } else if user.shareState == ShareType.screen.rawValue {
        SMeetingRemoteVideoView(meeting: meeting, uid: user.uid, trackDesc: .screen)
    } else if user.cameraState == .on {
        SMeetingRemoteVideoView(meeting: meeting, uid: user.uid, trackDesc: .cameraBig)
    }
}
```

---

### 远端画面（UIKit / AppKit）

如果你已经持有一个挂在视图层级上的 `SRTCVideoRenderer`，用这一对便利方法：

```swift
let renderer = SRTCVideoRenderer(frame: frame)
containerView.addSubview(renderer)

try await meeting.startPlayRemoteVideo(
    view: renderer,
    uid: remoteUid,
    trackDesc: .cameraBig
)

// 不再需要时
try await meeting.stopPlayRemoteVideo(
    view: renderer,
    uid: remoteUid,
    trackDesc: .cameraBig
)
```

`stopPlayRemoteVideo` 只会移除你传入的这一个渲染视图；只有当这路轨道上已经没有任何渲染视图时，才会真正取消订阅。所以同一路画面在多个窗口里显示时，关掉其中一个不会影响其它窗口。

---

### 自行控制订阅

需要把订阅时机和渲染时机分开时（例如先预订阅再决定布局），用核心接口：

```swift
let track = try await meeting.subscribeRemoteVideoTrack(uid: remoteUid, trackDesc: .cameraBig)

// SwiftUI：SRTCVideoView(track: track)
// UIKit / AppKit：track.addRenderer(renderer)

try await meeting.unsubscribeRemoteVideoTrack(uid: remoteUid, trackDesc: .cameraBig)
```

注意 `unsubscribeRemoteVideoTrack` 是**无条件退订**，不看还有没有渲染视图在用。多处渲染同一路画面时，请用 `SMeetingRemoteVideoView` 或 `stopPlayRemoteVideo`。

只想查一下某人某路轨道存不存在（不订阅），用：

```swift
let track = meeting.getRemoteVideoTrack(uid: remoteUid, desc: .cameraBig)
```

---

### 什么时候该订阅

远端视频是**按需订阅**的，SDK 不会替你自动订阅所有人。判断依据来自成员状态和事件：

+ `MeetingUserInfo.cameraState == .on` → 这个人有摄像头画面
+ `MeetingUserInfo.shareState == ShareType.screen.rawValue` → 这个人在共享屏幕
+ 收到 `userCameraStateDidChange`、`roomShareDidStart` / `roomShareDidStop` 时刷新布局

使用 `SMeetingRemoteVideoView` 时，你只要让视图跟着这些状态出现 / 消失，订阅就自动跟着走了。

---

### 服务端合屏画面（MCU）

会议开启了服务端合屏任务时，可以只拉一路合成画面而不是逐个订阅：

```swift
let track = try await meeting.startPlayRemoteVideoMcu(view: renderer, uid: mcuUid)
// 也可以随时通过 meeting.mcuTrack 取到这一路轨道

try await meeting.stopPlayRemoteVideoMcu(view: renderer)
```

合屏画面需要服务端先配置好合屏任务，布局由 `adminUpdateLayout(_:)` 控制，见 [录制与合屏布局](/zh/meeting/swift/advanced/recording)。

---

### 相关页面

+ [媒体控制](/zh/meeting/swift/advanced/media-control)
+ [屏幕共享](/zh/meeting/swift/advanced/screen-sharing)
+ [接口文档 - SMeetingRemoteVideoView](/zh/meeting/swift/api-reference/SMeetingRemoteVideoView)
