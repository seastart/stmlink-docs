---
title: "MeetingKit"
description: "Global singleton of the SMeeting iOS (Objective-C) SDK: login and logout, IM, meeting queries and scheduling, creating and querying room instances, local capture and preview, audio routing, virtual background, screen capture extension, and pre-call network check APIs. Read this for account- and device-level APIs."
---

`MeetingKit` is a singleton with only one instance per process. It carries only **account-level and device-level** capabilities: login, IM, local capture and preview, audio routing, process-side screen capture integration, the pre-call network check, and meeting queries and scheduling.

All in-meeting operations and events are scoped to a room and go through a [MeetingKitRoom](/en/meeting/ios/api-reference/MeetingKitRoom) instance created with `createRoomWithDelegate:`. The same account can create and enter multiple rooms at the same time, and the media and business state of each room are independent of each other.

<Warning>
Starting with `2.0.0`, the in-meeting APIs have moved out of this class. For `enterRoom:onSuccess:onFailed:`, `requestOpenCamera:view:onSuccess:onFailed:`, `sendRoomChatMessage:messageType:targetId:onSuccess:onFailed:`, the `adminXxx` family, cloud recording, the waiting room, sub-meetings, sign-in, and similar APIs, use [MeetingKitRoom](/en/meeting/ios/api-reference/MeetingKitRoom) instead.
</Warning>

## Core APIs
### sharedInstance()
`+ (MeetingKit *)sharedInstance`

Creates the MeetingKit instance (singleton).

### version()
`- (NSString *)version`

Gets the MeetingKit version number.

### language
`@property (nonatomic, copy, nullable) NSString *language`

SDK language (since `2.2.0`)

A BCP 47 language tag such as `@"zh-CN"` or `@"en"` (forms like `zh_CN` are normalized to `zh-CN`). `nil` or an empty string means following the system language (`[NSLocale preferredLanguages].firstObject`).

+ Only affects the `Accept-Language` request header sent to the backend: the backend returns business error messages in that language (the `message` of backend codes `1000`–`99999`)
+ Error `message`s produced by the SDK itself are always in English and don't change with the language
+ Applies process-wide and isn't reset by login / logout; we recommend setting it before login
+ Since `2.2.1`, it also sets the underlying [RTCEngineKit.language](/en/rtc/ios/api-reference/RTCEngineKit#language), so the meeting layer and the RTC layer use the same language; in `2.2.0`, RTC layer requests carry no language

```objectivec
[MeetingKit sharedInstance].language = @"en";
```

### currentLanguage
`@property (nonatomic, copy, readonly) NSString *currentLanguage`

The language actually in effect (since `2.2.0`; read-only)

Priority: `language` if set; otherwise the system's preferred language; `@"zh"` if that can't be obtained.

### addDelegate:()
`- (void)addDelegate:(id <MeetingKitDelegate>)delegate`

Sets the global event callback.

Through [MeetingKitDelegate](/en/meeting/ios/api-reference/MeetingKitDelegate) you receive two kinds of global event notifications: audio route changes and app performance. For in-room events, implement [MeetingKitRoomDelegate](/en/meeting/ios/api-reference/MeetingKitRoomDelegate) and pass it in when creating the room.

| Parameter | Description |
| :--- | --- |
| delegate | Listener instance |


### createRoomWithDelegate:()
`- (nullable MeetingKitRoom *)createRoomWithDelegate:(nullable id<MeetingKitRoomDelegate>)delegate`

Creates an independent meeting room instance.

Each call returns a new [MeetingKitRoom](/en/meeting/ios/api-reference/MeetingKitRoom) instance, and instances don't affect each other. To be in multiple rooms at the same time, call it multiple times and hold each instance separately.

The instance becomes invalid after you call the room's `exitRoom:`, and you need to create a new one.

| Parameter | Description |
| :--- | --- |
| delegate | Room event delegate; see [MeetingKitRoomDelegate](/en/meeting/ios/api-reference/MeetingKitRoomDelegate) |


### getRooms()
`- (NSArray<MeetingKitRoom *> *)getRooms`

Gets the list of meeting rooms you're currently in.

Instances that have been created but haven't entered the meeting yet, or that have already exited, aren't included in the result.

### loginWithToken:appGroup:onSuccess:onFailed:()
`- (void)loginWithToken:(NSString *)token appGroup:(NSString *)appGroup onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

Login API. You need to initialize the user information first before you can enter a room and perform other operations.

This API enables process-wide local log capture by default.

| Parameter | Description |
| :--- | --- |
| token | User token |
| appGroup | App Group identifier |
| onSuccess | Success callback |
| onFailed | Failure callback |


### loginWithToken:appGroup:logConfig:onSuccess:onFailed:()
`- (void)loginWithToken:(NSString *)token appGroup:(NSString *)appGroup logConfig:(SEALogConfig *)logConfig onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

Logs in with a custom log configuration. You need to initialize the user information first before you can enter a room and perform other operations.

| Parameter | Description |
| :--- | --- |
| token | User token |
| appGroup | App Group identifier |
| logConfig | Log configuration; see [SEALogConfig](/en/meeting/ios/types#sealogconfig) |
| onSuccess | Success callback |
| onFailed | Failure callback |


### logout()
`- (void)logout`

Logout API. Exits and destroys all room instances and releases resources, so you don't need to call `exitRoom:` on each room instance.

## IM APIs
### enableImWithDelegate:onSuccess:onFailed:()
`- (void)enableImWithDelegate:(nullable id<MeetingKitIMDelegate>)delegate onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

Enables IM.

Call this API to turn on the SDK's IM service, which you can use to build features such as pre-meeting calls and notifications.

| Parameter | Description |
| :--- | --- |
| delegate | Delegate; see [MeetingKitIMDelegate](/en/meeting/ios/api-reference/MeetingKitIMDelegate) |
| onSuccess | Success callback |
| onFailed | Failure callback |


### disableIm()
`- (void)disableIm`

Disables IM.

When you no longer need the IM service, disable it with this API.

## Meeting APIs
### getMeetingList:onFailed:()
`- (void)getMeetingList:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

Gets the meeting list.

| Parameter | Description |
| :--- | --- |
| onSuccess | Success callback; see [SEAMeetingListModel](/en/meeting/ios/types#seameetinglistmodel) |
| onFailed | Failure callback |


### getMoreMeetingList:onFailed:()
`- (void)getMoreMeetingList:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

Gets more of the meeting list (next page).

| Parameter | Description |
| :--- | --- |
| onSuccess | Success callback; see [SEAMeetingListModel](/en/meeting/ios/types#seameetinglistmodel) |
| onFailed | Failure callback |


### getHistoryMeetingList:onFailed:()
`- (void)getHistoryMeetingList:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

Gets the past meeting list.

| Parameter | Description |
| :--- | --- |
| onSuccess | Success callback; see [SEAMeetingListModel](/en/meeting/ios/types#seameetinglistmodel) |
| onFailed | Failure callback |


### getMoreHistoryMeetingList:onFailed:()
`- (void)getMoreHistoryMeetingList:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

Gets more of the past meeting list (next page).

| Parameter | Description |
| :--- | --- |
| onSuccess | Success callback; see [SEAMeetingListModel](/en/meeting/ios/types#seameetinglistmodel) |
| onFailed | Failure callback |


### getMeetingDetailsWithMeetingId:onSuccess:onFailed:()
`- (void)getMeetingDetailsWithMeetingId:(NSString *)meetingId onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

Gets meeting details.

| Parameter | Description |
| :--- | --- |
| meetingId | Meeting ID |
| onSuccess | Success callback; see [SEAMeetingModel](/en/meeting/ios/types#seameetingmodel) |
| onFailed | Failure callback |


### getMeetingDetailsWithRoomNo:onSuccess:onFailed:()
`- (void)getMeetingDetailsWithRoomNo:(NSString *)roomNo onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

Gets meeting details.

| Parameter | Description |
| :--- | --- |
| roomNo | Room number |
| onSuccess | Success callback; see [SEAMeetingModel](/en/meeting/ios/types#seameetingmodel) |
| onFailed | Failure callback |


### getParticipantListsWithMeetingId:onSuccess:onFailed:()
`- (void)getParticipantListsWithMeetingId:(NSString *)meetingId onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

Gets the attendance records of a meeting.

| Parameter | Description |
| :--- | --- |
| meetingId | Meeting ID |
| onSuccess | Success callback; see [SEAMemberListModel](/en/meeting/ios/types#seamemberlistmodel) |
| onFailed | Failure callback |


### getMoreParticipantListsWithMeetingId:onSuccess:onFailed:()
`- (void)getMoreParticipantListsWithMeetingId:(NSString *)meetingId onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

Gets more attendance records (next page).

| Parameter | Description |
| :--- | --- |
| meetingId | Meeting ID |
| onSuccess | Success callback; see [SEAMemberListModel](/en/meeting/ios/types#seamemberlistmodel) |
| onFailed | Failure callback |


### requestCancelMeetingWithMeetingId:onSuccess:onFailed:()
`- (void)requestCancelMeetingWithMeetingId:(NSString *)meetingId onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

Requests to cancel a meeting.

| Parameter | Description |
| :--- | --- |
| meetingId | Meeting ID |
| onSuccess | Success callback |
| onFailed | Failure callback |


### createRoom:onSuccess:onFailed:()
`- (void)createRoom:(SEAMeetingParam *)params onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

Creates a room.

| Parameter | Description |
| :--- | --- |
| params | Room creation parameters; see [SEAMeetingParam](/en/meeting/ios/types#seameetingparam) |
| onSuccess | Success callback |
| onFailed | Failure callback |


### updateRoom:onSuccess:onFailed:()
`- (void)updateRoom:(SEAMeetingParam *)params onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

Updates room data.

| Parameter | Description |
| :--- | --- |
| params | Room update parameters; see [SEAMeetingParam](/en/meeting/ios/types#seameetingparam) |
| onSuccess | Success callback |
| onFailed | Failure callback |

## Pre-call network check APIs

Available since `2.3.0`; requires `RTCEngineKit >= 3.3.0`. **Call it before joining**: it doesn't require entering a room or connecting to RTC. The check logic is the same as SRTC's [networkCheck:onItem:completion:](/en/rtc/ios/api-reference/RTCEngineKit#pre-call-network-check-apis): items are checked in the fixed order `permission` → `connectivity` → `mtu` → `dns` → `server`; when everything is normal it finishes within about 5 seconds, and takes at most about 10 seconds. The meeting layer adds a `meeting_api` subcheck (whether the meeting API is reachable) to the `server` item, and uses its own `SEANetworkCheckXxx` types.

### networkCheck:onItem:completion:()
`- (SEAError)networkCheck:(nullable SEANetworkCheckParams *)params onItem:(nullable SEANetworkCheckItemBlock)onItem completion:(nullable SEANetworkCheckCompletionBlock)completion`

Starts the pre-call network check.

| Parameter | Description |
| :--- | --- |
| params | Check parameters, see [SEANetworkCheckParams](/en/meeting/ios/types#seanetworkcheckparams). When logged in, you can pass `nil` and the app ID and server address are taken from the login info; when not logged in, pass `appId` + `serverUrl` or `token` |
| onItem | Per-item completion callback (main thread), called once per item in the order `permission` → `connectivity` → `mtu` → `dns` → `server`, with a [SEANetworkCheckItem](/en/meeting/ios/types#seanetworkcheckitem) |
| completion | Completion callback (main thread) with `(SEANetworkCheckResult * _Nullable result, SEAError errorCode)`: on normal completion, `errorCode` is `SEAErrorOK` and `result` is non-nil (see [SEANetworkCheckResult](/en/meeting/ios/types#seanetworkcheckresult)); when cancelled by `cancelNetworkCheck` (or by logging out), `result` is `nil` and `errorCode` is `SEAErrorUserCancelled` (`103026`) |

**Return value**

| Return value | Description |
| :--- | --- |
| `SEAErrorOK` | The check has started |
| `SEAErrorMeetingNotLoggedIn` (`203001`) | Not logged in, and `params` wasn't passed |
| `SEAErrorConflict` (`103005`) | A check is already running; only one check can run at a time (RTC layer code passed through) |
| `SEAErrorInvalidArgs` (`103031`) | Invalid parameters, or the token can't be decoded (RTC layer code passed through) |

**Example**

```objectivec
// When logged in, just pass nil for params
SEAError code = [[MeetingKit sharedInstance] networkCheck:nil onItem:^(SEANetworkCheckItem *item) {
    // Main thread, called once per completed item; message can be shown to users directly
    NSLog(@"%@ %@ %@", item.itemId, item.status, item.message);
} completion:^(SEANetworkCheckResult * _Nullable result, SEAError errorCode) {
    if (errorCode == SEAErrorUserCancelled) {
        return; // Cancelled by cancelNetworkCheck or by logging out
    }
    if ([result.status isEqualToString:SEANetworkCheckStatusFail]) {
        // Some item failed; prompt the user based on each item's reason / message
    }
}];
```

**The `meeting_api` subcheck of `server`**

+ It runs in parallel with the RTC checks and doesn't add to the total time; **any HTTP response counts as reachable**.
+ If the meeting API is unreachable, `server` is `fail` with `reason` `meeting_api_unreachable`; if `server` has already failed because of an RTC subcheck, the RTC `reason` is kept.
+ When not logged in, the meeting API address isn't available, so `meeting_api` is `skipped` with `reason` `server_info_unavailable`, which doesn't affect the overall status.
+ The other items' checks and reason codes are the same as SRTC's; see [SRTC iOS Types](/en/rtc/ios/types#rtcnetworkcheckitemid).

### cancelNetworkCheck()
`- (void)cancelNetworkCheck`

Cancels the pre-call network check.

After cancellation, `onItem` is no longer called and `completion` finishes with `SEAErrorUserCancelled` (`103026`). You can start a new check right away. Logging out also cancels a running check.

## User APIs
### getAgentList:keyword:onSuccess:onFailed:()
`- (void)getAgentList:(NSArray <NSNumber *> *)typesList keyword:(nullable NSString *)keyword onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

Gets the device list.

| Parameter | Description |
| :--- | --- |
| typesList | List of device types; for device types, see the [SEAAgentType](/en/meeting/ios/types#seaagenttype) definition |
| keyword | Keyword |
| onSuccess | Success callback; see [SEAAgentListModel](/en/meeting/ios/types#seaagentlistmodel) |
| onFailed | Failure callback |


### getMoreAgentList:keyword:onSuccess:onFailed:()
`- (void)getMoreAgentList:(NSArray <NSNumber *> *)typesList keyword:(nullable NSString *)keyword onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

Gets more of the device list (next page).

| Parameter | Description |
| :--- | --- |
| typesList | List of device types; for device types, see the [SEAAgentType](/en/meeting/ios/types#seaagenttype) definition |
| keyword | Keyword |
| onSuccess | Success callback; see [SEAAgentListModel](/en/meeting/ios/types#seaagentlistmodel) |
| onFailed | Failure callback |

## Local capture APIs
### updateLocalView:()
`- (void)updateLocalView:(VIEW_CLASS *)view`

Updates the local camera preview.

| Parameter | Description |
| :--- | --- |
| view | Video rendering view |


### switchCamera()
`- (void)switchCamera`

Switches between the front and rear cameras.

### setLocalPreviewMirror:()
`- (void)setLocalPreviewMirror:(BOOL)mirror`

Sets the local preview mirroring preference for the front camera.

Applies only to the local preview and doesn't affect the published data. The front camera is mirrored according to `mirror`, and the rear camera is never mirrored; after you switch cameras, the SDK applies the corresponding policy automatically.

| Parameter | Description |
| :--- | --- |
| mirror | YES: mirror the front camera; NO: don't mirror the front camera |


### currentCameraDirection()
`- (SEACameraDirection)currentCameraDirection`

Gets the current camera direction.

Returns the direction of the camera currently used for capture; see [SEACameraDirection](/en/meeting/ios/types#seacameradirection).

## Audio routing APIs
### switchAudioRoute:()
`- (void)switchAudioRoute:(SEAAudioRoute)route`

Switches the audio route.

Use this API to request switching between built-in audio output devices, such as the speaker and the earpiece. When a Bluetooth or wired headset is present, iOS decides which external device is used. The actual final route is whatever `currentAudioRoute` and the [onAudioRouteChange:previousRoute:()](/en/meeting/ios/api-reference/MeetingKitDelegate#onaudioroutechangepreviousroute) callback in `MeetingKitDelegate` report.

| Parameter | Description |
| :--- | --- |
| route | Audio route; see [SEAAudioRoute](/en/meeting/ios/types#seaaudioroute) |


### currentAudioRoute()
`- (SEAAudioRoute)currentAudioRoute`

Gets the system's current actual audio route.

Returns the audio route the system is actually using, such as the speaker, the earpiece, or a Bluetooth or wired headset. See [SEAAudioRoute](/en/meeting/ios/types#seaaudioroute).

### headphoneDeviceAvailable()
`- (BOOL)headphoneDeviceAvailable`

Whether a wired headset is present.

Returns whether a wired headset is present.

### bluetoothDeviceAvailable()
`- (BOOL)bluetoothDeviceAvailable`

Whether a Bluetooth headset is present.

Returns whether a Bluetooth headset is present.

## Virtual background APIs
Virtual background applies to the single shared camera capture pipeline in the process. It's a device-level capability, and its settings apply to all rooms at once. After you switch cameras during the meeting or reconnect after a disconnect, the SDK automatically re-applies the current configuration, so you don't need to do it yourself. For usage, see [Virtual background](/en/meeting/ios/advanced/virtual-background).

### installVirtualBackground:()
`- (SEAError)installVirtualBackground:(nullable NSString *)modelPath`

Installs the virtual background component.

We recommend calling it before entering the room and turning on the camera. After installation, you also need to call [enabledVirtualBackground:()](#enabledvirtualbackground) for it to take effect.

| Parameter | Description |
| :--- | --- |
| modelPath | Path to the person segmentation model file (`selfie_segmenter_fixed.onnx`); pass `nil` to use the copy built into the SDK |

| Return value | Description |
| :--- | --- |
| SEAErrorOK | Installed successfully |
| SEAErrorVirtualBackgroundAlreadyInstalled | The component is already installed; this call is discarded (`103027`; `SEAErrorConflict` before `2.2.0`) |
| SEAErrorVirtualBackgroundModelNotFound | The model file doesn't exist or is invalid; check `modelPath` (`103029`; `SEAErrorNotFound` before `2.2.0`) |
| SEAErrorVirtualBackgroundSessionFailed | Failed to create the inference session; this is a runtime environment problem (`103030`; `SEAErrorSystemError` before `2.2.0`) |


### uninstallVirtualBackground()
`- (void)uninstallVirtualBackground`

Uninstalls the virtual background component.

Releases the inference session and related buffers.

### enabledVirtualBackground:()
`- (SEAError)enabledVirtualBackground:(BOOL)enabled`

Virtual background switch.

After installation, it's off by default and must be turned on explicitly. When off, frames pass straight through with zero overhead, and no inference runs. Calling it before the component is installed returns `SEAErrorVirtualBackgroundNotInstalled` (`103028`; `SEAErrorConflict` before `2.2.0`).

| Parameter | Description |
| :--- | --- |
| enabled | YES: on; NO: off |


### setVirtualBackgroundBlur:()
`- (void)setVirtualBackgroundBlur:(NSInteger)level`

Sets background blur.

Mutually exclusive with [setVirtualBackgroundImage:()](#setvirtualbackgroundimage); the later call wins.

| Parameter | Description |
| :--- | --- |
| level | Blur level, range `1`–`10`, default `5`; out-of-range values are clamped to the boundary |


### setVirtualBackgroundImage:()
`- (void)setVirtualBackgroundImage:(nullable UIImage *)image`

Sets background replacement.

Mutually exclusive with [setVirtualBackgroundBlur:()](#setvirtualbackgroundblur); the later call wins.

| Parameter | Description |
| :--- | --- |
| image | Background image, cropped to cover without stretching; pass `nil` to cancel replacement and go back to blur |


### setVirtualBackgroundInferenceInterval:()
`- (void)setVirtualBackgroundInferenceInterval:(NSInteger)interval`

Sets the segmentation inference interval.

A performance tier for you to set per device model; we don't recommend exposing it to end users.

| Parameter | Description |
| :--- | --- |
| interval | Run segmentation every N frames (compositing still runs every frame); default `1`, and values below `1` are treated as `1`. Increase it on low-end devices to keep the frame rate up |


### setVirtualBackgroundMaskSync:()
`- (void)setVirtualBackgroundMaskSync:(BOOL)enabled`

Sets mask sync.

Eliminates misaligned trails when waving, at the cost of the video update rate dropping to the mask rate. When `interval` is `1`, turning it on or off makes no difference at all; it only takes effect after you increase the inference interval.

| Parameter | Description |
| :--- | --- |
| enabled | YES: on; NO: off; default NO |


### isVirtualBackgroundEnabled()
`- (BOOL)isVirtualBackgroundEnabled`

Gets whether virtual background is on.

## Screen sharing APIs
### broadcastStartedWithAppGroup:delegate:()
`- (void)broadcastStartedWithAppGroup:(NSString *)appGroup delegate:(id<MeetingKitScreenDelegate>)delegate`

Starts screen recording in the extension and binds the delegate.

Use this method in the extension's `SampleHandler`.

After screen capture is turned off, the SDK notifies you of the current device capture status through the [meetingRoom:onScreenRecordStatus:()](/en/meeting/ios/api-reference/MeetingKitRoomDelegate) callback in `MeetingKitRoomDelegate`. Based on the status in the callback, choose whether to request to start sharing or to stop sharing.

| Parameter | Description |
| :--- | --- |
| appGroup | App Group identifier |
| delegate | Screen recording extension delegate; see [Screen recording](/en/meeting/ios/advanced/screen-recording) |


### sendSampleBuffer:withType:()
`- (void)sendSampleBuffer:(CMSampleBufferRef)sampleBuffer withType:(RPSampleBufferType)sampleBufferType`

Sends screen capture frames from the extension.

Use this method in the extension's `SampleHandler`.

| Parameter | Description |
| :--- | --- |
| sampleBuffer | Data frame |
| sampleBufferType | Data frame type, including video, audio, and more |
