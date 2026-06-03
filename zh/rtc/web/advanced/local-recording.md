---
title: "本地合成录制"
description: "Web SDK 本地录制当前会议视角的视频宫格与会议音频"
---

### 概述

本地合成录制适合在浏览器端录制「当前用户看到的会议视角」：例如 3 宫格、9 宫格、翻页后的当前页、共享屏幕优先布局等。SDK 负责把传入的视频轨道绘制到内部 canvas，并把音频轨道混入同一条录制流，最终通过 `MediaRecorder` 输出一个 webm 文件；业务层负责决定当前要录哪些画面、每个画面放在录制画布的什么位置。

`LocalCompositeRecorder` 只处理媒体合成与录制生命周期，**不内置会议布局算法**——布局由应用层根据当前 UI 视角传入。

---

### 基本用法

```typescript
const recorder = srtc.createLocalCompositeRecorder();

await recorder.start({
  width: 1280,
  height: 720,
  fps: 15,
  videoItems: [
    {
      id: 'local-camera',
      track: localCameraTrack,
      label: '我',
      rect: { x: 0, y: 0, width: 640, height: 360 },
      fit: 'contain',
    },
    {
      id: 'remote-user-1-camera',
      track: remoteVideoTrack,
      label: '远端用户',
      rect: { x: 640, y: 0, width: 640, height: 360 },
      fit: 'contain',
    },
  ],
  audioTracks: [
    localMicTrack,
    remoteAudioMixTrack,
  ],
});

// 会议翻页、宫格变化或订阅关系变化后，更新当前录制视角。
recorder.updateVideoItems(nextVideoItems);
await recorder.updateAudioTracks(nextAudioTracks);

// 暂停与恢复作用于同一个最终文件。
recorder.pause();
recorder.resume();

// 结束录制，返回完整的 webm Blob。
const blob = await recorder.stop();
```

得到 `blob` 后即可下载或上传：

```typescript
const url = URL.createObjectURL(blob);
const a = document.createElement('a');
a.href = url;
a.download = 'recording.webm';
a.click();
URL.revokeObjectURL(url);
```

---

### 启动参数

`start(options)` 的 `LocalCompositeRecorderStartOptions`：

| 字段 | 类型 | 默认 | 说明 |
| --- | --- | --- | --- |
| `videoItems` | `LocalCompositeRecorderVideoItem[]` | — | 初始视频绘制列表，必填 |
| `audioTracks` | `LocalCompositeRecorderTrack[]` | — | 混入录制文件的音频轨道 |
| `width` | `number` | `1280` | 输出视频宽度（像素） |
| `height` | `number` | `720` | 输出视频高度（像素） |
| `fps` | `number` | `15` | `canvas.captureStream` 帧率 |
| `mimeType` | `string` | 自动 | 不传或不支持时自动选择浏览器支持的 webm 格式 |
| `timeslice` | `number` | — | `MediaRecorder` 分片间隔（毫秒）；不传则在 `stop` 时一次性返回 |
| `background` | `string` | `#101216` | 录制画布整体背景色 |
| `labelBackground` | `string` | `rgba(0,0,0,0.58)` | 标签背景色 |
| `onDataAvailable` | `(blob: Blob) => void` | — | 每次输出有效分片时触发，可用于边录边上传 |

`LocalCompositeRecorderVideoItem`（单个视频项）：

| 字段 | 类型 | 默认 | 说明 |
| --- | --- | --- | --- |
| `id` | `string` | — | 调用方维护的稳定唯一标识；同一 id 的 track 变更时复用槽位并替换解码源 |
| `track` | `LocalCompositeRecorderTrack \| null` | — | 要绘制的视频轨道；传 `null` 表示空槽位 |
| `rect` | `{ x, y, width, height }` | — | 在画布上的绘制区域（canvas 像素坐标） |
| `label` | `string` | — | 绘制在左下角的标签（如用户名）；不传则不绘制 |
| `fit` | `'contain' \| 'cover'` | `contain` | `contain` 保留完整画面，`cover` 填满并裁剪溢出 |
| `background` | `string` | `#1a1c22` | 单个槽位背景色 |

---

### 输入轨道

`videoItems[].track` 和 `audioTracks[]` 均可传入 SDK Track 或浏览器原生 `MediaStreamTrack`：

+ `LocalVideoTrack`
+ `RemoteVideoTrack`
+ `LocalAudioTrack`
+ `RemoteAudioTrack`
+ `MediaStreamTrack`

如果传入 SDK Track，录制器会监听内部媒体轨替换事件，并在重连或重新订阅导致底层 `MediaStreamTrack` 变化时自动切换到新轨道，无需业务层介入。

---

### 布局职责

`LocalCompositeRecorder` 不内置会议布局算法。应用层应根据当前 UI 视角生成 `videoItems`：

+ 当前只显示 3 个用户，就只传这 3 个视频项。
+ 当前是 9 宫格，就按 9 个槽位计算 `rect`。
+ 用户左右翻页后，调用 `updateVideoItems(...)` 切换到新一页。
+ 共享屏幕、主讲人模式等特殊布局，也由业务层计算 `rect`。

这样录制结果会跟随应用层传入的当前视角，而不是固定录制全部远端流。

---

### 音频建议

会议录制通常建议把本地麦克风轨道和远端混音轨道同时传入：

```typescript
const remoteAudioMixTrack = await srtc.subscribeRemoteAudioMixTrack();

await recorder.updateAudioTracks([
  localMicTrack,
  remoteAudioMixTrack,
]);
```

如果只录远端声音，可以只传 `remoteAudioMixTrack`；如果只录本地麦克风，可以只传 `localMicTrack`。

---

### 边录边上传

传入 `timeslice` 与 `onDataAvailable`，即可按分片实时拿到数据，用于边录边上传或落盘，避免长时间录制占用大量内存：

```typescript
await recorder.start({
  videoItems,
  audioTracks,
  timeslice: 5000, // 每 5 秒产出一个分片
  onDataAvailable: (chunk) => {
    uploadChunk(chunk); // 业务层上传逻辑
  },
});
```

> 注意：webm 分片为流式容器，单个分片通常不可独立播放，需服务端按顺序拼接为完整文件。

---

### 状态与释放

```typescript
// 'inactive' 未开始或已结束 | 'recording' 录制中 | 'paused' 暂停
const state = recorder.getState();

// 不再使用时释放内部资源（canvas、AudioContext、MediaRecorder 等）
recorder.destroy();
```

---

### 注意事项

- 需在 HTTPS（或 localhost）环境运行；`AudioContext` 可能需用户手势后才能启动。
- 输出格式为 webm；不同浏览器支持的编码（vp9/vp8/opus）不同，SDK 会自动回退到可用格式。
- `pause` / `resume` 作用于同一个最终文件，不会产生多个文件。
- 录制分辨率与帧率越高，CPU 占用越大，建议按场景选择合适的 `width`/`height`/`fps`。
