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
