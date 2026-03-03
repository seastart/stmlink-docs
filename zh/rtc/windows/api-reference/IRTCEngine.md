---
title: "IRTCEngine"
description: "Windows SRTC 音视频 SDK IRTCEngine 接口参考"
---



## IRTCEngine
### 创建IRTCEngine
```cpp
RTCENGINE_API StatusCode RTCENGINE_CALL RTCEngine_Init(IRTCEngine** rtc);
```cpp

**参数**

| rtc | IRTCEngine 对象类 |
| --- | --- |




### 释放IRTCEngine
```cpp
RTCENGINE_API void RTCENGINE_CALL RTCEngine_Free(IRTCEngine** rtc);
```

**参数**

| rtc | IRTCEngine 对象类 |
| --- | --- |




### 获取版本号信息
```cpp
RTCENGINE_API StatusCode RTCENGINE_CALL RTCEngine_Version(const char*v1);
```cpp

**参数**

| v1 | sdk版本号 |
| --- | --- |


注：需要传入的时候需要外面分配内存，至少100长度

### 
### 获取错误码描述
```cpp
RTCENGINE_API void RTCENGINE_CALL RTCEngine_GetStatusMsg(StatusCode code, char* msg);
```

**参数**

| code | 错误码 |
| --- | --- |
| msg | 错误码描述信息 |


注：msg需要传入的时候需要外面分配内存，至少100长度，中文编码gbk



## 基础函数
### 获取配置信息对象
```cpp
virtual StatusCode getSetting(IRTCSetting** set) = 0;
```cpp

**参数**

| set | sdk 配置信息类，详细内容[查看](https://www.yuque.com/anyconf/rtcengine/rpk21xqv0ilgfgw7) |
| --- | --- |




### 设置消息回调
```cpp
virtual StatusCode setEventHandler(IRTCEngineEvent* e) = 0;
```

**参数**

| e | 消息事件回调纯虚函数实体类，相关回调[点击查看](https://www.yuque.com/anyconf/rtcengine/yrwtcw) |
| --- | --- |


## 
## 频道相关函数
### 加入频道
```cpp
virtual StatusCode joinChannel(const char* token) = 0;
```cpp

**参数**

| token | 加入频道所需要的token |
| --- | --- |




### 离开频道
```cpp
virtual void leaveChannel() = 0;
```

### 
### 获取自身用户信息
```cpp
virtual StatusCode getMe(char** s, int* c) = 0;
```cpp

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


### 
### 获取频道所有成员信息
```cpp
virtual StatusCode getMembers(char** s, int* c) = 0;
```typescript

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






## 流媒体相关函数
### 网络测速
```cpp
	virtual StatusCode probeNetwork(int time, int upindex, int downindex) = 0;
```cpp

**参数**

| time | 需要测速的时间，建议是10的倍数 |
| --- | --- |
| upindex | 测速上行（单位KB），0 为不进行此项测速 |
| downindex | 测速下行（单位KB），0 为不进行此项测速 |


注：测速结果将在[回调](https://www.yuque.com/anyconf/rtcengine/yrwtcw/edit#wR50G)内返回





### 获取摄像头信息
```cpp
virtual StatusCode getEnumVideo(char** devices, int* iSize) = 0;
```

**参数**

| Devices | 摄像头信息json, [摄像头信息](https://www.yuque.com/anyconf/rtcengine/rhsp7k/edit#s0Yn4) |
| --- | --- |
| iSize | 摄像头信息json 长度 |




### 获取屏幕信息
```cpp
virtual StatusCode getEnumScreen(char** devices, int* iSize) = 0;
```cpp

**参数**

| Devices | 屏幕信息json, [共享屏幕信息](https://www.yuque.com/anyconf/rtcengine/rhsp7k#Ryiwr) |
| --- | --- |
| iSize | 屏幕信息json 长度 |




### 获取麦克风信息
```cpp
virtual StatusCode getEnumAudio(char** devices, int* iSize) = 0;
```

**参数**

| Devices | 麦克风信息json, [麦克风信息](https://www.yuque.com/anyconf/rtcengine/rhsp7k#gEyGf) |
| --- | --- |
| iSize | 麦克风信息json 长度 |




### 获取扬声器信息
```cpp
virtual StatusCode getEnumSpeaker(char** devices, int* iSize) = 0;
```typescript

**参数**

| Devices | 扬声器信息json, [扬声器信息](https://www.yuque.com/anyconf/rtcengine/rhsp7k#gEyGf) |
| --- | --- |
| iSize | 扬声器信息json 长度 |




### 获取视频轨道对象
```cpp
virtual StatusCode getCameraTrack(const char* track_key,IRTCLocalCameraTrack ** track) = 0;
```

**参数**

| track_key | 本地视频轨道对象key，使用者维护此key。用于区分不通轨道对象，默认推流的desc |
| --- | --- |
| track | [视频轨道对象](https://www.yuque.com/anyconf/rtcengine/tqhsrn) |




### 获取共享屏幕流对象
```cpp
virtual StatusCode getScreenTrack(const char* track_key,IRTCLocalScreenTrack ** track) = 0;
```typescript

**参数**

| track_key | 本地视频轨道对象key，使用者维护此key。用于区分不通轨道对象,默认推流的desc |
| --- | --- |
| track | [屏幕轨道对象](https://www.yuque.com/anyconf/rtcengine/tqhsrn) |




### 获取音频流对象
```cpp
virtual StatusCode getAudioTrack(const char* track_key,IRTCLocalMicTrack** track) = 0;
```

**参数**

| track_key | 本地视频轨道对象key，使用者维护此key。用于区分不通轨道对象,默认推流的desc |
| --- | --- |
| track | [麦克风轨道对象](https://www.yuque.com/anyconf/rtcengine/slm5sw) |




### 获取成员音频轨道对象
```cpp
virtual StatusCode getRemoteAudioTrack(const char* uid, const char* trackid, IRTCRemoteAudioTrack** track) = 0;
```typescript

**参数**

| uid | 用户id（空为全体用户） |
| --- | --- |
| trackid | 用户音频流轨道id（空为全体轨道） |
| track | [本地音频混音轨道对象](https://www.yuque.com/anyconf/rtcengine/dvvov9) |




### 获取成员视频轨道对象
```cpp
virtual StatusCode getRemoteVideoTrack(const char* uid, const char* trackid, IRTCRemoteVideoTrack** track) = 0;
```

**参数**

| uid | 用户id |
| --- | --- |
| trackid | 用户视频流轨道id |
| track | [成员视频轨道对象](https://www.yuque.com/anyconf/rtcengine/uqtaox) |




### 获取合成流视频轨道对象
```cpp
virtual StatusCode getMCUVideoTrack(IRTCRemoteVideoTrack** track) = 0;
```cpp

**参数**

| track | [合成流视频轨道对象](https://www.yuque.com/anyconf/rtcengine/uqtaox) |
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
```cpp

**参数**

| tk | 流轨道信息[IRTCRemoteVideoTrack](#xvHeQ)，[IRTCRemoteAudioTrack](#mxOa1) |
| --- | --- |


### 发布视频轨道
```cpp
virtual StatusCode publish(IRTCTrack* tk, RTCVideoPublishOptions* opt = nullptr) = 0;
```

**参数**

| tk | 流轨道信息，[IRTCLocalCameraTrack](#D2C4E)，[IRTCLocalScreenTrack](#WYT3t)， |
| --- | --- |
| opt | 推流轨道参数，空为，默认推流参数，[RTCVideoPublishOptions](https://www.yuque.com/anyconf/rtcengine/rhsp7k#oRuFU) |


### 发布音频轨道
```cpp
virtual StatusCode publish(IRTCTrack* tk, RTCAudioPublishOptions* opt = nullptr) = 0;
```typescript

**参数**

| tk | 流轨道信息，[IRTCLocalMicTrack](#zLaZA) |
| --- | --- |
| opt | 推流轨道参数，空为，默认推流参数，[RTCAudioPublishOptions](https://www.yuque.com/anyconf/rtcengine/rhsp7k#aqSxT) |






## 其他
### 添加上传日志
```cpp
virtual StatusCode addUploadLog(const char* type ,const char* msg) = 0;
```

**参数**

| type | 日志类型标识 |
| --- | --- |
| msg | 日志内容 |


添加后的日志会上传到日志服务器上。

