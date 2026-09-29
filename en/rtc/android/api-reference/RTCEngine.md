---
title: "RTCEngine"
description: "API reference for RTCEngine, the Android SRTC SDK entry point: lifecycle, IM, ASR, joining and leaving channels, listeners, media quality, audio routing, devices, virtual background, getting tracks, publishing, subscription, and info queries. Look up any Engine method here."
---

`RTCEngine` is the core entry point of the Android SRTC SDK. It handles the SDK lifecycle, joining and leaving channels, event listeners, media capture/publishing/subscription, and info queries. For the complete minimal integration flow, see [Quickstart](/en/rtc/android/quickstart).

## Static methods

### version()
```kotlin
fun version(): String
```
Description: Gets the SDK version.  
Parameters: None.  
Returns: `String`, the SDK version.

### buildTime()
```kotlin
fun buildTime(): String
```
Description: Gets the SDK build time.  
Parameters: None.  
Returns: `String`, the build time string.

### create(app, enableLocalLog, engineEvent, localLogPath, version)
```kotlin
fun create(
    app: Application,
    enableLocalLog: Boolean,
    engineEvent: RTCEngineEvent,
    localLogPath: String? = null,
    version: String = ""
): RTCEngine
```
Description: Creates an `RTCEngine` instance.  
Parameters:
- `app`: `Application`, the application context.
- `enableLocalLog`: `Boolean`, whether to enable local log storage.
- `engineEvent`: `RTCEngineEvent`, an error listener that shares the Engine lifecycle; see [RTCEngineEvent](/en/rtc/android/api-reference/RTCEngineEvent).
- `localLogPath`: `String?`, the log directory; the default path is used when `null`.
- `version`: `String`, the version identifier of your app (useful for logs/troubleshooting).

Returns: `RTCEngine`, the engine instance.

## Lifecycle

### initSDK()
```kotlin
fun initSDK()
```
Description: Initializes the RTC SDK. You must call it before any channel, capture, publishing, or subscription API.  
Parameters: None.  
Returns: None (`Unit`).

### releaseSDK()
```kotlin
fun releaseSDK()
```
Description: Releases RTC SDK resources.  
Parameters: None.  
Returns: None (`Unit`).

## IM

### enableIm(token, resultListener)
```kotlin
fun enableIm(token: String, resultListener: RTCResultListener?)
```
Description: Enables the IM channel (out-of-channel messaging).  
Parameters:
- `token`: `String`, the IM/channel authentication token.
- `resultListener`: `RTCResultListener?`, the enable result callback; can be `null`.

Returns: None (`Unit`).

### disableIm()
```kotlin
fun disableIm()
```
Description: Disables the IM channel.  
Parameters: None.  
Returns: None (`Unit`).

## Transcription

### startAsr()
```kotlin
fun startAsr()
```
Description: Starts transcription.  
Parameters: None.  
Returns: None (`Unit`).

### stopAsr()
```kotlin
fun stopAsr()
```
Description: Stops transcription.  
Parameters: None.  
Returns: None (`Unit`).

### isStartAsr()
```kotlin
fun isStartAsr(): Boolean
```
Description: Queries whether transcription is currently on.  
Parameters: None.  
Returns: `Boolean`, `true` if it's on.

## Channels

### join(activity, token, clientEvent, options)
```kotlin
fun join(
    activity: Activity,
    token: String,
    clientEvent: RTCClientEvent,
    options: JoinOptions? = null
): RTCChannel?
```
Description: Joins a channel and returns an operation handle for it. The first channel also becomes the default channel, and the flat channel APIs on `RTCEngine` delegate to it; subsequent channels use their own returned [`RTCChannel`](/en/rtc/android/api-reference/RTCChannel).
Parameters:
- `activity`: `Activity`, the current screen context.
- `token`: `String`, the token containing the information required to join.
- `clientEvent`: `RTCClientEvent`, the initial channel control listener for this channel; the join result is returned through `onJoinSucceed` / `onJoinFailed`.
- `options`: `JoinOptions?`, auto-subscribe configuration; you can set `autoSubscribeAudio` and `autoSubscribeVideo`.

Returns: `RTCChannel?`. A non-null value only means the SDK accepted the request and created a session, not that the join succeeded; if the request is rejected before creation, it returns `null`, and the failure reason is still returned through this call's `clientEvent.onJoinFailed(...)`. If the SDK isn't initialized or has been released, it synchronously throws `SdkNotInitializedException`.

> Joining the same channel twice returns `null` and calls back a failure with `RtcChannelErrorCode.CHANNEL_ALREADY_EXISTS` (`102208`); the existing channel and listener stay unchanged. For the full multi-channel flow, see [Multi-channel](/en/rtc/android/advanced/multi-channel).

### leave()
```kotlin
fun leave()
```
Description: Leaves the default channel. For additional channels, call the corresponding `RTCChannel.leave()`.
Parameters: None.  
Returns: None (`Unit`).

### resume()
```kotlin
fun resume()
```
Description: Resumes operation (commonly used to send a heartbeat immediately after the screen turns back on).  
Parameters: None.  
Returns: None (`Unit`).

### isAudience()
```kotlin
fun isAudience(): Boolean
```
Description: Queries whether you're currently an audience user. Audience users can subscribe to remote users and capture locally (camera/microphone/screen), but **can't publish local tracks**. The result is based on `is_audience` in your own user info cached by the SDK; it returns `false` when you haven't joined.  
Parameters: None.  
Returns: `Boolean`, `true` if you're currently an audience user.

> Read the initial role after joining with this method; when the role changes during the call, you're notified by [`RTCClientEvent.onMeMembershipChanged`](/en/rtc/android/api-reference/RTCClientEvent).

## Listener setup

### setRtcImEvent(e)
```kotlin
fun setRtcImEvent(e: RTCImEvent)
```
Description: Sets the IM event listener.  
Parameters:
- `e`: `RTCImEvent`, the IM callback implementation. See [RTCImEvent](/en/rtc/android/api-reference/RTCImEvent).

Returns: None (`Unit`).

### setRtcMediaEvent(e)
```kotlin
fun setRtcMediaEvent(e: RTCMediaEvent)
```
Description: Sets the media event listener for the default channel. For additional channels, use `RTCChannel.setRtcMediaEvent(...)`.
Parameters:
- `e`: `RTCMediaEvent`, the media callback implementation. See [RTCMediaEvent](/en/rtc/android/api-reference/RTCMediaEvent).

Returns: None (`Unit`).

### setRtcCameraDeviceEvent(e)

```kotlin
fun setRtcCameraDeviceEvent(e: RTCCameraDeviceEvent?)
```

Description: Sets the Engine-global camera device listener; pass `null` to unbind. Camera capture is shared by all channels, so events don't carry a channel ID and aren't duplicated across multiple channels. See [RTCCameraDeviceEvent](/en/rtc/android/api-reference/RTCCameraDeviceEvent).

### setRtcLocalVideoFrameEvent(e)
```kotlin
fun setRtcLocalVideoFrameEvent(e: RTCLocalVideoFrameEvent?)
```
Description: Sets an external callback for local video frames. Use it only when your app explicitly needs local video frame data (for example, for local beauty filters, post-processing, or custom-drawn previews); the SDK's internal preview rendering doesn't depend on it. Pass `null` to remove the callback.  
Parameters:
- `e`: `RTCLocalVideoFrameEvent?`, the local video frame callback implementation; `null` removes it.

Returns: None (`Unit`).

`RTCLocalVideoFrameEvent` interface methods:

```kotlin
interface RTCLocalVideoFrameEvent {
    fun onLocalVideoFrame(yuv: ByteArray?, width: Int, height: Int, stamp: Long, format: Int, facing: Int)
    fun onLocalVideoFrameSizeChanged(width: Int, height: Int, facing: Int)
}
```

- `onLocalVideoFrame`: called back with one local video frame. `yuv` is data the SDK copies separately for your app, so you can cache or process it yourself; `stamp` is the frame timestamp; `format` is the frame format; `facing` is the camera facing.
- `onLocalVideoFrameSizeChanged`: called back when the local video frame size or camera direction changes.

### setRtcLocalScreenFrameEvent(e)
```kotlin
fun setRtcLocalScreenFrameEvent(e: RTCLocalScreenFrameEvent?)
```
Description: Sets an Engine-level callback for local screen I420 frames. When the same shared capture is published to multiple channels, only one copy of the data is called back; when no listener is set, YUV data isn't copied for the app. Pass `null` to remove the callback.

Parameters:
- `e`: `RTCLocalScreenFrameEvent?`, the local screen frame callback implementation; `null` removes it.

Returns: None (`Unit`).

`RTCLocalScreenFrameEvent` interface methods:

```kotlin
interface RTCLocalScreenFrameEvent {
    fun onLocalScreenFrame(
        yuv: ByteArray,
        width: Int,
        height: Int,
        stamp: Long,
        format: Int,
        rotation: Int
    )
}
```

- `yuv`: tightly packed I420 data in Y, U, V order. The SDK has already created an independent copy, so your app can still cache it or process it asynchronously after the callback returns.
- `width` / `height`: the width and height of the frame actually dispatched.
- `stamp`: a nanosecond timestamp based on a monotonic clock.
- `format`: the video format, currently always `cn.seastart.rtc.media.format.YuvFormat.I420`.
- `rotation`: clockwise rotation angle: `0`, `90`, `180`, or `270`.

The callback runs synchronously on the screen capture thread, so your app shouldn't block it. When a single-app target isn't visible, you may receive black frames; for static pages, you may receive keep-alive replays of the most recent real frame, consistent with what's actually sent.

### setRtcLocalAudioFrameEvent(e)

```kotlin
fun setRtcLocalAudioFrameEvent(e: RTCLocalAudioFrameEvent?)
```

Description: Sets the local PCM callback for shared microphone capture; pass `null` to unbind. Registering the listener doesn't open the microphone automatically; you must call `LocalMicTrack.startCapture(...)`. See [RTCLocalAudioFrameEvent](/en/rtc/android/api-reference/RTCLocalAudioFrameEvent).

### setRtcMicDeviceEvent(e)

```kotlin
fun setRtcMicDeviceEvent(e: RTCMicDeviceEvent?)
```

Description: Sets the Engine-global microphone input device listener; pass `null` to unbind. See [RTCMicDeviceEvent](/en/rtc/android/api-reference/RTCMicDeviceEvent).

## Media quality

### getMetric()
```kotlin
fun getMetric(): MediaMetric.Metric?
```
Description: Actively gets the most recently collected media quality snapshot of the default channel (including `qualityReport`). Returns a thread-safe copy and doesn't trigger the underlying `getStats`; the sampling period is about 5 seconds, so it may be `null` right after media starts. For additional channels, use `RTCChannel.getMetric()`; for poor-network level changes, prefer listening to [`RTCMediaEvent.onNetworkQualityChanged`](/en/rtc/android/api-reference/RTCMediaEvent).
Parameters: None.  
Returns: `MediaMetric.Metric?`, the most recent quality snapshot; `null` when there's no data yet. For fields, see [Media quality](/en/rtc/android/media-quality); for how to get it and handle poor networks, see [Network quality](/en/rtc/android/network-quality).

## Audio routing

### getAudioRouterManager()
```kotlin
fun getAudioRouterManager(): AudioRouterManager
```
Description: Gets the audio routing manager (singleton).  
Parameters: None.  
Returns: `AudioRouterManager`, the routing manager instance. See [AudioRouterManager](/en/rtc/android/api-reference/AudioRouterManager) and [Audio routing](/en/rtc/android/advanced/audio-routing).

### releaseAudioRouterManager()
```kotlin
fun releaseAudioRouterManager()
```
Description: Releases audio routing resources (internally calls `release(true)`, restoring the system audio mode and switching back to the speaker).  
Parameters: None.  
Returns: None (`Unit`).

## Device capabilities

### getCameraDevices()
```kotlin
fun getCameraDevices(): List<CameraDeviceCapability>
```
Description: Gets the list of camera device capabilities currently available on the system (Camera2). The `cameraId` in the returned list can be used with [`LocalCameraTrack.switchCameraDevice`](/en/rtc/android/api-reference/LocalCameraTrack) to switch cameras exactly.  
Parameters: None.  
Returns: `List<CameraDeviceCapability>`; an empty list when no device is available. For the type definition, see [Types](/en/rtc/android/types).

> Dynamic changes to camera devices are notified through [`RTCCameraDeviceEvent`](/en/rtc/android/api-reference/RTCCameraDeviceEvent).

### getMicDevices()

```kotlin
fun getMicDevices(): List<MicDeviceCapability>
```

Description: Gets the list of microphone input device capabilities currently available on the system. For the returned fields, see [Types](/en/rtc/android/types).

### switchMicDevice(deviceId)

```kotlin
fun switchMicDevice(deviceId: String)
```

Description: Switches the input device used by shared microphone capture. `deviceId` comes from `getMicDevices()` and is valid only while that device stays connected; switching during capture rebuilds the recording pipeline. You can also use the method of the same name on `LocalMicTrack`.

## Virtual background

Performs local person segmentation on camera capture, supporting background blur and background image replacement. The local preview matches what remote users see.

Call order: `installVirtualBackground` → `setVirtualBackgroundBlur` or `setVirtualBackgroundImage` → `enabledVirtualBackground(true)`; call `uninstallVirtualBackground` when no longer needed.

### installVirtualBackground(modelData)

```kotlin
fun installVirtualBackground(modelData: ByteArray): Int
```

Description: Installs the virtual background module. The virtual background is an in-house module that doesn't need a license key, only a person segmentation model.  
Parameters: `modelData` is the content of the selfie_segmenter onnx model, read from assets by your app and passed in.  
Returns: An error code; `0` means success. If the model is empty or invalid, it returns `VIRTUAL_BACKGROUND_MODEL_INVALID`; see [Error codes](/en/rtc/android/error-codes).

### uninstallVirtualBackground()

```kotlin
fun uninstallVirtualBackground()
```

Description: Uninstalls the virtual background module and releases the model and GPU resources.

### enabledVirtualBackground(enabled)

```kotlin
fun enabledVirtualBackground(enabled: Boolean): Int
```

Description: Master switch for the virtual background. When off, the capture pipeline passes through with zero overhead—no inference or compositing.  
Parameters: `enabled` is `true` to turn it on, `false` to turn it off.  
Returns: An error code; `0` means success. If the module isn't installed, it returns `VIRTUAL_BACKGROUND_NOT_INSTALL`.

### setVirtualBackgroundBlur(level)

```kotlin
fun setVirtualBackgroundBlur(level: Int)
```

Description: Sets the background blur strength. Mutually exclusive with `setVirtualBackgroundImage`; whichever is called last takes effect.  
Parameters: `level` is in the range `1`–`10`; default `5`.

### setVirtualBackgroundImage(image)

```kotlin
fun setVirtualBackgroundImage(image: Bitmap?)
```

Description: Sets the background replacement image, cropped in cover mode without stretching. Mutually exclusive with `setVirtualBackgroundBlur`; whichever is called last takes effect.  
Parameters: `image` is the background image; pass `null` to cancel the replacement.

### setVirtualBackgroundInferenceInterval(interval)

```kotlin
fun setVirtualBackgroundInferenceInterval(interval: Int)
```

Description: Sets the segmentation inference interval: person segmentation runs once every `interval` frames; default `1`. Used to reduce overhead on low-end devices. We recommend that your app set it per device model rather than exposing it to end users.  
Parameters: `interval` is at least `1`.

### setVirtualBackgroundMaskSync(on)

```kotlin
fun setVirtualBackgroundMaskSync(on: Boolean)
```

Description: Sets the mask alignment switch; default `false`. Used to eliminate misaligned trailing artifacts when waving quickly; it only makes a difference when the inference interval is greater than `1`.

### isVirtualBackgroundEnabled()

```kotlin
fun isVirtualBackgroundEnabled(): Boolean
```

Description: Queries whether the virtual background is currently on.

## Getting tracks

### getLocalCameraTrack(preOpt)
```kotlin
fun getLocalCameraTrack(preOpt: PreOptionCamera = PreOptionCamera._480P): LocalCameraTrack
```
Description: Gets the local camera track controller.  
Parameters:
- `preOpt`: `PreOptionCamera`, the camera capture/publishing preset; default `_480P`. See [Camera preset](/en/rtc/android/presets/camera). The track copies `preOpt.capture`, so changing `capture` on the original object after getting the track has no effect—reassign `track.preOpt` instead; changes to `preOpt.publish` still take effect. See [`LocalCameraTrack`](/en/rtc/android/api-reference/LocalCameraTrack).

Returns: `LocalCameraTrack`, the local camera track instance.

### getLocalScreenTrack(activity, preOpt)
```kotlin
fun getLocalScreenTrack(activity: Activity, preOpt: PreOptionScreen = PreOptionScreen.def): LocalScreenTrack
```
Description: Gets the local screen sharing track controller.  
Parameters:
- `activity`: `Activity`, used to request the screen recording permission.
- `preOpt`: `PreOptionScreen`, the screen capture/publishing preset. See [Screen sharing preset](/en/rtc/android/presets/screen-sharing).

Returns: `LocalScreenTrack`, the local screen track instance.

### getLocalMicTrack(preOpt)
```kotlin
fun getLocalMicTrack(preOpt: PreOptionMic = PreOptionMic.def): LocalMicTrack
```
Description: Gets the local microphone track controller.  
Parameters:
- `preOpt`: `PreOptionMic`, the microphone capture/publishing preset. See [Microphone preset](/en/rtc/android/presets/microphone).

Returns: `LocalMicTrack`, the local microphone track instance. Getting the track doesn't open the microphone automatically; you must call [`LocalMicTrack.startCapture(...)`](/en/rtc/android/api-reference/LocalMicTrack) before publishing.

### getLocalCustomVideoTrack(preOpt)
```kotlin
fun getLocalCustomVideoTrack(preOpt: PreOptionCustomVideo = PreOptionCustomVideo.def): LocalCustomVideoTrack
```
Description: Gets the local custom video track controller, used to push external **raw YUV frames** (whiteboards, canvases, player video, and so on) to a published track. The SDK caches the track instance as a singleton; calling it again returns the same instance and overwrites the old value with the `preOpt` passed in.  
Parameters:
- `preOpt`: `PreOptionCustomVideo`, the custom video capture/publishing preset; default `PreOptionCustomVideo.def` (track description `custom`). To publish with the screen sharing description, use `PreOptionCustomVideo.screen`. See [Custom video preset](/en/rtc/android/presets/custom-video).

Returns: `LocalCustomVideoTrack`, the local custom video track instance. See [LocalCustomVideoTrack](/en/rtc/android/api-reference/LocalCustomVideoTrack).

> For the full integration flow, see [Custom tracks](/en/rtc/android/advanced/custom-track).

### getRemoteVideoTrack(uid, trackDesc)
```kotlin
fun getRemoteVideoTrack(uid: String, trackDesc: String): RemoteVideoTrack?
```
Description: Gets a remote video track by user and track description.  
Parameters:
- `uid`: `String`, the remote user ID.
- `trackDesc`: `String`, the track description (such as `camera_big` / `screen`).

Returns: `RemoteVideoTrack?`; `null` if not found.

### getRemoteMixtureTrack()
```kotlin
fun getRemoteMixtureTrack(): RemoteVideoTrack?
```
Description: Gets the remote composite video track.  
Parameters: None.  
Returns: `RemoteVideoTrack?`; `null` if not found.

### getRemoteAudioMixTrack()
```kotlin
fun getRemoteAudioMixTrack(): RemoteAudioMixTrack?
```
Description: Gets the remote mixed audio track.  
Parameters: None.  
Returns: `RemoteAudioMixTrack?`; `null` if not found. See [RemoteAudioMixTrack](/en/rtc/android/api-reference/RemoteAudioMixTrack).

## Publishing and subscription

### publishLocalVideo(track, publishCustomOpt, listener)
```kotlin
fun publishLocalVideo(track: LocalVideoTrack, publishCustomOpt: PublishCustomOptions?, listener: RTCResultListener?)
```
Description: Publishes a local video track.  
Parameters:
- `track`: `LocalVideoTrack`, the local video track (camera [`LocalCameraTrack`](/en/rtc/android/api-reference/LocalCameraTrack) / screen recording [`LocalScreenTrack`](/en/rtc/android/api-reference/LocalScreenTrack) / local custom [`LocalCustomVideoTrack`](/en/rtc/android/api-reference/LocalCustomVideoTrack)). Passing any other type returns `RtcChannelErrorCode.TRACK_TYPE_INVALID` (`102002`; see [Error codes](/en/rtc/android/error-codes)) through `listener.onFail`.
- `publishCustomOpt`: `PublishCustomOptions?`, custom publishing parameters; can be `null`. See [Camera preset](/en/rtc/android/presets/camera).
- `listener`: `RTCResultListener?`, the publishing result callback; can be `null`.

Returns: None (`Unit`).

> **Note**: camera publishing uses declarative reconciliation. When you `publish`/`unpublish` in rapid succession, intermediate calls merged into later operations may not call back; rely on the callback of the last call or the final state, and don't assume "every call gets exactly one callback".

### publishLocalAudio(track, publishCustomOpt, listener)
```kotlin
fun publishLocalAudio(track: LocalAudioTrack, publishCustomOpt: PublishCustomOptions?, listener: RTCResultListener?)
```
Description: Publishes an already-captured local audio track to the default channel. This API doesn't start microphone capture automatically; call `LocalMicTrack.startCapture(...)` first.
Parameters:
- `track`: `LocalAudioTrack`, the local audio track.
- `publishCustomOpt`: `PublishCustomOptions?`, custom publishing parameters; can be `null`.
- `listener`: `RTCResultListener?`, the publishing result callback; can be `null`.

Returns: None (`Unit`).

### unPublishLocalVideo(track, listener)
```kotlin
fun unPublishLocalVideo(track: LocalVideoTrack, listener: RTCResultListener?)
```
Description: Unpublishes a local video track.  
Parameters:
- `track`: `LocalVideoTrack`, the target video track.
- `listener`: `RTCResultListener?`, the unpublish result callback; can be `null`.

Returns: None (`Unit`).

> **Note**: as with `publishLocalVideo`, intermediate calls merged during rapid successive operations may not call back; rely on the last one.

### unPublishLocalAudio(track, listener)
```kotlin
fun unPublishLocalAudio(track: LocalAudioTrack, listener: RTCResultListener?)
```
Description: Unpublishes local audio in the default channel without stopping shared microphone capture; when you no longer need capture, also call `LocalMicTrack.stopCapture()`.
Parameters:
- `track`: `LocalAudioTrack`, the target audio track.
- `listener`: `RTCResultListener?`, the unpublish result callback; can be `null`.

Returns: None (`Unit`).

### subscribeRemoteTrack(uid, trackId, preferTrackIds, result)
```kotlin
fun subscribeRemoteTrack(
    uid: String,
    trackId: String,
    preferTrackIds: MutableList<String>?,
    result: RTCResultListener?
)
```
Description: Subscribes to the specified remote video track.  
Parameters:
- `uid`: `String`, the remote user ID.
- `trackId`: `String`, the target (default) remote track ID.
- `preferTrackIds`: `MutableList<String>?`, the candidate layer list, used in simulcast scenarios to declare the priority of acceptable tracks. When `null`, only `trackId` is subscribed; if the list doesn't contain `trackId`, the SDK automatically inserts it at the front.
- `result`: `RTCResultListener?`, the subscription result callback; can be `null`.

Returns: None (`Unit`).

### unSubscribeRemoteTrack(uid, trackId)
```kotlin
fun unSubscribeRemoteTrack(uid: String, trackId: String)
```
Description: Unsubscribes from the specified remote video track.  
Parameters:
- `uid`: `String`, the remote user ID.
- `trackId`: `String`, the remote track ID.

Returns: None (`Unit`).

### subscribeRemoteMixture()
```kotlin
fun subscribeRemoteMixture()
```
Description: Subscribes to the remote composite video track.  
Parameters: None.  
Returns: None (`Unit`).

### unSubscribeRemoteMixture()
```kotlin
fun unSubscribeRemoteMixture()
```
Description: Unsubscribes from the remote composite video track.  
Parameters: None.  
Returns: None (`Unit`).

## Wangsu generic streams (advanced / engine-specific)

> ⚠️ **Wangsu engine only**: the following APIs **work only with the Wangsu media streaming engine**. They subscribe to a "generic stream" by a stream name your app provides directly, an advanced capability for specific integration scenarios. With a non-Wangsu engine: `getRemoteStreamTrack` returns `null`, `subscribeRemoteStream` returns a not-supported error through `result.onFail`, and `unSubscribeRemoteStream` is ignored. Most integrations don't need these APIs.

### getRemoteStreamTrack(uid, trackDesc)
```kotlin
fun getRemoteStreamTrack(uid: String, trackDesc: String): RemoteVideoTrack?
```
Description: Gets the video controller for a Wangsu generic stream (for rendering with `addPlayView`). It doesn't depend on channel users and is obtained by the `(uid, trackDesc)` passed when subscribing. You can call it before `subscribeRemoteStream`—get the controller and call `addPlayView` first, then subscribe, and the video renders as soon as it arrives.  
Parameters:
- `uid`: `String`, the render routing identifier (defined by your app; can be the same as the stream name).
- `trackDesc`: `String`, the special stream identifier, used for render binding and to distinguish multiple generic streams.

Returns: `RemoteVideoTrack?`; `null` for a non-Wangsu engine or when the channel hasn't started.

### subscribeRemoteStream(streamName, uid, trackDesc, kind, result)
```kotlin
fun subscribeRemoteStream(
    streamName: String,
    uid: String,
    trackDesc: String,
    kind: String?,
    result: RTCResultListener?
)
```
Description: Subscribes to a Wangsu generic stream (the stream name is provided directly by your app, such as `"rtc_v_lesson_fknqb"`).  
Parameters:
- `streamName`: `String`, the full stream name, used directly in Wangsu HTTP requests.
- `uid`: `String`, the render routing identifier (defined by your app; can be the same as `streamName`).
- `trackDesc`: `String`, the special stream identifier, used for render binding and to distinguish multiple generic streams.
- `kind`: `String?`, optional, `"video"` / `"audio"`; when empty, inferred from the stream name prefix (`rtc_v` → video, `rtc_a` → audio).
- `result`: `RTCResultListener?`, the subscription result callback; can be `null`.

Returns: None (`Unit`).

### unSubscribeRemoteStream(streamName, uid, trackDesc, kind)
```kotlin
fun unSubscribeRemoteStream(streamName: String, uid: String, trackDesc: String, kind: String?)
```
Description: Unsubscribes from a Wangsu generic stream.  
Parameters:
- `streamName`: `String`, the full stream name passed when subscribing.
- `uid`: `String`, the render routing identifier passed when subscribing.
- `trackDesc`: `String`, the special stream identifier passed when subscribing.
- `kind`: `String?`, optional, `"video"` / `"audio"`; when empty, inferred from the stream name prefix.

Returns: None (`Unit`).

## Info queries

### getChannelInfo()
```kotlin
fun getChannelInfo(): ChannelInfo?
```
Description: Gets the current channel info.  
Parameters: None.  
Returns: `ChannelInfo?`; may be `null` when not joined or there's no data. See [Types](/en/rtc/android/types).

### getMeInfo()
```kotlin
fun getMeInfo(): UserInfo?
```
Description: Gets the current user's info.  
Parameters: None.  
Returns: `UserInfo?`; may be `null` when not joined or there's no data.

### getUserInfos()
```kotlin
fun getUserInfos(): MutableList<UserInfo>
```
Description: Gets info for all users in the channel (including yourself).  
Parameters: None.  
Returns: `MutableList<UserInfo>`, the user list.

### getUserInfo(uid)
```kotlin
fun getUserInfo(uid: String): UserInfo?
```
Description: Gets a user's info by user ID.  
Parameters:
- `uid`: `String`, the target user ID.

Returns: `UserInfo?`; `null` if not found.

### getTrackInfos(uid)
```kotlin
fun getTrackInfos(uid: String): List<TrackInfo>
```
Description: Gets the track list of the specified user.  
Parameters:
- `uid`: `String`, the target user ID.

Returns: `List<TrackInfo>`, the track info list.

### getTrackInfoByTrackDesc(uid, trackDesc)
```kotlin
fun getTrackInfoByTrackDesc(uid: String, trackDesc: String): TrackInfo?
```
Description: Gets track info by user ID + track description.  
Parameters:
- `uid`: `String`, the target user ID.
- `trackDesc`: `String`, the track description.

Returns: `TrackInfo?`; `null` if not found.

### getTrackInfoByTrackId(uid, trackId)
```kotlin
fun getTrackInfoByTrackId(uid: String, trackId: String): TrackInfo?
```
Description: Gets track info by user ID + track ID.  
Parameters:
- `uid`: `String`, the target user ID.
- `trackId`: `String`, the track ID.

Returns: `TrackInfo?`; `null` if not found.

## Common result callback types

Most asynchronous APIs return their results through `RTCResultListener`.

### RTCResultListener
```java
public interface RTCResultListener {
    void onSuccess();
    void onFail(int code);
}
```
- `onSuccess()`: the call succeeded.
- `onFail(int code)`: the call failed; `code` is the error code. See [Error codes](/en/rtc/android/error-codes).

### RTCValueResultListener\<T\>
```kotlin
interface RTCValueResultListener<T> {
    fun onSuccess(t: T)
    fun onFail(code: Int)
}
```
- `onSuccess(t)`: the call succeeded and returned the result object `t`.
- `onFail(code)`: the call failed; `code` is the error code.

`RTCResultListener2<T>` has been renamed to `RTCValueResultListener<T>`; apart from the type name, the method signatures are unchanged.
