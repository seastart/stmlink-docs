---
title: "Screen sharing"
description: "Share the screen with the Web SDK: create, capture, preview, and publish a LocalScreenTrack, handle the browser's built-in Stop sharing button via TRACK_ENDED, capture system audio, ScreenCaptureOptions parameters, and the ScreenPresets."
---

### Basic screen sharing

Screen sharing uses `LocalScreenTrack`, and the flow is similar to the camera:

```typescript
import {
  SRTC,
  LocalScreenTrack,
  ScreenPresets,
  ChannelEventType,
} from '@seastart/srtc-web-sdk';

const srtc = new SRTC();
let localScreenTrack: LocalScreenTrack | undefined;

const openScreen = async () => {
  // Create a screen sharing track with the 1080p preset
  localScreenTrack = srtc.createLocalScreenTrack(ScreenPresets['1080p']);

  // Start capture (the browser shows a screen picker)
  await localScreenTrack.startCapture();

  // Local preview (optional)
  localScreenTrack.addPlayView(document.querySelector<HTMLElement>('#screen-preview')!);

  // Publish
  await srtc.publishLocalTrack(localScreenTrack, { desc: 'screen' });
};

const closeScreen = async () => {
  if (!localScreenTrack) return;
  await srtc.unpublishLocalTrack(localScreenTrack);
  localScreenTrack.removeAllPlayViews();
  localScreenTrack.stopCapture();
  localScreenTrack = undefined;
};
```

---

### Handle the browser's built-in "Stop sharing" button

When the user clicks the "Stop sharing" button at the bottom of the browser, the SDK fires the `TRACK_ENDED` event, and you need to clean up state in the event callback:

```typescript
srtc.onNotifyChannelEvent = async (evt) => {
  if (evt.type === ChannelEventType.TRACK_ENDED) {
    if (evt.data === localScreenTrack) {
      // The user clicked the browser's "Stop sharing"; clean up proactively
      await closeScreen();
      // Update your UI state (e.g., hide the "Sharing" indicator)
    }
  }
};
```

---

### Capture system audio at the same time

Some browsers (Chrome 74+, Windows/macOS) support capturing **system audio** (such as audio from a playing video) while sharing the screen.

`createLocalScreenTrack` accepts a second parameter `audioPreset`; when you pass it, the SDK also captures system audio if the system supports it:

```typescript
import {
  SRTC,
  LocalScreenTrack,
  ScreenPresets,
  ScreenAudioPresets,
} from '@seastart/srtc-web-sdk';

const srtc = new SRTC();

// Create a screen sharing track and request system audio capture at the same time
const localScreenTrack = srtc.createLocalScreenTrack(
  ScreenPresets['1080p'],
  ScreenAudioPresets.default,  // Second parameter: system audio preset
);

await localScreenTrack.startCapture();

// Get the system audio track (if the browser supports it and the user checked "Share audio")
const screenAudioTrack = localScreenTrack.getAudioTrack();
if (screenAudioTrack) {
  // Publish the system audio to the channel too
  await srtc.publishLocalTrack(screenAudioTrack, { desc: 'screen_audio' });
  console.log('System audio published');
} else {
  console.warn('System audio capture is not supported in this environment, or the user did not check "Share audio"');
}

// Publish the screen sharing video
await srtc.publishLocalTrack(localScreenTrack, { desc: 'screen' });
```

> **Note:**
> + System audio capture is only reliably supported in Chrome (Windows/macOS)
> + Safari and Firefox don't support system audio capture
> + The user must check "Share audio" in the browser dialog for `getAudioTrack()` to return a valid track
> + When you stop sharing, remember to also call `unpublishLocalTrack(screenAudioTrack)` and `stopCapture()`

---

### ScreenCaptureOptions parameters

You can pass the following parameters when calling `localScreenTrack.startCapture(options)`:

| Parameter | Type | Description |
| --- | --- | --- |
| `width` | `number` | Desired capture width |
| `height` | `number` | Desired capture height |
| `frameRate` | `number` | Desired frame rate |
| `contentHint` | `'motion' \| 'detail' \| 'text'` | Content type hint that affects the encoding strategy: `motion` suits video/games, `detail` suits images/graphics, `text` suits documents/code |
| `showCursor` | `boolean` | Whether to show the mouse cursor |
| `rect` | `{ x, y, w, h }` | Region cropping parameter on Windows; on other platforms just pass `{ x: 0, y: 0, w: 0, h: 0 }` |

```typescript
await localScreenTrack.startCapture({
  frameRate: 15,
  contentHint: 'detail',  // Use when sharing documents/code to improve sharpness
  showCursor: true,
});
```

---

### Presets (ScreenPresets)

| Preset | Resolution | Frame rate | Bitrate | Description |
| --- | :---: | :---: | :---: | --- |
| `ScreenPresets['1080p']` | 1920×1080 | 10 fps | 2 Mbps | Default preset; medium priority and maintain-resolution degradation by default |
| `ScreenPresets['720p']` | 1280×720 | 10 fps | 1.5 Mbps | Medium priority and maintain-resolution degradation by default |
