## **连接相关回调**
### onImConnectSucceed:sessionId:()
`- (void)onImConnectSucceed:(NSString *)userId sessionId:(NSString *)sessionId`

连接成功回调

调用 `enableImWithToken:()` 接口执行启用即时通讯操作，当连接成功后，会收到该事件通知，如果遇到错误 SDK 会抛出 `onImDisconnected:errCode:errMsg:()` 回调。

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
`- (void)onImDisconnected:(RTCImDisconnectReason)reason errCode:(RTCEngineError)errCode errMsg:(nullable NSString *)errMsg`

<font style="color:rgb(0, 0, 0);">连接断开事件或者被动断开连接回调</font>

<font style="color:rgb(0, 0, 0);">当断开原因为</font>`<font style="color:rgb(0, 0, 0);">RTCImDisconnectReasonError</font>`<font style="color:rgb(0, 0, 0);">时，表示 SDK 抛出的不可恢复的错误，比如鉴权失败等，此时需要重新获取鉴权令牌才可重新启用即时通讯服务。具体错误码参考文档：</font>[错误码表](https://www.yuque.com/anyconf/rtcengine/hf08uk#aP2yB)

当断开原因非`<font style="color:rgb(0, 0, 0);">RTCImDisconnectReasonError</font>`<font style="color:rgb(0, 0, 0);">时，表示被动断开连接。具体离开原因参考文档：</font>[断开原因](https://www.yuque.com/anyconf/rtcengine/yi50z7#jMnRV)

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




