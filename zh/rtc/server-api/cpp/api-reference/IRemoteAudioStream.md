---
title: "IRemoteAudioStream"
description: "全平台 C++ SRTC 音视频 SDK IRemoteAudioStream 接口参考"
---

### void setFrameEvent(FrameEvent onFrameEvent,void* ctx)
设置码流数据接收回调。

**参数**

| onFrameEvent | 码流数据回调。<br/>void __stdcall FrameEvent(void* ctx,const char* userId, int linkId, const AVFrame& frame); |
| --- | --- |
| ctx | 回调上下文 |


### StatusCode subscribe()
订阅

### StatusCode unsubscribe()
取消订阅。

### void close()
销毁对象

