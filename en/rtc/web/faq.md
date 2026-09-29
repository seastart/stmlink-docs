---
title: "FAQ"
description: "Common Web SDK problems and fixes: camera/microphone permission denied, can receive but not publish in local development, autoplay blocked by the browser, screen sharing limits on Safari, TokenExpired when joining, and joining multiple channels at once."
---

### What if the browser says "access to the camera/microphone is not allowed"?

**Cause:** the browser permission was denied, or the page isn't in a secure context (HTTPS / localhost).

**Steps to fix:**

1. Make sure the page is accessed over HTTPS or localhost (plain HTTP domains can't access media devices)
2. Click the camera/microphone icon on the right side of the browser address bar and change the permission to "Allow"
3. If you previously chose "Always block", reset the permission manually in the browser's site settings:
   - Chrome: "🔒" on the left of the address bar → "Site settings" → "Camera/Microphone" → "Allow"
4. Refresh the page and try again

You can check in advance whether the environment can capture media through the `secure` and `mediaDevices` fields of `srtc.getEnvInfo()`:

```typescript
const env = srtc.getEnvInfo();
if (!env.secure) {
  alert('Please access this page over HTTPS or localhost');
} else if (!env.mediaDevices) {
  alert('This browser does not support media device access. Please check your permission settings');
}
```

---

### What if I can receive but not publish during local development?

**Cause:** most likely the page is running over plain HTTP, and the browser restricts WebRTC publishing.

**Solution:** access your local development environment via `http://localhost` or `http://127.0.0.1`, not `http://[local LAN IP]` (publishing isn't supported over that protocol).

For protocol and publishing support, see [Integration - URL protocol restrictions](/en/rtc/web/integration#url-protocol-restrictions).

---

### How do I handle video/audio autoplay being blocked by the browser?

The browser's autoplay policy forbids playing media without a user gesture; the symptom is no audio or no video after calling `startPlay()`.

The SDK notifies you through the `TRACK_AUTOPLAY_FAIL` event:

```typescript
srtc.onNotifyChannelEvent = (evt) => {
  if (evt.type === ChannelEventType.TRACK_AUTOPLAY_FAIL) {
    // Option 1: the SDK's built-in guide dialog (on by default)
    // Playback starts automatically after the user clicks the dialog

    // Option 2: handle it yourself and play again when the user clicks a button
    const failedTrack = evt.data; // BaseTrack
    document.querySelector('#play-btn')!.addEventListener('click', async () => {
      if (failedTrack instanceof RemoteAudioMixTrack) {
        await failedTrack.startPlay({ disableAutoPlayDialog: true });
      }
    }, { once: true });
  }
};
```

> **Best practice:** call `join` and `startPlay` after the user actively clicks a "Join" or "Start call" button; this user gesture context usually gets around the autoplay restriction.

---

### Is screen sharing unavailable on Safari?

Safari 15.4 and above support `getDisplayMedia` (screen sharing), with these limitations:

+ Capturing **system audio** isn't supported (`getAudioTrack()` returns `undefined`)
+ **Screen sharing isn't supported** on iOS Safari (a system limitation)
+ Some older Safari versions (< 15.4) don't support screen sharing at all

You can check in advance whether the current environment supports it with `srtc.getEnvInfo().screenshare`:

```typescript
const env = srtc.getEnvInfo();
if (!env.screenshare) {
  alert('This browser does not support screen sharing. Please use Chrome or desktop Safari 15.4+');
}
```

---

### What if joining the channel fails with TokenExpired?

The token is issued by the server and has a short validity period (usually from a few minutes to a few hours, decided by the issuer).

**Solution:**
+ Get a fresh token from the server right before calling `srtc.join()`; don't cache old tokens
+ Check that the client and server system clocks are in sync (clock skew can make the token expire early)

---

### How do I join multiple channels at once?

Call `join` multiple times on one `SRTC` instance. Each `join` returns that channel's Channel object, and each channel is operated independently:

```typescript
const channel1 = await srtc.join(token1);
const channel2 = await srtc.join(token2);

await channel1.publishLocalTrack(track);
await channel2.leave(); // Leave channel 2 without affecting channel 1
```

For event isolation, publishing one captured track to multiple channels, and more, see [Multi-channel](/en/rtc/web/advanced/multi-channel).

Note: running multiple channels in parallel uses more bandwidth and system resources, so use it only when needed.
