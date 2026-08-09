---
title: "类型定义"
description: "Android 音视频 SDK 的频道、用户、轨道与摄像头能力等数据结构字段说明"
---

## ChannelInfo

作用说明：频道信息数据，描述频道基础属性、容量限制及扩展字段。

| 属性名称 | 数据类型 | 说明 |
| --- | --- | --- |
| appId | String? | 应用 ID。 |
| channel | String | 频道号。 |
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
| stream_tracks | `ArrayList<TrackInfo>?` | 正在推流的轨道信息集合。 |
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
| fallback_ids | `MutableList<String>?` | 当前层可降级到的更低层 Track ID 列表，不含自己，按画质从高到低排列。 |
| variant | Boolean? | 是否为 simulcast 副层；主层通常为 `false`。 |
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

## ActiveSpeakerInfo

作用说明：活跃说话人信息，由 [`RTCMediaEvent.onActiveSpeakersChanged`](/zh/rtc/android/api-reference/RTCMediaEvent) 回调。

| 属性名称 | 数据类型 | 说明 |
| --- | --- | --- |
| uid | String | 说话用户 uid。 |
| trackId | String | 音频轨道 trackId。 |
| level | Double | 服务端量化后的音量强度。 |

## NetworkQualityChange

作用说明：网络质量档位变化事件，由 [`RTCMediaEvent.onNetworkQualityChanged`](/zh/rtc/android/api-reference/RTCMediaEvent) 回调。上行、下行各自独立触发，一次回调只表示一个方向的变化。

| 属性名称 | 数据类型 | 说明 |
| --- | --- | --- |
| direction | QualityDirection | 发生变化的方向（`UPLINK` / `DOWNLINK`）。枚举见 [枚举类型](/zh/rtc/android/enums)。 |
| previousLevel | String | 变化前的等级；首次（`INITIAL`）时为空串。 |
| currentLevel | String | 变化后的当前等级（`excellent` / `good` / `poor` / `lost`）。 |
| trend | QualityTrend | 变化趋势（`INITIAL` / `DEGRADED` / `RECOVERED`）。枚举见 [枚举类型](/zh/rtc/android/enums)。 |
| report | MediaMetric.QualityReport | 触发本次事件时的完整质量报告快照。字段见 [媒体质量](/zh/rtc/android/media-quality)。 |

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

## MicDeviceCapability

作用说明：麦克风输入设备能力信息，由 `RTCEngine.getMicDevices()`、`LocalMicTrack.getMicDevices()` 和 [`RTCMicDeviceEvent.onMicDeviceListChanged`](/zh/rtc/android/api-reference/RTCMicDeviceEvent) 返回。

| 属性名称 | 数据类型 | 说明 |
| --- | --- | --- |
| deviceId | String | 当前系统分配的 `AudioDeviceInfo.id` 字符串，只在本次设备连接期间有效，可用于 `switchMicDevice(...)`。 |
| key | MicDeviceKey | 跨设备重新插拔时用于匹配的持久键。 |
| type | Int | `AudioDeviceInfo.TYPE_*` 输入设备类型。 |
| displayName | String? | SDK 生成的展示名称。 |
| productName | String? | 系统报告的设备产品名。 |
| address | String? | 蓝牙地址、USB 路径等设备地址，可能为空。 |
| sampleRates | List\<Int\> | 设备报告支持的采样率列表。 |
| channelCounts | List\<Int\> | 设备报告支持的声道数列表。 |
| isDefault | Boolean | 是否为系统当前默认输入设备。 |
| isCurrent | Boolean | 是否为 SDK 麦克风采集模块当前使用的设备。 |

## MicDeviceKey

作用说明：麦克风设备的持久匹配键。系统 `deviceId` 在重新插拔后可能变化，SDK 使用 `type + address + productName` 重新匹配设备。

| 属性名称 | 数据类型 | 说明 |
| --- | --- | --- |
| type | Int | `AudioDeviceInfo.TYPE_*` 输入设备类型。 |
| address | String? | 设备地址，可能为空。 |
| productName | String? | 设备产品名，可能为空。 |

