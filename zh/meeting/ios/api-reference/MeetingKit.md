---
title: "MeetingKit"
description: "iOS SMeeting 会议 SDK MeetingKit 接口参考"
---

## 核心基础接口
### sharedInstance()
`+ (MeetingKit *)sharedInstance`

创建 MeetingKit 实例（单例模式）。

### version()
`- (NSString *)version`

获取 MeetingKit 版本号。

### addDelegate:()
`- (void)addDelegate:(id <MeetingKitDelegate>)delegate`

设置 MeetingKit 事件回调

您可以通过 `MeetingKitDelegate` 协议获得各类回调事件通知，例如：错误码，远端用户进房间，音视频状态参数等）。

| 参数 | 描述 |
| :--- | --- |
| delegate | 监听实例 |


### loginWithToken:appGroup:onSuccess:onFailed:()
`- (void)loginWithToken:(NSString *)token appGroup:(NSString *)appGroup onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

登录接口，您需要先初始化用户信息后才能进入房间，并进行一系列的操作。

| 参数 | 描述 |
| :--- | --- |
| token | 用户令牌 |
| appGroup | 应用分组标识符 |
| onSuccess | 成功回调 |
| onFailed | 失败回调 |


### logout()
`- (void)logout`

退出登录接口，会有主动离开房间操作、销毁资源等。

## 即时通讯接口
### enableImWithDelegate:onSuccess:onFailed:()
`- (void)enableImWithDelegate:(nullable id<MeetingKitIMDelegate>)delegate onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

启用即时通讯

调用该接口开启 SDK 即时通讯服务，开发者可以利用该服务实现，如会前呼叫、通知等业务功能。

| 参数 | 描述 |
| :--- | --- |
| delegate | 委托代理，参考文档：[MeetingKitIMDelegate](https://www.yuque.com/anyconf/eanoso/wh4gigxazm9esngc) |
| onSuccess | 成功回调 |
| onFailed | 失败回调 |


### disableIm()
`- (void)disableIm`

停用即时通讯

当您不再需要即时通讯服务时，可通过该接口进行停用。

## 通话操作接口
### callUser:onSuccess:onFailed:()
`- (void)callUser:(NSArray <NSString *> *)userIdLists onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

发起通话

会中主持人可以通过该接口呼叫成员，呼叫成员后，SDK会通过 `MeetingKitIMDelegate` 中的 [onCallReceived:nickname:roomNo:title:()](https://www.yuque.com/anyconf/eanoso/wh4gigxazm9esngc#Vjtg3) 回调通知对应用户。

| 参数 | 描述 |
| :--- | --- |
| userIdLists | 用户标识列表 |
| onSuccess | 成功回调 |
| onFailed | 失败回调 |


## 会议操作接口
### getMeetingList:onFailed:()
`- (void)getMeetingList:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

获取会议列表

| 参数 | 描述 |
| :--- | --- |
| onSuccess | 成功回调，参考文档：[SEAMeetingListModel](https://www.yuque.com/anyconf/eanoso/gkeau9oyh5vms80z#wSvDN) |
| onFailed | 失败回调 |


### getMoreMeetingList:onFailed:()
`- (void)getMoreMeetingList:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

获取更多会议列表（翻页操作）

| 参数 | 描述 |
| :--- | --- |
| onSuccess | 成功回调，参考文档：[SEAMeetingListModel](https://www.yuque.com/anyconf/eanoso/gkeau9oyh5vms80z#wSvDN) |
| onFailed | 失败回调 |


### getHistoryMeetingList:onFailed:()
`- (void)getHistoryMeetingList:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

获取历史会议列表

| 参数 | 描述 |
| :--- | --- |
| onSuccess | 成功回调，参考文档：[SEAMeetingListModel](https://www.yuque.com/anyconf/eanoso/gkeau9oyh5vms80z#wSvDN) |
| onFailed | 失败回调 |


### getHistoryMeetingList:onFailed:()
`- (void)getHistoryMeetingList:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

获取历史会议列表

| 参数 | 描述 |
| :--- | --- |
| onSuccess | 成功回调，参考文档：[SEAMeetingListModel](https://www.yuque.com/anyconf/eanoso/gkeau9oyh5vms80z#wSvDN) |
| onFailed | 失败回调 |


### getMeetingDetailsWithMeetingId:onSuccess:onFailed:()
`- (void)getMeetingDetailsWithMeetingId:(NSString *)meetingId onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

获取会议详情

| 参数 | 描述 |
| :--- | --- |
| meetingId | 会议标识 |
| onSuccess | 成功回调，参考文档：[SEAMeetingModel](https://www.yuque.com/anyconf/eanoso/gkeau9oyh5vms80z#NwAZR) |
| onFailed | 失败回调 |


### getMeetingDetailsWithRoomNo:onSuccess:onFailed:()
`- (void)getMeetingDetailsWithRoomNo:(NSString *)roomNo onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

获取会议详情

| 参数 | 描述 |
| :--- | --- |
| roomNo | 房间号码 |
| onSuccess | 成功回调，参考文档：[SEAMeetingModel](https://www.yuque.com/anyconf/eanoso/gkeau9oyh5vms80z#NwAZR) |
| onFailed | 失败回调 |


### getParticipantListsWithMeetingId:onSuccess:onFailed:()
`- (void)getParticipantListsWithMeetingId:(NSString *)meetingId onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

获取参会人员列表

| 参数 | 描述 |
| :--- | --- |
| meetingId | 会议标识 |
| onSuccess | 成功回调，参考文档：[SEAMemberListModel](https://www.yuque.com/anyconf/eanoso/gkeau9oyh5vms80z#c6qYV) |
| onFailed | 失败回调 |


### getMoreParticipantListsWithMeetingId:onSuccess:onFailed:()
`- (void)getMoreParticipantListsWithMeetingId:(NSString *)meetingId onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

获取更多参会人员列表（翻页操作）

| 参数 | 描述 |
| :--- | --- |
| meetingId | 会议标识 |
| onSuccess | 成功回调，参考文档：[SEAMemberListModel](https://www.yuque.com/anyconf/eanoso/gkeau9oyh5vms80z#c6qYV) |
| onFailed | 失败回调 |


### requestCancelMeetingWithMeetingId:onSuccess:onFailed:()
`- (void)requestCancelMeetingWithMeetingId:(NSString *)meetingId onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

请求取消会议

| 参数 | 描述 |
| :--- | --- |
| meetingId | 会议标识 |
| onSuccess | 成功回调 |
| onFailed | 失败回调 |


## 用户操作接口
### getAgentList:keyword:onSuccess:onFailed:()
`- (void)getAgentList:(NSArray <NSNumber *> *)typesList keyword:(nullable NSString *)keyword onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

获取设备列表

| 参数 | 描述 |
| :--- | --- |
| typesList | 设备类型列表，设备类型可参看 [SEAAgentType](https://www.yuque.com/anyconf/eanoso/gkeau9oyh5vms80z#rv0G4) 声明定义 |
| keyword | 关键词 |
| onSuccess | 成功回调，参考文档：[SEAAgentListModel](https://www.yuque.com/anyconf/eanoso/gkeau9oyh5vms80z#AzvcZ) |
| onFailed | 失败回调 |


### getMoreAgentList:keyword:onSuccess:onFailed:()
`- (void)getMoreAgentList:(NSArray <NSNumber *> *)typesList keyword:(nullable NSString *)keyword onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

获取更多设备列表（翻页操作）

| 参数 | 描述 |
| :--- | --- |
| typesList | 设备类型列表，设备类型可参看 [SEAAgentType](https://www.yuque.com/anyconf/eanoso/gkeau9oyh5vms80z#rv0G4) 声明定义 |
| keyword | 关键词 |
| onSuccess | 成功回调，参考文档：[SEAAgentListModel](https://www.yuque.com/anyconf/eanoso/gkeau9oyh5vms80z#AzvcZ) |
| onFailed | 失败回调 |


### createRoom:onSuccess:onFailed:()
`- (void)createRoom:(SEAMeetingParam *)params onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

创建房间

| 参数 | 描述 |
| :--- | --- |
| params | 创建房间参数，参考文档：[SEAMeetingParam](https://www.yuque.com/anyconf/eanoso/gkeau9oyh5vms80z#gQ8nA) |
| onSuccess | 成功回调 |
| onFailed | 失败回调 |


### updateRoom:onSuccess:onFailed:()
`- (void)updateRoom:(SEAMeetingParam *)params onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

修改房间数据

| 参数 | 描述 |
| :--- | --- |
| params | 修改房间参数，参考文档：[SEAMeetingParam](https://www.yuque.com/anyconf/eanoso/gkeau9oyh5vms80z#gQ8nA) |
| onSuccess | 成功回调 |
| onFailed | 失败回调 |


### enterRoom:onSuccess:onFailed:()
`- (void)enterRoom:(SEAMeetingEnterParam *)params onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

加入房间

加入房间后，SDK会通过 `MeetingKitDelegate` 中的 [onUserEnter:()](https://www.yuque.com/anyconf/eanoso/rfflpfbuav0xc28g#Pre1r) 回调通知房间内用户。

| 参数 | 描述 |
| :--- | --- |
| params | 加入房间参数，参考文档：[SEAMeetingEnterParam](https://www.yuque.com/anyconf/eanoso/gkeau9oyh5vms80z#OLcoA) |
| onSuccess | 成功回调 |
| onFailed | 失败回调 |


### exitRoom:()
`- (void)exitRoom:(nullable SEASuccessBlock)onSuccess`

离开房间

离开房间后，SDK会通过 `MeetingKitDelegate` 中的 [onUserExit:()](https://www.yuque.com/anyconf/eanoso/rfflpfbuav0xc28g#RimbD) 回调通知房间内用户。

| 参数 | 描述 |
| :--- | --- |
| onSuccess | 完成回调 |


### updateName:onSuccess:onFailed:()
`- (void)updateName:(NSString *)username onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

用户更新昵称

用户更新昵称后，SDK会通过 `MeetingKitDelegate` 中的 [onUserNameChanged:nickname:()](https://www.yuque.com/anyconf/eanoso/rfflpfbuav0xc28g#Gx6nw) 回调通知房间内用户。

| 参数 | 描述 |
| :--- | --- |
| username | 新昵称 |
| onSuccess | 成功回调 |
| onFailed | 失败回调 |


### requestOpenCamera:view:onSuccess:onFailed:()
`- (void)requestOpenCamera:(BOOL)frontCamera view:(VIEW_CLASS *)view onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

请求打开摄像头

在房间内打开本地摄像头后，默认推送本地视频流，SDK会通过 `MeetingKitDelegate` 中的 [onUserCameraStateChanged:cameraState:reason:()](https://www.yuque.com/anyconf/eanoso/rfflpfbuav0xc28g#JEQIr) 回调通知房间内用户。

| 参数 | 描述 |
| :--- | --- |
| frontCamera | 摄像头方向，YES-前置摄像头 NO-后置摄像头 |
| view | 视频渲染视图 |
| onSuccess | 成功回调 |
| onFailed | 失败回调 |


### requestOpenMic:onFailed:()
`- (void)requestOpenMic:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

请求打开麦克风

在房间内打开本地麦克风后，SDK会通过 `MeetingKitDelegate` 中的 [onUserMicStateChanged:micState:reason:()](https://www.yuque.com/anyconf/eanoso/rfflpfbuav0xc28g#yI7Vo) 回调通知房间内用户。

| 参数 | 描述 |
| :--- | --- |
| onSuccess | 成功回调 |
| onFailed | 失败回调 |


### closeCamera:onFailed:()
`- (void)closeCamera:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

关闭摄像头

在房间内关闭本地摄像头后，SDK会通过 `MeetingKitDelegate` 中的 [onUserCameraStateChanged:cameraState:reason:()](https://www.yuque.com/anyconf/eanoso/rfflpfbuav0xc28g#JEQIr) 回调通知房间内用户。

| 参数 | 描述 |
| :--- | --- |
| onSuccess | 成功回调 |
| onFailed | 失败回调 |


### closeMic:onFailed:()
`- (void)closeMic:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

关闭麦克风

在房间内关闭本地麦克风后，SDK会通过 `MeetingKitDelegate` 中的 [onUserMicStateChanged:micState:reason:()](https://www.yuque.com/anyconf/eanoso/rfflpfbuav0xc28g#yI7Vo) 回调通知房间内用户。

| 参数 | 描述 |
| :--- | --- |
| onSuccess | 成功回调 |
| onFailed | 失败回调 |


### requestShare:onSuccess:onFailed:()
`- (void)requestShare:(SEAShareType)shareType onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

请求开启共享

开启共享后，SDK会通过 `MeetingKitDelegate` 中的 [onRoomShareStart:shareType:()](https://www.yuque.com/anyconf/eanoso/rfflpfbuav0xc28g#UF8Js) 回调通知房间内用户。

| 参数 | 描述 |
| :--- | --- |
| shareType | 共享类型，参考文档：[SEAShareType](https://www.yuque.com/anyconf/eanoso/gkeau9oyh5vms80z#Ww9uW) |
| onSuccess | 成功回调 |
| onFailed | 失败回调 |


### stopShare:onFailed:()
`- (void)stopShare:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

关闭共享

关闭共享后，SDK会通过 `MeetingKitDelegate` 中的 [onRoomShareStop:shareType:()](https://www.yuque.com/anyconf/eanoso/rfflpfbuav0xc28g#WTGVD) 回调通知房间内用户。

| 参数 | 描述 |
| :--- | --- |
| shareType | 共享类型，参考文档：[SEAShareType](https://www.yuque.com/anyconf/eanoso/gkeau9oyh5vms80z#Ww9uW) |
| onSuccess | 成功回调 |
| onFailed | 失败回调 |


### sendRoomChatMessage:messageType:targetId:onSuccess:onFailed:()
`- (void)sendRoomChatMessage:(NSString *)message messageType:(SEAMessageType)messageType targetId:(nullable NSString *)targetId onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

发送聊天消息

发送聊天消息后，SDK会通过 `MeetingKitDelegate` 中的 [onReceiveChatMessage:message:messageType:()](https://www.yuque.com/anyconf/eanoso/rfflpfbuav0xc28g#CHAuV) 回调通知房间内用户。

| 参数 | 描述 |
| :--- | --- |
| message | 聊天消息 |
| messageType | 消息类型，参考文档：[SEAMessageType](https://www.yuque.com/anyconf/eanoso/gkeau9oyh5vms80z#xlxGu) |
| targetId | 目标标识，为空时表示全房间接收 |
| onSuccess | 成功回调 |
| onFailed | 失败回调 |


### sendRoomCustomMessage:targetId:onSuccess:onFailed:()
`- (void)sendRoomCustomMessage:(NSString *)message targetId:(nullable NSString *)targetId onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

发送自定义消息

发送自定义消息后，SDK会通过 `MeetingKitDelegate` 中的 [onReceiveChatMessage:message:messageType:()](https://www.yuque.com/anyconf/eanoso/rfflpfbuav0xc28g#CHAuV) 回调通知房间内用户。

| 参数 | 描述 |
| :--- | --- |
| message | 聊天消息 |
| targetId | 目标标识，为空时表示全房间接收 |
| onSuccess | 成功回调 |
| onFailed | 失败回调 |


### getChatList:onFailed:()
`- (void)getChatList:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

获取聊天列表

| 参数 | 描述 |
| :--- | --- |
| onSuccess | 成功回调，参考文档：[SEAChatListModel](https://www.yuque.com/anyconf/eanoso/gkeau9oyh5vms80z#kvOQP) |
| onFailed | 失败回调 |


### getMoreChatList:onFailed:()
`- (void)getMoreChatList:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

获取更多聊天列表（翻页操作）

| 参数 | 描述 |
| :--- | --- |
| onSuccess | 成功回调，参考文档：[SEAChatListModel](https://www.yuque.com/anyconf/eanoso/gkeau9oyh5vms80z#kvOQP) |
| onFailed | 失败回调 |


### requestHandup:onSuccess:onFailed:()
`- (void)requestHandup:(SEAHandupType)handupType onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

请求举手

请求举手后，SDK会通过 `MeetingKitDelegate` 中的 [onRoomHandUpChanged:enable:handupType:()](https://www.yuque.com/anyconf/eanoso/rfflpfbuav0xc28g#XjjFx) 回调通知房间内管理成员。

| 参数 | 描述 |
| :--- | --- |
| handupType | 聊天消息，参考文档：[SEAHandupType](https://www.yuque.com/anyconf/eanoso/gkeau9oyh5vms80z#P2v0K) |
| onSuccess | 成功回调 |
| onFailed | 失败回调 |


### cancelHandup:onSuccess:onFailed:()
`- (void)cancelHandup:(SEAHandupType)handupType onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

取消举手

取消举手后，SDK会通过 `MeetingKitDelegate` 中的 [onRoomHandUpChanged:enable:handupType:()](https://www.yuque.com/anyconf/eanoso/rfflpfbuav0xc28g#XjjFx) 回调通知房间内管理成员。

| 参数 | 描述 |
| :--- | --- |
| handupType | 举手类型，参考文档：[SEAHandupType](https://www.yuque.com/anyconf/eanoso/gkeau9oyh5vms80z#P2v0K) |
| onSuccess | 成功回调 |
| onFailed | 失败回调 |


### confirmAdminOpenCamera:frontCamera:view:onSuccess:onFailed:()
`- (void)confirmAdminOpenCamera:(NSString *)targetId frontCamera:(BOOL)frontCamera view:(VIEW_CLASS *)view onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

回复同意打开摄像头请求

当收到主持人或联席主持人邀请您开启摄像头，如果您同意开启摄像头，需要调用该接口回复给对应管理人员；举手后，收到主持人或联席主持人的处理结果通知，如果您需要开启摄像头，同样需要调用该接口回复给对应管理人员。

回复同意打开摄像头请求后，SDK会通过 `MeetingKitDelegate` 中的 [onUserCameraStateChanged:cameraState:reason:()](https://www.yuque.com/anyconf/eanoso/rfflpfbuav0xc28g#JEQIr) 回调通知房间内管理成员。

| 参数 | 描述 |
| :--- | --- |
| targetId | 目标标识，请求或同意您开启摄像头请求的管理者标识 |
| frontCamera | 摄像头方向，YES-前置摄像头 NO-后置摄像头 |
| view | 视频渲染视图 |
| onSuccess | 成功回调 |
| onFailed | 失败回调 |


### confirmAdminOpenMic:onSuccess:onFailed:()
`- (void)confirmAdminOpenMic:(NSString *)targetId onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

回复同意打开麦克风请求

当收到主持人或联席主持人邀请您开启麦克风，如果您同意开启麦克风，需要调用该接口回复给对应管理人员；举手后，收到主持人或联席主持人的处理结果通知，如果您需要开启麦克风，同样需要调用该接口回复给对应管理人员。

回复同意打开麦克风请求后，SDK会通过 `MeetingKitDelegate` 中的 [onUserMicStateChanged:micState:reason:()](https://www.yuque.com/anyconf/eanoso/rfflpfbuav0xc28g#awVw0) 回调通知房间内管理成员。

| 参数 | 描述 |
| :--- | --- |
| targetId | 目标标识，请求或同意您开启麦克风请求的管理者标识 |
| onSuccess | 成功回调 |
| onFailed | 失败回调 |


### confirmAdminRoomShare:shareType:onSuccess:onFailed:()
`- (void)confirmAdminRoomShare:(NSString *)targetId shareType:(SEAShareType)shareType onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

回复同意打开房间共享请求

当收到主持人或联席主持人邀请您开启共享，如果您同意开启共享，需要调用该接口回复给对应管理人员；举手后，收到主持人或联席主持人的处理结果通知，如果您需要开启共享，同样需要调用该接口回复给对应管理人员。

回复同意打开共享请求后，SDK会通过 `MeetingKitDelegate` 中的 [onRoomShareStart:shareType:()](https://www.yuque.com/anyconf/smeeting/rfflpfbuav0xc28g#F0DEZ) 回调通知房间内管理成员。

| 参数 | 描述 |
| :--- | --- |
| targetId | 目标标识，请求或同意您开启房间共享请求的管理者标识 |
| shareType | 共享类型，参考文档：[SEAShareType](https://www.yuque.com/anyconf/eanoso/gkeau9oyh5vms80z#Ww9uW) |
| onSuccess | 成功回调 |
| onFailed | 失败回调 |


### updateLocalView:()
`- (void)updateLocalView:(VIEW_CLASS *)view`

更新本地摄像头的预览画面

| 参数 | 描述 |
| :--- | --- |
| view | 视频渲染视图 |


### switchCamera()
`- (void)switchCamera`

切换摄像头前后置

### setLocalPreviewMirror:()
`- (void)setLocalPreviewMirror:(BOOL)mirror`

设置本地预览镜像

仅作用于本地预览画面，按 `mirror` 取值设置镜像；是否区分前后置（如后置不镜像）等策略由业务层自行决定。

| 参数 | 描述 |
| :--- | --- |
| mirror | YES-开启镜像 NO-关闭镜像 |


### currentCameraDirection()
`- (SEACameraDirection)currentCameraDirection`

获取当前摄像头方向

调用该接口，SDK 会返回当前采集使用的摄像头方向，参考 [SEACameraDirection](/zh/meeting/ios/types#seacameradirection)。

### switchSpeaker:()
`- (void)switchSpeaker:(BOOL)enabled`

切换扬声器状态

用户可通过该接口设置本地音频是否播放。

| 参数 | 描述 |
| :--- | --- |
| enabled | 扬声器状态，YES-开启 NO-关闭 |


### switchAudioRoute:()
`- (void)switchAudioRoute:(SEAAudioRoute)route`

切换音频路由

切换音频路由后，SDK会通过 `MeetingKitDelegate` 中的 [onAudioRouteChange:previousRoute:()](https://www.yuque.com/anyconf/eanoso/rfflpfbuav0xc28g#AvcCn) 回调通知您。

| 参数 | 描述 |
| :--- | --- |
| route | 音频路由，参考文档：[SEAAudioRoute](https://www.yuque.com/anyconf/eanoso/gkeau9oyh5vms80z#HhTLs) |


### currentAudioRoute()
`- (SEAAudioRoute)currentAudioRoute`

获取当前音频路由

调用该接口，SDK 会通过该接口返回当前的音频路由，参考文档：[SEAAudioRoute](https://www.yuque.com/anyconf/eanoso/gkeau9oyh5vms80z#HhTLs)。

### headphoneDeviceAvailable()
`- (BOOL)headphoneDeviceAvailable`

是否存在有线耳机设备

调用该接口，SDK 会通过该接口返回是否存在有线耳机设备。

### bluetoothDeviceAvailable()
`- (BOOL)bluetoothDeviceAvailable`

是否存在蓝牙耳机设备

调用该接口，SDK 会通过该接口返回是否存在蓝牙耳机设备。

### startRemoteView:streamType:view:()
`- (void)startRemoteView:(NSString *)userId streamType:(SEAVideoStreamType)streamType view:(VIEW_CLASS *)view`

开始播放远端用户视频

开始播放远端用户视频，并绑定视频渲染资源。

| 参数 | 描述 |
| :--- | --- |
| userId | 远端用户标识 |
| streamType | 视频流类型，参考文档：[SEAVideoStreamType](https://www.yuque.com/anyconf/eanoso/gkeau9oyh5vms80z#ckLzs) |
| view | 视频渲染视图 |


### stopRemoteView:streamType:()
`- (void)stopRemoteView:(NSString *)userId streamType:(SEAVideoStreamType)streamType`

停止播放远端用户视频

停止播放远端用户视频，并释放视频渲染资源。

| 参数 | 描述 |
| :--- | --- |
| userId | 远端用户标识 |
| streamType | 视频流类型，参考文档：[SEAVideoStreamType](https://www.yuque.com/anyconf/eanoso/gkeau9oyh5vms80z#ckLzs) |


### stopAllRemoteViewWithUserId:()
`- (void)stopAllRemoteViewWithUserId:(NSString *)userId`

停止播放远端用户的所有视频

停止播放远端用户的所有视频，并释放全部渲染资源。

| 参数 | 描述 |
| :--- | --- |
| userId | 远端用户标识 |


### startRemoteMixture:()
`- (void)startRemoteMixture:(VIEW_CLASS *)view`

订阅远端合成画面视频流

订阅远端合成画面视频流，并绑定视频渲染控件。

| 参数 | 描述 |
| :--- | --- |
| view | 视频渲染视图 |


### stopRemoteMixture()
`- (void)stopRemoteMixture`

停止订阅远端合成画面视频流

停止订阅远端合成画面视频流，并释放渲染控件。


### startRemoteRetweet:view:()
`- (void)startRemoteRetweet:(NSString *)streamName view:(VIEW_CLASS *)view`

订阅远端转推音视频流（webrtc 取流）

订阅由外部传入流名的远端转推音视频流，单条连接同时接收音视频，并绑定视频渲染控件。转推流不作为远端用户视频数据上报，其接收状态通过 onReceiveRetweetStreamStatusChange:status: 单独通知。目前仅支持 `wangsu` 流媒体供应商。

| 参数 | 描述 |
| :--- | --- |
| streamName | 需要订阅的远端流名（由外部传入） |
| view | 视频渲染视图 |


### stopRemoteRetweet:()
`- (void)stopRemoteRetweet:(NSString *)streamName`

停止订阅远端转推音视频流

停止订阅指定流名的远端转推音视频流，并释放渲染控件。

| 参数 | 描述 |
| :--- | --- |
| streamName | 需要停止订阅的远端流名（由外部传入） |

## 管理员操作接口
### adminDestroyRoom:onFailed:()
`- (void)adminDestroyRoom:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

解散房间（只有主持人或联席主持人能够调用）

房间解散后，SDK会通过 `MeetingKitDelegate` 中的 [onExitRoom:()](https://www.yuque.com/anyconf/eanoso/rfflpfbuav0xc28g#qZ4ki) 回调通知房间内用户。

| 参数 | 描述 |
| :--- | --- |
| onSuccess | 成功回调 |
| onFailed | 失败回调 |


### adminUpdateRoomCameraState:selfUnmuteCameraDisabled:onSuccess:onFailed:()
`- (void)adminUpdateRoomCameraState:(BOOL)cameraDisabled selfUnmuteCameraDisabled:(BOOL)selfUnmuteCameraDisabled onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

更新房间全体禁视频，控制当前房间内所有用户是否可打开摄像头采集设备的权限状态（只有主持人或联席主持人能够调用）

更新房间全体禁视频后，SDK会通过 `MeetingKitDelegate` 中的 [onRoomCameraStateChanged:selfUnmuteCameraDisabled:userId:()](https://www.yuque.com/anyconf/eanoso/rfflpfbuav0xc28g#cgUyr) 回调通知房间内用户。

| 参数 | 描述 |
| :--- | --- |
| cameraDisabled | 房间摄像头禁用状态，YES-禁用 NO-不禁用 |
| selfUnmuteCameraDisabled | 是否禁止自我解除摄像头状态，YES-禁止 NO-不禁止 |
| onSuccess | 成功回调 |
| onFailed | 失败回调 |


### adminUpdateRoomMicState:selfUnmuteMicDisabled:onSuccess:onFailed:()
`- (void)adminUpdateRoomMicState:(BOOL)micDisabled selfUnmuteMicDisabled:(BOOL)selfUnmuteMicDisabled onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

更新房间全体禁音频，控制当前房间内所有用户是否可打开麦克风采集设备的权限状态（只有主持人或联席主持人能够调用）

更新房间全体禁音频后，SDK会通过 `MeetingKitDelegate` 中的 [onRoomMicStateChanged:selfUnmuteMicDisabled:userId:()](https://www.yuque.com/anyconf/eanoso/rfflpfbuav0xc28g#rzgdB) 回调通知房间内用户。

| 参数 | 描述 |
| :--- | --- |
| micDisabled | 房间麦克风禁用状态，YES-禁用 NO-不禁用 |
| selfUnmuteMicDisabled | 是否禁止自我解除麦克风状态，YES-禁止 NO-不禁止 |
| onSuccess | 成功回调 |
| onFailed | 失败回调 |


### adminUpdateRoomSelfUnmuteCameraDisabled:onSuccess:onFailed:()
`- (void)adminUpdateRoomSelfUnmuteCameraDisabled:(BOOL)selfUnmuteCameraDisabled onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

更新房间是否禁止自我解除视频状态，控制当前房间内所有用户是否可以自主打开摄像头采集设备的权限状态

更新房间是否禁止自我解除视频状态后，SDK会通过 `MeetingKitDelegate` 中的 [onRoomCameraStateChanged:selfUnmuteCameraDisabled:userId:()](https://www.yuque.com/anyconf/eanoso/rfflpfbuav0xc28g#cgUyr) 回调通知房间内用户。

| 参数 | 描述 |
| :--- | --- |
| selfUnmuteCameraDisabled | 是否禁止自我解除摄像头状态，YES-禁止 NO-不禁止 |
| onSuccess | 成功回调 |
| onFailed | 失败回调 |


### adminUpdateRoomSelfUnmuteMicDisabled:onSuccess:onFailed:()
`- (void)adminUpdateRoomSelfUnmuteMicDisabled:(BOOL)selfUnmuteMicDisabled onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

更新房间是否禁止自我解除音频状态，控制当前房间内所有用户是否可以自主打开麦克风采集设备的权限状态

更新房间是否禁止自我解除音频状态后，SDK会通过 `MeetingKitDelegate` 中的 [onRoomMicStateChanged:selfUnmuteMicDisabled:userId:()](https://www.yuque.com/anyconf/eanoso/rfflpfbuav0xc28g#rzgdB) 回调通知房间内用户。

| 参数 | 描述 |
| :--- | --- |
| selfUnmuteMicDisabled | 是否禁止自我解除麦克风状态，YES-禁止 NO-不禁止 |
| onSuccess | 成功回调 |
| onFailed | 失败回调 |


### adminUpdateRoomChatDisabled:onSuccess:onFailed:()
`- (void)adminUpdateRoomChatDisabled:(BOOL)chatDisabled onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

更新房间聊天禁用状态，控制当前房间内所有用户是否可进行聊天的权限状态（只有主持人或联席主持人能够调用）

更新房间聊天禁用状态后，SDK会通过 `MeetingKitDelegate` 中的 [onRoomChatDisabledChanged:userId:()](https://www.yuque.com/anyconf/eanoso/rfflpfbuav0xc28g#K0Q7N) 回调通知房间内用户。

| 参数 | 描述 |
| :--- | --- |
| chatDisabled | 聊天禁用状态，YES-禁用 NO-不禁用 |
| onSuccess | 成功回调 |
| onFailed | 失败回调 |


### adminUpdateRoomShareDisabled:onSuccess:onFailed:()
`- (void)adminUpdateRoomShareDisabled:(BOOL)shareDisabled onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

更新房间共享禁用状态，控制当前房间内所有用户是否可进行共享的权限状态（只有主持人或联席主持人能够调用）

更新房间共享禁用状态后，SDK会通过 `MeetingKitDelegate` 中的 [onRoomShareDisabledChanged:userId:()](https://www.yuque.com/anyconf/eanoso/rfflpfbuav0xc28g#zWldw) 回调通知房间内用户。

| 参数 | 描述 |
| :--- | --- |
| shareDisabled | 共享禁用状态，YES-禁用 NO-不禁用 |
| onSuccess | 成功回调 |
| onFailed | 失败回调 |


### adminUpdateRoomScreenshotDisabled:onSuccess:onFailed:()
`- (void)adminUpdateRoomScreenshotDisabled:(BOOL)screenshotDisabled onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

更新房间截屏开关状态，控制当前房间内所有用户是否可进行截屏的权限状态（只有主持人或联席主持人能够调用）

更新房间截屏开关状态后，SDK会通过 `MeetingKitDelegate` 中的 [onRoomScreenshotDisabledChanged:userId:()](https://www.yuque.com/anyconf/eanoso/rfflpfbuav0xc28g#h5kAO) 回调通知房间内用户。

| 参数 | 描述 |
| :--- | --- |
| screenshotDisabled | 截屏禁用状态，YES-禁用 NO-不禁用 |
| onSuccess | 成功回调 |
| onFailed | 失败回调 |


### adminUpdateRoomWatermarkDisabled:onSuccess:onFailed:()
`- (void)adminUpdateRoomWatermarkDisabled:(BOOL)watermarkDisabled onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

更新房间水印开关状态，控制当前房间内是否开启水印状态（只有主持人或联席主持人能够调用）

更新房间水印开关状态后，SDK会通过 `MeetingKitDelegate` 中的 [onRoomWatermarkDisabledChanged:userId:()](https://www.yuque.com/anyconf/eanoso/rfflpfbuav0xc28g#dBCP1) 回调通知房间内用户。

| 参数 | 描述 |
| :--- | --- |
| watermarkDisabled | 房间水印状态，YES-开启 NO-关闭 |
| onSuccess | 成功回调 |
| onFailed | 失败回调 |


### adminUpdateRoomLocked:onSuccess:onFailed:()
`- (void)adminUpdateRoomLocked:(BOOL)locked onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

更新房间锁定状态，控制当前房间内是否锁定状态（只有主持人或联席主持人能够调用）

更新房间锁定状态后，SDK会通过 `MeetingKitDelegate` 中的 [onRoomLockedChanged:userId:()](https://www.yuque.com/anyconf/eanoso/rfflpfbuav0xc28g#NazqA) 回调通知房间内用户。

| 参数 | 描述 |
| :--- | --- |
| locked | 锁定状态，YES-开启 NO-关闭 |
| onSuccess | 成功回调 |
| onFailed | 失败回调 |


### adminUpdateNickname:nickname:onSuccess:onFailed:()
`- (void)adminUpdateNickname:(NSString *)userId nickname:(NSString *)nickname onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

更新用户昵称（只有主持人或联席主持人能够调用）

更新用户昵称后，SDK会通过 `MeetingKitDelegate` 中的 [onUserNameChanged:nickname:()](https://www.yuque.com/anyconf/eanoso/rfflpfbuav0xc28g#Gx6nw) 回调通知房间内用户。

| 参数 | 描述 |
| :--- | --- |
| userId | 用户标识 |
| nickname | 用户昵称 |
| onSuccess | 成功回调 |
| onFailed | 失败回调 |


### adminUpdateUserRole:userRole:onSuccess:onFailed:()
`- (void)adminUpdateUserRole:(NSString *)userId userRole:(SEAUserRole)userRole onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

更新用户角色（只有主持人或联席主持人能够调用）

更新用户角色后，SDK会通过 `MeetingKitDelegate` 中的 [onUserRoleChanged:userRole:()](https://www.yuque.com/anyconf/eanoso/rfflpfbuav0xc28g#H2KlN) 回调通知房间内用户。

| 参数 | 描述 |
| :--- | --- |
| userId | 用户标识 |
| userRole | 用户角色，参考文档：[SEAUserRole](https://www.yuque.com/anyconf/eanoso/gkeau9oyh5vms80z#QsCHa) |
| onSuccess | 成功回调 |
| onFailed | 失败回调 |


### adminMoveHost:onSuccess:onFailed:()
`- (void)adminMoveHost:(NSString *)userId onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

主持人转移（只有主持人或联席主持人能够调用）

主持人转移后，SDK会通过 `MeetingKitDelegate` 中的 [onRoomMoveHost:sourceUserId:()](https://www.yuque.com/anyconf/eanoso/rfflpfbuav0xc28g#eRG3J) 回调通知房间内用户。

| 参数 | 描述 |
| :--- | --- |
| userId | 用户标识 |
| onSuccess | 成功回调 |
| onFailed | 失败回调 |


### adminUpdateUserChatDisabled:chatDisabled:onSuccess:onFailed:()
`- (void)adminUpdateUserChatDisabled:(NSString *)userId chatDisabled:(BOOL)chatDisabled onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

主持人更新用户聊天状态（只有主持人或联席主持人能够调用）

主持人更新用户聊天状态后，SDK会通过 `MeetingKitDelegate` 中的 [onUserChatDisabledChanged:userId:()](https://www.yuque.com/anyconf/eanoso/rfflpfbuav0xc28g#awVw0) 回调通知房间内目标用户。

| 参数 | 描述 |
| :--- | --- |
| userId | 用户标识 |
| chatDisabled | 禁用状态，YES-禁用 NO-不禁用 |
| onSuccess | 成功回调 |
| onFailed | 失败回调 |


### adminUpdateUserDrawDisabled:drawDisabled:onSuccess:onFailed:()
`- (void)adminUpdateUserDrawDisabled:(NSString *)userId drawDisabled:(BOOL)drawDisabled onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

主持人更新用户涂鸦状态（只有主持人或联席主持人能够调用）

主持人更新用户涂鸦状态后，SDK会通过 `MeetingKitDelegate` 中的 [onUserDrawDisabledChanged:userId:()](https://www.yuque.com/anyconf/smeeting/rfflpfbuav0xc28g#p4pR7) 回调通知房间内目标用户。

| 参数 | 描述 |
| :--- | --- |
| userId | 用户标识 |
| drawDisabled | 禁用状态，YES-禁用 NO-不禁用 |
| onSuccess | 成功回调 |
| onFailed | 失败回调 |


### adminRequestUserOpenShare:onSuccess:onFailed:()
`- (void)adminRequestUserOpenShare:(NSString *)userId onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

请求打开成员屏幕共享（只有主持人或联席主持人能够调用）

请求打开成员屏幕共享后，SDK会通过 `MeetingKitDelegate` 中的 [onRequestOpenShare:()](https://www.yuque.com/anyconf/eanoso/rfflpfbuav0xc28g#aPi1r) 回调通知房间内指定用户。

| 参数 | 描述 |
| :--- | --- |
| userId | 用户标识 |
| onSuccess | 成功回调 |
| onFailed | 失败回调 |


### adminRequestUserOpenCamera:onSuccess:onFailed:()
`- (void)adminRequestUserOpenCamera:(NSString *)userId onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

请求打开成员摄像头（只有主持人或联席主持人能够调用）

请求打开成员摄像头后，SDK会通过 `MeetingKitDelegate` 中的 [onRequestOpenCamera:()](https://www.yuque.com/anyconf/eanoso/rfflpfbuav0xc28g#aPi1r) 回调通知房间内指定用户。

| 参数 | 描述 |
| :--- | --- |
| userId | 用户标识 |
| onSuccess | 成功回调 |
| onFailed | 失败回调 |


### adminCloseUserCamera:onSuccess:onFailed:()
`- (void)adminCloseUserCamera:(NSString *)userId onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

关闭远端用户摄像头（只有主持人或联席主持人能够调用）

关闭远端用户摄像头后，SDK会通过 `MeetingKitDelegate` 中的 [onUserCameraStateChanged:cameraState:reason:()](https://www.yuque.com/anyconf/eanoso/rfflpfbuav0xc28g#jE9fm) 回调通知房间内用户。

| 参数 | 描述 |
| :--- | --- |
| userId | 用户标识 |
| onSuccess | 成功回调 |
| onFailed | 失败回调 |


### adminRequestUserOpenMic:onSuccess:onFailed:()
`- (void)adminRequestUserOpenMic:(NSString *)userId onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

请求打开成员麦克风（只有主持人或联席主持人能够调用）

请求打开成员麦克风后，SDK会通过 `MeetingKitDelegate` 中的 [onRequestOpenMic:()](https://www.yuque.com/anyconf/eanoso/rfflpfbuav0xc28g#NA5v1) 回调通知房间内指定用户。

| 参数 | 描述 |
| :--- | --- |
| userId | 用户标识 |
| onSuccess | 成功回调 |
| onFailed | 失败回调 |


### adminCloseUserMic:onSuccess:onFailed:()
`- (void)adminCloseUserMic:(NSString *)userId onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

关闭远端用户麦克风（只有主持人或联席主持人能够调用）

关闭远端用户麦克风后，SDK会通过 `MeetingKitDelegate` 中的 [onUserMicStateChanged:micState:reason:()](https://www.yuque.com/anyconf/eanoso/rfflpfbuav0xc28g#yI7Vo) 回调通知房间内用户。

| 参数 | 描述 |
| :--- | --- |
| userId | 用户标识 |
| onSuccess | 成功回调 |
| onFailed | 失败回调 |


### adminKickUserOut:onSuccess:onFailed:()
`- (void)adminKickUserOut:(NSString *)userId onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

踢出成员（只有主持人或联席主持人能够调用）

踢出成员后，SDK会通过 `MeetingKitDelegate` 中的 [onExitRoom:()](https://www.yuque.com/anyconf/eanoso/rfflpfbuav0xc28g#qZ4ki) 回调通知房间内指定用户。

| 参数 | 描述 |
| :--- | --- |
| userId | 用户标识 |
| onSuccess | 成功回调 |
| onFailed | 失败回调 |


### adminStopRoomShare:onFailed:()
`- (void)adminStopRoomShare:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

关闭共享（只有主持人或联席主持人能够调用）

关闭共享后，SDK会通过 `MeetingKitDelegate` 中的 [onAdminRoomShareStop:shareType:()](https://www.yuque.com/anyconf/eanoso/rfflpfbuav0xc28g#oerNu) 回调通知房间内用户。

| 参数 | 描述 |
| :--- | --- |
| onSuccess | 成功回调 |
| onFailed | 失败回调 |


### adminConfirmHandup:handupType:approve:onSuccess:onFailed:()
`- (void)adminConfirmHandup:(NSString *)userId handupType:(SEAHandupType)handupType approve:(BOOL)approve onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

处理举手申请（只有主持人或联席主持人能够调用）

处理举手申请后，SDK会通过 `MeetingKitDelegate` 中的 [onHandupConfirm:approve:userId:()](https://www.yuque.com/anyconf/eanoso/rfflpfbuav0xc28g#aFxM1) 回调通知房间指定用户。

| 参数 | 描述 |
| :--- | --- |
| userId | 用户标识 |
| handupType | 举手申请类型 |
| approve | 处理举手结果，YES-同意 NO-拒绝 |
| onSuccess | 成功回调 |
| onFailed | 失败回调 |


### adminUpdateConferee:onSuccess:onFailed:()
`- (void)adminUpdateConferee:(NSArray <NSString *> *)conferee onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

主持人更新受邀成员（只有主持人或联席主持人能够调用）

更新受邀成员后，SDK 会将目标成员添加到会议的受邀成员列表。同时，目标成员也可通过查看待参加会议列表找到该会议。

| 参数 | 描述 |
| :--- | --- |
| conferee | 成员标识列表 |
| onSuccess | 成功回调 |
| onFailed | 失败回调 |


### adminInviteAgent:onSuccess:onFailed:()
`- (void)adminInviteAgent:(NSArray <SEAInviteModel *> *)invitesList onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

主持人邀请设备入会（只有主持人或联席主持人能够调用）

邀请设备入会后，SDK 会将 SIP/H323 等目标设备拉进会议参会，如果当前设备已在其它会议等异常情况 SDK 会通过`onFailed`回调通知具体失败原因。

| 参数 | 描述 |
| :--- | --- |
| invitesList | 邀请列表，参考文档：[SEAInviteModel](https://www.yuque.com/anyconf/eanoso/gkeau9oyh5vms80z#piZiy) |
| onSuccess | 成功回调 |
| onFailed | 失败回调 |


## 云录制相关接口
### getCloudRecordDetail:onFailed:()
`- (void)getCloudRecordDetail:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

获取云录制详情（只有主持人或联席主持人能够调用）

| 参数 | 描述 |
| :--- | --- |
| onSuccess | 成功回调，参考文档：[SEACloudRecordDetailsModel](https://www.yuque.com/anyconf/eanoso/gkeau9oyh5vms80z#bJyXC) |
| onFailed | 失败回调 |


### getCloudRecordConfig:onFailed:()
`- (void)getCloudRecordConfig:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

获取云录制配置（只有主持人或联席主持人能够调用）

| 参数 | 描述 |
| :--- | --- |
| onSuccess | 成功回调，参考文档：[SEACloudRecordConfigModel](https://www.yuque.com/anyconf/eanoso/gkeau9oyh5vms80z#zNkwP) |
| onFailed | 失败回调 |


### startCloudRecord:onSuccess:onFailed:()
`- (void)startCloudRecord:(SEACloudRecordParam *)params onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

开启云录制（只有主持人或联席主持人能够调用）

| 参数 | 描述 |
| :--- | --- |
| params | 云录制参数，参考文档：[SEACloudRecordParam](https://www.yuque.com/anyconf/eanoso/gkeau9oyh5vms80z#hFxgc) |
| onSuccess | 成功回调 |
| onFailed | 失败回调 |


### stopCloudRecord:onSuccess:onFailed:()
`- (void)stopCloudRecord:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

停止云录制（只有主持人或联席主持人能够调用）

| 参数 | 描述 |
| :--- | --- |
| onSuccess | 成功回调 |
| onFailed | 失败回调 |


## 等候室相关接口
### exitWaitingRoom:onSuccess:()
`- (void)exitWaitingRoom:(NSString *)roomNo onSuccess:(nullable SEASuccessBlock)onSuccess`

请求离开等候室

用户离开等候室后，SDK会通过 `MeetingKitDelegate` 中的 [onRoomUserEnterWaitingRoom:()](https://www.yuque.com/anyconf/smeeting/rfflpfbuav0xc28g#xwSvM) 回调通知房间内管理员用户。

| 参数 | 描述 |
| :--- | --- |
| roomNo | 会议号码 |
| onSuccess | 成功回调 |


### adminUpdateWaitingRoomDisabled:onSuccess:onFailed:()
`- (void)adminUpdateWaitingRoomDisabled:(BOOL)waitingRoomDisabled onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

更新房间等候室禁用状态，控制当前房间内是否开启等候室状态（只有主持人或联席主持人能够调用）

更新房间等候室禁用状态后，SDK会通过 `MeetingKitDelegate` 中的 [onRoomWaitingRoomDisabledChanged:userId:()](https://www.yuque.com/anyconf/smeeting/rfflpfbuav0xc28g#dGJps) 回调通知房间内用户。

| 参数 | 描述 |
| :--- | --- |
| waitingRoomDisabled | 房间等候室禁用状态，YES-禁用 NO-不禁用 |
| onSuccess | 成功回调 |
| onFailed | 失败回调 |


### adminMoveInWaitingRoom:ickname:onSuccess:onFailed:()
`- (void)adminMoveInWaitingRoom:(NSString *)userId nickname:(NSString *)nickname onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

将会议室成员移动到等候室，管理员用户可通过该接口将会中成员移至等候室中（只有主持人或联席主持人能够调用），SDK会通过 `MeetingKitDelegate` 中的 [onRoomMoveInWaitingRoom:()](https://www.yuque.com/anyconf/smeeting/rfflpfbuav0xc28g#qBV3v) 回调通知给目标用户。

| 参数 | 描述 |
| :--- | --- |
| userId | 用户标识 |
| nickname | 用户昵称 |
| onSuccess | 成功回调 |
| onFailed | 失败回调 |


### adminMoveOutWaitingRoom:nickname:onSuccess:onFailed:()
`- (void)adminMoveOutWaitingRoom:(NSString *)userId nickname:(NSString *)nickname onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

将等候室人员移动到会议室，管理员用户可通过该接口将当前等候室中成员移至会议室中（只有主持人或联席主持人能够调用），SDK会通过 `MeetingKitIMDelegate` 中的 [onWaitingRoomMoveInRoom:title:()](https://www.yuque.com/anyconf/smeeting/wh4gigxazm9esngc#Td4ag) 回调通知给目标用户。

| 参数 | 描述 |
| :--- | --- |
| userId | 用户标识，空表示全部成员 |
| nickname | 用户昵称 |
| onSuccess | 成功回调 |
| onFailed | 失败回调 |


### adminGetWaitingRoomUserList:onFailed:()
`- (void)adminGetWaitingRoomUserList:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

主持人获取等候室用户列表

| 参数 | 描述 |
| :--- | --- |
| onSuccess | 成功回调，参考文档：[SEAWaitingRoomMemberListModel](https://www.yuque.com/anyconf/smeeting/gkeau9oyh5vms80z#cUCiD) |
| onFailed | 失败回调 |


## 分组讨论相关接口
### subMeetingHelp:onFailed:()
`- (void)subMeetingHelp:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

小组成员请求管理员帮助，SDK会通过 `MeetingKitIMDelegate` 中的 [onSubMettingAskingHelp:meetingId:title:()](https://www.yuque.com/anyconf/smeeting/wh4gigxazm9esngc#jEQ8e) 回调通知给管理员用户。

| 参数 | 描述 |
| :--- | --- |
| onSuccess | 成功回调 |
| onFailed | 失败回调 |


### adminUpdateEnterBeforeHostDisabled:onSuccess:onFailed:()
`- (void)adminUpdateEnterBeforeHostDisabled:(BOOL)enterBeforeHostDisabled onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

更新禁止在主持人前入会状态，控制当前房间内是否允许在主持人前入会状态（只有主持人或联席主持人能够调用）。

| 参数 | 描述 |
| :--- | --- |
| enterBeforeHostDisabled | 禁止状态，YES-禁止 NO-不禁止 |
| onSuccess | 成功回调 |
| onFailed | 失败回调 |


### adminCreateSubMeeting:onSuccess:onFailed:()
`- (void)adminCreateSubMeeting:(NSArray <NSString *> *)titleList onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed;`

主持人创建小组会议

| 参数 | 描述 |
| :--- | --- |
| titleList | 标题列表 |
| onSuccess | 成功回调 |
| onFailed | 失败回调 |


### adminUpdateSubMeetingTitle:targetId:onSuccess:onFailed:()
`- (void)adminUpdateSubMeetingTitle:(NSString *)title targetId:(NSString *)targetId onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

主持人修改小组会议标题

| 参数 | 描述 |
| :--- | --- |
| title | 小组标题 |
| targetId | 小组标识 |
| onSuccess | 成功回调 |
| onFailed | 失败回调 |


### adminUpdateSubMeetingConferee:targetId:onSuccess:onFailed:()
`- (void)adminUpdateSubMeetingConferee:(NSArray <SEAConfereeModel *> *)confereeList targetId:(NSString *)targetId onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

主持人修改小组会议成员

| 参数 | 描述 |
| :--- | --- |
| confereeList | 小组参会列表，参考文档：[SEAConfereeModel](https://www.yuque.com/anyconf/smeeting/gkeau9oyh5vms80z#ipu1S) |
| targetId | 小组标识 |
| onSuccess | 成功回调 |
| onFailed | 失败回调 |


### adminDeleteSubMeeting:onSuccess:onFailed:()
`- (void)adminDeleteSubMeeting:(NSArray <NSString *> *)targetList onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

主持人删除小组会议

| 参数 | 描述 |
| :--- | --- |
| targetList | 小组标识列表 |
| onSuccess | 成功回调 |
| onFailed | 失败回调 |


### adminGetSubMeetingList:onSuccess:onFailed:()
`- (void)adminGetSubMeetingList:(NSString *)meetingId onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

主持人请求小组会议列表

| 参数 | 描述 |
| :--- | --- |
| meetingId | 会议标识 |
| onSuccess | 成功回调，参考文档：[SEARoomSubMeetingListModel](https://www.yuque.com/anyconf/smeeting/gkeau9oyh5vms80z#MrIJK) |
| onFailed | 失败回调 |


### adminStartSubMeeting:onSuccess:onFailed:()
`- (void)adminStartSubMeeting:(NSArray <NSString *> *)targetList onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

开始小组会议，管理员用户可通过该接口将创建之后的小组会议设置为开始（只有主持人或联席主持人能够调用），SDK会通过 `MeetingKitDelegate` 中的 [onRoomSubMeetingStart:title:conferee:()](https://www.yuque.com/anyconf/smeeting/rfflpfbuav0xc28g#o5QYi) 回调通知给目标用户。

| 参数 | 描述 |
| :--- | --- |
| targetList | 小组标识列表 |
| onSuccess | 成功回调 |
| onFailed | 失败回调 |


### adminStopSubMeeting:onSuccess:onFailed:()
`- (void)adminStopSubMeeting:(NSArray <NSString *> *)targetList onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

结束小组会议，管理员用户可通过该接口将创建之后的小组会议设置为结束（只有主持人或联席主持人能够调用），SDK会通过 `MeetingKitDelegate` 中的 [onRoomSubMeetingStop:()](https://www.yuque.com/anyconf/smeeting/rfflpfbuav0xc28g#AsdP0) 回调通知给目标用户。

| 参数 | 描述 |
| :--- | --- |
| targetList | 小组标识列表 |
| onSuccess | 成功回调 |
| onFailed | 失败回调 |


### adminMoveSubMeetingUser:fromGroupId:toGroupId:onSuccess:onFailed:()
`- (void)adminMoveSubMeetingUser:(NSString *)targetId fromGroupId:(NSString *)fromGroupId toGroupId:(nullable NSString *)toGroupId onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

小组会议之间移动用户，管理员用户可通过该接口在小组会议以及主会场之间移动指定成员（只有主持人或联席主持人能够调用），SDK会通过 `MeetingKitDelegate` 中的 [onRoomMoveSubMeeting:fromMeetingTitle:toMeetingId:toMeetingTitle:()](https://www.yuque.com/anyconf/smeeting/rfflpfbuav0xc28g#PXXkX) 回调通知给目标用户。

| 参数 | 描述 |
| :--- | --- |
| targetId | 目标成员标识 |
| fromGroupId | 原小组标识 |
| toGroupId | 目标小组标识，为空时表示主会议 |
| onSuccess | 成功回调 |
| onFailed | 失败回调 |


### getOnlineMemberList:onSuccess:onFailed:()
`- (void)getOnlineMemberList:(NSString *)meetingId onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

获取在线成员列表

| 参数 | 描述 |
| :--- | --- |
| meetingId | 会议标识 |
| onSuccess | 成功回调，参考文档：[SEAOnlineMemberListModel](https://www.yuque.com/anyconf/smeeting/gkeau9oyh5vms80z#CEmgE) |
| onFailed | 失败回调 |


### getMoreOnlineMemberList:onSuccess:onFailed:()
`- (void)getMoreOnlineMemberList:(NSString *)meetingId onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

获取更多在线成员列表（翻页操作）

| 参数 | 描述 |
| :--- | --- |
| meetingId | 会议标识 |
| onSuccess | 成功回调，参考文档：[SEAOnlineMemberListModel](https://www.yuque.com/anyconf/smeeting/gkeau9oyh5vms80z#CEmgE) |
| onFailed | 失败回调 |


## 签到相关接口
### signInCreate:desc:onSuccess:onFailed:()
`- (void)signInCreate:(NSInteger)dur desc:(nullable NSString *)desc onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

创建签到活动，管理员可通过该接口创建签到活动（只有主持人或联席主持人能够调用），SDK会通过 `MeetingKitDelegate` 中的  [onSignInActivity:epoch:beginAt:dur:endAt:desc:()]() 回调通知给全体会中成员。

| 参数 | 描述 |
| :--- | --- |
| dur | 签到时长，单位：分钟，0为不限时 |
| desc | 签到描述 |
| onSuccess | 成功回调 |
| onFailed | 失败回调 |


### signInList:onFailed:()
`- (void)signInList:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

获取签到活动列表，管理员可通过该接口获取签到活动列表（只有主持人或联席主持人能够调用）。

| 参数 | 描述 |
| :--- | --- |
| onSuccess | 成功回调，参考文档：[SEASignInListModel]() |
| onFailed | 失败回调 |


### signInCount:onSuccess:onFailed:()
`- (void)signInCount:(NSInteger)epoch onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

统计人数，管理员可通过该接口获取当前签到人数（只有主持人或联席主持人能够调用）。

| 参数 | 描述 |
| :--- | --- |
| epoch | 签到轮次，从0开始 |
| onSuccess | 成功回调，参考文档：[SEASignInCountModel]() |
| onFailed | 失败回调 |


### signInFinish:onFailed:()
`- (void)signInFinish:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

结束签到活动，管理员可通过该接口结束签到活动（只有主持人或联席主持人能够调用），SDK会通过 `MeetingKitDelegate` 中的  [onSignInFinish:epoch:()]() 回调通知给全体会中成员。

| 参数 | 描述 |
| :--- | --- |
| onSuccess | 成功回调 |
| onFailed | 失败回调 |


### signInDetail:onSuccess:onFailed:()
`- (void)signInDetail:(NSInteger)epoch onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

获取签到活动详情，管理员可通过该接口获取签到记录（只有主持人或联席主持人能够调用）。

| 参数 | 描述 |
| :--- | --- |
| epoch | 签到轮次，从0开始 |
| onSuccess | 成功回调，参考文档：[SEASignInDetailListModel]() |
| onFailed | 失败回调 |


### signInSign:onFailed:()
`- (void)signInSign:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

用户签到，当管理员发起签到活动后，会中成员可通过该接口完成签到。

| 参数 | 描述 |
| :--- | --- |
| onSuccess | 成功回调 |
| onFailed | 失败回调 |


### signInExportDetail:onSuccess:onFailed:()
`- (void)signInExportDetail:(NSInteger)epoch onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

导出签到数据，管理员可通过该接口导出签到数据，同时SDK会回调列表本地地址（只有主持人或联席主持人能够调用）。

| 参数 | 描述 |
| :--- | --- |
| epoch | 签到轮次，从0开始 |
| onSuccess | 成功回调，文件地址 |
| onFailed | 失败回调 |


## 屏幕共享接口
### stopScreenRecord()
`- (void)stopScreenRecord`

宿主程序主动关闭屏幕采集

此方法在宿主程序中使用，用于用户主动关闭屏幕共享使用。

关闭屏幕采集后，SDK会通过 `MeetingKitDelegate` 中的 [onScreenRecordStatus:()](https://www.yuque.com/anyconf/eanoso/rfflpfbuav0xc28g#iRVUP) 回调通知您当前设备采集状态。此时，需要根据回调状态选择调用 请求开启共享 还是 关闭共享。

### broadcastStartedWithAppGroup:delegate:()
`- (void)broadcastStartedWithAppGroup:(NSString *)appGroup delegate:(id<MeetingKitScreenDelegate>)delegate`

扩展程序开启屏幕录制方法，并绑定委托代理

此方法在扩展程序`SampleHandler`中使用。

关闭屏幕采集后，SDK会通过 `MeetingKitDelegate` 中的 [onScreenRecordStatus:()](https://www.yuque.com/anyconf/eanoso/rfflpfbuav0xc28g#iRVUP) 回调通知您当前设备采集状态。此时，需要根据回调状态选择调用 请求开启共享 还是 关闭共享。

| 参数 | 描述 |
| :--- | --- |
| appGroup | 应用分组标识符 |
| delegate | 屏幕录制扩展代理，参考文档：[屏幕录制](https://www.yuque.com/anyconf/eanoso/by65hp8d8zfxyd8k) |


### sendSampleBuffer:withType:()
`- (void)sendSampleBuffer:(CMSampleBufferRef)sampleBuffer withType:(RPSampleBufferType)sampleBufferType`

扩展程序发送屏幕采集帧数据

此方法在扩展程序`SampleHandler`中使用

| 参数 | 描述 |
| :--- | --- |
| sampleBuffer | 数据帧 |
| sampleBufferType | 数据帧类型，包括：视频、音频等 |

### publishScreenViewCaptureWithPixelBuffer:displayAngle:()
`- (void)publishScreenViewCaptureWithPixelBuffer:(CVPixelBufferRef)pixelBuffer displayAngle:(int)displayAngle`

发布视图录制的共享流，即：用户可以通过该接口送入与屏幕共享共用轨道的视频流数据。

**参数**

| pixelBuffer |  UIView采集的像素数据(CVPixelBufferRef) |
| --- | --- |
| displayAngle | 显示角度(0/90/180/270) |

### enabledViewCaptureShare:()
`- (RTCEngineError)enabledViewCaptureShare:(BOOL)enabled`

设置视图采集共享，该接口用来通知SDK，当前共享屏幕轨道推送的是屏幕采集流还是视图录制流；在调用`publishScreenViewCaptureWithPixelBuffer:displayAngle:()`之前需先调该接口进行SDK标记。

**参数**

| enabled |  启用状态 YES-开启 NO-关闭 |
| --- | --- |


## 数据管理接口
### getMySelf()
`- (SEAUserModel *)getMySelf`

获取本地登录用户的基本信息

返回值说明：

[SEAUserModel](https://www.yuque.com/anyconf/eanoso/gkeau9oyh5vms80z#pnMcF) 用户数据。

### findMemberWithUserId:()
`- (SEAUserModel *)findMemberWithUserId:(NSString *)userId`

获取指定远端用户的基本信息

返回值说明：

[SEAUserModel](https://www.yuque.com/anyconf/eanoso/gkeau9oyh5vms80z#pnMcF) 用户数据。

### getRemoteUsers()
`- (NSArray<SEAUserModel *> *)getRemoteUsers`

获取当前所在房间的成员列表

返回值说明：

[SEAUserModel](https://www.yuque.com/anyconf/eanoso/gkeau9oyh5vms80z#pnMcF) 用户数据。

### getRoomDetails()
`- (SEARoomModel *)getRoomDetails`

获取当前所在房间的基本信息

返回值说明：

[SEARoomModel](https://www.yuque.com/anyconf/eanoso/gkeau9oyh5vms80z#tcVka) 用户数据。

### getDrawingHost()
`- (NSString *)getDrawingHost`

获取电子画板访问地址

返回值说明：

电子画板采用网页形式实现，该接口只有在加入房间成功后调用有效并返回电子画板访问地址。 

## 媒体配置相关接口
### setStreamMediaConfig:()
`- (void)setStreamMediaConfig:(SEAMediaConfig *)config`

设置媒体配置参数

可通过该接口设置视频编码、音频编码、视频帧率、视频码流等参数。

**参数**

| config | 流媒体配置参数，用于指定视频编码、音频编码、视频帧率、视频码流等基本信息详情请参考 [SEAMediaConfig](https://www.yuque.com/anyconf/eanoso/gkeau9oyh5vms80z#pMzBp) |
| --- | --- |


### setNetworkQosParam:()
`- (void)setNetworkQosParam:(SEANetworkQosParam *)param`

设置网络质量控制参数

可通过该接口设置延迟自适应档位、延时抗抖动等级、码率自适应开关、网络自适应开关等参数。

**参数**

| param | 质量控制参数，用于指定延迟自适应档位、延时抗抖动等级、码率自适应开关、网络自适应开关等基本信息详情请参考 [SEANetworkQosParam](https://www.yuque.com/anyconf/eanoso/gkeau9oyh5vms80z#rUmBV) |
| --- | --- |


## 调试相关接口
### setDebugParam:()
`- (void)setDebugParam:(SEADebugParam *)param`

设置调试参数

可通过该接口设置调试地址、保存音视频流等参数。

**参数**

| param | 调试参数，用于设置调试地址、保存音视频流等基本信息详情请参考 [SEADebugParam](https://www.yuque.com/anyconf/eanoso/gkeau9oyh5vms80z#tdyrN) |
| --- | --- |


