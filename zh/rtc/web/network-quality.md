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
import { CommonChannelEventType, ConnectionQualityEventData } from '@stmlink/rtc-js';

srtc.onNotifyChannelEvent = (evt) => {
  switch (evt.type) {
    case CommonChannelEventType.CONNECTION_QUALITY_CHANGED: {
      // 网络等级变化时触发（excellent/good/poor/lost/unknown）
      const { evaluation, previous } = evt.data as ConnectionQualityEventData;
      console.log(`网络质量: ${previous} -> ${evaluation.overall}`);
      console.log(`原因:`, evaluation.reasons);
      console.log(`MOS:`, evaluation.mos);
      break;
    }
    case CommonChannelEventType.CPU_CONSTRAINED:
      // 发送端被 CPU 持续限制，建议降低画质/分辨率
      toast('CPU 过载，建议降低画质');
      break;
    case CommonChannelEventType.BANDWIDTH_CONSTRAINED:
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
  /** 音频 MOS 估算，1.0 ~ 4.5 */
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
  /** BWE 估算的可用下行带宽 kb/s（来自 candidate-pair） */
  available_incoming_bitrate?: number;
  /** candidate-pair 实时链路 RTT ms，比 remote-inbound-rtp 更准确 */
  current_rtt?: number;
}
```

:::note
旧版本的 `delay` 和 `up_level` 字段已被移除：`delay` 由更精确的 `current_rtt` 替代，`up_level` 由 `getConnectionQuality()` 返回的 `QualityEvaluation.uplink` 替代。
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
  /** 远端感知到的抖动 */
  jitter?: number;
  /** 远端报告的丢包数 */
  packetsLost?: number;
  /** 远端报告的往返时延(s) */
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
  /** 抖动缓冲延迟 */
  jitterBufferDelay?: number;
  /** 丢包数 */
  packetsLost?: number;
  /** 已接收的包数 */
  packetsReceived?: number;
  /** 已接收的字节数 */
  bytesReceived?: number;
  /** 流ID */
  streamId?: string;
  /** 抖动 */
  jitter?: number;
  /** 时间戳 */
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
  if (evt.type === CommonChannelEventType.CONNECTION_QUALITY_CHANGED) {
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
