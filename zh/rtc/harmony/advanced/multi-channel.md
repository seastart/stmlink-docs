---
title: "多频道"
description: "一个引擎同时加入多个频道、轨道跨频道共享、以及默认频道的顺延规则"
---

一个 `SRTCEngine` 可以同时加入多个频道。多次 `joinChannel` 各返回独立的 `Channel`
句柄，**发布 / 订阅 / 成员 / 事件 / 离会都在各自的频道上进行，互不干扰**。

```typescript
const chA: Channel = await srtc.joinChannel(tokenA, { autoSubscribeAudio: true });
const chB: Channel = await srtc.joinChannel(tokenB, { autoSubscribeAudio: true });

srtc.channels;          // [chA, chB]，按加入先后排序
srtc.defaultChannel;    // chA
```

只有**同名频道**重复加入才抛 `alreadyJoined`。

---

### 轨道属于引擎，不属于频道

这是多频道最重要的一条：**同一条采集轨道可以发布给多个频道，采集只做一次。**

```typescript
const camera = srtc.createLocalCameraTrack(cameraPreset720p());
await camera.startCapture();          // 只采集一次

await chA.publishLocalVideoTrack(camera);
await chB.publishLocalVideoTrack(camera);   // 同一条轨道，发给两个频道
```

摄像头只被打开一次，编码也只做一份，省的是最贵的那部分开销。

回收由**最后一个释放者**负责：

```typescript
await chA.unpublishLocalVideoTrack(camera);   // chB 还在发，采集继续
await chB.unpublishLocalVideoTrack(camera);   // 都不发了
await camera.stopCapture();                   // 这时才真正关摄像头
```

<Note>
SDK 内部有"某本地轨是否仍被其它存活频道发布着"的判定，所以某个频道离会时不会误关
还在别处使用的采集轨。业务侧只要保证自己 `stopCapture` 的时机正确即可。
</Note>

---

### 音频没有跨频道约束

<Note>
**这是 HarmonyOS 与 iOS / macOS 的一处实质差别，别照那边的经验推。**

iOS / macOS 上所有音频源必须先混成一路再发（那边的 WebRTC 音频源不提供推流接口、
整个进程只有一个音频输入口），代价是麦克风、自定义音频、屏幕音频三者共用一路发送，
多频道时还会互相串音 —— 所以那边有"各频道的音频源集合必须相同"这条硬约束。

鸿蒙这边**每条音频轨道有独立的 `AudioSource`**，各自带音量控制，所以：

+ 按轨道静音就是把自己的源音量设 0，不影响别的轨道
+ **多频道各发各的，不存在共用一份混音导致的跨频道泄漏**
+ 对端看到几路音频就是几路，语义直白

也就是说：你可以给频道 A 只发麦克风、给频道 B 发麦克风 + 屏幕音频，没有限制。
</Note>

---

### 默认频道的顺延规则

`srtc.leaveChannel()` 的**无参**版本作用于**默认频道** —— 最早加入且仍存活的那个。
它离会后，默认频道顺延到下一个。

```typescript
// chA, chB 都在
await srtc.leaveChannel();     // 离开 chA；此后 defaultChannel 变成 chB
await srtc.leaveChannel();     // 离开 chB
```

<Warning>
**多频道场景不要用无参的 `leaveChannel()`。**

"顺延"这个行为在有多个频道时很容易读错，写成循环更是灾难。请显式指定：

```typescript
await srtc.leaveChannelInstance(chB);
```

单频道使用者感知不到这条规则，可以继续用 `leaveChannel()`。
</Warning>

---

### 事件要按频道区分

所有 `ChannelDelegate` 回调的**第一个参数都是 `channel`**，多频道时必须用它区分来源：

```typescript
const delegate: ChannelDelegate = {
  onUserJoin: (channel: Channel, user: UserInfo) => {
    const name = channel.token.channel;      // 哪个频道
    console.info(`[${name}] ${user.uid} 加入`);
  }
};

chA.delegates.add(delegate);
chB.delegates.add(delegate);                 // 同一个 delegate 可以复用
```

同一个 delegate 对象注册到多个频道是可以的 —— 靠第一个参数分流。
但记得**每个频道都要单独 `remove`**。

---

### 状态与 UI 的组织

多频道下最容易出问题的是状态管理。几条经验：

+ 每个 `Channel` 一份独立的 UI 状态（成员列表、画面列表），不要合并成一个大列表
+ 用 `channel.token.channel`（频道名）或自己维护的 key 做索引
+ 渲染多路画面时 `ForEach` 的 key 要**同时包含频道标识和 trackId**，
  否则两个频道里同名 trackId 会撞

```typescript
ForEach(this.tiles, (tile: Tile) => {
  SRTCVideoView({
    track: tile.channel.getRemoteTrack(tile.uid, tile.trackId),
    trackKey: `${tile.channelName}:${tile.trackId}`
  })
}, (tile: Tile) => `${tile.channelName}:${tile.trackId}`)
```

<Warning>
ArkTS 的 `@Observed` **只观测第一层属性的赋值**。频道列表、画面列表这类数组
永远用「建新数组再整体赋值」，不要 `push` / `splice` 原数组 —— 那样 UI 不会刷新。
</Warning>

---

### 相关阅读

+ [SRTCEngine 与 Channel](/zh/rtc/harmony/api-reference/SRTCEngine)
+ [静音与停止发布](/zh/rtc/harmony/advanced/mute-vs-unpublish)
+ [核心概念](/zh/rtc/harmony/key-concepts)
