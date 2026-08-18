---
title: "MeetingKitRoomDelegate"
description: "会议房间事件回调协议：进出房间、房间设置与主持人操作、成员状态、聊天消息、云录制、屏幕共享、码流质量与签到，每个回调都带事件来源房间实例"
---

本协议承载房间内的一切事件。**全部回调的首参都是事件来源的 [MeetingKitRoom](/zh/meeting/ios/api-reference/MeetingKitRoom) 实例**，多房间场景下通过首参区分事件归属，房间号与会议标识可从 `room.roomNo`、`room.meetingId` 读取。

账号级与设备级事件（音频路由变更、应用性能）请实现 [MeetingKitDelegate](/zh/meeting/ios/api-reference/MeetingKitDelegate)。

```objectivec
@interface YourClass : NSObject <MeetingKitRoomDelegate>
```

<Note>
同一个 `userId` 可能同时出现在多个房间中。在回调里查询成员数据时，请使用首参传入的房间实例（如 `[room findMemberWithUserId:userId]`），不要跨房间复用索引。
</Note>

## 错误事件回调
### meetingRoom:onError:errMsg:()
`- (void)meetingRoom:(MeetingKitRoom *)room onError:(SEAError)errCode errMsg:(nullable NSString *)errMsg`

错误事件回调

表示 SDK 发生不可恢复的错误，比如：加入房间失败或设备开启失败等。这个事件触发一般需要获取新的令牌重新入会。

参考文档：[错误码表](/zh/meeting/ios/error-codes)

| 参数 | 描述 |
| --- | --- |
| room | 事件来源房间实例 |
| errCode | 错误码 |
| errMsg | 错误信息 |

## 连接事件回调
### meetingRoomOnReconnecting:()
`- (void)meetingRoomOnReconnecting:(MeetingKitRoom *)room`

开始重连事件回调

表示 SDK 连接发生异常，正在尝试重连，如：网络抖动等。如中途遇到错误 SDK 会抛出 `meetingRoom:onError:errMsg:()` 回调。

### meetingRoomOnReconnected:()
`- (void)meetingRoomOnReconnected:(MeetingKitRoom *)room`

重连成功事件回调

当 SDK 断线重连成功并且连接已经恢复时，会收到该事件通知。如中途遇到错误 SDK 会抛出 `meetingRoom:onError:errMsg:()` 回调。

## 我的相关回调
### meetingRoom:onEnterRoom:userId:()
`- (void)meetingRoom:(MeetingKitRoom *)room onEnterRoom:(NSString *)meetingId userId:(NSString *)userId`

进入房间事件回调

调用 `MeetingKitRoom` 的 `enterRoom:onSuccess:onFailed:()` 接口执行进入房间操作后，会收到来自 `MeetingKitRoomDelegate` 的 `meetingRoom:onEnterRoom:userId:()` 回调，如遇到错误 SDK 会通过方法中 `onFailed` 参数返回。

| 参数 | 描述 |
| --- | --- |
| room | 事件来源房间实例 |
| meetingId | 会议标识 |
| userId | 用户标识 |


### meetingRoom:onExitRoom:()
`- (void)meetingRoom:(MeetingKitRoom *)room onExitRoom:(SEALeaveReason)reason`

离开房间事件回调

当前用户非主动离开时，会收到该事件通知，如：被主持人踢出房间、会议解散等。

> 值得注意的是，调用 `MeetingKitRoom` 中的 `exitRoom: `接口会执行退出房间的相关逻辑，例如释放音视频设备资源和编解码器资源等。待 SDK 占用的所有资源释放完毕后，SDK 会通过方法携带的 `onSuccess` 参数抛出，你可以在此返回中执行“离开界面”等操作。此时，不会再收到 `meetingRoom:onExitRoom:()` 事件通知。
>

| 参数 | 描述 |
| :--- | --- |
| room | 事件来源房间实例 |
| reason | 离开原因，参考文档：[SEALeaveReason](/zh/meeting/ios/types#sealeavereason) |


### meetingRoom:onUserUpdate:()
`- (void)meetingRoom:(MeetingKitRoom *)room onUserUpdate:(NSString *)userId`

自己数据更新回调

自`2.0.0`起支持。服务端修改当前用户在该房间内的数据后，SDK 会通过该回调通知业务层。

| 参数 | 描述 |
| :--- | --- |
| room | 事件来源房间实例 |
| userId | 用户标识 |

### meetingRoom:onRequestOpenCamera:()
`- (void)meetingRoom:(MeetingKitRoom *)room onRequestOpenCamera:(NSString *)userId`

请求开启摄像头回调

当主持人调用 `MeetingKitRoom` 中的 `adminRequestUserOpenCamera:onSuccess:onFailed:()` 接口执行请求打开你的摄像头操作后，SDK 会抛出该事件通知您。

| 参数 | 描述 |
| :--- | --- |
| room | 事件来源房间实例 |
| userId | 请求者标识 |


### meetingRoom:onRequestOpenMic:()
`- (void)meetingRoom:(MeetingKitRoom *)room onRequestOpenMic:(NSString *)userId`

请求开启麦克风回调

当主持人调用 `MeetingKitRoom` 中的 `adminRequestUserOpenMic:onSuccess:onFailed:()` 接口执行请求打开你的麦克风操作后，SDK 会抛出该事件通知您。

| 参数 | 描述 |
| :--- | --- |
| room | 事件来源房间实例 |
| userId | 请求者标识 |


### meetingRoom:onRequestOpenShare:()
`- (void)meetingRoom:(MeetingKitRoom *)room onRequestOpenShare:(NSString *)userId`

请求开启共享回调

当主持人调用 `MeetingKitRoom` 中的 `adminRequestUserOpenShare:onSuccess:onFailed:()` 接口执行请求打开你的共享操作后，SDK 会抛出该事件通知您。

| 参数 | 描述 |
| :--- | --- |
| room | 事件来源房间实例 |
| userId | 请求者标识 |


### meetingRoom:onRoomMoveInWaitingRoom:()
`- (void)meetingRoom:(MeetingKitRoom *)room onRoomMoveInWaitingRoom:(NSString *)userId`

被管理员移进等候室回调

当主持人调用 `MeetingKitRoom` 中的 `adminMoveInWaitingRoom:nickname:onSuccess:onFailed:()` 接口执行将会议室成员移动到等候室操作后，SDK 会抛出该事件通知您。

| 参数 | 描述 |
| :--- | --- |
| room | 事件来源房间实例 |
| userId | 操作者标识 |


### meetingRoom:onRoomMoveSubMeeting:fromMeetingTitle:toMeetingId:toMeetingTitle:()
`- (void)meetingRoom:(MeetingKitRoom *)room onRoomMoveSubMeeting:(NSString *)fromMeetingId fromMeetingTitle:(NSString *)fromMeetingTitle toMeetingId:(NSString *)toMeetingId toMeetingTitle:(NSString *)toMeetingTitle`

被管理员移进小组会议或主会场回调

当主持人调用 `MeetingKitRoom` 中的 `adminMoveSubMeetingUser:fromGroupId:toGroupId:onSuccess:onFailed:()` 接口执行将您移进小组会议或主会场操作后，SDK 会抛出该事件通知您。

| 参数 | 描述 |
| :--- | --- |
| room | 事件来源房间实例 |
| fromMeetingId | 原小组会议标识 |
| fromMeetingTitle | 原小组会议标题 |
| toMeetingId | 目标小组会议标识 |
| toMeetingTitle | 目标小组会议标题 |

## 房间事件回调
### meetingRoom:onRoomCameraStateChanged:selfUnmuteCameraDisabled:userId:()
`- (void)meetingRoom:(MeetingKitRoom *)room onRoomCameraStateChanged:(BOOL)cameraDisabled selfUnmuteCameraDisabled:(BOOL)selfUnmuteCameraDisabled userId:(NSString *)userId`

房间摄像头禁用状态变更回调

当主持人调用 `MeetingKitRoom` 中的 `adminUpdateRoomCameraState:selfUnmuteCameraDisabled:onSuccess:onFailed:()` 接口执行更新房间全体禁视频操作后，SDK 会抛出该事件通知您。

| 参数 | 描述 |
| --- | --- |
| room | 事件来源房间实例 |
| cameraDisabled | 房间视频禁用状态，YES-禁用 NO-不禁用 |
| selfUnmuteCameraDisabled | 是否禁止自我解除视频状态，YES-禁止 NO-不禁止 |
| userId | 操作者标识 |


### meetingRoom:onRoomMicStateChanged:selfUnmuteMicDisabled:userId:()
`- (void)meetingRoom:(MeetingKitRoom *)room onRoomMicStateChanged:(BOOL)micDisabled selfUnmuteMicDisabled:(BOOL)selfUnmuteMicDisabled userId:(NSString *)userId`

房间麦克风禁用状态变更回调

当主持人调用 `MeetingKitRoom` 中的 `adminUpdateRoomMicState:selfUnmuteMicDisabled:onSuccess:onFailed:()` 接口执行更新房间全体禁音频操作后，SDK 会抛出该事件通知您。

| 参数 | 描述 |
| --- | --- |
| room | 事件来源房间实例 |
| cameraDisabled | 房间音频禁用状态，YES-禁用 NO-不禁用 |
| selfUnmuteCameraDisabled | 是否禁止自我解除音频状态，YES-禁止 NO-不禁止 |
| userId | 操作者标识 |


### meetingRoom:onRoomChatDisabledChanged:userId:()
`- (void)meetingRoom:(MeetingKitRoom *)room onRoomChatDisabledChanged:(BOOL)chatDisabled userId:(NSString *)userId`

房间聊天禁用状态变更回调

当主持人调用 `MeetingKitRoom` 中的 `adminUpdateRoomChatDisabled:onSuccess:onFailed:()` 接口执行更新房间聊天禁用状态操作后，SDK 会抛出该事件通知您。

| 参数 | 描述 |
| --- | --- |
| room | 事件来源房间实例 |
| chatDisabled | 禁用状态，YES-禁用 NO-不禁用 |
| userId | 操作者标识 |


### meetingRoom:onRoomShareDisabledChanged:userId:()
`- (void)meetingRoom:(MeetingKitRoom *)room onRoomShareDisabledChanged:(BOOL)shareDisabled userId:(NSString *)userId`

房间共享禁用状态变更回调

当主持人调用 `MeetingKitRoom` 中的 `adminUpdateRoomShareDisabled:onSuccess:onFailed:()` 接口执行更新房间共享禁用状态操作后，SDK 会抛出该事件通知您。

| 参数 | 描述 |
| --- | --- |
| room | 事件来源房间实例 |
| shareDisabled | 禁用状态，YES-禁用 NO-不禁用 |
| userId | 操作者标识 |


### meetingRoom:onRoomScreenshotDisabledChanged:userId:()
`- (void)meetingRoom:(MeetingKitRoom *)room onRoomScreenshotDisabledChanged:(BOOL)screenshotDisabled userId:(NSString *)userId`

房间截图禁用状态变更回调

当主持人调用 `MeetingKitRoom` 中的 `adminUpdateRoomScreenshotDisabled:onSuccess:onFailed:()` 接口执行更新房间截屏开关状态操作后，SDK 会抛出该事件通知您。

| 参数 | 描述 |
| --- | --- |
| room | 事件来源房间实例 |
| screenshotDisabled | 禁用状态，YES-禁用 NO-不禁用 |
| userId | 操作者标识 |


### meetingRoom:onRoomWatermarkDisabledChanged:userId:()
`- (void)meetingRoom:(MeetingKitRoom *)room onRoomWatermarkDisabledChanged:(BOOL)watermarkDisabled userId:(NSString *)userId`

房间水印禁用状态变更回调

当主持人调用 `MeetingKitRoom` 中的 `adminUpdateRoomWatermarkDisabled:onSuccess:onFailed:()` 接口执行更新房间水印开关状态操作后，SDK 会抛出该事件通知您。

| 参数 | 描述 |
| --- | --- |
| room | 事件来源房间实例 |
| watermarkDisabled | 禁用状态，YES-禁用 NO-不禁用 |
| userId | 操作者标识 |


### meetingRoom:onRoomWaitingRoomDisabledChanged:userId:()
`- (void)meetingRoom:(MeetingKitRoom *)room onRoomWaitingRoomDisabledChanged:(BOOL)waitingRoomDisabled userId:(NSString *)userId`

房间等候室禁用状态变更回调

当主持人调用 `MeetingKitRoom` 中的 `adminUpdateWaitingRoomDisabled:onSuccess:onFailed:()` 接口执行更新房间等候室禁用状态操作后，SDK 会抛出该事件通知您。

| 参数 | 描述 |
| --- | --- |
| room | 事件来源房间实例 |
| waitingRoomDisabled | 禁用状态，YES-禁用 NO-不禁用 |
| userId | 操作者标识 |


### meetingRoom:onRoomLockedChanged:userId:()
`- (void)meetingRoom:(MeetingKitRoom *)room onRoomLockedChanged:(BOOL)locked userId:(NSString *)userId`

房间锁定状态变化回调

当主持人调用 `MeetingKitRoom` 中的 `adminUpdateRoomLocked:onSuccess:onFailed:()` 接口执行更新房间锁定状态操作后，SDK 会抛出该事件通知您。

| 参数 | 描述 |
| --- | --- |
| room | 事件来源房间实例 |
| locked | 锁定状态，YES-开启 NO-关闭 |
| userId | 操作者标识 |


### meetingRoom:onRoomMoveHost:sourceUserId:()
`- (void)meetingRoom:(MeetingKitRoom *)room onRoomMoveHost:(NSString *)userId sourceUserId:(NSString *)sourceUserId`

房间转移主持人回调

当主持人调用 `MeetingKitRoom` 中的 `adminMoveHost:onSuccess:onFailed:()` 接口执行转移主持人操作后，SDK 会抛出该事件通知您。

| 参数 | 描述 |
| --- | --- |
| room | 事件来源房间实例 |
| userId | 新主持人用户标识 |
| sourceUserId | 原主持人用户标识 |


### meetingRoom:onRoomShareStart:shareType:()
`- (void)meetingRoom:(MeetingKitRoom *)room onRoomShareStart:(NSString *)userId shareType:(SEAShareType)shareType`

共享开始回调

当参会成员调用 `MeetingKitRoom` 中的 `requestShare:onSuccess:onFailed:()` 接口执行请求开启共享操作后，SDK 会抛出该事件通知您。

> 特别说明：如果当前房间正有成员开启着共享，后续加入的成员也会收到该事件通知。
>

| 参数 | 描述 |
| --- | --- |
| room | 事件来源房间实例 |
| userId | 共享成员标识 |
| shareType | 共享类型，参考文档：[SEAShareType](/zh/meeting/ios/types#seasharetype) |


### meetingRoom:onRoomShareStop:shareType:()
`- (void)meetingRoom:(MeetingKitRoom *)room onRoomShareStop:(NSString *)userId shareType:(SEAShareType)shareType`

共享结束回调

当参会成员调用 `MeetingKitRoom` 中的 `stopShare:onFailed:()` 接口执行关闭共享操作后，SDK 会抛出该事件通知您。

> 特别说明：如果共享成员在未结束共享情况直接执行离开房间操作，此时其他成员会先收到 `stopShare:onFailed:()` 事件通知再收到 `onUserExit:`事件通知。
>

| 参数 | 描述 |
| --- | --- |
| room | 事件来源房间实例 |
| userId | 共享成员标识 |
| shareType | 共享类型，参考文档：[SEAShareType](/zh/meeting/ios/types#seasharetype) |


### meetingRoom:onAdminRoomShareStop:shareType:()
`- (void)meetingRoom:(MeetingKitRoom *)room onAdminRoomShareStop:(NSString *)userId shareType:(SEAShareType)shareType`

主持人结束房间共享回调

当主持人调用 `MeetingKitRoom` 中的 `adminStopRoomShare:onFailed:()` 接口执行关闭成员共享操作后，SDK 会抛出该事件通知您。

| 参数 | 描述 |
| --- | --- |
| room | 事件来源房间实例 |
| userId | 共享成员标识 |
| shareType | 共享类型，参考文档：[SEAShareType](/zh/meeting/ios/types#seasharetype) |


### meetingRoom:onRoomHandUpChanged:enable:handupType:()
`- (void)meetingRoom:(MeetingKitRoom *)room onRoomHandUpChanged:(NSString *)userId enable:(BOOL)enable handupType:(SEAHandupType)handupType`

房间成员举手状态变化回调

当成员调用 `MeetingKitRoom` 中的 `requestHandup:onSuccess:onFailed:()` 接口执行请求举手操作后，如果您恰是房间管理角色时，SDK 会抛出该事件通知您。

| 参数 | 描述 |
| --- | --- |
| room | 事件来源房间实例 |
| userId | 成员标识 |
| enable | 举手状态，YES-申请举手 NO-取消举手 |
| shareType | 举手申请类型，参考文档：[SEAHandupType](/zh/meeting/ios/types#seahanduptype) |


### meetingRoom:onRoomSubMeetingStart:title:conferee:()
`- (void)meetingRoom:(MeetingKitRoom *)room onRoomSubMeetingStart:(NSString *)meetingId title:(NSString *)title conferee:(nullable NSArray <NSString *> *)conferee`

房间讨论组开始回调

当成员调用 `MeetingKitRoom` 中的 `adminStartSubMeeting:onSuccess:onFailed:()` 接口执行开始小组会议操作后，SDK 会抛出该事件通知您。

| 参数 | 描述 |
| --- | --- |
| room | 事件来源房间实例 |
| meetingId | 会议标识 |
| title | 小组名称 |
| conferee | 参会成员标识列表 |


### meetingRoom:onRoomSubMeetingStop:()
`- (void)meetingRoom:(MeetingKitRoom *)room onRoomSubMeetingStop:(NSString *)parentMid`

房间讨论组结束回调

当成员调用 `MeetingKitRoom` 中的 `adminStopSubMeeting:onSuccess:onFailed:()` 接口执行结束小组会议操作后，SDK 会抛出该事件通知您。

| 参数 | 描述 |
| :--- | --- |
| room | 事件来源房间实例 |
| parentMid | 上级会议标识 |


### meetingRoom:onRoomMeetingTitleChanged:()
`- (void)meetingRoom:(MeetingKitRoom *)room onRoomMeetingTitleChanged:(NSString *)title`

房间会议标题变化回调

当管理员调用 `MeetingKitRoom` 中的 `adminUpdateSubMeetingTitle:targetId:onSuccess:onFailed:()` 接口执行修改小组会议标题操作后，SDK 会抛出该事件通知您。

| 参数 | 描述 |
| :--- | --- |
| room | 事件来源房间实例 |
| title | 会议标题 |

## 用户事件回调
### meetingRoom:onUserEnter:()
`- (void)meetingRoom:(MeetingKitRoom *)room onUserEnter:(NSString *)userId`

成员进入房间回调，包括当前用户。

当远端用户调用 `MeetingKitRoom` 的 `enterRoom:onSuccess:onFailed:()` 接口执行加入房间操作后，SDK 会抛出该事件通知您。

| 参数 | 描述 |
| :--- | --- |
| room | 事件来源房间实例 |
| userId | 成员标识 |


### meetingRoom:onUserExit:()
`- (void)meetingRoom:(MeetingKitRoom *)room onUserExit:(NSString *)userId`

成员退出房间回调，包括当前用户。

当远端用户调用 `MeetingKitRoom` 中的 `exitRoom:()` 接口执行离开房间操作后，SDK 会抛出该事件通知您。

| 参数 | 描述 |
| :--- | --- |
| room | 事件来源房间实例 |
| userId | 成员标识 |


### meetingRoom:onUserNameChanged:nickname:()
`- (void)meetingRoom:(MeetingKitRoom *)room onUserNameChanged:(NSString *)targetUserId nickname:(NSString *)nickname`

用户昵称变化回调

当成员调用 `MeetingKitRoom` 中的 `updateName:onSuccess:onFailed:()` 接口或者主持人调用 `adminUpdateNickname:nickname:onSuccess:onFailed:()` 接口执行更新用户昵称操作后，SDK 会抛出该事件通知您。

| 参数 | 描述 |
| :--- | --- |
| room | 事件来源房间实例 |
| targetUserId | 目标成员标识 |
| nickname | 用户昵称 |


### meetingRoom:onUserRoleChanged:userRole:()
`- (void)meetingRoom:(MeetingKitRoom *)room onUserRoleChanged:(NSString *)targetUserId userRole:(SEAUserRole)userRole`

用户角色变化回调

房间管理人员调用 `MeetingKitRoom` 中的 `adminUpdateUserRole:userRole:onSuccess:onFailed:()` 接口执行更新用户角色操作后，SDK 会抛出该事件通知您。

| 参数 | 描述 |
| :--- | --- |
| room | 事件来源房间实例 |
| targetUserId | 目标成员标识 |
| userRole | 用户角色，参考文档：[SEAUserRole](/zh/meeting/ios/types#seauserrole) |


### meetingRoom:onUserCameraStateChanged:cameraState:reason:()
`- (void)meetingRoom:(MeetingKitRoom *)room onUserCameraStateChanged:(NSString *)targetUserId cameraState:(SEADeviceState)cameraState reason:(SEAChangeReason)reason`

用户摄像头状态变化回调

房间成员通过 `MeetingKitRoom` 中的 `requestOpenCamera:view:onSuccess:onFailed:()` 或 `closeCamera:onFailed:()` 接口执行打开/关闭摄像头操作，以及房间管理人员通过 `MeetingKitRoom` 中的 `adminCloseUserCamera:onSuccess:onFailed:()` 接口执行关闭远端用户摄像头操作后，SDK 会抛出该事件通知您。

> 特别说明：当在你加入房间之前已经有成员打开了摄像头，在你加入房间时也会抛出该事件。
>

| 参数 | 描述 |
| :--- | --- |
| room | 事件来源房间实例 |
| targetUserId | 目标成员标识 |
| cameraState | 摄像头状态，参考文档：[SEADeviceState](/zh/meeting/ios/types#seadevicestate) |
| reason | 发生变化原因，参考文档：[SEAChangeReason](/zh/meeting/ios/types#seachangereason) |


### meetingRoom:onUserMicStateChanged:micState:reason:()
`- (void)meetingRoom:(MeetingKitRoom *)room onUserMicStateChanged:(NSString *)targetUserId micState:(SEADeviceState)micState reason:(SEAChangeReason)reason`

用户麦克风状态变化回调

房间成员通过 `MeetingKitRoom` 中的 `requestOpenMic:onFailed:()` 或 `closeMic:onFailed:()` 接口执行打开/关闭麦克风操作，以及房间管理人员通过 `MeetingKitRoom` 中的 `adminCloseUserMic:onSuccess:onFailed:()` 接口执行关闭远端用户麦克风操作后，SDK 会抛出该事件通知您。

> 特别说明：当在你加入房间之前已经有成员打开了麦克风，在你加入房间时也会抛出该事件。
>

| 参数 | 描述 |
| :--- | --- |
| room | 事件来源房间实例 |
| targetUserId | 目标成员标识 |
| micState | 麦克风状态，参考文档：[SEADeviceState](/zh/meeting/ios/types#seadevicestate) |
| reason | 发生变化原因，参考文档：[SEAChangeReason](/zh/meeting/ios/types#seachangereason) |


### meetingRoom:onUserChatDisabledChanged:userId:()
`- (void)meetingRoom:(MeetingKitRoom *)room onUserChatDisabledChanged:(BOOL)chatDisabled userId:(NSString *)userId`

用户聊天能力禁用状态变化回调

房间管理人员通过 `MeetingKitRoom` 中的 `adminUpdateUserChatDisabled:chatDisabled:onSuccess:onFailed:()` 接口执行更新用户聊天状态操作后，SDK 会抛出该事件通知您。

| 参数 | 描述 |
| :--- | --- |
| room | 事件来源房间实例 |
| chatDisabled | 禁用状态，YES-禁用 NO-不禁用 |
| userId | 操作者标识 |


### meetingRoom:onUserDrawDisabledChanged:userId:()
`- (void)meetingRoom:(MeetingKitRoom *)room onUserDrawDisabledChanged:(BOOL)drawDisabled userId:(NSString *)userId`

用户涂鸦能力禁用状态变化回调

房间管理人员通过 `MeetingKitRoom` 中的 `adminUpdateUserDrawDisabled:drawDisabled:onSuccess:onFailed:()` 接口执行更新用户涂鸦状态操作后，SDK 会抛出该事件通知您。

| 参数 | 描述 |
| :--- | --- |
| room | 事件来源房间实例 |
| drawDisabled | 禁用状态，YES-禁用 NO-不禁用 |
| userId | 操作者标识 |


### meetingRoom:onHandupConfirm:approve:userId:()
`- (void)meetingRoom:(MeetingKitRoom *)room onHandupConfirm:(SEAHandupType)handupType approve:(BOOL)approve userId:(NSString *)userId`

举手处理结果回调

房间成员通过 `MeetingKitRoom` 中的 `requestHandup:onSuccess:onFailed:()` 接口执行请求举手操作后，房间内管理人员会接收到 SDK 抛出的 `meetingRoom:onRoomHandUpChanged:enable:handupType:()`事件，当管理人员可以通过 `adminConfirmHandup:handupType:approve:onSuccess:onFailed:()` 接口执行处理举手操作后，SDK 会抛出该事件通知您。

| 参数 | 描述 |
| :--- | --- |
| room | 事件来源房间实例 |
| handupType | 申请类型，参考文档：[SEAHandupType](/zh/meeting/ios/types#seahanduptype) |
| approve | 处理结果，YES-同意 NO-拒绝 |
| userId | 处理人标识 |


### meetingRoom:onRoomUserEnterWaitingRoom:nickname:()
`- (void)meetingRoom:(MeetingKitRoom *)room onRoomUserEnterWaitingRoom:(NSString *)userId nickname:(NSString *)nickname`

远端用户加入等候室回调

用户通过 `MeetingKitRoom` 中的 `enterRoom:()` 接口执行加入房间操作，同时，如果房间开启了等候室，系统会默认将成员拉入该房间的等候室中，此时，房间内管理员会接收到 SDK 抛出的该事件通知。

| 参数 | 描述 |
| :--- | --- |
| room | 事件来源房间实例 |
| userId | 成员标识 |
| nickname | 成员昵称 |


### meetingRoom:onRoomUserExitWaitingRoom:nickname:()
`- (void)meetingRoom:(MeetingKitRoom *)room onRoomUserExitWaitingRoom:(NSString *)userId nickname:(NSString *)nickname`

远端用户离开等候室回调

用户通过 `MeetingKitRoom` 中的 `exitWaitingRoom:onSuccess:onFailed:()` 接口执行离开等候室操作，房间内管理员会接收到 SDK 抛出的该事件通知。

| 参数 | 描述 |
| :--- | --- |
| room | 事件来源房间实例 |
| userId | 成员标识 |
| nickname | 成员昵称 |

## 消息事件回调
### meetingRoom:onReceiveChatMessage:message:messageType:()
`- (void)meetingRoom:(MeetingKitRoom *)room onReceiveChatMessage:(NSString *)senderId message:(NSString *)message messageType:(SEAMessageType)messageType`

收到聊天消息回调

当调用 `MeetingKitRoom` 中的 `sendRoomChatMessage:messageType:targetId:onSuccess:onFailed:()`或者 `sendRoomCustomMessage:targetId:onSuccess:onFailed:()` 接口执行发送消息操作后，SDK 会抛出该事件通知您。

| 参数 | 描述 |
| --- | --- |
| room | 事件来源房间实例 |
| senderId | 发送者标识 |
| message | 消息内容 |
| messageType | 消息类型，参考文档：[SEAMessageType](/zh/meeting/ios/types#seamessagetype) |


### meetingRoom:onReceiveSystemMessage:messageType:()
`- (void)meetingRoom:(MeetingKitRoom *)room onReceiveSystemMessage:(NSString *)message messageType:(SEAMessageType)messageType`

收到系统消息回调

表示收到了系统发送的消息。

| 参数 | 描述 |
| --- | --- |
| room | 事件来源房间实例 |
| message | 消息内容 |
| messageType | 消息类型，参考文档：[SEAMessageType](/zh/meeting/ios/types#seamessagetype) |


### meetingRoom:onReceiveCustomMessage:action:userId:sessionId:nickname:()
`- (void)meetingRoom:(MeetingKitRoom *)room onReceiveCustomMessage:(NSString *)content action:(NSString *)action userId:(nullable NSString *)userId sessionId:(nullable NSString *)sessionId nickname:(nullable NSString *)nickname`

接收自定义消息回调

自`2.0.0`起支持。业务层通过服务端下发的房间自定义消息，SDK 会通过该回调透传给对应房间。

| 参数 | 描述 |
| :--- | --- |
| room | 事件来源房间实例 |
| content | 消息内容 |
| action | 消息标识 |
| userId | 用户标识 |
| sessionId | 会话标识 |
| nickname | 用户昵称 |

## 云录制事件回调
### meetingRoom:onCloudRecordStatusChange:status:errMsg:()
`- (void)meetingRoom:(MeetingKitRoom *)room onCloudRecordStatusChange:(SEARecordType)recordType status:(SEARecordStatus)status errMsg:(nullable NSString *)errMsg`

云录制状态变更回调

当调用 `MeetingKitRoom` 中的 `startCloudRecord:onSuccess:onFailed:()`或者`stopCloudRecord:onFailed:()` 接口执行开启或停止云录制操作后，SDK 会抛出该事件通知您。

| 参数 | 描述 |
| --- | --- |
| room | 事件来源房间实例 |
| recordType | 录制类型，参考文档：[SEARecordType](/zh/meeting/ios/types#searecordtype) |
| status | 录制状态，参考文档：[SEARecordStatus](/zh/meeting/ios/types#searecordstatus) |
| errMsg | 错误描述 |


### meetingRoom:onCloudRecordAlarm:taskId:gateway:alarmAt:alarmBrief:()
`- (void)meetingRoom:(MeetingKitRoom *)room onCloudRecordAlarm:(SEARecordStatus)status taskId:(NSString *)taskId gateway:(NSString *)gateway alarmAt:(NSInteger)alarmAt alarmBrief:(nullable NSString *)alarmBrief`

云录制告警回调

当会议服务检测到云录制出现了异常时，SDK 会抛出该事件通知您。

| 参数 | 描述 |
| --- | --- |
| room | 事件来源房间实例 |
| status | 录制状态，参考文档：[SEARecordStatus](/zh/meeting/ios/types#searecordstatus) |
| taskId | 任务标识 |
| gateway | 所在网关 |
| alarmAt | 告警时间 |
| alarmBrief | 告警摘要 |

## 屏幕采集事件回调
### meetingRoom:onScreenRecordStatus:()
`- (void)meetingRoom:(MeetingKitRoom *)room onScreenRecordStatus:(SEAScreenRecordStatus)status`

屏幕共享状态回调

屏幕录制扩展程序调用 `MeetingKit` 中的 `broadcastStartedWithAppGroup:delegate:()` 接口执行启动录屏操作后， SDK 会通过 `meetingRoom:onScreenRecordStatus:()` 回调抛出当前的屏幕采集状态。

| 参数 | 描述 |
| --- | --- |
| room | 事件来源房间实例 |
| status | 状态码，参考文档：[SEAScreenRecordStatus](/zh/meeting/ios/types#seascreenrecordstatus) |

## 音频事件回调
### meetingRoom:onRemoteMemberAudioStatus:()
`- (void)meetingRoom:(MeetingKitRoom *)room onRemoteMemberAudioStatus:(NSArray<SEAStreamAudioModel *> *)audioArray`

远程成员音频状态数据回调

房间成员音频状态数据回调，包括：音频的分贝值、功率等信息，业务层可通过该回调统计音频数据进行语音激励等操作。

| 参数 | 描述 |
| --- | --- |
| room | 事件来源房间实例 |
| audioArray | 成员音频数据列表，参考文档：[SEAStreamAudioModel](/zh/meeting/ios/types#seastreamaudiomodel) |

## 流媒体事件回调
### meetingRoom:onDownBitrateAdaptiveUserId:state:()
`- (void)meetingRoom:(MeetingKitRoom *)room onDownBitrateAdaptiveUserId:(NSString *)userId state:(SEADownBitrateAdaptiveState)state`

下行码率自适应状态回调

开启码率自适应后，SDK 会根据网络情况动态调整下行成员链路的码率自适应等级。

| 参数 | 描述 |
| --- | --- |
| room | 事件来源房间实例 |
| userId | 用户标识 |
| state | 下行码率自适应状态，参考文档：[SEADownBitrateAdaptiveState](/zh/meeting/ios/types#seadownbitrateadaptivestate) |


### meetingRoom:onUploadBitrateAdaptiveState:()
`- (void)meetingRoom:(MeetingKitRoom *)room onUploadBitrateAdaptiveState:(SEAUploadBitrateAdaptiveState)state`

上行码率自适应状态回调

开启码率自适应后，SDK 会根据网络情况动态调整上行链路的码率自适应等级。

| 参数 | 描述 |
| --- | --- |
| room | 事件来源房间实例 |
| state | 上行码率自适应状态，参考文档：[SEAUploadBitrateAdaptiveState](/zh/meeting/ios/types#seauploadbitrateadaptivestate) |


### meetingRoom:onDownLossLevelChangeState:()
`- (void)meetingRoom:(MeetingKitRoom *)room onDownLossLevelChangeState:(SEADownLossLevelState)state`

下行平均丢包档位变化回调

| 参数 | 描述 |
| --- | --- |
| room | 事件来源房间实例 |
| state | 下行平均丢包档位，参考文档：[SEADownLossLevelState](/zh/meeting/ios/types#seadownlosslevelstate) |


### meetingRoom:onDownLossRateAverage:()
`- (void)meetingRoom:(MeetingKitRoom *)room onDownLossRateAverage:(CGFloat)average`

下行平均丢包率回调

| 参数 | 描述 |
| --- | --- |
| room | 事件来源房间实例 |
| average | 下行平均丢包率 |


### meetingRoom:onSendStreamModel:()
`- (void)meetingRoom:(MeetingKitRoom *)room onSendStreamModel:(SEAStreamSendModel *)sendModel`

流媒体发送状态数据回调

会在固定时间间隔，会收到来自 `MeetingKitRoomDelegate` 的 `meetingRoom:onSendStreamModel:()` 事件回调，描述当前数据发送状态延迟、丢包率等信息。

| 参数 | 描述 |
| --- | --- |
| room | 事件来源房间实例 |
| sendModel | 流媒体发送状态数据，参考文档：[SEAStreamSendModel](/zh/meeting/ios/types#seastreamsendmodel) |


### meetingRoom:onReceiveStreamModel:()
`- (void)meetingRoom:(MeetingKitRoom *)room onReceiveStreamModel:(NSArray <SEAStreamReceiveModel *> *)receiveArray`

流媒体接收状态数据回调

会在固定时间间隔，会收到来自 `MeetingKitRoomDelegate` 的 `meetingRoom:onReceiveStreamModel:()` 事件回调，描述当前数据接收状态延迟、丢包率等信息。

| 参数 | 描述 |
| --- | --- |
| room | 事件来源房间实例 |
| receiveModel | 流媒体接收状态数据，参考文档：[SEAStreamReceiveModel](/zh/meeting/ios/types#seastreamreceivemodel) |


### meetingRoom:onSendQualityModel:()
`- (void)meetingRoom:(MeetingKitRoom *)room onSendQualityModel:(SEAStreamQualityModel *)qualityModel`

流媒体上行质量数据回调

会在固定时间间隔，会收到来自 `MeetingKitRoomDelegate` 的 `meetingRoom:onSendQualityModel:()` 事件回调，描述当前数据发送状态延迟、丢包率等信息。

| 参数 | 描述 |
| --- | --- |
| room | 事件来源房间实例 |
| qualityModel | 流媒体质量数据，参考文档：[SEAStreamQualityModel]() |


### meetingRoom:onReceiveQualityModel:()
`- (void)meetingRoom:(MeetingKitRoom *)room onReceiveQualityModel:(SEAStreamQualityModel *)qualityModel`

流媒体下行质量数据回调

会在固定时间间隔，会收到来自 `MeetingKitRoomDelegate` 的 `meetingRoom:onReceiveQualityModel:()` 事件回调，描述当前数据接收状态延迟、丢包率等信息。

| 参数 | 描述 |
| --- | --- |
| room | 事件来源房间实例 |
| qualityModel | 流媒体质量数据，参考文档：[SEAStreamQualityModel]() |


### meetingRoom:onReceiveStreamStatusChange:streamType:status:()
`- (void)meetingRoom:(MeetingKitRoom *)room onReceiveStreamStatusChange:(NSString *)targetUserId streamType:(SEAVideoStreamType)streamType status:(BOOL)status`

流媒体接收视频流状态变更回调

订阅成员远程视频流后，如果持续一段时间没有收到该成员的视频流，会收到来自 `MeetingKitRoomDelegate` 的 `meetingRoom:onReceiveStreamStatusChange:streamType:status:()` 事件回调。同时，接收视频流恢复后也会收到该回调。

| 参数 | 描述 |
| --- | --- |
| room | 事件来源房间实例 |
| targetUserId | 目标成员标识 |
| streamType | 视频流类型，参考文档：[SEAVideoStreamType](/zh/meeting/ios/types#seavideostreamtype) |
| status | 接收状态，YES-超时 NO-恢复 |


### meetingRoom:onReceiveMixtureStreamStatusChange:()
`- (void)meetingRoom:(MeetingKitRoom *)room onReceiveMixtureStreamStatusChange:(BOOL)status`

流媒体接收合成流画面状态变更回调

订阅合成流画面视频流后，如果持续一段时间没有收到合成画面的视频流，会收到来自 `MeetingKitRoomDelegate` 的 `meetingRoom:onReceiveMixtureStreamStatusChange:()` 事件回调。同时，接收视频流恢复后也会收到该回调。

| 参数 | 描述 |
| --- | --- |
| room | 事件来源房间实例 |
| status | 接收状态，YES-超时 NO-恢复 |


### meetingRoom:onReceiveRetweetStreamStatusChange:status:()
`- (void)meetingRoom:(MeetingKitRoom *)room onReceiveRetweetStreamStatusChange:(NSString *)streamName status:(BOOL)status`

流媒体接收转推流画面状态变更回调

订阅远端转推流后，如果持续一段时间没有收到转推画面的视频流，会收到来自 `MeetingKitRoomDelegate` 的 `meetingRoom:onReceiveRetweetStreamStatusChange:status:()` 事件回调。同时，接收视频流恢复后也会收到该回调。可在该回调中按 `streamName` 区分对应转推流，显示/隐藏加载指示（如 `UIActivityIndicatorView`）。

| 参数 | 描述 |
| --- | --- |
| room | 事件来源房间实例 |
| streamName | 转推流名 |
| status | 接收状态，YES-超时 NO-恢复 |

## 其它事件回调
### meetingRoom:onExtendedEvents:content:()
`- (void)meetingRoom:(MeetingKitRoom *)room onExtendedEvents:(NSString *)event content:(NSString *)content`

扩展事件回调

房间内业务层自定义的扩展事件回调。

| 参数 | 描述 |
| --- | --- |
| room | 事件来源房间实例 |
| event | 事件类型 |
| content | 数据内容 |

## 签到事件回调
### meetingRoom:onSignInActivity:epoch:beginAt:dur:endAt:desc:()
`- (void)meetingRoom:(MeetingKitRoom *)room onSignInActivity:(NSString *)userId epoch:(NSInteger)epoch beginAt:(NSInteger)beginAt dur:(NSInteger)dur endAt:(NSInteger)endAt desc:(nullable NSString *)desc`

签到活动回调

当主持人调用 `MeetingKitRoom` 中的 `signInCreate:desc:onSuccess:onFailed:()` 接口执行创建签到活动后，SDK 会抛出该事件通知您。

| 参数 | 描述 |
| --- | --- |
| room | 事件来源房间实例 |
| userId | 发起人标识 |
| epoch | 签到轮次 |
| beginAt | 开始时间 |
| dur | 签到时长，单位：分钟，0为不限时 |
| endAt | 结束时间 |
| desc | 签到描述 |


### meetingRoom:onSignInFinish:epoch:()
`- (void)meetingRoom:(MeetingKitRoom *)room onSignInFinish:(NSString *)userId epoch:(NSInteger)epoch`

签到结束回调

当主持人调用 `MeetingKitRoom` 中的 `signInFinish:onFailed:()` 接口执行结束签到活动后，SDK 会抛出该事件通知您。

| 参数 | 描述 |
| --- | --- |
| room | 事件来源房间实例 |
| userId | 发起人标识 |
| epoch | 签到轮次 |
