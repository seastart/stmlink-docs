---
title: "Network quality"
description: "Distinguish FY server quality reports, local network and playback snapshots, and per-track statistics queried on demand."
---

The SDK provides three independent sources of quality information. Every callback includes `channel`; multi-channel apps should store results by channel. Public monitoring types are in `cn.seastart.rtc.monitoring.api`.

| Information | Entry point | Use |
| --- | --- | --- |
| FY server network quality | `RTCMediaEvent.onNetworkQualityChanged(channel, change)` | Each FY server report produces separate uplink and downlink events; WS does not provide this server report. |
| Local network and playback experience | `RTCMediaEvent.onLocalQualitySnapshot(channel, snapshot)` | About every 2 seconds after sampling completes, each channel delivers local uplink and downlink network quality and per-track downlink playback experience. |
| Detailed media statistics | `RTCEngine.getMetric()` / `RTCChannel.getMetric()` | Query the latest completed raw statistics sample for the default or a specified channel on demand. |

Local snapshots and FY server reports have different data sources and quality levels; do not combine their levels. See [Media quality](/en/rtc/android/media-quality) for the detailed models and units.

## Listen for periodic local snapshots

```kotlin
import cn.seastart.rtc.impl.RTCMediaSimpleEvent
import cn.seastart.rtc.monitoring.api.LocalQualitySnapshot

rtcEngine.setRtcMediaEvent(object : RTCMediaSimpleEvent() {
    override fun onLocalQualitySnapshot(channel: String, snapshot: LocalQualitySnapshot) {
        val uplink = snapshot.networkQuality.uplink.level
        val downlink = snapshot.networkQuality.downlink.level
        val affectedTracks = snapshot.networkQuality.remoteTracks
        val videoPlayback = snapshot.mediaPlaybackExperience.videoTracks
        // Route by channel; switch to the main thread before updating UI.
    }
})
```

`snapshot.timestamp`, `snapshot.networkQuality.timestamp`, and `snapshot.mediaPlaybackExperience.timestamp` match and use milliseconds. The interval starts after collection and delivery finish, so delivery is not fixed to an exact 2-second wall-clock schedule. Without valid samples, a network or playback level may be `UNKNOWN` and nullable measurements may be `null`. `NetworkQuality` contains both direction summaries and per-track results. Playback experience describes continuity of media received locally. Poor network quality does not always mean playback stalls, and smooth playback does not measure picture clarity.

Network levels are `UNKNOWN`, `EXCELLENT`, `GOOD`, `POOR`, `BAD`, and `LOST`. `LOST` applies only when ICE for an expected media track reaches `FAILED`; deliberate closure yields `UNKNOWN`. Video playback levels are `UNKNOWN`, `SMOOTH`, `DEGRADED`, and `FROZEN`; audio levels are `UNKNOWN`, `CLEAR`, `DEGRADED`, and `INTERRUPTED`. The per-track network `score` ranges from 0 to 100, is `null` when it cannot be evaluated, and is not a playback score.

## Query detailed statistics on demand

```kotlin
import cn.seastart.rtc.monitoring.api.MediaMetric

val metric: MediaMetric? = rtcEngine.getMetric() // Default channel
val otherMetric: MediaMetric? = rtcChannel.getMetric() // Specified channel
metric?.let { sample ->
    val channel = sample.channel
    val sampledAtMs = sample.sampleTimestampMs
    val localVideos = sample.localVideos
    val remoteVideos = sample.remoteVideos
    val serverReport = sample.qualityReport // Available for FY; null for WS
}
```

The query returns the most recent **completed** sample. It does not trigger another WebRTC `getStats()` call or advance the network or playback evaluation window. It returns `null` before a usable sample exists or after monitoring becomes unavailable; repeated queries of one sample return independent copies. `sampleTimestampMs` is the completion time. If another sample finishes after a snapshot callback, a later query may have a different timestamp. Check both `channel` and timestamp before combining the results. Per-track `timestamp` comes from RTCStats and differs from the top-level wall-clock time.

Detailed bitrates use bps, RTT and jitter use ms, and loss rates range from 0 to 1; packet, byte, and frame counts are cumulative. `null` means unavailable, while a measured zero stays `0`. Some direction totals are `0` when no tracks exist; that does not imply a measured zero for a particular track.

## FY server reports

```kotlin
import cn.seastart.rtc.monitoring.api.NetworkQualityChange

override fun onNetworkQualityChanged(channel: String, change: NetworkQualityChange) {
    val direction = change.direction // UPLINK or DOWNLINK
    val level = change.currentLevel // excellent / good / poor / lost
    val trend = change.trend // INITIAL / DEGRADED / RECOVERED / STABLE
    val report = change.report // ServerQualityReport
}
```

Each FY report triggers one callback for uplink and one for downlink, including `STABLE` when the level is unchanged; the SDK does not apply app-level debouncing. `report` contains server statistics for both directions. `getMetric().qualityReport` also holds a recent FY server report, but it is read when detailed statistics are first assembled for that sample and need not be synchronized exactly with a particular server callback. For WS, `qualityReport` is `null`. Callbacks run on an SDK background thread; switch to the main thread before updating UI.

## Handle poor networks

First identify the affected channel, direction, and track. Use direction levels for status displays, then `remoteTracks`, `localTracks`, and playback lists to locate affected tracks. Apps should choose persistence and recovery conditions for prompts or automatic degradation based on their use case; a single `POOR` or `BAD` sample does not by itself require stopping video. For connection state changes, see [`RTCClientEvent`](/en/rtc/android/api-reference/RTCClientEvent).
