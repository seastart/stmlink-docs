---
title: "RemoteAudioMixTrack"
description: "Android SRTC 音视频 SDK RemoteAudioMixTrack 接口参考"
---

## 说明

`RemoteAudioMixTrack` 用于控制远端混音轨道的本地播放开关。

## RemoteAudioMixTrack 自身方法

### startPlay()
```kotlin
fun startPlay()
```
方法说明：开始播放远端音频（内部会启用扬声器输出）。  
参数说明：无。  
返回值说明：无（`Unit`）。

### stopPlay()
```kotlin
fun stopPlay()
```
方法说明：停止播放远端音频（内部会关闭扬声器输出）。  
参数说明：无。  
返回值说明：无（`Unit`）。
