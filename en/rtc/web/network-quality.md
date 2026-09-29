---
title: "Network quality"
description: "Monitor network quality in the Web SDK: quality events, getConnectionQuality, getNetworkStats, getStreamMetric, per-track WebRTC stats, and a poor-network playbook with degradationPreference. Read when building a network indicator or handling poor networks."
---

The SDK provides three ways to get network quality, from coarse to fine:

| Method | Returns | When to use |
|---|---|---|
| `srtc.getConnectionQuality()` | `QualityEvaluation` | You only want to know "is the network good" and get the level/MOS |
| `srtc.getNetworkStats()` | `NetworkStats` | You only care about the overall network: bitrate, packet loss, RTT, available bandwidth |
| `srtc.getStreamMetric()` | `StreamMetric` | You need detailed statistics for each track |

The SDK also fires events proactively when connection quality changes or when CPU/bandwidth is constrained, so your app can subscribe passively instead of polling.

## 1. Subscribe to events (recommended)

Connection quality events reuse the existing `ChannelEvent` system; handle them directly in `onNotifyChannelEvent`:

```typescript
import { ChannelEventType } from '@seastart/srtc-web-sdk';
import type { ConnectionQualityEventData } from '@seastart/srtc-web-sdk';

srtc.onNotifyChannelEvent = (evt) => {
  switch (evt.type) {
    case ChannelEventType.CONNECTION_QUALITY_CHANGED: {
      // Fired when the network level changes (excellent/good/poor/lost/unknown)
      const { evaluation, previous } = evt.data as ConnectionQualityEventData;
      console.log(`Network quality: ${previous} -> ${evaluation.overall}`);
      console.log(`Reasons:`, evaluation.reasons);
      console.log(`MOS:`, evaluation.mos);
      break;
    }
    case ChannelEventType.CPU_CONSTRAINED:
      // The sender is persistently CPU-limited; consider lowering quality/resolution
      toast('CPU overloaded, consider lowering video quality');
      break;
    case ChannelEventType.BANDWIDTH_CONSTRAINED:
      // The sender is persistently bandwidth-limited
      toast('Insufficient uplink bandwidth');
      break;
  }
};
```

## 2. Query on demand

### 2.1 Connection quality evaluation `getConnectionQuality`

```typescript
const q = srtc.getConnectionQuality();
// => QualityEvaluation
```

```typescript
/** Connection quality level (aligned with the industry-standard 5 levels) */
export enum ConnectionQuality {
  /** Initial placeholder, used when there aren't enough samples, to avoid false alarms */
  Unknown = 'unknown',
  /** Excellent */
  Excellent = 'excellent',
  /** Good */
  Good = 'good',
  /** Poor */
  Poor = 'poor',
  /** Connection lost, media can't be transmitted; should trigger reconnection */
  Lost = 'lost',
}

export interface QualityEvaluation {
  /** Uplink quality */
  uplink: ConnectionQuality;
  /** Downlink quality */
  downlink: ConnectionQuality;
  /** Overall quality, the worse of uplink and downlink */
  overall: ConnectionQuality;
  /** Estimated audio/video MOS, 1.0 to 4.5 */
  mos: number;
  /** Main reasons for the current level, for troubleshooting */
  reasons: string[];
  /** Sample timestamp */
  timestamp: number;
}
```

The SDK evaluates over a 2-second sliding window, scoring across multiple metrics: packet loss rate, RTT, jitter, video freezes, uplink bandwidth pressure, `qualityLimitationReason`, and more.

### 2.2 Overall network statistics `getNetworkStats`

```typescript
const net = srtc.getNetworkStats();
// => NetworkStats
```

```typescript
/** Overall network statistics */
export interface NetworkStats {
  /** Downlink bitrate, kb/s */
  bitrate_down: number;
  /** Uplink bitrate, kb/s */
  bitrate_up: number;
  /** Downlink packet loss rate, % */
  lossrate_down: number;
  /** Uplink packet loss rate, % */
  lossrate_up: number;
  /** Uplink packet count */
  pkt_up: number;
  /** Downlink packet count */
  pkt_down: number;
  /** Uplink lost packet count */
  pkt_loss_up: number;
  /** Downlink lost packet count */
  pkt_loss_down: number;
  /** Available uplink bandwidth estimated by BWE, kb/s (from candidate-pair) */
  available_outgoing_bitrate?: number;
  /** Available downlink bandwidth estimated by SFU/BWE, kb/s (from candidate-pair) */
  available_incoming_bitrate?: number;
  /** RTT observed on the publish connection, in ms */
  rtt_up?: number;
  /** RTT observed on the subscribe connection, in ms */
  rtt_down?: number;
}
```

:::note
The `delay` and `up_level` fields from older versions have been removed: `delay` is now split into the more precise `rtt_up` and `rtt_down`, and `up_level` is replaced by `QualityEvaluation.uplink` returned by `getConnectionQuality()`.
:::

### 2.3 Full metric snapshot `getStreamMetric`

```typescript
const metric = srtc.getStreamMetric();
// => StreamMetric
```

```typescript
/** Metric snapshot output periodically by the media streaming engine */
export interface StreamMetric {
  /** Overall network statistics */
  network: NetworkStats;
  /** Locally published audio tracks */
  local_audios: TrackMetric[];
  /** Locally published video tracks */
  local_videos: TrackMetric[];
  /** Subscribed remote audio tracks */
  remote_audios: TrackMetric[];
  /** Subscribed remote video tracks */
  remote_videos: TrackMetric[];
}

/** Real-time metric snapshot of a single track */
export interface TrackMetric {
  /** Real-time bitrate, kb/s */
  bitrate?: number;
  /** Audio level, dBFS */
  db?: number;
  /** Video width */
  width?: number;
  /** Video height */
  height?: number;
  /** Real-time frame rate */
  fps?: number;
  /** Raw sender/receiver stats */
  stats?: AudioSenderStats | VideoSenderStats | AudioReceiverStats | VideoReceiverStats;
  /** uid of the user who owns the track (subscriber side) */
  uid?: string;
  /** Other fields expanded from track.getInfo() */
  [key: string]: any;
}
```

## 3. Track-level raw statistics

The `stats` field of each track in `StreamMetric` corresponds to WebRTC's native sender/receiver stats:

```typescript
/** Sending statistics */
interface SenderStats {
  /** Packets sent */
  packetsSent?: number;
  /** Bytes sent */
  bytesSent?: number;
  /** Network jitter perceived by the remote side, in ms */
  jitter?: number;
  /** Packets lost as reported by the remote side */
  packetsLost?: number;
  /** Round-trip time reported by the remote side, in ms */
  roundTripTime?: number;
  /** Outbound stream ID */
  streamId?: string;
  /** Timestamp */
  timestamp: number;
}

export interface AudioSenderStats extends SenderStats {
  type: 'audio';
  /** Audio level */
  audioLevel?: number;
}

export interface VideoSenderStats extends SenderStats {
  type: 'video';
  /** Number of FIR requests received */
  firCount: number;
  /** Number of PLI requests received */
  pliCount: number;
  /** Number of NACK requests received */
  nackCount: number;
  /** RTP stream ID */
  rid: string;
  /** Frame width */
  frameWidth: number;
  /** Frame height */
  frameHeight: number;
  /** Frame rate */
  framesPerSecond: number;
  /** Frames sent */
  framesSent: number;
  /** Quality limitation reason (bandwidth/cpu/other/none) */
  qualityLimitationReason?: string;
  /** Quality limitation durations */
  qualityLimitationDurations?: Record<string, number>;
  /** Number of resolution changes caused by quality limitation */
  qualityLimitationResolutionChanges?: number;
  /** Retransmitted packets */
  retransmittedPacketsSent?: number;
  /** Target bitrate */
  targetBitrate: number;
}

/** Receiving statistics */
interface ReceiverStats {
  /** Cumulative receiver jitter buffer delay (sum of delays of all frames emitted from the buffer since playback started), in ms */
  jitterBufferDelay?: number;
  /** Cumulative number of frames/samples emitted from the jitter buffer; used to convert the cumulative jitterBufferDelay into an average */
  jitterBufferEmittedCount?: number;
  /** Average per-frame jitter buffer delay within the period (since the previous stats sample), in ms; use this for perceived latency */
  jitterBufferAvgDelay?: number;
  /** Cumulative packets lost (based on RTP sequence number gaps) */
  packetsLost?: number;
  /** Cumulative RTP packets received */
  packetsReceived?: number;
  /** Cumulative bytes received (including RTP headers) */
  bytesReceived?: number;
  /** Media stream identifier (usually corresponds to the remote SSRC) */
  streamId?: string;
  /** Network-layer RTP jitter (as defined in RFC 3550), in ms */
  jitter?: number;
  /** Collection timestamp of this set of stats, in ms */
  timestamp: number;
}

export interface AudioReceiverStats extends ReceiverStats {
  type: 'audio';
  /** Audio level */
  audioLevel?: number;
  /** Concealed samples */
  concealedSamples?: number;
  /** Concealment events */
  concealmentEvents?: number;
  /** Silent concealed samples */
  silentConcealedSamples?: number;
  /** Silent concealment events */
  silentConcealmentEvents?: number;
  /** Total audio energy */
  totalAudioEnergy?: number;
  /** Total samples duration */
  totalSamplesDuration?: number;
}

export interface VideoReceiverStats extends ReceiverStats {
  type: 'video';
  /** Frames decoded */
  framesDecoded: number;
  /** Frames dropped */
  framesDropped: number;
  /** Frames received */
  framesReceived: number;
  /** Frame rate */
  framesPerSecond?: number;
  /** Frame width */
  frameWidth?: number;
  /** Frame height */
  frameHeight?: number;
  /** Number of FIR requests sent */
  firCount?: number;
  /** Number of PLI requests sent */
  pliCount?: number;
  /** Number of NACK requests sent */
  nackCount?: number;
  /** Decoder implementation */
  decoderImplementation?: string;
  /** MIME type */
  mimeType?: string;
  /** Video freeze count (a single freeze > 1 s or > 3x the average frame interval, per the W3C definition) */
  freezeCount?: number;
  /** Cumulative video freeze duration (s) */
  totalFreezesDuration?: number;
  /** Video pause count (remote side paused sending) */
  pauseCount?: number;
  /** Cumulative video pause duration (s) */
  totalPausesDuration?: number;
  /** Frames assembled from multiple RTP packets */
  framesAssembledFromMultiplePackets?: number;
  /** Cumulative assembly time of all frames (s) */
  totalAssemblyTime?: number;
}
```

## 4. Recommended integration

Most apps only need to show a "network status indicator". The recommended combination:

```typescript
// 1. Subscribe to level changes for UI hints
srtc.onNotifyChannelEvent = (evt) => {
  if (evt.type === ChannelEventType.CONNECTION_QUALITY_CHANGED) {
    const { evaluation } = evt.data as ConnectionQualityEventData;
    updateNetworkIndicator(evaluation.overall); // Your UI update function
  }
};

// 2. When you need a detailed data panel, call getStreamMetric on demand
setInterval(() => {
  const metric = srtc.getStreamMetric();
  if (metric) renderDashboard(metric);
}, 2000);
```

## 5. Handling poor networks

To handle a poor network, first distinguish two things: **direction** and **cause**.

+ A poor uplink means you can't send, and you can degrade proactively (lower bitrate, switch to the low stream, turn off the camera); a poor downlink means you can't receive, and all you can do is receive less (switch to the low stream, unsubscribe from video). So look at both the `uplink` and `downlink` directions, not just `overall`.
+ `BANDWIDTH_CONSTRAINED` means insufficient bandwidth, and `CPU_CONSTRAINED` means the device's encoder can't keep up; they call for different handling.

### 5.1 Show network status

Mapping `overall` to a status indicator is enough. Don't show raw data such as packet loss rate or RTT to end users:

| overall | Status |
| --- | --- |
| excellent / good | Normal |
| poor | Poor, video quality may drop |
| lost | Disconnected, reconnecting |
| unknown | Sampling |

Uplink and downlink problems need different hint messages:

```typescript
const q = srtc.getConnectionQuality();
if (q.uplink === ConnectionQuality.Poor) {
  showTip('Your network is poor; others may not see you clearly');
} else if (q.downlink === ConnectionQuality.Poor) {
  showTip('Poor network, optimizing video quality');
}
```

Debounce the hints: toast only after `poor` persists for a few seconds, not on every fluctuation. The SDK already debounces the `BANDWIDTH_CONSTRAINED` / `CPU_CONSTRAINED` events; we recommend rate-limiting your popups once more in your app.

### 5.2 Uplink degrades

Degrade step by step, from light to heavy:

1. **Encoder adaptation**: done automatically by the browser, on by default, no action needed. If you don't want the resolution to be lowered automatically, change the degradation mode with `degradationPreference` (see 5.4).
2. **Switch to the low stream / lower resolution**: if you publish simulcast, you can switch to the low stream (320×180, about 250 Kbps). See [Simulcast and resolution](/en/rtc/web/advanced/video-stream-layers).
3. **Turn off the camera, keep audio only**: audio bitrate is low (about 32 Kbps) and can almost always be kept on a poor network.

```typescript
srtc.disableLocalTrack(localVideoTrack);  // Disable (lightweight, keeps the publishing path, can be restored at any time)
srtc.enableLocalTrack(localVideoTrack);   // Re-enable after the network recovers
```

4. **Stop publishing entirely**: `unpublishLocalTrack(localVideoTrack)` is more thorough than turning off the camera and releases uplink encoding and sending resources.

On `CPU_CONSTRAINED`, prefer lowering resolution / frame rate (to reduce encoding load); on `BANDWIDTH_CONSTRAINED`, lowering either bitrate or resolution works.

Turning off the camera changes the shape of the call, so we recommend notifying the user before doing it rather than doing it silently—especially in scenarios such as emergency command and law enforcement recording.

### 5.3 Downlink degrades

1. **First check whether the problem is on the remote side**: only if you have downlink packet loss is your receiving path poor. If you have almost no packet loss and just one person's video is freezing, it's usually that person's uplink; unsubscribing won't help, so just show "the other party's network is poor". The SDK's scoring already distinguishes these two cases and won't lower your downlink level because of someone else's problem.
2. **When the publisher sends simulcast, the SFU switches layers automatically**: based on each subscriber's own downlink bandwidth and packet loss, the SFU automatically switches it to the appropriate high / low stream, with no manual switching on the subscriber side; if only a single stream is published, it can't degrade automatically. See [Simulcast and resolution](/en/rtc/web/advanced/video-stream-layers).
3. **Unsubscribe from video, receive audio only**:

```typescript
await srtc.unsubscribeRemoteTrack(remoteVideoTrack);
```

4. **Multi-party calls**: subscribe only to the current speaker's video, and receive audio only from everyone else.

### 5.4 Control the degradation mode: `degradationPreference`

`VideoPublishOptions.degradationPreference` of `publishLocalTrack` decides what to sacrifice on a poor network:

| Value | Behavior | Use for |
| --- | --- | --- |
| `maintain-framerate` | Lower resolution, keep frame rate | General real-time interaction, motion video |
| `maintain-resolution` | Lower frame rate, keep resolution | Screen sharing, documents / slides, where resolution shouldn't change |
| `balanced` | Lower both | A compromise |

If you don't want the resolution to be lowered automatically, set it to `maintain-resolution`:

```typescript
await srtc.publishLocalTrack(localVideoTrack, {
  degradationPreference: 'maintain-resolution',
});
```

Among the built-in presets, camera 720p / 1080p and all screen sharing presets default to `maintain-resolution`; 360p / 180p don't set it and use the browser default.

### 5.5 Connection lost (`lost`)

`overall === 'lost'` means media is interrupted. Start reconnecting and show the user "Reconnecting"; after recovery, refresh the status indicator and restore any camera or subscriptions you turned off earlier.

### 5.6 Quick reference

| Signal | Action |
| --- | --- |
| `BANDWIDTH_CONSTRAINED` (uplink) | Switch to the low stream → turn off the camera, keep audio; set `maintain-resolution` if you don't want resolution lowered |
| `CPU_CONSTRAINED` (uplink) | Lower resolution / frame rate |
| `uplink = poor / lost` | Degrade as in 5.2, show "your network" |
| `downlink = poor` (local packet loss) | Unsubscribe from video, keep audio / keep only the main speaker in multi-party calls |
| `downlink = poor` (no local packet loss) | Show "the other party's network is poor" |
| `overall = lost` | Reconnect, refresh the status after recovery |

### 5.7 Complete example

Putting it all together: configure the degradation strategy when publishing, and at runtime subscribe to events to update the status indicator, show direction-specific hints, and degrade and restore as needed.

```typescript
import { ChannelEventType, ConnectionQuality } from '@seastart/srtc-web-sdk';
import type { ConnectionQualityEventData, LocalVideoTrack } from '@seastart/srtc-web-sdk';

// Assume a local camera track has already been created and is held here
let cameraTrack: LocalVideoTrack;
// Marks whether the camera was turned off because of a poor network, so it can be turned back on automatically after recovery
let cameraOffByNetwork = false;

// Publish: enable simulcast (the remote side can drop to the low stream automatically on a poor network); if sharing documents/slides, use maintain-resolution to keep it sharp
await srtc.publishLocalTrack(cameraTrack, {
  degradationPreference: 'maintain-framerate', // Use this for general interaction; change to 'maintain-resolution' for document sharing
});

// Simple debounce: show the same kind of hint at most once every N seconds
const lastToast: Record<string, number> = {};
function toastOnce(key: string, msg: string, intervalMs = 8000) {
  const now = Date.now();
  if (now - (lastToast[key] ?? 0) < intervalMs) return;
  lastToast[key] = now;
  toast(msg); // Replace with your toast implementation
}

srtc.onNotifyChannelEvent = (evt) => {
  switch (evt.type) {
    // 1) Network level changed: update the indicator + direction-specific hints + reconnection + recovery
    case ChannelEventType.CONNECTION_QUALITY_CHANGED: {
      const { evaluation } = evt.data as ConnectionQualityEventData;
      updateNetworkIndicator(evaluation.overall); // Your status indicator

      if (evaluation.overall === ConnectionQuality.Lost) {
        showReconnecting(); // Show "Reconnecting"
      } else if (evaluation.uplink === ConnectionQuality.Poor) {
        toastOnce('uplink', 'Your network is poor; others may not see you clearly');
      } else if (evaluation.downlink === ConnectionQuality.Poor) {
        toastOnce('downlink', 'Poor network, optimizing video quality');
        // When the downlink is poor, the SFU automatically drops you to the low stream, which usually resolves it; generally no action is needed.
        // For an "audio only" fallback: if the downlink stays poor for a long time, ask the user to confirm first,
        // then call srtc.unsubscribeRemoteTrack(videoTrack) on the currently subscribed remote video tracks to unsubscribe, keeping only audio.
      }

      // Network recovered and the camera was turned off earlier because of the poor network → turn it back on automatically
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

    // 2) Insufficient uplink bandwidth: notify the user and offer a one-click "turn off camera, keep audio" action (not done silently)
    case ChannelEventType.BANDWIDTH_CONSTRAINED:
      toastOnce('bw', 'Insufficient uplink bandwidth; turn off the camera to keep the voice call');
      showDowngradeButton(() => {
        srtc.disableLocalTrack(cameraTrack); // Turn off the camera, keep audio
        cameraOffByNetwork = true;
      });
      break;

    // 3) The device's encoder can't keep up: suggest lowering quality / closing other apps
    case ChannelEventType.CPU_CONSTRAINED:
      toastOnce('cpu', 'Device busy; close other apps or lower video quality');
      break;
  }
};
```

> `publishLocalTrack` / `disableLocalTrack` / `enableLocalTrack` in the example are all existing SDK methods. Operations that change the shape of the call, such as turning off the camera, are handed to the user for confirmation via a button rather than done silently; for regular calls and similar scenarios you can make them automatic. Implement the downlink "audio only" fallback yourself following the idea in the comments (use `unsubscribeRemoteTrack` to unsubscribe from video and keep audio).
