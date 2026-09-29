---
title: "Multi-window and dual-screen video layout"
description: "Show video in separate windows with the Web SDK: pop out a track to its own window for dual-screen layouts, keep a floating camera window via picture-in-picture while sharing the screen, sync UI with TRACK_PIP_* / TRACK_POPOUT_* events, and clean up when sharing ends."
---

When your app needs to put video in a separate window or on a second monitor, or keep a small window of your own camera while sharing the screen, you can combine the following capabilities:

+ `enterPictureInPicture(container, options?)`
+ `popOutToWindow(container, options?)`
+ `closePopOutWindow(container)`
+ `ChannelEventType.TRACK_PIP_ENTER / TRACK_PIP_EXIT`
+ `ChannelEventType.TRACK_POPOUT_OPEN / TRACK_POPOUT_CLOSE`

---

### Scenario 1: dual-screen layout

Typical requirements:

+ Monitor A shows the remote shared desktop
+ Monitor B shows the local camera or a remote person's video

The recommended approach:

+ Keep using `addPlayView(container)` on the main page to maintain the video card structure
+ When the user clicks "Pop out", call `popOutToWindow`
+ Drag the new window popped out by the browser to the second monitor

```typescript
const remoteScreenTrack = await srtc.subscribeRemoteVideoTrack(uid, trackId);
remoteScreenTrack.addPlayView(document.querySelector('#remote-screen')!);

remoteScreenTrack.popOutToWindow(
  document.querySelector('#remote-screen')!,
  {
    title: 'Remote shared desktop',
    width: 1600,
    height: 900,
    hideOriginView: true,
  }
);

localCameraTrack.addPlayView(document.querySelector('#local-camera')!);
localCameraTrack.popOutToWindow(
  document.querySelector('#local-camera')!,
  {
    title: 'My camera',
    width: 480,
    height: 360,
    hideOriginView: true,
  }
);
```

> `hideOriginView` defaults to `true`. For separate-window mode, we generally recommend keeping the default, to avoid rendering the same video in both the main page and the popped-out window.

---

### Scenario 2: keep a floating camera window while sharing the desktop

Typical requirements:

+ The user starts desktop sharing
+ The main browser window may be minimized or covered by other apps
+ The user still wants a small window of their own camera in the top-right corner to confirm how they appear on camera

Recommended combination:

+ Use `LocalScreenTrack` for desktop sharing
+ Use `LocalCameraTrack.enterPictureInPicture(...)` to put the camera into picture-in-picture

```typescript
const localScreenTrack = srtc.createLocalScreenTrack(ScreenPresets['1080p']);
await localScreenTrack.startCapture({ contentHint: 'detail' });
localScreenTrack.addPlayView(document.querySelector('#screen-preview')!);
await srtc.publishLocalTrack(localScreenTrack, { desc: 'screen' });

const localCameraTrack = srtc.createLocalCameraTrack(CameraPresets['720p']);
await localCameraTrack.startCapture();
localCameraTrack.addPlayView(document.querySelector('#camera-preview')!);
await srtc.publishLocalTrack(localCameraTrack, { desc: 'camera_big' });

await localCameraTrack.enterPictureInPicture(
  document.querySelector('#camera-preview')!,
  {
    width: 320,
    height: 240,
    hideOriginView: true,
  }
);
```

> If the current browser supports `Document PiP`, the SDK uses it first; otherwise it falls back to the traditional `video PiP`. Traditional `video PiP` relies on the original `video` element, so the original view isn't hidden.

---

### Sync UI state with channel events

PiP / pop-out windows usually need to keep button labels, badges, or overlay hints in sync. We recommend using channel events for this rather than maintaining scattered state yourself.

```typescript
srtc.onNotifyChannelEvent = (evt) => {
  switch (evt.type) {
    case ChannelEventType.TRACK_PIP_ENTER:
      console.log('Track entered picture-in-picture', evt.data);
      break;
    case ChannelEventType.TRACK_PIP_EXIT:
      console.log('Track exited picture-in-picture', evt.data);
      break;
    case ChannelEventType.TRACK_POPOUT_OPEN:
      console.log('Track popped out to a separate window', evt.data);
      break;
    case ChannelEventType.TRACK_POPOUT_CLOSE:
      console.log('Track closed its separate window', evt.data);
      break;
  }
};
```

---

### Cleanup when sharing ends

If the user clicks the browser's native "Stop sharing", the SDK fires `TRACK_ENDED`. At a minimum, clean up the sharing track itself:

```typescript
srtc.onNotifyChannelEvent = async (evt) => {
  if (evt.type === ChannelEventType.TRACK_ENDED && evt.data === localScreenTrack) {
    await srtc.unpublishLocalTrack(localScreenTrack);
    localScreenTrack.removeAllPlayViews();
    localScreenTrack.stopCapture();
  }
};
```

> For the same `track`, `removePlayView(container)` and `removeAllPlayViews()` automatically clean up the picture-in-picture / pop-out window state associated with that track, so you don't need to call that track's `exitPictureInPicture` or `closePopOutWindow` again.
>
> If your product wants "when sharing ends, close the floating camera window too", that's a linkage policy at your app layer; you can additionally exit picture-in-picture for `localCameraTrack`, but it isn't a required step for SDK resource cleanup.

---

### Best practices

+ `Picture-in-picture` suits small videos you want to "glance at any time", such as the local camera or self-preview
+ `Pop-out windows` suit dual-screen collaboration and large displays, such as a remote shared desktop or the presenter's video
+ If your UI needs to restore button states automatically, listen for the `TRACK_PIP_*` and `TRACK_POPOUT_*` events first
