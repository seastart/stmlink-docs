---
title: "网络质量"
description: "Web SRTC 音视频 SDK 流媒体网络质量监测接口说明"
---

当前流媒体网络质量可以通过`srtc.getStreamMetric`来获取

获取到的是一个map，包括最核心`network`数据，这是一个网络总体统计，说明如下

```typescript
/**
 * 网络总体统计
 */
export interface NetworkStats {
  /** 下行码率kb/s */
  bitrate_down: number;
  /** 上行码率kb/s */
  bitrate_up: number;
  /** 延迟ms */
  delay: number;
  /** 下行丢包率 */
  lossrate_down: number;
  /** 上行丢包率 */
  lossrate_up: number;
  /** 上行等级 */
  up_level: number;
  /** 上行包数 */
  pkt_up: number;
  /** 下行包数 */
  pkt_down: number;
  /** 上行丢包数 */
  pkt_loss_up: number;
  /** 下行丢包数 */
  pkt_loss_down: number;
}
```typescript

如果需要更详细的数据，包括`local_audios``local_videos``remote_audios``remote_videos`数据，说明如下

```typescript
/**
 * 发送数据统计
 */
interface SenderStats {
    /** 已发送的包数 */
    packetsSent?: number;

    /** 已发送的字节数 */
    bytesSent?: number;

    /** 远端感知到的抖动 */
    jitter?: number;

    /** 远端报告的丢包数 */
    packetsLost?: number;

    /** 远端报告的往返时延(ms) */
    roundTripTime?: number;

    /** 出站流ID */
    streamId?: string;

    /** 时间戳 */
    timestamp: number;
}

export interface AudioSenderStats extends SenderStats {
    /** 类型 */
    type: 'audio';

    /** 音频电平 */
    audioLevel?: number;
}

export interface VideoSenderStats extends SenderStats {
    /** 类型 */
    type: 'video';

    /** 收到的FIR(Full Intra Request)请求次数 */
    firCount: number;

    /** 收到的PLI(Picture Loss Indication)请求次数 */
    pliCount: number;

    /** 收到的NACK(Negative Acknowledgement)请求次数 */
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

    /** 质量限制原因(bandwidth, cpu, other, none) */
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

/**
 * 接收数据统计
 */
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
    /** 类型 */
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
    /** 类型 */
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

    /** 发送的FIR(Full Intra Request)请求次数 */
    firCount?: number;

    /** 发送的PLI(Picture Loss Indication)请求次数 */
    pliCount?: number;

    /** 发送的NACK(Negative Acknowledgement)请求次数 */
    nackCount?: number;

    /** 解码器实现 */
    decoderImplementation?: string;

    /** MIME类型 */
    mimeType?: string;
}
```

