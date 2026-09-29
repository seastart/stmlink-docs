---
title: "Local recording"
description: "Record the current user's call view in the browser with LocalCompositeRecorder: composite video tiles you lay out yourself plus mixed audio into one webm file, start options and video item fields, updating the view, pause/resume, chunked upload, state, and cleanup."
---

### Overview

Local recording suits recording "the call view the current user sees" in the browser: for example a 3-tile or 9-tile grid, the current page after paging, or a layout that prioritizes screen sharing. The SDK draws the video tracks you pass in onto an internal canvas, mixes the audio tracks into the same recording stream, and finally outputs a webm file through `MediaRecorder`. Your app decides which videos to record right now and where each one goes on the recording canvas.

`LocalCompositeRecorder` only handles media compositing and the recording lifecycle and **has no built-in call layout algorithm**—your app passes in the layout based on the current UI view.

---

### Basic usage

```typescript
const recorder = srtc.createLocalCompositeRecorder();

await recorder.start({
  width: 1280,
  height: 720,
  fps: 15,
  videoItems: [
    {
      id: 'local-camera',
      track: localCameraTrack,
      label: 'Me',
      rect: { x: 0, y: 0, width: 640, height: 360 },
      fit: 'contain',
    },
    {
      id: 'remote-user-1-camera',
      track: remoteVideoTrack,
      label: 'Remote user',
      rect: { x: 640, y: 0, width: 640, height: 360 },
      fit: 'contain',
    },
  ],
  audioTracks: [
    localMicTrack,
    remoteAudioMixTrack,
  ],
});

// After the call view pages, the grid changes, or subscriptions change, update the current recording view.
recorder.updateVideoItems(nextVideoItems);
await recorder.updateAudioTracks(nextAudioTracks);

// Pause and resume apply to the same final file.
recorder.pause();
recorder.resume();

// Stop recording and return the complete webm Blob.
const blob = await recorder.stop();
```

Once you have the `blob`, you can download or upload it:

```typescript
const url = URL.createObjectURL(blob);
const a = document.createElement('a');
a.href = url;
a.download = 'recording.webm';
a.click();
URL.revokeObjectURL(url);
```

---

### Start options

`LocalCompositeRecorderStartOptions` for `start(options)`:

| Field | Type | Default | Description |
| --- | --- | --- | --- |
| `videoItems` | `LocalCompositeRecorderVideoItem[]` | — | Initial list of videos to draw, required |
| `audioTracks` | `LocalCompositeRecorderTrack[]` | — | Audio tracks mixed into the recording file |
| `width` | `number` | `1280` | Output video width (pixels) |
| `height` | `number` | `720` | Output video height (pixels) |
| `fps` | `number` | `15` | `canvas.captureStream` frame rate |
| `mimeType` | `string` | Auto | If omitted or unsupported, a webm format supported by the browser is chosen automatically |
| `timeslice` | `number` | — | `MediaRecorder` chunk interval (milliseconds); if omitted, everything is returned at once on `stop` |
| `background` | `string` | `#101216` | Overall background color of the recording canvas |
| `labelBackground` | `string` | `rgba(0,0,0,0.58)` | Label background color |
| `onDataAvailable` | `(blob: Blob) => void` | — | Fires each time a valid chunk is output; can be used to upload while recording |

`LocalCompositeRecorderVideoItem` (a single video item):

| Field | Type | Default | Description |
| --- | --- | --- | --- |
| `id` | `string` | — | Stable unique identifier maintained by the caller; when the track for the same id changes, the slot is reused and the decode source replaced |
| `track` | `LocalCompositeRecorderTrack \| null` | — | Video track to draw; pass `null` for an empty slot |
| `rect` | `{ x, y, width, height }` | — | Drawing area on the canvas (canvas pixel coordinates) |
| `label` | `string` | — | Label drawn in the bottom-left corner (such as the user name); not drawn if omitted |
| `avatar` | `string` | — | URL of the round avatar drawn in the center of the tile when the camera is off (no video track); loaded anonymously cross-origin, and falls back to a gray circle with the nickname's first letter if loading fails or cross-origin access is refused |
| `fit` | `'contain' \| 'cover'` | `contain` | `contain` keeps the full video, `cover` fills the area and crops the overflow |
| `background` | `string` | `#1a1c22` | Background color of a single slot |

---

### Input tracks

Both `videoItems[].track` and `audioTracks[]` accept an SDK Track or a native browser `MediaStreamTrack`:

+ `LocalVideoTrack`
+ `RemoteVideoTrack`
+ `LocalAudioTrack`
+ `RemoteAudioTrack`
+ `MediaStreamTrack`

If you pass an SDK Track, the recorder listens for internal media track replacement events and automatically switches to the new track when a reconnect or resubscription changes the underlying `MediaStreamTrack`, with no action needed from your app.

---

### Layout responsibility

`LocalCompositeRecorder` has no built-in call layout algorithm. Your app should generate `videoItems` based on the current UI view:

+ If only 3 users are shown right now, pass only those 3 video items.
+ If it's a 9-tile grid, compute `rect` for 9 slots.
+ After the user pages left or right, call `updateVideoItems(...)` to switch to the new page.
+ Special layouts such as screen sharing or speaker mode also have their `rect` computed by your app.

This way the recording follows the current view passed in by your app, rather than always recording all remote streams.

---

### Audio recommendations

For call recording, we generally recommend passing in both the local microphone track and the remote mixed audio track:

```typescript
const remoteAudioMixTrack = await srtc.subscribeRemoteAudioMixTrack();

await recorder.updateAudioTracks([
  localMicTrack,
  remoteAudioMixTrack,
]);
```

To record only remote audio, pass only `remoteAudioMixTrack`; to record only the local microphone, pass only `localMicTrack`.

---

### Upload while recording

Pass `timeslice` and `onDataAvailable` to get data in chunks in real time, for uploading or writing to disk while recording, so long recordings don't take up a lot of memory:

```typescript
await recorder.start({
  videoItems,
  audioTracks,
  timeslice: 5000, // Produce a chunk every 5 seconds
  onDataAvailable: (chunk) => {
    uploadChunk(chunk); // Your app's upload logic
  },
});
```

> Note: webm chunks are a streaming container; a single chunk usually can't be played on its own, and the server needs to concatenate them in order into a complete file.

---

### State and cleanup

```typescript
// 'inactive' not started or ended | 'recording' recording | 'paused' paused
const state = recorder.getState();

// Release internal resources (canvas, AudioContext, MediaRecorder, etc.) when no longer needed
recorder.destroy();
```

---

### Notes

- Must run over HTTPS (or localhost); `AudioContext` may need a user gesture before it can start.
- The output format is webm; browsers support different codecs (vp9/vp8/opus), and the SDK falls back to an available format automatically.
- `pause` / `resume` apply to the same final file and don't produce multiple files.
- The higher the recording resolution and frame rate, the higher the CPU usage; choose `width`/`height`/`fps` to suit your scenario.
