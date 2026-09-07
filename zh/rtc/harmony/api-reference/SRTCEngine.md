---
title: "SRTCEngine 与 Channel"
description: "SRTC HarmonyOS SDK 主入口 SRTCEngine 与频道对象 Channel 的接口说明"
---

## `SRTC`

只做一件事：把宿主的 Context 交给 SDK。

### `SRTC.init(context)`

```typescript
static init(context: common.Context): void
```

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `context` | `common.Context` | 通常传 `UIAbility` 的 `this.context` |

在 `UIAbility.onCreate` 里调用一次。

<Warning>
不调用**不会报错**，但摄像头档位查询拿不到 Context，分辨率会退化为"由底层自行吸附档位"，
你在 `CameraPreset` 里设定的值不再生效。
</Warning>

### `SRTC.context`

```typescript
static get context(): common.Context | undefined
```

返回 `undefined` 表示没有调用过 `init()`。

---

## `SRTCEngine`

SDK 主入口。**无参构造**。

```typescript
const srtc: SRTCEngine = new SRTCEngine();
srtc.logLevel = LogLevel.info;
```

### 属性

| 属性 | 类型 | 读写 | 说明 |
| --- | --- | --- | --- |
| `SRTCEngine.version` | `string` | 静态只读 | SDK 版本，等同导出的 `SRTC_VERSION` |
| `channels` | `Channel[]` | 只读 | 当前存活的频道，按加入先后排序 |
| `defaultChannel` | `Channel \| undefined` | 只读 | 最早加入的频道 |
| `deviceId` | `string` | 只读 | 本机设备 ID（上报用） |
| `deviceType` | `DeviceType` | 只读 | 恒为 `DeviceType.harmonyOS`（`8`） |
| `logLevel` | `LogLevel` | 读写 | 日志级别 |

<Note>
`SRTCEngine` **没有** `dispose()`。要释放资源就 `leaveChannel()` 并把注册过的
delegate 逐一 `remove`。
</Note>

### `joinChannel(tokenString, options?)`

加入频道。

```typescript
joinChannel(tokenString: string, options?: JoinOptions): Promise<Channel>
```

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `tokenString` | `string` | 是 | Base64 编码的频道 Token，由**业务后端**签发 |
| `options` | `JoinOptions` | 否 | 入会选项，见[类型定义](/zh/rtc/harmony/types) |

**返回**：`Promise<Channel>`

**抛出**：`tokenExpired` / `tokenInvalid` / `alreadyJoined` / `apiRequestFailed` /
`signalingConnectFailed`

可以调用多次加入多个频道，各频道互不干扰。

<Warning>
`options.autoSubscribeAudio` 与 `autoSubscribeVideo` **默认都是 `false`**，
入会后不会自动收流。典型现象是"入会成功但听不到、看不到别人"。
</Warning>

### `leaveChannel()`

```typescript
leaveChannel(): Promise<void>
```

离开**默认频道**（最早加入的那个）。

### `leaveChannelInstance(channel)`

```typescript
leaveChannelInstance(channel: Channel): Promise<void>
```

离开指定频道。多频道场景用这个。

### `createLocalMicTrack(preset?)`

```typescript
createLocalMicTrack(preset?: MicPreset): LocalMicTrack
```

创建麦克风轨道。不传 `preset` 用默认参数。

<Note>
创建 ≠ 采集 ≠ 发布。拿到轨道后还要 `startCapture()`，要让对端看到 / 听到还要
`channel.publishLocalAudioTrack()`。
</Note>

### `createLocalCameraTrack(preset?)`

```typescript
createLocalCameraTrack(preset?: CameraPreset): LocalCameraTrack
```

创建摄像头轨道。可选预设：`cameraPreset1080p()` / `cameraPreset720p()` /
`cameraPreset360p()` / `cameraPreset180p()`。

<Note>
`LocalCameraTrack` 本身是**无参构造**，预设必须经引擎传入 ——
`new LocalCameraTrack(preset)` 编不过。
</Note>

### `createLocalScreenTrack(preset?, audioPreset?)`

```typescript
createLocalScreenTrack(preset?: ScreenPreset, audioPreset?: ScreenAudioPreset): LocalScreenTrack
```

创建屏幕采集轨道。传了 `audioPreset` 时会同时采集系统音频，通过
`screenTrack.audioTrack` 取到那条音频轨。

`startCapture()` 会弹出系统授权窗，用户同意后才出帧。

### `enableIm(tokenString)` / `disableIm()`

```typescript
enableIm(tokenString: string): Promise<Im>
disableIm(): Promise<void>
```

开启 / 关闭频道 IM 通道。`Im` 对象上注册 `ImDelegate` 收消息。

<Note>
IM 是**只收不发**的：SDK 提供 `onImMessage` 回调，但没有发送接口 ——
发消息由业务后端负责。频道内自定义消息（`onCustomMessage`）同理。
</Note>

---

## `Channel`

一次已经完成鉴权和网络连接的 RTC 会话。由 `joinChannel` 返回，不要自己构造。

### 属性

| 属性 | 类型 | 说明 |
| --- | --- | --- |
| `token` | `ChannelToken` | 本次入会用的 Token（已解析） |
| `delegates` | `MulticastDelegate<ChannelDelegate>` | 事件回调容器 |
| `connectState` | `ConnectionState` | **信令面**连接状态 |
| `mediaState` | `MediaConnectionState` | **媒体面**连接状态（PeerConnection），与 `connectState` 相互独立 |
| `channelInfo` | `ChannelInfo \| undefined` | 频道信息 |
| `me` | `User \| undefined` | 自己 |
| `streamVendor` | `StreamVendor` | 当前流媒体引擎，排障用 |

<Warning>
`delegates` 是**强引用**，必须成对 `add` / `remove`。ArkTS 没有弱引用也没有 `deinit`，
漏掉会导致监听者永不回收、且离开页面后仍收到回调。
</Warning>

### 发布

```typescript
publishLocalAudioTrack(track: LocalAudioTrack, options?: AudioPublishOptions): Promise<void>
publishLocalVideoTrack(track: LocalVideoTrack, options?: VideoPublishOptions): Promise<void>
unpublishLocalAudioTrack(track: LocalAudioTrack): Promise<void>
unpublishLocalVideoTrack(track: LocalVideoTrack): Promise<void>
publishedTracks(): Track[]
```

不传 `options` 时用轨道的 `defaultPublishOptions`（预设里带的那份）。

**抛出**：`trackAlreadyPublished` / `trackNotPublished` / `transportNotReady` /
`maxPublishLimitReached`

<Note>
**轨道属于引擎而不是频道** —— 同一条采集轨道可以发布给多个频道，采集只做一次。
</Note>

### 订阅

```typescript
subscribeRemoteAudioTrack(uid: string, trackId: string): Promise<void>
subscribeRemoteVideoTrack(uid: string, trackId: string): Promise<void>
unsubscribeRemoteTrack(track: Track, debounceMs: number): Promise<void>
getRemoteTrack(uid: string, trackId: string): Track | undefined
getRemoteTrackByDesc(uid: string, desc: string): Track | undefined
```

`uid` + `trackId` 来自 `onTrackAdded` 回调里的 `UserInfo` 与 `TrackInfo`。

`unsubscribeRemoteTrack` 的 `debounceMs` 用来抑制"快速滑动列表导致的反复订阅/退订"——
传 0 表示立即退订。

<Note>
拿到 `Track` 对象**不等于已经有帧**。远端轨道是信令先建对象、订阅协商完成后才绑定底层
轨道，渲染时机看 `onTrackBindRtcTrack`（`SRTCVideoView` 内部已处理）。
</Note>

### Simulcast

```typescript
switchLayer(pubUid: string, trackId: string, targetTrackId: string): void
getSubscribeHit(uid: string, trackId: string): string | undefined
```

`switchLayer` 主动切到指定层（大流 / 小流）。`getSubscribeHit` 返回当前实际命中的
轨道 ID —— 服务端可能因带宽自动降级，这个值才是真相。

切换结果通过 `onLayerSwitched` 回调上报。

### 远端音频播放控制

```typescript
setRemoteAudioPlayback(enabled: boolean): void
setUserAudioPlayback(uid: string, enabled: boolean): void
isUserAudioMuted(uid: string): boolean
getMutedAudioUids(): string[]
```

这几个只影响**本地播放**，不改变订阅关系 —— 也就是"关扬声器"而不是"退订"。
带宽照旧消耗，但切回来是瞬时的。

### 成员

```typescript
getUsers(): Map<string, UserInfo>
getUser(uid: string): User | undefined
getInfo(): ChannelInfo | undefined
```

### 质量

```typescript
getConnectionQuality(): QualityEvaluation | undefined
```

主动查询当前连接质量。做 UI 指示器更建议监听 `onConnectionQualityChange`，
它已经做过等级判定与抖动抑制。

### 统计

```typescript
getStats(): Promise<RtcStatsSnapshot>
logStats(): Promise<void>
rawStatsTypeCounts(): Promise<string>
```

采集一次**本端** WebRTC 统计，返回 [`RtcStatsSnapshot`](/zh/rtc/harmony/types#rtcstatssnapshot)。

与 `getConnectionQuality()` / `onQualityReport` 的分工：

| | 来源 | 覆盖范围 |
| --- | --- | --- |
| `QualityReport` | SFU 通过控制面下发 | **只有 SeaStart 引擎**，服务端视角 |
| `getStats()` | 本端观察 PeerConnection | **两条引擎都有**，本端视角 |

所以网宿 CDN 路径上想拿到任何质量数据，只有 `getStats()` 这一条路；而"我实际编码出来是多少分辨率""编码器是被 CPU 还是被带宽限住了"这类问题服务端根本答不了，也只有这一条路。

`logStats()` 是排障快捷入口，采集一次并按每行一路流打成日志。

<Warning>
**首次调用的码率恒为 0。** 码率由两次采集之间的字节差算出，没有上一次快照就没有差分区间。要展示码率就周期性调用，**1 秒一次**比较合适；排障时连着调两次、看第二次。
</Warning>

<Note>
**上新机型或升级底层库后先跑 `rawStatsTypeCounts()`。** 底层 `webrtc.d.ts` 没有声明 `outbound-rtp` 等类型的字段，native 侧究竟填了哪些未经约定。类型缺失时上面所有统计读出来都是 `undefined`，**而且不报错**。
</Note>

### 离开

```typescript
leave(): Promise<void>
```

一般用 `srtc.leaveChannel()` / `srtc.leaveChannelInstance(channel)`，
它们会同时维护引擎侧的频道列表。

<Note>
`Channel` 上还有 `refresh()` / `leaveWithReason()` / `onDisconnect` /
`isTrackPublishedInOtherChannel` 等成员，那些是 **SDK 内部**在用的，业务侧不要调。
</Note>

---

## `User`

频道成员。由 `channel.getUser(uid)` 取得。

| 成员 | 说明 |
| --- | --- |
| `uid` / `sid` / `linkId` | 标识 |
| `getInfo(): UserInfo` | 信息副本 |
| `getTrack(id)` / `getTrackByDesc(desc)` / `getTracks()` | 该成员的轨道 |

---

### 相关阅读

+ [轨道接口](/zh/rtc/harmony/api-reference/media-tracks)
+ [事件参考](/zh/rtc/harmony/events)
+ [类型定义](/zh/rtc/harmony/types)
+ [多频道](/zh/rtc/harmony/advanced/multi-channel)
