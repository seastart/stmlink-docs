## **连接相关回调**
### onImConnectSucceed:sessionId:()
`- (void)onImConnectSucceed:(NSString *)userId sessionId:(NSString *)sessionId`

连接成功回调

调用 `enableImWithDelegate:()` 接口执行启用即时通讯操作，当连接成功后，会收到该事件通知，如果遇到错误 SDK 会抛出 `onImDisconnected:errCode:errMsg:()` 回调。

**<font style="color:rgb(0, 0, 0);">参数</font>**

| userId | <font style="color:rgb(0, 0, 0);">用户标识</font> |
| --- | --- |
| sessionId | <font style="color:rgb(0, 0, 0);">会话标识</font> |


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

<font style="color:rgb(0, 0, 0);">连接断开事件或者被动断开连接回调</font>

<font style="color:rgb(0, 0, 0);">当断开原因为</font>`<font style="color:rgb(0, 0, 0);">SEAImDisconnectReasonError</font>`<font style="color:rgb(0, 0, 0);">时，表示 SDK 抛出的不可恢复的错误，比如鉴权失败等，此时需要重新获取鉴权令牌才可重新启用即时通讯服务。具体错误码参考文档：</font>[错误码表](https://www.yuque.com/anyconf/eanoso/zbbk63kiyugwavue)

当断开原因非`<font style="color:rgb(0, 0, 0);">SEAImDisconnectReasonError</font>`<font style="color:rgb(0, 0, 0);">时，表示被动断开连接。具体离开原因参考文档：</font>[断开原因](https://www.yuque.com/anyconf/eanoso/gkeau9oyh5vms80z#bTaTr)

**<font style="color:rgb(0, 0, 0);">参数</font>**

| reason | <font style="color:rgb(0, 0, 0);">断开原因</font> |
| --- | --- |
| errCode | <font style="color:rgb(0, 0, 0);">错误码</font> |
| errMsg | <font style="color:rgb(0, 0, 0);">错误信息</font> |


## **消息相关回调**
### onImMessage:action:userId:sessionId:nickname:()
`- (void)onImMessage:(NSString *)content action:(NSString *)action userId:(nullable NSString *)userId sessionId:(nullable NSString *)sessionId nickname:(nullable NSString *)nickname`

接收消息回调

应用层业务功能通过后台接口发送消息操作事件，SDK 会通过这个回调通知您。

**<font style="color:rgb(0, 0, 0);">参数</font>**

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

**<font style="color:rgb(0, 0, 0);">参数</font>**

| remindModel | 会议提醒内容，详情请参见 [SEAMeetingRemindModel](https://www.yuque.com/anyconf/eanoso/gkeau9oyh5vms80z#ScyOV) |
| --- | --- |


## **通话相关回调**
### onCallReceived:nickname:roomNo:title:()
`- (void)onCallReceived:(NSString *)callerId nickname:(nullable NSString *)nickname roomNo:(NSString *)roomNo title:(NSString *)title`

通话请求的回调

当主持人调用发起通话接口对您完成呼叫时，SDK 会通过这个回调通知您，您可以通过监听这个事件，来决定是否显示通话接听界面。。

**<font style="color:rgb(0, 0, 0);">参数</font>**

| callerId | 主叫标识 |
| --- | --- |
| nickname | 主叫昵称 |
| roomNo | 房间号码 |
| title | 会议标题 |


## **等候室相关回调**
### onWaitingRoomMoveInRoom:title:()
`- (void)onWaitingRoomMoveInRoom:(NSString *)meetingId title:(nullable NSString *)title`

被管理员从等候室移入会议室回调

当主持人调用将等候室人员移动到会议室时，SDK 会通过这个回调通知您，您可以通过监听这个事件，来决定是否立刻加入会议。

**<font style="color:rgb(0, 0, 0);">参数</font>**

| meetingId | 会议标识 |
| --- | --- |
| title | 会议标题 |


## **分组讨论相关回调**
### onSubMettingAskingHelp:meetingId:title:()
`- (void)onSubMettingAskingHelp:(NSString *)parentMid meetingId:(NSString *)meetingId title:(nullable NSString *)title`

小组会议请求帮助回调

当小组会议成员请求帮助时，SDK 会通过这个回调通知主会场管理员，您可以通过监听这个事件，来决定是否处理帮助请求。

**<font style="color:rgb(0, 0, 0);">参数</font>**

| parentMid | 上级会议标识 |
| --- | --- |
| meetingId | 小组会议标识 |
| title | 小组会议标题 |


