---
title: "RTCEngineChannel"
description: "API reference for RTCEngineChannel, a single channel instance in the Objective-C SRTC SDK on iOS: joining and leaving, user and channel data queries, publishing and subscribing to streams, audio sending, screen sharing publishing, and custom streams. Look up any per-channel method here."
---

`RTCEngineChannel` represents an independent RTC channel and is created by `-[RTCEngineKit createChannelWithDelegate:]`. Each instance holds its own signaling channel, media connection, user cache, and remote rendering state. Multiple instances can exist in the same process at the same time, and user data, stream statistics, and rendering don't interfere across instances.

Process-level shared capabilities such as the camera, audio routing, ReplayKit capture, and beauty filter rendering are provided by the [RTCEngineKit](/en/rtc/ios/api-reference/RTCEngineKit) singleton and aren't duplicated on channel instances.

<Warning>
The engine holds channel instances. When you're done with one, you must call `destroy` to destroy it; otherwise the engine keeps holding the channel.
</Warning>

```objectivec
RTCEngineChannel *channel = [[RTCEngineKit sharedEngine] createChannelWithDelegate:self];
[channel joinChannelWithToken:@"Your Token"];
```

## Properties
### delegate
`id<RTCEngineChannelDelegate> delegate`

Channel event delegate; see [RTCEngineChannelDelegate](/en/rtc/ios/api-reference/RTCEngineChannelDelegate).

### channel
`NSString *channel` (read-only)

Name of the joined channel; empty when not joined.

### enabledTrans
`BOOL enabledTrans` (read-only)

Transcription state.

## Channel APIs
### joinChannelWithToken:()
`- (RTCEngineError)joinChannelWithToken:(NSString *)token`

Joins the channel.

Every RTC user must join a channel to "publish" or "subscribe" to audio and video streams. "Publish" means pushing your own audio and video to the cloud; "subscribe" means pulling the audio and video streams of other users in the channel from the cloud.

**Parameters**

| token | Authentication token |
| --- | --- |


**Notes**

+ A channel instance can join only one channel at a time. To join multiple channels at the same time, call `createChannelWithDelegate:` to create multiple instances; don't join repeatedly on the same instance.
+ On the same instance, make sure `joinChannelWithToken` and `leaveChannel` are called in pairs—that is, "leave the previous channel before joining the next one"—otherwise many unexpected issues can occur.

### leaveChannel:()
`- (void)leaveChannel:(nullable RTCEngineKitFinishBlock)finishBlock`

Leaves the channel.

Calling this API makes the user leave the channel this instance is in and releases the media resources that channel occupies. Once the resources are released, the SDK notifies you through the `finishBlock` callback. If you want to call `joinChannelWithToken:()` again, we recommend waiting for the `finishBlock` callback before doing anything else.

Shared hardware such as the camera and microphone is managed by the engine and is actually released only after the last channel is left.

**Parameters**

| finishBlock | Completion callback |
| --- | --- |


### destroy()
`- (void)destroy`

Destroys the channel instance.

It first leaves the channel, then removes the instance from the engine's channel list and disconnects the delegate. You can't use the instance after calling this; to join again, create a new instance with `createChannelWithDelegate:`.

## Data management APIs
### getMySelf()
`- (nullable RTCEngineUserModel *)getMySelf`

Gets the current account's data in this channel.

### getChannelDetails()
`- (nullable RTCEngineChannelModel *)getChannelDetails`

Gets the current channel's data.

### findMemberWithUserId:()
`- (nullable RTCEngineUserModel *)findMemberWithUserId:(NSString *)userId`

Looks up the user info for `userId` in this channel.

<Note>
The same `userId` may exist in multiple channel instances at the same time. Query through the channel instance the event comes from, and don't reuse query results across instances.
</Note>

**Parameters**

| userId | User ID |
| --- | --- |


### getRemoteUsers()
`- (NSArray<RTCEngineUserModel *> *)getRemoteUsers`

Gets the user list of this channel.

### getDrawingHost()
`- (nullable NSString *)getDrawingHost`

Gets the whiteboard address.

## Video APIs
### publishLocalVideo:()
`- (RTCEngineError)publishLocalVideo:(BOOL)publish`

Pauses/resumes publishing the local video stream.

The published video comes from the process-level shared camera, and whether it's published to this channel is controlled independently by the current instance. In multi-channel scenarios, pausing publishing on one channel doesn't affect other channels.

This API only pauses or lets through the data stream in software and doesn't turn the camera hardware on or off, so it's more efficient and better suited to scenarios where you toggle frequently. After you pause/resume publishing the local video stream, other users in the same channel receive the `engineChannel:onRemoteUserUpdate:` callback.

**Parameters**

| publish | YES: resume; NO: pause |
| --- | --- |


### startRemoteView:trackId:view:()
`- (RTCEngineError)startRemoteView:(NSString *)userId trackId:(RTCTrackIdentifierFlags)trackId view:(VIEW_CLASS *)view`

Subscribes to a remote user's video stream and binds a video rendering view.

Calling this API makes the SDK pull the video stream of the specified `userId` in this channel and render it to the view specified by `view`.

**Parameters**

| userId | ID of the remote user |
| --- | --- |
| trackId | ID of the track to view; see [RTCTrackIdentifierFlags](/en/rtc/ios/types#rtctrackidentifierflags) |
| view | Video rendering view |


### updateRemoteView:trackId:view:()
`- (RTCEngineError)updateRemoteView:(NSString *)userId trackId:(RTCTrackIdentifierFlags)trackId view:(VIEW_CLASS *)view`

Updates a remote user's video rendering view.

Use this API to update the render view of remote video, commonly in interactions that switch display areas.

**Parameters**

| userId | ID of the remote user |
| --- | --- |
| trackId | ID of the track to view; see [RTCTrackIdentifierFlags](/en/rtc/ios/types#rtctrackidentifierflags) |
| view | Video rendering view |


### stopRemoteView:trackId:()
`- (RTCEngineError)stopRemoteView:(NSString *)userId trackId:(RTCTrackIdentifierFlags)trackId`

Unsubscribes from a remote user's video stream and releases the render view.

**Parameters**

| userId | ID of the remote user |
| --- | --- |
| trackId | ID of the track to view; see [RTCTrackIdentifierFlags](/en/rtc/ios/types#rtctrackidentifierflags) |


### stopAllRemoteViewWithUserId:()
`- (RTCEngineError)stopAllRemoteViewWithUserId:(NSString *)userId`

Unsubscribes from all video streams of the specified remote user and releases the render views.

**Parameters**

| userId | ID of the remote user |
| --- | --- |


### stopAllRemoteView()
`- (RTCEngineError)stopAllRemoteView`

Unsubscribes from the video streams of all remote users in this channel and releases all render resources.

### startRemoteMixture:()
`- (RTCEngineError)startRemoteMixture:(VIEW_CLASS *)view`

Subscribes to the remote composite video stream and binds a video rendering view.

**Parameters**

| view | Video rendering view |
| --- | --- |


### stopRemoteMixture()
`- (RTCEngineError)stopRemoteMixture`

Unsubscribes from the remote composite video stream and releases the render view.

### startRemoteRetweet:view:()
`- (RTCEngineError)startRemoteRetweet:(NSString *)streamName view:(VIEW_CLASS *)view`

Subscribes to a remote re-streamed audio and video stream (pulled over WebRTC) and binds a video rendering view.

Calling this API makes the SDK subscribe over WebRTC to a remote re-streamed stream whose stream name you pass in. A single connection receives both audio and video, and the video is rendered to the view specified by `view`. This API uses the original stream name as the stream identifier; the re-streamed stream isn't reported as remote user video data, and its receiving status is reported separately through `engineChannel:onReceiveRetweetStreamStatusChange:status:`.

> Note: pulling re-streamed streams currently supports only the `wangsu` media streaming vendor.

**Parameters**

| streamName | Name of the remote stream to subscribe to (passed in by you; the value is the stream name on the media streaming server as is) |
| --- | --- |
| view | Video rendering view |


### stopRemoteRetweet:()
`- (RTCEngineError)stopRemoteRetweet:(NSString *)streamName`

Unsubscribes from a remote re-streamed audio and video stream and releases the render view.

**Parameters**

| streamName | Name of the remote stream to unsubscribe from (passed in by you) |
| --- | --- |


## Media streaming APIs
### setStreamMediaConfig:()
`- (void)setStreamMediaConfig:(RTCEngineMediaConfig *)config`

Sets media streaming configuration parameters.

Use this API to set parameters such as video encoding, audio encoding, video frame rate, and video bitrate. The configuration applies to the current channel instance.

**Parameters**

| config | Media streaming configuration parameters; see [RTCEngineMediaConfig](/en/rtc/ios/types#rtcenginemediaconfig) |
| --- | --- |


### setNetworkQosParam:()
`- (void)setNetworkQosParam:(RTCEngineNetworkQosParam *)param`

Sets network quality control parameters.

Use this API to set parameters such as the latency adaptation level, the anti-jitter delay level, the bitrate adaptation switch, and the network adaptation switch.

**Parameters**

| param | Quality control parameters; see [RTCEngineNetworkQosParam](/en/rtc/ios/types#rtcenginenetworkqosparam) |
| --- | --- |


### setRemoteDebugParam:()
`- (void)setRemoteDebugParam:(RTCEngineDebugParam *)param`

Sets remote debugging parameters.

Use this API to set debugging parameters such as the remote debugging address and whether to save audio and video streams.

**Parameters**

| param | Debugging parameters; see [RTCEngineDebugParam](/en/rtc/ios/types#rtcenginedebugparam) |
| --- | --- |


## Audio APIs
### enabledSendAudio:()
`- (RTCEngineError)enabledSendAudio:(BOOL)enabled`

Pauses/resumes publishing the local audio stream to this channel.

**Parameters**

| enabled | YES: turn audio on; NO: turn audio off |
| --- | --- |


### setAudioPriorityWithUserId:enabled:()
`- (RTCEngineError)setAudioPriorityWithUserId:(NSString *)userId enabled:(BOOL)enabled`

Sets the audio priority policy.

Use this API to prioritize audio reception when a user's downlink is poor.

**Parameters**

| userId | ID of the remote user |
| --- | --- |
| enabled | YES: on; NO: off |


### enabledAudioSpeaker:()
`- (RTCEngineError)enabledAudioSpeaker:(BOOL)enabled`

Sets the remote audio playback state.

Use this API to turn remote audio playback for this channel on or off. It doesn't switch between the speaker, earpiece, or external device routes; to switch the audio output device, use `-[RTCEngineKit switchAudioRoute:]`.

**Parameters**

| enabled | YES: turn remote audio playback on; NO: turn remote audio playback off |
| --- | --- |


### enabledAudioModule:()
`- (RTCEngineError)enabledAudioModule:(BOOL)enabled`

Starts or stops the local audio unit.

Supported since `2.5.9`. For purely local playback scenarios such as recorded or live playback, where the local side neither captures nor receives RTC audio, turning off the audio unit releases the underlying voice processing unit (VPIO) and prevents the playback volume of local players (such as `AVPlayer`) from being lowered; when you leave such a scenario, restore it to automatic management. Each time you join a channel, the SDK automatically resets it to automatic management, so a manually disabled state from the previous session doesn't leak into the next one.

**Parameters**

| enabled | YES: the audio unit is managed automatically by media streaming; NO: stop the audio unit |
| --- | --- |


### enabledSpeechTrans:()
`- (RTCEngineError)enabledSpeechTrans:(BOOL)enabled`

Sets the transcription state.

**Parameters**

| enabled | YES: turn transcription on; NO: turn transcription off |
| --- | --- |


### resetAudioSession()
`- (void)resetAudioSession`

Restarts the audio session.

When your app competes with other audio apps for the audio session, or the system audio session is interrupted externally and doesn't recover automatically, call this API to rebuild the SDK's audio session configuration. The audio route may change after the call, and the SDK notifies you through the `onAudioRouteChange:previousRoute:` callback of [RTCEngineDelegate](/en/rtc/ios/api-reference/RTCEngineDelegate).

## Screen sharing APIs
### publishScreenRecord:()
`- (RTCEngineError)publishScreenRecord:(BOOL)publish`

Publishes/stops the screen sharing stream on this channel.

Supported since `3.0.0`. ReplayKit capture is a process-level shared capability, and this API only controls whether the current channel instance publishes the captured data.

Starting with `3.0.1`, the capture service starts and keeps listening as soon as you join the channel. **Call this API to publish only after `engineChannel:onScreenRecordStatus:` of `RTCEngineChannelDelegate` reports `RTCScreenRecordStatusStart`**. Only when the last publishing channel stops publishing does the SDK disconnect the extension and end this system screen recording.

To end this system screen recording all at once, call `-[RTCEngineKit stopScreenRecord]`.

**Parameters**

| publish | YES: publish; NO: stop |
| --- | --- |


### publishScreenViewCaptureWithPixelBuffer:displayAngle:()
`- (void)publishScreenViewCaptureWithPixelBuffer:(CVPixelBufferRef)pixelBuffer displayAngle:(int)displayAngle`

Publishes a view capture sharing stream; through this API you can feed video data that shares the track with screen sharing.

Mutually exclusive with `publishCustomStreamWithStreamData:`; your app decides which method to use to feed the stream.

**Parameters**

| pixelBuffer | Pixel data captured from a UIView (CVPixelBufferRef) |
| --- | --- |
| displayAngle | Display angle (0/90/180/270) |


### enabledViewCaptureShare:()
`- (RTCEngineError)enabledViewCaptureShare:(BOOL)enabled`

Sets view capture sharing.

This API tells the SDK whether the screen sharing track currently carries the screen capture stream or the view capture stream; call it to mark the SDK before calling `publishScreenViewCaptureWithPixelBuffer:displayAngle:()`.

View capture is the "fallback video source" for cloud recording, and screen sharing is the "high-priority video source". The two share the screen sharing path and switch automatically by priority:

+ When turned on: if screen recording isn't in progress, the sharing path is set up; if screen recording is already in progress, the path already exists and doesn't need to be set up again;
+ When screen recording stops: if view capture is on, the path isn't closed, and publishing of view capture data resumes automatically;
+ When turned off: if screen recording isn't in progress, the sharing path is torn down; if screen recording is in progress, the path is kept for screen recording.

**Parameters**

| enabled | Enabled state. YES: on; NO: off |
| --- | --- |


## Custom stream publishing APIs
### startCustomStreamWithStreamTrackModel:()
`- (RTCEngineError)startCustomStreamWithStreamTrackModel:(RTCEngineStreamTrackModel *)streamTrackModel`

Starts a custom stream.

This API must specify basic stream information such as the track, resolution, and bitrate to publish. Only tracks declared through this API can publish custom streams via `publishCustomStreamWithStreamData:`; when your app finishes publishing the custom stream, call `stopCustomStreamWithTrackId:` to close the corresponding track.

**Parameters**

| streamTrackModel | Stream information; see [RTCEngineStreamTrackModel](/en/rtc/ios/types#rtcenginestreamtrackmodel) |
| --- | --- |


### stopCustomStreamWithTrackId:()
`- (RTCEngineError)stopCustomStreamWithTrackId:(RTCTrackIdentifierFlags)trackId`

Stops a custom stream.

**Parameters**

| trackId | Track ID; see [RTCTrackIdentifierFlags](/en/rtc/ios/types#rtctrackidentifierflags) |
| --- | --- |


### publishCustomStreamWithStreamData:()
`- (RTCEngineError)publishCustomStreamWithStreamData:(const unsigned char *)streamData bitslen:(int)bitslen pts:(uint32_t)pts dts:(uint32_t)dts trackId:(RTCTrackIdentifierFlags)trackId streamType:(RTCStreamType)streamType`

Publishes custom stream data.

Use this API to push custom stream data to the track ID declared in `startCustomStreamWithStreamTrackModel:`.

**Parameters**

| streamData | Encoded data |
| --- | --- |
| bitslen | Data length |
| pts | Presentation timestamp |
| dts | Decoding timestamp |
| trackId | Track ID; see [RTCTrackIdentifierFlags](/en/rtc/ios/types#rtctrackidentifierflags) |
| streamType | Media stream type; see [RTCStreamType](/en/rtc/ios/types#rtcstreamtype) |
