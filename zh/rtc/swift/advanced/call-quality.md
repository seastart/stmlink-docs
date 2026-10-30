---
title: "通话质量与活跃说话人"
description: "读取网络质量数值与等级、做「网络不佳」提示与主动降级、渲染说话人高亮，以及大小流主动切层"
---

### 概述

SFU 会周期性下发一组控制面消息，SDK 把它们转成四个 `ChannelDelegate` 事件：

| 事件 | 内容 | 典型用途 |
| --- | --- | --- |
| `didReceiveQualityReport` | 上下行的原始数值（丢包、RTT、抖动、码率、MOS） | 信号塔图标、诊断面板 |
| `didChangeConnectionQuality` | 质量**等级跳档** | 「当前网络不佳」提示、主动降级 |
| `didChangeActiveSpeakers` | 活跃说话人全量快照 | 说话人高亮、语音激励布局 |
| `didSwitchLayer` | 大小流切层结果 | 排查画质突变 |

<Note>
质量与切层三个事件**仅 SeaStart（SFU）引擎有**。它们走的是订阅 PeerConnection 上的信令 DataChannel，而网宿（CDN）引擎没有这条通道，因此走 CDN 时收不到，`getConnectionQuality()` 也返回 `nil`。`didChangeActiveSpeakers` 例外：网宿频道里由 SDK 本地计算远端说话人（只覆盖已订阅的音频），两种引擎都会触发。用 `Channel.streamVendor` 判断当前引擎，见 [类型定义](/zh/rtc/swift/types#streamvendor)。
</Note>

所有回调都有默认空实现，只实现关心的即可。注册方式与其他频道事件一致：

```swift
channel.delegates.add(delegate: self)
```

---

### 网络质量：两条轨，别混用

质量走**双轨**设计，因为两类需求的触发频率差了一个量级：

+ `didReceiveQualityReport` —— **每次服务端上报都触发**，是原始数值流
+ `didChangeConnectionQuality` —— **只在等级跳档时触发**，是断言

```swift
extension CallController: ChannelDelegate {

    // 数值流：驱动信号塔、诊断面板
    func channel(_ channel: Channel, didReceiveQualityReport report: QualityReport) {
        signalBars.update(
            level: report.sub.level,          // 下行等级，用户"看/听得好不好"
            rtt: report.sub.rtt,
            loss: report.sub.loss
        )
    }

    // 跳档：驱动提示与降级
    func channel(_ channel: Channel, didChangeConnectionQuality change: ConnectionQualityChange) {
        switch change.evaluation.overall {
        case .poor, .lost:
            showToast("当前网络不佳")
            // 主动降级：切到小流（见下方「大小流」），或退订不在视野内的远端视频
            try? channel.switchLayer(pubUid: uid, trackId: trackId, targetTrackId: lowLayerId)
        case .excellent, .good:
            hideToast()
        case .unknown:
            break
        }
    }
}
```

<Warning>
**不要用 `didReceiveQualityReport` 去驱动 Toast 或降级决策。** 它每个上报周期都触发，等级在两档之间抖动时会造成提示反复闪烁、降级来回抽风。「网络变差了」这个语义请用 `didChangeConnectionQuality`，SDK 已经在里面做了跳档判断。
</Warning>

`QualityReport` 分 `pub`（上行，客户端到 SFU）与 `sub`（下行，SFU 到客户端）两个 `QualitySample`，字段含义见 [类型定义](/zh/rtc/swift/types#qualitysample)。要点：

+ `level` 是服务端给出的等级，`score`（0~100）与 `mos`（1.0~4.5）都是越大越好
+ `loss` 是 0~1 的比例，不是百分数
+ `rtt`、`jitter` 单位是毫秒，`bitrate` 单位是 kbps
+ 排查「谁的问题」时看两侧：`pub` 差是自己上行有问题，`sub` 差是下行或对端上行的问题

`ConnectionQualityChange` 里的 `evaluation.overall` 取上下行**较差**的那一档（`unknown` < `excellent` < `good` < `poor` < `lost`），`evaluation.mos` 取上下行较小值 —— 都是按「用户感知最弱的一侧」来的。`previous` 是跳档前的等级，首次跳档时为 `.unknown`。

#### 冷启动：进页面就要显示等级

事件只在变化时来，UI 刚创建时手上没有值。用 `getConnectionQuality()` 取一次当前快照补上：

```swift
if let evaluation = channel.getConnectionQuality() {
    signalBars.update(level: evaluation.overall)
}
```

未收到过任何报告时返回 `nil`（与「收到了但等级是 `unknown`」是两件事）。

<Note>
断线重连后 SDK 会清空质量缓存（最近评估、跳档基线、说话人快照），避免恢复后 UI 上残留旧的 `poor` 等级。所以重连后 `getConnectionQuality()` 会短暂返回 `nil`，直到新报告到达 —— 这是有意的，UI 上按「暂无数据」处理即可。
</Note>

---

### 活跃说话人

```swift
func channel(_ channel: Channel, didChangeActiveSpeakers snapshot: ActiveSpeakersSnapshot) {
    // 全量快照，已按音量降序 —— 直接覆盖，不要自己累加
    highlightedUids = Set(snapshot.speakers.map(\.uid))
    loudestUid = snapshot.speakers.first?.uid
}
```

`snapshot.speakers` 是**全量列表**，SDK 已经把服务端的增量协议（谁开始说、谁停止说）合并成完整快照并按 `level` 降序排好。所以：

+ 业务侧直接整体覆盖 UI 状态即可，**不需要**自己维护「谁还在说话」的集合
+ 无人说话时 `speakers` 是空数组，不是不发事件
+ `level` 是 0~1 的归一化线性音量，可以直接用来画音量条

每个 `ActiveSpeakerInfo` 带 `uid` 与 `trackId` —— 同一个用户可能有多条音频轨道，要精确定位到轨道时用后者。

#### 自己的音量（1.6.0 起）

快照里**也有自己**：`isLocal == true` 的那一条，`trackId` 是本端发布的音频轨。它只在已发布音频、没有静音且确实在说话时出现 —— 与对端听到的一致。服务端不会把你的音量回传给你，这一条由 SDK 在本地按服务端判定说话人的**同一算法**计算，所以与远端同一量纲（都按 1/8 分档），一个阈值即可：

```swift
let speakingLevel = 0.125   // 远端和自己共用

func channel(_ channel: Channel, didChangeActiveSpeakers snapshot: ActiveSpeakersSnapshot) {
    selfLevel = snapshot.speakers.first(where: \.isLocal)?.level ?? 0
    selfSpeaking = selfLevel >= speakingLevel
    remoteLevels = Dictionary(snapshot.speakers.filter { !$0.isLocal }.map { ($0.uid, $0.level) },
                              uniquingKeysWith: max)
}
```

本端这一条的参数用 `srtc.activeSpeakerOptions` 调：

| 参数 | 默认 | 说明 |
| --- | --- | --- |
| `includeLocal` | `true` | 是否把自己并进快照；`false` 即只含远端 |
| `interval` | `0.5` | 本端采样间隔（秒），加入频道时读取 |
| `silenceThreshold` | `0.01` | 本端静默门限（约 -40dBFS），低于它不进快照 |

<Note>
1.5.5 及以前「我」的音量要自己实现 `AudioProcessor`、挂到 `audioCaptureProcessor` 上从采集数据算。升级后删掉那套即可；不删也不冲突（SDK 的计量与你的处理器串在同一条链上，互不顶替），但自己算的那份与远端不是一个量纲。
</Note>

---

### 大小流：主动切层

发布端开了联播（simulcast）时，同一路视频会有多个层。默认由 SFU 按带宽自动选层，切完通过 `didSwitchLayer` 通知（`reason` 是 `bwe_down` / `bwe_up` 这类服务端原因）：

```swift
func channel(_ channel: Channel, didSwitchLayer info: LayerSwitchedInfo) {
    // info.reason 服务端原因，info.latencyMs 切层耗时
    logger.debug("切层 \(info.fromTrackId ?? "-") → \(info.toTrackId)，原因 \(info.reason)")
}
```

业务 UI 自己知道「这一路现在只显示成小窗」时，可以主动要低层，省带宽和解码开销：

```swift
try channel.switchLayer(
    pubUid: uid,
    trackId: trackId,            // 订阅时使用的稳定句柄
    targetTrackId: lowLayerId    // 想切到的目标层
)
```

主动切层完成后同样触发 `didSwitchLayer`，此时 `reason` 为 `client`。

<Warning>
`targetTrackId` 必须在订阅时声明的候选层范围内，**SDK 不做二次校验**（避免维护一份重复状态）。传了范围外的值不会立即报错，只是服务端不会切过去。当前服务端实际命中的是哪一层，用 `channel.getSubscribeHit(uid:trackId:)` 查。
</Warning>

**可能抛出：**

+ `SRTCError.engineNotSupported(_:)` —— 当前不是 SeaStart 引擎（如走 CDN）
+ `SRTCError.transportNotReady` —— 信令通道尚未就绪（刚入会、或正在重连）
+ `SRTCError.webrtcError(_:)` —— 信令通道发送失败（通常是缓冲区拥塞）

典型用法是「大小窗切换、分页、进后台降级」这三类场景：布局变化时主动切一次，剩下的交给 SFU 的自动策略。

---

### 相关页面

+ [事件参考](/zh/rtc/swift/events)
+ [类型定义](/zh/rtc/swift/types)
+ [静音与停止发布](/zh/rtc/swift/advanced/mute-vs-unpublish)
+ [多频道](/zh/rtc/swift/advanced/multi-channel)
