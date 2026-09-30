---
title: "Quickstart"
description: "The minimal Objective-C SRTC flow on iOS: initialize RTCEngineKit, implement RTCEngineDelegate and RTCEngineChannelDelegate, create a channel instance and join, preview and publish the camera, subscribe to remote video by track ID, then leave and destroy. Read after completing integration."
---

<Note>
Starting with `3.0.0`, the SDK has two layers: `RTCEngineKit` is a process-level singleton that handles initialization, shared hardware (camera, audio routing, screen capture), and creating channel instances; `RTCEngineChannel` is a channel instance that handles joining the channel, publishing, and subscribing to streams. A single process can create multiple channel instances and join multiple channels at the same time.
</Note>

### Step 1: Initialize the SDK
#### Create the initialization parameters
You must initialize the SDK before calling any other SDK function. To initialize the SDK, create an instance of the `RTCEngineConfig` object.

```objectivec
RTCEngineConfig *engineConfig = [[RTCEngineConfig alloc] init];
engineConfig.enableLocalLog = YES;
```

+ **The following table describes all properties of the `RTCEngineConfig` object.**

| **Parameter** | **Required** | **Description** |
| --- | :---: | --- |
| logPath | No | Log file path; defaults to the sandbox Document directory |
| enableLocalLog | No | Whether to enable local logging; defaults to NO |


#### Initialize the RTC engine
After creating the `RTCEngineConfig` object, call the SDK's `initializeWithConfig` function to set the delegate and verify that initialization succeeded.

```objectivec
RTCEngineError errorCode = [[RTCEngineKit sharedEngine] initializeWithConfig:self.engineConfig appGroup:@"Application Group Identifier" delegate:self];
if (errorCode != RTCEngineErrorOK) {
    NSLog(@"Failed to initialize the RTC service");
}
```

#### Set the delegates
The SDK has two event protocols; implement each according to which events it owns:

+ `RTCEngineDelegate`: process-level events (audio route changes, network speed tests, app performance), passed in during initialization;
+ `RTCEngineChannelDelegate`: in-channel events (connection, users, messages, streams, screen sharing), passed in when you create a channel instance.

```objectivec
@interface YourClass : NSObject <RTCEngineDelegate, RTCEngineChannelDelegate>
/// Add any of the following callbacks here as needed.
```

#### Implement the callbacks

The first parameter of every `RTCEngineChannelDelegate` callback is the channel instance the event comes from. In multi-channel scenarios, use it to tell which channel an event belongs to; the channel name is available from `channel.channel`.

+ **Join succeeded callback**

```objectivec
/// Join succeeded callback
/// @param channel channel instance the event comes from
/// @param userId user ID
- (void)engineChannel:(RTCEngineChannel *)channel onJoinSucceed:(NSString *)userId {
    
    NSLog(@"Joined the channel: channel = %@, userId = %@", channel.channel, userId);
}
```

+ **Local user data updated callback**

```objectivec
/// Local user data updated callback
/// @param channel channel instance the event comes from
/// @param userId user ID
- (void)engineChannel:(RTCEngineChannel *)channel onUserUpdate:(NSString *)userId {
    
    NSLog(@"Local user data updated: channel = %@, userId = %@", channel.channel, userId);
}
```

+ **Reconnecting callback**

```objectivec
/// Reconnecting callback
/// @param channel channel instance the event comes from
- (void)engineChannelOnReconnecting:(RTCEngineChannel *)channel {
    
    NSLog(@"Connection lost, the SDK is trying to reconnect channel = %@", channel.channel);
}
```

+ **Reconnected callback**

```objectivec
/// Reconnected callback
/// @param channel channel instance the event comes from
- (void)engineChannelOnReconnected:(RTCEngineChannel *)channel {
    
    NSLog(@"Service connected/reconnected channel = %@", channel.channel);
}
```

+ **Disconnected callback**

```objectivec
/// Disconnected callback
/// Triggered by an unrecoverable error or when you leave the channel involuntarily; you need to get a new token after this event
/// @param channel channel instance the event comes from
/// @param reason leave reason
/// @param errCode error code
/// @param errMsg error message
- (void)engineChannel:(RTCEngineChannel *)channel onDisconnected:(RTCLeaveReason)reason errCode:(RTCEngineError)errCode errMsg:(nullable NSString *)errMsg {
    
    NSLog(@"Disconnected or removed from the channel, please log in again channel = %@, reason = %ld, errCode = %ld, errMsg = %@", channel.channel, (long)reason, (long)errCode, errMsg);
}
```

+ **Custom message callback**

```objectivec
/// Custom message callback
/// @param channel channel instance the event comes from
/// @param content message content
/// @param action message action
/// @param userId user ID
/// @param sessionId session ID
/// @param nickname user nickname
- (void)engineChannel:(RTCEngineChannel *)channel onCustomMessage:(NSString *)content action:(NSString *)action userId:(nullable NSString *)userId sessionId:(nullable NSString *)sessionId nickname:(nullable NSString *)nickname {
    
    NSLog(@"Received a custom message channel = %@, action = %@, content = %@", channel.channel, action, content);
}
```

+ **Channel updated callback**

```objectivec
/// Channel updated callback
/// @param channel channel instance the event comes from
/// @param props custom data
- (void)engineChannel:(RTCEngineChannel *)channel onChannelUpdate:(NSString *)props {
    
    NSLog(@"Channel data updated channel = %@, props = %@", channel.channel, props);
}
```

+ **User joined callback**

```objectivec
/// User joined callback
/// @param channel channel instance the event comes from
/// @param userId user ID
- (void)engineChannel:(RTCEngineChannel *)channel onRemoteUserJoinChannel:(NSString *)userId {
    
    NSLog(@"A user joined the channel channel = %@, userId = %@", channel.channel, userId);
}
```

+ **User data updated callback**

```objectivec
/// User data updated callback
/// @param channel channel instance the event comes from
/// @param userId user ID
- (void)engineChannel:(RTCEngineChannel *)channel onRemoteUserUpdate:(NSString *)userId {
    
    NSLog(@"User data updated channel = %@, userId = %@", channel.channel, userId);
}
```

+ **User left callback**

```objectivec
/// User left callback
/// @param channel channel instance the event comes from
/// @param userId user ID
/// @param reason leave reason
- (void)engineChannel:(RTCEngineChannel *)channel onRemoteUserLeaveChannel:(NSString *)userId reason:(RTCLeaveReason)reason {
    
    NSLog(@"A user left the channel channel = %@, userId = %@", channel.channel, userId);
}
```

+ **User stream changed callback**

```objectivec
/// User stream changed callback
/// @param channel channel instance the event comes from
/// @param userId user ID
/// @param streamTrackModel stream track data
/// @param changeType change type
- (void)engineChannel:(RTCEngineChannel *)channel onRemoteStreamTrackChange:(NSString *)userId streamTrackModel:(RTCEngineStreamTrackModel *)streamTrackModel changeType:(RTCChangeType)changeType {
    
    NSLog(@"User stream changed channel = %@, userId = %@, streamTrackModel = %@", channel.channel, userId, streamTrackModel);
}
```

### Step 2: Create a channel instance and join the channel
#### Create a channel instance
```objectivec
RTCEngineChannel *channel = [[RTCEngineKit sharedEngine] createChannelWithDelegate:self];
/// The engine holds the channel instance; just keep your own reference to it
self.channel = channel;
```

To join multiple channels at the same time, call `createChannelWithDelegate:` multiple times and hold each instance separately. User data, stream statistics, and rendering don't interfere across instances.

#### Join the channel
```objectivec
RTCEngineError errorCode = [self.channel joinChannelWithToken:@"Your Token"];
if (errorCode != RTCEngineErrorOK) {
    NSLog(@"Failed to join the channel");
}
```

#### Leave the channel
```objectivec
[self.channel leaveChannel:^{
    /// TO DO...
}];
```

#### Destroy the channel instance
You must destroy the instance when you're done with it; otherwise the engine keeps holding the channel.

```objectivec
[self.channel destroy];
self.channel = nil;
```

### Step 3: Publish video
The camera is process-level shared hardware, so capture and preview are controlled through the `RTCEngineKit` singleton; whether that video is published to a given channel is controlled separately by that channel instance's `publishLocalVideo:`.

#### Start the preview
```objectivec
[[RTCEngineKit sharedEngine] startLocalPreview:YES view:self.localView];
```

#### Update the preview
```objectivec
[[RTCEngineKit sharedEngine] updateLocalView:self.localView];
```

#### Stop the preview
```objectivec
[[RTCEngineKit sharedEngine] stopLocalPreview];
```

#### Resume/pause publishing to the current channel
```objectivec
[self.channel publishLocalVideo:YES];
```

### Step 4: Subscribe to and unsubscribe from remote video
#### Subscribe to a remote user's video
```objectivec
[self.channel startRemoteView:userId trackId:trackId view:self.previewView];
```

+ **The following table describes all values of the `RTCTrackIdentifierFlags` track ID enum.**

| **Enum name** | **Value** | **Description** |
| --- | :---: | --- |
| RTCTrackIdentifierFlags0 | `0` | Track 0 |
| RTCTrackIdentifierFlags1 | `1` | Track 1 |
| RTCTrackIdentifierFlags2 | `2` | Track 2 |
| RTCTrackIdentifierFlags3 | `3` | Track 3 |
| RTCTrackIdentifierFlags4 | `4` | Track 4 |
| RTCTrackIdentifierFlags5 | `5` | Track 5 |
| RTCTrackIdentifierFlags6 | `6` | Track 6 |


#### Update a remote user's video
```objectivec
[self.channel updateRemoteView:userId trackId:trackId view:self.previewView];
```

#### Unsubscribe from a remote user's video
```objectivec
[self.channel stopRemoteView:userId trackId:trackId];
```

#### Unsubscribe from all video streams of a specific remote user
```objectivec
[self.channel stopAllRemoteViewWithUserId:userId];
```

### Step 5: Release resources
`destroy` first destroys all live channel instances and waits for them to finish leaving before releasing process-level resources, so you don't need to call `destroy` on each channel instance yourself.

```objectivec
[[RTCEngineKit sharedEngine] destroy];
```
