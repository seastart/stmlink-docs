---
title: "RTCEngineKit"
description: "进程级引擎单例：初始化与销毁、频道实例的创建与查询、即时通讯、摄像头采集预览、音频路由、屏幕采集进程接入、网络测速与美颜渲染"
---

`RTCEngineKit` 是一个进程内只存在一个实例的单例对象，只承载**账号级与共享硬件级**能力：摄像头采集与预览、音频路由、ReplayKit 屏幕采集、美颜渲染、网络测速、即时通讯，以及频道实例的生命周期管理。

频道内的加入与离开、成员数据、码流发布与订阅、音频发送等能力由 [RTCEngineChannel](/zh/rtc/ios/api-reference/RTCEngineChannel) 承载，通过 `createChannelWithDelegate:` 创建。同一进程可以同时存在多个频道实例，实例之间的成员数据、码流统计与渲染互不干扰。

<Warning>
自 `3.0.0` 起，频道相关接口已从本类移出。`joinChannelWithToken:`、`leaveChannel:`、`publishLocalVideo:`、`startRemoteView:trackId:view:` 等接口请改用 [RTCEngineChannel](/zh/rtc/ios/api-reference/RTCEngineChannel)。
</Warning>

## 创建实例和事件回调
### delegate
`id<RTCEngineDelegate> delegate`

设置进程级引擎事件回调

您可以通过 [RTCEngineDelegate](/zh/rtc/ios/api-reference/RTCEngineDelegate) 获得音频路由变更、网络测速与应用性能三类进程级事件通知。频道内的事件请实现 [RTCEngineChannelDelegate](/zh/rtc/ios/api-reference/RTCEngineChannelDelegate)。

### imDelegate
`id<RTCEngineIMDelegate> imDelegate`

设置即时通讯事件回调，详情请参考 [RTCEngineIMDelegate](/zh/rtc/ios/api-reference/RTCEngineIMDelegate)。

### sharedEngine()
`+ (RTCEngineKit *)sharedEngine`

创建 RTCEngineKit 实例（单例模式）。

### sharedEngineWithConfig:appGroup:delegate:()
`+ (instancetype)sharedEngineWithConfig:(RTCEngineConfig *)engineConfig appGroup:(NSString *)appGroup delegate:(nullable id <RTCEngineDelegate>)delegate`

创建 RTCEngineKit 实例并同时完成初始化（单例模式）。

该接口等价于先调用 `sharedEngine()` 再调用 `initializeWithConfig:appGroup:delegate:()`，适合在业务层希望一步完成创建与初始化的场景。

**参数**

| engineConfig | 配置参数，用于日志等的相关配置，例如：日志等级等等信息，详情请参考 [RTCEngineConfig](/zh/rtc/ios/types#rtcengineconfig) |
| --- | --- |
| appGroup | Application Group Identifier |
| delegate | 用于指定回调代理，详情请参考 [RTCEngineDelegate](/zh/rtc/ios/api-reference/RTCEngineDelegate) |


### initializeWithConfig:appGroup:delegate:()
`- (RTCEngineError)initializeWithConfig:(RTCEngineConfig *)engineConfig appGroup:(NSString *)appGroup delegate:(nullable id <RTCEngineDelegate>)delegate`

初始化 RTCEngineKit 服务

RTC 的所有用户都需要初始化 RTCEngineKit 服务之后才可以使用相关的接口，包括创建频道实例、加入频道等。

**参数**

| engineConfig | 配置参数，用于日志等的相关配置，例如：日志等级等等信息，详情请参考 [RTCEngineConfig](/zh/rtc/ios/types#rtcengineconfig) |
| --- | --- |
| appGroup | Application Group Identifier |
| delegate | 用于指定回调代理，详情请参考 [RTCEngineDelegate](/zh/rtc/ios/api-reference/RTCEngineDelegate) |


### destroy()
`- (void)destroy`

销毁 RTCEngineKit 实例（单例模式）。

内部会先销毁全部存活的频道实例，等待其离开完成后再释放进程级资源，业务层无需逐个调用频道实例的 `destroy`。

### version()
`- (NSString *)version`

获取 RTCEngineKit 版本号。

### decrypt:()
`+ (nullable NSString *)decrypt:(nullable NSString *)value`

解密字符串

**参数**

| value | 加密字符串 |
| --- | --- |


## 频道实例相关接口函数
### createChannelWithDelegate:()
`- (nullable RTCEngineChannel *)createChannelWithDelegate:(nullable id<RTCEngineChannelDelegate>)delegate`

创建频道实例

每次调用返回一个独立的 [RTCEngineChannel](/zh/rtc/ios/api-reference/RTCEngineChannel) 实例，可以多次调用以同时加入多个频道。频道实例由引擎持有，业务侧使用完毕后需调用其 `destroy` 归还，否则实例不会被释放。

引擎正在销毁时返回 `nil`。

**参数**

| delegate | 频道事件代理，详情请参考 [RTCEngineChannelDelegate](/zh/rtc/ios/api-reference/RTCEngineChannelDelegate) |
| --- | --- |


### getChannels()
`- (NSArray<RTCEngineChannel *> *)getChannels`

获取活跃频道列表

返回当前已经加入频道的实例列表。已创建但尚未加入、或者已经离开的实例不会出现在结果中。

## 即时通讯相关接口函数
### enableImWithToken:delegate:()
`- (RTCEngineError)enableImWithToken:(NSString *)token delegate:(nullable id<RTCEngineIMDelegate>)delegate`

启用即时通讯

RTC 的所有用户如需使用即时通讯业务，首先调后台接口获取启用即时通讯的鉴权令牌，然后调用该接口开启 SDK 即时通讯服务，方便开发者利用该服务实现，如会前呼叫、通知等业务功能。

即时通讯属于账号级能力，与加入了几个频道无关。

**参数**

| token | 鉴权令牌 |
| --- | --- |
| delegate | 用于指定回调代理，详情请参考 [RTCEngineIMDelegate](/zh/rtc/ios/api-reference/RTCEngineIMDelegate) |


### disableIm()
`- (void)disableIm`

停用即时通讯

当您不再需要即时通讯服务时，可通过该接口进行停用。

## 视频相关接口函数

<Note>
摄像头在 iOS 上是单路共享硬件，采集与预览属进程级能力，全部频道实例共用同一路采集数据。是否把该路数据推送到某个频道，由该频道实例的 `publishLocalVideo:` 单独控制。
</Note>

### startLocalPreview:view:()
`- (RTCEngineError)startLocalPreview:(BOOL)frontCamera view:(VIEW_CLASS *)view`

开启本地摄像头的预览画面

在加入频道之前调用此函数，SDK 只会开启摄像头，并一直等到频道实例加入频道之后才开始推流。在加入频道之后调用此函数，SDK 会开启摄像头并自动开始视频推流。

自`2.5.7`起，如果`frontCamera`指定的摄像头无法创建输入或启动后未输出有效视频帧，SDK 会自动尝试另一可用摄像头。业务层无需通过额外调用`switchCamera`恢复预览；实际采集方向可通过`currentCameraDirection`获取。

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

### switchCamera()
`- (RTCEngineError)switchCamera`

切换摄像头

SDK 仅在目标摄像头能够创建输入时执行切换。目标摄像头不可用时保持当前实际采集设备，不会切换到无效输入。

### setLocalPreviewMirror:()
`- (RTCEngineError)setLocalPreviewMirror:(BOOL)mirror`

设置前置摄像头本地预览镜像偏好

仅作用于本地预览画面，不影响推流数据。前置摄像头按 `mirror` 取值设置镜像，后置摄像头始终不镜像；切换摄像头后 SDK 会自动应用对应策略。

**参数**

| mirror | YES-前置摄像头镜像 NO-前置摄像头不镜像 |
| --- | --- |


### currentCameraDirection()
`- (RTCEngineCameraDirection)currentCameraDirection`

获取当前摄像头方向

可通过该接口获取当前实际采集使用的摄像头方向。请求的摄像头不可用并发生自动回退时，该接口返回回退后设备的方向。返回值参考 [RTCEngineCameraDirection](/zh/rtc/ios/types#rtcenginecameradirection)。

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


## 音频路由相关接口函数

<Note>
音频路由对应进程内唯一的 `AVAudioSession`，属共享设备能力，切换结果对全部频道实例同时生效。
</Note>

### switchAudioRoute:()
`- (RTCEngineError)switchAudioRoute:(RTCAudioRoute)audioRoute`

切换音频路由

可通过该接口显式请求切换扬声器、听筒、蓝牙耳机或有线耳机。显式选择扬声器或听筒后，SDK 会优先保留该选择；未显式选择内置路由时，自`2.5.8`起，音频会话重配后 SDK 会主动恢复可用外设，同时存在蓝牙和有线耳机时优先使用蓝牙耳机。

接口返回成功表示系统调用已受理，最终实际路由以 `currentAudioRoute` 和 `onAudioRouteChange:previousRoute:` 回调为准。

**参数**

| audioRoute | 音频路由枚举，详情请参考 [RTCAudioRoute](/zh/rtc/ios/types#rtcaudioroute) |
| --- | --- |


### currentAudioRoute()
`- (RTCAudioRoute)currentAudioRoute`

获取系统当前实际音频路由

可通过该接口获取系统当前实际使用的音频播放设备，如扬声器、听筒、蓝牙或有线耳机。

### headphoneDeviceAvailable()
`- (BOOL)headphoneDeviceAvailable`

判断是否存在有线耳机设备

### bluetoothDeviceAvailable()
`- (BOOL)bluetoothDeviceAvailable`

判断是否存在蓝牙耳机设备

## 共享屏幕相关接口函数

<Note>
ReplayKit 采集运行在独立的 Broadcast Upload Extension 进程，属进程级共享能力，采集数据按订阅关系分发给各个频道实例。单个频道是否推送共享流，由该频道实例的 `publishScreenRecord:` 控制。
</Note>

### broadcastStartedWithAppGroup:delegate:()
`- (void)broadcastStartedWithAppGroup:(NSString *)appGroup delegate:(id<RTCScreenDelegate>)delegate`

扩展程序开启屏幕共享，并绑定代理回调

此方法在扩展程序`SampleHandler`中使用，详情请参考[屏幕录制](/zh/rtc/ios/advanced/screen-recording)。

**参数**

| appGroup | Application Group Identifier |
| --- | --- |
| delegate | 用于指定回调代理，详情请参考[屏幕录制](/zh/rtc/ios/advanced/screen-recording) |


### sendSampleBuffer:withType:()
`- (void)sendSampleBuffer:(CMSampleBufferRef)sampleBuffer withType:(RPSampleBufferType)sampleBufferType`

扩展程序发送共享屏幕帧数据

此方法在扩展程序`SampleHandler`中使用。当前支持 `RPSampleBufferTypeVideo` 与 `RPSampleBufferTypeAudioApp` 类型的数据帧，`RPSampleBufferTypeAudioMic` 不支持，麦克风采集数据请在宿主 App 中处理。

**参数**

| sampleBuffer | 屏幕帧数据 |
| --- | --- |
| sampleBufferType | 屏幕帧数据类型，包括：应用视频、应用音频、麦克风音频 |


### stopScreenRecord()
`- (void)stopScreenRecord`

宿主程序关闭屏幕共享

此方法在宿主程序中使用，会断开扩展端连接以结束本次系统录屏，并停止进程内全部频道实例的共享推流。采集服务在会中保持监听，用户仍可再次通过系统面板拉起屏幕录制。仅需停止单个频道推流时，请调用该频道实例的 `publishScreenRecord:` 并传入 `NO`。

## 网络测速相关接口函数
### startSpeedTest:()
`- (RTCEngineError)startSpeedTest:(RTCSpeedTestParams *)params`

开始进行网速测试（加入频道前使用）

**参数**

| params | 测速参数，用于指定链路标识、服务器地址以及端口、监测时长等基本信息，详情请参考 [RTCSpeedTestParams](/zh/rtc/ios/types#rtcspeedtestparams) |
| --- | --- |


**注意**

+ 请在进入频道前进行网速测试，在频道中网速测试会影响正常的音视频传输效果，而且由于干扰过多，网速测试结果也不准确。
+ 同一时间只允许一项网速测试任务运行。

### stopSpeedTest()
`- (void)stopSpeedTest`

停止网络测速

## 视频渲染接口函数

<Note>
视频渲染与美颜作用于共享摄像头采集链路，设置对全部频道实例同时生效。
</Note>

### installRenderModule:authDataSize:logLevel:()
`- (RTCEngineError)installRenderModule:(char *)authData authDataSize:(int)authDataSize logLevel:(RTCEngineLogLevel)logLevel`

装载视频渲染组件

RTC 所有用户在使用 SDK 提供的美颜、滤镜等视频处理功能时，首先需要调用此函数加载视频渲染资源以及初始化视频渲染实例。

**参数**

| authData | 密钥 |
| --- | --- |
| authDataSize | 密钥长度 |
| logLevel | 日志等级，详情请参考 [RTCEngineLogLevel](/zh/rtc/ios/types#rtcengineloglevel) |


### uninstallRenderModule()
`- (void)uninstallRenderModule`

卸载视频渲染组件

视频渲染组件不再使用时，需要调用此方法释放视频渲染资源。

### enabledBeauty:()
`- (RTCEngineError)enabledBeauty:(BOOL)enabled`

美颜功能开关

调用`installRenderModule:authDataSize:logLevel:()`方法加载视频渲染组件之后，可以通过该方法设置视频美颜功能的开关。

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
`- (NSString *)getFilterName`

获取当前滤镜效果
