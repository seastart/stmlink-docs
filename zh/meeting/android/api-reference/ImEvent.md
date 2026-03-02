即时通讯事件监听

### onImDisconnected()
即时通讯断开连接

```java
fun onImDisconnected(reason: DisconnectedImReason)
```

参数

| reason | DisconnectedImReason 枚举类型，即时通讯断开原因，详见 [DisconnectedImReason](https://www.yuque.com/anyconf/smeeting/sly78y2qziqggiwx#IxLKb) |
| --- | --- |


### onError()
即时通讯出现不可恢复错误

```java
fun onError(errorCode: Int, errorMsg: String)
```

参数

| errorCode | Int 类型，错误码 |
| --- | --- |
| errorMsg | String 类型，错误信息 |


### onImReconnecting()
即时通讯断开且正在重新连接

```java
fun onImReconnecting()
```

### onImReconnected()
即时通讯重连成功

```java
fun onImReconnected()
```

### onImMessage()
即时通讯接收消息

```java
fun onImMessage(
    uid: String, sid: String, name: String, 
    action: String, content: String
)
```

参数

| uid | String 类型，消息发送方用户 uid |
| --- | --- |
| sid | String 类型，消息发送方用户会话 id |
| name | String 类型，消息发送方用户名称 |
| action | String 类型，消息标识 |
| content | String 类型，消息内容 |


### onCallReceived()
通话请求的回调

```java
fun onCallReceived(uid: String, nickname: String, roomNo: String, title: String)
```

参数

| uid | String 类型，呼叫邀请方用户 id |
| --- | --- |
| nickname | String 类型，呼叫邀请方用户昵称 |
| roomNo | String 类型，会议房间号 |
| title | String 类型，会议标题 |


### onMeetingRemind()
会议提醒

```java
fun onMeetingRemind(uid: String, meetingRemind: ImContent.MeetingRemind)
```

参数

| uid | String 类型，会议提醒发送方 uid |
| --- | --- |
| meetingRemind | MeetingRemind 类型，会议提醒消息 |


MeetingRemind 说明

| meetingId | String 类型，会议 id |
| --- | --- |
| title | String 类型，会议名称 |
| roomNo | String 类型，会议号 |
| creatorUid | String 类型，创建者 uid |
| creatorName | String 类型，创建者名称 |
| planTime | String 类型，预计开始时间 |
| planDur | String 类型，预计持续时间 |


### onMoveOutWaitingRoom()
成员被从等候室移入会议

```kotlin
fun onMoveOutWaitingRoom(uid: String, moveOutWaitingRoom: ImContent.MoveOutWaitingRoom)
```

参数

| uid | String 类型，会议提醒发送方 uid |
| --- | --- |
| moveOutWaitingRoom | MoveOutWaitingRoom 类型，等候室移入会议消息体 |


MoveOutWaitingRoom 说明

| meetingId | String 类型，会议 id |
| --- | --- |
| title | String 类型，会议名称 |


### onUserHelpSubMeeting()
子会议请求帮助

```kotlin
fun onUserHelpSubMeeting(uid: String, userHelpSubMeeting: ImContent.UserHelpSubMeeting)
```

参数

| uid | String 类型，会议提醒发送方 uid |
| --- | --- |
| userHelpSubMeeting | userHelpSubMeeting 类型，子会议请求信息 |


MoveOutWaitingRoom 说明

| parent | String 类型，主会议会议id |
| --- | --- |
| meetingId | String 类型，子会议关联的会议id |
| title | String 类型，子会议名称 |


