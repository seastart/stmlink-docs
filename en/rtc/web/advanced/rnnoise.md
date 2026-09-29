---
title: "RNN noise suppression plugin"
description: "Enable AI noise suppression on a microphone track with @seastart/srtc-plugin-rnnoise: install, host the three static assets in one directory, attach with setProcessor and basePath, options, and trade-offs vs. the browser's native noiseSuppression."
---

### Overview

`@seastart/srtc-plugin-rnnoise` is an AI noise suppression plugin based on [RNNoise](https://github.com/xiph/rnnoise) (AudioWorklet + WebAssembly) that implements the SDK's [`TrackProcessor`](/en/rtc/web/advanced/audio-processor) interface. Compared with the browser's native `noiseSuppression`, RNNoise suppresses both stationary and non-stationary noise (keyboard, fans, ambient noise, etc.) more strongly.

---

### Installation

```bash
npm i @seastart/srtc-web-sdk @seastart/srtc-plugin-rnnoise
```

---

### Host the static assets

The plugin depends on three static assets (in the package's `assets/` directory):

- `rnnoise-runtime.js`
- `rnnoise-processor.js`
- `rnnoise-processor.wasm`

<Warning>
`rnnoise-runtime.js` locates the worklet and wasm in the same directory via `document.currentScript.src`, so these three files **must be placed in the same directory**, and `basePath` must point to it.
</Warning>

Copy the assets to your static directory, for example `public/rnnoise/`:

```bash
cp node_modules/@seastart/srtc-plugin-rnnoise/assets/* public/rnnoise/
```

> In Vite projects you can also copy them automatically at build time with `vite-plugin-static-copy`.

---

### Usage

```typescript
import { SRTC } from "@seastart/srtc-web-sdk";
import { RnnoiseProcessor } from "@seastart/srtc-plugin-rnnoise";

const srtc = new SRTC();

// 1. Create the microphone track and start capture
const mic = srtc.createLocalMicTrack();
await mic.startCapture({ deviceId });

// 2. Enable noise suppression (basePath points to the directory hosting the assets from the previous step)
await mic.setProcessor(new RnnoiseProcessor({ basePath: "/rnnoise/" }));

// 3. Publish
await srtc.publishLocalTrack(mic);
```

To turn off noise suppression and restore the original microphone track:

```typescript
await mic.removeProcessor();
```

---

### Options

| Option | Type | Default | Description |
| --- | --- | --- | --- |
| `basePath` | `string` | `"/"` | Directory containing the static assets; must end with `/` |

---

### Trade-offs vs. native `noiseSuppression`

| | RNNoise plugin | Native `noiseSuppression` |
| --- | --- | --- |
| Noise suppression | Strong, suits complex noise | Moderate |
| Extra cost | Uses CPU, loads ~125 KB of wasm | Almost none |
| Deployment | Requires hosting static assets | None |

> For low-end devices or scenarios with little noise, keep using the native `noiseSuppression` of `createLocalMicTrack`; for strong noise and high call-quality requirements, use this plugin.

---

### Notes

- Supports audio tracks only.
- Must run over HTTPS (or localhost); `AudioContext` may need a user gesture before it can `resume`.
- The sample rate is fixed at 48 kHz.
- After switching the microphone device (`changeDeviceId`) or calling `startCapture` again, noise suppression resumes automatically; you don't need to call `setProcessor` again.
- Can be chained with other processors; see [Audio/video processors](/en/rtc/web/advanced/audio-processor#chaining-multiple-processors).
