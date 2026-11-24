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

作用说明：网络质量档位事件，由 [`RTCMediaEvent.onNetworkQualityChanged`](/zh/rtc/android/api-reference/RTCMediaEvent) 回调。每份服务端质量报告都为上行、下行各回调一次（不做去抖），一次回调只表示一个方向。

| 属性名称 | 数据类型 | 说明 |
| --- | --- | --- |
| direction | QualityDirection | 发生变化的方向（`UPLINK` / `DOWNLINK`）。枚举见 [枚举类型](/zh/rtc/android/enums)。 |
| previousLevel | String | 上一次回调的等级；首次（`INITIAL`）时为空串。 |
| currentLevel | String | 本次等级（`excellent` / `good` / `poor` / `lost`）。 |
| trend | QualityTrend | 与上一次相比的趋势（`INITIAL` / `DEGRADED` / `RECOVERED` / `STABLE`）。枚举见 [枚举类型](/zh/rtc/android/enums)。 |
| report | ServerQualityReport | 触发本次事件时的 FY 服务端质量报告。字段见 [媒体质量](/zh/rtc/android/media-quality)。 |

## CameraDeviceCapability

作用说明：摄像头设备能力信息，由 [`RTCEngine.getCameraDevices`](/zh/rtc/android/api-reference/RTCEngine) 与 [`RTCCameraDeviceEvent.onCameraDeviceListChanged`](/zh/rtc/android/api-reference/RTCCameraDeviceEvent) 返回。

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

## YuvFormat

包路径：`cn.seastart.rtc.media.format.YuvFormat`。用于标识原始视频帧的像素布局，不代表每个输入接口都支持所有格式。

| 常量 | 值 | 像素布局 |
| --- | --- | --- |
| `NV21` | `17` | Y 平面 + VU 交错平面。 |
| `NV12` | `19` | Y 平面 + UV 交错平面。 |
| `I420` | `808596553` | Y、U、V 三平面。 |
| `YV12` | `842094169` | Y、V、U 三平面。 |
| `YUY2` | `20` | YUYV 打包格式。 |

屏幕原始帧回调与 `LocalCustomVideoTrack.inputData` 使用 I420。渲染控件的 `updateFrame` 支持 I420、NV12、NV21，不支持 YV12、YUY2。

## AudioCaptureProcessor

包路径：`cn.seastart.rtc.audio.AudioCaptureProcessor`，自 2.0.39 起提供。麦克风采集处理器，通过 `RTCEngine.setAudioCaptureProcessor(...)` 挂载，在 SDK 采集线程上原地处理每一帧 PCM，处理后再分发给所有频道。

| 成员 | 说明 |
| --- | --- |
| `audioProcessing: AudioProcessingConstraints?` | 对自带 3A 的要求，默认 `null`（不干预）。 |
| `initialize(sampleRate: Int, channelCount: Int)` | 采集格式确定时调用（每次采集会话启动，含设备切换、路由变化后的重建；以及采集中挂上处理器时），须快速返回。 |
| `process(data: ByteArray, offset: Int, length: Int)` | 原地处理一帧 16bit 小端 PCM（交错声道），默认 48kHz 单声道 10ms 即 960 字节。每 10ms 同步调用一次，须在几毫秒内返回；返回后缓冲会被复用，不要持有 `data`。抛出的异常会被 SDK 捕获，该帧按原样发送。 |
| `release()` | 处理器被替换或清空时调用，之后不会再收到 `process`。 |

## AudioProcessingConstraints

包路径：`cn.seastart.rtc.audio.AudioProcessingConstraints`，自 2.0.39 起提供。采集处理器对自带音频前处理（3A）的要求，与 Web、Swift SDK 的同名类型含义一致。

| 属性名称 | 数据类型 | 说明 |
| --- | --- | --- |
| noiseSuppression | Boolean? | 降噪。`false` 时关闭系统与 WebRTC 自带降噪。 |
| echoCancellation | Boolean? | 回声消除，Android 暂不处理，保持 SDK 默认。 |
| autoGainControl | Boolean? | 自动增益，Android 暂不处理，保持 SDK 默认。 |

取值 `false` 表示要求关闭；`true` 或 `null` 表示不干预，沿用 SDK 默认配置。

## NetworkCheckOptions

包路径：`cn.seastart.rtc.netcheck.NetworkCheckOptions`，自 2.0.40 起提供。[会前网络检测](/zh/rtc/android/api-reference/RTCEngine#networkcheck-options-listener) 的入参。服务器信息二选一：直接给 `appId` + `serverUrl`，或给一个入会 / IM token 由 SDK 解出；两种都给时以 `appId` / `serverUrl` 为准。检测本身不使用 token 鉴权。

| 属性名称 | 数据类型 | 说明 |
| --- | --- | --- |
| appId | String? | 应用 ID。 |
| serverUrl | String? | SDK 接口前缀，即 token 中的 `client_api`（如 `https://host/client/`）。 |
| token | String? | 可选，入会或 IM token，仅用于解出 `appId` 与 `serverUrl`。 |
| timeoutMs | Int | 单项检测超时（毫秒），默认 `3000`。 |

## NetworkCheckItem

包路径：`cn.seastart.rtc.netcheck.NetworkCheckItem`，自 2.0.40 起提供。单项检测结果。

| 属性名称 | 数据类型 | 说明 |
| --- | --- | --- |
| id | String | 检测项，取值见 `NetworkCheckItemId`。 |
| status | String | 检测状态：`pass` / `warning` / `fail` / `skipped` / `unsupported`，见 `NetworkCheckStatus`。 |
| reason | String | 机器可读的原因码，`pass` 时为空串，取值见 `NetworkCheckReason`。 |
| message | String | 可直接展示给用户的中文说明。 |
| costMs | Long | 本项耗时（毫秒）。 |
| data | Map\<String, Any?\> | 本项测量值，如 `connectivity` 的 `netType`、`mtu` 的 `maxSize`、`dns` 的 `hosts`、`server` 的 `api` / `signal` / `media` 子检查（各含 `ok`、`status`、`reason`、`rttMs`）。 |

## NetworkCheckResult

包路径：`cn.seastart.rtc.netcheck.NetworkCheckResult`，自 2.0.40 起提供。整体检测结果。

| 属性名称 | 数据类型 | 说明 |
| --- | --- | --- |
| status | String | 汇总状态：有 `fail` 即 `fail`；无 `fail` 但有 `warning` 即 `warning`；否则 `ok`。 |
| items | List\<NetworkCheckItem\> | 固定 5 项，顺序为 `permission`、`connectivity`、`mtu`、`dns`、`server`。 |
| costMs | Long | 总耗时（毫秒）。 |

## 网络检测常量

自 2.0.40 起提供，均在 `cn.seastart.rtc.netcheck` 包下。

`NetworkCheckItemId`（检测项）：

| 常量 | 值 | 说明 |
| --- | --- | --- |
| `PERMISSION` | `permission` | 网络权限 |
| `CONNECTIVITY` | `connectivity` | 网络连接 |
| `MTU` | `mtu` | 最大传输单元 |
| `DNS` | `dns` | 域名解析 |
| `SERVER` | `server` | 服务器连接（接口 / 信令 / 媒体） |

`NetworkCheckStatus`（检测状态）：

| 常量 | 值 | 说明 |
| --- | --- | --- |
| `OK` | `ok` | 汇总：全部正常 |
| `PASS` | `pass` | 单项：通过 |
| `WARNING` | `warning` | 有风险但可用 |
| `FAIL` | `fail` | 失败 |
| `SKIPPED` | `skipped` | 单项：无需检测 |
| `UNSUPPORTED` | `unsupported` | 单项：当前设备不支持 |

`NetworkCheckReason`（原因码）：

| 常量 | 值 | 说明 |
| --- | --- | --- |
| `NO_PERMISSION` | `no_permission` | 未授予网络权限 |
| `CELLULAR_RESTRICTED` | `cellular_restricted` | 系统限制了后台或蜂窝数据 |
| `OFFLINE` | `offline` | 当前没有网络连接 |
| `MTU_TOO_SMALL` | `mtu_too_small` | 1200 字节探测包不通，但媒体服务器可达 |
| `UDP_BLOCKED` | `udp_blocked` | 媒体 UDP 不通 |
| `DNS_FAILED` | `dns_failed` | 域名解析失败 |
| `API_UNREACHABLE` | `api_unreachable` | 检测信息接口不可达（含服务端未支持会前网络检测） |
| `SERVER_INFO_UNAVAILABLE` | `server_info_unavailable` | 拿不到服务端检测信息，依赖它的检测记 `skipped` |
| `SIGNAL_UNREACHABLE` | `signal_unreachable` | 信令服务器不可达 |
| `VENDOR_NOT_SUPPORTED` | `vendor_not_supported` | 当前流媒体引擎无需进行媒体检测 |
| `MEDIA_UNAVAILABLE` | `media_unavailable` | 服务端没有可用的媒体节点 |
| `DF_NOT_SUPPORTED` | `df_not_supported` | 系统不允许设置不分片，MTU 检测不可用 |
