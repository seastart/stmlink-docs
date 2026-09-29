---
title: "Integration"
description: "Set up the SRTC Web SDK: supported browsers and minimum versions, embedding in WeChat Mini Program via web-view, HTTPS/localhost protocol limits for publishing, installing via npm, CDN, or local files, import styles, and using the SDK with Vue and other reactive frameworks."
---

### Supported browsers

The SRTC Web SDK supports mainstream desktop and mobile browsers:

| Browser | Minimum version | Notes |
| --- | :---: | --- |
| Chrome | 72+ | Recommended, full feature support |
| Edge | 79+ | Chromium-based |
| Firefox | 66+ | Doesn't support choosing the speaker output |
| Safari | 14+ | Doesn't support system audio in screen sharing |
| WeChat in-app browser | iOS 14.3+ / Android | Supports sending and receiving. Older iOS versions below 14.3 can only receive |
| Mobile Chrome / Safari | Latest | Supports basic audio and video calls |

> **Tip:** We recommend that users use the latest version of Chrome for the best experience.

---

### WeChat Mini Program

When you need audio and video in a WeChat Mini Program, **we recommend embedding a page built with this Web SDK via the Mini Program's `<web-view>`**, rather than building a separate native Mini Program implementation. One Web codebase then covers both browsers and Mini Programs, features and future updates stay consistent, and maintenance cost is lowest.

Key points:

+ The embedded page must be served over **HTTPS**, and its domain must be configured as a **business domain** in the Mini Program admin console and pass verification
+ Pass parameters between the Mini Program and the embedded page through the `web-view` communication mechanism; the channel name, token, and so on can be delivered via URL query
+ The page runs in the WeChat in-app browser; on iOS 14.3 and above and on Android it can publish and receive normally. Only older systems below iOS 14.3 are limited by the system WebView and can only receive

---

### URL protocol restrictions

WebRTC APIs restrict the page protocol. Choose the protocol that fits your deployment:

| Scenario | Protocol | Receive | Publish | Notes |
| --- | --- | :---: | :---: | --- |
| Production | HTTPS | ✅ | ✅ | **Recommended** |
| Production | HTTP | ✅ | ❌ | Receive only |
| Local development | http://localhost | ✅ | ✅ | **Recommended** |
| Local development | http://127.0.0.1 | ✅ | ✅ | |
| Local development | http://[local IP] | ✅ | ❌ | Receive only |
| Local development | file:/// | ✅ | ✅ | |

---

### Installation

#### npm

```bash
npm install @seastart/srtc-web-sdk --save
```

#### CDN

For projects without a build tool, include the SDK directly in HTML with a `<script>` tag:

```html
<!-- Load the latest version from the unpkg CDN -->
<script src="https://unpkg.com/@seastart/srtc-web-sdk@latest/srtc.js"></script>
```

After loading from the CDN, the global variable `SRTC` is available directly.

#### Local download

1. Download [srtc.js](https://unpkg.com/@seastart/srtc-web-sdk@latest/srtc.js) and [srtc.d.ts](https://unpkg.com/@seastart/srtc-web-sdk@latest/srtc.d.ts)
2. Copy both files into your project directory

---

### Importing

#### ES Module (recommended, with npm)

```typescript
import {
  SRTC,
  LocalMicTrack,
  LocalCameraTrack,
  LocalScreenTrack,
  RemoteAudioMixTrack,
  RemoteVideoTrack,
  ChannelEventType,
  MicPresets,
  CameraPresets,
  ScreenPresets,
  LogLevel,
  LogTarget,
} from '@seastart/srtc-web-sdk';
import type { ChannelEvent } from '@seastart/srtc-web-sdk';
```

#### Script tag (with CDN or local files)

```html
<script src="srtc.js"></script>
<script>
  // The global variable SRTC is the main class
  const srtc = new SRTC({ logLevel: 'debug' });
</script>
```

### Using with reactive frameworks

<Warning>
Don't put the `SRTC` instance or the `Channel` returned by `join()` into **deeply reactive containers** such as Vue's `reactive()` / `ref()` or Pinia state. The SDK relies on object identity comparisons in many places (channels, tracks, subscriptions); once the instance is proxied, these comparisons break, and they fail silently—the typical symptom is that you receive no channel events at all, with no error reported.
</Warning>

Store them with `markRaw()` or `shallowRef`:

```typescript
import { markRaw, shallowRef } from 'vue';

// Engine instance
const srtc = markRaw(new SRTC({ logLevel: LogLevel.DEBUG }));

// The Channel returned by join must also be unproxied
const channel = shallowRef();
channel.value = markRaw(await srtc.join(token));
```
