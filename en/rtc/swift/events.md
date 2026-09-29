---
title: "Events"
description: "Event reference for the SRTC Swift SDK: ChannelDelegate connection, user, track, message, and call quality events; TrackDelegate track-level and iOS screen broadcast events; and the iOS-only AudioRouteSessionDelegate, with when each fires and its key parameters."
---

### ChannelDelegate

Register with `channel.delegates.add(delegate: self)`.

```swift
final class RoomController: ChannelDelegate {
    func channel(_ channel: Channel, didJoinSucceed info: ChannelInfo) {
        print("joined:", info.channel)
    }
}
```

---

### Connection events

| Method | When it fires | Key parameters |
| --- | --- | --- |
| `channel(_:didJoinSucceed:)` | Joined the channel successfully for the first time | `ChannelInfo` |
| `channelIsReconnecting(_:)` | Reconnection starts after a network disconnect | `Channel` |
| `channel(_:didReconnect:)` | Reconnected successfully | `ChannelInfo` |
| `channel(_:didDisconnect:error:)` | The connection is fully lost or you left the channel | `DisconnectReason`, `Error?` |

---

### User events

| Method | When it fires | Key parameters |
| --- | --- | --- |
| `channel(_:userDidJoin:)` | A remote user joined | `UserInfo` |
| `channel(_:userDidUpdate:)` | A remote user's profile was updated | `UserInfo` |
| `channel(_:meDidUpdate:)` | Your own info was updated | `UserInfo` |
| `channel(_:userDidLeave:reason:)` | A remote user left | `uid`, `DisconnectReason` |

---

### Track events

| Method | When it fires | Key parameters |
| --- | --- | --- |
| `channel(_:user:didAddTrack:)` | A remote user added a track | `UserInfo`, `TrackInfo` |
| `channel(_:user:didUpdateTrack:)` | A remote track's info was updated | `UserInfo`, `TrackInfo` |
| `channel(_:user:didRemoveTrack:)` | A remote track was removed | `UserInfo`, `TrackInfo` |
| `channel(_:didChangeReceiveStreamStatus:)` | A remote video timed out on receiving / recovered | `ReceiveStreamStatus` |

The most common entry point for your app is `didAddTrack`, because that's usually where you decide whether to subscribe to remote video or remote audio.

`didChangeReceiveStreamStatus` is judged **per track**: after subscribing, if no frames of that video arrive for a period of time, it reports a timeout (`timedOut == true`), and as soon as frames resume it reports again (`timedOut == false`). Use it to toggle a "loading / remote network issue" indicator on a given video tile. When the first frame arrives after subscribing, you first receive a recovery report, which you can use to hide the initial loading indicator. You can also query `RemoteVideoTrack.isReceiveTimedOut` at any time.

<Warning>
**Don't use `didChangeConnectionQuality` in its place.** The quality level is one value for the whole link and describes "whether the network is good", not "whether this video has stopped": when a single track stops being published, the sender's camera freezes, or one video fails to decode, the link level can stay excellent the whole time; conversely, when the network jitters and the level drops, several videos may actually still be producing frames normally. Substituting the level for a per-track stall judgment inevitably causes false alarms.
</Warning>

---

### Message and channel events

| Method | When it fires | Key parameters |
| --- | --- | --- |
| `channel(_:didReceiveCustomMessage:)` | A custom message was received | `CustomMessage` |
| `channel(_:didUpdateInfo:)` | Channel info was updated | `ChannelInfo` |

---

### Call quality events

| Method | When it fires | Key parameters |
| --- | --- | --- |
| `channel(_:didReceiveQualityReport:)` | Every time the server sends a quality report (real-time value stream) | `QualityReport` |
| `channel(_:didChangeConnectionQuality:)` | The quality level changed (state change) | `ConnectionQualityChange` |
| `channel(_:didChangeActiveSpeakers:)` | Active speakers changed | `ActiveSpeakersSnapshot` |
| `channel(_:didSwitchLayer:)` | A simulcast layer switch completed | `LayerSwitchedInfo` |

Quality uses **two event streams**; pick one by purpose: `didReceiveQualityReport` delivers raw values every report cycle, suited for signal-strength icons and diagnostics panels; `didChangeConnectionQuality` fires only when the level changes, suited for "poor network" prompts and proactive downgrading. **Don't use the former to drive prompts or downgrading**—it flashes repeatedly when the level jitters.

`didChangeActiveSpeakers` delivers a **full snapshot** (already sorted by volume in descending order), so your app just overwrites the UI without merging increments itself; when nobody is speaking, it's an empty array.

<Note>
These four events exist only on the **SeaStart (SFU) engine**—they travel over the signaling DataChannel on the subscribing PeerConnection, and the Wangsu (CDN) engine has no such path. See [Call quality and active speakers](/en/rtc/swift/advanced/call-quality) for details.
</Note>

---

### TrackDelegate

Register with `track.delegates.add(delegate: self)`.

---

### Track-level events

| Method | When it fires | Key parameters |
| --- | --- | --- |
| `track(_:didUpdateInfo:)` | Track info was updated | `TrackInfo` |
| `trackDidMute(_:)` | The track was muted | `Track` |
| `trackDidUnmute(_:)` | The track was unmuted | `Track` |
| `trackDidEnd(_:)` | The track ended | `Track` |
| `trackDidBindRtcTrack(_:)` | The underlying WebRTC track has been bound | `Track` |
| `screenBroadcastDidStart(_:)` | iOS full-screen sharing: the extension has connected and video has started transmitting | `Track` |
| `screenBroadcastDidFinish(_:reason:)` | iOS full-screen sharing: the broadcast ended (including the user tapping the system pill) | `Track`, `String` |

`trackDidBindRtcTrack(_:)` is especially useful for video rendering, because the remote track object may appear first and the underlying media track finishes binding a bit later—receiving this event is what means you can render.

The two `screenBroadcast` events fire only with iOS full-screen capture (`ScreenCaptureMode.broadcast`):
full-screen sharing is started by the user from the system UI and may be stopped directly from the system pill; these actions happen outside the app,
so you can only detect them through events. A successful `startCapture()` only means the SDK is ready; receiving `screenBroadcastDidStart`
is what really means "sharing". See [Screen sharing](/en/rtc/swift/advanced/screen-sharing) for details.

---

### AudioRouteSessionDelegate

**iOS only.** Register with `AudioRouteSession.shared.delegates.add(delegate: self)`.
All callbacks run on the main thread, and the protocol provides default empty implementations, so implement only the methods you care about.

| Method | When it fires | Key parameters |
| --- | --- | --- |
| `audioRouteSession(_:didChangeRoute:from:reason:)` | The audio output route changed | `AudioRoute`, `AVAudioSession.RouteChangeReason` |
| `audioRouteSessionWasInterrupted(_:)` | The audio session was interrupted (incoming call / Siri / another app took over) | `AudioRouteSession` |
| `audioRouteSessionDidRecoverFromInterruption(_:)` | After the interruption has **actually been recovered successfully** | `AudioRouteSession` |
| `audioRouteSession(_:didChangeCallState:)` | The system call state changed (CallKit) | `AudioCallState` |

`reason` distinguishes the source of the change (`.oldDeviceUnavailable` unplugged, `.newDeviceAvailable` plugged in,
`.override` actively overridden by the app); when troubleshooting route issues, it's often more valuable than the result itself.

`audioRouteSessionDidRecoverFromInterruption(_:)` is **not equivalent** to the system's
`AVAudioSession.interruptionNotification(.ended)`: at the moment a system phone call hangs up, the audio hardware hasn't been released yet,
so the SDK waits until the call has really ended and the app is back in the foreground before rebuilding the session, and retries on failure—this callback fires only after a real, successful recovery.
Your app just refreshes the UI here and doesn't need to handle this timing itself.

See [Audio routing](/en/rtc/swift/advanced/audio-routing) for details.
