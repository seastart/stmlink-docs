### RTCOptions
RTC 配置参数

| 属性名称 | 数据类型 | 说明 |
| --- | --- | --- |
| deviceId | String | 设备 id |
| deviceType | Int | 设备类型 |
| deviceDesc | String | 设备描述 |
| logPath | String | 日志存储路径 |
| enableLocalLog | Boolean | 是否存储本地日志 |
| version | String | 上层版本信息 |


### RTCMediaOptions
流媒体全局配置参数

| 属性名称 | 数据类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| audioChannels | Int  | 1 | 音频采样通道 |
| audioSamplerate | Int  | 48000 | 音频采样率 |
| audioBitrate | Int  |  32 * 1024 | 音频码率 |
| audioCodec | CodecType 枚举类型 | CodecType.OPUS | 音频编码格式 |
| videoWidthMain | Int  | 640 | 视频分辨率宽度 |
| videoHeightMain | Int  | 480 | 视频分辨率高度 |
| videoBitrateMain | Int  | 512 * 1024 | 视频码率 |
| fpsMain | Int  | 25 | 视频帧率 |
| sft | Boolean  | true | 是否使用移频 |
| agc | Int  | 10000 | 音频 agc |
| aec | Int  | 12 | 音频 aec |
| xdelay | Boolean  | true | 是否开启延时自适应 |
| xbitrate | Int  |  5 | 码率自适应 |
| defFrontCamera | Boolean  | false | 默认打开的摄像头位置：前置 / 后置 |
| defMcuTrack | Int  | 0 | mcu默认轨道 |
| plc | Int  | 2 | 延迟抖动 |
| hwDecoder | Boolean  | true | 是否优先硬解码 |
| hwEncoder | Boolean  | true | 是否优先硬编码 |
| isDaulStream | Boolean  | true | 是否双流 |
| statInterval | Int  | 1000 | 网络统计间隔 ms |
| statAudioInterval | Int  | 500 | 音频统计间隔 ms |


### PublishCustomOptions
自定义参数配置

+ <font style="color:#DF2A3F;">PS：只有摄像头流可以设置辅流的自定义发布参数，但只能设置一路且不允许嵌套设置。</font>

| 属性名称 | 数据类型 | 说明 |
| --- | --- | --- |
| desc | String | 轨道描述<br/>默认描述：camera_big、camera_small、screen、mic、custom |
| props | Any | 扩展信息 |
| simulcasts | MutableList<PublishCustomOptions> | 辅流的自定义发布参数 |


### ChannelInfo
频道信息

| 属性名称 | 数据类型 | 说明 |
| --- | --- | --- |
| appId | String  | APP ID |
| channel | String  | 频道号 |
| created_at | Long  | 创建时间 |
| updated_at | Long | 更新时间 |
| link_id | Int  | 流媒体连接ID |
| max_user | Int  | 频道最大用户数 |
| max_audio | Int  | 频道音频最大转发数 |
| max_peer | Int  | 频道用户最大可转发数 |
| max_video | Int | 频道用户视频最大可转发数 |
| props | JsonElement  | 扩展属性 |


### UserInfo
用户信息

| 属性名称 | 数据类型 | 说明 |
| --- | --- | --- |
| app_id | String | app ID |
| uid | String | 三方平台用户ID |
| sid | String | 会话ID |
| name | String | 用户名 |
| device_type | Int | 设备类型：<br/>android：2 |
| device_id | String  | 终端唯一编号 |
| sdk_version | String  | sdk版本号 |
| version | String | 版本号 |
| props | JsonElement  | 自定义属性 |
| netid | String | 网络号 |
| sgid | String | 分组号 |
| channel | String | 频道号 |
| is_audience | Boolean | 是否观众 |
| join_at | Long | 加入时间 |
| updated_at | Long | 更新时间 |
| leave_at | Long | 离开时间 |
| stream_tracks | ArrayList<TrackInfo> | 正在推流的码流信息集合 |
| link_id | Int | 流媒体连接ID |
| session_key | String | 流媒体连接key |
| upload_id | String | 当前所属流媒体服务ID |


### TrackInfo
轨道信息

| 属性名称 | 数据类型 | 说明 |
| --- | --- | --- |
| id | String | 轨道 id |
| desc | String | 轨道描述 |
| kind | String | 轨道类型：video / audio |
| codec | Int | 编码类型：<br/>unknow：0<br/>H264：0x1b<br/>H265：0x24<br/>AAC：0x0f<br/>OPUS：0x5355504f |
| width | Int | 视频宽度 |
| height | Int  | 视频高度 |
| fps | Int  | 视频帧率 |
| angle | Int  | angle |
| bitrate | Int | bitrate |
| sample_rate | Int | 音频采样率 |
| track | Int | 轨道号 （0-6） |
| props | JsonElement | 自定义属性 |


### UserTrackDesc
用户、轨道封装类

| uid | String 类型，用户 id |
| --- | --- |
| trackDesc | String 类型，轨道描述 |


### VolumeInfo
音量信息

| 属性名称 | 数据类型 | 说明 |
| --- | --- | --- |
| uid | String | 用于 id |
| db | Int | 音频能量，分贝数 |


