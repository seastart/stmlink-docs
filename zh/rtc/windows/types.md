### 视频轨道推流信息（RTCVideoPublishOptions）
| 参数名称 | 参数类型 | 参数说明 |
| --- | --- | --- |
| desc | char * | 轨道描述信息 |
| codec | int | 编码类型[查看](https://www.yuque.com/anyconf/rtcengine/pfzomlthc9l03830#oRuFU) |
| width | int | 编码宽度，-1为自动匹配采集宽度 |
| height | int | 编码高度，-1为自动匹配采集高度 |
| maxFps | int | 最大帧率，-1为自动匹配采集帧率 |
| maxBitrate | int | 最大码率，-1为自动匹配合适码率 |
| simucast | RTCVideoPublishOptions* | 协同辅流 |
| simucast_size | int | 协同辅流个数 |




### 视频轨道采集信息（RTCCameraCaptureOptions）
| 参数名称 | 参数类型 | 参数说明 |
| --- | --- | --- |
| deviceId | char * | 设备名称 |
| width | int | 采集视频宽度，-1为自动匹配 |
| height | int | 采集视频高度，-1为自动匹配 |
| maxFps | int | 采集视频最大帧率，-1为自动匹配 |


### 屏幕轨道采集信息（RTCScreenCaptureOptions）
| 参数名称 | 参数类型 | 参数说明 |
| --- | --- | --- |
| deviceId | char * | 设备名称 |
| width | int | 采集屏幕宽度，-1为自动匹配 |
| height | int | 采集屏幕高度，-1为自动匹配 |
| maxFps | int | 采集视频最大帧率 |
| showCursor | int | 是否采集鼠标 |
| x | int | 采集屏幕左上角点x坐标 |
| y | int | 采集屏幕左上角点y坐标 |






### 音频轨道推流信息（RTCAudioPublishOptions）
| 参数名称 | 参数类型 | 参数说明 |
| --- | --- | --- |
| desc | char * | 轨道描述信息 |
| codec | int | 编码类型[查看](https://www.yuque.com/anyconf/rtcengine/pfzomlthc9l03830#oRuFU) |
| maxBitrate | int | 最大码率，-1为自动匹配合适码率 |




### 音频轨道采集信息（RTCMicCaptureOptions）
| 参数名称 | 参数类型 | 参数说明 |
| --- | --- | --- |
| deviceId | char * | 设备名称，default 为默认设备 |
| echoCancellation | int | aec，回音消除 |
| noiseSuppression | int | ans，噪声抑制 |
| autoGainControl | int | agc，自动增益 |
| channelCount | int | 声道数 |
| sampleRate | int | 采样波特率 |
| sampleSize | int | 采样位深 |




### 音频轨道输出信息（RTCAudioOutputOptions）
| 参数名称 | 参数类型 | 参数说明 |
| --- | --- | --- |
| deviceId | char * | 设备名称，default 为默认设备 |




### 轨道信息
| 参数名称 | 参数类型 | 参数说明 |
| --- | --- | --- |
| id | char* | 轨道id |
| desc | char* | 轨道描述 |
| kind | char* | 轨道种类 |
| codec | int | 编码类型：[StreamCodec](https://www.yuque.com/anyconf/rtcengine/pfzomlthc9l03830#oRuFU) |
| width | int | 视频宽度 |
| height | int | 视频高度 |
| fps | int | 视频帧率 |
| angle | int | 视频流角度 |
| bitrate | int | 码率 |
| sample_rate | int | 音频采样频率 |
| track | int | 轨道号 |








### 用户信息
| 参数名称 | 参数类型 | 参数说明 |
| --- | --- | --- |
| channel | string | 频道id |
| device_id | string | 设备id |
| device_type | int | 设备类型 |
| name | string | 昵称 |
| props | json | 扩展信息 |
| sid | string | sid |
| stream_tracks | list<stream_track> | 流轨道集合 |
| uid | string | uid |
| version | string | 版本信息 |


#### 流信息
stream_track

| angle | int | 角度 |
| --- | --- | --- |
| bitrate | int | 码率 |
| codec | int | 编码类型 |
| desc | string | 流描述 |
| fps | int | 编码帧率 |
| height | int | 高度 |
| id | string | 流id |
| kind | string | 流类型 |
| sample_rate | int | 音频波特率 |
| track | int | 轨道号 |
| width | int | 宽度 |


### 
### 摄像头枚举信息
```cpp
{
    "count":1,
    "equip_list":[
        {"name":"USB HD Webcam",
            "resolutions":[
                {"height":480,"width":640,"type":0},
                {"height":144,"width":176,"type":0},
                {"height":240,"width":320,"type":0},
                {"height":288,"width":352,"type":0},
                {"height":360,"width":640,"type":0},
                {"height":720,"width":1280,"type":0}
            ]
        }
    ]
}
```

| count | int | 设备个数 |
| --- | --- | --- |
| equip_list | list<obj> | 设备信息集合 |
| equip_list[0].name | string | 设备名称 |
| equip_list[0].resolutions | list<obj> | 设备分辨率集合 |
| equip_list[0].resolutions[0].width | int | 设备分辨率宽 |
| equip_list[0].resolutions[0].height | int | 设备分辨率高 |
| equip_list[0].resolutions[0].type | int | 设备分辨率类型 |


### 麦克风/扬声器枚举信息
```cpp
{
    "count":1,
    "equip_list":[
        {"name":"麦克风 (Realtek(R) Audio)","type":"default"}
    ]
}
```

| count | int | 设备个数 |
| --- | --- | --- |
| equip_list | list<obj> | 设备信息集合 |
| equip_list[0].name | string | 设备名称 |
| equip_list[0].type | string | 表示是否为系统默认设备 |


### 共享屏幕枚举信息
```cpp
{
    "count":1,
    "equip_list":[
        {
            "name":"//display"
            "height":1080,
            "width":1920,
            "x":0,
            "y":0
        }
    ]
}
```

| count | int | 设备个数 |
| --- | --- | --- |
| equip_list | list<obj> | 设备信息集合 |
| equip_list[0].name | string | 设备名称 |
| equip_list[0].x | int | 设备左上坐标x |
| equip_list[0].y | int | 设备左上坐标y |
| equip_list[0].height | int | 设备分辨率高 |
| equip_list[0].width | int | 设备分辨率宽 |




### 流数据自定义收流结构体
av_frame_s

| bits | unsigned char* | frame buffer |
| --- | --- | --- |
| bitslen | unsigned int | frame length |
| bitspos | unsigned int | frame start pos within buffer |
| medtype | unsigned int | media type such as audio or video |
| stmtype | unsigned int | stream type such as h264, aac etc |
| frmtype | unsigned int | frame type such as key frame |
| frmmisc | unsigned int | misc character |
| tmscale | unsigned int | time scale for pts and dts |
| frmsequ | unsigned int | frame's sequence |
| pcr | long long | frame pcr |
| pts | long long | frame pts |
| dts | long long | frame dts |
| dur | int | frame duration |
| track | track | frame track |
| arg | void* | |
| language | int | frame language |




### 上行回调
| delay | int | 延迟<font style="color:#E8323C;">,delay = -1 表示流媒体短线</font> |
| --- | --- | --- |
| rate | int | 速率 |
| first_lost | double | 丢包 |
| re_lost | double | 补偿丢包 |
| signal | int | 信号塔能量 0最差，4最好 |


```cpp
{
    "delay":20,
    "rate":0,
    "first_lost":0,
    "re_lost":0,
    "signal":4
}
```

### 下行回调
| audio | int | 音频包 |
| --- | --- | --- |
| comp | int | 补偿包数 |
| losf | int | 总丢包 |
| lr1 | double | 端到端丢包 |
| lr2 | double | 服务到段丢包 |
| recv | int | 总包 |
| userid | std::string | userid |


```cpp
[
    {
        "audio":10,
        "comp":0,
        "losf":0,
        "lr1":0,
        "lr2":0,
        "recv":20,
        "userid":"123131231"
    }
]
```



### 音柱回调
| [0].pow | long | 能量 |
| --- | --- | --- |
| [0].userid | string | uid |
| [0].db | int | db |


```cpp

[
    {
        "pow":10,
        "userid":"12345678",
        "db":-60,
    }
]

```



### 网络检测回调
| probe_time | int |  |
| --- | --- | --- |
| stream | int | 流媒体是否正常 |
| network | int | 网络 |
| delay | int | 延迟 |
| up_data | | 上行数据集合 |
| up_data.delay | int | 延迟 |
| up_data.recv | int | 接收包数 |
| up_data.miss | int | 错续包数 |
| up_data.losf | int | 丢包数 |
| up_data.speed | int | 速度 |
| up_data.losf2 | double | 丢包率 |
| up_data.status | int | 综合状态值，0 好，1不佳，2 较差，3极差 |
| up_data.test_data | int | 测试速率 |
| down_data | int | 下行数据集合 |
| down_data.delay | int | 延迟 |
| down_data.recv | int | 接收包数 |
| down_data.miss | int | 错续包数 |
| down_data.losf | int | 丢包数 |
| down_data.speed | int | 速度 |
| down_data.losf2 | double | 丢包率 |
| down_data.status | int | 综合状态值，0 好，1不佳，2 较差，3极差 |
| down_data.test_data | int | 测试速率 |


```cpp
{
    "probe_time":10,
    "stream":1,
    "network":1,
    "delay":100,
    "up_data":{
        "delay":100,
        "recv":10000,
        "miss":0,
        "losf":0,
        "speed":100,
        "losf2":0,
        "status":0,
        "test_data":1024
    },
    "down_data":{
        "delay":100,
        "recv":10000,
        "miss":0,
        "losf":0,
        "speed":100,
        "losf2":0,
        "status":0,
        "test_data":1024
    }
}
```



