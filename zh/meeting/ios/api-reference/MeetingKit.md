## <font style="color:rgb(0, 0, 0);">核心基础接口</font>
### sharedInstance()
`+ (MeetingKit *)sharedInstance`

<font style="color:rgb(0, 0, 0);">创建 </font>MeetingKit<font style="color:rgb(0, 0, 0);"> 实例（单例模式）。</font>

### <font style="color:rgb(0, 0, 0);">version()</font>
`<font style="color:rgb(0, 0, 0);">- (NSString *)version</font>`

<font style="color:rgb(0, 0, 0);">获取 MeetingKit 版本号。</font>

### <font style="color:rgb(0, 0, 0);">addDelegate:()</font>
`<font style="color:rgb(0, 0, 0);">- (void)addDelegate:(id <MeetingKitDelegate>)delegate</font>`

<font style="color:rgb(0, 0, 0);">设置 MeetingKit 事件回调</font>

<font style="color:rgb(0, 0, 0);">您可以通过 </font>`<font style="color:rgb(0, 0, 0);">MeetingKitDelegate</font>`<font style="color:rgb(0, 0, 0);"> 协议获得各类回调事件通知，例如：错误码，远端用户进房间，音视频状态参数等）。</font>

| <font style="color:#8A8F8D;">参数</font> | <font style="color:#8A8F8D;">描述</font> |
| :--- | --- |
| <font style="color:rgb(0, 0, 0);">delegate</font> | <font style="color:rgb(0, 0, 0);">监听实例</font> |


### <font style="color:rgb(0, 0, 0);">loginWithToken:appGroup:onSuccess:onFailed:()</font>
`<font style="color:rgb(0, 0, 0);">- (void)loginWithToken:(NSString *)token appGroup:(NSString *)appGroup onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed</font>`

<font style="color:rgb(0, 0, 0);">登录接口，</font>您需要先初始化用户信息后才能进入房间，并进行一系列的操作<font style="color:rgb(0, 0, 0);">。</font>

| <font style="color:#8A8F8D;">参数</font> | <font style="color:#8A8F8D;">描述</font> |
| :--- | --- |
| <font style="color:rgb(0, 0, 0);">token</font> | <font style="color:rgb(0, 0, 0);">用户令牌</font> |
| <font style="color:rgb(0, 0, 0);">appGroup</font> | <font style="color:rgb(0, 0, 0);">应用分组标识符</font> |
| <font style="color:rgb(0, 0, 0);">onSuccess</font> | <font style="color:rgb(0, 0, 0);">成功回调</font> |
| <font style="color:rgb(0, 0, 0);">onFailed</font> | <font style="color:rgb(0, 0, 0);">失败回调</font> |


### <font style="color:rgb(0, 0, 0);">logout()</font>
`<font style="color:rgb(0, 0, 0);">- (void)logout</font>`

<font style="color:rgb(0, 0, 0);">退出登录接口，</font>会有主动离开房间操作、销毁资源等<font style="color:rgb(0, 0, 0);">。</font>

## <font style="color:rgb(0, 0, 0);">即时通讯接口</font>
### <font style="color:rgb(0, 0, 0);">enableImWithDelegate:onSuccess:onFailed:()</font>
`<font style="color:rgb(0, 0, 0);">- (void)enableImWithDelegate:(nullable id<MeetingKitIMDelegate>)delegate onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed</font>`

<font style="color:rgb(0, 0, 0);">启用即时通讯</font>

<font style="color:rgb(0, 0, 0);">调用该接口开启 SDK 即时通讯服务，开发者可以利用该服务实现，如会前呼叫、通知等业务功能。</font>

| <font style="color:#8A8F8D;">参数</font> | <font style="color:#8A8F8D;">描述</font> |
| :--- | --- |
| <font style="color:rgb(0, 0, 0);">delegate</font> | <font style="color:rgb(0, 0, 0);">委托代理，参考文档：</font>[MeetingKitIMDelegate](https://www.yuque.com/anyconf/eanoso/wh4gigxazm9esngc) |
| <font style="color:rgb(0, 0, 0);">onSuccess</font> | <font style="color:rgb(0, 0, 0);">成功回调</font> |
| <font style="color:rgb(0, 0, 0);">onFailed</font> | <font style="color:rgb(0, 0, 0);">失败回调</font> |


### <font style="color:rgb(0, 0, 0);">disableIm()</font>
`<font style="color:rgb(0, 0, 0);">- (void)disableIm</font>`

<font style="color:rgb(0, 0, 0);">停用即时通讯</font>

<font style="color:rgb(0, 0, 0);">当您不再需要即时通讯服务时，可通过该接口进行停用。</font>

## <font style="color:rgb(0, 0, 0);">通话操作接口</font>
### <font style="color:rgb(0, 0, 0);">callUser:onSuccess:onFailed:()</font>
`<font style="color:rgb(0, 0, 0);">- (void)callUser:(NSArray <NSString *> *)userIdLists onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed</font>`

<font style="color:rgb(0, 0, 0);">发起通话</font>

<font style="color:rgb(0, 0, 0);">会中主持人可以通过该接口呼叫成员，呼叫成员后，SDK会通过 </font>`<font style="color:rgb(0, 0, 0);">MeetingKitIMDelegate</font>`<font style="color:rgb(0, 0, 0);"> 中的 </font>[onCallReceived:nickname:roomNo:title:()](https://www.yuque.com/anyconf/eanoso/wh4gigxazm9esngc#Vjtg3)<font style="color:rgb(0, 0, 0);"> 回调通知对应用户。</font>

| <font style="color:#8A8F8D;">参数</font> | <font style="color:#8A8F8D;">描述</font> |
| :--- | --- |
| <font style="color:rgb(0, 0, 0);">userIdLists</font> | 用户标识列表 |
| <font style="color:rgb(0, 0, 0);">onSuccess</font> | <font style="color:rgb(0, 0, 0);">成功回调</font> |
| <font style="color:rgb(0, 0, 0);">onFailed</font> | <font style="color:rgb(0, 0, 0);">失败回调</font> |


## <font style="color:rgb(0, 0, 0);">会议操作接口</font>
### <font style="color:rgb(0, 0, 0);">getMeetingList:onFailed:()</font>
`<font style="color:rgb(0, 0, 0);">- (void)getMeetingList:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed</font>`

获取会议列表

| <font style="color:#8A8F8D;">参数</font> | <font style="color:#8A8F8D;">描述</font> |
| :--- | --- |
| <font style="color:rgb(0, 0, 0);">onSuccess</font> | <font style="color:rgb(0, 0, 0);">成功回调，参考文档：</font>[SEAMeetingListModel](https://www.yuque.com/anyconf/eanoso/gkeau9oyh5vms80z#wSvDN) |
| <font style="color:rgb(0, 0, 0);">onFailed</font> | <font style="color:rgb(0, 0, 0);">失败回调</font> |


### <font style="color:rgb(0, 0, 0);">getMoreMeetingList:onFailed:()</font>
`<font style="color:rgb(0, 0, 0);">- (void)getMoreMeetingList:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed</font>`

获取更多会议列表（翻页操作）

| <font style="color:#8A8F8D;">参数</font> | <font style="color:#8A8F8D;">描述</font> |
| :--- | --- |
| <font style="color:rgb(0, 0, 0);">onSuccess</font> | <font style="color:rgb(0, 0, 0);">成功回调，参考文档：</font>[SEAMeetingListModel](https://www.yuque.com/anyconf/eanoso/gkeau9oyh5vms80z#wSvDN) |
| <font style="color:rgb(0, 0, 0);">onFailed</font> | <font style="color:rgb(0, 0, 0);">失败回调</font> |


### <font style="color:rgb(0, 0, 0);">getHistoryMeetingList:onFailed:()</font>
`<font style="color:rgb(0, 0, 0);">- (void)getHistoryMeetingList:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed</font>`

获取历史会议列表

| <font style="color:#8A8F8D;">参数</font> | <font style="color:#8A8F8D;">描述</font> |
| :--- | --- |
| <font style="color:rgb(0, 0, 0);">onSuccess</font> | <font style="color:rgb(0, 0, 0);">成功回调，参考文档：</font>[SEAMeetingListModel](https://www.yuque.com/anyconf/eanoso/gkeau9oyh5vms80z#wSvDN) |
| <font style="color:rgb(0, 0, 0);">onFailed</font> | <font style="color:rgb(0, 0, 0);">失败回调</font> |


### <font style="color:rgb(0, 0, 0);">getHistoryMeetingList:onFailed:()</font>
`<font style="color:rgb(0, 0, 0);">- (void)getHistoryMeetingList:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed</font>`

获取历史会议列表

| <font style="color:#8A8F8D;">参数</font> | <font style="color:#8A8F8D;">描述</font> |
| :--- | --- |
| <font style="color:rgb(0, 0, 0);">onSuccess</font> | <font style="color:rgb(0, 0, 0);">成功回调，参考文档：</font>[SEAMeetingListModel](https://www.yuque.com/anyconf/eanoso/gkeau9oyh5vms80z#wSvDN) |
| <font style="color:rgb(0, 0, 0);">onFailed</font> | <font style="color:rgb(0, 0, 0);">失败回调</font> |


### <font style="color:rgb(0, 0, 0);">getMeetingDetailsWithMeetingId:onSuccess:onFailed:()</font>
`<font style="color:rgb(0, 0, 0);">- (void)getMeetingDetailsWithMeetingId:(NSString *)meetingId onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed</font>`

获取会议详情

| <font style="color:#8A8F8D;">参数</font> | <font style="color:#8A8F8D;">描述</font> |
| :--- | --- |
| <font style="color:rgb(0, 0, 0);">meetingId</font> | <font style="color:rgb(0, 0, 0);">会议标识</font> |
| <font style="color:rgb(0, 0, 0);">onSuccess</font> | <font style="color:rgb(0, 0, 0);">成功回调，参考文档：</font>[SEAMeetingModel](https://www.yuque.com/anyconf/eanoso/gkeau9oyh5vms80z#NwAZR) |
| <font style="color:rgb(0, 0, 0);">onFailed</font> | <font style="color:rgb(0, 0, 0);">失败回调</font> |


### <font style="color:rgb(0, 0, 0);">getMeetingDetailsWithRoomNo:onSuccess:onFailed:()</font>
`<font style="color:rgb(0, 0, 0);">- (void)getMeetingDetailsWithRoomNo:(NSString *)roomNo onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed</font>`

获取会议详情

| <font style="color:#8A8F8D;">参数</font> | <font style="color:#8A8F8D;">描述</font> |
| :--- | --- |
| <font style="color:rgb(0, 0, 0);">roomNo</font> | <font style="color:rgb(0, 0, 0);">房间号码</font> |
| <font style="color:rgb(0, 0, 0);">onSuccess</font> | <font style="color:rgb(0, 0, 0);">成功回调，参考文档：</font>[SEAMeetingModel](https://www.yuque.com/anyconf/eanoso/gkeau9oyh5vms80z#NwAZR) |
| <font style="color:rgb(0, 0, 0);">onFailed</font> | <font style="color:rgb(0, 0, 0);">失败回调</font> |


### <font style="color:rgb(0, 0, 0);">getParticipantListsWithMeetingId:onSuccess:onFailed:()</font>
`<font style="color:rgb(0, 0, 0);">- (void)getParticipantListsWithMeetingId:(NSString *)meetingId onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed</font>`

获取参会人员列表

| <font style="color:#8A8F8D;">参数</font> | <font style="color:#8A8F8D;">描述</font> |
| :--- | --- |
| <font style="color:rgb(0, 0, 0);">meetingId</font> | <font style="color:rgb(0, 0, 0);">会议标识</font> |
| <font style="color:rgb(0, 0, 0);">onSuccess</font> | <font style="color:rgb(0, 0, 0);">成功回调，参考文档：</font>[SEAMemberListModel](https://www.yuque.com/anyconf/eanoso/gkeau9oyh5vms80z#c6qYV) |
| <font style="color:rgb(0, 0, 0);">onFailed</font> | <font style="color:rgb(0, 0, 0);">失败回调</font> |


### <font style="color:rgb(0, 0, 0);">getMoreParticipantListsWithMeetingId:onSuccess:onFailed:()</font>
`<font style="color:rgb(0, 0, 0);">- (void)getMoreParticipantListsWithMeetingId:(NSString *)meetingId onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed</font>`

获取更多参会人员列表（翻页操作）

| <font style="color:#8A8F8D;">参数</font> | <font style="color:#8A8F8D;">描述</font> |
| :--- | --- |
| <font style="color:rgb(0, 0, 0);">meetingId</font> | <font style="color:rgb(0, 0, 0);">会议标识</font> |
| <font style="color:rgb(0, 0, 0);">onSuccess</font> | <font style="color:rgb(0, 0, 0);">成功回调，参考文档：</font>[SEAMemberListModel](https://www.yuque.com/anyconf/eanoso/gkeau9oyh5vms80z#c6qYV) |
| <font style="color:rgb(0, 0, 0);">onFailed</font> | <font style="color:rgb(0, 0, 0);">失败回调</font> |


### <font style="color:rgb(0, 0, 0);">requestCancelMeetingWithMeetingId:onSuccess:onFailed:()</font>
`<font style="color:rgb(0, 0, 0);">- (void)requestCancelMeetingWithMeetingId:(NSString *)meetingId onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed</font>`

请求取消会议

| <font style="color:#8A8F8D;">参数</font> | <font style="color:#8A8F8D;">描述</font> |
| :--- | --- |
| <font style="color:rgb(0, 0, 0);">meetingId</font> | <font style="color:rgb(0, 0, 0);">会议标识</font> |
| <font style="color:rgb(0, 0, 0);">onSuccess</font> | <font style="color:rgb(0, 0, 0);">成功回调</font> |
| <font style="color:rgb(0, 0, 0);">onFailed</font> | <font style="color:rgb(0, 0, 0);">失败回调</font> |


## <font style="color:rgb(0, 0, 0);">用户操作接口</font>
### <font style="color:rgb(0, 0, 0);">getAgentList:keyword:onSuccess:onFailed:()</font>
`<font style="color:rgb(0, 0, 0);">- (void)getAgentList:(NSArray <NSNumber *> *)typesList keyword:(nullable NSString *)keyword onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed</font>`

获取设备列表

| <font style="color:#8A8F8D;">参数</font> | <font style="color:#8A8F8D;">描述</font> |
| :--- | --- |
| <font style="color:rgb(0, 0, 0);">typesList</font> | <font style="color:rgb(0, 0, 0);">设备类型列表，设备类型可参看 </font>[SEAAgentType](https://www.yuque.com/anyconf/eanoso/gkeau9oyh5vms80z#rv0G4)<font style="color:rgb(0, 0, 0);"> 声明定义</font> |
| <font style="color:rgb(0, 0, 0);">keyword</font> | <font style="color:rgb(0, 0, 0);">关键词</font> |
| <font style="color:rgb(0, 0, 0);">onSuccess</font> | <font style="color:rgb(0, 0, 0);">成功回调，参考文档：</font>[SEAAgentListModel](https://www.yuque.com/anyconf/eanoso/gkeau9oyh5vms80z#AzvcZ) |
| <font style="color:rgb(0, 0, 0);">onFailed</font> | <font style="color:rgb(0, 0, 0);">失败回调</font> |


### <font style="color:rgb(0, 0, 0);">getMoreAgentList:keyword:onSuccess:onFailed:()</font>
`<font style="color:rgb(0, 0, 0);">- (void)getMoreAgentList:(NSArray <NSNumber *> *)typesList keyword:(nullable NSString *)keyword onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed</font>`

获取更多设备列表（翻页操作）

| <font style="color:#8A8F8D;">参数</font> | <font style="color:#8A8F8D;">描述</font> |
| :--- | --- |
| <font style="color:rgb(0, 0, 0);">typesList</font> | <font style="color:rgb(0, 0, 0);">设备类型列表，设备类型可参看 </font>[SEAAgentType](https://www.yuque.com/anyconf/eanoso/gkeau9oyh5vms80z#rv0G4)<font style="color:rgb(0, 0, 0);"> 声明定义</font> |
| <font style="color:rgb(0, 0, 0);">keyword</font> | <font style="color:rgb(0, 0, 0);">关键词</font> |
| <font style="color:rgb(0, 0, 0);">onSuccess</font> | <font style="color:rgb(0, 0, 0);">成功回调，参考文档：</font>[SEAAgentListModel](https://www.yuque.com/anyconf/eanoso/gkeau9oyh5vms80z#AzvcZ) |
| <font style="color:rgb(0, 0, 0);">onFailed</font> | <font style="color:rgb(0, 0, 0);">失败回调</font> |


### <font style="color:rgb(0, 0, 0);">createRoom:onSuccess:onFailed:()</font>
`<font style="color:rgb(0, 0, 0);">- (void)createRoom:(SEAMeetingParam *)params onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed</font>`

创建房间

| <font style="color:#8A8F8D;">参数</font> | <font style="color:#8A8F8D;">描述</font> |
| :--- | --- |
| <font style="color:rgb(0, 0, 0);">params</font> | <font style="color:rgb(0, 0, 0);">创建房间参数，参考文档：</font>[SEAMeetingParam](https://www.yuque.com/anyconf/eanoso/gkeau9oyh5vms80z#gQ8nA) |
| <font style="color:rgb(0, 0, 0);">onSuccess</font> | <font style="color:rgb(0, 0, 0);">成功回调</font> |
| <font style="color:rgb(0, 0, 0);">onFailed</font> | <font style="color:rgb(0, 0, 0);">失败回调</font> |


### <font style="color:rgb(0, 0, 0);">updateRoom:onSuccess:onFailed:()</font>
`<font style="color:rgb(0, 0, 0);">- (void)updateRoom:(SEAMeetingParam *)params onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed</font>`

修改房间数据

| <font style="color:#8A8F8D;">参数</font> | <font style="color:#8A8F8D;">描述</font> |
| :--- | --- |
| <font style="color:rgb(0, 0, 0);">params</font> | <font style="color:rgb(0, 0, 0);">修改房间参数，参考文档：</font>[SEAMeetingParam](https://www.yuque.com/anyconf/eanoso/gkeau9oyh5vms80z#gQ8nA) |
| <font style="color:rgb(0, 0, 0);">onSuccess</font> | <font style="color:rgb(0, 0, 0);">成功回调</font> |
| <font style="color:rgb(0, 0, 0);">onFailed</font> | <font style="color:rgb(0, 0, 0);">失败回调</font> |


### <font style="color:rgb(0, 0, 0);">enterRoom:onSuccess:onFailed:()</font>
`<font style="color:rgb(0, 0, 0);">- (void)enterRoom:(SEAMeetingEnterParam *)params onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed</font>`

加入房间

加入房间后，SDK会通过 `<font style="color:rgb(0, 0, 0);">MeetingKitDelegate</font>` 中的 [onUserEnter:()](https://www.yuque.com/anyconf/eanoso/rfflpfbuav0xc28g#Pre1r) 回调通知房间内用户。

| <font style="color:#8A8F8D;">参数</font> | <font style="color:#8A8F8D;">描述</font> |
| :--- | --- |
| <font style="color:rgb(0, 0, 0);">params</font> | <font style="color:rgb(0, 0, 0);">加入房间参数，参考文档：</font>[SEAMeetingEnterParam](https://www.yuque.com/anyconf/eanoso/gkeau9oyh5vms80z#OLcoA) |
| <font style="color:rgb(0, 0, 0);">onSuccess</font> | <font style="color:rgb(0, 0, 0);">成功回调</font> |
| <font style="color:rgb(0, 0, 0);">onFailed</font> | <font style="color:rgb(0, 0, 0);">失败回调</font> |


### <font style="color:rgb(0, 0, 0);">exitRoom:()</font>
`<font style="color:rgb(0, 0, 0);">- (void)exitRoom:(nullable SEASuccessBlock)onSuccess</font>`

离开房间

离开房间后，SDK会通过 `<font style="color:rgb(0, 0, 0);">MeetingKitDelegate</font>` 中的 [onUserExit:()](https://www.yuque.com/anyconf/eanoso/rfflpfbuav0xc28g#RimbD) 回调通知房间内用户。

| <font style="color:#8A8F8D;">参数</font> | <font style="color:#8A8F8D;">描述</font> |
| :--- | --- |
| <font style="color:rgb(0, 0, 0);">onSuccess</font> | <font style="color:rgb(0, 0, 0);">完成回调</font> |


### <font style="color:rgb(0, 0, 0);">updateName:onSuccess:onFailed:()</font>
`<font style="color:rgb(0, 0, 0);">- (void)updateName:(NSString *)username onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed</font>`

用户更新昵称

用户更新昵称后，SDK会通过 `<font style="color:rgb(0, 0, 0);">MeetingKitDelegate</font>` 中的 [onUserNameChanged:nickname:()](https://www.yuque.com/anyconf/eanoso/rfflpfbuav0xc28g#Gx6nw) 回调通知房间内用户。

| <font style="color:#8A8F8D;">参数</font> | <font style="color:#8A8F8D;">描述</font> |
| :--- | --- |
| <font style="color:rgb(0, 0, 0);">username</font> | 新昵称 |
| <font style="color:rgb(0, 0, 0);">onSuccess</font> | <font style="color:rgb(0, 0, 0);">成功回调</font> |
| <font style="color:rgb(0, 0, 0);">onFailed</font> | <font style="color:rgb(0, 0, 0);">失败回调</font> |


### <font style="color:rgb(0, 0, 0);">requestOpenCamera:view:onSuccess:onFailed:()</font>
`<font style="color:rgb(0, 0, 0);">- (void)requestOpenCamera:(BOOL)frontCamera view:(VIEW_CLASS *)view onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed</font>`

请求打开摄像头

在房间内打开本地摄像头后，默认推送本地视频流，SDK会通过 `<font style="color:rgb(0, 0, 0);">MeetingKitDelegate</font>`<font style="color:rgb(0, 0, 0);"> </font>中的 [onUserCameraStateChanged:cameraState:reason:()](https://www.yuque.com/anyconf/eanoso/rfflpfbuav0xc28g#JEQIr) 回调通知房间内用户。

| <font style="color:#8A8F8D;">参数</font> | <font style="color:#8A8F8D;">描述</font> |
| :--- | --- |
| <font style="color:rgb(0, 0, 0);">frontCamera</font> | 摄像头方向，YES-前置摄像头 NO-后置摄像头 |
| <font style="color:rgb(0, 0, 0);">view</font> | 视频渲染视图 |
| <font style="color:rgb(0, 0, 0);">onSuccess</font> | <font style="color:rgb(0, 0, 0);">成功回调</font> |
| <font style="color:rgb(0, 0, 0);">onFailed</font> | <font style="color:rgb(0, 0, 0);">失败回调</font> |


### <font style="color:rgb(0, 0, 0);">requestOpenMic:onFailed:()</font>
`<font style="color:rgb(0, 0, 0);">- (void)requestOpenMic:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed</font>`

请求打开麦克风

在房间内打开本地麦克风后，SDK会通过 `<font style="color:rgb(0, 0, 0);">MeetingKitDelegate</font>`<font style="color:rgb(0, 0, 0);"> </font>中的 [onUserMicStateChanged:micState:reason:()](https://www.yuque.com/anyconf/eanoso/rfflpfbuav0xc28g#yI7Vo) 回调通知房间内用户。

| <font style="color:#8A8F8D;">参数</font> | <font style="color:#8A8F8D;">描述</font> |
| :--- | --- |
| <font style="color:rgb(0, 0, 0);">onSuccess</font> | <font style="color:rgb(0, 0, 0);">成功回调</font> |
| <font style="color:rgb(0, 0, 0);">onFailed</font> | <font style="color:rgb(0, 0, 0);">失败回调</font> |


### <font style="color:rgb(0, 0, 0);">closeCamera:onFailed:()</font>
`<font style="color:rgb(0, 0, 0);">- (void)closeCamera:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed</font>`

关闭摄像头

在房间内关闭本地摄像头后，SDK会通过 `<font style="color:rgb(0, 0, 0);">MeetingKitDelegate</font>`<font style="color:rgb(0, 0, 0);"> </font>中的 [onUserCameraStateChanged:cameraState:reason:()](https://www.yuque.com/anyconf/eanoso/rfflpfbuav0xc28g#JEQIr) 回调通知房间内用户。

| <font style="color:#8A8F8D;">参数</font> | <font style="color:#8A8F8D;">描述</font> |
| :--- | --- |
| <font style="color:rgb(0, 0, 0);">onSuccess</font> | <font style="color:rgb(0, 0, 0);">成功回调</font> |
| <font style="color:rgb(0, 0, 0);">onFailed</font> | <font style="color:rgb(0, 0, 0);">失败回调</font> |


### <font style="color:rgb(0, 0, 0);">closeMic:onFailed:()</font>
`<font style="color:rgb(0, 0, 0);">- (void)closeMic:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed</font>`

关闭麦克风

在房间内关闭本地麦克风后，SDK会通过 `<font style="color:rgb(0, 0, 0);">MeetingKitDelegate</font>`<font style="color:rgb(0, 0, 0);"> </font>中的 [onUserMicStateChanged:micState:reason:()](https://www.yuque.com/anyconf/eanoso/rfflpfbuav0xc28g#yI7Vo) 回调通知房间内用户。

| <font style="color:#8A8F8D;">参数</font> | <font style="color:#8A8F8D;">描述</font> |
| :--- | --- |
| <font style="color:rgb(0, 0, 0);">onSuccess</font> | <font style="color:rgb(0, 0, 0);">成功回调</font> |
| <font style="color:rgb(0, 0, 0);">onFailed</font> | <font style="color:rgb(0, 0, 0);">失败回调</font> |


### <font style="color:rgb(0, 0, 0);">requestShare:onSuccess:onFailed:()</font>
`<font style="color:rgb(0, 0, 0);">- (void)requestShare:(SEAShareType)shareType onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed</font>`

请求开启共享

开启共享后，SDK会通过 `<font style="color:rgb(0, 0, 0);">MeetingKitDelegate</font>`<font style="color:rgb(0, 0, 0);"> </font>中的 [onRoomShareStart:shareType:()](https://www.yuque.com/anyconf/eanoso/rfflpfbuav0xc28g#UF8Js) 回调通知房间内用户。

| <font style="color:#8A8F8D;">参数</font> | <font style="color:#8A8F8D;">描述</font> |
| :--- | --- |
| <font style="color:rgb(0, 0, 0);">shareType</font> | <font style="color:rgb(0, 0, 0);">共享类型，参考文档：</font>[SEAShareType](https://www.yuque.com/anyconf/eanoso/gkeau9oyh5vms80z#Ww9uW) |
| <font style="color:rgb(0, 0, 0);">onSuccess</font> | <font style="color:rgb(0, 0, 0);">成功回调</font> |
| <font style="color:rgb(0, 0, 0);">onFailed</font> | <font style="color:rgb(0, 0, 0);">失败回调</font> |


### <font style="color:rgb(0, 0, 0);">stopShare:onFailed:()</font>
`<font style="color:rgb(0, 0, 0);">- (void)stopShare:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed</font>`

关闭共享

关闭共享后，SDK会通过 `<font style="color:rgb(0, 0, 0);">MeetingKitDelegate</font>`<font style="color:rgb(0, 0, 0);"> </font>中的 [onRoomShareStop:shareType:()](https://www.yuque.com/anyconf/eanoso/rfflpfbuav0xc28g#WTGVD) 回调通知房间内用户。

| <font style="color:#8A8F8D;">参数</font> | <font style="color:#8A8F8D;">描述</font> |
| :--- | --- |
| <font style="color:rgb(0, 0, 0);">shareType</font> | <font style="color:rgb(0, 0, 0);">共享类型，参考文档：</font>[SEAShareType](https://www.yuque.com/anyconf/eanoso/gkeau9oyh5vms80z#Ww9uW) |
| <font style="color:rgb(0, 0, 0);">onSuccess</font> | <font style="color:rgb(0, 0, 0);">成功回调</font> |
| <font style="color:rgb(0, 0, 0);">onFailed</font> | <font style="color:rgb(0, 0, 0);">失败回调</font> |


### <font style="color:rgb(0, 0, 0);">sendRoomChatMessage:messageType:targetId:onSuccess:onFailed:()</font>
`<font style="color:rgb(0, 0, 0);">- (void)sendRoomChatMessage:(NSString *)message messageType:(SEAMessageType)messageType targetId:(nullable NSString *)targetId onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed</font>`

发送聊天消息

发送聊天消息后，SDK会通过 `<font style="color:rgb(0, 0, 0);">MeetingKitDelegate</font>`<font style="color:rgb(0, 0, 0);"> </font>中的 [onReceiveChatMessage:message:messageType:()](https://www.yuque.com/anyconf/eanoso/rfflpfbuav0xc28g#CHAuV) 回调通知房间内用户。

| <font style="color:#8A8F8D;">参数</font> | <font style="color:#8A8F8D;">描述</font> |
| :--- | --- |
| <font style="color:rgb(0, 0, 0);">message</font> | 聊天消息 |
| <font style="color:rgb(0, 0, 0);">messageType</font> | <font style="color:rgb(0, 0, 0);">消息类型，参考文档：</font>[SEAMessageType](https://www.yuque.com/anyconf/eanoso/gkeau9oyh5vms80z#xlxGu) |
| <font style="color:rgb(0, 0, 0);">targetId</font> | <font style="color:rgb(0, 0, 0);">目标标识，为空时表示全房间接收</font> |
| <font style="color:rgb(0, 0, 0);">onSuccess</font> | <font style="color:rgb(0, 0, 0);">成功回调</font> |
| <font style="color:rgb(0, 0, 0);">onFailed</font> | <font style="color:rgb(0, 0, 0);">失败回调</font> |


### <font style="color:rgb(0, 0, 0);">sendRoomCustomMessage:targetId:onSuccess:onFailed:()</font>
`<font style="color:rgb(0, 0, 0);">- (void)sendRoomCustomMessage:(NSString *)message targetId:(nullable NSString *)targetId onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed</font>`

发送自定义消息

发送自定义消息后，SDK会通过 `<font style="color:rgb(0, 0, 0);">MeetingKitDelegate</font>`<font style="color:rgb(0, 0, 0);"> </font>中的 [onReceiveChatMessage:message:messageType:()](https://www.yuque.com/anyconf/eanoso/rfflpfbuav0xc28g#CHAuV) 回调通知房间内用户。

| <font style="color:#8A8F8D;">参数</font> | <font style="color:#8A8F8D;">描述</font> |
| :--- | --- |
| <font style="color:rgb(0, 0, 0);">message</font> | 聊天消息 |
| <font style="color:rgb(0, 0, 0);">targetId</font> | <font style="color:rgb(0, 0, 0);">目标标识，为空时表示全房间接收</font> |
| <font style="color:rgb(0, 0, 0);">onSuccess</font> | <font style="color:rgb(0, 0, 0);">成功回调</font> |
| <font style="color:rgb(0, 0, 0);">onFailed</font> | <font style="color:rgb(0, 0, 0);">失败回调</font> |


### <font style="color:rgb(0, 0, 0);">getChatList:onFailed:()</font>
`<font style="color:rgb(0, 0, 0);">- (void)getChatList:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed</font>`

获取聊天列表

| <font style="color:#8A8F8D;">参数</font> | <font style="color:#8A8F8D;">描述</font> |
| :--- | --- |
| <font style="color:rgb(0, 0, 0);">onSuccess</font> | <font style="color:rgb(0, 0, 0);">成功回调，参考文档：</font>[SEAChatListModel](https://www.yuque.com/anyconf/eanoso/gkeau9oyh5vms80z#kvOQP) |
| <font style="color:rgb(0, 0, 0);">onFailed</font> | <font style="color:rgb(0, 0, 0);">失败回调</font> |


### <font style="color:rgb(0, 0, 0);">getMoreChatList:onFailed:()</font>
`<font style="color:rgb(0, 0, 0);">- (void)getMoreChatList:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed</font>`

获取更多聊天列表（翻页操作）

| <font style="color:#8A8F8D;">参数</font> | <font style="color:#8A8F8D;">描述</font> |
| :--- | --- |
| <font style="color:rgb(0, 0, 0);">onSuccess</font> | <font style="color:rgb(0, 0, 0);">成功回调，参考文档：</font>[SEAChatListModel](https://www.yuque.com/anyconf/eanoso/gkeau9oyh5vms80z#kvOQP) |
| <font style="color:rgb(0, 0, 0);">onFailed</font> | <font style="color:rgb(0, 0, 0);">失败回调</font> |


### <font style="color:rgb(0, 0, 0);">requestHandup:onSuccess:onFailed:()</font>
`<font style="color:rgb(0, 0, 0);">- (void)requestHandup:(SEAHandupType)handupType onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed</font>`

请求举手

请求举手后，SDK会通过 `<font style="color:rgb(0, 0, 0);">MeetingKitDelegate</font>`<font style="color:rgb(0, 0, 0);"> </font>中的 [onRoomHandUpChanged:enable:handupType:()](https://www.yuque.com/anyconf/eanoso/rfflpfbuav0xc28g#XjjFx) 回调通知房间内管理成员。

| <font style="color:#8A8F8D;">参数</font> | <font style="color:#8A8F8D;">描述</font> |
| :--- | --- |
| <font style="color:rgb(0, 0, 0);">handupType</font> | 聊天消息<font style="color:rgb(0, 0, 0);">，参考文档：</font>[SEAHandupType](https://www.yuque.com/anyconf/eanoso/gkeau9oyh5vms80z#P2v0K) |
| <font style="color:rgb(0, 0, 0);">onSuccess</font> | <font style="color:rgb(0, 0, 0);">成功回调</font> |
| <font style="color:rgb(0, 0, 0);">onFailed</font> | <font style="color:rgb(0, 0, 0);">失败回调</font> |


### <font style="color:rgb(0, 0, 0);">cancelHandup:onSuccess:onFailed:()</font>
`<font style="color:rgb(0, 0, 0);">- (void)cancelHandup:(SEAHandupType)handupType onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed</font>`

取消举手

取消举手后，SDK会通过 `<font style="color:rgb(0, 0, 0);">MeetingKitDelegate</font>`<font style="color:rgb(0, 0, 0);"> </font>中的 [onRoomHandUpChanged:enable:handupType:()](https://www.yuque.com/anyconf/eanoso/rfflpfbuav0xc28g#XjjFx) 回调通知房间内管理成员。

| <font style="color:#8A8F8D;">参数</font> | <font style="color:#8A8F8D;">描述</font> |
| :--- | --- |
| <font style="color:rgb(0, 0, 0);">handupType</font> | 举手类型<font style="color:rgb(0, 0, 0);">，参考文档：</font>[SEAHandupType](https://www.yuque.com/anyconf/eanoso/gkeau9oyh5vms80z#P2v0K) |
| <font style="color:rgb(0, 0, 0);">onSuccess</font> | <font style="color:rgb(0, 0, 0);">成功回调</font> |
| <font style="color:rgb(0, 0, 0);">onFailed</font> | <font style="color:rgb(0, 0, 0);">失败回调</font> |


### <font style="color:rgb(0, 0, 0);">confirmAdminOpenCamera:frontCamera:view:onSuccess:onFailed:()</font>
`<font style="color:rgb(0, 0, 0);">- (void)confirmAdminOpenCamera:(NSString *)targetId frontCamera:(BOOL)frontCamera view:(VIEW_CLASS *)view onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed</font>`

回复同意打开摄像头请求

当收到主持人或联席主持人邀请您开启摄像头，如果您同意开启摄像头，需要调用该接口回复给对应管理人员；举手后，收到主持人或联席主持人的处理结果通知，如果您需要开启摄像头，同样需要调用该接口回复给对应管理人员。

回复同意打开摄像头请求后，SDK会通过 `<font style="color:rgb(0, 0, 0);">MeetingKitDelegate</font>`<font style="color:rgb(0, 0, 0);"> </font>中的 [onUserCameraStateChanged:cameraState:reason:()](https://www.yuque.com/anyconf/eanoso/rfflpfbuav0xc28g#JEQIr) 回调通知房间内管理成员。

| <font style="color:#8A8F8D;">参数</font> | <font style="color:#8A8F8D;">描述</font> |
| :--- | --- |
| <font style="color:rgb(0, 0, 0);">targetId</font> | 目标标识，请求或同意您开启摄像头请求的管理者标识 |
| <font style="color:rgb(0, 0, 0);">frontCamera</font> | 摄像头方向，YES-前置摄像头 NO-后置摄像头 |
| <font style="color:rgb(0, 0, 0);">view</font> | 视频渲染视图 |
| <font style="color:rgb(0, 0, 0);">onSuccess</font> | <font style="color:rgb(0, 0, 0);">成功回调</font> |
| <font style="color:rgb(0, 0, 0);">onFailed</font> | <font style="color:rgb(0, 0, 0);">失败回调</font> |


### <font style="color:rgb(0, 0, 0);">confirmAdminOpenMic:onSuccess:onFailed:()</font>
`<font style="color:rgb(0, 0, 0);">- (void)confirmAdminOpenMic:(NSString *)targetId onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed</font>`

回复同意打开麦克风请求

当收到主持人或联席主持人邀请您开启麦克风，如果您同意开启麦克风，需要调用该接口回复给对应管理人员；举手后，收到主持人或联席主持人的处理结果通知，如果您需要开启麦克风，同样需要调用该接口回复给对应管理人员。

回复同意打开麦克风请求后，SDK会通过 `<font style="color:rgb(0, 0, 0);">MeetingKitDelegate</font>`<font style="color:rgb(0, 0, 0);"> </font>中的 [onUserMicStateChanged:micState:reason:()](https://www.yuque.com/anyconf/eanoso/rfflpfbuav0xc28g#awVw0) 回调通知房间内管理成员。

| <font style="color:#8A8F8D;">参数</font> | <font style="color:#8A8F8D;">描述</font> |
| :--- | --- |
| <font style="color:rgb(0, 0, 0);">targetId</font> | 目标标识，请求或同意您开启麦克风请求的管理者标识 |
| <font style="color:rgb(0, 0, 0);">onSuccess</font> | <font style="color:rgb(0, 0, 0);">成功回调</font> |
| <font style="color:rgb(0, 0, 0);">onFailed</font> | <font style="color:rgb(0, 0, 0);">失败回调</font> |


### <font style="color:rgb(0, 0, 0);">confirmAdminRoomShare:shareType:onSuccess:onFailed:()</font>
`<font style="color:rgb(0, 0, 0);">- (void)confirmAdminRoomShare:(NSString *)targetId shareType:(SEAShareType)shareType onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed</font>`

回复同意打开房间共享请求

当收到主持人或联席主持人邀请您开启共享，如果您同意开启共享，需要调用该接口回复给对应管理人员；举手后，收到主持人或联席主持人的处理结果通知，如果您需要开启共享，同样需要调用该接口回复给对应管理人员。

回复同意打开共享请求后，SDK会通过 `<font style="color:rgb(0, 0, 0);">MeetingKitDelegate</font>`<font style="color:rgb(0, 0, 0);"> </font>中的 [onRoomShareStart:shareType:()](https://www.yuque.com/anyconf/smeeting/rfflpfbuav0xc28g#F0DEZ) 回调通知房间内管理成员。

| <font style="color:#8A8F8D;">参数</font> | <font style="color:#8A8F8D;">描述</font> |
| :--- | --- |
| <font style="color:rgb(0, 0, 0);">targetId</font> | 目标标识，请求或同意您开启房间共享请求的管理者标识 |
| <font style="color:rgb(0, 0, 0);">shareType</font> | 共享类型<font style="color:rgb(0, 0, 0);">，参考文档：</font>[SEAShareType](https://www.yuque.com/anyconf/eanoso/gkeau9oyh5vms80z#Ww9uW) |
| <font style="color:rgb(0, 0, 0);">onSuccess</font> | <font style="color:rgb(0, 0, 0);">成功回调</font> |
| <font style="color:rgb(0, 0, 0);">onFailed</font> | <font style="color:rgb(0, 0, 0);">失败回调</font> |


### <font style="color:rgb(0, 0, 0);">updateLocalView:()</font>
`<font style="color:rgb(0, 0, 0);">- (void)updateLocalView:(VIEW_CLASS *)view</font>`

更新本地摄像头的预览画面

| <font style="color:#8A8F8D;">参数</font> | <font style="color:#8A8F8D;">描述</font> |
| :--- | --- |
| <font style="color:rgb(0, 0, 0);">view</font> | 视频渲染视图 |


### <font style="color:rgb(0, 0, 0);">switchCamera()</font>
`<font style="color:rgb(0, 0, 0);">- (void)switchCamera</font>`

切换摄像头前后置

### <font style="color:rgb(0, 0, 0);">switchSpeaker:()</font>
`<font style="color:rgb(0, 0, 0);">- (void)switchSpeaker:(BOOL)enabled</font>`

切换扬声器状态

用户可通过该接口设置本地音频是否播放。

| <font style="color:#8A8F8D;">参数</font> | <font style="color:#8A8F8D;">描述</font> |
| :--- | --- |
| <font style="color:rgb(0, 0, 0);">enabled</font> | 扬声器状态，YES-开启 NO-关闭 |


### <font style="color:rgb(0, 0, 0);">switchAudioRoute:()</font>
`<font style="color:rgb(0, 0, 0);">- (void)switchAudioRoute:(SEAAudioRoute)route</font>`

切换音频路由

切换音频路由后，SDK会通过 `<font style="color:rgb(0, 0, 0);">MeetingKitDelegate</font>`<font style="color:rgb(0, 0, 0);"> </font>中的 [onAudioRouteChange:previousRoute:()](https://www.yuque.com/anyconf/eanoso/rfflpfbuav0xc28g#AvcCn) 回调通知您。

| <font style="color:#8A8F8D;">参数</font> | <font style="color:#8A8F8D;">描述</font> |
| :--- | --- |
| <font style="color:rgb(0, 0, 0);">route</font> | 音频路由<font style="color:rgb(0, 0, 0);">，参考文档：</font>[SEAAudioRoute](https://www.yuque.com/anyconf/eanoso/gkeau9oyh5vms80z#HhTLs) |


### <font style="color:rgb(0, 0, 0);">currentAudioRoute()</font>
`<font style="color:rgb(0, 0, 0);">- (SEAAudioRoute)currentAudioRoute</font>`

获取当前音频路由

调用该接口，SDK 会通过该接口返回当前的音频路由，<font style="color:rgb(0, 0, 0);">参考文档：</font>[SEAAudioRoute](https://www.yuque.com/anyconf/eanoso/gkeau9oyh5vms80z#HhTLs)。

### <font style="color:rgb(0, 0, 0);">headphoneDeviceAvailable()</font>
`<font style="color:rgb(0, 0, 0);">- (BOOL)headphoneDeviceAvailable</font>`

是否存在有线耳机设备

调用该接口，SDK 会通过该接口返回是否存在有线耳机设备。

### <font style="color:rgb(0, 0, 0);">bluetoothDeviceAvailable()</font>
`<font style="color:rgb(0, 0, 0);">- (BOOL)bluetoothDeviceAvailable</font>`

是否存在蓝牙耳机设备

调用该接口，SDK 会通过该接口返回是否存在蓝牙耳机设备。

### <font style="color:rgb(0, 0, 0);">startRemoteView:streamType:view:()</font>
`<font style="color:rgb(0, 0, 0);">- (void)startRemoteView:(NSString *)userId streamType:(SEAVideoStreamType)streamType view:(VIEW_CLASS *)view</font>`

开始播放远端用户视频

开始播放远端用户视频，并绑定视频渲染资源。

| <font style="color:#8A8F8D;">参数</font> | <font style="color:#8A8F8D;">描述</font> |
| :--- | --- |
| <font style="color:rgb(0, 0, 0);">userId</font> | 远端用户标识 |
| <font style="color:rgb(0, 0, 0);">streamType</font> | 视频流类型<font style="color:rgb(0, 0, 0);">，参考文档：</font>[SEAVideoStreamType](https://www.yuque.com/anyconf/eanoso/gkeau9oyh5vms80z#ckLzs) |
| <font style="color:rgb(0, 0, 0);">view</font> | 视频渲染视图 |


### <font style="color:rgb(0, 0, 0);">stopRemoteView:streamType:()</font>
`<font style="color:rgb(0, 0, 0);">- (void)stopRemoteView:(NSString *)userId streamType:(SEAVideoStreamType)streamType</font>`

停止播放远端用户视频

停止播放远端用户视频，并释放视频渲染资源。

| <font style="color:#8A8F8D;">参数</font> | <font style="color:#8A8F8D;">描述</font> |
| :--- | --- |
| <font style="color:rgb(0, 0, 0);">userId</font> | 远端用户标识 |
| <font style="color:rgb(0, 0, 0);">streamType</font> | 视频流类型<font style="color:rgb(0, 0, 0);">，参考文档：</font>[SEAVideoStreamType](https://www.yuque.com/anyconf/eanoso/gkeau9oyh5vms80z#ckLzs) |


### <font style="color:rgb(0, 0, 0);">stopAllRemoteViewWithUserId:()</font>
`<font style="color:rgb(0, 0, 0);">- (void)stopAllRemoteViewWithUserId:(NSString *)userId</font>`

停止播放远端用户的所有视频

停止播放远端用户的所有视频，并释放全部渲染资源。

| <font style="color:#8A8F8D;">参数</font> | <font style="color:#8A8F8D;">描述</font> |
| :--- | --- |
| <font style="color:rgb(0, 0, 0);">userId</font> | 远端用户标识 |


### <font style="color:rgb(0, 0, 0);">startRemoteMixture:()</font>
`<font style="color:rgb(0, 0, 0);">- (void)startRemoteMixture:(VIEW_CLASS *)view</font>`

订阅远端合成画面视频流

订阅远端合成画面视频流，并绑定视频渲染控件。

| <font style="color:#8A8F8D;">参数</font> | <font style="color:#8A8F8D;">描述</font> |
| :--- | --- |
| <font style="color:rgb(0, 0, 0);">view</font> | 视频渲染视图 |


### <font style="color:rgb(0, 0, 0);">stopRemoteMixture()</font>
`<font style="color:rgb(0, 0, 0);">- (void)stopRemoteMixture</font>`

停止订阅远端合成画面视频流

停止订阅远端合成画面视频流，并释放渲染控件。

## <font style="color:rgb(0, 0, 0);">管理员操作接口</font>
### <font style="color:rgb(0, 0, 0);">adminDestroyRoom:onFailed:()</font>
`<font style="color:rgb(0, 0, 0);">- (void)adminDestroyRoom:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed</font>`

解散房间（只有主持人或联席主持人能够调用）

房间解散后，SDK会通过 `<font style="color:rgb(0, 0, 0);">MeetingKitDelegate</font>`<font style="color:rgb(0, 0, 0);"> </font>中的 [onExitRoom:()](https://www.yuque.com/anyconf/eanoso/rfflpfbuav0xc28g#qZ4ki) 回调通知房间内用户。

| <font style="color:#8A8F8D;">参数</font> | <font style="color:#8A8F8D;">描述</font> |
| :--- | --- |
| <font style="color:rgb(0, 0, 0);">onSuccess</font> | <font style="color:rgb(0, 0, 0);">成功回调</font> |
| <font style="color:rgb(0, 0, 0);">onFailed</font> | <font style="color:rgb(0, 0, 0);">失败回调</font> |


### <font style="color:rgb(0, 0, 0);">adminUpdateRoomCameraState:selfUnmuteCameraDisabled:onSuccess:onFailed:()</font>
`<font style="color:rgb(0, 0, 0);">- (void)adminUpdateRoomCameraState:(BOOL)cameraDisabled selfUnmuteCameraDisabled:(BOOL)selfUnmuteCameraDisabled onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed</font>`

更新房间全体禁视频，控制当前房间内所有用户是否可打开摄像头采集设备的权限状态（只有主持人或联席主持人能够调用）

更新房间全体禁视频后，SDK会通过 `<font style="color:rgb(0, 0, 0);">MeetingKitDelegate</font>`<font style="color:rgb(0, 0, 0);"> </font>中的 [onRoomCameraStateChanged:selfUnmuteCameraDisabled:userId:()](https://www.yuque.com/anyconf/eanoso/rfflpfbuav0xc28g#cgUyr) 回调通知房间内用户。

| <font style="color:#8A8F8D;">参数</font> | <font style="color:#8A8F8D;">描述</font> |
| :--- | --- |
| <font style="color:rgb(0, 0, 0);">cameraDisabled</font> | <font style="color:rgb(0, 0, 0);">房间摄像头禁用状态，YES-禁用 NO-不禁用</font> |
| <font style="color:rgb(0, 0, 0);">selfUnmuteCameraDisabled</font> | <font style="color:rgb(0, 0, 0);">是否禁止自我解除摄像头状态，YES-禁止 NO-不禁止</font> |
| <font style="color:rgb(0, 0, 0);">onSuccess</font> | <font style="color:rgb(0, 0, 0);">成功回调</font> |
| <font style="color:rgb(0, 0, 0);">onFailed</font> | <font style="color:rgb(0, 0, 0);">失败回调</font> |


### <font style="color:rgb(0, 0, 0);">adminUpdateRoomMicState:selfUnmuteMicDisabled:onSuccess:onFailed:()</font>
`<font style="color:rgb(0, 0, 0);">- (void)adminUpdateRoomMicState:(BOOL)micDisabled selfUnmuteMicDisabled:(BOOL)selfUnmuteMicDisabled onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed</font>`

更新房间全体禁音频，控制当前房间内所有用户是否可打开麦克风采集设备的权限状态（只有主持人或联席主持人能够调用）

更新房间全体禁音频后，SDK会通过 `<font style="color:rgb(0, 0, 0);">MeetingKitDelegate</font>`<font style="color:rgb(0, 0, 0);"> </font>中的 [onRoomMicStateChanged:selfUnmuteMicDisabled:userId:()](https://www.yuque.com/anyconf/eanoso/rfflpfbuav0xc28g#rzgdB) 回调通知房间内用户。

| <font style="color:#8A8F8D;">参数</font> | <font style="color:#8A8F8D;">描述</font> |
| :--- | --- |
| <font style="color:rgb(0, 0, 0);">micDisabled</font> | <font style="color:rgb(0, 0, 0);">房间麦克风禁用状态，YES-禁用 NO-不禁用</font> |
| <font style="color:rgb(0, 0, 0);">selfUnmuteMicDisabled</font> | <font style="color:rgb(0, 0, 0);">是否禁止自我解除麦克风状态，YES-禁止 NO-不禁止</font> |
| <font style="color:rgb(0, 0, 0);">onSuccess</font> | <font style="color:rgb(0, 0, 0);">成功回调</font> |
| <font style="color:rgb(0, 0, 0);">onFailed</font> | <font style="color:rgb(0, 0, 0);">失败回调</font> |


### <font style="color:rgb(0, 0, 0);">adminUpdateRoomSelfUnmuteCameraDisabled:onSuccess:onFailed:()</font>
`<font style="color:rgb(0, 0, 0);">- (void)adminUpdateRoomSelfUnmuteCameraDisabled:(BOOL)selfUnmuteCameraDisabled onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed</font>`

更新房间是否禁止自我解除视频状态，控制当前房间内所有用户是否可以自主打开摄像头采集设备的权限状态

更新房间是否禁止自我解除视频状态后，SDK会通过 `<font style="color:rgb(0, 0, 0);">MeetingKitDelegate</font>`<font style="color:rgb(0, 0, 0);"> </font>中的 [onRoomCameraStateChanged:selfUnmuteCameraDisabled:userId:()](https://www.yuque.com/anyconf/eanoso/rfflpfbuav0xc28g#cgUyr) 回调通知房间内用户。

| <font style="color:#8A8F8D;">参数</font> | <font style="color:#8A8F8D;">描述</font> |
| :--- | --- |
| <font style="color:rgb(0, 0, 0);">selfUnmuteCameraDisabled</font> | <font style="color:rgb(0, 0, 0);">是否禁止自我解除摄像头状态，YES-禁止 NO-不禁止</font> |
| <font style="color:rgb(0, 0, 0);">onSuccess</font> | <font style="color:rgb(0, 0, 0);">成功回调</font> |
| <font style="color:rgb(0, 0, 0);">onFailed</font> | <font style="color:rgb(0, 0, 0);">失败回调</font> |


### <font style="color:rgb(0, 0, 0);">adminUpdateRoomSelfUnmuteMicDisabled:onSuccess:onFailed:()</font>
`<font style="color:rgb(0, 0, 0);">- (void)adminUpdateRoomSelfUnmuteMicDisabled:(BOOL)selfUnmuteMicDisabled onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed</font>`

更新房间是否禁止自我解除音频状态，控制当前房间内所有用户是否可以自主打开麦克风采集设备的权限状态

更新房间是否禁止自我解除音频状态后，SDK会通过 `<font style="color:rgb(0, 0, 0);">MeetingKitDelegate</font>`<font style="color:rgb(0, 0, 0);"> </font>中的 [onRoomMicStateChanged:selfUnmuteMicDisabled:userId:()](https://www.yuque.com/anyconf/eanoso/rfflpfbuav0xc28g#rzgdB) 回调通知房间内用户。

| <font style="color:#8A8F8D;">参数</font> | <font style="color:#8A8F8D;">描述</font> |
| :--- | --- |
| <font style="color:rgb(0, 0, 0);">selfUnmuteMicDisabled</font> | <font style="color:rgb(0, 0, 0);">是否禁止自我解除麦克风状态，YES-禁止 NO-不禁止</font> |
| <font style="color:rgb(0, 0, 0);">onSuccess</font> | <font style="color:rgb(0, 0, 0);">成功回调</font> |
| <font style="color:rgb(0, 0, 0);">onFailed</font> | <font style="color:rgb(0, 0, 0);">失败回调</font> |


### <font style="color:rgb(0, 0, 0);">adminUpdateRoomChatDisabled:onSuccess:onFailed:()</font>
`<font style="color:rgb(0, 0, 0);">- (void)adminUpdateRoomChatDisabled:(BOOL)chatDisabled onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed</font>`

更新房间聊天禁用状态，控制当前房间内所有用户是否可进行聊天的权限状态（只有主持人或联席主持人能够调用）

更新房间聊天禁用状态后，SDK会通过 `<font style="color:rgb(0, 0, 0);">MeetingKitDelegate</font>`<font style="color:rgb(0, 0, 0);"> </font>中的 [onRoomChatDisabledChanged:userId:()](https://www.yuque.com/anyconf/eanoso/rfflpfbuav0xc28g#K0Q7N) 回调通知房间内用户。

| <font style="color:#8A8F8D;">参数</font> | <font style="color:#8A8F8D;">描述</font> |
| :--- | --- |
| <font style="color:rgb(0, 0, 0);">chatDisabled</font> | <font style="color:rgb(0, 0, 0);">聊天禁用状态，YES-禁用 NO-不禁用</font> |
| <font style="color:rgb(0, 0, 0);">onSuccess</font> | <font style="color:rgb(0, 0, 0);">成功回调</font> |
| <font style="color:rgb(0, 0, 0);">onFailed</font> | <font style="color:rgb(0, 0, 0);">失败回调</font> |


### <font style="color:rgb(0, 0, 0);">adminUpdateRoomShareDisabled:onSuccess:onFailed:()</font>
`<font style="color:rgb(0, 0, 0);">- (void)adminUpdateRoomShareDisabled:(BOOL)shareDisabled onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed</font>`

更新房间共享禁用状态，控制当前房间内所有用户是否可进行共享的权限状态（只有主持人或联席主持人能够调用）

更新房间共享禁用状态后，SDK会通过 `<font style="color:rgb(0, 0, 0);">MeetingKitDelegate</font>`<font style="color:rgb(0, 0, 0);"> </font>中的 [onRoomShareDisabledChanged:userId:()](https://www.yuque.com/anyconf/eanoso/rfflpfbuav0xc28g#zWldw) 回调通知房间内用户。

| <font style="color:#8A8F8D;">参数</font> | <font style="color:#8A8F8D;">描述</font> |
| :--- | --- |
| <font style="color:rgb(0, 0, 0);">shareDisabled</font> | <font style="color:rgb(0, 0, 0);">共享禁用状态，YES-禁用 NO-不禁用</font> |
| <font style="color:rgb(0, 0, 0);">onSuccess</font> | <font style="color:rgb(0, 0, 0);">成功回调</font> |
| <font style="color:rgb(0, 0, 0);">onFailed</font> | <font style="color:rgb(0, 0, 0);">失败回调</font> |


### <font style="color:rgb(0, 0, 0);">adminUpdateRoomScreenshotDisabled:onSuccess:onFailed:()</font>
`<font style="color:rgb(0, 0, 0);">- (void)adminUpdateRoomScreenshotDisabled:(BOOL)screenshotDisabled onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed</font>`

更新房间截屏开关状态，控制当前房间内所有用户是否可进行截屏的权限状态（只有主持人或联席主持人能够调用）

更新房间截屏开关状态后，SDK会通过 `<font style="color:rgb(0, 0, 0);">MeetingKitDelegate</font>`<font style="color:rgb(0, 0, 0);"> </font>中的 [onRoomScreenshotDisabledChanged:userId:()](https://www.yuque.com/anyconf/eanoso/rfflpfbuav0xc28g#h5kAO) 回调通知房间内用户。

| <font style="color:#8A8F8D;">参数</font> | <font style="color:#8A8F8D;">描述</font> |
| :--- | --- |
| <font style="color:rgb(0, 0, 0);">screenshotDisabled</font> | <font style="color:rgb(0, 0, 0);">截屏禁用状态，YES-禁用 NO-不禁用</font> |
| <font style="color:rgb(0, 0, 0);">onSuccess</font> | <font style="color:rgb(0, 0, 0);">成功回调</font> |
| <font style="color:rgb(0, 0, 0);">onFailed</font> | <font style="color:rgb(0, 0, 0);">失败回调</font> |


### <font style="color:rgb(0, 0, 0);">adminUpdateRoomWatermarkDisabled:onSuccess:onFailed:()</font>
`<font style="color:rgb(0, 0, 0);">- (void)adminUpdateRoomWatermarkDisabled:(BOOL)watermarkDisabled onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed</font>`

更新房间水印开关状态，控制当前房间内是否开启水印状态（只有主持人或联席主持人能够调用）

更新房间水印开关状态后，SDK会通过 `<font style="color:rgb(0, 0, 0);">MeetingKitDelegate</font>`<font style="color:rgb(0, 0, 0);"> </font>中的 [onRoomWatermarkDisabledChanged:userId:()](https://www.yuque.com/anyconf/eanoso/rfflpfbuav0xc28g#dBCP1) 回调通知房间内用户。

| <font style="color:#8A8F8D;">参数</font> | <font style="color:#8A8F8D;">描述</font> |
| :--- | --- |
| <font style="color:rgb(0, 0, 0);">watermarkDisabled</font> | <font style="color:rgb(0, 0, 0);">房间水印状态，YES-开启 NO-关闭</font> |
| <font style="color:rgb(0, 0, 0);">onSuccess</font> | <font style="color:rgb(0, 0, 0);">成功回调</font> |
| <font style="color:rgb(0, 0, 0);">onFailed</font> | <font style="color:rgb(0, 0, 0);">失败回调</font> |


### <font style="color:rgb(0, 0, 0);">adminUpdateRoomLocked:onSuccess:onFailed:()</font>
`<font style="color:rgb(0, 0, 0);">- (void)adminUpdateRoomLocked:(BOOL)locked onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed</font>`

更新房间锁定状态，控制当前房间内是否锁定状态（只有主持人或联席主持人能够调用）

更新房间锁定状态后，SDK会通过 `<font style="color:rgb(0, 0, 0);">MeetingKitDelegate</font>`<font style="color:rgb(0, 0, 0);"> </font>中的 [onRoomLockedChanged:userId:()](https://www.yuque.com/anyconf/eanoso/rfflpfbuav0xc28g#NazqA) 回调通知房间内用户。

| <font style="color:#8A8F8D;">参数</font> | <font style="color:#8A8F8D;">描述</font> |
| :--- | --- |
| <font style="color:rgb(0, 0, 0);">locked</font> | <font style="color:rgb(0, 0, 0);">锁定状态，YES-开启 NO-关闭</font> |
| <font style="color:rgb(0, 0, 0);">onSuccess</font> | <font style="color:rgb(0, 0, 0);">成功回调</font> |
| <font style="color:rgb(0, 0, 0);">onFailed</font> | <font style="color:rgb(0, 0, 0);">失败回调</font> |


### <font style="color:rgb(0, 0, 0);">adminUpdateNickname:nickname:onSuccess:onFailed:()</font>
`<font style="color:rgb(0, 0, 0);">- (void)adminUpdateNickname:(NSString *)userId nickname:(NSString *)nickname onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed</font>`

更新用户昵称（只有主持人或联席主持人能够调用）

更新用户昵称后，SDK会通过 `<font style="color:rgb(0, 0, 0);">MeetingKitDelegate</font>`<font style="color:rgb(0, 0, 0);"> </font>中的 [onUserNameChanged:nickname:()](https://www.yuque.com/anyconf/eanoso/rfflpfbuav0xc28g#Gx6nw) 回调通知房间内用户。

| <font style="color:#8A8F8D;">参数</font> | <font style="color:#8A8F8D;">描述</font> |
| :--- | --- |
| <font style="color:rgb(0, 0, 0);">userId</font> | <font style="color:rgb(0, 0, 0);">用户标识</font> |
| <font style="color:rgb(0, 0, 0);">nickname</font> | <font style="color:rgb(0, 0, 0);">用户昵称</font> |
| <font style="color:rgb(0, 0, 0);">onSuccess</font> | <font style="color:rgb(0, 0, 0);">成功回调</font> |
| <font style="color:rgb(0, 0, 0);">onFailed</font> | <font style="color:rgb(0, 0, 0);">失败回调</font> |


### <font style="color:rgb(0, 0, 0);">adminUpdateUserRole:userRole:onSuccess:onFailed:()</font>
`<font style="color:rgb(0, 0, 0);">- (void)adminUpdateUserRole:(NSString *)userId userRole:(SEAUserRole)userRole onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed</font>`

更新用户角色（只有主持人或联席主持人能够调用）

更新用户角色后，SDK会通过 `<font style="color:rgb(0, 0, 0);">MeetingKitDelegate</font>`<font style="color:rgb(0, 0, 0);"> </font>中的 [onUserRoleChanged:userRole:()](https://www.yuque.com/anyconf/eanoso/rfflpfbuav0xc28g#H2KlN) 回调通知房间内用户。

| <font style="color:#8A8F8D;">参数</font> | <font style="color:#8A8F8D;">描述</font> |
| :--- | --- |
| <font style="color:rgb(0, 0, 0);">userId</font> | <font style="color:rgb(0, 0, 0);">用户标识</font> |
| <font style="color:rgb(0, 0, 0);">userRole</font> | <font style="color:rgb(0, 0, 0);">用户角色，参考文档：</font>[SEAUserRole](https://www.yuque.com/anyconf/eanoso/gkeau9oyh5vms80z#QsCHa) |
| <font style="color:rgb(0, 0, 0);">onSuccess</font> | <font style="color:rgb(0, 0, 0);">成功回调</font> |
| <font style="color:rgb(0, 0, 0);">onFailed</font> | <font style="color:rgb(0, 0, 0);">失败回调</font> |


### <font style="color:rgb(0, 0, 0);">adminMoveHost:onSuccess:onFailed:()</font>
`<font style="color:rgb(0, 0, 0);">- (void)adminMoveHost:(NSString *)userId onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed</font>`

主持人转移（只有主持人或联席主持人能够调用）

主持人转移后，SDK会通过 `<font style="color:rgb(0, 0, 0);">MeetingKitDelegate</font>`<font style="color:rgb(0, 0, 0);"> </font>中的 [onRoomMoveHost:sourceUserId:()](https://www.yuque.com/anyconf/eanoso/rfflpfbuav0xc28g#eRG3J) 回调通知房间内用户。

| <font style="color:#8A8F8D;">参数</font> | <font style="color:#8A8F8D;">描述</font> |
| :--- | --- |
| <font style="color:rgb(0, 0, 0);">userId</font> | <font style="color:rgb(0, 0, 0);">用户标识</font> |
| <font style="color:rgb(0, 0, 0);">onSuccess</font> | <font style="color:rgb(0, 0, 0);">成功回调</font> |
| <font style="color:rgb(0, 0, 0);">onFailed</font> | <font style="color:rgb(0, 0, 0);">失败回调</font> |


### <font style="color:rgb(0, 0, 0);">adminUpdateUserChatDisabled:chatDisabled:onSuccess:onFailed:()</font>
`<font style="color:rgb(0, 0, 0);">- (void)adminUpdateUserChatDisabled:(NSString *)userId chatDisabled:(BOOL)chatDisabled onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed</font>`

主持人更新用户聊天状态（只有主持人或联席主持人能够调用）

主持人更新用户聊天状态后，SDK会通过 `<font style="color:rgb(0, 0, 0);">MeetingKitDelegate</font>`<font style="color:rgb(0, 0, 0);"> </font>中的 [onUserChatDisabledChanged:userId:()](https://www.yuque.com/anyconf/eanoso/rfflpfbuav0xc28g#awVw0) 回调通知房间内目标用户。

| <font style="color:#8A8F8D;">参数</font> | <font style="color:#8A8F8D;">描述</font> |
| :--- | --- |
| <font style="color:rgb(0, 0, 0);">userId</font> | <font style="color:rgb(0, 0, 0);">用户标识</font> |
| <font style="color:rgb(0, 0, 0);">chatDisabled</font> | <font style="color:rgb(0, 0, 0);">禁用状态，YES-禁用 NO-不禁用</font> |
| <font style="color:rgb(0, 0, 0);">onSuccess</font> | <font style="color:rgb(0, 0, 0);">成功回调</font> |
| <font style="color:rgb(0, 0, 0);">onFailed</font> | <font style="color:rgb(0, 0, 0);">失败回调</font> |


### <font style="color:rgb(0, 0, 0);">adminUpdateUserDrawDisabled:drawDisabled:onSuccess:onFailed:()</font>
`<font style="color:rgb(0, 0, 0);">- (void)adminUpdateUserDrawDisabled:(NSString *)userId drawDisabled:(BOOL)drawDisabled onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed</font>`

主持人更新用户涂鸦状态（只有主持人或联席主持人能够调用）

主持人更新用户涂鸦状态后，SDK会通过 `<font style="color:rgb(0, 0, 0);">MeetingKitDelegate</font>`<font style="color:rgb(0, 0, 0);"> </font>中的 [onUserDrawDisabledChanged:userId:()](https://www.yuque.com/anyconf/smeeting/rfflpfbuav0xc28g#p4pR7) 回调通知房间内目标用户。

| <font style="color:#8A8F8D;">参数</font> | <font style="color:#8A8F8D;">描述</font> |
| :--- | --- |
| <font style="color:rgb(0, 0, 0);">userId</font> | <font style="color:rgb(0, 0, 0);">用户标识</font> |
| <font style="color:rgb(0, 0, 0);">drawDisabled</font> | <font style="color:rgb(0, 0, 0);">禁用状态，YES-禁用 NO-不禁用</font> |
| <font style="color:rgb(0, 0, 0);">onSuccess</font> | <font style="color:rgb(0, 0, 0);">成功回调</font> |
| <font style="color:rgb(0, 0, 0);">onFailed</font> | <font style="color:rgb(0, 0, 0);">失败回调</font> |


### <font style="color:rgb(0, 0, 0);">adminRequestUserOpenShare:onSuccess:onFailed:()</font>
`<font style="color:rgb(0, 0, 0);">- (void)adminRequestUserOpenShare:(NSString *)userId onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed</font>`

请求打开成员屏幕共享（只有主持人或联席主持人能够调用）

请求打开成员屏幕共享后，SDK会通过 `<font style="color:rgb(0, 0, 0);">MeetingKitDelegate</font>`<font style="color:rgb(0, 0, 0);"> </font>中的 [onRequestOpenShare:()](https://www.yuque.com/anyconf/eanoso/rfflpfbuav0xc28g#aPi1r) 回调通知房间内指定用户。

| <font style="color:#8A8F8D;">参数</font> | <font style="color:#8A8F8D;">描述</font> |
| :--- | --- |
| <font style="color:rgb(0, 0, 0);">userId</font> | <font style="color:rgb(0, 0, 0);">用户标识</font> |
| <font style="color:rgb(0, 0, 0);">onSuccess</font> | <font style="color:rgb(0, 0, 0);">成功回调</font> |
| <font style="color:rgb(0, 0, 0);">onFailed</font> | <font style="color:rgb(0, 0, 0);">失败回调</font> |


### <font style="color:rgb(0, 0, 0);">adminRequestUserOpenCamera:onSuccess:onFailed:()</font>
`<font style="color:rgb(0, 0, 0);">- (void)adminRequestUserOpenCamera:(NSString *)userId onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed</font>`

请求打开成员摄像头（只有主持人或联席主持人能够调用）

请求打开成员摄像头后，SDK会通过 `<font style="color:rgb(0, 0, 0);">MeetingKitDelegate</font>`<font style="color:rgb(0, 0, 0);"> </font>中的 [onRequestOpenCamera:()](https://www.yuque.com/anyconf/eanoso/rfflpfbuav0xc28g#aPi1r) 回调通知房间内指定用户。

| <font style="color:#8A8F8D;">参数</font> | <font style="color:#8A8F8D;">描述</font> |
| :--- | --- |
| <font style="color:rgb(0, 0, 0);">userId</font> | <font style="color:rgb(0, 0, 0);">用户标识</font> |
| <font style="color:rgb(0, 0, 0);">onSuccess</font> | <font style="color:rgb(0, 0, 0);">成功回调</font> |
| <font style="color:rgb(0, 0, 0);">onFailed</font> | <font style="color:rgb(0, 0, 0);">失败回调</font> |


### <font style="color:rgb(0, 0, 0);">adminCloseUserCamera:onSuccess:onFailed:()</font>
`<font style="color:rgb(0, 0, 0);">- (void)adminCloseUserCamera:(NSString *)userId onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed</font>`

关闭远端用户摄像头（只有主持人或联席主持人能够调用）

关闭远端用户摄像头后，SDK会通过 `<font style="color:rgb(0, 0, 0);">MeetingKitDelegate</font>`<font style="color:rgb(0, 0, 0);"> </font>中的 [onUserCameraStateChanged:cameraState:reason:()](https://www.yuque.com/anyconf/eanoso/rfflpfbuav0xc28g#jE9fm) 回调通知房间内用户。

| <font style="color:#8A8F8D;">参数</font> | <font style="color:#8A8F8D;">描述</font> |
| :--- | --- |
| <font style="color:rgb(0, 0, 0);">userId</font> | <font style="color:rgb(0, 0, 0);">用户标识</font> |
| <font style="color:rgb(0, 0, 0);">onSuccess</font> | <font style="color:rgb(0, 0, 0);">成功回调</font> |
| <font style="color:rgb(0, 0, 0);">onFailed</font> | <font style="color:rgb(0, 0, 0);">失败回调</font> |


### <font style="color:rgb(0, 0, 0);">adminRequestUserOpenMic:onSuccess:onFailed:()</font>
`<font style="color:rgb(0, 0, 0);">- (void)adminRequestUserOpenMic:(NSString *)userId onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed</font>`

请求打开成员麦克风（只有主持人或联席主持人能够调用）

请求打开成员麦克风后，SDK会通过 `<font style="color:rgb(0, 0, 0);">MeetingKitDelegate</font>`<font style="color:rgb(0, 0, 0);"> </font>中的 [onRequestOpenMic:()](https://www.yuque.com/anyconf/eanoso/rfflpfbuav0xc28g#NA5v1) 回调通知房间内指定用户。

| <font style="color:#8A8F8D;">参数</font> | <font style="color:#8A8F8D;">描述</font> |
| :--- | --- |
| <font style="color:rgb(0, 0, 0);">userId</font> | <font style="color:rgb(0, 0, 0);">用户标识</font> |
| <font style="color:rgb(0, 0, 0);">onSuccess</font> | <font style="color:rgb(0, 0, 0);">成功回调</font> |
| <font style="color:rgb(0, 0, 0);">onFailed</font> | <font style="color:rgb(0, 0, 0);">失败回调</font> |


### <font style="color:rgb(0, 0, 0);">adminCloseUserMic:onSuccess:onFailed:()</font>
`<font style="color:rgb(0, 0, 0);">- (void)adminCloseUserMic:(NSString *)userId onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed</font>`

关闭远端用户麦克风（只有主持人或联席主持人能够调用）

关闭远端用户麦克风后，SDK会通过 `<font style="color:rgb(0, 0, 0);">MeetingKitDelegate</font>`<font style="color:rgb(0, 0, 0);"> </font>中的 [onUserMicStateChanged:micState:reason:()](https://www.yuque.com/anyconf/eanoso/rfflpfbuav0xc28g#yI7Vo) 回调通知房间内用户。

| <font style="color:#8A8F8D;">参数</font> | <font style="color:#8A8F8D;">描述</font> |
| :--- | --- |
| <font style="color:rgb(0, 0, 0);">userId</font> | <font style="color:rgb(0, 0, 0);">用户标识</font> |
| <font style="color:rgb(0, 0, 0);">onSuccess</font> | <font style="color:rgb(0, 0, 0);">成功回调</font> |
| <font style="color:rgb(0, 0, 0);">onFailed</font> | <font style="color:rgb(0, 0, 0);">失败回调</font> |


### <font style="color:rgb(0, 0, 0);">adminKickUserOut:onSuccess:onFailed:()</font>
`<font style="color:rgb(0, 0, 0);">- (void)adminKickUserOut:(NSString *)userId onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed</font>`

踢出成员（只有主持人或联席主持人能够调用）

踢出成员后，SDK会通过 `<font style="color:rgb(0, 0, 0);">MeetingKitDelegate</font>`<font style="color:rgb(0, 0, 0);"> </font>中的 [onExitRoom:()](https://www.yuque.com/anyconf/eanoso/rfflpfbuav0xc28g#qZ4ki) 回调通知房间内指定用户。

| <font style="color:#8A8F8D;">参数</font> | <font style="color:#8A8F8D;">描述</font> |
| :--- | --- |
| <font style="color:rgb(0, 0, 0);">userId</font> | <font style="color:rgb(0, 0, 0);">用户标识</font> |
| <font style="color:rgb(0, 0, 0);">onSuccess</font> | <font style="color:rgb(0, 0, 0);">成功回调</font> |
| <font style="color:rgb(0, 0, 0);">onFailed</font> | <font style="color:rgb(0, 0, 0);">失败回调</font> |


### <font style="color:rgb(0, 0, 0);">adminStopRoomShare:onFailed:()</font>
`<font style="color:rgb(0, 0, 0);">- (void)adminStopRoomShare:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed</font>`

关闭共享（只有主持人或联席主持人能够调用）

关闭共享后，SDK会通过 `<font style="color:rgb(0, 0, 0);">MeetingKitDelegate</font>`<font style="color:rgb(0, 0, 0);"> </font>中的 [onAdminRoomShareStop:shareType:()](https://www.yuque.com/anyconf/eanoso/rfflpfbuav0xc28g#oerNu) 回调通知房间内用户。

| <font style="color:#8A8F8D;">参数</font> | <font style="color:#8A8F8D;">描述</font> |
| :--- | --- |
| <font style="color:rgb(0, 0, 0);">onSuccess</font> | <font style="color:rgb(0, 0, 0);">成功回调</font> |
| <font style="color:rgb(0, 0, 0);">onFailed</font> | <font style="color:rgb(0, 0, 0);">失败回调</font> |


### <font style="color:rgb(0, 0, 0);">adminConfirmHandup:handupType:approve:onSuccess:onFailed:()</font>
`<font style="color:rgb(0, 0, 0);">- (void)adminConfirmHandup:(NSString *)userId handupType:(SEAHandupType)handupType approve:(BOOL)approve onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed</font>`

处理举手申请（只有主持人或联席主持人能够调用）

处理举手申请后，SDK会通过 `<font style="color:rgb(0, 0, 0);">MeetingKitDelegate</font>`<font style="color:rgb(0, 0, 0);"> </font>中的 [onHandupConfirm:approve:userId:()](https://www.yuque.com/anyconf/eanoso/rfflpfbuav0xc28g#aFxM1) 回调通知房间指定用户。

| <font style="color:#8A8F8D;">参数</font> | <font style="color:#8A8F8D;">描述</font> |
| :--- | --- |
| <font style="color:rgb(0, 0, 0);">userId</font> | <font style="color:rgb(0, 0, 0);">用户标识</font> |
| <font style="color:rgb(0, 0, 0);">handupType</font> | <font style="color:rgb(0, 0, 0);">举手申请类型</font> |
| <font style="color:rgb(0, 0, 0);">approve</font> | <font style="color:rgb(0, 0, 0);">处理举手结果，YES-同意 NO-拒绝</font> |
| <font style="color:rgb(0, 0, 0);">onSuccess</font> | <font style="color:rgb(0, 0, 0);">成功回调</font> |
| <font style="color:rgb(0, 0, 0);">onFailed</font> | <font style="color:rgb(0, 0, 0);">失败回调</font> |


### <font style="color:rgb(0, 0, 0);">adminUpdateConferee:onSuccess:onFailed:()</font>
`<font style="color:rgb(0, 0, 0);">- (void)adminUpdateConferee:(NSArray <NSString *> *)conferee onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed</font>`

主持人更新受邀成员（只有主持人或联席主持人能够调用）

更新受邀成员后，SDK 会将目标成员添加到会议的受邀成员列表。同时，目标成员也可通过查看待参加会议列表找到该会议。

| <font style="color:#8A8F8D;">参数</font> | <font style="color:#8A8F8D;">描述</font> |
| :--- | --- |
| <font style="color:rgb(0, 0, 0);">conferee</font> | <font style="color:rgb(0, 0, 0);">成员标识列表</font> |
| <font style="color:rgb(0, 0, 0);">onSuccess</font> | <font style="color:rgb(0, 0, 0);">成功回调</font> |
| <font style="color:rgb(0, 0, 0);">onFailed</font> | <font style="color:rgb(0, 0, 0);">失败回调</font> |


### <font style="color:rgb(0, 0, 0);">adminInviteAgent:onSuccess:onFailed:()</font>
`<font style="color:rgb(0, 0, 0);">- (void)adminInviteAgent:(NSArray <SEAInviteModel *> *)invitesList onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed</font>`

主持人邀请设备入会（只有主持人或联席主持人能够调用）

邀请设备入会后，SDK 会将 SIP/H323 等目标设备拉进会议参会，如果当前设备已在其它会议等异常情况 SDK 会通过`onFailed`回调通知具体失败原因。

| <font style="color:#8A8F8D;">参数</font> | <font style="color:#8A8F8D;">描述</font> |
| :--- | --- |
| <font style="color:rgb(0, 0, 0);">invitesList</font> | <font style="color:rgb(0, 0, 0);">邀请列表，参考文档：</font>[SEAInviteModel](https://www.yuque.com/anyconf/eanoso/gkeau9oyh5vms80z#piZiy) |
| <font style="color:rgb(0, 0, 0);">onSuccess</font> | <font style="color:rgb(0, 0, 0);">成功回调</font> |
| <font style="color:rgb(0, 0, 0);">onFailed</font> | <font style="color:rgb(0, 0, 0);">失败回调</font> |


## <font style="color:rgb(0, 0, 0);">云录制相关接口</font>
### <font style="color:rgb(0, 0, 0);">getCloudRecordDetail:onFailed:()</font>
`<font style="color:rgb(0, 0, 0);">- (void)getCloudRecordDetail:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed</font>`

获取云录制详情（只有主持人或联席主持人能够调用）

| <font style="color:#8A8F8D;">参数</font> | <font style="color:#8A8F8D;">描述</font> |
| :--- | --- |
| <font style="color:rgb(0, 0, 0);">onSuccess</font> | <font style="color:rgb(0, 0, 0);">成功回调，参考文档：</font>[SEACloudRecordDetailsModel](https://www.yuque.com/anyconf/eanoso/gkeau9oyh5vms80z#bJyXC) |
| <font style="color:rgb(0, 0, 0);">onFailed</font> | <font style="color:rgb(0, 0, 0);">失败回调</font> |


### <font style="color:rgb(0, 0, 0);">getCloudRecordConfig:onFailed:()</font>
`<font style="color:rgb(0, 0, 0);">- (void)getCloudRecordConfig:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed</font>`

获取云录制配置（只有主持人或联席主持人能够调用）

| <font style="color:#8A8F8D;">参数</font> | <font style="color:#8A8F8D;">描述</font> |
| :--- | --- |
| <font style="color:rgb(0, 0, 0);">onSuccess</font> | <font style="color:rgb(0, 0, 0);">成功回调，参考文档：</font>[SEACloudRecordConfigModel](https://www.yuque.com/anyconf/eanoso/gkeau9oyh5vms80z#zNkwP) |
| <font style="color:rgb(0, 0, 0);">onFailed</font> | <font style="color:rgb(0, 0, 0);">失败回调</font> |


### <font style="color:rgb(0, 0, 0);">startCloudRecord:onSuccess:onFailed:()</font>
`<font style="color:rgb(0, 0, 0);">- (void)startCloudRecord:(SEACloudRecordParam *)params onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed</font>`

开启云录制（只有主持人或联席主持人能够调用）

| <font style="color:#8A8F8D;">参数</font> | <font style="color:#8A8F8D;">描述</font> |
| :--- | --- |
| <font style="color:rgb(0, 0, 0);">params</font> | <font style="color:rgb(0, 0, 0);">云录制参数，参考文档：</font>[SEACloudRecordParam](https://www.yuque.com/anyconf/eanoso/gkeau9oyh5vms80z#hFxgc) |
| <font style="color:rgb(0, 0, 0);">onSuccess</font> | <font style="color:rgb(0, 0, 0);">成功回调</font> |
| <font style="color:rgb(0, 0, 0);">onFailed</font> | <font style="color:rgb(0, 0, 0);">失败回调</font> |


### <font style="color:rgb(0, 0, 0);">stopCloudRecord:onSuccess:onFailed:()</font>
`<font style="color:rgb(0, 0, 0);">- (void)stopCloudRecord:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed</font>`

停止云录制（只有主持人或联席主持人能够调用）

| <font style="color:#8A8F8D;">参数</font> | <font style="color:#8A8F8D;">描述</font> |
| :--- | --- |
| <font style="color:rgb(0, 0, 0);">onSuccess</font> | <font style="color:rgb(0, 0, 0);">成功回调</font> |
| <font style="color:rgb(0, 0, 0);">onFailed</font> | <font style="color:rgb(0, 0, 0);">失败回调</font> |


## <font style="color:rgb(0, 0, 0);">等候室相关接口</font>
### <font style="color:rgb(0, 0, 0);">exitWaitingRoom:onSuccess:()</font>
`<font style="color:rgb(0, 0, 0);">- (void)exitWaitingRoom:(NSString *)roomNo onSuccess:(nullable SEASuccessBlock)onSuccess</font>`

请求离开等候室

用户离开等候室后，SDK会通过 `<font style="color:rgb(0, 0, 0);">MeetingKitDelegate</font>` 中的 [onRoomUserEnterWaitingRoom:()](https://www.yuque.com/anyconf/smeeting/rfflpfbuav0xc28g#xwSvM) 回调通知房间内管理员用户。

| <font style="color:#8A8F8D;">参数</font> | <font style="color:#8A8F8D;">描述</font> |
| :--- | --- |
| <font style="color:rgb(0, 0, 0);">roomNo</font> | 会议号码 |
| <font style="color:rgb(0, 0, 0);">onSuccess</font> | <font style="color:rgb(0, 0, 0);">成功回调</font> |


### <font style="color:rgb(0, 0, 0);">adminUpdateWaitingRoomDisabled:onSuccess:onFailed:()</font>
`<font style="color:rgb(0, 0, 0);">- (void)adminUpdateWaitingRoomDisabled:(BOOL)waitingRoomDisabled onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed</font>`

更新房间等候室禁用状态，控制当前房间内是否开启等候室状态（只有主持人或联席主持人能够调用）

更新房间等候室禁用状态后，SDK会通过 `<font style="color:rgb(0, 0, 0);">MeetingKitDelegate</font>`<font style="color:rgb(0, 0, 0);"> </font>中的 [onRoomWaitingRoomDisabledChanged:userId:()](https://www.yuque.com/anyconf/smeeting/rfflpfbuav0xc28g#dGJps) 回调通知房间内用户。

| <font style="color:#8A8F8D;">参数</font> | <font style="color:#8A8F8D;">描述</font> |
| :--- | --- |
| <font style="color:rgb(0, 0, 0);">waitingRoomDisabled</font> | <font style="color:rgb(0, 0, 0);">房间等候室禁用状态，YES-禁用 NO-不禁用</font> |
| <font style="color:rgb(0, 0, 0);">onSuccess</font> | <font style="color:rgb(0, 0, 0);">成功回调</font> |
| <font style="color:rgb(0, 0, 0);">onFailed</font> | <font style="color:rgb(0, 0, 0);">失败回调</font> |


### <font style="color:rgb(0, 0, 0);">adminMoveInWaitingRoom:ickname:onSuccess:onFailed:()</font>
`<font style="color:rgb(0, 0, 0);">- (void)adminMoveInWaitingRoom:(NSString *)userId nickname:(NSString *)nickname onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed</font>`

将会议室成员移动到等候室，管理员用户可通过该接口将会中成员移至等候室中（只有主持人或联席主持人能够调用），SDK会通过 `<font style="color:rgb(0, 0, 0);">MeetingKitDelegate</font>`<font style="color:rgb(0, 0, 0);"> </font>中的 [onRoomMoveInWaitingRoom:()](https://www.yuque.com/anyconf/smeeting/rfflpfbuav0xc28g#qBV3v) 回调通知给目标用户。

| <font style="color:#8A8F8D;">参数</font> | <font style="color:#8A8F8D;">描述</font> |
| :--- | --- |
| <font style="color:rgb(0, 0, 0);">userId</font> | <font style="color:rgb(0, 0, 0);">用户标识</font> |
| <font style="color:rgb(0, 0, 0);">nickname</font> | <font style="color:rgb(0, 0, 0);">用户昵称</font> |
| <font style="color:rgb(0, 0, 0);">onSuccess</font> | <font style="color:rgb(0, 0, 0);">成功回调</font> |
| <font style="color:rgb(0, 0, 0);">onFailed</font> | <font style="color:rgb(0, 0, 0);">失败回调</font> |


### <font style="color:rgb(0, 0, 0);">adminMoveOutWaitingRoom:nickname:onSuccess:onFailed:()</font>
`<font style="color:rgb(0, 0, 0);">- (void)adminMoveOutWaitingRoom:(NSString *)userId nickname:(NSString *)nickname onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed</font>`

将等候室人员移动到会议室，管理员用户可通过该接口将当前等候室中成员移至会议室中（只有主持人或联席主持人能够调用），SDK会通过 `<font style="color:rgb(0, 0, 0);">MeetingKitIMDelegate</font>`<font style="color:rgb(0, 0, 0);"> </font>中的 [onWaitingRoomMoveInRoom:title:()](https://www.yuque.com/anyconf/smeeting/wh4gigxazm9esngc#Td4ag) 回调通知给目标用户。

| <font style="color:#8A8F8D;">参数</font> | <font style="color:#8A8F8D;">描述</font> |
| :--- | --- |
| <font style="color:rgb(0, 0, 0);">userId</font> | <font style="color:rgb(0, 0, 0);">用户标识，空表示全部成员</font> |
| <font style="color:rgb(0, 0, 0);">nickname</font> | <font style="color:rgb(0, 0, 0);">用户昵称</font> |
| <font style="color:rgb(0, 0, 0);">onSuccess</font> | <font style="color:rgb(0, 0, 0);">成功回调</font> |
| <font style="color:rgb(0, 0, 0);">onFailed</font> | <font style="color:rgb(0, 0, 0);">失败回调</font> |


### <font style="color:rgb(0, 0, 0);">adminGetWaitingRoomUserList:onFailed:()</font>
`<font style="color:rgb(0, 0, 0);">- (void)adminGetWaitingRoomUserList:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed</font>`

主持人获取等候室用户列表

| <font style="color:#8A8F8D;">参数</font> | <font style="color:#8A8F8D;">描述</font> |
| :--- | --- |
| <font style="color:rgb(0, 0, 0);">onSuccess</font> | <font style="color:rgb(0, 0, 0);">成功回调，参考文档：</font>[SEAWaitingRoomMemberListModel](https://www.yuque.com/anyconf/smeeting/gkeau9oyh5vms80z#cUCiD) |
| <font style="color:rgb(0, 0, 0);">onFailed</font> | <font style="color:rgb(0, 0, 0);">失败回调</font> |


## <font style="color:rgb(0, 0, 0);">分组讨论相关接口</font>
### <font style="color:rgb(0, 0, 0);">subMeetingHelp:onFailed:()</font>
`<font style="color:rgb(0, 0, 0);">- (void)subMeetingHelp:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed</font>`

小组成员请求管理员帮助，SDK会通过 `<font style="color:rgb(0, 0, 0);">MeetingKitIMDelegate</font>`<font style="color:rgb(0, 0, 0);"> </font>中的 [onSubMettingAskingHelp:meetingId:title:()](https://www.yuque.com/anyconf/smeeting/wh4gigxazm9esngc#jEQ8e) 回调通知给管理员用户。

| <font style="color:#8A8F8D;">参数</font> | <font style="color:#8A8F8D;">描述</font> |
| :--- | --- |
| <font style="color:rgb(0, 0, 0);">onSuccess</font> | <font style="color:rgb(0, 0, 0);">成功回调</font> |
| <font style="color:rgb(0, 0, 0);">onFailed</font> | <font style="color:rgb(0, 0, 0);">失败回调</font> |


### <font style="color:rgb(0, 0, 0);">adminUpdateEnterBeforeHostDisabled:onSuccess:onFailed:()</font>
`<font style="color:rgb(0, 0, 0);">- (void)adminUpdateEnterBeforeHostDisabled:(BOOL)enterBeforeHostDisabled onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed</font>`

更新禁止在主持人前入会状态，控制当前房间内是否允许在主持人前入会状态（只有主持人或联席主持人能够调用）。

| <font style="color:#8A8F8D;">参数</font> | <font style="color:#8A8F8D;">描述</font> |
| :--- | --- |
| <font style="color:rgb(0, 0, 0);">enterBeforeHostDisabled</font> | <font style="color:rgb(0, 0, 0);">禁止状态，YES-禁止 NO-不禁止</font> |
| <font style="color:rgb(0, 0, 0);">onSuccess</font> | <font style="color:rgb(0, 0, 0);">成功回调</font> |
| <font style="color:rgb(0, 0, 0);">onFailed</font> | <font style="color:rgb(0, 0, 0);">失败回调</font> |


### <font style="color:rgb(0, 0, 0);">adminCreateSubMeeting:onSuccess:onFailed:()</font>
`<font style="color:rgb(0, 0, 0);">- (void)adminCreateSubMeeting:(NSArray <NSString *> *)titleList onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed;</font>`

主持人创建小组会议

| <font style="color:#8A8F8D;">参数</font> | <font style="color:#8A8F8D;">描述</font> |
| :--- | --- |
| <font style="color:rgb(0, 0, 0);">titleList</font> | <font style="color:rgb(0, 0, 0);">标题列表</font> |
| <font style="color:rgb(0, 0, 0);">onSuccess</font> | <font style="color:rgb(0, 0, 0);">成功回调</font> |
| <font style="color:rgb(0, 0, 0);">onFailed</font> | <font style="color:rgb(0, 0, 0);">失败回调</font> |


### <font style="color:rgb(0, 0, 0);">adminUpdateSubMeetingTitle:targetId:onSuccess:onFailed:()</font>
`<font style="color:rgb(0, 0, 0);">- (void)adminUpdateSubMeetingTitle:(NSString *)title targetId:(NSString *)targetId onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed</font>`

主持人修改小组会议标题

| <font style="color:#8A8F8D;">参数</font> | <font style="color:#8A8F8D;">描述</font> |
| :--- | --- |
| <font style="color:rgb(0, 0, 0);">title</font> | <font style="color:rgb(0, 0, 0);">小组标题</font> |
| <font style="color:rgb(0, 0, 0);">targetId</font> | 小组标识 |
| <font style="color:rgb(0, 0, 0);">onSuccess</font> | <font style="color:rgb(0, 0, 0);">成功回调</font> |
| <font style="color:rgb(0, 0, 0);">onFailed</font> | <font style="color:rgb(0, 0, 0);">失败回调</font> |


### <font style="color:rgb(0, 0, 0);">adminUpdateSubMeetingConferee:targetId:onSuccess:onFailed:()</font>
`<font style="color:rgb(0, 0, 0);">- (void)adminUpdateSubMeetingConferee:(NSArray <SEAConfereeModel *> *)confereeList targetId:(NSString *)targetId onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed</font>`

主持人修改小组会议成员

| <font style="color:#8A8F8D;">参数</font> | <font style="color:#8A8F8D;">描述</font> |
| :--- | --- |
| <font style="color:rgb(0, 0, 0);">confereeList</font> | <font style="color:rgb(0, 0, 0);">小组参会列表，参考文档：</font>[SEAConfereeModel](https://www.yuque.com/anyconf/smeeting/gkeau9oyh5vms80z#ipu1S) |
| <font style="color:rgb(0, 0, 0);">targetId</font> | 小组标识 |
| <font style="color:rgb(0, 0, 0);">onSuccess</font> | <font style="color:rgb(0, 0, 0);">成功回调</font> |
| <font style="color:rgb(0, 0, 0);">onFailed</font> | <font style="color:rgb(0, 0, 0);">失败回调</font> |


### <font style="color:rgb(0, 0, 0);">adminDeleteSubMeeting:onSuccess:onFailed:()</font>
`<font style="color:rgb(0, 0, 0);">- (void)adminDeleteSubMeeting:(NSArray <NSString *> *)targetList onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed</font>`

主持人删除小组会议

| <font style="color:#8A8F8D;">参数</font> | <font style="color:#8A8F8D;">描述</font> |
| :--- | --- |
| <font style="color:rgb(0, 0, 0);">targetList</font> | 小组标识列表 |
| <font style="color:rgb(0, 0, 0);">onSuccess</font> | <font style="color:rgb(0, 0, 0);">成功回调</font> |
| <font style="color:rgb(0, 0, 0);">onFailed</font> | <font style="color:rgb(0, 0, 0);">失败回调</font> |


### <font style="color:rgb(0, 0, 0);">adminGetSubMeetingList:onSuccess:onFailed:()</font>
`<font style="color:rgb(0, 0, 0);">- (void)adminGetSubMeetingList:(NSString *)meetingId onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed</font>`

主持人请求小组会议列表

| <font style="color:#8A8F8D;">参数</font> | <font style="color:#8A8F8D;">描述</font> |
| :--- | --- |
| <font style="color:rgb(0, 0, 0);">meetingId</font> | 会议标识 |
| <font style="color:rgb(0, 0, 0);">onSuccess</font> | <font style="color:rgb(0, 0, 0);">成功回调，参考文档：</font>[SEARoomSubMeetingListModel](https://www.yuque.com/anyconf/smeeting/gkeau9oyh5vms80z#MrIJK) |
| <font style="color:rgb(0, 0, 0);">onFailed</font> | <font style="color:rgb(0, 0, 0);">失败回调</font> |


### <font style="color:rgb(0, 0, 0);">adminStartSubMeeting:onSuccess:onFailed:()</font>
`<font style="color:rgb(0, 0, 0);">- (void)adminStartSubMeeting:(NSArray <NSString *> *)targetList onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed</font>`

开始小组会议，管理员用户可通过该接口将创建之后的小组会议设置为开始（只有主持人或联席主持人能够调用），SDK会通过 `<font style="color:rgb(0, 0, 0);">MeetingKitDelegate</font>`<font style="color:rgb(0, 0, 0);"> </font>中的 [onRoomSubMeetingStart:title:conferee:()](https://www.yuque.com/anyconf/smeeting/rfflpfbuav0xc28g#o5QYi) 回调通知给目标用户。

| <font style="color:#8A8F8D;">参数</font> | <font style="color:#8A8F8D;">描述</font> |
| :--- | --- |
| <font style="color:rgb(0, 0, 0);">targetList</font> | <font style="color:rgb(0, 0, 0);">小组标识列表</font> |
| <font style="color:rgb(0, 0, 0);">onSuccess</font> | <font style="color:rgb(0, 0, 0);">成功回调</font> |
| <font style="color:rgb(0, 0, 0);">onFailed</font> | <font style="color:rgb(0, 0, 0);">失败回调</font> |


### <font style="color:rgb(0, 0, 0);">adminStopSubMeeting:onSuccess:onFailed:()</font>
`<font style="color:rgb(0, 0, 0);">- (void)adminStopSubMeeting:(NSArray <NSString *> *)targetList onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed</font>`

结束小组会议，管理员用户可通过该接口将创建之后的小组会议设置为结束（只有主持人或联席主持人能够调用），SDK会通过 `<font style="color:rgb(0, 0, 0);">MeetingKitDelegate</font>`<font style="color:rgb(0, 0, 0);"> </font>中的 [onRoomSubMeetingStop:()](https://www.yuque.com/anyconf/smeeting/rfflpfbuav0xc28g#AsdP0) 回调通知给目标用户。

| <font style="color:#8A8F8D;">参数</font> | <font style="color:#8A8F8D;">描述</font> |
| :--- | --- |
| <font style="color:rgb(0, 0, 0);">targetList</font> | <font style="color:rgb(0, 0, 0);">小组标识列表</font> |
| <font style="color:rgb(0, 0, 0);">onSuccess</font> | <font style="color:rgb(0, 0, 0);">成功回调</font> |
| <font style="color:rgb(0, 0, 0);">onFailed</font> | <font style="color:rgb(0, 0, 0);">失败回调</font> |


### <font style="color:rgb(0, 0, 0);">adminMoveSubMeetingUser:fromGroupId:toGroupId:onSuccess:onFailed:()</font>
`<font style="color:rgb(0, 0, 0);">- (void)adminMoveSubMeetingUser:(NSString *)targetId fromGroupId:(NSString *)fromGroupId toGroupId:(nullable NSString *)toGroupId onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed</font>`

小组会议之间移动用户，管理员用户可通过该接口在小组会议以及主会场之间移动指定成员（只有主持人或联席主持人能够调用），SDK会通过 `<font style="color:rgb(0, 0, 0);">MeetingKitDelegate</font>`<font style="color:rgb(0, 0, 0);"> </font>中的 [onRoomMoveSubMeeting:fromMeetingTitle:toMeetingId:toMeetingTitle:()](https://www.yuque.com/anyconf/smeeting/rfflpfbuav0xc28g#PXXkX) 回调通知给目标用户。

| <font style="color:#8A8F8D;">参数</font> | <font style="color:#8A8F8D;">描述</font> |
| :--- | --- |
| <font style="color:rgb(0, 0, 0);">targetId</font> | <font style="color:rgb(0, 0, 0);">目标成员标识</font> |
| <font style="color:rgb(0, 0, 0);">fromGroupId</font> | <font style="color:rgb(0, 0, 0);">原小组标识</font> |
| <font style="color:rgb(0, 0, 0);">toGroupId</font> | <font style="color:rgb(0, 0, 0);">目标小组标识，为空时表示主会议</font> |
| <font style="color:rgb(0, 0, 0);">onSuccess</font> | <font style="color:rgb(0, 0, 0);">成功回调</font> |
| <font style="color:rgb(0, 0, 0);">onFailed</font> | <font style="color:rgb(0, 0, 0);">失败回调</font> |


### <font style="color:rgb(0, 0, 0);">getOnlineMemberList:onSuccess:onFailed:()</font>
`<font style="color:rgb(0, 0, 0);">- (void)getOnlineMemberList:(NSString *)meetingId onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed</font>`

获取在线成员列表

| <font style="color:#8A8F8D;">参数</font> | <font style="color:#8A8F8D;">描述</font> |
| :--- | --- |
| <font style="color:rgb(0, 0, 0);">meetingId</font> | 会议标识 |
| <font style="color:rgb(0, 0, 0);">onSuccess</font> | <font style="color:rgb(0, 0, 0);">成功回调，参考文档：</font>[SEAOnlineMemberListModel](https://www.yuque.com/anyconf/smeeting/gkeau9oyh5vms80z#CEmgE) |
| <font style="color:rgb(0, 0, 0);">onFailed</font> | <font style="color:rgb(0, 0, 0);">失败回调</font> |


### <font style="color:rgb(0, 0, 0);">getMoreOnlineMemberList:onSuccess:onFailed:()</font>
`<font style="color:rgb(0, 0, 0);">- (void)getMoreOnlineMemberList:(NSString *)meetingId onSuccess:(nullable SEASuccessBlock)onSuccess onFailed:(nullable SEAFailedBlock)onFailed</font>`

获取更多在线成员列表（翻页操作）

| <font style="color:#8A8F8D;">参数</font> | <font style="color:#8A8F8D;">描述</font> |
| :--- | --- |
| <font style="color:rgb(0, 0, 0);">meetingId</font> | 会议标识 |
| <font style="color:rgb(0, 0, 0);">onSuccess</font> | <font style="color:rgb(0, 0, 0);">成功回调，参考文档：</font>[SEAOnlineMemberListModel](https://www.yuque.com/anyconf/smeeting/gkeau9oyh5vms80z#CEmgE) |
| <font style="color:rgb(0, 0, 0);">onFailed</font> | <font style="color:rgb(0, 0, 0);">失败回调</font> |


## <font style="color:rgb(0, 0, 0);">屏幕共享接口</font>
### stopScreenRecord()
`- (void)stopScreenRecord`

宿主程序主动关闭屏幕采集

<font style="color:rgb(0, 0, 0);">此方法在宿主程序中</font>使用，用于用户主动关闭屏幕共享使用。

关闭屏幕采集后，SDK会通过 `<font style="color:rgb(0, 0, 0);">MeetingKitDelegate</font>` 中的 [onScreenRecordStatus:()](https://www.yuque.com/anyconf/eanoso/rfflpfbuav0xc28g#iRVUP) 回调通知您当前设备采集状态。此时，需要根据回调状态选择调用 请求开启共享 还是 关闭共享。

### <font style="color:rgb(0, 0, 0);">broadcastStartedWithAppGroup:delegate:()</font>
`<font style="color:rgb(0, 0, 0);">- (void)broadcastStartedWithAppGroup:(NSString *)appGroup delegate:(id<MeetingKitScreenDelegate>)delegate</font>`

扩展程序开启屏幕录制方法<font style="color:rgb(0, 0, 0);">，并绑定委托代理</font>

<font style="color:rgb(0, 0, 0);">此方法在扩展程序</font>`<font style="color:rgb(0, 0, 0);">SampleHandler</font>`<font style="color:rgb(0, 0, 0);">中使用。</font>

关闭屏幕采集后，SDK会通过 `<font style="color:rgb(0, 0, 0);">MeetingKitDelegate</font>` 中的 [onScreenRecordStatus:()](https://www.yuque.com/anyconf/eanoso/rfflpfbuav0xc28g#iRVUP) 回调通知您当前设备采集状态。此时，需要根据回调状态选择调用 请求开启共享 还是 关闭共享。

| <font style="color:#8A8F8D;">参数</font> | <font style="color:#8A8F8D;">描述</font> |
| :--- | --- |
| <font style="color:rgb(0, 0, 0);">appGroup</font> | <font style="color:rgb(0, 0, 0);">应用分组标识符</font> |
| <font style="color:rgb(0, 0, 0);">delegate</font> | <font style="color:rgb(0, 0, 0);">屏幕录制扩展代理，参考文档：</font>[屏幕录制](https://www.yuque.com/anyconf/eanoso/by65hp8d8zfxyd8k) |


### sendSampleBuffer:withType:()
`- (void)sendSampleBuffer:(CMSampleBufferRef)sampleBuffer withType:(RPSampleBufferType)sampleBufferType`

扩展程序发送屏幕采集帧数据

<font style="color:rgb(0, 0, 0);">此方法在</font>扩展程序`SampleHandler`中使用

| <font style="color:#8A8F8D;">参数</font> | <font style="color:#8A8F8D;">描述</font> |
| :--- | --- |
| <font style="color:rgb(0, 0, 0);">sampleBuffer</font> | <font style="color:rgb(0, 0, 0);">数据帧</font> |
| <font style="color:rgb(0, 0, 0);">sampleBufferType</font> | 数据帧类型，包括：视频、音频等 |


## <font style="color:rgb(0, 0, 0);">数据管理接口</font>
### <font style="color:rgb(0, 0, 0);">getMySelf()</font>
`<font style="color:rgb(0, 0, 0);">- (SEAUserModel *)getMySelf</font>`

<font style="color:rgb(0, 0, 0);">获取本地登录用户的基本信息</font>

<font style="color:rgb(0, 0, 0);">返回值说明：</font>

[SEAUserModel](https://www.yuque.com/anyconf/eanoso/gkeau9oyh5vms80z#pnMcF)<font style="color:rgb(0, 0, 0);"> 用户数据。</font>

### <font style="color:rgb(0, 0, 0);">findMemberWithUserId:()</font>
`<font style="color:rgb(0, 0, 0);">- (SEAUserModel *)findMemberWithUserId:(NSString *)userId</font>`

<font style="color:rgb(0, 0, 0);">获取指定远端用户的基本信息</font>

<font style="color:rgb(0, 0, 0);">返回值说明：</font>

[SEAUserModel](https://www.yuque.com/anyconf/eanoso/gkeau9oyh5vms80z#pnMcF)<font style="color:rgb(0, 0, 0);"> 用户数据。</font>

### <font style="color:rgb(0, 0, 0);">getRemoteUsers()</font>
`<font style="color:rgb(0, 0, 0);">- (NSArray<SEAUserModel *> *)getRemoteUsers</font>`

<font style="color:rgb(0, 0, 0);">获取当前所在房间的成员列表</font>

<font style="color:rgb(0, 0, 0);">返回值说明：</font>

[SEAUserModel](https://www.yuque.com/anyconf/eanoso/gkeau9oyh5vms80z#pnMcF)<font style="color:rgb(0, 0, 0);"> 用户数据。</font>

### <font style="color:rgb(0, 0, 0);">getRoomDetails()</font>
`<font style="color:rgb(0, 0, 0);">- (SEARoomModel *)getRoomDetails</font>`

<font style="color:rgb(0, 0, 0);">获取当前所在房间的基本信息</font>

<font style="color:rgb(0, 0, 0);">返回值说明：</font>

[SEARoomModel](https://www.yuque.com/anyconf/eanoso/gkeau9oyh5vms80z#tcVka)<font style="color:rgb(0, 0, 0);"> 用户数据。</font>

### <font style="color:rgb(0, 0, 0);">getDrawingHost()</font>
`<font style="color:rgb(0, 0, 0);">- (NSString *)getDrawingHost</font>`

<font style="color:rgb(0, 0, 0);">获取电子画板访问地址</font>

<font style="color:rgb(0, 0, 0);">返回值说明：</font>

电子画板采用网页形式实现，该接口只有在加入房间成功后调用有效并返回电子画板访问地址。 

## <font style="color:rgb(0, 0, 0);">媒体配置相关接口</font>
### setStreamMediaConfig:()
`- (void)setStreamMediaConfig:(SEAMediaConfig *)config`

设置媒体配置参数

<font style="color:rgb(0, 0, 0);">可通过该接口设置视频编码、音频编码、视频帧率、视频码流等参数。</font>

**<font style="color:rgb(0, 0, 0);">参数</font>**

| config | 流媒体配置参数，<font style="color:rgb(0, 0, 0);">用于指定视频编码、音频编码、视频帧率、视频码流等基本信息详情请参考 </font>[SEAMediaConfig](https://www.yuque.com/anyconf/eanoso/gkeau9oyh5vms80z#pMzBp) |
| --- | --- |


### setNetworkQosParam:()
`- (void)setNetworkQosParam:(SEANetworkQosParam *)param`

设置网络质量控制参数

<font style="color:rgb(0, 0, 0);">可通过该接口设置延迟自适应档位、延时抗抖动等级、码率自适应开关、网络自适应开关等参数。</font>

**<font style="color:rgb(0, 0, 0);">参数</font>**

| param | 质量控制参数，<font style="color:rgb(0, 0, 0);">用于指定延迟自适应档位、延时抗抖动等级、码率自适应开关、网络自适应开关等基本信息详情请参考 </font>[SEANetworkQosParam](https://www.yuque.com/anyconf/eanoso/gkeau9oyh5vms80z#rUmBV) |
| --- | --- |


## <font style="color:rgb(0, 0, 0);">调试相关接口</font>
### setDebugParam:()
`- (void)setDebugParam:(SEADebugParam *)param`

设置调试参数

<font style="color:rgb(0, 0, 0);">可通过该接口设置调试地址、保存音视频流等参数。</font>

**<font style="color:rgb(0, 0, 0);">参数</font>**

| param | 调试参数，<font style="color:rgb(0, 0, 0);">用于设置调试地址、保存音视频流等基本信息详情请参考 </font>[SEADebugParam](https://www.yuque.com/anyconf/eanoso/gkeau9oyh5vms80z#tdyrN) |
| --- | --- |


