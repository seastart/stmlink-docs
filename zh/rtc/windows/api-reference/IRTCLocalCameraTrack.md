---
title: "IRTCLocalCameraTrack"
description: "Windows SRTC 音视频 SDK IRTCLocalCameraTrack 接口参考"
---



## 函数说明
本地视频流推流对象。



## 继承关系
[IRTCTrack](https://www.yuque.com/anyconf/rtcengine/fkp5s07gsry40a9i) -> [IRTCLocalVideoTrack](https://www.yuque.com/anyconf/rtcengine/wupb3vgmah8ggqp5) ->IRTCLocalCameraTrack



## 函数方法
### 更新采集参数
```cpp
virtual StatusCode updateOptions(RTCCameraCaptureOptions* cap) = 0;
```cpp

**参数**

| cap | 视频轨道采集对象[查看](https://www.yuque.com/anyconf/rtcengine/rhsp7k#KUK5g) |
| --- | --- |


注意：

1，更新后，推荐更新推流信息否则会使用之前的推流参数

2，已经打开采集后，无需调用再次打开



### 开始采集
```cpp
virtual StatusCode startCapture(RTCCameraCaptureOptions* cap = nullptr) = 0;
```

**参数**

| cap | 视频轨道采集对象[查看](https://www.yuque.com/anyconf/rtcengine/rhsp7k#KUK5g) |
| --- | --- |




### 停止采集
```cpp
virtual StatusCode stopCapture() = 0;
```cpp





