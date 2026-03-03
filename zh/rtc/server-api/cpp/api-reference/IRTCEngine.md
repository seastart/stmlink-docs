---
title: "IRTCEngine"
description: "全平台 C++ SRTC 音视频 SDK IRTCEngine 接口参考"
---

### StatusCode login(const char* user, uint32_t userSize, const char* args = nullptr, uint32_t argsSize=0);
登录，当手动onLogin事件后才是真正登录成功。

**参数**

| user | user对象 json格式字符串 |
| --- | --- |
| userSize | user的字节数 |
| args | 第三方平台透传参数，鉴权时会携带给第三方平台 |
| argsSize | args的字节数 |


### oid logout();
退出登录



### StatusCode joinRoom(const char* roomId, UserRole role = UserRole::Default);
加入房间。只有在收到onJoinRoom事件之后才是真正的加入房间成功。

**参数**

| roomId | 房间id |
| --- | --- |
| role | 入会角色。UserRole::Default 普通用户；UserRole::Audience 听众<br/>听众不会出现在其他人的成员列表上 |


### void leaveRoom();
离开房间



### void setEvent(IRTCClientEvent* e);
设置事件接口

**参数**

| e | IRTCClientEvent 事件接口 |
| --- | --- |


### StatusCode updateUser(const char* user, uint32_t userSize);
更新用户信息，如果当前在房间中，会广播给房间内成员。

**参数**

| user | user对象 json格式字符串， 可以只填修改的字段 |
| --- | --- |
| userSize | user的字节数 |


### StatusCode updateRoom(const char* room, uint32_t roomSize);
更新房间信息，调用此接口会广播给房间内成员。

**参数**

| room | room对象 json格式字符串， 可以只填修改的字段 |
| --- | --- |
| roomSize | room的字节数 |




### StatusCode sendMessage(const char* userIds, const char* action, const char* content, uint32_t contentSize);
发送自定义消息。

**参数**

| userIds | 接收者的用户id，json数组格式的字符串。<br/>["id1","id2","id3",...] |
| --- | --- |
| action | 自定义action |
| content | 消息内容 |
| contentSize | content字节数 |




### StatusCode sendRoomMessage(const char* action, const char* content,uint32_t contentSize);
给房间内成员发送自定义消息。

**参数**

| action | 自定义action |
| --- | --- |
| content | 消息内容 |
| contentSize | content字节数 |






void me(char** s,uint32_t* c);

获取sdk内部我的信息。

输出内容放在*s内，当不再需要时必须通过VCS_Free释放。

**参数**

| s | 输出 user结构的json字符串 |
| --- | --- |
| c | 输出*s 的字节数 |




### void room(char** s, uint32_t* c);
获取sdk内部房间的信息。

输出内容放在*s内，当不再需要时必须通过VCS_Free释放。

**参数**

| s | 输出 room结构的json字符串 |
| --- | --- |
| c | 输出*s 的字节数 |




### void members(char** s, uint32_t* c);
获取当前加入房间的所有成员信息（包括自己）。

输出内容放在*s内，当不再需要时必须通过VCS_Free释放。

**参数**

| s | 输出 user结构的json字符串 |
| --- | --- |
| c | 输出*s 的字节数 |




### StatusCode getMember(const char* userId, char** s, uint32_t* c);
根据用户id查找成员信息。

输出内容放在*s内，当不再需要时必须通过VCS_Free释放。

**参数**

| s | 输出 user结构的json字符串 |
| --- | --- |
| c | 输出*s 的字节数 |




### StatusCode getMemberByLinkId(const char* linkId, char** s, uint32_t* c);
根据用户linkid查找成员信息。

输出内容放在*s内，当不再需要时必须通过VCS_Free释放。

**参数**

| s | 输出 user结构的json字符串 |
| --- | --- |
| c | 输出*s 的字节数 |




### StatusCode getMemberByLinkId(int linkId, char** s, uint32_t* c);
根据用户linkid查找成员信息。

输出内容放在*s内，当不再需要时必须通过VCS_Free释放。

**参数**

| s | 输出 user结构的json字符串 |
| --- | --- |
| c | 输出*s 的字节数 |




### void resume();
当网络恢复，或者界面重置到前台时，调用此接口可以立即发送心跳探测网络状况并重连。



### StatusCode createLocalVideoStream(int id,int type, CodecType codec,int width,int height,int fps,int bitrate,int angle, ILocalVideoStream** p);
创建本地视频流。

**参数**

| id | 轨道号 0-7 |
| --- | --- |
| type | 自定义类型 |
| codec | 编码类型 |
| width | 视频宽度 |
| height | 视频高度 |
| fps | 帧率，固定值 |
| bitrate | 码率，固定值  Bps |
| angle | 视频初始角度 |
| p | 输出流对象指针。 |


### StatusCode createLocalAudioStream(CodecType codec, int samplerate, int channels, ILocalAudioStream** p);
创建本地音频流。

**参数**

| id | 轨道号 0-7 |
| --- | --- |
| codec | 编码类型 |
| samplerate | 音频采样率 |
| channels | 音频通道数 |
| p | 输出流对象指针。 |


### StatusCode createRemoteVideoStream(const char* userId,IRemoteVideoStream** p);
创建远程视频流。

**参数**

| id | 轨道号 0-7 |
| --- | --- |
| userId | 用户id |
| p | 输出流对象指针。 |


### StatusCode createRemoteMixAudioStream(IRemoteMixAudioStream** p);
创建远程全局音频流。

**参数**

| p | 输出流对象指针。 |
| --- | --- |


