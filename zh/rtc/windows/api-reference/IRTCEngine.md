---
title: "IRTCEngine"
description: "Windows 音视频 SDK 的核心接口：创建与释放实例、频道进出、成员信息查询、媒体控制"
---



## IRTCEngine
### 创建IRTCEngine
```cpp
RTCENGINE_API StatusCode RTCENGINE_CALL RTCEngine_Init(IRTCEngine** rtc, RTCEngineOptions* opt);
```

**参数**

| rtc | IRTCEngine 对象类，失败时为 nullptr |
| --- | --- |
| opt | 引擎初始化参数，[RTCEngineOptions](../types.md#引擎初始化参数（RTCEngineOptions）)。**传 nullptr 表示完全不写 SDK 日志** |


注：日志开关和日志路径原先在 `IRTCSetting` 上（`enable_stream_log` / `sdk_log_path`），现已移到这里 —— 
它们在引擎自身初始化阶段就被消费，那时还没有任何频道对象。


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
```

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
### 设置消息回调
```cpp
virtual StatusCode setEventHandler(IRTCEngineEvent* e) = 0;
```

**参数**

| e | 消息事件回调纯虚函数实体类，相关回调[点击查看](./IRTCEngineEvent.md) |
| --- | --- |



## 频道相关函数

支持同时加入多个频道。每个频道对应一个 [IRTCChannel](./IRTCChannel.md) 对象，频道级的接口和回调都在那个对象上，
不再像旧版一样在 `IRTCEngine` 上用 `channelId` 首参来区分。

**关于 channelId**

+ `channelId` 就是 token 中 `channel` 字段的值，由 SDK 内部解析，通过 `IRTCChannel::getChannelId()` 取得
+ `channelId` 只用于 `leaveChannel` 和 `getChannelIds`，其余接口都直接调频道对象

### 创建频道对象
```cpp
virtual StatusCode createChannel(const char* token, IRTCChannel** ch) = 0;
```

**参数**

| token | 加入频道所需要的token |
| --- | --- |
| ch | 出参，频道对象。失败时为 nullptr |


注：**只创建对象，不进入频道**。拿到对象后设置好配置和事件回调，再调用 [IRTCChannel::join()](./IRTCChannel.md#进入频道)。
重复创建同一频道返回 `Conflict`；token 解析不出频道返回 `SdkTokenInvalid`。


### 离开频道
```cpp
virtual void leaveChannel(const char* channelId) = 0;
```

**参数**

| channelId | 要离开的频道id |
| --- | --- |


### 离开所有频道
```cpp
virtual void leaveAllChannel() = 0;
```


### 获取已加入的频道列表
```cpp
virtual StatusCode getChannelIds(char** s, int* c) = 0;
```

**参数**

| s | 已加入的 channelId json array，例如 ["ch_a","ch_b"] |
| --- | --- |
| c | json array 长度 |



## 流媒体相关函数
### 网络测速
```cpp
	virtual StatusCode probeNetwork(int time, int upindex, int downindex) = 0;
```

**参数**

| time | 需要测速的时间，建议是10的倍数 |
| --- | --- |
| upindex | 测速上行（单位KB），0 为不进行此项测速 |
| downindex | 测速下行（单位KB），0 为不进行此项测速 |


注：测速结果将在[回调](./IRTCEngineEvent.md#上行统计回调)内返回





### 获取摄像头信息
```cpp
virtual StatusCode getEnumVideo(char** devices, int* iSize) = 0;
```

**参数**

| Devices | 摄像头信息json, [摄像头信息](../types.md#摄像头枚举信息) |
| --- | --- |
| iSize | 摄像头信息json 长度 |




### 获取屏幕信息
```cpp
virtual StatusCode getEnumScreen(char** devices, int* iSize) = 0;
```

**参数**

| Devices | 屏幕信息json, [共享屏幕信息](../types.md#共享屏幕枚举信息) |
| --- | --- |
| iSize | 屏幕信息json 长度 |




### 获取麦克风信息
```cpp
virtual StatusCode getEnumAudio(char** devices, int* iSize) = 0;
```

**参数**

| Devices | 麦克风信息json, [麦克风信息](../types.md#麦克风/扬声器枚举信息) |
| --- | --- |
| iSize | 麦克风信息json 长度 |




### 获取扬声器信息
```cpp
virtual StatusCode getEnumSpeaker(char** devices, int* iSize) = 0;
```

**参数**

| Devices | 扬声器信息json, [扬声器信息](../types.md#麦克风/扬声器枚举信息) |
| --- | --- |
| iSize | 扬声器信息json 长度 |






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

