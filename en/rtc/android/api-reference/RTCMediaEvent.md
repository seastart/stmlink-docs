---
title: "RTCMediaEvent"
description: "Android per-channel media events: media server connection, remote video frames, media metrics, network quality changes, volume reports, and active speakers. Every callback carries the channel ID. Read when handling media callbacks on Android."
---

`RTCMediaEvent` carries the media events of one channel. `RTCEngine.setRtcMediaEvent(...)` sets the listener for the default channel; for additional channels, use `RTCChannel.setRtcMediaEvent(...)`. If you only care about a few events, extend `RTCMediaSimpleEvent`.

The first parameter of every callback is `channel: String`, which identifies which channel the event belongs to in multi-channel scenarios.

## Interface methods

### onMediaConnected(channel)

```kotlin
fun onMediaConnected(channel: String)
```

Connected to the media streaming server of this channel.

### onRemoteVideoFrame(channel, uid, trackDesc, y, u, v, width, height, format, angle)

```kotlin
fun onRemoteVideoFrame(
    channel: String,
    uid: String,
    trackDesc: String,
    y: ByteArray?,
    u: ByteArray?,
    v: ByteArray?,
    width: Int,
    height: Int,
    format: Int,
    angle: Int
)
```

A remote video frame was received in this channel. `uid` and `trackDesc` identify the remote track; `y`, `u`, and `v` are the image components, `width` / `height` are the dimensions, `format` is the pixel format, and `angle` is the rotation angle.

### onMediaMetric(channel, metric)

```kotlin
fun onMediaMetric(channel: String, metric: MediaMetric.Metric)
```

A snapshot of this channel's media performance metrics, reported about every 5 seconds after joining. For fields, see [Media quality](/en/rtc/android/media-quality).

### onNetworkQualityChanged(channel, change)

```kotlin
fun onNetworkQualityChanged(
    channel: String,
    change: NetworkQualityChange
)
```

This channel received a quality report from the server. Every report fires once each for uplink and downlink; when the level hasn't changed, `trend` is `STABLE`. The SDK doesn't check for level crossings or debounce, so debounce yourself if needed. The callback runs on an SDK background thread, so switch to the main thread before updating the UI. For usage, see [Network quality](/en/rtc/android/network-quality).

### onVolumesReport(channel, volumes)

```kotlin
fun onVolumesReport(
    channel: String,
    volumes: MutableMap<UserTrackDesc, VolumeInfo>
)
```

Volume info for this channel.

### onActiveSpeakersChanged(channel, speakers)

```kotlin
fun onActiveSpeakersChanged(
    channel: String,
    speakers: List<ActiveSpeakerInfo>
)
```

This channel's list of active speakers changed.

:::note
Camera device additions, removals, and runtime errors are Engine-global events. They have moved from `RTCMediaEvent` to [`RTCCameraDeviceEvent`](/en/rtc/android/api-reference/RTCCameraDeviceEvent) and aren't reported repeatedly because of multiple channels. Local video frames and local audio frames also use their own separate listeners.
:::
