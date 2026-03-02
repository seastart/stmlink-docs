流媒体事件监听接口

### onMediaConnected()
流媒体服务器连接

```java
fun onMediaConnected()
```

### onRemoteVideoFrame()
远端视频流

```java
fun onRemoteVideoFrame(
    uid: String, trackDesc: String,
    y: ByteArray?, u: ByteArray?, v: ByteArray?,
    width: Int, height: Int, format: Int, angle: Int
)
```

参数

| uid | String 类型，用户 id |
| --- | --- |
| trackDesc | String 类型，轨道描述 |
| y | ByteArray 类型，y 分量数据 |
| u | ByteArray 类型，u 分量数据 |
| v | ByteArray 类型，v 分量数据 |
| width | Int 类型，画面宽度 |
| height | Int 类型，画面高度 |
| format | Int 类型，编码格式 |
| angle | Int 类型，画面角度 |


### onPreviewFrame()
本地视频流

```java
fun onPreviewFrame(
    yuv: ByteArray?, width: Int, height: Int, 
    stamp: Long, format: Int, facing: Int
)
```

参数

| yuv | ByteArray 类型，帧数据 | |
| --- | --- | --- |
| width | Int 类型，视频帧宽度 | |
| height | Int 类型，视频帧高度 | |
| stamp | Long 类型，时间戳 | |
| format | Int 类型，视频帧格式 | |
| facing | Int 类型，前后置摄像头标识<br/>        1：前置摄像头<br/>        0：后置摄像头 | Int 类型，前后置摄像头标识<br/>        1：前置摄像头<br/>        0：后置摄像头 |


### onPreviewRealSize()
本地视频流参数改变

```java
fun onPreviewRealSize(width: Int, height: Int, facing: Int)
```

参数

| width | Int 类型，画面宽度 |
| --- | --- |
| height | Int 类型，画面高度 |
| facing | Int 类型，前后置摄像头标识<br/>        1：前置摄像头<br/>        0：后置摄像头 |


### onMediaMetric()
媒体性能指标

```java
fun onMediaMetric(metric: MediaMetric.Metric)
```

参数

| metric | [MediaMetric](https://www.yuque.com/anyconf/smeeting/bfo4ig3hohgp9duy) 类型，媒体性能指标数据 |
| --- | --- |


### onVolumesReport()
音量信息

```java
fun onVolumesReport(volumes: MutableMap<UserTrackDesc, VolumeInfo>)
```

参数

| volumes | MutableMap 类型，key：UserTrackDesc 类型，用户id、轨道描述的封装类；value：VolumeInfo 类型，音量信息 |
| --- | --- |


UserTrackDesc 属性说明

| uid | String 类型，用户 id |
| --- | --- |
| trackDesc | String 类型，轨道描述 |


VolumeInfo 属性说明

| uid | String 类型，用户 id |
| --- | --- |
| db | Int 类型，音频能量，单位分贝 |


### 
### 
### 
### 
