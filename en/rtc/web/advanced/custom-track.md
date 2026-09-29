---
title: "Custom tracks"
description: "Publish any MediaStreamTrack with the Web SDK: wrap synthesized audio with createLocalCustomAudioTrack, Canvas video with createLocalCustomVideoTrack, mix several audio tracks with createMixedAudioMediaStreamTrack, and stop custom tracks. Read when built-in mic and camera capture isn't enough."
---

### Overview

When the built-in microphone and camera capture don't meet your needs, you can use any `MediaStreamTrack` as an audio or video source. Common scenarios:

+ Draw content with Canvas and publish it as a video track (avatars, game footage)
+ Synthesize audio with the Web Audio API and publish it
+ Mix several audio tracks and publish the result

---

### Custom audio track

Wrap a `MediaStreamTrack` with `srtc.createLocalCustomAudioTrack(msTrack)` to publish it as a local audio track:

```typescript
import { SRTC } from '@seastart/srtc-web-sdk';

const srtc = new SRTC();

// Example: synthesize an audio MediaStreamTrack with the Web Audio API
const audioContext = new AudioContext();
const oscillator = audioContext.createOscillator();
const destination = audioContext.createMediaStreamDestination();
oscillator.connect(destination);
oscillator.start();

const msAudioTrack = destination.stream.getAudioTracks()[0];

// Wrap it as an SDK track and publish
const customAudioTrack = srtc.createLocalCustomAudioTrack(msAudioTrack);
await srtc.publishLocalTrack(customAudioTrack, { desc: 'synthesized audio' });
```

---

### Custom video track

Wrap it with `srtc.createLocalCustomVideoTrack(msTrack)`, which suits Canvas drawing scenarios:

```typescript
import { SRTC } from '@seastart/srtc-web-sdk';

const srtc = new SRTC();

// Example: publish Canvas content as a video track
const canvas = document.querySelector<HTMLCanvasElement>('#my-canvas')!;
const ctx = canvas.getContext('2d')!;

// Draw content (an animated rectangle here as an example)
function draw() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  ctx.fillStyle = `hsl(${Date.now() / 10 % 360}, 70%, 50%)`;
  ctx.fillRect(50, 50, 200, 200);
  requestAnimationFrame(draw);
}
draw();

// Capture the Canvas as a MediaStream (the parameter is the frame rate)
const canvasStream = canvas.captureStream(15);
const msVideoTrack = canvasStream.getVideoTracks()[0];

// Wrap it as an SDK track
const customVideoTrack = srtc.createLocalCustomVideoTrack(msVideoTrack);

// Local preview
customVideoTrack.addPlayView(document.querySelector<HTMLElement>('#preview')!);

// Publish
await srtc.publishLocalTrack(customVideoTrack, { desc: 'canvas video' });
```

---

### Publishing mixed audio (createMixedAudioMediaStreamTrack)

When you need to merge several `MediaStreamTrack`s into one audio track for publishing, use the `createMixedAudioMediaStreamTrack` utility function:

```typescript
import { SRTC, createMixedAudioMediaStreamTrack } from '@seastart/srtc-web-sdk';

const srtc = new SRTC();

// Assume you already have two MediaStreamTracks: a microphone track + a system audio track
const micMsTrack: MediaStreamTrack = /* ... */;
const systemAudioMsTrack: MediaStreamTrack = /* ... */;

// Merge into a single mixed audio track
const mixedMsTrack = createMixedAudioMediaStreamTrack([micMsTrack, systemAudioMsTrack]);

// Wrap it as an SDK track and publish
const mixedAudioTrack = srtc.createLocalCustomAudioTrack(mixedMsTrack);
await srtc.publishLocalTrack(mixedAudioTrack, { desc: 'mixed audio' });
```

> **When to use:** when you talk while sharing a video and need to merge microphone audio and system audio into one track for publishing.

---

### Stop a custom track

Custom tracks also support the standard unpublish flow:

```typescript
// Unpublish
await srtc.unpublishLocalTrack(customVideoTrack);

// Stop the underlying MediaStreamTrack
msVideoTrack.stop();
```
