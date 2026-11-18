---
title: "AI noise suppression (DeepFilterNet)"
description: "Turn on AI noise suppression for the microphone in Web meetings: install @seastart/srtc-plugin-deepfilternet and hand it to the meeting layer with setAudioProcessor, which attaches it whenever the mic opens and detaches it when the mic closes"
---

### Overview

The meeting layer sets the microphone audio processor through `setAudioProcessor`, available since `0.3.4`. The most common use is attaching the SRTC AI noise suppression plugin `@seastart/srtc-plugin-deepfilternet`. It is based on DeepFilterNet, uses the same algorithm and model as the Android and iOS SDKs, and lets you adjust the suppression strength and bypass it at runtime.

For installing the plugin, hosting its static assets, and its options and runtime methods, see the SRTC page [DeepFilterNet noise suppression plugin](/en/rtc/web/advanced/deepfilternet). This page only covers how to wire it into a meeting. Web only; the mini program SDK does not support it.

---

### Installation

```bash
npm install @seastart/smeeting-web-sdk@latest @seastart/srtc-plugin-deepfilternet --save
```

The plugin loads model and WebAssembly files at runtime. Host them on your site first, as described in [Host the static assets](/en/rtc/web/advanced/deepfilternet#host-the-static-assets).

---

### Usage

```typescript
import { SMeeting } from "@seastart/smeeting-web-sdk";
import { DeepFilterNetProcessor } from "@seastart/srtc-plugin-deepfilternet";

const processor = new DeepFilterNetProcessor({
  assetBasePath: "/deepfilternet/",  // Directory where you hosted the assets in the previous step
  suppressionLevel: 50,              // 0–100
});

// Can be called before or after entering a meeting; takes effect immediately if the mic is on
await meeting.setAudioProcessor(processor);

// From now on, noise suppression is attached every time the mic opens
await meeting.requestOpenMic();
```

To adjust the strength or bypass, call the plugin directly; no need to set it again:

```typescript
processor.setSuppressionLevel(80); // 0–100
processor.setEnabled(false);       // Bypass (output the original audio)
processor.setEnabled(true);        // Resume noise suppression
```

Turn noise suppression off:

```typescript
await meeting.setAudioProcessor(undefined);
```

---

### Meeting-layer behavior

+ **The SDK remembers the setting**: the meeting creates a new microphone track every time the mic opens, so the SDK keeps the processor and attaches it after capture starts and before publishing, then detaches it when the mic closes or you leave the meeting. The setting persists after leaving, so it applies again the next time you enter and open the mic.
+ **The same instance can be reused**: the processor is destroyed when the mic closes and initialized again the next time it opens, so you don't need to create a new one each time.
+ **A failure to attach when the mic opens doesn't block the mic** (for example, if the static assets fail to load). The mic opens as usual and sends audio without noise suppression; the SDK only logs a warning to the console. If the mic is already on when you call `setAudioProcessor`, a failure throws directly.
+ The noise suppression plugin turns off the browser's built-in noise suppression automatically so the two don't stack. This requires SRTC Web `0.7.3` or later, which `0.3.4` already depends on.
+ Pass an array to chain multiple processors in order, for example noise suppression followed by a voice changer. See the SRTC page [Audio processors](/en/rtc/web/advanced/audio-processor) for the rules.
