### StatusCode publish();
发布音频流。

### StatusCode unpublish();
停止发布。

### StatusCode input(const uint8_t& data,int dataSize,int64_t pts,int64_t dts,int volume)
输入一帧编码好的音频数据。

**参数**

| data | 帧数据 |
| --- | --- |
| dataSize | 数据字节数 |
| pts | pts |
| dst | dts |
| volume | PCM 帧的平均幅度（0 ~ 32787） |


### void close();
销毁对象。

