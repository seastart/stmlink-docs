---
title: "MeetingKitIMDelegate"
description: "Callback protocol of the iOS SMeeting SDK's out-of-meeting message path (IM): connection state, incoming calls, meeting reminders, being admitted from the waiting room, and sub-meeting help requests. Read this after calling enableImWithDelegate:."
---

## Connection callbacks
### onImConnectSucceed:sessionId:()
`- (void)onImConnectSucceed:(NSString *)userId sessionId:(NSString *)sessionId`

Called when the connection succeeds.

After you call `enableImWithDelegate:()` to enable IM, you receive this notification once the connection succeeds. If an error occurs, the SDK fires the `onImDisconnected:errCode:errMsg:()` callback.

**Parameters**

| userId | User ID |
| --- | --- |
| sessionId | Session ID |


### onImReconnecting()
`- (void)onImReconnecting`

Called when reconnection starts.

Fires when the connection drops and reconnection starts. If an error occurs, the SDK fires the `onImDisconnected:errCode:errMsg:()` callback.

### onImReconnected()
`- (void)onImReconnected`

Called when reconnection succeeds.

Fires after reconnecting successfully following a disconnect. If an error occurs, the SDK fires the `onImDisconnected:errCode:errMsg:()` callback.

### onImDisconnected:errCode:errMsg:()
`- (void)onImDisconnected:(SEAImDisconnectReason)reason errCode:(SEAError)errCode errMsg:(nullable NSString *)errMsg`

Called when the connection drops or you're passively disconnected.

When the disconnect reason is `SEAImDisconnectReasonError`, the SDK has hit an unrecoverable error, such as an authentication failure. In this case you must get a new token before you can enable IM again. For the error codes, see [Error codes](/en/meeting/ios/error-codes).

When the disconnect reason is anything other than `SEAImDisconnectReasonError`, the connection was dropped passively. For the specific reasons, see [Disconnect reasons](/en/meeting/ios/types#seaimdisconnectreason).

**Parameters**

| reason | Disconnect reason |
| --- | --- |
| errCode | Error code |
| errMsg | Error message |


## Message callbacks
### onImMessage:action:userId:sessionId:nickname:()
`- (void)onImMessage:(NSString *)content action:(NSString *)action userId:(nullable NSString *)userId sessionId:(nullable NSString *)sessionId nickname:(nullable NSString *)nickname`

Called when a message is received.

When your app's business features send a message event through the backend API, the SDK notifies you through this callback.

**Parameters**

| content | Message content |
| --- | --- |
| action | Message identifier |
| userId | User ID |
| sessionId | Session ID |
| nickname | User nickname |


### onMeetingRemind:()
`- (void)onMeetingRemind:(SEAMeetingRemindModel *)remindModel`

Called when a meeting is about to start.

When a scheduled meeting you need to attend is about to start, the SDK notifies you through this callback.

**Parameters**

| remindModel | Meeting reminder content. For details, see [SEAMeetingRemindModel](/en/meeting/ios/types#seameetingremindmodel) |
| --- | --- |


## Call callbacks
### onCallReceived:nickname:roomNo:title:()
`- (void)onCallReceived:(NSString *)callerId nickname:(nullable NSString *)nickname roomNo:(NSString *)roomNo title:(NSString *)title`

Called when a call request arrives.

When the host calls you through the call API, the SDK notifies you through this callback. Listen for this event to decide whether to show the call answering UI.

**Parameters**

| callerId | Caller ID |
| --- | --- |
| nickname | Caller nickname |
| roomNo | Room number |
| title | Meeting title |


## Waiting room callbacks
### onWaitingRoomMoveInRoom:title:()
`- (void)onWaitingRoomMoveInRoom:(NSString *)meetingId title:(nullable NSString *)title`

Called when the host or a co-host admits you from the waiting room into the meeting.

When the host moves people from the waiting room into the meeting, the SDK notifies you through this callback. Listen for this event to decide whether to enter the meeting right away.

**Parameters**

| meetingId | Meeting ID |
| --- | --- |
| title | Meeting title |


## Sub-meeting callbacks
### onSubMettingAskingHelp:meetingId:title:()
`- (void)onSubMettingAskingHelp:(NSString *)parentMid meetingId:(NSString *)meetingId title:(nullable NSString *)title`

Called when a sub-meeting asks for help.

When members of a sub-meeting ask for help, the SDK notifies the host and co-hosts of the main meeting through this callback. Listen for this event to decide whether to handle the help request.

**Parameters**

| parentMid | Parent meeting ID |
| --- | --- |
| meetingId | Sub-meeting ID |
| title | Sub-meeting title |


