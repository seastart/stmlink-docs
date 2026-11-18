---
title: "Device checks (pre-meeting / in-meeting preview)"
description: "Check the camera, microphone, and speaker before or during a meeting: list devices with getDevices, capture without publishing via publish: false on requestOpenCamera / requestOpenMic, read the mic level with getVolume, decide whether to close with isCameraOpened / isMicOpened, and test speakers with <audio> + setSinkId"
---

### Overview

A pre-meeting device check page and an in-meeting settings page both need to "turn the device on to see and hear it without sending it to anyone". How each check works on the Web meeting layer:

| Check | How |
| --- | --- |
| Device list | `getDevices(kind)` |
| Camera preview | `requestOpenCamera(container, deviceId, preset, false, undefined, false)` (`publish: false`) |
| Mic level | `getVolume()` on the track returned by `requestOpenMic(deviceId, preset, false, undefined, false)` |
| Speaker test | The SDK has no API; play a test sound yourself with `<audio>` + `setSinkId` |

`publish: false` is available since `0.3.5`: it only captures and previews, without asking the meeting for permission, publishing, or firing state events, and you can call it before or during a meeting. The host turning off your device or disabling it for everyone doesn't affect a preview-only track.

---

### Device list

```typescript
const cameras = await meeting.getDevices("videoinput");
const microphones = await meeting.getDevices("audioinput");
const speakers = await meeting.getDevices("audiooutput");
```

Browsers don't return device names before permission is granted, so when the names are empty the SDK first requests camera / microphone permission once. Pass `false` as the second argument if you don't want to trigger the permission prompt.

---

### Camera preview

```typescript
// Open the preview: pass false as the last argument, publish
const camTrack = await meeting.requestOpenCamera(previewEl, cameraId, undefined, false, undefined, false);

// Switch cameras: call it again with the new deviceId
await meeting.requestOpenCamera(previewEl, newCameraId, undefined, false, undefined, false);

// Close the preview
if (!meeting.isCameraOpened()) {
  await meeting.closeCamera();           // Close only a preview-only camera
} else {
  camTrack.removePlayView(previewEl);    // The meeting camera is on: remove only the preview container you added
}
```

+ **Deciding to turn the camera on after previewing**: call `requestOpenCamera()` again with the default `publish: true`. It asks the meeting for permission and publishes **the same track**, without restarting capture.
+ **Opening a preview while the meeting camera is already on**: `publish: false` just returns the track in use and adds the `container` you pass as a preview, without starting another capture.
+ **A camera opened with default parameters before entering a meeting**: calling `requestOpenCamera()` again after entering publishes it to the meeting.

---

### Mic level

```typescript
const micTrack = await meeting.requestOpenMic(micId, undefined, false, undefined, false);

const timer = setInterval(() => {
  volumeBar.style.width = `${micTrack.getVolume()}%`;   // getVolume() returns 0–100
}, 100);

// When the check ends
clearInterval(timer);
if (!meeting.isMicOpened()) {
  await meeting.closeMic();
}
```

+ Processors set with [`setAudioProcessor()`](/en/meeting/web/advanced/deepfilternet) (such as AI noise suppression) are attached during capture-only too, so you can hear and see the result after noise suppression directly.
+ Deciding to open the mic after testing, the meeting mic already being on, and opening before entering a meeting follow the same rules as the camera; use `isMicOpened()` to decide whether to close it.

---

### Speaker test

The SDK has no API for playing a test sound. Play it with the browser's `<audio>`, and choose the output device with `setSinkId` (some browsers don't support `setSinkId`; there you can only use the system default output):

```typescript
const audio = new Audio("/assets/test-tone.mp3");
if ("setSinkId" in audio) {
  await (audio as any).setSinkId(speakerId);
}
await audio.play();
```

To use the chosen speaker for remote audio in the meeting, pass it through `toggleRemoteAudioMute(false, { deviceId: speakerId })`.

---

### Related pages

+ [SMeeting API](/en/meeting/web/api-reference/SMeeting)
+ [AI noise suppression](/en/meeting/web/advanced/deepfilternet)
