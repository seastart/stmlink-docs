---
title: "Quickstart"
description: "A minimal SwiftUI example for the SRTC Swift SDK: create SRTCEngine, join a channel, capture and publish local microphone and camera tracks, subscribe to remote video in ChannelDelegate, and leave. Also explains why joinChannel returns a Channel and why create, capture, and publish are separate."
---

### Prerequisites

+ You have completed [SDK integration](/en/rtc/swift/integration)
+ Your server can issue tokens for joining a channel
+ Your app has requested camera and microphone permissions

The token must be issued by your backend; the client isn't involved in signing. For how to issue it, see [Token and authentication](/en/rtc/token).

---

### Minimal runnable example

The example below covers the core path: initialize the SDK, join a channel, turn on the microphone and camera, subscribe to remote video, and leave the channel.

```swift
import SRTC
import SwiftUI

@MainActor
final class RoomViewModel: ObservableObject, ChannelDelegate {
    @Published var localTrack: LocalCameraTrack?
    @Published var remoteTrack: Track?

    private let srtc = SRTCEngine()
    private var channel: Channel?
    private var micTrack: LocalMicTrack?

    func join(with token: String) async throws {
        srtc.logLevel = .debug

        let channel = try await srtc.joinChannel(
            token: token,
            options: JoinOptions(autoSubscribeAudio: true)
        )
        channel.delegates.add(delegate: self)
        self.channel = channel

        let micTrack = srtc.createLocalMicTrack(preset: .music)
        try await micTrack.startCapture()
        try await channel.publishLocalTrack(micTrack)
        self.micTrack = micTrack

        let cameraTrack = srtc.createLocalCameraTrack(preset: .h720p)
        try await cameraTrack.startCapture()
        try await channel.publishLocalTrack(cameraTrack)
        self.localTrack = cameraTrack
    }

    func leave() async {
        // The SDK stops capture and unpublishes internally; your code only needs to clear references
        await srtc.leaveChannel()
        channel = nil
        micTrack = nil
        localTrack = nil
        remoteTrack = nil
    }

    func channel(_ channel: Channel, user: UserInfo, didAddTrack track: TrackInfo) {
        guard track.kind == .video else { return }

        Task {
            try? await channel.subscribeRemoteVideoTrack(uid: user.uid, trackId: track.id)
            let subscribedTrack = channel.getRemoteTrack(uid: user.uid, trackId: track.id)
            await MainActor.run {
                self.remoteTrack = subscribedTrack
            }
        }
    }
}

struct RoomView: View {
    @StateObject private var vm = RoomViewModel()
    let token: String

    var body: some View {
        VStack(spacing: 12) {
            if let localTrack = vm.localTrack {
                SRTCVideoView(track: localTrack)
                    .frame(height: 220)
            }

            if let remoteTrack = vm.remoteTrack {
                SRTCVideoView(track: remoteTrack)
                    .frame(height: 220)
            }

            HStack {
                Button("Join channel") {
                    Task { try? await vm.join(with: token) }
                }

                Button("Leave channel") {
                    Task { await vm.leave() }
                }
            }
        }
        .padding()
    }
}
```

---

### How the flow works

#### 1. Initialize `SRTCEngine`

`SRTCEngine` is the main entry point of the SDK. It is responsible for:

+ Creating local tracks
+ Parsing the token and joining the channel
+ Managing the lifecycle of the current `Channel`
+ Configuring the log level and audio processors

#### 2. Call `joinChannel`

```swift
let channel = try await srtc.joinChannel(
    token: token,
    options: JoinOptions(autoSubscribeAudio: true)
)
```

The key idea: the core object in real-time audio and video isn't a UI page but the connected channel state. That's why `joinChannel(...)` returns a `Channel` object rather than a Boolean, and publishing, subscribing, messaging, and the user list all revolve around it.

#### 3. Create and publish local tracks

Audio and video follow the same path:

+ `create...Track(...)` only creates the track object
+ `startCapture()` is what actually starts hardware capture
+ `publishLocalTrack(...)` is what sends the data to the channel

With these three steps separated, you get finer control over "when to acquire hardware resources" and "when to actually publish".

#### 4. Subscribe to remote video in the callback

When a remote user publishes, you're notified through the `didAddTrack` callback of `ChannelDelegate`. Once you have the `TrackInfo`:

+ Call `subscribeRemoteVideoTrack(uid:trackId:)` to subscribe
+ Then get the track object with `getRemoteTrack(uid:trackId:)`
+ Pass the track to `SRTCVideoView`, `VideoView`, or `SRTCVideoRenderer`

---

### Next steps

+ [Key concepts](/en/rtc/swift/key-concepts)
+ [Mute vs. unpublish](/en/rtc/swift/advanced/mute-vs-unpublish)
+ [Device management](/en/rtc/swift/advanced/device-management)
+ [Screen sharing](/en/rtc/swift/advanced/screen-sharing)
+ [Custom tracks](/en/rtc/swift/advanced/custom-track)
+ [API reference - SRTCEngine](/en/rtc/swift/api-reference/SRTCEngine)
+ [API reference - Channel and Track](/en/rtc/swift/api-reference/media-tracks)
