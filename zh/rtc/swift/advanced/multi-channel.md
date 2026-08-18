---
title: "多频道"
description: "同时加入多个频道：轨道如何跨频道复用、采集何时回收、以及多频道发布音频的硬约束"
---

一个 `SRTCEngine` 可以同时加入多个频道。典型场景是「主会场 + 分组讨论」这类需要同时收听
两路的业务，或者把一路摄像头同时推给两个频道。

### 加入与离开

`joinChannel` 可以多次调用，每次返回一个独立的 `Channel`：

```swift
let main = try await srtc.joinChannel(token: mainToken)
let group = try await srtc.joinChannel(token: groupToken)

srtc.channels          // [main, group]，按加入先后排序
srtc.defaultChannel    // main（最早加入且仍存活的那个）
```

同一个频道名重复加入会抛 `SRTCError.alreadyJoined`——正在加入中也算，不会出现两个
`Channel` 指向同一频道。

离开建议显式指定：

```swift
await group.leave()            // 或 srtc.leaveChannel(group)
await srtc.leaveChannel()      // 无参版本作用于 defaultChannel
```

`leaveChannel()` 的无参版本只作用于默认频道，默认频道离会后会顺延到下一个。单频道使用者
感知不到这条规则，但多频道下建议不要依赖它，直接指名要离开哪个频道。

发布、订阅、成员列表、事件回调、离会都在各自的 `Channel` 上进行，互不干扰。

---

### 轨道是引擎级对象，可以发给多个频道

`createLocalXxxTrack` 创建的轨道属于引擎而不是某个频道，同一条轨道可以发布到多个频道：

```swift
let camera = srtc.createLocalCameraTrack(preset: .h720p)
try await camera.startCapture()

try await main.publishLocalTrack(camera)
try await group.publishLocalTrack(camera)   // 同一路采集，两个频道各自发送
```

这样做只采集一次、编码按频道各自进行，不会把摄像头打开两遍。

**采集回收遵循「最后一个释放者负责」**：取消发布或离开其中一个频道时，只要这条轨道还被
其它存活频道发布着，SDK 就不会停掉采集；直到最后一个持有者释放，才真正
`stopCapture()`。所以下面这段代码里，离开 `group` 之后 `main` 的画面不会中断：

```swift
await group.leave()      // camera 仍被 main 发布 → 保持采集
await main.leave()        // 最后一个持有者 → 自动停止采集
```

屏幕共享同理。iOS 全屏采集（Broadcast Extension）本身是进程级独占的，一条屏幕轨道对应
一次广播，发给多个频道也只有一路采集。

---

### 多频道发布音频的硬约束

<Warning>
多个频道同时**发布**音频时，各频道发布的音频源集合必须**完全相同**，否则
`publishLocalTrack` 会抛 `SRTCError.invalidState`。
</Warning>

原因在音频链路：整个进程只有一个音频设备模块与一份混音，所有频道的音频轨道拿到的都是**同一份
混音结果**。如果频道 A 只发了麦克风、频道 B 发了麦克风 + 屏幕音频，那么这份全局混音里含有
屏幕音频，A 的订阅者也会听到 B 正在共享的声音——按 API 语义 A 完全无从预料，这是跨频道的
音频泄漏，所以 SDK 在发布入口就拦下来。

集合相同则是可预期的行为：两个频道发的内容一致。所以最常见的用法是被允许的：

```swift
let mic = srtc.createLocalMicTrack()
try await mic.startCapture()

try await main.publishLocalTrack(mic)
try await group.publishLocalTrack(mic)     // ✅ 两个频道的音频源集合都是 {mic}
```

而下面这样会被拒绝：

```swift
try await main.publishLocalTrack(mic)                    // {mic}
try await group.publishLocalTrack(mic)                   // {mic}
try await group.publishLocalTrack(screenTrack)           // ❌ group 变成 {mic, screen_audio}
// SRTCError.invalidState：各频道发布的音频源必须完全相同
```

要么让两个频道发布相同的音频源，要么先取消另一个频道的音频发布。

**订阅侧不受任何限制**：任意频道都能正常订阅远端音频，下行由 WebRTC 自行混音，与上面的约束无关。

---

### 事件

每个 `Channel` 有自己的委托列表，注册在哪个频道上就只收到那个频道的事件：

```swift
main.delegates.add(delegate: mainHandler)
group.delegates.add(delegate: groupHandler)
```

轨道级事件（`TrackDelegate`）注册在轨道上，跨频道共享的轨道只需注册一次。

---

### 常见问题

#### 多频道会不会把摄像头 / 麦克风打开多次？

不会。采集是引擎级的，多个频道共享同一路采集，硬件只打开一次。

#### 离开一个频道后另一个频道画面黑了？

正常情况不会——采集回收由「最后一个释放者」负责。如果确实出现，检查是不是给两个频道各创建了
一条轨道（那就是两路采集，互不相干），而不是复用同一条。

#### 能不能让两个频道发送不同的音频？

当前不行，原因见上面的混音约束。需要这种能力的场景请联系我们，它依赖直连发布路径的支持。
