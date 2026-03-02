+ 提供自定义推流相关操作

### startCustomVideo()
开始推自定义视频流

```kotlin
fun startCustomVideo(option: CustomVideoOptions, listener: RTCResultListener?)
```

参数

| option | CustomVideoOptions 类型。推送参数 |
| --- | --- |
| listener | 操作结果回调 |


CustomVideoOptions 属性说明

| id | String 类型。 流 id |
| --- | --- |
| codec | CodecType 枚举类型。流编码类型<br/>CodecType.H264   H264 视频格式<br/>CodecType.H265  H265 视频格式 |
| width | Int 类型。视频宽 |
| height | Int 类型。视频高 |
| maxFps | Int 类型。视频帧率 |
| angle | Int 类型。视频角度 |
| maxBitrate | Int 类型。码率 |
| track | 指定要推送的轨道号 |
| props | JsonElement 类型。扩展信息 |


### stopCustomVideo()
停止推送自定义视频流

```kotlin
fun stopCustomVideo(listener: RTCResultListener?)
```

参数

| listener | 操作结果回调 | 操作结果回调 |
| --- | --- | --- |


### inputData()
发送编码后的流

```kotlin
fun inputData(stamp:Long,data:ByteArray,angle:Int)
```

参数

| stamp | Long 类型。时间戳 | |
| --- | --- | --- |
| data | ByteArray 类型。帧数据 | 操作结果回调 |
| angle | Int 类型。角度信息 |  |




