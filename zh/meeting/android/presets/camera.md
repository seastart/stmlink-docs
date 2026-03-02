### PreOptionCamera 
PreOptionCamera 类中包含 CameraCaptureOptions、VideoPublishOptions 两个属性

| CameraCaptureOptions | 摄像头采集配置参数 |
| --- | --- |
| VideoPublishOptions | 视频流发布配置参数 |


### CameraCaptureOptions
CameraCaptureOptions 类主要用于配置摄像头采集参数，具体参数如下

| deviceId | String 类型，设备 id |
| --- | --- |
| position | CamraPosition 类型，摄像头位置。<font style="color:#DF2A3F;">手机专用</font><br/>CamraPosition.FRONT：前置摄像头<br/>CamraPosition.BACK：后置摄像头 |
| facingMode | CameraFacingMode 类型，摄像头位置。<font style="color:#DF2A3F;">webrtc 专用</font><br/>CameraFacingMode.USER：朝向用户<br/>CameraFacingMode.ENVIRONMENT：朝向环境<br/>CameraFacingMode.LEFT：朝向左边<br/>CameraFacingMode.RIGHT：朝向右边 |
| width | Int 类型，预览画面宽 |
| height | Int 类型，预览画面高 |
| maxFps | Int 类型，最大帧率 |


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
| simulcasts | MutableList<VideoPublishOptions> 类型。<br/>+ 摄像头流可以发布两条视频流，一条主流、一条辅流，可以在这里对辅流进行配置<br/>+ 目前只可以配置一条辅流，所以该列表的大小只能为 1。<br/>+ <font style="color:#DF2A3F;">可空，空表示不配置辅流。</font> |


### PublishCustomOptions
PublishCustomOptions 类是用于在发布时对 desc、props 这两个参数做修改

| desc | String 类型，轨道描述。<br/>+ 可空，表示不做修改 |
| --- | --- |
| props | Any 类型，自定义属性。<br/>+ 可空，表示不做修改 |
| simulcasts | MutableList<PublishCustomOptions> 类型。<br/>+ 因为摄像头流可能存在主流、辅流两路流，这里就是用于对辅流参数做修改的<br/>+ 该列表大小只能为 1，因为最多只能配置一条辅流。<br/>+ 可空，表示不修改辅流配置 |


## 预设值
目前预设值只有一个 PreOptionCamera.def

+ 可以通过直接修改 PreOptionCamera.def 获取到的实例的参数值，然后使用。<font style="color:#DF2A3F;">如无特殊需求不建议修改</font>

```kotlin
// 获取默认预设值
val preOpt: PreOptionCamera = PreOptionCamera.get_1080P()
// 修改采集配置中的摄像头位置
preOpt.capture.position = CameraCaptureOptions.CamraPosition.BACK
// 修改发布配置中的编码格式
preOpt.publish.codec = CodecType.H265
// 使用修改后的预设值
...
```

### PreOptionCamera.def
配置如下：

```kotlin
val _1080P: PreOptionCamera = PreOptionCamera(
    CameraCaptureOptions(
        deviceId = "cameraCapMain",
        position = CameraCaptureOptions.CamraPosition.FRONT,
        facingMode = CameraCaptureOptions.CameraFacingMode.USER,
        width = 1920,
        height = 1080,
        maxFps = 30
    ),
    VideoPublishOptions(
        desc = TrackDesc.TRACK_MAIN.value,
        codec = CodecType.H264,
        maxBitrate = 2000 * 1024,
        width = 1920,
        height = 1080,
        maxFps = 25,
        props = null,
        simulcasts = mutableListOf(
            VideoPublishOptions(
                desc = TrackDesc.TRACK_SUB.value,
                codec = CodecType.H264,
                maxBitrate = 128 * 1024,
                width = 320,
                height = 180,
                maxFps = 25,
                props = null,
                simulcasts = null
            )
        )
    )
)

val _720P: PreOptionCamera = PreOptionCamera(
    CameraCaptureOptions(
        deviceId = "cameraCapMain",
        position = CameraCaptureOptions.CamraPosition.FRONT,
        facingMode = CameraCaptureOptions.CameraFacingMode.USER,
        width = 1280,
        height = 720,
        maxFps = 30
    ),
    VideoPublishOptions(
        desc = TrackDesc.TRACK_MAIN.value,
        codec = CodecType.H264,
        maxBitrate = 900 * 1024,
        width = 1280,
        height = 720,
        maxFps = 25,
        props = null,
        simulcasts = mutableListOf(
            VideoPublishOptions(
                desc = TrackDesc.TRACK_SUB.value,
                codec = CodecType.H264,
                maxBitrate = 128 * 1024,
                width = 320,
                height = 180,
                maxFps = 25,
                props = null,
                simulcasts = null
            )
        )
    )
)

val _480P: PreOptionCamera = PreOptionCamera(
    CameraCaptureOptions(
        deviceId = "cameraCapMain",
        position = CameraCaptureOptions.CamraPosition.FRONT,
        facingMode = CameraCaptureOptions.CameraFacingMode.USER,
        width = 640,
        height = 480,
        maxFps = 30
    ),
    VideoPublishOptions(
        desc = TrackDesc.TRACK_MAIN.value,
        codec = CodecType.H264,
        maxBitrate = 512 * 1024,
        width = 640,
        height = 480,
        maxFps = 25,
        props = null,
        simulcasts = mutableListOf(
            VideoPublishOptions(
                desc = TrackDesc.TRACK_SUB.value,
                codec = CodecType.H264,
                maxBitrate = 128 * 1024,
                width = 320,
                height = 180,
                maxFps = 25,
                props = null,
                simulcasts = null
            )
        )
    )
)

val _180P: PreOptionCamera = PreOptionCamera(
    CameraCaptureOptions(
        deviceId = "cameraCapMain",
        position = CameraCaptureOptions.CamraPosition.FRONT,
        facingMode = CameraCaptureOptions.CameraFacingMode.USER,
        width = 320,
        height = 180,
        maxFps = 30
    ),
    VideoPublishOptions(
        desc = TrackDesc.TRACK_MAIN.value,
        codec = CodecType.H264,
        maxBitrate = 128 * 1024,
        width = 320,
        height = 180,
        maxFps = 25,
        props = null,
        simulcasts = mutableListOf(
            VideoPublishOptions(
                desc = TrackDesc.TRACK_SUB.value,
                codec = CodecType.H264,
                maxBitrate = 128 * 1024,
                width = 320,
                height = 180,
                maxFps = 25,
                props = null,
                simulcasts = null
            )
        )
    )
)
```

