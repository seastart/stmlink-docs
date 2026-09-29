---
title: "Screen sharing"
description: "Screen sharing with the SRTC Swift SDK and its platform differences: display/window sharing and system audio on macOS, in-app capture on iOS, and full-screen capture on iOS via a Broadcast Upload Extension with SRTCBroadcastKit and an App Group, plus troubleshooting."
---

### Platform differences

| Platform | Support | Description |
| --- | --- | --- |
| macOS 12.3+ | Display / window sharing | Based on `ScreenCaptureKit`; your app lets the user choose a source first |
| iOS in-app capture | Captures only your own app's content | Default mode, no extra integration |
| iOS full-screen capture | Captures the entire system screen | Requires integrating a Broadcast Upload Extension; see below |
| macOS system audio | Supported | Just pass `audioPreset` |
| iOS system audio | Not supported | Neither capture mode supports it; the SDK ignores the screen audio capture option |

On iOS, the two capture modes are selected with `createLocalScreenTrack(mode:)`, defaulting to `.inApp`:

```swift
// In-app capture: only your own app's content; after switching to another app, the remote side sees a frozen frame
let track = srtc.createLocalScreenTrack(preset: .h1080p)

// Full-screen capture: the entire system screen; sharing continues no matter which app you switch to
let track = srtc.createLocalScreenTrack(
    preset: .h720p,
    mode: .broadcast(appGroup: "group.your.app.group")
)
```

---

### Basic usage

#### Create a screen-sharing track with defaults

```swift
let screenTrack = srtc.createLocalScreenTrack(preset: .h1080p)
try await screenTrack.startCapture()
try await channel.publishLocalTrack(screenTrack)
```

If you don't need system audio, this is the most direct way to integrate.

---

### macOS: choose a display or window

On macOS, your app first enumerates capture sources, then passes the source the user selected to the SDK:

```swift
import SRTC

@available(macOS 12.3, *)
func startScreenShare(srtc: SRTCEngine, channel: Channel) async throws {
    let displays = try await ScreenCaptureSources.availableDisplays()
    let windows = try await ScreenCaptureSources.availableWindows()

    // Your app shows its own picker UI; here the first display is used as an example
    let selectedSource = displays.first

    let screenTrack = srtc.createLocalScreenTrack(
        source: selectedSource,
        preset: .h1080p
    )
    try await screenTrack.startCapture()
    try await channel.publishLocalTrack(screenTrack)
}
```

Note one design boundary here:

+ The SDK is responsible for "discovering shareable sources" and "actually starting capture"
+ Your app is responsible for "how to present the list of displays / windows to the user"

The benefit is that the SDK isn't tied to any particular UI approach—SwiftUI, AppKit, TCA, and MVVM can all integrate it.

---

### macOS: exclude your own windows when sharing a full display

When sharing an **entire display**, the captured content **includes your own app's windows** by default (consistent with Zoom / Tencent Meeting). This means any window that's rendering this shared content—the sharing preview in your UI, or the in-call window showing the remote screen share when you test with two instances on one machine—creates an infinite mirror. Put the IDs of these windows in `excludedWindowIds` to cut them out one by one:

```swift
let previewWindowIds = NSApplication.shared.windows
    .filter { $0.isVisible && $0.identifier?.rawValue == "meeting-room" }
    .map { UInt32($0.windowNumber) }

let screenTrack = srtc.createLocalScreenTrack(
    source: selectedDisplay,
    preset: .h1080p,
    excludedWindowIds: previewWindowIds
)
```

+ The value is `UInt32(NSWindow.windowNumber)`. It only matters when sharing an entire display, and is ignored when capturing a single window (`WindowSource`)
+ The list is snapshotted once at `startCapture()`; windows opened afterward all appear in the capture
+ If you really want to go back to the old behavior of excluding the entire app from the capture, set `excludesCurrentApplication` to `true`; `excludedWindowIds` is then ignored

<Note>
`ScreenCaptureSources.availableWindows(includeCurrentApp:)` includes your own windows by default, so sharing one of your own app's windows is a normal option. But likewise, don't pick "a window that's rendering the shared content" as the sharing source.
</Note>

<Warning>
This is a **behavior change** in 1.4.2: previously the SDK cut all of the process's windows out of the full-display capture, so the remote side couldn't see your own app windows. If your product relies on the old behavior, set `excludesCurrentApplication: true` explicitly after upgrading.
</Warning>

---

### macOS: capture system audio at the same time

If you want to send system audio along with screen sharing, pass `audioPreset`:

```swift
let screenTrack = srtc.createLocalScreenTrack(
    source: selectedSource,
    preset: .h1080p,
    audioPreset: .default
)

try await screenTrack.startCapture()
try await channel.publishLocalTrack(screenTrack)
```

When you publish a `LocalScreenTrack` that contains an internal `audioTrack`, the SDK automatically sends the screen audio along through the audio mixing pipeline.

---

### iOS: in-app screen capture

On iOS you don't need to pass `source`:

```swift
let screenTrack = srtc.createLocalScreenTrack(preset: .h1080p)
try await screenTrack.startCapture()
try await channel.publishLocalTrack(screenTrack)
```

Be clear about the following:

+ This is an in-app capture model, not a desktop-style window selection model
+ Once the user switches to another app, no content is captured and the remote side sees a frozen frame
+ Even if you pass `audioPreset`, iOS doesn't capture system audio

---

### iOS: full-screen capture (Broadcast Extension)

To capture the entire system screen, iOS offers only one path: ReplayKit's **Broadcast Upload Extension**.
Capture happens in a separate extension process launched by the system; the SDK carries the frames back to the app process, then encodes and sends them.
What your app needs to do is set up the extension target.

#### 1. Create the extension target

In Xcode, choose **File → New → Target → Broadcast Upload Extension** and uncheck "Include UI Extension".
Add the `SRTCBroadcastKit` dependency to this target (do **not** add `SRTC`), and replace the template-generated `SampleHandler`
entirely with:

```swift
import SRTCBroadcastKit

class SampleHandler: SRTCBroadcastSampleHandler {}
```

Capture, scaling, and cross-process transport are all in the base class; normally you don't need to override any method.

<Warning>
The extension target can link only `SRTCBroadcastKit`. The extension process has a memory limit of **50 MB**, and linking `SRTC`, which
includes WebRTC, gets the extension killed by the system during capture. Conversely, don't add `SRTCBroadcastKit` to the app target
either—`SRTC` on the app side already contains the same code.
</Warning>

#### 2. Configure an App Group

The app and the extension need a shared App Group to exchange capture parameters and host the cross-process channel (the App Group must first be registered in
the Apple Developer portal, and the provisioning profiles for both bundle IDs must include this capability):

1. Enable the **App Groups** capability on both the app target and the extension target, and check the same group;
2. Add it to the **extension's** Info.plist:

```xml
<key>SRTCAppGroupIdentifier</key>
<string>group.your.app.group</string>
```

#### 3. Create the track and start listening

```swift
let screenTrack = srtc.createLocalScreenTrack(
    preset: .h720p,
    mode: .broadcast(appGroup: "group.your.app.group")
)
screenTrack.delegates.add(delegate: self)

try await screenTrack.startCapture()               // Only starts listening; there's no video yet
try await channel.publishLocalTrack(screenTrack)
```

<Note>
A successful `startCapture()` **doesn't mean there's video yet**; it only means the SDK is ready and waiting for the extension to connect.
When the user starts the broadcast isn't up to the app, so listening must be turned on in advance.
</Note>

#### 4. Let the user start the broadcast

Full-screen capture can only be started by the user from the system UI; the app can't tap for the user. The SDK wraps the system picker:

```swift
import SRTC
import SwiftUI

struct ShareButton: View {
    var body: some View {
        SRTCBroadcastPicker(
            preferredExtension: "com.your.app.broadcast",   // The extension's bundle ID
            title: "Start sharing"
        )
        .frame(width: 64, height: 32)
    }
}
```

For UIKit, use `SRTCBroadcastPickerView`. After tapping, the user sees the system broadcast picker panel; only after they select your extension and tap
**Start Broadcast** does video actually start transmitting.

#### 5. Listen for the real start and end

The user may stop sharing directly from the system pill (the red timer at the top of the screen). This happens outside the app,
so you must detect it through events:

```swift
extension MyState: TrackDelegate {
    func screenBroadcastDidStart(_ track: Track) {
        // The extension has connected and video is transmitting — this is what "sharing" really means
    }

    func screenBroadcastDidFinish(_ track: Track, reason: String) {
        // The user tapped the system pill, or the system interrupted the broadcast. Listening stays on, so the user can start again
    }
}
```

Keep these two states apart:

| Property / event | Meaning |
| --- | --- |
| `track.isCapturing` | Listening is ready (`true` after `startCapture()` succeeds) |
| `track.isBroadcastActive` | The extension is sending video, and **the remote side can see it** |
| `screenBroadcastDidStart` | Moves from "waiting" to "sharing" |
| `screenBroadcastDidFinish` | The user or the system ended the broadcast |

To display UI state such as "sharing", check `isBroadcastActive`.

---

### Stop sharing

```swift
try await channel.unpublishLocalTrack(screenTrack)
try await screenTrack.stopCapture()
```

We recommend the order "unpublish first, then stop capture", so the channel-side state and local hardware state stay more consistent.

One more point for iOS full-screen capture: ReplayKit specifies that **only the extension itself can end the broadcast**; the host app can only send a request.
`stopCapture()` notifies the extension to end; the extension then exits on its own and the system pill disappears—so there's a short delay between the call and the pill disappearing.
This is platform behavior, not a sign that the call had no effect.

---

### FAQ

#### Why must macOS let the user choose a source first?

Because desktop capture is fundamentally "the user authorizing which screen or which window to share", and the SDK can't make that choice for the user.

#### Why doesn't iOS support system audio?

This is a platform capability boundary, not a simple switch at the SDK level. The Swift SDK explicitly ignores the screen audio configuration on iOS rather than providing an API that looks supported but does nothing.

#### No video from full-screen sharing on the Simulator?

Full-screen capture depends on real code signing and an App Group, so **it doesn't work on the Simulator—use a real device**. On the Simulator you can only verify that the project compiles.

#### Where do I find the extension's logs?

The extension is a separate process, so its logs don't appear in the Xcode console for the main app. Use **Console.app** to connect to the device
and filter by subsystem `com.srtc.broadcast`. Two common messages:

+ "请先在 App 内开启屏幕共享，再从系统菜单开始广播" ("Start screen sharing in the app first, then start the broadcast from the system menu")—the user tapped the system pill first, before the app called
  `startCapture()`; the extension can't connect to the host and ends on its own;
+ "未配置 App Group" ("App Group not configured")—`SRTCAppGroupIdentifier` in the extension's Info.plist is missing or misspelled.

#### Occasional frame skipping during full-screen sharing?

Screen frames go through a fixed-capacity buffer pool on the host side. When encoding can't keep up, intermediate frames are coalesced and only the latest frame is kept.
This is intentional protection (otherwise memory would grow without bound). The SDK periodically logs a summary of `received / delivered /
coalesced / footprint`; if `coalesced` keeps growing, the current resolution / frame rate is too high for the device,
and you can switch to a lower `ScreenPreset`.
