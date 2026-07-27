---
title: "IRemoteVideoStream"
description: "全平台 C++ SRTC 音视频 SDK IRemoteVideoStream 接口参考"
---

### void setFrameEvent(FrameEvent onFrameEvent,void* ctx)
设置码流数据接收回调。

**参数**

| onFrameEvent | 码流数据回调。<br/>void __stdcall FrameEvent(void* ctx,const char* userId, int linkId, const AVFrame& frame); |
| --- | --- |
| ctx | 回调上下文 |


### StatusCode subscribe(int mask, bool async = false)
订阅。

**参数**

| mask | 0-7轨道的掩码 |
| --- | --- |
| async | 是否异步<br/> true表示等待目标轨道上的i帧，如果目标轨道一直没有i帧则不会切换过去；false表示不等待直接切换。 |


掩码和轨道的转换方法

```cpp
static int track_to_mask(int track) {
    if (track < 0) {
        return 0;
    }
    return std::pow(2, track);
}

static int mask_to_track(int mask) {
    if (mask == 0) {
        return 0;
    }
    return std::log2(mask);
}
```

### StatusCode unsubscribe()
取消订阅。

### void close()
销毁对象

