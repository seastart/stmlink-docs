---
title: "media-tracks"
description: "Web SRTC 音视频 SDK media-tracks 接口参考"
---

### 继承关系

```typescript
BaseTrack
├── LocalAudioTrack           ← 本地音频基类（自定义音频流）
│   ├── LocalMicTrack         ← 麦克风流
│   └── LocalScreenAudioTrack ← 屏幕共享附带的系统音频流
├── LocalVideoTrack           ← 本地视频基类（自定义视频流）
│   ├── LocalCameraTrack      ← 摄像头流
│   └── LocalScreenTrack      ← 屏幕共享视频流
├── RemoteAudioTrack          ← 远端单路音频流
│   └── RemoteAudioMixTrack   ← 远端全频道混音流
└── RemoteVideoTrack          ← 远端视频流
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

轨道描述，由发布时指定，例如 `'camera_big'`、`'screen'`。

#### getInfo

获取完整轨道信息，例如分辨率、码率、采样率等。

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

获取底层 `MediaStreamTrack`，可用于 Web Audio API、自定义后处理等场景。

```typescript
getMediaStreamTrack(): MediaStreamTrack | undefined
```

---

## LocalAudioTrack

本地音频轨道基类，也用于自定义音频流，例如 `srtc.createLocalCustomAudioTrack(...)` 的返回值。

继承自 `BaseTrack`。

#### startPlay

播放音频，可用于本地监听。

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

获取当前音频输入音量，范围 `0 ~ 100`。

```typescript
getVolume(): number
```

#### isPlaying

当前是否正在播放。

```typescript
isPlaying(): boolean
```

#### setProcessor

挂载音频处理器（如 RNN 降噪、变声）。需先 `startCapture` 采集到轨道后调用；传入数组时按顺序串联。已发布的轨道也可挂载，SDK 会免重协商地切换；切换设备后处理器会自动重挂。详见[音视频处理器](/zh/rtc/web/advanced/audio-processor)。

```typescript
setProcessor(processor: TrackProcessor | TrackProcessor[]): Promise<void>
```

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | :---: | --- |
| `processor` | `TrackProcessor \| TrackProcessor[]` | 是 | 处理器实例，或按顺序串联的处理器数组 |

#### removeProcessor

卸载已挂载的处理器，还原为原始采集轨道并释放处理器资源。

```typescript
removeProcessor(): Promise<void>
```

---

## LocalMicTrack

本地麦克风轨道，继承自 `LocalAudioTrack`，通过 `srtc.createLocalMicTrack` 创建。

#### startCapture

开始采集，会向用户请求麦克风权限。

```typescript
startCapture(opt?: Partial<MicCaptureOptions>): Promise<void>
```

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | :---: | --- |
| `opt` | `Partial<MicCaptureOptions>` | 否 | 采集配置，可指定设备 ID、回声消除等 |

#### stopCapture

停止采集，释放麦克风设备。

```typescript
stopCapture(): void
```

#### changeDeviceId

热切换麦克风设备。

```typescript
changeDeviceId(deviceId: string): Promise<void>
```

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | :---: | --- |
| `deviceId` | `string` | 是 | 目标设备 ID，可通过 `getDevices('audioinput')` 获取 |

---

## LocalScreenAudioTrack

屏幕共享附带的系统音频轨道，继承自 `LocalAudioTrack`。

这个类通常不直接手动创建，而是通过 `LocalScreenTrack.getAudioTrack()` 获取。

#### stopCapture

停止系统音频采集。

```typescript
stopCapture(): void
```

> 其余播放相关方法继承自 `LocalAudioTrack`，例如 `startPlay()`、`stopPlay()`、`isPlaying()`。

---

## LocalVideoTrack

本地视频轨道基类，也用于自定义视频流，例如 `srtc.createLocalCustomVideoTrack(...)` 的返回值。

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

#### enterPictureInPicture

让指定容器对应的视频进入画中画模式。

```typescript
enterPictureInPicture(container: HTMLElement, options?: PipOptions): Promise<PipHandle>
```

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | :---: | --- |
| `container` | `HTMLElement` | 是 | 已通过 `addPlayView` 绑定的视频容器 |
| `options` | `PipOptions` | 否 | 画中画配置，可指定窗口尺寸、是否优先使用 Document PiP、是否隐藏原始视图 |

> 默认优先使用 Document PiP。若浏览器不支持，会自动降级到传统 `video.requestPictureInPicture()`。

#### exitPictureInPicture

退出指定容器的画中画模式。

```typescript
exitPictureInPicture(container: HTMLElement): Promise<void>
```

#### isPictureInPicture

判断指定容器是否处于画中画模式。

```typescript
isPictureInPicture(container: HTMLElement): boolean
```

#### popOutToWindow

将指定容器对应的视频弹出到独立浏览器窗口。

```typescript
popOutToWindow(container: HTMLElement, options?: PopOutOptions): PopOutHandle
```

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | :---: | --- |
| `container` | `HTMLElement` | 是 | 已通过 `addPlayView` 绑定的视频容器 |
| `options` | `PopOutOptions` | 否 | 弹窗配置，可指定窗口尺寸、标题、是否隐藏原始视图 |

#### closePopOutWindow

关闭指定容器对应的弹出窗口。

```typescript
closePopOutWindow(container: HTMLElement): void
```

#### isPopOut

判断指定容器是否已经弹出到独立窗口。

```typescript
isPopOut(container: HTMLElement): boolean
```

#### getSimulcastTrack

基于给定的联播发布参数创建或获取一个联播子轨道。

```typescript
getSimulcastTrack(opt: VideoPublishOptions, owidth?: number, oheight?: number): LocalVideoTrack
```

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | :---: | --- |
| `opt` | `VideoPublishOptions` | 是 | 联播子轨道的发布参数，`desc` 不能为空 |
| `owidth` | `number` | 否 | 原始视频宽度，用于计算编码缩放比例 |
| `oheight` | `number` | 否 | 原始视频高度，用于计算编码缩放比例 |

#### setProcessor

挂载视频处理器（如美颜、虚化背景）。需先 `startCapture` 采集到轨道后调用；传入数组时按顺序串联。已发布的轨道也可挂载，SDK 会免重协商地切换；切换设备后处理器会自动重挂。详见[音视频处理器](/zh/rtc/web/advanced/audio-processor)。

```typescript
setProcessor(processor: TrackProcessor | TrackProcessor[]): Promise<void>
```

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | :---: | --- |
| `processor` | `TrackProcessor \| TrackProcessor[]` | 是 | 处理器实例，或按顺序串联的处理器数组 |

#### removeProcessor

卸载已挂载的处理器，还原为原始采集轨道并释放处理器资源。

```typescript
removeProcessor(): Promise<void>
```

> 对于 `LocalCameraTrack`、`LocalScreenTrack` 和 `RemoteVideoTrack`，以上 PiP / 弹窗方法均可使用。
>
> 当 `options.hideOriginView` 为 `true`（默认值）时：
> - `Document PiP` 和 `弹出窗口` 会隐藏主页面中的原始播放视图，避免双重渲染
> - 传统 `video PiP` 仍依赖原始 `video` 元素，因此不会隐藏原始视图

---

## LocalCameraTrack

本地摄像头视频轨道，继承自 `LocalVideoTrack`，通过 `srtc.createLocalCameraTrack` 创建。

#### startCapture

开始采集，会向用户请求摄像头权限。

```typescript
startCapture(opt?: Partial<CameraCaptureOptions>): Promise<void>
```

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | :---: | --- |
| `opt` | `Partial<CameraCaptureOptions>` | 否 | 采集配置，可指定设备 ID、分辨率、帧率 |

#### stopCapture

停止采集，释放摄像头设备。

```typescript
stopCapture(): void
```

#### changeDeviceId

热切换摄像头设备。

```typescript
changeDeviceId(deviceId: string): Promise<void>
```

#### switchFacingMode

在前置/后置摄像头之间切换，仅移动端生效。

```typescript
switchFacingMode(): Promise<void>
```

---

## LocalScreenTrack

本地屏幕共享视频轨道，继承自 `LocalVideoTrack`，通过 `srtc.createLocalScreenTrack` 创建。

#### startCapture

开始屏幕采集，浏览器会弹出屏幕选择窗口。

```typescript
startCapture(opt?: Partial<ScreenCaptureOptions>): Promise<void>
```

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | :---: | --- |
| `opt` | `Partial<ScreenCaptureOptions>` | 否 | 采集配置，可指定分辨率、帧率、`contentHint` 等 |

#### stopCapture

停止屏幕采集。

```typescript
stopCapture(): void
```

#### getAudioTrack

获取同时采集的系统音频轨道。仅当 `createLocalScreenTrack` 传入了 `audioPreset` 且浏览器支持时有效。

```typescript
getAudioTrack(): LocalScreenAudioTrack | undefined
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

#### isPlaying

当前是否正在播放。

```typescript
isPlaying(): boolean
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

> 播放相关方法继承自 `RemoteAudioTrack`，例如 `startPlay()`、`stopPlay()`、`isPlaying()`。

---

## RemoteVideoTrack

远端视频轨道，通过 `srtc.subscribeRemoteVideoTrack` 订阅。

继承自 `BaseTrack`。

#### setJitterBufferTarget

设置接收端抗抖动缓冲的目标延迟，单位 ms。

```typescript
setJitterBufferTarget(ms?: number): void
```

参数说明：

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | :---: | --- |
| `ms` | `number` | 否 | 目标延迟。`0` 表示低延迟优先，`200` 到 `500` 这类较大值更偏向平滑播放；不传或传 `undefined` 表示清除设置，回到浏览器默认自适应策略。 |

> 该能力依赖浏览器 WebRTC 接收端实现。Chrome / Edge 会优先使用 `jitterBufferTarget`，并兼容旧的 `playoutDelayHint`；Firefox / Safari 不支持时会静默忽略。

#### getJitterBufferTarget

获取当前设置的接收端抗抖动缓冲目标延迟。

```typescript
getJitterBufferTarget(): number | undefined
```

返回值为当前业务设置的目标延迟，单位 ms；返回 `undefined` 表示未设置，使用浏览器默认自适应策略。

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

#### enterPictureInPicture

让指定容器对应的远端视频进入画中画模式。

```typescript
enterPictureInPicture(container: HTMLElement, options?: PipOptions): Promise<PipHandle>
```

#### exitPictureInPicture

退出指定容器的画中画模式。

```typescript
exitPictureInPicture(container: HTMLElement): Promise<void>
```

#### isPictureInPicture

判断指定容器是否处于画中画模式。

```typescript
isPictureInPicture(container: HTMLElement): boolean
```

#### popOutToWindow

将远端视频弹出到独立窗口。

```typescript
popOutToWindow(container: HTMLElement, options?: PopOutOptions): PopOutHandle
```

#### closePopOutWindow

关闭指定容器对应的弹出窗口。

```typescript
closePopOutWindow(container: HTMLElement): void
```

#### isPopOut

判断指定容器是否已经弹出到独立窗口。

```typescript
isPopOut(container: HTMLElement): boolean
```
