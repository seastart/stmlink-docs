---
title: "Quickstart"
description: "A minimal runnable SMeeting Swift SDK example in SwiftUI: log in with a meeting token, create an instant meeting or enter by room number, turn the microphone and camera on, render local and remote video, and exit. Read this right after integrating the SDK."
---

### Prerequisites

+ You have completed [SDK integration](/en/meeting/swift/integration)
+ Your backend can issue the meeting token used to log in to the SDK
+ Your app has requested camera and microphone permissions

> The meeting token is issued by your backend and delivered to the client; the SDK only uses it. Don't assemble credentials on the client yourself.

---

### Minimal runnable example

The example below covers the core flow: log in to the SDK, create an instant meeting, enter the meeting, turn local audio and video on or off, render local and remote video, and exit the meeting.

```swift
import SMeeting
import SRTC
import SwiftUI

@MainActor
final class MeetingViewModel: ObservableObject {
    /// Main SDK entry point; create only one instance for the whole app lifecycle
    let meeting = SMeetingEngine(logLevel: .info)

    @Published var users: [MeetingUserInfo] = []
    @Published var isInMeeting = false
    @Published var isCameraOn = false

    /// 1. Log in: the token comes from your backend
    func login(token: String) async throws {
        try await meeting.login(token: token)
        meeting.delegates.add(delegate: self)
    }

    /// 2. Create an instant meeting and enter it
    func createAndEnter(nickname: String) async throws {
        var createReq = MeetingCreateReq(title: "\(nickname)'s meeting", meetingMode: .normal)
        createReq.meetingType = .instant
        let (_, meetingId) = try await meeting.createRoom(createReq)

        try await meeting.enterRoom(MeetingEnterReq(nickname: nickname, meetingId: meetingId))
        isInMeeting = true
        users = meeting.getUsersInfoList()
    }

    /// 3. Enter an existing meeting by room number
    func enter(roomNo: String, nickname: String, password: String? = nil) async throws {
        var enterReq = MeetingEnterReq(nickname: nickname, roomNo: roomNo)
        enterReq.password = password
        try await meeting.enterRoom(enterReq)
        isInMeeting = true
        users = meeting.getUsersInfoList()
    }

    /// 4. Turn on the local microphone and camera (SwiftUI doesn't need a preview view)
    func openLocalMedia() async throws {
        try await meeting.requestOpenMic()
        try await meeting.requestOpenCamera()
        isCameraOn = true      // Triggers a UI refresh so the local video shows up
    }

    /// 5. Exit the meeting
    func exit() async {
        await meeting.closeCamera()
        await meeting.closeMic()
        await meeting.exitRoom()
        isCameraOn = false
        isInMeeting = false
        users = []
    }
}

// Event callbacks are dispatched on the main thread; @MainActor types must declare protocol methods as nonisolated
extension MeetingViewModel: SMeetingDelegate {
    nonisolated func meeting(_ meeting: SMeetingEngine, userDidEnter user: MeetingUserInfo) {
        DispatchQueue.main.async { self.users = meeting.getUsersInfoList() }
    }

    nonisolated func meeting(_ meeting: SMeetingEngine, userDidExit data: UserExitEventData) {
        DispatchQueue.main.async { self.users = meeting.getUsersInfoList() }
    }
}

struct MeetingView: View {
    @StateObject private var vm = MeetingViewModel()

    var body: some View {
        VStack(spacing: 8) {
            // Local video: pass the local camera track to SRTCVideoView
            if vm.isCameraOn, let cameraTrack = vm.meeting.cameraTrack {
                SRTCVideoView(track: cameraTrack).frame(height: 180)
            }

            // Remote video: the component handles subscribing and unsubscribing internally
            ForEach(vm.users.filter { $0.uid != vm.meeting.currentUserId }, id: \.uid) { user in
                SMeetingRemoteVideoView(meeting: vm.meeting, uid: user.uid, trackDesc: .cameraBig)
                    .frame(height: 180)
            }
        }
    }
}
```

---

### Walkthrough

#### 1. Create `SMeetingEngine`

```swift
let meeting = SMeetingEngine(logLevel: .info)
```

`SMeetingEngine` is the single entry point of the SDK, responsible for login, meeting management, entering and exiting meetings, media control, host operations, and event dispatch. **Create only one instance per app** and hold it globally; multiple instances make meeting state and media devices compete with each other.

#### 2. Log in and register for events

```swift
try await meeting.login(token: token)
meeting.delegates.add(delegate: self)
```

`delegates` is a weak-reference multicast that supports multiple observers at once. Every method of `SMeetingDelegate` has a default empty implementation, so you only implement the events you care about. Remember to call `meeting.delegates.remove(delegate:)` before the object is released or before logging out.

#### 3. Create a meeting or enter one directly

Before the meeting and in the meeting are two separate stages:

+ `createRoom(_:)` creates a meeting and returns `(roomNo, meetingId)`
+ `enterRoom(_:)` enters a meeting; in `MeetingEnterReq`, provide either `meetingId` or `roomNo`

If the meeting has already been created by someone else (or by your backend), skip `createRoom` and enter directly with the room number.

#### 4. Turn on local audio and video

```swift
try await meeting.requestOpenMic()
try await meeting.requestOpenCamera()
```

The method names include `request` because they cover two steps: "asking the meeting for permission to turn it on" and "starting and publishing the local stream." When the host has turned on mute all or camera off for everyone and doesn't allow members to turn them back on themselves, calls from non-hosts throw `SMeetingError.unauthorized`.

In SwiftUI, `requestOpenCamera` doesn't need a `view`; just pass `meeting.cameraTrack` to `SRTCVideoView(track:)` for rendering.

#### 5. Render remote video

Use `SMeetingRemoteVideoView` for remote video. It subscribes by `uid + TrackDesc` when the view appears and unsubscribes when the view disappears, so you don't need to manage the subscription lifecycle yourself.

To render in UIKit / AppKit, or to control subscription timing yourself, see [Video rendering](/zh/meeting/swift/advanced/video-rendering) (Chinese).

#### 6. Exit

+ `exitRoom()` exits the current meeting without logging out
+ `logout()` logs out; if you're still in a meeting, it exits the meeting first automatically

---

### Next steps

+ [Key concepts](/en/meeting/swift/key-concepts)
+ [Media control](/zh/meeting/swift/advanced/media-control) (Chinese)
+ [Video rendering](/zh/meeting/swift/advanced/video-rendering) (Chinese)
+ [Host controls](/zh/meeting/swift/advanced/host-controls) (Chinese)
+ [API reference - SMeetingEngine](/zh/meeting/swift/api-reference/SMeetingEngine) (Chinese)
+ [Events](/zh/meeting/swift/events) (Chinese)
