---
title: "Events"
description: "Every SMeetingDelegate event in the SMeeting Swift SDK—connection, members, room state, messages, host commands, waiting room, sub-meetings, sign-in, devices, audio routing, call quality, receive stream status, and IM—with when each fires and its data type. Read when handling events."
---

### Registering and unregistering

All meeting events are reported through `SMeetingDelegate`:

```swift
final class MeetingController: SMeetingDelegate {
    init(meeting: SMeetingEngine) {
        meeting.delegates.add(delegate: self)
    }

    func meeting(_ meeting: SMeetingEngine, userDidEnter user: MeetingUserInfo) {
        print("Member entered:", user.name)
    }
}
```

Key points:

+ `delegates` is a **weak-reference multicast**, so you can register multiple observers; the SDK doesn't extend your object's lifetime because you registered it
+ Every method in the protocol has a default empty implementation, so you only implement the events you care about
+ Call `meeting.delegates.remove(delegate:)` when you no longer need it
+ Callbacks are always dispatched on the **main thread**, so you can update the UI directly

If your observer is a `@MainActor` type, declare the protocol methods as `nonisolated`, then hop back to the main actor context inside them:

```swift
extension MeetingController: SMeetingDelegate {
    nonisolated func meeting(_ meeting: SMeetingEngine, userDidExit data: UserExitEventData) {
        DispatchQueue.main.async { self.users = meeting.getUsersInfoList() }
    }
}
```

---

### Connection events

| Method | When it fires | Data type |
| --- | --- | --- |
| `meetingIsReconnecting(_:)` | The meeting connection is interrupted and automatic reconnection starts | None |
| `meetingDidReconnect(_:)` | Reconnection succeeded | None |
| `meeting(_:didDisconnect:)` | You were disconnected: you exited the meeting, were removed, the meeting ended, a timeout occurred, etc. | `DisconnectEventData` |

The `reason` of `DisconnectEventData` is a `DisconnectReason`, which tells you whether you exited on your own or were disconnected; `error` carries the underlying error when the disconnection is abnormal.

---

### Member events

| Method | When it fires | Data type |
| --- | --- | --- |
| `meeting(_:userDidEnter:)` | Another member enters the meeting | `MeetingUserInfo` |
| `meeting(_:userDidExit:)` | A member exits the meeting | `UserExitEventData` |
| `meeting(_:userCameraStateDidChange:)` | Any member (including you) turns the camera on / off | `UserCameraStateChangeEventData` |
| `meeting(_:userMicStateDidChange:)` | Any member (including you) turns the microphone on / off | `UserMicStateChangeEventData` |
| `meeting(_:userNameDidChange:)` | A member's in-meeting display name changes | `UserNameChangeEventData` |
| `meeting(_:userRoleDidChange:)` | A member's role changes, including host transfer | `UserRoleChangeEventData` |
| `meeting(_:userChatDisabledDidChange:)` | Chat is disabled / re-enabled for a member individually | `UserChatDisabledChangeEventData` |
| `meeting(_:userDrawDisabledDidChange:)` | A member is prevented from drawing / allowed again | `UserDrawDisabledChangeEventData` |
| `meeting(_:userDidHandup:)` | A member raises or lowers their hand, or responds to the host's turn-on request | `UserHandupEventData` |

When `byAdmin` in a media state event is `true`, the change was caused by a host action, and `opUid` is the operator. You can use this to show the user a hint such as "The host turned off your microphone."

`UserHandupEventData.step` tells you which step it is: `.request` raise hand, `.cancel` lower hand, `.confirmOpen` accept the request, `.rejectOpen` decline the request.

---

### Room state events

| Method | When it fires | Data type |
| --- | --- | --- |
| `meeting(_:roomMicStateDidChange:)` | The mute all setting changes | `RoomMicStateChangeEventData` |
| `meeting(_:roomCameraStateDidChange:)` | The camera off for everyone setting changes | `RoomCameraStateChangeEventData` |
| `meeting(_:roomShareStateDidChange:)` | The sharing-disabled setting changes | `RoomShareStateChangeEventData` |
| `meeting(_:roomChatDisabledDidChange:)` | The disable chat for everyone setting changes | `RoomChatDisabledChangeEventData` |
| `meeting(_:roomScreenshotDisabledDidChange:)` | The screenshot-disabled setting changes | `RoomScreenshotDisabledChangeEventData` |
| `meeting(_:roomWatermarkDisabledDidChange:)` | The watermark switch changes | `RoomWatermarkDisabledChangeEventData` |
| `meeting(_:roomLockedDidChange:)` | The meeting's lock state changes | `RoomLockedChangeEventData` |
| `meeting(_:roomTitleDidChange:)` | The meeting title is renamed, including sub-meeting renames | `RoomTitleChangeEventData` |
| `meeting(_:roomShareDidStart:)` | Someone starts sharing (screen or whiteboard) | `RoomShareStartEventData` |
| `meeting(_:roomShareDidStop:)` | Sharing ends | `RoomShareStopEventData` |
| `meeting(_:shareBroadcastDidStart:)` | iOS full-screen sharing only: the extension actually starts producing frames | `ShareBroadcastStartEventData` |
| `meeting(_:shareBroadcastDidFinish:)` | iOS full-screen sharing only: frame production ends | `ShareBroadcastStopEventData` |
| `meeting(_:roomMcuTask:)` | The state of a recording / stream mixing task changes | `RoomMcuTaskEventData` |
| `meeting(_:roomJoinDidFail:)` | A member failed to enter the meeting | `RoomJoinFailedEventData` |

For screen sharing, `roomShareDidStart` is based on the RTC media track: it's reported as soon as the remote screen track arrives, so you can render the shared video directly when you receive it.

`shareBroadcastDidStart` / `shareBroadcastDidFinish` fire only for iOS full-screen sharing, and only on the sharer's own side. They distinguish "the listener is attached" from "there is actually video"; for how to wire them up, see [Screen sharing](/en/meeting/swift/advanced/screen-sharing).

When the host turns on "mute all" or "camera off for everyone," the SDK automatically turns off the local devices of non-host members and additionally reports the corresponding member media state event.

The payload of `roomTitleDidChange` carries `title` and `previousTitle`, and both main meeting renames and sub-meeting renames (`adminUpdateSubMeetingTitle`) trigger it. It **has no `opUid`**: renaming a meeting has no dedicated broadcast command, and the event is derived by comparing titles after the channel properties are updated. The properties contain only the result, not the operator, and making up an operator would only mislead callers.

---

### Message events

| Method | When it fires | Data type |
| --- | --- | --- |
| `meeting(_:didReceiveChatMessage:)` | An in-meeting chat message is received | `RoomChatMsgEventData` |
| `meeting(_:didReceiveCustomMessage:)` | A custom business message is received | `RoomCustomMsgEventData` |

Both have an `isPrivate` flag indicating whether it's a private message, and `uid` is the sender.

---

### Host command events

| Method | When it fires | Data type |
| --- | --- | --- |
| `meeting(_:adminDidConfirmHandup:)` | The host handled a raise-hand request | `AdminConfirmHandupEventData` |
| `meeting(_:adminDidRequestOpenMic:)` | The host asks you to turn on your microphone | `AdminRequestOpenMicEventData` |
| `meeting(_:adminDidRequestOpenCamera:)` | The host asks you to turn on your camera | `AdminRequestOpenCameraEventData` |

For how to handle them, see [Raise hand and turn-on requests](/en/meeting/swift/advanced/handup).

---

### Waiting room events

| Method | When it fires | Data type |
| --- | --- | --- |
| `meeting(_:userDidEnterWaitingRoom:)` | Someone enters the waiting room | `UserEnterWaitingRoomEventData` |
| `meeting(_:userDidExitWaitingRoom:)` | Someone exits the waiting room | `UserExitWaitingRoomEventData` |
| `meeting(_:waitingRoomDisabledDidChange:)` | The waiting room switch changes | `AdminUpdateWaitingRoomDisabledEventData` |
| `meetingDidMoveToWaitingRoom(_:)` | You were moved back to the waiting room by the host | None |

---

### Sub-meeting events

| Method | When it fires | Data type |
| --- | --- | --- |
| `meeting(_:adminDidStartSubMeeting:)` | The host started the sub-meetings | `AdminStartSubMeetingEventData` |
| `meeting(_:adminDidStopSubMeeting:)` | The host ended the sub-meetings | `AdminStopSubMeetingEventData` |
| `meeting(_:adminDidMoveSubMeetingUser:)` | You were moved to another sub-meeting | `AdminMoveSubMeetingUserEventData` |

For all three events, you need to perform the switch yourself: "exit the current meeting, then enter the target meeting."

---

### Sign-in and roll call events

| Method | When it fires | Data type |
| --- | --- | --- |
| `meeting(_:signInActivity:)` | The host started a round of sign-in | `SignInActivityEventData` |
| `meeting(_:signInDidFinish:)` | The sign-in activity ended | `SignInFinishEventData` |
| `meeting(_:rollCallNamed:)` | Your name was called in a roll call | `RollCallNamedEventData` |

---

### Device events

| Method | When it fires | Data type |
| --- | --- | --- |
| `meeting(_:didAddDevice:)` | A camera / microphone / speaker is connected to the system, or an iOS audio route is added | `DeviceChangeEventData` |
| `meeting(_:didRemoveDevice:)` | A device is removed | `DeviceChangeEventData` |

Device events **don't depend on meeting state**; the SDK starts reporting them once the instance is created, so you can use them on a pre-meeting device check page.

---

### Audio routing events (iOS)

| Method | When it fires | Data type |
| --- | --- | --- |
| `meeting(_:audioRouteDidChange:)` | The output route changes: switching among earpiece / speaker / Bluetooth / wired | `AudioRouteChangeEventData` |
| `meetingAudioRouteDidRecoverFromInterruption(_:)` | Audio has **actually recovered** after an interruption by an incoming call / Siri | None |

Both callbacks exist only on iOS (their declarations are wrapped in `#if os(iOS)`), and like device events, they don't depend on meeting state.

`AudioRouteChangeEventData.reason` is the change reason given by the system, and it's more useful than the result itself when troubleshooting routing issues. Recovery from an interruption may be delayed because a system call hasn't ended or the app is still in the background; the SDK fires the event only once, after audio has actually recovered. For details, see [Audio routing](/en/meeting/swift/advanced/audio-routing).

---

### Call quality events

| Method | When it fires | Data type |
| --- | --- | --- |
| `meeting(_:didReceiveQualityReport:)` | Each time the server delivers a quality report (a real-time stream of values) | `QualityReport` |
| `meeting(_:connectionQualityDidChange:)` | The quality level jumps to a different tier (assertion-style) | `ConnectionQualityChange` |
| `meeting(_:activeSpeakersDidChange:)` | The active speakers change | `ActiveSpeakersSnapshot` |
| `meeting(_:didSwitchLayer:)` | A simulcast layer switch completes | `LayerSwitchedInfo` |

Quality is reported through **two separate feeds**; pick one based on what you need, and don't use both to drive the same UI:

+ `didReceiveQualityReport` fires on every report with the raw values (packet loss, RTT, jitter, bitrate, MOS), suitable for signal bar icons and detailed diagnostics panels
+ `connectionQualityDidChange` fires only when the level jumps to a different tier, suitable for "your network is poor" hints and proactive downgrade decisions

`activeSpeakersDidChange` gives a **full snapshot** (already sorted by volume in descending order), so just overwrite your UI with it; you don't need to merge increments yourself. When no one is speaking, `speakers` is an empty array.

The data structures of these four events are defined in the underlying SRTC module, so you need `import SRTC` to use them; for the fields, see [Types](/en/meeting/swift/types). For level determination, cold-start values, and proactive layer switching, see [SRTC · Call quality and active speakers](/en/rtc/swift/advanced/call-quality).

<Note>
These four events are available only when the meeting uses the **SeaStart (SFU)** engine—meetings that go through the CDN (Wangsu) don't have this signaling path and receive none of them.
</Note>

---

### Receive stream status events

| Method | When it fires | Data type |
| --- | --- | --- |
| `meeting(_:didChangeReceiveStreamStatus:)` | Receiving a remote video track times out / recovers | `ReceiveStreamStatus` |

It's determined **per track**: when a video track produces no frames for a period of time, a timeout is reported (`timedOut == true`), and as soon as frames resume, it's reported again (`timedOut == false`). A typical use is toggling the "loading" indicator on a video tile. When the first frame arrives after you subscribe, you first receive a recovery, which you can use to turn off the initial loading indicator.

The payload directly reuses the underlying SRTC `ReceiveStreamStatus` (requires `import SRTC`); for the fields, see [Types](/en/meeting/swift/types). It corresponds to `onReceiveStreamStatusChange:streamType:status:` in the old `MeetingKit`.

<Warning>
**Don't use `connectionQualityDidChange` in its place.** The quality tier is one value for the whole connection and tells you "whether the network is good," not "whether this tile's video has stopped": when a single track stops being published, the sender's camera freezes, or one track fails to decode, the tier can stay at excellent the whole time. Using the tier to drive a single tile's loading indicator inevitably produces false alarms.
</Warning>

<Note>
Unlike the four quality events above, this event is **available with both engines**—it's determined by whether video frames are received locally and doesn't depend on the SFU's signaling path.
</Note>

---

### Out-of-meeting message events

You need to call `enableIm()` first; see [Out-of-meeting messages](/en/meeting/swift/advanced/im).

| Method | When it fires | Data type |
| --- | --- | --- |
| `meeting(_:imCallCalling:)` | Someone in a meeting is calling you | `ImCallCallingEventData` |
| `meeting(_:imMeetingRemind:)` | Meeting start reminder | `ImMeetingRemindEventData` |
| `meeting(_:imAdminMoveOutWaitingRoom:)` | You were admitted from the waiting room | `ImAdminMoveOutWaitingRoomEventData` |
| `meeting(_:imUserHelpSubMeeting:)` | A sub-meeting is asking for help | `ImUserHelpSubMeetingEventData` |
| `meetingImIsReconnecting(_:)` | The out-of-meeting message path starts reconnecting | None |
| `meetingImDidReconnect(_:)` | The out-of-meeting message path reconnected successfully | None |
| `meeting(_:imDidDisconnect:)` | The out-of-meeting message path disconnected | `ImDisconnectEventData` |

These connection events and the meeting connection events above belong to two independent paths; don't mix them up.

---

### Event identifier enums

The SDK also exposes two enums that list the string identifier of each event:

+ `RoomEventType`—in-meeting event identifiers, such as `user_enter` and `room_share_start`
+ `ImEventType`—out-of-meeting message event identifiers, such as `call_calling`

On the Swift side, events are dispatched through the `SMeetingDelegate` methods above. You don't need these two enums in a normal integration; they're useful only when you need logging instrumentation or want to align event naming with other platforms.

---

### Related pages

+ [Key concepts](/en/meeting/swift/key-concepts)
+ [Types](/en/meeting/swift/types)
+ [Error handling](/en/meeting/swift/error-codes)
