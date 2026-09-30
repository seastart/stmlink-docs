---
title: "RTCEngineKit"
description: "API reference for RTCEngineKit, the process-level engine singleton in the Objective-C SRTC SDK on iOS: init and destroy, creating and querying channel instances, IM, camera capture and preview, audio routing, screen capture extension, speed tests, beauty filters, and virtual background."
---

`RTCEngineKit` is a singleton with only one instance per process. It carries only **account-level and shared-hardware-level** capabilities: camera capture and preview, audio routing, ReplayKit screen capture, beauty filter rendering, network speed tests, IM (out-of-channel messaging), and the lifecycle management of channel instances.

In-channel capabilities such as joining and leaving, user data, publishing and subscribing to streams, and sending audio are carried by [RTCEngineChannel](/en/rtc/ios/api-reference/RTCEngineChannel), which you create with `createChannelWithDelegate:`. Multiple channel instances can exist in the same process at the same time, and user data, stream statistics, and rendering don't interfere across instances.

<Warning>
Starting with `3.0.0`, channel-related APIs have moved out of this class. Use [RTCEngineChannel](/en/rtc/ios/api-reference/RTCEngineChannel) for APIs such as `joinChannelWithToken:`, `leaveChannel:`, `publishLocalVideo:`, and `startRemoteView:trackId:view:`.
</Warning>

## Instance creation and event callbacks
### delegate
`id<RTCEngineDelegate> delegate`

Sets the process-level engine event callback.

Through [RTCEngineDelegate](/en/rtc/ios/api-reference/RTCEngineDelegate) you receive three kinds of process-level events: audio route changes, network speed tests, and app performance. For in-channel events, implement [RTCEngineChannelDelegate](/en/rtc/ios/api-reference/RTCEngineChannelDelegate).

### imDelegate
`id<RTCEngineIMDelegate> imDelegate`

Sets the IM event callback; see [RTCEngineIMDelegate](/en/rtc/ios/api-reference/RTCEngineIMDelegate).

### sharedEngine()
`+ (RTCEngineKit *)sharedEngine`

Creates the RTCEngineKit instance (singleton).

### sharedEngineWithConfig:appGroup:delegate:()
`+ (instancetype)sharedEngineWithConfig:(RTCEngineConfig *)engineConfig appGroup:(NSString *)appGroup delegate:(nullable id <RTCEngineDelegate>)delegate`

Creates the RTCEngineKit instance and initializes it at the same time (singleton).

This API is equivalent to calling `sharedEngine()` and then `initializeWithConfig:appGroup:delegate:()`, and suits cases where you want to create and initialize in one step.

**Parameters**

| engineConfig | Configuration parameters for logging and related settings, such as the log level; see [RTCEngineConfig](/en/rtc/ios/types#rtcengineconfig) |
| --- | --- |
| appGroup | App Group identifier |
| delegate | The callback delegate; see [RTCEngineDelegate](/en/rtc/ios/api-reference/RTCEngineDelegate) |


### initializeWithConfig:appGroup:delegate:()
`- (RTCEngineError)initializeWithConfig:(RTCEngineConfig *)engineConfig appGroup:(NSString *)appGroup delegate:(nullable id <RTCEngineDelegate>)delegate`

Initializes the RTCEngineKit service.

All RTC users must initialize the RTCEngineKit service before using the related APIs, including creating channel instances and joining channels.

**Parameters**

| engineConfig | Configuration parameters for logging and related settings, such as the log level; see [RTCEngineConfig](/en/rtc/ios/types#rtcengineconfig) |
| --- | --- |
| appGroup | App Group identifier |
| delegate | The callback delegate; see [RTCEngineDelegate](/en/rtc/ios/api-reference/RTCEngineDelegate) |


### destroy()
`- (void)destroy`

Destroys the RTCEngineKit instance (singleton).

It first destroys all live channel instances and waits for them to finish leaving before releasing process-level resources, so you don't need to call `destroy` on each channel instance yourself.

### version()
`- (NSString *)version`

Gets the RTCEngineKit version.

### decrypt:()
`+ (nullable NSString *)decrypt:(nullable NSString *)value`

Decrypts a string.

**Parameters**

| value | Encrypted string |
| --- | --- |


## Channel instance APIs
### createChannelWithDelegate:()
`- (nullable RTCEngineChannel *)createChannelWithDelegate:(nullable id<RTCEngineChannelDelegate>)delegate`

Creates a channel instance.

Each call returns an independent [RTCEngineChannel](/en/rtc/ios/api-reference/RTCEngineChannel) instance; you can call it multiple times to join multiple channels at the same time. The engine holds the channel instance; when you're done with it, call its `destroy` to destroy it; otherwise the instance isn't released.

Returns `nil` while the engine is being destroyed.

**Parameters**

| delegate | Channel event delegate; see [RTCEngineChannelDelegate](/en/rtc/ios/api-reference/RTCEngineChannelDelegate) |
| --- | --- |


### getChannels()
`- (NSArray<RTCEngineChannel *> *)getChannels`

Gets the list of active channels.

Returns the instances that have currently joined a channel. Instances that have been created but not yet joined, or that have already left, aren't included.

## IM APIs
### enableImWithToken:delegate:()
`- (RTCEngineError)enableImWithToken:(NSString *)token delegate:(nullable id<RTCEngineIMDelegate>)delegate`

Enables IM.

To use IM, an RTC user first calls the backend API to get an authentication token for enabling IM, then calls this API to start the SDK's IM service. You can use this service to build features such as pre-call invitations and notifications.

IM is an account-level capability, independent of how many channels you've joined.

**Parameters**

| token | Authentication token |
| --- | --- |
| delegate | The callback delegate; see [RTCEngineIMDelegate](/en/rtc/ios/api-reference/RTCEngineIMDelegate) |


### disableIm()
`- (void)disableIm`

Disables IM.

Use this API to disable the IM service when you no longer need it.

## Video APIs

<Note>
On iOS, the camera is single shared hardware, so capture and preview are process-level capabilities, and all channel instances share the same capture data. Whether that data is published to a given channel is controlled separately by that channel instance's `publishLocalVideo:`.
</Note>

### startLocalPreview:view:()
`- (RTCEngineError)startLocalPreview:(BOOL)frontCamera view:(VIEW_CLASS *)view`

Starts the local camera preview.

If you call this function before joining a channel, the SDK only turns on the camera and waits until a channel instance joins a channel before it starts publishing. If you call it after joining a channel, the SDK turns on the camera and starts publishing video automatically.

Starting with `2.5.7`, if the camera specified by `frontCamera` can't create an input or outputs no valid video frames after starting, the SDK automatically tries the other available camera. You don't need to call `switchCamera` to recover the preview; get the actual capture direction from `currentCameraDirection`.

**Parameters**

| frontCamera | YES: front camera; NO: rear camera |
| --- | --- |
| view | The view that displays the video |


### updateLocalView:()
`- (RTCEngineError)updateLocalView:(VIEW_CLASS *)view`

Updates the local camera preview view.

### stopLocalPreview()
`- (RTCEngineError)stopLocalPreview`

Stops the camera preview.

### switchCamera()
`- (RTCEngineError)switchCamera`

Switches the camera.

The SDK switches only if the target camera can create an input. If the target camera is unavailable, it keeps the current actual capture device and doesn't switch to an invalid input.

### setLocalPreviewMirror:()
`- (RTCEngineError)setLocalPreviewMirror:(BOOL)mirror`

Sets the mirroring preference for the front camera's local preview.

Applies only to the local preview, not to the published data. The front camera is mirrored according to `mirror`, and the rear camera is never mirrored; after you switch cameras, the SDK applies the corresponding policy automatically.

**Parameters**

| mirror | YES: mirror the front camera; NO: don't mirror the front camera |
| --- | --- |


### currentCameraDirection()
`- (RTCEngineCameraDirection)currentCameraDirection`

Gets the current camera direction.

Use this API to get the direction of the camera actually used for capture. If the requested camera is unavailable and an automatic fallback occurs, it returns the direction of the fallback device. For the return value, see [RTCEngineCameraDirection](/en/rtc/ios/types#rtcenginecameradirection).

### setCameraZoomRatio:()
`- (RTCEngineError)setCameraZoomRatio:(CGFloat)zoomRatio`

Sets the camera zoom ratio.

**Parameters**

| zoomRatio | Zoom factor, range 1.0–5.0 |
| --- | --- |


### setCameraFocusPosition:()
`- (RTCEngineError)setCameraFocusPosition:(CGPoint)position`

Sets the camera focus position.

**Parameters**

| position | Focus position |
| --- | --- |


### setCameraExposureRatio:()
`- (RTCEngineError)setCameraExposureRatio:(CGFloat)exposureRatio`

Sets the camera exposure factor.

**Parameters**

| exposureRatio | Exposure factor, range -8.0 to 8.0 |
| --- | --- |


### enableCameraTorch:()
`- (RTCEngineError)enableCameraTorch:(BOOL)enabled`

Sets the torch state.

**Parameters**

| enabled | YES: on; NO: off |
| --- | --- |


## Audio routing APIs

<Note>
Audio routing corresponds to the single `AVAudioSession` in the process. It's a shared device capability, and switching applies to all channel instances at once.
</Note>

### switchAudioRoute:()
`- (RTCEngineError)switchAudioRoute:(RTCAudioRoute)audioRoute`

Switches the audio route.

Use this API to explicitly request switching to the speaker, earpiece, Bluetooth headset, or wired headset. After you explicitly select the speaker or earpiece, the SDK keeps that selection; when no built-in route has been explicitly selected, starting with `2.5.8`, the SDK actively restores an available external device after the audio session is reconfigured, preferring the Bluetooth headset when both Bluetooth and wired headsets are present.

A successful return means the system call was accepted; the final actual route is determined by `currentAudioRoute` and the `onAudioRouteChange:previousRoute:` callback.

**Parameters**

| audioRoute | Audio route enum; see [RTCAudioRoute](/en/rtc/ios/types#rtcaudioroute) |
| --- | --- |


### currentAudioRoute()
`- (RTCAudioRoute)currentAudioRoute`

Gets the system's current actual audio route.

Use this API to get the audio playback device the system is actually using, such as the speaker, earpiece, Bluetooth headset, or wired headset.

### headphoneDeviceAvailable()
`- (BOOL)headphoneDeviceAvailable`

Checks whether a wired headset is present.

### bluetoothDeviceAvailable()
`- (BOOL)bluetoothDeviceAvailable`

Checks whether a Bluetooth headset is present.

## Screen sharing APIs

<Note>
ReplayKit capture runs in a separate Broadcast Upload Extension process and is a process-level shared capability; the captured data is distributed to channel instances according to their subscriptions. Whether a given channel publishes the sharing stream is controlled by that channel instance's `publishScreenRecord:`.
</Note>

### broadcastStartedWithAppGroup:delegate:()
`- (void)broadcastStartedWithAppGroup:(NSString *)appGroup delegate:(id<RTCScreenDelegate>)delegate`

Starts screen sharing from the extension and binds the callback delegate.

Use this method in the extension's `SampleHandler`; see [Screen recording](/en/rtc/ios/advanced/screen-recording) for details.

**Parameters**

| appGroup | App Group identifier |
| --- | --- |
| delegate | The callback delegate; see [Screen recording](/en/rtc/ios/advanced/screen-recording) |


### sendSampleBuffer:withType:()
`- (void)sendSampleBuffer:(CMSampleBufferRef)sampleBuffer withType:(RPSampleBufferType)sampleBufferType`

Sends shared screen frames from the extension.

Use this method in the extension's `SampleHandler`. It currently supports frames of type `RPSampleBufferTypeVideo` and `RPSampleBufferTypeAudioApp`; `RPSampleBufferTypeAudioMic` isn't supported, so handle microphone capture in the host app.

**Parameters**

| sampleBuffer | Screen frame data |
| --- | --- |
| sampleBufferType | Screen frame data type: app video, app audio, or microphone audio |


### stopScreenRecord()
`- (void)stopScreenRecord`

Stops screen sharing from the host app.

Use this method in the host app. It disconnects the extension to end this system screen recording, and stops sharing on all channel instances in the process. The capture service keeps listening while in the channel, so the user can still start screen recording again from the system panel. To stop publishing on a single channel only, call that channel instance's `publishScreenRecord:` with `NO`.

## Network speed test APIs
### startSpeedTest:()
`- (RTCEngineError)startSpeedTest:(RTCSpeedTestParams *)params`

Starts a network speed test (use before joining a channel).

**Parameters**

| params | Speed test parameters that specify basic information such as the link ID, server address and port, and test duration; see [RTCSpeedTestParams](/en/rtc/ios/types#rtcspeedtestparams) |
| --- | --- |


**Notes**

+ Run the speed test before joining a channel. A speed test while in a channel affects normal audio and video transmission, and because of heavy interference, the results are also inaccurate.
+ Only one speed test task can run at a time.

### stopSpeedTest()
`- (void)stopSpeedTest`

Stops the network speed test.

## Video rendering APIs

<Note>
Video rendering and beauty filters act on the shared camera capture pipeline, so settings apply to all channel instances at once.
</Note>

### installRenderModule:authDataSize:logLevel:()
`- (RTCEngineError)installRenderModule:(char *)authData authDataSize:(int)authDataSize logLevel:(RTCEngineLogLevel)logLevel`

Installs the video render module.

To use the SDK's video processing features such as beauty and filters, every RTC user must first call this function to load the video render resources and initialize the video render instance.

**Parameters**

| authData | License key |
| --- | --- |
| authDataSize | License key length |
| logLevel | Log level; see [RTCEngineLogLevel](/en/rtc/ios/types#rtcengineloglevel) |


### uninstallRenderModule()
`- (void)uninstallRenderModule`

Uninstalls the video render module.

When you no longer use the video render module, call this method to release the video render resources.

### enabledBeauty:()
`- (RTCEngineError)enabledBeauty:(BOOL)enabled`

Turns the beauty filter on or off.

After installing the video render module with `installRenderModule:authDataSize:logLevel:()`, use this method to turn the beauty filter on or off.

**Parameters**

| enabled | YES: turn the beauty filter on; NO: turn it off |
| --- | --- |


### setBlurLevel:()
`- (void)setBlurLevel:(float)blurLevel`

Sets the smoothing level.

**Parameters**

| blurLevel | Smoothing level, range 0.0–1.0, default 0.5 |
| --- | --- |


### getBlurLevel()
`- (float)getBlurLevel`

Gets the current smoothing level.

### setWhiteLevel:()
`- (void)setWhiteLevel:(float)whiteLevel`

Sets the whitening level.

**Parameters**

| whiteLevel | Whitening level, range 0.0–1.0, default 0.3 |
| --- | --- |


### getWhiteLevel()
`- (float)getWhiteLevel`

Gets the current whitening level.

### setRedLevel:()
`- (void)setRedLevel:(float)redLevel`

Sets the rosiness level.

**Parameters**

| redLevel | Rosiness level, range 0.0–1.0, default 0.3 |
| --- | --- |


### getRedLevel()
`- (float)getRedLevel`

Gets the current rosiness level.

### setSharpenLevel:()
`- (void)setSharpenLevel:(float)sharpenLevel`

Sets the sharpening level.

**Parameters**

| sharpenLevel | Sharpening level, range 0.0–1.0, default 0.3 |
| --- | --- |


### getSharpenLevel()
`- (float)getSharpenLevel`

Gets the current sharpening level.

### setFilterLevel:()
`- (void)setFilterLevel:(float)filterLevel`

Sets the filter level.

**Parameters**

| filterLevel | Filter level, range 0.0–1.0, default 0.8 |
| --- | --- |


### getFilterLevel()
`- (float)getFilterLevel`

Gets the current filter level.

### setFilterName:()
`- (void)setFilterName:(NSString *)filterName`

Sets the filter effect.

**Parameters**

| filterName | Filter effect, default "origin"; origin means the original image |
| --- | --- |


### getFilterName()
`- (NSString *)getFilterName`

Gets the current filter effect.

## Virtual background APIs

<Note>
Virtual background and beauty filters act on the same shared camera capture pipeline, so settings apply to all channel instances at once. When both are on, the order is fixed: beauty filter first, then virtual background.

Virtual background is an in-house component, and **installing it doesn't require a license key**. Before using it, make sure your project meets the iOS 16.0 and `onnxruntime` requirements; see [Integration](/en/rtc/ios/integration) and [Virtual background](/en/rtc/ios/advanced/virtual-background) for details.
</Note>

### installVirtualBackground:()
`- (RTCEngineError)installVirtualBackground:(nullable NSString *)modelPath`

Installs the virtual background component.

Before using background blur or background replacement, call this method to load the person segmentation model and create the inference session. After installing, it's off by default; `enabledVirtualBackground:()` decides whether it's on.

**Parameters**

| modelPath | Path to the person segmentation model file; pass nil to use the SDK's built-in model |
| --- | --- |


**Returns**

| RTCEngineErrorOK | Installed successfully |
| --- | --- |
| RTCEngineErrorConflict | The component is already installed; this call is discarded |
| RTCEngineErrorNotFound | The model file doesn't exist |
| RTCEngineErrorSystemError | Failed to create the inference session |


### uninstallVirtualBackground()
`- (void)uninstallVirtualBackground`

Uninstalls the virtual background component.

When you no longer use virtual background, call this method to release the inference session and related buffers. It's uninstalled automatically when the engine is destroyed.

### enabledVirtualBackground:()
`- (RTCEngineError)enabledVirtualBackground:(BOOL)enabled`

Turns virtual background on or off.

Returns `RTCEngineErrorConflict` if called when the component isn't installed. When off, it's a zero-overhead pass-through that runs no inference, and the inter-frame state is cleared, so the next time it's turned on it converges again from the first frame.

**Parameters**

| enabled | YES: on; NO: off |
| --- | --- |


### setVirtualBackgroundBlur:()
`- (void)setVirtualBackgroundBlur:(NSInteger)level`

Sets background blur.

Mutually exclusive with `setVirtualBackgroundImage:()`; the later call wins. If called before installing, it's remembered and takes effect automatically once installation completes.

**Parameters**

| level | Blur level, range 1–10, default 5; out-of-range values are clamped to the bounds |
| --- | --- |


### setVirtualBackgroundImage:()
`- (void)setVirtualBackgroundImage:(nullable UIImage *)image`

Sets background replacement.

Mutually exclusive with `setVirtualBackgroundBlur:()`; the later call wins.

**Parameters**

| image | Background image, scaled to cover (cropped, not stretched); pass nil to cancel replacement and go back to background blur |
| --- | --- |


### setVirtualBackgroundInferenceInterval:()
`- (void)setVirtualBackgroundInferenceInterval:(NSInteger)interval`

Sets the segmentation inference interval.

Used to keep frame rate on low-end devices; compositing still runs every frame.

**Parameters**

| interval | Run segmentation once every N frames, default 1; values less than 1 are treated as 1 |
| --- | --- |


### setVirtualBackgroundMaskSync:()
`- (void)setVirtualBackgroundMaskSync:(BOOL)enabled`

Sets mask sync.

When on, non-inference frames aren't recomposited, so the video and the mask are always from the same moment, which eliminates the misaligned trail when waving; the price is that the video update rate drops to the mask rate. When `interval` is 1, turning it on or off makes no difference.

**Parameters**

| enabled | YES: on; NO: off; default NO |
| --- | --- |


### isVirtualBackgroundEnabled()
`- (BOOL)isVirtualBackgroundEnabled`

Gets whether virtual background is on.
