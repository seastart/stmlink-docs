---
title: "轨道接口"
description: "SRTC HarmonyOS SDK 的 Track 继承体系、本地采集与远端播放接口"
---

## 继承关系

```
Track
├── LocalTrack
│   ├── LocalAudioTrack ── LocalMicTrack / LocalScreenAudioTrack
│   └── LocalVideoTrack ── LocalCameraTrack / LocalScreenTrack
└── RemoteTrack
    ├── RemoteAudioTrack ── RemoteAudioMixTrack
    └── RemoteVideoTrack
```

本地轨道由 `SRTCEngine.createLocalXxxTrack()` 创建，远端轨道由 SDK 在收到信令后创建、
经 `channel.getRemoteTrack()` 取得。**两边都不要自己 `new`。**

---

## `Track`（基类）

| 成员 | 类型 | 说明 |
| --- | --- | --- |
| `id` | `string` | 轨道 ID |
| `kind` | `TrackKind` | `audio` / `video` |
| `desc` | `string` | 描述，如 `camera` / `screen` / `mic` / `audio_mix` |
| `variant` | `boolean \| undefined` | 是否为 Simulcast 副层 |
| `uid` | `string \| undefined` | 所属用户 |
| `delegates` | `MulticastDelegate<TrackDelegate>` | 事件回调容器 |
| `getInfo()` | `TrackInfo` | 信息**副本** |
| `toString()` | `string` | 调试用 |

<Warning>
`delegates` 是**强引用**，必须成对 `add` / `remove`。
</Warning>

<Note>
`getRtcTrack()` / `setRtcTrack()` / `updateInfo()` / `updatePartialInfo()`
是 SDK 内部接口，业务侧不要调。
</Note>

---

## `LocalTrack`

所有本地轨道的共同部分。

| 成员 | 签名 | 说明 |
| --- | --- | --- |
| `isCapturing` | `boolean`（只读） | 是否正在采集 |
| `isMutedByUser` | `boolean` | 用户是否主动静音过（`restartCapture` 会回放这个状态） |
| `stopCapture()` | `Promise<void>` | 停止采集 |

---

## `LocalAudioTrack`

| 成员 | 签名 | 说明 |
| --- | --- | --- |
| `captureOptions` | `MicCaptureOptions` | 当前采集参数 |
| `defaultPublishOptions` | `AudioPublishOptions \| undefined` | 发布时的默认参数 |
| `startCapture(options?)` | `Promise<void>` | 开始采集 |
| `mute()` / `unmute()` | `void` | 静音 / 取消静音 |
| `isMuted` | `boolean`（只读） | 当前是否静音 |
| `setVolume(v)` | `void` | 设置音量 |
| `restartCapture()` | `Promise<void>` | 重启采集 |
| `changeDeviceId(deviceId)` | `Promise<void>` | 切换麦克风 |

**抛出**：`captureError`（权限未授予、设备被占用等）

<Warning>
**`changeDeviceId` / `restartCapture` 会换一条底层轨道。**

已发布的轨道需要重新发布，正确顺序是：

```typescript
await channel.unpublishLocalAudioTrack(mic);
await mic.changeDeviceId(newId);
await channel.publishLocalAudioTrack(mic);
```

静音状态会自动保留 —— `startCapture` 内部会回放 `isMutedByUser`。
</Warning>

### 子类

| 类 | 说明 |
| --- | --- |
| `LocalMicTrack` | 麦克风。无参构造，经 `srtc.createLocalMicTrack(preset?)` 创建 |
| `LocalScreenAudioTrack` | 屏幕共享里的系统音频。随 `LocalScreenTrack` 一并产生，不要单独创建 |

---

## `LocalVideoTrack`

| 成员 | 签名 | 说明 |
| --- | --- | --- |
| `defaultPublishOptions` | `VideoPublishOptions \| undefined` | 发布默认参数 |
| `captureWidth` / `captureHeight` | `number \| undefined` | **实际**采集尺寸（可能被档位吸附过） |
| `isMirrored` | `boolean`（只读） | 是否镜像 |
| `setMirrored(mirrored)` | `void` | 设置镜像 |
| `addRenderer(r)` | `void` | 挂一个自定义渲染器 |
| `removeRenderer(r)` / `removeAllRenderers()` | `void` | 摘除渲染器 |
| `hasRenderers` / `rendererCount` | 只读 | 渲染器状态 |
| `simulcastTracks` | `Map<string, LocalVideoTrack>` | Simulcast 各层 |
| `getOrCreateSimulcastTrack(trackId, option)` | `LocalVideoTrack` | 取或建某一层 |

<Note>
`captureWidth` / `captureHeight` 与你设定的值**可能不同**：采集分辨率受设备档位限制，
底层会吸附到最近的档位。要看实际值就读这两个字段。
</Note>

用 `SRTCVideoView` 渲染时不需要自己碰 `addRenderer` —— 组件内部已经处理。

### `LocalCameraTrack`

| 成员 | 签名 | 说明 |
| --- | --- | --- |
| `captureOptions` | `CameraCaptureOptions` | 当前采集参数 |
| `startCapture(options?)` | `Promise<void>` | 开始采集 |
| `switchCamera(cameraId?)` | `void` | 前后置切换；传 ID 可切到指定摄像头 |
| `changeDeviceId(deviceId)` | `void` | 切换摄像头 |
| `restartCapture()` | `Promise<void>` | 重启采集 |
| `zoomRange()` | `ZoomRange` | 当前可用的变焦范围 |
| `setZoom(ratio)` | `Promise<void>` | 设置变焦倍率 |
| `currentZoom()` | `number` | 当前倍率，没设过时返回 `1` |

```typescript
const camera = srtc.createLocalCameraTrack(cameraPreset720p());
await camera.startCapture();
await channel.publishLocalVideoTrack(camera);
```

#### 变焦

```typescript
// ⚠️ 要在发布之后调
await channel.publishLocalVideoTrack(camera);

const range = camera.zoomRange();   // 例如 { min: 0.67, max: 6, supported: true }
await camera.setZoom(2);
```

<Warning>
**`zoomRange()` 返回的是"现在这一刻能不能变焦"，不是"这台设备支不支持变焦"。**

变焦范围与变焦设置都挂在系统的 CaptureSession 上，而该 session 只有在**真的有人在消费视频帧**时才处于 active 状态。同一台设备、同一条轨道的真机实测：

| 状态 | `zoomRange()` |
| --- | --- |
| 只 `startCapture()`、没有任何消费者 | `{ min: 1, max: 1, supported: false }` |
| 轨道已发布、正在编码出帧 | `{ min: 0.67, max: 6, supported: true }` |

因此：

+ **变焦要在轨道发布之后（或已挂上渲染之后）调**，光 `startCapture()` 不够；
+ UI 上**不要用 `supported` 决定变焦控件的显示与否** —— 在"开了摄像头但还没发布"这个很常见的中间态里它是 `false`，控件会莫名消失。
</Warning>

<Note>
`setZoom()` 在不支持或超范围时**不抛错**：相机变焦是连续调节，手势滑到端点是常态，抛错会让调用方每次都得自己判边界。超范围的值会被夹到范围内。

排障看 `hdc shell hilog -x | grep -a SetZoomRatio`，native 侧三种结果各有日志：`clamped=`（已生效）、`ignored: zoom not supported by device`、`ignored: capture session not active`。
</Note>

### `LocalScreenTrack`

| 成员 | 签名 | 说明 |
| --- | --- | --- |
| `captureOptions` | `ScreenCaptureOptions` | 屏幕采集参数 |
| `audioCaptureOptions` | `ScreenAudioCaptureOptions \| undefined` | 系统音频采集参数 |
| `audioPublishOptions` | `AudioPublishOptions \| undefined` | 系统音频发布参数 |
| `audioTrack` / `getAudioTrack()` | `LocalAudioTrack \| undefined` | 系统音频轨道 |

```typescript
const screen = srtc.createLocalScreenTrack(screenPreset1080p(), screenAudioPresetDefault());
await screen.startCapture();                          // 弹系统授权窗
await channel.publishLocalVideoTrack(screen);
const sysAudio = screen.audioTrack;
if (sysAudio !== undefined) {
  await channel.publishLocalAudioTrack(sysAudio);      // 系统音频要单独发布
}
```

详见[屏幕共享](/zh/rtc/harmony/advanced/screen-sharing)。

---

## `RemoteAudioTrack`

| 成员 | 签名 | 说明 |
| --- | --- | --- |
| `isPlaying` | `boolean`（只读） | 是否正在播放 |
| `startPlay()` / `stopPlay()` | `void` | 开始 / 停止本地播放 |

<Note>
`stopPlay()` 只停**本地播放**，不退订 —— 带宽照旧消耗，但切回来是瞬时的。
要真正省带宽得用 `channel.unsubscribeRemoteTrack()`。

按用户维度控制播放更方便的做法是
`channel.setUserAudioPlayback(uid, enabled)`。
</Note>

### `RemoteAudioMixTrack`

云端混音轨道。SeaStart 引擎在服务端把多路音频混成一路下发，客户端只订阅这一条，
省掉 N 路解码。

| 成员 | 签名 | 说明 |
| --- | --- | --- |
| `getFilterUids()` | `string[]` | 非空表示只混这些用户的音频 |

轨道 `id` 与 `desc` 固定是 `audio_mix`，与其它端一致 —— 服务端按这个字符串识别混音轨。

---

## `RemoteVideoTrack`

| 成员 | 签名 | 说明 |
| --- | --- | --- |
| `addRenderer(r)` | `void` | 挂渲染器 |
| `removeRenderer(r)` / `removeAllRenderers()` | `void` | 摘除渲染器 |
| `hasRenderers` / `rendererCount` | 只读 | 渲染器状态 |

用 `SRTCVideoView` 时不需要自己管：

```typescript
ForEach(this.tiles, (tile: Tile) => {
  SRTCVideoView({
    track: channel.getRemoteTrack(tile.uid, tile.trackId),
    trackKey: tile.trackId
  })
}, (tile: Tile) => tile.trackId)
```

---

## 渲染层

### `SRTCVideoView`

ArkUI 自定义组件。参数：

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `track` | `Track \| undefined` | 要渲染的轨道 |
| `trackKey` | `string` | 轨道标识，通常传 `track.id` |

另有 `ScalingMode` 控制填充方式。

<Warning>
**`track` 必须是普通成员变量，不能声明成 `@Prop`。**

ArkTS 的 `@Prop` 对复杂类型做**深拷贝**，且拷贝过程中除基本类型 / Map / Set / Date /
Array 之外**会丢失类型** —— `Track` 拷过来会变成一个没有方法的普通对象，
结果是画面黑屏、事件也永远收不到。

`@Link` / `@ObjectLink` 能引用传递，但要求父组件为每一路画面单独持有一个 `@State`，
多路远端画面写不出来。所以轨道走普通成员变量按引用传入，**换轨道靠组件重建** ——
让 `if` 分支或 `ForEach` 的 key 带上 trackId。
</Warning>

<Note>
**surface 与轨道的生命周期不同步，两个方向都要考虑：**

1. **surface 比轨道晚到**：远端轨道是信令先建对象、订阅协商完成后才绑底层轨道；
   本地轨道则可能在组件挂载前就采集好了。
2. **surface 会重建**：切后台、旋屏都会走一遍 destroy → create。

组件内部已经处理了这两种情况（挂载时主动挂一次 + 监听 `onTrackBindRtcTrack` 补挂），
但前提是**保持同一个组件实例** —— 不要每次 `build` 都换 key。
</Note>

### `SRTCVideoRenderer` / `VideoRendererRegistry`

需要自己接渲染（画到自定义画布、做录制等）时用这一层。`VideoRendererRegistry`
维护 trackKey → 渲染器的映射，`SRTCVideoView` 内部走的也是它。

绝大多数业务不需要碰这层。

---

### 相关阅读

+ [静音与停止发布](/zh/rtc/harmony/advanced/mute-vs-unpublish) —— `mute` 与 `unpublish` 该用哪个
+ [设备管理](/zh/rtc/harmony/advanced/device-management)
+ [SRTCEngine 与 Channel](/zh/rtc/harmony/api-reference/SRTCEngine)
+ [类型定义](/zh/rtc/harmony/types)
