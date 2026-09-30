---
title: "MeetingKitRoom"
description: "Meeting room instance of the SMeeting iOS (Objective-C) SDK: enter and exit the room, local audio, video, and sharing, chat and raise hand, host controls, cloud recording, waiting room, sub-meetings, sign-in, and room data queries. Read this for all in-meeting APIs."
---

`MeetingKitRoom` represents an independent meeting room and is created by `-[MeetingKit createRoomWithDelegate:]`. Each instance holds its own room context (room number, meeting ID, member cache, media connection). The same account can create and enter multiple rooms at the same time, and the media and business state of each room are independent of each other.

Account-level and device-level capabilities such as login, IM, meeting queries and scheduling, local camera capture and preview, audio routing, and process-side screen capture integration are provided centrally by the [MeetingKit](/en/meeting/ios/api-reference/MeetingKit) singleton and aren't duplicated on room instances.

<Warning>
A room instance becomes invalid after `exitRoom:` is called. To enter the meeting again, create a new instance with `createRoomWithDelegate:`.
</Warning>

```objectivec
MeetingKitRoom *room = [[MeetingKit sharedInstance] createRoomWithDelegate:self];
[room enterRoom:params onSuccess:^(id _Nullable data) {
    /// TO DO...
} onFailed:^(SEAError errCode, NSString * _Nullable errMsg) {
    /// TO DO...
}];
```

## Room properties
### delegate
`id<MeetingKitRoomDelegate> delegate`

Room event delegate. For details, see [MeetingKitRoomDelegate](/en/meeting/ios/api-reference/MeetingKitRoomDelegate).

### rtcChannel
`RTCEngineChannel *rtcChannel` (read-only)

The RTC channel instance for this room. For details, see [RTCEngineChannel](/en/rtc/ios/api-reference/RTCEngineChannel).

### roomNo
`NSString *roomNo` (read-only)

Current room number; empty before you enter the meeting.

### meetingId
`NSString *meetingId` (read-only)

Current meeting ID; empty before you enter the meeting.

### joined
`BOOL joined` (read-only, getter=isJoined)

Whether you've entered the room.

## Enter and exit APIs
### enterRoom:onSuccess:onFailed:()
`- (void)enterRoom:(SEAMeetingEnterParam *)params onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

Enters the room.

After you enter the room, the SDK notifies users in the room through the [meetingRoom:onUserEnter:()](/en/meeting/ios/api-reference/MeetingKitRoomDelegate) callback in `MeetingKitRoomDelegate`.

| Parameter | Description |
| :--- | --- |
| params | Room entry parameters; see [SEAMeetingEnterParam](/en/meeting/ios/types#seameetingenterparam) |
| onSuccess | Success callback |
| onFailed | Failure callback |


### exitRoom:()
`- (void)exitRoom:(nullable SEASuccessBlock)onSuccess`

Exits the room.

After you exit the room, the SDK notifies users in the room through the [meetingRoom:onUserExit:()](/en/meeting/ios/api-reference/MeetingKitRoomDelegate) callback in `MeetingKitRoomDelegate`.

| Parameter | Description |
| :--- | --- |
| onSuccess | Completion callback |

## Call APIs
### callUser:onSuccess:onFailed:()
`- (void)callUser:(NSArray <NSString *> *)userIdLists onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

Starts a call.

During the meeting, the host can call members with this API. After a member is called, the SDK notifies that user through the [onCallReceived:nickname:roomNo:title:()](/en/meeting/ios/api-reference/MeetingKitIMDelegate) callback in `MeetingKitIMDelegate`.

| Parameter | Description |
| :--- | --- |
| userIdLists | List of user IDs |
| onSuccess | Success callback |
| onFailed | Failure callback |

## User APIs
### updateName:onSuccess:onFailed:()
`- (void)updateName:(NSString *)username onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

Updates your own nickname.

After the user updates their nickname, the SDK notifies users in the room through the [meetingRoom:onUserNameChanged:nickname:()](/en/meeting/ios/api-reference/MeetingKitRoomDelegate) callback in `MeetingKitRoomDelegate`.

| Parameter | Description |
| :--- | --- |
| username | New nickname |
| onSuccess | Success callback |
| onFailed | Failure callback |


### requestOpenCamera:view:onSuccess:onFailed:()
`- (void)requestOpenCamera:(BOOL)frontCamera view:(VIEW_CLASS *)view onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

Requests to turn on the camera.

After you turn on the local camera in the room, the local video stream is published by default, and the SDK notifies users in the room through the [meetingRoom:onUserCameraStateChanged:cameraState:reason:()](/en/meeting/ios/api-reference/MeetingKitRoomDelegate) callback in `MeetingKitRoomDelegate`.

| Parameter | Description |
| :--- | --- |
| frontCamera | Camera direction; YES: front camera; NO: rear camera |
| view | Video rendering view |
| onSuccess | Success callback |
| onFailed | Failure callback |


### requestOpenMic:onFailed:()
`- (void)requestOpenMic:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

Requests to turn on the microphone.

After you turn on the local microphone in the room, the SDK notifies users in the room through the [meetingRoom:onUserMicStateChanged:micState:reason:()](/en/meeting/ios/api-reference/MeetingKitRoomDelegate) callback in `MeetingKitRoomDelegate`.

| Parameter | Description |
| :--- | --- |
| onSuccess | Success callback |
| onFailed | Failure callback |


### closeCamera:onFailed:()
`- (void)closeCamera:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

Turns off the camera.

After you turn off the local camera in the room, the SDK notifies users in the room through the [meetingRoom:onUserCameraStateChanged:cameraState:reason:()](/en/meeting/ios/api-reference/MeetingKitRoomDelegate) callback in `MeetingKitRoomDelegate`.

| Parameter | Description |
| :--- | --- |
| onSuccess | Success callback |
| onFailed | Failure callback |


### closeMic:onFailed:()
`- (void)closeMic:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

Turns off the microphone.

After you turn off the local microphone in the room, the SDK notifies users in the room through the [meetingRoom:onUserMicStateChanged:micState:reason:()](/en/meeting/ios/api-reference/MeetingKitRoomDelegate) callback in `MeetingKitRoomDelegate`.

| Parameter | Description |
| :--- | --- |
| onSuccess | Success callback |
| onFailed | Failure callback |


### requestShare:onSuccess:onFailed:()
`- (void)requestShare:(SEAShareType)shareType onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

Requests to start sharing.

After sharing starts, the SDK notifies users in the room through the [meetingRoom:onRoomShareStart:shareType:()](/en/meeting/ios/api-reference/MeetingKitRoomDelegate) callback in `MeetingKitRoomDelegate`.

| Parameter | Description |
| :--- | --- |
| shareType | Sharing type; see [SEAShareType](/en/meeting/ios/types#seasharetype) |
| onSuccess | Success callback |
| onFailed | Failure callback |


### stopShare:onFailed:()
`- (void)stopShare:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

Stops sharing.

After sharing stops, the SDK notifies users in the room through the [meetingRoom:onRoomShareStop:shareType:()](/en/meeting/ios/api-reference/MeetingKitRoomDelegate) callback in `MeetingKitRoomDelegate`.

| Parameter | Description |
| :--- | --- |
| onSuccess | Success callback |
| onFailed | Failure callback |


### sendRoomChatMessage:messageType:targetId:onSuccess:onFailed:()
`- (void)sendRoomChatMessage:(NSString *)message messageType:(SEAMessageType)messageType targetId:(nullable NSString *)targetId onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

Sends a chat message.

After the chat message is sent, the SDK notifies users in the room through the [meetingRoom:onReceiveChatMessage:message:messageType:()](/en/meeting/ios/api-reference/MeetingKitRoomDelegate) callback in `MeetingKitRoomDelegate`.

| Parameter | Description |
| :--- | --- |
| message | Chat message |
| messageType | Message type; see [SEAMessageType](/en/meeting/ios/types#seamessagetype) |
| targetId | Target ID; empty means everyone in the room receives it |
| onSuccess | Success callback |
| onFailed | Failure callback |


### sendRoomCustomMessage:targetId:onSuccess:onFailed:()
`- (void)sendRoomCustomMessage:(NSString *)message targetId:(nullable NSString *)targetId onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

Sends a custom message.

After the custom message is sent, the SDK notifies users in the room through the [meetingRoom:onReceiveChatMessage:message:messageType:()](/en/meeting/ios/api-reference/MeetingKitRoomDelegate) callback in `MeetingKitRoomDelegate`.

| Parameter | Description |
| :--- | --- |
| message | Chat message |
| targetId | Target ID; empty means everyone in the room receives it |
| onSuccess | Success callback |
| onFailed | Failure callback |


### getChatList:onFailed:()
`- (void)getChatList:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

Gets the chat list.

| Parameter | Description |
| :--- | --- |
| onSuccess | Success callback; see [SEAChatListModel](/en/meeting/ios/types#seachatlistmodel) |
| onFailed | Failure callback |


### getMoreChatList:onFailed:()
`- (void)getMoreChatList:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

Gets more of the chat list (next page).

| Parameter | Description |
| :--- | --- |
| onSuccess | Success callback; see [SEAChatListModel](/en/meeting/ios/types#seachatlistmodel) |
| onFailed | Failure callback |


### requestHandup:onSuccess:onFailed:()
`- (void)requestHandup:(SEAHandupType)handupType onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

Raises a hand.

After you raise your hand, the SDK notifies the room's host and co-hosts through the [meetingRoom:onRoomHandUpChanged:enable:handupType:()](/en/meeting/ios/api-reference/MeetingKitRoomDelegate) callback in `MeetingKitRoomDelegate`.

| Parameter | Description |
| :--- | --- |
| handupType | Raise hand type; see [SEAHandupType](/en/meeting/ios/types#seahanduptype) |
| onSuccess | Success callback |
| onFailed | Failure callback |


### cancelHandup:onSuccess:onFailed:()
`- (void)cancelHandup:(SEAHandupType)handupType onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

Lowers a raised hand.

After you lower your hand, the SDK notifies the room's host and co-hosts through the [meetingRoom:onRoomHandUpChanged:enable:handupType:()](/en/meeting/ios/api-reference/MeetingKitRoomDelegate) callback in `MeetingKitRoomDelegate`.

| Parameter | Description |
| :--- | --- |
| handupType | Raise hand type; see [SEAHandupType](/en/meeting/ios/types#seahanduptype) |
| onSuccess | Success callback |
| onFailed | Failure callback |


### confirmAdminOpenCamera:frontCamera:view:onSuccess:onFailed:()
`- (void)confirmAdminOpenCamera:(NSString *)targetId frontCamera:(BOOL)frontCamera view:(VIEW_CLASS *)view onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

Replies to accept a request to turn on the camera.

When the host or a co-host invites you to turn on your camera and you agree, call this API to reply to that host or co-host. Likewise, after you raise your hand and receive the host's or co-host's decision, if you need to turn on your camera, call this API to reply to them.

After you accept the camera request, the SDK notifies the room's host and co-hosts through the [meetingRoom:onUserCameraStateChanged:cameraState:reason:()](/en/meeting/ios/api-reference/MeetingKitRoomDelegate) callback in `MeetingKitRoomDelegate`.

| Parameter | Description |
| :--- | --- |
| targetId | Target ID: the ID of the host or co-host who requested or approved turning on your camera |
| frontCamera | Camera direction; YES: front camera; NO: rear camera |
| view | Video rendering view |
| onSuccess | Success callback |
| onFailed | Failure callback |


### confirmAdminOpenMic:onSuccess:onFailed:()
`- (void)confirmAdminOpenMic:(NSString *)targetId onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

Replies to accept a request to turn on the microphone.

When the host or a co-host invites you to turn on your microphone and you agree, call this API to reply to that host or co-host. Likewise, after you raise your hand and receive the host's or co-host's decision, if you need to turn on your microphone, call this API to reply to them.

After you accept the microphone request, the SDK notifies the room's host and co-hosts through the [meetingRoom:onUserMicStateChanged:micState:reason:()](/en/meeting/ios/api-reference/MeetingKitRoomDelegate) callback in `MeetingKitRoomDelegate`.

| Parameter | Description |
| :--- | --- |
| targetId | Target ID: the ID of the host or co-host who requested or approved turning on your microphone |
| onSuccess | Success callback |
| onFailed | Failure callback |


### confirmAdminRoomShare:shareType:onSuccess:onFailed:()
`- (void)confirmAdminRoomShare:(NSString *)targetId shareType:(SEAShareType)shareType onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

Replies to accept a request to start sharing in the room.

When the host or a co-host invites you to start sharing and you agree, call this API to reply to that host or co-host. Likewise, after you raise your hand and receive the host's or co-host's decision, if you need to start sharing, call this API to reply to them.

After you accept the sharing request, the SDK notifies the room's host and co-hosts through the [meetingRoom:onRoomShareStart:shareType:()](/en/meeting/ios/api-reference/MeetingKitRoomDelegate) callback in `MeetingKitRoomDelegate`.

| Parameter | Description |
| :--- | --- |
| targetId | Target ID: the ID of the host or co-host who requested or approved your room sharing request |
| shareType | Sharing type; see [SEAShareType](/en/meeting/ios/types#seasharetype) |
| onSuccess | Success callback |
| onFailed | Failure callback |

## Audio control APIs
### switchSpeaker:()
`- (void)switchSpeaker:(BOOL)enabled`

Sets the remote audio playback state.

Use this API to turn remote audio playback on or off. It doesn't switch between the speaker, the earpiece, or external device routes.

| Parameter | Description |
| :--- | --- |
| enabled | Remote audio playback state; YES: on; NO: off |


### enabledAudioModule:()
`- (void)enabledAudioModule:(BOOL)enabled`

Starts or stops the local audio unit.

Supported since `1.3.6`. In purely local playback scenarios where this device neither captures nor receives RTC audio, such as playing back a recording or live stream, turning off the audio unit releases the underlying voice processing unit and keeps the local player's volume from being lowered; when you leave such a scenario, restore it to automatic management. The SDK resets it to automatic management every time you enter a room.

| Parameter | Description |
| :--- | --- |
| enabled | YES: the audio unit is managed automatically by the underlying layer; NO: stop the audio unit |


### enabledSendAudio:()
`- (RTCEngineError)enabledSendAudio:(BOOL)enabled`

Pauses or resumes publishing local audio to this room.

Supported since `2.0.0`. When you're in multiple rooms, pausing audio sending in one room doesn't affect the others.

| Parameter | Description |
| :--- | --- |
| enabled | YES: audio on; NO: audio off |

## Video rendering APIs
### publishLocalVideo:()
`- (RTCEngineError)publishLocalVideo:(BOOL)publish`

Pauses or resumes publishing local video to this room.

Supported since `2.0.0`. On iOS, the camera is a single shared piece of hardware: capture and preview are controlled by the [MeetingKit](/en/meeting/ios/api-reference/MeetingKit) singleton, and each instance independently controls whether that video is published to its room. When you're in multiple rooms, pausing publishing in one room doesn't affect the others.

| Parameter | Description |
| :--- | --- |
| publish | YES: resume; NO: pause |


### startRemoteView:streamType:view:()
`- (void)startRemoteView:(NSString *)userId streamType:(SEAVideoStreamType)streamType view:(VIEW_CLASS *)view`

Starts playing a remote user's video.

Starts playing a remote user's video and binds the video rendering resources.

| Parameter | Description |
| :--- | --- |
| userId | Remote user ID |
| streamType | Video stream type; see [SEAVideoStreamType](/en/meeting/ios/types#seavideostreamtype) |
| view | Video rendering view |


### stopRemoteView:streamType:()
`- (void)stopRemoteView:(NSString *)userId streamType:(SEAVideoStreamType)streamType`

Stops playing a remote user's video.

Stops playing a remote user's video and releases the video rendering resources.

| Parameter | Description |
| :--- | --- |
| userId | Remote user ID |
| streamType | Video stream type; see [SEAVideoStreamType](/en/meeting/ios/types#seavideostreamtype) |


### stopAllRemoteViewWithUserId:()
`- (void)stopAllRemoteViewWithUserId:(NSString *)userId`

Stops playing all video of a remote user.

Stops playing all of a remote user's video and releases all rendering resources.

| Parameter | Description |
| :--- | --- |
| userId | Remote user ID |


### startRemoteMixture:()
`- (void)startRemoteMixture:(VIEW_CLASS *)view`

Subscribes to the remote composite video stream.

Subscribes to the remote composite video stream and binds the video rendering view.

| Parameter | Description |
| :--- | --- |
| view | Video rendering view |


### stopRemoteMixture()
`- (void)stopRemoteMixture`

Stops subscribing to the remote composite video stream.

Stops subscribing to the remote composite video stream and releases the rendering view.


### startRemoteRetweet:view:()
`- (void)startRemoteRetweet:(NSString *)streamName view:(VIEW_CLASS *)view`

Subscribes to a remote re-streamed audio and video stream (pulled over WebRTC).

Subscribes to the remote re-streamed audio and video stream whose stream name you pass in; a single connection receives both audio and video, and the video rendering view is bound. The re-streamed stream isn't reported as remote user video data; its receive status is reported separately through onReceiveRetweetStreamStatusChange:status:. Currently only the `wangsu` streaming vendor is supported.

| Parameter | Description |
| :--- | --- |
| streamName | Name of the remote stream to subscribe to (passed in by you) |
| view | Video rendering view |


### stopRemoteRetweet:()
`- (void)stopRemoteRetweet:(NSString *)streamName`

Stops subscribing to a remote re-streamed audio and video stream.

Stops subscribing to the remote re-streamed audio and video stream with the specified name and releases the rendering view.

| Parameter | Description |
| :--- | --- |
| streamName | Name of the remote stream to stop subscribing to (passed in by you) |

## Screen sharing APIs
### stopScreenRecord()
`- (void)stopScreenRecord`

Stops screen capture from the host app.

Use this method in the host app when the user actively stops screen sharing.

Starting with `2.0.1`, this API stops this room's sharing stream and also ends the current system screen recording (disconnecting the extension). The capture service keeps listening during the meeting, so the user can start screen recording again from the system panel.

After screen capture is turned off, the SDK notifies you of the current device capture status through the [meetingRoom:onScreenRecordStatus:()](/en/meeting/ios/api-reference/MeetingKitRoomDelegate) callback in `MeetingKitRoomDelegate`. Based on the status in the callback, choose whether to request to start sharing or to stop sharing.

### publishScreenViewCaptureWithPixelBuffer:displayAngle:()
`- (void)publishScreenViewCaptureWithPixelBuffer:(CVPixelBufferRef)pixelBuffer displayAngle:(int)displayAngle`

Publishes a view capture sharing stream; that is, you can use this API to feed video data into the track shared with screen sharing.

**Parameters**

| pixelBuffer |  Pixel data captured from a UIView (CVPixelBufferRef) |
| --- | --- |
| displayAngle | Display angle (0/90/180/270) |

### enabledViewCaptureShare:()
`- (RTCEngineError)enabledViewCaptureShare:(BOOL)enabled`

Sets view capture sharing. This API tells the SDK whether the current screen sharing track is publishing a screen capture stream or a view capture stream; call it to mark the SDK before calling `publishScreenViewCaptureWithPixelBuffer:displayAngle:()`.

**Parameters**

| enabled |  Enabled state; YES: on; NO: off |
| --- | --- |

## Host APIs
### adminDestroyRoom:onFailed:()
`- (void)adminDestroyRoom:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

Ends the meeting and dissolves the room (host or co-host only).

After the room ends, the SDK notifies users in the room through the [meetingRoom:onExitRoom:()](/en/meeting/ios/api-reference/MeetingKitRoomDelegate) callback in `MeetingKitRoomDelegate`.

| Parameter | Description |
| :--- | --- |
| onSuccess | Success callback |
| onFailed | Failure callback |


### adminUpdateRoomCameraState:selfUnmuteCameraDisabled:onSuccess:onFailed:()
`- (void)adminUpdateRoomCameraState:(BOOL)cameraDisabled selfUnmuteCameraDisabled:(BOOL)selfUnmuteCameraDisabled onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

Updates camera off for everyone in the room, which controls whether all users in the current room are allowed to turn on their camera capture devices (host or co-host only).

After camera off for everyone is updated, the SDK notifies users in the room through the [meetingRoom:onRoomCameraStateChanged:selfUnmuteCameraDisabled:userId:()](/en/meeting/ios/api-reference/MeetingKitRoomDelegate) callback in `MeetingKitRoomDelegate`.

| Parameter | Description |
| :--- | --- |
| cameraDisabled | Room camera disabled state; YES: disabled; NO: enabled |
| selfUnmuteCameraDisabled | Whether members are prevented from turning their cameras back on themselves; YES: prevented; NO: allowed |
| onSuccess | Success callback |
| onFailed | Failure callback |


### adminUpdateRoomMicState:selfUnmuteMicDisabled:onSuccess:onFailed:()
`- (void)adminUpdateRoomMicState:(BOOL)micDisabled selfUnmuteMicDisabled:(BOOL)selfUnmuteMicDisabled onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

Updates mute all in the room, which controls whether all users in the current room are allowed to turn on their microphone capture devices (host or co-host only).

After mute all is updated, the SDK notifies users in the room through the [meetingRoom:onRoomMicStateChanged:selfUnmuteMicDisabled:userId:()](/en/meeting/ios/api-reference/MeetingKitRoomDelegate) callback in `MeetingKitRoomDelegate`.

| Parameter | Description |
| :--- | --- |
| micDisabled | Room microphone disabled state; YES: disabled; NO: enabled |
| selfUnmuteMicDisabled | Whether members are prevented from unmuting themselves; YES: prevented; NO: allowed |
| onSuccess | Success callback |
| onFailed | Failure callback |


### adminUpdateRoomSelfUnmuteCameraDisabled:onSuccess:onFailed:()
`- (void)adminUpdateRoomSelfUnmuteCameraDisabled:(BOOL)selfUnmuteCameraDisabled onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

Updates whether members in the room are prevented from turning their cameras back on themselves, which controls whether all users in the current room can turn on their camera capture devices on their own.

After this is updated, the SDK notifies users in the room through the [meetingRoom:onRoomCameraStateChanged:selfUnmuteCameraDisabled:userId:()](/en/meeting/ios/api-reference/MeetingKitRoomDelegate) callback in `MeetingKitRoomDelegate`.

| Parameter | Description |
| :--- | --- |
| selfUnmuteCameraDisabled | Whether members are prevented from turning their cameras back on themselves; YES: prevented; NO: allowed |
| onSuccess | Success callback |
| onFailed | Failure callback |


### adminUpdateRoomSelfUnmuteMicDisabled:onSuccess:onFailed:()
`- (void)adminUpdateRoomSelfUnmuteMicDisabled:(BOOL)selfUnmuteMicDisabled onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

Updates whether members in the room are prevented from unmuting themselves, which controls whether all users in the current room can turn on their microphone capture devices on their own.

After this is updated, the SDK notifies users in the room through the [meetingRoom:onRoomMicStateChanged:selfUnmuteMicDisabled:userId:()](/en/meeting/ios/api-reference/MeetingKitRoomDelegate) callback in `MeetingKitRoomDelegate`.

| Parameter | Description |
| :--- | --- |
| selfUnmuteMicDisabled | Whether members are prevented from unmuting themselves; YES: prevented; NO: allowed |
| onSuccess | Success callback |
| onFailed | Failure callback |


### adminUpdateRoomChatDisabled:onSuccess:onFailed:()
`- (void)adminUpdateRoomChatDisabled:(BOOL)chatDisabled onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

Updates the room's chat disabled state, which controls whether all users in the current room are allowed to chat (host or co-host only).

After the room's chat disabled state is updated, the SDK notifies users in the room through the [meetingRoom:onRoomChatDisabledChanged:userId:()](/en/meeting/ios/api-reference/MeetingKitRoomDelegate) callback in `MeetingKitRoomDelegate`.

| Parameter | Description |
| :--- | --- |
| chatDisabled | Chat disabled state; YES: disabled; NO: enabled |
| onSuccess | Success callback |
| onFailed | Failure callback |


### adminUpdateRoomShareDisabled:onSuccess:onFailed:()
`- (void)adminUpdateRoomShareDisabled:(BOOL)shareDisabled onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

Updates the room's sharing disabled state, which controls whether all users in the current room are allowed to share (host or co-host only).

After the room's sharing disabled state is updated, the SDK notifies users in the room through the [meetingRoom:onRoomShareDisabledChanged:userId:()](/en/meeting/ios/api-reference/MeetingKitRoomDelegate) callback in `MeetingKitRoomDelegate`.

| Parameter | Description |
| :--- | --- |
| shareDisabled | Sharing disabled state; YES: disabled; NO: enabled |
| onSuccess | Success callback |
| onFailed | Failure callback |


### adminUpdateRoomScreenshotDisabled:onSuccess:onFailed:()
`- (void)adminUpdateRoomScreenshotDisabled:(BOOL)screenshotDisabled onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

Updates the room's screenshot permission, which controls whether all users in the current room are allowed to take screenshots (host or co-host only).

After the room's screenshot permission is updated, the SDK notifies users in the room through the [meetingRoom:onRoomScreenshotDisabledChanged:userId:()](/en/meeting/ios/api-reference/MeetingKitRoomDelegate) callback in `MeetingKitRoomDelegate`.

| Parameter | Description |
| :--- | --- |
| screenshotDisabled | Screenshot disabled state; YES: disabled; NO: enabled |
| onSuccess | Success callback |
| onFailed | Failure callback |


### adminUpdateRoomWatermarkDisabled:onSuccess:onFailed:()
`- (void)adminUpdateRoomWatermarkDisabled:(BOOL)watermarkDisabled onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

Updates the room's watermark switch, which controls whether the watermark is on in the current room (host or co-host only).

After the room's watermark switch is updated, the SDK notifies users in the room through the [meetingRoom:onRoomWatermarkDisabledChanged:userId:()](/en/meeting/ios/api-reference/MeetingKitRoomDelegate) callback in `MeetingKitRoomDelegate`.

| Parameter | Description |
| :--- | --- |
| watermarkDisabled | Room watermark disabled state; YES: disabled; NO: enabled |
| onSuccess | Success callback |
| onFailed | Failure callback |


### adminUpdateRoomLocked:onSuccess:onFailed:()
`- (void)adminUpdateRoomLocked:(BOOL)locked onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

Updates the room's locked state, which controls whether the current room is locked (host or co-host only).

After the room's locked state is updated, the SDK notifies users in the room through the [meetingRoom:onRoomLockedChanged:userId:()](/en/meeting/ios/api-reference/MeetingKitRoomDelegate) callback in `MeetingKitRoomDelegate`.

| Parameter | Description |
| :--- | --- |
| locked | Locked state; YES: locked; NO: unlocked |
| onSuccess | Success callback |
| onFailed | Failure callback |


### adminUpdateNickname:nickname:onSuccess:onFailed:()
`- (void)adminUpdateNickname:(NSString *)userId nickname:(NSString *)nickname onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

Updates a user's nickname (host or co-host only).

After the user's nickname is updated, the SDK notifies users in the room through the [meetingRoom:onUserNameChanged:nickname:()](/en/meeting/ios/api-reference/MeetingKitRoomDelegate) callback in `MeetingKitRoomDelegate`.

| Parameter | Description |
| :--- | --- |
| userId | User ID |
| nickname | User nickname |
| onSuccess | Success callback |
| onFailed | Failure callback |


### adminUpdateUserRole:userRole:onSuccess:onFailed:()
`- (void)adminUpdateUserRole:(NSString *)userId userRole:(SEAUserRole)userRole onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

Updates a user's role (host or co-host only).

After the user's role is updated, the SDK notifies users in the room through the [meetingRoom:onUserRoleChanged:userRole:()](/en/meeting/ios/api-reference/MeetingKitRoomDelegate) callback in `MeetingKitRoomDelegate`.

| Parameter | Description |
| :--- | --- |
| userId | User ID |
| userRole | User role; see [SEAUserRole](/en/meeting/ios/types#seauserrole) |
| onSuccess | Success callback |
| onFailed | Failure callback |


### adminMoveHost:onSuccess:onFailed:()
`- (void)adminMoveHost:(NSString *)userId onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

Transfers the host role (host or co-host only).

After the host is transferred, the SDK notifies users in the room through the [meetingRoom:onRoomMoveHost:sourceUserId:()](/en/meeting/ios/api-reference/MeetingKitRoomDelegate) callback in `MeetingKitRoomDelegate`.

| Parameter | Description |
| :--- | --- |
| userId | User ID |
| onSuccess | Success callback |
| onFailed | Failure callback |


### adminUpdateUserChatDisabled:chatDisabled:onSuccess:onFailed:()
`- (void)adminUpdateUserChatDisabled:(NSString *)userId chatDisabled:(BOOL)chatDisabled onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

The host updates a user's chat state (host or co-host only).

After the host updates the user's chat state, the SDK notifies the target user in the room through the [meetingRoom:onUserChatDisabledChanged:userId:()](/en/meeting/ios/api-reference/MeetingKitRoomDelegate) callback in `MeetingKitRoomDelegate`.

| Parameter | Description |
| :--- | --- |
| userId | User ID |
| chatDisabled | Disabled state; YES: disabled; NO: enabled |
| onSuccess | Success callback |
| onFailed | Failure callback |


### adminUpdateUserDrawDisabled:drawDisabled:onSuccess:onFailed:()
`- (void)adminUpdateUserDrawDisabled:(NSString *)userId drawDisabled:(BOOL)drawDisabled onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

The host updates a user's drawing permission (host or co-host only).

After the host updates the user's drawing permission, the SDK notifies the target user in the room through the [meetingRoom:onUserDrawDisabledChanged:userId:()](/en/meeting/ios/api-reference/MeetingKitRoomDelegate) callback in `MeetingKitRoomDelegate`.

| Parameter | Description |
| :--- | --- |
| userId | User ID |
| drawDisabled | Disabled state; YES: disabled; NO: enabled |
| onSuccess | Success callback |
| onFailed | Failure callback |


### adminRequestUserOpenShare:onSuccess:onFailed:()
`- (void)adminRequestUserOpenShare:(NSString *)userId onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

Asks a member to start screen sharing (host or co-host only).

After the request is sent, the SDK notifies the specified user in the room through the [meetingRoom:onRequestOpenShare:()](/en/meeting/ios/api-reference/MeetingKitRoomDelegate) callback in `MeetingKitRoomDelegate`.

| Parameter | Description |
| :--- | --- |
| userId | User ID |
| onSuccess | Success callback |
| onFailed | Failure callback |


### adminRequestUserOpenCamera:onSuccess:onFailed:()
`- (void)adminRequestUserOpenCamera:(NSString *)userId onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

Asks a member to turn on their camera (host or co-host only).

After the request is sent, the SDK notifies the specified user in the room through the [meetingRoom:onRequestOpenCamera:()](/en/meeting/ios/api-reference/MeetingKitRoomDelegate) callback in `MeetingKitRoomDelegate`.

| Parameter | Description |
| :--- | --- |
| userId | User ID |
| onSuccess | Success callback |
| onFailed | Failure callback |


### adminCloseUserCamera:onSuccess:onFailed:()
`- (void)adminCloseUserCamera:(NSString *)userId onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

Turns off a remote user's camera (host or co-host only).

After the remote user's camera is turned off, the SDK notifies users in the room through the [meetingRoom:onUserCameraStateChanged:cameraState:reason:()](/en/meeting/ios/api-reference/MeetingKitRoomDelegate) callback in `MeetingKitRoomDelegate`.

| Parameter | Description |
| :--- | --- |
| userId | User ID |
| onSuccess | Success callback |
| onFailed | Failure callback |


### adminRequestUserOpenMic:onSuccess:onFailed:()
`- (void)adminRequestUserOpenMic:(NSString *)userId onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

Asks a member to turn on their microphone (host or co-host only).

After the request is sent, the SDK notifies the specified user in the room through the [meetingRoom:onRequestOpenMic:()](/en/meeting/ios/api-reference/MeetingKitRoomDelegate) callback in `MeetingKitRoomDelegate`.

| Parameter | Description |
| :--- | --- |
| userId | User ID |
| onSuccess | Success callback |
| onFailed | Failure callback |


### adminCloseUserMic:onSuccess:onFailed:()
`- (void)adminCloseUserMic:(NSString *)userId onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

Turns off a remote user's microphone (host or co-host only).

After the remote user's microphone is turned off, the SDK notifies users in the room through the [meetingRoom:onUserMicStateChanged:micState:reason:()](/en/meeting/ios/api-reference/MeetingKitRoomDelegate) callback in `MeetingKitRoomDelegate`.

| Parameter | Description |
| :--- | --- |
| userId | User ID |
| onSuccess | Success callback |
| onFailed | Failure callback |


### adminKickUserOut:joinDisabled:onSuccess:onFailed:()
`- (void)adminKickUserOut:(NSString *)userId joinDisabled:(BOOL)joinDisabled onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

Removes a member (host or co-host only).

After the member is removed, the SDK notifies the specified user in the room through the [meetingRoom:onExitRoom:()](/en/meeting/ios/api-reference/MeetingKitRoomDelegate) callback in `MeetingKitRoomDelegate`.

| Parameter | Description |
| :--- | --- |
| userId | User ID |
| joinDisabled | Whether to prevent the member from entering the room again; `YES`: prevent; `NO`: allow |
| onSuccess | Success callback |
| onFailed | Failure callback |


### adminStopRoomShare:onFailed:()
`- (void)adminStopRoomShare:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

Stops sharing (host or co-host only).

After sharing stops, the SDK notifies users in the room through the [meetingRoom:onAdminRoomShareStop:shareType:()](/en/meeting/ios/api-reference/MeetingKitRoomDelegate) callback in `MeetingKitRoomDelegate`.

| Parameter | Description |
| :--- | --- |
| onSuccess | Success callback |
| onFailed | Failure callback |


### adminConfirmHandup:handupType:approve:onSuccess:onFailed:()
`- (void)adminConfirmHandup:(NSString *)userId handupType:(SEAHandupType)handupType approve:(BOOL)approve onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

Handles a raise-hand request (host or co-host only).

After the raise-hand request is handled, the SDK notifies the specified user in the room through the [meetingRoom:onHandupConfirm:approve:userId:()](/en/meeting/ios/api-reference/MeetingKitRoomDelegate) callback in `MeetingKitRoomDelegate`.

| Parameter | Description |
| :--- | --- |
| userId | User ID |
| handupType | Raise-hand request type |
| approve | Result of handling the raised hand; YES: approve; NO: reject |
| onSuccess | Success callback |
| onFailed | Failure callback |


### adminUpdateConferee:onSuccess:onFailed:()
`- (void)adminUpdateConferee:(NSArray <NSString *> *)conferee onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

The host updates invitees (host or co-host only).

After the invitees are updated, the SDK adds the target members to the meeting's invitee list. The target members can also find the meeting in their list of upcoming meetings.

| Parameter | Description |
| :--- | --- |
| conferee | List of member IDs |
| onSuccess | Success callback |
| onFailed | Failure callback |


### adminInviteAgent:onSuccess:onFailed:()
`- (void)adminInviteAgent:(NSArray <SEAInviteModel *> *)invitesList onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

The host invites devices to the meeting (host or co-host only).

After the devices are invited, the SDK brings the target devices, such as SIP or H.323 devices, into the meeting. If something goes wrong, such as a device already being in another meeting, the SDK reports the specific failure reason through the `onFailed` callback.

| Parameter | Description |
| :--- | --- |
| invitesList | Invitation list; see [SEAInviteModel](/en/meeting/ios/types#seainvitemodel) |
| onSuccess | Success callback |
| onFailed | Failure callback |

## Cloud recording APIs
### getCloudRecordDetail:onFailed:()
`- (void)getCloudRecordDetail:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

Gets cloud recording details (host or co-host only).

| Parameter | Description |
| :--- | --- |
| onSuccess | Success callback; see [SEACloudRecordDetailsModel](/en/meeting/ios/types#seacloudrecorddetailsmodel) |
| onFailed | Failure callback |


### getCloudRecordConfig:onFailed:()
`- (void)getCloudRecordConfig:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

Gets the cloud recording configuration (host or co-host only).

| Parameter | Description |
| :--- | --- |
| onSuccess | Success callback; see [SEACloudRecordConfigModel](/en/meeting/ios/types#seacloudrecordconfigmodel) |
| onFailed | Failure callback |


### startCloudRecord:onSuccess:onFailed:()
`- (void)startCloudRecord:(SEACloudRecordParam *)params onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

Starts cloud recording (host or co-host only).

| Parameter | Description |
| :--- | --- |
| params | Cloud recording parameters; see [SEACloudRecordParam](/en/meeting/ios/types#seacloudrecordparam) |
| onSuccess | Success callback |
| onFailed | Failure callback |


### stopCloudRecord:onSuccess:onFailed:()
`- (void)stopCloudRecord:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

Stops cloud recording (host or co-host only).

| Parameter | Description |
| :--- | --- |
| onSuccess | Success callback |
| onFailed | Failure callback |

## Waiting room APIs
### exitWaitingRoom:onSuccess:()
`- (void)exitWaitingRoom:(NSString *)roomNo onSuccess:(nullable SEASuccessBlock)onSuccess`

Requests to exit the waiting room.

After the user exits the waiting room, the SDK notifies the room's host and co-hosts through the [meetingRoom:onRoomUserExitWaitingRoom:nickname:()](/en/meeting/ios/api-reference/MeetingKitRoomDelegate) callback in `MeetingKitRoomDelegate`.

| Parameter | Description |
| :--- | --- |
| roomNo | Meeting number |
| onSuccess | Success callback |


### adminUpdateWaitingRoomDisabled:onSuccess:onFailed:()
`- (void)adminUpdateWaitingRoomDisabled:(BOOL)waitingRoomDisabled onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

Updates the room's waiting room disabled state, which controls whether the waiting room is on in the current room (host or co-host only).

After the room's waiting room disabled state is updated, the SDK notifies users in the room through the [meetingRoom:onRoomWaitingRoomDisabledChanged:userId:()](/en/meeting/ios/api-reference/MeetingKitRoomDelegate) callback in `MeetingKitRoomDelegate`.

| Parameter | Description |
| :--- | --- |
| waitingRoomDisabled | Room waiting room disabled state; YES: disabled; NO: enabled |
| onSuccess | Success callback |
| onFailed | Failure callback |


### adminMoveInWaitingRoom:nickname:onSuccess:onFailed:()
`- (void)adminMoveInWaitingRoom:(NSString *)userId nickname:(NSString *)nickname onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

Moves a meeting member to the waiting room. The host or a co-host can use this API to move an in-meeting member to the waiting room (host or co-host only), and the SDK notifies the target user through the [meetingRoom:onRoomMoveInWaitingRoom:()](/en/meeting/ios/api-reference/MeetingKitRoomDelegate) callback in `MeetingKitRoomDelegate`.

| Parameter | Description |
| :--- | --- |
| userId | User ID |
| nickname | User nickname |
| onSuccess | Success callback |
| onFailed | Failure callback |


### adminMoveOutWaitingRoom:onSuccess:onFailed:()
`- (void)adminMoveOutWaitingRoom:(nullable NSString *)userId onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

Moves people from the waiting room into the meeting. The host or a co-host can use this API to move members currently in the waiting room into the meeting (host or co-host only), and the SDK notifies the target user through the [onWaitingRoomMoveInRoom:title:()](/en/meeting/ios/api-reference/MeetingKitIMDelegate) callback in `MeetingKitIMDelegate`.

| Parameter | Description |
| :--- | --- |
| userId | User ID; pass empty for all members |
| onSuccess | Success callback |
| onFailed | Failure callback |


### adminGetWaitingRoomUserList:onFailed:()
`- (void)adminGetWaitingRoomUserList:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

The host gets the list of users in the waiting room.

| Parameter | Description |
| :--- | --- |
| onSuccess | Success callback; see [SEAWaitingRoomMemberListModel](/en/meeting/ios/types#seawaitingroommemberlistmodel) |
| onFailed | Failure callback |

## Sub-meeting APIs
### subMeetingHelp:onFailed:()
`- (void)subMeetingHelp:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

A sub-meeting member asks the host or a co-host for help, and the SDK notifies the host and co-hosts through the [onSubMettingAskingHelp:meetingId:title:()](/en/meeting/ios/api-reference/MeetingKitIMDelegate) callback in `MeetingKitIMDelegate`.

| Parameter | Description |
| :--- | --- |
| onSuccess | Success callback |
| onFailed | Failure callback |


### adminUpdateEnterBeforeHostDisabled:onSuccess:onFailed:()
`- (void)adminUpdateEnterBeforeHostDisabled:(BOOL)enterBeforeHostDisabled onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

Updates whether entering the meeting before the host is prevented, which controls whether members in the current room can enter the meeting before the host (host or co-host only).

| Parameter | Description |
| :--- | --- |
| enterBeforeHostDisabled | Prevented state; YES: prevented; NO: allowed |
| onSuccess | Success callback |
| onFailed | Failure callback |


### adminCreateSubMeeting:onSuccess:onFailed:()
`- (void)adminCreateSubMeeting:(NSArray <NSString *> *)titleList onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed;`

The host creates sub-meetings.

| Parameter | Description |
| :--- | --- |
| titleList | List of titles |
| onSuccess | Success callback |
| onFailed | Failure callback |


### adminUpdateSubMeetingTitle:targetId:onSuccess:onFailed:()
`- (void)adminUpdateSubMeetingTitle:(NSString *)title targetId:(NSString *)targetId onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

The host changes a sub-meeting's title.

| Parameter | Description |
| :--- | --- |
| title | Sub-meeting title |
| targetId | Sub-meeting ID |
| onSuccess | Success callback |
| onFailed | Failure callback |


### adminUpdateSubMeetingConferee:targetId:onSuccess:onFailed:()
`- (void)adminUpdateSubMeetingConferee:(NSArray <SEAConfereeModel *> *)confereeList targetId:(NSString *)targetId onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

The host changes a sub-meeting's members.

| Parameter | Description |
| :--- | --- |
| confereeList | Sub-meeting member list; see [SEAConfereeModel](/en/meeting/ios/types#seaconfereemodel) |
| targetId | Sub-meeting ID |
| onSuccess | Success callback |
| onFailed | Failure callback |


### adminDeleteSubMeeting:onSuccess:onFailed:()
`- (void)adminDeleteSubMeeting:(NSArray <NSString *> *)targetList onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

The host deletes sub-meetings.

| Parameter | Description |
| :--- | --- |
| targetList | List of sub-meeting IDs |
| onSuccess | Success callback |
| onFailed | Failure callback |


### adminGetSubMeetingList:onSuccess:onFailed:()
`- (void)adminGetSubMeetingList:(NSString *)meetingId onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

The host requests the sub-meeting list.

| Parameter | Description |
| :--- | --- |
| meetingId | Meeting ID |
| onSuccess | Success callback; see [SEARoomSubMeetingListModel](/en/meeting/ios/types#searoomsubmeetinglistmodel) |
| onFailed | Failure callback |


### adminStartSubMeeting:onSuccess:onFailed:()
`- (void)adminStartSubMeeting:(NSArray <NSString *> *)targetList onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

Starts sub-meetings. The host or a co-host can use this API to start sub-meetings that have been created (host or co-host only), and the SDK notifies the target users through the [meetingRoom:onRoomSubMeetingStart:title:conferee:()](/en/meeting/ios/api-reference/MeetingKitRoomDelegate) callback in `MeetingKitRoomDelegate`.

| Parameter | Description |
| :--- | --- |
| targetList | List of sub-meeting IDs |
| onSuccess | Success callback |
| onFailed | Failure callback |


### adminStopSubMeeting:onSuccess:onFailed:()
`- (void)adminStopSubMeeting:(NSArray <NSString *> *)targetList onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

Ends sub-meetings. The host or a co-host can use this API to end sub-meetings that have been created (host or co-host only), and the SDK notifies the target users through the [meetingRoom:onRoomSubMeetingStop:()](/en/meeting/ios/api-reference/MeetingKitRoomDelegate) callback in `MeetingKitRoomDelegate`.

| Parameter | Description |
| :--- | --- |
| targetList | List of sub-meeting IDs |
| onSuccess | Success callback |
| onFailed | Failure callback |


### adminMoveSubMeetingUser:fromGroupId:toGroupId:onSuccess:onFailed:()
`- (void)adminMoveSubMeetingUser:(NSString *)targetId fromGroupId:(NSString *)fromGroupId toGroupId:(nullable NSString *)toGroupId onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

Moves a user between sub-meetings. The host or a co-host can use this API to move a specified member between sub-meetings and the main meeting (host or co-host only), and the SDK notifies the target user through the [meetingRoom:onRoomMoveSubMeeting:fromMeetingTitle:toMeetingId:toMeetingTitle:()](/en/meeting/ios/api-reference/MeetingKitRoomDelegate) callback in `MeetingKitRoomDelegate`.

| Parameter | Description |
| :--- | --- |
| targetId | Target member ID |
| fromGroupId | Source sub-meeting ID |
| toGroupId | Target sub-meeting ID; empty means the main meeting |
| onSuccess | Success callback |
| onFailed | Failure callback |


### getOnlineMemberList:onSuccess:onFailed:()
`- (void)getOnlineMemberList:(NSString *)meetingId onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

Gets the online member list.

| Parameter | Description |
| :--- | --- |
| meetingId | Meeting ID |
| onSuccess | Success callback; see [SEAOnlineMemberListModel](/en/meeting/ios/types#seaonlinememberlistmodel) |
| onFailed | Failure callback |


### getMoreOnlineMemberList:onSuccess:onFailed:()
`- (void)getMoreOnlineMemberList:(NSString *)meetingId onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

Gets more of the online member list (next page).

| Parameter | Description |
| :--- | --- |
| meetingId | Meeting ID |
| onSuccess | Success callback; see [SEAOnlineMemberListModel](/en/meeting/ios/types#seaonlinememberlistmodel) |
| onFailed | Failure callback |

## Sign-in APIs
### signInCreate:desc:onSuccess:onFailed:()
`- (void)signInCreate:(NSInteger)dur desc:(nullable NSString *)desc onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

Creates a sign-in activity. The host or a co-host can use this API to create a sign-in activity (host or co-host only), and the SDK notifies all in-meeting members through the  [meetingRoom:onSignInActivity:epoch:beginAt:dur:endAt:desc:()](/en/meeting/ios/api-reference/MeetingKitRoomDelegate#meetingroomonsigninactivityepochbeginatdurendatdesc) callback in `MeetingKitRoomDelegate`.

| Parameter | Description |
| :--- | --- |
| dur | Sign-in duration in minutes; 0 means no time limit |
| desc | Sign-in description |
| onSuccess | Success callback |
| onFailed | Failure callback |


### signInList:onFailed:()
`- (void)signInList:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

Gets the list of sign-in activities. The host or a co-host can use this API to get the list of sign-in activities (host or co-host only).

| Parameter | Description |
| :--- | --- |
| onSuccess | Success callback; see [SEASignInListModel](/en/meeting/ios/types#seasigninlistmodel) |
| onFailed | Failure callback |


### signInCount:onSuccess:onFailed:()
`- (void)signInCount:(NSInteger)epoch onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

Counts sign-ins. The host or a co-host can use this API to get the current number of people who have signed in (host or co-host only).

| Parameter | Description |
| :--- | --- |
| epoch | Sign-in round, starting from 0 |
| onSuccess | Success callback; see [SEASignInCountModel](/en/meeting/ios/types#seasignincountmodel) |
| onFailed | Failure callback |


### signInFinish:onFailed:()
`- (void)signInFinish:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

Ends a sign-in activity. The host or a co-host can use this API to end a sign-in activity (host or co-host only), and the SDK notifies all in-meeting members through the  [meetingRoom:onSignInFinish:epoch:()](/en/meeting/ios/api-reference/MeetingKitRoomDelegate#meetingroomonsigninfinishepoch) callback in `MeetingKitRoomDelegate`.

| Parameter | Description |
| :--- | --- |
| onSuccess | Success callback |
| onFailed | Failure callback |


### signInDetail:onSuccess:onFailed:()
`- (void)signInDetail:(NSInteger)epoch onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

Gets sign-in activity details. The host or a co-host can use this API to get the sign-in records (host or co-host only).

| Parameter | Description |
| :--- | --- |
| epoch | Sign-in round, starting from 0 |
| onSuccess | Success callback; see [SEASignInDetailListModel](/en/meeting/ios/types#seasignindetaillistmodel) |
| onFailed | Failure callback |


### signInSign:onFailed:()
`- (void)signInSign:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

Signs in. After the host or a co-host starts a sign-in activity, in-meeting members can use this API to sign in.

| Parameter | Description |
| :--- | --- |
| onSuccess | Success callback |
| onFailed | Failure callback |


### signInExportDetail:onSuccess:onFailed:()
`- (void)signInExportDetail:(NSInteger)epoch onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

Exports sign-in data. The host or a co-host can use this API to export sign-in data, and the SDK returns the local path of the list in the callback (host or co-host only).

| Parameter | Description |
| :--- | --- |
| epoch | Sign-in round, starting from 0 |
| onSuccess | Success callback; file path |
| onFailed | Failure callback |

## Data management APIs
### getMySelf()
`- (SEAUserModel *)getMySelf`

Gets the basic information of the locally logged-in user.

Returns:

[SEAUserModel](/en/meeting/ios/types#seausermodel) user data.

### findMemberWithUserId:()
`- (SEAUserModel *)findMemberWithUserId:(NSString *)userId`

Gets the basic information of a specified remote user.

Returns:

[SEAUserModel](/en/meeting/ios/types#seausermodel) user data.

### getRemoteUsers()
`- (NSArray<SEAUserModel *> *)getRemoteUsers`

Gets the member list of the current room.

Returns:

[SEAUserModel](/en/meeting/ios/types#seausermodel) user data.

### getRoomDetails()
`- (SEARoomModel *)getRoomDetails`

Gets the basic information of the current room.

Returns:

[SEARoomModel](/en/meeting/ios/types#searoommodel) room details.

### getDrawingHost()
`- (NSString *)getDrawingHost`

Gets the whiteboard address.

Returns:

The whiteboard is implemented as a web page. This API only works after you've entered the room, and returns the whiteboard address.

## Media configuration APIs
### setStreamMediaConfig:()
`- (void)setStreamMediaConfig:(SEAMediaConfig *)config`

Sets media configuration parameters.

Use this API to set parameters such as video encoding, audio encoding, video frame rate, and video bitrate.

**Parameters**

| config | Media streaming configuration parameters, used to specify basic information such as video encoding, audio encoding, video frame rate, and video bitrate. For details, see [SEAMediaConfig](/en/meeting/ios/types#seamediaconfig) |
| --- | --- |


### setNetworkQosParam:()
`- (void)setNetworkQosParam:(SEANetworkQosParam *)param`

Sets network quality control parameters.

Use this API to set parameters such as the latency adaptation level, the anti-jitter level, the bitrate adaptation switch, and the network adaptation switch.

**Parameters**

| param | Quality control parameters, used to specify basic information such as the latency adaptation level, the anti-jitter level, the bitrate adaptation switch, and the network adaptation switch. For details, see [SEANetworkQosParam](/en/meeting/ios/types#seanetworkqosparam) |
| --- | --- |

## Debugging APIs
### setDebugParam:()
`- (void)setDebugParam:(SEADebugParam *)param`

Sets debugging parameters.

Use this API to set parameters such as the debug address and saving audio and video streams.

**Parameters**

| param | Debugging parameters, used to set basic information such as the debug address and saving audio and video streams. For details, see [SEADebugParam](/en/meeting/ios/types#seadebugparam) |
| --- | --- |
