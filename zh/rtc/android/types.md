---
title: "类型定义"
description: "Android SRTC 音视频 SDK 信息数据类型定义"
---

## ChannelInfo

作用说明：频道信息数据，描述频道基础属性、容量限制及扩展字段。

| 属性名称 | 数据类型 | 说明 |
| --- | --- | --- |
| appId | String? | 应用 ID。 |
| channel | String? | 频道号。 |
| created_at | Long | 频道创建时间。 |
| updated_at | Long | 频道更新时间。 |
| link_id | Int | 流媒体连接 ID。 |
| max_user | Int | 频道最大用户数。 |
| max_audio | Int | 频道音频最大转发数。 |
| max_peer | Int | 频道用户最大可转发数。 |
| max_video | Int | 频道用户视频最大可转发数。 |
| props | JsonElement? | 自定义属性。 |

## UserInfo

作用说明：用户信息数据，描述成员身份、终端信息、入会状态与其发布轨道信息。

| 属性名称 | 数据类型 | 说明 |
| --- | --- | --- |
| app_id | String? | 应用 ID。 |
| uid | String | 三方平台用户 ID。 |
| sid | String? | 会话 ID。 |
| name | String? | 用户名。 |
| device_type | Int? | 设备类型。 |
| device_id | String? | 终端唯一编号。 |
| sdk_version | String? | SDK 版本号。 |
| version | String? | 版本号。 |
| props | JsonElement? | 自定义属性。 |
| netid | String? | 网络号。 |
| sgid | String? | 分组号。 |
| channel | String? | 频道号。 |
| is_audience | Boolean | 是否观众。 |
| join_at | Long | 加入时间。 |
| updated_at | Long | 更新时间。 |
| leave_at | Long | 离开时间。 |
| stream_tracks | ArrayList<TrackInfo>? | 正在推流的轨道信息集合。 |
| link_id | Int | 流媒体连接 ID。 |
| session_key | String? | 流媒体连接 key。 |
| upload_id | String? | 当前所属流媒体服务 ID。 |

## TrackInfo

作用说明：轨道信息数据，描述音视频流的标识、媒体参数与扩展字段。

| 属性名称 | 数据类型 | 说明 |
| --- | --- | --- |
| id | String | 流 ID。 |
| desc | String | 流描述。 |
| kind | String | 流类型（`video` / `audio`）。 |
| codec | Int | 编码类型。 |
| width | Int | 视频宽度。 |
| height | Int | 视频高度。 |
| fps | Int | 视频帧率。 |
| angle | Int | 视频角度。 |
| bitrate | Int | 码率。 |
| sample_rate | Int | 音频采样率。 |
| track | Int | 流媒体轨道（0~6）。 |
| props | JsonElement? | 自定义属性。 |

## UserTrackDesc

作用说明：用户与轨道描述的组合键数据，常用于按用户轨道定位统计或流信息。

| 属性名称 | 数据类型 | 说明 |
| --- | --- | --- |
| uid | String | 用户 UID。 |
| trackDesc | String | 轨道描述。 |

## VolumeInfo

作用说明：音量数据，描述用户当前音频能量信息。

| 属性名称 | 数据类型 | 说明 |
| --- | --- | --- |
| uid | String | 用户 UID。 |
| db | Int | 音频能量（分贝）。 |

## CustomVideoOptions

作用说明：自定义编码视频流参数，用于描述外部输入视频流的编码信息与媒体属性。

| 属性名称 | 数据类型 | 说明 |
| --- | --- | --- |
| id | String | 流 ID。 |
| codec | CodecType? | 编码格式。 |
| width | Int? | 视频宽度。 |
| height | Int? | 视频高度。 |
| maxFps | Int? | 最大帧率。 |
| angle | Int? | 视频角度。 |
| maxBitrate | Int? | 最大码率。 |
| track | Int? | 流媒体轨道号（`0~6`）。 |
| props | JsonElement? | 自定义属性。 |

## ActiveSpeakerInfo

作用说明：活跃说话人信息，由 [`RTCMediaEvent.onActiveSpeakersChanged`](/zh/rtc/android/api-reference/RTCMediaEvent) 回调。

| 属性名称 | 数据类型 | 说明 |
| --- | --- | --- |
| uid | String | 说话用户 uid。 |
| trackId | String | 音频轨道 trackId。 |
| level | Double | 服务端量化后的音量强度。 |

## CameraDeviceCapability

作用说明：摄像头设备能力信息，由 [`RTCEngine.getCameraDevices`](/zh/rtc/android/api-reference/RTCEngine) 与 [`RTCMediaEvent.onCameraDeviceListChanged`](/zh/rtc/android/api-reference/RTCMediaEvent) 返回。

| 属性名称 | 数据类型 | 说明 |
| --- | --- | --- |
| cameraId | String | Camera2 原生摄像头 id，可用于 `LocalCameraTrack.switchCameraDevice`。 |
| position | CamraPosition | SDK 统一摄像头方向（`FRONT` / `BACK` / `External`）。 |
| displayName | String? | SDK 生成的默认展示名。 |
| sensorOrientation | Int | Camera2 传感器安装方向。 |
| hardwareLevel | Int | Camera2 硬件能力等级。 |
| formats | List\<CameraFormatCapability\> | 当前设备支持的 YUV 采集格式列表。 |
| controls | CameraControlCapability | 当前设备支持的控制能力。 |

## CameraFormatCapability

作用说明：摄像头采集格式能力。

| 属性名称 | 数据类型 | 说明 |
| --- | --- | --- |
| width | Int | 采集宽度。 |
| height | Int | 采集高度。 |
| minFps | Int | AE fps range 最小帧率。 |
| maxFps | Int | AE fps range 最大帧率。 |

## CameraControlCapability

作用说明：摄像头控制能力。

| 属性名称 | 数据类型 | 说明 |
| --- | --- | --- |
| supportsTorch | Boolean | 是否支持闪光灯或补光灯。 |
| supportsZoom | Boolean | 是否支持变焦能力。 |
| supportsFocus | Boolean | 是否支持对焦控制能力。 |
| supportsExposure | Boolean | 是否支持曝光补偿能力。 |
| supportsWhiteBalance | Boolean | 是否支持白平衡模式控制能力。 |

