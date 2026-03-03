---
title: "SRTC"
description: "Web SRTC 音视频 SDK SRTC 接口参考"
---

SRTC 是绝大多数操作的入口，通过 `new SRTC(initParams)` 创建实例。

---

### constructor

```typescript
constructor(initParams: SdkInitParams)
```typescript

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | :---: | --- |
| `initParams` | `SdkInitParams` | 否 | 初始化参数，详见 [SdkInitParams](/zh/rtc/web/types#sdkinitparams) |

---

### buildInfo

获取 SDK 编译信息（版本号等）。

```typescript
buildInfo(): BuildInfo
```

**返回值：** `BuildInfo`

---

### getEnvInfo

获取当前浏览器的 WebRTC 能力检测结果，建议在初始化后立即调用。

```typescript
getEnvInfo(): EnvWebInfo
```typescript

**返回值：** `EnvWebInfo`，详见 [EnvWebInfo](/zh/rtc/web/types#envwebinfo)

---

### onNotifyChannelEvent

频道内事件回调，在 `join` 前注册。

```typescript
onNotifyChannelEvent?: ((event: ChannelEvent) => void) | null
```

完整事件类型详见 [事件参考](/zh/rtc/web/events)。

---

### onNotifyImEvent

频道外 IM 事件回调。

```typescript
onNotifyImEvent?: ((event: ImEvent) => void) | null
```typescript

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

**返回值：** `Promise<ChannelInfo>`

---

### leave

主动离开频道，会释放所有已发布轨道。

```typescript
leave(): Promise<void>
```typescript

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
```html

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | :---: | --- |
| `uid` | `string` | 是 | 用户 ID |

---

### getUsersInfo

获取频道内所有用户信息，支持两种返回格式。

```typescript
getUsersInfo(map: true): Record<string, UserInfo>
getUsersInfo(map: false): UserInfo[]
```

---

### getStreamMetric

获取当前流媒体网络质量指标（上下行码率、丢包率等）。

```typescript
getStreamMetric(): Record<string, any> | undefined
```typescript

---

### getDevices

枚举媒体设备列表。

```typescript
getDevices(kind?: MediaDeviceKind, requestPermissions?: boolean): Promise<MediaDeviceInfo[]>
```

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | :---: | --- |
| `kind` | `'audioinput' \| 'audiooutput' \| 'videoinput'` | 否 | 不传则返回所有类型设备 |
| `requestPermissions` | `boolean` | 否 | 是否主动请求麦克风/摄像头权限，默认 `false` |

**返回值：** `Promise<MediaDeviceInfo[]>`

---

### createLocalMicTrack

创建麦克风音频轨道。

```typescript
createLocalMicTrack(preset?: MicPreset): LocalMicTrack
```typescript

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
| `msTrack` | `MediaStreamTrack` | 是 | 音频类型的 MediaStreamTrack |

---

### createLocalCameraTrack

创建摄像头视频轨道。

```typescript
createLocalCameraTrack(preset?: CameraPreset): LocalCameraTrack
```typescript

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | :---: | --- |
| `preset` | `CameraPreset` | 否 | 摄像头预设，默认 `CameraPresets['720p']` |

---

### createLocalScreenTrack

创建屏幕共享视频轨道，可同时请求系统音频采集。

```typescript
createLocalScreenTrack(preset?: ScreenPreset, audioPreset?: ScreenAudioPreset): LocalScreenTrack
```

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | :---: | --- |
| `preset` | `ScreenPreset` | 否 | 视频预设，默认 `ScreenPresets['1080p']` |
| `audioPreset` | `ScreenAudioPreset` | 否 | 系统音频预设，传入后会请求采集系统声音。详见 [屏幕共享](/zh/rtc/web/advanced/screen-sharing) |

---

### createLocalCustomVideoTrack

使用自定义 `MediaStreamTrack` 创建本地视频轨道。

```typescript
createLocalCustomVideoTrack(msTrack: MediaStreamTrack): LocalVideoTrack
```typescript

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | :---: | --- |
| `msTrack` | `MediaStreamTrack` | 是 | 视频类型的 MediaStreamTrack |

---

### publishLocalTrack

将本地轨道发布到频道，发布后远端用户可以订阅。

```typescript
publishLocalTrack(
  track: LocalAudioTrack | LocalVideoTrack,
  opt?: AudioPublishOptions | VideoPublishOptions
): Promise<void>
```

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | :---: | --- |
| `track` | `LocalAudioTrack \| LocalVideoTrack` | 是 | 要发布的本地轨道 |
| `opt` | `AudioPublishOptions \| VideoPublishOptions` | 否 | 发布参数（描述、码率、自定义属性等） |

---

### unpublishLocalTrack

停止发布本地轨道，远端用户将收到 `USER_TRACK_REMOVE` 事件。

```typescript
unpublishLocalTrack(track: LocalAudioTrack | LocalVideoTrack): Promise<void>
```typescript

---

### enableLocalTrack

恢复已暂停的本地轨道的数据发送（轻量操作，推流连接保持）。

```typescript
enableLocalTrack(track: LocalAudioTrack | LocalVideoTrack): Promise<void>
```

> 远端会收到 `TRACK_UNMUTED` 事件。与 `publishLocalTrack` 的区别详见 [静音 vs 停止发布](/zh/rtc/web/advanced/mute-vs-unpublish)。

---

### disableLocalTrack

暂停本地轨道的数据发送（轻量操作，推流连接保持）。

```typescript
disableLocalTrack(track: LocalAudioTrack | LocalVideoTrack): Promise<void>
```typescript

> 远端会收到 `TRACK_MUTED` 事件。与 `unpublishLocalTrack` 的区别详见 [静音 vs 停止发布](/zh/rtc/web/advanced/mute-vs-unpublish)。

---

### subscribeRemoteAudioMixTrack

订阅全频道混音流（一般场景推荐使用此方法接收远端声音）。

```typescript
subscribeRemoteAudioMixTrack(filterUids?: string[]): Promise<RemoteAudioMixTrack>
```

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | :---: | --- |
| `filterUids` | `string[]` | 否 | 需要从混音中排除的用户 ID 列表 |

---

### subscribeRemoteAudioTrack

订阅指定用户的单路音频流。

```typescript
subscribeRemoteAudioTrack(uid: string, id: string): Promise<RemoteAudioTrack>
```typescript

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | :---: | --- |
| `uid` | `string` | 是 | 用户 ID |
| `id` | `string` | 是 | 轨道 ID（从 `TrackInfo.id` 获取） |

---

### subscribeRemoteVideoTrack

订阅指定用户的视频流。

```typescript
subscribeRemoteVideoTrack(uid: string, id: string): Promise<RemoteVideoTrack>
```

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | :---: | --- |
| `uid` | `string` | 是 | 用户 ID |
| `id` | `string` | 是 | 轨道 ID（从 `TrackInfo.id` 获取） |

---

### subscribeRemoteVideoMcuTrack

订阅远端视频合成流（服务端混流合成的单路视频）。

```typescript
subscribeRemoteVideoMcuTrack(): Promise<RemoteVideoTrack>
```typescript

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

通过用户 ID + 轨道 ID 或描述获取已订阅的远端轨道实例。

```typescript
getRemoteTrack(uid: string, id?: string, desc?: string): RemoteAudioTrack | RemoteVideoTrack
```typescript

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | :---: | --- |
| `uid` | `string` | 是 | 用户 ID |
| `id` | `string` | 否 | 轨道 ID，与 `desc` 二选一 |
| `desc` | `string` | 否 | 轨道描述，与 `id` 二选一 |

---

### enableIm

启用频道外 IM 消息功能。

```typescript
enableIm(token: string): Promise<string>
```

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | :---: | --- |
| `token` | `string` | 是 | IM 启用 Token |

**返回值：** `Promise<string>`，返回 IM 会话 sid。

---

### disableIm

关闭频道外 IM 消息功能。

```typescript
disableIm(): Promise<void>
```typescript
