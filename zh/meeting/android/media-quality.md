---
title: "媒体质量"
description: "Android SMeeting 会议 SDK 媒体质量统计数据结构说明"
---

## 说明

本文基于 `MediaMetric.kt` 中的数据类（`data class`）整理。  
不包含接口（`interface`）定义说明。

## MediaMetric.Metric

综合媒体质量统计对象。

| 属性名称 | 数据类型 | 说明 |
| --- | --- | --- |
| localAudios | `MutableMap<UserTrackDesc, AudioSenderStats>` | 本地音频统计（按用户轨道）。 |
| localVideos | `MutableMap<UserTrackDesc, VideoSenderStats>` | 本地视频统计（按用户轨道）。 |
| remoteAudios | `MutableMap<UserTrackDesc, AudioReceiverStats>` | 远端音频统计（按用户轨道）。 |
| remoteVideos | `MutableMap<UserTrackDesc, VideoReceiverStats>` | 远端视频统计（按用户轨道）。 |
| localUploadStats | LocalUploadStats | 本地上传总览统计。 |
| remoteDownloadStats | `MutableMap<String, RemoteDownloadStats>` | 远端下载统计（按 `uid`）。 |
| networkStats | NetworkStats | 网络状态统计。 |
| qualityReport | QualityReport? | 服务端补充下发的上下行质量报告；首个报告到达前为 `null`。 |

## MediaMetric.QualityReport

服务端计算并下发的上下行连接质量报告，区分上行（本端到服务端）与下行（服务端到本端）。

| 属性名称 | 数据类型 | 说明 |
| --- | --- | --- |
| timestamp | Long | 服务端生成该质量报告的时间戳（ms）。 |
| uplink | QualityStats | 本端到服务端的上行质量。 |
| downlink | QualityStats | 服务端到本端的下行质量。 |

## MediaMetric.QualityStats

单侧链路（上行或下行）的质量样本。

| 属性名称 | 数据类型 | 说明 |
| --- | --- | --- |
| score | Double | 综合质量分数，0 ~ 100，越高越好。 |
| level | String | 质量等级：`excellent` / `good` / `poor` / `lost`。 |
| mos | Double | 语音主观质量分估算，1.0 ~ 4.5，越高越好。 |
| loss | Double | 丢包率，0 ~ 1。 |
| rtt | Double | 往返时延（ms）。 |
| jitter | Double | 抖动（ms）。 |
| packets | Long | 本轮统计参与计算的包数。 |
| bitrate | Double | 平均码率（kbps）。 |
| bytes | Long | 本窗口字节数。 |

## MediaMetric.LocalMetric

本地聚合统计对象（Map 的 key 为 `String`）。

| 属性名称 | 数据类型 | 说明 |
| --- | --- | --- |
| localAudios | `MutableMap<String, AudioSenderStats>` | 本地音频统计。 |
| localVideos | `MutableMap<String, VideoSenderStats>` | 本地视频统计。 |
| remoteAudios | `MutableMap<String, AudioReceiverStats>` | 远端音频统计。 |
| remoteVideos | `MutableMap<String, VideoReceiverStats>` | 远端视频统计。 |
| networkStats | NetworkStats | 网络状态统计。 |

## MediaMetric.NetworkStats

网络状态统计对象。

| 属性名称 | 数据类型 | 说明 |
| --- | --- | --- |
| bitrateUp | Float | 上行码率（kb/s）。 |
| bitrateDown | Float | 下行码率（kb/s）。 |
| delay | Float | 延迟。 |
| lossrateUp | Float | 上行丢包率。 |
| lossrateDown | Float | 下行丢包率。 |
| upLevel | MediaUploadLevel | 上行质量等级。 |
| downLossLevel | MediaDownLossLevel | 下行丢包等级。 |
| pktUp | Long | 上行包数。 |
| pktDown | Long | 下行包数。 |
| pktLossUp | Long | 上行丢包数。 |
| pktLossDown | Long | 下行丢包数。 |

## MediaMetric.LocalUploadStats

本地上传统计对象。

| 属性名称 | 数据类型 | 说明 |
| --- | --- | --- |
| uid | String | 用户 ID。 |
| delay | Float | 上传延时。 |
| videoBitrate | Float | 视频上传码率（kb/s）。 |
| audioBitrate | Float | 音频上传码率（kb/s）。 |
| lossrate | Float | 丢包率。 |

## MediaMetric.RemoteDownloadStats

远端下载统计对象。

| 属性名称 | 数据类型 | 说明 |
| --- | --- | --- |
| uid | String | 用户 ID。 |
| audioPacketsReceived | Long | 接收的音频包数。 |
| videoPacketsReceived | Long | 接收的视频包数（含重传包）。 |
| packetsLost | Long | 丢包数。 |
| retransmittedPackets | Long | 重传包数（视频）。 |
| lossrate | Float | 丢包率。 |
| downLevel | MediaDownLevel | 下行质量等级。 |
| audioBitrate | Float | 音频码率（kb/s）。 |
| videoBitrate | Float | 视频码率（kb/s）。 |

## MediaMetric.AudioSenderStats

音频发送统计对象。

| 属性名称 | 数据类型 | 说明 |
| --- | --- | --- |
| audioLevel | Float | 音频能量。 |
| trackId | String | 轨道 ID。 |
| packetsSent | Long | 发送包数。 |
| byteSent | Long | 发送字节数。 |
| bitrateSent | Float | 发送码率（kb/s）。 |
| jitter | Float | 网络抖动。 |
| packetsLost | Int | 丢包数（未扣除重传）。 |
| roundTripTime | Float | 往返时延。 |
| mimeType | String | 编解码器类型。 |
| timestamp | Long | 时间戳（ms）。 |
| type | String | 媒体类型，固定为 `audio`。 |

## MediaMetric.VideoSenderStats

视频发送统计对象。

| 属性名称 | 数据类型 | 说明 |
| --- | --- | --- |
| firCount | Long | 请求发送 I 帧次数。 |
| pliCount | Long | 请求发送 P 帧次数。 |
| nackCount | Long | 请求重传丢失 RTP 包次数。 |
| rid | String | Simulcast 流标识。 |
| frameWidth | Int | 视频帧宽度。 |
| frameHeight | Int | 视频帧高度。 |
| framesPerSecond | Float | 视频帧率（fps）。 |
| frameSent | Long | 发送帧数。 |
| qualityLimitationReason | String | 质量受限主要原因（如 none/cpu/bandwidth/other/inactive）。 |
| qualityLimitationDurations | `Map<String, Float>` | 各限制原因累计时长（秒）。 |
| qualityLImitationResolutionChange | Long | 因质量限制导致分辨率变化次数。 |
| retransmittedPacketsSent | Long | 已重传 RTP 包数。 |
| targetBitrate | Float | 编码器目标比特率（bps）。 |
| trackId | String | 轨道 ID。 |
| packetsSent | Long | 发送包数。 |
| byteSent | Long | 发送字节数。 |
| bitrateSent | Float | 发送码率（kb/s）。 |
| jitter | Float | 网络抖动。 |
| packetsLost | Int | 丢包数（未扣除重传）。 |
| roundTripTime | Float | 往返时延。 |
| mimeType | String | 编解码器类型。 |
| timestamp | Long | 时间戳（ms）。 |
| type | String | 媒体类型，固定为 `video`。 |

## MediaMetric.AudioReceiverStats

音频接收统计对象。

| 属性名称 | 数据类型 | 说明 |
| --- | --- | --- |
| audioLevel | Float | 音频能量。 |
| concealedSamples | Long | 补偿恢复的音频样本总数。 |
| concealEvents | Long | 插值操作次数。 |
| silentConcealedSamples | Long | 被补偿为静音的样本数量。 |
| silentConcealmentEvents | Long | 静音补偿事件次数。 |
| totalAudioEnergy | Double | 累计接收音频能量。 |
| totalSamplesDuration | Double | 累计播放时长（秒）。 |
| trackId | String | 轨道 ID。 |
| packetsReceived | Long | 接收包数。 |
| bytesReceived | Long | 接收字节数。 |
| bitrateReceived | Float | 接收码率（kb/s）。 |
| jitter | Float | 网络抖动。 |
| jitterBufferDelay | Float | 抖动缓冲累计延迟。 |
| packetsLost | Int | 丢包数（未扣除重传）。 |
| mimeType | String | 编解码器类型。 |
| timestamp | Long | 时间戳（ms）。 |
| type | String | 媒体类型，固定为 `audio`。 |

## MediaMetric.VideoReceiverStats

视频接收统计对象。

| 属性名称 | 数据类型 | 说明 |
| --- | --- | --- |
| framesDecoded | Long | 成功解码帧数。 |
| framesDropped | Long | 解码丢弃帧数。 |
| framesReceived | Long | 接收总帧数。 |
| framesPerSecond | Float | 接收帧率（fps）。 |
| frameWidth | Int | 接收帧宽度。 |
| frameHeight | Int | 接收帧高度。 |
| firCount | Int | 请求发送 I 帧次数。 |
| pliCount | Int | 请求发送 P 帧次数。 |
| nackCount | Int | 请求重传丢失 RTP 包次数。 |
| retransmittedPacketsReceived | Long | 接收端统计的重传包数。 |
| decoderImplementation | String | 解码器实现名称。 |
| trackId | String | 轨道 ID。 |
| packetsReceived | Long | 接收包数。 |
| bytesReceived | Long | 接收字节数。 |
| bitrateReceived | Float | 接收码率（kb/s）。 |
| jitter | Float | 网络抖动。 |
| jitterBufferDelay | Float | 抖动缓冲累计延迟。 |
| packetsLost | Int | 丢包数（未扣除重传）。 |
| mimeType | String | 编解码器类型。 |
| timestamp | Long | 时间戳（ms）。 |
| type | String | 媒体类型，固定为 `video`。 |
