---
title: "Error code format and unified table"
description: "How SRTC error codes are numbered and the cross-platform unified table: tell from a code whether it came from the server or which platform's SDK, with the low 3 digits meaning the same on every platform. Covers the language parameter, which platforms have shipped the new codes, and old-to-new mappings. Read when you get an unfamiliar error code or upgrade an SDK."
---

`0` means success; anything non-zero is an error.

There are two kinds of error codes: **4–5 digit codes are business error codes returned by the server**, and **6-digit codes are produced by the client SDK itself**. A 6-digit code is **platform prefix + 3-digit low code**. The low 3 digits are assigned from the unified table on this page, and **the same low code means the same thing on every platform**.

---

## How to read an error code

```text
  1 0 6 2 3 1
  │ │ │ └─┴─┴── Low code 000-999: 231 = camera permission denied (same on every platform)
  │ │ └──────── Platform type: 6 = Web
  └─┴────────── Product layer: 10 = SRTC
```

| Digits | Source | Structure | Example |
| --- | --- | --- | --- |
| 4–5 digits (1000–99999) | Returned by the **server**, passed through unchanged by the SDK | Server error code | `1021` Token already used |
| 6 digits | Produced by the client **SDK** | `10` + platform type + low 3 digits | `106231` Web: camera permission denied |

So `102231` and `106231` read as the same error (camera permission denied), coming from Android and Web respectively.

---

## Platform types

| Type | Platform | SRTC prefix |
| :---: | --- | --- |
| 1 | Windows | `101` |
| 2 | Android phone | `102` |
| 3 | iOS phone | `103` |
| 4 | Linux C/C++ | `104` |
| 5 | macOS | `105` |
| 6 | Web (WebRTC) | `106` |
| 7 | Mini Program | `107` |
| 8 | HarmonyOS NEXT | `108` |
| 9 | Android embedded | `109` |
| 80 | Server / embedded integration (Go / Python / C SDK) | `180` |

<Note>
The Swift SDK supports both iOS and macOS and uses the `103` or `105` prefix depending on the platform it runs on.
</Note>

---

## Branch on codes, not messages

+ **Decide the error type by its code only.** The SDK's own error messages are always in English, are meant for developers and logs, and change between versions. Don't branch on them, and don't show them to end users
+ Map error codes to your own end-user messages. Each platform's error code page has a "Suggested user message" column you can start from
+ To compare the same kind of error across platforms, you can compare only the low 3 digits (each SDK exposes a field such as `baseCode`; see that platform's error code page)

### The language parameter

Each SDK provides a `language` setting (the name follows each platform's API reference, for example the `language` init parameter on Web and `rtc_set_language` in the C SDK):

+ The value is a language tag such as `zh-CN` or `en`. If you don't set it, it follows the system language, falling back to Chinese if that isn't available
+ The SDK sends `Accept-Language` with its server requests, and **the messages of server business errors (1000–99999) come back in Chinese or English accordingly**
+ **The SDK's own errors (6-digit codes) are always in English and aren't affected by `language`**

So seeing both Chinese and English error messages in the same app is expected: the former come from the server, the latter from the SDK.

---

## Unified table (low 3 digits)

Ranges: `000–099` general meanings; `200–299` channel / device specifics; `300–349` media streaming.

**Each meaning has exactly one code**, and every platform uses the same code for the same situation. Not every platform produces every code; see each platform's error code page for the codes it actually produces.

| Low code | Name | Meaning |
| :---: | --- | --- |
| 000 | Unknown | Unclassified error (fallback; shouldn't normally appear) |
| 001 | NotInChannel | Not in the channel: not joined, already left, or the channel hasn't started |
| 002 | TokenExpired | The token has expired |
| 003 | TrackNotFound | The track doesn't exist |
| 004 | TokenInvalid | The token is invalid: it can't be parsed or is incomplete |
| 005 | AlreadyJoined | Already joined / conflicting duplicate operation |
| 006 | ConnectionFailed | Connection failed: the network request failed or HTTP wasn't 200 (the HTTP status is in the error details) |
| 007 | ConnectionTimeout | Connection / request timed out |
| 008 | SignatureError | Signature error |
| 009 | SignalingConnectFailed | Failed to connect to signaling |
| 010 | SignalingSubscribeFailed | Failed to subscribe to signaling |
| 011 | MessageDecodeFailed | Failed to parse a signaling message / server response (not JSON, missing the `code` field, or invalid fields) |
| 012 | WebrtcError | Underlying WebRTC / media network error |
| 013 | SdpNegotiationFailed | SDP negotiation failed |
| 014 | TransportNotReady | Transport not ready / reconnecting; retry later |
| 015 | PeerConnectionFailed | The media connection (PeerConnection) failed to be created or was disconnected |
| 016 | TrackAlreadyPublished | The same track was published twice |
| 017 | TrackNotPublished | The track isn't published |
| 018 | CaptureFailed | Capture failed: device in use, failed to open, or hardware error |
| 019 | CodecNotSupported | Codec not supported |
| 020 | MaxPublishLimitReached | Publish limit exceeded |
| 021 | DeviceNotFound | The device doesn't exist, or the specified device was unplugged |
| 022 | EngineNotSupported | Media streaming engine not supported |
| 023 | EngineDisconnected | The engine is disconnected or closed (still waiting or calling after leaving the channel or destroying the instance) |
| 024 | InvalidState | The operation isn't allowed in the current state: wrong call order, not initialized, or must be set before joining a channel |
| 025 | InternalError | SDK internal error |
| 026 | Cancelled | The operation was canceled |
| 027 | VirtualBackgroundAlreadyInstalled | Virtual background is already installed |
| 028 | VirtualBackgroundNotInstalled | Virtual background isn't installed |
| 029 | VirtualBackgroundModelNotFound | The virtual background model doesn't exist or is invalid |
| 030 | VirtualBackgroundSessionFailed | Virtual background processing failed |
| 031 | InvalidArgument | Invalid argument |
| 032 | FeatureNotSupported | The capability isn't supported in the current environment / OS version / mode |
| 033 | TrackNotCaptured | The track was published / played before capture started (or after it stopped) |
| 034 | MaxSubscribeLimitReached | Subscribe limit exceeded |
| 035 | PublishDescConflict | The publish description (desc / stream slot) is already used by another track |
| 036 | PlayFailed | Playback failed (not caused by the autoplay policy) |
| 037 | PlayViewNotFound | The playback container doesn't exist |
| 038 | PopupBlocked | The popup was blocked by the browser |
| 039 | ScreenShareDenied | Screen sharing was denied: the user canceled, or the system didn't allow screen recording |
| 040 | NotMcuPublisher | Not allowed to publish composite streams (must connect as the MCU) |
| 041 | OperationTooFrequent | Operation too frequent |
| 042 | PermissionDenied | Device permission denied (when camera and microphone can't be told apart; otherwise 231 / 251) |
| 043 | Forbidden | The current identity / role isn't allowed to do this |
| 044 | AudioRouteSwitchFailed | Failed to switch the audio route |
| 204 | UserNotFound | No such user in the channel |
| 209 | ChannelJoinNativeException | Native-layer exception while joining the channel (Android only) |
| 212 | ChannelResourceCreateFailed | Failed to create local resources while joining the channel (Android only) |
| 213 | ChannelJoinDisconnected | The connection dropped while joining the channel (Android only) |
| 231 | CameraPermissionDenied | Camera permission denied |
| 233 | CameraSessionFailed | Failed to create the camera session |
| 234 | CameraRequestFailed | Camera capture request failed |
| 235 | CameraDisconnected | The camera was disconnected by the system |
| 239 | CameraFirstFrameTimeout | Timed out waiting for the camera's first frame |
| 242 | CameraFormatUnavailable | Camera format unavailable |
| 243 | CameraOpenTimeout | Timed out opening the camera |
| 244 | CameraSessionTimeout | Camera session timed out |
| 251 | MicPermissionDenied | Microphone permission denied |
| 255 | MicFormatUnsupported | Microphone format not supported |
| 270 | ScreenCaptureRequestRejected | The screen sharing request wasn't accepted: the authorization UI was destroyed or the request was duplicated (Android only) |
| 300 | PublishFailed | Publish failed (including when the media streaming engine isn't connected / is disconnected) |
| 301 | SubscribeFailed | Subscribe failed / subscription rejected |
| 302 | PublishTimeout | Publish negotiation timed out |
| 303 | SubscribeTimeout | Subscribe negotiation timed out |
| 304 | SubscribeTrackNotFound | The track doesn't exist yet when subscribing; the SDK retries automatically (Go / Python / C SDK) |
| 312 | OperationIgnored | The operation was ignored; not a failure (Android only) |

Codes that are easy to confuse, resolved by "the most specific cause wins":

+ The media connection failed to be created, or entered failed / closed → **015**, whether during publish, subscribe, or joining the channel
+ Reconnecting, retry later → **014**; the engine was closed or destroyed → **023**
+ Publishing / subscribing while the media streaming engine isn't connected (and isn't reconnecting), or being rejected / failing negotiation with no more specific code → **300 / 301**
+ Not supported in the current environment → **032**, not 018 (capture failed)

---

## Which platforms have shipped the new codes

This table is version 2, finalized on 2026-09-30. **Each platform follows the version in which it ships the new codes.** Platforms that haven't shipped yet still use the codes listed on their own error code pages.

| Platform | Prefix | Uses this table since |
| --- | --- | --- |
| Web | `106` | `@seastart/srtc-web-sdk` 0.7.0 |
| WeChat Mini Program | `107` | `@seastart/srtc-wx-sdk` 0.3.0 |
| C SDK / Python SDK | `180` | C SDK 0.1.0, Python SDK (`srtc`) 0.2.0 |
| Swift (iOS / macOS) | `103` / `105` | SRTC Swift SDK 1.5.0 and later ([changelog](/en/rtc/swift/changelog)) |
| Android, iOS (Objective-C), HarmonyOS, Windows | `102`, `103`, `108`, `101` | **Not shipped yet**; follows each platform's release. Until then, use that platform's error code page |

---

## Old code → new code mapping

### Old common codes `100001`–`100012`

The `100xxx` common codes that some platforms (iOS Objective-C, Windows, and others) exposed in older versions are retired and replaced with "platform prefix + low 3 digits". For example, the old `100008` (token invalid) becomes "platform prefix + `004`". **This takes effect once that platform ships the new codes.**

| Old code | Old name | New low code |
| :---: | --- | :---: |
| `100001` | SystemError | 025 |
| `100002` | NotInitialized | 024 |
| `100003` | MediaNotInitialized | 024 |
| `100004` | ProtocolParsingError | 011 |
| `100005` | Timeout | 007 |
| `100006` | InvalidArgs | 031 |
| `100007` | Conflict | 005 |
| `100008` | SdkTokenInvalid | 004 |
| `100009` | NetError | 006 |
| `100010` | MediaNetError | 012 |
| `100011` | NotFound | 204 (when looking up a user); other "not found" cases by meaning, such as 003 |
| `100012` | UserCancelled | 026 |

### Platforms that have shipped the new codes

| Platform | Main changes | Detailed mapping |
| --- | --- | --- |
| Web / WeChat Mini Program | Most errors used to fall into the fallback code `106000` / `107000`; they now have their own codes by scenario. HTTP failures changed from an `Error` with no code to `106006` / `107006`; capture and permission failures changed from the browser's raw exception to `106231` / `106251` / `106039` / `106021` / `106018`. `106001`–`106003` are unchanged | [Web changelog](/en/rtc/web/changelog) · [Web error codes](/en/rtc/web/error-codes) |
| C SDK / Python SDK | Failures that used to be `180000` or had no code now have specific codes; "not allowed to publish composite streams" moved from `180004` to `180040`, and `180004` now means token invalid | [C SDK changelog](/en/rtc/capi/changelog) · [Python SDK changelog](/en/rtc/python/changelog) |
| Swift | See the mapping table in its changelog | [Swift changelog](/en/rtc/swift/changelog) |

Mappings for the other platforms (Android, iOS Objective-C, HarmonyOS, Windows) will be given in each platform's changelog when it ships the new codes.

---

## Using it when troubleshooting

| Code | Meaning | Where to look first |
| --- | --- | --- |
| `1xxx` and similar (1000–99999) | The server rejected the request | Check the signature, token, and channel state. See [Server API error codes](/en/rtc/server-api/error-codes) |
| `10Nxxx` | An error from that platform's SDK itself; see the unified table above for the low 3 digits | See that platform's error code page |
| `180xxx` | Errors from the Go / Python / C SDK itself (server / embedded integration) | See [C SDK error codes](/en/rtc/capi/error-codes) and [Python SDK error codes](/en/rtc/python/error-codes) |

Full error code tables for each platform:
[Web](/en/rtc/web/error-codes) · [Android](/en/rtc/android/error-codes) · [Windows](/en/rtc/windows/error-codes) · [Swift](/en/rtc/swift/error-codes) · [iOS](/en/rtc/ios/error-codes) · [HarmonyOS](/zh/rtc/harmony/error-codes) (Chinese) · [C](/en/rtc/capi/error-codes) · [Python](/en/rtc/python/error-codes)

<Note>
**Read the C SDK at two levels.** Its **API return values** are simple status values such as `0 / -1 / -2 / -3 / -4`; they only express the result of the call and carry no reason. Get the actual reason with `rtc_get_last_error`; it's also written to the log, which contains both the SDK's own `180xxx` codes and `1xxx` codes passed through from the server. See [C SDK error codes](/en/rtc/capi/error-codes).
</Note>

---

## Difference from SMeeting

Same rules, only a different product layer number: SRTC uses `10`, SMeeting uses `20`, and the low 3 digits of the two layers are **two independent tables**.

If you use SMeeting, you see both kinds of error codes: `20Nxxx` come from the meeting layer, and `10Nxxx` come from the underlying SRTC (passed through unchanged by the meeting layer to help you locate the problem). See [SMeeting error code format and unified table](/en/meeting/error-codes).
