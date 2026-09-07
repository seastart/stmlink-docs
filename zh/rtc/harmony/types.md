---
title: "类型定义"
description: "SRTC HarmonyOS SDK 的枚举、接口与预设函数完整清单"
---

本页是类型参考。所有类型都从 `srtc` 直接导出：

```typescript
import { Codec, TrackKind, JoinOptions, TrackInfo /* ... */ } from 'srtc';
```

---

## 枚举

### `Codec`

编解码格式。数值是国际标准的编码标识，与其它端一致。

| 成员 | 值 | 说明 |
| --- | --- | --- |
| `h264` | `0x1B` | 视频，**默认与推荐** |
| `h265` | `0x24` | 视频 |
| `vp8` | `0x38` | 视频 |
| `vp9` | `0x39` | 视频 |
| `av1` | `0x3A` | 视频 |
| `aac` | `0x0F` | 音频 |
| `opus` | `0x5355504F` | 音频，**默认** |

配套函数：`codecSdpName(codec)`、`codecIsVideo(codec)`、`codecIsAudio(codec)`、
`codecFromSdpName(name)`、`codecFromValue(v)`、`ALL_CODECS`。

<Warning>
H264 / H265 在 HarmonyOS 上**只有硬编、没有软编兜底**。设备不支持时 SDK
**不报错而是静默退回 VP8**，请用 `isCodecSupported(Codec.h264)` 与
`videoCodecReport()` 核对，详见[错误码](/zh/rtc/harmony/error-codes)。
</Warning>

### `TrackKind`

| 成员 | 值 |
| --- | --- |
| `audio` | `'audio'` |
| `video` | `'video'` |

### `ConnectionState`

| 成员 | 值 | 说明 |
| --- | --- | --- |
| `disconnected` | `0` | 未连接 |
| `connected` | `1` | 已连接 |
| `reconnecting` | `2` | 正在重连 |
| `left` | `3` | 已主动离开 |

### `MediaConnectionState`

**媒体面**（PeerConnection）连接状态，由 `channel.mediaState` 读取、`onMediaStateChange` 上报。

| 成员 | 值 | 说明 |
| --- | --- | --- |
| `disconnected` | `0` | 未连接，或已断开且不再重试 |
| `connecting` | `1` | 首次连接中 |
| `connected` | `2` | 已连接，正常收发 |
| `reconnecting` | `3` | 重连中（引擎正在重建 PeerConnection 并恢复发布订阅） |

配套函数：`mediaConnectionStateName(s)`。

<Warning>
**它与 `ConnectionState` 不是同一条线，不要合并成一个状态。**

信令面（MQTT）与媒体面（PeerConnection）会**各自独立地断开和恢复**：信令断了媒体流往往照旧（SFU 不经信令通道转发媒体），反过来媒体通路失败时信令通常一切正常。

把两者当成一条线会导致两种故障：只看信令 → "网络恢复提示已消失、画面还是黑的"；只看媒体 → 成员列表早已不再更新却毫无提示。UI 上的网络异常提示应当同时接这两条线。

`disconnected` 意味着 SDK 已经放弃重连、**不会再自行恢复**，此时应引导用户重新入会。
</Warning>

### `DisconnectReason`

| 成员 | 值 | 说明 |
| --- | --- | --- |
| `error` | `-1` | 异常断开 |
| `selfLeave` | `1` | 自己离开 |
| `kicked` | `2` | 被踢出 |
| `replaced` | `3` | 同一账号在别处登录，被顶替 |
| `timeout` | `4` | 超时 |
| `destroyed` | `5` | 频道被销毁 |

配套函数：`disconnectReasonFromValue(v)`。

### `DeviceType`

上报的端侧类型。HarmonyOS 是 **`8`**（与错误码前缀 `108` 配套）。

| 成员 | 值 | | 成员 | 值 |
| --- | --- | --- | --- | --- |
| `unknown` | `0` | | `harmonyOS` | `8` |
| `windows` | `1` | | `mcu` | `81` |
| `android` | `2` | | `sip` | `82` |
| `iOS` | `3` | | `h323` | `83` |
| `linux` | `4` | | `gb28181` | `84` |
| `macOS` | `5` | | `rtsp` | `85` |
| `webrtc` | `6` | | `rtmp` | `86` |
| `xcx` | `7` | | `filePlay` | `87` |
| | | | `streamDistribute` | `88` |
| | | | `asr` | `89` |

常量 `CURRENT_DEVICE_TYPE` 即 `DeviceType.harmonyOS`。配套 `deviceTypeFromValue(v)`。

### `DeviceKind`

| 成员 | 值 |
| --- | --- |
| `audioInput` | `'audioInput'` |
| `audioOutput` | `'audioOutput'` |
| `videoInput` | `'videoInput'` |

### `VideoRotation`

| 成员 | 值 |
| --- | --- |
| `deg0` | `0` |
| `deg90` | `90` |
| `deg180` | `180` |
| `deg270` | `270` |

### `CameraPosition` / `CaptureOrientation` / `ScreenCaptureMode`

| 枚举 | 成员 |
| --- | --- |
| `CameraPosition` | `front` / `back` |
| `CaptureOrientation` | `followDevice` / `landscape` / `portrait` |
| `ScreenCaptureMode` | `homeScreen` / `specifiedScreen` / `specifiedWindow` |

### `TrackPriority` / `DegradationPreference`

| 枚举 | 成员 | 说明 |
| --- | --- | --- |
| `TrackPriority` | `veryLow` / `low` / `medium` / `high` | 弱网时的码率分配权重 |
| `DegradationPreference` | `maintainResolution` / `maintainFramerate` / `balanced` / `disabled` | 带宽不足时牺牲分辨率还是帧率 |

配套函数：`trackPriorityBitrateWeight(priority)`。

### `AudioRoute` / `AudioRouteTarget` / `AudioCallState`

| 枚举 | 成员 | 说明 |
| --- | --- | --- |
| `AudioRoute` | `speaker` / `earpiece` / `bluetooth` / `wired` / `other` | **当前**路由，只读五态 |
| `AudioRouteTarget` | `speaker` / `earpiece` | **可切换**目标，只有两态 |
| `AudioCallState` | `unknown` / `dialing` / `incoming` / `connected` / `disconnected` | 系统通话状态 |

`AudioRoute` 比 `AudioRouteTarget` 多三个成员，是因为蓝牙与有线耳机由系统接管 ——
SDK 能上报你现在走的是它们，但**不能主动切到某个具体外设**。

配套函数：`audioRouteName`、`audioRouteTargetName`、`audioRouteTargetAsRoute`、
`audioRouteIsExternal`、`audioRouteIsBuiltIn`、`audioCallStateName`。

### `ConnectionQuality`

| 成员 | 值 |
| --- | --- |
| `unknown` | `'unknown'` |
| `excellent` | `'excellent'` |
| `good` | `'good'` |
| `poor` | `'poor'` |
| `lost` | `'lost'` |

配套函数：`worseQuality(a, b)` —— 取两者中较差的一个。

### `StreamVendor`

| 成员 | 值 | 说明 |
| --- | --- | --- |
| `seastart` | `'seastart'` | SeaStart 自研 SFU |
| `wangsuCDN` | `'wangsucdn'` | 网宿 CDN |

由服务端下发决定，配套 `streamVendorFromValue(v)`。

### `LogLevel`

`SRTCLogger` 的级别。设置方式是 `srtc.logLevel = LogLevel.info`。
配套函数：`logVerbose` / `logDebug` / `logInfo` / `logWarning` / `logError`，
以及可替换的 `LogHandler`。

---

## 入会与频道

### `JoinOptions`

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `autoSubscribeAudio?` | `boolean` | 自动订阅音频，**默认 `false`** |
| `autoSubscribeVideo?` | `boolean` | 自动订阅视频，**默认 `false`** |
| `preferVideoCodec?` | `Codec` | 优先视频编码 |
| `preferAudioCodec?` | `Codec` | 优先音频编码 |
| `userName?` | `string` | 会中昵称 |
| `props?` | `Map<string, string>` | 自定义属性 |

`defaultJoinOptions()` 返回一份全默认的选项。

<Warning>
两个 `autoSubscribe*` 默认都是 `false`，与部分同类 SDK 相反。典型现象是
"入会成功但听不到、看不到别人"。
</Warning>

### `ChannelInfo`

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `appId` | `string` | 应用 ID |
| `channel` | `string` | 频道名 |
| `streamVendor?` | `string` | 流媒体引擎 |
| `props?` | `Map<string, Object>` | 频道自定义属性 |
| `whiteBoard?` | `string` | 白板地址 |
| `createdAt?` / `updatedAt?` | `number` | 时间戳 |

配套：`channelInfoFromJson` / `channelInfoToJson`。

### `UserInfo`

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `uid` | `string` | 用户 ID |
| `sid?` | `string` | 会话 ID |
| `name?` | `string` | 昵称 |
| `deviceType?` | `DeviceType` | 端类型 |
| `deviceId?` | `string` | 设备 ID |
| `version?` | `string` | 对端 SDK 版本 |
| `network?` | `string` | 网络类型 |
| `linkId?` | `number` | 链路 ID |
| `streamTracks?` | `TrackInfo[]` | 该用户当前发布的轨道 |
| `props?` | `Map<string, Object>` | 自定义属性 |
| `updatedAt?` | `number` | 时间戳 |

配套：`userInfoFromJson` / `userInfoToJson`。

---

## 轨道

### `TrackInfo`

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `id` | `string` | 轨道 ID |
| `desc` | `string` | 描述，如 `camera` / `screen` / `mic` / `audio_mix` |
| `kind` | `TrackKind` | 音频还是视频 |
| `codec?` | `Codec` | 编码格式 |
| `width?` / `height?` / `fps?` | `number` | 视频参数 |
| `angle?` | `number` | 视频角度（移动端旋转用） |
| `maxBitrate?` | `number` | 最大码率 |
| `sampleRate?` / `channels?` | `number` | 音频参数 |
| `props?` | `Map<string, string>` | 自定义属性 |
| `simulcasts?` | `SimulcastInfo[]` | Simulcast 各层信息 |
| `fallbackIds?` | `string[]` | 降级候选轨道 ID |
| `variant?` | `boolean` | 是否为副层 |

配套：`trackInfoFromJson` / `trackInfoToJson` / `cloneTrackInfo`。

### `SimulcastInfo`

| 字段 | 类型 |
| --- | --- |
| `rid?` | `string` |
| `width?` / `height?` / `fps?` / `maxBitrate?` | `number` |

配套：`simulcastInfoFromJson` / `simulcastInfoToJson`。

---

## 采集参数

### `MicCaptureOptions`

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `deviceId?` | `string` | 指定麦克风 |
| `echoCancellation` | `boolean` | 回声消除 |
| `noiseSuppression` | `boolean` | 噪声抑制 |
| `autoGainControl` | `boolean` | 自动增益 |
| `channelCount` | `number` | 声道数 |
| `sampleRate` | `number` | 采样率 |

### `CameraCaptureOptions`

| 字段 | 类型 | 默认 | 说明 |
| --- | --- | --- | --- |
| `deviceId?` | `string` | — | 指定摄像头 |
| `position` | `CameraPosition` | `front` | 前置 / 后置 |
| `width` / `height` | `number` | `1280×720` | 采集分辨率 |
| `frameRate` | `number` | `15` | 帧率 |
| `orientation` | `CaptureOrientation` | `followDevice` | 方向策略 |

<Note>
**采集分辨率受设备档位限制，档位表因机型而异。** 底层会把请求宽高吸附到最近的档位，
所以实际拿到的尺寸可能与设定值不同。这也是必须调用 `SRTC.init(context)` 的原因 ——
没有 Context 就查不到档位表。
</Note>

### `ScreenCaptureOptions`

| 字段 | 类型 | 默认 | 说明 |
| --- | --- | --- | --- |
| `width` / `height` | `number` | `1920×1080` | 采集分辨率 |
| `frameRate` | `number` | `10` | 帧率 |
| `mode` | `ScreenCaptureMode` | `homeScreen` | 整屏 / 指定屏 / 指定窗口 |
| `targetId?` | `number` | — | 指定屏或窗口时的目标 ID |

### `ScreenAudioCaptureOptions`

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `sampleRate` | `number` | 采样率 |
| `channelCount` | `number` | 声道数 |
| `excludesCurrentProcessAudio` | `boolean` | 是否排除本进程音频（防回环） |

### 其它

+ `VideoCaptureParams`：`width` / `height` / `frameRate`
+ `CaptureSize`：`width` / `height`，配套 `orientCaptureSize(size, orientation)`
+ `ZoomRange`：`min` / `max` / `supported`。设备变焦范围，由 `track.zoomRange()` 返回。
  `supported === false` 时 `min` / `max` 均为 `1`，调用方不必判空。
  ⚠️ 它反映的是**当前这一刻能不能变焦**而不是设备能力，详见
  [轨道接口](/zh/rtc/harmony/api-reference/media-tracks#变焦)
+ 默认值函数：`defaultMicCaptureOptions()` / `defaultCameraCaptureOptions()` /
  `defaultScreenCaptureOptions()` / `defaultScreenAudioCaptureOptions()`
+ 合并函数：`mergeMicCaptureOptions()` / `mergeCameraCaptureOptions()` /
  `mergeScreenCaptureOptions()` / `mergeScreenAudioCaptureOptions()`

---

## 发布参数

### `AudioPublishOptions`

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `desc` | `string` | 轨道描述 |
| `codec?` | `Codec` | 编码格式 |
| `maxBitrate?` | `number` | 最大码率 |
| `dtx` | `boolean` | 静音时不连续传输 |
| `red` | `boolean` | 冗余编码 |
| `priority?` | `TrackPriority` | 弱网优先级 |
| `props?` | `Map<string, string>` | 自定义属性 |

### `VideoPublishOptions`

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `desc` | `string` | 轨道描述 |
| `codec?` | `Codec` | 编码格式 |
| `width?` / `height?` | `number` | 编码分辨率 |
| `maxBitrate?` / `maxFramerate?` | `number` | 码率与帧率上限 |
| `priority?` | `TrackPriority` | 弱网优先级 |
| `degradationPreference` | `DegradationPreference` | 降级策略 |
| `props?` | `Map<string, string>` | 自定义属性 |
| `simulcasts?` | `VideoPublishOptions[]` | Simulcast 各层配置 |

默认值：`defaultAudioPublishOptions()` / `defaultVideoPublishOptions()`；
合并：`mergeAudioPublishOptions()` / `mergeVideoPublishOptions()`。

---

## 预设

预设是「采集参数 + 发布参数」的成对封装，直接传给 `createLocalXxxTrack`。

| 接口 | 组成 |
| --- | --- |
| `MicPreset` | `captureOptions: MicCaptureOptions` + `publishOptions: AudioPublishOptions` |
| `CameraPreset` | `captureOptions: CameraCaptureOptions` + `publishOptions: VideoPublishOptions` |
| `ScreenPreset` | `captureOptions: ScreenCaptureOptions` + `publishOptions: VideoPublishOptions` |
| `ScreenAudioPreset` | `captureOptions: ScreenAudioCaptureOptions` + `publishOptions: AudioPublishOptions` |

现成预设：

| 分类 | 函数 |
| --- | --- |
| 麦克风 | `micPresetSpeech()`、`micPresetMusic()`、`micPresetMusicStereo()`、`micPresetMusicHighQuality()`、`micPresetMusicHighQualityStereo()` |
| 摄像头 | `cameraPreset1080p()`、`cameraPreset720p()`、`cameraPreset360p()`、`cameraPreset180p()` |
| 屏幕 | `screenPreset1080p()`、`screenPreset720p()` |
| 屏幕音频 | `screenAudioPresetDefault()` |
| Simulcast 副层 | `cameraSmallStreamPreset()` |

---

## 质量与信令消息

### `QualitySample`

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `level` | `ConnectionQuality` | 质量等级 |
| `score` | `number` | 综合评分 |
| `mos` | `number` | MOS 值 |
| `loss` | `number` | 丢包率 |
| `rtt` | `number` | 往返时延 |
| `jitter` | `number` | 抖动 |
| `packets` / `bytes` / `bitrate` | `number` | 流量统计 |

### `QualityReport`

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `ts` | `number` | 时间戳 |
| `pub` | `QualitySample` | 上行 |
| `sub` | `QualitySample` | 下行 |

### `QualityEvaluation` / `ConnectionQualityChange`

| 接口 | 字段 |
| --- | --- |
| `QualityEvaluation` | `uplink` / `downlink` / `overall`（均为 `ConnectionQuality`）、`mos`、`timestamp` |
| `ConnectionQualityChange` | `evaluation: QualityEvaluation`、`previous: ConnectionQuality` |

### 活跃说话人

| 接口 | 字段 |
| --- | --- |
| `ActiveSpeakerInfo` | `uid`、`trackId`、`level` |
| `ActiveSpeakersSnapshot` | `ts`、`speakers: ActiveSpeakerInfo[]` |
| `ActiveSpeakerDelta` | `uid`、`trackId`、`level`、`active` |
| `ActiveSpeakersDeltaMessage` | `ts`、`speakers: ActiveSpeakerDelta[]` |

### `LayerSwitchedInfo`

Simulcast 层切换。

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `subKey` | `string` | 订阅键（`uid:trackId`） |
| `fromTrackId?` | `string` | 切换前的轨道 |
| `toTrackId` | `string` | 切换后的轨道 |
| `reason` | `string` | 切换原因 |
| `latencyMs` | `number` | 切换耗时 |

配套解析函数：`qualityReportFromJson`、`activeSpeakersFromJson`、`layerSwitchedFromJson`、
`signalMessageType`。

### `RtcStatsSnapshot`

`channel.getStats()` 返回的一次采集快照。

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `timestampMs` | `number` | 采集时刻（`Date.now()`，毫秒） |
| `outbound` | `OutboundStreamStats[]` | 发送侧各路流 |
| `inbound` | `InboundStreamStats[]` | 接收侧各路流 |
| `connection` | `ConnectionStats` | 连接级统计 |

#### `OutboundStreamStats`

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `kind` | `string` | `audio` / `video` |
| `ssrc?` | `number` | |
| `trackIdentifier?` | `string` | 对应的 `Track.id` |
| `rid?` | `string` | Simulcast 分层标识 |
| `codec?` | `string` | 实际协商使用的编码名（大写，如 `H264`） |
| `bitrateKbps` | `number` | 实际发送码率 |
| `packetsSent?` | `number` | |
| `packetsLost?` | `number` | **远端报回来的**丢包数，不是本端统计 |
| `frameWidth?` / `frameHeight?` | `number` | 实际编码宽高。与预设不一致说明被设备档位吸附了 |
| `framesPerSecond?` | `number` | |
| `qualityLimitationReason?` | `string` | 编码器降级原因：`none` / `cpu` / `bandwidth` / `other` |

<Note>
**判断"某条轨道的 RTP 有没有在发"必须用 `trackIdentifier` 匹配**，不能只看"有任意一条 outbound 的 `packetsSent > 0`"。取消发布后 transceiver 只是 stop、不从连接上移除，它那条旧统计会一直留在报告里（真机实测：关掉摄像头再重开，旧统计的 `packetsSent` 卡在原值不动）。
</Note>

`qualityLimitationReason` 是弱网排障的第一现场：`bandwidth` 说明码率被带宽估计压了，`cpu` 说明设备扛不住，两者的处理完全不同。

#### `InboundStreamStats`

`kind`、`ssrc?`、`codec?`、`bitrateKbps`、`packetsReceived?`、`packetsLost?`（本端统计）、`jitter?`（**秒**，不是毫秒）、`frameWidth?` / `frameHeight?`、`framesPerSecond?`、`totalFreezesDuration?`（累计冻结秒数，卡顿的直接指标）。

#### `ConnectionStats`

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `roundTripTimeMs?` | `number` | 当前 RTT（**毫秒**，W3C 原值是秒，这里已换算） |
| `availableOutgoingBitrateKbps?` | `number` | 带宽估计得出的可用上行带宽 |
| `availableIncomingBitrateKbps?` | `number` | 可用下行带宽。见下方警告 |
| `bytesSent?` / `bytesReceived?` | `number` | |

<Warning>
**`availableIncomingBitrateKbps` 实测恒为 `undefined`。** 海思平台（nova 12 Pro / OpenHarmony-6.1.1.120）的 `candidate-pair` 统计里没有这个字段（上行那个有）。W3C 规范里它本就是可选的，底层只在部分路径上填。

保留该字段是为了对齐 W3C 与其它端的结构，**不要在 UI 上依赖它** —— 要展示下行状况请用 `inbound` 各路 `bitrateKbps` 求和。
</Warning>

配套函数：`emptyStatsSnapshot()`（空快照，取不到统计时返回它而不抛错）、
`statsSummary(s)`（压成便于阅读的多行文本，形如 `发送 video H264 1180kbps 1280x720@30 (bandwidth) 丢包=3`）。

### 协商结果

| 类型 / 函数 | 说明 |
| --- | --- |
| `NegotiatedMedia` | `kind`、`mid`、`codec`（大写）、`fmtp`（`a=fmtp:` 参数原文） |
| `negotiatedMedias(sdp)` | 解出每条 m-line 实际协商到的编码 |
| `negotiatedVideoCodec(sdp)` | 本次协商的视频编码名，多条视频 m-line 时取第一条 |
| `negotiatedAudioCodec(sdp)` | 本次协商的音频编码名 |
| `negotiatedSummary(sdp)` | 压成一行，形如 `video/mid=1 H264 [profile-level-id=42e01f]; audio/mid=0 OPUS` |

<Warning>
**这是"视频到底是不是 H264"唯一可靠的判据。**

要传 **answer**（本端发布看远端 answer，本端订阅看远端 offer）—— offer 里是候选列表，只有 answer 才代表最终选中的那一个。

不要拿 `videoCodecReport()` 核对：它回答的是**设备能不能** H264，而静默降级恰恰发生在能力表漂亮、协商结果却是 VP8 的情况下，拿它核对等于没核对。

SDK 内部在每次协商后已自动打日志，真机排障可直接
`hdc shell hilog -x | grep -a 协商结果`。
</Warning>

---

## 设备与消息

### `DeviceInfo`

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `deviceId` | `string` | 设备 ID，可回填到采集参数 |
| `name` | `string` | 设备名 |
| `kind` | `DeviceKind` | 设备类别 |
| `isDefault` | `boolean` | 是否系统默认 |

配套：`deviceKindFromValue`、`deviceListEquals`、`deviceListDiff`。

### `AudioRouteInfo`

| 字段 | 类型 |
| --- | --- |
| `route` | `AudioRoute` |
| `name` | `string` |
| `deviceId` | `number` |
| `isActive` | `boolean` |

### `CustomMessage` / `ImMessage`

| 接口 | 字段 |
| --- | --- |
| `CustomMessage` | `action`、`content`、`uid`、`isPrivate` |
| `ImMessage` | `action`、`content`、`sid`、`uid`、`name?` |

`content` 统一是**字符串** —— 需要结构化数据请自己 `JSON.parse`。

---

## Token

| 接口 | 字段 |
| --- | --- |
| `BaseRtcToken` | `appId`、`uid`、`sid`、`expAt`、`clientKey`、`clientApi`、`logCenter?` |
| `ChannelToken` | 继承 `BaseRtcToken`，加 `channel` |
| `ImToken` | 继承 `BaseRtcToken` |

解析与校验：`decodeChannelToken(str)`、`decodeImToken(str)`、`isTokenExpired(token)`。

Token 由**业务后端**签发，SDK 只负责解析与过期判断。

---

## 服务端配置

由入会响应下发，一般不需要直接构造：

`MqttServer`、`WebrtcServer`、`TurnServer`、`UploadServer`、`RtmpServer`、
`ChannelJoinResponse`。

解析函数：`mqttServerFromJson`、`webrtcServerFromJson`、`channelJoinResponseFromJson`、
`channelJoinResponseAsChannelInfo`。

---

## 工具类型

| 名称 | 说明 |
| --- | --- |
| `JsonObject` | `Record<string, Object>`，信令 JSON 的统一形态 |
| `MulticastDelegate<T>` | 多播委托容器，`delegates` 字段的类型 |
| `StateSync<T>` | 状态同步容器 |
| `AsyncMutex` / `SerialRunner` | 并发控制 |
| `Debounce` / `AsyncDebounce` | 防抖 |
| `RetryConfig` | 重试配置，配套 `withRetry`、`defaultRetryConfig` |
| `MsgPackValue` | MessagePack 值，配套 `msgPackUnpack`、`msgPackToJson`、`MsgPackError` |

JSON 读取工具（ArkTS 禁止对任意对象下标访问，所以统一走这层）：
`asObject`、`getString`、`getNumber`、`getBool`、`getObject`、`getArray`、
`getStringMap`、`getAnyMap`、`mapToObject`、`putIfPresent`。

---

### 相关阅读

+ [核心概念](/zh/rtc/harmony/key-concepts)
+ [事件参考](/zh/rtc/harmony/events)
+ [SRTCEngine 接口](/zh/rtc/harmony/api-reference/SRTCEngine)
