---
title: "Network quality"
description: "Monitor network quality in the Android SRTC SDK: quality level changes via onNetworkQualityChanged, periodic onMediaMetric snapshots, on-demand getMetric(), qualityReport levels, and handling poor uplink/downlink and reconnects. Read when building network indicators or poor-network handling."
---

The SDK offers three ways to get network quality, from "passively reacting to changes" to "actively querying". Pick the one that fits:

| Method | API | Use case |
|---|---|---|
| Subscribe to quality level changes (recommended) | `RTCMediaEvent.onNetworkQualityChanged` | Network status indicators and poor-network prompts; **fires once each for uplink and downlink on every quality report from the server**, with no debouncing |
| Periodic quality snapshots | `RTCMediaEvent.onMediaMetric` | Detailed diagnostic panels; delivers a full `MediaMetric.Metric` about every 5 seconds |
| Actively query a snapshot | `RTCEngine.getMetric()` | Pull the latest full quality snapshot at any time |

`onNetworkQualityChanged` and `onMediaMetric` are delivered passively through `RTCMediaEvent`—just subscribe, no polling needed. `getMetric()` is for pulling on demand.

For the full data dictionary of `Metric` fields, see [Media quality](/en/rtc/android/media-quality).

## 1. Subscribe to quality level changes (recommended)

Most apps only need "a network status indicator + poor-network prompts", so prefer `onNetworkQualityChanged`. It's driven by the server's quality reports (about one every 5 seconds) and **fires on every report**, even when the level hasn't changed:

- **No debouncing**: the SDK doesn't check for tier crossings or apply hysteresis, so when the level hovers around a boundary, the callback results flip back and forth with it. A status indicator can show `currentLevel` directly; for actions that interrupt the user or change the call, such as poor-network prompts and automatic degradation, debounce yourself (see 5.1).
- **`trend` only compares with the previous callback**: `INITIAL` the first time, `DEGRADED` when worse, `RECOVERED` when better, and `STABLE` when unchanged (or when this level can't be recognized).
- **Per direction**: uplink and downlink are evaluated and reported independently; each callback represents **one direction** only (`direction`).

Extend `RTCMediaSimpleEvent`, override only the callbacks you need, and register it with `setRtcMediaEvent`:

```kotlin
import cn.seastart.rtc.impl.RTCMediaSimpleEvent
import cn.seastart.rtc.info.NetworkQualityChange
import cn.seastart.rtc.info.QualityDirection
import cn.seastart.rtc.info.QualityTrend

rtcEngine.setRtcMediaEvent(object : RTCMediaSimpleEvent() {
    override fun onNetworkQualityChanged(channel: String, change: NetworkQualityChange) {
        // change.direction     : UPLINK / DOWNLINK, the direction of this callback
        // change.previousLevel : level in the previous callback
        // change.currentLevel  : current level (excellent / good / poor / lost)
        // change.trend         : INITIAL (first) / DEGRADED (worse) / RECOVERED (better) / STABLE (unchanged)
        // change.report        : the full QualityReport that triggered this callback

        // The callback may run off the main thread; switch to the main thread to update the UI
        runOnUiThread {
            when (change.direction) {
                QualityDirection.UPLINK -> updateUplinkIndicator(change.currentLevel)
                QualityDirection.DOWNLINK -> updateDownlinkIndicator(change.currentLevel)
            }
        }
    }
})
```

:::note
`onNetworkQualityChanged` is called on a background thread of the signaling channel. Switch to the main thread (for example, `runOnUiThread` / `View.post`) before updating the UI.
:::

`NetworkQualityChange` structure:

```kotlin
/** Direction of the change */
enum class QualityDirection {
    /** Uplink: from this client to the server */
    UPLINK,
    /** Downlink: from the server to this client */
    DOWNLINK
}

/** Trend of the change */
enum class QualityTrend {
    /** First level observed for this direction (no history to compare) */
    INITIAL,
    /** Level dropped; the network got worse */
    DEGRADED,
    /** Level rose; the network got better */
    RECOVERED,
    /** Level is the same as last time, or this level can't be recognized */
    STABLE
}

data class NetworkQualityChange(
    /** Direction of this callback */
    var direction: QualityDirection,
    /** Level in the previous callback; an empty string the first time (INITIAL) */
    var previousLevel: String,
    /** Current level: excellent / good / poor / lost */
    var currentLevel: String,
    /** Trend of the change */
    var trend: QualityTrend,
    /** The full quality report that triggered this callback, with uplink and downlink details */
    var report: MediaMetric.QualityReport
)
```

## 2. Periodic quality snapshots with `onMediaMetric`

When you need a detailed diagnostic panel (bitrate, packet loss, frame rate, and so on for each track), subscribe to `onMediaMetric`. After joining a channel, the SDK delivers a full `MediaMetric.Metric` about every **5 seconds**:

```kotlin
import cn.seastart.rtc.impl.RTCMediaSimpleEvent
import cn.seastart.rtc.statistics.MediaMetric

rtcEngine.setRtcMediaEvent(object : RTCMediaSimpleEvent() {
    override fun onMediaMetric(channel: String, metric: MediaMetric.Metric) {
        // Connection quality assessment (same data source as onNetworkQualityChanged)
        metric.qualityReport?.let { report ->
            val up = report.uplink.level     // excellent / good / poor / lost
            val down = report.downlink.level
            renderDashboard(up, down)
        }
        // Overall network statistics
        val net = metric.networkStats
        // Track-level statistics
        val localVideos = metric.localVideos
        val remoteVideos = metric.remoteVideos
    }
})
```

:::note
`qualityReport` is computed and delivered by the server. After you first join a channel, it may be `null` until the server's first quality report arrives; the example handles this with nullable access.
:::

## 3. Actively query with `getMetric`

Pull the most recently collected full quality snapshot (including `qualityReport`) at any time. This suits on-demand cases such as a diagnostic panel that only computes when the user opens the details:

```kotlin
val metric = rtcEngine.getMetric()
metric?.qualityReport?.let { report ->
    // report.uplink.level / report.downlink.level ...
}
```

:::note
Returns a thread-safe copy and doesn't trigger the underlying `getStats`. The sampling period is about 5 seconds, so it may be `null` right after media starts.
:::

## 4. Connection quality assessment with `qualityReport`

All three methods return the same `qualityReport`: the server has already combined packet loss, RTT, jitter, bitrate, and other metrics to compute a level and MOS, so you can use it directly without computing anything yourself. It distinguishes two directions: **uplink** (from this client to the server) and **downlink** (from the server to this client).

```kotlin
data class QualityReport(
    /** Timestamp at which the server generated this quality report */
    var timestamp: Long = 0L,
    /** Uplink quality from this client to the server */
    var uplink: QualityStats = QualityStats(),
    /** Downlink quality from the server to this client */
    var downlink: QualityStats = QualityStats()
)

data class QualityStats(
    /** Overall quality score, 0–100; higher is better */
    var score: Double = 0.0,
    /** Quality level: excellent / good / poor / lost */
    var level: String = "",
    /** Estimated subjective voice quality score, 1.0–4.5; higher is better */
    var mos: Double = 0.0,
    /** Packet loss rate, 0–1 */
    var loss: Double = 0.0,
    /** Round-trip time, in milliseconds */
    var rtt: Double = 0.0,
    /** Jitter, in milliseconds */
    var jitter: Double = 0.0,
    /** Number of packets counted in this round of statistics */
    var packets: Long = 0L,
    /** Average bitrate, in kbps */
    var bitrate: Double = 0.0,
    /** Bytes in this window */
    var bytes: Long = 0L
)
```

`level` values:

| level | Meaning |
|---|---|
| `excellent` | Excellent, nearly lossless |
| `good` | Good, slight packet loss or delay |
| `poor` | Poor, noticeable stuttering and packet loss |
| `lost` | Connection lost; media can't be transmitted |

> `onNetworkQualityChanged`, `onMediaMetric.qualityReport`, and `getMetric().qualityReport` share the same data source—the same quality report delivered by the server. They differ only in how it's delivered (per report / periodically / on demand).

Besides `qualityReport`, `Metric` also contains overall network statistics `networkStats`, uplink/downlink aggregates `localUploadStats` / `remoteDownloadStats`, and track-level statistics `localAudios` / `localVideos` / `remoteAudios` / `remoteVideos`. For all fields, see [Media quality](/en/rtc/android/media-quality).

## 5. Handling poor networks

To handle a poor network, first separate two things: **direction** and **response**.

+ A poor uplink means you can't send; you can proactively degrade (turn off the camera, unpublish video). A poor downlink means you can't receive; the server usually optimizes this automatically, and you can unsubscribe from video if needed. So look at both `uplink` and `downlink`, not just one side.
+ `onNetworkQualityChanged` fires on every quality report, and the SDK doesn't debounce it. A status indicator can simply follow `currentLevel`; for actions like poor-network prompts and degradation, debounce yourself and act only after the network has stayed poor for a while (see 5.1). The same applies if you read `onMediaMetric` periodically.

### 5.1 Show network status

Map the quality level to a status indicator. Don't show raw data like packet loss or RTT to end users:

| level | Status indicator |
|---|---|
| `excellent` / `good` | Normal |
| `poor` | Poor; video quality may drop |
| `lost` | Connection interrupted, reconnecting |

A poor uplink and a poor downlink need different prompt messages. The callback isn't debounced, so when the level hovers around the `good` / `poor` boundary, it keeps reporting a drop. Prompt only after the network has stayed poor beyond a threshold, and only once per poor-network episode:

```kotlin
// When each direction entered poor / lost; no entry means it isn't poor right now
private val badSince = mutableMapOf<QualityDirection, Long>()
// Directions already prompted in this poor-network episode, to avoid repeated interruptions
private val tipped = mutableSetOf<QualityDirection>()

override fun onNetworkQualityChanged(channel: String, change: NetworkQualityChange) {
    val dir = change.direction
    if (!isBad(change.currentLevel)) {
        // Clear after recovery; timing restarts the next time it gets worse
        badSince.remove(dir)
        tipped.remove(dir)
        return
    }
    val since = badSince.getOrPut(dir) { System.currentTimeMillis() }
    // Prompt only after it has stayed poor for more than 10 seconds
    if (System.currentTimeMillis() - since >= 10_000 && tipped.add(dir)) {
        when (dir) {
            QualityDirection.UPLINK -> showTip("Your network is poor; others may not see you clearly")
            QualityDirection.DOWNLINK -> showTip("Poor network; optimizing video quality")
        }
    }
}

private fun isBad(level: String) = level == "poor" || level == "lost"
```

### 5.2 Poor uplink

When the uplink level stays at `poor` / `lost`, degrade step by step from light to heavy:

**1. Turn off the camera and keep only audio.** Audio bitrate is low and almost always survives a poor network. Stopping camera capture significantly reduces uplink usage while keeping the publishing path, so you can restart capture as soon as the network recovers:

```kotlin
// On a poor network: stop camera capture; audio is unaffected
localCameraTrack.stopCapture()

// After the network recovers: restart capture
localCameraTrack.startCapture(object : RTCResultListener {
    override fun onSuccess() {}
    override fun onFail(code: Int) {}
})
```

**2. Unpublish video entirely.** More thorough than turning off the camera; it frees uplink encoding and sending resources:

```kotlin
rtcEngine.unPublishLocalVideo(localVideoTrack, object : RTCResultListener {
    override fun onSuccess() {}
    override fun onFail(code: Int) {}
})
```

Turning off the camera changes the nature of the call, so prompt the user before doing it rather than acting silently—especially in scenarios like emergency command or law enforcement recording.

To further pinpoint why the uplink is limited, read `qualityLimitationReason` on the local video tracks:

```kotlin
rtcEngine.getMetric()?.localVideos?.values?.forEach { stats ->
    when (stats.qualityLimitationReason) {
        "bandwidth" -> { /* Insufficient uplink bandwidth: lower the bitrate / turn off the camera first */ }
        "cpu"       -> { /* The device can't keep up with encoding: lower the resolution / frame rate */ }
    }
}
```

### 5.3 Poor downlink

When the downlink level stays at `poor`:

**1. First check whether the problem is on the other side.** Only if this client has downlink packet loss (`downlink.loss` clearly > 0) is your receiving path poor. If this client has almost no packet loss and only one person's video stutters, it's usually that person's poor uplink; unsubscribing won't help, so just show "The other user's network is poor".

**2. When the publisher sends simulcast, the server switches layers automatically.** Based on each subscriber's own downlink bandwidth and packet loss, the server automatically switches it to the appropriate high or low stream; subscribers don't need to switch manually (when subscribing, the candidate layer list tells the server which layers it can switch to). With a single stream, there's nothing to degrade to automatically.

**3. Unsubscribe from video and receive only audio.**

```kotlin
rtcEngine.unSubscribeRemoteTrack(uid, trackId)
```

**4. Multi-party calls**: subscribe only to the current speaker's video and receive only audio from everyone else. You can get the current speakers from `onActiveSpeakersChanged`:

```kotlin
override fun onActiveSpeakersChanged(channel: String, speakers: List<ActiveSpeakerInfo>) {
    // speakers is the list of users currently speaking; use it to decide whose video to subscribe to
    speakers.forEach { it.uid; it.level }
}
```

### 5.4 Disconnects and reconnects

Connection state notifications are in `RTCClientEvent`. The initial listener is passed in through `join(..., clientEvent, ...)`; the SDK reconnects automatically when the network drops, and you only need to update the UI accordingly:

```kotlin
import cn.seastart.rtc.impl.RTCClientSimpleEvent

val clientEvent = object : RTCClientSimpleEvent() {
    override fun onReconnecting(channel: String) {
        showReconnecting()   // Show "Reconnecting"
    }
    override fun onReconnected(channel: String) {
        hideReconnecting()   // Reconnected; restore the status indicator and any camera / subscriptions you turned off earlier
    }
    override fun onDisconnected(
        channel: String,
        leaveReason: LeaveReason,
        statusCode: Int,
        message: String
    ) {
        // The connection is lost
    }
}

val rtcChannel = rtcEngine.join(this, token, clientEvent, null)
```

### 5.5 Quick reference

| Signal | Response |
|---|---|
| `uplink = poor / lost` | Turn off the camera and keep audio → unpublish video; prompt "your network" |
| `uplink` limitation reason `bandwidth` | Turn off the camera / lower the bitrate |
| `uplink` limitation reason `cpu` | Lower the resolution / frame rate |
| `downlink = poor` (this client has packet loss) | Unsubscribe from video and keep audio / in multi-party calls keep only the main speaker |
| `downlink = poor` (this client has no packet loss) | Prompt "The other user's network is poor" |
| `onReconnecting` | Show "Reconnecting" and refresh the state after recovery |

## 6. Complete example

Putting it all together: use `onNetworkQualityChanged` to drive the status indicator and per-direction prompts (prompt only on `DEGRADED`, so `STABLE` doesn't repeat it; a level hovering around a boundary can still repeat it, so debounce as in 5.1 if needed), degrade and recover as needed, and handle disconnects and reconnects.

```kotlin
import cn.seastart.rtc.impl.RTCMediaSimpleEvent
import cn.seastart.rtc.impl.RTCClientSimpleEvent
import cn.seastart.rtc.info.NetworkQualityChange
import cn.seastart.rtc.info.QualityDirection
import cn.seastart.rtc.info.QualityTrend
import cn.seastart.rtc.track.LocalCameraTrack

class NetworkQualityHandler(
    private val rtcEngine: RTCEngine,
    private val cameraTrack: LocalCameraTrack,
    private val localVideoTrack: LocalVideoTrack
) {
    // Whether the camera was turned off proactively due to a poor network, so it can be turned back on after recovery
    private var cameraOffByNetwork = false

    // The creator must pass this listener to RTCEngine.join(...)
    val clientEvent = object : RTCClientSimpleEvent() {
        override fun onReconnecting(channel: String) {
            showReconnecting()
        }

        override fun onReconnected(channel: String) {
            hideReconnecting()
            if (cameraOffByNetwork) {
                cameraTrack.startCapture(null)
                cameraOffByNetwork = false
            }
        }
    }

    fun attach() {
        rtcEngine.setRtcMediaEvent(object : RTCMediaSimpleEvent() {
            override fun onNetworkQualityChanged(channel: String, change: NetworkQualityChange) {
                runOnUiThread {
                    // Status indicator: update per direction (each callback represents one direction only)
                    when (change.direction) {
                        QualityDirection.UPLINK -> updateUplinkIndicator(change.currentLevel)
                        QualityDirection.DOWNLINK -> updateDownlinkIndicator(change.currentLevel)
                    }

                    // Prompt only when it gets worse, with per-direction messages
                    if (change.trend == QualityTrend.DEGRADED && isBad(change.currentLevel)) {
                        when (change.direction) {
                            QualityDirection.UPLINK ->
                                showTip("Your network is poor; turn off your camera to keep the voice call going")
                            QualityDirection.DOWNLINK ->
                                showTip("Poor network; optimizing video quality")
                        }
                    }
                }
            }
        })

    }

    // After the user confirms: turn off the camera and keep audio
    fun downgradeToAudioOnly() {
        cameraTrack.stopCapture()
        cameraOffByNetwork = true
    }

    private fun isBad(level: String) = level == "poor" || level == "lost"
}
```

> After creating `NetworkQualityHandler`, call `attach()` first, then pass `handler.clientEvent` to `RTCEngine.join(...)`. For degrading actions such as `stopCapture` in the example, we recommend letting the user confirm via a button instead of silently changing the nature of the call.
