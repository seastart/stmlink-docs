---
title: "Error code format and unified table"
description: "How SMeeting error codes are numbered, the meeting-layer cross-platform unified table, and why you see both 20Nxxx and 10Nxxx codes. Covers the language parameter, which platforms have shipped the new codes, and old-to-new mappings. Read when you get an unfamiliar error code or upgrade an SDK."
---

`0` means success; anything non-zero is an error.

There are two kinds of error codes: **4–5 digit codes are business error codes returned by the server**, and **6-digit codes are produced by the client SDK itself**. A 6-digit code is **platform prefix + 3-digit low code**. The meeting layer's low 3 digits are assigned from the unified table on this page, and **the same low code means the same thing on every platform**.

---

## How to read an error code

```text
  2 0 6 0 0 3
  │ │ │ └─┴─┴── Low code 000-999: 003 = not in a meeting (same on every platform)
  │ │ └──────── Platform type: 6 = Web
  └─┴────────── Product layer: 20 = SMeeting
```

| Digits | Source | Structure | Example |
| --- | --- | --- | --- |
| 4–5 digits (1000–99999) | Returned by the **server**, passed through unchanged by the SDK | Server error code | `2xxx` meeting service business errors |
| 6 digits | Produced by the meeting-layer **SDK** | `20` + platform type + low 3 digits | `206003` Web: not in a meeting |

---

## Platform types

| Type | Platform | SMeeting prefix |
| :---: | --- | --- |
| 1 | Windows | `201` |
| 2 | Android phone | `202` |
| 3 | iOS phone | `203` |
| 4 | Linux C/C++ | `204` |
| 5 | macOS | `205` |
| 6 | Web | `206` |
| 7 | Mini Program | `207` |
| 8 | HarmonyOS NEXT | `208` |
| 9 | Android embedded | `209` |

<Note>
The Swift SDK supports both iOS and macOS and automatically uses the `203` or `205` prefix depending on the platform it runs on.
</Note>

---

## Why you see error codes starting with 10Nxxx

**This is expected, not a bug.**

SMeeting is built on SRTC. When an error occurs in the underlying audio and video layer (for example capture failure, device permission denied, or publish / subscribe failure), SMeeting passes SRTC's original error code through to you **as-is** instead of wrapping it in its own code—so you can pinpoint which layer the problem is in.

| What you see | Meaning | Where to look |
| --- | --- | --- |
| `2xxx` and similar | The meeting server rejected the request (no permission, meeting doesn't exist, etc.) | [Server API error codes](/en/meeting/server-api/error-codes) |
| `20Nxxx` | An error from the meeting-layer SDK | The unified table below and the error code page for that platform |
| `1xxx` | An error from the underlying SRTC **server** | [SRTC error code format and unified table](/en/rtc/error-codes) |
| `10Nxxx` | An error from the underlying SRTC **client** (for example "camera permission denied", `106231`) | [SRTC error code format and unified table](/en/rtc/error-codes) |

The low 3 digits of the meeting layer and the SRTC layer are **two independent tables**: seeing both `206003` and `106003` in the Web conferencing SDK is not a contradiction—the former is "not in a meeting" and the latter is "track doesn't exist". So in a conferencing SDK, compare the **full 6-digit code**, not just the low 3 digits.

<Tip>
When troubleshooting, look at the first two digits first: if it starts with `20`, look for meeting-layer causes (permissions, meeting state, member roles); if it starts with `10`, look for audio and video layer causes (devices, token, channel, network).
</Tip>

---

## Branch on codes, not messages

+ **Decide the error type by its code only.** The SDK's own error messages are always in English, are meant for developers and logs, and change between versions. Don't branch on them, and don't show them to end users
+ Map error codes to your own end-user messages. Each platform's error code page has a "Suggested user message" column you can start from

### The language parameter

Each conferencing SDK provides a `language` setting (the name follows each platform's API reference, for example the `language` init parameter on Web), and **it also applies to the underlying SRTC**:

+ The value is a language tag such as `zh-CN` or `en`. If you don't set it, it follows the system language, falling back to Chinese if that isn't available
+ The SDK sends `Accept-Language` with its requests to both the meeting server and the SRTC server, and **the messages of server business errors (1000–99999) come back in Chinese or English accordingly**
+ **The SDK's own errors (`20Nxxx`, and passed-through `10Nxxx`) are always in English and aren't affected by `language`**

---

## Unified table (meeting-layer low 3 digits)

**Each meaning has exactly one code**, and every platform uses the same code for the same situation. Not every platform produces every code; see each platform's error code page for the codes it actually produces.

| Low code | Name | Meaning |
| :---: | --- | --- |
| 000 | Unknown | Unclassified error (fallback; shouldn't normally appear) |
| 001 | NotLoggedIn | Not logged in / SDK not initialized |
| 002 | TokenExpired | The token has expired |
| 003 | NotInMeeting | Not in a meeting / session not active |
| 004 | Unauthorized | No permission: a non-host performed a host operation, or the room has disabled turning on the camera / microphone / screen sharing |
| 005 | TokenInvalid | The token is malformed and can't be parsed |
| 006 | AlreadyInMeeting | Already in a meeting; exit it first |
| 007 | NetworkError | Network error: the request failed or HTTP wasn't 200 (the HTTP status is in the error details) |
| 008 | DeviceError | Device error (newer versions pass through the SRTC-layer code for device errors; this code is kept only for compatibility) |
| 009 | InternalError | SDK internal error |
| 010 | UserNotFound | No such member in the meeting |
| 011 | InvalidState | Not allowed in the current state: already on / not on yet, SDK not ready, instance destroyed |
| 012 | InvalidArgument | Invalid argument |
| 013 | HostNotSet | Host error or no host set |
| 103 | EnterMeetingCancelled | Entering the meeting was canceled |
| 104 | WaitingRoomContextMissing | Waiting room context missing |
| 105 | AudienceOperationForbidden | The operation isn't allowed for audience members |
| 106 | SessionOperationCancelled | The session operation was canceled |
| 201 | CameraOpenFailed | Failed to turn on the camera (meeting-layer orchestration failed; underlying capture errors pass through the SRTC code) |
| 202 | MicOpenFailed | Failed to turn on the microphone (same as above) |
| 203 | ScreenPermissionDenied | Screen sharing permission denied |
| 204 | ScreenTrackUnavailable | Screen sharing track unavailable |
| 205 | WhiteboardRequestCancelled | Whiteboard request canceled |
| 206 | WhiteboardUrlMissing | Whiteboard URL missing |
| 207 | CloudRecordCaptureDisabled | Capture is disabled for cloud recording |
| 208 | LocalTrackUnavailable | Local track unavailable |
| 209 | RemoteTrackUnavailable | Remote track unavailable (the member is in the meeting but doesn't have that track) |
| 210 | LocalDeviceOperationCancelled | Local device operation canceled |
| 211 | LocalDeviceCapabilityUnsupported | Local device capability not supported |
| 212 | LocalDeviceOperationInProgress | A local device operation is in progress |
| 301 | ImEnableCancelled | Enabling IM was canceled |
| 302 | ImTokenMissing | IM token missing |
| 351 | HttpClientNotInitialized | HTTP client not initialized |
| 353 | RequestTimeout | Request timed out |
| 354 | RequestCancelled | Request canceled |
| 355 | EmptyResponseBody | Empty response body |
| 356 | ResponseParseFailed | Failed to parse the response: not JSON or missing the `code` field |

---

## Which platforms have shipped the new codes

This table is version 2, finalized on 2026-09-30. **Each platform follows the version in which it ships the new codes.** Platforms that haven't shipped yet still use the codes listed on their own error code pages.

| Platform | Prefix | Uses this table since |
| --- | --- | --- |
| Web | `206` | `@seastart/smeeting-web-sdk` 0.3.0 |
| WeChat Mini Program | `207` | `@seastart/smeeting-wx-sdk` 0.1.0 |
| Swift (iOS / macOS) | `203` / `205` | SMeeting Swift SDK 1.4.0 and later ([changelog](/en/meeting/swift/changelog)) |
| Android, iOS (Objective-C), HarmonyOS, Windows | `202`, `203`, `208`, `201` | **Not shipped yet**; follows each platform's release. Until then, use that platform's error code page |

---

## Old code → new code mapping

| Platform | Main changes | Detailed mapping |
| --- | --- | --- |
| Web / WeChat Mini Program | Apart from `206001`–`206004` (`207001`–`207004`), errors used to fall into the fallback code `206000` / `207000`; they now have their own codes by scenario. Network / HTTP failures when calling the meeting server are now `206007` / `207007`, and unparsable responses are `206356` / `207356`; capture and permission failures pass through SRTC-layer codes such as `106231`. `001`–`004` are unchanged | [Web changelog](/en/meeting/web/changelog) · [Web error codes](/en/meeting/web/error-codes) |
| Swift | See the mapping table in its changelog | [Swift changelog](/en/meeting/swift/changelog) |

Mappings for the other platforms (Android, iOS Objective-C, HarmonyOS, Windows) will be given in each platform's changelog when it ships the new codes. For old SRTC-layer codes that are passed through (such as the `100xxx` common codes), see the [SRTC old-to-new mapping](/en/rtc/error-codes).

---

## Full error code tables by platform

[Web](/en/meeting/web/error-codes) · [Android](/en/meeting/android/error-codes) · [Windows](/en/meeting/windows/error-codes) · [Swift](/en/meeting/swift/error-codes) · [iOS](/en/meeting/ios/error-codes) · [HarmonyOS](/zh/meeting/harmony/error-codes) (Chinese)
