---
title: "DeepFilterNet noise suppression plugin"
description: "Enable AI noise suppression with adjustable strength on a microphone track with @seastart/srtc-plugin-deepfilternet: install, self-host the wasm and model, attach with setProcessor, adjust suppressionLevel or bypass at runtime, and trade-offs vs. the RNNoise plugin."
---

### Overview

`@seastart/srtc-plugin-deepfilternet` is an AI noise suppression plugin based on [DeepFilterNet](https://github.com/Rikorose/DeepFilterNet) (AudioWorklet + WebAssembly) that implements the SDK's [`TrackProcessor`](/en/rtc/web/advanced/audio-processor) interface. Compared with the [RNNoise plugin](/en/rtc/web/advanced/rnnoise), DeepFilterNet delivers higher noise suppression quality and supports **suppression strength adjustable at runtime** and a **bypass switch**; the cost is more computation and larger assets.

---

### Installation

```bash
npm i @seastart/srtc-web-sdk @seastart/srtc-plugin-deepfilternet
```

---

### Host the static assets

The plugin depends on two static assets (wasm + model, about 18 MB in total) that you need to self-host:

- `v2/pkg/df_bg.wasm`
- `v2/models/DeepFilterNet3_onnx.tar.gz`

<Warning>
The `v2/pkg` and `v2/models` subdirectories are fixed relative paths. When copying, you **must keep this directory structure**, and point `assetBasePath` to its root directory.
</Warning>

The assets aren't checked into the source repository; after installation, a script in the package fetches them, and then you copy them to your static directory (keeping the `v2/` structure):

```bash
# Fetch the assets into the package's assets/ (versions published to npm already include them; this step is only a fallback)
npm run fetch-assets --prefix node_modules/@seastart/srtc-plugin-deepfilternet

# Copy to your static directory
cp -r node_modules/@seastart/srtc-plugin-deepfilternet/assets/v2 public/deepfilternet/v2
```

> In Vite projects you can also copy them automatically at build time with `vite-plugin-static-copy`.

---

### Usage

```typescript
import { SRTC } from "@seastart/srtc-web-sdk";
import { DeepFilterNetProcessor } from "@seastart/srtc-plugin-deepfilternet";

const srtc = new SRTC();

// 1. Create the microphone track and start capture
const mic = srtc.createLocalMicTrack();
await mic.startCapture({ deviceId });

// 2. Enable noise suppression (assetBasePath points to the directory hosting the assets from the previous step)
const processor = new DeepFilterNetProcessor({
  assetBasePath: "/deepfilternet/",
  suppressionLevel: 50,
});
await mic.setProcessor(processor);

// 3. Publish
await srtc.publishLocalTrack(mic);
```

Adjust the suppression strength at runtime (without rebuilding the audio stream), or bypass:

```typescript
processor.setSuppressionLevel(80); // 0–100
processor.setEnabled(false);       // Bypass (output the original audio)
processor.setEnabled(true);        // Resume noise suppression
```

To turn off noise suppression and restore the original microphone track:

```typescript
await mic.removeProcessor();
```

---

### Options

| Option | Type | Default | Description |
| --- | --- | --- | --- |
| `suppressionLevel` | `number` | `50` | Suppression strength 0–100, mapped to DeepFilterNet's attenuation limit `atten_lim_db`; adjustable at runtime |
| `assetBasePath` | `string` | `"/"` | Root directory of the self-hosted assets (must contain `v2/pkg` and `v2/models`) |
| `cdnUrl` | `string` | — | Advanced: overrides the asset root URL directly; takes precedence over `assetBasePath` |

---

### Runtime methods

| Method | Description |
| --- | --- |
| `setSuppressionLevel(level: number)` | Adjusts suppression strength 0–100 without rebuilding the audio stream |
| `setEnabled(enabled: boolean)` | Bypass (`false` outputs the original audio) / resume noise suppression (`true`) |

---

### Trade-offs vs. the RNNoise plugin

| | DeepFilterNet plugin | RNNoise plugin |
| --- | --- | --- |
| Noise suppression | Higher | Strong |
| Adjustable strength | Supported (at runtime) | Not supported |
| Extra cost | Higher, assets about 18 MB | Lower, wasm ~125 KB |
| Latency | STFT minimum about 20 ms | About 10 ms |

> Use this plugin when noise suppression quality matters and device performance allows; for low-end devices or when lightweight and low latency matter more, use the [RNNoise plugin](/en/rtc/web/advanced/rnnoise).

---

### Notes

- Supports audio tracks only.
- Must run over HTTPS (or localhost); `AudioContext` may need a user gesture before it can `resume`.
- The sample rate is fixed at 48 kHz.
- Computation is higher than RNNoise; measure CPU usage and end-to-end latency on your target devices.
- After switching the microphone device (`changeDeviceId`) or calling `startCapture` again, noise suppression resumes automatically; you don't need to call `setProcessor` again.
- Can be chained with other processors; see [Audio/video processors](/en/rtc/web/advanced/audio-processor#chaining-multiple-processors).
- License: DeepFilterNet itself is Apache-2.0/MIT; verify the licensing of the model weights yourself before distribution.

<Note>
The model file itself is gzip. Some servers/proxies add `Content-Encoding: gzip` to `.gz` files again; after the browser decompresses once automatically, the underlying code receives an uncompressed `.tar`, and initialization crashes (`RuntimeError: unreachable`). The plugin **handles this automatically**: when it detects the file was decompressed, it re-gzips it in the browser to restore it, so you don't need to change server configuration. This relies on `CompressionStream` (Chrome 80+ / Edge 80+ / Safari 16.4+ / Firefox 113+).
</Note>
