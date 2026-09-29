---
title: "Media quality"
description: "Field-level data dictionary for Android SRTC media quality statistics in MediaMetric: the overall Metric, server-side uplink/downlink QualityReport, network, upload, and download stats, and per-track audio/video sender and receiver stats. Read when interpreting onMediaMetric data."
---

## Description

This page is compiled from the data classes (`data class`) in `MediaMetric.kt` and serves as a field-level data dictionary.  
It doesn't cover interface (`interface`) definitions.

For how to get quality data (subscription callbacks / active queries) and how to handle poor networks, see [Network quality](/en/rtc/android/network-quality).

## MediaMetric.Metric

The overall media quality statistics object.

| Property | Data type | Description |
| --- | --- | --- |
| localAudios | `MutableMap<UserTrackDesc, AudioSenderStats>` | Local audio stats (by user track). |
| localVideos | `MutableMap<UserTrackDesc, VideoSenderStats>` | Local video stats (by user track). |
| remoteAudios | `MutableMap<UserTrackDesc, AudioReceiverStats>` | Remote audio stats (by user track). |
| remoteVideos | `MutableMap<UserTrackDesc, VideoReceiverStats>` | Remote video stats (by user track). |
| localUploadStats | LocalUploadStats | Local upload overview stats. |
| remoteDownloadStats | `MutableMap<String, RemoteDownloadStats>` | Remote download stats (by `uid`). |
| networkStats | NetworkStats | Network status stats. |
| qualityReport | QualityReport? | Uplink/downlink quality report additionally sent by the server; `null` until the first report arrives. |

## MediaMetric.QualityReport

The uplink/downlink connection quality report computed and sent by the server, distinguishing uplink (this client to the server) from downlink (the server to this client).

| Property | Data type | Description |
| --- | --- | --- |
| timestamp | Long | Timestamp (ms) when the server generated the quality report. |
| uplink | QualityStats | Uplink quality from this client to the server. |
| downlink | QualityStats | Downlink quality from the server to this client. |

## MediaMetric.QualityStats

A quality sample for one direction of the link (uplink or downlink).

| Property | Data type | Description |
| --- | --- | --- |
| score | Double | Overall quality score, 0–100; higher is better. |
| level | String | Quality level: `excellent` / `good` / `poor` / `lost`. |
| mos | Double | Estimated voice MOS (mean opinion score), 1.0–4.5; higher is better. |
| loss | Double | Packet loss rate, 0–1. |
| rtt | Double | Round-trip time (ms). |
| jitter | Double | Jitter (ms). |
| packets | Long | Number of packets included in this round of statistics. |
| bitrate | Double | Average bitrate (kbps). |
| bytes | Long | Bytes in this window. |

## MediaMetric.LocalMetric

The local aggregated statistics object (Map keys are `String`).

| Property | Data type | Description |
| --- | --- | --- |
| localAudios | `MutableMap<String, AudioSenderStats>` | Local audio stats. |
| localVideos | `MutableMap<String, VideoSenderStats>` | Local video stats. |
| remoteAudios | `MutableMap<String, AudioReceiverStats>` | Remote audio stats. |
| remoteVideos | `MutableMap<String, VideoReceiverStats>` | Remote video stats. |
| networkStats | NetworkStats | Network status stats. |

## MediaMetric.NetworkStats

The network status statistics object.

| Property | Data type | Description |
| --- | --- | --- |
| bitrateUp | Float | Uplink bitrate (kb/s). |
| bitrateDown | Float | Downlink bitrate (kb/s). |
| delay | Float | Delay. |
| lossrateUp | Float | Uplink packet loss rate. |
| lossrateDown | Float | Downlink packet loss rate. |
| pktUp | Long | Uplink packet count. |
| pktDown | Long | Downlink packet count. |
| pktLossUp | Long | Uplink packets lost. |
| pktLossDown | Long | Downlink packets lost. |

## MediaMetric.LocalUploadStats

The local upload statistics object.

| Property | Data type | Description |
| --- | --- | --- |
| uid | String | User ID. |
| delay | Float | Upload delay. |
| videoBitrate | Float | Video upload bitrate (kb/s). |
| audioBitrate | Float | Audio upload bitrate (kb/s). |
| lossrate | Float | Packet loss rate. |

## MediaMetric.RemoteDownloadStats

The remote download statistics object.

| Property | Data type | Description |
| --- | --- | --- |
| uid | String | User ID. |
| audioPacketsReceived | Long | Audio packets received. |
| videoPacketsReceived | Long | Video packets received (including retransmitted packets). |
| packetsLost | Long | Packets lost. |
| retransmittedPackets | Long | Retransmitted packets (video). |
| lossrate | Float | Packet loss rate. |
| audioBitrate | Float | Audio bitrate (kb/s). |
| videoBitrate | Float | Video bitrate (kb/s). |

## MediaMetric.AudioSenderStats

The audio sender statistics object.

| Property | Data type | Description |
| --- | --- | --- |
| audioLevel | Float | Audio energy. |
| trackId | String | Track ID. |
| packetsSent | Long | Packets sent. |
| byteSent | Long | Bytes sent. |
| bitrateSent | Float | Send bitrate (kb/s). |
| jitter | Float | Network jitter. |
| packetsLost | Int | Packets lost (retransmissions not deducted). |
| roundTripTime | Float | Round-trip time. |
| mimeType | String | Codec type. |
| timestamp | Long | Timestamp (ms). |
| type | String | Media type, always `audio`. |

## MediaMetric.VideoSenderStats

The video sender statistics object.

| Property | Data type | Description |
| --- | --- | --- |
| firCount | Long | Number of requests to send an I-frame. |
| pliCount | Long | Number of PLI (Picture Loss Indication) requests, i.e., keyframe requests. |
| nackCount | Long | Number of requests to retransmit lost RTP packets. |
| rid | String | Simulcast stream identifier. |
| frameWidth | Int | Video frame width. |
| frameHeight | Int | Video frame height. |
| framesPerSecond | Float | Video frame rate (fps). |
| frameSent | Long | Frames sent. |
| qualityLimitationReason | String | The main reason quality is limited (such as none/cpu/bandwidth/other/inactive). |
| qualityLimitationDurations | `Map<String, Float>` | Cumulative duration of each limitation reason (seconds). |
| qualityLImitationResolutionChange | Long | Number of resolution changes caused by quality limitation. |
| retransmittedPacketsSent | Long | RTP packets retransmitted. |
| targetBitrate | Float | Encoder target bitrate (bps). |
| trackId | String | Track ID. |
| packetsSent | Long | Packets sent. |
| byteSent | Long | Bytes sent. |
| bitrateSent | Float | Send bitrate (kb/s). |
| jitter | Float | Network jitter. |
| packetsLost | Int | Packets lost (retransmissions not deducted). |
| roundTripTime | Float | Round-trip time. |
| mimeType | String | Codec type. |
| timestamp | Long | Timestamp (ms). |
| type | String | Media type, always `video`. |

## MediaMetric.AudioReceiverStats

The audio receiver statistics object.

| Property | Data type | Description |
| --- | --- | --- |
| audioLevel | Float | Audio energy. |
| concealedSamples | Long | Total audio samples recovered by concealment. |
| concealEvents | Long | Number of interpolation operations. |
| silentConcealedSamples | Long | Number of samples concealed as silence. |
| silentConcealmentEvents | Long | Number of silent concealment events. |
| totalAudioEnergy | Double | Cumulative received audio energy. |
| totalSamplesDuration | Double | Cumulative playback duration (seconds). |
| trackId | String | Track ID. |
| packetsReceived | Long | Packets received. |
| bytesReceived | Long | Bytes received. |
| bitrateReceived | Float | Receive bitrate (kb/s). |
| jitter | Float | Network jitter. |
| jitterBufferDelay | Float | Cumulative jitter buffer delay. |
| packetsLost | Int | Packets lost (retransmissions not deducted). |
| mimeType | String | Codec type. |
| timestamp | Long | Timestamp (ms). |
| type | String | Media type, always `audio`. |

## MediaMetric.VideoReceiverStats

The video receiver statistics object.

| Property | Data type | Description |
| --- | --- | --- |
| framesDecoded | Long | Frames decoded successfully. |
| framesDropped | Long | Frames dropped during decoding. |
| framesReceived | Long | Total frames received. |
| framesPerSecond | Float | Receive frame rate (fps). |
| frameWidth | Int | Received frame width. |
| frameHeight | Int | Received frame height. |
| firCount | Int | Number of requests to send an I-frame. |
| pliCount | Int | Number of PLI (Picture Loss Indication) requests, i.e., keyframe requests. |
| nackCount | Int | Number of requests to retransmit lost RTP packets. |
| retransmittedPacketsReceived | Long | Retransmitted packets counted by the receiver. |
| decoderImplementation | String | Decoder implementation name. |
| trackId | String | Track ID. |
| packetsReceived | Long | Packets received. |
| bytesReceived | Long | Bytes received. |
| bitrateReceived | Float | Receive bitrate (kb/s). |
| jitter | Float | Network jitter. |
| jitterBufferDelay | Float | Cumulative jitter buffer delay. |
| packetsLost | Int | Packets lost (retransmissions not deducted). |
| mimeType | String | Codec type. |
| timestamp | Long | Timestamp (ms). |
| type | String | Media type, always `video`. |
