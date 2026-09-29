---
title: "Error code format"
description: "How SMeeting error codes are numbered (prefix plus a 3-digit code), how to tell server, cross-platform SDK, and platform-specific errors apart, and why SRTC 1xxxxx codes show up alongside SMeeting 2xxxxx codes. Read this when troubleshooting an error code."
---

`0` means success; anything other than 0 is an error.

Every error code is structured as **prefix + a 3-digit specific code (001–999)**. Once you can read the prefix, you can tell right away **which layer** and **which platform** the error comes from.

---

## How to read an error code

```text
  2 0 3 0 0 1
  │ │ │ └─┴─┴── Specific code 001-999
  │ │ └──────── Platform type: 3 = iOS
  └─┴────────── Product layer: 2 = SMeeting
```

There are three cases:

| Digits | Source | Prefix | Example |
| --- | --- | --- | --- |
| 4 digits | Returned by the **server** | `2` | `2xxx` business errors from the meeting service |
| 6 digits, third digit is `0` | Client SDK, **common to all platforms** | `200` | `200xxx` |
| 6 digits | Client SDK, **platform-specific** | `20` + platform type | `203001` iOS error |

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
| 8 | Android set-top box | `208` |
| 9 | Android embedded | `209` |

<Note>
The Swift SDK supports both iOS and macOS and automatically uses the `203` or `205` prefix depending on the platform it runs on.
</Note>

---

## Why you see error codes starting with 1xxxxx

**This is expected, not a bug.**

SMeeting is built on SRTC. When an error occurs in the underlying audio and video layer, SMeeting passes SRTC's original error code through to you **as-is** instead of wrapping it in its own code—so you can pinpoint which layer the problem is in.

| What you see | Meaning | Where to look |
| --- | --- | --- |
| `2xxx` | The meeting server rejected the request (no permission, meeting doesn't exist, etc.) | [Server API error codes](/en/meeting/server-api/error-codes) |
| `20Nxxx` | An error from the meeting-layer SDK | The error code page for that platform |
| `1xxx` | An error from the underlying SRTC **server** | [SRTC error code format](/en/rtc/error-codes) |
| `10Nxxx` | An error from the underlying SRTC **client** (for example, "not in a channel") | [SRTC error code format](/en/rtc/error-codes) |

So seeing both `203002` and `103002` in the iOS conferencing SDK is not a contradiction: the former is error 002 of the meeting layer, and the latter is error 002 of the SRTC layer; the two are unrelated.

<Tip>
When troubleshooting, look at the first two digits first: if it starts with `2`, look for meeting-layer causes (permissions, meeting state, member roles); if it starts with `1`, look for audio and video layer causes (token, channel, network).
</Tip>

---

## Full error code tables by platform

[Web](/en/meeting/web/types) · [Android](/en/meeting/android/error-codes) · [Windows](/zh/meeting/windows/error-codes) (Chinese) · [Swift](/en/meeting/swift/error-codes) · [iOS](/zh/meeting/ios/error-codes) (Chinese)

<Warning>
Don't branch on the error **message text**—the text may change between versions, but error codes don't.
</Warning>
