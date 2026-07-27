---
title: "事件参考"
description: "SRTC Swift SDK 中 ChannelDelegate 与 TrackDelegate 的事件列表"
---

### ChannelDelegate

通过 `channel.delegates.add(delegate: self)` 注册。

```swift
final class RoomController: ChannelDelegate {
    func channel(_ channel: Channel, didJoinSucceed info: ChannelInfo) {
        print("joined:", info.channel)
    }
}
```

---

### 连接事件

| 方法 | 触发时机 | 关键参数 |
| --- | --- | --- |
| `channel(_:didJoinSucceed:)` | 首次加入频道成功 | `ChannelInfo` |
| `channelIsReconnecting(_:)` | 网络断开后开始重连 | `Channel` |
| `channel(_:didReconnect:)` | 重连成功 | `ChannelInfo` |
| `channel(_:didDisconnect:error:)` | 连接彻底断开或离开频道 | `DisconnectReason`、`Error?` |

---

### 用户事件

| 方法 | 触发时机 | 关键参数 |
| --- | --- | --- |
| `channel(_:userDidJoin:)` | 远端用户加入 | `UserInfo` |
| `channel(_:userDidUpdate:)` | 远端用户资料更新 | `UserInfo` |
| `channel(_:meDidUpdate:)` | 自己的信息更新 | `UserInfo` |
| `channel(_:userDidLeave:reason:)` | 远端用户离开 | `uid`、`DisconnectReason` |

---

### 轨道事件

| 方法 | 触发时机 | 关键参数 |
| --- | --- | --- |
| `channel(_:user:didAddTrack:)` | 远端用户新增轨道 | `UserInfo`、`TrackInfo` |
| `channel(_:user:didUpdateTrack:)` | 远端轨道信息更新 | `UserInfo`、`TrackInfo` |
| `channel(_:user:didRemoveTrack:)` | 远端轨道移除 | `UserInfo`、`TrackInfo` |

最常见的业务入口是 `didAddTrack`，因为你通常会在这里决定是否订阅远端视频或远端音频。

---

### 消息与频道事件

| 方法 | 触发时机 | 关键参数 |
| --- | --- | --- |
| `channel(_:didReceiveCustomMessage:)` | 收到自定义消息 | `CustomMessage` |
| `channel(_:didUpdateInfo:)` | 频道信息更新 | `ChannelInfo` |

---

### TrackDelegate

通过 `track.delegates.add(delegate: self)` 注册。

---

### 轨道级事件

| 方法 | 触发时机 | 关键参数 |
| --- | --- | --- |
| `track(_:didUpdateInfo:)` | 轨道信息更新 | `TrackInfo` |
| `trackDidMute(_:)` | 轨道静音 | `Track` |
| `trackDidUnmute(_:)` | 轨道取消静音 | `Track` |
| `trackDidEnd(_:)` | 轨道结束 | `Track` |
| `trackDidBindRtcTrack(_:)` | 底层 WebRTC 轨道已绑定 | `Track` |

其中 `trackDidBindRtcTrack(_:)` 对视频渲染尤其有用，因为远端轨道对象可能先出现，底层 `rtcTrack` 稍后才真正绑定完成。
