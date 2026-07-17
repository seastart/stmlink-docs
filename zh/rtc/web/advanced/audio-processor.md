---
title: "音视频处理器（插件）"
description: "通过 TrackProcessor 接口为本地音视频轨道挂载降噪、变声等处理插件"
---

### 概述

当需要在采集到发布之间对音视频做额外处理（如 AI 降噪、美颜、变声）时，SDK 提供统一的**处理器（Processor）机制**。

第一性原理：一个处理器的本质就是「输入一条 `MediaStreamTrack`，输出一条处理后的 `MediaStreamTrack`」。SDK 只需在本地轨道上提供挂载点，处理逻辑由插件实现，二者通过 `TrackProcessor` 接口解耦。

处理器以**独立 npm 包**形式分发，例如 RNN 降噪插件 [`@seastart/srtc-plugin-rnnoise`](/zh/rtc/web/advanced/rnnoise)。

---

### 挂载与卸载

本地音频/视频轨道（`LocalMicTrack`、`LocalCameraTrack`、自定义轨道等）都提供两个方法：

```typescript
// 挂载处理器（需先 startCapture 采集到轨道）
await track.setProcessor(processor);

// 卸载处理器，还原为原始采集轨道
await track.removeProcessor();
```

挂载后，**无论轨道是否已发布**都会生效：未发布时处理后的轨道会在发布时自动使用；已发布时 SDK 通过 `replaceTrack` 免重协商地切换，远端无感知。

```typescript
import SRTC from "@seastart/srtc-web-sdk";
import { RnnoiseProcessor } from "@seastart/srtc-plugin-rnnoise";

const srtc = new SRTC();

const mic = srtc.createLocalMicTrack();
await mic.startCapture({ deviceId });

await mic.setProcessor(new RnnoiseProcessor({ basePath: "/rnnoise/" }));
await srtc.publishLocalTrack(mic);
```

---

### 多处理器串联

`setProcessor` 接受数组，按顺序串联多个处理器（源 → P1 → P2 → … → 发布）。常见组合：先降噪再变声。

```typescript
import { RnnoiseProcessor } from "@seastart/srtc-plugin-rnnoise";

await mic.setProcessor([
  new RnnoiseProcessor({ basePath: "/rnnoise/" }), // 先降噪
  new VoiceChanger({ preset: "cartoon" }),         // 再变声（示例）
]);

await mic.removeProcessor(); // 整条链一起卸载、释放
```

传入数组时，SDK 内部用 `ProcessorPipeline` 把多个处理器收敛成一个；音频链会**共享同一个 `AudioContext`**，减少多级处理的开销。也可直接使用 `ProcessorPipeline`：

```typescript
import { ProcessorPipeline } from "@seastart/srtc-web-sdk";

const pipeline = new ProcessorPipeline([processorA, processorB]);
await mic.setProcessor(pipeline);
```

---

### 编写自定义处理器

实现 `TrackProcessor` 接口即可接入：

```typescript
import type { TrackProcessor, ProcessorOptions } from "@seastart/srtc-web-sdk";

export class MyProcessor implements TrackProcessor {
  readonly name = "my-processor";
  processedTrack?: MediaStreamTrack;

  // 初始化：建立处理管线，产出 processedTrack
  async init(options: ProcessorOptions): Promise<void> {
    const { track, kind, audioContext } = options;
    // ... 基于 track 建立处理链，赋值 this.processedTrack
  }

  // 释放：断开节点、关闭自建的 AudioContext 等
  async destroy(): Promise<void> {
    // ...
  }
}
```

`ProcessorOptions` 字段：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `track` | `MediaStreamTrack` | 源轨道（采集得到的原始轨道） |
| `kind` | `TrackKind` | 轨道类型（`audio` / `video`） |
| `audioContext` | `AudioContext?` | 串联场景下由 `ProcessorPipeline` 传入的共享上下文，应优先复用 |

> 编写音频处理器时，若 `options.audioContext` 存在应复用它（不要自行 `close`）；仅在自建上下文时才在 `destroy` 中关闭。

---

### 生命周期与注意事项

- 必须先 `startCapture` 采集到轨道，再 `setProcessor`，否则抛错。
- `setProcessor` 幂等：重复调用会先卸载已有处理器再挂载新的。
- **自动重挂**：切换设备（`changeDeviceId`）或重新 `startCapture` 后，SDK 会自动用新源轨道重建处理器，无需重新调用 `setProcessor`。
- 处理器多依赖 `AudioContext`/WASM，需在 HTTPS（或 localhost）环境，且可能需用户手势后才能运行。
