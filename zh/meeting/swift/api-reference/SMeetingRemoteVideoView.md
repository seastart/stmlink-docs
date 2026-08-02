---
title: "SMeetingRemoteVideoView"
description: "渲染远端成员画面的 SwiftUI 组件，视图出现与消失时自动完成订阅和退订"
---

`SMeetingRemoteVideoView` 是渲染远端成员画面的 SwiftUI 组件。它把「订阅 / 退订」和「视图生命周期」绑定在一起，你只要让视图出现和消失，订阅关系就跟着走。

可用性：iOS 13.0+ / macOS 10.15+。

---

### `init(meeting:uid:trackDesc:)`

```swift
SMeetingRemoteVideoView(
    meeting: meeting,
    uid: user.uid,
    trackDesc: .cameraBig
)
.frame(height: 180)
```

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | :---: | --- |
| `meeting` | `SMeeting` | 是 | SDK 实例 |
| `uid` | `String` | 是 | 要渲染的远端成员 ID |
| `trackDesc` | `TrackDesc` | 是 | 轨道描述，摄像头传 `.cameraBig`，屏幕共享传 `.screen` |

**返回值：** 一个 SwiftUI `View`

---

### 行为约定

+ 视图出现时按 `(uid, trackDesc)` 发起订阅，视图消失时退订
+ `uid` 或 `trackDesc` 变化时会自动退订旧的、订阅新的，你不需要给视图加 `id(...)` 强制重建
+ 布局切换导致视图重建（旧实例消失、新实例紧接着出现）时不会产生多余的退订 + 重订，画面不会闪断
+ 同一路画面在多个位置同时渲染时，关掉其中一处不会影响其它位置
+ 订阅完成与底层媒体到达不是同一时刻，组件会在数据真正到达后自动完成绑定，你不需要做延时或重试
+ 订阅失败不会崩溃，视图保持空白，失败原因会写进 SDK 日志

---

### 不适用的场景

以下情况请改用其它入口：

| 场景 | 使用 |
| --- | --- |
| 渲染本端摄像头 / 共享 | `SRTCVideoView(track: meeting.cameraTrack)` |
| UIKit / AppKit | `startPlayRemoteVideo(view:uid:trackDesc:)` |
| 需要把订阅时机和渲染时机分开 | `subscribeRemoteVideoTrack(uid:trackDesc:)` |

---

### 相关页面

+ [视频渲染](/zh/meeting/swift/advanced/video-rendering)
+ [媒体控制接口](/zh/meeting/swift/api-reference/media-control)
