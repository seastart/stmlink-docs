用户事件监听接口

### onExitRoom()
离开会议事件回调

```java
void onExitRoom(LeaveMeetingReason reason);
```

参数

| reason | LeaveReason 类型，离会原因，详见枚举类型中的 [LeaveMeetingReason](https://www.yuque.com/anyconf/eanoso/sly78y2qziqggiwx#KewU3) |
| --- | --- |


### onUserEnter()
远端用户进入会议事件

```java
void onUserEnter(String uid);
```

参数

| uid | String 类型，远端用户 uid |
| --- | --- |


### onUserExit()
远端用户离开会议事件

```java
void onUserExit(String uid);
```

参数

| uid | String 类型，远端用户 uid |
| --- | --- |


### onUserNameChanged()
用户昵称变化，所有成员收到

```java
void onUserNameChanged(String targetUid, String nick);
```

参数

| targetUid | String 类型，目标成员 uid |
| --- | --- |
| nick | String 类型，新昵称 |


### onUserRoleChanged()
用户角色变化事件

```java
void onUserRoleChanged(String targetUid, MemberRoleType roleType);
```

参数

| targetUid | String 类型，目标成员 uid |
| --- | --- |
| roleType | MemberRoleType 枚举类型，成员角色类型<br/>Normal：普通成员，值为 0；<br/>Host：主持人，值为 1；<br/>UnionHost：联席主持人，值为 2； |


### onUserCameraStateChanged()
用户视频状态变化事件

+ 此处包含自己打开、关闭摄像头，主持人关闭其他人摄像头，不包含主持人打开其他人摄像头

```java
void onUserCameraStateChanged(
    String targetUid, DeviceState cameraState, ChangeReason reason
);
```

参数

| targetUid | String 类型，目标成员 uid |
| --- | --- |
| cameraState | DeviceState 类型，新的摄像头状态，详见枚举类型中的 [DeviceState](https://www.yuque.com/anyconf/eanoso/sly78y2qziqggiwx#hT40E) |
| reason | ChangeReason 类型，变更原因，详见枚举类型中的 [ChangeReason](https://www.yuque.com/anyconf/eanoso/sly78y2qziqggiwx#qMoCE) |


### onUserMicStateChanged()
用户麦克风状态变化事件

+ 此处包含自己打开、关闭麦克风，主持人关闭其他人麦克风，不包含主持人打开其他人麦克风

```java
void onUserMicStateChanged(String targetUid, DeviceState micState, ChangeReason reason);
```

参数

| targetUid | String 类型，目标成员 uid |
| --- | --- |
| micState | DeviceState 类型，新的摄像头状态，详见枚举类型中的 [DeviceState](https://www.yuque.com/anyconf/eanoso/sly78y2qziqggiwx#hT40E) |
| reason | ChangeReason 类型，变更原因，详见枚举类型中的 [ChangeReason](https://www.yuque.com/anyconf/eanoso/sly78y2qziqggiwx#qMoCE) |


### onUserChatDisabledChange()
用户聊天能力禁用状态变化回调

```java
void onUserChatDisabledChange(String operatorUid, boolean disabled);
```

参数

| operatorUid | String 类型，操作者 uid |
| --- | --- |
| disabled | boolean 类型，聊天能力禁用状态，true-禁用、false-不禁用 |


### onHandupConfirm()
举手处理结果回调

```java
void onHandupConfirm(String operatorUid, Boolean approve, HandupType handupType);
```

参数

| operatorUid | String 类型，操作者 uid |
| --- | --- |
| approve | boolean 类型，处理结果，true-同意，false-不同意 |
| handupType | HandupType 类型，举手申请类型，详见枚举类型中的 [HandupType](https://www.yuque.com/anyconf/eanoso/sly78y2qziqggiwx#lWByu) |


### onRequestOpenCamera()
请求打开摄像头

+ 一般为主持人或联席主持人请求普通用户打开摄像头，普通用户收到此事件

```java
void onRequestOpenCamera(String operatorUid);
```

参数

| operatorUid | String 类型，请求者 uid |
| --- | --- |


### onRequestOpenMic()
请求打开麦克风

+ 一般为主持人或联席主持人请求普通用户打开麦克风，普通用户收到此事件

```java
void onRequestOpenMic(String operatorUid);
```

参数

| operatorUid | String 类型，请求者 uid |
| --- | --- |


### onUserConfirmOpenCamera()
用户回复打开摄像头请求事件

+ 一般为普通用户回复主持人的打开摄像头请求，主持人收到此事件

```java
void onUserConfirmOpenCamera(String operatorUid, Boolean approve);
```

参数

| operatorUid | String 类型，响应者 uid |
| --- | --- |
| approve | boolean 类型，处理结果，true-同意，false-不同意 |


### onUserConfirmOpenMic()
用户回复打开麦克风请求事件

+ 一般为普通用户回复主持人的打开麦克风请求，主持人收到此事件

```java
void onUserConfirmOpenMic(String operatorUid, Boolean approve);
```

参数

| operatorUid | String 类型，响应者 uid |
| --- | --- |
| approve | boolean 类型，处理结果，true-同意，false-不同意 |


### onMoveInWaitingRoom()
用户被从会议移到等候室

```java
void onMoveInWaitingRoom(String operatorUid, String nickName);
```

参数

| operatorUid | String 类型，响应者 uid |
| --- | --- |
| nickName | boolean 类型，响应者名称  |


### onUserEnterWaitingRoom()
用户进入等待室，只有主持人收到

```java
void onUserEnterWaitingRoom(String uid, String nickName);
```

参数

| uid | String 类型，用户 uid |
| --- | --- |
| nickName | boolean 类型，用户名称 |


### onUserExitWaitingRoom()
用户离开等待室，只有主持人收到

```java
void onUserExitWaitingRoom(String uid, String nickName);
```

参数

| uid | String 类型，用户 uid |
| --- | --- |
| nickName | boolean 类型，用户名称 |


### onRequestMoveToMainMeetOrSubMeet()
主持人将成员移动到主会场或子会场

```java
void onRequestMoveToMainMeetOrSubMeet(String targetMeetingId, String targetMeetingTitle);
```

参数

| targetMeetingId | String 类型，目标会议 id |
| --- | --- |
| targetMeetingTitle | boolean 类型，目标会议标题 |


