---
title: "RTCEngineDelegate"
description: "iOS SRTC 音视频 SDK RTCEngineDelegate 接口参考"
---

## **连接相关回调**
### onReconnecting()
`- (void)onReconnecting`

开始重连回调

连接断开并开始重连时触发，如遇到错误 SDK 会抛出`onDisconnected:errCode:errMsg:()`回调

### onReconnected()
`- (void)onReconnected`

重连成功回调

断线重连成功后触发，如遇到错误 SDK 会抛出`onDisconnected:errCode:errMsg:()`回调

### onDisconnected:errCode:errMsg:()
`- (void)onDisconnected:(RTCLeaveReason)reason errCode:(RTCEngineError)errCode errMsg:(nullable NSString *)errMsg`

连连接断开事件或者被动离开频道回调

当离开原因为`RTCLeaveReasonError`时，表示 SDK 抛出的不可恢复的错误，比如加入频道失败等，此时需要重新获取鉴权令牌才可重新加入频道。具体错误码参考文档：[错误码表](https://www.yuque.com/anyconf/rtcengine/hf08uk#aP2yB)

当离开原因非`RTCLeaveReasonError`时，表示被动离开频道。具体离开原因参考文档：[离开原因](https://www.yuque.com/anyconf/rtcengine/yi50z7#WgkRO)

**参数**

| reason | 离开原因 |
| --- | --- |
| errCode | 错误码 |
| errMsg | 错误信息 |


## **消息相关回调**
### onCustomMessage:action:userId:sessionId:nickname:()
`- (void)onCustomMessage:(NSString *)content action:(NSString *)action userId:(nullable NSString *)userId sessionId:(nullable NSString *)sessionId nickname:(nullable NSString *)nickname`

自定义消息回调

应用层业务功能通过服务出发操作事件，SDK 会通过这个回调通知您。

**参数**

| content | 消息内容 |
| --- | --- |
| action | 消息标识 |
| userId | 用户标识 |
| sessionId | 会话标识 |
| nickname | 用户昵称 |


## **我的相关回调**
### onJoinSucceed:userId:()
`- (void)onJoinSucceed:(NSString *)channel userId:(NSString *)userId`

加入频道成功回调

调用`RTCEngineKit`中的`joinChannelWithToken:()`接口执行加入频道操作后，会收到来自`RTCEngineDelegate`的`onJoinSucceed:userId:()`回调，如遇到错误 SDK 会抛出`onDisconnected:errCode:errMsg:()`回调。

**参数**

| channel | 频道名称 |
| --- | --- |
| userId | 用户标识 |


### onUserUpdate:userId:()
`- (void)onUserUpdate:(NSString *)channel userId:(NSString *)userId`

自己数据更新回调

服务端修改当前用户数据操作后，会收到来自`RTCEngineDelegate`的`onUserUpdate:userId:()`回调，来通知当前用户数据发生了改变。

**参数**

| channel | 频道名称 |
| --- | --- |
| userId | 用户标识 |


## **频道相关回调**
### onChannelUpdate:props:()
`- (void)onChannelUpdate:(NSString *)channel props:(NSString *)props`

频道更新回调

应用层调用服务接口执行变更频道信息操作后，会收到来自`RTCEngineDelegate`的`onChannelUpdate:props:()`回调。

**参数**

| channel | 频道名称 |
| --- | --- |
| props | 自定义数据 |


## **用户相关回调**
### onRemoteUserJoinChannel:userId:()
`- (void)onRemoteUserJoinChannel:(NSString *)channel userId:(NSString *)userId`

用户加入频道回调，包括当前用户。

事件回调`onRemoteUserJoinChannel:`和`onRemoteUserLeaveChannel:`只适用于维护当前频道里的“用户列表”，有此事件回调不代表一定有视频画面，需要使用成员信息中的`streamTracks`来判断用户是否推流以及获取轨道号码等信息。

**参数**

| channel | 频道名称 |
| --- | --- |
| userId | 用户标识 |


### onRemoteUserUpdate:userId:()
`- (void)onRemoteUserUpdate:(NSString *)channel userId:(NSString *)userId`

当前频道有成员数据更新回调

业务层通过服务端接口执行变更用户数据操作后，会收到来自`RTCEngineDelegate`的`onRemoteUserUpdate:userId:()`回调。

**参数**

| channel | 频道名称 |
| --- | --- |
| userId | 用户标识 |


### onRemoteUserLeaveChannel:userId:reason:()
`- (void)onRemoteUserLeaveChannel:(NSString *)channel userId:(NSString *)userId reason:(RTCLeaveChannelReason)reason`

用户离开频道回调，包括当前用户。

该回调与`onRemoteUserJoinChannel`相对应。

**参数**

| channel | 频道名称 |
| --- | --- |
| userId | 用户标识 |
| reason | 离开原因，详情请参照 [RTCLeaveChannelReason](https://www.yuque.com/anyconf/rtcengine/yi50z7#zGDtN) |


### onRemoteStreamTrackChange:userId:streamTrackModel:changeType:()
`- (void)onRemoteStreamTrackChange:(NSString *)channel userId:(NSString *)userId streamTrackModel:(RTCEngineStreamTrackModel *)streamTrackModel changeType:(RTCChangeType)changeType`

当前频道有用户码流数据变更回调

频道中用户变更自己的码流数据，SDK 会通过该接口通知您。

**参数**

| channel | 频道名称 |
| --- | --- |
| userId | 用户标识 |
| streamTrackModel | 码流轨道数据，详情请参见 [RTCEngineStreamTrackModel](https://www.yuque.com/anyconf/rtcengine/yi50z7#o95yb) |
| changeType | 操作类型，详情请参照 [RTCChangeType](https://www.yuque.com/anyconf/rtcengine/yi50z7#SsAoS) |


## 音频相关回调
### onAudioRouteChange:previousRoute:
`- (void)onAudioRouteChange:(RTCAudioRoute)route previousRoute:(RTCAudioRoute)previousRoute`

音频路由变更回调

音频路由发生变化时，SDK 会通过`onAudioRouteChange:previousRoute:`调用通知业务层。

自`2.5.8`起，未显式选择扬声器或听筒且存在可用外设时，SDK 会先恢复外设；恢复成功后，不会上报音频会话重配期间短暂出现的扬声器或听筒路由，业务层收到的是最终实际路由。

**参数**

| route | 音频路由，详情请参照 [RTCAudioRoute](https://www.yuque.com/anyconf/rtcengine/yi50z7#fcHdd) |
| --- | --- |
| previousRoute | 变更前的音频路由 |


### onRemoteMemberAudioStatus:()
`- (void)onRemoteMemberAudioStatus:(NSArray<RTCStreamAudioModel *> *)audioArray`

远程成员音频状态回调

频道成员音频状态回调，包括：音频的分贝值、功率等信息，业务层可通过该回调统计音频数据进行语音激励操作。

**参数**

| audioArray | 成员音频数据列表，详情请参见 [RTCStreamAudioModel](https://www.yuque.com/anyconf/rtcengine/yi50z7#zj1s4) |
| --- | --- |


### onServiceEnabledSpeak:()
`- (void)onServiceEnabledSpeak:(BOOL)enabled`

服务是否允许发言回调

**参数**

| enabled | 是否允许发言，YES-允许发言 NO-不允许发言 |
| --- | --- |


## **流媒体相关回调**
### onStreamMediaDidConnectSucceed()
`- (void)onStreamMediaDidConnectSucceed`

流媒体连接成功回调

流媒体初次连接成功后，SDK 会通过该接口通知您。

### onDownBitrateAdaptiveUserId:state:()
`- (void)onDownBitrateAdaptiveUserId:(NSString *)userId state:(RTCDownBitrateAdaptiveState)state`

下行码率自适应状态回调

开启码率自适应后，SDK 会根据网络情况动态调整下行成员链路的码率自适应等级。

**参数**

| userId | 用户标识 |
| --- | --- |
| state | 下行码率自适应状态，详情请参考 [RTCDownBitrateAdaptiveState](https://www.yuque.com/anyconf/rtcengine/yi50z7#hHKyj) |


### onUploadBitrateAdaptiveState:()
`- (void)onUploadBitrateAdaptiveState:(RTCUploadBitrateAdaptiveState)state`

上行码率自适应状态回调

开启码率自适应后，SDK 会根据网络情况动态调整上行链路的码率自适应等级。

**参数**

| state | 上行码率自适应状态，详情请参考 [RTCUploadBitrateAdaptiveState](https://www.yuque.com/anyconf/rtcengine/yi50z7#ZryAr) |
| --- | --- |


### onDownLossLevelChangeState:()
`- (void)onDownLossLevelChangeState:(RTCDownLossLevelState)state`

下行平均丢包档位变化回调

**参数**

| state | 下行平均丢包档位，详情请参考 [RTCDownLossLevelState](https://www.yuque.com/anyconf/rtcengine/yi50z7#yMw23) |
| --- | --- |


### onDownLossRateAverage:()
`- (void)onDownLossRateAverage:(CGFloat)average`

下行平均丢包率回调

**参数**

| average | 下行平均丢包率 |
| --- | --- |


### onSendStreamModel:()
`- (void)onSendStreamModel:(RTCStreamSendModel *)sendModel`

流媒体发送状态数据回调

会在固定时间间隔，会收到来自`RTCEngineDelegate`的`onSendStreamModel:()`回调，描述当前数据发送状态延迟、丢包率等信息。

**参数**

| sendModel | 发送状态数据，内容包含：延迟、丢包率等基本信息详情请参考 [RTCStreamSendModel](https://www.yuque.com/anyconf/rtcengine/yi50z7#tSKwL) |
| --- | --- |


### onReceiveStreamModel:()
`- (void)onReceiveStreamModel:(NSArray <RTCStreamReceiveModel *> *)receiveArray`

流媒体接收状态数据回调

会在固定时间间隔，会收到来自`RTCEngineDelegate`的`onReceiveStreamModel:()`回调，描述当前数据接收状态延迟、丢包率等信息。

**参数**

| receiveModel | 接收状态数据，内容包含：延迟、丢包率等基本信息详情请参考 [RTCStreamReceiveModel](https://www.yuque.com/anyconf/rtcengine/yi50z7#d6fij) |
| --- | --- |


### onSendQualitySample:()
`- (void)onSendQualitySample:(RTCStreamQualitySampleModel *)sample`

服务端上行质量检测回调

会在固定时间间隔，会收到来自`RTCEngineDelegate`的`onSendQualitySample:()`回调，描述当前数据发送状态延迟、丢包率等信息。

**参数**

| sample | 发送状态数据，内容包含：延迟、丢包率等基本信息详情请参考 [RTCStreamQualitySampleModel]() |
| --- | --- |


### onReceiveQualitySample:()
`- (void)onReceiveQualitySample:(RTCStreamQualitySampleModel *)sample`

服务端下行质量检测回调

会在固定时间间隔，会收到来自`RTCEngineDelegate`的`onReceiveQualitySample:()`回调，描述当前数据接收状态延迟、丢包率等信息。

**参数**

| sample | 接收状态数据，内容包含：延迟、丢包率等基本信息详情请参考 [RTCStreamQualitySampleModel]() |
| --- | --- |


### onReceiveStreamStatusChange:trackId:status:()
`- (void)onReceiveStreamStatusChange:(NSString *)userId trackId:(RTCTrackIdentifierFlags)trackId status:(BOOL)status`

流媒体接收远端流状态变更回调

订阅成员远程视频流后，如果持续一段时间没有收到该成员的视频流，会收到来自`RTCEngineDelegate`的`onReceiveStreamStatusChange:status:()`回调。同时，接收视频流恢复后也会收到该回调。

**参数**

| userId | 用户标识 |
| --- | --- |
| trackId | 轨道标识，，详情请参考 [RTCTrackIdentifierFlags](https://www.yuque.com/anyconf/rtcengine/yi50z7#QmrJ5) |
| status | 接收状态，YES-超时 NO-恢复 |


### onReceiveRetweetStreamStatusChange:status:()
`- (void)onReceiveRetweetStreamStatusChange:(NSString *)streamName status:(BOOL)status`

流媒体接收转推流状态变更回调

订阅远端转推流后，如果持续一段时间没有收到该转推流的画面，会收到来自`RTCEngineDelegate`的`onReceiveRetweetStreamStatusChange:status:()`回调。同时，接收画面恢复后也会收到该回调。转推流不作为远端用户视频数据上报，其接收状态通过本回调单独通知。

**参数**

| streamName | 转推流名 |
| --- | --- |
| status | 接收状态，YES-超时 NO-恢复 |


## **屏幕共享相关回调**
### onScreenRecordStatus:()
`- (void)onScreenRecordStatus:(RTCScreenRecordStatus)status`

屏幕共享状态回调

扩展程序调用`RTCEngineKit`中的`startScreenRecordingClient:()`接口执行开启屏幕共享操作后， SDK 会通过`RTCEngineDelegate`的`onScreenRecordStatus:()`回调通知宿主程序当前的屏幕共享状态。

**参数**

| status | 屏幕共享状态码，详情请参考 [RTCScreenRecordStatus](https://www.yuque.com/anyconf/rtcengine/yi50z7#JwIlf) |
| --- | --- |


## 网络测速相关回调
### onSpeedTestBegined()
`- (void)onSpeedTestBegined`

网络测速开始回调

调用`RTCEngineKit`中的`startSpeedTest:()`接口执行开始网络测速操作后，会收到来自`RTCEngineDelegate`的`onSpeedTestBegined()`回调。

### onSpeedTestUploadResult:downResult:connectResult:()
`- (void)onSpeedTestUploadResult:(nullable RTCSpeedTestResult *)uploadResult downResult:(nullable RTCSpeedTestResult *)downResult connectResult:(nullable RTCSpeedTestConnectResult *)connectResult`

网络测速的结果回调

调用`RTCEngineKit`中的`startSpeedTest:()`接口执行开始网络测速操作后，底层监测完成之后会收到来自`RTCEngineDelegate`的`onSpeedTestUploadResult:downResult:connectResult:()`回调。

**参数**

| uploadResult | 上行网速测试结果，详情请参考 [RTCSpeedTestResult](https://www.yuque.com/anyconf/rtcengine/yi50z7#ApYUD) |
| --- | --- |
| downResult | 下行网速测试结果，详情请参考 [RTCSpeedTestResult](https://www.yuque.com/anyconf/rtcengine/yi50z7#ApYUD) |
| connectResult | 连接情况测试结果，详情请参考 [RTCSpeedTestConnectResult](https://www.yuque.com/anyconf/rtcengine/yi50z7#I9DK2) |


## **其它相关回调**
### onApplicationPerformance:cpuUsage:()
`- (void)onApplicationPerformance:(CGFloat)memory cpuUsage:(CGFloat)cpuUsage`

应用性能使用情况回调

频道内当前性能使用情况回调。

**参数**

| memory | 内存使用情况 |
| --- | --- |
| cpuUsage | CUP使用率 |
