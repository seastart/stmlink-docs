---
title: "iOS UI SDK integration"
description: "Low-code integration with UI for iOS (Objective-C): run the open-source MeetingKit demo, open the meeting UI to host or enter meetings, schedule meetings, use meeting controls, add screen sharing via a Broadcast Upload Extension, and customize chat. Read this to add a ready-made meeting UI to an Objective-C app."
---

The video conferencing SDK provides an open-source upper-layer UI kit. On iOS it currently supports only Objective-C, and you can bring up the meeting UI with a few simple API calls.

> Note: if you have your own UI design and want to build on the meeting features yourself, we also provide the more flexible and full-featured MeetingKit SDK. See our [MeetingKit API](/zh/meeting/ios/api-reference/MeetingKit) (Chinese) documentation to learn more.
>

## Features
The kit provides a rich set of interactions—scheduled meetings, audio and video control, screen sharing, meeting recording, member management, meeting controls, in-meeting chat, and more—and supports a variety of business scenarios.

| **Feature** | **Description** |
| --- | --- |
| Multi-party audio and video | Supports large meetings, with many members turning on audio and video at the same time. |
| Standard meeting UI | Contains the UI components a standard meeting needs, covering the features of basic audio and video meeting scenarios. |
| Custom UI | Because the kit is open source, you can also customize the UI for your own business scenarios. |
| Scheduled meetings | Supports scheduling meetings and shows scheduled meetings in the meeting list. |
| Screen sharing | Supports screen sharing, so members in the meeting can all watch what is shown on the shared screen. |
| Meeting controls | Meeting controls are split into before-the-meeting controls and in-meeting controls:<br/>+ Before the meeting, when creating and entering a meeting, you can preset meeting parameters to decide whether the microphone, camera, and speaker are on, as well as the meeting mode, type, and entry method (password, invitees only, etc.).<br/>+ During the meeting, all members can be managed: mute all / camera off for everyone, rename, remove from the room, transfer host, ask to unmute / mute, lock, and more. |
| In-meeting chat | Members can send messages in the chat area in real time, and the host or a co-host can also disable chat for members in the meeting. |
| Cloud recording | Supports recording and video compositing in video meeting scenarios. |
| Multi-device meeting login | Supports logging in on multiple devices. |
| Raise hand to speak | When mute all is on, members can send a request to speak to the host. |
| Room password | Supports creating password-protected rooms and scheduling password-protected rooms. |
| Set nickname and avatar | Supports changing the user's in-meeting nickname during the meeting. |


## Run the demo
### Prerequisites
+ iOS 12.0 or later

### Download the demo
#### 1. Download the source code
+ Option 1: download the [MeetingKit Demo](https://github.com/seastart/meeting-iOS-demo) source code from GitHub.
+ Option 2: run the following command directly in the terminal:

```objectivec
 git clone https://github.com/seastart/meeting-iOS-demo.git
```

#### 2. Add the dependency
```objectivec
pod 'MeetingKit', :git => "https://github.com/seastart/meeting-ios-cocoapods.git"
```

#### 3. Install the dependency
```objectivec
pod install
```

### Run the demo
#### 1. Generate your own certificate
##### 1.1. In Xcode, find Edit Behaviors.
![](/zh/meeting/ui-sdk/images/430475_1736933640871-ab3f72dd-4413-4620-aee5-c4899d515ab6.png)

##### 1.2. Click the Account tab, click the + button in the lower-left corner, choose to add an Apple ID, and click Continue.
![](/zh/meeting/ui-sdk/images/905562_1736934109790-8920f2fe-bf1e-4c29-9372-15db21c747e6.png)

##### 1.3. Enter your Apple ID and password to log in.
![](/zh/meeting/ui-sdk/images/202533_1736934290625-a6286ef8-6f4b-4ded-931e-e165bc525b23.png)

#### 2. Open the Signing & Capabilities tab under the project's TARGETS and select your own developer certificate in Team
![](/zh/meeting/ui-sdk/images/807711_1736934428150-41c9a25b-79ff-4aec-9dec-907dae463a27.png)

#### 3. Run the project
##### 3.1. First turn on Developer Mode on the iOS device under Settings > Privacy & Security > Developer Mode. Connect the device to your computer and select it as the run destination for the demo in Xcode.
![](/zh/meeting/ui-sdk/images/619379_1736934737291-dc604cf6-4816-4707-a9ef-6309fbe54f81.png)

##### 3.2. Click Run to run the MeetingKit iOS Demo on the target device.
| **Login screen** | **Main screen** | **Create meeting screen** |
| --- | --- | --- |
| ![](/zh/meeting/ui-sdk/images/575796_1736992186065-cd369eb8-8399-4824-8d33-a6a07704a6f1.png) | ![](/zh/meeting/ui-sdk/images/449513_1736934945587-e3c0abcb-b5b0-4368-b192-e920a572ee36.png) | ![](/zh/meeting/ui-sdk/images/622236_1736934974549-ee575fc1-6c95-4c11-9efc-c5abfaedc5e2.png) |


### Host starts a meeting
The meeting main screen is `FWRoomViewController`. After creating a room with the MeetingKit API, create and navigate to `FWRoomViewController` as in the example below to start a quick meeting.

#### Create a room
##### Build meeting parameters
Meeting parameters consist of many fields, but you usually only need a few of them. See [SEAMeetingParam](/zh/meeting/ios/types#seameetingparam) (Chinese) for details.

```objectivec
SEAMeetingParam *meetingParam = [[SEAMeetingParam alloc] init];
meetingParam.title = @"Meeting Title";
```

##### Create the room
```objectivec
[[MeetingKit sharedInstance] createRoom:meetingParam onSuccess:^(id _Nullable data) {
    NSString *roomNo = (NSString *)data;
    NSLog(@"Room created, room number: %@", roomNo);
} onFailed:^(SEAError code, NSString * _Nonnull message) {
    NSLog(@"Failed to create room, code = %ld, message = %@", code, message);
}];
```

#### Enter a room
##### Build meeting entry parameters
```objectivec
/// Create the meeting entry object
FWMeetingEnterModel *enterModel = [[FWMeetingEnterModel alloc] init];
enterModel.roomNo = @"Your Room No";
enterModel.nickname = @"Your Nickname";
enterModel.audioState = YES;
enterModel.videoState = NO;
enterModel.avatar = @"Your Avatar";
```

##### Navigate to the meeting main screen 
```objectivec
/// Enter the meeting main screen
[self push:@"FWRoomViewController" info:enterModel block:nil];
```

| **In-meeting screen** | **Meeting controls screen** |
| --- | --- |
| ![](/zh/meeting/ui-sdk/images/171180_1736993893112-9a82acbf-c8ce-4b46-86f6-622701c3f815.png) | ![](/zh/meeting/ui-sdk/images/930920_1736937496822-4040d787-cc39-4179-8580-cb9c1e9f134b.png) |


### Regular members enter a meeting
Create and navigate to the meeting main screen as in the **Enter a room** example above to enter a meeting.

| **Enter meeting screen** | **In-meeting screen** |
| --- | --- |
| ![](/zh/meeting/ui-sdk/images/453018_1736935601794-818414d9-aa1d-410b-aa9e-82398ad92cc7.png) | ![](/zh/meeting/ui-sdk/images/873379_1736993916062-da596a22-fffb-4b6d-a369-495955fc8191.png) |


## Scheduled meetings
### Overview
Users can schedule a room and arrange a meeting in their calendar. When the meeting time comes, they can start the meeting with a single tap.

| **Schedule a meeting** | **Meeting list** |
| --- | --- |
| ![](/zh/meeting/ui-sdk/images/276739_1736941919841-a4b84c17-9056-4541-a231-50013d04261f.png) | ![](/zh/meeting/ui-sdk/images/435834_1736941941160-baa381e6-8f69-4054-89a6-f2fbc10efac6.png) |


| **Meeting settings** | **Invite members** |
| --- | --- |
| ![](/zh/meeting/ui-sdk/images/765916_1736942097375-eec4522d-f2a9-4fe5-b212-9fa777334c1e.png) | ![](/zh/meeting/ui-sdk/images/380446_1736942106286-3c9cb2a7-4aab-4bf9-8d48-26d8397764c6.png) |


### Integration
#### Schedule a room
To use room scheduling, bring up the room scheduling page provided in the demo:

```objectivec
/// Create meeting details
FWMeetingDetailsModel *detailsModel = [[FWMeetingDetailsModel alloc] init];
/// Not currently in the room
detailsModel.isRoom = NO;
/// Mark the current user as the meeting creator
detailsModel.isMeetingAdmin = YES;
/// The meeting has not ended
detailsModel.isMeetingFinish = NO;
/// Set the invitee list data
detailsModel.memberLists = [self.viewModel.memberLists mutableCopy];
/// Navigate to the schedule meeting page
[self push:@"FWMeetingScheduleViewController" info:detailsModel tag:FWMeetingScheduleStateCreate block:nil];
```

+ Properties you can set for a scheduled meeting: meeting name, meeting type, start time, meeting duration, meeting mode, invited members, meeting password, member management, and more.
+ How to invite members: tap **邀请与会人** (*Invite invitees*) -> **添加** (*Add*) to invite members.

| **Invite invitees** | **Invitee list** | **Select invitees** |
| --- | --- | --- |
| ![](/zh/meeting/ui-sdk/images/459045_1736943352606-ed960e92-0920-47a0-93da-29936f40dfca.png) | ![](/zh/meeting/ui-sdk/images/820421_1736943359940-ccc56a5a-d406-4e96-aed4-a6918b71f360.png) | ![](/zh/meeting/ui-sdk/images/361854_1736943368075-072fa3c7-1978-461c-8559-f65211212530.png) |


#### View scheduled rooms
The demo provides a room list UI view, `FWHomeViewController`. The meeting list provides the following features:

+ View the meeting list: the list includes meetings you created and meetings you were invited to.
+ View meeting details: tap a meeting to view its details.
+ Edit meeting information: tap a meeting in the list; if it hasn't started yet and you are the organizer, you can edit its information.

| **Meeting list** | **View meeting details** | **Edit meeting information** |
| --- | --- | --- |
| ![](/zh/meeting/ui-sdk/images/190717_1736943827676-11dac981-e1db-4c1d-9708-e70d842ef347.png) | ![](/zh/meeting/ui-sdk/images/342963_1736943835475-6d78b8b1-bf7f-4f71-bf52-a5319dcffa40.png) | ![](/zh/meeting/ui-sdk/images/268033_1736943844704-8fc67f84-b50a-4965-92de-de058919f442.png) |


## Meeting controls
### Overview
After a user creates and enters a room, the host or a co-host can tap the members button in the bottom toolbar. In the member list that pops up from the bottom, they can select any regular member for meeting control actions such as asking to turn on video/audio, assigning co-hosts, disabling chat, and removing the member from the room, and can also apply meeting control actions such as mute all to all members in the room.

| **In-meeting screen** | **Member management** | **Mute all / camera off for everyone** |
| --- | --- | --- |
| ![](/zh/meeting/ui-sdk/images/697990_1736994746521-7623258a-08da-49f0-a2f6-a1fd19a8047b.png) | ![](/zh/meeting/ui-sdk/images/448718_1736994756908-5350085c-5ea0-4789-a496-0c76bf1a5d55.png) | ![](/zh/meeting/ui-sdk/images/574078_1736994766459-bd375991-7b22-4020-b386-2da8d87a93cf.png) |


| **Before-the-meeting controls** | |
| --- | --- |
| Create a room | You can configure the room: turn on the microphone/camera, mute all, camera off for everyone, room password, meeting name, meeting type, entry method, and more. |
| Enter a room | You can configure the room: turn on the microphone/camera. |
| **In-meeting controls** | |
| You are the host or a co-host | You can control the room: mute all / camera off for everyone, invite members, assign co-hosts and transfer host, remove members from the room, turn members' camera/microphone on or off, and more. |


#### Before-the-meeting controls
When creating and entering a meeting, you preset the meeting parameters through the before-the-meeting control features of `MeetingKit`.

| **Create a meeting** | **Enter a meeting** |
| --- | --- |
| ![](/zh/meeting/ui-sdk/images/490920_1736995488409-04cc4605-6b50-4f00-8b63-5658bcd42376.png) | ![](/zh/meeting/ui-sdk/images/519992_1736995498929-185b6bf2-9ec8-4fe9-8294-69104c5614b6.png) |


+ Create a room as follows to apply before-the-meeting controls:

```objectivec
/// Build meeting parameters
SEAMeetingParam *meetingParam = [[SEAMeetingParam alloc] init];
/// Replace with your custom room number; if not set, the system assigns one automatically
meetingParam.roomNo = @"Your room no";
/// Meeting title
meetingParam.title = @"Your title";
/// Meeting password; replace with your custom password
meetingParam.password = @"Your password";
/// Meeting type
meetingParam.meetingType = SEAMeetingTypeInitiate;
/// Meeting mode
meetingParam.meetingMode = SEAMeetingModeNormal;
/// Mute state when entering
meetingParam.entryMutePolicy = SEAMeetingMuteState3;
/// Invited members; replace with the IDs of the members you want to invite
meetingParam.conferee = @[@"target id"];
/// Create the room
[[MeetingKit sharedInstance] createRoom:meetingParam onSuccess:nil onFailed:nil];
```

+ Enter a room and set the entry parameters as follows to apply before-the-meeting controls:

```objectivec
/// Create the room entry object
FWMeetingEnterModel *enterModel = [[FWMeetingEnterModel alloc] init];
enterModel.roomNo = @"Your room no";
enterModel.nickname = @"User name";
enterModel.audioState = YES;
enterModel.videoState = YES;
enterModel.avatar = @"User avatar";
/// Enter the room screen
[self push:@"FWRoomViewController" info:enterModel block:nil];
```

#### In-meeting controls
The host or a co-host can manage all members in the meeting under **参会成员** (*Members*) -> **成员列表** (*Member list*).

+ The host or a co-host can select any member and control them individually: unmute/mute, turn video on/off, disable/enable chat, rename, remove from the room, and more.

| **Member management** | **Rename** | **Remove from meeting** |
| --- | --- | --- |
| ![](/zh/meeting/ui-sdk/images/453394_1736996984437-465ad89f-75d4-4417-b3ff-09c2f7e3557b.png) | ![](/zh/meeting/ui-sdk/images/315091_1736997006250-b0fd8f4e-f4a6-4213-ba5f-dd9eb32db954.png) | ![](/zh/meeting/ui-sdk/images/664325_1736997018971-aa589a7b-ce2c-4017-95e6-5d4986fa06bc.png) |


+ The host or a co-host can control all members in the room at once: mute all / unmute all, camera off for everyone / lift camera off for everyone, invite members, and more.

| **Mute all** | **Unmute all** | **Invite members** |
| --- | --- | --- |
| ![](/zh/meeting/ui-sdk/images/224773_1736997253741-87e83b37-f1ed-4998-8f00-f74baf9128ed.png) | ![](/zh/meeting/ui-sdk/images/450967_1736997262898-3d5f44b5-9a7b-4d4c-a39e-77a457cf1c8a.png) | ![](/zh/meeting/ui-sdk/images/904432_1736997271536-0b55b1b1-f10d-4660-aec8-5379c876499f.png) |


## Screen sharing
### Overview
After entering a room, users can share their screen by tapping the share button in the bottom toolbar.

| **Screen sharing** | **Start screen capture** |
| :---: | :---: |
| ![](/zh/meeting/ui-sdk/images/424226_1736937948724-d202827c-856b-4119-8270-676ef5225c6c.png) | ![](/zh/meeting/ui-sdk/images/618148_1736942451310-dab938c3-218b-4d4b-b8d9-792f36398bdf.png) |


### Integration
Cross-app screen sharing on iOS requires iOS 12 or later and a **Broadcast Upload Extension** screen recording process that works with the host app process to publish the stream. The system creates the extension's recording process when screen recording is needed, and it receives the screen images captured by the system. So you need to:

1. Create an **App Group** and configure it in Xcode (required). This lets the extension's recording process communicate with the host app process across processes;
2. In your project, create a new **Broadcast Upload Extension** target and integrate the **`MeetingKit.framework`** customized for extension modules in the SDK;
3. Implement the receiving logic on the host app side, so that the host app waits for the screen recording data from the **Broadcast Upload Extension**.

#### 1. Create an App Group
Log in to [https://developer.apple.com/](https://developer.apple.com/) with your developer account and do the following. Note that you need to download the corresponding **Provisioning Profile** again afterward.

1. Click **Identifiers**
2. Click the plus button on the right
3. Select **App Groups** and click **Continue**
4. Fill in **Description** and **Identifier** in the form. The **Identifier** is what you pass as the corresponding **AppGroup** parameter of the API. Then click **Continue**![](/zh/meeting/ui-sdk/images/302892_1681213421985-54346121-8573-4894-8e11-d565d65f6f8a.png)![](/zh/meeting/ui-sdk/images/959701_1681213164507-c107986e-b8b0-4325-8d02-36167e3474f5.png)
5. Back on the **Identifier** page, select **App IDs** from the menu in the upper right, then click your **App ID** (the host **App** and the **Extension** **AppID** need the same configuration)
6. Select **App Groups** and click **Edit**
7. In the form, select the **App Group** you created earlier, click **Continue** to return to the edit page, and click **Save**![](/zh/meeting/ui-sdk/images/583210_1681263123253-b6f939a2-e88e-42ce-ac8f-79f595f96355.png)
8. Download the **Provisioning Profile** again and configure it in **Xcode**

#### 2. Create a Broadcast Upload Extension
In your existing project, choose [New] -> [Target…] and select [Broadcast Upload Extension], as shown:

![](/zh/meeting/ui-sdk/images/377016_1591942375623-34530649-a3fe-4a08-8a5d-f2eb0d2a9a85.png)

Set the Product Name. After you click [Finish], the project has a new directory named after the Product Name you entered, containing a system-generated `SampleHandler` class that handles screen recording.

#### 3. Add the SDK dependency to the extension
1. For manual integration, import **`MeetingKit.framework`** into the project directory of the Product Name above and configure the required system libraries;
2. For automatic integration, update the `Podfile` and run `pod install`, as shown:

![](/zh/meeting/ui-sdk/images/486570_1736940851016-5ec8f955-6e57-4c56-9c04-5ec68e2f656d.png)

#### 4. Add background permissions to the host project
In the host project, go to [TARGETS] -> [Signing & Capabilities] -> [Capability] and select [Background Modes], as shown:

![](/zh/meeting/ui-sdk/images/236350_1591942975317-bd2e2df2-2452-44cb-b652-3db10a7d3928.png)

Double-click to add it, then check [Audio, AirPlay, and Picture in Picture], as shown:

![](/zh/meeting/ui-sdk/images/875454_1591943083527-5e406fa3-2988-48ed-a8b0-eaf1bb6b9def.png)

#### 5. Add the App Group to the extension project
Select the new target, click + Capability, and double-click App Groups, as shown:

![](/zh/meeting/ui-sdk/images/801090_1736941021633-f59f506e-fde9-48b1-b2f6-6ce15cc9f34c.png)

![](/zh/meeting/ui-sdk/images/916344_1681264222024-4b1c2971-2a4d-4cb2-b01b-9a962cf818b8.png)

When done, a file named `<target name>.entitlements` appears in the file list, as shown below. Select it, click +, and enter the App Group from the steps above.

![](/zh/meeting/ui-sdk/images/767042_1681264332965-1508da44-c011-4c52-b4ca-3aebf3a6b2bd.png)

In the new target, Xcode automatically creates a file named `SampleHandler.h`. Replace it with the following code, changing `kAppGroup` to the App Group Identifier you created above.

```objectivec
#import "SampleHandler.h"

/// Application Group Identifier
#define kAppGroup @"Application Group Identifier"

@interface SampleHandler() <MeetingKitScreenDelegate>

@end

@implementation SampleHandler

#pragma mark - Broadcast started
- (void)broadcastStartedWithSetupInfo:(NSDictionary<NSString *, NSObject *> *)setupInfo {
    
    /// User has requested to start the broadcast. Setup info from the UI extension can be supplied but optional.
    [[MeetingKit sharedInstance] broadcastStartedWithAppGroup:kAppGroup delegate:self];
}

#pragma mark - Broadcast paused
- (void)broadcastPaused {
    
    /// User has requested to pause the broadcast. Samples will stop being delivered.
}

#pragma mark - Broadcast resumed
- (void)broadcastResumed {
    
    /// User has requested to resume the broadcast. Samples delivery will resume.
}

#pragma mark - Broadcast finished
- (void)broadcastFinished {
    
    /// User has requested to finish the broadcast.
}

#pragma mark - Media data (audio and video)
/// Media data (audio and video)
/// - Parameters:
///   - sampleBuffer: video or audio frame
///   - sampleBufferType: media type
- (void)processSampleBuffer:(CMSampleBufferRef)sampleBuffer withType:(RPSampleBufferType)sampleBufferType {
    
    /// Send media data (audio and video)
    [[MeetingKit sharedInstance] sendSampleBuffer:sampleBuffer withType:sampleBufferType];
}


#pragma mark - ----- MeetingKitScreenDelegate methods -----
#pragma mark Screen recording finished callback
/// Screen recording finished callback
/// @param engine callback instance
/// @param reason reason for finishing
- (void)broadcastFinished:(MeetingKit *)engine reason:(NSString *)reason {
    
    /// Description
    NSString *describe = @"Screen recording has ended";
    /// Build the error
    NSError *error = [NSError errorWithDomain:NSStringFromClass(self.class) code:0 userInfo:@{NSLocalizedFailureReasonErrorKey : describe}];
    /// Finish screen recording
    [self finishBroadcastWithError:error];
}
```

### Integration steps
1\. Where you need the recording service, import `#import <MeetingKit/MeetingKit.h>` and create an `RPSystemBroadcastPickerView` object, as shown:

![](/zh/meeting/ui-sdk/images/692079_1721979921917-cdc69773-454e-4a1b-84d6-0cdbf3c744f0.png)

2\. To implement your business details, replace the `RPSystemBroadcastPickerView` button as follows. If the following page appears after the `broadcastButton` event, the extension is integrated successfully:

![](/zh/meeting/ui-sdk/images/574588_1721979942480-41eb9848-2602-43ef-a2e4-66080d0af1fd.png)

3\. In the host project, after initializing `MeetingKit`, implement the screen sharing status callback:

```objectivec
/// Screen capture status callback
/// @param status status code
- (void)onScreenRecordStatus:(SEAScreenRecordStatus)status {
    
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
/// @param engine callback instance
/// @param reason reason for finishing
- (void)broadcastFinished:(MeetingKit *)engine reason:(NSString *)reason {

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
    [[MeetingKit sharedInstance] broadcastStartedWithAppGroup:@"Application Group Identifier" delegate:self];
}
```

6\. Implement sending shared screen frames in the screen extension's `SampleHandler`:

```objectivec
- (void)processSampleBuffer:(CMSampleBufferRef)sampleBuffer withType:(RPSampleBufferType)sampleBufferType {
    
    /// Send media data (audio and video)
    [[MeetingKit sharedInstance] sendSampleBuffer:sampleBuffer withType:sampleBufferType];
}
```



## Meeting chat
### Overview
After entering a room, users can send text and emoji messages and transfer and view files under **聊天** (*Chat*) -> **聊天窗口** (*Chat window*).

| **In-meeting screen** | **Chat screen** | **Upload files** |
| --- | --- | --- |
| ![](/zh/meeting/ui-sdk/images/470982_1736999730740-2eaa1887-00a0-4320-9e9e-1648d1ec5439.png) | ![](/zh/meeting/ui-sdk/images/630197_1736999744568-10fed10c-097e-470d-94c5-ba50138b9131.png) | ![](/zh/meeting/ui-sdk/images/508684_1736999756543-4213bf13-3535-4181-b49f-6d2c43cf5044.png) |


### Customization
If the current UI doesn't meet your needs, you can modify the source code to get the UI you want. For reference:

```objectivec
You can modify the source code under the MeetingExample/Classes/Room/View/Message directory to get the UI you want.

Message       
  └── FWRoomMessageViewController.h          // Chat screen controller
  └── FWRoomMessageTableSectionHeaderView.h      // Chat screen section header
  └── FWRoomMessageMineTableViewCell.h      // Own text chat message cell
  └── FWRoomMessageMineFileTableViewCell.h      // Own file chat message cell
  └── FWRoomMessageTableViewCell.h      // Member text chat message cell
  └── FWRoomMessageFileTableViewCell.h      // Member file chat message cell
```
