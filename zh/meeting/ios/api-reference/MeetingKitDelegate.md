## **错误事件回调**
### onError:errMsg:()
`- (void)onError:(SEAError)errCode errMsg:(nullable NSString *)errMsg`

<font style="color:rgb(0, 0, 0);">错误事件回调</font>

<font style="color:rgb(0, 0, 0);">表示 SDK 发生不可恢复的错误，比如：加入房间失败或设备开启失败等。这个事件触发一般需要获取新的令牌重新入会。</font>

<font style="color:rgb(0, 0, 0);">参考文档：</font>[错误码表](https://www.yuque.com/anyconf/eanoso/zbbk63kiyugwavue)

| <font style="color:#8A8F8D;">参数</font> | <font style="color:#8A8F8D;">描述</font> |
| --- | --- |
| errCode | 错误码 |
| errMsg | 错误信息 |


## **连接事件回调**
### onReconnecting()
`- (void)onReconnecting`

<font style="color:rgb(0, 0, 0);">开始重连事件回调</font>

<font style="color:rgb(0, 0, 0);">表示 SDK 连接发生异常，正在尝试重连，如：网络抖动等。如中途遇到错误 SDK 会抛出 </font>`<font style="color:rgb(0, 0, 0);">onError:errMsg:()</font>`<font style="color:rgb(0, 0, 0);"> 回调。</font>

### <font style="color:rgb(0, 0, 0);">onReconnected()</font>
`<font style="color:rgb(0, 0, 0);">- (void)onReconnected</font>`

<font style="color:rgb(0, 0, 0);">重连成功事件回调</font>

<font style="color:rgb(0, 0, 0);">当 SDK 断线重连成功并且连接已经恢复时，会收到该事件通知。如中途遇到错误 SDK 会抛出 </font>`<font style="color:rgb(0, 0, 0);">onError:errMsg:()</font>`<font style="color:rgb(0, 0, 0);"> 回调。</font>

## **我的相关回调**
### <font style="color:rgb(0, 0, 0);">onEnterRoom:userId:()</font>
`<font style="color:rgb(0, 0, 0);">- (void)onEnterRoom:(NSString *)meetingId userId:(NSString *)userId</font>`

<font style="color:rgb(0, 0, 0);">进入房间事件回调</font>

<font style="color:rgb(0, 0, 0);">调用 </font>MeetingKit <font style="color:rgb(0, 0, 0);">中的 </font>`<font style="color:rgb(0, 0, 0);">enterRoom:onSuccess:onFailed:()</font>`<font style="color:rgb(0, 0, 0);"> 接口执行进入房间操作后，会收到来自</font>`MeetingKitDelegate` <font style="color:rgb(0, 0, 0);">的 </font>`onEnterRoom:userId:()` <font style="color:rgb(0, 0, 0);">回调，如遇到错误 SDK 会通过方法中 </font>`<font style="color:rgb(0, 0, 0);">onFailed</font>`<font style="color:rgb(0, 0, 0);"> 参数返回</font>。

| <font style="color:#8A8F8D;">参数</font> | <font style="color:#8A8F8D;">描述</font> |
| --- | --- |
| <font style="color:rgb(0, 0, 0);">meetingId</font> | <font style="color:rgb(0, 0, 0);">会议标识</font> |
| <font style="color:rgb(0, 0, 0);">userId</font> | <font style="color:rgb(0, 0, 0);">用户标识</font> |


### <font style="color:rgb(0, 0, 0);">onExitRoom:()</font>
`<font style="color:rgb(0, 0, 0);">- (void)onExitRoom:(SEALeaveReason)reason</font>`

<font style="color:rgb(0, 0, 0);">离开房间事件回调</font>

<font style="color:rgb(0, 0, 0);">当前用户非主动离开时，会收到该事件通知，如：被主持人踢出房间、会议解散等。</font>

> 值得注意的是，调用 MeetingKit 中的 `exitRoom: `接口会执行退出房间的相关逻辑，例如释放音视频设备资源和编解码器资源等。待 SDK 占用的所有资源释放完毕后，SDK 会通过方法携带的 `onSuccess` 参数抛出，你可以在此返回中执行“离开界面”等操作。此时，不会再收到 `onExitRoom()` 事件通知。
>

| <font style="color:#8A8F8D;">参数</font> | <font style="color:#8A8F8D;">描述</font> |
| :--- | --- |
| <font style="color:rgb(0, 0, 0);">reason</font> | <font style="color:rgb(0, 0, 0);">离开原因，参考文档：</font>[SEALeaveReason](https://www.yuque.com/anyconf/eanoso/gkeau9oyh5vms80z#bbLNp) |


### <font style="color:rgb(0, 0, 0);">onRequestOpenCamera:()</font>
`<font style="color:rgb(0, 0, 0);">- (void)onRequestOpenCamera:(NSString *)userId</font>`

<font style="color:rgb(0, 0, 0);">请求开启摄像头回调</font>

<font style="color:rgb(0, 0, 0);">当主持人调用 MeetingKit 中的 </font>`<font style="color:rgb(0, 0, 0);">adminRequestUserOpenCamera:onSuccess:onFailed:()</font>`<font style="color:rgb(0, 0, 0);"> 接口执行请求打开你的摄像头操作后，SDK 会抛出该事件通知您。</font>

| <font style="color:#8A8F8D;">参数</font> | <font style="color:#8A8F8D;">描述</font> |
| :--- | --- |
| <font style="color:rgb(0, 0, 0);">userId</font> | 请求者标识 |


### <font style="color:rgb(0, 0, 0);">onRequestOpenMic:()</font>
`<font style="color:rgb(0, 0, 0);">- (void)onRequestOpenMic:(NSString *)userId</font>`

<font style="color:rgb(0, 0, 0);">请求开启麦克风回调</font>

<font style="color:rgb(0, 0, 0);">当主持人调用 MeetingKit 中的 </font>`<font style="color:rgb(0, 0, 0);">adminRequestUserOpenMic:onSuccess:onFailed:()</font>`<font style="color:rgb(0, 0, 0);"> 接口执行请求打开你的麦克风操作后，SDK 会抛出该事件通知您。</font>

| <font style="color:#8A8F8D;">参数</font> | <font style="color:#8A8F8D;">描述</font> |
| :--- | --- |
| <font style="color:rgb(0, 0, 0);">userId</font> | 请求者标识 |


### <font style="color:rgb(0, 0, 0);">onRequestOpenShare:()</font>
`<font style="color:rgb(0, 0, 0);">- (void)onRequestOpenShare:(NSString *)userId</font>`

<font style="color:rgb(0, 0, 0);">请求开启共享回调</font>

<font style="color:rgb(0, 0, 0);">当主持人调用 MeetingKit 中的 </font>`<font style="color:rgb(0, 0, 0);">adminRequestUserOpenShare:onSuccess:onFailed:()</font>`<font style="color:rgb(0, 0, 0);"> 接口执行请求打开你的共享操作后，SDK 会抛出该事件通知您。</font>

| <font style="color:#8A8F8D;">参数</font> | <font style="color:#8A8F8D;">描述</font> |
| :--- | --- |
| <font style="color:rgb(0, 0, 0);">userId</font> | 请求者标识 |


### <font style="color:rgb(0, 0, 0);">onRoomMoveInWaitingRoom:()</font>
`<font style="color:rgb(0, 0, 0);">- (void)onRoomMoveInWaitingRoom:(NSString *)userId</font>`

<font style="color:rgb(0, 0, 0);">被管理员移进等候室回调</font>

<font style="color:rgb(0, 0, 0);">当主持人调用 MeetingKit 中的 </font>`<font style="color:rgb(0, 0, 0);">adminMoveInWaitingRoom:ickname:onSuccess:onFailed:()</font>`<font style="color:rgb(0, 0, 0);"> 接口执行将会议室成员移动到等候室操作后，SDK 会抛出该事件通知您。</font>

| <font style="color:#8A8F8D;">参数</font> | <font style="color:#8A8F8D;">描述</font> |
| :--- | --- |
| <font style="color:rgb(0, 0, 0);">userId</font> | 操作者标识 |


### <font style="color:rgb(0, 0, 0);">onRoomMoveSubMeeting:fromMeetingTitle:toMeetingId:toMeetingTitle:()</font>
`<font style="color:rgb(0, 0, 0);">- (void)onRoomMoveSubMeeting:(NSString *)fromMeetingId fromMeetingTitle:(NSString *)fromMeetingTitle toMeetingId:(NSString *)toMeetingId toMeetingTitle:(NSString *)toMeetingTitle</font>`

<font style="color:rgb(0, 0, 0);">被管理员移进小组会议或主会场回调</font>

<font style="color:rgb(0, 0, 0);">当主持人调用 MeetingKit 中的 </font>`<font style="color:rgb(0, 0, 0);">adminMoveSubMeetingUser:fromGroupId:toGroupId:onSuccess:onFailed:()</font>`<font style="color:rgb(0, 0, 0);"> 接口执行将您移进小组会议或主会场操作后，SDK 会抛出该事件通知您。</font>

| <font style="color:#8A8F8D;">参数</font> | <font style="color:#8A8F8D;">描述</font> |
| :--- | --- |
| <font style="color:rgb(0, 0, 0);">fromMeetingId</font> | 原小组会议标识 |
| <font style="color:rgb(0, 0, 0);">fromMeetingTitle</font> | 原小组会议标题 |
| <font style="color:rgb(0, 0, 0);">toMeetingId</font> | 目标小组会议标识 |
| <font style="color:rgb(0, 0, 0);">toMeetingTitle</font> | 目标小组会议标题 |


## **房间事件回调**
### <font style="color:rgb(0, 0, 0);">onRoomCameraStateChanged:selfUnmuteCameraDisabled:userId:()</font>
`<font style="color:rgb(0, 0, 0);">- (void)onRoomCameraStateChanged:(BOOL)cameraDisabled selfUnmuteCameraDisabled:(BOOL)selfUnmuteCameraDisabled userId:(NSString *)userId</font>`

<font style="color:rgb(0, 0, 0);">房间摄像头禁用状态变更回调</font>

<font style="color:rgb(0, 0, 0);">当主持人调用 MeetingKit 中的 </font>`<font style="color:rgb(0, 0, 0);">adminUpdateRoomCameraState:selfUnmuteCameraDisabled:onSuccess:onFailed:()</font>`<font style="color:rgb(0, 0, 0);"> 接口执行更新房间全体禁视频操作后，SDK 会抛出该事件通知您。</font>

| <font style="color:#8A8F8D;">参数</font> | <font style="color:#8A8F8D;">描述</font> |
| --- | --- |
| <font style="color:rgb(0, 0, 0);">cameraDisabled</font> | <font style="color:rgb(0, 0, 0);">房间视频禁用状态，YES-禁用 NO-不禁用</font> |
| <font style="color:rgb(0, 0, 0);">selfUnmuteCameraDisabled</font> | <font style="color:rgb(0, 0, 0);">是否禁止自我解除视频状态，YES-禁止 NO-不禁止</font> |
| <font style="color:rgb(0, 0, 0);">userId</font> | <font style="color:rgb(0, 0, 0);">操作者标识</font> |


### <font style="color:rgb(0, 0, 0);">onRoomMicStateChanged:selfUnmuteMicDisabled:userId:()</font>
`<font style="color:rgb(0, 0, 0);">- (void)onRoomMicStateChanged:(BOOL)micDisabled selfUnmuteMicDisabled:(BOOL)selfUnmuteMicDisabled userId:(NSString *)userId</font>`

<font style="color:rgb(0, 0, 0);">房间麦克风禁用状态变更回调</font>

<font style="color:rgb(0, 0, 0);">当主持人调用 MeetingKit 中的 </font>`<font style="color:rgb(0, 0, 0);">adminUpdateRoomMicState:selfUnmuteMicDisabled:onSuccess:onFailed:()</font>`<font style="color:rgb(0, 0, 0);"> 接口执行更新房间全体禁音频操作后，SDK 会抛出该事件通知您。</font>

| <font style="color:#8A8F8D;">参数</font> | <font style="color:#8A8F8D;">描述</font> |
| --- | --- |
| <font style="color:rgb(0, 0, 0);">cameraDisabled</font> | <font style="color:rgb(0, 0, 0);">房间音频禁用状态，YES-禁用 NO-不禁用</font> |
| <font style="color:rgb(0, 0, 0);">selfUnmuteCameraDisabled</font> | <font style="color:rgb(0, 0, 0);">是否禁止自我解除音频状态，YES-禁止 NO-不禁止</font> |
| <font style="color:rgb(0, 0, 0);">userId</font> | <font style="color:rgb(0, 0, 0);">操作者标识</font> |


### <font style="color:rgb(0, 0, 0);">onRoomChatDisabledChanged:userId:()</font>
`<font style="color:rgb(0, 0, 0);">- (void)onRoomChatDisabledChanged:(BOOL)chatDisabled userId:(NSString *)userId</font>`

<font style="color:rgb(0, 0, 0);">房间聊天禁用状态变更回调</font>

<font style="color:rgb(0, 0, 0);">当主持人调用 MeetingKit 中的 </font>`<font style="color:rgb(0, 0, 0);">adminUpdateRoomChatDisabled:onSuccess:onFailed:()</font>`<font style="color:rgb(0, 0, 0);"> 接口执行更新房间聊天禁用状态操作后，SDK 会抛出该事件通知您。</font>

| <font style="color:#8A8F8D;">参数</font> | <font style="color:#8A8F8D;">描述</font> |
| --- | --- |
| <font style="color:rgb(0, 0, 0);">chatDisabled</font> | <font style="color:rgb(0, 0, 0);">禁用状态，YES-禁用 NO-不禁用</font> |
| <font style="color:rgb(0, 0, 0);">userId</font> | <font style="color:rgb(0, 0, 0);">操作者标识</font> |


### <font style="color:rgb(0, 0, 0);">onRoomShareDisabledChanged:userId:()</font>
`<font style="color:rgb(0, 0, 0);">- (void)onRoomShareDisabledChanged:(BOOL)shareDisabled userId:(NSString *)userId</font>`

<font style="color:rgb(0, 0, 0);">房间共享禁用状态变更回调</font>

<font style="color:rgb(0, 0, 0);">当主持人调用 MeetingKit 中的 </font>`<font style="color:rgb(0, 0, 0);">adminUpdateRoomShareDisabled:onSuccess:onFailed:()</font>`<font style="color:rgb(0, 0, 0);"> 接口执行更新房间共享禁用状态操作后，SDK 会抛出该事件通知您。</font>

| <font style="color:#8A8F8D;">参数</font> | <font style="color:#8A8F8D;">描述</font> |
| --- | --- |
| <font style="color:rgb(0, 0, 0);">shareDisabled</font> | <font style="color:rgb(0, 0, 0);">禁用状态，YES-禁用 NO-不禁用</font> |
| <font style="color:rgb(0, 0, 0);">userId</font> | <font style="color:rgb(0, 0, 0);">操作者标识</font> |


### <font style="color:rgb(0, 0, 0);">onRoomScreenshotDisabledChanged:userId:()</font>
`<font style="color:rgb(0, 0, 0);">- (void)onRoomScreenshotDisabledChanged:(BOOL)screenshotDisabled userId:(NSString *)userId</font>`

<font style="color:rgb(0, 0, 0);">房间截图禁用状态变更回调</font>

<font style="color:rgb(0, 0, 0);">当主持人调用 MeetingKit 中的 </font>`<font style="color:rgb(0, 0, 0);">adminUpdateRoomScreenshotDisabled:onSuccess:onFailed:()</font>`<font style="color:rgb(0, 0, 0);"> 接口执行更新房间截屏开关状态操作后，SDK 会抛出该事件通知您。</font>

| <font style="color:#8A8F8D;">参数</font> | <font style="color:#8A8F8D;">描述</font> |
| --- | --- |
| <font style="color:rgb(0, 0, 0);">screenshotDisabled</font> | <font style="color:rgb(0, 0, 0);">禁用状态，YES-禁用 NO-不禁用</font> |
| <font style="color:rgb(0, 0, 0);">userId</font> | <font style="color:rgb(0, 0, 0);">操作者标识</font> |


### <font style="color:rgb(0, 0, 0);">onRoomWatermarkDisabledChanged:userId:()</font>
`<font style="color:rgb(0, 0, 0);">- (void)onRoomWatermarkDisabledChanged:(BOOL)watermarkDisabled userId:(NSString *)userId</font>`

<font style="color:rgb(0, 0, 0);">房间水印禁用状态变更回调</font>

<font style="color:rgb(0, 0, 0);">当主持人调用 MeetingKit 中的 </font>`<font style="color:rgb(0, 0, 0);">adminUpdateRoomWatermarkDisabled:onSuccess:onFailed:()</font>`<font style="color:rgb(0, 0, 0);"> 接口执行更新房间水印开关状态操作后，SDK 会抛出该事件通知您。</font>

| <font style="color:#8A8F8D;">参数</font> | <font style="color:#8A8F8D;">描述</font> |
| --- | --- |
| <font style="color:rgb(0, 0, 0);">watermarkDisabled</font> | <font style="color:rgb(0, 0, 0);">禁用状态，YES-禁用 NO-不禁用</font> |
| <font style="color:rgb(0, 0, 0);">userId</font> | <font style="color:rgb(0, 0, 0);">操作者标识</font> |


### <font style="color:rgb(0, 0, 0);">onRoomWaitingRoomDisabledChanged:userId:()</font>
`<font style="color:rgb(0, 0, 0);">- (void)onRoomWaitingRoomDisabledChanged:(BOOL)waitingRoomDisabled userId:(NSString *)userId</font>`

<font style="color:rgb(0, 0, 0);">房间等候室禁用状态变更回调</font>

<font style="color:rgb(0, 0, 0);">当主持人调用 MeetingKit 中的 </font>`<font style="color:rgb(0, 0, 0);">adminUpdateWaitingRoomDisabled:onSuccess:onFailed:()</font>`<font style="color:rgb(0, 0, 0);"> 接口执行更新房间等候室禁用状态操作后，SDK 会抛出该事件通知您。</font>

| <font style="color:#8A8F8D;">参数</font> | <font style="color:#8A8F8D;">描述</font> |
| --- | --- |
| <font style="color:rgb(0, 0, 0);">waitingRoomDisabled</font> | <font style="color:rgb(0, 0, 0);">禁用状态，YES-禁用 NO-不禁用</font> |
| <font style="color:rgb(0, 0, 0);">userId</font> | <font style="color:rgb(0, 0, 0);">操作者标识</font> |


### <font style="color:rgb(0, 0, 0);">onRoomLockedChanged:userId:()</font>
`<font style="color:rgb(0, 0, 0);">- (void)onRoomLockedChanged:(BOOL)locked userId:(NSString *)userId</font>`

<font style="color:rgb(0, 0, 0);">房间锁定状态变化回调</font>

<font style="color:rgb(0, 0, 0);">当主持人调用 MeetingKit 中的 </font>`<font style="color:rgb(0, 0, 0);">adminUpdateRoomLocked:onSuccess:onFailed:()</font>`<font style="color:rgb(0, 0, 0);"> 接口执行更新房间锁定状态操作后，SDK 会抛出该事件通知您。</font>

| <font style="color:#8A8F8D;">参数</font> | <font style="color:#8A8F8D;">描述</font> |
| --- | --- |
| <font style="color:rgb(0, 0, 0);">locked</font> | <font style="color:rgb(0, 0, 0);">锁定状态，YES-开启 NO-关闭</font> |
| <font style="color:rgb(0, 0, 0);">userId</font> | <font style="color:rgb(0, 0, 0);">操作者标识</font> |


### <font style="color:rgb(0, 0, 0);">onRoomMoveHost:sourceUserId:()</font>
`<font style="color:rgb(0, 0, 0);">- (void)onRoomMoveHost:(NSString *)userId sourceUserId:(NSString *)sourceUserId</font>`

<font style="color:rgb(0, 0, 0);">房间转移主持人回调</font>

<font style="color:rgb(0, 0, 0);">当主持人调用 MeetingKit 中的 </font>`<font style="color:rgb(0, 0, 0);">adminMoveHost:onSuccess:onFailed:()</font>`<font style="color:rgb(0, 0, 0);"> 接口执行转移主持人操作后，SDK 会抛出该事件通知您。</font>

| <font style="color:#8A8F8D;">参数</font> | <font style="color:#8A8F8D;">描述</font> |
| --- | --- |
| <font style="color:rgb(0, 0, 0);">userId</font> | <font style="color:rgb(0, 0, 0);">新主持人用户标识</font> |
| <font style="color:rgb(0, 0, 0);">sourceUserId</font> | <font style="color:rgb(0, 0, 0);">原主持人用户标识</font> |


### <font style="color:rgb(0, 0, 0);">onRoomShareStart:shareType:()</font>
`<font style="color:rgb(0, 0, 0);">- (void)onRoomShareStart:(NSString *)userId shareType:(SEAShareType)shareType</font>`

<font style="color:rgb(0, 0, 0);">共享开始回调</font>

<font style="color:rgb(0, 0, 0);">当参会成员调用 MeetingKit 中的 </font>`<font style="color:rgb(0, 0, 0);">requestShare:onSuccess:onFailed:()</font>`<font style="color:rgb(0, 0, 0);"> 接口执行请求开启共享操作后，SDK 会抛出该事件通知您。</font>

> <font style="color:rgb(0, 0, 0);">特别说明：如果当前房间正有成员开启着共享，后续加入的成员也会收到该事件通知。</font>
>

| <font style="color:#8A8F8D;">参数</font> | <font style="color:#8A8F8D;">描述</font> |
| --- | --- |
| <font style="color:rgb(0, 0, 0);">userId</font> | <font style="color:rgb(0, 0, 0);">共享成员标识</font> |
| <font style="color:rgb(0, 0, 0);">shareType</font> | <font style="color:rgb(0, 0, 0);">共享类型，参考文档：</font>[SEAShareType](https://www.yuque.com/anyconf/eanoso/gkeau9oyh5vms80z#Ww9uW) |


### <font style="color:rgb(0, 0, 0);">onRoomShareStop:shareType:()</font>
`<font style="color:rgb(0, 0, 0);">- (void)onRoomShareStop:(NSString *)userId shareType:(SEAShareType)shareType</font>`

<font style="color:rgb(0, 0, 0);">共享结束回调</font>

<font style="color:rgb(0, 0, 0);">当参会成员调用 MeetingKit 中的 </font>`<font style="color:rgb(0, 0, 0);">stopShare:onFailed:()</font>`<font style="color:rgb(0, 0, 0);"> 接口执行关闭共享操作后，SDK 会抛出该事件通知您。</font>

> <font style="color:rgb(0, 0, 0);">特别说明：如果共享成员在未结束共享情况直接执行离开房间操作，此时其他成员会先收到 </font>`<font style="color:rgb(0, 0, 0);">stopShare:onFailed:()</font>`<font style="color:rgb(0, 0, 0);"> 事件通知再收到 </font>`<font style="color:rgb(0, 0, 0);">onUserExit:</font>`<font style="color:rgb(0, 0, 0);">事件通知。</font>
>

| <font style="color:#8A8F8D;">参数</font> | <font style="color:#8A8F8D;">描述</font> |
| --- | --- |
| <font style="color:rgb(0, 0, 0);">userId</font> | <font style="color:rgb(0, 0, 0);">共享成员标识</font> |
| <font style="color:rgb(0, 0, 0);">shareType</font> | <font style="color:rgb(0, 0, 0);">共享类型，参考文档：</font>[SEAShareType](https://www.yuque.com/anyconf/eanoso/gkeau9oyh5vms80z#Ww9uW) |


### <font style="color:rgb(0, 0, 0);">onAdminRoomShareStop:shareType:()</font>
`<font style="color:rgb(0, 0, 0);">- (void)onAdminRoomShareStop:(NSString *)userId shareType:(SEAShareType)shareType</font>`

<font style="color:rgb(0, 0, 0);">主持人结束房间共享回调</font>

<font style="color:rgb(0, 0, 0);">当主持人调用 MeetingKit 中的 </font>`<font style="color:rgb(0, 0, 0);">adminStopRoomShare:onFailed:()</font>`<font style="color:rgb(0, 0, 0);"> 接口执行关闭成员共享操作后，SDK 会抛出该事件通知您。</font>

| <font style="color:#8A8F8D;">参数</font> | <font style="color:#8A8F8D;">描述</font> |
| --- | --- |
| <font style="color:rgb(0, 0, 0);">userId</font> | <font style="color:rgb(0, 0, 0);">共享成员标识</font> |
| <font style="color:rgb(0, 0, 0);">shareType</font> | <font style="color:rgb(0, 0, 0);">共享类型，参考文档：</font>[SEAShareType](https://www.yuque.com/anyconf/eanoso/gkeau9oyh5vms80z#Ww9uW) |


### <font style="color:rgb(0, 0, 0);">onRoomHandUpChanged:enable:handupType:()</font>
`<font style="color:rgb(0, 0, 0);">- (void)onRoomHandUpChanged:(NSString *)userId enable:(BOOL)enable handupType:(SEAHandupType)handupType</font>`

<font style="color:rgb(0, 0, 0);">房间成员举手状态变化回调</font>

<font style="color:rgb(0, 0, 0);">当成员调用 MeetingKit 中的 </font>`<font style="color:rgb(0, 0, 0);">requestHandup:onSuccess:onFailed:()</font>`<font style="color:rgb(0, 0, 0);"> 接口执行请求举手操作后，如果您恰是房间管理角色时，SDK 会抛出该事件通知您。</font>

| <font style="color:#8A8F8D;">参数</font> | <font style="color:#8A8F8D;">描述</font> |
| --- | --- |
| <font style="color:rgb(0, 0, 0);">userId</font> | <font style="color:rgb(0, 0, 0);">成员标识</font> |
| <font style="color:rgb(0, 0, 0);">enable</font> | <font style="color:rgb(0, 0, 0);">举手状态，YES-申请举手 NO-取消举手</font> |
| <font style="color:rgb(0, 0, 0);">shareType</font> | <font style="color:rgb(0, 0, 0);">举手申请类型，参考文档：</font>[SEAHandupType](https://www.yuque.com/anyconf/eanoso/gkeau9oyh5vms80z#P2v0K) |


### <font style="color:rgb(0, 0, 0);">onRoomSubMeetingStart:title:conferee:()</font>
`<font style="color:rgb(0, 0, 0);">- (void)onRoomSubMeetingStart:(NSString *)meetingId title:(NSString *)title conferee:(nullable NSArray <NSString *> *)conferee</font>`

<font style="color:rgb(0, 0, 0);">房间讨论组开始回调</font>

<font style="color:rgb(0, 0, 0);">当成员调用 MeetingKit 中的 </font>`<font style="color:rgb(0, 0, 0);">adminStartSubMeeting:onSuccess:onFailed:()</font>`<font style="color:rgb(0, 0, 0);"> 接口执行开始小组会议操作后，SDK 会抛出该事件通知您。</font>

| <font style="color:#8A8F8D;">参数</font> | <font style="color:#8A8F8D;">描述</font> |
| --- | --- |
| <font style="color:rgb(0, 0, 0);">meetingId</font> | <font style="color:rgb(0, 0, 0);">会议标识</font> |
| <font style="color:rgb(0, 0, 0);">title</font> | <font style="color:rgb(0, 0, 0);">小组名称</font> |
| <font style="color:rgb(0, 0, 0);">conferee</font> | 参会成员标识列表 |


### <font style="color:rgb(0, 0, 0);">onRoomSubMeetingStop:()</font>
`<font style="color:rgb(0, 0, 0);">- (void)onRoomSubMeetingStop:(NSString *)parentMid</font>`

<font style="color:rgb(0, 0, 0);">房间讨论组结束回调</font>

<font style="color:rgb(0, 0, 0);">当成员调用 MeetingKit 中的 </font>`<font style="color:rgb(0, 0, 0);">adminStopSubMeeting:onSuccess:onFailed:()</font>`<font style="color:rgb(0, 0, 0);"> 接口执行结束小组会议操作后，SDK 会抛出该事件通知您。</font>

| <font style="color:#8A8F8D;">参数</font> | <font style="color:#8A8F8D;">描述</font> |
| :--- | --- |
| <font style="color:rgb(0, 0, 0);">parentMid</font> | <font style="color:rgb(0, 0, 0);">上级会议标识</font> |


### <font style="color:rgb(0, 0, 0);">onRoomMeetingTitleChanged:()</font>
`<font style="color:rgb(0, 0, 0);">- (void)onRoomMeetingTitleChanged:(NSString *)title</font>`

<font style="color:rgb(0, 0, 0);">房间会议标题变化回调</font>

<font style="color:rgb(0, 0, 0);">当管理员调用 MeetingKit 中的 </font>`<font style="color:rgb(0, 0, 0);">adminUpdateSubMeetingTitle:targetId:onSuccess:onFailed:()</font>`<font style="color:rgb(0, 0, 0);"> 接口执行修改小组会议标题操作后，SDK 会抛出该事件通知您。</font>

| <font style="color:#8A8F8D;">参数</font> | <font style="color:#8A8F8D;">描述</font> |
| :--- | --- |
| <font style="color:rgb(0, 0, 0);">title</font> | <font style="color:rgb(0, 0, 0);">会议标题</font> |


## **用户事件回调**
### <font style="color:rgb(0, 0, 0);">onUserEnter:()</font>
`<font style="color:rgb(0, 0, 0);">- (void)onUserEnter:(NSString *)userId</font>`

<font style="color:rgb(0, 0, 0);">远端用户加入房间回调</font>

<font style="color:rgb(0, 0, 0);">当远端用户调用 MeetingKit 中的 </font>`<font style="color:rgb(0, 0, 0);">enterRoom:onSuccess:onFailed:()</font>`<font style="color:rgb(0, 0, 0);"> 接口执行加入房间操作后，SDK 会抛出该事件通知您。</font>

| <font style="color:#8A8F8D;">参数</font> | <font style="color:#8A8F8D;">描述</font> |
| :--- | --- |
| <font style="color:rgb(0, 0, 0);">userId</font> | <font style="color:rgb(0, 0, 0);">成员标识</font> |


### <font style="color:rgb(0, 0, 0);">onUserExit:()</font>
`<font style="color:rgb(0, 0, 0);">- (void)onUserExit:(NSString *)userId</font>`

<font style="color:rgb(0, 0, 0);">远端用户离开房间回调</font>

<font style="color:rgb(0, 0, 0);">当远端用户调用 MeetingKit 中的 </font>`<font style="color:rgb(0, 0, 0);">exitRoom:()</font>`<font style="color:rgb(0, 0, 0);"> 接口执行离开房间操作后，SDK 会抛出该事件通知您。</font>

| <font style="color:#8A8F8D;">参数</font> | <font style="color:#8A8F8D;">描述</font> |
| :--- | --- |
| <font style="color:rgb(0, 0, 0);">userId</font> | <font style="color:rgb(0, 0, 0);">成员标识</font> |


### <font style="color:rgb(0, 0, 0);">onUserNameChanged:nickname:()</font>
`<font style="color:rgb(0, 0, 0);">- (void)onUserNameChanged:(NSString *)targetUserId nickname:(NSString *)nickname</font>`

<font style="color:rgb(0, 0, 0);">用户昵称变化回调</font>

<font style="color:rgb(0, 0, 0);">当成员调用 MeetingKit 中的 </font>`<font style="color:rgb(0, 0, 0);">updateName:onSuccess:onFailed:()</font>`<font style="color:rgb(0, 0, 0);"> 接口或者主持人调用 </font>`<font style="color:rgb(0, 0, 0);">adminUpdateNickname:nickname:onSuccess:onFailed:()</font>`<font style="color:rgb(0, 0, 0);"> 接口执行更新用户昵称操作后，SDK 会抛出该事件通知您。</font>

| <font style="color:#8A8F8D;">参数</font> | <font style="color:#8A8F8D;">描述</font> |
| :--- | --- |
| <font style="color:rgb(0, 0, 0);">targetUserId</font> | <font style="color:rgb(0, 0, 0);">目标成员标识</font> |
| <font style="color:rgb(0, 0, 0);">nickname</font> | <font style="color:rgb(0, 0, 0);">用户昵称</font> |


### <font style="color:rgb(0, 0, 0);">onUserRoleChanged:userRole:()</font>
`<font style="color:rgb(0, 0, 0);">- (void)onUserRoleChanged:(NSString *)targetUserId userRole:(SEAUserRole)userRole</font>`

<font style="color:rgb(0, 0, 0);">用户角色变化回调</font>

<font style="color:rgb(0, 0, 0);">房间管理人员调用 MeetingKit 中的 </font>`<font style="color:rgb(0, 0, 0);">adminUpdateUserRole:userRole:onSuccess:onFailed:()</font>`<font style="color:rgb(0, 0, 0);"> 接口执行更新用户角色操作后，SDK 会抛出该事件通知您。</font>

| <font style="color:#8A8F8D;">参数</font> | <font style="color:#8A8F8D;">描述</font> |
| :--- | --- |
| <font style="color:rgb(0, 0, 0);">targetUserId</font> | <font style="color:rgb(0, 0, 0);">目标成员标识</font> |
| <font style="color:rgb(0, 0, 0);">userRole</font> | <font style="color:rgb(0, 0, 0);">用户角色，参考文档：</font>[SEAUserRole](https://www.yuque.com/anyconf/eanoso/gkeau9oyh5vms80z#QsCHa) |


### <font style="color:rgb(0, 0, 0);">onUserCameraStateChanged:cameraState:reason:()</font>
`<font style="color:rgb(0, 0, 0);">- (void)onUserCameraStateChanged:(NSString *)targetUserId cameraState:(SEADeviceState)cameraState reason:(SEAChangeReason)reason</font>`

<font style="color:rgb(0, 0, 0);">用户摄像头状态变化回调</font>

<font style="color:rgb(0, 0, 0);">房间成员通过 MeetingKit 中的 </font>`<font style="color:rgb(0, 0, 0);">requestOpenCamera:view:onSuccess:onFailed:()</font>`<font style="color:rgb(0, 0, 0);"> 或 </font>`<font style="color:rgb(0, 0, 0);">closeCamera:onFailed:()</font>`<font style="color:rgb(0, 0, 0);"> 接口执行打开/关闭摄像头操作，以及房间管理人员通过 MeetingKit 中的 </font>`<font style="color:rgb(0, 0, 0);">adminCloseUserCamera:onSuccess:onFailed:()</font>`<font style="color:rgb(0, 0, 0);"> 接口执行关闭远端用户摄像头操作后，SDK 会抛出该事件通知您。</font>

> <font style="color:rgb(0, 0, 0);">特别说明：当在你加入房间之前已经有成员打开了摄像头，在你加入房间时也会抛出该事件。</font>
>

| <font style="color:#8A8F8D;">参数</font> | <font style="color:#8A8F8D;">描述</font> |
| :--- | --- |
| <font style="color:rgb(0, 0, 0);">targetUserId</font> | <font style="color:rgb(0, 0, 0);">目标成员标识</font> |
| <font style="color:rgb(0, 0, 0);">cameraState</font> | <font style="color:rgb(0, 0, 0);">摄像头状态，参考文档：</font>[SEADeviceState](https://www.yuque.com/anyconf/eanoso/gkeau9oyh5vms80z#kiwuX) |
| <font style="color:rgb(0, 0, 0);">reason</font> | <font style="color:rgb(0, 0, 0);">发生变化原因，参考文档：</font>[SEAChangeReason](https://www.yuque.com/anyconf/eanoso/gkeau9oyh5vms80z#QEutl) |


### <font style="color:rgb(0, 0, 0);">onUserMicStateChanged:micState:reason:()</font>
`<font style="color:rgb(0, 0, 0);">- (void)onUserMicStateChanged:(NSString *)targetUserId micState:(SEADeviceState)micState reason:(SEAChangeReason)reason</font>`

<font style="color:rgb(0, 0, 0);">用户麦克风状态变化回调</font>

<font style="color:rgb(0, 0, 0);">房间成员通过 MeetingKit 中的 </font>`<font style="color:rgb(0, 0, 0);">requestOpenMic:onFailed:()</font>`<font style="color:rgb(0, 0, 0);"> 或 </font>`<font style="color:rgb(0, 0, 0);">closeMic:onFailed:()</font>`<font style="color:rgb(0, 0, 0);"> 接口执行打开/关闭麦克风操作，以及房间管理人员通过 MeetingKit 中的 </font>`<font style="color:rgb(0, 0, 0);">adminCloseUserMic:onSuccess:onFailed:()</font>`<font style="color:rgb(0, 0, 0);"> 接口执行关闭远端用户麦克风操作后，SDK 会抛出该事件通知您。</font>

> <font style="color:rgb(0, 0, 0);">特别说明：当在你加入房间之前已经有成员打开了麦克风，在你加入房间时也会抛出该事件。</font>
>

| <font style="color:#8A8F8D;">参数</font> | <font style="color:#8A8F8D;">描述</font> |
| :--- | --- |
| <font style="color:rgb(0, 0, 0);">targetUserId</font> | <font style="color:rgb(0, 0, 0);">目标成员标识</font> |
| <font style="color:rgb(0, 0, 0);">micState</font> | <font style="color:rgb(0, 0, 0);">麦克风状态，参考文档：</font>[SEADeviceState](https://www.yuque.com/anyconf/eanoso/gkeau9oyh5vms80z#kiwuX) |
| <font style="color:rgb(0, 0, 0);">reason</font> | <font style="color:rgb(0, 0, 0);">发生变化原因，参考文档：</font>[SEAChangeReason](https://www.yuque.com/anyconf/eanoso/gkeau9oyh5vms80z#QEutl) |


### <font style="color:rgb(0, 0, 0);">onUserChatDisabledChanged:userId:()</font>
`<font style="color:rgb(0, 0, 0);">- (void)onUserChatDisabledChanged:(BOOL)chatDisabled userId:(NSString *)userId</font>`

<font style="color:rgb(0, 0, 0);">用户聊天能力禁用状态变化回调</font>

<font style="color:rgb(0, 0, 0);">房间管理人员通过 MeetingKit 中的 </font>`<font style="color:rgb(0, 0, 0);">adminUpdateUserChatDisabled:chatDisabled:onSuccess:onFailed:()</font>`<font style="color:rgb(0, 0, 0);"> 接口执行更新用户聊天状态操作后，SDK 会抛出该事件通知您。</font>

| <font style="color:#8A8F8D;">参数</font> | <font style="color:#8A8F8D;">描述</font> |
| :--- | --- |
| <font style="color:rgb(0, 0, 0);">chatDisabled</font> | <font style="color:rgb(0, 0, 0);">禁用状态，YES-禁用 NO-不禁用</font> |
| <font style="color:rgb(0, 0, 0);">userId</font> | 操作者标识 |


### <font style="color:rgb(0, 0, 0);">onUserDrawDisabledChanged:userId:()</font>
`<font style="color:rgb(0, 0, 0);">- (void)onUserDrawDisabledChanged:(BOOL)drawDisabled userId:(NSString *)userId</font>`

<font style="color:rgb(0, 0, 0);">用户涂鸦能力禁用状态变化回调</font>

<font style="color:rgb(0, 0, 0);">房间管理人员通过 MeetingKit 中的 </font>`<font style="color:rgb(0, 0, 0);">adminUpdateUserDrawDisabled:drawDisabled:onSuccess:onFailed:()</font>`<font style="color:rgb(0, 0, 0);"> 接口执行更新用户涂鸦状态操作后，SDK 会抛出该事件通知您。</font>

| <font style="color:#8A8F8D;">参数</font> | <font style="color:#8A8F8D;">描述</font> |
| :--- | --- |
| <font style="color:rgb(0, 0, 0);">drawDisabled</font> | <font style="color:rgb(0, 0, 0);">禁用状态，YES-禁用 NO-不禁用</font> |
| <font style="color:rgb(0, 0, 0);">userId</font> | 操作者标识 |


### <font style="color:rgb(0, 0, 0);">onHandupConfirm:approve:userId:()</font>
`<font style="color:rgb(0, 0, 0);">- (void)onHandupConfirm:(SEAHandupType)handupType approve:(BOOL)approve userId:(NSString *)userId</font>`

<font style="color:rgb(0, 0, 0);">举手处理结果回调</font>

<font style="color:rgb(0, 0, 0);">房间成员通过 MeetingKit 中的 </font>`<font style="color:rgb(0, 0, 0);">requestHandup:onSuccess:onFailed:()</font>`<font style="color:rgb(0, 0, 0);"> 接口执行请求举手操作后，房间内管理人员会接收到 SDK 抛出的 </font>`<font style="color:rgb(0, 0, 0);">onRoomHandUpChanged:enable:handupType:()</font>`<font style="color:rgb(0, 0, 0);">事件，当管理人员可以通过 </font>`<font style="color:rgb(0, 0, 0);">adminConfirmHandup:handupType:approve:onSuccess:onFailed:()</font>`<font style="color:rgb(0, 0, 0);"> 接口执行处理举手操作后，SDK 会抛出该事件通知您。</font>

| <font style="color:#8A8F8D;">参数</font> | <font style="color:#8A8F8D;">描述</font> |
| :--- | --- |
| <font style="color:rgb(0, 0, 0);">handupType</font> | <font style="color:rgb(0, 0, 0);">申请类型，参考文档：</font>[SEAHandupType](https://www.yuque.com/anyconf/eanoso/gkeau9oyh5vms80z#P2v0K) |
| <font style="color:rgb(0, 0, 0);">approve</font> | <font style="color:rgb(0, 0, 0);">处理结果，YES-同意 NO-拒绝</font> |
| <font style="color:rgb(0, 0, 0);">userId</font> | 处理人标识 |


### <font style="color:rgb(0, 0, 0);">onRoomUserEnterWaitingRoom:nickname:()</font>
`<font style="color:rgb(0, 0, 0);">- (void)onRoomUserEnterWaitingRoom:(NSString *)userId nickname:(NSString *)nickname</font>`

<font style="color:rgb(0, 0, 0);">远端用户加入等候室回调</font>

<font style="color:rgb(0, 0, 0);">用户通过 MeetingKit 中的 </font>`<font style="color:rgb(0, 0, 0);">enterRoom:()</font>`<font style="color:rgb(0, 0, 0);"> 接口执行加入房间操作，同时，如果房间开启了等候室，系统会默认将成员拉入该房间的等候室中，此时，房间内管理员会接收到 SDK 抛出的该事件通知。</font>

| <font style="color:#8A8F8D;">参数</font> | <font style="color:#8A8F8D;">描述</font> |
| :--- | --- |
| <font style="color:rgb(0, 0, 0);">userId</font> | 成员标识 |
| <font style="color:rgb(0, 0, 0);">nickname</font> | 成员昵称 |


### <font style="color:rgb(0, 0, 0);">onRoomUserExitWaitingRoom:nickname:()</font>
`<font style="color:rgb(0, 0, 0);">- (void)onRoomUserExitWaitingRoom:(NSString *)userId nickname:(NSString *)nickname</font>`

<font style="color:rgb(0, 0, 0);">远端用户离开等候室回调</font>

<font style="color:rgb(0, 0, 0);">用户通过 MeetingKit 中的 </font>`<font style="color:rgb(0, 0, 0);">exitWaitingRoom:onSuccess:onFailed:()</font>`<font style="color:rgb(0, 0, 0);"> 接口执行离开等候室操作，房间内管理员会接收到 SDK 抛出的该事件通知。</font>

| <font style="color:#8A8F8D;">参数</font> | <font style="color:#8A8F8D;">描述</font> |
| :--- | --- |
| <font style="color:rgb(0, 0, 0);">userId</font> | 成员标识 |
| <font style="color:rgb(0, 0, 0);">nickname</font> | 成员昵称 |


## **消息事件回调**
### <font style="color:rgb(0, 0, 0);">onReceiveChatMessage:message:messageType:()</font>
`<font style="color:rgb(0, 0, 0);">- (void)onReceiveChatMessage:(NSString *)senderId message:(NSString *)message messageType:(SEAMessageType)messageType</font>`

<font style="color:rgb(0, 0, 0);">收到聊天消息回调</font>

<font style="color:rgb(0, 0, 0);">当调用 MeetingKit 中的 </font>`<font style="color:rgb(0, 0, 0);">sendRoomChatMessage:messageType:targetId:onSuccess:onFailed:()</font>`<font style="color:rgb(0, 0, 0);">或者 </font>`<font style="color:rgb(0, 0, 0);">sendRoomCustomMessage:targetId:onSuccess:onFailed:()</font>`<font style="color:rgb(0, 0, 0);"> 接口执行发送消息操作后，SDK 会抛出该事件通知您。</font>

| <font style="color:#8A8F8D;">参数</font> | <font style="color:#8A8F8D;">描述</font> |
| --- | --- |
| <font style="color:rgb(0, 0, 0);">senderId</font> | <font style="color:rgb(0, 0, 0);">发送者标识</font> |
| <font style="color:rgb(0, 0, 0);">message</font> | <font style="color:rgb(0, 0, 0);">消息内容</font> |
| <font style="color:rgb(0, 0, 0);">messageType</font> | <font style="color:rgb(0, 0, 0);">消息类型，参考文档：</font>[SEAMessageType](https://www.yuque.com/anyconf/eanoso/gkeau9oyh5vms80z#xlxGu) |


### <font style="color:rgb(0, 0, 0);">onReceiveSystemMessage:messageType:()</font>
`<font style="color:rgb(0, 0, 0);">- (void)onReceiveSystemMessage:(NSString *)message messageType:(SEAMessageType)messageType</font>`

<font style="color:rgb(0, 0, 0);">收到系统消息回调</font>

<font style="color:rgb(0, 0, 0);">表示收到了系统发送的消息。</font>

| <font style="color:#8A8F8D;">参数</font> | <font style="color:#8A8F8D;">描述</font> |
| --- | --- |
| <font style="color:rgb(0, 0, 0);">message</font> | <font style="color:rgb(0, 0, 0);">消息内容</font> |
| <font style="color:rgb(0, 0, 0);">messageType</font> | <font style="color:rgb(0, 0, 0);">消息类型，参考文档：</font>[SEAMessageType](https://www.yuque.com/anyconf/eanoso/gkeau9oyh5vms80z#xlxGu) |


## **云录制事件回调**
### <font style="color:rgb(0, 0, 0);">onCloudRecordStatusChange:status:errMsg:()</font>
`<font style="color:rgb(0, 0, 0);">- (void)onCloudRecordStatusChange:(SEARecordType)recordType status:(SEARecordStatus)status errMsg:(nullable NSString *)errMsg</font>`

<font style="color:rgb(0, 0, 0);">云录制状态变更回调</font>

<font style="color:rgb(0, 0, 0);">当调用 MeetingKit 中的 </font>`<font style="color:rgb(0, 0, 0);">startCloudRecord:onSuccess:onFailed:()</font>`<font style="color:rgb(0, 0, 0);">或者</font>`<font style="color:rgb(0, 0, 0);">stopCloudRecord:onFailed:()</font>`<font style="color:rgb(0, 0, 0);"> 接口执行开启或停止云录制操作后，SDK 会抛出该事件通知您。</font>

| <font style="color:#8A8F8D;">参数</font> | <font style="color:#8A8F8D;">描述</font> |
| --- | --- |
| <font style="color:rgb(0, 0, 0);">recordType</font> | <font style="color:rgb(0, 0, 0);">录制类型，参考文档：</font>[SEARecordType](https://www.yuque.com/anyconf/smeeting/gkeau9oyh5vms80z#QYWNw) |
| <font style="color:rgb(0, 0, 0);">status</font> | <font style="color:rgb(0, 0, 0);">录制状态，参考文档：</font>[SEARecordStatus](https://www.yuque.com/anyconf/smeeting/gkeau9oyh5vms80z#XOsJa) |
| <font style="color:rgb(0, 0, 0);">errMsg</font> | <font style="color:rgb(0, 0, 0);">错误描述</font> |


### <font style="color:rgb(0, 0, 0);">onCloudRecordAlarm:taskId:gateway:alarmAt:alarmBrief:()</font>
`<font style="color:rgb(0, 0, 0);">- (void)onCloudRecordAlarm:(SEARecordStatus)status taskId:(NSString *)taskId gateway:(NSString *)gateway alarmAt:(NSInteger)alarmAt alarmBrief:(nullable NSString *)alarmBrief</font>`

<font style="color:rgb(0, 0, 0);">云录制告警回调</font>

<font style="color:rgb(0, 0, 0);">当会议服务检测到云录制出现了异常时，SDK 会抛出该事件通知您。</font>

| <font style="color:#8A8F8D;">参数</font> | <font style="color:#8A8F8D;">描述</font> |
| --- | --- |
| <font style="color:rgb(0, 0, 0);">status</font> | <font style="color:rgb(0, 0, 0);">录制状态，参考文档：</font>[SEARecordStatus](https://www.yuque.com/anyconf/smeeting/gkeau9oyh5vms80z#XOsJa) |
| <font style="color:rgb(0, 0, 0);">taskId</font> | 任务标识 |
| <font style="color:rgb(0, 0, 0);">gateway</font> | 所在网关 |
| <font style="color:rgb(0, 0, 0);">alarmAt</font> | 告警时间 |
| <font style="color:rgb(0, 0, 0);">alarmBrief</font> | <font style="color:rgb(0, 0, 0);">告警摘要</font> |


## **屏幕采集事件回调**
### <font style="color:rgb(0, 0, 0);">onScreenRecordStatus:()</font>
`<font style="color:rgb(0, 0, 0);">- (void)onScreenRecordStatus:(SEAScreenRecordStatus)status</font>`

<font style="color:rgb(0, 0, 0);">屏幕共享状态回调</font>

<font style="color:rgb(0, 0, 0);">屏幕录制扩展程序调用 MeetingKit 中的 </font>`<font style="color:rgb(0, 0, 0);">broadcastStartedWithAppGroup:delegate:()</font>`<font style="color:rgb(0, 0, 0);"> 接口执行启动录屏操作后， SDK 会通过 </font>`<font style="color:rgb(0, 0, 0);">onScreenRecordStatus:()</font>`<font style="color:rgb(0, 0, 0);"> 回调抛出当前的屏幕采集状态。</font>

| <font style="color:#8A8F8D;">参数</font> | <font style="color:#8A8F8D;">描述</font> |
| --- | --- |
| <font style="color:rgb(0, 0, 0);">status</font> | <font style="color:rgb(0, 0, 0);">状态码，参考文档：</font>[SEAScreenRecordStatus](https://www.yuque.com/anyconf/eanoso/gkeau9oyh5vms80z#kVZHh) |


## **音频事件回调**
### <font style="color:rgb(0, 0, 0);">onAudioRouteChange:previousRoute:()</font>
`<font style="color:rgb(0, 0, 0);">- (void)onAudioRouteChange:(SEAAudioRoute)route previousRoute:(SEAAudioRoute)previousRoute</font>`

<font style="color:rgb(0, 0, 0);">音频路由变更回调</font>

<font style="color:rgb(0, 0, 0);">音频路由发生改变时，SDK 会抛出 </font>`<font style="color:rgb(0, 0, 0);">onAudioRouteChange:previousRoute:()</font>`<font style="color:rgb(0, 0, 0);"> 回调。</font>

<font style="color:rgb(0, 0, 0);">参考文档：</font>[SEAAudioRoute](https://www.yuque.com/anyconf/eanoso/gkeau9oyh5vms80z#HhTLs)

| <font style="color:#8A8F8D;">参数</font> | <font style="color:#8A8F8D;">描述</font> |
| --- | --- |
| <font style="color:rgb(0, 0, 0);">route</font> | 音频路由 |
| <font style="color:rgb(0, 0, 0);">previousRoute</font> | <font style="color:rgb(0, 0, 0);">变更前的音频路由</font> |


### <font style="color:rgb(0, 0, 0);">onRemoteMemberAudioStatus:()</font>
`<font style="color:rgb(0, 0, 0);">- (void)onRemoteMemberAudioStatus:(NSArray<SEAStreamAudioModel *> *)audioArray</font>`

<font style="color:rgb(0, 0, 0);">远程成员音频状态数据回调</font>

<font style="color:rgb(0, 0, 0);">房间成员音频状态数据回调，包括：音频的分贝值、功率等信息，业务层可通过该回调统计音频数据进行语音激励等操作。</font>

| <font style="color:#8A8F8D;">参数</font> | <font style="color:#8A8F8D;">描述</font> |
| --- | --- |
| <font style="color:rgb(0, 0, 0);">audioArray</font> | 成员音频数据列表，<font style="color:rgb(0, 0, 0);">参考文档：</font>[SEAStreamAudioModel](https://www.yuque.com/anyconf/eanoso/gkeau9oyh5vms80z#Lw5lL) |


## **流媒体事件回调**
### <font style="color:rgb(0, 0, 0);">onDownBitrateAdaptiveUserId:state:()</font>
`<font style="color:rgb(0, 0, 0);">- (void)onDownBitrateAdaptiveUserId:(NSString *)userId state:(SEADownBitrateAdaptiveState)state</font>`

<font style="color:rgb(0, 0, 0);">下行码率自适应状态回调</font>

<font style="color:rgb(0, 0, 0);">开启码率自适应后，SDK 会根据网络情况动态调整下行成员链路的码率自适应等级。</font>

| <font style="color:#8A8F8D;">参数</font> | <font style="color:#8A8F8D;">描述</font> |
| --- | --- |
| <font style="color:rgb(0, 0, 0);">userId</font> | 用户标识 |
| <font style="color:rgb(0, 0, 0);">state</font> | <font style="color:rgb(0, 0, 0);">下行码率自适应状态，参考文档：</font>[SEADownBitrateAdaptiveState](https://www.yuque.com/anyconf/eanoso/gkeau9oyh5vms80z#hHKyj) |


### <font style="color:rgb(0, 0, 0);">onUploadBitrateAdaptiveState:()</font>
`<font style="color:rgb(0, 0, 0);">- (void)onUploadBitrateAdaptiveState:(SEAUploadBitrateAdaptiveState)state</font>`

<font style="color:rgb(0, 0, 0);">上行码率自适应状态回调</font>

<font style="color:rgb(0, 0, 0);">开启码率自适应后，SDK 会根据网络情况动态调整上行链路的码率自适应等级。</font>

| <font style="color:#8A8F8D;">参数</font> | <font style="color:#8A8F8D;">描述</font> |
| --- | --- |
| <font style="color:rgb(0, 0, 0);">state</font> | <font style="color:rgb(0, 0, 0);">上行码率自适应状态，参考文档：</font>[SEAUploadBitrateAdaptiveState](https://www.yuque.com/anyconf/eanoso/gkeau9oyh5vms80z#ZryAr) |


### <font style="color:rgb(0, 0, 0);">onDownLossLevelChangeState:()</font>
`<font style="color:rgb(0, 0, 0);">- (void)onDownLossLevelChangeState:(SEADownLossLevelState)state</font>`

<font style="color:rgb(0, 0, 0);">下行平均丢包档位变化回调</font>

| <font style="color:#8A8F8D;">参数</font> | <font style="color:#8A8F8D;">描述</font> |
| --- | --- |
| <font style="color:rgb(0, 0, 0);">state</font> | <font style="color:rgb(0, 0, 0);">下行平均丢包档位，参考文档：</font>[SEADownLossLevelState](https://www.yuque.com/anyconf/eanoso/gkeau9oyh5vms80z#yMw23) |


### <font style="color:rgb(0, 0, 0);">onDownLossRateAverage:()</font>
`<font style="color:rgb(0, 0, 0);">- (void)onDownLossRateAverage:(CGFloat)average</font>`

<font style="color:rgb(0, 0, 0);">下行平均丢包率回调</font>

| <font style="color:#8A8F8D;">参数</font> | <font style="color:#8A8F8D;">描述</font> |
| --- | --- |
| <font style="color:rgb(0, 0, 0);">average</font> | 下行平均丢包率 |


### <font style="color:rgb(0, 0, 0);">onSendStreamModel:()</font>
`<font style="color:rgb(0, 0, 0);">- (void)onSendStreamModel:(SEAStreamSendModel *)sendModel</font>`

<font style="color:rgb(0, 0, 0);">流媒体发送状态数据回调</font>

<font style="color:rgb(0, 0, 0);">会在固定时间间隔，会收到来自 </font>`<font style="color:rgb(0, 0, 0);">MeetingKitDelegate</font>`<font style="color:rgb(0, 0, 0);"> 的 </font>`<font style="color:rgb(0, 0, 0);">onSendStreamModel:()</font>`<font style="color:rgb(0, 0, 0);"> 事件回调，描述当前数据发送状态延迟、丢包率等信息。</font>

| <font style="color:#8A8F8D;">参数</font> | <font style="color:#8A8F8D;">描述</font> |
| --- | --- |
| <font style="color:rgb(0, 0, 0);">sendModel</font> | 流媒体发送状态数据，<font style="color:rgb(0, 0, 0);">参考文档：</font>[SEAStreamSendModel](https://www.yuque.com/anyconf/eanoso/gkeau9oyh5vms80z#e4l7V) |


### <font style="color:rgb(0, 0, 0);">onReceiveStreamModel:()</font>
`<font style="color:rgb(0, 0, 0);">- (void)onReceiveStreamModel:(NSArray <SEAStreamReceiveModel *> *)receiveArray</font>`

<font style="color:rgb(0, 0, 0);">流媒体接收状态数据回调</font>

<font style="color:rgb(0, 0, 0);">会在固定时间间隔，会收到来自 </font>`<font style="color:rgb(0, 0, 0);">MeetingKitDelegate</font>`<font style="color:rgb(0, 0, 0);"> 的 </font>`<font style="color:rgb(0, 0, 0);">onReceiveStreamModel:()</font>`<font style="color:rgb(0, 0, 0);"> 事件回调，描述当前数据接收状态延迟、丢包率等信息。</font>

| <font style="color:#8A8F8D;">参数</font> | <font style="color:#8A8F8D;">描述</font> |
| --- | --- |
| <font style="color:rgb(0, 0, 0);">receiveModel</font> | 流媒体接收状态数据，<font style="color:rgb(0, 0, 0);">参考文档：</font>[SEAStreamReceiveModel](https://www.yuque.com/anyconf/eanoso/gkeau9oyh5vms80z#leOhF) |


### <font style="color:rgb(0, 0, 0);">onReceiveStreamStatusChange:streamType:status:()</font>
`<font style="color:rgb(0, 0, 0);">- (void)onReceiveStreamStatusChange:(NSString *)targetUserId streamType:(SEAVideoStreamType)streamType status:(BOOL)status</font>`

<font style="color:rgb(0, 0, 0);">流媒体接收视频流状态变更回调</font>

<font style="color:rgb(0, 0, 0);">订阅成员远程视频流后，如果持续一段时间没有收到该成员的视频流，会收到来自 </font>`<font style="color:rgb(0, 0, 0);">MeetingKitDelegate</font>`<font style="color:rgb(0, 0, 0);"> 的 </font>`<font style="color:rgb(0, 0, 0);">onReceiveStreamStatusChange:streamType:status:()</font>`<font style="color:rgb(0, 0, 0);"> 事件回调。同时，接收视频流恢复后也会收到该回调。</font>

| <font style="color:#8A8F8D;">参数</font> | <font style="color:#8A8F8D;">描述</font> |
| --- | --- |
| <font style="color:rgb(0, 0, 0);">targetUserId</font> | 目标成员标识 |
| <font style="color:rgb(0, 0, 0);">streamType</font> | 视频流类型，<font style="color:rgb(0, 0, 0);">参考文档：</font>[SEAVideoStreamType](https://www.yuque.com/anyconf/eanoso/gkeau9oyh5vms80z#ckLzs) |
| <font style="color:rgb(0, 0, 0);">status</font> | 接收状态，YES-超时 NO-恢复 |


### <font style="color:rgb(0, 0, 0);">onReceiveMixtureStreamStatusChange:()</font>
`<font style="color:rgb(0, 0, 0);">- (void)onReceiveMixtureStreamStatusChange:(BOOL)status</font>`

<font style="color:rgb(0, 0, 0);">流媒体接收合成流画面状态变更回调</font>

<font style="color:rgb(0, 0, 0);">订阅合成流画面视频流后，如果持续一段时间没有收到合成画面的视频流，会收到来自 </font>`<font style="color:rgb(0, 0, 0);">MeetingKitDelegate</font>`<font style="color:rgb(0, 0, 0);"> 的 </font>`<font style="color:rgb(0, 0, 0);">onReceiveMixtureStreamStatusChange:()</font>`<font style="color:rgb(0, 0, 0);"> 事件回调。同时，接收视频流恢复后也会收到该回调。</font>

| <font style="color:#8A8F8D;">参数</font> | <font style="color:#8A8F8D;">描述</font> |
| --- | --- |
| <font style="color:rgb(0, 0, 0);">status</font> | 接收状态，YES-超时 NO-恢复 |


## **其它事件回调**
### <font style="color:rgb(0, 0, 0);">onApplicationPerformance:cpuUsage:()</font>
`<font style="color:rgb(0, 0, 0);">- (void)onApplicationPerformance:(CGFloat)memory cpuUsage:(CGFloat)cpuUsage</font>`

<font style="color:rgb(0, 0, 0);">应用性能使用情况回调</font>

<font style="color:rgb(0, 0, 0);">房间内当前性能使用情况回调。</font>

| <font style="color:#8A8F8D;">参数</font> | <font style="color:#8A8F8D;">描述</font> |
| --- | --- |
| <font style="color:rgb(0, 0, 0);">memory</font> | 内存使用情况 |
| <font style="color:rgb(0, 0, 0);">cpuUsage</font> | <font style="color:rgb(0, 0, 0);">CUP使用率</font> |


