---
title: "LocalMicTrack"
description: "Android SRTC 音视频 SDK LocalMicTrack 接口参考"
---

## 说明

`LocalMicTrack` 用于获取本地麦克风采集音量信息，并可作为 `publishLocalAudio` 的输入轨道。

## LocalMicTrack 自身方法

### getVolume()
```kotlin
fun getVolume(): Int
```
方法说明：获取实时麦克风音量大小。  
参数说明：无。  
返回值说明：`Int`，当前麦克风音量值。
