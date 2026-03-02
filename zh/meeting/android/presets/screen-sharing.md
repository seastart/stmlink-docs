### PreOptionScreen 
PreOptionScreen 类中包含 ScreenCaptureOptions、VideoPublishOptions 两个属性

| ScreenCaptureOptions | 屏幕采集配置参数 |
| --- | --- |
| VideoPublishOptions | 视频流发布配置参数 |


### ScreenCaptureOptions
ScreenCaptureOptions 类主要用于配置频屏幕采集参数，具体参数如下

| deviceId | String 类型，设备 id |
| --- | --- |
| width | Int 类型，屏幕采集画面宽 |
| height | Int 类型，屏幕采集画面高 |
| maxFps | Int 类型，最大帧率 |
| maxBitrate | Int 类型，最大码率 |


### VideoPublishOptions
VideoPublishOptions 类主要用于配置视频流发布参数，具体参数如下

| desc | String 类型，轨道描述 |
| --- | --- |
| codec | CodecType 类型，编码格式<br/>CodecType.unknow：未知<br/>CodecType.H264：h264 格式<br/>CodecType.H265：h265 格式 |
| maxBitrate | Int 类型，最大码率 |
| width | Int 类型，发布的画面宽度 |
| height | Int 类型，发布的画面高度 |
| maxFps | Int 类型，最大帧率 |
| props | Any 类型，自定义属性。<font style="color:#DF2A3F;">可空</font> |
| simulcasts | MutableList<VideoPublishOptions> 类型。<br/>+ <font style="color:#DF2A3F;">目前只有摄像头流存在发布多路流的情况，所以此处用不上这个属性</font> |


### PublishCustomOptions
PublishCustomOptions 类是用于在发布时对 desc、props 这两个参数做修改

| desc | String 类型，轨道描述。<br/>+ 可空，表示不做修改 |
| --- | --- |
| props | Any 类型，自定义属性。<br/>+ 可空，表示不做修改 |
| simulcasts | MutableList<PublishCustomOptions> 类型。<br/>+ <font style="color:#DF2A3F;">目前只有摄像头流存在发布多路流的情况，所以此处用不上这个属性</font> |


## 预设值
目前预设值只有一个 PreOptionScreen.def

+ 可以通过直接修改 PreOptionScreen.def 获取到的实例的参数值，然后使用。<font style="color:#DF2A3F;">如无特殊需求不建议修改</font>

```kotlin
// 获取默认预设值
val preOpt: PreOptionScreen = PreOptionScreen.def
// 修改采集配置中的最大帧率
preOpt.capture.maxFps = 10
// 修改发布配置中的编码格式
preOpt.publish.codec = CodecType.H264
// 使用修改后的预设值
...
```

### PreOptionScreen.def
配置如下：

```kotlin
val def = PreOptionScreen(
            ScreenCaptureOptions(
                deviceId = "screenCapDef",
                width = 1280,
                height = 720,
                maxFps = 10,
                maxBitrate = 1024*1024
            ),
            VideoPublishOptions(
                desc = TrackDesc.TRACK_SHARE.value,
                codec = CodecType.H264,
                maxBitrate = 1024*1024,
                width = 1280,
                height = 720,
                maxFps = 10,
                props = null,
                simulcasts = null
            )
        )
```

