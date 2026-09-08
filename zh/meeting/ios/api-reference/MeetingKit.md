---
title: "MeetingKit"
description: "会议组件全局入口单例：登录登出、即时通讯、会议查询与预约、房间实例的创建与查询、本地采集预览、音频路由与屏幕采集进程接入"
---

`MeetingKit` 是一个进程内只存在一个实例的单例对象，只承载**账号级与设备级**能力：登录、即时通讯、本地采集与预览、音频路由、屏幕采集进程侧接入，以及会议的查询与预约。

会中的一切操作与事件都属于房间维度，通过 `createRoomWithDelegate:` 创建 [MeetingKitRoom](/zh/meeting/ios/api-reference/MeetingKitRoom) 实例进行。同一账号可以同时创建并加入多个房间，各房间的媒体与业务状态相互独立。

<Warning>
自 `2.0.0` 起，会中接口已从本类移出。`enterRoom:onSuccess:onFailed:`、`requestOpenCamera:view:onSuccess:onFailed:`、`sendRoomChatMessage:messageType:targetId:onSuccess:onFailed:`、`adminXxx` 系列、云录制、等候室、分组讨论、签到等接口请改用 [MeetingKitRoom](/zh/meeting/ios/api-reference/MeetingKitRoom)。
</Warning>

## 核心基础接口
### sharedInstance()
`+ (MeetingKit *)sharedInstance`

创建 MeetingKit 实例（单例模式）。

### version()
`- (NSString *)version`

获取 MeetingKit 版本号。

### addDelegate:()
`- (void)addDelegate:(id <MeetingKitDelegate>)delegate`

设置全局事件回调

您可以通过 [MeetingKitDelegate](/zh/meeting/ios/api-reference/MeetingKitDelegate) 获得音频路由变更与应用性能两类全局事件通知。房间内的事件请实现 [MeetingKitRoomDelegate](/zh/meeting/ios/api-reference/MeetingKitRoomDelegate) 并在创建房间时传入。

| 参数 | 描述 |
| :--- | --- |
| delegate | 监听实例 |


### createRoomWithDelegate:()
`- (nullable MeetingKitRoom *)createRoomWithDelegate:(nullable id<MeetingKitRoomDelegate>)delegate`

创建独立会议房间实例

每次调用都会返回一个新的 [MeetingKitRoom](/zh/meeting/ios/api-reference/MeetingKitRoom) 实例，实例之间互不影响。需要同时加入多个房间时，多次调用并分别持有各自的实例即可。

调用房间的 `exitRoom:` 后该实例即失效，需要重新创建。

| 参数 | 描述 |
| :--- | --- |
| delegate | 房间事件代理，参考 [MeetingKitRoomDelegate](/zh/meeting/ios/api-reference/MeetingKitRoomDelegate) |


### getRooms()
`- (NSArray<MeetingKitRoom *> *)getRooms`

获取当前已经加入的会议房间列表

已创建但尚未入会、或者已经退出的实例不会出现在结果中。

### loginWithToken:appGroup:onSuccess:onFailed:()
`- (void)loginWithToken:(NSString *)token appGroup:(NSString *)appGroup onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

登录接口，您需要先初始化用户信息后才能进入房间，并进行一系列的操作。

该接口默认启用全进程本地日志采集。

| 参数 | 描述 |
| :--- | --- |
| token | 用户令牌 |
| appGroup | 应用分组标识符 |
| onSuccess | 成功回调 |
| onFailed | 失败回调 |


### loginWithToken:appGroup:logConfig:onSuccess:onFailed:()
`- (void)loginWithToken:(NSString *)token appGroup:(NSString *)appGroup logConfig:(SEALogConfig *)logConfig onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

使用自定义日志配置登录。您需要先初始化用户信息后才能进入房间，并进行一系列的操作。

| 参数 | 描述 |
| :--- | --- |
| token | 用户令牌 |
| appGroup | 应用分组标识符 |
| logConfig | 日志配置，参考[SEALogConfig](/zh/meeting/ios/types#sealogconfig) |
| onSuccess | 成功回调 |
| onFailed | 失败回调 |


### logout()
`- (void)logout`

退出登录接口，会离开并销毁全部房间实例、销毁资源，业务层无需逐个调用房间实例的 `exitRoom:`。

## 即时通讯接口
### enableImWithDelegate:onSuccess:onFailed:()
`- (void)enableImWithDelegate:(nullable id<MeetingKitIMDelegate>)delegate onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

启用即时通讯

调用该接口开启 SDK 即时通讯服务，开发者可以利用该服务实现，如会前呼叫、通知等业务功能。

| 参数 | 描述 |
| :--- | --- |
| delegate | 委托代理，参考文档：[MeetingKitIMDelegate](/zh/meeting/ios/api-reference/MeetingKitIMDelegate) |
| onSuccess | 成功回调 |
| onFailed | 失败回调 |


### disableIm()
`- (void)disableIm`

停用即时通讯

当您不再需要即时通讯服务时，可通过该接口进行停用。

## 会议操作接口
### getMeetingList:onFailed:()
`- (void)getMeetingList:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

获取会议列表

| 参数 | 描述 |
| :--- | --- |
| onSuccess | 成功回调，参考文档：[SEAMeetingListModel](/zh/meeting/ios/types#seameetinglistmodel) |
| onFailed | 失败回调 |


### getMoreMeetingList:onFailed:()
`- (void)getMoreMeetingList:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

获取更多会议列表（翻页操作）

| 参数 | 描述 |
| :--- | --- |
| onSuccess | 成功回调，参考文档：[SEAMeetingListModel](/zh/meeting/ios/types#seameetinglistmodel) |
| onFailed | 失败回调 |


### getHistoryMeetingList:onFailed:()
`- (void)getHistoryMeetingList:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

获取历史会议列表

| 参数 | 描述 |
| :--- | --- |
| onSuccess | 成功回调，参考文档：[SEAMeetingListModel](/zh/meeting/ios/types#seameetinglistmodel) |
| onFailed | 失败回调 |


### getMoreHistoryMeetingList:onFailed:()
`- (void)getMoreHistoryMeetingList:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

获取更多历史会议列表（翻页操作）

| 参数 | 描述 |
| :--- | --- |
| onSuccess | 成功回调，参考文档：[SEAMeetingListModel](/zh/meeting/ios/types#seameetinglistmodel) |
| onFailed | 失败回调 |


### getMeetingDetailsWithMeetingId:onSuccess:onFailed:()
`- (void)getMeetingDetailsWithMeetingId:(NSString *)meetingId onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

获取会议详情

| 参数 | 描述 |
| :--- | --- |
| meetingId | 会议标识 |
| onSuccess | 成功回调，参考文档：[SEAMeetingModel](/zh/meeting/ios/types#seameetingmodel) |
| onFailed | 失败回调 |


### getMeetingDetailsWithRoomNo:onSuccess:onFailed:()
`- (void)getMeetingDetailsWithRoomNo:(NSString *)roomNo onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

获取会议详情

| 参数 | 描述 |
| :--- | --- |
| roomNo | 房间号码 |
| onSuccess | 成功回调，参考文档：[SEAMeetingModel](/zh/meeting/ios/types#seameetingmodel) |
| onFailed | 失败回调 |


### getParticipantListsWithMeetingId:onSuccess:onFailed:()
`- (void)getParticipantListsWithMeetingId:(NSString *)meetingId onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

获取参会人员列表

| 参数 | 描述 |
| :--- | --- |
| meetingId | 会议标识 |
| onSuccess | 成功回调，参考文档：[SEAMemberListModel](/zh/meeting/ios/types#seamemberlistmodel) |
| onFailed | 失败回调 |


### getMoreParticipantListsWithMeetingId:onSuccess:onFailed:()
`- (void)getMoreParticipantListsWithMeetingId:(NSString *)meetingId onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

获取更多参会人员列表（翻页操作）

| 参数 | 描述 |
| :--- | --- |
| meetingId | 会议标识 |
| onSuccess | 成功回调，参考文档：[SEAMemberListModel](/zh/meeting/ios/types#seamemberlistmodel) |
| onFailed | 失败回调 |


### requestCancelMeetingWithMeetingId:onSuccess:onFailed:()
`- (void)requestCancelMeetingWithMeetingId:(NSString *)meetingId onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

请求取消会议

| 参数 | 描述 |
| :--- | --- |
| meetingId | 会议标识 |
| onSuccess | 成功回调 |
| onFailed | 失败回调 |


### createRoom:onSuccess:onFailed:()
`- (void)createRoom:(SEAMeetingParam *)params onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

创建房间

| 参数 | 描述 |
| :--- | --- |
| params | 创建房间参数，参考文档：[SEAMeetingParam](/zh/meeting/ios/types#seameetingparam) |
| onSuccess | 成功回调 |
| onFailed | 失败回调 |


### updateRoom:onSuccess:onFailed:()
`- (void)updateRoom:(SEAMeetingParam *)params onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

修改房间数据

| 参数 | 描述 |
| :--- | --- |
| params | 修改房间参数，参考文档：[SEAMeetingParam](/zh/meeting/ios/types#seameetingparam) |
| onSuccess | 成功回调 |
| onFailed | 失败回调 |

## 用户操作接口
### getAgentList:keyword:onSuccess:onFailed:()
`- (void)getAgentList:(NSArray <NSNumber *> *)typesList keyword:(nullable NSString *)keyword onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

获取设备列表

| 参数 | 描述 |
| :--- | --- |
| typesList | 设备类型列表，设备类型可参看 [SEAAgentType](/zh/meeting/ios/types#seaagenttype) 声明定义 |
| keyword | 关键词 |
| onSuccess | 成功回调，参考文档：[SEAAgentListModel](/zh/meeting/ios/types#seaagentlistmodel) |
| onFailed | 失败回调 |


### getMoreAgentList:keyword:onSuccess:onFailed:()
`- (void)getMoreAgentList:(NSArray <NSNumber *> *)typesList keyword:(nullable NSString *)keyword onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed`

获取更多设备列表（翻页操作）

| 参数 | 描述 |
| :--- | --- |
| typesList | 设备类型列表，设备类型可参看 [SEAAgentType](/zh/meeting/ios/types#seaagenttype) 声明定义 |
| keyword | 关键词 |
| onSuccess | 成功回调，参考文档：[SEAAgentListModel](/zh/meeting/ios/types#seaagentlistmodel) |
| onFailed | 失败回调 |

## 本地采集相关接口
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

设置前置摄像头本地预览镜像偏好

仅作用于本地预览画面，不影响推流数据。前置摄像头按 `mirror` 取值设置镜像，后置摄像头始终不镜像；切换摄像头后 SDK 会自动应用对应策略。

| 参数 | 描述 |
| :--- | --- |
| mirror | YES-前置摄像头镜像 NO-前置摄像头不镜像 |


### currentCameraDirection()
`- (SEACameraDirection)currentCameraDirection`

获取当前摄像头方向

调用该接口，SDK 会返回当前采集使用的摄像头方向，参考 [SEACameraDirection](/zh/meeting/ios/types#seacameradirection)。

## 音频路由相关接口
### switchAudioRoute:()
`- (void)switchAudioRoute:(SEAAudioRoute)route`

切换音频路由

该接口用于请求切换内置音频播放设备，如扬声器、听筒。存在蓝牙或有线耳机时，外设选择由 iOS 决定。最终实际路由以 `currentAudioRoute` 和 `MeetingKitDelegate` 中的 [onAudioRouteChange:previousRoute:()](/zh/meeting/ios/api-reference/MeetingKitDelegate#onaudioroutechangepreviousroute) 回调为准。

| 参数 | 描述 |
| :--- | --- |
| route | 音频路由，参考文档：[SEAAudioRoute](/zh/meeting/ios/types#seaaudioroute) |


### currentAudioRoute()
`- (SEAAudioRoute)currentAudioRoute`

获取系统当前实际音频路由

调用该接口，SDK 会返回系统当前实际使用的音频路由，如扬声器、听筒、蓝牙或有线耳机。参考 [SEAAudioRoute](/zh/meeting/ios/types#seaaudioroute)。

### headphoneDeviceAvailable()
`- (BOOL)headphoneDeviceAvailable`

是否存在有线耳机设备

调用该接口，SDK 会通过该接口返回是否存在有线耳机设备。

### bluetoothDeviceAvailable()
`- (BOOL)bluetoothDeviceAvailable`

是否存在蓝牙耳机设备

调用该接口，SDK 会通过该接口返回是否存在蓝牙耳机设备。

## 虚拟背景接口
虚拟背景作用于进程内唯一的共享摄像头采集链路，属设备级能力，设置会同时作用于全部房间。会中切换摄像头、断线重连后 SDK 会自动把当前配置重新应用，调用方不必自己补。用法详见 [虚拟背景](/zh/meeting/ios/advanced/virtual-background)。

### installVirtualBackground:()
`- (SEAError)installVirtualBackground:(nullable NSString *)modelPath`

装载虚拟背景组件

建议在进入房间、打开摄像头之前调用；装载后需要再调 [enabledVirtualBackground:()](#enabledvirtualbackground) 才会生效。

| 参数 | 描述 |
| :--- | --- |
| modelPath | 人像分割模型（`selfie_segmenter_fixed.onnx`）文件路径，传 `nil` 使用 SDK 内置的那一份 |

| 返回值 | 描述 |
| :--- | --- |
| SEAErrorOK | 装载成功 |
| SEAErrorConflict | 组件已装载，本次指令被丢弃 |
| SEAErrorNotFound | 模型文件不存在，检查 `modelPath` |
| SEAErrorSystemError | 推理会话创建失败，属于运行环境问题 |


### uninstallVirtualBackground()
`- (void)uninstallVirtualBackground`

卸载虚拟背景组件

释放推理会话与相关缓冲。

### enabledVirtualBackground:()
`- (SEAError)enabledVirtualBackground:(BOOL)enabled`

虚拟背景功能开关

装载后默认不开启，需要显式打开。关闭后是零开销直通，不再跑推理。组件未装载时调用返回 `SEAErrorConflict`。

| 参数 | 描述 |
| :--- | --- |
| enabled | YES-开启 NO-关闭 |


### setVirtualBackgroundBlur:()
`- (void)setVirtualBackgroundBlur:(NSInteger)level`

设置背景虚化

与 [setVirtualBackgroundImage:()](#setvirtualbackgroundimage) 互斥，后调用的生效。

| 参数 | 描述 |
| :--- | --- |
| level | 虚化等级，取值范围 `1`-`10`，默认 `5`，超出范围会被收敛到边界值 |


### setVirtualBackgroundImage:()
`- (void)setVirtualBackgroundImage:(nullable UIImage *)image`

设置背景替换

与 [setVirtualBackgroundBlur:()](#setvirtualbackgroundblur) 互斥，后调用的生效。

| 参数 | 描述 |
| :--- | --- |
| image | 背景图片，按 cover 裁剪不拉伸；传 `nil` 表示取消替换回到虚化 |


### setVirtualBackgroundInferenceInterval:()
`- (void)setVirtualBackgroundInferenceInterval:(NSInteger)interval`

设置分割推理间隔

给调用方按机型下发的性能档，不建议暴露给终端用户。

| 参数 | 描述 |
| :--- | --- |
| interval | 分割每 N 帧跑一次（合成仍每帧跑），默认 `1`，小于 `1` 按 `1` 处理；低端机可调大保帧率 |


### setVirtualBackgroundMaskSync:()
`- (void)setVirtualBackgroundMaskSync:(BOOL)enabled`

设置蒙版对齐

消除挥手时的错位拖影，代价是画面更新率降到蒙版率。`interval` 为 `1` 时开与不开没有任何区别，它只在调大推理间隔后才起作用。

| 参数 | 描述 |
| :--- | --- |
| enabled | YES-开启 NO-关闭，默认 NO |


### isVirtualBackgroundEnabled()
`- (BOOL)isVirtualBackgroundEnabled`

获取虚拟背景开启状态

## 屏幕共享接口
### broadcastStartedWithAppGroup:delegate:()
`- (void)broadcastStartedWithAppGroup:(NSString *)appGroup delegate:(id<MeetingKitScreenDelegate>)delegate`

扩展程序开启屏幕录制方法，并绑定委托代理

此方法在扩展程序`SampleHandler`中使用。

关闭屏幕采集后，SDK 会通过 `MeetingKitRoomDelegate` 中的 [meetingRoom:onScreenRecordStatus:()](/zh/meeting/ios/api-reference/MeetingKitRoomDelegate) 回调通知您当前设备采集状态。此时，需要根据回调状态选择调用 请求开启共享 还是 关闭共享。

| 参数 | 描述 |
| :--- | --- |
| appGroup | 应用分组标识符 |
| delegate | 屏幕录制扩展代理，参考文档：[屏幕录制](/zh/meeting/ios/advanced/screen-recording) |


### sendSampleBuffer:withType:()
`- (void)sendSampleBuffer:(CMSampleBufferRef)sampleBuffer withType:(RPSampleBufferType)sampleBufferType`

扩展程序发送屏幕采集帧数据

此方法在扩展程序`SampleHandler`中使用

| 参数 | 描述 |
| :--- | --- |
| sampleBuffer | 数据帧 |
| sampleBufferType | 数据帧类型，包括：视频、音频等 |
