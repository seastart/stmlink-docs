---
title: "MeetingKitDelegate"
description: "iOS SMeeting 会议 SDK MeetingKitDelegate 接口参考"
---

## **错误事件回调**
### onError:errMsg:()
`- (void)onError:(SEAError)errCode errMsg:(nullable NSString *)errMsg`

错误事件回调

表示 SDK 发生不可恢复的错误，比如：加入房间失败或设备开启失败等。这个事件触发一般需要获取新的令牌重新入会。

参考文档：[错误码表](https://www.yuque.com/anyconf/eanoso/zbbk63kiyugwavue)

| 参数 | 描述 |
| --- | --- |
| errCode | 错误码 |
| errMsg | 错误信息 |


## **连接事件回调**
### onReconnecting()
`- (void)onReconnecting`

开始重连事件回调

表示 SDK 连接发生异常，正在尝试重连，如：网络抖动等。如中途遇到错误 SDK 会抛出 `onError:errMsg:()` 回调。

### onReconnected()
`- (void)onReconnected`

重连成功事件回调

当 SDK 断线重连成功并且连接已经恢复时，会收到该事件通知。如中途遇到错误 SDK 会抛出 `onError:errMsg:()` 回调。

## **我的相关回调**
### onEnterRoom:userId:()
`- (void)onEnterRoom:(NSString *)meetingId userId:(NSString *)userId`

进入房间事件回调

调用 MeetingKit 中的 `enterRoom:onSuccess:onFailed:()` 接口执行进入房间操作后，会收到来自`MeetingKitDelegate` 的 `onEnterRoom:userId:()` 回调，如遇到错误 SDK 会通过方法中 `onFailed` 参数返回。

| 参数 | 描述 |
| --- | --- |
| meetingId | 会议标识 |
| userId | 用户标识 |


### onExitRoom:()
`- (void)onExitRoom:(SEALeaveReason)reason`

离开房间事件回调

当前用户非主动离开时，会收到该事件通知，如：被主持人踢出房间、会议解散等。

> 值得注意的是，调用 MeetingKit 中的 `exitRoom: `接口会执行退出房间的相关逻辑，例如释放音视频设备资源和编解码器资源等。待 SDK 占用的所有资源释放完毕后，SDK 会通过方法携带的 `onSuccess` 参数抛出，你可以在此返回中执行“离开界面”等操作。此时，不会再收到 `onExitRoom()` 事件通知。
>

| 参数 | 描述 |
| :--- | --- |
| reason | 离开原因，参考文档：[SEALeaveReason](https://www.yuque.com/anyconf/eanoso/gkeau9oyh5vms80z#bbLNp) |


### onRequestOpenCamera:()
`- (void)onRequestOpenCamera:(NSString *)userId`

请求开启摄像头回调

当主持人调用 MeetingKit 中的 `adminRequestUserOpenCamera:onSuccess:onFailed:()` 接口执行请求打开你的摄像头操作后，SDK 会抛出该事件通知您。

| 参数 | 描述 |
| :--- | --- |
| userId | 请求者标识 |


### onRequestOpenMic:()
`- (void)onRequestOpenMic:(NSString *)userId`

请求开启麦克风回调

当主持人调用 MeetingKit 中的 `adminRequestUserOpenMic:onSuccess:onFailed:()` 接口执行请求打开你的麦克风操作后，SDK 会抛出该事件通知您。

| 参数 | 描述 |
| :--- | --- |
| userId | 请求者标识 |


### onRequestOpenShare:()
`- (void)onRequestOpenShare:(NSString *)userId`

请求开启共享回调

当主持人调用 MeetingKit 中的 `adminRequestUserOpenShare:onSuccess:onFailed:()` 接口执行请求打开你的共享操作后，SDK 会抛出该事件通知您。

| 参数 | 描述 |
| :--- | --- |
| userId | 请求者标识 |


### onRoomMoveInWaitingRoom:()
`- (void)onRoomMoveInWaitingRoom:(NSString *)userId`

被管理员移进等候室回调

当主持人调用 MeetingKit 中的 `adminMoveInWaitingRoom:ickname:onSuccess:onFailed:()` 接口执行将会议室成员移动到等候室操作后，SDK 会抛出该事件通知您。

| 参数 | 描述 |
| :--- | --- |
| userId | 操作者标识 |


### onRoomMoveSubMeeting:fromMeetingTitle:toMeetingId:toMeetingTitle:()
`- (void)onRoomMoveSubMeeting:(NSString *)fromMeetingId fromMeetingTitle:(NSString *)fromMeetingTitle toMeetingId:(NSString *)toMeetingId toMeetingTitle:(NSString *)toMeetingTitle`

被管理员移进小组会议或主会场回调

当主持人调用 MeetingKit 中的 `adminMoveSubMeetingUser:fromGroupId:toGroupId:onSuccess:onFailed:()` 接口执行将您移进小组会议或主会场操作后，SDK 会抛出该事件通知您。

| 参数 | 描述 |
| :--- | --- |
| fromMeetingId | 原小组会议标识 |
| fromMeetingTitle | 原小组会议标题 |
| toMeetingId | 目标小组会议标识 |
| toMeetingTitle | 目标小组会议标题 |


## **房间事件回调**
### onRoomCameraStateChanged:selfUnmuteCameraDisabled:userId:()
`- (void)onRoomCameraStateChanged:(BOOL)cameraDisabled selfUnmuteCameraDisabled:(BOOL)selfUnmuteCameraDisabled userId:(NSString *)userId`

房间摄像头禁用状态变更回调

当主持人调用 MeetingKit 中的 `adminUpdateRoomCameraState:selfUnmuteCameraDisabled:onSuccess:onFailed:()` 接口执行更新房间全体禁视频操作后，SDK 会抛出该事件通知您。

| 参数 | 描述 |
| --- | --- |
| cameraDisabled | 房间视频禁用状态，YES-禁用 NO-不禁用 |
| selfUnmuteCameraDisabled | 是否禁止自我解除视频状态，YES-禁止 NO-不禁止 |
| userId | 操作者标识 |


### onRoomMicStateChanged:selfUnmuteMicDisabled:userId:()
`- (void)onRoomMicStateChanged:(BOOL)micDisabled selfUnmuteMicDisabled:(BOOL)selfUnmuteMicDisabled userId:(NSString *)userId`

房间麦克风禁用状态变更回调

当主持人调用 MeetingKit 中的 `adminUpdateRoomMicState:selfUnmuteMicDisabled:onSuccess:onFailed:()` 接口执行更新房间全体禁音频操作后，SDK 会抛出该事件通知您。

| 参数 | 描述 |
| --- | --- |
| cameraDisabled | 房间音频禁用状态，YES-禁用 NO-不禁用 |
| selfUnmuteCameraDisabled | 是否禁止自我解除音频状态，YES-禁止 NO-不禁止 |
| userId | 操作者标识 |


### onRoomChatDisabledChanged:userId:()
`- (void)onRoomChatDisabledChanged:(BOOL)chatDisabled userId:(NSString *)userId`

房间聊天禁用状态变更回调

当主持人调用 MeetingKit 中的 `adminUpdateRoomChatDisabled:onSuccess:onFailed:()` 接口执行更新房间聊天禁用状态操作后，SDK 会抛出该事件通知您。

| 参数 | 描述 |
| --- | --- |
| chatDisabled | 禁用状态，YES-禁用 NO-不禁用 |
| userId | 操作者标识 |


### onRoomShareDisabledChanged:userId:()
`- (void)onRoomShareDisabledChanged:(BOOL)shareDisabled userId:(NSString *)userId`

房间共享禁用状态变更回调

当主持人调用 MeetingKit 中的 `adminUpdateRoomShareDisabled:onSuccess:onFailed:()` 接口执行更新房间共享禁用状态操作后，SDK 会抛出该事件通知您。

| 参数 | 描述 |
| --- | --- |
| shareDisabled | 禁用状态，YES-禁用 NO-不禁用 |
| userId | 操作者标识 |


### onRoomScreenshotDisabledChanged:userId:()
`- (void)onRoomScreenshotDisabledChanged:(BOOL)screenshotDisabled userId:(NSString *)userId`

房间截图禁用状态变更回调

当主持人调用 MeetingKit 中的 `adminUpdateRoomScreenshotDisabled:onSuccess:onFailed:()` 接口执行更新房间截屏开关状态操作后，SDK 会抛出该事件通知您。

| 参数 | 描述 |
| --- | --- |
| screenshotDisabled | 禁用状态，YES-禁用 NO-不禁用 |
| userId | 操作者标识 |


### onRoomWatermarkDisabledChanged:userId:()
`- (void)onRoomWatermarkDisabledChanged:(BOOL)watermarkDisabled userId:(NSString *)userId`

房间水印禁用状态变更回调

当主持人调用 MeetingKit 中的 `adminUpdateRoomWatermarkDisabled:onSuccess:onFailed:()` 接口执行更新房间水印开关状态操作后，SDK 会抛出该事件通知您。

| 参数 | 描述 |
| --- | --- |
| watermarkDisabled | 禁用状态，YES-禁用 NO-不禁用 |
| userId | 操作者标识 |


### onRoomWaitingRoomDisabledChanged:userId:()
`- (void)onRoomWaitingRoomDisabledChanged:(BOOL)waitingRoomDisabled userId:(NSString *)userId`

房间等候室禁用状态变更回调

当主持人调用 MeetingKit 中的 `adminUpdateWaitingRoomDisabled:onSuccess:onFailed:()` 接口执行更新房间等候室禁用状态操作后，SDK 会抛出该事件通知您。

| 参数 | 描述 |
| --- | --- |
| waitingRoomDisabled | 禁用状态，YES-禁用 NO-不禁用 |
| userId | 操作者标识 |


### onRoomLockedChanged:userId:()
`- (void)onRoomLockedChanged:(BOOL)locked userId:(NSString *)userId`

房间锁定状态变化回调

当主持人调用 MeetingKit 中的 `adminUpdateRoomLocked:onSuccess:onFailed:()` 接口执行更新房间锁定状态操作后，SDK 会抛出该事件通知您。

| 参数 | 描述 |
| --- | --- |
| locked | 锁定状态，YES-开启 NO-关闭 |
| userId | 操作者标识 |


### onRoomMoveHost:sourceUserId:()
`- (void)onRoomMoveHost:(NSString *)userId sourceUserId:(NSString *)sourceUserId`

房间转移主持人回调

当主持人调用 MeetingKit 中的 `adminMoveHost:onSuccess:onFailed:()` 接口执行转移主持人操作后，SDK 会抛出该事件通知您。

| 参数 | 描述 |
| --- | --- |
| userId | 新主持人用户标识 |
| sourceUserId | 原主持人用户标识 |


### onRoomShareStart:shareType:()
`- (void)onRoomShareStart:(NSString *)userId shareType:(SEAShareType)shareType`

共享开始回调

当参会成员调用 MeetingKit 中的 `requestShare:onSuccess:onFailed:()` 接口执行请求开启共享操作后，SDK 会抛出该事件通知您。

> 特别说明：如果当前房间正有成员开启着共享，后续加入的成员也会收到该事件通知。
>

| 参数 | 描述 |
| --- | --- |
| userId | 共享成员标识 |
| shareType | 共享类型，参考文档：[SEAShareType](https://www.yuque.com/anyconf/eanoso/gkeau9oyh5vms80z#Ww9uW) |


### onRoomShareStop:shareType:()
`- (void)onRoomShareStop:(NSString *)userId shareType:(SEAShareType)shareType`

共享结束回调

当参会成员调用 MeetingKit 中的 `stopShare:onFailed:()` 接口执行关闭共享操作后，SDK 会抛出该事件通知您。

> 特别说明：如果共享成员在未结束共享情况直接执行离开房间操作，此时其他成员会先收到 `stopShare:onFailed:()` 事件通知再收到 `onUserExit:`事件通知。
>

| 参数 | 描述 |
| --- | --- |
| userId | 共享成员标识 |
| shareType | 共享类型，参考文档：[SEAShareType](https://www.yuque.com/anyconf/eanoso/gkeau9oyh5vms80z#Ww9uW) |


### onAdminRoomShareStop:shareType:()
`- (void)onAdminRoomShareStop:(NSString *)userId shareType:(SEAShareType)shareType`

主持人结束房间共享回调

当主持人调用 MeetingKit 中的 `adminStopRoomShare:onFailed:()` 接口执行关闭成员共享操作后，SDK 会抛出该事件通知您。

| 参数 | 描述 |
| --- | --- |
| userId | 共享成员标识 |
| shareType | 共享类型，参考文档：[SEAShareType](https://www.yuque.com/anyconf/eanoso/gkeau9oyh5vms80z#Ww9uW) |


### onRoomHandUpChanged:enable:handupType:()
`- (void)onRoomHandUpChanged:(NSString *)userId enable:(BOOL)enable handupType:(SEAHandupType)handupType`

房间成员举手状态变化回调

当成员调用 MeetingKit 中的 `requestHandup:onSuccess:onFailed:()` 接口执行请求举手操作后，如果您恰是房间管理角色时，SDK 会抛出该事件通知您。

| 参数 | 描述 |
| --- | --- |
| userId | 成员标识 |
| enable | 举手状态，YES-申请举手 NO-取消举手 |
| shareType | 举手申请类型，参考文档：[SEAHandupType](https://www.yuque.com/anyconf/eanoso/gkeau9oyh5vms80z#P2v0K) |


### onRoomSubMeetingStart:title:conferee:()
`- (void)onRoomSubMeetingStart:(NSString *)meetingId title:(NSString *)title conferee:(nullable NSArray <NSString *> *)conferee`

房间讨论组开始回调

当成员调用 MeetingKit 中的 `adminStartSubMeeting:onSuccess:onFailed:()` 接口执行开始小组会议操作后，SDK 会抛出该事件通知您。

| 参数 | 描述 |
| --- | --- |
| meetingId | 会议标识 |
| title | 小组名称 |
| conferee | 参会成员标识列表 |


### onRoomSubMeetingStop:()
`- (void)onRoomSubMeetingStop:(NSString *)parentMid`

房间讨论组结束回调

当成员调用 MeetingKit 中的 `adminStopSubMeeting:onSuccess:onFailed:()` 接口执行结束小组会议操作后，SDK 会抛出该事件通知您。

| 参数 | 描述 |
| :--- | --- |
| parentMid | 上级会议标识 |


### onRoomMeetingTitleChanged:()
`- (void)onRoomMeetingTitleChanged:(NSString *)title`

房间会议标题变化回调

当管理员调用 MeetingKit 中的 `adminUpdateSubMeetingTitle:targetId:onSuccess:onFailed:()` 接口执行修改小组会议标题操作后，SDK 会抛出该事件通知您。

| 参数 | 描述 |
| :--- | --- |
| title | 会议标题 |


## **用户事件回调**
### onUserEnter:()
`- (void)onUserEnter:(NSString *)userId`

远端用户加入房间回调

当远端用户调用 MeetingKit 中的 `enterRoom:onSuccess:onFailed:()` 接口执行加入房间操作后，SDK 会抛出该事件通知您。

| 参数 | 描述 |
| :--- | --- |
| userId | 成员标识 |


### onUserExit:()
`- (void)onUserExit:(NSString *)userId`

远端用户离开房间回调

当远端用户调用 MeetingKit 中的 `exitRoom:()` 接口执行离开房间操作后，SDK 会抛出该事件通知您。

| 参数 | 描述 |
| :--- | --- |
| userId | 成员标识 |


### onUserNameChanged:nickname:()
`- (void)onUserNameChanged:(NSString *)targetUserId nickname:(NSString *)nickname`

用户昵称变化回调

当成员调用 MeetingKit 中的 `updateName:onSuccess:onFailed:()` 接口或者主持人调用 `adminUpdateNickname:nickname:onSuccess:onFailed:()` 接口执行更新用户昵称操作后，SDK 会抛出该事件通知您。

| 参数 | 描述 |
| :--- | --- |
| targetUserId | 目标成员标识 |
| nickname | 用户昵称 |


### onUserRoleChanged:userRole:()
`- (void)onUserRoleChanged:(NSString *)targetUserId userRole:(SEAUserRole)userRole`

用户角色变化回调

房间管理人员调用 MeetingKit 中的 `adminUpdateUserRole:userRole:onSuccess:onFailed:()` 接口执行更新用户角色操作后，SDK 会抛出该事件通知您。

| 参数 | 描述 |
| :--- | --- |
| targetUserId | 目标成员标识 |
| userRole | 用户角色，参考文档：[SEAUserRole](https://www.yuque.com/anyconf/eanoso/gkeau9oyh5vms80z#QsCHa) |


### onUserCameraStateChanged:cameraState:reason:()
`- (void)onUserCameraStateChanged:(NSString *)targetUserId cameraState:(SEADeviceState)cameraState reason:(SEAChangeReason)reason`

用户摄像头状态变化回调

房间成员通过 MeetingKit 中的 `requestOpenCamera:view:onSuccess:onFailed:()` 或 `closeCamera:onFailed:()` 接口执行打开/关闭摄像头操作，以及房间管理人员通过 MeetingKit 中的 `adminCloseUserCamera:onSuccess:onFailed:()` 接口执行关闭远端用户摄像头操作后，SDK 会抛出该事件通知您。

> 特别说明：当在你加入房间之前已经有成员打开了摄像头，在你加入房间时也会抛出该事件。
>

| 参数 | 描述 |
| :--- | --- |
| targetUserId | 目标成员标识 |
| cameraState | 摄像头状态，参考文档：[SEADeviceState](https://www.yuque.com/anyconf/eanoso/gkeau9oyh5vms80z#kiwuX) |
| reason | 发生变化原因，参考文档：[SEAChangeReason](https://www.yuque.com/anyconf/eanoso/gkeau9oyh5vms80z#QEutl) |


### onUserMicStateChanged:micState:reason:()
`- (void)onUserMicStateChanged:(NSString *)targetUserId micState:(SEADeviceState)micState reason:(SEAChangeReason)reason`

用户麦克风状态变化回调

房间成员通过 MeetingKit 中的 `requestOpenMic:onFailed:()` 或 `closeMic:onFailed:()` 接口执行打开/关闭麦克风操作，以及房间管理人员通过 MeetingKit 中的 `adminCloseUserMic:onSuccess:onFailed:()` 接口执行关闭远端用户麦克风操作后，SDK 会抛出该事件通知您。

> 特别说明：当在你加入房间之前已经有成员打开了麦克风，在你加入房间时也会抛出该事件。
>

| 参数 | 描述 |
| :--- | --- |
| targetUserId | 目标成员标识 |
| micState | 麦克风状态，参考文档：[SEADeviceState](https://www.yuque.com/anyconf/eanoso/gkeau9oyh5vms80z#kiwuX) |
| reason | 发生变化原因，参考文档：[SEAChangeReason](https://www.yuque.com/anyconf/eanoso/gkeau9oyh5vms80z#QEutl) |


### onUserChatDisabledChanged:userId:()
`- (void)onUserChatDisabledChanged:(BOOL)chatDisabled userId:(NSString *)userId`

用户聊天能力禁用状态变化回调

房间管理人员通过 MeetingKit 中的 `adminUpdateUserChatDisabled:chatDisabled:onSuccess:onFailed:()` 接口执行更新用户聊天状态操作后，SDK 会抛出该事件通知您。

| 参数 | 描述 |
| :--- | --- |
| chatDisabled | 禁用状态，YES-禁用 NO-不禁用 |
| userId | 操作者标识 |


### onUserDrawDisabledChanged:userId:()
`- (void)onUserDrawDisabledChanged:(BOOL)drawDisabled userId:(NSString *)userId`

用户涂鸦能力禁用状态变化回调

房间管理人员通过 MeetingKit 中的 `adminUpdateUserDrawDisabled:drawDisabled:onSuccess:onFailed:()` 接口执行更新用户涂鸦状态操作后，SDK 会抛出该事件通知您。

| 参数 | 描述 |
| :--- | --- |
| drawDisabled | 禁用状态，YES-禁用 NO-不禁用 |
| userId | 操作者标识 |


### onHandupConfirm:approve:userId:()
`- (void)onHandupConfirm:(SEAHandupType)handupType approve:(BOOL)approve userId:(NSString *)userId`

举手处理结果回调

房间成员通过 MeetingKit 中的 `requestHandup:onSuccess:onFailed:()` 接口执行请求举手操作后，房间内管理人员会接收到 SDK 抛出的 `onRoomHandUpChanged:enable:handupType:()`事件，当管理人员可以通过 `adminConfirmHandup:handupType:approve:onSuccess:onFailed:()` 接口执行处理举手操作后，SDK 会抛出该事件通知您。

| 参数 | 描述 |
| :--- | --- |
| handupType | 申请类型，参考文档：[SEAHandupType](https://www.yuque.com/anyconf/eanoso/gkeau9oyh5vms80z#P2v0K) |
| approve | 处理结果，YES-同意 NO-拒绝 |
| userId | 处理人标识 |


### onRoomUserEnterWaitingRoom:nickname:()
`- (void)onRoomUserEnterWaitingRoom:(NSString *)userId nickname:(NSString *)nickname`

远端用户加入等候室回调

用户通过 MeetingKit 中的 `enterRoom:()` 接口执行加入房间操作，同时，如果房间开启了等候室，系统会默认将成员拉入该房间的等候室中，此时，房间内管理员会接收到 SDK 抛出的该事件通知。

| 参数 | 描述 |
| :--- | --- |
| userId | 成员标识 |
| nickname | 成员昵称 |


### onRoomUserExitWaitingRoom:nickname:()
`- (void)onRoomUserExitWaitingRoom:(NSString *)userId nickname:(NSString *)nickname`

远端用户离开等候室回调

用户通过 MeetingKit 中的 `exitWaitingRoom:onSuccess:onFailed:()` 接口执行离开等候室操作，房间内管理员会接收到 SDK 抛出的该事件通知。

| 参数 | 描述 |
| :--- | --- |
| userId | 成员标识 |
| nickname | 成员昵称 |


## **消息事件回调**
### onReceiveChatMessage:message:messageType:()
`- (void)onReceiveChatMessage:(NSString *)senderId message:(NSString *)message messageType:(SEAMessageType)messageType`

收到聊天消息回调

当调用 MeetingKit 中的 `sendRoomChatMessage:messageType:targetId:onSuccess:onFailed:()`或者 `sendRoomCustomMessage:targetId:onSuccess:onFailed:()` 接口执行发送消息操作后，SDK 会抛出该事件通知您。

| 参数 | 描述 |
| --- | --- |
| senderId | 发送者标识 |
| message | 消息内容 |
| messageType | 消息类型，参考文档：[SEAMessageType](https://www.yuque.com/anyconf/eanoso/gkeau9oyh5vms80z#xlxGu) |


### onReceiveSystemMessage:messageType:()
`- (void)onReceiveSystemMessage:(NSString *)message messageType:(SEAMessageType)messageType`

收到系统消息回调

表示收到了系统发送的消息。

| 参数 | 描述 |
| --- | --- |
| message | 消息内容 |
| messageType | 消息类型，参考文档：[SEAMessageType](https://www.yuque.com/anyconf/eanoso/gkeau9oyh5vms80z#xlxGu) |


## **云录制事件回调**
### onCloudRecordStatusChange:status:errMsg:()
`- (void)onCloudRecordStatusChange:(SEARecordType)recordType status:(SEARecordStatus)status errMsg:(nullable NSString *)errMsg`

云录制状态变更回调

当调用 MeetingKit 中的 `startCloudRecord:onSuccess:onFailed:()`或者`stopCloudRecord:onFailed:()` 接口执行开启或停止云录制操作后，SDK 会抛出该事件通知您。

| 参数 | 描述 |
| --- | --- |
| recordType | 录制类型，参考文档：[SEARecordType](https://www.yuque.com/anyconf/smeeting/gkeau9oyh5vms80z#QYWNw) |
| status | 录制状态，参考文档：[SEARecordStatus](https://www.yuque.com/anyconf/smeeting/gkeau9oyh5vms80z#XOsJa) |
| errMsg | 错误描述 |


### onCloudRecordAlarm:taskId:gateway:alarmAt:alarmBrief:()
`- (void)onCloudRecordAlarm:(SEARecordStatus)status taskId:(NSString *)taskId gateway:(NSString *)gateway alarmAt:(NSInteger)alarmAt alarmBrief:(nullable NSString *)alarmBrief`

云录制告警回调

当会议服务检测到云录制出现了异常时，SDK 会抛出该事件通知您。

| 参数 | 描述 |
| --- | --- |
| status | 录制状态，参考文档：[SEARecordStatus](https://www.yuque.com/anyconf/smeeting/gkeau9oyh5vms80z#XOsJa) |
| taskId | 任务标识 |
| gateway | 所在网关 |
| alarmAt | 告警时间 |
| alarmBrief | 告警摘要 |


## **屏幕采集事件回调**
### onScreenRecordStatus:()
`- (void)onScreenRecordStatus:(SEAScreenRecordStatus)status`

屏幕共享状态回调

屏幕录制扩展程序调用 MeetingKit 中的 `broadcastStartedWithAppGroup:delegate:()` 接口执行启动录屏操作后， SDK 会通过 `onScreenRecordStatus:()` 回调抛出当前的屏幕采集状态。

| 参数 | 描述 |
| --- | --- |
| status | 状态码，参考文档：[SEAScreenRecordStatus](https://www.yuque.com/anyconf/eanoso/gkeau9oyh5vms80z#kVZHh) |


## **音频事件回调**
### onAudioRouteChange:previousRoute:()
`- (void)onAudioRouteChange:(SEAAudioRoute)route previousRoute:(SEAAudioRoute)previousRoute`

音频路由变更回调

音频路由发生改变时，SDK 会抛出 `onAudioRouteChange:previousRoute:()` 回调。

参考文档：[SEAAudioRoute](https://www.yuque.com/anyconf/eanoso/gkeau9oyh5vms80z#HhTLs)

| 参数 | 描述 |
| --- | --- |
| route | 音频路由 |
| previousRoute | 变更前的音频路由 |


### onRemoteMemberAudioStatus:()
`- (void)onRemoteMemberAudioStatus:(NSArray<SEAStreamAudioModel *> *)audioArray`

远程成员音频状态数据回调

房间成员音频状态数据回调，包括：音频的分贝值、功率等信息，业务层可通过该回调统计音频数据进行语音激励等操作。

| 参数 | 描述 |
| --- | --- |
| audioArray | 成员音频数据列表，参考文档：[SEAStreamAudioModel](https://www.yuque.com/anyconf/eanoso/gkeau9oyh5vms80z#Lw5lL) |


## **流媒体事件回调**
### onDownBitrateAdaptiveUserId:state:()
`- (void)onDownBitrateAdaptiveUserId:(NSString *)userId state:(SEADownBitrateAdaptiveState)state`

下行码率自适应状态回调

开启码率自适应后，SDK 会根据网络情况动态调整下行成员链路的码率自适应等级。

| 参数 | 描述 |
| --- | --- |
| userId | 用户标识 |
| state | 下行码率自适应状态，参考文档：[SEADownBitrateAdaptiveState](https://www.yuque.com/anyconf/eanoso/gkeau9oyh5vms80z#hHKyj) |


### onUploadBitrateAdaptiveState:()
`- (void)onUploadBitrateAdaptiveState:(SEAUploadBitrateAdaptiveState)state`

上行码率自适应状态回调

开启码率自适应后，SDK 会根据网络情况动态调整上行链路的码率自适应等级。

| 参数 | 描述 |
| --- | --- |
| state | 上行码率自适应状态，参考文档：[SEAUploadBitrateAdaptiveState](https://www.yuque.com/anyconf/eanoso/gkeau9oyh5vms80z#ZryAr) |


### onDownLossLevelChangeState:()
`- (void)onDownLossLevelChangeState:(SEADownLossLevelState)state`

下行平均丢包档位变化回调

| 参数 | 描述 |
| --- | --- |
| state | 下行平均丢包档位，参考文档：[SEADownLossLevelState](https://www.yuque.com/anyconf/eanoso/gkeau9oyh5vms80z#yMw23) |


### onDownLossRateAverage:()
`- (void)onDownLossRateAverage:(CGFloat)average`

下行平均丢包率回调

| 参数 | 描述 |
| --- | --- |
| average | 下行平均丢包率 |


### onSendStreamModel:()
`- (void)onSendStreamModel:(SEAStreamSendModel *)sendModel`

流媒体发送状态数据回调

会在固定时间间隔，会收到来自 `MeetingKitDelegate` 的 `onSendStreamModel:()` 事件回调，描述当前数据发送状态延迟、丢包率等信息。

| 参数 | 描述 |
| --- | --- |
| sendModel | 流媒体发送状态数据，参考文档：[SEAStreamSendModel](https://www.yuque.com/anyconf/eanoso/gkeau9oyh5vms80z#e4l7V) |


### onReceiveStreamModel:()
`- (void)onReceiveStreamModel:(NSArray <SEAStreamReceiveModel *> *)receiveArray`

流媒体接收状态数据回调

会在固定时间间隔，会收到来自 `MeetingKitDelegate` 的 `onReceiveStreamModel:()` 事件回调，描述当前数据接收状态延迟、丢包率等信息。

| 参数 | 描述 |
| --- | --- |
| receiveModel | 流媒体接收状态数据，参考文档：[SEAStreamReceiveModel](https://www.yuque.com/anyconf/eanoso/gkeau9oyh5vms80z#leOhF) |


### onReceiveStreamStatusChange:streamType:status:()
`- (void)onReceiveStreamStatusChange:(NSString *)targetUserId streamType:(SEAVideoStreamType)streamType status:(BOOL)status`

流媒体接收视频流状态变更回调

订阅成员远程视频流后，如果持续一段时间没有收到该成员的视频流，会收到来自 `MeetingKitDelegate` 的 `onReceiveStreamStatusChange:streamType:status:()` 事件回调。同时，接收视频流恢复后也会收到该回调。

| 参数 | 描述 |
| --- | --- |
| targetUserId | 目标成员标识 |
| streamType | 视频流类型，参考文档：[SEAVideoStreamType](https://www.yuque.com/anyconf/eanoso/gkeau9oyh5vms80z#ckLzs) |
| status | 接收状态，YES-超时 NO-恢复 |


### onReceiveMixtureStreamStatusChange:()
`- (void)onReceiveMixtureStreamStatusChange:(BOOL)status`

流媒体接收合成流画面状态变更回调

订阅合成流画面视频流后，如果持续一段时间没有收到合成画面的视频流，会收到来自 `MeetingKitDelegate` 的 `onReceiveMixtureStreamStatusChange:()` 事件回调。同时，接收视频流恢复后也会收到该回调。

| 参数 | 描述 |
| --- | --- |
| status | 接收状态，YES-超时 NO-恢复 |


## **其它事件回调**
### onApplicationPerformance:cpuUsage:()
`- (void)onApplicationPerformance:(CGFloat)memory cpuUsage:(CGFloat)cpuUsage`

应用性能使用情况回调

房间内当前性能使用情况回调。

| 参数 | 描述 |
| --- | --- |
| memory | 内存使用情况 |
| cpuUsage | CUP使用率 |


