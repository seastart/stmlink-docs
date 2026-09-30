---
title: "Screen recording"
description: "Screen sharing for the SMeeting iOS (Objective-C) SDK: create a Broadcast Upload Extension, add the MeetingKit dependency and background mode, handle screen capture status in MeetingKitRoomDelegate, and start capture and send frames from SampleHandler."
---

## Development environment
You need Xcode 14.0 or later, and the phone must run iOS 16.0 or later (the SDK's minimum system requirement starting with `2.1.0`; versions before `2.1.0` need iOS 12 or later to use screen recording).

#### Create the extension
In your existing project, choose [New] -> [Target…] and select [Broadcast Upload Extension], as shown:

![](/zh/meeting/ios/advanced/images/377016_1591942375623-34530649-a3fe-4a08-8a5d-f2eb0d2a9a85.png)

Set the Product Name. After you click [Finish], the project has a new directory named after the Product Name you entered, containing a system-generated `SampleHandler` class that handles screen recording, plus a corresponding Product Name SetupUI directory containing a system-generated `BroadcastSetupViewController` class that handles the screen recording UI.

#### Add the SDK dependency to the extension
To integrate `MeetingKit.framework` into the screen recording extension, update the `Podfile` and run `pod install`, as shown:

![](/zh/meeting/ios/advanced/images/162144_1721980142474-6e009eeb-2771-478c-a249-d63608f32ea9.png)

#### Add background permissions to the host app
In the host project, go to [TARGETS] -> [Signing & Capabilities] -> [Capability] and select [Background Modes], as shown:

![](/zh/meeting/ios/advanced/images/236350_1591942975317-bd2e2df2-2452-44cb-b652-3db10a7d3928.png)

Double-click to add it, then check [Audio, AirPlay, and Picture in Picture], as shown:

![](/zh/meeting/ios/advanced/images/875454_1591943083527-5e406fa3-2988-48ed-a8b0-eaf1bb6b9def.png)

## Integration steps
1\. Where you need the recording service, import `#import <MeetingKit/MeetingKit.h>` and create an `RPSystemBroadcastPickerView` object, as shown:

![](/zh/meeting/ios/advanced/images/692079_1721979921917-cdc69773-454e-4a1b-84d6-0cdbf3c744f0.png)

2\. To customize the button, replace the `RPSystemBroadcastPickerView` button as follows. If the page below appears after the `broadcastButton` event fires, the extension is integrated successfully:

![](/zh/meeting/ios/advanced/images/574588_1721979942480-41eb9848-2602-43ef-a2e4-66080d0af1fd.png)

3\. In the host project, pass in `MeetingKitRoomDelegate` when creating the room instance, and implement the screen sharing status callback:

<Note>
Starting with `2.0.0`, the process-side screen capture integration (`broadcastStartedWithAppGroup:delegate:`, `sendSampleBuffer:withType:`) stays on the `MeetingKit` singleton, while the screen sharing status callback has moved to `MeetingKitRoomDelegate` along with the other in-meeting events, and carries the room instance the event came from. To stop sharing, call `stopScreenRecord` on the room instance.
</Note>

```objectivec
/// Screen capture status callback
/// @param room Room instance the event came from
/// @param status Status code
- (void)meetingRoom:(MeetingKitRoom *)room onScreenRecordStatus:(SEAScreenRecordStatus)status {
    
    SGLOG(@"Screen sharing status notification, status = %ld", status);
    
    switch (status) {
        case SEAScreenRecordStatusError:
            /// Screen capture connection error
            break;
        case SEAScreenRecordStatusStop:
            /// Screen capture has stopped
            break;
        case SEAScreenRecordStatusStart:
            /// Screen capture has started
            break;
        default:
            break;
    }
}
```

4\. Implement the `RTCScreenDelegate` delegate in the screen extension's `SampleHandler`:

```objectivec
@interface SampleHandler : NSObject <MeetingKitScreenDelegate>
/// Add any of the following callbacks here as needed.
```

```objectivec
/// Screen recording finished callback
/// @param engine Callback instance
/// @param reason Reason for finishing
- (void)broadcastFinished:(MeetingKit *)engine reason:(NSString *)reason {

    /// Description
    NSString *describe = @"Screen recording has ended";
    /// Build the error
    NSError *error = [NSError errorWithDomain:NSStringFromClass(self.class) code:0 userInfo:@{NSLocalizedFailureReasonErrorKey : describe}];
    /// Finish screen recording
    [self finishBroadcastWithError:error];
}
```

5\. Start screen recording in the screen extension's `SampleHandler`:

```objectivec
- (void)broadcastStartedWithSetupInfo:(NSDictionary<NSString *,NSObject *> *)setupInfo {
    
    /// User has requested to start the broadcast. Setup info from the UI extension can be supplied but optional.
    [[MeetingKit sharedInstance] broadcastStartedWithAppGroup:@"Application Group Identifier" delegate:self];
}
```

6\. Send shared screen frames in the screen extension's `SampleHandler`:

```objectivec
- (void)processSampleBuffer:(CMSampleBufferRef)sampleBuffer withType:(RPSampleBufferType)sampleBufferType {
    
    /// Send media data (audio and video)
    [[MeetingKit sharedInstance] sendSampleBuffer:sampleBuffer withType:sampleBufferType];
}
```





