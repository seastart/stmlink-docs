### StatusCode publish();
发布视频流。

### StatusCode unpublish();
停止发布。

### StatusCode input(const uint8_t* data,int dataSize,int64_t pts,int64_t dts,FrameType ft);
输入一帧h264的视频数据。

**参数**

| data | 帧数据 |
| --- | --- |
| dataSize | 数据字节数 |
| pts | pts |
| dst | dts |
| ft | 帧类型FrameType |


### StatusCode setAngle(int angle);
设置角度。

手机类终端横竖屏的时候需要设置一个表示旋转和镜像的角度

**参数**

| angle |  |
| --- | --- |


### void close();
销毁对象。

