---
title: "Raise hand and turn-on requests"
description: "The full request flows in the SMeeting Swift SDK: members raise a hand to ask for the microphone, camera, speaking, or sharing and the host approves; the host asks members to turn on their microphone or camera and members accept or decline. Read when building raise-hand or host invitation UI."
---

### Overview

A meeting has two "request" flows that go in opposite directions and are easy to confuse. Tell them apart first:

| Flow | Direction | Member-side API | Host-side API |
| --- | --- | --- | --- |
| Raise hand | Member → host | `requestHandup(_:)` / `cancelHandup(_:)` | `adminConfirmHandup(targetId:approve:code:)` |
| Turn-on request | Host → member | `requestOpenMic(byAdmin:adminUid:)` / `rejectOpenMic(adminUid:)` | `adminRequestUserOpenMic(targetId:)` |

`HandupType` has four raise-hand types: `.mic` asks to turn on the microphone, `.camera` asks to turn on the camera, `.chat` asks for the right to speak, and `.share` asks to share.

---

### Members raise a hand

```swift
// Ask to turn on the microphone
try await meeting.requestHandup(.mic)

// Cancel the request
try await meeting.cancelHandup(.mic)
```

---

### The host receives a raised hand

```swift
func meeting(_ meeting: SMeetingEngine, userDidHandup data: UserHandupEventData) {
    // data.uid  the member who raised a hand
    // data.type raise-hand type
    // data.step step of the action
}
```

`UserHandupStep` indicates which step of the flow the event is at:

| Step | Description |
| --- | --- |
| `.request` | The member raises a hand |
| `.cancel` | The member lowers the hand |
| `.confirmOpen` | The member accepted the host's turn-on request |
| `.rejectOpen` | The member declined the host's turn-on request |

In other words, this one event carries two kinds of notifications—"raise-hand requests" and "responses to the host's request"—and you handle them differently based on `step`.

---

### The host approves a raised hand

```swift
try await meeting.adminConfirmHandup(targetId: data.uid, approve: true, code: .mic)
```

The approval result is delivered to the relevant members through an event:

```swift
func meeting(_ meeting: SMeetingEngine, adminDidConfirmHandup data: AdminConfirmHandupEventData) {
    // data.targetId the member being approved
    // data.approve  whether it's approved
    // data.type     raise-hand type
    // data.opUid    the host who approved
}
```

Approval **doesn't** turn on the member's microphone or camera automatically—after receiving this event, the member side needs to call `requestOpenMic()` / `requestOpenCamera()` itself.

---

### The host asks a member to turn on media

```swift
try await meeting.adminRequestUserOpenMic(targetId: user.uid)
try await meeting.adminRequestUserOpenCamera(targetId: user.uid)
```

The member side receives:

```swift
func meeting(_ meeting: SMeetingEngine, adminDidRequestOpenMic data: AdminRequestOpenMicEventData) {
    // data.opUid the host who sent the request
}

func meeting(_ meeting: SMeetingEngine, adminDidRequestOpenCamera data: AdminRequestOpenCameraEventData) {
    // data.opUid
}
```

To accept, pass `byAdmin: true` together with `adminUid` to the turn-on API, so the SDK takes the "respond to the request" path instead of "request on your own":

```swift
try await meeting.requestOpenMic(byAdmin: true, adminUid: data.opUid)
try await meeting.requestOpenCamera(byAdmin: true, adminUid: data.opUid)
```

To decline:

```swift
try await meeting.rejectOpenMic(adminUid: data.opUid)
try await meeting.rejectOpenCamera(adminUid: data.opUid)
```

Whether the member accepts or declines, the host side receives a `userDidHandup` with `step` set to `.confirmOpen` or `.rejectOpen`.

---

### The host turns off a member's devices directly

Turning off doesn't require consent:

```swift
try await meeting.adminCloseUserMic(targetId: user.uid)
try await meeting.adminCloseUserCamera(targetId: user.uid)
```

The affected member's SDK stops the stream automatically and reports `userMicStateDidChange` / `userCameraStateDidChange` once, with `byAdmin` set to `true` and `opUid` set to the operator; you can use this to show the user a message such as "The host turned off your microphone."

---

### A complete interaction example

```swift
// Member side
func meeting(_ meeting: SMeetingEngine, adminDidRequestOpenMic data: AdminRequestOpenMicEventData) {
    Task { @MainActor in
        showConfirmDialog(
            title: "The host is asking you to unmute",
            onAccept: { Task { try? await meeting.requestOpenMic(byAdmin: true, adminUid: data.opUid) } },
            onReject: { Task { try? await meeting.rejectOpenMic(adminUid: data.opUid) } }
        )
    }
}
```

---

### Related pages

+ [Media control](/en/meeting/swift/advanced/media-control)
+ [Host controls](/en/meeting/swift/advanced/host-controls)
+ [Events](/en/meeting/swift/events)
