---
title: "RTCEngineKit"
description: "iOS SRTC 音视频 SDK RTCEngineKit 接口参考"
---

## 创建实例和事件回调
### delegate
`id<RTCEngineDelegate> delegate`

设置 RTC 事件回调

您可以通过`RTCEngineDelegate`获得来自 SDK 的各类事件通知（比如：错误码，音视频状态参数等）。

### sharedEngine()
`+ (RTCEngineKit *)sharedEngine`

创建 RTCEngineKit 实例（单例模式）。

### destroy()
`- (void)destroy`

销毁 RTCEngineKit 实例（单例模式）。

### version()
`- (NSString *)version`

获取 RTCEngineKit 版本号。

### initializeWithConfig:appGroup:delegate:()
`- (RTCEngineError)initializeWithConfig:(RTCEngineConfig *)engineConfig appGroup:(NSString *)appGroup delegate:(nullable id <RTCEngineDelegate>)delegate`

初始化 RTCEngineKit 服务

RTC 的所有用户都需要初始化 RTCEngineKit 服务之后才可以使用相关的接口，包括加入频道等。

**参数**

| engineConfig | 配置参数，用于日志等的相关配置，例如：日志等级等等信息，详情请参考 [RTCEngineConfig](https://www.yuque.com/anyconf/rtcengine/yi50z7#aP2yB) |
| --- | --- |
| appGroup | Application Group Identifier |
| delegate | 用于指定回调代理，详情请参考 [RTCEngineDelegate](https://www.yuque.com/anyconf/rtcengine/su58c7) |


## 即时通讯相关接口函数
### enableImWithToken:delegate:()
`- (RTCEngineError)enableImWithToken:(NSString *)token delegate:(nullable id<RTCEngineIMDelegate>)delegate`

启用即时通讯

RTC 的所有用户如需使用即时通讯业务，首先调后台接口获取启用即时通讯的鉴权令牌，然后调用该接口开启 SDK 即时通讯服务，方便开发者利用该服务实现，如会前呼叫、通知等业务功能。

**参数**

| token | 鉴权令牌 |
| --- | --- |
| delegate | 用于指定回调代理，详情请参考 [RTCEngineIMDelegate](https://www.yuque.com/anyconf/rtcengine/mgx1kn004ra54ygw) |


### disableIm()
`- (void)disableIm`

停用即时通讯

当您不再需要即时通讯服务时，可通过该接口进行停用。

## 频道相关接口函数
### joinChannelWithToken:()
`- (RTCEngineError)joinChannelWithToken:(NSString *)token`

加入频道

RTC 的所有用户都需要加入频道才能“发布”或“订阅”音视频流，“发布”是指将自己的音频和视频推送到云端，“订阅”是指从云端拉取频道里其他用户的音视频流。

**参数**

| token | 鉴权令牌 |
| --- | --- |


**注意**

+ 请您尽量保证`joinChannelWithToken`与`leaveChannel`前后配对使用，即保证“先退出前一个频道再进入下一个频道”，否则会导致很多异常问题。

### leaveChannel:()
`- (void)leaveChannel:(nullable RTCEngineKitFinishBlock)finishBlock`  
离开频道

调用该接口会让用户离开自己所在的频道，并释放摄像头、麦克风、扬声器等设备资源。 等资源释放完毕之后，SDK 会通过`finishBlock`回调向您通知。 如果您要再次调用`joinChannelWithToken:()`，建议等待`finishBlock`回调到来之后再执行之后的操作，以避免摄像头或麦克风被占用等异常问题。

**参数**

| finishBlock | 完成回调 |
| --- | --- |


## 数据管理相关接口函数
### getMySelf()
`- (RTCEngineUserModel *)getMySelf`

获取当前账户信息

### getChannelDetails()
`- (RTCEngineChannelModel *)getChannelDetails`

获取当前频道数据

### findMemberWithUserId:()
`- (RTCEngineUserModel *)findMemberWithUserId:(NSString *)userId`

查找频道内`userId`的用户信息

### getRemoteUsers()
`- (NSArray<RTCEngineUserModel *> *)getRemoteUsers`

获取当前频道成员列表

### getDrawingHost()
`- (NSString *)getDrawingHost`

获取画板地址

## 视频相关接口函数
### startLocalPreview:view:()
`- (RTCEngineError)startLocalPreview:(BOOL)frontCamera view:(VIEW_CLASS *)view`

开启本地摄像头的预览画面

在`joinRoomWithRoomId`之前调用此函数，SDK 只会开启摄像头，并一直等到您调用`joinRoomWithRoomId`之后才开始推流。 在`joinRoomWithRoomId`之后调用此函数，SDK 会开启摄像头并自动开始视频推流。

**参数**

| frontCamera | YES-前置摄像头 NO-后置摄像头 |
| --- | --- |
| view | 承载视频画面的控件 |


### updateLocalView:()
`- (RTCEngineError)updateLocalView:(VIEW_CLASS *)view`  
更新本地摄像头的预览画面

### stopLocalPreview()
`- (RTCEngineError)stopLocalPreview`

停止摄像头预览

### publishLocalVideo:()
`- (RTCEngineError)publishLocalVideo:(BOOL)publish`

暂停/恢复发布本地的视频流

该接口可以暂停（或恢复）发布本地的视频画面，暂停之后，同一频道中的其他用户将无法继续看到自己画面。 该接口等效于`start/stopLocalPreview`这两个接口，但具有更好的响应速度。 因为`start/stopLocalPreview`需要打开和关闭摄像头，而打开和关闭摄像头都是硬件设备相关的操作，非常耗时。 相比之下，`publishLocalVideo`只需要在软件层面对数据流进行暂停或者放行即可，因此效率更高，也更适合需要频繁打开关闭的场景。 当暂停/恢复发布本地的视频流后，同一频道中的其他用户将会收到`onUserUpdate`回调通知。

**参数**

| publish | YES-恢复 NO-暂停 |
| --- | --- |


### switchCamera()
`- (RTCEngineError)switchCamera`

切换摄像头

### setCameraZoomRatio:()
`- (RTCEngineError)setCameraZoomRatio:(CGFloat)zoomRatio`

设置摄像头的缩放倍数

**参数**

| zoomRatio | 缩放系数，取值范围为：1.0~5.0 |
| --- | --- |


### setCameraFocusPosition:()
`- (RTCEngineError)setCameraFocusPosition:(CGPoint)position`

设置摄像头的对焦位置

**参数**

| position | 对焦位置 |
| --- | --- |


### setCameraExposureRatio:()
`- (RTCEngineError)setCameraExposureRatio:(CGFloat)exposureRatio`

设置摄像头的曝光系数

**参数**

| exposureRatio | 曝光系数，取值范围：-8.0~8.0 |
| --- | --- |


### enableCameraTorch:()
`- (RTCEngineError)enableCameraTorch:(BOOL)enabled`

设置闪光灯状态

**参数**

| enabled | YES-开启 NO-关闭 |
| --- | --- |


### startRemoteView:trackId:view:()
`- (RTCEngineError)startRemoteView:(NSString *)userId trackId:(RTCTrackIdentifierFlags)trackId view:(VIEW_CLASS *)view`

订阅远端用户的视频流，并绑定视频渲染控件

调用该接口可以让 SDK 拉取指定`userid`的视频流，并渲染到参数`view`指定的渲染控件上。

**参数**

| userId | 指定远端用户标识 |
| --- | --- |
| trackId | 指定要观看轨道标识，详情请参考 [RTCTrackIdentifierFlags](https://www.yuque.com/anyconf/rtcengine/yi50z7#QmrJ5) |
| view | 用于承载视频画面的渲染控件 |


### updateRemoteView:trackId:view:()
`- (RTCEngineError)updateRemoteView:(NSString *)userId trackId:(RTCTrackIdentifierFlags)trackId view:(VIEW_CLASS *)view`

更新远端用户的视频渲染控件

该接口可用于更新远端视频画面的渲染控件，常被用于切换显示区域的交互场景中。

**参数**

| userId | 指定远端用户标识 |
| --- | --- |
| trackId | 指定要观看轨道标识，详情请参考 [RTCTrackIdentifierFlags](https://www.yuque.com/anyconf/rtcengine/yi50z7#QmrJ5) |
| view | 用于承载视频画面的渲染控件 |


### stopRemoteView:trackId:()
`- (RTCEngineError)stopRemoteView:(NSString *)userId trackId:(RTCTrackIdentifierFlags)trackId`  
停止订阅远端用户的视频流，并释放渲染控件

调用此接口会让 SDK 停止接收该用户的视频流，并释放该路视频流的解码和渲染资源。

**参数**

| userId | 指定远端用户标识 |
| --- | --- |
| trackId | 指定要观看轨道标识，详情请参考 [RTCTrackIdentifierFlags](https://www.yuque.com/anyconf/rtcengine/yi50z7#QmrJ5) |


### stopAllRemoteViewWithUserId:()
`- (RTCEngineError)stopAllRemoteViewWithUserId:(NSString *)userId`  
停止订阅指定远端用户的所有视频流，并释放渲染控件

调用此接口会让 SDK 停止接收该用户的所有视频流，并释放该路视频流的解码和渲染资源。

**参数**

| userId | 指定远端用户标识 |
| --- | --- |


### stopAllRemoteView()
`- (RTCEngineError)stopAllRemoteView`

停止订阅所有远端用户的视频流，并释放全部渲染资源

调用此接口会让 SDK 停止接收所有来自远端的视频流，并释放全部的解码和渲染资源。

### startRemoteMixture:()
`- (RTCEngineError)startRemoteMixture:(VIEW_CLASS *)view`

订阅远端合成画面视频流，并绑定视频渲染控件

调用该接口可以让 SDK 拉取远端合成画面视频流，并渲染到参数`view`指定的渲染控件上。

**参数**

| view | 用于承载视频画面的渲染控件 |
| --- | --- |


### stopRemoteMixture()
`- (RTCEngineError)stopRemoteMixture`  
停止订阅远端合成画面视频流，并释放渲染控件

调用此接口会让 SDK 停止接收远端合成画面视频流，并释放该路视频流的解码和渲染资源。

## 视频渲染接口函数
### installRenderModule:authDataSize:logLevel:()
`- (RTCEngineError)installRenderModule:(char *)authData authDataSize:(int)authDataSize logLevel:(RTCEngineLogLevel)logLevel`

装载视频渲染组件

RTC 所有用户在使用 SDK 提供的美颜、滤镜等视频处理功能时，首先需要调用此函数加载视频渲染资源以及初始化视频渲染实例 。

**参数**

| authData | 密钥 |
| --- | --- |
| authDataSize | 密钥长度 |
| logLevel | 日志等级，详情请参考 [RTCEngineLogLevel](https://www.yuque.com/anyconf/rtcengine/yi50z7#KyTud) |


### uninstallRenderModule()
`- (void)uninstallRenderModule`

卸载视频渲染组件

视频渲染组件不再使用时，需要调用此方法释放视频渲染资源 。

### enabledBeauty:()
`- (RTCEngineError)enabledBeauty:(BOOL)enabled`

美颜功能开关

调用`installRenderModule:()`方法加载视频渲染组件之后，可以通过该方法设置视频美颜功能的开关 。

**参数**

| enabled | YES-开启美颜 NO-关闭美颜 |
| --- | --- |


### setBlurLevel:()
`- (void)setBlurLevel:(float)blurLevel`

设置磨皮等级

**参数**

| blurLevel | 磨皮等级，取值范围 0.0-1.0，默认0.5 |
| --- | --- |


### getBlurLevel()
`- (float)getBlurLevel`

获取当前磨皮等级

### setWhiteLevel:()
`- (void)setWhiteLevel:(float)whiteLevel`

设置美白等级

**参数**

| whiteLevel | 美白等级，取值范围 0.0-1.0，默认值0.3 |
| --- | --- |


### getWhiteLevel()
`- (float)getWhiteLevel`

获取当前美白等级

### setRedLevel:()
`- (void)setRedLevel:(float)redLevel`

设置红润等级

**参数**

| redLevel | 红润等级，取值范围 0.0-1.0，默认值0.3 |
| --- | --- |


### getRedLevel()
`- (float)getRedLevel`

获取当前红润等级

### setSharpenLevel:()
`- (void)setSharpenLevel:(float)sharpenLevel`

设置锐化等级

**参数**

| sharpenLevel | 锐化等级，取值范围 0.0-1.0，默认值0.3 |
| --- | --- |


### getSharpenLevel()
`- (float)getSharpenLevel`

获取当前锐化等级

### setFilterLevel:()
`- (void)setFilterLevel:(float)filterLevel`

设置滤镜等级

**参数**

| filterLevel | 滤镜等级，取值范围 0.0-1.0，默认值0.8 |
| --- | --- |


### getFilterLevel()
`- (float)getFilterLevel`

获取当前滤镜等级

### setFilterName:()
`- (void)setFilterName:(NSString *)filterName`

设置滤镜效果

**参数**

| filterName | 滤镜效果，默认值为 “origin” ，origin即为使用原图效果 |
| --- | --- |


### getFilterName()
`- (float)getFilterName`

获取当前滤镜效果

## 音频相关接口函数
### enabledSendAudio()
`- (RTCEngineError)enabledSendAudio:(BOOL)enabled`

暂停/恢复发布本地的音频流

**参数**

| enabled | YES-开启音频 NO-关闭音频 |
| --- | --- |


### setAudioPriorityWithUserId:enabled:()
`- (RTCEngineError)setAudioPriorityWithUserId:(NSString *)userId enabled:(BOOL)enabled`

设置音频优先策略

可通过该接口保证成员下行状态不佳时，优先保证音频的接收效果。

**参数**

| userId | 远端用户的ID |
| --- | --- |
| enabled | YES-开启 NO-关闭 |


### enabledAudioSpeaker:()
`- (RTCEngineError)enabledAudioSpeaker:(BOOL)enabled`

设置扬声器状态

可通过该接口设置扬声器设备是否静音。

**参数**

| enabled | YES-开启扬声器 NO-关闭扬声器 |
| --- | --- |


### enabledSpeechTrans:()
`- (RTCEngineError)enabledSpeechTrans:(BOOL)enabled`

设置语音转写状态

可通过该接口设置语音转写是否开启。

**参数**

| enabled | YES-开启语音转写 NO-关闭语音转写 |
| --- | --- |


### switchAudioRoute:()
`- (RTCEngineError)switchAudioRoute:(RTCAudioRoute)audioRoute`

切换音频路由

可通过该接口设置音频播放设备，如：扬声器、听筒等。

**参数**

| audioRoute | 音频路由枚举，详情请参考 [RTCAudioRoute](https://www.yuque.com/anyconf/rtcengine/yi50z7#fcHdd) |
| --- | --- |


### currentAudioRoute()
`- (RTCAudioRoute)currentAudioRoute`

获取当前音频路由

可通过该接口获取当前音频播放设备，如：扬声器、听筒等。

### headphoneDeviceAvailable()
`- (BOOL)headphoneDeviceAvailable`

判断是否存在有线耳机设备

可通过该接口判断是否存在有线耳机设备。

### bluetoothDeviceAvailable()
`- (BOOL)bluetoothDeviceAvailable`

判断是否存在蓝牙耳机设备

可通过该接口判断是否存在蓝牙耳机设备。

## 流媒体相关接口函数
### setStreamMediaConfig:()
`- (void)setStreamMediaConfig:(RTCEngineMediaConfig *)config`

设置流媒体配置参数

可通过该接口设置视频编码、音频编码、视频帧率、视频码流等参数。

**参数**

| config | 流媒体配置参数，用于指定视频编码、音频编码、视频帧率、视频码流等基本信息详情请参考 [RTCEngineMediaConfig](https://www.yuque.com/anyconf/rtcengine/yi50z7#pMzBp) |
| --- | --- |


### setNetworkQosParam:()
`- (void)setNetworkQosParam:(RTCEngineNetworkQosParam *)param`

设置网络质量控制参数

可通过该接口设置延迟自适应档位、延时抗抖动等级、码率自适应开关、网络自适应开关等参数。

**参数**

| param | 质量控制参数，用于指定延迟自适应档位、延时抗抖动等级、码率自适应开关、网络自适应开关等基本信息详情请参考 [RTCEngineNetworkQosParam](https://www.yuque.com/anyconf/rtcengine/yi50z7#rUmBV) |
| --- | --- |


### setRemoteDebugParam:()
`- (void)setRemoteDebugParam:(RTCEngineDebugParam *)param`

设置远程调试参数

可通过该接口设置远程调试地址、音视频流保存状态等调试参数。

**参数**

| param | 调试参数，用于指定远程调试地址、音视频流保存状态等调试基本信息详情请参考 [RTCEngineDebugParam](https://www.yuque.com/anyconf/rtcengine/yi50z7#tdyrN) |
| --- | --- |


## 共享屏幕相关接口函数
### broadcastStartedWithAppGroup:delegate:()
`- (void)broadcastStartedWithAppGroup:(NSString *)appGroup delegate:(id<RTCScreenDelegate>)delegate`

扩展程序开启屏幕共享，并绑定代理回调

此方法在扩展程序`SampleHandler`中使用

**参数**

| appGroup |  Application Group Identifier |
| --- | --- |
| delegate | 用于指定回调代理，详情请参考[屏幕录制](https://www.yuque.com/anyconf/rtcengine/tsm60n#.E5.AF.B9.E6.8E.A5.E6.B5.81.E7.A8.8B) |


### stopScreenRecord()
`- (void)stopScreenRecord`

宿主程序关闭屏幕共享

此方法在宿主程序中使用，用于用户主动关闭屏幕共享使用。

### sendSampleBuffer:withType:()
`- (void)sendSampleBuffer:(CMSampleBufferRef)sampleBuffer withType:(RPSampleBufferType)sampleBufferType`

扩展程序发送共享屏幕帧数据

此方法在扩展程序`SampleHandler`中使用

**参数**

| sampleBuffer | 屏幕帧数据 |
| --- | --- |
| sampleBufferType | 屏幕帧数据类型，包括：应用视频、应用音频、麦克风音频 |


## **发布自定义流相关接口**函数
### startCustomStreamWithStreamModel:()
`- (RTCEngineError)startCustomStreamWithStreamModel:(RTCEngineStreamModel *)streamModel`

启动自定义流，该接口需要指明发布的轨道、分辨率、码流等基础码流信息，需要注意的是：只有调用该接口申明的轨道才可以通过[发布自定义码流接口](#Jki7P)进行自定义推流，当程序结束自定义推流后需要调用[关闭自定义流接口](#P0Xlj)关闭对应轨道。

**参数**

| streamModel | 码流信息，用于指定轨道、分辨率、码流等码流基本信息详情请参考  [RTCEngineStreamModel](https://www.yuque.com/anyconf/rtcengine/yi50z7#o95yb) |
| --- | --- |


### stopCustomStreamWithTrackId:()
`- (RTCEngineError)stopCustomStreamWithTrackId:(RTCTrackIdentifierFlags)trackId`

关闭自定义流，该接口需要指明关闭的轨道标识，需要注意的是：当程序结束自定义推流时需要调用该方法关闭对应的轨道。

**参数**

| trackId | 轨道标识，详情请参考 [RTCTrackIdentifierFlags](https://www.yuque.com/anyconf/rtcengine/yi50z7#QmrJ5) |
| --- | --- |


### publishCustomStreamWithStreamData:()
`- (RTCEngineError)publishCustomStreamWithStreamData:(constunsignedchar *)streamData bitslen:(int)bitslen pts:(uint32_t)pts dts:(uint32_t)dts trackId:(RTCTrackIdentifierFlags)trackId mediaType:(RTCMediaType)mediaType`

发布自定义码流，可以通过该接口向[启动自定义流接口](#hly8D)中声明的轨道ID推送自定义码流数据。

**参数**

| streamData | 编码数据 |
| --- | --- |
| bitslen | 数据长度 |
| pts | 显示时间戳 |
| dts | 解码时间戳 |
| trackId | 轨道标识，详情请参考 [RTCTrackIdentifierFlags](https://www.yuque.com/anyconf/rtcengine/yi50z7#QmrJ5) |
| mediaType | 媒体类型，详情请参考 [RTCMediaType](https://www.yuque.com/anyconf/rtcengine/yi50z7#bFOsG) |


## 网络测速相关接口函数
### startSpeedTest:()
`- (RTCEngineError)startSpeedTest:(RTCSpeedTestParams *)params`

开始进行网速测试（加入频道前使用）

**参数**

| params | 测速参数，用于指定链路标识、服务器地址以及端口、监测时长等基本信息详情请参考 [RTCSpeedTestParams](https://www.yuque.com/anyconf/rtcengine/yi50z7#dMXCH) |
| --- | --- |


**注意**

+ 请在进入频道前进行网速测试，在频道中网速测试会影响正常的音视频传输效果，而且由于干扰过多，网速测试结果也不准确。
+ 同一时间只允许一项网速测试任务运行。

### stopSpeedTest()
`- (void)stopSpeedTest`

停止网络测速

