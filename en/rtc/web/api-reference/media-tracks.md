---
title: "media-tracks"
description: "API reference for the Web SDK's local and remote track classes: the class hierarchy, BaseTrack metadata, capture and device switching, playback and play views, picture-in-picture and pop-out windows, simulcast sub-tracks, processors, mirroring, and jitter buffer control."
---

### Class hierarchy

```typescript
BaseTrack
├── LocalAudioTrack           ← Local audio base class (custom audio stream)
│   ├── LocalMicTrack         ← Microphone stream
│   └── LocalScreenAudioTrack ← System audio stream that comes with screen sharing
├── LocalVideoTrack           ← Local video base class (custom video stream)
│   ├── LocalCameraTrack      ← Camera stream
│   └── LocalScreenTrack      ← Screen sharing video stream
├── RemoteAudioTrack          ← Single remote audio stream
│   └── RemoteAudioMixTrack   ← Remote channel-wide mixed audio stream
└── RemoteVideoTrack          ← Remote video stream
```

---

## BaseTrack

Base class of all tracks, providing access to track metadata.

#### id

```typescript
get id(): string
```

Track ID, uniquely identifying the track within the channel.

#### kind

```typescript
get kind(): TrackKind
```

Track type: `'audio'` or `'video'`.

#### desc

```typescript
get desc(): string
```

Track description, specified when publishing, such as `'camera_big'` or `'screen'`.

#### getInfo

Gets the full track info, such as resolution, bitrate, and sample rate.

```typescript
getInfo(): TrackInfo
```

**Returns:** `TrackInfo`; see [Types](/en/rtc/web/types#trackinfo)

> When a local track is published to multiple channels at once, the same track has separate track info in each channel. In that case `getInfo()` throws; use `channel.getPublishInfo(track)` instead to query the track info in a given channel. See [Multi-channel](/en/rtc/web/advanced/multi-channel).

#### getUid

Gets the UID of the user who owns the track.

```typescript
getUid(): string
```

#### getMediaStreamTrack

Gets the underlying `MediaStreamTrack`, for scenarios such as the Web Audio API or custom post-processing.

```typescript
getMediaStreamTrack(): MediaStreamTrack | undefined
```

---

## LocalAudioTrack

Base class for local audio tracks, also used for custom audio streams, such as the return value of `srtc.createLocalCustomAudioTrack(...)`.

Extends `BaseTrack`.

#### startPlay

Plays the audio, for local monitoring.

```typescript
startPlay(opt?: AudioOutputOptions): Promise<void>
```

| Parameter | Type | Required | Description |
| --- | --- | :---: | --- |
| `opt` | `AudioOutputOptions` | No | Playback options; can specify the speaker device |

#### stopPlay

Stops playback and releases the playback device.

```typescript
stopPlay(): void
```

#### getVolume

Gets the current audio input volume, in the range 0–100.

```typescript
getVolume(): number
```

#### isPlaying

Whether it's currently playing.

```typescript
isPlaying(): boolean
```

#### setProcessor

Attaches an audio processor (such as RNN noise suppression or voice changing). Call it after `startCapture` has produced a track; when you pass an array, the processors are chained in order. Published tracks can also have processors attached, and the SDK switches without renegotiation; after a device switch, processors are reattached automatically. See [Audio/video processors](/en/rtc/web/advanced/audio-processor).

```typescript
setProcessor(processor: TrackProcessor | TrackProcessor[]): Promise<void>
```

| Parameter | Type | Required | Description |
| --- | --- | :---: | --- |
| `processor` | `TrackProcessor \| TrackProcessor[]` | Yes | A processor instance, or an array of processors chained in order |

#### removeProcessor

Detaches the attached processor, restores the original captured track, and releases processor resources.

```typescript
removeProcessor(): Promise<void>
```

---

## LocalMicTrack

Local microphone track, extends `LocalAudioTrack`, created with `srtc.createLocalMicTrack`.

#### startCapture

Starts capture and requests microphone permission from the user.

```typescript
startCapture(opt?: Partial<MicCaptureOptions>): Promise<void>
```

| Parameter | Type | Required | Description |
| --- | --- | :---: | --- |
| `opt` | `Partial<MicCaptureOptions>` | No | Capture options; can specify the device ID, echo cancellation, etc. |

#### stopCapture

Stops capture and releases the microphone device.

```typescript
stopCapture(): void
```

#### changeDeviceId

Hot-switches the microphone device.

```typescript
changeDeviceId(deviceId: string): Promise<void>
```

| Parameter | Type | Required | Description |
| --- | --- | :---: | --- |
| `deviceId` | `string` | Yes | Target device ID, available from `getDevices('audioinput')` |

---

## LocalScreenAudioTrack

System audio track that comes with screen sharing, extends `LocalAudioTrack`.

You usually don't create this class manually; get it through `LocalScreenTrack.getAudioTrack()`.

#### stopCapture

Stops system audio capture.

```typescript
stopCapture(): void
```

> The other playback methods are inherited from `LocalAudioTrack`, such as `startPlay()`, `stopPlay()`, and `isPlaying()`.

---

## LocalVideoTrack

Base class for local video tracks, also used for custom video streams, such as the return value of `srtc.createLocalCustomVideoTrack(...)`.

Extends `BaseTrack`.

#### addPlayView

Renders the video into the given HTML container element.

```typescript
addPlayView(container: HTMLElement): void
```

#### hasPlayView

Checks whether there's already a render container.

```typescript
hasPlayView(): boolean
```

#### removePlayView

Removes the given render container.

```typescript
removePlayView(container: HTMLElement): void
```

#### removeAllPlayViews

Removes all render containers.

```typescript
removeAllPlayViews(): void
```

#### enterPictureInPicture

Puts the video of the given container into picture-in-picture mode.

```typescript
enterPictureInPicture(container: HTMLElement, options?: PipOptions): Promise<PipHandle>
```

| Parameter | Type | Required | Description |
| --- | --- | :---: | --- |
| `container` | `HTMLElement` | Yes | A video container already bound via `addPlayView` |
| `options` | `PipOptions` | No | Picture-in-picture options; can specify the window size, whether to prefer Document PiP, and whether to hide the original view |

> Document PiP is preferred by default. If the browser doesn't support it, it falls back automatically to the traditional `video.requestPictureInPicture()`.

#### exitPictureInPicture

Exits picture-in-picture mode for the given container.

```typescript
exitPictureInPicture(container: HTMLElement): Promise<void>
```

#### isPictureInPicture

Checks whether the given container is in picture-in-picture mode.

```typescript
isPictureInPicture(container: HTMLElement): boolean
```

#### popOutToWindow

Pops the video of the given container out to a separate browser window.

```typescript
popOutToWindow(container: HTMLElement, options?: PopOutOptions): PopOutHandle
```

| Parameter | Type | Required | Description |
| --- | --- | :---: | --- |
| `container` | `HTMLElement` | Yes | A video container already bound via `addPlayView` |
| `options` | `PopOutOptions` | No | Pop-out options; can specify the window size, title, and whether to hide the original view |

#### closePopOutWindow

Closes the pop-out window of the given container.

```typescript
closePopOutWindow(container: HTMLElement): void
```

#### isPopOut

Checks whether the given container has been popped out to a separate window.

```typescript
isPopOut(container: HTMLElement): boolean
```

#### getSimulcastTrack

Creates or gets a simulcast sub-track based on the given simulcast publish parameters.

```typescript
getSimulcastTrack(opt: VideoPublishOptions, owidth?: number, oheight?: number): LocalVideoTrack
```

| Parameter | Type | Required | Description |
| --- | --- | :---: | --- |
| `opt` | `VideoPublishOptions` | Yes | Publish parameters of the simulcast sub-track; `desc` can't be empty |
| `owidth` | `number` | No | Original video width, used to compute the encoding scale factor |
| `oheight` | `number` | No | Original video height, used to compute the encoding scale factor |

#### setProcessor

Attaches a video processor (such as a beauty filter or background blur). Call it after `startCapture` has produced a track; when you pass an array, the processors are chained in order. Published tracks can also have processors attached, and the SDK switches without renegotiation; after a device switch, processors are reattached automatically. See [Audio/video processors](/en/rtc/web/advanced/audio-processor).

```typescript
setProcessor(processor: TrackProcessor | TrackProcessor[]): Promise<void>
```

| Parameter | Type | Required | Description |
| --- | --- | :---: | --- |
| `processor` | `TrackProcessor \| TrackProcessor[]` | Yes | A processor instance, or an array of processors chained in order |

#### removeProcessor

Detaches the attached processor, restores the original captured track, and releases processor resources.

```typescript
removeProcessor(): Promise<void>
```

> The PiP / pop-out methods above are all available on `LocalCameraTrack`, `LocalScreenTrack`, and `RemoteVideoTrack`.
>
> When `options.hideOriginView` is `true` (the default):
> - `Document PiP` and `pop-out windows` hide the original play view on the main page to avoid double rendering
> - Traditional `video PiP` still relies on the original `video` element, so the original view isn't hidden

---

## LocalCameraTrack

Local camera video track, extends `LocalVideoTrack`, created with `srtc.createLocalCameraTrack`.

#### startCapture

Starts capture and requests camera permission from the user.

```typescript
startCapture(opt?: Partial<CameraCaptureOptions>): Promise<void>
```

| Parameter | Type | Required | Description |
| --- | --- | :---: | --- |
| `opt` | `Partial<CameraCaptureOptions>` | No | Capture options; can specify the device ID, resolution, and frame rate |

#### stopCapture

Stops capture and releases the camera device.

```typescript
stopCapture(): void
```

#### changeDeviceId

Hot-switches the camera device.

```typescript
changeDeviceId(deviceId: string): Promise<void>
```

#### switchFacingMode

Switches between the front and rear cameras; only takes effect on mobile.

```typescript
switchFacingMode(): Promise<void>
```

#### setMirror

Sets the mirroring switch for the local preview. The front camera is mirrored by default (like looking in a mirror), which you can adjust here; the rear camera doesn't support mirroring, and calling this has no effect.

Mirroring only affects rendering of the local preview (including picture-in-picture and pop-out windows) and **doesn't change the published data or the video remote users see**. Switching between front and rear cameras recalculates the mirroring state automatically and keeps the user's on/off preference for the front camera.

```typescript
setMirror(enabled: boolean): void
```

| Parameter | Type | Required | Description |
| --- | --- | :---: | --- |
| `enabled` | `boolean` | Yes | Whether to enable mirroring |

#### isMirrored

Returns whether it's currently mirrored (front camera with mirroring on). Always `false` for the rear camera; you can use it to reflect the current mirroring state in the UI.

```typescript
isMirrored(): boolean
```

#### isFrontFacing

Checks whether the current camera is the front camera. A `facingMode` specified explicitly at capture is the most reliable; if unspecified, it's treated as front.

```typescript
isFrontFacing(): boolean
```

---

## LocalScreenTrack

Local screen sharing video track, extends `LocalVideoTrack`, created with `srtc.createLocalScreenTrack`.

#### startCapture

Starts screen capture; the browser shows a screen picker.

```typescript
startCapture(opt?: Partial<ScreenCaptureOptions>): Promise<void>
```

| Parameter | Type | Required | Description |
| --- | --- | :---: | --- |
| `opt` | `Partial<ScreenCaptureOptions>` | No | Capture options; can specify resolution, frame rate, `contentHint`, etc. |

#### stopCapture

Stops screen capture.

```typescript
stopCapture(): void
```

#### getAudioTrack

Gets the system audio track captured at the same time. Only valid when `audioPreset` was passed to `createLocalScreenTrack` and the browser supports it.

```typescript
getAudioTrack(): LocalScreenAudioTrack | undefined
```

> For detailed usage, see [Screen sharing - Capture system audio at the same time](/en/rtc/web/advanced/screen-sharing#capture-system-audio-at-the-same-time)

---

## RemoteAudioTrack

Single remote audio track, subscribed with `srtc.subscribeRemoteAudioTrack`.

Extends `BaseTrack`.

#### startPlay

Plays the remote audio.

```typescript
startPlay(opt?: AudioOutputOptions): Promise<void>
```

| Parameter | Type | Required | Description |
| --- | --- | :---: | --- |
| `opt` | `AudioOutputOptions` | No | Can specify the speaker device |

#### stopPlay

Stops playback and releases the playback device.

```typescript
stopPlay(): void
```

#### isPlaying

Whether it's currently playing.

```typescript
isPlaying(): boolean
```

#### setJitterBufferTarget

Sets the target delay of the receiver's jitter buffer, in ms.

```typescript
setJitterBufferTarget(ms?: number): void
```

Parameters:

| Parameter | Type | Required | Description |
| --- | --- | :---: | --- |
| `ms` | `number` | No | Target delay. `0` prioritizes low latency, while larger values such as `200` to `500` favor smooth playback; omitting it or passing `undefined` clears the setting and returns to the browser's default adaptive strategy. |

Not set by default; the browser adapts on its own. You generally don't need to adjust it; use it only when you have explicit playback latency requirements.

> This relies on the browser's WebRTC receiver implementation. Chrome / Edge prefer `jitterBufferTarget` and remain compatible with the older `playoutDelayHint`; Firefox / Safari silently ignore it when unsupported.

#### getJitterBufferTarget

Gets the currently set target delay of the receiver's jitter buffer.

```typescript
getJitterBufferTarget(): number | undefined
```

The return value is the target delay currently set by your app, in ms; `undefined` means it isn't set and the browser's default adaptive strategy is used.

---

## RemoteAudioMixTrack

Remote channel-wide mixed audio track, extends `RemoteAudioTrack`, subscribed with `srtc.subscribeRemoteAudioMixTrack`.

In most scenarios you only need to subscribe to this one mixed track, without subscribing to each user's individual audio stream.

#### getFilterUids

Gets the list of user IDs currently excluded from the mix.

```typescript
getFilterUids(): string[]
```

> Playback methods are inherited from `RemoteAudioTrack`, such as `startPlay()`, `stopPlay()`, and `isPlaying()`.

---

## RemoteVideoTrack

Remote video track, subscribed with `srtc.subscribeRemoteVideoTrack`.

Extends `BaseTrack`.

#### setJitterBufferTarget

Sets the target delay of the receiver's jitter buffer, in ms.

```typescript
setJitterBufferTarget(ms?: number): void
```

Parameters:

| Parameter | Type | Required | Description |
| --- | --- | :---: | --- |
| `ms` | `number` | No | Target delay. `0` prioritizes low latency, while larger values such as `200` to `500` favor smooth playback; omitting it or passing `undefined` clears the setting and returns to the browser's default adaptive strategy. |

> This relies on the browser's WebRTC receiver implementation. Chrome / Edge prefer `jitterBufferTarget` and remain compatible with the older `playoutDelayHint`; Firefox / Safari silently ignore it when unsupported.

#### getJitterBufferTarget

Gets the currently set target delay of the receiver's jitter buffer.

```typescript
getJitterBufferTarget(): number | undefined
```

The return value is the target delay currently set by your app, in ms; `undefined` means it isn't set and the browser's default adaptive strategy is used.

#### addPlayView

Renders the remote video into the given HTML container element.

```typescript
addPlayView(container: HTMLElement): void
```

#### hasPlayView

Checks whether there's already a render container.

```typescript
hasPlayView(): boolean
```

#### removePlayView

Removes the given render container.

```typescript
removePlayView(container: HTMLElement): void
```

#### removeAllPlayViews

Removes all render containers.

```typescript
removeAllPlayViews(): void
```

#### enterPictureInPicture

Puts the remote video of the given container into picture-in-picture mode.

```typescript
enterPictureInPicture(container: HTMLElement, options?: PipOptions): Promise<PipHandle>
```

#### exitPictureInPicture

Exits picture-in-picture mode for the given container.

```typescript
exitPictureInPicture(container: HTMLElement): Promise<void>
```

#### isPictureInPicture

Checks whether the given container is in picture-in-picture mode.

```typescript
isPictureInPicture(container: HTMLElement): boolean
```

#### popOutToWindow

Pops the remote video out to a separate window.

```typescript
popOutToWindow(container: HTMLElement, options?: PopOutOptions): PopOutHandle
```

#### closePopOutWindow

Closes the pop-out window of the given container.

```typescript
closePopOutWindow(container: HTMLElement): void
```

#### isPopOut

Checks whether the given container has been popped out to a separate window.

```typescript
isPopOut(container: HTMLElement): boolean
```
