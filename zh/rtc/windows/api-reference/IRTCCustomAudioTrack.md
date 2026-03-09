---
title: "IRTCCustomAudioTrack"
description: "Windows SRTC 音视频 SDK IRTCCustomAudioTrack 自定义音频轨道接口参考"
---

## 函数说明
自定义音频轨道接口，用于推送自定义音频数据流。

## 继承关系
[IRTCTrack](./IRTCTrack.md) -> IRTCCustomAudioTrack

## 函数方法

### 推送音频帧
```cpp
virtual StatusCode pushAudioFrame(int stmtype, unsigned char* buf, int buf_len, long ts) = 0;
```

**参数**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| stmtype | int | 流类型（如 AAC、OPUS 等编码类型） |
| buf | unsigned char* | 音频帧数据缓冲区 |
| buf_len | int | 数据缓冲区长度 |
| ts | long | 时间戳 |

**返回值**

| 返回值 | 说明 |
| --- | --- |
| StatusCode | 操作结果状态码 |

**示例**

```cpp
// 推送 OPUS 音频帧
IRTCCustomAudioTrack* track = nullptr;
engine->getCustomAudioTrack("my_custom_audio", &track);
track->pushAudioFrame(0x5355504F, audioData, audioSize, timestamp);
```
