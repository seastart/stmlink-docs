---
title: "IRTCLocalCameraTrack"
description: "Windows SRTC 音视频 SDK IRTCLocalCameraTrack 接口参考"
---



## 函数说明
本地视频流推流对象。



## 继承关系
[IRTCTrack](./IRTCTrack.md) -> [IRTCLocalVideoTrack](./IRTCLocalVideoTrack.md) ->IRTCLocalCameraTrack



## 函数方法
### 更新采集参数
```cpp
virtual StatusCode updateOptions(RTCCameraCaptureOptions* cap) = 0;
```

**参数**

| cap | 视频轨道采集对象[查看](../types.md#视频轨道采集信息（RTCCameraCaptureOptions）) |
| --- | --- |


注意：

1，更新后，推荐更新推流信息否则会使用之前的推流参数

2，已经打开采集后，无需调用再次打开



### 开始采集
```cpp
virtual StatusCode startCapture(RTCCameraCaptureOptions* cap = nullptr) = 0;
```

**参数**

| cap | 视频轨道采集对象[查看](../types.md#视频轨道采集信息（RTCCameraCaptureOptions）) |
| --- | --- |




### 停止采集
```cpp
virtual StatusCode stopCapture() = 0;
```





