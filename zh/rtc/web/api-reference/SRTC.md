---
title: "SRTC"
description: "Web SRTC 音视频 SDK SRTC 接口参考"
---

SRTC 是 Web SDK 的核心入口，通过 `new SRTC(initParams)` 创建实例。

---

### constructor

```typescript
constructor(initParams: SdkInitParams)
```

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | :---: | --- |
| `initParams` | `SdkInitParams` | 是 | 初始化参数，详见 [SdkInitParams](/zh/rtc/web/types#sdkinitparams) |

---

### buildInfo

获取 SDK 编译信息。

```typescript
buildInfo(): BuildInfo
```

---

### getEnvInfo

获取当前浏览器的 WebRTC 能力检测结果，建议在初始化后尽早调用。

```typescript
getEnvInfo(): EnvWebInfo
```

**返回值：** `EnvWebInfo`，详见 [EnvWebInfo](/zh/rtc/web/types#envwebinfo)

---

### onNotifyChannelEvent

频道内事件回调，建议在 `join` 前注册。

```typescript
onNotifyChannelEvent?: ((event: ChannelEvent) => void) | null
```

完整事件类型详见 [事件参考](/zh/rtc/web/events)。

---

### onNotifyImEvent

频道外 IM 事件回调。

```typescript
onNotifyImEvent?: ((event: ImEvent) => void) | null
```

---

### join

加入频道。

```typescript
join(token: string, options?: JoinOptions): Promise<ChannelInfo>
```

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | :---: | --- |
| `token` | `string` | 是 | 服务端签发的加入频道 Token |
| `options` | `JoinOptions` | 否 | 加入选项，详见 [JoinOptions](/zh/rtc/web/types#joinoptions) |

---

### leave

主动离开频道。对于本地轨道，SDK 会在离会后自动停止采集、停止播放或移除播放视图。

```typescript
leave(): Promise<void>
```

---

### getChannelInfo

获取当前频道信息。未加入频道时返回 `null`。

```typescript
getChannelInfo(): ChannelInfo | null
```

---

### getUserInfo

获取频道内指定用户信息。

```typescript
getUserInfo(uid: string): UserInfo
```

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | :---: | --- |
| `uid` | `string` | 是 | 用户 ID |

---

### getUsersInfo

获取频道内所有用户信息，支持数组和映射两种返回格式。

```typescript
getUsersInfo(map: true): Record<string, UserInfo>
getUsersInfo(map: false): UserInfo[]
```

---

### getStreamMetric

获取当前流媒体网络质量指标快照，例如上下行码率、丢包率等。

```typescript
getStreamMetric(): Record<string, any> | undefined
```

> 未加入频道时调用会抛出异常。

---

### getDevices

枚举媒体设备列表。

```typescript
getDevices(kind?: MediaDeviceKind, requestPermissions?: boolean): Promise<MediaDeviceInfo[]>
```

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | :---: | --- |
| `kind` | `'audioinput' \| 'audiooutput' \| 'videoinput'` | 否 | 不传则返回所有类型设备 |
| `requestPermissions` | `boolean` | 否 | 是否主动请求媒体权限，默认 `true` |

---

### createLocalMicTrack

创建麦克风音频轨道。

```typescript
createLocalMicTrack(preset?: MicPreset): LocalMicTrack
```

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | :---: | --- |
| `preset` | `MicPreset` | 否 | 麦克风预设，默认 `MicPresets.music` |

---

### createLocalCustomAudioTrack

使用自定义 `MediaStreamTrack` 创建本地音频轨道。

```typescript
createLocalCustomAudioTrack(msTrack: MediaStreamTrack): LocalAudioTrack
```

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | :---: | --- |
| `msTrack` | `MediaStreamTrack` | 是 | 音频类型的 `MediaStreamTrack` |

---

### createLocalCameraTrack

创建摄像头视频轨道。

```typescript
createLocalCameraTrack(preset?: CameraPreset): LocalCameraTrack
```

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | :---: | --- |
| `preset` | `CameraPreset` | 否 | 摄像头预设，默认 `CameraPresets['720p']` |

---

### createLocalScreenTrack

创建屏幕共享视频轨道。

```typescript
createLocalScreenTrack(preset?: ScreenPreset, audioPreset?: ScreenAudioPreset): LocalScreenTrack
```

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | :---: | --- |
| `preset` | `ScreenPreset` | 否 | 视频预设，默认 `ScreenPresets['1080p']` |
| `audioPreset` | `ScreenAudioPreset` | 否 | 系统音频预设，默认 `ScreenAudioPresets.default` |

> 默认会同时创建系统音频轨道。真正能否采集到系统音频，还取决于浏览器能力和用户是否在系统分享弹窗中勾选“分享音频”。

---

### createLocalCustomVideoTrack

使用自定义 `MediaStreamTrack` 创建本地视频轨道。

```typescript
createLocalCustomVideoTrack(msTrack: MediaStreamTrack): LocalVideoTrack
```

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | :---: | --- |
| `msTrack` | `MediaStreamTrack` | 是 | 视频类型的 `MediaStreamTrack` |

---

### publishLocalTrack

将本地轨道发布到频道，发布后远端用户可以订阅。

```typescript
publishLocalTrack(
  track: LocalAudioTrack | LocalVideoTrack,
  opt?: Partial<AudioPublishOptions> | Partial<VideoPublishOptions>
): Promise<void>
```

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | :---: | --- |
| `track` | `LocalAudioTrack \| LocalVideoTrack` | 是 | 要发布的本地轨道 |
| `opt` | `Partial<AudioPublishOptions> \| Partial<VideoPublishOptions>` | 否 | 发布参数，会与创建轨道时的预设参数合并 |

---

### unpublishLocalTrack

停止发布本地轨道，远端用户将收到 `USER_TRACK_REMOVE` 事件。

```typescript
unpublishLocalTrack(track: LocalAudioTrack | LocalVideoTrack): Promise<void>
```

---

### enableLocalTrack

恢复已暂停的本地轨道数据发送。

```typescript
enableLocalTrack(track: LocalAudioTrack | LocalVideoTrack): Promise<void>
```

> 远端会收到 `TRACK_UNMUTED` 事件。与 `publishLocalTrack` 的区别详见 [静音 vs 停止发布](/zh/rtc/web/advanced/mute-vs-unpublish)。

---

### disableLocalTrack

暂停本地轨道数据发送，但不取消发布。

```typescript
disableLocalTrack(track: LocalAudioTrack | LocalVideoTrack): void
```

> 远端会收到 `TRACK_MUTED` 事件。与 `unpublishLocalTrack` 的区别详见 [静音 vs 停止发布](/zh/rtc/web/advanced/mute-vs-unpublish)。

---

### subscribeRemoteAudioMixTrack

订阅全频道混音流。

```typescript
subscribeRemoteAudioMixTrack(
  filter?: string[] | ((track: BaseTrack) => boolean)
): Promise<RemoteAudioMixTrack>
```

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | :---: | --- |
| `filter` | `string[] \| ((track: BaseTrack) => boolean)` | 否 | 传 `string[]` 时按 UID 排除；传函数时按轨道判断是否过滤 |

---

### subscribeRemoteAudioTrack

订阅指定用户的单路音频流。

```typescript
subscribeRemoteAudioTrack(uid: string, id: string): Promise<RemoteAudioTrack>
```

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | :---: | --- |
| `uid` | `string` | 是 | 用户 ID |
| `id` | `string` | 是 | 轨道 ID，可从 `TrackInfo.id` 获取 |

---

### subscribeRemoteVideoTrack

订阅指定用户的视频流。

```typescript
subscribeRemoteVideoTrack(uid: string, id: string): Promise<RemoteVideoTrack>
```

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | :---: | --- |
| `uid` | `string` | 是 | 用户 ID |
| `id` | `string` | 是 | 轨道 ID，可从 `TrackInfo.id` 获取 |

---

### subscribeRemoteVideoMcuTrack

订阅远端视频合成流。

```typescript
subscribeRemoteVideoMcuTrack(): Promise<RemoteVideoMcuTrack>
```

> `RemoteVideoMcuTrack` 继承自 `RemoteVideoTrack`，可按普通远端视频轨道使用。

---

### unsubscribeRemoteTrack

取消订阅远端流。

```typescript
unsubscribeRemoteTrack(
  track: RemoteAudioMixTrack | RemoteAudioTrack | RemoteVideoTrack
): Promise<void>
```

---

### getRemoteTrack

通过用户 ID 与轨道 ID 或轨道描述获取已订阅的远端轨道实例。

```typescript
getRemoteTrack(uid: string, id?: string, desc?: string): RemoteAudioTrack | RemoteVideoTrack
```

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | :---: | --- |
| `uid` | `string` | 是 | 用户 ID |
| `id` | `string` | 否 | 轨道 ID，与 `desc` 二选一 |
| `desc` | `string` | 否 | 轨道描述，与 `id` 二选一 |

> `id` 和 `desc` 至少要传一个，否则会抛出异常。

---

### enableIm

启用频道外 IM 消息功能。

```typescript
enableIm(token: string): Promise<string>
```

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | :---: | --- |
| `token` | `string` | 是 | IM 启用 Token |

**返回值：** `Promise<string>`，返回 IM 会话 `sid`。

---

### disableIm

关闭频道外 IM 消息功能。

```typescript
disableIm(): Promise<void>
```
