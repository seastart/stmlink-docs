### CodecType
编码格式枚举

| 枚举名 | 值 |
| --- | --- |
| unknow | 0 |
| H264 | 0x1b |
| H265 | 0x24 |
| AAC | 0x0f |
| OPUS | 0x5355504f |


### DeviceType
设备枚举类型

| 枚举名 | 值 |
| --- | --- |
| unknow | 0 |
| Windows | 1 |
| Android | 2 |
| iOS | 3 |
| Linux | 4 |
| MacOS | 5 |
| WebRTC | 6 |
| Rtmp | 7 |


### LeaveReason
离开原因

| 枚举名 | 值 | 说明 |
| --- | --- | --- |
| Error | -1 | 出错离开 |
| Unknown | 0 | 原因未知 |
| VoluntarilyLeave | 1 | 主动离开 |
| KickOut | 2 | 被踢出 |
| BeReplaced | 3 | 被顶号 |
| HeartbeatTimeout | 4 | 心跳超时 |
| ChannelDestroy | 5 | 频道销毁 |


### TrackKind
轨道类型

| 枚举名 | 值 |
| --- | --- |
| VIDEO | "video" |
| AUDIO | "audio" |


### TrackDesc
默认轨道描述

| 枚举名 | 值 |
| --- | --- |
| TRACK_MAIN | "camera_big" |
| TRACK_SUB | "camera_small" |
| TRACK_SHARE | "screen" |
| TRACK_AUDIO | "mic" |
| TRACK_CUSTOM | "custom" |
| TRACK_UN_KNOW | "unknow" |


### AudioOutputDeviceType
音频输出设备类型

| 枚举名称 | 说明 |
| --- | --- |
| UN_KNOW | 未知 |
| SPEAKER | 扬声器 |
| EARPIECE | 听筒 |
| WIRED_EARPHONE | 有线耳机 |
| BLUETOOTH_HEADSET | 蓝牙耳机 |


