---
title: "多频道"
description: "同时加入多个频道：join 返回的 Channel 对象怎么用、事件如何按频道隔离、一条采集轨发布到多个频道时如何查询各频道内的轨道信息"
---

### 概述

Web SDK 支持一个 SRTC 实例**同时加入多个频道**，典型场景如：在会议频道收发音视频的同时，加入一个语音对讲频道单独收发对讲音频。

```typescript
const meeting = await srtc.join(meetingToken);   // 会议频道
const intercom = await srtc.join(intercomToken); // 对讲频道，两者并行

await meeting.publishLocalTrack(cameraTrack);
await intercom.publishLocalTrack(micTrack);

await intercom.leave();   // 退出对讲，会议不受影响
```

`join` 的返回值就是频道操作句柄（Channel 对象），发布、订阅、成员查询、事件监听、离会都在它上面进行，多个频道互不干扰。

### Channel 对象

Channel 对象的频道级方法与 `srtc` 实例上的同名方法**语义完全一致**（参数与返回值见 [SRTC API 参考](/zh/rtc/web/api-reference/SRTC)），只是把操作目标从"当前频道"变成了这个具体频道：

| 分类 | 方法 |
| --- | --- |
| 信息查询 | `getInfo()`、`getUsersInfo(map)` |
| 发布 | `publishLocalTrack(track, opt?)`、`unpublishLocalTrack(track)`、`getPublishInfo(track)` |
| 订阅 | `subscribeRemoteAudioMixTrack` / `subscribeRemoteAudioTrack` / `subscribeRemoteVideoTrack` / `subscribeRemoteVideoMcuTrack` / `unsubscribeRemoteTrack` |
| 质量统计 | `getStreamMetric()`、`getNetworkStats()`、`getConnectionQuality()` |
| 事件 | `onNotifyEvent` 回调属性、`on()` / `once()` / `off()` 类型化监听 |
| 离会 | `leave()` |

Channel 对象只能由 `srtc.join()` 创建，不允许 `new`。

### 事件按频道隔离

每个频道的事件在各自的 Channel 对象上抛出，二选一：

```typescript
// 方式一：回调属性（与 srtc.onNotifyChannelEvent 一样的判别联合）
intercom.onNotifyEvent = (evt) => {
  switch (evt.type) {
    case ChannelEventType.USER_TRACK_ADD:
      // 只会收到对讲频道的事件
      break;
  }
};

// 方式二：类型化监听单个事件
meeting.on(ChannelEventType.CONNECTION_QUALITY_CHANGED, (evt) => { ... });
```

`srtc.onNotifyChannelEvent` 仍然可用：它收到**默认频道**（见下节）的频道事件，外加设备插拔等与频道无关的设备级事件。多频道应用建议频道事件一律走 `channel.onNotifyEvent`，`srtc.onNotifyChannelEvent` 只留给设备级事件。

### 单频道兼容：默认频道规则

`srtc` 实例上的频道级方法（`publishLocalTrack`、`subscribe*`、`getChannelInfo`、`leave` 等）内部作用于**默认频道**——最早加入且仍在会的那个频道，它离会后顺延到下一个。

只加入一个频道时，默认频道恒等于该频道，所有既有单频道代码行为不变；同时加入多个频道后，建议不再依赖这些便捷方法，显式使用各 Channel 对象，避免"默认频道顺延"带来的歧义。

### 一条采集轨发布到多个频道

同一条本地轨可以同时发布到多个频道，采集只有一份，编码推流各频道独立：

```typescript
const mic = srtc.createLocalMicTrack();
await meeting.publishLocalTrack(mic);
await intercom.publishLocalTrack(mic);
```

发布到多个频道后，这条轨在**每个频道内有各自独立的轨道信息**（服务端分配的轨道 id、编码参数等各不相同），此时：

- `track.getInfo()` 会**抛错**——它无法回答"哪个频道的 info"；
- 改用 `channel.getPublishInfo(track)` 查询指定频道内的轨道描述；
- 只发布到一个频道时 `track.getInfo()` 行为与旧版一致，无需改动。

```typescript
const infoInMeeting = meeting.getPublishInfo(mic);   // 会议频道内的轨道 id 等
const infoInIntercom = intercom.getPublishInfo(mic); // 对讲频道内的另一份
```

### 采集资源的回收

离会时 SDK 按"还有没有频道在用"回收采集：

- 某频道 `leave()`：只停止「曾发布于该频道、且当前没有任何频道在发布」的本地轨采集；仍被其它频道发布的轨保持采集推流。
- 最后一个频道离会：回收 SRTC 实例创建的全部本地轨（与单频道时代行为一致）。

因此上例中 `intercom.leave()` 不会停掉 mic 的采集（会议还在用），两个频道都退出后才会停。

### 释放实例

不再使用 SRTC 实例时（SPA 路由切走、组件卸载、准备重建实例），调用 `srtc.destroy()` 一次性离开所有频道、关闭 IM 并解除全局监听，详见 [destroy](/zh/rtc/web/api-reference/SRTC#destroy)。
