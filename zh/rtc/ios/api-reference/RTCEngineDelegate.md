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

<font style="color:rgb(0, 0, 0);">连连接断开事件或者被动离开频道回调</font>

<font style="color:rgb(0, 0, 0);">当离开原因为</font>`<font style="color:rgb(0, 0, 0);">RTCLeaveReasonError</font>`<font style="color:rgb(0, 0, 0);">时，表示 SDK 抛出的不可恢复的错误，比如加入频道失败等，此时需要重新获取鉴权令牌才可重新加入频道。具体错误码参考文档：</font>[错误码表](https://www.yuque.com/anyconf/rtcengine/hf08uk#aP2yB)

当离开原因非`<font style="color:rgb(0, 0, 0);">RTCLeaveReasonError</font>`<font style="color:rgb(0, 0, 0);">时，表示被动离开频道。具体离开原因参考文档：</font>[离开原因](https://www.yuque.com/anyconf/rtcengine/yi50z7#WgkRO)

**<font style="color:rgb(0, 0, 0);">参数</font>**

| reason | <font style="color:rgb(0, 0, 0);">离开原因</font> |
| --- | --- |
| errCode | <font style="color:rgb(0, 0, 0);">错误码</font> |
| errMsg | <font style="color:rgb(0, 0, 0);">错误信息</font> |


## **消息相关回调**
### onCustomMessage:action:userId:sessionId:nickname:()
`- (void)onCustomMessage:(NSString *)content action:(NSString *)action userId:(nullable NSString *)userId sessionId:(nullable NSString *)sessionId nickname:(nullable NSString *)nickname`

自定义消息回调

应用层业务功能通过服务出发操作事件，SDK 会通过这个回调通知您。

**<font style="color:rgb(0, 0, 0);">参数</font>**

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

<font style="color:rgb(0, 0, 0);">调用</font>`RTCEngineKit`<font style="color:rgb(0, 0, 0);">中的</font>`joinChannelWithToken:<font style="color:rgb(0, 0, 0);">()</font>`<font style="color:rgb(0, 0, 0);">接口执行加入频道操作后，会收到来自</font>`RTCEngineDelegate`<font style="color:rgb(0, 0, 0);">的</font>`onJoinSucceed:userId:()`<font style="color:rgb(0, 0, 0);">回调，</font>如遇到错误 SDK 会抛出`onDisconnected:errCode:errMsg:()`回调。

**<font style="color:rgb(0, 0, 0);">参数</font>**

| channel | 频道名称 |
| --- | --- |
| userId | 用户标识 |


### onUserUpdate:userId:()
`- (void)onUserUpdate:(NSString *)channel userId:(NSString *)userId`

自己数据更新回调

<font style="color:rgb(0, 0, 0);">服务端修改当前用户</font>数据<font style="color:rgb(0, 0, 0);">操作后，会收到来自</font>`RTCEngineDelegate`<font style="color:rgb(0, 0, 0);">的</font>`onUserUpdate:userId:()`<font style="color:rgb(0, 0, 0);">回调，来通知当前用户数据发生了改变。</font>

**<font style="color:rgb(0, 0, 0);">参数</font>**

| channel | 频道名称 |
| --- | --- |
| userId | 用户标识 |


## **频道相关回调**
### onChannelUpdate:props:()
`- (void)onChannelUpdate:(NSString *)channel props:(NSString *)props`

频道更新回调

<font style="color:rgb(0, 0, 0);">应用层调用服务接口执行</font>变更频道信息<font style="color:rgb(0, 0, 0);">操作后，会收到来自</font>`RTCEngineDelegate`<font style="color:rgb(0, 0, 0);">的</font>`onChannelUpdate:props:()`<font style="color:rgb(0, 0, 0);">回调。</font>

**<font style="color:rgb(0, 0, 0);">参数</font>**

| channel | 频道名称 |
| --- | --- |
| props | 自定义数据 |


## **用户相关回调**
### onRemoteUserJoinChannel:userId:()
`- (void)onRemoteUserJoinChannel:(NSString *)channel userId:(NSString *)userId`

有用户加入频道回调

<font style="color:rgb(0, 0, 0);">事件回调</font>`<font style="color:rgb(0, 0, 0);">onRemoteUserJoinChannel:</font>`<font style="color:rgb(0, 0, 0);">和</font>`<font style="color:rgb(0, 0, 0);">onRemoteUserLeaveChannel:</font>`<font style="color:rgb(0, 0, 0);">只适用于维护当前频道里的“用户列表”，有此事件回调不代表一定有视频画面，需要使用成员信息中的</font>`streamTracks`<font style="color:rgb(0, 0, 0);">来判断用户是否推流以及获取轨道号码等信息。</font>

**<font style="color:rgb(0, 0, 0);">参数</font>**

| channel | 频道名称 |
| --- | --- |
| userId | 用户标识 |


### onRemoteUserUpdate:userId:()
`- (void)onRemoteUserUpdate:(NSString *)channel userId:(NSString *)userId`

当前频道有成员数据更新回调

<font style="color:rgb(0, 0, 0);">业务层通过服务端接口执行</font>变更用户数据<font style="color:rgb(0, 0, 0);">操作后，会收到来自</font>`RTCEngineDelegate`<font style="color:rgb(0, 0, 0);">的</font>`onRemoteUserUpdate:userId:()`<font style="color:rgb(0, 0, 0);">回调。</font>

**<font style="color:rgb(0, 0, 0);">参数</font>**

| channel | 频道名称 |
| --- | --- |
| userId | 用户标识 |


### onRemoteUserLeaveChannel:userId:reason:()
`- (void)onRemoteUserLeaveChannel:(NSString *)channel userId:(NSString *)userId reason:(RTCLeaveChannelReason)reason`

有用户离开频道回调

<font style="color:rgb(0, 0, 0);">该回调与</font>`<font style="color:rgb(0, 0, 0);">onRemoteUserJoinChannel</font>`<font style="color:rgb(0, 0, 0);">相对应。</font>

**<font style="color:rgb(0, 0, 0);">参数</font>**

| channel | 频道名称 |
| --- | --- |
| userId | 用户标识 |
| reason | 离开原因，详情请参照 [RTCLeaveChannelReason](https://www.yuque.com/anyconf/rtcengine/yi50z7#zGDtN) |


### onRemoteStreamTrackChange:userId:streamTrackModel:changeType:()
`- (void)onRemoteStreamTrackChange:(NSString *)channel userId:(NSString *)userId streamTrackModel:(RTCEngineStreamTrackModel *)streamTrackModel changeType:(RTCChangeType)changeType`

当前频道有用户码流数据变更回调

<font style="color:rgb(0, 0, 0);">频道中用户变更自己的码流数据，SDK 会通过该接口通知您。</font>

**<font style="color:rgb(0, 0, 0);">参数</font>**

| channel | 频道名称 |
| --- | --- |
| userId | 用户标识 |
| streamTrackModel | 码流轨道数据，详情请参见 [RTCEngineStreamTrackModel](https://www.yuque.com/anyconf/rtcengine/yi50z7#o95yb) |
| changeType | 操作类型，详情请参照 [RTCChangeType](https://www.yuque.com/anyconf/rtcengine/yi50z7#SsAoS) |


## 音频相关回调
### onAudioRouteChange:previousRoute:
`- (void)onAudioRouteChange:(RTCAudioRoute)route previousRoute:(RTCAudioRoute)previousRoute`

音频路由变更回调

<font style="color:rgb(0, 0, 0);">音频路由发生变化时，SDK 会通过</font>`onAudioRouteChange:previousRoute:`<font style="color:rgb(0, 0, 0);">调用通知业务层。</font>

**<font style="color:rgb(0, 0, 0);">参数</font>**

| route | 音频路由，详情请参照 [RTCAudioRoute](https://www.yuque.com/anyconf/rtcengine/yi50z7#fcHdd) |
| --- | --- |
| previousRoute | 变更前的音频路由 |


### onRemoteMemberAudioStatus:()
`- (void)onRemoteMemberAudioStatus:(NSArray<RTCStreamAudioModel *> *)audioArray`

远程成员音频状态回调

<font style="color:rgb(0, 0, 0);">频道成员音频状态回调，包括：音频的分贝值、功率等信息，业务层可通过该回调统计音频数据进行语音激励操作。</font>

**<font style="color:rgb(0, 0, 0);">参数</font>**

| audioArray | 成员音频数据列表，详情请参见 [RTCStreamAudioModel](https://www.yuque.com/anyconf/rtcengine/yi50z7#zj1s4) |
| --- | --- |


### onServiceEnabledSpeak:()
`- (void)onServiceEnabledSpeak:(BOOL)enabled`

服务是否允许发言回调

**<font style="color:rgb(0, 0, 0);">参数</font>**

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

**<font style="color:rgb(0, 0, 0);">参数</font>**

| userId | 用户标识 |
| --- | --- |
| state | 下行码率自适应状态，<font style="color:rgb(0, 0, 0);">详情请参考 </font>[RTCDownBitrateAdaptiveState](https://www.yuque.com/anyconf/rtcengine/yi50z7#hHKyj) |


### onUploadBitrateAdaptiveState:()
`- (void)onUploadBitrateAdaptiveState:(RTCUploadBitrateAdaptiveState)state`

上行码率自适应状态回调

开启码率自适应后，SDK 会根据网络情况动态调整上行链路的码率自适应等级。

**<font style="color:rgb(0, 0, 0);">参数</font>**

| state | 上行码率自适应状态，<font style="color:rgb(0, 0, 0);">详情请参考 </font>[RTCUploadBitrateAdaptiveState](https://www.yuque.com/anyconf/rtcengine/yi50z7#ZryAr) |
| --- | --- |


### onDownLossLevelChangeState:()
`- (void)onDownLossLevelChangeState:(RTCDownLossLevelState)state`

下行平均丢包档位变化回调

**<font style="color:rgb(0, 0, 0);">参数</font>**

| state | 下行平均丢包档位，<font style="color:rgb(0, 0, 0);">详情请参考 </font>[RTCDownLossLevelState](https://www.yuque.com/anyconf/rtcengine/yi50z7#yMw23) |
| --- | --- |


### onDownLossRateAverage:()
`- (void)onDownLossRateAverage:(CGFloat)average`

下行平均丢包率回调

**<font style="color:rgb(0, 0, 0);">参数</font>**

| average | 下行平均丢包率 |
| --- | --- |


### onSendStreamModel:()
`- (void)onSendStreamModel:(RTCStreamSendModel *)sendModel`

流媒体发送状态数据回调

会在固定时间间隔，<font style="color:rgb(0, 0, 0);">会收到来自</font>`RTCEngineDelegate`<font style="color:rgb(0, 0, 0);">的</font>`onSendStreamModel:()`<font style="color:rgb(0, 0, 0);">回调，描述当前数据发送状态延迟、丢包率等信息。</font>

**<font style="color:rgb(0, 0, 0);">参数</font>**

| sendModel | 发送状态数据，<font style="color:rgb(0, 0, 0);">内容包含：延迟、丢包率等基本信息详情请参考 </font>[RTCStreamSendModel](https://www.yuque.com/anyconf/rtcengine/yi50z7#tSKwL) |
| --- | --- |


### onReceiveStreamModel:()
`- (void)onReceiveStreamModel:(NSArray <RTCStreamReceiveModel *> *)receiveArray`

流媒体接收状态数据回调

会在固定时间间隔，<font style="color:rgb(0, 0, 0);">会收到来自</font>`RTCEngineDelegate`<font style="color:rgb(0, 0, 0);">的</font>`onReceiveStreamModel:()`<font style="color:rgb(0, 0, 0);">回调，描述当前数据接收状态延迟、丢包率等信息。</font>

**<font style="color:rgb(0, 0, 0);">参数</font>**

| receiveModel | 接收状态数据，<font style="color:rgb(0, 0, 0);">内容包含：延迟、丢包率等基本信息详情请参考 </font>[RTCStreamReceiveModel](https://www.yuque.com/anyconf/rtcengine/yi50z7#d6fij) |
| --- | --- |


### onReceiveStreamStatusChange:trackId:status:()
`- (void)onReceiveStreamStatusChange:(NSString *)userId trackId:(RTCTrackIdentifierFlags)trackId status:(BOOL)status`

流媒体接收远端流状态变更回调

订阅成员远程视频流后，如果持续一段时间没有收到该成员的视频流，<font style="color:rgb(0, 0, 0);">会收到来自</font>`RTCEngineDelegate`<font style="color:rgb(0, 0, 0);">的</font>`onReceiveStreamStatusChange:status:()`<font style="color:rgb(0, 0, 0);">回调。同时，接收视频流恢复后也会收到该回调。</font>

**<font style="color:rgb(0, 0, 0);">参数</font>**

| userId | 用户标识 |
| --- | --- |
| trackId | 轨道标识，，<font style="color:rgb(0, 0, 0);">详情请参考 </font>[RTCTrackIdentifierFlags](https://www.yuque.com/anyconf/rtcengine/yi50z7#QmrJ5) |
| status | 接收状态，YES-超时 NO-恢复 |


## **屏幕共享相关回调**
### onScreenRecordStatus:()
`- (void)onScreenRecordStatus:(RTCScreenRecordStatus)status`

屏幕共享状态回调

<font style="color:rgb(0, 0, 0);">扩展程序调用</font>`RTCEngineKit`<font style="color:rgb(0, 0, 0);">中的</font>`startScreenRecordingClient:<font style="color:rgb(0, 0, 0);">()</font>`<font style="color:rgb(0, 0, 0);">接口执行开启屏幕共享操作后， SDK 会通过</font>`RTCEngineDelegate`<font style="color:rgb(0, 0, 0);">的</font>`onScreenRecordStatus:()`<font style="color:rgb(0, 0, 0);">回调通知宿主程序当前的屏幕共享状态。</font>

**<font style="color:rgb(0, 0, 0);">参数</font>**

| status | 屏幕共享状态码，<font style="color:rgb(0, 0, 0);">详情请参考 </font>[RTCScreenRecordStatus](https://www.yuque.com/anyconf/rtcengine/yi50z7#JwIlf) |
| --- | --- |


## 网络测速相关回调
### onSpeedTestBegined()
`- (void)onSpeedTestBegined`

网络测速开始回调

<font style="color:rgb(0, 0, 0);">调用</font>`RTCEngineKit`<font style="color:rgb(0, 0, 0);">中的</font>`startSpeedTest:<font style="color:rgb(0, 0, 0);">()</font>`<font style="color:rgb(0, 0, 0);">接口执行</font>开始网络测速<font style="color:rgb(0, 0, 0);">操作后，会收到来自</font>`RTCEngineDelegate`<font style="color:rgb(0, 0, 0);">的</font>`onSpeedTestBegined()`<font style="color:rgb(0, 0, 0);">回调。</font>

### onSpeedTestUploadResult:downResult:connectResult:()
`- (void)onSpeedTestUploadResult:(nullable RTCSpeedTestResult *)uploadResult downResult:(nullable RTCSpeedTestResult *)downResult connectResult:(nullable RTCSpeedTestConnectResult *)connectResult`

网络测速的结果回调

<font style="color:rgb(0, 0, 0);">调用</font>`RTCEngineKit`<font style="color:rgb(0, 0, 0);">中的</font>`startSpeedTest:<font style="color:rgb(0, 0, 0);">()</font>`<font style="color:rgb(0, 0, 0);">接口执行</font>开始网络测速<font style="color:rgb(0, 0, 0);">操作后，底层监测完成之后会收到来自</font>`RTCEngineDelegate`<font style="color:rgb(0, 0, 0);">的</font>`onSpeedTestUploadResult:downResult:connectResult:()`<font style="color:rgb(0, 0, 0);">回调。</font>

**<font style="color:rgb(0, 0, 0);">参数</font>**

| uploadResult | 上行网速测试结果，<font style="color:rgb(0, 0, 0);">详情请参考 </font>[RTCSpeedTestResult](https://www.yuque.com/anyconf/rtcengine/yi50z7#ApYUD) |
| --- | --- |
| downResult | 下行网速测试结果，<font style="color:rgb(0, 0, 0);">详情请参考 </font>[RTCSpeedTestResult](https://www.yuque.com/anyconf/rtcengine/yi50z7#ApYUD) |
| connectResult | 连接情况测试结果，<font style="color:rgb(0, 0, 0);">详情请参考 </font>[RTCSpeedTestConnectResult](https://www.yuque.com/anyconf/rtcengine/yi50z7#I9DK2) |


## **其它相关回调**
### onApplicationPerformance:cpuUsage:()
`- (void)onApplicationPerformance:(CGFloat)memory cpuUsage:(CGFloat)cpuUsage`

应用性能使用情况回调

<font style="color:rgb(0, 0, 0);">频道内当前性能使用情况回调。</font>

**<font style="color:rgb(0, 0, 0);">参数</font>**

| memory | 内存使用情况 |
| --- | --- |
| cpuUsage | CUP使用率 |


