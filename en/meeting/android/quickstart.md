---
title: "Quickstart"
description: "Use SMeeting Android 2.0.39 to initialize MeetingEngine, create a meeting, register in-meeting events, enter and exit the meeting, publish the local camera and mic, and subscribe to remote video. Read this after adding the dependency."
---

## Prerequisites

+ Add `cn.seastart.meeting:meeting:2.0.39` as described in [Integration](/en/meeting/android/integration).
+ Get a `meetToken` from your backend. Don't store the secret key used to generate tokens in the client.
+ Request the camera and audio recording runtime permissions in your app.
+ Prepare the `streamVendor` agreed for your deployment. The example uses `wangsucdn`; the actual value depends on your backend configuration.

## 1. Create and initialize the Engine

Your app should hold a single `MeetingEngine` in one place. Callbacks stay on the thread they actually come from; switch to the main thread before any UI operation.

```kotlin
private lateinit var meetingEngine: MeetingEngine

fun initMeeting(application: Application, meetToken: String) {
    meetingEngine = MeetingEngine.create(application)
    meetingEngine.initSdk(
        meetToken,
        null,
        object : MeetingResultCallback {
            override fun onSuccess() {
                // The SDK is ready
            }

            override fun onFailure(errorCode: Int, message: String?) {
                // message is for diagnostics only; build user-facing text from errorCode
            }
        }
    )
}
```

Release the Engine when you no longer use the SDK:

```kotlin
fun releaseMeeting() {
    meetingEngine.release()
}
```

## 2. Create a meeting

When an instant meeting is created successfully, `MeetingCreatedBean` is returned directly; the `Data<T>` network wrapper is no longer exposed.

```kotlin
val option = CreateImmediateMeetingOption(
    content = "Product review",
    attendType = AttendType.ATTEND_NOT_LIMIT,
    mode = MeetingMode.Normal,
    entryMutePolicy = MuteState.MuteState3
)

meetingEngine.createImmediateMeeting(
    "Weekly project sync",
    option,
    object : MeetingValueResultCallback<MeetingCreatedBean> {
        override fun onSuccess(value: MeetingCreatedBean) {
            val meetingId = value.meetingId
            val roomNo = value.roomNo
        }

        override fun onFailure(errorCode: Int, message: String?) {
            // Creation failed
        }
    }
)
```

For scheduled meetings, use `createScheduleMeeting()`, where `planTime` is a Unix timestamp in seconds and `planDur` is in minutes.

## 3. Register in-meeting events

Assign room, member, message, and media events before entering the meeting so you don't miss the initial events; they are cleared automatically after you exit the meeting.

```kotlin
meetingEngine.roomEvent = object : MeetingRoomSimpleEvent() {
    override fun onDisconnected(
        reason: LeaveReason,
        statusCode: Int,
        message: String?
    ) {
        // The meeting is actually disconnected
    }
}

meetingEngine.userEvent = object : MeetingUserSimpleEvent() {
    override fun onUserEnter(uid: String) {
        val member = meetingEngine.infosManager.getMemberByUid(uid)
        // Refresh the member list
    }

    override fun onTrackAdded(uid: String, trackInfo: TrackInfo) {
        // Decide whether to subscribe based on trackInfo.desc
    }
}
```

For the full list of events, see [Meeting events overview](/zh/meeting/android/api-reference/meeting-events) (Chinese).

## 4. Enter and exit the meeting

A successful entry returns `MeetingEnterInfo`. In-meeting APIs are still called on `MeetingEngine`; don't reference the SDK's internal `MeetingSession`.

```kotlin
meetingEngine.enterMeeting(
    activity = this,
    roomNo = "10000001",
    password = null,
    nick = "Alice",
    avatar = "",
    streamVendor = "wangsucdn",
    isAudience = false,
    extendInfo = null,
    callback = object : MeetingValueResultCallback<MeetingEnterInfo> {
        override fun onSuccess(value: MeetingEnterInfo) {
            val meetingId = value.meetingId
            val myUid = value.uid
            // Server-side meeting entry and SRTC join are complete
        }

        override fun onFailure(errorCode: Int, message: String?) {
            // Failed to enter the meeting
        }
    }
)
```

To enter by meeting ID, use `enterMeetingByMeetingId()`; the other parameters are the same. To exit the meeting, call:

```kotlin
meetingEngine.exitMeeting()
```

## 5. Open and publish the camera and mic

`openCamera()` / `openMic()` only do local capture before the meeting; after entering, you must use `openCameraAndPublish()` / `openMicAndPublish()` to publish to the meeting.

```kotlin
meetingEngine.openCameraAndPublish(
    localPreview,
    PreOptionCamera._480P,
    object : MeetingResultCallback {
        override fun onSuccess() {
            // The camera is capturing and published
        }

        override fun onFailure(errorCode: Int, message: String?) {
            // This publish and capture have been rolled back
        }
    }
)

meetingEngine.openMicAndPublish(
    PreOptionMic.def,
    object : MeetingResultCallback {
        override fun onSuccess() {
            // The mic is capturing and published
        }

        override fun onFailure(errorCode: Int, message: String?) {
            // This publish and capture have been rolled back
        }
    }
)
```

Close the devices:

```kotlin
meetingEngine.closeCamera()
meetingEngine.closeMic()
```

Remote video must be rendered with `VcsPlayerGlTextureView` or `VcsPlayerGlSurfaceView`; a plain Android `TextureView` / `SurfaceView` doesn't work.

## 6. Subscribe to remote video

Look up the track from `InfosManager`, then get the `RemoteVideoTrack` through the asynchronous result callback.

```kotlin
val targetUid = "remote-user-001"
val trackInfo = meetingEngine.infosManager
    .getTrackInfoByTrackDesc(targetUid, TrackDesc.TRACK_MAIN.value)
    ?: return

meetingEngine.startPlayRemoteVideo(
    uid = targetUid,
    trackDesc = trackInfo.desc,
    view = remoteView,
    event = object : MeetingRemoteVideoSimpleEvent() {
        override fun onReceiveStreamStatusChange(
            uid: String,
            trackDesc: String,
            isChoke: Boolean
        ) {
            // Update the stutter indicator
        }
    },
    callback = object : MeetingValueResultCallback<RemoteVideoTrack> {
        override fun onSuccess(value: RemoteVideoTrack) {
            // Subscribed; you can keep using value to manage the render view
        }

        override fun onFailure(errorCode: Int, message: String?) {
            // Subscription failed
        }
    }
)
```

Unsubscribe:

```kotlin
meetingEngine.stopPlayRemoteVideo(targetUid, trackInfo.desc)
```

## Next steps

+ [MeetingEngine](/zh/meeting/android/api-reference/MeetingEngine) (Chinese): all public methods, parameters, and return values
+ [Model types](/zh/meeting/android/types) (Chinese): configuration and result models
+ [Error codes](/en/meeting/android/error-codes): handling `202xxx` and passed-through errors
+ [Camera presets](/zh/meeting/android/presets/camera) (Chinese): choosing resolution and bitrate
+ [Audio routing](/zh/meeting/android/advanced/audio-routing) (Chinese): speaker, earpiece, Bluetooth, and wired headsets
