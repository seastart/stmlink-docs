---
title: "Quickstart"
description: "Get the SMeeting iOS (Objective-C) MeetingKit SDK running: install via CocoaPods, set permissions, log in, create a room, create a MeetingKitRoom instance and enter it, handle room events, turn the camera and microphone on or off, and subscribe to remote video. Read this first."
---

<Note>
**Apple platforms have two SMeeting SDKs. Decide which one you need first.** This page covers the Objective-C `MeetingKit` (distributed via CocoaPods, iOS only). There's also a native Swift SDK (`import SMeeting`, distributed as a Swift Package, supporting both iOS and macOS); see [Swift SDK](/en/meeting/swift/integration).

**We recommend the Swift SDK for new projects.** The two APIs can't be mixed, and don't add both to the same project.
</Note>

### Prerequisites
+ iOS 16.0 or later (starting with `2.1.0`; previously iOS 10.0)
+ Xcode 14.0 or later

<Warning>
Starting with `2.1.0`, the SDK has built-in virtual background, and the minimum system requirement is raised from iOS 10.0 to **iOS 16.0**. Both `IPHONEOS_DEPLOYMENT_TARGET` in your project and `platform :ios` in your `Podfile` must be at least 16.0; otherwise the dependency can't be resolved.

The virtual background inference engine `onnxruntime-c` is pulled in transitively by the `RTCEngineKit` podspec, so you don't need to declare it in your `Podfile`.
</Warning>

<Note>
Starting with `2.0.0`, the SDK is split into two layers: `MeetingKit` is a global singleton responsible for login, IM, meeting queries and scheduling, shared devices (camera, audio routing, screen capture), and creating room instances; `MeetingKitRoom` is a room instance responsible for entering and exiting the room and all in-meeting operations. The same account can create multiple room instances and be in multiple rooms at the same time.
</Note>

### Step 1: Import the SDK and set app permissions
#### Import the SDK
1\. Add the following dependency to your `Podfile`.

```objectivec
pod 'MeetingKit'
```

2\. Run the following command to install the SDK.

```objectivec
pod install
```

> Note:
>
> If you can't install the latest version of MeetingKit, run the following command to update your local CocoaPods repo list:
>

```objectivec
pod repo update
```

> If you still can't get the latest version, try specifying the MeetingKit source:
>

```objectivec
pod 'MeetingKit', :git => "https://github.com/seastart/meeting-ios-cocoapods.git"
```

3\. Import the header wherever you use MeetingKit.

```objectivec
#import <MeetingKit/MeetingKit.h>
```

#### Configure app permissions
Audio and video features require permission to use the microphone, camera, and photo library. Add the following entries to your app's Info.plist; they are the prompts shown in the system authorization dialogs for the microphone, camera, and photo library respectively.

```xml
<key>NSCameraUsageDescription</key>
<string>MeetingKit needs access to your camera</string>
<key>NSMicrophoneUsageDescription</key>
<string>MeetingKit needs access to your microphone</string>
<key>NSPhotoLibraryUsageDescription</key>
<string>MeetingKit needs access to your photo library</string>
```

### Step 2: Log in and log out
#### Log in
Before calling any other SDK function, you need to log in to the SDK. Add the following code to your project; it calls the relevant MeetingKit API to initialize the conferencing SDK. This step is essential, because MeetingKit features only work after login succeeds:

```objectivec
SEALogConfig *logConfig = [[SEALogConfig alloc] init];
logConfig.enableLocalLog = YES;

[[MeetingKit sharedInstance] loginWithToken:@"Meeting User Auth Token" appGroup:@"Application Group Identifier" logConfig:logConfig onSuccess:^(id _Nullable data) {
    NSLog(@"Conferencing SDK login succeeded");
} onFailed:^(SEAError code, NSString * _Nonnull message) {
    NSLog(@"Conferencing SDK login failed (%ld, %@)", code, message);
}];
```

`enableLocalLog` defaults to `YES`. When enabled, logs from the whole process are captured to a local file, and the host app's console output is kept. The login API without the `logConfig` parameter also uses this default.

#### Log out
```objectivec
[[MeetingKit sharedInstance] logout];
```

### Step 3: Create a room
#### Build meeting parameters
Meeting parameters consist of many fields, but you usually only need a few of them. For details, see [SEAMeetingParam](/en/meeting/ios/types#seameetingparam).

```objectivec
SEAMeetingParam *meetingParam = [[SEAMeetingParam alloc] init];
meetingParam.title = @"Meeting Title";
```

+ **The following table describes some properties of the `SEAMeetingParam` object.**

| **Parameter** | **Required** | **Description** |
| --- | :---: | --- |
| title | Yes | Meeting title |
| content | No | Meeting description |
| password | No | Meeting password |


#### Create the room
After creating the `SEAMeetingParam` object, call the SDK's `createRoom` function to create a cloud meeting room.

```objectivec
[[MeetingKit sharedInstance] createRoom:meetingParam onSuccess:^(id _Nullable data) {
    NSString *roomNo = (NSString *)data;
    NSLog(@"Room created, room number: %@", roomNo);
} onFailed:^(SEAError code, NSString * _Nonnull message) {
    NSLog(@"Failed to create room, code = %ld, message = %@", code, message);
}];
```

### Step 4: Create a room instance and enter the room
Starting with `2.0.0`, all in-meeting operations and events are scoped to a room. Before entering a room, create a `MeetingKitRoom` instance with `createRoomWithDelegate:`, passing in the room event delegate when you create it.

#### Set delegates
The SDK has two event protocols; implement each according to which events it owns:

+ `MeetingKitDelegate`: global events (audio route changes, app performance), set with `addDelegate:`;
+ `MeetingKitRoomDelegate`: in-room events (entering and exiting the room, member state, messages, cloud recording, stream quality, etc.), passed in when you create the room instance.

```objectivec
@interface YourClass : NSObject <MeetingKitDelegate, MeetingKitRoomDelegate>
/// Add any of the following callbacks here as needed.
```

#### Create a room instance
```objectivec
MeetingKitRoom *room = [[MeetingKit sharedInstance] createRoomWithDelegate:self];
/// The room instance becomes invalid after exitRoom: is called; keep your own reference to it
self.room = room;
```

To be in multiple rooms at the same time, call `createRoomWithDelegate:` multiple times and hold each instance separately. The media and business state of each room are independent of each other.

#### Implement event callbacks

The first parameter of every `MeetingKitRoomDelegate` callback is the room instance the event comes from, which tells you which room an event belongs to when you're in multiple rooms. The room number and meeting ID can be read from `room.roomNo` and `room.meetingId`.

+ **Error event callback**

```objectivec
/// Error event callback
/// An unrecoverable error occurred; this event usually means you need to get a new token and enter the meeting again.
/// - Parameters:
///   - room: Room instance the event comes from
///   - errCode: Error code
///   - errMsg: Error message
- (void)meetingRoom:(MeetingKitRoom *)room onError:(SEAError)errCode errMsg:(nullable NSString *)errMsg {
    
    NSLog(@"An error occurred (%ld), %@", (long)errCode, errMsg);
}
```

+ **Enter room event callback**

```objectivec
/// Enter room event callback
/// You receive this event after calling enterRoom: to enter the room; errors are thrown through the method's onFailed parameter.
/// - Parameters:
///   - room: Room instance the event comes from
///   - meetingId: Meeting ID
///   - userId: User ID
- (void)meetingRoom:(MeetingKitRoom *)room onEnterRoom:(NSString *)meetingId userId:(NSString *)userId {
    
    NSLog(@"Entered the room, %@ %@", meetingId, userId);
}
```

+ **Remote user entered the room callback**

```objectivec
/// Remote user entered the room callback
/// After a member calls enterRoom: to enter the room, all members in the current room receive this event.
/// - Parameters:
///   - room: Room instance the event comes from
///   - userId: Member ID
- (void)meetingRoom:(MeetingKitRoom *)room onUserEnter:(NSString *)userId {

    NSLog(@"Remote user entered the room, userId = %@", userId);
}
```

+ **Remote user exited the room callback**

```objectivec
/// Remote user exited the room callback
/// After a member calls exitRoom: to exit the room, all members in the current room receive this event.
/// - Parameters:
///   - room: Room instance the event comes from
///   - userId: Member ID
- (void)meetingRoom:(MeetingKitRoom *)room onUserExit:(NSString *)userId {

    NSLog(@"Remote user exited the room, userId = %@", userId);
}
```

+ **User camera state changed callback**

```objectivec
/// User camera state changed callback
/// All members in the current room receive this event after a member calls requestOpenCamera: or closeCamera: to turn the camera on or off, or after the host calls adminCloseUserCamera: to turn off a remote user's camera. Note: if members in the room already have their cameras on, you also receive this event when you enter the room.
/// - Parameters:
///   - room: Room instance the event comes from
///   - targetUserId: Target member ID
///   - cameraState: Video state
///   - reason: Reason for the change
- (void)meetingRoom:(MeetingKitRoom *)room onUserCameraStateChanged:(NSString *)targetUserId cameraState:(SEADeviceState)cameraState reason:(SEAChangeReason)reason {

    NSLog(@"User camera state changed, userId = %@ cameraState = %ld reason = %ld", targetUserId, (long)cameraState, (long)reason);
}
```

+ **User microphone state changed callback**

```objectivec
/// User microphone state changed callback
/// All members in the current room receive this event after a member calls requestOpenMic: or closeMic: to turn the microphone on or off, or after the host calls adminCloseUserMic: to turn off a remote user's microphone. Note: if members in the room already have their microphones on, you also receive this event when you enter the room.
/// - Parameters:
///   - room: Room instance the event comes from
///   - targetUserId: Target member ID
///   - micState: Audio state
///   - reason: Reason for the change
- (void)meetingRoom:(MeetingKitRoom *)room onUserMicStateChanged:(NSString *)targetUserId micState:(SEADeviceState)micState reason:(SEAChangeReason)reason {

    NSLog(@"User microphone state changed, userId = %@ micState = %ld reason = %ld", targetUserId, (long)micState, (long)reason);
}
```

#### Build meeting entry parameters
When calling the enterRoom API, fill in the key SEAMeetingEnterParam parameters. For details, see [SEAMeetingEnterParam](/en/meeting/ios/types#seameetingenterparam).

```objectivec
SEAMeetingEnterParam *meetingEnterParam = [[SEAMeetingEnterParam alloc] init];
meetingEnterParam.roomNo = @"Target Room No";
meetingEnterParam.nickname = @"Your Name";
meetingEnterParam.avatar = @"Your Portrait";
meetingEnterParam.isAudience = NO; // By default you enter the meeting as a full member; set to YES to enter as audience
```

#### Enter the room
After creating the `SEAMeetingEnterParam` object, call the SDK's `enterRoom` function to enter the cloud meeting room.

> Note that this method's success callback doesn't reflect whether you actually entered the room; it only means the API call itself completed. To confirm that you really entered the room, listen for the `onEnterRoom` event through the delegate above.
>

```objectivec
[self.room enterRoom:meetingEnterParam onSuccess:^(id  _Nullable data) {
    NSString *roomId = (NSString *)data;
    NSLog(@"Entered the room, room ID: %@", roomId);
} onFailed:^(SEAError code, NSString * _Nonnull message) {
    NSLog(@"Failed to enter the room, code = %ld, message = %@", code, message);
}];
```

#### Exit the room
> Calling this API makes the user exit their current room and releases device resources such as the camera, microphone, and speaker. Once the resources are released, the SDK notifies you through the `onSuccess` callback. If you want to call `enterRoom:()` again, we recommend waiting for the `onSuccess` callback before doing anything else, to avoid problems such as the camera or microphone being occupied.
>

```objectivec
[self.room exitRoom:^(id  _Nullable data) {
    /// TO DO...
}];
self.room = nil;
```

> The room instance becomes invalid after `exitRoom:` is called. To enter the meeting again, create a new instance with `createRoomWithDelegate:`. Calling `logout` exits and destroys all room instances, so you don't need to exit each one.
>

### Step 5: Turn the camera on and off
After you request to turn the camera on or off, the service determines the user's camera state through its own logic. The SDK then receives the `onUserCameraStateChanged` event.

#### Turn on the camera
```objectivec
[self.room requestOpenCamera:YES view:preview onSuccess:^(id  _Nullable data) {
    NSLog(@"Request to turn on the camera succeeded");
} onFailed:^(SEAError code, NSString * _Nonnull message) {
    NSLog(@"Request to turn on the camera failed, code = %ld, message = %@", code, message);
}];
```

#### Turn off the camera
```objectivec
[self.room closeCamera:^(id  _Nullable data) {
    NSLog(@"Request to turn off the camera succeeded");
} onFailed:^(SEAError code, NSString * _Nonnull message) {
    NSLog(@"Request to turn off the camera failed, code = %ld, message = %@", code, message);
}];
```

> Note that the success callbacks of the methods above don't reflect the actual camera state; they only mean the API call itself completed. To keep the camera state consistent between the client and the server, listen for the `onUserCameraStateChanged` event through the delegate.
>

### Step 6: Turn the microphone on and off
After you request to turn the microphone on or off, the service determines the user's microphone state through its own logic. The SDK then receives the `onUserMicStateChanged` event.

#### Turn on the microphone
```objectivec
[self.room requestOpenMic:^(id  _Nullable data) {
    NSLog(@"Request to turn on the microphone succeeded");
} onFailed:^(SEAError code, NSString * _Nonnull message) {
    NSLog(@"Request to turn on the microphone failed, code = %ld, message = %@", code, message);
}];
```

#### Turn off the microphone
```objectivec
[self.room closeMic:^(id  _Nullable data) {
    NSLog(@"Request to turn off the microphone succeeded");
} onFailed:^(SEAError code, NSString * _Nonnull message) {
    NSLog(@"Request to turn off the microphone failed, code = %ld, message = %@", code, message);
}];
```

> Note that the success callbacks of the methods above don't reflect the actual microphone state; they only mean the API call itself completed. To keep the microphone state consistent between the client and the server, listen for the `onUserMicStateChanged` event through the delegate.
>

### Step 7: Subscribe to and unsubscribe from remote user video
#### Subscribe to remote user video
```objectivec
[self.room startRemoteView:@"Remote User ID" streamType:SEAVideoStreamTypeBig view:playerView];
```

+ **The following table describes all values of the `SEAVideoStreamType` video stream type.**

| **Enum** | **Value** | **Description** |
| --- | :---: | --- |
| SEAVideoStreamTypeBig | `1` | High stream: the large, high-definition view, usually used to carry camera video |
| SEAVideoStreamTypeSmall | `2` | Low stream: the small, low-definition view. It has the same content as the high stream, but a lower resolution and bitrate, so it's less sharp |
| SEAVideoStreamTypeScreen | `3` | Screen sharing stream |


#### Unsubscribe from remote user video
```objectivec
[self.room stopRemoteView:@"Remote User ID" streamType:SEAVideoStreamTypeBig];
```

#### Unsubscribe from all video of a specific remote user
```objectivec
[self.room stopAllRemoteViewWithUserId:@"Remote User ID"];
```

#### Unsubscribe from all remote users' video
The SDK doesn't provide an API to unsubscribe from all members at once. Iterate over the member list and call `stopAllRemoteViewWithUserId:` for each one.

```objectivec
for (SEAUserModel *userModel in [self.room getRemoteUsers]) {
    [self.room stopAllRemoteViewWithUserId:userModel.userId];
}
```

> Note: after you unsubscribe from a member's video, the SDK releases the rendering view itself.
>
