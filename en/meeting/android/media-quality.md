---
title: "Media quality"
description: "Monitor current-meeting audio and video quality through SMeeting Android local quality snapshots, on-demand detailed statistics, and FY server reports."
---

SMeeting 2.0.40 uses the monitoring models in `cn.seastart.rtc.monitoring.api` from SRTC 2.0.37. The old nested types under `cn.seastart.rtc.statistics.MediaMetric` and `onMediaMetric()` have been removed. See [SRTC media quality](/en/rtc/android/media-quality) for all fields and units.

## Get quality data

| Entry point | Data | When to use it |
| --- | --- | --- |
| `MeetingMediaEvent.onLocalQualitySnapshot(snapshot)` | `LocalQualitySnapshot`, local uplink and downlink network quality and remote audio/video playback experience from the same sample | Show network and playback quality periodically; the callback stays on the RTC statistics thread, so switch threads before updating the UI |
| `MeetingEngine.getMetric()` | `MediaMetric?`, a copy of the latest completed detailed sample for the current meeting channel | Read per-track bitrate, frame rate, loss, and network data on demand; it does not trigger an immediate underlying statistics sample |
| `MeetingMediaEvent.onNetworkQualityChanged(change)` | FY server `NetworkQualityChange` | Handle server-side uplink and downlink quality levels; it is independent of the local snapshot, and WS does not produce FY reports |

`getMetric()` returns `null` when no meeting is active, no sample has completed, or the media connection is invalid. `onLocalQualitySnapshot()` is delivered about every 2 seconds after sampling completes; query detailed statistics only when needed.

```kotlin
import cn.seastart.meeting.event.MeetingMediaSimpleEvent
import cn.seastart.rtc.monitoring.api.LocalQualitySnapshot
import cn.seastart.rtc.monitoring.api.MediaMetric
import cn.seastart.rtc.monitoring.api.NetworkQualityChange

meetingEngine.mediaEvent = object : MeetingMediaSimpleEvent() {
    override fun onLocalQualitySnapshot(snapshot: LocalQualitySnapshot) {
        val downlinkLevel = snapshot.networkQuality.downlink.level
        // This callback runs on the RTC statistics thread. Switch to the main thread before displaying downlinkLevel.
    }

    override fun onNetworkQualityChanged(change: NetworkQualityChange) {
        // FY server quality report; debounce poor-network prompts in your app.
    }
}

val metric: MediaMetric? = meetingEngine.getMetric()
```

## Local quality snapshot

`LocalQualitySnapshot` contains `timestamp: Long`, `networkQuality: NetworkQuality`, and `mediaPlaybackExperience: MediaPlaybackExperience` from the same sample. Network quality provides levels, loss rates, bitrates, RTT, and jitter by direction and user track. Playback experience provides smoothness or interruption data by remote video and audio track. The snapshot does not contain raw per-track counters; see [SRTC media quality](/en/rtc/android/media-quality) for fields and levels.

## Detailed statistics

The top-level `MediaMetric` returned by `getMetric()` contains `channel`, `sampleTimestampMs`, local sending tracks `localAudios` / `localVideos`, remote receiving tracks `remoteAudios` / `remoteVideos`, aggregates `localUploadStats` / `remoteDownloadStats`, `networkStats`, and the nullable FY server `qualityReport`. Per-track maps use `UserTrackDesc` keys. Bitrates are in bps; loss rates are fractions from 0 to 1. See [SRTC media quality](/en/rtc/android/media-quality) for the full fields and units.

## FY server quality reports

`onNetworkQualityChanged()` fires once for the uplink and once for the downlink for each FY server report, without debouncing. When the level is unchanged, `trend` is `STABLE`. It is independent of the local `LocalQualitySnapshot` evaluation. See [SRTC enums](/en/rtc/android/enums) for directions, levels, and trends, and [SRTC network quality](/en/rtc/android/network-quality) for poor-network handling.
