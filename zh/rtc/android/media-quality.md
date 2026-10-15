---
title: "媒体质量"
description: "Android SRTC 本地质量快照、按需查询的 MediaMetric 与 FY 服务端报告的数据结构和数值单位。"
---

本页记录 `cn.seastart.rtc.monitoring.api` 的公开监测模型。如何接收回调和查询数据，见 [网络质量](/zh/rtc/android/network-quality)。旧版 `cn.seastart.rtc.statistics.MediaMetric` 的嵌套类型与 `onMediaMetric` 回调已移除；迁移时改用本页的顶层类型、`onLocalQualitySnapshot` 和 `getMetric()`。

## LocalQualitySnapshot

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `timestamp` | `Long` | 本轮底层采样完成的墙钟时间，毫秒。 |
| `networkQuality` | `NetworkQuality` | 本地上下行网络质量。 |
| `mediaPlaybackExperience` | `MediaPlaybackExperience` | 本地下行音视频播放连续性。 |

两个子对象的 `timestamp` 与外层时间戳必须相等。快照不包含逐轨原始计数；需要详细统计时调用 `getMetric()`。

### NetworkQuality、DirectionQuality 与 TrackQuality

`NetworkQuality` 包含 `timestamp`、`uplink: DirectionQuality`、`downlink: DirectionQuality`、`localTracks: List<TrackQuality>` 和 `remoteTracks: List<TrackQuality>`。无对应轨道时列表为空。

| 模型 | 字段 | 说明 |
| --- | --- | --- |
| `DirectionQuality` | `level: QualityLevel` | 可评估轨道的最差网络档位，样本不足为 `UNKNOWN`。 |
| `DirectionQuality` | `constraint: QualityConstraint?` | 上行视频受限原因；下行不适用为 `NONE`，应有但不可得为 `null`。 |
| `DirectionQuality` | `lossRate: Float?`、`rttMs: Float?`、`jitterMs: Float?` | 方向内可得单轨窗口丢包率最大值（0～1）、路径 RTT 和抖动（ms）。 |
| `TrackQuality` | `key: UserTrackDesc`、`kind: TrackKind`、`direction: QualityDirection` | 定位用户轨道、音视频种类与收发方向。 |
| `TrackQuality` | `level: QualityLevel`、`score: Float?`、`constraint: QualityConstraint?` | 单轨网络档位、0～100 分数和上行视频受限原因。分数不可算时为 `null`。 |
| `TrackQuality` | `lossRate: Float?`、`bitrateBps: Float?`、`rttMs: Float?`、`jitterMs: Float?` | 单轨窗口丢包率（0～1）、实际码率（bps）、RTT 与抖动（ms）。 |

`QualityLevel` 为 `UNKNOWN`、`EXCELLENT`、`GOOD`、`POOR`、`BAD`、`LOST`；`QualityConstraint` 为 `NONE`、`CPU`、`BANDWIDTH`。`QualityDirection` 为 `UPLINK`、`DOWNLINK`。`UNKNOWN` 表示无可靠判定；`LOST` 仅表示预期传输轨道的 ICE 进入 `FAILED`。更多枚举见 [枚举类型](/zh/rtc/android/enums)。

### MediaPlaybackExperience

`MediaPlaybackExperience` 包含 `timestamp`、`videoTracks: List<VideoTrackPlaybackExperience>` 和 `audioTracks: List<AudioTrackPlaybackExperience>`，只描述本地**下行**播放连续性。

| 模型 | 字段 | 说明 |
| --- | --- | --- |
| `VideoTrackPlaybackExperience` | `key: UserTrackDesc`、`level: VideoPlaybackLevel` | 视频轨标识与 `UNKNOWN` / `SMOOTH` / `DEGRADED` / `FROZEN` 档位。 |
| `VideoTrackPlaybackExperience` | `dropRatio: Float?`、`currentBlockDurationMs: Long?`、`blockRate10s: Float?` | 窗口丢帧比（0～1）、当前连续卡顿时长（ms）、最近 10 秒卡顿时间比例（0～1）。 |
| `AudioTrackPlaybackExperience` | `key: UserTrackDesc`、`level: AudioPlaybackLevel` | 音频轨标识与 `UNKNOWN` / `CLEAR` / `DEGRADED` / `INTERRUPTED` 档位。 |
| `AudioTrackPlaybackExperience` | `concealmentRatio: Float?`、`silentConcealmentRatio: Float?` | 窗口隐藏样本与静音隐藏样本占接收样本的比例，0～1。 |
| `AudioTrackPlaybackExperience` | `averageJitterBufferDelayMs: Float?`、`currentInterruptionDurationMs: Long?` | 平均 jitter buffer 输出延迟与当前连续中断时长，ms。 |

## MediaMetric

`RTCEngine.getMetric()` 返回默认频道的 `MediaMetric?`，`RTCChannel.getMetric()` 返回指定频道的 `MediaMetric?`。结果是最近完成采样的副本；不可用时为 `null`。详细模型不提供网络或播放等级。

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `channel` | `String` | 采样所属频道。 |
| `sampleTimestampMs` | `Long` | 采样完成的墙钟时间，与同帧快照时间戳相同。 |
| `localAudios` | `MutableMap<UserTrackDesc, AudioSenderStats>` | 已识别本地音频发送轨道的统计。 |
| `localVideos` | `MutableMap<UserTrackDesc, VideoSenderStats>` | 已识别本地视频发送轨道的统计。 |
| `remoteAudios` | `MutableMap<UserTrackDesc, AudioReceiverStats>` | 已识别远端音频接收轨道的统计。 |
| `remoteVideos` | `MutableMap<UserTrackDesc, VideoReceiverStats>` | 已识别远端视频接收轨道的统计。 |
| `localUploadStats` | `LocalUploadStats` | 本地音视频窗口码率合计。 |
| `remoteDownloadStats` | `MutableMap<String, RemoteDownloadStats>` | 按远端 `uid` 汇总的统计。 |
| `networkStats` | `NetworkStats` | 上下行网络总体统计。 |
| `qualityReport` | `ServerQualityReport?` | FY 服务端报告；WS 或尚无报告时为 `null`。 |

### 详细统计字段与单位

| 模型 | 字段 | 口径 |
| --- | --- | --- |
| `SenderStats` | `trackId`、`packetsSent`、`byteSent`、`bitrateSent`、`jitter`、`packetsLost`、`roundTripTime`、`mimeType`、`timestamp` | 包数和字节数累计；窗口码率 bps；抖动与 RTT 为 ms；逐轨时间戳来自 RTCStats，单位 ms。 |
| `ReceiverStats` | `trackId`、`packetsReceived`、`bytesReceived`、`bitrateReceived`、`jitter`、`packetsLost`、`mimeType`、`timestamp` | 包数和字节数累计；窗口码率 bps；抖动 ms。 |
| `AudioSenderStats` | `audioLevel` | 音量，约 -60～0 dBFS；另含 `SenderStats` 字段。 |
| `VideoSenderStats` | `firCount`、`pliCount`、`nackCount`、`rid`、`frameWidth`、`frameHeight`、`framesPerSecond`、`frameSent`、`qualityLimitationReason`、`qualityLimitationDurationsSeconds`、`qualityLImitationResolutionChange`、`retransmittedPacketsSent`、`targetBitrate`、`maxBitrate` | 另含 `SenderStats` 字段；帧率 fps，目标及最大码率 bps；限制时长为累计秒数，`maxBitrate=0` 表示未配置。 |
| `AudioReceiverStats` | `audioLevel`、`totalSamplesReceived`、`concealedSamples`、`concealEvents`、`silentConcealedSamples`、`silentConcealmentEvents`、`generatedNoiseSamples`、`interruptionCount`、`totalInterruptionDurationSeconds`、`totalAudioEnergy`、`totalSamplesDurationSeconds`、`jitterBufferDelaySeconds`、`jitterBufferEmittedCount` | 另含 `ReceiverStats` 字段；时长字段为累计秒数，样本与事件字段为累计计数。 |
| `VideoReceiverStats` | `framesDecoded`、`framesRendered`、`framesDropped`、`framesReceived`、`jitterBufferDelaySeconds`、`framesPerSecond`、`frameWidth`、`frameHeight`、`firCount`、`pliCount`、`nackCount`、`retransmittedPacketsReceived`、`decoderImplementation`、`freezeCount`、`totalFreezesDurationSeconds` | 另含 `ReceiverStats` 字段；帧与事件字段为累计计数，冻结和缓冲时长为累计秒数。 |
| `LocalUploadStats` | `uid`、`videoBitrate`、`audioBitrate` | 按本地发送轨合计的窗口码率，bps。 |
| `RemoteDownloadStats` | `uid`、`audioPacketsReceived`、`videoPacketsReceived`、`packetsLost`、`retransmittedPackets`、`lossrate`、`audioBitrate`、`videoBitrate` | 按远端用户聚合；计数累计，`lossrate` 为窗口比例 0～1，码率 bps。 |
| `NetworkStats` | `bitrateUp`、`bitrateDown`、`lossrateUp`、`lossrateDown`、`rttUpMs`、`rttDownMs`、`pktUp`、`pktDown`、`pktLossUp`、`pktLossDown` | 码率 bps；丢包率为窗口比例 0～1；RTT ms；包数累计。 |

不存在的轨道不进入 map。无对应轨道时，部分合计为 `0`；已有轨道但原始计数或有效窗口不足时，相关测量为 `null`，不会把缺失伪装为实测零。多个轨道中任一组成值不可得时，该项合计为 `null`。详细方向丢包率按合计包数计算，快照方向 `lossRate` 则取可得单轨窗口丢包率最大值，因此两者可能不同。逐轨 `timestamp` 不能与 `sampleTimestampMs` 直接当作同一时钟比较。

## ServerQualityReport 与 NetworkQualityChange

FY 的 `ServerQualityReport` 含 `timestamp`、`uplink: ServerQualityStats`、`downlink: ServerQualityStats`。每个 `ServerQualityStats` 含 `score`（0～100）、`level`（`excellent` / `good` / `poor` / `lost`）、`mos`、`loss`（0～1）、`rtt`（ms）、`jitter`（ms）、`packets`、`bitrate`（kbps）、`bytes`。服务端数值沿后端契约透传，不套用本地统计单位。

`NetworkQualityChange` 含 `direction: QualityDirection`、`previousLevel: String`、`currentLevel: String`、`trend: QualityTrend` 和 `report: ServerQualityReport`。它只由 FY 服务端报告驱动，与本地 `LocalQualitySnapshot` 的评估相互独立。
