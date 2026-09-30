---
title: "Types"
description: "Structs and JSON for the Windows SRTC C++ SDK: engine options, publishing and capture options, track and user info, device enumeration JSON, custom stream frames, callback JSON (uplink, downlink, audio level, network probe), and the recording layout. Read when filling structs or parsing callbacks."
---

### Engine initialization options (RTCEngineOptions)
```cpp
struct RTCEngineOptions {
    int         enable_log = 1;
    const char* log_path   = nullptr;
};
```

| Parameter name | Parameter type | Description |
| --- | --- | --- |
| enable_log | int | 0 means no SDK log is written at all. Not passing `RTCEngineOptions` to `RTCEngine_Init` (passing nullptr) is equivalent to 0 |
| log_path | const char* | SDK log directory; if empty, "Documents/&lt;app name&gt;/logs/" is used |

Passed to [RTCEngine_Init](/en/rtc/windows/api-reference/IRTCEngine#create-irtcengine).
These two items used to be `enable_stream_log` / `sdk_log_path` on `IRTCSetting`.



### Video track publishing options (RTCVideoPublishOptions)
| Parameter name | Parameter type | Description |
| --- | --- | --- |
| desc | char * | Track description |
| codec | int | Codec type; see [StreamCodec](/en/rtc/windows/enums#codec-type-streamcodec) |
| width | int | Encoding width; -1 matches the capture width automatically |
| height | int | Encoding height; -1 matches the capture height automatically |
| maxFps | int | Maximum frame rate; -1 matches the capture frame rate automatically |
| maxBitrate | int | Maximum bitrate; -1 picks a suitable bitrate automatically |
| simucast | RTCVideoPublishOptions* | Simulcast low streams published alongside the high stream |
| simucast_size | int | Number of simulcast low streams |




### Video track capture options (RTCCameraCaptureOptions)
| Parameter name | Parameter type | Description |
| --- | --- | --- |
| deviceId | char * | Device name |
| width | int | Capture video width; -1 matches automatically |
| height | int | Capture video height; -1 matches automatically |
| maxFps | int | Maximum capture frame rate; -1 matches automatically |


### Screen track capture options (RTCScreenCaptureOptions)
| Parameter name | Parameter type | Description |
| --- | --- | --- |
| deviceId | char * | Device name |
| width | int | Capture screen width; -1 matches automatically |
| height | int | Capture screen height; -1 matches automatically |
| maxFps | int | Maximum capture frame rate |
| showCursor | int | Whether to capture the mouse cursor |
| x | int | x coordinate of the top-left corner of the captured screen area |
| y | int | y coordinate of the top-left corner of the captured screen area |






### Audio track publishing options (RTCAudioPublishOptions)
| Parameter name | Parameter type | Description |
| --- | --- | --- |
| desc | char * | Track description |
| codec | int | Codec type; see [StreamCodec](/en/rtc/windows/enums#codec-type-streamcodec) |
| maxBitrate | int | Maximum bitrate; -1 picks a suitable bitrate automatically |




### Audio track capture options (RTCMicCaptureOptions)
| Parameter name | Parameter type | Description |
| --- | --- | --- |
| deviceId | char * | Device name; default means the default device |
| echoCancellation | int | aec, acoustic echo cancellation |
| noiseSuppression | int | ans, noise suppression |
| autoGainControl | int | agc, automatic gain control |
| channelCount | int | Number of audio channels |
| sampleRate | int | Sample rate |
| sampleSize | int | Sample bit depth |




### Audio track output options (RTCAudioOutputOptions)
| Parameter name | Parameter type | Description |
| --- | --- | --- |
| deviceId | char * | Device name; default means the default device |




### Track info
| Parameter name | Parameter type | Description |
| --- | --- | --- |
| id | char* | Track ID |
| desc | char* | Track description |
| kind | char* | Track kind |
| codec | int | Codec type: [StreamCodec](/en/rtc/windows/enums#codec-type-streamcodec) |
| width | int | Video width |
| height | int | Video height |
| fps | int | Video frame rate |
| angle | int | Video rotation angle |
| bitrate | int | Bitrate |
| sample_rate | int | Audio sample rate |
| track | int | Track number |








### User info
| Parameter name | Parameter type | Description |
| --- | --- | --- |
| channel | string | Channel ID |
| device_id | string | Device ID |
| device_type | int | Device type |
| name | string | Display name |
| props | json | Extended info |
| sid | string | sid |
| stream_tracks | `list<stream_track>` | Collection of tracks |
| uid | string | uid |
| version | string | Version info |


#### Stream info
stream_track

| angle | int | Rotation angle |
| --- | --- | --- |
| bitrate | int | Bitrate |
| codec | int | Codec type |
| desc | string | Track description |
| fps | int | Encoding frame rate |
| height | int | Height |
| id | string | Track ID |
| kind | string | Stream kind |
| sample_rate | int | Audio sample rate |
| track | int | Track number |
| width | int | Width |


### Camera enumeration info
```json
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

| count | int | Number of devices |
| --- | --- | --- |
| equip_list | `list<obj>` | Collection of device info |
| equip_list[0].name | string | Device name |
| equip_list[0].resolutions | `list<obj>` | Collection of device resolutions |
| equip_list[0].resolutions[0].width | int | Resolution width |
| equip_list[0].resolutions[0].height | int | Resolution height |
| equip_list[0].resolutions[0].type | int | Resolution type |


### Microphone/speaker enumeration info
```cpp
{
    "count":1,
    "equip_list":[
        {"name":"麦克风 (Realtek(R) Audio)","type":"default"}   // Device name as reported by Windows; "麦克风" = "Microphone"
    ]
}
```

| count | int | Number of devices |
| --- | --- | --- |
| equip_list | `list<obj>` | Collection of device info |
| equip_list[0].name | string | Device name |
| equip_list[0].type | string | Indicates whether this is the system default device |


### Shared screen enumeration info
```json
{
    "count":1,
    "equip_list":[
        {
            "name":"//display",
            "height":1080,
            "width":1920,
            "x":0,
            "y":0
        }
    ]
}
```

| count | int | Number of devices |
| --- | --- | --- |
| equip_list | `list<obj>` | Collection of device info |
| equip_list[0].name | string | Device name |
| equip_list[0].x | int | x coordinate of the device's top-left corner |
| equip_list[0].y | int | y coordinate of the device's top-left corner |
| equip_list[0].height | int | Device resolution height |
| equip_list[0].width | int | Device resolution width |




### Custom stream receiving struct
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




### Uplink callback
| delay | int | Latency; delay = -1 means the media stream is disconnected |
| --- | --- | --- |
| rate | int | Rate |
| first_lost | double | Packet loss |
| re_lost | double | Packet loss after recovery |
| signal | int | Signal strength, 0 worst, 4 best |


```cpp
{
    "delay":20,
    "rate":0,
    "first_lost":0,
    "re_lost":0,
    "signal":4
}
```

### Downlink callback
| audio | int | Audio packets |
| --- | --- | --- |
| comp | int | Number of recovered packets |
| losf | int | Total packets lost |
| lr1 | double | End-to-end packet loss |
| lr2 | double | Server-to-client packet loss |
| recv | int | Total packets |
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


### Audio level callback
| [0].pow | long | Energy |
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



### Network probe callback
| probe_time | int |  |
| --- | --- | --- |
| stream | int | Whether the media stream is working |
| network | int | Network |
| delay | int | Latency |
| up_data | obj | Collection of uplink data |
| up_data.delay | int | Latency |
| up_data.recv | int | Packets received |
| up_data.miss | int | Out-of-order packets |
| up_data.losf | int | Packets lost |
| up_data.speed | int | Speed |
| up_data.losf2 | double | Packet loss rate |
| up_data.status | int | Overall status, 0 good, 1 fair, 2 poor, 3 very poor |
| up_data.test_data | int | Test rate |
| down_data | obj | Collection of downlink data |
| down_data.delay | int | Latency |
| down_data.recv | int | Packets received |
| down_data.miss | int | Out-of-order packets |
| down_data.losf | int | Packets lost |
| down_data.speed | int | Speed |
| down_data.losf2 | double | Packet loss rate |
| down_data.status | int | Overall status, 0 good, 1 fair, 2 poor, 3 very poor |
| down_data.test_data | int | Test rate |


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

### Recording layout user view configuration
The user view configuration JSON used when setting the recording layout:

```json
{
    "layout": 0,
    "all_member": 20,
    "member": [
        {
            "uid": "__uid__",
            "name": "Alice",
            "track_id": "camera",
            "portrait": "",
            "layout_index": 0,
            "cam_st": 1,
            "mic_st": 1
        }
    ]
}
```

| Parameter | Type | Description |
| --- | --- | --- |
| layout | int | Layout type (0: automatic layout) |
| all_member | int | Total number of users |
| member | list | Array of user configurations |
| member[].uid | string | User ID |
| member[].name | string | User's display name |
| member[].track_id | string | Stream ID or the publishing key (such as camera or screen) |
| member[].portrait | string | Avatar URL |
| member[].layout_index | int | Index of the user's position |
| member[].cam_st | int | Camera on/off state (1: off, 2: on) |
| member[].mic_st | int | Microphone on/off state (1: off, 2: on) |





