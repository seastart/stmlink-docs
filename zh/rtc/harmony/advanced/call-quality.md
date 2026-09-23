---
title: "通话质量"
description: "读取网络质量、监听质量等级变化、活跃说话人、Simulcast 层切换，以及编解码能力核对"
---

质量相关的能力分四块：**网络质量**、**活跃说话人**、**Simulcast 层切换**、
**编解码能力核对**。前三块靠事件，最后一块靠主动查询。

---

### 网络质量：两个入口，别用错

| 入口 | 类型 | 用途 |
| --- | --- | --- |
| `onConnectionQualityChange` | 事件 | **做 UI 指示器用这个** |
| `onQualityReport` | 事件 | 原始采样，适合上报到自己的监控系统 |
| `channel.getConnectionQuality()` | 主动查询 | 需要立刻拿一次当前值时用 |

```typescript
const delegate: ChannelDelegate = {
  onConnectionQualityChange: (channel, change: ConnectionQualityChange) => {
    // change.evaluation.overall / uplink / downlink
    // change.previous  上一次的等级
    this.qualityIcon = change.evaluation.overall;
  },
  onQualityReport: (channel, report: QualityReport) => {
    // report.pub 上行采样，report.sub 下行采样
    myMonitor.report(report);
  }
};
```

<Note>
**`onConnectionQualityChange` 已经做过等级判定与抖动抑制**，只在等级真的变了才回调。
直接拿 `onQualityReport` 的原始采样去驱动 UI，图标会不停闪。
</Note>

`ConnectionQuality` 有五档：`unknown` / `excellent` / `good` / `poor` / `lost`。

`QualityEvaluation` 同时给三个维度：

| 字段 | 说明 |
| --- | --- |
| `uplink` | 上行（你发出去的） |
| `downlink` | 下行（你收到的） |
| `overall` | 综合，取两者中较差的一个 |
| `mos` | MOS 值 |

需要自己合并两个等级时用 `worseQuality(a, b)`。

<Note>
UI 上区分上下行是有意义的：`uplink` 差是**你**的问题（提示"你的网络不稳定"），
`downlink` 差可能是对端或中间链路的问题。只显示 `overall` 会让用户误判。
</Note>

### 原始采样字段

`QualitySample`（`report.pub` / `report.sub` 各一份）：

| 字段 | 说明 |
| --- | --- |
| `level` | 该方向的质量等级 |
| `score` | 综合评分 |
| `mos` | MOS 值 |
| `loss` | 丢包率 |
| `rtt` | 往返时延 |
| `jitter` | 抖动 |
| `packets` / `bytes` / `bitrate` | 流量统计 |

---

### 活跃说话人

```typescript
onActiveSpeakersChange: (channel, snapshot: ActiveSpeakersSnapshot) => {
  // snapshot.speakers: ActiveSpeakerInfo[]  含 uid / trackId / level
  this.speakingUids = snapshot.speakers.map((s: ActiveSpeakerInfo) => s.uid);
}
```

`level` 是音量级别，可以用来做"说话时头像发光"的强弱效果，而不只是二值状态。

<Note>
这是**服务端**算出来的集合，不是客户端逐路分析音量 —— 所以在云端混音
（`RemoteAudioMixTrack`）模式下依然可用，那种模式下客户端根本拿不到分路音频。
</Note>

---

### Simulcast 层切换

大小流切换由服务端按带宽决定，客户端也可以主动切。

```typescript
// 监听切换结果
onLayerSwitched: (channel, info: LayerSwitchedInfo) => {
  // info.subKey / fromTrackId / toTrackId / reason / latencyMs
}

// 主动切到指定层
channel.switchLayer(pubUid, trackId, targetTrackId);

// 查当前实际命中的是哪一层
const hit: string | undefined = channel.getSubscribeHit(uid, trackId);
```

<Warning>
**判断"当前在看大流还是小流"要用 `getSubscribeHit()`，不能用自己订阅时传的 trackId。**

服务端可能因带宽自动降级，你订的是大流、实际下发的是小流。`getSubscribeHit` 返回的
才是真相。
</Warning>

订阅小流的办法是直接订那一层的 trackId —— `TrackInfo.simulcasts` 里有各层信息
（`rid` / `width` / `height` / `fps` / `maxBitrate`），`variant` 为 `true` 的是副层。

发布端配置多层用 `VideoPublishOptions.simulcasts`，副层可以直接用现成的
`cameraSmallStreamPreset()`。

---

### 影响弱网表现的两个发布参数

```typescript
import { TrackPriority, DegradationPreference, defaultVideoPublishOptions } from 'srtc';

const opts = defaultVideoPublishOptions();
opts.priority = TrackPriority.high;
opts.degradationPreference = DegradationPreference.maintainResolution;
await channel.publishLocalVideoTrack(camera, opts);
```

| 参数 | 取值 | 含义 |
| --- | --- | --- |
| `priority` | `veryLow` / `low` / `medium` / `high` | 带宽紧张时的码率分配权重 |
| `degradationPreference` | `maintainResolution` | 保分辨率，宁可掉帧（**屏幕共享、文档演示**） |
| | `maintainFramerate` | 保帧率，宁可降分辨率（**摄像头、人物**） |
| | `balanced` | 折中 |
| | `disabled` | 不降级 |

`trackPriorityBitrateWeight(priority)` 可以查某个优先级对应的权重值。

<Note>
上游 `@ohos/webrtc` 目前**没有暴露 `networkPriority` / `bitratePriority`**，
所以做不到"弱网时优先保音频、先牺牲视频"这种跨轨道的全局策略。
`TrackPriority` 只在视频轨之间起作用。
</Note>

---

### 编解码能力核对（发版与排障必做）

```typescript
import { videoCodecNames, videoCodecReport, isCodecSupported, Codec } from 'srtc';

console.info(`codecs = [${videoCodecNames().join(', ')}]`);
console.info(`H264 = ${isCodecSupported(Codec.h264)}`);
videoCodecReport().forEach((line: string) => console.info(line));
```

`videoCodecReport()` 会把**收发两个方向**的能力连同 `sdpFmtpLine` 一起列出来，例如：

```
发送: video/H264 [level-asymmetry-allowed=1;packetization-mode=1;profile-level-id=42e01f]
发送: video/H265
发送: video/VP8
接收: video/H264 [level-asymmetry-allowed=1;packetization-mode=1;profile-level-id=640c1f]
接收: video/H264 [level-asymmetry-allowed=1;packetization-mode=1;profile-level-id=42e01f]
```

<Warning>
**这是 HarmonyOS 上最容易踩的一个坑：H264 不支持时不报错，而是静默退回 VP8。**

`@ohos/webrtc` 的 H264 / H265 是**纯硬编、没有软编兜底**。设备能力表里查不到 H264 时，
SDK 内部会跳过编码偏好设置、退回默认顺序 —— 整个过程**不抛异常**。

表现是本机看得到画面，但与 Web / iOS / Android / CDN **互通不上**。

所以自测不能以"看到画面"为准，必须核对 `videoCodecReport()` 里**发送侧**有没有
`video/H264`。只有接收侧有是不够的 —— 收得下不代表发得出。

模拟器上一个 H264 都没有，编解码相关一律真机验。
</Warning>

---

### 一个最小的质量指示器

```typescript
@State quality: ConnectionQuality = ConnectionQuality.unknown;
@State uplink: ConnectionQuality = ConnectionQuality.unknown;
@State downlink: ConnectionQuality = ConnectionQuality.unknown;

private delegate: ChannelDelegate = {
  onConnectionQualityChange: (channel, change: ConnectionQualityChange) => {
    this.quality = change.evaluation.overall;
    this.uplink = change.evaluation.uplink;
    this.downlink = change.evaluation.downlink;
  }
};
```

`poor` 时提示用户，`lost` 时按断线处理（但注意 SDK 会自己重连，
真正断开要看 `onDisconnected`）。

---

### 相关阅读

+ [事件参考](/zh/rtc/harmony/events)
+ [类型定义](/zh/rtc/harmony/types) —— 质量相关的完整字段
+ [错误码](/zh/rtc/harmony/error-codes)
