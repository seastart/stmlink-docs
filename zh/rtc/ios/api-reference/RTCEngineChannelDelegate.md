---
title: "RTCEngineChannelDelegate"
description: "频道级会话事件回调协议：连接与重连、成员进出、自定义消息、音频状态、码流质量与屏幕共享，每个回调都带事件来源频道实例"
---

本协议承载频道内的连接、成员、消息、码流、音频与屏幕共享事件。**全部回调的首参都是事件来源的 [RTCEngineChannel](/zh/rtc/ios/api-reference/RTCEngineChannel) 实例**，多频道场景下通过首参区分事件归属，频道名称可从 `channel.channel` 读取。

进程级共享能力事件（音频路由、网络测速、应用性能）请实现 [RTCEngineDelegate](/zh/rtc/ios/api-reference/RTCEngineDelegate)。

```objectivec
@interface YourClass : NSObject <RTCEngineChannelDelegate>
```

<Note>
同一个 `userId` 可能同时出现在多个频道中。在回调里查询成员数据时，请使用首参传入的频道实例（如 `[channel findMemberWithUserId:userId]`），不要跨频道复用索引。
</Note>

## 连接相关回调
### engineChannelOnReconnecting:()
`- (void)engineChannelOnReconnecting:(RTCEngineChannel *)channel`

开始重连回调

该频道连接断开并开始重连时触发，如遇到错误 SDK 会抛出`engineChannel:onDisconnected:errCode:errMsg:()`回调。

**参数**

| channel | 事件来源频道实例 |
| --- | --- |


### engineChannelOnReconnected:()
`- (void)engineChannelOnReconnected:(RTCEngineChannel *)channel`

重连成功回调

断线重连成功后触发。

**参数**

| channel | 事件来源频道实例 |
| --- | --- |


### engineChannel:onDisconnected:errCode:errMsg:()
`- (void)engineChannel:(RTCEngineChannel *)channel onDisconnected:(RTCLeaveReason)reason errCode:(RTCEngineError)errCode errMsg:(nullable NSString *)errMsg`

连接断开事件或者被动离开频道回调

当离开原因为`RTCLeaveReasonError`时，表示 SDK 抛出的不可恢复的错误，比如加入频道失败等，此时需要重新获取鉴权令牌才可重新加入频道。具体错误码参考 [错误码表](/zh/rtc/ios/error-codes)。

当离开原因非`RTCLeaveReasonError`时，表示被动离开频道。具体离开原因参考 [RTCLeaveReason](/zh/rtc/ios/types#rtcleavereason)。

**参数**

| channel | 事件来源频道实例 |
| --- | --- |
| reason | 离开原因 |
| errCode | 错误码 |
| errMsg | 错误信息 |


## 我的相关回调
### engineChannel:onJoinSucceed:()
`- (void)engineChannel:(RTCEngineChannel *)channel onJoinSucceed:(NSString *)userId`

加入频道成功回调

调用频道实例的`joinChannelWithToken:()`接口执行加入频道操作后，会收到该回调；如遇到错误 SDK 会抛出`engineChannel:onDisconnected:errCode:errMsg:()`回调。

**参数**

| channel | 事件来源频道实例 |
| --- | --- |
| userId | 用户标识 |


### engineChannel:onUserUpdate:()
`- (void)engineChannel:(RTCEngineChannel *)channel onUserUpdate:(NSString *)userId`

自己数据更新回调

服务端修改当前用户数据操作后，会收到该回调，来通知当前用户在该频道内的数据发生了改变。

**参数**

| channel | 事件来源频道实例 |
| --- | --- |
| userId | 用户标识 |


## 频道相关回调
### engineChannel:onChannelUpdate:()
`- (void)engineChannel:(RTCEngineChannel *)channel onChannelUpdate:(NSString *)props`

频道更新回调

应用层调用服务接口执行变更频道信息操作后，会收到该回调。

**参数**

| channel | 事件来源频道实例 |
| --- | --- |
| props | 自定义数据 |


## 用户相关回调
### engineChannel:onRemoteUserJoinChannel:()
`- (void)engineChannel:(RTCEngineChannel *)channel onRemoteUserJoinChannel:(NSString *)userId`

用户加入频道回调，包括当前用户。

事件回调`engineChannel:onRemoteUserJoinChannel:`和`engineChannel:onRemoteUserLeaveChannel:reason:`只适用于维护该频道里的“用户列表”，有此事件回调不代表一定有视频画面，需要使用成员信息中的`streamTracks`来判断用户是否推流以及获取轨道号码等信息。

**参数**

| channel | 事件来源频道实例 |
| --- | --- |
| userId | 用户标识 |


### engineChannel:onRemoteUserUpdate:()
`- (void)engineChannel:(RTCEngineChannel *)channel onRemoteUserUpdate:(NSString *)userId`

当前频道有成员数据更新回调

**参数**

| channel | 事件来源频道实例 |
| --- | --- |
| userId | 用户标识 |


### engineChannel:onRemoteUserLeaveChannel:reason:()
`- (void)engineChannel:(RTCEngineChannel *)channel onRemoteUserLeaveChannel:(NSString *)userId reason:(RTCLeaveReason)reason`

用户离开频道回调，包括当前用户。

该回调与`engineChannel:onRemoteUserJoinChannel:`相对应。

**参数**

| channel | 事件来源频道实例 |
| --- | --- |
| userId | 用户标识 |
| reason | 离开原因，详情请参照 [RTCLeaveReason](/zh/rtc/ios/types#rtcleavereason) |


### engineChannel:onRemoteStreamTrackChange:streamTrackModel:changeType:()
`- (void)engineChannel:(RTCEngineChannel *)channel onRemoteStreamTrackChange:(NSString *)userId streamTrackModel:(RTCEngineStreamTrackModel *)streamTrackModel changeType:(RTCChangeType)changeType`

当前频道有用户码流数据变更回调

**参数**

| channel | 事件来源频道实例 |
| --- | --- |
| userId | 用户标识 |
| streamTrackModel | 码流轨道数据，详情请参见 [RTCEngineStreamTrackModel](/zh/rtc/ios/types#rtcenginestreamtrackmodel) |
| changeType | 操作类型，详情请参照 [RTCChangeType](/zh/rtc/ios/types#rtcchangetype) |


## 消息相关回调
### engineChannel:onCustomMessage:action:userId:sessionId:nickname:()
`- (void)engineChannel:(RTCEngineChannel *)channel onCustomMessage:(NSString *)content action:(NSString *)action userId:(nullable NSString *)userId sessionId:(nullable NSString *)sessionId nickname:(nullable NSString *)nickname`

自定义消息回调

应用层业务功能通过服务触发操作事件，SDK 会通过这个回调通知您。

**参数**

| channel | 事件来源频道实例 |
| --- | --- |
| content | 消息内容 |
| action | 消息标识 |
| userId | 用户标识 |
| sessionId | 会话标识 |
| nickname | 用户昵称 |


## 音频相关回调
### engineChannel:onAudioCapture:channels:stamp:dataSize:pcmData:()
`- (void)engineChannel:(RTCEngineChannel *)channel onAudioCapture:(int)samplerate channels:(int)channels stamp:(unsigned int)stamp dataSize:(int)dataSize pcmData:(void *)pcmData`

音频采集数据回调

SDK 采集到麦克风原始 PCM 数据后通过该回调抛出，业务层可用于本地录制、音频分析等场景。

注：该回调在音频采集线程中触发，请勿在回调中执行耗时操作，也不要持有 `pcmData` 指针，需要留用时请自行拷贝数据。

**参数**

| channel | 事件来源频道实例 |
| --- | --- |
| samplerate | 采样率 |
| channels | 声道数 |
| stamp | 时间戳 |
| dataSize | 数据大小 |
| pcmData | 音频元数据 |


### engineChannel:onAudioCaptureResampled:channels:stamp:resampledData:()
`- (void)engineChannel:(RTCEngineChannel *)channel onAudioCaptureResampled:(int)samplerate channels:(int)channels stamp:(unsigned int)stamp resampledData:(NSData *)resampledData`

音频采集重采样数据回调

与 `engineChannel:onAudioCapture:channels:stamp:dataSize:pcmData:()` 的区别在于数据已按 SDK 内部采样率转换，并以 `NSData` 形式给出，业务层无需自行管理内存。

注：该回调同样在音频采集线程中触发，请勿在回调中执行耗时操作。

**参数**

| channel | 事件来源频道实例 |
| --- | --- |
| samplerate | 采样率 |
| channels | 声道数 |
| stamp | 时间戳 |
| resampledData | 音频重采样数据 |


### engineChannel:onRemoteMemberAudioStatus:()
`- (void)engineChannel:(RTCEngineChannel *)channel onRemoteMemberAudioStatus:(NSArray<RTCStreamAudioModel *> *)audioArray`

远程成员音频状态回调

频道成员音频状态回调，包括：音频的分贝值、功率等信息，业务层可通过该回调统计音频数据进行语音激励操作。

**参数**

| channel | 事件来源频道实例 |
| --- | --- |
| audioArray | 成员音频数据列表，详情请参见 [RTCStreamAudioModel](/zh/rtc/ios/types#rtcstreamaudiomodel) |


### engineChannel:onServiceEnabledSpeak:()
`- (void)engineChannel:(RTCEngineChannel *)channel onServiceEnabledSpeak:(BOOL)enabled`

服务是否允许发言回调

**参数**

| channel | 事件来源频道实例 |
| --- | --- |
| enabled | 是否允许发言，YES-允许发言 NO-不允许发言 |


## 流媒体相关回调
### engineChannelOnStreamMediaDidConnectSucceed:()
`- (void)engineChannelOnStreamMediaDidConnectSucceed:(RTCEngineChannel *)channel`

流媒体连接成功回调

该频道的流媒体初次连接成功后，SDK 会通过该接口通知您。

**参数**

| channel | 事件来源频道实例 |
| --- | --- |


### engineChannel:onStreamChangedVendorName:()
`- (void)engineChannel:(RTCEngineChannel *)channel onStreamChangedVendorName:(NSString *)vendorName`

流媒体平台变化回调

当前频道使用的流媒体平台发生切换时，SDK 会通过该回调告知业务层当前生效的平台名称。

**参数**

| channel | 事件来源频道实例 |
| --- | --- |
| vendorName | 平台名称 |


### engineChannel:onDownBitrateAdaptiveUserId:state:()
`- (void)engineChannel:(RTCEngineChannel *)channel onDownBitrateAdaptiveUserId:(NSString *)userId state:(RTCDownBitrateAdaptiveState)state`

下行码率自适应状态回调

**参数**

| channel | 事件来源频道实例 |
| --- | --- |
| userId | 用户标识 |
| state | 下行码率自适应状态，详情请参考 [RTCDownBitrateAdaptiveState](/zh/rtc/ios/types#rtcdownbitrateadaptivestate) |


### engineChannel:onUploadBitrateAdaptiveState:()
`- (void)engineChannel:(RTCEngineChannel *)channel onUploadBitrateAdaptiveState:(RTCUploadBitrateAdaptiveState)state`

上行码率自适应状态回调

**参数**

| channel | 事件来源频道实例 |
| --- | --- |
| state | 上行码率自适应状态，详情请参考 [RTCUploadBitrateAdaptiveState](/zh/rtc/ios/types#rtcuploadbitrateadaptivestate) |


### engineChannel:onDownLossLevelChangeState:()
`- (void)engineChannel:(RTCEngineChannel *)channel onDownLossLevelChangeState:(RTCDownLossLevelState)state`

下行平均丢包档位变化回调

**参数**

| channel | 事件来源频道实例 |
| --- | --- |
| state | 下行平均丢包档位，详情请参考 [RTCDownLossLevelState](/zh/rtc/ios/types#rtcdownlosslevelstate) |


### engineChannel:onDownLossRateAverage:()
`- (void)engineChannel:(RTCEngineChannel *)channel onDownLossRateAverage:(CGFloat)average`

下行平均丢包率回调

**参数**

| channel | 事件来源频道实例 |
| --- | --- |
| average | 下行平均丢包率 |


### engineChannel:onSendStreamModel:()
`- (void)engineChannel:(RTCEngineChannel *)channel onSendStreamModel:(RTCStreamSendModel *)sendModel`

流媒体发送状态数据回调

会在固定时间间隔收到该回调，描述当前数据发送状态延迟、丢包率等信息。

**参数**

| channel | 事件来源频道实例 |
| --- | --- |
| sendModel | 发送状态数据，详情请参考 [RTCStreamSendModel](/zh/rtc/ios/types#rtcstreamsendmodel) |


### engineChannel:onReceiveStreamModel:()
`- (void)engineChannel:(RTCEngineChannel *)channel onReceiveStreamModel:(NSArray <RTCStreamReceiveModel *> *)receiveArray`

流媒体接收状态数据回调

会在固定时间间隔收到该回调，描述当前数据接收状态延迟、丢包率等信息。

**参数**

| channel | 事件来源频道实例 |
| --- | --- |
| receiveArray | 接收状态数据，详情请参考 [RTCStreamReceiveModel](/zh/rtc/ios/types#rtcstreamreceivemodel) |


### engineChannel:onSendQualitySample:()
`- (void)engineChannel:(RTCEngineChannel *)channel onSendQualitySample:(RTCStreamQualitySampleModel *)sample`

服务端上行质量检测回调

Seastart SFU 26.4 起，由服务端通过 Signal DataChannel 下发，含 score/level/mos 等服务端独有指标，作为本地 `engineChannel:onSendStreamModel:` 的补充。

**参数**

| channel | 事件来源频道实例 |
| --- | --- |
| sample | 上行质量样本，详情请参考 [RTCStreamQualitySampleModel](/zh/rtc/ios/types#rtcstreamqualitysamplemodel) |


### engineChannel:onReceiveQualitySample:()
`- (void)engineChannel:(RTCEngineChannel *)channel onReceiveQualitySample:(RTCStreamQualitySampleModel *)sample`

服务端下行质量检测回调

Seastart SFU 26.4 起，由服务端通过 Signal DataChannel 下发，为整体下行的聚合样本，与 `engineChannel:onReceiveStreamModel:` 的 per-stream 维度互补。

**参数**

| channel | 事件来源频道实例 |
| --- | --- |
| sample | 下行质量样本，详情请参考 [RTCStreamQualitySampleModel](/zh/rtc/ios/types#rtcstreamqualitysamplemodel) |


### engineChannel:onReceiveStreamStatusChange:trackId:status:()
`- (void)engineChannel:(RTCEngineChannel *)channel onReceiveStreamStatusChange:(NSString *)userId trackId:(RTCTrackIdentifierFlags)trackId status:(BOOL)status`

流媒体接收远端流状态变更回调

订阅成员远程视频流后，如果持续一段时间没有收到该成员的视频流，会收到该回调。同时，接收视频流恢复后也会收到该回调。

**参数**

| channel | 事件来源频道实例 |
| --- | --- |
| userId | 用户标识 |
| trackId | 轨道标识，详情请参考 [RTCTrackIdentifierFlags](/zh/rtc/ios/types#rtctrackidentifierflags) |
| status | 接收状态，YES-超时 NO-恢复 |


### engineChannel:onReceiveRetweetStreamStatusChange:status:()
`- (void)engineChannel:(RTCEngineChannel *)channel onReceiveRetweetStreamStatusChange:(NSString *)streamName status:(BOOL)status`

流媒体接收转推流状态变更回调

订阅远端转推流后，如果持续一段时间没有收到该转推流的画面，会收到该回调。转推流不作为远端用户视频数据上报，其接收状态通过本回调单独通知。

**参数**

| channel | 事件来源频道实例 |
| --- | --- |
| streamName | 转推流名 |
| status | 接收状态，YES-超时 NO-恢复 |


## 屏幕共享相关回调
### engineChannel:onScreenRecordStatus:()
`- (void)engineChannel:(RTCEngineChannel *)channel onScreenRecordStatus:(RTCScreenRecordStatus)status`

屏幕共享状态回调

调用频道实例的`publishScreenRecord:()`接口执行开启屏幕共享操作后，SDK 会通过该回调通知宿主程序当前的屏幕共享状态。

**参数**

| channel | 事件来源频道实例 |
| --- | --- |
| status | 屏幕共享状态码，详情请参考 [RTCScreenRecordStatus](/zh/rtc/ios/types#rtcscreenrecordstatus) |
