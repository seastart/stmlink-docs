### 概述

当内置的麦克风采集和摄像头采集无法满足需求时，可以使用任意 `MediaStreamTrack` 作为音视频源。常见场景：

+ 使用 Canvas 绘制内容并推送为视频流（虚拟形象、游戏画面）
+ 使用 Web Audio API 合成音频并推送
+ 将多路音频混音后推送

---

### 自定义音频流

通过 `srtc.createLocalCustomAudioTrack(msTrack)` 包装一个 `MediaStreamTrack`，即可作为本地音频流发布：

```typescript
import SRTC from '@seastart/srtc-web-sdk';

const srtc = new SRTC();

// 示例：使用 Web Audio API 合成一个音频 MediaStreamTrack
const audioContext = new AudioContext();
const oscillator = audioContext.createOscillator();
const destination = audioContext.createMediaStreamDestination();
oscillator.connect(destination);
oscillator.start();

const msAudioTrack = destination.stream.getAudioTracks()[0];

// 包装为 SDK 轨道并发布
const customAudioTrack = srtc.createLocalCustomAudioTrack(msAudioTrack);
await srtc.publishLocalTrack(customAudioTrack, { desc: '合成音频' });
```

---

### 自定义视频流

通过 `srtc.createLocalCustomVideoTrack(msTrack)` 包装，适合 Canvas 绘制场景：

```typescript
import SRTC from '@seastart/srtc-web-sdk';

const srtc = new SRTC();

// 示例：将 Canvas 内容作为视频流推送
const canvas = document.querySelector<HTMLCanvasElement>('#my-canvas')!;
const ctx = canvas.getContext('2d')!;

// 绘制内容（此处以动画矩形为例）
function draw() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  ctx.fillStyle = `hsl(${Date.now() / 10 % 360}, 70%, 50%)`;
  ctx.fillRect(50, 50, 200, 200);
  requestAnimationFrame(draw);
}
draw();

// Canvas 捕获为 MediaStream（参数为帧率）
const canvasStream = canvas.captureStream(15);
const msVideoTrack = canvasStream.getVideoTracks()[0];

// 包装为 SDK 轨道
const customVideoTrack = srtc.createLocalCustomVideoTrack(msVideoTrack);

// 本地预览
customVideoTrack.addPlayView(document.querySelector<HTMLElement>('#preview')!);

// 发布
await srtc.publishLocalTrack(customVideoTrack, { desc: 'canvas 视频' });
```

---

### 混音推流（createMixedAudioMediaStreamTrack）

当需要将多路 `MediaStreamTrack` 合并为一路音频推送时，可使用 `createMixedAudioMediaStreamTrack` 工具函数：

```typescript
import SRTC, { createMixedAudioMediaStreamTrack } from '@seastart/srtc-web-sdk';

const srtc = new SRTC();

// 假设已有两路 MediaStreamTrack：麦克风轨道 + 系统音频轨道
const micMsTrack: MediaStreamTrack = /* ... */;
const systemAudioMsTrack: MediaStreamTrack = /* ... */;

// 合并为单路混音轨道
const mixedMsTrack = createMixedAudioMediaStreamTrack([micMsTrack, systemAudioMsTrack]);

// 包装为 SDK 轨道并发布
const mixedAudioTrack = srtc.createLocalCustomAudioTrack(mixedMsTrack);
await srtc.publishLocalTrack(mixedAudioTrack, { desc: '混音' });
```

> **使用场景：** 边讲话边分享视频，需要将麦克风声音和系统声音合并成一路推送时使用。

---

### 停止自定义流

自定义轨道也支持标准的 unpublish 流程：

```typescript
// 停止发布
await srtc.unpublishLocalTrack(customVideoTrack);

// 停止底层 MediaStreamTrack
msVideoTrack.stop();
```
