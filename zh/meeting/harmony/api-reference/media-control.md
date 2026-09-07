---
title: "媒体控制接口"
description: "SMeetingEngine 的开麦、摄像头、屏幕共享、订阅与远端音频控制接口"
---

会议 SDK 把「后端授权 → 建轨道 → 采集 → 发布」收成一个调用，
所以这里的接口比直接用 SRTC 少很多步。

所有方法都要求**在会中**，否则抛 `notInMeeting`（`208003`）。

---

## 本地轨道

| 属性 | 类型 | 说明 |
| --- | --- | --- |
| `micTrack` | `LocalMicTrack \| undefined` | 当前麦克风轨道 |
| `cameraTrack` | `LocalCameraTrack \| undefined` | 当前摄像头轨道 |
| `screenTrack` | `LocalScreenTrack \| undefined` | 当前屏幕共享轨道 |
| `mcuTrack` | `RemoteVideoTrack \| undefined` | 当前订阅的 MCU 合流轨道 |

本地预览就是把 `cameraTrack` 交给 `SRTCVideoView`：

```typescript
if (this.meeting.cameraTrack !== undefined) {
  SRTCVideoView({ track: this.meeting.cameraTrack, trackKey: this.meeting.cameraTrack.id })
    .width('100%').height(240)
}
```

---

## 麦克风

```typescript
requestOpenMic(preset?: MicPreset, byAdmin?: boolean, adminUid?: string): Promise<LocalMicTrack>
closeMic(): Promise<void>
setMicMuted(muted: boolean): void
```

| 方法 | 说明 |
| --- | --- |
| `requestOpenMic` | 申请开麦。**会被后端拒绝**（全体静音时） |
| `closeMic` | 关麦，销毁轨道 |
| `setMicMuted` | 通话中临时静音，**不重建轨道** |

<Note>
**`setMicMuted` 与 `closeMic` 的区别很重要：**

+ `setMicMuted(true)` —— 静音但轨道还在，对端仍看到你在会中，切回是瞬时的。
  日常的"静音/取消静音"按钮用这个。
+ `closeMic()` —— 真正关掉，轨道消失。

高频操作用 `setMicMuted`，不要每次都 `closeMic` + `requestOpenMic`。
</Note>

`byAdmin` / `adminUid` 是给「响应主持人请求」用的：收到
`onAdminRequestOpenMic` 后询问用户，同意则带上这两个参数调用，
后端据此知道这是响应请求而非自主开麦。

---

## 摄像头

```typescript
requestOpenCamera(preset?: CameraPreset, byAdmin?: boolean, adminUid?: string): Promise<LocalCameraTrack>
closeCamera(): Promise<void>
switchCamera(cameraId?: string): void
```

`switchCamera()` 不传参数就是前后置切换，传 `deviceId` 切到指定摄像头。

预设可用 SRTC 的 `cameraPreset1080p()` / `cameraPreset720p()` /
`cameraPreset360p()` / `cameraPreset180p()`。

<Note>
摄像头没有 `setMuted` 这种"假关"—— 用户预期关摄像头就该真的关（指示灯熄灭），
所以只有 `closeCamera()`。
</Note>

### 变焦

```typescript
cameraZoomRange(): ZoomRange
setCameraZoom(ratio: number): Promise<void>
currentCameraZoom(): number
```

`currentCameraZoom()` 在摄像头未开或没设过时返回 `1`。`setCameraZoom()` 对超范围的值做夹取而不抛错；摄像头未开或设备不支持时记 warning 后返回。

<Warning>
**`cameraZoomRange()` 反映的是"现在这一刻能不能变焦"，不是设备能力。**

变焦挂在系统的 CaptureSession 上，该 session 只有在**真的有人消费视频帧**时才 active。所以摄像头刚打开、画面还没真正跑起来的那个中间态里，它返回的是 `{ min: 1, max: 1, supported: false }`。

**不要用 `supported` 决定变焦控件的显示与否**，否则控件会在这个常见中间态里莫名消失。详细实测数据见 [SRTC 轨道接口 · 变焦](/zh/rtc/harmony/api-reference/media-tracks#变焦)。
</Warning>

---

## 屏幕共享

```typescript
requestShare(shareType?: ShareType, preset?: ScreenPreset, byAdmin?: boolean, adminUid?: string): Promise<void>
stopShare(): Promise<void>
```

`ShareType` 有 `screen`（屏幕）与 `whiteBoard`（白板）两种。

<Warning>
`requestShare()` 会弹**系统授权窗**，用户点同意之后才真正出帧。
方法返回只代表已发起。UI 上不要在 `await` 返回后立刻显示"正在共享"。

另外鸿蒙的屏幕采集**每次重启都要重新授权**，没有"沿用上次授权"这种待遇。
</Warning>

主持人可以强制停止别人的共享：`adminStopRoomShare()`，见
[会控接口](/zh/meeting/harmony/api-reference/admin-actions)。

---

## 订阅远端视频

```typescript
subscribeRemoteVideoTrack(uid: string, trackDesc?: TrackDesc): Promise<RemoteVideoTrack>
unsubscribeRemoteVideoTrack(uid: string, trackDesc?: TrackDesc, debounceMs?: number): Promise<void>
unsubscribeRemoteVideoTrackIfNoRenderers(uid: string, trackDesc?: TrackDesc, debounceMs?: number): Promise<boolean>
getRemoteVideoTrack(uid: string, trackDesc?: TrackDesc): Track | undefined
```

`trackDesc` 选订哪一路：

| 值 | 用途 |
| --- | --- |
| `cameraBig` | 摄像头大流，**默认** |
| `cameraSmall` | 摄像头小流，宫格视图用 |
| `screen` | 屏幕共享 |

<Note>
**宫格视图用 `cameraSmall`、大窗用 `cameraBig`**，这是控制带宽最直接的手段。
20 个人的宫格全订大流会把下行打满。
</Note>

`unsubscribeRemoteVideoTrack` 的 `debounceMs` 用来抑制列表滚动导致的反复订阅/退订 ——
防抖窗口内重新订阅会取消待执行的退订，所以快速滑动是无感的。

`unsubscribeRemoteVideoTrackIfNoRenderers` 是**守卫版**：只在该轨道已经没有渲染器时
才退订，返回是否真的退了。适合"同一路画面渲染在多处"的场景。

<Warning>
守卫版在 ArkUI 的 `aboutToDisappear` 里**不可靠** —— 父组件的
`aboutToDisappear` 先于子组件执行，此时子 `SRTCVideoView` 还没摘除渲染器，
会永远判成"还有渲染器"而永不退订。详见
[视频渲染](/zh/meeting/harmony/advanced/video-rendering)。
</Warning>

---

## 订阅远端音频

```typescript
subscribeRemoteAudioTrack(uid: string, trackDesc?: TrackDesc): Promise<void>
unsubscribeRemoteAudioTrack(uid: string, trackDesc?: TrackDesc): Promise<void>
```

---

## 远端音频播放控制

```typescript
toggleRemoteAudioMute(mute: boolean): void
toggleUserAudioMute(uid: string, mute: boolean): void
isUserAudioMuted(uid: string): boolean
getMutedAudioUids(): string[]
```

<Note>
这几个只影响**本地播放**，不改变订阅关系 —— 也就是"关扬声器"而不是"退订"。
带宽照旧消耗，但切回来是瞬时的。

| 场景 | 用哪个 |
| --- | --- |
| 用户点了"扬声器关闭" | `toggleRemoteAudioMute(true)` |
| 把某人"本地静音" | `toggleUserAudioMute(uid, true)` |
| 真要省带宽 | `unsubscribeRemoteAudioTrack(uid)` |
</Note>

---

## MCU 合流

```typescript
subscribeRemoteVideoMcu(uid: string): Promise<RemoteVideoTrack>
unsubscribeRemoteVideoMcu(): Promise<void>
```

订阅服务端合成的一路画面，替代 N 路各自订阅。大型会议下这是主要方案 ——
客户端解码开销不随人数线性上升。

布局由 `adminUpdateLayout(layoutData)` 控制。

---

## 音频路由

```typescript
get defaultAudioRoute(): AudioRouteTarget
set defaultAudioRoute(target: AudioRouteTarget)
setAudioRoute(target: AudioRouteTarget): void
```

+ `defaultAudioRoute` —— **持久设置**，长期有效，外设拔出后按它回落
+ `setAudioRoute` —— **临时设置**，优先级更高

详见[音频路由](/zh/meeting/harmony/advanced/audio-routing)。

---

### 相关阅读

+ [SMeetingEngine](/zh/meeting/harmony/api-reference/SMeetingEngine)
+ [会控接口](/zh/meeting/harmony/api-reference/admin-actions)
+ [视频渲染](/zh/meeting/harmony/advanced/video-rendering)
+ [SRTC 轨道接口](/zh/rtc/harmony/api-reference/media-tracks)
