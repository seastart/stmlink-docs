---
title: "快速开始"
description: "在 HarmonyOS 应用中用 SRTC 完成加入频道、推流、订阅远端画面的最小流程"
---

本文用最小代码跑通一次音视频通话：加入频道 → 开麦 → 开摄像头 → 订阅远端画面 → 离会。

开始之前请先完成 [集成方式](/zh/rtc/harmony/integration) 中的依赖声明、权限配置与 `SRTC.init`。

---

### 调用序列总览

```
加入频道    srtc.joinChannel(token, { autoSubscribeAudio: true })
            channel.delegates.add(delegate)

开麦        srtc.createLocalMicTrack() → track.startCapture()
                                      → channel.publishLocalAudioTrack(track)
            之后开关麦用 mute() / unmute()，不要重建轨道

开摄像头    srtc.createLocalCameraTrack() → track.startCapture()
                                          → channel.publishLocalVideoTrack(track)

订阅远端    channel.subscribeRemoteVideoTrack(uid, trackId)
            → channel.getRemoteTrack(uid, trackId) 交给 SRTCVideoView

离会        srtc.leaveChannel()
```

---

### 第一步：创建引擎

`SRTCEngine` 是无参构造，日志级别通过属性设置：

```typescript
import { SRTCEngine, LogLevel } from 'srtc';

const srtc: SRTCEngine = new SRTCEngine();
srtc.logLevel = LogLevel.info;
```

---

### 第二步：加入频道

Token 由**你的业务后端**签发，SDK 不负责发号。

```typescript
import { Channel, JoinOptions } from 'srtc';

const options: JoinOptions = {
  autoSubscribeAudio: true,   // 入会后自动收音频
  autoSubscribeVideo: false   // 视频按需订阅，见第五步
};

const channel: Channel = await srtc.joinChannel(token, options);
```

<Warning>
`autoSubscribeAudio` 与 `autoSubscribeVideo` **默认都是 `false`**，即入会后不会自动收流。这与部分同类 SDK 的默认值相反，典型现象是"入会成功但听不到、看不到别人"。
</Warning>

---

### 第三步：监听频道事件

```typescript
import { ChannelDelegate, UserInfo, TrackInfo, TrackKind, DisconnectReason } from 'srtc';

const delegate: ChannelDelegate = {
  onJoinSucceed: (ch, info) => {
    console.info(`加入成功：${info.channel}`);
  },
  onUserJoin: (ch, user: UserInfo) => {
    console.info(`${user.uid} 加入`);
  },
  onUserLeave: (ch, uid: string, reason: DisconnectReason) => {
    console.info(`${uid} 离开`);
  },
  onTrackAdded: (ch, user: UserInfo, track: TrackInfo) => {
    // 远端有新流可订阅
    if (track.kind === TrackKind.video) {
      this.subscribeVideo(user.uid, track);
    }
  },
  onTrackRemoved: (ch, user: UserInfo, track: TrackInfo) => {
    // 远端流已移除，把对应画面从 UI 上摘掉
  },
  onDisconnected: (ch, reason: DisconnectReason, error?: Error) => {
    console.warn(`连接断开：${reason}`);
  }
};

channel.delegates.add(delegate);
```

<Warning>
**`delegates` 是强引用，必须成对 `add` / `remove`。**

ArkTS 没有弱引用，也没有 `deinit`。注册后不摘除会导致监听者永不回收，而且离开页面后仍然收到回调。通常在组件的 `aboutToAppear` / `aboutToDisappear` 里配对处理：

```typescript
aboutToDisappear(): void {
  channel.delegates.remove(delegate);
}
```
</Warning>

---

### 第四步：推送本地音视频

#### 开麦

```typescript
import { LocalMicTrack, micPresetMusic } from 'srtc';

const mic: LocalMicTrack = srtc.createLocalMicTrack(micPresetMusic());
await mic.startCapture();
await channel.publishLocalAudioTrack(mic);
```

之后开关麦不要重建轨道，用静音开关即可：

```typescript
mic.mute();     // 关麦
mic.unmute();   // 开麦
```

#### 开摄像头

```typescript
import { LocalCameraTrack, cameraPreset720p } from 'srtc';

const camera: LocalCameraTrack = srtc.createLocalCameraTrack(cameraPreset720p());
await camera.startCapture();
await channel.publishLocalVideoTrack(camera);
```

关摄像头与关麦不同，走"停止发布 + 停止采集"，而不是静音：

```typescript
await channel.unpublishLocalVideoTrack(camera);
await camera.stopCapture();
```

<Note>
麦克风用 `mute()` 而摄像头用 `unpublish` + `stopCapture`，是因为两者的用户预期不同：静音时对方应当仍看到你在会中，而关摄像头时摄像头指示灯必须真的熄灭。
</Note>

---

### 第五步：渲染画面

`SRTCVideoView` 是 SDK 提供的 ArkUI 组件，视频帧由底层直接写进 XComponent 的 surface。

#### 本地预览

```typescript
if (this.cameraTrack !== undefined) {
  SRTCVideoView({ track: this.cameraTrack, trackKey: this.cameraTrack.id })
    .width('100%')
    .height(240)
}
```

#### 订阅并渲染远端

```typescript
// 订阅
await channel.subscribeRemoteVideoTrack(uid, trackInfo.id);

// 取到轨道交给组件
const remote: Track | undefined = channel.getRemoteTrack(uid, trackInfo.id);
```

多路远端画面用 `ForEach`，**key 必须带上 trackId**：

```typescript
ForEach(this.tiles, (tile: Tile) => {
  SRTCVideoView({
    track: channel.getRemoteTrack(tile.uid, tile.trackId),
    trackKey: tile.trackId
  })
}, (tile: Tile) => tile.trackId)
```

<Warning>
**`track` 是普通成员变量，不能声明成 `@Prop`。**

ArkTS 的 `@Prop` 对复杂类型做**深拷贝**，且拷贝过程中除基本类型 / Map / Set / Date / Array 之外**会丢失类型** —— `Track` 拷过来会变成一个没有方法的普通对象，结果是画面黑屏、事件也收不到。

轨道要**按引用**传入，换轨道靠组件重建（`if` 分支切换或 `ForEach` 的 key 带上 trackId）。
</Warning>

---

### 第六步：离会与清理

```typescript
await srtc.leaveChannel();
channel.delegates.remove(delegate);
```

ArkTS 没有析构函数，委托、定时器、采集都必须显式收掉，否则会出现"页面永不回收 + 摄像头指示灯一直亮"。

---

### 自测建议

+ **本地预览不需要服务端**：只做"创建摄像头轨道 → `startCapture` → `SRTCVideoView`"就能验证采集与渲染是否正常，模拟器上也能跑（本地预览不经过硬件编码器）。
+ **发布与订阅必须在真机上验证**：所有视频预设都用 H264，而 H264 只有硬编、没有软编兜底，模拟器上编码器建不出来。
+ **不要以"看到画面"作为通过标准**：缺少 H264 硬编能力的设备会静默退回 VP8，表现为和其它端互通不上。请确认实际协商到的编码格式。

---

### 下一步

+ [集成方式](/zh/rtc/harmony/integration) —— 环境要求与权限配置
+ [更新日志](/zh/rtc/harmony/changelog) —— 版本变更记录
