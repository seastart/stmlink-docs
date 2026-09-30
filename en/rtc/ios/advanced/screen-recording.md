---
title: "Screen recording"
description: "Set up screen sharing with ReplayKit in the Objective-C SRTC SDK on iOS: create a Broadcast Upload Extension, add the SDK and background modes, implement RTCScreenDelegate in SampleHandler, and publish per channel with publishScreenRecord: only after the RTCScreenRecordStatusStart callback."
---

## Prepare the development environment
Use Xcode 14.0 or later, and the device must run iOS 16.0 or later; otherwise screen recording isn't available.

#### Create the extension
In your existing project, choose **New** -> **Target…** and select **Broadcast Upload Extension**, as shown:

![](/zh/rtc/ios/advanced/images/563485_1591942375623-34530649-a3fe-4a08-8a5d-f2eb0d2a9a85.png)

Set the Product Name. After you click **Finish**, the project has a new directory named after the Product Name you entered, containing a system-generated `SampleHandler` class that handles screen recording, and a corresponding Product Name SetupUI directory, containing a system-generated `BroadcastSetupViewController` class that handles the screen recording UI.

#### Add the SDK dependency to the extension
1. For manual integration, import `RTCEngineKit.framework` into the project directory of the Product Name above and configure the required system libraries;
2. For automatic integration, update the `Podfile` and run `pod install`, as shown:

![](/zh/rtc/ios/advanced/images/431440_1659061024229-9c42a253-7849-4db5-83e6-0302afcaede6.png)

#### Add background permissions to the host app
In the host project, go to **TARGETS** -> **Signing & Capabilities** -> **Capability** and select **Background Modes**, as shown:

![](/zh/rtc/ios/advanced/images/557448_1591942975317-bd2e2df2-2452-44cb-b652-3db10a7d3928.png)

Double-click to add it, then check **Audio, AirPlay, and Picture in Picture**, as shown:

![](/zh/rtc/ios/advanced/images/792573_1591943083527-5e406fa3-2988-48ed-a8b0-eaf1bb6b9def.png)

## Integration flow
1\. Where you use the recording service, add `#import <ReplayKit/ReplayKit.h>` and create an `RPSystemBroadcastPickerView` object, as shown: ![](/zh/rtc/ios/advanced/images/730239_1659061385614-7b8fbffe-03b4-439e-9358-4078457b5920.png)
2\. To implement your business details, replace the `RPSystemBroadcastPickerView` button as follows. If the following page appears after the `broadcastButton` event, the extension is integrated successfully: ![](/zh/rtc/ios/advanced/images/743648_1659061479129-4bb5753b-86f1-4277-90d8-ea9a8797c1ca.png)![](/zh/rtc/ios/advanced/images/375434_1591944630207-bd25dc92-4aab-4c28-9798-3b6d28449f8a.png)
3\. In the host project, pass in `RTCEngineChannelDelegate` when creating the channel instance, and implement the screen sharing status callback:

<Note>
Starting with `3.0.0`, ReplayKit capture is a process-level shared capability. Whether a given channel publishes the sharing stream is controlled by that channel instance's `publishScreenRecord:`, and the screen sharing status callback has accordingly moved to `RTCEngineChannelDelegate`, carrying the channel instance the event comes from. To stop screen recording for all channels in the process at once, still call `-[RTCEngineKit stopScreenRecord]`.

Starting with `3.0.1`, the SDK starts the capture service and keeps listening as soon as you join the channel, so users can start screen recording from the system panel at any time; `RTCScreenRecordStatusStart` is called back only after the extension connects. Therefore **you must call `publishScreenRecord:YES` only after receiving the `Start` callback**—don't call it early to publish the sharing stream.
</Note>

```objectivec
/// Screen sharing status callback
/// @param channel channel instance the event comes from
/// @param status status code
- (void)engineChannel:(RTCEngineChannel *)channel onScreenRecordStatus:(RTCScreenRecordStatus)status {
    
    /// Message to show
    NSString *toastStr = @"Screen sharing connection error";
    switch (status) {
        case RTCScreenRecordStatusError:
            toastStr = @"Screen sharing connection error";
            break;
        case RTCScreenRecordStatusStop:
            toastStr = @"Screen sharing has stopped";
            break;
        case RTCScreenRecordStatusStart:
            toastStr = @"Screen sharing has started";
            break;
        default:
            break;
    }
    [FWToastBridge showToastAction:toastStr];
    SGLOG(@"%@", toastStr);
}
```

4\. Implement the `RTCScreenDelegate` delegate in the screen extension's `SampleHandler`:

```objectivec
@interface SampleHandler : NSObject <RTCScreenDelegate>
/// Add any of the following callbacks here as needed.
```

```objectivec
/// Screen recording finished callback
/// @param engine callback instance
/// @param reason reason for finishing
- (void)broadcastFinished:(RTCEngineKit *)engine reason:(NSString *)reason {

    /// Description
    NSString *describe = @"Screen recording has ended";
    /// Build the error
    NSError *error = [NSError errorWithDomain:NSStringFromClass(self.class) code:0 userInfo:@{NSLocalizedFailureReasonErrorKey : describe}];
    /// Finish screen recording
    [self finishBroadcastWithError:error];
}
```

5\. Implement starting screen recording in the screen extension's `SampleHandler`:

```objectivec
- (void)broadcastStartedWithSetupInfo:(NSDictionary<NSString *,NSObject *> *)setupInfo {
    
    /// User has requested to start the broadcast. Setup info from the UI extension can be supplied but optional.
    [[RTCEngineKit sharedEngine] broadcastStartedWithAppGroup:@"Application Group Identifier" delegate:self];
}
```

6\. Implement sending shared screen frames in the screen extension's `SampleHandler`:

```objectivec
- (void)processSampleBuffer:(CMSampleBufferRef)sampleBuffer withType:(RPSampleBufferType)sampleBufferType {
    
    /// Send media data (audio and video)
    [[RTCEngineKit sharedEngine] sendSampleBuffer:sampleBuffer withType:sampleBufferType];
}
```

7\. After receiving the `RTCScreenRecordStatusStart` callback, the host project publishes screen sharing on each channel instance that should publish the sharing stream. Only when the last publishing channel unpublishes does the SDK disconnect the extension and end this system screen recording:

```objectivec
/// Publish the screen sharing stream on the current channel (call only after receiving the RTCScreenRecordStatusStart callback)
[self.channel publishScreenRecord:YES];

/// Stop the screen sharing stream on the current channel
[self.channel publishScreenRecord:NO];
```

The full sequence is: join the channel successfully (the SDK automatically starts the capture service and listens) → the user starts system screen recording via `RPSystemBroadcastPickerView` → the extension connects and you receive `RTCScreenRecordStatusStart` → the channel instance calls `publishScreenRecord:YES` to start publishing. To finish, call `publishScreenRecord:NO` (stops publishing on the current channel only) or `-[RTCEngineKit stopScreenRecord]` (ends this system screen recording; the capture service keeps listening, and the user can start it again).





