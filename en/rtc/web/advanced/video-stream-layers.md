---
title: "Simulcast and resolution"
description: "Capture resolution vs. simulcast in the Web SDK: default camera_big / camera_small behavior of the camera presets, how to change high-stream resolution, publish only the high stream, publish a single low-resolution stream, customize simulcasts, and how remote users see layers."
---

### TL;DR

What `rtc-js` users most often confuse are actually two different things:

+ **Capture resolution**: decides how large the raw video captured by the camera is
+ **Publishing simulcast**: decides whether the same video is encoded into multiple layers and sent together

From first principles, **the "low stream" isn't another camera, nor a separate mode**; it's essentially just a low-resolution encoding layer of the same video track.

So:

+ To capture sharper video, change the **capture parameters**
+ To control "send one layer or two", change **`simulcasts` in the publish parameters**
+ To "send only the low stream", you don't "enable low-stream mode"; you **send a single low-resolution stream**

---

### SDK default behavior

The Web SDK's built-in camera presets behave as follows by default:

+ `CameraPresets['720p']`: publishes `camera_big + camera_small` by default
+ `CameraPresets['1080p']`: publishes `camera_big + camera_small` by default
+ `CameraPresets['360p']` / `CameraPresets['180p']`: no default simulcast configuration

The current built-in low-stream parameters are:

| Layer | `desc` | Resolution | Frame rate | Bitrate |
| --- | --- | --- | --- | --- |
| High stream | `camera_big` | Follows the main preset | Follows the main preset | Follows the main preset |
| Low stream | `camera_small` | 320 × 180 | 15 fps | 250 Kbps |

This means that if you write it like this:

```typescript
const localCameraTrack = srtc.createLocalCameraTrack(CameraPresets['720p']);
await localCameraTrack.startCapture();
await srtc.publishLocalTrack(localCameraTrack);
```

you're already sending, by default:

+ one `camera_big`
+ one `camera_small`

---

### The concepts, separated

#### 1. Capture resolution

Capture resolution is determined by the preset passed to `createLocalCameraTrack(...)`, or by the parameters passed to `startCapture(...)`:

```typescript
const localCameraTrack = srtc.createLocalCameraTrack(CameraPresets['1080p']);

await localCameraTrack.startCapture({
  width: 1920,
  height: 1080,
  frameRate: 15,
});
```

It affects "how sharp the source is".

#### 2. Publishing simulcast

Publishing simulcast is determined by `VideoPublishOptions.simulcasts` when calling `publishLocalTrack(...)`:

```typescript
await srtc.publishLocalTrack(localCameraTrack, {
  desc: 'camera_big',
  width: 1280,
  height: 720,
  maxBitrate: 1_200_000,
  maxFramerate: 15,
  simulcasts: [
    {
      desc: 'camera_small',
      width: 320,
      height: 180,
      maxBitrate: 250_000,
      maxFramerate: 15,
    },
  ],
});
```

It affects "how many encoding layers are sent into the channel".

> **Key point:**
> Changing only the capture resolution doesn't turn off the low stream automatically;
> changing only `simulcasts` doesn't change the camera's actual capture resolution either.

---

### Scenario 1: change the high-stream resolution but keep simulcast

This is the most common need. To do it:

+ First set the camera capture resolution to the target value
+ Then keep `simulcasts`

For example, change the high stream to 1080p while still sending a 320 × 180 low stream:

```typescript
import { SRTC, CameraPresets } from '@seastart/srtc-web-sdk';

const srtc = new SRTC();

const localCameraTrack = srtc.createLocalCameraTrack(CameraPresets['1080p']);
await localCameraTrack.startCapture();

// With the 1080p preset, camera_small is included by default
await srtc.publishLocalTrack(localCameraTrack);
```

If you want to customize the low-stream parameters, you can override them explicitly:

```typescript
await srtc.publishLocalTrack(localCameraTrack, {
  desc: 'camera_big',
  width: 1920,
  height: 1080,
  maxBitrate: 2_500_000,
  maxFramerate: 15,
  // Core logic: encode an additional lower-spec secondary layer from the same camera track
  simulcasts: [
    {
      desc: 'camera_small',
      width: 480,
      height: 270,
      maxBitrate: 350_000,
      maxFramerate: 15,
    },
  ],
});
```

---

### Scenario 2: send only the high stream, no low stream

Don't just change `width / height` here; explicitly empty `simulcasts`.

```typescript
import { SRTC, CameraPresets } from '@seastart/srtc-web-sdk';

const srtc = new SRTC();

const localCameraTrack = srtc.createLocalCameraTrack(CameraPresets['720p']);
await localCameraTrack.startCapture();

await srtc.publishLocalTrack(localCameraTrack, {
  desc: 'camera_big',
  // Core logic: empty simulcasts to send only the main layer
  simulcasts: [],
});
```

When to use it:

+ The channel is small and doesn't need layer switching
+ Your app only consumes one main video
+ You want to reduce uplink encoding and bandwidth cost

> **Note:**
> `CameraPresets['720p']` / `['1080p']` include the low stream by default.
> If your goal is "send only the high stream", you must explicitly pass `simulcasts: []` to override the default.

---

### Scenario 3: send only a single low-resolution stream

When people say "send only the low stream", from an encoding standpoint what they usually want is:

+ Don't send `camera_big`
+ Send only a single low-resolution stream

In that case, don't think in terms of "720p high stream + low stream"; instead create a low-resolution camera track directly and publish only that layer:

```typescript
import { SRTC } from '@seastart/srtc-web-sdk';

const srtc = new SRTC();

const localCameraTrack = srtc.createLocalCameraTrack({
  capture: {
    width: 320,
    height: 180,
    frameRate: 15,
  },
  publish: {
    desc: 'camera_small',
    width: 320,
    height: 180,
    maxBitrate: 250_000,
    maxFramerate: 15,
  },
});

await localCameraTrack.startCapture();
await srtc.publishLocalTrack(localCameraTrack);
```

What this approach really is:

+ There's only one video track
+ That track's spec is low resolution
+ Whether it's called `camera_small` is just naming for your app's semantics; underneath, it isn't "the secondary layer of the high stream turned on by itself"

---

### Scenario 4: customize simulcast parameters

If the default `320 × 180 / 250 Kbps` doesn't fit your app, customize it directly:

```typescript
const localCameraTrack = srtc.createLocalCameraTrack({
  capture: {
    width: 1280,
    height: 720,
    frameRate: 15,
  },
  publish: {
    desc: 'camera_big',
    width: 1280,
    height: 720,
    maxBitrate: 1_200_000,
    maxFramerate: 15,
    simulcasts: [
      {
        desc: 'camera_small',
        width: 640,
        height: 360,
        maxBitrate: 400_000,
        maxFramerate: 15,
      },
    ],
  },
});

await localCameraTrack.startCapture();
await srtc.publishLocalTrack(localCameraTrack);
```

Recommendations:

+ Decide the main layer's resolution based on what your UI actually needs; don't chase 1080p blindly
+ The secondary layer mainly serves thumbnails, small windows, and grids, so its resolution and bitrate should be clearly lower than the main layer's
+ If the channel often has poor networks or multiple videos on screen at once, keeping the low stream is usually more stable than sending only the high stream

---

### Not recommended

#### Don't create two camera tracks manually to simulate simulcast

For example, this approach isn't recommended:

```typescript
const bigTrack = srtc.createLocalCameraTrack(CameraPresets['720p']);
const smallTrack = srtc.createLocalCameraTrack({
  capture: { width: 320, height: 180, frameRate: 15 },
  publish: { desc: 'camera_small', width: 320, height: 180, maxBitrate: 250_000 },
});
```

The reasons are straightforward:

+ It becomes two independent app-level tracks rather than multiple encoding layers of the same video
+ Remote users have to handle two streams separately, which muddles the semantics
+ Local capture, encoding, and bandwidth costs are also higher

The right approach:

+ When you need simulcast, use **one camera track + `simulcasts`**
+ When you only need a single low-resolution stream, send just **one low-resolution stream** directly

---

### How remote users see simulcast

In the `TrackInfo` seen by remote users, two fields matter:

+ `fallback_ids`: which lower layers the main layer can fall back to
+ `variant`: whether this is a simulcast secondary layer

Your app should generally follow this rule:

+ **Subscribe to the main layer track first**
+ Don't display a secondary layer with `variant === true` as a separate new video

The SDK follows the same principle when auto-subscribing: it skips secondary layers and leaves the actual layer switching to the SFU and `fallback_ids`.

---

### Recommendations

| Need | Recommended approach |
| --- | --- |
| Change the main video from 720p to 1080p | Change the camera preset or the `startCapture` parameters |
| Keep simulcast | Keep `simulcasts`, or use `CameraPresets['720p'] / ['1080p']` directly |
| Send only the high stream | `publishLocalTrack(..., { simulcasts: [] })` |
| Send only a single low-resolution stream | Create a low-resolution single stream directly; don't use two-layer encoding |
| Adjust the low-stream spec separately | Customize the `simulcasts` array |

---

### Related docs

+ [Key concepts](/en/rtc/web/key-concepts)
+ [SRTC API reference](/en/rtc/web/api-reference/SRTC)
+ [Types](/en/rtc/web/types#video-capture-playback-and-publishing)
+ [media-tracks API reference](/en/rtc/web/api-reference/media-tracks)
