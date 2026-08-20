---
title: "类型定义"
description: "SRTC Swift SDK 常用结构体、枚举、预设与设备类型说明"
---

本文不逐字段复刻源码中的所有内部实现，而是整理接入最常用、最需要理解的公开类型。

---

### JoinOptions

加入频道的可选参数。

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `autoSubscribeAudio` | `Bool` | 是否自动订阅已有远端音频，默认 `false` |
| `autoSubscribeVideo` | `Bool` | 是否自动订阅已有远端视频，默认 `false` |
| `preferVideoCodec` | `Codec?` | 优先视频编码 |
| `preferAudioCodec` | `Codec?` | 优先音频编码 |
| `userName` | `String?` | 用户名 |
| `props` | `[String: String]?` | 自定义业务属性 |

示例：

```swift
let options = JoinOptions(
    autoSubscribeAudio: true,
    autoSubscribeVideo: false,
    userName: "alice"
)
```

---

### ChannelInfo

频道信息。

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `appId` | `String` | 应用 ID |
| `channel` | `String` | 频道名 |
| `streamVendor` | `String?` | 当前流媒体引擎 |
| `props` | `[String: AnyCodable]?` | 频道自定义属性 |
| `whiteBoard` | `String?` | 白板页面地址，已拼好授权码，用 `WKWebView` 加载即可，见[电子白板](/zh/rtc/whiteboard) |
| `createdAt` | `TimeInterval?` | 创建时间 |
| `updatedAt` | `TimeInterval?` | 更新时间 |

---

### UserInfo

用户信息。

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `uid` | `String` | 用户 ID |
| `sid` | `String?` | 会话 ID |
| `name` | `String?` | 用户名 |
| `deviceType` | `DeviceType?` | 设备类型 |
| `deviceId` | `String?` | 设备 ID |
| `version` | `String?` | SDK 版本 |
| `network` | `String?` | 网络类型 |
| `streamTracks` | `[TrackInfo]?` | 当前用户已发布轨道 |
| `props` | `[String: AnyCodable]?` | 用户自定义属性 |

---

### TrackInfo

轨道描述信息。

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `id` | `String` | 轨道 ID |
| `desc` | `String` | 轨道描述，如 `mic`、`screen`、`camera_big` |
| `kind` | `TrackKind` | `audio` 或 `video` |
| `codec` | `Codec?` | 编解码器 |
| `width` / `height` | `Int?` | 视频宽高 |
| `fps` | `Int?` | 帧率 |
| `angle` | `Int?` | 视频角度 |
| `maxBitrate` | `Int?` | 最大码率 |
| `sampleRate` | `Int?` | 音频采样率 |
| `channels` | `Int?` | 声道数 |
| `props` | `[String: String]?` | 自定义属性 |
| `simulcasts` | `[SimulcastInfo]?` | 联播编码层信息 |

---

### Codec

编解码器枚举。

| 枚举值 | 说明 |
| --- | --- |
| `h264` | H.264 视频编码 |
| `h265` | H.265 视频编码 |
| `vp8` | VP8 视频编码 |
| `vp9` | VP9 视频编码 |
| `av1` | AV1 视频编码 |
| `aac` | AAC 音频编码 |
| `opus` | Opus 音频编码 |

---

### VideoRotation

视频帧旋转方向，用于 `pushFrame(_:rotation:timestampNs:)` 与 `VideoFrame`。

| 枚举值 | 原始值 | 说明 |
| --- | --- | --- |
| `_0` | `0` | 不旋转（默认） |
| `_90` | `90` | 顺时针 90 度 |
| `_180` | `180` | 180 度 |
| `_270` | `270` | 顺时针 270 度 |

原始值就是角度，与 Android 端 `inputData` 的 `rotation` 参数同一口径。

---

### StreamVendor

流媒体引擎供应商。

| 枚举值 | 原始值 | 说明 |
| --- | --- | --- |
| `seastart` | `"seastart"` | SeaStart 自研 SFU 引擎 |
| `wangsuCDN` | `"wangsucdn"` | 网宿 CDN 引擎 |

SDK 会根据 Token / Join 响应中的 `stream_vendor` 自动选择对应引擎。

---

### ConnectionState

| 枚举值 | 说明 |
| --- | --- |
| `disconnected` | 初始状态或未连接 |
| `connected` | 已连接 |
| `reconnecting` | 重连中 |
| `left` | 已离开 |

### DisconnectReason

| 枚举值 | 原始值 | 说明 |
| --- | --- | --- |
| `error` | `-1` | 错误导致断开 |
| `self` | `1` | 自己主动离开 |
| `kicked` | `2` | 被踢出 |
| `replaced` | `3` | 同 UID 其他端替换登录 |
| `timeout` | `4` | 超时断开 |
| `destroyed` | `5` | 频道被销毁 |

---

### 预设类型

#### MicPreset

常用预设：

+ `.speech`
+ `.music`
+ `.musicStereo`
+ `.musicHighQuality`
+ `.musicHighQualityStereo`

#### CameraPreset

常用预设：

+ `.h180p`
+ `.h360p`
+ `.h720p`
+ `.h1080p`

#### ScreenPreset

常用预设：

+ `.h720p`
+ `.h1080p`

#### ScreenAudioPreset

常用预设：

+ `.default`

这些预设本质上都是“采集参数 + 发布参数”的组合体。也就是说，预设不是语法糖，而是把一组合理默认值打包成一个对象，减少业务层重复配置。

---

### ScreenCaptureMode

iOS 屏幕采集方式，传给 `createLocalScreenTrack(mode:)`。macOS 忽略此项（始终走 `ScreenCaptureKit`）。

| 取值 | 说明 |
| --- | --- |
| `.inApp` | 默认值。应用内采集，零额外集成，但**只能采到本 App 的画面** |
| `.broadcast(appGroup: String)` | 全屏采集，能采整个系统屏幕；需要集成 Broadcast Upload Extension 与 App Group |

```swift
let track = srtc.createLocalScreenTrack(
    preset: .h720p,
    mode: .broadcast(appGroup: "group.your.app.group")
)
```

集成步骤见[屏幕共享](/zh/rtc/swift/advanced/screen-sharing)。

---

### DeviceInfo

设备管理器返回的统一设备结构。

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `deviceId` | `String` | 设备唯一标识 |
| `name` | `String` | 设备名称 |
| `kind` | `DeviceInfo.DeviceKind` | 设备类型 |
| `isDefault` | `Bool` | 是否为默认设备 |

`DeviceKind` 可选值：

+ `audioInput`
+ `audioOutput`
+ `videoInput`

<Note>
iOS 上 `getDevices(kind: .audioOutput)` 返回空数组——系统不暴露输出设备枚举。
控制输出走向请用下面的音频路由类型，见[音频路由](/zh/rtc/swift/advanced/audio-routing)。
</Note>

---

### AudioRoute

**iOS 专有。** 当前音频输出路由，**只读上报用**，五态。

| 取值 | 说明 |
| --- | --- |
| `speaker` | 内置扬声器（免提） |
| `receiver` | 内置听筒 |
| `bluetooth` | 蓝牙耳机 |
| `headset` | 有线耳机（3.5mm / Lightning / USB） |
| `unknown` | 其他输出（AirPlay、CarPlay、HDMI 等） |

辅助属性：

| 成员 | 类型 | 说明 |
| --- | --- | --- |
| `displayName` | `String` | 中文名称，可直接用于 UI |
| `isBuiltIn` | `Bool` | 是否内置路由（扬声器 / 听筒） |
| `isExternal` | `Bool` | 是否外接路由（蓝牙 / 有线） |

---

### AudioRouteTarget

**iOS 专有。** 可**主动切换**的路由目标，只有两态。

| 取值 | 说明 |
| --- | --- |
| `speaker` | 扬声器（免提） |
| `earpiece` | 听筒 |

与 `AudioRoute` 刻意分开：iOS 不提供切换到指定蓝牙 / 有线设备的能力，外设由系统接管，
SDK 只能控制「内置扬声器还是听筒」。`asRoute` 可映射回 `AudioRoute`（`.earpiece` → `.receiver`）。

---

### AudioRouteInfo

**iOS 专有。** 系统音频端口快照，**诊断 / 展示用**，不是可选择的列表。

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `id` | `String` | 端口 UID；扬声器为固定值 `"speaker"` |
| `route` | `AudioRoute` | 该端口对应的语义路由 |
| `name` | `String` | 端口名称，如 "AirPods Pro" |
| `isActive` | `Bool` | 是否为当前生效路由 |

---

### AudioCallState

**iOS 专有。** 系统通话状态，来自 CallKit。SDK 用它决定音频中断后何时可以恢复。

| 取值 | 说明 |
| --- | --- |
| `dialing` | 去电拨号中 |
| `incoming` | 来电响铃中 |
| `connected` | 通话已接通 |
| `disconnected` | 无通话 / 通话已结束 |
| `unknown` | 未知 |

---

### ConnectionQuality

连接质量等级，从服务端下发的报告里解出。

| 取值 | 说明 |
| --- | --- |
| `unknown` | 初始占位，尚无报告 |
| `excellent` | 优秀 |
| `good` | 良好 |
| `poor` | 较差 |
| `lost` | 已丢失 |

「较差」比较的顺序是 `unknown` < `excellent` < `good` < `poor` < `lost`。

---

### QualitySample

单方向的质量数值快照，信号塔 / 网络面板可以直接读这些字段渲染。

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `level` | `ConnectionQuality` | 服务端给出的等级 |
| `score` | `Int` | 0~100，越大越好 |
| `mos` | `Double` | 1.0~4.5，越大越好 |
| `loss` | `Double` | 丢包率，0~1 的**比例**（不是百分数） |
| `rtt` | `Double` | 往返时延，毫秒 |
| `jitter` | `Double` | 抖动，毫秒 |
| `packets` | `Int` | 本轮统计参与计算的包数 |
| `bitrate` | `Int` | 平均码率，kbps |
| `bytes` | `Int` | 本窗口字节数 |

---

### QualityReport

一次完整的质量报告，服务端每次下发都会抛一份。

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `ts` | `Int64` | 服务端生成报告时的 Unix 毫秒时间戳 |
| `pub` | `QualitySample` | 上行（客户端到 SFU） |
| `sub` | `QualitySample` | 下行（SFU 到客户端） |

---

### QualityEvaluation

简化的等级评估快照，`getConnectionQuality()` 与跳档事件用它。

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `uplink` | `ConnectionQuality` | 上行等级 |
| `downlink` | `ConnectionQuality` | 下行等级 |
| `overall` | `ConnectionQuality` | 取上下行**较差**的一档 |
| `mos` | `Double` | 取上下行较小值，反映用户感知最弱的一侧 |
| `timestamp` | `Int64` | 对应报告的 `ts` |

---

### ConnectionQualityChange

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `evaluation` | `QualityEvaluation` | 跳档后的评估 |
| `previous` | `ConnectionQuality` | 跳档前的等级，首次跳档时为 `unknown` |

---

### ActiveSpeakerInfo / ActiveSpeakersSnapshot

| 类型 | 字段 |
| --- | --- |
| `ActiveSpeakerInfo` | `uid`、`trackId`、`level`（0~1 归一化线性音量） |
| `ActiveSpeakersSnapshot` | `ts`、`speakers: [ActiveSpeakerInfo]` |

`speakers` 是**全量列表**，SDK 已合并服务端的增量协议并按 `level` 降序排好，无人说话时为空数组。

---

### LayerSwitchedInfo

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `subKey` | `String` | 订阅键，形如 `发布者uid:trackId` |
| `fromTrackId` | `String?` | 切换前的层 |
| `toTrackId` | `String` | 切换后的层 |
| `reason` | `String` | 服务端给出的原因，如 `bwe_down`、`bwe_up`、`track_ended`；客户端主动切层为 `client` |
| `latencyMs` | `Int` | 从发起切层到真正切到目标层的耗时，毫秒 |

以上质量相关类型的用法见 [通话质量与活跃说话人](/zh/rtc/swift/advanced/call-quality)。
