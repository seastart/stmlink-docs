---
title: "DeepFilterNet 降噪插件"
description: "使用 @seastart/srtc-plugin-deepfilternet 为麦克风轨道开启可调强度的 AI 降噪"
---

### 概述

`@seastart/srtc-plugin-deepfilternet` 是基于 [DeepFilterNet](https://github.com/Rikorose/DeepFilterNet)（AudioWorklet + WebAssembly）的 AI 降噪插件，实现了 SDK 的 [`TrackProcessor`](/zh/rtc/web/advanced/audio-processor) 接口。相比 [RNNoise 插件](/zh/rtc/web/advanced/rnnoise)，DeepFilterNet 降噪质量更高，并支持**运行时可调的降噪强度**与**旁路开关**；代价是计算量与资源体积更大。

---

### 安装

```bash
npm i @seastart/srtc-web-sdk @seastart/srtc-plugin-deepfilternet
```

---

### 托管静态资源

插件依赖两个静态资源（wasm + 模型，合计约 18MB），需自托管：

- `v2/pkg/df_bg.wasm`
- `v2/models/DeepFilterNet3_onnx.tar.gz`

<Warning>
`v2/pkg`、`v2/models` 这两层子目录是固定相对路径，拷贝时**必须保留该目录结构**，并用 `assetBasePath` 指向其根目录。
</Warning>

资源不随源码入库，安装后由包内脚本拉取，再拷到你的静态目录（保留 `v2/` 结构）：

```bash
# 拉取资源到包的 assets/（发布到 npm 的版本已内置，此步仅作兜底）
npm run fetch-assets --prefix node_modules/@seastart/srtc-plugin-deepfilternet

# 拷贝到你的静态目录
cp -r node_modules/@seastart/srtc-plugin-deepfilternet/assets/v2 public/deepfilternet/v2
```

> Vite 项目也可用 `vite-plugin-static-copy` 在构建时自动拷贝。

---

### 使用

```typescript
import SRTC from "@seastart/srtc-web-sdk";
import { DeepFilterNetProcessor } from "@seastart/srtc-plugin-deepfilternet";

const srtc = new SRTC();

// 1. 创建并采集麦克风
const mic = srtc.createLocalMicTrack();
await mic.startCapture({ deviceId });

// 2. 开启降噪（assetBasePath 指向上一步托管资源的目录）
const processor = new DeepFilterNetProcessor({
  assetBasePath: "/deepfilternet/",
  suppressionLevel: 50,
});
await mic.setProcessor(processor);

// 3. 发布
await srtc.publishLocalTrack(mic);
```

运行时调整降噪强度（无需重建音频流）或旁路：

```typescript
processor.setSuppressionLevel(80); // 0–100
processor.setEnabled(false);       // 旁路（输出原始音频）
processor.setEnabled(true);        // 恢复降噪
```

关闭降噪，还原原始麦克风轨道：

```typescript
await mic.removeProcessor();
```

---

### 选项

| 选项 | 类型 | 默认 | 说明 |
| --- | --- | --- | --- |
| `suppressionLevel` | `number` | `50` | 降噪强度 0–100，映射 DeepFilterNet 衰减上限 `atten_lim_db`；可运行时调整 |
| `assetBasePath` | `string` | `"/"` | 自托管资源根目录（其下需有 `v2/pkg`、`v2/models`） |
| `cdnUrl` | `string` | — | 高级：直接覆盖资源根 URL，优先级高于 `assetBasePath` |

---

### 运行时方法

| 方法 | 说明 |
| --- | --- |
| `setSuppressionLevel(level: number)` | 调整降噪强度 0–100，无需重建音频流 |
| `setEnabled(enabled: boolean)` | 旁路（`false` 输出原始音频）/ 恢复降噪（`true`） |

---

### 与 RNNoise 插件的取舍

| | DeepFilterNet 插件 | RNNoise 插件 |
| --- | --- | --- |
| 降噪效果 | 更高 | 强 |
| 可调强度 | 支持（运行时） | 不支持 |
| 额外开销 | 较高，资源约 18MB | 较低，wasm ~125KB |
| 延迟 | STFT 最小约 20ms | 约 10ms |

> 对降噪质量要求高、设备性能允许的场景，使用本插件；对低端设备或更看重轻量与低延迟的场景，使用 [RNNoise 插件](/zh/rtc/web/advanced/rnnoise)。

---

### 注意事项

- 仅支持音频轨道。
- 需在 HTTPS（或 localhost）环境运行；`AudioContext` 可能需用户手势后才能 `resume`。
- 采样率固定 48kHz。
- 计算量高于 RNNoise，请在目标设备实测 CPU 占用与端到端延迟。
- 切换麦克风设备（`changeDeviceId`）或重新 `startCapture` 后，降噪会自动恢复，无需重新调用 `setProcessor`。
- 可与其他处理器串联，详见[音视频处理器](/zh/rtc/web/advanced/audio-processor#多处理器串联)。
- 许可：DeepFilterNet 本体为 Apache-2.0/MIT；模型权重的授权请在分发前自行核实。

<Note>
模型文件本身是 gzip。部分服务器/代理会对 `.gz` 再加 `Content-Encoding: gzip`，浏览器自动解压一次后，底层拿到的是未压缩的 `.tar`，初始化会崩溃（`RuntimeError: unreachable`）。插件已**自动兜底**：检测到被解压会在浏览器内重新 gzip 还原，无需改服务器配置。该能力依赖 `CompressionStream`（Chrome 80+ / Edge 80+ / Safari 16.4+ / Firefox 113+）。
</Note>
