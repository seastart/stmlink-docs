---
title: "Quickstart"
description: "The minimal Android SRTC flow in Kotlin: create and initialize RTCEngine, register channel and media callbacks, join a channel, explicitly start camera/microphone/screen capture and publish, subscribe to remote video, then leave and release resources. Read after completing integration."
---

This page walks through the minimal working flow of the Android SRTC SDK in this order: create the Engine → bind callbacks → join a channel → start capture and publish → subscribe to remote media → leave and release.

Before you start, complete the following:

+ Configure the Maven repository, SDK dependency, and basic environment as described in [Integration](/en/rtc/android/integration).
+ Prepare a channel `token` issued by your server.
+ Request camera and microphone runtime permissions in your app.
+ To manage output devices such as the speaker, earpiece, or Bluetooth headsets, see [Audio routing](/en/rtc/android/advanced/audio-routing).

Use `cn.seastart.rtc.media.original.render.VcsPlayerGlTextureView` or `VcsPlayerGlSurfaceView` for preview and remote display views, with this package path in both code imports and XML layouts.

## Step 1: Create and initialize `RTCEngine`

`RTCEngine.create(...)` requires an Engine-level error listener. It receives errors that don't belong to any channel callback, as well as blocking errors such as calling a channel that hasn't started; `channelId` is `null` when it can't be determined.

```kotlin
private lateinit var rtcEngine: RTCEngine

fun initRtcSdk(application: Application) {
    rtcEngine = RTCEngine.create(
        app = application,
        enableLocalLog = true,
        engineEvent = object : RTCEngineSimpleEvent() {
            override fun onError(channelId: String?, errorCode: Int, message: String?) {
                // Log or display Engine errors in one place
            }
        },
        localLogPath = null,
        version = "app: ${BuildConfig.VERSION_NAME}"
    )
    rtcEngine.initSDK()
}
```

For full parameter descriptions, see [RTCEngine](/en/rtc/android/api-reference/RTCEngine) and [RTCEngineEvent](/en/rtc/android/api-reference/RTCEngineEvent).

## Step 2: Prepare channel and media callbacks

Every `join(...)` call takes its own `RTCClientEvent` for that channel. If you only override a few events, extend `RTCClientSimpleEvent` instead of implementing the full interface.

```kotlin
private val clientEvent = object : RTCClientSimpleEvent() {
    override fun onJoinSucceed(channel: String, uid: String, whiteBoard: String?) {
        // Actually joined the channel; update the UI or start publishing here
    }

    override fun onJoinFailed(channel: String?, statusCode: Int, message: String) {
        // Failed to join; see the error codes page for statusCode
    }

    override fun onRemoteUserJoin(channel: String, uid: String) {
        // Maintain the user list for this channel
    }

    override fun onStreamTrackAdd(
        uid: String,
        channel: String,
        trackId: String,
        trackDesc: String
    ) {
        subscribeRemoteVideo(uid, trackId, trackDesc)
    }

    override fun onDisconnected(
        channel: String,
        leaveReason: LeaveReason,
        statusCode: Int,
        message: String
    ) {
        // An unrecoverable disconnect occurred in this channel
    }
}

rtcEngine.setRtcMediaEvent(object : RTCMediaSimpleEvent() {
    override fun onMediaConnected(channel: String) {
        // Connected to the media server of the default channel
    }

    override fun onVolumesReport(
        channel: String,
        volumes: MutableMap<UserTrackDesc, VolumeInfo>
    ) {
        // Channel volume info, useful for highlighting the active speaker
    }
})
```

Every channel-level callback explicitly carries `channel`. Even if a listener is bound to only one `RTCChannel`, use this parameter to keep logs and state separated. For more definitions, see [RTCClientEvent](/en/rtc/android/api-reference/RTCClientEvent) and [RTCMediaEvent](/en/rtc/android/api-reference/RTCMediaEvent).

## Step 3: Join a channel

`join(...)` synchronously returns `RTCChannel?`:

+ A non-null return only means the SDK accepted the request and created a channel handle, not that the join succeeded.
+ The actual result is reported by `onJoinSucceed(...)` or `onJoinFailed(...)`.
+ If the SDK isn't initialized or has been released, it synchronously throws `SdkNotInitializedException`.

```kotlin
private var defaultChannel: RTCChannel? = null

fun joinChannel(token: String) {
    defaultChannel = rtcEngine.join(
        token = token,
        clientEvent = clientEvent,
        options = JoinOptions(
            autoSubscribeAudio = true,
            autoSubscribeVideo = false
        )
    )

    if (defaultChannel == null) {
        // The request was rejected before the channel session was created; the reason is still reported via onJoinFailed
    }
}
```

The first `join` creates the default channel, and the flat APIs on `RTCEngine`—publish, subscribe, query, `leave()`, and so on—all act on it. The SDK also supports joining multiple channels at the same time; this quickstart covers only the single-channel flow. For details, see [Multi-channel](/en/rtc/android/advanced/multi-channel).

## Step 4: Start local capture and publish

Run the following publishing flow after `onJoinSucceed(...)`. Capture and publishing are two separate actions: explicitly start local capture first, then publish the same local track to the channel. Unpublishing doesn't automatically stop shared capture; when you no longer need the device, also call the track's `stopCapture()`.

### 4.1 Camera capture and publishing

```kotlin
private lateinit var cameraTrack: LocalCameraTrack

fun startCamera(previewView: VcsPlayerGlTextureView) {
    cameraTrack = rtcEngine.getLocalCameraTrack(PreOptionCamera._720P)
    cameraTrack.addPlayView(previewView)
    cameraTrack.startCapture(object : RTCResultListener {
        override fun onSuccess() {
            rtcEngine.publishLocalVideo(
                track = cameraTrack,
                publishCustomOpt = PublishCustomOptions(
                    desc = TrackDesc.TRACK_MAIN.value,
                    props = null,
                    simulcasts = null
                ),
                listener = null
            )
        }

        override fun onFail(code: Int, message: String) {
            // For example, the CAMERA permission wasn't granted
        }
    })
}
```

For details, see [LocalCameraTrack](/en/rtc/android/api-reference/LocalCameraTrack).

### 4.2 Microphone capture and publishing

The microphone capture module is decoupled from joining and publishing. `publishLocalAudio(...)` no longer opens the microphone; you must call `LocalMicTrack.startCapture(...)` first.

```kotlin
private lateinit var micTrack: LocalMicTrack

fun startMicrophone() {
    micTrack = rtcEngine.getLocalMicTrack(PreOptionMic.def)
    micTrack.startCapture(object : RTCResultListener {
        override fun onSuccess() {
            rtcEngine.publishLocalAudio(
                track = micTrack,
                publishCustomOpt = PublishCustomOptions(
                    desc = TrackDesc.TRACK_AUDIO.value,
                    props = null,
                    simulcasts = null
                ),
                listener = null
            )
        }

        override fun onFail(code: Int, message: String) {
            // For example, the RECORD_AUDIO permission wasn't granted or the microphone failed to open
        }
    })
}
```

Explicit capture also works outside a channel. Set `setRtcLocalAudioFrameEvent(...)` first, then call `micTrack.startCapture(...)` to receive local PCM data for recording or processing; registering the callback alone doesn't open the microphone. See [LocalMicTrack](/en/rtc/android/api-reference/LocalMicTrack) and [RTCEngine](/en/rtc/android/api-reference/RTCEngine#setrtclocalaudioframeevent-e).

### 4.3 Screen sharing (optional)

```kotlin
val screenTrack = rtcEngine.getLocalScreenTrack(this, PreOptionScreen.def)

screenTrack.setEvent(object : RTCScreenStateEvent {
    override fun onScreenCaptureStateChanged(state: ScreenCaptureState, args: String?) {
        when (state) {
            ScreenCaptureState.START -> Unit // Screen capture is established
            ScreenCaptureState.STOP -> Unit  // Screen capture has stopped
            ScreenCaptureState.ERROR -> Unit // args contains the error info
        }
    }
})

screenTrack.request { granted, intent ->
    if (granted && intent != null) {
        screenTrack.startCapture(intent, object : RTCResultListener {
            override fun onSuccess() {
                // This only means the SDK accepted the start request; the actual state is reported by RTCScreenStateEvent
                rtcEngine.publishLocalVideo(
                    track = screenTrack,
                    publishCustomOpt = PublishCustomOptions(
                        desc = TrackDesc.TRACK_SHARE.value,
                        props = null,
                        simulcasts = null
                    ),
                    listener = null
                )
            }

            override fun onFail(code: Int, message: String) {
                // For example, a duplicate start or the current lifecycle state doesn't allow starting
            }
        })
    }
}
```

For API details, see [LocalScreenTrack](/en/rtc/android/api-reference/LocalScreenTrack).

## Step 5: Subscribe to and play remote media

After receiving `onStreamTrackAdd(...)`, get the remote track from the default channel, bind a render view, then subscribe:

```kotlin
private fun subscribeRemoteVideo(uid: String, trackId: String, trackDesc: String) {
    val remoteTrack = rtcEngine.getRemoteVideoTrack(uid, trackDesc)
    remoteTrack?.addPlayView(remoteView)

    rtcEngine.subscribeRemoteTrack(
        uid = uid,
        trackId = trackId,
        preferTrackIds = null,
        result = object : RTCResultListener {
            override fun onSuccess() = Unit
            override fun onFail(code: Int, message: String) {
                // Subscription failed
            }
        }
    )
}

// Put this in the clientEvent implementation above
override fun onStreamTrackRemove(uid: String, channel: String, trackInfo: TrackInfo) {
    rtcEngine.unSubscribeRemoteTrack(uid, trackInfo.id)
    rtcEngine.getRemoteVideoTrack(uid, trackInfo.desc)?.removePlayView(remoteView)
}
```

For details, see [RemoteVideoTrack](/en/rtc/android/api-reference/RemoteVideoTrack).

## Step 6: Leave the channel and release resources

```kotlin
// First, unpublish from the default channel
rtcEngine.unPublishLocalAudio(micTrack, null)
rtcEngine.unPublishLocalVideo(cameraTrack, null)

// Then close the shared capture devices
micTrack.stopCapture()
cameraTrack.stopCapture()

// Leave the default channel; you can also call defaultChannel?.leave()
rtcEngine.leave()

// Release the Engine when the app no longer uses RTC
rtcEngine.releaseSDK()
```

`releaseSDK()` releases all channels and shared resources from the current initialization cycle; you can call `initSDK()` again afterward.

## More capabilities

+ Joining multiple channels concurrently, per-channel publishing and subscription, and resource isolation: [Multi-channel](/en/rtc/android/advanced/multi-channel)
+ Microphone input device enumeration, switching, and PCM callbacks: [LocalMicTrack](/en/rtc/android/api-reference/LocalMicTrack)
+ Custom video publishing: [Custom tracks](/en/rtc/android/advanced/custom-track)
+ Whiteboard: [Whiteboard](/en/rtc/whiteboard)
+ Audio output device management: [Audio routing](/en/rtc/android/advanced/audio-routing)
+ Full SDK API: [RTCEngine](/en/rtc/android/api-reference/RTCEngine)
