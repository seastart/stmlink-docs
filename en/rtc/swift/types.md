---
title: "Types"
description: "Public types of the SRTC Swift SDK: JoinOptions, ChannelInfo, UserInfo, TrackInfo, codec and state enums, capture presets, ScreenCaptureMode, DeviceInfo, the iOS audio route types, call quality and active speaker types, and ReceiveStreamStatus. Look up field meanings here."
---

This page doesn't replicate every internal implementation field from the source code; it covers the public types most commonly used and most important to understand when integrating.

---

### JoinOptions

Optional parameters for joining a channel.

| Field | Type | Description |
| --- | --- | --- |
| `autoSubscribeAudio` | `Bool` | Whether to auto-subscribe to existing remote audio; default `false` |
| `autoSubscribeVideo` | `Bool` | Whether to auto-subscribe to existing remote video; default `false` |
| `preferVideoCodec` | `Codec?` | Preferred video codec |
| `preferAudioCodec` | `Codec?` | Preferred audio codec |
| `userName` | `String?` | User name |
| `props` | `[String: String]?` | Custom business properties |

Example:

```swift
let options = JoinOptions(
    autoSubscribeAudio: true,
    autoSubscribeVideo: false,
    userName: "alice"
)
```

---

### ChannelInfo

Channel info.

| Field | Type | Description |
| --- | --- | --- |
| `appId` | `String` | App ID |
| `channel` | `String` | Channel name |
| `streamVendor` | `String?` | The current media streaming engine |
| `props` | `[String: AnyCodable]?` | Custom channel properties |
| `whiteBoard` | `String?` | Whiteboard page URL with the authorization code already appended; just load it in a `WKWebView`—see [Whiteboard](/en/rtc/whiteboard) |
| `createdAt` | `TimeInterval?` | Creation time |
| `updatedAt` | `TimeInterval?` | Update time |

---

### UserInfo

User info.

| Field | Type | Description |
| --- | --- | --- |
| `uid` | `String` | User ID |
| `sid` | `String?` | Session ID |
| `name` | `String?` | User name |
| `deviceType` | `DeviceType?` | Device type |
| `deviceId` | `String?` | Device ID |
| `version` | `String?` | SDK version |
| `network` | `String?` | Network type |
| `streamTracks` | `[TrackInfo]?` | Tracks the user has published |
| `props` | `[String: AnyCodable]?` | Custom user properties |

---

### TrackInfo

Track description.

| Field | Type | Description |
| --- | --- | --- |
| `id` | `String` | Track ID |
| `desc` | `String` | Track description, such as `mic`, `screen`, or `camera_big` |
| `kind` | `TrackKind` | `audio` or `video` |
| `codec` | `Codec?` | Codec |
| `width` / `height` | `Int?` | Video width and height |
| `fps` | `Int?` | Frame rate |
| `angle` | `Int?` | Video angle |
| `maxBitrate` | `Int?` | Maximum bitrate |
| `sampleRate` | `Int?` | Audio sample rate |
| `channels` | `Int?` | Number of audio channels |
| `props` | `[String: String]?` | Custom properties |
| `simulcasts` | `[SimulcastInfo]?` | Simulcast encoding layer info |

---

### Codec

Codec enum.

| Enum value | Description |
| --- | --- |
| `h264` | H.264 video codec |
| `h265` | H.265 video codec |
| `vp8` | VP8 video codec |
| `vp9` | VP9 video codec |
| `av1` | AV1 video codec |
| `aac` | AAC audio codec |
| `opus` | Opus audio codec |

---

### VideoRotation

Video frame rotation, used by `pushFrame(_:rotation:timestampNs:)` and `VideoFrame`.

| Enum value | Raw value | Description |
| --- | --- | --- |
| `_0` | `0` | No rotation (default) |
| `_90` | `90` | 90 degrees clockwise |
| `_180` | `180` | 180 degrees |
| `_270` | `270` | 270 degrees clockwise |

The raw value is the angle, using the same convention as the `rotation` parameter of `inputData` on Android.

---

### StreamVendor

Media streaming engine vendor.

| Enum value | Raw value | Description |
| --- | --- | --- |
| `seastart` | `"seastart"` | SeaStart in-house SFU engine |
| `wangsuCDN` | `"wangsucdn"` | Wangsu CDN engine |

The SDK automatically selects the engine based on `stream_vendor` in the token / join response.

---

### ConnectionState

| Enum value | Description |
| --- | --- |
| `disconnected` | Initial state or not connected |
| `connected` | Connected |
| `reconnecting` | Reconnecting |
| `left` | Left |

### DisconnectReason

| Enum value | Raw value | Description |
| --- | --- | --- |
| `error` | `-1` | Disconnected due to an error |
| `self` | `1` | Left voluntarily |
| `kicked` | `2` | Removed from the channel |
| `replaced` | `3` | Replaced by another session with the same uid |
| `timeout` | `4` | Disconnected due to timeout |
| `destroyed` | `5` | The channel was destroyed |

---

### Preset types

#### MicPreset

Common presets:

+ `.speech`
+ `.music`
+ `.musicStereo`
+ `.musicHighQuality`
+ `.musicHighQualityStereo`

#### CameraPreset

Common presets:

+ `.h180p`
+ `.h360p`
+ `.h720p`
+ `.h1080p`

#### ScreenPreset

Common presets:

+ `.h720p`
+ `.h1080p`

#### ScreenAudioPreset

Common presets:

+ `.default`

These presets are essentially combinations of "capture parameters + publishing parameters". In other words, a preset isn't syntactic sugar; it packages a set of sensible defaults into one object, reducing repeated configuration in your app.

---

### ScreenCaptureMode

iOS screen capture mode, passed to `createLocalScreenTrack(mode:)`. Ignored on macOS (which always uses `ScreenCaptureKit`).

| Value | Description |
| --- | --- |
| `.inApp` | Default. In-app capture with no extra integration, but it **can capture only your own app's content** |
| `.broadcast(appGroup: String)` | Full-screen capture of the entire system screen; requires integrating a Broadcast Upload Extension and an App Group |

```swift
let track = srtc.createLocalScreenTrack(
    preset: .h720p,
    mode: .broadcast(appGroup: "group.your.app.group")
)
```

For integration steps, see [Screen sharing](/en/rtc/swift/advanced/screen-sharing).

---

### DeviceInfo

The unified device structure returned by the device manager.

| Field | Type | Description |
| --- | --- | --- |
| `deviceId` | `String` | Unique device identifier |
| `name` | `String` | Device name |
| `kind` | `DeviceInfo.DeviceKind` | Device type |
| `isDefault` | `Bool` | Whether it's the default device |

Possible values of `DeviceKind`:

+ `audioInput`
+ `audioOutput`
+ `videoInput`

<Note>
On iOS, `getDevices(kind: .audioOutput)` returns an empty array—the system doesn't expose output device enumeration.
To control where output goes, use the audio route types below—see [Audio routing](/en/rtc/swift/advanced/audio-routing).
</Note>

---

### AudioRoute

**iOS only.** The current audio output route, **read-only, for reporting**, with five states.

| Value | Description |
| --- | --- |
| `speaker` | Built-in speaker (speakerphone) |
| `receiver` | Built-in receiver |
| `bluetooth` | Bluetooth headphones |
| `headset` | Wired headphones (3.5 mm / Lightning / USB) |
| `unknown` | Other outputs (AirPlay, CarPlay, HDMI, etc.) |

Helper properties:

| Member | Type | Description |
| --- | --- | --- |
| `displayName` | `String` | Route name, usable directly in the UI; follows the system language—Chinese on Chinese systems, English otherwise (since 1.5.1; always Chinese before) |
| `isBuiltIn` | `Bool` | Whether it's a built-in route (speaker / receiver) |
| `isExternal` | `Bool` | Whether it's an external route (Bluetooth / wired) |

---

### AudioRouteTarget

**iOS only.** Route targets you can **switch to actively**, with only two states.

| Value | Description |
| --- | --- |
| `speaker` | Speaker (speakerphone) |
| `earpiece` | Receiver |

It's deliberately separate from `AudioRoute`: iOS doesn't provide the ability to switch to a specific Bluetooth / wired device; external devices are taken over by the system,
and the SDK can only control "built-in speaker or receiver". `asRoute` maps back to `AudioRoute` (`.earpiece` → `.receiver`).

---

### AudioRouteInfo

**iOS only.** A snapshot of a system audio port, **for diagnostics / display**, not a list to choose from.

| Field | Type | Description |
| --- | --- | --- |
| `id` | `String` | Port UID; the fixed value `"speaker"` for the speaker |
| `route` | `AudioRoute` | The semantic route this port corresponds to |
| `name` | `String` | Port name, such as "AirPods Pro" |
| `isActive` | `Bool` | Whether it's the route currently in effect |

---

### AudioCallState

**iOS only.** The system call state, from CallKit. The SDK uses it to decide when it can recover after an audio interruption.

| Value | Description |
| --- | --- |
| `dialing` | Outgoing call dialing |
| `incoming` | Incoming call ringing |
| `connected` | Call connected |
| `disconnected` | No call / call ended |
| `unknown` | Unknown |

---

### ConnectionQuality

Connection quality level, parsed from the reports sent by the server.

| Value | Description |
| --- | --- |
| `unknown` | Initial placeholder; no report yet |
| `excellent` | Excellent |
| `good` | Good |
| `poor` | Poor |
| `lost` | Lost |

When comparing which level is worse, the order is `unknown` < `excellent` < `good` < `poor` < `lost`.

---

### QualitySample

A snapshot of quality values in one direction; a signal-strength icon / network panel can render directly from these fields.

| Field | Type | Description |
| --- | --- | --- |
| `level` | `ConnectionQuality` | Level given by the server |
| `score` | `Int` | 0–100, higher is better |
| `mos` | `Double` | 1.0–4.5, higher is better |
| `loss` | `Double` | Packet loss rate as a **ratio** (0–1, not a percentage) |
| `rtt` | `Double` | Round-trip time, in milliseconds |
| `jitter` | `Double` | Jitter, in milliseconds |
| `packets` | `Int` | Number of packets included in this round of statistics |
| `bitrate` | `Int` | Average bitrate, in kbps |
| `bytes` | `Int` | Bytes in this window |

---

### QualityReport

A complete quality report. The SDK emits one each time the server sends a report.

| Field | Type | Description |
| --- | --- | --- |
| `ts` | `Int64` | Unix timestamp in milliseconds when the server generated the report |
| `pub` | `QualitySample` | Uplink (client to SFU) |
| `sub` | `QualitySample` | Downlink (SFU to client) |

---

### QualityEvaluation

A simplified level evaluation snapshot, used by `getConnectionQuality()` and the level-change event.

| Field | Type | Description |
| --- | --- | --- |
| `uplink` | `ConnectionQuality` | Uplink level |
| `downlink` | `ConnectionQuality` | Downlink level |
| `overall` | `ConnectionQuality` | The **worse** of the uplink and downlink levels |
| `mos` | `Double` | The smaller of the uplink and downlink values, reflecting the side the user perceives as weakest |
| `timestamp` | `Int64` | The `ts` of the corresponding report |

---

### ConnectionQualityChange

| Field | Type | Description |
| --- | --- | --- |
| `evaluation` | `QualityEvaluation` | The evaluation after the change |
| `previous` | `ConnectionQuality` | The level before the change; `unknown` on the first change |

---

### ActiveSpeakerInfo / ActiveSpeakersSnapshot

| Type | Fields |
| --- | --- |
| `ActiveSpeakerInfo` | `uid`, `trackId`, `level` (normalized linear volume, 0–1) |
| `ActiveSpeakersSnapshot` | `ts`, `speakers: [ActiveSpeakerInfo]` |

`speakers` is the **full list**: the SDK has already merged the server's incremental protocol and sorted it by `level` in descending order; when nobody is speaking, it's an empty array.

---

### LayerSwitchedInfo

| Field | Type | Description |
| --- | --- | --- |
| `subKey` | `String` | Subscription key, in the form `publisherUid:trackId` |
| `fromTrackId` | `String?` | The layer before the switch |
| `toTrackId` | `String` | The layer after the switch |
| `reason` | `String` | Reason given by the server, such as `bwe_down`, `bwe_up`, or `track_ended`; `client` for a manual layer switch by the client |
| `latencyMs` | `Int` | Time from initiating the switch to actually reaching the target layer, in milliseconds |

For how to use the quality-related types above, see [Call quality and active speakers](/en/rtc/swift/advanced/call-quality).

---

### ReceiveStreamStatus

The payload of a receive status change for one remote video, delivered by the `channel(_:didChangeReceiveStreamStatus:)` callback.

| Field | Type | Description |
| --- | --- | --- |
| `uid` | `String` | Identifier of the user publishing the stream |
| `trackId` | `String` | Track identifier |
| `trackDesc` | `String` | Track description (`camera` / `screen`, etc., corresponding to `TrackInfo.desc`) |
| `timedOut` | `Bool` | `true` means receiving has timed out; `false` means receiving has recovered |

It's **judged per track**, looking only at whether this video is producing frames, and is unrelated to the quality level of the whole link—don't use `ConnectionQualityChange` in its place; see [Events](/en/rtc/swift/events) for details.

<Note>
It corresponds to `engineChannel:onReceiveStreamStatusChange:trackId:status:` in the older `RTCEngineKit`; `timedOut` has the same truth value as the old `status` (`true` means timed out), so you don't need to invert it when migrating.
</Note>
