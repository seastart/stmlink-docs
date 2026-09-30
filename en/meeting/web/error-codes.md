---
title: "Error codes"
description: "Error codes of the SMeeting Web SDK (0.3.0 and later): how to tell meeting-layer 206xxx codes, passed-through SRTC 106xxx codes, and server business codes apart by code, how the language parameter affects the language of server errors, and each code's meaning, common causes, and suggested user message."
---

<Warning>
**Since 0.3.0, error codes have been renumbered and error messages are in English** (breaking change). This page lists codes for 0.3.0 and later; older versions used `206000` for everything except `206001`–`206004`. See [Changelog · v0.3.0](/en/meeting/web/changelog) for the old-to-new mapping.
</Warning>

### How to check an error

Errors thrown by the conferencing SDK can come from three places. **Tell them apart by the full `code`**:

| `code` | Source | Description |
| --- | --- | --- |
| `206xxx` | Meeting-layer SDK | See "Meeting-layer error codes" below |
| `106xxx` | Underlying SRTC SDK, passed through unchanged | Capture failures, device permission denied, publish / subscribe failures, and so on; see [SRTC Web error codes](/en/rtc/web/error-codes) |
| `1000`–`99999` | Server business errors, passed through unchanged | For the meeting server, see [Server API error codes](/en/meeting/server-api/error-codes); show the `message` returned by the server directly to users |

The error object has the same fields as SRTC's `SdkError`: `code` (full code), `baseCode` (low 3 digits), and `message` / `msg` (English details). The package exports `SdkError` and `MeetingErrorCode` (meeting-layer low 3 digits).

+ **Check `code`, not the message text**—messages are for developers and logs and change between versions. For messages shown to end users, map codes yourself using the "Suggested user message" column below; don't show `message` directly
+ **The low 3 digits of the meeting layer and the SRTC layer are two independent tables** (`206003` is "not in a meeting", `106003` is "track doesn't exist"). In the conferencing SDK, compare the full `code`; comparing only `baseCode` mixes them up
+ Don't use `instanceof`: with the UMD bundle, the SDK ships its own copy of SRTC, which isn't the same class as an SRTC you import separately

```typescript
import { SMeeting } from '@seastart/smeeting-web-sdk';

try {
  await smeeting.requestOpenCamera(container);
} catch (e: any) {
  switch (e?.code) {
    case 206004: // the host has disabled turning on cameras
      showToast('The host has disabled turning on cameras');
      break;
    case 106231: // passed through from SRTC: camera permission denied
      showToast('Please allow camera access in your browser');
      break;
    case 106018: // passed through from SRTC: device in use
      showToast('The device may be in use by another app. Close it and try again');
      break;
    default:
      if (e?.code >= 1000 && e?.code < 100000) {
        showToast(e.message); // server business error; its language follows language
      } else {
        console.error(e?.code, e?.message);
      }
  }
}
```

### The language parameter

The `language` init parameter sets the SDK language (a language tag such as `zh-CN` or `en`). It's a process-wide global setting and **also applies to the underlying SRTC**:

```typescript
const smeeting = new SMeeting({
  language: 'en',   // if omitted, follows navigator.language; falls back to zh
});
```

+ Requests to both the meeting server and the SRTC server carry `Accept-Language`, and **the `message` of server business errors (`1000`–`99999`) comes back in Chinese or English accordingly**
+ The prompt shown when the browser blocks autoplay uses Chinese or English according to `language`; override the text with the `autoPlayDialogText` init parameter
+ **The SDK's own errors (`206xxx`, and passed-through `106xxx`) are always in English and aren't affected by `language`**

---

### Meeting-layer error codes

For the cross-platform meaning of the low 3 digits, see [Error code format and unified table](/en/meeting/error-codes).

| Code | `MeetingErrorCode` | Meaning | Common causes | Suggested user message |
| --- | --- | --- | --- | --- |
| `206000` | `Unknown` | Unclassified error | Fallback code that shouldn't normally appear; check `message` and the logs | —— |
| `206001` | `NotLoggedIn` | Not logged in | `login` wasn't called, or a method that requires login was called after login failed | —— |
| `206002` | `TokenExpired` | The token has expired | The token was past its validity period at `login`; issue a new one | Your session has expired. Please rejoin |
| `206003` | `NotInMeeting` | Not in a meeting | An in-meeting method was called before entering the meeting or after exiting it | —— |
| `206004` | `Unauthorized` | No permission | A non-host performed a host operation, or the room has disabled turning on the camera / mic / screen sharing | The host has disabled this action |
| `206005` | `TokenInvalid` | Invalid token | The `login` token can't be parsed; check that it was copied completely and was issued for this environment | —— |
| `206006` | `AlreadyInMeeting` | Already in a meeting | Entered a meeting again; exit the current meeting first | —— |
| `206007` | `NetworkError` | Network error | The request to the meeting server failed or HTTP wasn't 200 (the status is in `message`) | Network error. Check your connection and try again |
| `206010` | `UserNotFound` | No such member in the meeting | The uid being queried isn't in the room | —— |
| `206011` | `InvalidState` | Not allowed in the current state | Turning on the camera / mic / screen sharing when it's already on, switching devices before it's on, turning on the document camera without turning off the camera first, and so on | —— |
| `206012` | `InvalidArgument` | Invalid argument | Reserved; not used in this version | —— |
| `206356` | `ResponseParseFailed` | Failed to parse the response | The meeting server's response isn't JSON or is missing the `code` field—usually a misconfigured service URL, or a proxy is rewriting responses | —— |

---

### Passed-through SRTC error codes

Failures related to capture, permissions, and publishing / subscribing are thrown by the underlying SRTC and passed through unchanged. Common ones:

| Code | Meaning | Suggested user message |
| --- | --- | --- |
| `106231` | Camera permission denied | Please allow camera access in your browser |
| `106251` | Microphone permission denied | Please allow microphone access in your browser |
| `106039` | Screen sharing was denied | Screen sharing was canceled. If no picker appeared, allow screen recording for the browser in system settings |
| `106021` | The device doesn't exist | No camera or microphone found. Check the device connection |
| `106018` | Capture failed (device in use, and so on) | The device may be in use by another app. Close it and try again |
| `106006` / `106007` / `106014` / `106015` / `106300`–`106303` | Network / media connection failure | Network error. Check your connection and try again |

See [SRTC Web error codes](/en/rtc/web/error-codes) for the full list.
