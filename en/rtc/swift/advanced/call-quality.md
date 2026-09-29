---
title: "Call quality and active speakers"
description: "Read network quality values and levels in the SRTC Swift SDK, show a \"poor network\" prompt and downgrade proactively, highlight active speakers, and switch simulcast layers manually. These events exist only on the SeaStart (SFU) engine."
---

### Overview

The SFU periodically sends a set of control-plane messages, which the SDK turns into four `ChannelDelegate` events:

| Event | Content | Typical use |
| --- | --- | --- |
| `didReceiveQualityReport` | Raw uplink and downlink values (packet loss, RTT, jitter, bitrate, MOS) | Signal-strength icon, diagnostics panel |
| `didChangeConnectionQuality` | A **level change** in quality | "Poor network" prompt, proactive downgrade |
| `didChangeActiveSpeakers` | A full snapshot of active speakers | Speaker highlighting, voice-activated layout |
| `didSwitchLayer` | Result of a simulcast layer switch | Troubleshooting sudden changes in video quality |

<Note>
These four events **exist only on the SeaStart (SFU) engine**. They travel over the signaling DataChannel on the subscribing PeerConnection, and the Wangsu (CDN) engine has no such path, so with CDN you receive none of them and `getConnectionQuality()` also returns `nil`. Use `Channel.streamVendor` to tell the current engine—see [Types](/en/rtc/swift/types#streamvendor).
</Note>

All callbacks have default empty implementations, so implement only the ones you care about. Register the same way as for other channel events:

```swift
channel.delegates.add(delegate: self)
```

---

### Network quality: two event streams, don't mix them up

Quality uses **two event streams**, because the two kinds of needs differ in trigger frequency by an order of magnitude:

+ `didReceiveQualityReport`—**fires on every server report**; it's a stream of raw values
+ `didChangeConnectionQuality`—**fires only when the level changes**; it signals a state change

```swift
extension CallController: ChannelDelegate {

    // Value stream: drives the signal-strength icon and diagnostics panel
    func channel(_ channel: Channel, didReceiveQualityReport report: QualityReport) {
        signalBars.update(
            level: report.sub.level,          // Downlink level: whether the user "sees/hears well"
            rtt: report.sub.rtt,
            loss: report.sub.loss
        )
    }

    // Level change: drives prompts and downgrading
    func channel(_ channel: Channel, didChangeConnectionQuality change: ConnectionQualityChange) {
        switch change.evaluation.overall {
        case .poor, .lost:
            showToast("Poor network connection")
            // Proactive downgrade: switch to the low stream (see "Simulcast" below), or unsubscribe from remote video that's out of view
            try? channel.switchLayer(pubUid: uid, trackId: trackId, targetTrackId: lowLayerId)
        case .excellent, .good:
            hideToast()
        case .unknown:
            break
        }
    }
}
```

<Warning>
**Don't use `didReceiveQualityReport` to drive toasts or downgrade decisions.** It fires every report cycle, and when the level jitters between two values, prompts flash repeatedly and downgrading flip-flops back and forth. For the meaning "the network got worse", use `didChangeConnectionQuality`; the SDK already does the level-change detection inside it.
</Warning>

`QualityReport` has two `QualitySample` values, `pub` (uplink, client to SFU) and `sub` (downlink, SFU to client); for field meanings, see [Types](/en/rtc/swift/types#qualitysample). Key points:

+ `level` is the level given by the server; for both `score` (0–100) and `mos` (1.0–4.5), higher is better
+ `loss` is a ratio (0–1), not a percentage
+ `rtt` and `jitter` are in milliseconds; `bitrate` is in kbps
+ When figuring out "whose problem it is", look at both sides: a poor `pub` means a problem with your own uplink; a poor `sub` means a problem with the downlink or the remote side's uplink

`evaluation.overall` in `ConnectionQualityChange` takes the **worse** of the uplink and downlink levels (`unknown` < `excellent` < `good` < `poor` < `lost`), and `evaluation.mos` takes the smaller of the two—both follow "the side the user perceives as weakest". `previous` is the level before the change, and is `.unknown` on the first change.

#### Cold start: show the level as soon as the page opens

Events arrive only on changes, so when the UI is first created you have no value yet. Call `getConnectionQuality()` once to fill in the current snapshot:

```swift
if let evaluation = channel.getConnectionQuality() {
    signalBars.update(level: evaluation.overall)
}
```

It returns `nil` when no report has been received yet (which is different from "a report was received but the level is `unknown`").

<Note>
After a reconnect, the SDK clears the quality cache (latest evaluation, level-change baseline, speaker snapshot), so the UI doesn't keep showing a stale `poor` level after recovery. So after a reconnect, `getConnectionQuality()` briefly returns `nil` until a new report arrives—this is intentional; just treat it as "no data yet" in the UI.
</Note>

---

### Active speakers

```swift
func channel(_ channel: Channel, didChangeActiveSpeakers snapshot: ActiveSpeakersSnapshot) {
    // Full snapshot, already sorted by volume in descending order — overwrite directly, don't accumulate yourself
    highlightedUids = Set(snapshot.speakers.map(\.uid))
    loudestUid = snapshot.speakers.first?.uid
}
```

`snapshot.speakers` is the **full list**: the SDK has already merged the server's incremental protocol (who started speaking, who stopped) into a complete snapshot, sorted by `level` in descending order. So:

+ Your app just overwrites the UI state as a whole; you **don't need** to maintain a set of "who is still speaking" yourself
+ When nobody is speaking, `speakers` is an empty array—the event isn't skipped
+ `level` is a normalized linear volume (0–1), which you can use directly to draw a volume bar

Each `ActiveSpeakerInfo` carries `uid` and `trackId`—the same user may have multiple audio tracks, so use the latter when you need to pinpoint the exact track.

---

### Simulcast: switch layers manually

When the publisher has simulcast enabled, the same video has multiple layers. By default the SFU selects a layer automatically based on bandwidth, and notifies you through `didSwitchLayer` after switching (`reason` is a server reason such as `bwe_down` / `bwe_up`):

```swift
func channel(_ channel: Channel, didSwitchLayer info: LayerSwitchedInfo) {
    // info.reason is the server reason; info.latencyMs is the time taken to switch
    logger.debug("Layer switch \(info.fromTrackId ?? "-") → \(info.toTrackId), reason \(info.reason)")
}
```

When your UI knows that "this video is now shown only as a small tile", you can request a lower layer yourself to save bandwidth and decoding cost:

```swift
try channel.switchLayer(
    pubUid: uid,
    trackId: trackId,            // The stable handle used when subscribing
    targetTrackId: lowLayerId    // The target layer to switch to
)
```

When a manual layer switch completes, `didSwitchLayer` fires as well, with `reason` set to `client`.

<Warning>
`targetTrackId` must be within the candidate layers declared when subscribing; **the SDK doesn't validate it again** (to avoid maintaining a duplicate copy of state). An out-of-range value doesn't raise an error immediately—the server just doesn't switch to it. To check which layer the server is actually serving right now, use `channel.getSubscribeHit(uid:trackId:)`.
</Warning>

**Throws:**

+ `SRTCError.engineNotSupported(_:)`—the current engine isn't SeaStart (for example, when using CDN)
+ `SRTCError.transportNotReady`—the signaling channel isn't ready yet (just joined, or reconnecting)
+ `SRTCError.webrtcError(_:)`—sending on the signaling channel failed (usually buffer congestion)

The typical usage covers three scenarios: "switching between large and small tiles, pagination, and downgrading in the background". Switch once manually when the layout changes, and leave the rest to the SFU's automatic policy.

---

### Related pages

+ [Events](/en/rtc/swift/events)
+ [Types](/en/rtc/swift/types)
+ [Mute vs. unpublish](/en/rtc/swift/advanced/mute-vs-unpublish)
+ [Multi-channel](/en/rtc/swift/advanced/multi-channel)
