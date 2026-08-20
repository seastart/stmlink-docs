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

### 通话质量事件

| 方法 | 触发时机 | 关键参数 |
| --- | --- | --- |
| `channel(_:didReceiveQualityReport:)` | 服务端每次下发质量报告（实时数值流） | `QualityReport` |
| `channel(_:didChangeConnectionQuality:)` | 质量等级发生跳档（断言式） | `ConnectionQualityChange` |
| `channel(_:didChangeActiveSpeakers:)` | 活跃说话人变化 | `ActiveSpeakersSnapshot` |
| `channel(_:didSwitchLayer:)` | 大小流切层完成 | `LayerSwitchedInfo` |

质量走**双轨**，按用途选一条：`didReceiveQualityReport` 是每个上报周期都触发的原始数值，适合信号塔与诊断面板；`didChangeConnectionQuality` 只在跳档时触发，适合「网络不佳」提示与主动降级。**别用前者驱动提示或降级**，等级抖动时会反复闪烁。

`didChangeActiveSpeakers` 给的是**全量快照**（已按音量降序），业务侧直接覆盖 UI，不需要自己合并增量；无人说话时为空数组。

<Note>
这四个事件仅 **SeaStart（SFU）引擎**有 —— 它们走订阅 PeerConnection 上的信令 DataChannel，WangSu（CDN）引擎没有这条通道。详见 [通话质量与活跃说话人](/zh/rtc/swift/advanced/call-quality)。
</Note>

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
| `screenBroadcastDidStart(_:)` | iOS 全屏共享：扩展已连上、画面开始传输 | `Track` |
| `screenBroadcastDidFinish(_:reason:)` | iOS 全屏共享：广播结束（含用户点系统胶囊） | `Track`、`String` |

其中 `trackDidBindRtcTrack(_:)` 对视频渲染尤其有用，因为远端轨道对象可能先出现，底层媒体轨道稍后才真正绑定完成 —— 收到这个事件才代表可以渲染。

两个 `screenBroadcast` 事件只在 iOS 全屏采集（`ScreenCaptureMode.broadcast`）下触发：
全屏共享由用户从系统 UI 发起、也可能从系统胶囊直接停止，这些动作发生在 App 之外，
只能靠事件感知。`startCapture()` 成功仅代表 SDK 已就绪，收到 `screenBroadcastDidStart`
才是真正"共享中"。详见[屏幕共享](/zh/rtc/swift/advanced/screen-sharing)。

---

### AudioRouteSessionDelegate

**iOS 专有。** 通过 `AudioRouteSession.shared.delegates.add(delegate: self)` 注册，
所有回调均在主线程执行，协议提供默认空实现，只实现关心的方法即可。

| 方法 | 触发时机 | 关键参数 |
| --- | --- | --- |
| `audioRouteSession(_:didChangeRoute:from:reason:)` | 音频输出路由变化 | `AudioRoute`、`AVAudioSession.RouteChangeReason` |
| `audioRouteSessionWasInterrupted(_:)` | 音频会话被中断（来电 / Siri / 其他 App 抢占） | `AudioRouteSession` |
| `audioRouteSessionDidRecoverFromInterruption(_:)` | 中断**真正恢复成功**后 | `AudioRouteSession` |
| `audioRouteSession(_:didChangeCallState:)` | 系统通话状态变化（CallKit） | `AudioCallState` |

`reason` 区分了变化来源（`.oldDeviceUnavailable` 拔出、`.newDeviceAvailable` 插入、
`.override` App 主动覆盖），排查路由问题时它往往比结果本身更有价值。

`audioRouteSessionDidRecoverFromInterruption(_:)` 与系统的
`AVAudioSession.interruptionNotification(.ended)` **不等价**：系统电话挂断瞬间音频硬件尚未释放，
SDK 会等通话真正结束且 App 回到前台后才重建会话，失败还会重试——只有真正恢复成功才触发此回调。
业务层在这里刷新 UI 即可，不需要自己处理这套时序。

详见[音频路由](/zh/rtc/swift/advanced/audio-routing)。
