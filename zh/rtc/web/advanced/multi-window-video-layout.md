---
title: "多窗口与双屏视频布局"
description: "Web SRTC 音视频 SDK 多窗口显示、双屏布局与摄像头浮窗实践指南"
---

当业务需要将视频放到独立窗口、第二块显示器，或在共享屏幕时保留自己的摄像头小窗时，可以结合以下能力实现：

+ `enterPictureInPicture(container, options?)`
+ `popOutToWindow(container, options?)`
+ `closePopOutWindow(container)`
+ `ChannelEventType.TRACK_PIP_ENTER / TRACK_PIP_EXIT`
+ `ChannelEventType.TRACK_POPOUT_OPEN / TRACK_POPOUT_CLOSE`

---

### 场景一：双屏布局

典型需求：

+ 显示器 A 展示远端共享桌面
+ 显示器 B 展示本地摄像头或远端人物视频

推荐做法是：

+ 主页面仍使用 `addPlayView(container)` 维持视频卡片结构
+ 用户点击“弹出窗口”后，调用 `popOutToWindow`
+ 将浏览器弹出的新窗口拖到第二块显示器

```typescript
const remoteScreenTrack = await srtc.subscribeRemoteVideoTrack(uid, trackId);
remoteScreenTrack.addPlayView(document.querySelector('#remote-screen')!);

remoteScreenTrack.popOutToWindow(
  document.querySelector('#remote-screen')!,
  {
    title: '远端共享桌面',
    width: 1600,
    height: 900,
    hideOriginView: true,
  }
);

localCameraTrack.addPlayView(document.querySelector('#local-camera')!);
localCameraTrack.popOutToWindow(
  document.querySelector('#local-camera')!,
  {
    title: '我的摄像头',
    width: 480,
    height: 360,
    hideOriginView: true,
  }
);
```

> `hideOriginView` 默认为 `true`。对于独立窗口模式，通常建议保留默认值，避免主页面和弹出窗口同时渲染同一路视频。

---

### 场景二：共享桌面时保留摄像头浮窗

典型需求：

+ 用户发起桌面共享
+ 浏览器主窗口可能被最小化或被其他应用遮挡
+ 仍希望右上角保留自己的摄像头小窗，便于确认出镜状态

推荐组合：

+ 使用 `LocalScreenTrack` 负责共享桌面
+ 使用 `LocalCameraTrack.enterPictureInPicture(...)` 将摄像头放入画中画

```typescript
const localScreenTrack = srtc.createLocalScreenTrack(ScreenPresets['1080p']);
await localScreenTrack.startCapture({ contentHint: 'detail' });
localScreenTrack.addPlayView(document.querySelector('#screen-preview')!);
await srtc.publishLocalTrack(localScreenTrack, { desc: 'screen' });

const localCameraTrack = srtc.createLocalCameraTrack(CameraPresets['720p']);
await localCameraTrack.startCapture();
localCameraTrack.addPlayView(document.querySelector('#camera-preview')!);
await srtc.publishLocalTrack(localCameraTrack, { desc: 'camera_big' });

await localCameraTrack.enterPictureInPicture(
  document.querySelector('#camera-preview')!,
  {
    width: 320,
    height: 240,
    hideOriginView: true,
  }
);
```

> 如果当前浏览器支持 `Document PiP`，SDK 会优先使用它；否则会降级到传统 `video PiP`。传统 `video PiP` 依赖原始 `video` 元素，因此不会隐藏原始视图。

---

### 用频道事件同步 UI 状态

PiP / 弹窗通常需要同步按钮文字、角标状态或浮层提示，建议统一使用频道事件而不是自己维护分散状态。

```typescript
srtc.onNotifyChannelEvent = (evt) => {
  switch (evt.type) {
    case ChannelEventType.TRACK_PIP_ENTER:
      console.log('轨道进入画中画', evt.data);
      break;
    case ChannelEventType.TRACK_PIP_EXIT:
      console.log('轨道退出画中画', evt.data);
      break;
    case ChannelEventType.TRACK_POPOUT_OPEN:
      console.log('轨道弹出独立窗口', evt.data);
      break;
    case ChannelEventType.TRACK_POPOUT_CLOSE:
      console.log('轨道关闭独立窗口', evt.data);
      break;
  }
};
```

---

### 共享结束时的清理建议

如果用户点击了浏览器原生“停止共享”，SDK 会触发 `TRACK_ENDED`。此时至少应清理共享轨道本身：

```typescript
srtc.onNotifyChannelEvent = async (evt) => {
  if (evt.type === ChannelEventType.TRACK_ENDED && evt.data === localScreenTrack) {
    await srtc.unpublishLocalTrack(localScreenTrack);
    localScreenTrack.removeAllPlayViews();
    localScreenTrack.stopCapture();
  }
};
```

> 对于同一个 `track`，`removePlayView(container)` 和 `removeAllPlayViews()` 会自动清理该轨道自身关联的画中画 / 弹出窗口状态，因此不需要再额外调用一次该轨道的 `exitPictureInPicture` 或 `closePopOutWindow`。
>
> 如果你的产品希望“共享结束时，连摄像头浮窗也一起关闭”，那属于业务层联动策略，可以再额外关闭 `localCameraTrack` 的画中画状态；但这不是 SDK 资源清理所必需的步骤。

---

### 实践建议

+ `画中画` 更适合“随时查看”的小尺寸视频，如本地摄像头、自我预览
+ `弹出窗口` 更适合双屏协作、大尺寸展示，如远端共享桌面或演讲人视频
+ 若 UI 需要自动恢复按钮状态，优先监听 `TRACK_PIP_*` 和 `TRACK_POPOUT_*` 事件
