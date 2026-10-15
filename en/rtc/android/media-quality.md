---
title: "Media quality"
description: "Data models and units for Android SRTC local quality snapshots, on-demand MediaMetric queries, and FY server reports."
---

This page documents the public monitoring models in `cn.seastart.rtc.monitoring.api`. For callbacks and queries, see [Network quality](/en/rtc/android/network-quality). The old nested types under `cn.seastart.rtc.statistics.MediaMetric` and the `onMediaMetric` callback have been removed. Migrate to the top-level types here, `onLocalQualitySnapshot`, and `getMetric()`.

## LocalQualitySnapshot

| Field | Type | Description |
| --- | --- | --- |
| `timestamp` | `Long` | Wall-clock time when the underlying sample completed, in milliseconds. |
| `networkQuality` | `NetworkQuality` | Local uplink and downlink network quality. |
| `mediaPlaybackExperience` | `MediaPlaybackExperience` | Continuity of audio and video received locally. |

Both child objects must have a `timestamp` equal to the outer timestamp. The snapshot does not contain raw per-track counters; call `getMetric()` for detailed statistics.

### NetworkQuality, DirectionQuality, and TrackQuality

`NetworkQuality` contains `timestamp`, `uplink: DirectionQuality`, `downlink: DirectionQuality`, `localTracks: List<TrackQuality>`, and `remoteTracks: List<TrackQuality>`. Lists are empty when no corresponding tracks exist.

| Model | Fields | Description |
| --- | --- | --- |
| `DirectionQuality` | `level: QualityLevel` | Worst evaluable track level for the direction; `UNKNOWN` with insufficient samples. |
| `DirectionQuality` | `constraint: QualityConstraint?` | Uplink video limitation; `NONE` when inapplicable to downlink, `null` when a needed reason is unavailable. |
| `DirectionQuality` | `lossRate: Float?`, `rttMs: Float?`, `jitterMs: Float?` | Maximum available per-track window loss rate (0–1), path RTT, and jitter (ms). |
| `TrackQuality` | `key: UserTrackDesc`, `kind: TrackKind`, `direction: QualityDirection` | User track, audio/video kind, and traffic direction. |
| `TrackQuality` | `level: QualityLevel`, `score: Float?`, `constraint: QualityConstraint?` | Per-track network level, 0–100 score, and uplink video limitation. `score` is `null` when unavailable. |
| `TrackQuality` | `lossRate: Float?`, `bitrateBps: Float?`, `rttMs: Float?`, `jitterMs: Float?` | Window loss rate (0–1), actual bitrate (bps), RTT, and jitter (ms). |

`QualityLevel` is `UNKNOWN`, `EXCELLENT`, `GOOD`, `POOR`, `BAD`, or `LOST`; `QualityConstraint` is `NONE`, `CPU`, or `BANDWIDTH`. `QualityDirection` is `UPLINK` or `DOWNLINK`. `UNKNOWN` means there is no reliable assessment; `LOST` only means ICE for an expected media track reached `FAILED`. See [Enums](/en/rtc/android/enums) for more.

### MediaPlaybackExperience

`MediaPlaybackExperience` contains `timestamp`, `videoTracks: List<VideoTrackPlaybackExperience>`, and `audioTracks: List<AudioTrackPlaybackExperience>`. It describes only **downlink** playback continuity on this device.

| Model | Fields | Description |
| --- | --- | --- |
| `VideoTrackPlaybackExperience` | `key: UserTrackDesc`, `level: VideoPlaybackLevel` | Video track and `UNKNOWN` / `SMOOTH` / `DEGRADED` / `FROZEN` level. |
| `VideoTrackPlaybackExperience` | `dropRatio: Float?`, `currentBlockDurationMs: Long?`, `blockRate10s: Float?` | Window drop ratio (0–1), current uninterrupted stall (ms), and stalled-time ratio over the last 10 seconds (0–1). |
| `AudioTrackPlaybackExperience` | `key: UserTrackDesc`, `level: AudioPlaybackLevel` | Audio track and `UNKNOWN` / `CLEAR` / `DEGRADED` / `INTERRUPTED` level. |
| `AudioTrackPlaybackExperience` | `concealmentRatio: Float?`, `silentConcealmentRatio: Float?` | Concealed and silent-concealed samples divided by received samples in the window (0–1). |
| `AudioTrackPlaybackExperience` | `averageJitterBufferDelayMs: Float?`, `currentInterruptionDurationMs: Long?` | Average jitter-buffer output delay and current uninterrupted interruption, in ms. |

## MediaMetric

`RTCEngine.getMetric()` returns `MediaMetric?` for the default channel; `RTCChannel.getMetric()` returns `MediaMetric?` for a specified channel. The result copies the latest completed sample and is `null` when unavailable. This detailed model contains no network or playback levels.

| Field | Type | Description |
| --- | --- | --- |
| `channel` | `String` | Channel that produced the sample. |
| `sampleTimestampMs` | `Long` | Sample completion wall-clock time; matches the snapshot from the same frame. |
| `localAudios` | `MutableMap<UserTrackDesc, AudioSenderStats>` | Statistics for identified local audio sending tracks. |
| `localVideos` | `MutableMap<UserTrackDesc, VideoSenderStats>` | Statistics for identified local video sending tracks. |
| `remoteAudios` | `MutableMap<UserTrackDesc, AudioReceiverStats>` | Statistics for identified remote audio receiving tracks. |
| `remoteVideos` | `MutableMap<UserTrackDesc, VideoReceiverStats>` | Statistics for identified remote video receiving tracks. |
| `localUploadStats` | `LocalUploadStats` | Combined local audio/video window bitrate. |
| `remoteDownloadStats` | `MutableMap<String, RemoteDownloadStats>` | Statistics grouped by remote `uid`. |
| `networkStats` | `NetworkStats` | Overall uplink and downlink statistics. |
| `qualityReport` | `ServerQualityReport?` | FY server report; `null` for WS or before a report exists. |

### Detailed statistics fields and units

| Model | Fields | Interpretation |
| --- | --- | --- |
| `SenderStats` | `trackId`, `packetsSent`, `byteSent`, `bitrateSent`, `jitter`, `packetsLost`, `roundTripTime`, `mimeType`, `timestamp` | Packet and byte counts are cumulative; window bitrate is bps; jitter and RTT are ms; the per-track timestamp comes from RTCStats in ms. |
| `ReceiverStats` | `trackId`, `packetsReceived`, `bytesReceived`, `bitrateReceived`, `jitter`, `packetsLost`, `mimeType`, `timestamp` | Packet and byte counts are cumulative; window bitrate is bps; jitter is ms. |
| `AudioSenderStats` | `audioLevel` | Level is approximately -60 to 0 dBFS; also includes `SenderStats` fields. |
| `VideoSenderStats` | `firCount`, `pliCount`, `nackCount`, `rid`, `frameWidth`, `frameHeight`, `framesPerSecond`, `frameSent`, `qualityLimitationReason`, `qualityLimitationDurationsSeconds`, `qualityLImitationResolutionChange`, `retransmittedPacketsSent`, `targetBitrate`, `maxBitrate` | Also includes `SenderStats` fields; frame rate is fps, target and maximum bitrates are bps; limitation durations are cumulative seconds; `maxBitrate=0` means not configured. |
| `AudioReceiverStats` | `audioLevel`, `totalSamplesReceived`, `concealedSamples`, `concealEvents`, `silentConcealedSamples`, `silentConcealmentEvents`, `generatedNoiseSamples`, `interruptionCount`, `totalInterruptionDurationSeconds`, `totalAudioEnergy`, `totalSamplesDurationSeconds`, `jitterBufferDelaySeconds`, `jitterBufferEmittedCount` | Also includes `ReceiverStats` fields; duration fields are cumulative seconds, and sample and event fields are cumulative counts. |
| `VideoReceiverStats` | `framesDecoded`, `framesRendered`, `framesDropped`, `framesReceived`, `jitterBufferDelaySeconds`, `framesPerSecond`, `frameWidth`, `frameHeight`, `firCount`, `pliCount`, `nackCount`, `retransmittedPacketsReceived`, `decoderImplementation`, `freezeCount`, `totalFreezesDurationSeconds` | Also includes `ReceiverStats` fields; frame and event fields are cumulative counts, and freeze and buffer durations are cumulative seconds. |
| `LocalUploadStats` | `uid`, `videoBitrate`, `audioBitrate` | Window bitrates summed over local sending tracks, in bps. |
| `RemoteDownloadStats` | `uid`, `audioPacketsReceived`, `videoPacketsReceived`, `packetsLost`, `retransmittedPackets`, `lossrate`, `audioBitrate`, `videoBitrate` | Grouped by remote user; counts are cumulative, `lossrate` is a 0–1 window ratio, and bitrates are bps. |
| `NetworkStats` | `bitrateUp`, `bitrateDown`, `lossrateUp`, `lossrateDown`, `rttUpMs`, `rttDownMs`, `pktUp`, `pktDown`, `pktLossUp`, `pktLossDown` | Bitrates use bps; loss rates are 0–1 window ratios; RTT uses ms; packet counts are cumulative. |

Nonexistent tracks do not appear in a map. Some totals are `0` when no corresponding tracks exist. When a track exists but raw counters or a valid window are missing, the affected measurement is `null`, not a measured zero. If any track contributing to an aggregate lacks a needed value, that aggregate is `null`. Detailed direction loss rates use combined packet counts; snapshot direction `lossRate` uses the maximum available per-track window rate, so the two may differ. Do not treat per-track `timestamp` and `sampleTimestampMs` as the same clock.

## ServerQualityReport and NetworkQualityChange

FY `ServerQualityReport` contains `timestamp`, `uplink: ServerQualityStats`, and `downlink: ServerQualityStats`. Each `ServerQualityStats` contains `score` (0–100), `level` (`excellent` / `good` / `poor` / `lost`), `mos`, `loss` (0–1), `rtt` (ms), `jitter` (ms), `packets`, `bitrate` (kbps), and `bytes`. Server values follow the backend contract; local-statistics unit conversions do not apply.

`NetworkQualityChange` contains `direction: QualityDirection`, `previousLevel: String`, `currentLevel: String`, `trend: QualityTrend`, and `report: ServerQualityReport`. Only FY server reports drive it; it is independent of local `LocalQualitySnapshot` evaluation.
