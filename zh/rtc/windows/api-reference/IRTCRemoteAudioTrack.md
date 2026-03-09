---
title: "IRTCRemoteAudioTrack"
description: "Windows SRTC 音视频 SDK IRTCRemoteAudioTrack 接口参考"
---

## 函数说明
远端音频混音对象。



## 继承关系
[IRTCTrack](./IRTCTrack.md) ->IRTCRemoteAudioTrack





## 函数方法
### 开启音频输出
```cpp
virtual StatusCode startPlay(RTCAudioOutputOptions* opt = nullptr) = 0;
```

**参数**

| opt | 音频轨道输出信息[查看](../types.md#音频轨道输出信息（RTCAudioOutputOptions）) |
| --- | --- |




### 停止音频输出
```cpp
virtual StatusCode stopPlay() = 0;
```



