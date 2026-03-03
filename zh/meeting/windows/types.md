---
title: "类型定义"
description: "Windows SMeeting 会议 SDK 完整类型与结构体定义"
---

## 结构体类型
### IRTCSetting
会议默认参数设置

该参数是一些可配置参数的设置和获取修改的。

| **属性名称** | **描述** |
| --- | --- |
| stream_model | 【字段含义】流媒体模式<br/>【特别说明】1：画布，1：纯收发流，2：多路流<br/>【推荐取值】默认值：1 |
| sdk_log_path | 【字段含义】日志目录<br/>【推荐取值】默认值：文档\{appname}\ |
| stat_interval | 【字段含义】会议上下行信息数据回调间隔，0为不回调<br/>【推荐取值】默认值：0 |
| speaker_interval | 【字段含义】音柱回调间隔，0为不回调<br/>【推荐取值】默认值：0 |
| enable_stream_log | 【字段含义】流媒体日志存储<br/>【推荐取值】默认值：false |
| enable_audio_record | 【字段含义】开启音频录音<br/>【推荐取值】默认值：false |
| mcu_track | 【字段含义】mcu录制轨道<br/>【特别说明】1 |
| den_model | 【字段含义】会议降噪参数<br/>【特别说明】0：声学，1：ai，2：ai+声学，3关闭。<br/>【推荐取值】默认值：2 |
| simple | 【字段含义】是否使用简易方式<br/>【推荐取值】默认值：false |
| opus | 【字段含义】是否使用opus传输音频<br/>【推荐取值】默认值：YES |




### RTCTrackInfo
轨道信息

该参数是取流和推流轨道信息，基本参数

| **属性名称** | **描述** |
| --- | --- |
| id | 【字段含义】轨道id |
| desc | 【字段含义】轨道描述信息 |
| kind | 【字段含义】音视频种类 |
| codec | 【字段含义】编码格式 |
| width | 【字段含义】宽度 |
| height | 【字段含义】高度 |
| fps | 【字段含义】帧率 |
| angle | 【字段含义】视频角度 |
| bitrate | 【字段含义】码率 |
| sample_rate | 【字段含义】波特率 |
| track | 【字段含义】轨道号 |


### RTCMicCaptureOptions
麦克风采集参数配置

| **属性名称** | **描述** |
| --- | --- |
| deviceId | 【字段含义】设备名称 |
| echoCancellation | 【字段含义】 |
| noiseSuppression | 【字段含义】 |
| autoGainControl | 【字段含义】 |
| channelCount | 【字段含义】声道数 |
| sampleRate | 【字段含义】采样率 |
| sampleSize | 【字段含义】位深 |


### RTCAudioOutputOptions
扬声器播放参数配置

| **属性名称** | **描述** |
| :--- | --- |
| deviceId | 【字段含义】设备名称 |


### RTCAudioPublishOptions
音频推流参数设置

| **属性名称** | **描述** |
| --- | --- |
| desc | 【字段含义】轨道描述信息 |
| codec | 【字段含义】编码类型 |
| maxBitrate | 【字段含义】最大码率 |


### RTCCameraCaptureOptions
视频采集参数配置

| **属性名称** | **描述** |
| --- | --- |
| deviceId | 【字段含义】设备昵称 |
| width | 【字段含义】宽度 |
| height | 【字段含义】高度 |
| maxFps | 【字段含义】采集帧率 |


### RTCScreenCaptureOptions
屏幕采集参数配置

| **属性名称** | **描述** |
| --- | --- |
| deviceId | 【字段含义】设备id |
| width | 【字段含义】宽度 |
| height | 【字段含义】高度 |
| maxFps | 【字段含义】最大帧率 |
| showCursor | 【字段含义】是否显示光标 |
| x | 【字段含义】x |
| y | 【字段含义】y |


### RTCVideoPublishOptions
视频推流参数配置

| **属性名称** | **描述** |
| --- | --- |
| desc | 【字段含义】推流描述信息 |
| codec | 【字段含义】编码类型 |
| width | 【字段含义】宽度 |
| height | 【字段含义】高度 |
| maxFps | 【字段含义】最大码率 |
| maxBitrate | 【字段含义】最大帧率 |
| simucast | 【字段含义】辅流对象 |
| simucast_size | 【字段含义】辅流数量 |


