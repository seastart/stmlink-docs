---
title: "RoomEvent"
description: "Android SMeeting 会议 SDK RoomEvent 接口参考"
---

房间事件监听接口

### onRoomCameraStateChanged()
房间内所有用户摄像头状态能力改变事件

```java
void onRoomCameraStateChanged(
    String operatorUid, boolean selfUnMuteCameraDisabled, boolean disabled
);
```kotlin

参数

| operatorUid | String 类型，操作者 uid |
| --- | --- |
| selfUnMuteCameraDisabled | boolean 类型，是否允许自我解除禁画状态 |
| disabled | boolean 类型， 房间视频禁用状态。true-禁用；false-不禁用 |


### onRoomMicStateChanged()
房间内所有用户麦克风状态能力改变事件

```java
void onRoomMicStateChanged(
    String operatorUid, boolean selfUnMuteMicDisabled, boolean disabled
);
```

参数

| operatorUid | String 类型，操作者 uid |
| --- | --- |
| selfUnMuteMicDisabled | boolean 类型，是否允许自我解除禁音状态 |
| disabled | boolean 类型， 房间音频禁用状态。true-禁用；false-不禁用 |


### onRoomChatDisabledChanged()
房间内用户发送文本消息被禁用事件

```java
void onRoomChatDisabledChanged(String operatorUid, boolean disabled);
```kotlin

参数

| operatorUid | String 类型，操作者 uid |
| --- | --- |
| disabled | boolean 类型， 房间文本消息禁用状态。true-禁用；false-不禁用 |


### onRoomScreenshotDisabledChanged()
房间内截屏功能变化事件

```java
void onRoomScreenshotDisabledChanged(String operatorUid, boolean disabled);
```

参数

| operatorUid | String 类型，操作者 uid |
| --- | --- |
| disabled | boolean 类型， 房间截屏功能禁用状态。true-禁用；false-不禁用 |


### onRoomWatermarkDisabledChanged()
房间内水印功能变化事件

```java
void onRoomWatermarkDisabledChanged(String operatorUid, boolean disabled);
```kotlin

参数

| operatorUid | String 类型，操作者 uid |
| --- | --- |
| disabled | boolean 类型， 房间水印功能禁用状态。true-禁用；false-不禁用 |


### onRoomLockedChanged()
房间锁定状态变化事件

```java
void onRoomLockedChanged(String operatorUid, boolean locked);
```

参数

| operatorUid | String 类型，操作者 uid |
| --- | --- |
| locked | boolean 类型， 房间锁定状态。true-开启；false-关闭 |


### onWaitingRoomDisabledChanged()
等候室禁用状态变化事件

```java
void onWaitingRoomDisabledChanged(String operatorUid, boolean disabled);
```kotlin

参数

| operatorUid | String 类型，操作者 uid |
| --- | --- |
| disabled | boolean 类型， 等候室禁用状态。true-开启；false-关闭 |


### onRoomHostMove()
主持人转移

```java
void onRoomHostMove(String sourceUid, String targetUid);
```

参数

| sourceUid | String 类型，原主持人 |
| --- | --- |
| targetUid | String 类型， 目标主持人 |


### onCloudRecordStatusChange()
云录制状态改变

```java
void onCloudRecordStatusChange(
    CloudRecordType type, 
    CloudRecordStatus status, 
    String errMsg
);
```html

参数

| type | CloudRecordType  枚举类型，云录制类型<br/>Mode_Video：录像模式，值为 1<br/>Mode_Mixture：合流模式，值为 2<br/>Mode_All：混合模式，值为 3 |
| --- | --- |
| status | CloudRecordStatus 枚举类型， 云录制状态<br/>Status_Not_Start：未开始，值为 0<br/>Status_Ing：进行中，值为 1<br/>Status_Not_End：待结束，值为 2<br/>Status_Error：异常结束，值为 3<br/>Status_Ended：正常结束，值为 4 |
| errMsg | String 类型，错误信息 |


### onRoomShareStart()
共享开始事件，屏幕共享、共享白板

```java
void onRoomShareStart(String shareUid, ShareType shareType);
```

参数

| shareUid | String 类型，共享者 uid |
| --- | --- |
| shareType | ShareType 类型， 共享类型，详见枚举类型中的 [ShareType](https://www.yuque.com/anyconf/eanoso/sly78y2qziqggiwx#TA7zJ) |


### onRoomShareStop()
共享结束事件

```java
void onRoomShareStop(String shareUid, ShareType shareType);
```kotlin

参数

| shareUid | String 类型，共享者 uid |
| --- | --- |
| shareType | ShareType 类型， 共享类型，详见枚举类型中的 [ShareType](https://www.yuque.com/anyconf/eanoso/sly78y2qziqggiwx#TA7zJ) |


### onAdminRoomShareStop()
主持人结束共享事件

```java
void onAdminRoomShareStop(String shareUid, ShareType shareType);
```

参数

| shareUid | String 类型，共享者 uid |
| --- | --- |
| shareType | ShareType 类型， 共享类型，详见枚举类型中的 [ShareType](https://www.yuque.com/anyconf/eanoso/sly78y2qziqggiwx#TA7zJ) |


### onRoomHandUpChanged()
房间内举手状态变化事件

```java
void onRoomHandUpChanged(String operatorUid, Boolean enable, HandupType handupType);
```html

参数

| operatorUid | String 类型，操作者 uid |
| --- | --- |
| enable | boolean 类型， 举手状态，true-申请举手；false-取消举手 |
| handupType | HandupType 类型，举手申请类型，详见枚举类型中的 [HandupType](https://www.yuque.com/anyconf/eanoso/sly78y2qziqggiwx#dWRbl) |


### onAdminRoomStartSubMeeting()
主持人开始子会议

```java
void onAdminRoomStartSubMeeting(String subMeetingId, String subTitle, List<String> uids);
```

参数

| subMeetingId | String 类型，子会议关联的会议 id |
| --- | --- |
| subTitle | String 类型，子会议的会议标题 |
| uids | `List<String>` 类型，子会议中包含的成员 |


### onAdminRoomStopSubMeeting()
主持人停止子会议，在主会场的成员收到

```java
void onAdminRoomStopSubMeeting(String mainMeetingId, String subMeetingId, String subTitle);
```kotlin

参数

| mainMeetingId | String 类型，主会议的会议 id |
| --- | --- |
| subMeetingId | String 类型，子会议关联的会议 id |
| subTitle | String 类型，子会议标题 |


### onError()
错误事件回调

+ 无法恢复的错误，需要执行退会操作

```java
void onError(int errorCode, String errMsg);
```

参数

| errorCode | String 类型，操作者 uid |
| --- | --- |
| errMsg | boolean 类型， 举手状态，true-申请举手；false-取消举手 |


### onReconnecting()
开始重连事件

```java
void onReconnecting();
```kotlin

### onReconnected()
重连成功事件

```java
void onReconnected();
```

