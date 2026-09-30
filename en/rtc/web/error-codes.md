---
title: "Error codes"
description: "Error codes of the SRTC Web SDK (0.7.0 and later): how to check SdkError's code / baseCode, how the language parameter affects the language of server errors, and the meaning, common causes, and suggested user messages for the 106xxx client codes. Read when handling join, capture, publish, or subscribe failures."
---

<Warning>
**Since 0.7.0, error codes have been renumbered and error messages are in English** (breaking change). This page lists codes for 0.7.0 and later; older versions mostly used `106000`. See [Changelog · v0.7.0](/en/rtc/web/changelog) for the old-to-new mapping.
</Warning>

### How to check an error

Errors thrown by the SDK are `SdkError` (extends `Error`; the package exports `SdkError` and `ErrorCode`):

| Field | Description |
| --- | --- |
| `code` | Full error code. The SDK's own errors are `106` + a 3-digit low code (for example `106231`); `1000`–`99999` are business error codes returned by the server, passed through unchanged |
| `baseCode` | The low 3-digit code, matching the `ErrorCode` enum and meaning the same in every SDK; for server error codes it returns the code itself |
| `message` / `msg` | Error details (the two are identical; `msg` is kept for backward compatibility). The SDK's own errors are always in English; server error messages follow `language` |
| `name` / `cause` | On capture failures, `name` keeps the browser's original value (for example `NotAllowedError`), and the original exception is in `cause` |

**Check `code` / `baseCode`, not the message text**—messages are for developers and logs and change between versions. For messages shown to end users, map codes yourself using the "Suggested user message" column below; don't show `message` directly.

```typescript
import { SRTC, SdkError, ErrorCode } from '@seastart/srtc-web-sdk';

try {
  await camera.startCapture();
} catch (e) {
  if (e instanceof SdkError) {
    switch (e.baseCode) {
      case ErrorCode.CameraPermissionDenied: // 106231
        showToast('Please allow camera access in your browser');
        break;
      case ErrorCode.CaptureFailed:          // 106018
        showToast('The device may be in use by another app. Close it and try again');
        break;
      default:
        console.error(e.code, e.message);
    }
  }
}
```

### The language parameter

The `language` init parameter sets the SDK language (a language tag such as `zh-CN` or `en`). It's a process-wide global setting:

```typescript
const srtc = new SRTC({
  language: 'en',   // if omitted, follows navigator.language; falls back to zh
});
```

+ The SDK sends `Accept-Language` with its server requests, and **the `message` of server business errors (`1000`–`99999`) comes back in Chinese or English accordingly**
+ The prompt shown when the browser blocks autoplay uses Chinese or English according to `language`; override the text with the `autoPlayDialogText` init parameter
+ **The SDK's own errors (`106xxx`) are always in English and aren't affected by `language`**

---

### Client error codes

For the cross-platform meaning of the low 3 digits, see [Error code format and unified table](/en/rtc/error-codes). "Suggested user message" is filled in only for codes end users need to know about; the rest are mostly integration issues—check "Common causes".

| Code | `ErrorCode` | Meaning | Common causes | Suggested user message |
| --- | --- | --- | --- | --- |
| `106000` | `Unknown` | Unclassified error | Fallback code that shouldn't normally appear; check `message` and the logs | —— |
| `106001` | `NotInChannel` | Not in the channel | Not joined yet, or a channel method such as publish / subscribe was called after leaving the channel | —— |
| `106002` | `TokenExpired` | The token has expired | The token was past its validity period when joining the channel or enabling IM; issue a new one | —— |
| `106003` | `TrackNotFound` | The track doesn't exist | No remote track matches the uid + id / desc: the other side hasn't published it or has unpublished it | —— |
| `106005` | `AlreadyJoined` | Already joined | IM was enabled twice, or the whiteboard was joined twice | —— |
| `106006` | `ConnectionFailed` | Connection failed | The network request failed or HTTP wasn't 200 (the status is in `message`), or an SFU API still failed after retries | Network error. Check your connection and try again |
| `106007` | `ConnectionTimeout` | Connection timed out | The media connection couldn't be established when joining the channel; check that UDP is allowed | Network error. Check your connection and try again |
| `106009` | `SignalingConnectFailed` | Failed to connect to signaling | The signaling service is unreachable; check the network and firewall | Network error. Check your connection and try again |
| `106010` | `SignalingSubscribeFailed` | Failed to subscribe to signaling | Same as above | Network error. Check your connection and try again |
| `106011` | `MessageDecodeFailed` | Failed to parse the response | The API response isn't JSON or is missing the `code` field—usually the service URL points to the wrong service, or a proxy is rewriting responses | —— |
| `106013` | `SdpNegotiationFailed` | SDP negotiation failed | The SDP exchange API of the CDN media streaming engine returned an error | —— |
| `106014` | `TransportNotReady` | Transport not ready | The channel or media streaming engine is reconnecting, or the publish / subscribe media connection isn't connected yet; **retry later** | Network error. Check your connection and try again |
| `106015` | `PeerConnectionFailed` | Media connection failed | The publish / subscribe PeerConnection entered failed / closed; check the network and UDP ports | Network error. Check your connection and try again |
| `106018` | `CaptureFailed` | Capture failed | The device is in use by another app, or a hardware error (browser `NotReadableError` / `AbortError`) | The device may be in use by another app. Close it and try again |
| `106019` | `CodecNotSupported` | Codec not supported | The browser lacks OPUS / H264 | This browser doesn't support this feature. Use the latest Chrome or Edge |
| `106020` | `MaxPublishLimitReached` | Publish limit exceeded | The number of published audio / video tracks has reached the media streaming engine's limit | —— |
| `106021` | `DeviceNotFound` | The device doesn't exist | No camera / microphone found, or the specified `deviceId` was unplugged (browser `NotFoundError` / `OverconstrainedError`) | No camera or microphone found. Check the device connection |
| `106022` | `EngineNotSupported` | Media streaming engine not supported | The server assigned a media streaming engine this SDK version doesn't recognize; upgrade the SDK | —— |
| `106024` | `InvalidState` | The operation isn't allowed in the current state | Wrong call order, for example the instance was destroyed or local user info isn't ready yet | —— |
| `106025` | `InternalError` | SDK internal error | For example a processor plugin didn't produce a track. Contact us with the logs | —— |
| `106026` | `Cancelled` | The operation was canceled | The channel was left during the call | —— |
| `106031` | `InvalidArgument` | Invalid argument | A required argument is empty, the `MediaStreamTrack` passed in is the wrong kind, and so on | —— |
| `106032` | `FeatureNotSupported` | The browser doesn't support this capability | Screen sharing, Picture-in-Picture, simulcast, local recording (MediaRecorder), and so on | This browser doesn't support this feature. Use the latest Chrome or Edge |
| `106033` | `TrackNotCaptured` | The track isn't captured | Published, played, or set a processor without calling `startCapture` (or after it stopped) | —— |
| `106034` | `MaxSubscribeLimitReached` | Subscribe limit exceeded | The number of subscribed audio / video tracks has reached the media streaming engine's limit | —— |
| `106035` | `PublishDescConflict` | Publish description conflict | The same `desc` (or CDN stream slot) is already used by another track; use a different `desc` or unpublish first | —— |
| `106036` | `PlayFailed` | Playback failed | Playback failed and it wasn't caused by the browser's autoplay policy (autoplay blocking is reported through the `track_autoplay_fail` event) | Playback failed. Refresh the page and try again |
| `106037` | `PlayViewNotFound` | The playback container doesn't exist | Picture-in-Picture / pop-out was given a container that was never passed to `addPlayView` | —— |
| `106038` | `PopupBlocked` | The popup was blocked | `window.open` was blocked by the browser during pop-out playback | The popup was blocked. Allow popups for this site |
| `106039` | `ScreenShareDenied` | Screen sharing was denied | The user canceled in the picker, or the system didn't allow the browser to record the screen | Screen sharing was canceled. If no picker appeared, allow screen recording for the browser in system settings |
| `106204` | `UserNotFound` | No such user in the channel | The uid being subscribed / queried isn't in the channel | —— |
| `106231` | `CameraPermissionDenied` | Camera permission denied | The user or system denied camera access (browser `NotAllowedError` / `SecurityError`) | Please allow camera access in your browser |
| `106251` | `MicPermissionDenied` | Microphone permission denied | The user or system denied microphone access | Please allow microphone access in your browser |
| `106300` | `PublishFailed` | Publish failed | Published while the media streaming engine wasn't connected or was disconnected (not reconnecting) | Network error. Check your connection and try again |
| `106301` | `SubscribeFailed` | Subscribe failed | Subscribed while the media streaming engine wasn't connected or was disconnected (not reconnecting) | Network error. Check your connection and try again |
| `106302` | `PublishTimeout` | Publish negotiation timed out | The CDN media streaming engine timed out publishing; the network is down or the server is unreachable | Network error. Check your connection and try again |
| `106303` | `SubscribeTimeout` | Subscribe negotiation timed out | Same as above (subscribe) | Network error. Check your connection and try again |

---

### Server error codes

Codes from `1000` to `99999` come from the server and are passed through unchanged by the SDK. When showing them to users, **show the `message` returned by the server directly** (its language follows `language`). Common ones:

| Code | Description |
| :---: | --- |
| `1011` | Invalid app |
| `1021` | The channel token has already been used |
| `1022` | The session isn't in the channel |
| `1023` | The user isn't in the channel |
| `1024` | The channel isn't open |
| `1025` | The channel is already open |

See [Server API · Error codes](/en/rtc/server-api/error-codes) for the full list.
