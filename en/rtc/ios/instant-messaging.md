---
title: "IM"
description: "Use out-of-channel IM messages in the Objective-C SRTC SDK on iOS: enable IM with a token via enableImWithToken:delegate:, implement RTCEngineIMDelegate connection, reconnection, disconnection, and message callbacks, then disable IM and release resources."
---

### Step 1: Initialize the SDK
You must initialize the SDK before calling any other SDK function. For details, see [SDK initialization](/en/rtc/ios/quickstart#step-1-initialize-the-sdk).

### Step 2: Enable IM
#### Get a token
To enable the SDK's IM (out-of-channel messaging) service, first get an authentication token through the server API, then establish the messaging connection with the following API.

```objectivec
RTCEngineError errorCode = [[RTCEngineKit sharedEngine] enableImWithToken:@"Your Token" delegate:self];
if (errorCode != RTCEngineErrorOK) {
    NSLog(@"Failed to establish the IM connection");
}
```

#### Set the delegate
To subscribe to delegate events, you must create an instance of `RTCEngineIMDelegate` and make your class conform to the `RTCEngineIMDelegate` protocol.

```objectivec
@interface YourClass : NSObject <RTCEngineIMDelegate>
/// Add any of the following callbacks here as needed.
```

#### Implement the callbacks
+ **Connected callback**

```objectivec
/// Connected callback
/// You receive this event after calling enableImWithToken:() to enable IM; errors are reported through the onImDisconnected:() event.
/// - Parameters:
///   - userId: user ID
///   - sessionId: session ID
- (void)onImConnectSucceed:(NSString *)userId sessionId:(NSString *)sessionId {
    
    NSLog(@"IM connection established userId = %@, sessionId = %@", userId, sessionId);
}
```

+ **Reconnecting callback**

```objectivec
/// Reconnecting callback
/// This event means the connection has a problem, such as a network error, and the SDK is trying to reconnect.
- (void)onImReconnecting {
    
    NSLog(@"IM connection lost, the SDK is trying to reconnect.");
}
```

+ **Reconnected callback**

```objectivec
/// Reconnected callback
/// You receive this event when the connection is restored.
- (void)onImReconnected {
    
    NSLog(@"IM connection restored.");
}
```

+ **Disconnected callback**

```objectivec
/// Disconnected callback
/// Triggered by an unrecoverable error or an involuntary disconnect; if it's an error, you need to get a new token
/// @param reason leave reason
/// @param errCode error code
/// @param errMsg error message
- (void)onImDisconnected:(RTCImDisconnectReason)reason errCode:(RTCEngineError)errCode errMsg:(nullable NSString *)errMsg {
    
    NSLog(@"IM connection error or passive disconnect, please reconnect reason = %ld, errCode = %ld, errMsg = %@", reason, errCode, errMsg);
}
```

+ **Message received callback**

```objectivec
/// Message received callback
/// After a message is sent through the backend API, the specified users receive this event.
/// @param content message content
/// @param action message action
/// @param userId user ID
/// @param sessionId session ID
/// @param nickname user nickname
- (void)onImMessage:(NSString *)content action:(NSString *)action userId:(nullable NSString *)userId sessionId:(nullable NSString *)sessionId nickname:(nullable NSString *)nickname {
    
    NSLog(@"IM message received action = %@ content = %@ userId = %@", action, content, userId);
}
```

### Step 3: Disable IM
```objectivec
[[RTCEngineKit sharedEngine] disableIm];
```

### Step 4: Release resources
```objectivec
[[RTCEngineKit sharedEngine] destroy];
```

