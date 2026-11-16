---
title: "Audio/video processors (plugins)"
description: "Attach processing plugins such as noise suppression or voice changing to local tracks in the Web SDK through the TrackProcessor interface: setProcessor / removeProcessor, chaining processors with ProcessorPipeline, writing a custom processor, and lifecycle rules."
---

### Overview

When you need extra audio or video processing between capture and publishing (such as AI noise suppression, beauty filters, or voice changing), the SDK provides a unified **processor mechanism**.

From first principles, a processor is essentially "take one `MediaStreamTrack` in, output one processed `MediaStreamTrack`". The SDK only needs to provide an attachment point on local tracks, while plugins implement the processing logic; the two are decoupled through the `TrackProcessor` interface.

Processors are distributed as **separate npm packages**, such as the RNN noise suppression plugin [`@seastart/srtc-plugin-rnnoise`](/en/rtc/web/advanced/rnnoise).

---

### Attaching and detaching

Local audio/video tracks (`LocalMicTrack`, `LocalCameraTrack`, custom tracks, etc.) all provide two methods:

```typescript
// Attach a processor (call startCapture first to have a track)
await track.setProcessor(processor);

// Detach the processor and restore the original captured track
await track.removeProcessor();
```

Once attached, it takes effect **whether or not the track is published**: if not yet published, the processed track is used automatically when publishing; if already published, the SDK switches via `replaceTrack` without renegotiation, and remote users notice nothing.

```typescript
import { SRTC } from "@seastart/srtc-web-sdk";
import { RnnoiseProcessor } from "@seastart/srtc-plugin-rnnoise";

const srtc = new SRTC();

const mic = srtc.createLocalMicTrack();
await mic.startCapture({ deviceId });

await mic.setProcessor(new RnnoiseProcessor({ basePath: "/rnnoise/" }));
await srtc.publishLocalTrack(mic);
```

---

### Chaining multiple processors

`setProcessor` accepts an array and chains multiple processors in order (source → P1 → P2 → … → publish). A common combination: noise suppression first, then voice changing.

```typescript
import { RnnoiseProcessor } from "@seastart/srtc-plugin-rnnoise";

await mic.setProcessor([
  new RnnoiseProcessor({ basePath: "/rnnoise/" }), // Noise suppression first
  new VoiceChanger({ preset: "cartoon" }),         // Then voice changing (example)
]);

await mic.removeProcessor(); // Detach and release the whole chain together
```

When you pass an array, the SDK internally uses `ProcessorPipeline` to combine the processors into one; audio chains **share the same `AudioContext`**, reducing the cost of multi-stage processing. You can also use `ProcessorPipeline` directly:

```typescript
import { ProcessorPipeline } from "@seastart/srtc-web-sdk";

const pipeline = new ProcessorPipeline([processorA, processorB]);
await mic.setProcessor(pipeline);
```

---

### Writing a custom processor

Implement the `TrackProcessor` interface to plug in:

```typescript
import type { TrackProcessor, ProcessorOptions } from "@seastart/srtc-web-sdk";

export class MyProcessor implements TrackProcessor {
  readonly name = "my-processor";
  processedTrack?: MediaStreamTrack;

  // Initialize: build the processing pipeline and produce processedTrack
  async init(options: ProcessorOptions): Promise<void> {
    const { track, kind, audioContext } = options;
    // ... build the processing chain from track and assign this.processedTrack
  }

  // Release: disconnect nodes, close any AudioContext you created, etc.
  async destroy(): Promise<void> {
    // ...
  }
}
```

`ProcessorOptions` fields:

| Field | Type | Description |
| --- | --- | --- |
| `track` | `MediaStreamTrack` | Source track (the original captured track) |
| `kind` | `TrackKind` | Track type (`audio` / `video`) |
| `audioContext` | `AudioContext?` | Shared context passed in by `ProcessorPipeline` when chaining; reuse it first |

> When writing an audio processor, reuse `options.audioContext` if it exists (don't `close` it yourself); only close it in `destroy` if you created the context yourself.

### Declaring browser 3A requirements (audio processors)

When the browser captures the microphone it applies its own 3A (noise suppression, echo cancellation, auto gain control). If your processor already does noise suppression, adding the browser's on top makes voices sound muffled. An audio processor can implement `AudioTrackProcessor` (which extends `TrackProcessor`) and use `audioProcessing` to declare what the browser should do:

```typescript
import type { AudioTrackProcessor, ProcessorOptions } from "@seastart/srtc-web-sdk";

export class MyDenoiser implements AudioTrackProcessor {
  readonly name = "my-denoiser";
  // Ask the browser to turn off its own noise suppression; echo cancellation and
  // auto gain control are not declared, so the capture options still apply
  readonly audioProcessing = { noiseSuppression: false };
  processedTrack?: MediaStreamTrack;

  async init(options: ProcessorOptions): Promise<void> { /* ... */ }
  async destroy(): Promise<void> { /* ... */ }
}
```

`audioProcessing` fields (type `AudioProcessingConstraints`):

| Field | Type | Description |
| --- | --- | --- |
| `noiseSuppression` | `boolean?` | Browser noise suppression |
| `echoCancellation` | `boolean?` | Browser echo cancellation |
| `autoGainControl` | `boolean?` | Browser auto gain control |

Rules:

- When attached to a microphone track (`LocalMicTrack`), the SDK **recaptures the microphone once** with the declared settings, so audio drops out briefly. Detaching the processor, or a processor that fails to initialize, restores the original settings. Browsers can't switch these settings mid-capture, so a recapture is the only way.
- If the declaration matches the current capture settings (for example, your app already turned noise suppression off), no recapture happens.
- When chaining processors (an array or a `ProcessorPipeline`), the declarations are merged: a setting is turned off if any processor asks for it to be off.
- The options you passed to `startCapture` are left unchanged; the declaration stays in effect after switching devices or calling `startCapture` again.
- The SDK's [RNNoise](/en/rtc/web/advanced/rnnoise) and [DeepFilterNet](/en/rtc/web/advanced/deepfilternet) plugins both declare `{ noiseSuppression: false }`.
- In Chrome, if the same microphone has another live capture track on the same page (such as a mic test your page runs), those tracks share one set of 3A settings and the declaration may not take effect. Stop other captures on the same device before attaching the processor.

---

### Lifecycle and notes

- You must `startCapture` to have a track before calling `setProcessor`; otherwise it throws.
- `setProcessor` is idempotent: calling it again detaches the existing processor before attaching the new one.
- **Automatic reattachment**: after switching devices (`changeDeviceId`) or calling `startCapture` again, the SDK automatically rebuilds the processor with the new source track, so you don't need to call `setProcessor` again.
- Processors mostly rely on `AudioContext`/WASM, need HTTPS (or localhost), and may need a user gesture before they can run.
