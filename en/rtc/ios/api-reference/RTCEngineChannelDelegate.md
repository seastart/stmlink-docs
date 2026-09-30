---
title: "RTCEngineChannelDelegate"
description: "iOS (Objective-C) channel-level event protocol: connection and reconnection, users joining and leaving, custom messages, audio status, stream quality, and screen sharing. Every callback carries the source channel instance. Read when implementing channel event handling on iOS."
---

This protocol carries in-channel connection, user, message, stream, audio, and screen sharing events. **The first parameter of every callback is the [RTCEngineChannel](/en/rtc/ios/api-reference/RTCEngineChannel) instance the event comes from.** With multiple channels, use the first parameter to tell which channel an event belongs to; read the channel name from `channel.channel`.

For process-level shared events (audio routing, network speed test, app performance), implement [RTCEngineDelegate](/en/rtc/ios/api-reference/RTCEngineDelegate).

```objectivec
@interface YourClass : NSObject <RTCEngineChannelDelegate>
```

<Note>
The same `userId` may appear in multiple channels at once. When querying user data in a callback, use the channel instance passed as the first parameter (such as `[channel findMemberWithUserId:userId]`); don't reuse indexes across channels.
</Note>

## Connection callbacks
### engineChannelOnReconnecting:()
`- (void)engineChannelOnReconnecting:(RTCEngineChannel *)channel`

Called when reconnection starts.

Triggered when the channel's connection drops and reconnection begins. If an error occurs, the SDK fires the `engineChannel:onDisconnected:errCode:errMsg:()` callback.

**Parameters**

| channel | Channel instance the event comes from |
| --- | --- |


### engineChannelOnReconnected:()
`- (void)engineChannelOnReconnected:(RTCEngineChannel *)channel`

Called when reconnection succeeds.

Triggered after the connection is restored.

**Parameters**

| channel | Channel instance the event comes from |
| --- | --- |


### engineChannel:onDisconnected:errCode:errMsg:()
`- (void)engineChannel:(RTCEngineChannel *)channel onDisconnected:(RTCLeaveReason)reason errCode:(RTCEngineError)errCode errMsg:(nullable NSString *)errMsg`

Called when the connection drops or you leave the channel involuntarily.

When the reason is `RTCLeaveReasonError`, the SDK has hit an unrecoverable error, such as a failure to join the channel. You need to get a new token before joining the channel again. For error codes, see the [error code table](/en/rtc/ios/error-codes).

When the reason is anything other than `RTCLeaveReasonError`, you left the channel involuntarily. For the specific reasons, see [RTCLeaveReason](/en/rtc/ios/types#rtcleavereason).

**Parameters**

| channel | Channel instance the event comes from |
| --- | --- |
| reason | Leave reason |
| errCode | Error code |
| errMsg | Error message |


## Local user callbacks
### engineChannel:onJoinSucceed:()
`- (void)engineChannel:(RTCEngineChannel *)channel onJoinSucceed:(NSString *)userId`

Called when joining the channel succeeds.

You receive this callback after calling the channel instance's `joinChannelWithToken:()` to join the channel. If an error occurs, the SDK fires the `engineChannel:onDisconnected:errCode:errMsg:()` callback.

**Parameters**

| channel | Channel instance the event comes from |
| --- | --- |
| userId | User ID |


### engineChannel:onUserUpdate:()
`- (void)engineChannel:(RTCEngineChannel *)channel onUserUpdate:(NSString *)userId`

Called when the local user's data is updated.

You receive this callback after the server modifies the current user's data, notifying you that the current user's data in this channel has changed.

**Parameters**

| channel | Channel instance the event comes from |
| --- | --- |
| userId | User ID |


## Channel callbacks
### engineChannel:onChannelUpdate:()
`- (void)engineChannel:(RTCEngineChannel *)channel onChannelUpdate:(NSString *)props`

Called when the channel is updated.

You receive this callback after your app calls a server API to change the channel info.

**Parameters**

| channel | Channel instance the event comes from |
| --- | --- |
| props | Custom data |


## User callbacks
### engineChannel:onRemoteUserJoinChannel:()
`- (void)engineChannel:(RTCEngineChannel *)channel onRemoteUserJoinChannel:(NSString *)userId`

Called when a user joins the channel, including the current user.

The `engineChannel:onRemoteUserJoinChannel:` and `engineChannel:onRemoteUserLeaveChannel:reason:` callbacks are only for maintaining the channel's "user list". Receiving them doesn't mean there's video. Use `streamTracks` in the user info to check whether the user is publishing and to get the track numbers.

**Parameters**

| channel | Channel instance the event comes from |
| --- | --- |
| userId | User ID |


### engineChannel:onRemoteUserUpdate:()
`- (void)engineChannel:(RTCEngineChannel *)channel onRemoteUserUpdate:(NSString *)userId`

Called when a user's data in the current channel is updated.

**Parameters**

| channel | Channel instance the event comes from |
| --- | --- |
| userId | User ID |


### engineChannel:onRemoteUserLeaveChannel:reason:()
`- (void)engineChannel:(RTCEngineChannel *)channel onRemoteUserLeaveChannel:(NSString *)userId reason:(RTCLeaveReason)reason`

Called when a user leaves the channel, including the current user.

This callback is the counterpart of `engineChannel:onRemoteUserJoinChannel:`.

**Parameters**

| channel | Channel instance the event comes from |
| --- | --- |
| userId | User ID |
| reason | Leave reason; see [RTCLeaveReason](/en/rtc/ios/types#rtcleavereason) |


### engineChannel:onRemoteStreamTrackChange:streamTrackModel:changeType:()
`- (void)engineChannel:(RTCEngineChannel *)channel onRemoteStreamTrackChange:(NSString *)userId streamTrackModel:(RTCEngineStreamTrackModel *)streamTrackModel changeType:(RTCChangeType)changeType`

Called when a user's stream track data in the current channel changes.

**Parameters**

| channel | Channel instance the event comes from |
| --- | --- |
| userId | User ID |
| streamTrackModel | Stream track data; see [RTCEngineStreamTrackModel](/en/rtc/ios/types#rtcenginestreamtrackmodel) |
| changeType | Operation type; see [RTCChangeType](/en/rtc/ios/types#rtcchangetype) |


## Message callbacks
### engineChannel:onCustomMessage:action:userId:sessionId:nickname:()
`- (void)engineChannel:(RTCEngineChannel *)channel onCustomMessage:(NSString *)content action:(NSString *)action userId:(nullable NSString *)userId sessionId:(nullable NSString *)sessionId nickname:(nullable NSString *)nickname`

Called when a custom message arrives.

When your app's business features trigger an event through the server, the SDK notifies you through this callback.

**Parameters**

| channel | Channel instance the event comes from |
| --- | --- |
| content | Message content |
| action | Message action |
| userId | User ID |
| sessionId | Session ID |
| nickname | User nickname |


## Audio callbacks
### engineChannel:onAudioCapture:channels:stamp:dataSize:pcmData:()
`- (void)engineChannel:(RTCEngineChannel *)channel onAudioCapture:(int)samplerate channels:(int)channels stamp:(unsigned int)stamp dataSize:(int)dataSize pcmData:(void *)pcmData`

Called with captured audio data.

The SDK delivers the raw microphone PCM data through this callback after capturing it. You can use it for local recording, audio analysis, and similar scenarios.

Note: This callback fires on the audio capture thread. Don't do time-consuming work in it, and don't hold on to the `pcmData` pointer; copy the data yourself if you need to keep it.

**Parameters**

| channel | Channel instance the event comes from |
| --- | --- |
| samplerate | Sample rate |
| channels | Number of audio channels |
| stamp | Timestamp |
| dataSize | Data size |
| pcmData | Raw audio data |


### engineChannel:onAudioCaptureResampled:channels:stamp:resampledData:()
`- (void)engineChannel:(RTCEngineChannel *)channel onAudioCaptureResampled:(int)samplerate channels:(int)channels stamp:(unsigned int)stamp resampledData:(NSData *)resampledData`

Called with resampled captured audio data.

Unlike `engineChannel:onAudioCapture:channels:stamp:dataSize:pcmData:()`, the data has already been converted to the SDK's internal sample rate and is delivered as `NSData`, so you don't need to manage the memory yourself.

Note: This callback also fires on the audio capture thread. Don't do time-consuming work in it.

**Parameters**

| channel | Channel instance the event comes from |
| --- | --- |
| samplerate | Sample rate |
| channels | Number of audio channels |
| stamp | Timestamp |
| resampledData | Resampled audio data |


### engineChannel:onRemoteMemberAudioStatus:()
`- (void)engineChannel:(RTCEngineChannel *)channel onRemoteMemberAudioStatus:(NSArray<RTCStreamAudioModel *> *)audioArray`

Called with remote users' audio status.

Reports the audio status of users in the channel, including the audio decibel value, power, and more. You can use this callback to collect audio data for voice activation.

**Parameters**

| channel | Channel instance the event comes from |
| --- | --- |
| audioArray | List of user audio data; see [RTCStreamAudioModel](/en/rtc/ios/types#rtcstreamaudiomodel) |


### engineChannel:onServiceEnabledSpeak:()
`- (void)engineChannel:(RTCEngineChannel *)channel onServiceEnabledSpeak:(BOOL)enabled`

Called when the service allows or disallows speaking.

**Parameters**

| channel | Channel instance the event comes from |
| --- | --- |
| enabled | Whether speaking is allowed. YES: allowed; NO: not allowed |


## Media streaming callbacks
### engineChannelOnStreamMediaDidConnectSucceed:()
`- (void)engineChannelOnStreamMediaDidConnectSucceed:(RTCEngineChannel *)channel`

Called when the media streaming connection succeeds.

The SDK notifies you through this method when the channel's media streaming connects for the first time.

**Parameters**

| channel | Channel instance the event comes from |
| --- | --- |


### engineChannel:onStreamChangedVendorName:()
`- (void)engineChannel:(RTCEngineChannel *)channel onStreamChangedVendorName:(NSString *)vendorName`

Called when the media streaming platform changes.

When the media streaming platform used by the current channel switches, the SDK uses this callback to tell you the name of the platform now in effect.

**Parameters**

| channel | Channel instance the event comes from |
| --- | --- |
| vendorName | Platform name |


### engineChannel:onDownBitrateAdaptiveUserId:state:()
`- (void)engineChannel:(RTCEngineChannel *)channel onDownBitrateAdaptiveUserId:(NSString *)userId state:(RTCDownBitrateAdaptiveState)state`

Called with the downlink adaptive bitrate state.

**Parameters**

| channel | Channel instance the event comes from |
| --- | --- |
| userId | User ID |
| state | Downlink adaptive bitrate state; see [RTCDownBitrateAdaptiveState](/en/rtc/ios/types#rtcdownbitrateadaptivestate) |


### engineChannel:onUploadBitrateAdaptiveState:()
`- (void)engineChannel:(RTCEngineChannel *)channel onUploadBitrateAdaptiveState:(RTCUploadBitrateAdaptiveState)state`

Called with the uplink adaptive bitrate state.

**Parameters**

| channel | Channel instance the event comes from |
| --- | --- |
| state | Uplink adaptive bitrate state; see [RTCUploadBitrateAdaptiveState](/en/rtc/ios/types#rtcuploadbitrateadaptivestate) |


### engineChannel:onDownLossLevelChangeState:()
`- (void)engineChannel:(RTCEngineChannel *)channel onDownLossLevelChangeState:(RTCDownLossLevelState)state`

Called when the downlink average packet loss level changes.

**Parameters**

| channel | Channel instance the event comes from |
| --- | --- |
| state | Downlink average packet loss level; see [RTCDownLossLevelState](/en/rtc/ios/types#rtcdownlosslevelstate) |


### engineChannel:onDownLossRateAverage:()
`- (void)engineChannel:(RTCEngineChannel *)channel onDownLossRateAverage:(CGFloat)average`

Called with the downlink average packet loss rate.

**Parameters**

| channel | Channel instance the event comes from |
| --- | --- |
| average | Downlink average packet loss rate |


### engineChannel:onSendStreamModel:()
`- (void)engineChannel:(RTCEngineChannel *)channel onSendStreamModel:(RTCStreamSendModel *)sendModel`

Called with media streaming send status data.

You receive this callback at a fixed interval. It describes the current send status, such as latency and packet loss rate.

**Parameters**

| channel | Channel instance the event comes from |
| --- | --- |
| sendModel | Send status data; see [RTCStreamSendModel](/en/rtc/ios/types#rtcstreamsendmodel) |


### engineChannel:onReceiveStreamModel:()
`- (void)engineChannel:(RTCEngineChannel *)channel onReceiveStreamModel:(NSArray <RTCStreamReceiveModel *> *)receiveArray`

Called with media streaming receive status data.

You receive this callback at a fixed interval. It describes the current receive status, such as latency and packet loss rate.

**Parameters**

| channel | Channel instance the event comes from |
| --- | --- |
| receiveArray | Receive status data; see [RTCStreamReceiveModel](/en/rtc/ios/types#rtcstreamreceivemodel) |


### engineChannel:onSendQualitySample:()
`- (void)engineChannel:(RTCEngineChannel *)channel onSendQualitySample:(RTCStreamQualitySampleModel *)sample`

Called with a server-side uplink quality sample.

Available since SeaStart SFU 26.4. The server delivers it over the Signal DataChannel. It includes server-only metrics such as score, level, and mos, and complements the local `engineChannel:onSendStreamModel:`.

**Parameters**

| channel | Channel instance the event comes from |
| --- | --- |
| sample | Uplink quality sample; see [RTCStreamQualitySampleModel](/en/rtc/ios/types#rtcstreamqualitysamplemodel) |


### engineChannel:onReceiveQualitySample:()
`- (void)engineChannel:(RTCEngineChannel *)channel onReceiveQualitySample:(RTCStreamQualitySampleModel *)sample`

Called with a server-side downlink quality sample.

Available since SeaStart SFU 26.4. The server delivers it over the Signal DataChannel as an aggregate sample for the whole downlink, complementing the per-stream view of `engineChannel:onReceiveStreamModel:`.

**Parameters**

| channel | Channel instance the event comes from |
| --- | --- |
| sample | Downlink quality sample; see [RTCStreamQualitySampleModel](/en/rtc/ios/types#rtcstreamqualitysamplemodel) |


### engineChannel:onReceiveStreamStatusChange:trackId:status:()
`- (void)engineChannel:(RTCEngineChannel *)channel onReceiveStreamStatusChange:(NSString *)userId trackId:(RTCTrackIdentifierFlags)trackId status:(BOOL)status`

Called when the receive status of a remote stream changes.

After you subscribe to a user's remote video stream, you receive this callback if no video from that user arrives for a while. You also receive it when the video stream recovers.

**Parameters**

| channel | Channel instance the event comes from |
| --- | --- |
| userId | User ID |
| trackId | Track identifier; see [RTCTrackIdentifierFlags](/en/rtc/ios/types#rtctrackidentifierflags) |
| status | Receive status. YES: timed out; NO: recovered |


### engineChannel:onReceiveRetweetStreamStatusChange:status:()
`- (void)engineChannel:(RTCEngineChannel *)channel onReceiveRetweetStreamStatusChange:(NSString *)streamName status:(BOOL)status`

Called when the receive status of a re-streamed stream changes.

After you subscribe to a remote re-streamed stream, you receive this callback if no video from it arrives for a while. Re-streamed streams aren't reported as remote user video data; their receive status is reported separately through this callback.

**Parameters**

| channel | Channel instance the event comes from |
| --- | --- |
| streamName | Re-streamed stream name |
| status | Receive status. YES: timed out; NO: recovered |


## Screen sharing callbacks
### engineChannel:onScreenRecordStatus:()
`- (void)engineChannel:(RTCEngineChannel *)channel onScreenRecordStatus:(RTCScreenRecordStatus)status`

Called with the screen sharing status.

After you call the channel instance's `publishScreenRecord:()` to start screen sharing, the SDK uses this callback to notify the host app of the current screen sharing status.

**Parameters**

| channel | Channel instance the event comes from |
| --- | --- |
| status | Screen sharing status code; see [RTCScreenRecordStatus](/en/rtc/ios/types#rtcscreenrecordstatus) |
