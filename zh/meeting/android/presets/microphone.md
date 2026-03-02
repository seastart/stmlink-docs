### PreOptionMic
PreOptionMic 类中包含 MicCaptureOptions、AudioPublishOptions 两个属性

| MicCaptureOptions | 麦克风采集配置参数 |
| --- | --- |
| AudioPublishOptions | 音频流发布配置参数 |


### MicCaptureOptions
MicCaptureOptions 类主要用于配置麦克风采集参数，具体参数如下

| deviceId | String 类型，设备 id |
| --- | --- |
| echoCancellation | Boolean 类型，是否配置 AEC 回声消除 |
| noiseSuppression | Boolean 类型，是否配置 ANS 降噪 |
| autoGainControl | Boolean 类型，是否配置 AGC 自动增益 |
| channelCount | Int 类型，声道数，目前只支持单声道 |
| sampleRate | Int 类型，采样率，16K 或者 48K |
| sampleSize | Int 类型，位深，默认 16bit |
| latency | Double 类型，可接收或需要的延迟或延迟范围 |


### AudioPublishOptions
AudioPublishOptions 类主要用于配置音频流发布参数，具体参数如下

| desc | String 类型，轨道描述 |
| --- | --- |
| codec | CodecType 类型，编码格式<br/>CodecType.unknow：未知<br/>CodecType.AAC：AAC 格式<br/>CodecType.OPUS：OPUS 格式 |
| maxBitrate | Int 类型，最大码率 |
| dtx | Boolean 类型，是否启用 dtx(音频的不连续传输) |
| red | Boolean 类型，是否启用 red(冗余音频数据) |
| props | Any 类型，自定义属性。<font style="color:#DF2A3F;">可空</font> |


### PublishCustomOptions
PublishCustomOptions 类是用于在发布时对 desc、props 这两个参数做修改

| desc | String 类型，轨道描述。<br/>+ 可空，表示不做修改 |
| --- | --- |
| props | Any 类型，自定义属性。<br/>+ 可空，表示不做修改 |
| simulcasts | MutableList<PublishCustomOptions> 类型。<br/>+ <font style="color:#DF2A3F;">目前只有摄像头流存在发布多路流的情况，所以此处用不上这个属性</font> |


## 预设值
目前预设值只有一个 PreOptionMic.def

+ 可以通过直接修改 PreOptionMic.def 获取到的实例的参数值，然后使用。<font style="color:#DF2A3F;">如无特殊需求不建议修改</font>

```kotlin
// 获取默认预设值
val preOpt: PreOptionMic = PreOptionMic.def
// 修改采集配置中的采样率
preOpt.capture.sampleRate = 48000
// 修改发布配置中的编码格式
preOpt.publish.codec = CodecType.AAC
// 使用修改后的预设值
...
```

### PreOptionMic.def
配置如下：

```kotlin
val def = PreOptionMic(
            MicCaptureOptions(
                deviceId = "MicCapDef",
                echoCancellation = true,
                noiseSuppression = true,
                autoGainControl = true,
                channelCount = 1,
                sampleRate = 48000,
                sampleSize = 16,
                latency = 0.0
            ),
            AudioPublishOptions(
                desc = TrackDesc.TRACK_AUDIO.value,
                codec = CodecType.OPUS,
                maxBitrate = 32*1024,
                dtx = true,
                red = true,
                props = null
            )
        )
```

