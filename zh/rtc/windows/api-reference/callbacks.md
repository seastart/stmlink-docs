---
title: "callbacks"
description: "Windows SRTC 音视频 SDK callbacks 接口参考"
---

## 房间相关回调
### 加入房间成功回调
```cpp
virtual void onJoinChannel(const char* channel, int channelSize, const char* me, int meSize, const char* members, int memberSize, const char* opts, int optSize) = 0;
```typescript

**触发条件**

加入频道成功

**参数**

| channel | 房间信息 |
| --- | --- |
| channelSize | 房间信息长度 |
| me | 自己信息[查看](https://www.yuque.com/anyconf/rtcengine/rhsp7k#Cz51I) |
| meSize | 自己信息长度 |
| members | 会中成员信息集合[查看](https://www.yuque.com/anyconf/rtcengine/rhsp7k#Cz51I) |
| memberSize | 会中成员信息集合长度 |
| opts | 系统配置参数 |
| optSize | 系统配置参数长度 |




### 房间状态更新回调
```cpp
virtual void onChannelUpdate(const char* channelId,const char * props, int propsSize) = 0;
```

**触发条件**

频道扩展消息改变时

**参数**

| channelId | 频道id |
| --- | --- |
| props | 扩展信息 |
| propsSize | 扩展信息字符串长度 |




### 用户加入回调
```cpp
virtual void onUserJoin(const char* channelId, const char* user, int userSize) = 0;
```typescript

**触发条件**

房间内用户加入房间后触发。

**参数**

| channelId | 频道id |
| --- | --- |
| user | 更新用户信息[查看](https://www.yuque.com/anyconf/rtcengine/rhsp7k#Cz51I) |
| userSize | 更新用户信息长度 |




### 用户信息改变回调
```cpp
virtual void onUserUpdate(const char* channelId, const char* user, int userSize) = 0;
```

**触发条件**

房间内其他用户状态发生改变时触发

**参数**

| channelId | 频道id |
| --- | --- |
| user | 更新用户信息[查看](https://www.yuque.com/anyconf/rtcengine/rhsp7k#Cz51I) |
| userSize | 更新用户信息长度 |




### 用户流信息添加
```cpp
virtual void onUserStreamAdd(const char* channelId, const char* uid,const char* stream, int streamSize) = 0;
```typescript

**触发条件**

房间内其他用户流信息改变

**参数**

| channelId | 频道id |
| --- | --- |
| uid | 更新用户信息 |
| stream | 流信息[查看](https://www.yuque.com/anyconf/rtcengine/rhsp7k#TpNet) |
| streamSize | 流信息长度 |


### 用户流信息更新
```cpp
virtual void onUserStreamUpdate(const char* channelId, const char* user, const char* stream, int streamSize) = 0;
```

**触发条件**

房间内其他用户流信息改变

**参数**

| channelId | 频道id |
| --- | --- |
| uid | 更新用户信息 |
| stream | 流信息[查看](https://www.yuque.com/anyconf/rtcengine/rhsp7k#TpNet) |
| streamSize | 流信息长度 |


### 用户流信息删除
```cpp
virtual void onUserStreamRemove(const char* channelId, const char* user, const char* stream, int streamSize) = 0;
```typescript

**触发条件**

房间内其他用户流信息改变

**参数**

| channelId | 频道id |
| --- | --- |
| uid | 更新用户信息 |
| stream | 流信息，[查看](https://www.yuque.com/anyconf/rtcengine/rhsp7k#TpNet) |
| streamSize | 流信息长度 |






### 用户离开回调
```cpp
virtual void onUserLeave(const char* channelId, const char* user, int userSize) = 0;
```

**触发条件**

房间内用户加入房间后触发

**参数**

| channelId | 频道id |
| --- | --- |
| user | 更新用户信息[查看](https://www.yuque.com/anyconf/rtcengine/rhsp7k#Cz51I) |
| userSize | 更新用户信息长度 |




### 自定义消息回调
```cpp
virtual void onCustomMessage(const char* action, const char* message, int messageSize, const char* senderid) = 0;
```cpp

**触发条件**

收到消息触发

**参数**

| action | 消息类型 |
| --- | --- |
| message | 消息内容 |
| messageSize | 消息内容长度 |
| senderid | 发送用户id |


## 流媒体相关回调
### 流媒体上传挡位改变回调
```cpp
virtual void onStreamUpLevel(int level) = 0;
```

**触发条件**

上传挡位变化（和发送的数据和网络有关）

**参数**

| level | 挡位等级 ，0 好，1 中，2 差，3极差 |
| --- | --- |




### 流媒体下行成为挡位改变回调
```cpp
virtual void onStreamDownLevel(const char* uid, int level) = 0;
```typescript

**触发条件**

下行挡位变化（和对方网络有关）

**参数**

| uid | 成员id |
| --- | --- |
| level | 挡位等级 ，0 好，1 中，2 差，3极差 |




### 流媒体上行回调
```cpp
virtual void onStreamUpStat(const char* upstat, int upstatsize) = 0;
```

**触发条件**

通过流媒体参数设置，每个一段时间后回调

**参数**

| upstat | 上行数据json，[查看](https://www.yuque.com/anyconf/rtcengine/rhsp7k/edit#ONyNJ) |
| --- | --- |
| upstatsize | 上行数据json长度 |


注：需要设置需要在[_getSetting_](https://www.yuque.com/anyconf/rtcengine/ec4ggd#Mn3Gb)_，_设置stat_interval后才会触发回调



### 流媒体下行回调
```cpp
virtual void onStreamDownStat(const char* downstat, int downstatsize) = 0;
```typescript

**触发条件**

通过流媒体参数设置，每个一段时间后回调

**参数**

| downstat | 成员下行集合json，[查看](https://www.yuque.com/anyconf/rtcengine/rhsp7k/edit#p8VfT) |
| --- | --- |
| downstatsize | 成员下行集合json长度 |


注：需要设置需要在[_getSetting_](https://www.yuque.com/anyconf/rtcengine/ec4ggd#Mn3Gb)_，_设置stat_interval后才会触发回调



### 流媒体音柱回调
```cpp
virtual void onStreamSpeakers(const char* Speakers) = 0;
```

**触发条件**

通过流媒体参数设置，每个一段时间后回调

**参数**

| Speakers | 发言成员集合，[查看](https://www.yuque.com/anyconf/rtcengine/rhsp7k/edit#UQLVt) |
| --- | --- |


注：需要设置需要在[_getSetting_](https://www.yuque.com/anyconf/rtcengine/ec4ggd#Mn3Gb)_，_设置speaker_interval后才会触发回调



### 测速回调
```cpp
virtual void onProbeResult(int action,const char* result) = 0;
```cpp

**触发条件**

测试结果

**参数**

| action | 检测步骤 |
| --- | --- |
| result | 检测结果json ,[查看](https://www.yuque.com/anyconf/rtcengine/rhsp7k/edit#WQJCu) |




### 音频采集播放恢复回调
```cpp
virtual void onDeviceStatusChange(int devtype,int status) = 0;
```

**触发条件**

硬件设备采集或播放恢复,或采集播放异常

**参数**

| devtype | 1 麦克风 2 扬声器，3摄像头 |
| --- | --- |
| status | 1异常，2恢复 |




### 系统设备发生改变
```cpp
virtual void onDeviceChange(int devtype,int action,const char* name,int namesize) = 0;
```typescript

**触发条件**

插拔电脑音频外设

**参数**

| devtype | 1 麦克风，2 扬声器，3摄像头 |
| --- | --- |
| action | 1 插入 2拔出 |
| name | 设备名称 |
| namesize | 设备名称长度 |




### 系统默认设备发生改变
```cpp
virtual void onDeviceDefChange(int devtype, const char* name, int namesize) = 0;
```

**触发条件**

触发电脑默认设备改变（插拔外设也可能会改变默认设备）

**参数**

| devtype | 1 麦克风 2 扬声器 |
| --- | --- |
| name | 设备名称 |
| namesize | 设备名称长度 |




## 网络状态回调
### 断开连接（无法连接）
```cpp
virtual void onDisconnected(int reason, StatusCode code, const char* message, size_t message_size) = 0;
```typescript

**触发条件**

与服务器断开连接，切重连一段时间均失败

**参数**

| reason | 原因<br/>-1，异常错误<br/>0，未知<br/>1，主动离开<br/>2，被踢出<br/>3，被顶号<br/>4，心跳超时<br/>5，频道销毁 |
| --- | --- |
| code | 错误码 |
| message | 异常描述信息 |
| message_size | 异常描述信息长度 |


	

### 重连成功
```cpp
virtual void onReconnected(const char* channel, const char* options, size_t options_size) = 0;
```

**触发条件**

与服务器断开连接，后重连成功

**参数**

| channel | 频道id |
| --- | --- |
| options | 重连成功扩展信息 |
| options_size | 重连成功扩展信息长度 |


	

### 尝试重连
```cpp
virtual void onReconnecting() = 0;
```cpp

**触发条件**

与服务器断开连接，



