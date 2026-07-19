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

## 五、弱网处理

处理弱网先分清两件事：**方向**和**原因**。

+ 上行差是你发不出去，你能主动降级（降码率、切小流、关摄像头）；下行差是你收不进来，只能少收（切小流、退订视频）。所以要看 `uplink` / `downlink` 两个方向，而不是只看 `overall`。
+ `BANDWIDTH_CONSTRAINED` 是带宽不足，`CPU_CONSTRAINED` 是设备编码跟不上，两者处置不同。

### 5.1 展示网络状态

用 `overall` 映射一个状态灯即可，不要把丢包率、RTT 这类原始数据直接展示给终端用户：

| overall | 状态 |
| --- | --- |
| excellent / good | 正常 |
| poor | 较差，画质可能下降 |
| lost | 断开，重连中 |
| unknown | 采样中 |

上行差和下行差的提示文案不同，需要区分：

```typescript
const q = srtc.getConnectionQuality();
if (q.uplink === ConnectionQuality.Poor) {
  showTip('您的网络不佳，对方可能看不清您');
} else if (q.downlink === ConnectionQuality.Poor) {
  showTip('网络不佳，正在优化画质');
}
```

提示要去抖：`poor` 持续几秒再 toast，不要一波动就弹。`BANDWIDTH_CONSTRAINED` / `CPU_CONSTRAINED` 事件 SDK 已做去抖，业务层弹窗建议再限一次频率。

### 5.2 上行变差

按从轻到重逐级降级：

1. **编码器自适应**：浏览器自动完成，默认已开，无需干预。不想让分辨率被自动压低时，用 `degradationPreference` 改变降级方式（见 5.4）。
2. **切小流 / 降分辨率**：发布了大小流时可切到小流（320×180、约 250 Kbps）。见[大小流与分辨率](/zh/rtc/web/advanced/video-stream-layers)。
3. **关摄像头、只保留音频**：音频码率低（约 32 Kbps），弱网下几乎总能保住。

```typescript
srtc.disableLocalTrack(localVideoTrack);  // 关闭（轻量，保留发布通道，可随时恢复）
srtc.enableLocalTrack(localVideoTrack);   // 网络恢复后重新开启
```

4. **彻底停止发布**：`unpublishLocalTrack(localVideoTrack)`，比关摄像头更彻底，释放上行编码与发送资源。

`CPU_CONSTRAINED` 时优先降分辨率 / 帧率（减轻编码负载）；`BANDWIDTH_CONSTRAINED` 时降码率或分辨率都可以。

关摄像头会改变通话形态，建议提示用户后再执行，不要静默操作——应急指挥、执法记录等场景尤其如此。

### 5.3 下行变差

1. **先确认是不是对端的问题**：本端有下行丢包，才是你的接收链路差；若本端几乎无丢包、只是某人画面卡顿，通常是对方上行差，此时你退订也无济于事，提示"对方网络不佳"即可。SDK 评分已区分这两种情况，不会因对方问题误降你的下行档。
2. **发布方发大小流时，SFU 自动切层**：SFU 会依据每个订阅者自身的下行带宽和丢包，自动把它切到合适的大 / 小流，订阅端无需手动切；只发单流则无法自动降。见[大小流与分辨率](/zh/rtc/web/advanced/video-stream-layers)。
3. **退订视频、只收音频**：

```typescript
await srtc.unsubscribeRemoteTrack(remoteVideoTrack);
```

4. **多路会议**：只订阅当前说话人的视频，其余成员只收音频。

### 5.4 控制降级方式：`degradationPreference`

`publishLocalTrack` 的 `VideoPublishOptions.degradationPreference` 决定弱网下牺牲什么：

| 取值 | 行为 | 适用 |
| --- | --- | --- |
| `maintain-framerate` | 降分辨率、保帧率 | 一般实时互动、运动画面 |
| `maintain-resolution` | 降帧率、保分辨率 | 屏幕共享、文档 / PPT，不希望分辨率变化 |
| `balanced` | 两者都降 | 折中 |

不希望分辨率被自动压低时，设为 `maintain-resolution`：

```typescript
await srtc.publishLocalTrack(localVideoTrack, {
  degradationPreference: 'maintain-resolution',
});
```

内置预设中，摄像头 720p / 1080p 与全部屏幕共享预设默认已是 `maintain-resolution`；480p / 360p 未设置，走浏览器默认。

### 5.5 连接断开（`lost`）

`overall === 'lost'` 表示媒体已中断，应进入重连并提示用户"正在重连"；恢复后刷新状态灯，并恢复此前主动关闭的摄像头或订阅。

### 5.6 速查表

| 信号 | 处置 |
| --- | --- |
| `BANDWIDTH_CONSTRAINED`（上行） | 切小流 → 关摄像头保音频；不想降分辨率则设 `maintain-resolution` |
| `CPU_CONSTRAINED`（上行） | 降分辨率 / 帧率 |
| `uplink = poor / lost` | 按 5.2 降级，提示"您的网络" |
| `downlink = poor`（本端有丢包） | 退订视频保音频 / 多路只留主讲 |
| `downlink = poor`（本端无丢包） | 提示"对方网络不佳" |
| `overall = lost` | 重连，恢复后刷新状态 |

### 5.7 完整示例

把上面的做法串起来：发布时配置降级策略，运行时订阅事件更新状态灯、分方向提示、按需降级与恢复。

```typescript
import { ChannelEventType, ConnectionQuality } from '@seastart/srtc-web-sdk';
import type { ConnectionQualityEventData, LocalVideoTrack } from '@seastart/srtc-web-sdk';

// 假设已创建并持有本地摄像头轨道
let cameraTrack: LocalVideoTrack;
// 标记是否因弱网主动关了摄像头，用于网络恢复后自动开回
let cameraOffByNetwork = false;

// 发布：开大小流（弱网时对端可自动降到小流）；若共享的是文档/PPT，用 maintain-resolution 保清晰
await srtc.publishLocalTrack(cameraTrack, {
  degradationPreference: 'maintain-framerate', // 一般互动用这个；文档共享改 'maintain-resolution'
});

// 简单去抖：同一类提示 N 秒内只弹一次
const lastToast: Record<string, number> = {};
function toastOnce(key: string, msg: string, intervalMs = 8000) {
  const now = Date.now();
  if (now - (lastToast[key] ?? 0) < intervalMs) return;
  lastToast[key] = now;
  toast(msg); // 替换为你的 toast 实现
}

srtc.onNotifyChannelEvent = (evt) => {
  switch (evt.type) {
    // 1) 网络等级变化：更新状态灯 + 按方向提示 + 断线重连 + 恢复
    case ChannelEventType.CONNECTION_QUALITY_CHANGED: {
      const { evaluation } = evt.data as ConnectionQualityEventData;
      updateNetworkIndicator(evaluation.overall); // 你的状态灯

      if (evaluation.overall === ConnectionQuality.Lost) {
        showReconnecting(); // 显示"正在重连"
      } else if (evaluation.uplink === ConnectionQuality.Poor) {
        toastOnce('uplink', '您的网络不佳，对方可能看不清您');
      } else if (evaluation.downlink === ConnectionQuality.Poor) {
        toastOnce('downlink', '网络不佳，正在优化画质');
        // 下行较差时 SFU 会自动把你降到小流，多数能自行缓解，一般无需处理。
        // 若要做"仅语音"兜底：建议下行持续较久仍不佳时，再让用户确认，
        // 然后对当前订阅的远端视频轨调用 srtc.unsubscribeRemoteTrack(videoTrack) 退订、只留音频。
      }

      // 网络恢复且此前因弱网关过摄像头 → 自动开回
      if (
        cameraOffByNetwork &&
        (evaluation.overall === ConnectionQuality.Good ||
          evaluation.overall === ConnectionQuality.Excellent)
      ) {
        srtc.enableLocalTrack(cameraTrack);
        cameraOffByNetwork = false;
      }
      break;
    }

    // 2) 上行带宽不足：提示用户，并给一个"关摄像头保语音"的一键操作（不静默执行）
    case ChannelEventType.BANDWIDTH_CONSTRAINED:
      toastOnce('bw', '上行带宽不足，可关闭摄像头以保证语音通话');
      showDowngradeButton(() => {
        srtc.disableLocalTrack(cameraTrack); // 关摄像头，保留音频
        cameraOffByNetwork = true;
      });
      break;

    // 3) 设备编码跟不上：提示降低画质 / 关闭其他应用
    case ChannelEventType.CPU_CONSTRAINED:
      toastOnce('cpu', '设备繁忙，建议关闭其他应用或降低画质');
      break;
  }
};
```

> 示例里 `publishLocalTrack` / `disableLocalTrack` / `enableLocalTrack` 均为 SDK 现有方法。关摄像头这类改变通话形态的操作通过按钮交给用户确认，未静默执行；普通会议等场景可自行改为自动。下行"仅语音"兜底按注释里的思路自行实现（用 `unsubscribeRemoteTrack` 退订视频、保留音频）。
