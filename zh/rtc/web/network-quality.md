---
title: "网络质量"
description: "Web SRTC 音视频 SDK 流媒体网络质量监测接口说明"
---

SDK 提供三种获取网络质量的方式，按粒度从粗到细：

| 接口 | 返回 | 使用场景 |
|---|---|---|
| `srtc.getConnectionQuality()` | `QualityEvaluation` | 只想知道"网络好不好"，拿等级/MOS |
| `srtc.getNetworkStats()` | `NetworkStats` | 只关心网络总体：码率、丢包、RTT、可用带宽 |
| `srtc.getStreamMetric()` | `StreamMetric` | 需要每条轨道的详细统计 |

同时 SDK 会在连接质量变化、CPU/带宽受限时主动触发事件，业务层可以被动订阅而不用轮询。

## 一、主动订阅事件（推荐）

连接质量相关事件复用现有的 `ChannelEvent` 体系，直接在 `onNotifyChannelEvent` 里处理：

```typescript
import { ChannelEventType } from '@seastart/srtc-web-sdk';
import type { ConnectionQualityEventData } from '@seastart/srtc-web-sdk';

srtc.onNotifyChannelEvent = (evt) => {
  switch (evt.type) {
    case ChannelEventType.CONNECTION_QUALITY_CHANGED: {
      // 网络等级变化时触发（excellent/good/poor/lost/unknown）
      const { evaluation, previous } = evt.data as ConnectionQualityEventData;
      console.log(`网络质量: ${previous} -> ${evaluation.overall}`);
      console.log(`原因:`, evaluation.reasons);
      console.log(`MOS:`, evaluation.mos);
      break;
    }
    case ChannelEventType.CPU_CONSTRAINED:
      // 发送端被 CPU 持续限制，建议降低画质/分辨率
      toast('CPU 过载，建议降低画质');
      break;
    case ChannelEventType.BANDWIDTH_CONSTRAINED:
      // 发送端被带宽持续限制
      toast('上行带宽不足');
      break;
  }
};
```

## 二、主动查询

### 2.1 连接质量评估 `getConnectionQuality`

```typescript
const q = srtc.getConnectionQuality();
// => QualityEvaluation
```

```typescript
/** 连接质量等级（对齐业界 5 档） */
export enum ConnectionQuality {
  /** 初始占位，采样不足时使用，避免误报 */
  Unknown = 'unknown',
  /** 优秀 */
  Excellent = 'excellent',
  /** 良好 */
  Good = 'good',
  /** 较差 */
  Poor = 'poor',
  /** 连接已丢失，媒体无法传输，应触发重连 */
  Lost = 'lost',
}

export interface QualityEvaluation {
  /** 上行质量 */
  uplink: ConnectionQuality;
  /** 下行质量 */
  downlink: ConnectionQuality;
  /** 总体质量，取上下行中较差的一档 */
  overall: ConnectionQuality;
  /** 音视频 MOS 估算，1.0 ~ 4.5 */
  mos: number;
  /** 触发当前等级的主要原因，便于排查 */
  reasons: string[];
  /** 采样时间戳 */
  timestamp: number;
}
```

SDK 以 2 秒为周期滑动窗口评估，结合丢包率、RTT、jitter、视频卡顿、上行带宽压力、`qualityLimitationReason` 等多维指标综合打分。

### 2.2 网络总体统计 `getNetworkStats`

```typescript
const net = srtc.getNetworkStats();
// => NetworkStats
```

```typescript
/** 网络总体统计 */
export interface NetworkStats {
  /** 下行码率 kb/s */
  bitrate_down: number;
  /** 上行码率 kb/s */
  bitrate_up: number;
  /** 下行丢包率 % */
  lossrate_down: number;
  /** 上行丢包率 % */
  lossrate_up: number;
  /** 上行包数 */
  pkt_up: number;
  /** 下行包数 */
  pkt_down: number;
  /** 上行丢包数 */
  pkt_loss_up: number;
  /** 下行丢包数 */
  pkt_loss_down: number;
  /** BWE 估算的可用上行带宽 kb/s（来自 candidate-pair） */
  available_outgoing_bitrate?: number;
  /** SFU/BWE 估算的可用下行带宽 kb/s（来自 candidate-pair） */
  available_incoming_bitrate?: number;
  /** 发布连接观测到的 RTT，单位 ms */
  rtt_up?: number;
  /** 订阅连接观测到的 RTT，单位 ms */
  rtt_down?: number;
}
```

:::note
旧版本的 `delay` 和 `up_level` 字段已被移除：`delay` 现在拆分为更精确的 `rtt_up` 与 `rtt_down`，`up_level` 由 `getConnectionQuality()` 返回的 `QualityEvaluation.uplink` 替代。
:::

### 2.3 全量 metric 快照 `getStreamMetric`

```typescript
const metric = srtc.getStreamMetric();
// => StreamMetric
```

```typescript
/** 流媒体引擎周期性输出的 metric 快照 */
export interface StreamMetric {
  /** 网络总体统计 */
  network: NetworkStats;
  /** 本地发布的音频轨道 */
  local_audios: TrackMetric[];
  /** 本地发布的视频轨道 */
  local_videos: TrackMetric[];
  /** 订阅的远端音频轨道 */
  remote_audios: TrackMetric[];
  /** 订阅的远端视频轨道 */
  remote_videos: TrackMetric[];
}

/** 单条轨道的实时 metric 快照 */
export interface TrackMetric {
  /** 实时码率 kb/s */
  bitrate?: number;
  /** 音频电平 dBFS */
  db?: number;
  /** 视频宽 */
  width?: number;
  /** 视频高 */
  height?: number;
  /** 实时帧率 */
  fps?: number;
  /** 原始 sender/receiver stats */
  stats?: AudioSenderStats | VideoSenderStats | AudioReceiverStats | VideoReceiverStats;
  /** 订阅端轨道所属用户 uid */
  uid?: string;
  /** 其他由 track.getInfo() 展开的字段 */
  [key: string]: any;
}
```

## 三、Track 级原始统计

`StreamMetric` 里每个 track 的 `stats` 字段对应 WebRTC 原生的 sender/receiver stats：

```typescript
/** 发送数据统计 */
interface SenderStats {
  /** 已发送的包数 */
  packetsSent?: number;
  /** 已发送的字节数 */
  bytesSent?: number;
  /** 远端感知到的网络抖动，单位 ms */
  jitter?: number;
  /** 远端报告的丢包数 */
  packetsLost?: number;
  /** 远端报告的往返时延，单位 ms */
  roundTripTime?: number;
  /** 出站流ID */
  streamId?: string;
  /** 时间戳 */
  timestamp: number;
}

export interface AudioSenderStats extends SenderStats {
  type: 'audio';
  /** 音频电平 */
  audioLevel?: number;
}

export interface VideoSenderStats extends SenderStats {
  type: 'video';
  /** 收到的FIR请求次数 */
  firCount: number;
  /** 收到的PLI请求次数 */
  pliCount: number;
  /** 收到的NACK请求次数 */
  nackCount: number;
  /** RTP流ID */
  rid: string;
  /** 帧宽度 */
  frameWidth: number;
  /** 帧高度 */
  frameHeight: number;
  /** 帧率 */
  framesPerSecond: number;
  /** 已发送的帧数 */
  framesSent: number;
  /** 质量限制原因(bandwidth/cpu/other/none) */
  qualityLimitationReason?: string;
  /** 质量限制持续时间 */
  qualityLimitationDurations?: Record<string, number>;
  /** 质量限制分辨率变化次数 */
  qualityLimitationResolutionChanges?: number;
  /** 重传包数 */
  retransmittedPacketsSent?: number;
  /** 目标码率 */
  targetBitrate: number;
}

/** 接收数据统计 */
interface ReceiverStats {
  /** 接收端抗抖动缓冲区累计延迟（开播至今所有出 buffer 帧的延迟总和），单位 ms */
  jitterBufferDelay?: number;
  /** 已从抖动缓冲区出列的帧/样本累计数；用于把累计 jitterBufferDelay 折算为均值 */
  jitterBufferEmittedCount?: number;
  /** 周期内（与上一次 stats 采样之间）平均每帧抖动缓冲延迟，单位 ms；体感延迟以此为准 */
  jitterBufferAvgDelay?: number;
  /** 累计丢包数（基于 RTP 序列号间隙统计） */
  packetsLost?: number;
  /** 累计接收 RTP 包数 */
  packetsReceived?: number;
  /** 累计接收字节数（含 RTP 头） */
  bytesReceived?: number;
  /** 媒体流标识（通常对应远端 SSRC） */
  streamId?: string;
  /** 网络层 RTP 抖动（RFC 3550 定义），单位 ms */
  jitter?: number;
  /** 本组 stats 的采集时间戳，单位 ms */
  timestamp: number;
}

export interface AudioReceiverStats extends ReceiverStats {
  type: 'audio';
  /** 音频电平 */
  audioLevel?: number;
  /** 隐藏样本数 */
  concealedSamples?: number;
  /** 隐藏事件次数 */
  concealmentEvents?: number;
  /** 静音隐藏样本数 */
  silentConcealedSamples?: number;
  /** 静音隐藏事件次数 */
  silentConcealmentEvents?: number;
  /** 总音频能量 */
  totalAudioEnergy?: number;
  /** 总样本时长 */
  totalSamplesDuration?: number;
}

export interface VideoReceiverStats extends ReceiverStats {
  type: 'video';
  /** 已解码的帧数 */
  framesDecoded: number;
  /** 丢帧数 */
  framesDropped: number;
  /** 已接收的帧数 */
  framesReceived: number;
  /** 帧率 */
  framesPerSecond?: number;
  /** 帧宽度 */
  frameWidth?: number;
  /** 帧高度 */
  frameHeight?: number;
  /** 发送的FIR请求次数 */
  firCount?: number;
  /** 发送的PLI请求次数 */
  pliCount?: number;
  /** 发送的NACK请求次数 */
  nackCount?: number;
  /** 解码器实现 */
  decoderImplementation?: string;
  /** MIME类型 */
  mimeType?: string;
  /** 视频卡顿次数（单次冻结 > 1s 或 > 3倍平均帧间隔，W3C 定义） */
  freezeCount?: number;
  /** 视频卡顿累计时长(s) */
  totalFreezesDuration?: number;
  /** 视频暂停次数（远端暂停发送） */
  pauseCount?: number;
  /** 视频暂停累计时长(s) */
  totalPausesDuration?: number;
  /** 由多 RTP 包拼装的帧数 */
  framesAssembledFromMultiplePackets?: number;
  /** 所有帧累计拼装耗时(s) */
  totalAssemblyTime?: number;
}
```

## 四、推荐的接入姿势

大多数业务只需要展示"网络状态灯"，推荐组合：

```typescript
// 1. 主动订阅等级变化，用于 UI 提示
srtc.onNotifyChannelEvent = (evt) => {
  if (evt.type === ChannelEventType.CONNECTION_QUALITY_CHANGED) {
    const { evaluation } = evt.data as ConnectionQualityEventData;
    updateNetworkIndicator(evaluation.overall); // 你的 UI 更新函数
  }
};

// 2. 需要详细数据面板时，按需调用 getStreamMetric
setInterval(() => {
  const metric = srtc.getStreamMetric();
  if (metric) renderDashboard(metric);
}, 2000);
```

## 五、弱网处理最佳实践

前面几节讲的是"怎么读信号"，这一节讲"读到信号后该做什么"——弱网下如何展示、如何提示、上行/下行分别怎么降级。

### 5.1 三条原则

从第一性原理出发，弱网处置有三条原则贯穿始终：

+ **分方向**：上行是**你可控**的（你是发送方，能降码率、关摄像头）；下行你**控制不了源头**（对方在发），只能**选择少收**。这是上行、下行处置本质不同的根源——所以永远优先看 `uplink` / `downlink` 两个方向，而不是只看 `overall`。
+ **分归因**：同样是"卡"，是**带宽不足**、**CPU 过载**还是**对方网络差**，处置完全不同。SDK 已用 `BANDWIDTH_CONSTRAINED` / `CPU_CONSTRAINED` 事件和 `reasons` 帮你区分。
+ **分级不打扰**：网络状态灯常驻，弹窗要克制。弱网本就让人烦躁，频繁弹窗是二次伤害。

### 5.2 展示什么

大多数场景只需要**一盏网络状态灯**，用 `getConnectionQuality()` 的 `overall` 四档映射颜色即可，不要把丢包率 / RTT 这类原始数字直接摆给终端用户（那是诊断面板才需要的）：

| `overall` | 灯 | 含义 |
| --- | --- | --- |
| `excellent` | 🟢 | 优秀 |
| `good` | 🟢 | 良好 |
| `poor` | 🟡 | 较差，画质可能下降 |
| `lost` | 🔴 | 连接断开，重连中 |
| `unknown` | ⚪️ | 采样中 |

**务必区分"你的问题"还是"对方的问题"**（避免用户困惑于"为什么网络好画面还糊"）：

```typescript
const q = srtc.getConnectionQuality();
if (q.uplink === ConnectionQuality.Poor) {
  // 上行差：是"你"发不出去
  showTip('您的网络不佳，对方可能看不清您的画面');
} else if (q.downlink === ConnectionQuality.Poor) {
  // 下行差：是"你"收不进来（也可能是对方发不出，见 5.5）
  showTip('网络不佳，正在优化接收画质');
}
```

### 5.3 提示什么（分级 + 去抖）

分级提示，别一有波动就弹窗：

| 触发 | 建议动作 | 文案示意 |
| --- | --- | --- |
| `good` → `poor` | 只变灯，不弹窗 | —— |
| `poor` 持续（如 5s 以上） | toast 一次 | "当前网络不佳" |
| `BANDWIDTH_CONSTRAINED` | toast + 触发上行降级（见 5.4） | "上行带宽不足，建议降低画质" |
| `CPU_CONSTRAINED` | toast | "设备繁忙，建议关闭其他应用" |
| `lost` | 明显提示 + 重连 UI | "连接已断开，正在重连…" |

SDK 的 `BANDWIDTH_CONSTRAINED` / `CPU_CONSTRAINED` 事件本身已做连续多次去抖再触发，但**业务层弹窗还要再做一层去抖**（进入弱网期不要反复弹）。

### 5.4 上行不行怎么处理

上行降级是一个"损失从小到大"的阶梯，逐级往下走：

1. **编码器自适应**（浏览器自动，SDK 默认已开）——第一层，无需干预，自动在带宽内调整。若你**不希望画面清晰度被自动压低**，见 5.6 用 `degradationPreference` 改变自适应方式。
2. **主动切小流 / 降分辨率**——切到小流（默认 `camera_small`：320×180、约 250 Kbps）或直接发一条低清单流，还有画面但更糊。见[大小流（simulcast）与分辨率](/zh/rtc/web/advanced/video-stream-layers)。
3. **关摄像头、只保留音频**——`disableLocalTrack(videoTrack)`，弱网上行的**终极兜底**。音频码率极低（约 32 Kbps）几乎总能保住，先保住"能听见"：

```typescript
// 关摄像头（轻量，保留发布通道，随时可 enableLocalTrack 恢复）
srtc.disableLocalTrack(localVideoTrack);
// 网络恢复后
srtc.enableLocalTrack(localVideoTrack);
```

4. **彻底停止发布视频**——`unpublishLocalTrack(videoTrack)`，比 `disableLocalTrack` 更重，彻底释放上行编码与发送资源。

> **CPU 受限与带宽受限的处置不同**：`CPU_CONSTRAINED` 时优先降**分辨率 / 帧率**（直接减轻编码负载）比降码率更有效；`BANDWIDTH_CONSTRAINED` 时降**码率 / 分辨率**都行。

**推荐交互（重要）**：关摄像头这类"改变通话形态"的操作，推荐**提示用户 + 一键降级**，而非静默自动执行——尤其应急指挥、执法记录等场景，**绝不能悄悄关掉画面**。普通会议等对画面连续性不敏感的场景，可以做得更自动。

### 5.5 下行不行怎么处理

下行你控制不了对方发多少，但能控制"收多少"：

1. **先判断是不是你自己的问题**：`downlink` 差**且**本端有下行丢包 → 是你的接收链路差；若本端几乎无丢包、只是对端画面卡顿 → 大概率是**对方上行差**（SDK 内部评分已做此区分，不会因对方的问题误降你的下行档）。这种情况本端退订也没用，只能提示"对方网络不佳"。
2. **保证发布方发了大小流（simulcast）**：这是下行降级的**主力**。"大小流"指同一路画面同时编码出一条大流（高清）和一条小流（默认 320×180、15fps、约 250 Kbps）。当发布方发了大小流，SFU 会**依据每个订阅者自身的下行带宽与丢包，自动**把该订阅者切到合适的那一条（下行变差自动切到 180p 小流，恢复后自动切回大流），订阅端**无需手动切**。反之，发布方只发单流时无小流可切，SFU 也无能为力。详见[大小流与分辨率](/zh/rtc/web/advanced/video-stream-layers)。
3. **退订视频、只收音频**——`unsubscribeRemoteTrack(remoteVideoTrack)`，下行的**终极兜底**，与上行"关摄像头保音频"对称：

```typescript
// 只退视频，保留音频，先保住"能听见"
await srtc.unsubscribeRemoteTrack(remoteVideoTrack);
```

4. **多路会议**：只订阅**当前说话人**的视频，其余成员只收音频；画廊视图里滚出可视区域的成员先退订视频。

### 5.6 控制自适应方式：`degradationPreference`

弱网下编码器必须有所取舍，`degradationPreference`（`publishLocalTrack` 的 `VideoPublishOptions` 字段）决定**牺牲什么**：

| 取值 | 弱网下的行为 | 适用 |
| --- | --- | --- |
| `maintain-framerate` | 宁**降分辨率**保帧率（画面变糊但流畅） | 一般实时互动、运动画面 |
| `maintain-resolution` | 宁**降帧率**保分辨率（画面清晰但变卡） | 屏幕共享、文档 / PPT、不希望分辨率跳变的场景 |
| `balanced` | 分辨率与帧率一起降 | 折中 |

**如果你不希望上行不好时分辨率被自动调低**（例如共享的是文字、图表，糊了就没法看），把它设成 `maintain-resolution`——这样带宽不足时编码器会先降帧率，保住分辨率：

```typescript
await srtc.publishLocalTrack(localVideoTrack, {
  // 宁可掉帧也不降分辨率，保清晰
  degradationPreference: 'maintain-resolution',
});
```

> SDK 的内置预设里，**摄像头 720p / 1080p 预设**与**全部屏幕共享预设**已默认 `maintain-resolution`（屏共尤其需要保清晰度）；480p / 360p 等低档预设未设置，走浏览器默认（弱网下通常优先降分辨率保帧率）。你在 `publishLocalTrack` 时显式传入该字段即可覆盖默认。

### 5.7 连接丢失（`lost`）与重连

`overall === 'lost'` 表示媒体已无法传输，应进入重连流程：给出明确的"正在重连"提示，避免界面停在一盏红灯；重连成功后刷新状态灯、按需恢复此前主动关闭的摄像头 / 订阅。

### 5.8 信号 → 处置 速查表

| 信号 | 方向 | 处置 |
| --- | --- | --- |
| `BANDWIDTH_CONSTRAINED` | 上行 | 切小流 → 关摄像头保音频；不想降分辨率则改用 `maintain-resolution` |
| `CPU_CONSTRAINED` | 上行 | 降分辨率 / 帧率，减轻编码负载 |
| `uplink = poor / lost` | 上行 | 按 5.4 阶梯降级 + 提示"您的网络" |
| `downlink = poor`（本端有丢包） | 下行 | 退订视频保音频 / 多路只留主讲；确保发布方发小流 |
| `downlink = poor`（本端无丢包） | 对方 | 提示"对方网络不佳"，本端不动 |
| `overall = lost` | —— | 重连 UI，恢复后刷新状态 |
