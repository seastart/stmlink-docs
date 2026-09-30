---
title: "RTCEngineIMDelegate"
description: "iOS (Objective-C) callback protocol for IM (out-of-channel messaging): connection success, reconnecting, reconnected, disconnect, and incoming IM messages. Read when handling IM connection state or messages on iOS."
---

## Connection callbacks
### onImConnectSucceed:sessionId:()
`- (void)onImConnectSucceed:(NSString *)userId sessionId:(NSString *)sessionId`

Called when the connection succeeds.

After you call `enableImWithToken:()` to enable IM (out-of-channel messaging), you receive this event once the connection succeeds. If an error occurs, the SDK fires the `onImDisconnected:errCode:errMsg:()` callback.

**Parameters**

| userId | User ID |
| --- | --- |
| sessionId | Session ID |


### onImReconnecting()
`- (void)onImReconnecting`

Called when reconnection starts.

Triggered when the connection drops and reconnection begins. If an error occurs, the SDK fires the `onImDisconnected:errCode:errMsg:()` callback.

### onImReconnected()
`- (void)onImReconnected`

Called when reconnection succeeds.

Triggered after the connection is restored. If an error occurs, the SDK fires the `onImDisconnected:errCode:errMsg:()` callback.

### onImDisconnected:errCode:errMsg:()
`- (void)onImDisconnected:(RTCImDisconnectReason)reason errCode:(RTCEngineError)errCode errMsg:(nullable NSString *)errMsg`

Called when the connection drops or is closed involuntarily.

When the reason is `RTCImDisconnectReasonError`, the SDK has hit an unrecoverable error, such as an authentication failure. You need to get a new token before enabling the IM service again. For error codes, see [Error codes](/en/rtc/ios/error-codes).

When the reason is anything other than `RTCImDisconnectReasonError`, the connection was closed involuntarily. For the specific reasons, see [RTCImDisconnectReason](/en/rtc/ios/types#rtcimdisconnectreason).

**Parameters**

| reason | Disconnect reason |
| --- | --- |
| errCode | Error code |
| errMsg | Error message |


## Message callbacks
### onImMessage:action:userId:sessionId:nickname:()
`- (void)onImMessage:(NSString *)content action:(NSString *)action userId:(nullable NSString *)userId sessionId:(nullable NSString *)sessionId nickname:(nullable NSString *)nickname`

Called when a message arrives.

When your app's business features send a message through the backend API, the SDK notifies you through this callback.

**Parameters**

| content | Message content |
| --- | --- |
| action | Message action |
| userId | User ID |
| sessionId | Session ID |
| nickname | User nickname |
