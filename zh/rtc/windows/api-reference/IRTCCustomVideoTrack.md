---
title: "IRTCCustomVideoTrack"
description: "Windows SRTC 音视频 SDK IRTCCustomVideoTrack 自定义视频轨道接口参考"
---

## 函数说明
自定义视频轨道接口，用于推送自定义视频数据流。

## 继承关系
[IRTCTrack](./IRTCTrack.md) -> IRTCCustomVideoTrack

## 函数方法

### 推送视频帧
```cpp
virtual StatusCode pushVideoFrame(int stmtype, unsigned char* buf, int buf_len, int frmtype, long ts) = 0;
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| stmtype | int | 流类型（如 H264、H265 等编码类型） |
| buf | unsigned char* | 视频帧数据缓冲区 |
| buf_len | int | 数据缓冲区长度 |
| frmtype | int | 帧类型（如关键帧、P 帧等） |
| ts | long | 时间戳 |

**返回值**

| 返回值 | 说明 |
| --- | --- |
| StatusCode | 操作结果状态码 |

**示例**

```cpp
// 推送 H264 关键帧
IRTCCustomVideoTrack* track = nullptr;
engine->getCustomVideoTrack("my_custom_track", &track);
track->pushVideoFrame(0x1b, frameData, frameSize, 1, timestamp);
```
