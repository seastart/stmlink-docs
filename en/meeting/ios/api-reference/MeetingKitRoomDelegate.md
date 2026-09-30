---
title: "MeetingKitRoomDelegate"
description: "Room event callback protocol of the iOS SMeeting SDK: entering and exiting, room settings and host actions, member state, chat messages, cloud recording, screen sharing, stream quality, and sign-in. Every callback carries the source room instance. Read this when handling in-room events."
---

This protocol carries all in-room events. **The first parameter of every callback is the [MeetingKitRoom](/en/meeting/ios/api-reference/MeetingKitRoom) instance the event comes from.** With multiple rooms, use the first parameter to tell which room an event belongs to; read the room number and meeting ID from `room.roomNo` and `room.meetingId`.

For account-level and device-level events (audio route changes, app performance), implement [MeetingKitDelegate](/en/meeting/ios/api-reference/MeetingKitDelegate).

```objectivec
@interface YourClass : NSObject <MeetingKitRoomDelegate>
```

<Note>
The same `userId` may appear in multiple rooms at once. When querying member data in a callback, use the room instance passed as the first parameter (such as `[room findMemberWithUserId:userId]`); don't reuse indexes across rooms.
</Note>

## Error callbacks
### meetingRoom:onError:errMsg:()
`- (void)meetingRoom:(MeetingKitRoom *)room onError:(SEAError)errCode errMsg:(nullable NSString *)errMsg`

Called when an error occurs.

Indicates that the SDK has hit an unrecoverable error, such as a failure to enter the room or to turn on a device. When this fires, you usually need to get a new token and enter the meeting again.

See: [Error codes](/en/meeting/ios/error-codes)

| Parameter | Description |
| --- | --- |
| room | Room instance the event comes from |
| errCode | Error code |
| errMsg | Error message |

## Connection callbacks
### meetingRoomOnReconnecting:()
`- (void)meetingRoomOnReconnecting:(MeetingKitRoom *)room`

Called when reconnection starts.

Indicates that the SDK connection has run into a problem, such as network jitter, and the SDK is trying to reconnect. If an error occurs along the way, the SDK fires the `meetingRoom:onError:errMsg:()` callback.

### meetingRoomOnReconnected:()
`- (void)meetingRoomOnReconnected:(MeetingKitRoom *)room`

Called when reconnection succeeds.

You receive this notification when the SDK has reconnected after a disconnect and the connection is restored. If an error occurs along the way, the SDK fires the `meetingRoom:onError:errMsg:()` callback.

## Local user callbacks
### meetingRoom:onEnterRoom:userId:()
`- (void)meetingRoom:(MeetingKitRoom *)room onEnterRoom:(NSString *)meetingId userId:(NSString *)userId`

Called when you enter the room.

After you call `enterRoom:onSuccess:onFailed:()` on `MeetingKitRoom` to enter the room, you receive the `meetingRoom:onEnterRoom:userId:()` callback from `MeetingKitRoomDelegate`. If an error occurs, the SDK returns it through the method's `onFailed` parameter.

| Parameter | Description |
| --- | --- |
| room | Room instance the event comes from |
| meetingId | Meeting ID |
| userId | User ID |


### meetingRoom:onExitRoom:()
`- (void)meetingRoom:(MeetingKitRoom *)room onExitRoom:(SEALeaveReason)reason`

Called when you exit the room.

You receive this notification when the current user exits without having requested it, for example when removed from the room by the host or when the meeting is ended.

> Note that calling `exitRoom: ` on `MeetingKitRoom` runs the exit logic, such as releasing audio and video device resources and codec resources. Once all resources held by the SDK are released, the SDK reports it through the method's `onSuccess` parameter, where you can perform actions such as leaving the screen. In this case, you no longer receive the `meetingRoom:onExitRoom:()` notification.
>

| Parameter | Description |
| :--- | --- |
| room | Room instance the event comes from |
| reason | Exit reason. See [SEALeaveReason](/en/meeting/ios/types#sealeavereason) |


### meetingRoom:onUserUpdate:()
`- (void)meetingRoom:(MeetingKitRoom *)room onUserUpdate:(NSString *)userId`

Called when your own data is updated.

Supported since `2.0.0`. After the server changes the current user's data in this room, the SDK notifies your app through this callback.

| Parameter | Description |
| :--- | --- |
| room | Room instance the event comes from |
| userId | User ID |

### meetingRoom:onRequestOpenCamera:()
`- (void)meetingRoom:(MeetingKitRoom *)room onRequestOpenCamera:(NSString *)userId`

Called when you're asked to turn on the camera.

After the host calls `adminRequestUserOpenCamera:onSuccess:onFailed:()` on `MeetingKitRoom` to ask you to turn on your camera, the SDK fires this event to notify you.

| Parameter | Description |
| :--- | --- |
| room | Room instance the event comes from |
| userId | Requester ID |


### meetingRoom:onRequestOpenMic:()
`- (void)meetingRoom:(MeetingKitRoom *)room onRequestOpenMic:(NSString *)userId`

Called when you're asked to turn on the microphone.

After the host calls `adminRequestUserOpenMic:onSuccess:onFailed:()` on `MeetingKitRoom` to ask you to turn on your microphone, the SDK fires this event to notify you.

| Parameter | Description |
| :--- | --- |
| room | Room instance the event comes from |
| userId | Requester ID |


### meetingRoom:onRequestOpenShare:()
`- (void)meetingRoom:(MeetingKitRoom *)room onRequestOpenShare:(NSString *)userId`

Called when you're asked to start sharing.

After the host calls `adminRequestUserOpenShare:onSuccess:onFailed:()` on `MeetingKitRoom` to ask you to start sharing, the SDK fires this event to notify you.

| Parameter | Description |
| :--- | --- |
| room | Room instance the event comes from |
| userId | Requester ID |


### meetingRoom:onRoomMoveInWaitingRoom:()
`- (void)meetingRoom:(MeetingKitRoom *)room onRoomMoveInWaitingRoom:(NSString *)userId`

Called when the host or a co-host moves you into the waiting room.

After the host calls `adminMoveInWaitingRoom:nickname:onSuccess:onFailed:()` on `MeetingKitRoom` to move a member of the meeting into the waiting room, the SDK fires this event to notify you.

| Parameter | Description |
| :--- | --- |
| room | Room instance the event comes from |
| userId | Operator ID |


### meetingRoom:onRoomMoveSubMeeting:fromMeetingTitle:toMeetingId:toMeetingTitle:()
`- (void)meetingRoom:(MeetingKitRoom *)room onRoomMoveSubMeeting:(NSString *)fromMeetingId fromMeetingTitle:(NSString *)fromMeetingTitle toMeetingId:(NSString *)toMeetingId toMeetingTitle:(NSString *)toMeetingTitle`

Called when the host or a co-host moves you into a sub-meeting or the main meeting.

After the host calls `adminMoveSubMeetingUser:fromGroupId:toGroupId:onSuccess:onFailed:()` on `MeetingKitRoom` to move you into a sub-meeting or the main meeting, the SDK fires this event to notify you.

| Parameter | Description |
| :--- | --- |
| room | Room instance the event comes from |
| fromMeetingId | ID of the original sub-meeting |
| fromMeetingTitle | Title of the original sub-meeting |
| toMeetingId | ID of the target sub-meeting |
| toMeetingTitle | Title of the target sub-meeting |

## Room callbacks
### meetingRoom:onRoomCameraStateChanged:selfUnmuteCameraDisabled:userId:()
`- (void)meetingRoom:(MeetingKitRoom *)room onRoomCameraStateChanged:(BOOL)cameraDisabled selfUnmuteCameraDisabled:(BOOL)selfUnmuteCameraDisabled userId:(NSString *)userId`

Called when the room's camera-disabled state changes.

After the host calls `adminUpdateRoomCameraState:selfUnmuteCameraDisabled:onSuccess:onFailed:()` on `MeetingKitRoom` to update camera off for everyone, the SDK fires this event to notify you.

| Parameter | Description |
| --- | --- |
| room | Room instance the event comes from |
| cameraDisabled | Room camera disabled state. YES: disabled; NO: enabled |
| selfUnmuteCameraDisabled | Whether members are prevented from turning their cameras back on themselves. YES: prevented; NO: allowed |
| userId | Operator ID |


### meetingRoom:onRoomMicStateChanged:selfUnmuteMicDisabled:userId:()
`- (void)meetingRoom:(MeetingKitRoom *)room onRoomMicStateChanged:(BOOL)micDisabled selfUnmuteMicDisabled:(BOOL)selfUnmuteMicDisabled userId:(NSString *)userId`

Called when the room's microphone-disabled state changes.

After the host calls `adminUpdateRoomMicState:selfUnmuteMicDisabled:onSuccess:onFailed:()` on `MeetingKitRoom` to update mute all, the SDK fires this event to notify you.

| Parameter | Description |
| --- | --- |
| room | Room instance the event comes from |
| micDisabled | Room microphone disabled state. YES: disabled; NO: enabled |
| selfUnmuteMicDisabled | Whether members are prevented from unmuting themselves. YES: prevented; NO: allowed |
| userId | Operator ID |


### meetingRoom:onRoomChatDisabledChanged:userId:()
`- (void)meetingRoom:(MeetingKitRoom *)room onRoomChatDisabledChanged:(BOOL)chatDisabled userId:(NSString *)userId`

Called when the room's chat-disabled state changes.

After the host calls `adminUpdateRoomChatDisabled:onSuccess:onFailed:()` on `MeetingKitRoom` to update the room's chat-disabled state, the SDK fires this event to notify you.

| Parameter | Description |
| --- | --- |
| room | Room instance the event comes from |
| chatDisabled | Disabled state. YES: disabled; NO: enabled |
| userId | Operator ID |


### meetingRoom:onRoomShareDisabledChanged:userId:()
`- (void)meetingRoom:(MeetingKitRoom *)room onRoomShareDisabledChanged:(BOOL)shareDisabled userId:(NSString *)userId`

Called when the room's sharing-disabled state changes.

After the host calls `adminUpdateRoomShareDisabled:onSuccess:onFailed:()` on `MeetingKitRoom` to update the room's sharing-disabled state, the SDK fires this event to notify you.

| Parameter | Description |
| --- | --- |
| room | Room instance the event comes from |
| shareDisabled | Disabled state. YES: disabled; NO: enabled |
| userId | Operator ID |


### meetingRoom:onRoomScreenshotDisabledChanged:userId:()
`- (void)meetingRoom:(MeetingKitRoom *)room onRoomScreenshotDisabledChanged:(BOOL)screenshotDisabled userId:(NSString *)userId`

Called when the room's screenshot-disabled state changes.

After the host calls `adminUpdateRoomScreenshotDisabled:onSuccess:onFailed:()` on `MeetingKitRoom` to update the room's screenshot permission, the SDK fires this event to notify you.

| Parameter | Description |
| --- | --- |
| room | Room instance the event comes from |
| screenshotDisabled | Disabled state. YES: disabled; NO: enabled |
| userId | Operator ID |


### meetingRoom:onRoomWatermarkDisabledChanged:userId:()
`- (void)meetingRoom:(MeetingKitRoom *)room onRoomWatermarkDisabledChanged:(BOOL)watermarkDisabled userId:(NSString *)userId`

Called when the room's watermark-disabled state changes.

After the host calls `adminUpdateRoomWatermarkDisabled:onSuccess:onFailed:()` on `MeetingKitRoom` to update the room's watermark setting, the SDK fires this event to notify you.

| Parameter | Description |
| --- | --- |
| room | Room instance the event comes from |
| watermarkDisabled | Disabled state. YES: disabled; NO: enabled |
| userId | Operator ID |


### meetingRoom:onRoomWaitingRoomDisabledChanged:userId:()
`- (void)meetingRoom:(MeetingKitRoom *)room onRoomWaitingRoomDisabledChanged:(BOOL)waitingRoomDisabled userId:(NSString *)userId`

Called when the room's waiting-room-disabled state changes.

After the host calls `adminUpdateWaitingRoomDisabled:onSuccess:onFailed:()` on `MeetingKitRoom` to update the room's waiting-room-disabled state, the SDK fires this event to notify you.

| Parameter | Description |
| --- | --- |
| room | Room instance the event comes from |
| waitingRoomDisabled | Disabled state. YES: disabled; NO: enabled |
| userId | Operator ID |


### meetingRoom:onRoomLockedChanged:userId:()
`- (void)meetingRoom:(MeetingKitRoom *)room onRoomLockedChanged:(BOOL)locked userId:(NSString *)userId`

Called when the room's locked state changes.

After the host calls `adminUpdateRoomLocked:onSuccess:onFailed:()` on `MeetingKitRoom` to update the room's locked state, the SDK fires this event to notify you.

| Parameter | Description |
| --- | --- |
| room | Room instance the event comes from |
| locked | Locked state. YES: locked; NO: unlocked |
| userId | Operator ID |


### meetingRoom:onRoomMoveHost:sourceUserId:()
`- (void)meetingRoom:(MeetingKitRoom *)room onRoomMoveHost:(NSString *)userId sourceUserId:(NSString *)sourceUserId`

Called when the host role is transferred.

After the host calls `adminMoveHost:onSuccess:onFailed:()` on `MeetingKitRoom` to transfer the host role, the SDK fires this event to notify you.

| Parameter | Description |
| --- | --- |
| room | Room instance the event comes from |
| userId | User ID of the new host |
| sourceUserId | User ID of the previous host |


### meetingRoom:onRoomShareStart:shareType:()
`- (void)meetingRoom:(MeetingKitRoom *)room onRoomShareStart:(NSString *)userId shareType:(SEAShareType)shareType`

Called when sharing starts.

After a member calls `requestShare:onSuccess:onFailed:()` on `MeetingKitRoom` to start sharing, the SDK fires this event to notify you.

> Note: If a member is already sharing in the room, members who enter later also receive this notification.
>

| Parameter | Description |
| --- | --- |
| room | Room instance the event comes from |
| userId | ID of the sharing member |
| shareType | Sharing type. See [SEAShareType](/en/meeting/ios/types#seasharetype) |


### meetingRoom:onRoomShareStop:shareType:()
`- (void)meetingRoom:(MeetingKitRoom *)room onRoomShareStop:(NSString *)userId shareType:(SEAShareType)shareType`

Called when sharing stops.

After a member calls `stopShare:onFailed:()` on `MeetingKitRoom` to stop sharing, the SDK fires this event to notify you.

> Note: If the sharing member exits the room without stopping sharing first, other members receive the `meetingRoom:onRoomShareStop:shareType:()` event first and then the `meetingRoom:onUserExit:()` event.
>

| Parameter | Description |
| --- | --- |
| room | Room instance the event comes from |
| userId | ID of the sharing member |
| shareType | Sharing type. See [SEAShareType](/en/meeting/ios/types#seasharetype) |


### meetingRoom:onAdminRoomShareStop:shareType:()
`- (void)meetingRoom:(MeetingKitRoom *)room onAdminRoomShareStop:(NSString *)userId shareType:(SEAShareType)shareType`

Called when the host stops a member's sharing.

After the host calls `adminStopRoomShare:onFailed:()` on `MeetingKitRoom` to stop a member's sharing, the SDK fires this event to notify you.

| Parameter | Description |
| --- | --- |
| room | Room instance the event comes from |
| userId | ID of the sharing member |
| shareType | Sharing type. See [SEAShareType](/en/meeting/ios/types#seasharetype) |


### meetingRoom:onRoomHandUpChanged:enable:handupType:()
`- (void)meetingRoom:(MeetingKitRoom *)room onRoomHandUpChanged:(NSString *)userId enable:(BOOL)enable handupType:(SEAHandupType)handupType`

Called when a member's raise-hand state changes.

After a member calls `requestHandup:onSuccess:onFailed:()` on `MeetingKitRoom` to raise a hand, the SDK fires this event to notify you if you are a host or co-host of the room.

| Parameter | Description |
| --- | --- |
| room | Room instance the event comes from |
| userId | Member ID |
| enable | Raise-hand state. YES: hand raised; NO: hand lowered |
| handupType | Raise-hand request type. See [SEAHandupType](/en/meeting/ios/types#seahanduptype) |


### meetingRoom:onRoomSubMeetingStart:title:conferee:()
`- (void)meetingRoom:(MeetingKitRoom *)room onRoomSubMeetingStart:(NSString *)meetingId title:(NSString *)title conferee:(nullable NSArray <NSString *> *)conferee`

Called when a sub-meeting starts.

After the host or a co-host calls `adminStartSubMeeting:onSuccess:onFailed:()` on `MeetingKitRoom` to start sub-meetings, the SDK fires this event to notify you.

| Parameter | Description |
| --- | --- |
| room | Room instance the event comes from |
| meetingId | Meeting ID |
| title | Sub-meeting name |
| conferee | List of member IDs in the sub-meeting |


### meetingRoom:onRoomSubMeetingStop:()
`- (void)meetingRoom:(MeetingKitRoom *)room onRoomSubMeetingStop:(NSString *)parentMid`

Called when sub-meetings end.

After the host or a co-host calls `adminStopSubMeeting:onSuccess:onFailed:()` on `MeetingKitRoom` to end sub-meetings, the SDK fires this event to notify you.

| Parameter | Description |
| :--- | --- |
| room | Room instance the event comes from |
| parentMid | Parent meeting ID |


### meetingRoom:onRoomMeetingTitleChanged:()
`- (void)meetingRoom:(MeetingKitRoom *)room onRoomMeetingTitleChanged:(NSString *)title`

Called when the room's meeting title changes.

After the host or a co-host calls `adminUpdateSubMeetingTitle:targetId:onSuccess:onFailed:()` on `MeetingKitRoom` to change a sub-meeting's title, the SDK fires this event to notify you.

| Parameter | Description |
| :--- | --- |
| room | Room instance the event comes from |
| title | Meeting title |

## User callbacks
### meetingRoom:onUserEnter:()
`- (void)meetingRoom:(MeetingKitRoom *)room onUserEnter:(NSString *)userId`

Called when a member enters the room, including the current user.

After a remote user calls `enterRoom:onSuccess:onFailed:()` on `MeetingKitRoom` to enter the room, the SDK fires this event to notify you.

| Parameter | Description |
| :--- | --- |
| room | Room instance the event comes from |
| userId | Member ID |


### meetingRoom:onUserExit:()
`- (void)meetingRoom:(MeetingKitRoom *)room onUserExit:(NSString *)userId`

Called when a member exits the room, including the current user.

After a remote user calls `exitRoom:()` on `MeetingKitRoom` to exit the room, the SDK fires this event to notify you.

| Parameter | Description |
| :--- | --- |
| room | Room instance the event comes from |
| userId | Member ID |


### meetingRoom:onUserNameChanged:nickname:()
`- (void)meetingRoom:(MeetingKitRoom *)room onUserNameChanged:(NSString *)targetUserId nickname:(NSString *)nickname`

Called when a user's nickname changes.

After a member calls `updateName:onSuccess:onFailed:()` on `MeetingKitRoom`, or the host calls `adminUpdateNickname:nickname:onSuccess:onFailed:()`, to update a user's nickname, the SDK fires this event to notify you.

| Parameter | Description |
| :--- | --- |
| room | Room instance the event comes from |
| targetUserId | Target member ID |
| nickname | User nickname |


### meetingRoom:onUserRoleChanged:userRole:()
`- (void)meetingRoom:(MeetingKitRoom *)room onUserRoleChanged:(NSString *)targetUserId userRole:(SEAUserRole)userRole`

Called when a user's role changes.

After a host or co-host of the room calls `adminUpdateUserRole:userRole:onSuccess:onFailed:()` on `MeetingKitRoom` to update a user's role, the SDK fires this event to notify you.

| Parameter | Description |
| :--- | --- |
| room | Room instance the event comes from |
| targetUserId | Target member ID |
| userRole | User role. See [SEAUserRole](/en/meeting/ios/types#seauserrole) |


### meetingRoom:onUserCameraStateChanged:cameraState:reason:()
`- (void)meetingRoom:(MeetingKitRoom *)room onUserCameraStateChanged:(NSString *)targetUserId cameraState:(SEADeviceState)cameraState reason:(SEAChangeReason)reason`

Called when a user's camera state changes.

The SDK fires this event to notify you after a member of the room turns the camera on or off through `requestOpenCamera:view:onSuccess:onFailed:()` or `closeCamera:onFailed:()` on `MeetingKitRoom`, and after a host or co-host of the room turns off a remote user's camera through `adminCloseUserCamera:onSuccess:onFailed:()` on `MeetingKitRoom`.

> Note: If a member already had the camera on before you entered the room, this event also fires when you enter the room.
>

| Parameter | Description |
| :--- | --- |
| room | Room instance the event comes from |
| targetUserId | Target member ID |
| cameraState | Camera state. See [SEADeviceState](/en/meeting/ios/types#seadevicestate) |
| reason | Reason for the change. See [SEAChangeReason](/en/meeting/ios/types#seachangereason) |


### meetingRoom:onUserMicStateChanged:micState:reason:()
`- (void)meetingRoom:(MeetingKitRoom *)room onUserMicStateChanged:(NSString *)targetUserId micState:(SEADeviceState)micState reason:(SEAChangeReason)reason`

Called when a user's microphone state changes.

The SDK fires this event to notify you after a member of the room turns the microphone on or off through `requestOpenMic:onFailed:()` or `closeMic:onFailed:()` on `MeetingKitRoom`, and after a host or co-host of the room turns off a remote user's microphone through `adminCloseUserMic:onSuccess:onFailed:()` on `MeetingKitRoom`.

> Note: If a member already had the microphone on before you entered the room, this event also fires when you enter the room.
>

| Parameter | Description |
| :--- | --- |
| room | Room instance the event comes from |
| targetUserId | Target member ID |
| micState | Microphone state. See [SEADeviceState](/en/meeting/ios/types#seadevicestate) |
| reason | Reason for the change. See [SEAChangeReason](/en/meeting/ios/types#seachangereason) |


### meetingRoom:onUserChatDisabledChanged:userId:()
`- (void)meetingRoom:(MeetingKitRoom *)room onUserChatDisabledChanged:(BOOL)chatDisabled userId:(NSString *)userId`

Called when a user's chat-disabled state changes.

After a host or co-host of the room calls `adminUpdateUserChatDisabled:chatDisabled:onSuccess:onFailed:()` on `MeetingKitRoom` to update a user's chat state, the SDK fires this event to notify you.

| Parameter | Description |
| :--- | --- |
| room | Room instance the event comes from |
| chatDisabled | Disabled state. YES: disabled; NO: enabled |
| userId | Operator ID |


### meetingRoom:onUserDrawDisabledChanged:userId:()
`- (void)meetingRoom:(MeetingKitRoom *)room onUserDrawDisabledChanged:(BOOL)drawDisabled userId:(NSString *)userId`

Called when a user's drawing-disabled state changes.

After a host or co-host of the room calls `adminUpdateUserDrawDisabled:drawDisabled:onSuccess:onFailed:()` on `MeetingKitRoom` to update a user's drawing permission, the SDK fires this event to notify you.

| Parameter | Description |
| :--- | --- |
| room | Room instance the event comes from |
| drawDisabled | Disabled state. YES: disabled; NO: enabled |
| userId | Operator ID |


### meetingRoom:onHandupConfirm:approve:userId:()
`- (void)meetingRoom:(MeetingKitRoom *)room onHandupConfirm:(SEAHandupType)handupType approve:(BOOL)approve userId:(NSString *)userId`

Called with the result of handling a raised hand.

After a member of the room calls `requestHandup:onSuccess:onFailed:()` on `MeetingKitRoom` to raise a hand, the host and co-hosts in the room receive the `meetingRoom:onRoomHandUpChanged:enable:handupType:()` event from the SDK. After the host or a co-host handles the raised hand through `adminConfirmHandup:handupType:approve:onSuccess:onFailed:()`, the SDK fires this event to notify you.

| Parameter | Description |
| :--- | --- |
| room | Room instance the event comes from |
| handupType | Request type. See [SEAHandupType](/en/meeting/ios/types#seahanduptype) |
| approve | Result. YES: approved; NO: declined |
| userId | ID of the person who handled it |


### meetingRoom:onRoomUserEnterWaitingRoom:nickname:()
`- (void)meetingRoom:(MeetingKitRoom *)room onRoomUserEnterWaitingRoom:(NSString *)userId nickname:(NSString *)nickname`

Called when a remote user enters the waiting room.

When a user calls `enterRoom:()` on `MeetingKitRoom` to enter the room and the room has the waiting room enabled, the system places the member in the room's waiting room by default. The host and co-hosts in the room then receive this notification from the SDK.

| Parameter | Description |
| :--- | --- |
| room | Room instance the event comes from |
| userId | Member ID |
| nickname | Member nickname |


### meetingRoom:onRoomUserExitWaitingRoom:nickname:()
`- (void)meetingRoom:(MeetingKitRoom *)room onRoomUserExitWaitingRoom:(NSString *)userId nickname:(NSString *)nickname`

Called when a remote user exits the waiting room.

When a user calls `exitWaitingRoom:onSuccess:()` on `MeetingKitRoom` to exit the waiting room, the host and co-hosts in the room receive this notification from the SDK.

| Parameter | Description |
| :--- | --- |
| room | Room instance the event comes from |
| userId | Member ID |
| nickname | Member nickname |

## Message callbacks
### meetingRoom:onReceiveChatMessage:message:messageType:()
`- (void)meetingRoom:(MeetingKitRoom *)room onReceiveChatMessage:(NSString *)senderId message:(NSString *)message messageType:(SEAMessageType)messageType`

Called when a chat message is received.

After `sendRoomChatMessage:messageType:targetId:onSuccess:onFailed:()` or `sendRoomCustomMessage:targetId:onSuccess:onFailed:()` on `MeetingKitRoom` is called to send a message, the SDK fires this event to notify you.

| Parameter | Description |
| --- | --- |
| room | Room instance the event comes from |
| senderId | Sender ID |
| message | Message content |
| messageType | Message type. See [SEAMessageType](/en/meeting/ios/types#seamessagetype) |


### meetingRoom:onReceiveSystemMessage:messageType:()
`- (void)meetingRoom:(MeetingKitRoom *)room onReceiveSystemMessage:(NSString *)message messageType:(SEAMessageType)messageType`

Called when a system message is received.

Indicates that a message sent by the system has been received.

| Parameter | Description |
| --- | --- |
| room | Room instance the event comes from |
| message | Message content |
| messageType | Message type. See [SEAMessageType](/en/meeting/ios/types#seamessagetype) |


### meetingRoom:onReceiveCustomMessage:action:userId:sessionId:nickname:()
`- (void)meetingRoom:(MeetingKitRoom *)room onReceiveCustomMessage:(NSString *)content action:(NSString *)action userId:(nullable NSString *)userId sessionId:(nullable NSString *)sessionId nickname:(nullable NSString *)nickname`

Called when a custom message is received.

Supported since `2.0.0`. The SDK passes room custom messages that your app sends through the server to the corresponding room through this callback.

| Parameter | Description |
| :--- | --- |
| room | Room instance the event comes from |
| content | Message content |
| action | Message identifier |
| userId | User ID |
| sessionId | Session ID |
| nickname | User nickname |

## Cloud recording callbacks
### meetingRoom:onCloudRecordStatusChange:status:errMsg:()
`- (void)meetingRoom:(MeetingKitRoom *)room onCloudRecordStatusChange:(SEARecordType)recordType status:(SEARecordStatus)status errMsg:(nullable NSString *)errMsg`

Called when the cloud recording status changes.

After `startCloudRecord:onSuccess:onFailed:()` or `stopCloudRecord:onFailed:()` on `MeetingKitRoom` is called to start or stop cloud recording, the SDK fires this event to notify you.

| Parameter | Description |
| --- | --- |
| room | Room instance the event comes from |
| recordType | Recording type. See [SEARecordType](/en/meeting/ios/types#searecordtype) |
| status | Recording status. See [SEARecordStatus](/en/meeting/ios/types#searecordstatus) |
| errMsg | Error description |


### meetingRoom:onCloudRecordAlarm:taskId:gateway:alarmAt:alarmBrief:()
`- (void)meetingRoom:(MeetingKitRoom *)room onCloudRecordAlarm:(SEARecordStatus)status taskId:(NSString *)taskId gateway:(NSString *)gateway alarmAt:(NSInteger)alarmAt alarmBrief:(nullable NSString *)alarmBrief`

Called when a cloud recording alarm is raised.

When the meeting service detects a problem with cloud recording, the SDK fires this event to notify you.

| Parameter | Description |
| --- | --- |
| room | Room instance the event comes from |
| status | Recording status. See [SEARecordStatus](/en/meeting/ios/types#searecordstatus) |
| taskId | Task ID |
| gateway | Gateway the task runs on |
| alarmAt | Alarm time |
| alarmBrief | Alarm summary |

## Screen capture callbacks
### meetingRoom:onScreenRecordStatus:()
`- (void)meetingRoom:(MeetingKitRoom *)room onScreenRecordStatus:(SEAScreenRecordStatus)status`

Called with the screen sharing status.

After the screen recording extension calls `broadcastStartedWithAppGroup:delegate:()` on `MeetingKit` to start screen recording, the SDK reports the current screen capture status through the `meetingRoom:onScreenRecordStatus:()` callback.

| Parameter | Description |
| --- | --- |
| room | Room instance the event comes from |
| status | Status code. See [SEAScreenRecordStatus](/en/meeting/ios/types#seascreenrecordstatus) |

## Audio callbacks
### meetingRoom:onRemoteMemberAudioStatus:()
`- (void)meetingRoom:(MeetingKitRoom *)room onRemoteMemberAudioStatus:(NSArray<SEAStreamAudioModel *> *)audioArray`

Called with remote members' audio status data.

Reports the audio status data of the room's members, including audio decibel and power values. Your app can use this data for purposes such as voice-activated switching.

| Parameter | Description |
| --- | --- |
| room | Room instance the event comes from |
| audioArray | List of member audio data. See [SEAStreamAudioModel](/en/meeting/ios/types#seastreamaudiomodel) |

## Media streaming callbacks
### meetingRoom:onDownBitrateAdaptiveUserId:state:()
`- (void)meetingRoom:(MeetingKitRoom *)room onDownBitrateAdaptiveUserId:(NSString *)userId state:(SEADownBitrateAdaptiveState)state`

Called with the downlink adaptive bitrate state.

With adaptive bitrate enabled, the SDK dynamically adjusts the adaptive bitrate level of each member's downlink based on network conditions.

| Parameter | Description |
| --- | --- |
| room | Room instance the event comes from |
| userId | User ID |
| state | Downlink adaptive bitrate state. See [SEADownBitrateAdaptiveState](/en/meeting/ios/types#seadownbitrateadaptivestate) |


### meetingRoom:onUploadBitrateAdaptiveState:()
`- (void)meetingRoom:(MeetingKitRoom *)room onUploadBitrateAdaptiveState:(SEAUploadBitrateAdaptiveState)state`

Called with the uplink adaptive bitrate state.

With adaptive bitrate enabled, the SDK dynamically adjusts the adaptive bitrate level of the uplink based on network conditions.

| Parameter | Description |
| --- | --- |
| room | Room instance the event comes from |
| state | Uplink adaptive bitrate state. See [SEAUploadBitrateAdaptiveState](/en/meeting/ios/types#seauploadbitrateadaptivestate) |


### meetingRoom:onDownLossLevelChangeState:()
`- (void)meetingRoom:(MeetingKitRoom *)room onDownLossLevelChangeState:(SEADownLossLevelState)state`

Called when the downlink average packet loss level changes.

| Parameter | Description |
| --- | --- |
| room | Room instance the event comes from |
| state | Downlink average packet loss level. See [SEADownLossLevelState](/en/meeting/ios/types#seadownlosslevelstate) |


### meetingRoom:onDownLossRateAverage:()
`- (void)meetingRoom:(MeetingKitRoom *)room onDownLossRateAverage:(CGFloat)average`

Called with the downlink average packet loss rate.

| Parameter | Description |
| --- | --- |
| room | Room instance the event comes from |
| average | Downlink average packet loss rate |


### meetingRoom:onSendStreamModel:()
`- (void)meetingRoom:(MeetingKitRoom *)room onSendStreamModel:(SEAStreamSendModel *)sendModel`

Called with media stream send status data.

At a fixed interval, you receive the `meetingRoom:onSendStreamModel:()` callback from `MeetingKitRoomDelegate`, describing the current send status such as latency and packet loss rate.

| Parameter | Description |
| --- | --- |
| room | Room instance the event comes from |
| sendModel | Media stream send status data. See [SEAStreamSendModel](/en/meeting/ios/types#seastreamsendmodel) |


### meetingRoom:onReceiveStreamModel:()
`- (void)meetingRoom:(MeetingKitRoom *)room onReceiveStreamModel:(NSArray <SEAStreamReceiveModel *> *)receiveArray`

Called with media stream receive status data.

At a fixed interval, you receive the `meetingRoom:onReceiveStreamModel:()` callback from `MeetingKitRoomDelegate`, describing the current receive status such as latency and packet loss rate.

| Parameter | Description |
| --- | --- |
| room | Room instance the event comes from |
| receiveModel | Media stream receive status data. See [SEAStreamReceiveModel](/en/meeting/ios/types#seastreamreceivemodel) |


### meetingRoom:onSendQualityModel:()
`- (void)meetingRoom:(MeetingKitRoom *)room onSendQualityModel:(SEAStreamQualityModel *)qualityModel`

Called with media stream uplink quality data.

At a fixed interval, you receive the `meetingRoom:onSendQualityModel:()` callback from `MeetingKitRoomDelegate`, describing the current send status such as latency and packet loss rate.

| Parameter | Description |
| --- | --- |
| room | Room instance the event comes from |
| qualityModel | Media stream quality data. See [SEAStreamQualityModel](/en/meeting/ios/types#seastreamqualitymodel) |


### meetingRoom:onReceiveQualityModel:()
`- (void)meetingRoom:(MeetingKitRoom *)room onReceiveQualityModel:(SEAStreamQualityModel *)qualityModel`

Called with media stream downlink quality data.

At a fixed interval, you receive the `meetingRoom:onReceiveQualityModel:()` callback from `MeetingKitRoomDelegate`, describing the current receive status such as latency and packet loss rate.

| Parameter | Description |
| --- | --- |
| room | Room instance the event comes from |
| qualityModel | Media stream quality data. See [SEAStreamQualityModel](/en/meeting/ios/types#seastreamqualitymodel) |


### meetingRoom:onReceiveStreamStatusChange:streamType:status:()
`- (void)meetingRoom:(MeetingKitRoom *)room onReceiveStreamStatusChange:(NSString *)targetUserId streamType:(SEAVideoStreamType)streamType status:(BOOL)status`

Called when the receive status of a video stream changes.

After you subscribe to a member's remote video stream, you receive the `meetingRoom:onReceiveStreamStatusChange:streamType:status:()` callback from `MeetingKitRoomDelegate` if no video from that member arrives for a while. You also receive this callback when the video stream recovers.

| Parameter | Description |
| --- | --- |
| room | Room instance the event comes from |
| targetUserId | Target member ID |
| streamType | Video stream type. See [SEAVideoStreamType](/en/meeting/ios/types#seavideostreamtype) |
| status | Receive status. YES: timed out; NO: recovered |


### meetingRoom:onReceiveMixtureStreamStatusChange:()
`- (void)meetingRoom:(MeetingKitRoom *)room onReceiveMixtureStreamStatusChange:(BOOL)status`

Called when the receive status of the composite stream changes.

After you subscribe to the composite video stream, you receive the `meetingRoom:onReceiveMixtureStreamStatusChange:()` callback from `MeetingKitRoomDelegate` if no composite video arrives for a while. You also receive this callback when the video stream recovers.

| Parameter | Description |
| --- | --- |
| room | Room instance the event comes from |
| status | Receive status. YES: timed out; NO: recovered |


### meetingRoom:onReceiveRetweetStreamStatusChange:status:()
`- (void)meetingRoom:(MeetingKitRoom *)room onReceiveRetweetStreamStatusChange:(NSString *)streamName status:(BOOL)status`

Called when the receive status of a re-streamed stream changes.

After you subscribe to a remote re-streamed stream, you receive the `meetingRoom:onReceiveRetweetStreamStatusChange:status:()` callback from `MeetingKitRoomDelegate` if no re-streamed video arrives for a while. You also receive this callback when the video stream recovers. In this callback, use `streamName` to tell which re-streamed stream it is, and show or hide a loading indicator (such as `UIActivityIndicatorView`).

| Parameter | Description |
| --- | --- |
| room | Room instance the event comes from |
| streamName | Re-streamed stream name |
| status | Receive status. YES: timed out; NO: recovered |

## Other callbacks
### meetingRoom:onExtendedEvents:content:()
`- (void)meetingRoom:(MeetingKitRoom *)room onExtendedEvents:(NSString *)event content:(NSString *)content`

Called when an extended event is received.

Callback for extended events that your app defines in the room.

| Parameter | Description |
| --- | --- |
| room | Room instance the event comes from |
| event | Event type |
| content | Data content |

## Sign-in callbacks
### meetingRoom:onSignInActivity:epoch:beginAt:dur:endAt:desc:()
`- (void)meetingRoom:(MeetingKitRoom *)room onSignInActivity:(NSString *)userId epoch:(NSInteger)epoch beginAt:(NSInteger)beginAt dur:(NSInteger)dur endAt:(NSInteger)endAt desc:(nullable NSString *)desc`

Called when a sign-in activity is created.

After the host calls `signInCreate:desc:onSuccess:onFailed:()` on `MeetingKitRoom` to create a sign-in activity, the SDK fires this event to notify you.

| Parameter | Description |
| --- | --- |
| room | Room instance the event comes from |
| userId | Initiator ID |
| epoch | Sign-in round |
| beginAt | Start time |
| dur | Sign-in duration in minutes; 0 means no time limit |
| endAt | End time |
| desc | Sign-in description |


### meetingRoom:onSignInFinish:epoch:()
`- (void)meetingRoom:(MeetingKitRoom *)room onSignInFinish:(NSString *)userId epoch:(NSInteger)epoch`

Called when a sign-in activity ends.

After the host calls `signInFinish:onFailed:()` on `MeetingKitRoom` to end the sign-in activity, the SDK fires this event to notify you.

| Parameter | Description |
| --- | --- |
| room | Room instance the event comes from |
| userId | Initiator ID |
| epoch | Sign-in round |
