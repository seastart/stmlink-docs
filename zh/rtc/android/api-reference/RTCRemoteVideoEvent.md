---
title: "RTCRemoteVideoEvent"
description: "Android SRTC 音视频 SDK RTCRemoteVideoEvent 接口参考"
---

## 说明

`RTCRemoteVideoEvent` 为远端视频流状态回调接口。

## 接口方法

### onReceiveStreamStatusChange(uid, trackDesc, isChoke)
```kotlin
fun onReceiveStreamStatusChange(uid: String, trackDesc: String, isChoke: Boolean)
```
方法说明：远端视频流状态变化回调。  
参数说明：
- `uid`：`String`，远端用户 ID。
- `trackDesc`：`String`，轨道描述。
- `isChoke`：`Boolean`，是否卡顿；`true` 为卡顿，`false` 为恢复正常。
返回值说明：无（`Unit`）。
