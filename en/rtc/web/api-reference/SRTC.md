---
title: "SRTC"
description: "API reference for SRTC, the Web SDK's main entry class: constructor, joining and leaving channels, channel and user info, network quality queries, device enumeration, creating local tracks, publishing and subscribing, IM, event callbacks, and destroy."
---

SRTC is the main entry point of the Web SDK. Create an instance with `new SRTC(initParams)`.

The channel-level methods on this page (publishing, subscribing, user queries, `leave`, etc.) are **equivalent** to the methods of the same name on the Channel object returned by `join`, and act on the current (default) channel. When you join multiple channels at once, call them on each Channel object instead to specify the target. See [Multi-channel](/en/rtc/web/advanced/multi-channel).

---

### constructor

```typescript
constructor(initParams: SdkInitParams)
```

| Parameter | Type | Required | Description |
| --- | --- | :---: | --- |
| `initParams` | `SdkInitParams` | Yes | Initialization parameters; see [SdkInitParams](/en/rtc/web/types#sdkinitparams) |

---

### buildInfo

Gets the SDK build information.

```typescript
buildInfo(): BuildInfo
```

---

### getEnvInfo

Gets the WebRTC capability detection result for the current browser. We recommend calling it as early as possible after initialization.

```typescript
getEnvInfo(): EnvWebInfo
```

**Returns:** `EnvWebInfo`; see [EnvWebInfo](/en/rtc/web/types#envwebinfo)

---

### onNotifyChannelEvent

In-channel event callback. We recommend registering it before `join`.

```typescript
onNotifyChannelEvent?: ((event: ChannelEvent) => void) | null
```

For the full list of event types, see [Events](/en/rtc/web/events).

---

### onNotifyImEvent

Out-of-channel IM event callback.

```typescript
onNotifyImEvent?: ((event: ImEvent) => void) | null
```

---

### join

Joins a channel and returns that channel's **Channel object**. Get the channel info with `channel.getInfo()`.

```typescript
join(token: string, options?: JoinOptions): Promise<Channel>
```

| Parameter | Type | Required | Description |
| --- | --- | :---: | --- |
| `token` | `string` | Yes | Token for joining the channel, issued by the server |
| `options` | `JoinOptions` | No | Join options; see [JoinOptions](/en/rtc/web/types#joinoptions) |

You can call it multiple times to join several channels at once. Single-channel apps can ignore the return value and keep using the channel-level methods on the `srtc` instance (which act on the current channel). For the Channel object's methods and multi-channel usage, see [Multi-channel](/en/rtc/web/advanced/multi-channel).

> Migrating from older versions: `join` used to return `ChannelInfo` and now returns a Channel object; the old return value is equivalent to `(await srtc.join(token)).getInfo()`.

---

### leave

Leaves the channel. For local tracks, the SDK automatically stops capture, stops playback, or removes play views after leaving.

```typescript
leave(): Promise<void>
```

With multiple channels, it acts on the earliest-joined channel and is equivalent to that channel's `channel.leave()`; to leave a specific channel, call `leave()` on its Channel object directly.

---

### getChannelInfo

Gets the current channel info. Returns `null` when not in a channel.

```typescript
getChannelInfo(): ChannelInfo | null
```

---

### getUserInfo

Gets the info of a given user in the channel.

```typescript
getUserInfo(uid: string): UserInfo
```

| Parameter | Type | Required | Description |
| --- | --- | :---: | --- |
| `uid` | `string` | Yes | User ID |

---

### getUsersInfo

Gets the info of all users in the channel, as either an array or a map.

```typescript
getUsersInfo(map: true): Record<string, UserInfo>
getUsersInfo(map: false): UserInfo[]
```

---

### getStreamMetric

Gets the current full media metric snapshot, including overall network statistics and a `TrackMetric` for each local/remote track.

```typescript
getStreamMetric(): StreamMetric | undefined
```

> Throws if called when not in a channel. For field details, see [Network quality](/en/rtc/web/network-quality).

---

### getNetworkStats

Gets the current overall network statistics. Use it when you only care about the network overview (bitrate, packet loss, RTT, available bandwidth); it's lighter than `getStreamMetric`.

```typescript
getNetworkStats(): NetworkStats | undefined
```

> Throws if called when not in a channel.

---

### getConnectionQuality

Gets the current connection quality evaluation, returning the uplink/downlink levels, the overall level, MOS, and the triggering reasons. The SDK evaluates internally over a 2-second sliding window.

```typescript
getConnectionQuality(): QualityEvaluation | undefined
```

> Throws if called when not in a channel. For apps, we recommend subscribing to the `ChannelEventType.CONNECTION_QUALITY_CHANGED` event to be notified of changes passively.

---

### getDevices

Enumerates media devices.

```typescript
getDevices(kind?: MediaDeviceKind, requestPermissions?: boolean): Promise<MediaDeviceInfo[]>
```

| Parameter | Type | Required | Description |
| --- | --- | :---: | --- |
| `kind` | `'audioinput' \| 'audiooutput' \| 'videoinput'` | No | If omitted, devices of all types are returned |
| `requestPermissions` | `boolean` | No | Whether to request media permissions proactively; defaults to `true` |

---

### createLocalMicTrack

Creates a microphone audio track.

```typescript
createLocalMicTrack(preset?: MicPreset): LocalMicTrack
```

| Parameter | Type | Required | Description |
| --- | --- | :---: | --- |
| `preset` | `MicPreset` | No | Microphone preset; defaults to `MicPresets.music` |

---

### createLocalCustomAudioTrack

Creates a local audio track from a custom `MediaStreamTrack`.

```typescript
createLocalCustomAudioTrack(msTrack: MediaStreamTrack): LocalAudioTrack
```

| Parameter | Type | Required | Description |
| --- | --- | :---: | --- |
| `msTrack` | `MediaStreamTrack` | Yes | An audio `MediaStreamTrack` |

---

### createLocalCameraTrack

Creates a camera video track.

```typescript
createLocalCameraTrack(preset?: CameraPreset): LocalCameraTrack
```

| Parameter | Type | Required | Description |
| --- | --- | :---: | --- |
| `preset` | `CameraPreset` | No | Camera preset; defaults to `CameraPresets['720p']` |

---

### createLocalScreenTrack

Creates a screen sharing video track.

```typescript
createLocalScreenTrack(preset?: ScreenPreset, audioPreset?: ScreenAudioPreset): LocalScreenTrack
```

| Parameter | Type | Required | Description |
| --- | --- | :---: | --- |
| `preset` | `ScreenPreset` | No | Video preset; defaults to `ScreenPresets['1080p']` |
| `audioPreset` | `ScreenAudioPreset` | No | System audio preset; defaults to `ScreenAudioPresets.default` |

> A system audio track is created as well by default. Whether system audio can actually be captured also depends on the browser's capabilities and on whether the user checks "Share audio" in the system sharing dialog.

---

### createLocalCustomVideoTrack

Creates a local video track from a custom `MediaStreamTrack`.

```typescript
createLocalCustomVideoTrack(msTrack: MediaStreamTrack): LocalVideoTrack
```

| Parameter | Type | Required | Description |
| --- | --- | :---: | --- |
| `msTrack` | `MediaStreamTrack` | Yes | A video `MediaStreamTrack` |

---

### createLocalCompositeRecorder

Creates a local composite recorder, used in the browser to composite the video tiles and audio tracks that the current page needs to record into a local recording file.

```typescript
createLocalCompositeRecorder(): LocalCompositeRecorder
```

The returned `LocalCompositeRecorder` is only responsible for media compositing and the `MediaRecorder` lifecycle; your app computes the view—video grids, paging, speaker layout, screen sharing priority, and so on—and passes it in through `videoItems` and `updateVideoItems(...)`.

> For detailed usage, see [Local recording](/en/rtc/web/advanced/local-recording).

---

### publishLocalTrack

Publishes a local track to the channel; after publishing, remote users can subscribe to it.

```typescript
publishLocalTrack(
  track: LocalAudioTrack | LocalVideoTrack,
  opt?: Partial<AudioPublishOptions> | Partial<VideoPublishOptions>
): Promise<TrackInfo>
```

| Parameter | Type | Required | Description |
| --- | --- | :---: | --- |
| `track` | `LocalAudioTrack \| LocalVideoTrack` | Yes | The local track to publish |
| `opt` | `Partial<AudioPublishOptions> \| Partial<VideoPublishOptions>` | No | Publish parameters, merged with the preset parameters given when the track was created |

**Returns:** `TrackInfo`, a snapshot of this publication's track description in the channel; to get the latest value later, use `channel.getPublishInfo(track)`.

<Warning>
Within one channel, only one track per `desc` can be published. Publishing the same `desc` again with **a different** track (for example, a `mic` track is already published and you publish a second `mic`) throws; publishing the same track again is unaffected and remains idempotent.

So serialize entry points such as turning on the microphone or camera yourself: if you publish again before the previous `publishLocalTrack` has finished awaiting, two tracks publish at the same time, and you usually only keep a reference to the one created later, so the one published first can never be unpublished.
</Warning>

---

### unpublishLocalTrack

Unpublishes a local track; remote users receive the `USER_TRACK_REMOVE` event.

```typescript
unpublishLocalTrack(track: LocalAudioTrack | LocalVideoTrack): Promise<void>
```

---

### enableLocalTrack

Resumes sending data for a paused local track.

```typescript
enableLocalTrack(track: LocalAudioTrack | LocalVideoTrack): Promise<void>
```

> Remote users receive the `TRACK_UNMUTED` event. For how it differs from `publishLocalTrack`, see [Mute vs. unpublish](/en/rtc/web/advanced/mute-vs-unpublish).

---

### disableLocalTrack

Pauses sending data for a local track without unpublishing it.

```typescript
disableLocalTrack(track: LocalAudioTrack | LocalVideoTrack): void
```

> Remote users receive the `TRACK_MUTED` event. For how it differs from `unpublishLocalTrack`, see [Mute vs. unpublish](/en/rtc/web/advanced/mute-vs-unpublish).

---

### subscribeRemoteAudioMixTrack

Subscribes to the channel-wide mixed audio track.

```typescript
subscribeRemoteAudioMixTrack(
  filter?: string[] | ((track: BaseTrack) => boolean)
): Promise<RemoteAudioMixTrack>
```

| Parameter | Type | Required | Description |
| --- | --- | :---: | --- |
| `filter` | `string[] \| ((track: BaseTrack) => boolean)` | No | Pass `string[]` to exclude by UID; pass a function to decide per track whether to filter it out |

---

### subscribeRemoteAudioTrack

Subscribes to a single audio stream of a given user.

```typescript
subscribeRemoteAudioTrack(uid: string, id: string): Promise<RemoteAudioTrack>
```

| Parameter | Type | Required | Description |
| --- | --- | :---: | --- |
| `uid` | `string` | Yes | User ID |
| `id` | `string` | Yes | Track ID, available from `TrackInfo.id` |

---

### subscribeRemoteVideoTrack

Subscribes to a given user's video stream.

```typescript
subscribeRemoteVideoTrack(uid: string, id: string): Promise<RemoteVideoTrack>
```

| Parameter | Type | Required | Description |
| --- | --- | :---: | --- |
| `uid` | `string` | Yes | User ID |
| `id` | `string` | Yes | Track ID, available from `TrackInfo.id` |

---

### subscribeRemoteVideoMcuTrack

Subscribes to the remote composite video stream.

```typescript
subscribeRemoteVideoMcuTrack(): Promise<RemoteVideoMcuTrack>
```

> `RemoteVideoMcuTrack` extends `RemoteVideoTrack` and can be used like a regular remote video track.

---

### unsubscribeRemoteTrack

Unsubscribes from a remote stream.

```typescript
unsubscribeRemoteTrack(
  track: RemoteAudioMixTrack | RemoteAudioTrack | RemoteVideoTrack
): Promise<void>
```

---

### getRemoteTrack

Gets a subscribed remote track instance by user ID and either track ID or track description.

```typescript
getRemoteTrack(uid: string, id?: string, desc?: string): RemoteAudioTrack | RemoteVideoTrack
```

| Parameter | Type | Required | Description |
| --- | --- | :---: | --- |
| `uid` | `string` | Yes | User ID |
| `id` | `string` | No | Track ID; pass either this or `desc` |
| `desc` | `string` | No | Track description; pass either this or `id` |

> You must pass at least one of `id` and `desc`; otherwise it throws.

---

### enableIm

Enables out-of-channel IM messages.

```typescript
enableIm(token: string): Promise<string>
```

| Parameter | Type | Required | Description |
| --- | --- | :---: | --- |
| `token` | `string` | Yes | IM enable token |

**Returns:** `Promise<string>`, the IM session `sid`.

---

### disableIm

Disables out-of-channel IM messages.

```typescript
disableIm(): Promise<void>
```

---

### destroy

Fully releases the SRTC instance: leaves all channels in turn, disables IM, and removes the listeners the instance registered on browser global objects (device plug/unplug, page visibility). It's idempotent—repeated calls return immediately; calling the instance's methods afterward throws.

```typescript
destroy(): Promise<void>
```

Without `destroy()`, the global listeners keep holding a reference to the instance so it can't be garbage-collected. So you **must call it** before an SPA route navigates away from the audio/video page, before a component unmounts, or before you create a new SRTC instance; apps whose instance lives as long as the page don't need to call it.

For everyday joining and leaving of channels, `leave()` (or `channel.leave()`) is enough, and the instance can be reused to `join` again.
