---
title: "MeetingKitIMDelegate"
description: "会议外消息通道的回调协议：连接状态、来电呼叫、会议提醒、等候室移入、子会议求助"
---

## 连接相关回调
### onImConnectSucceed:sessionId:()
`- (void)onImConnectSucceed:(NSString *)userId sessionId:(NSString *)sessionId`

连接成功回调

调用 `enableImWithDelegate:()` 接口执行启用即时通讯操作，当连接成功后，会收到该事件通知，如果遇到错误 SDK 会抛出 `onImDisconnected:errCode:errMsg:()` 回调。

**参数**

| userId | 用户标识 |
| --- | --- |
| sessionId | 会话标识 |


### onImReconnecting()
`- (void)onImReconnecting`

开始重连回调

连接断开并开始重连时触发，如果遇到错误 SDK 会抛出 `onImDisconnected:errCode:errMsg:()` 回调。

### onImReconnected()
`- (void)onImReconnected`

重连成功回调

断线重连成功后触发，如果遇到错误 SDK 会抛出 `onImDisconnected:errCode:errMsg:()` 回调。

### onImDisconnected:errCode:errMsg:()
`- (void)onImDisconnected:(SEAImDisconnectReason)reason errCode:(SEAError)errCode errMsg:(nullable NSString *)errMsg`

连接断开事件或者被动断开连接回调

当断开原因为`SEAImDisconnectReasonError`时，表示 SDK 抛出的不可恢复的错误，比如鉴权失败等，此时需要重新获取鉴权令牌才可重新启用即时通讯服务。具体错误码参考文档：[错误码表](/zh/meeting/ios/error-codes)

当断开原因非`SEAImDisconnectReasonError`时，表示被动断开连接。具体离开原因参考文档：[断开原因](/zh/meeting/ios/types#seaimdisconnectreason)

**参数**

| reason | 断开原因 |
| --- | --- |
| errCode | 错误码 |
| errMsg | 错误信息 |


## 消息相关回调
### onImMessage:action:userId:sessionId:nickname:()
`- (void)onImMessage:(NSString *)content action:(NSString *)action userId:(nullable NSString *)userId sessionId:(nullable NSString *)sessionId nickname:(nullable NSString *)nickname`

接收消息回调

应用层业务功能通过后台接口发送消息操作事件，SDK 会通过这个回调通知您。

**参数**

| content | 消息内容 |
| --- | --- |
| action | 消息标识 |
| userId | 用户标识 |
| sessionId | 会话标识 |
| nickname | 用户昵称 |


### onMeetingRemind:()
`- (void)onMeetingRemind:(SEAMeetingRemindModel *)remindModel`

会议即将开始回调

当您需要参与的预约会议即将开始时，SDK 会通过这个回调通知您。

**参数**

| remindModel | 会议提醒内容，详情请参见 [SEAMeetingRemindModel](/zh/meeting/ios/types#seameetingremindmodel) |
| --- | --- |


## 通话相关回调
### onCallReceived:nickname:roomNo:title:()
`- (void)onCallReceived:(NSString *)callerId nickname:(nullable NSString *)nickname roomNo:(NSString *)roomNo title:(NSString *)title`

通话请求的回调

当主持人调用发起通话接口对您完成呼叫时，SDK 会通过这个回调通知您，您可以通过监听这个事件，来决定是否显示通话接听界面。

**参数**

| callerId | 主叫标识 |
| --- | --- |
| nickname | 主叫昵称 |
| roomNo | 房间号码 |
| title | 会议标题 |

<Note>
实现了下方带 `meetingId` / `forceJoin` 的 `onCallReceived:nickname:roomNo:title:meetingId:forceJoin:()` 后，SDK 不再回调本方法。
</Note>

### onCallReceived:nickname:roomNo:title:meetingId:forceJoin:()
`- (void)onCallReceived:(NSString *)callerId nickname:(nullable NSString *)nickname roomNo:(NSString *)roomNo title:(NSString *)title meetingId:(nullable NSString *)meetingId forceJoin:(BOOL)forceJoin`

通话请求的回调（含会议标识与强制入会标记），2.5.0 起提供。

与 `onCallReceived:nickname:roomNo:title:()` 时机相同，多带会议标识 `meetingId` 与强制入会标记 `forceJoin`。实现本方法后不再回调旧方法。

`forceJoin` 对应服务端 [呼叫成员](/zh/meeting/server-api/meet-admin#会议时呼叫人员入会) 接口的 `force_join` 参数，缺省为 `NO`。为 `YES` 表示管理员要求被叫直接入会，建议：

+ 不弹接听界面，提示一句后直接进入目标会议；已在该会议中则忽略
+ 正在其它会议中时，先离开当前会议（只退出自己，不结束会议）再进入
+ 短时间内重复收到同一会议的强制呼叫只处理第一次
+ 应用在后台时 iOS 无法自动切到前台，可发本地通知，用户点通知或回到前台后再入会

被叫凭这次呼叫进入密码会议免密（服务端处理），等候室、锁定等规则照旧。

**参数**

| callerId | 主叫标识 |
| --- | --- |
| nickname | 主叫昵称 |
| roomNo | 房间号码 |
| title | 会议标题 |
| meetingId | 会议标识 |
| forceJoin | 是否强制入会，缺省为 `NO` |


## 等候室相关回调
### onWaitingRoomMoveInRoom:title:()
`- (void)onWaitingRoomMoveInRoom:(NSString *)meetingId title:(nullable NSString *)title`

被管理员从等候室移入会议室回调

当主持人调用将等候室人员移动到会议室时，SDK 会通过这个回调通知您，您可以通过监听这个事件，来决定是否立刻加入会议。

**参数**

| meetingId | 会议标识 |
| --- | --- |
| title | 会议标题 |


## 分组讨论相关回调
### onSubMettingAskingHelp:meetingId:title:()
`- (void)onSubMettingAskingHelp:(NSString *)parentMid meetingId:(NSString *)meetingId title:(nullable NSString *)title`

小组会议请求帮助回调

当小组会议成员请求帮助时，SDK 会通过这个回调通知主会场管理员，您可以通过监听这个事件，来决定是否处理帮助请求。

**参数**

| parentMid | 上级会议标识 |
| --- | --- |
| meetingId | 小组会议标识 |
| title | 小组会议标题 |


