### 继承关系

```
BaseTrack
├── LocalAudioTrack          ← 本地音频基类（自定义音频流）
│   └── LocalMicTrack        ← 麦克风流
├── LocalVideoTrack          ← 本地视频基类（自定义视频流）
│   ├── LocalCameraTrack     ← 摄像头流
│   └── LocalScreenTrack     ← 屏幕共享流（含系统音频）
├── RemoteAudioTrack         ← 远端单路音频流
│   └── RemoteAudioMixTrack  ← 远端全频道混音流
└── RemoteVideoTrack         ← 远端视频流
```

---

## BaseTrack

所有轨道的基类，提供轨道元信息访问。

#### id

```typescript
get id(): string
```

轨道 ID，在频道内唯一标识该轨道。

#### kind

```typescript
get kind(): TrackKind
```

轨道类型：`'audio'` 或 `'video'`。

#### desc

```typescript
get desc(): string
```

轨道描述，由发布时指定（如 `'camera_big'`、`'screen'`）。

#### getInfo

获取完整轨道信息（分辨率、码率、采样率等）。

```typescript
getInfo(): TrackInfo
```

**返回值：** `TrackInfo`，详见 [类型定义](/zh/rtc/web/types#trackinfo)

#### getUid

获取轨道所属用户的 UID。

```typescript
getUid(): string
```

#### getMediaStreamTrack

获取底层 `MediaStreamTrack`（可用于自定义处理，如 Web Audio API 接入）。

```typescript
getMediaStreamTrack(): MediaStreamTrack | undefined
```

---

## LocalAudioTrack

本地音频轨道基类，也用于自定义音频流（通过 `srtc.createLocalCustomAudioTrack` 创建）。

继承自 `BaseTrack`。

#### startPlay

播放音频（本地监听，可用于测试麦克风是否采集到声音）。

```typescript
startPlay(opt?: AudioOutputOptions): Promise<void>
```

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | :---: | --- |
| `opt` | `AudioOutputOptions` | 否 | 播放配置，可指定扬声器设备 |

#### stopPlay

停止播放，释放对播放设备的占用。

```typescript
stopPlay(): void
```

#### getVolume

获取当前音频输入音量（0 ~ 100）。

```typescript
getVolume(): number
```

#### isPlaying

当前是否正在播放。

```typescript
isPlaying(): boolean
```

---

## LocalMicTrack

本地麦克风轨道，继承自 `LocalAudioTrack`，通过 `srtc.createLocalMicTrack` 创建。

#### startCapture

开始采集，会向用户请求麦克风权限。

```typescript
startCapture(opt?: MicCaptureOptions): Promise<void>
```

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | :---: | --- |
| `opt` | `MicCaptureOptions` | 否 | 采集配置，可指定设备 ID、回声消除等 |

#### stopCapture

停止采集，释放麦克风设备。

```typescript
stopCapture(): void
```

#### changeDeviceId

热切换麦克风设备（无需停止采集）。

```typescript
changeDeviceId(deviceId: string): Promise<void>
```

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | :---: | --- |
| `deviceId` | `string` | 是 | 目标设备 ID（从 `getDevices('audioinput')` 获取） |

---

## LocalVideoTrack

本地视频轨道基类，也用于自定义视频流（通过 `srtc.createLocalCustomVideoTrack` 创建）。

继承自 `BaseTrack`。

#### addPlayView

将视频渲染到指定 HTML 容器元素。

```typescript
addPlayView(container: HTMLElement): void
```

#### hasPlayView

判断是否已有渲染容器。

```typescript
hasPlayView(): boolean
```

#### removePlayView

移除指定渲染容器。

```typescript
removePlayView(container: HTMLElement): void
```

#### removeAllPlayViews

移除所有渲染容器。

```typescript
removeAllPlayViews(): void
```

#### getSimulcastTrack

获取联播（Simulcast）模式下的指定清晰度轨道（需发布时配置了 Simulcast）。

```typescript
getSimulcastTrack(layer: 'high' | 'medium' | 'low'): MediaStreamTrack | undefined
```

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | :---: | --- |
| `layer` | `'high' \| 'medium' \| 'low'` | 是 | 清晰度层级 |

---

## LocalCameraTrack

本地摄像头视频轨道，继承自 `LocalVideoTrack`，通过 `srtc.createLocalCameraTrack` 创建。

#### startCapture

开始采集，会向用户请求摄像头权限。

```typescript
startCapture(opt?: CameraCaptureOptions): Promise<void>
```

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | :---: | --- |
| `opt` | `CameraCaptureOptions` | 否 | 采集配置，可指定设备 ID、分辨率、帧率 |

#### stopCapture

停止采集，释放摄像头设备。

```typescript
stopCapture(): void
```

#### changeDeviceId

热切换摄像头设备（无需停止采集）。

```typescript
changeDeviceId(deviceId: string): Promise<void>
```

#### switchFacingMode

在前置/后置摄像头之间切换（仅移动端）。

```typescript
switchFacingMode(): Promise<void>
```

---

## LocalScreenTrack

本地屏幕共享视频轨道，继承自 `LocalVideoTrack`，通过 `srtc.createLocalScreenTrack` 创建。

#### startCapture

开始屏幕采集，浏览器会弹出屏幕选择弹窗。

```typescript
startCapture(opt?: ScreenCaptureOptions): Promise<void>
```

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | :---: | --- |
| `opt` | `ScreenCaptureOptions` | 否 | 采集配置，可指定分辨率、帧率、内容提示 |

#### stopCapture

停止屏幕采集。

```typescript
stopCapture(): void
```

#### getAudioTrack

获取同时采集的系统音频轨道。仅当 `createLocalScreenTrack` 传入了 `audioPreset` 且浏览器支持时有效。

```typescript
getAudioTrack(): LocalAudioTrack | undefined
```

> 详细用法见 [屏幕共享 - 同时采集系统音频](/zh/rtc/web/advanced/screen-sharing#同时采集系统音频)

---

## RemoteAudioTrack

远端单路音频轨道，通过 `srtc.subscribeRemoteAudioTrack` 订阅。

继承自 `BaseTrack`。

#### startPlay

播放远端音频。

```typescript
startPlay(opt?: AudioOutputOptions): Promise<void>
```

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | :---: | --- |
| `opt` | `AudioOutputOptions` | 否 | 可指定扬声器设备 |

#### stopPlay

停止播放，释放对播放设备的占用。

```typescript
stopPlay(): void
```

---

## RemoteAudioMixTrack

远端全频道混音流，继承自 `RemoteAudioTrack`，通过 `srtc.subscribeRemoteAudioMixTrack` 订阅。

大多数场景下只需要订阅这一路混音流，而无需订阅每个用户的单独音频流。

#### getFilterUids

获取当前从混音中排除的用户 ID 列表。

```typescript
getFilterUids(): string[]
```

继承了 `RemoteAudioTrack` 的 `startPlay` / `stopPlay` 方法。

---

## RemoteVideoTrack

远端视频轨道，通过 `srtc.subscribeRemoteVideoTrack` 订阅。

继承自 `BaseTrack`。

#### addPlayView

将远端视频渲染到指定 HTML 容器元素。

```typescript
addPlayView(container: HTMLElement): void
```

#### hasPlayView

判断是否已有渲染容器。

```typescript
hasPlayView(): boolean
```

#### removePlayView

移除指定渲染容器。

```typescript
removePlayView(container: HTMLElement): void
```

#### removeAllPlayViews

移除所有渲染容器。

```typescript
removeAllPlayViews(): void
```
