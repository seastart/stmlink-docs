---
title: "RTCChannel"
description: "API reference for RTCChannel, the Android handle for a single channel returned by RTCEngine.join(...): lifecycle, listeners, user and track queries, publishing, subscription, ASR, and media statistics, all isolated per channel. Read when working with multiple channels or per-channel operations."
---

`RTCChannel` is returned by `RTCEngine.join(...)`, and all of its methods act only on the channel session bound to that handle. The first `join` returns the default channel handle; the flat channel APIs retained on `RTCEngine` operate on the same session as this handle.

A non-null handle only means the SDK accepted the join request. Call publishing, subscription, and info queries after `RTCClientEvent.onJoinSucceed(...)`.

## Identity and lifecycle

### channelId

```kotlin
val channelId: String?
```

The channel ID. If the token can be parsed, it may be available before the join succeeds; otherwise it's filled in by the success callback. Don't treat a non-null value as a successful join.

### leave()

```kotlin
fun leave()
```

Leaves and tears down the current channel without affecting other channels or shared capture devices.

### resume()

```kotlin
fun resume()
```

Immediately triggers a heartbeat check for the current channel after the app resumes from a state such as screen-off.

## Listeners

```kotlin
fun setRtcClientEvent(e: RTCClientEvent?)
fun setRtcMediaEvent(e: RTCMediaEvent?)
```

+ `setRtcClientEvent`: replaces or unbinds the channel control listener after the join succeeds. The initial listener must be passed to `join(...)`.
+ `setRtcMediaEvent`: replaces or unbinds the media listener for the current channel; you can set it after `join(...)` returns the handle.

## Channel, user, and track queries

```kotlin
fun getChannelInfo(): ChannelInfo?
fun getMeInfo(): UserInfo?
fun isAudience(): Boolean
fun getUserInfos(): MutableList<UserInfo>
fun getUserInfo(uid: String): UserInfo?
fun getTrackInfos(uid: String): List<TrackInfo>
fun getTrackInfoByTrackDesc(uid: String, trackDesc: String): TrackInfo?
fun getTrackInfoByTrackId(uid: String, trackId: String): TrackInfo?
```

These queries read only the current channel's data. When not joined or the target doesn't exist, nullable methods return `null` and list methods return an empty list; `isAudience()` returns `false` when not joined.

## Publish local tracks

```kotlin
fun publishLocalVideo(
    track: LocalVideoTrack,
    publishCustomOpt: PublishCustomOptions?,
    listener: RTCResultListener?
)

fun publishLocalAudio(
    track: LocalAudioTrack,
    publishCustomOpt: PublishCustomOptions?,
    listener: RTCResultListener?
)

fun unPublishLocalVideo(track: LocalVideoTrack, listener: RTCResultListener?)
fun unPublishLocalAudio(track: LocalAudioTrack, listener: RTCResultListener?)
fun enableLocalAudio(track: LocalAudioTrack, enable: Boolean): Boolean
```

Local tracks are created and shared by `RTCEngine`, but publishing state is isolated per channel. When an audience user calls a publishing API, it fails with `FORBIDDEN_FOR_AUDIENCE`. `enableLocalAudio` only toggles audio already published in the current channel with low latency; it doesn't close microphone capture or remove the remote track.

## Subscribe to remote tracks

```kotlin
fun getRemoteVideoTrack(uid: String, trackDesc: String): RemoteVideoTrack?
fun getRemoteStreamTrack(uid: String, trackDesc: String): RemoteVideoTrack?
fun getRemoteMixtureTrack(): RemoteVideoTrack?
fun getRemoteAudioMixTrack(): RemoteAudioMixTrack?

fun subscribeRemoteTrack(
    uid: String,
    trackId: String,
    preferTrackIds: MutableList<String>?,
    result: RTCResultListener?
)
fun unSubscribeRemoteTrack(uid: String, trackId: String)

fun subscribeRemoteStream(
    streamName: String,
    uid: String,
    trackDesc: String,
    kind: String?,
    result: RTCResultListener?
)
fun unSubscribeRemoteStream(
    streamName: String,
    uid: String,
    trackDesc: String,
    kind: String?
)

fun subscribeRemoteMixture()
fun unSubscribeRemoteMixture()
```

Remote tracks, subscription IDs, and render objects must all come from the same channel. `getRemoteStreamTrack` and `subscribeRemoteStream` work only with the Wangsu media streaming engine; other engines return `STREAM_VENDOR_NOT_SUPPORTED` or an empty result.

## Statistics and ASR

```kotlin
fun getMetric(): MediaMetric.Metric?
fun startAsr()
fun stopAsr()
fun isStartAsr(): Boolean
```

Each channel has its own media statistics and ASR state. `getMetric()` returns the most recent thread-safe snapshot and doesn't actively trigger underlying statistics collection.

For the full multi-channel integration flow, see [Multi-channel](/en/rtc/android/advanced/multi-channel).
