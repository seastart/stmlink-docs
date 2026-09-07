---
title: "事件参考"
description: "SRTC HarmonyOS SDK 的全部事件回调：ChannelDelegate、TrackDelegate、DeviceManagerDelegate、AudioRouteSessionDelegate、ImDelegate"
---

事件都以**可选方法的接口**形式提供，只实现关心的那几个即可：

```typescript
import { ChannelDelegate, UserInfo, TrackInfo } from 'srtc';

const delegate: ChannelDelegate = {
  onUserJoin: (channel, user: UserInfo) => { /* ... */ },
  onTrackAdded: (channel, user: UserInfo, track: TrackInfo) => { /* ... */ }
};

channel.delegates.add(delegate);
```

<Warning>
**`delegates` 是强引用，必须成对 `add` / `remove`。**

ArkTS 既没有弱引用、也没有 `deinit`。注册后不摘除会导致监听者永不回收，
而且离开页面后仍然收到回调。通常在 `aboutToAppear` / `aboutToDisappear` 里配对：

```typescript
aboutToAppear(): void {
  this.channel.delegates.add(this.delegate);
}
aboutToDisappear(): void {
  this.channel.delegates.remove(this.delegate);
}
```
</Warning>

---

### ChannelDelegate

频道级事件。第一个参数恒为 `channel`，下表省略。

#### 连接状态

| 事件 | 其余参数 | 触发时机 |
| --- | --- | --- |
| `onJoinSucceed` | `info: ChannelInfo` | 加入频道成功，信令与媒体均已就绪 |
| `onReconnecting` | — | 连接中断，SDK 正在自动重连 |
| `onReconnected` | `info: ChannelInfo` | 重连成功，频道信息可能已变化 |
| `onDisconnected` | `reason: DisconnectReason`, `error?: Error` | 连接断开且不再自动恢复 |

<Note>
`onReconnecting` / `onReconnected` 之间 SDK 会自行恢复发布与订阅，业务侧一般只需要
更新 UI 上的连接指示。收到 `onDisconnected` 才需要走「退出会议」的业务流程。
</Note>

#### 成员

| 事件 | 其余参数 | 触发时机 |
| --- | --- | --- |
| `onUserJoin` | `user: UserInfo` | 有成员加入 |
| `onUserUpdate` | `user: UserInfo` | 成员信息变化（昵称、自定义属性等） |
| `onMeUpdate` | `user: UserInfo` | **自己**的信息变化 |
| `onUserLeave` | `uid: string`, `reason: DisconnectReason` | 成员离开 |

#### 媒体轨道

| 事件 | 其余参数 | 触发时机 |
| --- | --- | --- |
| `onTrackAdded` | `user: UserInfo`, `track: TrackInfo` | 远端有新流可订阅 |
| `onTrackUpdated` | `user: UserInfo`, `track: TrackInfo` | 远端流信息变化（分辨率、静音态等） |
| `onTrackRemoved` | `user: UserInfo`, `track: TrackInfo` | 远端流已移除 |

<Note>
`onTrackAdded` 只表示「可以订阅了」，**不会自动订阅**（除非入会时开了
`autoSubscribeAudio` / `autoSubscribeVideo`）。要看到画面还需要显式调用
`channel.subscribeRemoteVideoTrack(uid, trackId)`。
</Note>

#### 频道与消息

| 事件 | 其余参数 | 触发时机 |
| --- | --- | --- |
| `onChannelInfoUpdate` | `info: ChannelInfo` | 频道属性变化 |
| `onCustomMessage` | `msg: CustomMessage` | 收到频道内自定义消息 |

#### 质量与 Simulcast

| 事件 | 其余参数 | 触发时机 |
| --- | --- | --- |
| `onQualityReport` | `report: QualityReport` | 周期性上报的原始质量采样 |
| `onConnectionQualityChange` | `change: ConnectionQualityChange` | 连接质量**等级**发生变化 |
| `onActiveSpeakersChange` | `snapshot: ActiveSpeakersSnapshot` | 活跃说话人集合变化 |
| `onLayerSwitched` | `info: LayerSwitchedInfo` | Simulcast 大小流发生切换 |

<Note>
做 UI 指示器请用 `onConnectionQualityChange`（已经做过等级判定与抖动抑制），
`onQualityReport` 是原始采样，适合上报到自己的监控系统。
细节见[通话质量](/zh/rtc/harmony/advanced/call-quality)。
</Note>

---

### TrackDelegate

轨道级事件。第一个参数恒为 `track`。

| 事件 | 其余参数 | 触发时机 |
| --- | --- | --- |
| `onTrackInfoUpdate` | `info: TrackInfo` | 轨道信息变化 |
| `onTrackMute` | — | 轨道被静音 |
| `onTrackUnmute` | — | 轨道取消静音 |
| `onTrackEnd` | — | 采集结束 / 轨道失效 |
| `onTrackBindRtcTrack` | — | 底层 WebRTC 轨道绑定完成 |
| `onTrackMirrorUpdate` | — | 镜像状态变化 |

<Note>
`onTrackBindRtcTrack` 是渲染的关键时机：远端轨道是信令先建对象、订阅协商完成后才绑定
底层轨道，所以**拿到 `Track` 对象不等于已经有帧**。`SRTCVideoView` 内部已经监听了它并
自动补挂，自己接渲染层时需要处理这一点。
</Note>

---

### DeviceManagerDelegate

设备热插拔。注册在 `DeviceManager.shared.delegates` 上。

| 事件 | 参数 | 触发时机 |
| --- | --- | --- |
| `onDeviceAdd` | `device: DeviceInfo` | 设备接入 |
| `onDeviceRemove` | `device: DeviceInfo` | 设备移除 |

---

### AudioRouteSessionDelegate

音频路由与通话状态。注册在 `AudioRouteSession.shared.delegates` 上。

| 事件 | 参数 | 触发时机 |
| --- | --- | --- |
| `onAudioRouteChange` | `route: AudioRoute`, `previousRoute: AudioRoute` | 输出路由变化（含蓝牙 / 有线耳机插拔） |
| `onCallStateChange` | `state: AudioCallState`, `previous: AudioCallState` | 系统通话状态变化 |

<Note>
外接设备由系统接管，SDK **只上报不主动切换** —— 收到 `onAudioRouteChange` 时更新 UI 即可，
不要试图在回调里再切回去，那会和系统抢。见[音频路由](/zh/rtc/harmony/advanced/audio-routing)。
</Note>

---

### ImDelegate

频道 IM。`srtc.enableIm(tokenString)` 之后注册在返回的 `Im` 对象上。

| 事件 | 其余参数 | 触发时机 |
| --- | --- | --- |
| `onImEnabled` | — | IM 通道就绪 |
| `onImReconnecting` | — | IM 连接中断，正在重连 |
| `onImReconnected` | — | IM 重连成功 |
| `onImDisconnected` | `reason: ImDisconnectReason`, `error?: Error` | IM 断开且不再自动恢复 |
| `onImMessage` | `msg: ImMessage` | 收到 IM 消息 |

第一个参数恒为 `im`。

---

### 相关阅读

+ [核心概念](/zh/rtc/harmony/key-concepts) —— 事件模型在整体架构里的位置
+ [类型定义](/zh/rtc/harmony/types) —— 上面各回调参数的字段说明
+ [SRTCEngine 接口](/zh/rtc/harmony/api-reference/SRTCEngine)
