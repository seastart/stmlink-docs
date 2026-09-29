---
title: "Multi-channel"
description: "Join multiple channels at once with one Android RTCEngine: per-channel RTCChannel handles and callbacks, shared camera/microphone capture published per channel, per-channel subscription, leaving and releasing, and error handling. Read when your app must be in several channels at once."
---

The Android SRTC SDK lets a single `RTCEngine` join multiple channels at the same time within one initialization cycle. Each `join(...)` returns an `RTCChannel` handle. Local camera, microphone, and screen capture are shared by the Engine, while each channel's signaling, media streaming session, users, remote tracks, and statistics are independent of one another.

## Objects and scopes

| Object or capability | Scope | Description |
| --- | --- | --- |
| `RTCEngine` | App / SDK initialization cycle | Manages the SDK lifecycle, IM, shared capture devices, and all channels. |
| First `RTCChannel` | Default channel | The flat channel APIs on `RTCEngine` delegate to it. |
| Subsequent `RTCChannel` | A single additional channel | Publishing, subscription, queries, statistics, and leaving affect only that channel. |
| Local Camera / Mic / Screen Track | Shared by the Engine | Start capture only once; the same track can be published to multiple channels. |
| `RTCClientEvent` / `RTCMediaEvent` | A single channel | Callbacks still carry the `channel` parameter, so you can reuse listeners and verify which channel an event belongs to. |
| Device events, PCM / local video frame events | Engine-global | Joining multiple channels doesn't produce duplicate device-level callbacks. |

:::note
The first `join` is the "default channel", not the first channel to reach `onJoinSucceed`. After the default channel is left, the next newly created channel can take the default slot. Multi-channel apps should always keep and use the `RTCChannel` returned by each `join`, rather than relying on the flat APIs to infer the target channel.
:::

## Integration flow

### 1. Create the Engine

Multiple channels need only one `RTCEngine`:

```kotlin
val rtcEngine = RTCEngine.create(
    app = application,
    enableLocalLog = true,
    engineEvent = object : RTCEngineSimpleEvent() {
        override fun onError(channelId: String?, errorCode: Int, message: String?) {
            // When channelId has a value, route to the corresponding channel; null means an Engine-global error
        }
    }
)
rtcEngine.initSDK()
```

### 2. Start shared capture

Capture and per-channel publishing are independent. The following tracks are shared within the Engine and started only once:

```kotlin
val cameraTrack = rtcEngine.getLocalCameraTrack(PreOptionCamera._720P)
val micTrack = rtcEngine.getLocalMicTrack(PreOptionMic.def)

cameraTrack.startCapture(object : RTCResultListener {
    override fun onSuccess() {
        // Record that the camera is ready
    }
    override fun onFail(code: Int) {
        // Handle camera start failure
    }
})
micTrack.startCapture(object : RTCResultListener {
    override fun onSuccess() {
        // Record that the microphone is ready
    }
    override fun onFail(code: Int) {
        // Handle microphone start failure
    }
})
```

Wait for each `RTCResultListener.onSuccess()` before publishing. Setting a local audio frame listener alone doesn't open the microphone; if you need PCM, you still have to call `micTrack.startCapture(...)`.

### 3. Create callbacks for each channel and join

The initial `RTCClientEvent` must be passed in through this `join(...)` call, because the join success or failure event may follow immediately. `RTCChannel.setRtcClientEvent(...)` is only for replacing or unbinding the listener after the join succeeds.

```kotlin
private val channels = mutableMapOf<String, RTCChannel>()

private fun joinOneChannel(key: String, activity: Activity, token: String) {
    val clientEvent = object : RTCClientSimpleEvent() {
        override fun onJoinSucceed(channel: String, uid: String, whiteBoard: String?) {
            val rtcChannel = channels[key] ?: return

            // Publish the same shared capture tracks to each channel separately
            rtcChannel.publishLocalVideo(
                cameraTrack,
                PublishCustomOptions(TrackDesc.TRACK_MAIN.value, null, null),
                null
            )
            rtcChannel.publishLocalAudio(
                micTrack,
                PublishCustomOptions(TrackDesc.TRACK_AUDIO.value, null, null),
                null
            )
        }

        override fun onJoinFailed(channel: String?, statusCode: Int) {
            channels.remove(key)
        }

        override fun onStreamTrackAdd(
            uid: String,
            channel: String,
            trackId: String,
            trackDesc: String
        ) {
            subscribeVideo(key, uid, trackId, trackDesc)
        }

        override fun onDisconnected(
            channel: String,
            leaveReason: LeaveReason,
            statusCode: Int,
            message: String
        ) {
            // Clean up only the UI and app state for this channel
        }
    }

    val rtcChannel = rtcEngine.join(
        activity = activity,
        token = token,
        clientEvent = clientEvent,
        options = JoinOptions(autoSubscribeAudio = true, autoSubscribeVideo = false)
    ) ?: return

    channels[key] = rtcChannel
    rtcChannel.setRtcMediaEvent(object : RTCMediaSimpleEvent() {
        override fun onMediaConnected(channel: String) {
            // Media connection for this channel succeeded
        }

        override fun onMediaMetric(channel: String, metric: MediaMetric.Metric) {
            // Each channel has its own statistics snapshot
        }
    })
}
```

The SDK guarantees that `onJoinSucceed(...)` is dispatched only after `join(...)` returns. A non-null handle only means the request was accepted; channel operations such as publishing and subscribing called before the success callback are blocked with `CHANNEL_NOT_START`.

### 4. Subscribe and render per channel

Remote tracks must be obtained and subscribed through the same `RTCChannel` that produced the event:

```kotlin
private fun subscribeVideo(
    key: String,
    uid: String,
    trackId: String,
    trackDesc: String
) {
    val rtcChannel = channels[key] ?: return
    val remoteTrack = rtcChannel.getRemoteVideoTrack(uid, trackDesc)
    remoteTrack?.addPlayView(remoteViewFor(key, uid, trackDesc))
    rtcChannel.subscribeRemoteTrack(uid, trackId, null, null)
}
```

Don't take a `uid` / `trackId` from channel A and query or subscribe with it on channel B's handle. Even if the strings are identical, users, tracks, and media state are not shared between the two channel sessions.

## Shared capture and per-channel publishing

Capture, publishing, and muting are three different layers:

| Operation | Scope | Typical use |
| --- | --- | --- |
| `track.startCapture(...)` / `stopCapture()` | The data source shared by all channels | Open or close the physical device. |
| `channel.publishLocalAudio/Video(...)` | The current channel | Decide whether to send the shared capture data into that channel. |
| `channel.enableLocalAudio(track, false)` | Published audio in the current channel | Frequent muting without removing the remote track. |
| `channel.unPublishLocalAudio/Video(...)` | The current channel | Stop publishing to that channel without closing shared capture. |

So unpublishing in channel A doesn't affect channel B, but calling `micTrack.stopCapture()` or `cameraTrack.stopCapture()` closes the shared data source, and every channel still publishing that track loses its capture data.

## Leaving and releasing

To leave a single channel, call its handle; other channels are unaffected:

```kotlin
channels.remove("channel-a")?.leave()
```

When you're done with everything, first unpublish and leave channel by channel, then close shared capture, and finally release the Engine:

```kotlin
channels.values.toList().forEach { channel ->
    channel.unPublishLocalAudio(micTrack, null)
    channel.unPublishLocalVideo(cameraTrack, null)
    channel.leave()
}
channels.clear()

micTrack.stopCapture()
cameraTrack.stopCapture()
rtcEngine.releaseSDK()
```

`releaseSDK()` releases all channels and shared resources in the current initialization cycle as a fallback. To use the SDK again, call `initSDK()` again.

## Failures and error handling

+ `join(...)` returns `null`: the request was rejected before the channel session was created; the status code from this call's `onJoinFailed(...)` is still authoritative.
+ Joining the same channel twice: `onJoinFailed(channel, RtcChannelErrorCode.CHANNEL_ALREADY_EXISTS)` (`102208`); the existing channel and listener are unaffected.
+ SDK not initialized or already released: `join(...)` synchronously throws `SdkNotInitializedException`.
+ Asynchronous operations that fail after joining: reported through each operation's `RTCResultListener.onFail(code)`.
+ Operations blocked by the Engine or global errors: reported through `RTCEngineEvent.onError(channelId, errorCode, message)`.
+ Channel disconnects and reconnects: distinguished by `onDisconnected`, `onReconnecting`, and `onReconnected`, which carry the `channel` parameter.

For error code ownership and the `102xxx` domain constants, see [Error codes](/en/rtc/android/error-codes). For the full channel API, see [RTCChannel](/en/rtc/android/api-reference/RTCChannel).
