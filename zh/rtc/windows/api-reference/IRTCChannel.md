---
title: "IRTCChannel"
description: "一个频道（会议）对象：频道配置、事件回调、进入频道、成员信息查询、轨道与推拉流"
---



## IRTCChannel

`IRTCChannel` 代表**一个频道**，由 [IRTCEngine::createChannel](./IRTCEngine.md#创建频道对象) 创建。

`createChannel` 只解析 token、创建对象，**并不进入频道**。这样调用方有机会在 `join()` 之前把
配置和事件回调设置好 —— `onJoinChannel` 是在 `join()` 还没返回时就回调出去的，回调设置晚了就会漏掉。

```cpp
SRTC::IRTCChannel* ch = nullptr;
if (engine->createChannel(token, &ch) != SRTC::StatusCode::OK) {
    return;   // 失败时 ch 一定是 nullptr
}

// 1) 配置（join 前才有意义的项见 IRTCChannelSetting）
SRTC::IRTCChannelSetting* set = nullptr;
ch->getSetting(&set);
set->set_stream_model(1);

// 2) 事件回调，必须在 join() 之前
ch->setEventHandler(this);

// 3) 进入频道
if (ch->join() != SRTC::StatusCode::OK) {
    engine->leaveChannel(ch->getChannelId());   // 失败的频道对象也要回收
    ch = nullptr;
    return;
}
```

退出频道统一走 [IRTCEngine::leaveChannel](./IRTCEngine.md#离开频道)，`IRTCChannel` 自身**没有** `leave()`。
调用后该对象已销毁，调用方必须自行把指针置空。

## 基础函数
### 获取频道id
```cpp
virtual const char* getChannelId() = 0;
```

返回 token 中 `channel` 字段的值。指针由 SDK 持有，有效期到该频道退出为止，不需要调用方释放。


### 获取配置信息对象
```cpp
virtual StatusCode getSetting(IRTCChannelSetting** set) = 0;
```

**参数**

| set | 频道配置信息类，详细内容[查看](./IRTCChannelSetting.md) |
| --- | --- |


### 设置消息回调
```cpp
virtual StatusCode setEventHandler(IRTCChannelEvent* e) = 0;
```

**参数**

| e | 频道消息事件回调纯虚函数实体类，相关回调[点击查看](./IRTCChannelEvent.md) |
| --- | --- |


注：必须在 `join()` 之前设置，否则收不到 `onJoinChannel`。


### 进入频道
```cpp
virtual StatusCode join() = 0;
```

注：同步接口，返回前 `onJoinChannel` 已经回调完毕。重复调用返回 `Conflict`。失败时该频道对象仍然存在，
需要用 [IRTCEngine::leaveChannel](./IRTCEngine.md#离开频道) 回收。


## 成员信息函数
### 获取自身用户信息
```cpp
virtual StatusCode getMe(char** s, int* c) = 0;
```

**参数**

| s | 用户信息json  |
| --- | --- |
| c | 用户信息json 长度 |




### 获取频道信息
```cpp
virtual StatusCode getChannel(char** s, int* c) = 0;
```

**参数**

| s | 频道信息json  |
| --- | --- |
| c | 频道信息json 长度 |



### 获取频道所有成员信息
```cpp
virtual StatusCode getMembers(char** s, int* c) = 0;
```

**参数**

| s | 所有用户信息json array |
| --- | --- |
| c | 所有用户信息json array长度 |






### 获取指定成员信息
```cpp
virtual StatusCode getMember(const char* uid, char** s, int* c) = 0;
virtual StatusCode getMemberByLinkId(const char* linkId, char** s, int* c) = 0;
virtual StatusCode getMemberByLinkId(int linkId, char** s, int* c) = 0;
		
```

**参数**

| uid/linkid | 用户id,流媒体linkid |
| --- | --- |
| s | 用户信息json |
| c | 用户信息json 长度 |



### 频道级接口的错误码

| 还没 `join()` 就调用媒体类接口 | `NotInitialized` |
| --- | --- |

## 流媒体相关函数
### 获取视频轨道对象
```cpp
virtual StatusCode getCameraTrack(const char* track_key,IRTCLocalCameraTrack ** track) = 0;
```

**参数**

| track_key | 本地视频轨道对象key，使用者维护此key。用于区分不通轨道对象，默认推流的desc |
| --- | --- |
| track | [视频轨道对象](./IRTCLocalScreenTrack.md) |




### 获取共享屏幕流对象
```cpp
virtual StatusCode getScreenTrack(const char* track_key,IRTCLocalScreenTrack ** track) = 0;
```

**参数**

| track_key | 本地视频轨道对象key，使用者维护此key。用于区分不通轨道对象,默认推流的desc |
| --- | --- |
| track | [屏幕轨道对象](./IRTCLocalScreenTrack.md) |




### 获取音频流对象
```cpp
virtual StatusCode getAudioTrack(const char* track_key,IRTCLocalMicTrack** track) = 0;
```

**参数**

| track_key | 本地视频轨道对象key，使用者维护此key。用于区分不通轨道对象,默认推流的desc |
| --- | --- |
| track | [麦克风轨道对象](./IRTCLocalAudioTrack.md) |




### 获取成员音频轨道对象
```cpp
virtual StatusCode getRemoteAudioTrack(const char* uid, const char* trackid, IRTCRemoteAudioTrack** track) = 0;
```

**参数**

| uid | 用户id（空为全体用户） |
| --- | --- |
| trackid | 用户音频流轨道id（空为全体轨道） |
| track | [本地音频混音轨道对象](./IRTCRemoteAudioTrack.md) |




### 获取成员视频轨道对象
```cpp
virtual StatusCode getRemoteVideoTrack(const char* uid, const char* trackid, IRTCRemoteVideoTrack** track) = 0;
```

**参数**

| uid | 用户id |
| --- | --- |
| trackid | 用户视频流轨道id |
| track | [成员视频轨道对象](./IRTCRemoteVideoTrack.md) |




### 获取合成流视频轨道对象
```cpp
virtual StatusCode getMCUVideoTrack(IRTCRemoteVideoTrack** track) = 0;
```

**参数**

| track | [合成流视频轨道对象](./IRTCRemoteVideoTrack.md) |
| --- | --- |






### 订阅流轨道
```cpp
virtual StatusCode subscribe(IRTCTrack* tk ) = 0;
```

**参数**

| tk | 流轨道信息[IRTCRemoteVideoTrack](#xvHeQ)，[IRTCRemoteAudioTrack](#mxOa1) |
| --- | --- |


### 取消订阅流轨道
```cpp
virtual StatusCode unsubscribe(IRTCTrack* tk ) = 0;
```

**参数**

| tk | 流轨道信息[IRTCRemoteVideoTrack](#xvHeQ)，[IRTCRemoteAudioTrack](#mxOa1) |
| --- | --- |


### 发布视频轨道
```cpp
virtual StatusCode publish(IRTCTrack* tk, RTCVideoPublishOptions* opt) = 0;
```

**参数**

| tk | 流轨道信息，[IRTCLocalCameraTrack](#D2C4E)，[IRTCLocalScreenTrack](#WYT3t)， |
| --- | --- |
| opt | 推流轨道参数，空为，默认推流参数，[RTCVideoPublishOptions](../types.md#视频轨道推流信息（RTCVideoPublishOptions）) |


### 发布音频轨道
```cpp
virtual StatusCode publish(IRTCTrack* tk, RTCAudioPublishOptions* opt) = 0;
```

**参数**

| tk | 流轨道信息，[IRTCLocalMicTrack](#zLaZA) |
| --- | --- |
| opt | 推流轨道参数，空为，默认推流参数，[RTCAudioPublishOptions](../types.md#音频轨道输出信息（RTCAudioOutputOptions）) |


注：两个 `publish` 重载不再带默认参数（原先 `publish(tk)` 本身就是二义调用、无法编译），调用时必须显式传 `opt`。





