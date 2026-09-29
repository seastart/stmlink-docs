---
title: "MeetingMediaEvent"
description: "Receive the current meeting's media connection, remote raw frames, media statistics, volume, active speaker, and network quality changes through MeetingEngine.mediaEvent. Read this when you show call quality, speaking indicators, or process remote video frames."
---

`MeetingMediaEvent` carries media events of the current meeting and is registered through `MeetingEngine.mediaEvent`. You can extend `MeetingMediaSimpleEvent` and override only what you need.

## Usage notes

+ This interface covers connection state, raw remote frames, and aggregated quality statistics; for the receive state of a single remote video, use `MeetingRemoteVideoEvent`.

+ `onRemoteVideoFrame()` is called back on the SRTC media thread and must not block.
+ Media statistics are usually produced about every 5 seconds; for poor-network level changes, prefer `onNetworkQualityChanged()`.
+ This listener is cleared when you exit the meeting; reassign it for the next meeting.

## Methods

### onMediaConnected()

```kotlin
fun onMediaConnected()
```

Description: The connection to the current meeting's SRTC media streaming server succeeded.

Parameters: None.

Returns: None (`Unit`).

### onRemoteVideoFrame(uid, trackDesc, y, u, v, width, height, format, angle)

```kotlin
fun onRemoteVideoFrame(
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

Description: Received one frame of raw remote video data.

Parameters:

| Parameter | Description |
| --- | --- |
| `uid` | Remote user UID. |
| `trackDesc` | Remote track description. |
| `y` | Nullable Y image plane. |
| `u` | Nullable U image plane. |
| `v` | Nullable V image plane. |
| `width` | Video width in pixels. |
| `height` | Video height in pixels. |
| `format` | Pixel format value defined by SRTC. |
| `angle` | Video rotation angle. |

Returns: None (`Unit`).

### onMediaMetric(metric)

```kotlin
fun onMediaMetric(metric: MediaMetric.Metric)
```

Description: Delivers a media performance metric snapshot of the current meeting.

Parameters:

| Parameter | Description |
| --- | --- |
| `metric` | Send, receive, network, and server-side quality statistics; for fields, see [Media quality](/en/meeting/android/media-quality). |

Returns: None (`Unit`).

### onVolumesReport(volumes)

```kotlin
fun onVolumesReport(volumes: MutableMap<UserTrackDesc, VolumeInfo>)
```

Description: Delivers a volume snapshot of each user track in the current meeting.

Parameters:

| Parameter | Description |
| --- | --- |
| `volumes` | Volume map keyed by `UserTrackDesc`, which identifies a user track. |

Returns: None (`Unit`).

### onActiveSpeakersChanged(speakers)

```kotlin
fun onActiveSpeakersChanged(speakers: List<ActiveSpeakerInfo>)
```

Description: The current meeting's active speaker list changed.

Parameters:

| Parameter | Description |
| --- | --- |
| `speakers` | Active speaker snapshot, sorted by SRTC rules. |

Returns: None (`Unit`).

### onNetworkQualityChanged(change)

```kotlin
fun onNetworkQualityChanged(change: NetworkQualityChange)
```

Description: Called once for the uplink and once for the downlink each time the current meeting receives a quality report from the server, without debouncing; when the level hasn't changed, `trend` is `STABLE`.

Parameters:

| Parameter | Description |
| --- | --- |
| `change` | Direction, old level, new level, trend, and other information. |

Returns: None (`Unit`). For the data type, see [SRTC types](/en/rtc/android/types); for the levels, see [SRTC enums](/en/rtc/android/enums).
