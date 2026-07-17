---
title: "RNN 降噪插件"
description: "使用 @seastart/srtc-plugin-rnnoise 为麦克风轨道开启 AI 降噪"
---

### 概述

`@seastart/srtc-plugin-rnnoise` 是基于 [RNNoise](https://github.com/xiph/rnnoise)（AudioWorklet + WebAssembly）的 AI 降噪插件，实现了 SDK 的 [`TrackProcessor`](/zh/rtc/web/advanced/audio-processor) 接口。相比浏览器原生的 `noiseSuppression`，RNNoise 对稳态与非稳态噪声（键盘声、风扇声、环境嘈杂等）抑制更强。

---

### 安装

```bash
npm i @seastart/srtc-web-sdk @seastart/srtc-plugin-rnnoise
```

---

### 托管静态资源

插件依赖三个静态资源（位于包的 `assets/` 目录）：

- `rnnoise-runtime.js`
- `rnnoise-processor.js`
- `rnnoise-processor.wasm`

<Warning>
`rnnoise-runtime.js` 内部通过 `document.currentScript.src` 定位同目录下的 worklet 与 wasm，因此这三个文件**必须放在同一目录**，并用 `basePath` 指向它。
</Warning>

把资源拷到你的静态目录，例如 `public/rnnoise/`：

```bash
cp node_modules/@seastart/srtc-plugin-rnnoise/assets/* public/rnnoise/
```

> Vite 项目也可用 `vite-plugin-static-copy` 在构建时自动拷贝。

---

### 使用

```typescript
import SRTC from "@seastart/srtc-web-sdk";
import { RnnoiseProcessor } from "@seastart/srtc-plugin-rnnoise";

const srtc = new SRTC();

// 1. 创建并采集麦克风
const mic = srtc.createLocalMicTrack();
await mic.startCapture({ deviceId });

// 2. 开启降噪（basePath 指向上一步托管资源的目录）
await mic.setProcessor(new RnnoiseProcessor({ basePath: "/rnnoise/" }));

// 3. 发布
await srtc.publishLocalTrack(mic);
```

关闭降噪，还原原始麦克风轨道：

```typescript
await mic.removeProcessor();
```

---

### 选项

| 选项 | 类型 | 默认 | 说明 |
| --- | --- | --- | --- |
| `basePath` | `string` | `"/"` | 静态资源所在目录，需以 `/` 结尾 |

---

### 与原生 `noiseSuppression` 的取舍

| | RNNoise 插件 | 原生 `noiseSuppression` |
| --- | --- | --- |
| 降噪效果 | 强，适合复杂噪声 | 一般 |
| 额外开销 | 占用 CPU、加载 ~125KB wasm | 几乎为零 |
| 部署 | 需托管静态资源 | 无需 |

> 对低端设备或弱噪声场景，可继续使用 `createLocalMicTrack` 的原生 `noiseSuppression`；对噪声较强、对通话质量要求高的场景，使用本插件。

---

### 注意事项

- 仅支持音频轨道。
- 需在 HTTPS（或 localhost）环境运行；`AudioContext` 可能需用户手势后才能 `resume`。
- 采样率固定 48kHz。
- 切换麦克风设备（`changeDeviceId`）或重新 `startCapture` 后，降噪会自动恢复，无需重新调用 `setProcessor`。
- 可与其他处理器串联，详见[音视频处理器](/zh/rtc/web/advanced/audio-processor#多处理器串联)。
