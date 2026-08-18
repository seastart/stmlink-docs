---
title: "RTCEngineChannel"
description: "单频道实例：加入与离开频道、成员与频道数据查询、码流发布与订阅、音频发送、屏幕共享推送与自定义流"
---

`RTCEngineChannel` 表示一个独立的 RTC 频道，由 `-[RTCEngineKit createChannelWithDelegate:]` 创建。每个实例独立持有信令频道、媒体连接、成员缓存与远端渲染状态，同一进程可以同时存在多个实例，实例之间的成员数据、码流统计与渲染互不干扰。

摄像头、音频路由、ReplayKit 采集、美颜渲染等进程级共享能力由 [RTCEngineKit](/zh/rtc/ios/api-reference/RTCEngineKit) 单例统一提供，频道实例不重复暴露。

<Warning>
频道实例由引擎持有。使用完毕后必须调用 `destroy` 归还，否则引擎会一直持有该频道。
</Warning>

```objectivec
RTCEngineChannel *channel = [[RTCEngineKit sharedEngine] createChannelWithDelegate:self];
[channel joinChannelWithToken:@"Your Token"];
```

## 属性
### delegate
`id<RTCEngineChannelDelegate> delegate`

频道事件代理，详情请参考 [RTCEngineChannelDelegate](/zh/rtc/ios/api-reference/RTCEngineChannelDelegate)。

### channel
`NSString *channel`（只读）

已加入的频道名称，未加入时为空。

### enabledTrans
`BOOL enabledTrans`（只读）

语音转写状态。

## 频道相关接口函数
### joinChannelWithToken:()
`- (RTCEngineError)joinChannelWithToken:(NSString *)token`

加入频道

RTC 的所有用户都需要加入频道才能“发布”或“订阅”音视频流，“发布”是指将自己的音频和视频推送到云端，“订阅”是指从云端拉取频道里其他用户的音视频流。

**参数**

| token | 鉴权令牌 |
| --- | --- |


**注意**

+ 一个频道实例同一时间只能加入一个频道。需要同时加入多个频道时，请调用 `createChannelWithDelegate:` 创建多个实例，不要在同一实例上重复加入。
+ 同一实例上请保证`joinChannelWithToken`与`leaveChannel`前后配对使用，即保证“先退出前一个频道再进入下一个频道”，否则会导致很多异常问题。

### leaveChannel:()
`- (void)leaveChannel:(nullable RTCEngineKitFinishBlock)finishBlock`

离开频道

调用该接口会让用户离开该实例所在的频道，并释放该频道占用的媒体资源。等资源释放完毕之后，SDK 会通过`finishBlock`回调向您通知。如果您要再次调用`joinChannelWithToken:()`，建议等待`finishBlock`回调到来之后再执行之后的操作。

摄像头、麦克风等共享硬件由引擎统一管理，只有在最后一个频道离开后才会真正释放。

**参数**

| finishBlock | 完成回调 |
| --- | --- |


### destroy()
`- (void)destroy`

销毁频道实例

内部先执行离开频道，完成后从引擎的频道列表中摘除并断开代理。调用后不可再使用该实例，需要重新加入时请通过 `createChannelWithDelegate:` 创建新实例。

## 数据管理相关接口函数
### getMySelf()
`- (nullable RTCEngineUserModel *)getMySelf`

获取当前账户在该频道内的数据

### getChannelDetails()
`- (nullable RTCEngineChannelModel *)getChannelDetails`

获取当前频道数据

### findMemberWithUserId:()
`- (nullable RTCEngineUserModel *)findMemberWithUserId:(NSString *)userId`

查找该频道内`userId`的用户信息

<Note>
同一个 `userId` 可能同时存在于多个频道实例中。请使用事件来源频道实例查询，不要跨实例复用查询结果。
</Note>

**参数**

| userId | 用户标识 |
| --- | --- |


### getRemoteUsers()
`- (NSArray<RTCEngineUserModel *> *)getRemoteUsers`

获取该频道的成员列表

### getDrawingHost()
`- (nullable NSString *)getDrawingHost`

获取画板地址

## 视频相关接口函数
### publishLocalVideo:()
`- (RTCEngineError)publishLocalVideo:(BOOL)publish`

暂停/恢复发布本地的视频流

推送的画面来源为进程级共享摄像头，是否推送到本频道由当前实例独立控制。多频道场景下，某个频道暂停推流不会影响其它频道。

该接口只在软件层面对数据流进行暂停或者放行，不涉及摄像头硬件的开关，因此效率更高，也更适合需要频繁打开关闭的场景。当暂停/恢复发布本地的视频流后，同一频道中的其他用户将会收到`engineChannel:onRemoteUserUpdate:`回调通知。

**参数**

| publish | YES-恢复 NO-暂停 |
| --- | --- |


### startRemoteView:trackId:view:()
`- (RTCEngineError)startRemoteView:(NSString *)userId trackId:(RTCTrackIdentifierFlags)trackId view:(VIEW_CLASS *)view`

订阅远端用户的视频流，并绑定视频渲染控件

调用该接口可以让 SDK 拉取该频道内指定`userId`的视频流，并渲染到参数`view`指定的渲染控件上。

**参数**

| userId | 指定远端用户标识 |
| --- | --- |
| trackId | 指定要观看轨道标识，详情请参考 [RTCTrackIdentifierFlags](/zh/rtc/ios/types#rtctrackidentifierflags) |
| view | 用于承载视频画面的渲染控件 |


### updateRemoteView:trackId:view:()
`- (RTCEngineError)updateRemoteView:(NSString *)userId trackId:(RTCTrackIdentifierFlags)trackId view:(VIEW_CLASS *)view`

更新远端用户的视频渲染控件

该接口可用于更新远端视频画面的渲染控件，常被用于切换显示区域的交互场景中。

**参数**

| userId | 指定远端用户标识 |
| --- | --- |
| trackId | 指定要观看轨道标识，详情请参考 [RTCTrackIdentifierFlags](/zh/rtc/ios/types#rtctrackidentifierflags) |
| view | 用于承载视频画面的渲染控件 |


### stopRemoteView:trackId:()
`- (RTCEngineError)stopRemoteView:(NSString *)userId trackId:(RTCTrackIdentifierFlags)trackId`

停止订阅远端用户的视频流，并释放渲染控件

**参数**

| userId | 指定远端用户标识 |
| --- | --- |
| trackId | 指定要观看轨道标识，详情请参考 [RTCTrackIdentifierFlags](/zh/rtc/ios/types#rtctrackidentifierflags) |


### stopAllRemoteViewWithUserId:()
`- (RTCEngineError)stopAllRemoteViewWithUserId:(NSString *)userId`

停止订阅指定远端用户的所有视频流，并释放渲染控件

**参数**

| userId | 指定远端用户标识 |
| --- | --- |


### stopAllRemoteView()
`- (RTCEngineError)stopAllRemoteView`

停止订阅该频道内所有远端用户的视频流，并释放全部渲染资源

### startRemoteMixture:()
`- (RTCEngineError)startRemoteMixture:(VIEW_CLASS *)view`

订阅远端合成画面视频流，并绑定视频渲染控件

**参数**

| view | 用于承载视频画面的渲染控件 |
| --- | --- |


### stopRemoteMixture()
`- (RTCEngineError)stopRemoteMixture`

停止订阅远端合成画面视频流，并释放渲染控件

### startRemoteRetweet:view:()
`- (RTCEngineError)startRemoteRetweet:(NSString *)streamName view:(VIEW_CLASS *)view`

订阅远端转推音视频流（webrtc 取流），并绑定视频渲染控件

调用该接口可以让 SDK 通过 webrtc 订阅由外部传入流名的远端转推流，单条连接同时接收音视频，并将画面渲染到参数`view`指定的渲染控件上。该接口以原始流名作为流标识，转推流不作为远端用户视频数据上报，其接收状态通过 `engineChannel:onReceiveRetweetStreamStatusChange:status:` 单独通知。

> 注：转推取流目前仅支持 `wangsu` 流媒体供应商。

**参数**

| streamName | 需要订阅的远端流名（由外部传入，原值即流媒体服务器的流名） |
| --- | --- |
| view | 用于承载视频画面的渲染控件 |


### stopRemoteRetweet:()
`- (RTCEngineError)stopRemoteRetweet:(NSString *)streamName`

停止订阅远端转推音视频流，并释放渲染控件

**参数**

| streamName | 需要停止订阅的远端流名（由外部传入） |
| --- | --- |


## 流媒体相关接口函数
### setStreamMediaConfig:()
`- (void)setStreamMediaConfig:(RTCEngineMediaConfig *)config`

设置流媒体配置参数

可通过该接口设置视频编码、音频编码、视频帧率、视频码流等参数。配置作用于当前频道实例。

**参数**

| config | 流媒体配置参数，详情请参考 [RTCEngineMediaConfig](/zh/rtc/ios/types#rtcenginemediaconfig) |
| --- | --- |


### setNetworkQosParam:()
`- (void)setNetworkQosParam:(RTCEngineNetworkQosParam *)param`

设置网络质量控制参数

可通过该接口设置延迟自适应档位、延时抗抖动等级、码率自适应开关、网络自适应开关等参数。

**参数**

| param | 质量控制参数，详情请参考 [RTCEngineNetworkQosParam](/zh/rtc/ios/types#rtcenginenetworkqosparam) |
| --- | --- |


### setRemoteDebugParam:()
`- (void)setRemoteDebugParam:(RTCEngineDebugParam *)param`

设置远程调试参数

可通过该接口设置远程调试地址、音视频流保存状态等调试参数。

**参数**

| param | 调试参数，详情请参考 [RTCEngineDebugParam](/zh/rtc/ios/types#rtcenginedebugparam) |
| --- | --- |


## 音频相关接口函数
### enabledSendAudio:()
`- (RTCEngineError)enabledSendAudio:(BOOL)enabled`

暂停/恢复向该频道发布本地的音频流

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

设置远端音频播放状态

可通过该接口开启或关闭该频道的远端音频播放，不会切换扬声器、听筒或外设路由。音频输出设备的切换请使用 `-[RTCEngineKit switchAudioRoute:]`。

**参数**

| enabled | YES-开启远端音频播放 NO-关闭远端音频播放 |
| --- | --- |


### enabledAudioModule:()
`- (RTCEngineError)enabledAudioModule:(BOOL)enabled`

设置本端音频单元启停

自`2.5.9`起支持。录像直播等本端不采集、不接收 RTC 音频的纯本地播放场景，关闭音频单元可释放底层语音处理单元（VPIO），避免本地播放器（如 `AVPlayer`）的播放音量被压低；返回该类场景后需将其恢复为自动管理。SDK 每次加入频道会自动复位为自动管理，避免上一会话的手动停用状态跨会话泄漏。

**参数**

| enabled | YES-由流媒体自动管理音频单元 NO-停止音频单元 |
| --- | --- |


### enabledSpeechTrans:()
`- (RTCEngineError)enabledSpeechTrans:(BOOL)enabled`

设置语音转写状态

**参数**

| enabled | YES-开启语音转写 NO-关闭语音转写 |
| --- | --- |


### resetAudioSession()
`- (void)resetAudioSession`

重启音频会话

当 App 与其它音频应用抢占音频会话，或系统音频会话被外部打断后未能自动恢复时，业务层可调用该接口重建 SDK 的音频会话配置。调用后音频路由可能发生变化，SDK 会通过 [RTCEngineDelegate](/zh/rtc/ios/api-reference/RTCEngineDelegate) 的 `onAudioRouteChange:previousRoute:` 回调通知业务层。

## 共享屏幕相关接口函数
### publishScreenRecord:()
`- (RTCEngineError)publishScreenRecord:(BOOL)publish`

发布/停止该频道的屏幕共享流

自`3.0.0`起支持。ReplayKit 采集为进程级共享能力，本接口只控制当前频道实例是否推送采集数据。

自`3.0.1`起，采集服务在加入频道成功后即启动并保持监听，**业务层需在收到 `RTCEngineChannelDelegate` 的 `engineChannel:onScreenRecordStatus:` 上报 `RTCScreenRecordStatusStart` 之后再调用本接口发布**；最后一个发布的频道停止发布时，才会断开扩展端连接并结束本次系统录屏。

需要一次性结束本次系统录屏时，请调用 `-[RTCEngineKit stopScreenRecord]`。

**参数**

| publish | YES-发布 NO-停止 |
| --- | --- |


### publishScreenViewCaptureWithPixelBuffer:displayAngle:()
`- (void)publishScreenViewCaptureWithPixelBuffer:(CVPixelBufferRef)pixelBuffer displayAngle:(int)displayAngle`

发布视图录制的共享流，即用户可以通过该接口送入与屏幕共享共用轨道的视频流数据。

与 `publishCustomStreamWithStreamData:` 互斥使用，由外部业务决定采用哪种方式送流。

**参数**

| pixelBuffer | UIView采集的像素数据(CVPixelBufferRef) |
| --- | --- |
| displayAngle | 显示角度(0/90/180/270) |


### enabledViewCaptureShare:()
`- (RTCEngineError)enabledViewCaptureShare:(BOOL)enabled`

设置视图采集共享

该接口用来通知 SDK，当前共享屏幕轨道推送的是屏幕采集流还是视图录制流；在调用`publishScreenViewCaptureWithPixelBuffer:displayAngle:()`之前需先调该接口进行 SDK 标记。

视图采集为云录制的“保底画面源”，屏幕共享为“高优先级画面源”，两者共用屏幕共享通道并按优先级自动切换：

+ 开启时：若屏幕录制未进行，建立共享通道；若屏幕录制已在进行，通道已存在无需重复建立；
+ 屏幕录制停止时：若视图采集已开启，通道不关闭，自动恢复推送视图采集数据；
+ 关闭时：若屏幕录制未进行，拆除共享通道；若屏幕录制已在进行，通道保留给屏幕录制。

**参数**

| enabled | 启用状态 YES-开启 NO-关闭 |
| --- | --- |


## 发布自定义流相关接口
### startCustomStreamWithStreamTrackModel:()
`- (RTCEngineError)startCustomStreamWithStreamTrackModel:(RTCEngineStreamTrackModel *)streamTrackModel`

启动自定义流

该接口需要指明发布的轨道、分辨率、码流等基础码流信息。只有调用该接口申明的轨道才可以通过`publishCustomStreamWithStreamData:`进行自定义推流，当程序结束自定义推流后需要调用`stopCustomStreamWithTrackId:`关闭对应轨道。

**参数**

| streamTrackModel | 码流信息，详情请参考 [RTCEngineStreamTrackModel](/zh/rtc/ios/types#rtcenginestreamtrackmodel) |
| --- | --- |


### stopCustomStreamWithTrackId:()
`- (RTCEngineError)stopCustomStreamWithTrackId:(RTCTrackIdentifierFlags)trackId`

关闭自定义流

**参数**

| trackId | 轨道标识，详情请参考 [RTCTrackIdentifierFlags](/zh/rtc/ios/types#rtctrackidentifierflags) |
| --- | --- |


### publishCustomStreamWithStreamData:()
`- (RTCEngineError)publishCustomStreamWithStreamData:(const unsigned char *)streamData bitslen:(int)bitslen pts:(uint32_t)pts dts:(uint32_t)dts trackId:(RTCTrackIdentifierFlags)trackId streamType:(RTCStreamType)streamType`

发布自定义码流

可以通过该接口向`startCustomStreamWithStreamTrackModel:`中声明的轨道 ID 推送自定义码流数据。

**参数**

| streamData | 编码数据 |
| --- | --- |
| bitslen | 数据长度 |
| pts | 显示时间戳 |
| dts | 解码时间戳 |
| trackId | 轨道标识，详情请参考 [RTCTrackIdentifierFlags](/zh/rtc/ios/types#rtctrackidentifierflags) |
| streamType | 媒体流类型，详情请参考 [RTCStreamType](/zh/rtc/ios/types#rtcstreamtype) |
