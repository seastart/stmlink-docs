---
title: "Meeting events overview"
description: "How SMeeting Android splits ongoing events into Engine, IM, device, room, member, message, media, and raw-frame interfaces, their lifecycles and callback threads, and which interface to register for each need. Read this before registering in-meeting events."
---

SMeeting Android splits ongoing events by scope into Engine, IM, device, room, member, message, media, and other interfaces. Most events are registered through nullable properties on `MeetingEngine`; events for a single remote video are registered through a parameter of the subscribe method.

## Usage notes

+ Engine, IM, camera device, and mic device events share the `MeetingEngine` lifecycle; assigning `null` stops new dispatches.
+ Room, member, message, and media events are bound to the current meeting and cleared automatically when you exit the meeting; reassign them for the next meeting.
+ `MeetingRemoteVideoEvent` is passed in with a single remote subscription and stops dispatching after you unsubscribe or exit the meeting.
+ Callbacks stay on the actual source thread of SRTC, IM, or the network and are not switched to the Android main thread automatically.
+ Local and remote raw-frame callbacks run on high-frequency media threads; don't perform blocking operations in them.
+ Each event group provides a corresponding `MeetingXxxSimpleEvent` empty implementation, so you only override the methods you actually care about.

## Registration example

```kotlin
engine.engineEvent = object : MeetingEngineSimpleEvent() {
    override fun onError(errorCode: Int, message: String?) {
        // Log global runtime errors
    }
}

engine.userEvent = object : MeetingUserSimpleEvent() {
    override fun onUserEnter(uid: String) {
        // Refresh the member list
    }
}
```

## Choosing an event interface

| Event interface | When to use |
| --- | --- |
| [MeetingEngineEvent](/en/meeting/android/api-reference/MeetingEngineEvent) | Global Engine runtime errors |
| [MeetingImEvent](/en/meeting/android/api-reference/MeetingImEvent) | IM connection, reconnection, calls, and reminders |
| [MeetingCameraDeviceEvent](/en/meeting/android/api-reference/MeetingCameraDeviceEvent) | Camera list, disconnection, and runtime errors |
| [MeetingMicDeviceEvent](/en/meeting/android/api-reference/MeetingMicDeviceEvent) | Mic list and invalidation of the current device |
| [MeetingScreenCaptureEvent](/en/meeting/android/api-reference/MeetingScreenCaptureEvent) | Android local screen capture state |
| [MeetingRoomEvent](/en/meeting/android/api-reference/MeetingRoomEvent) | Room configuration, connection, recording, sharing, sub-meetings, and sign-in |
| [MeetingUserEvent](/en/meeting/android/api-reference/MeetingUserEvent) | Members, roles, permissions, device state, waiting room, and tracks |
| [MeetingMessageEvent](/en/meeting/android/api-reference/MeetingMessageEvent) | Chat, system messages, and app extension messages |
| [MeetingMediaEvent](/en/meeting/android/api-reference/MeetingMediaEvent) | Media connection, remote frames, statistics, volume, and network quality |
| [MeetingLocalVideoFrameEvent](/en/meeting/android/api-reference/MeetingLocalVideoFrameEvent) | Local YUV video frames |
| [MeetingLocalAudioFrameEvent](/en/meeting/android/api-reference/MeetingLocalAudioFrameEvent) | Local PCM audio frames |
| [MeetingRemoteVideoEvent](/en/meeting/android/api-reference/MeetingRemoteVideoEvent) | Receive and stutter state of a single remote video |
