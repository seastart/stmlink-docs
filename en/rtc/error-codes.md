---
title: "Error code format"
description: "How SRTC error codes are numbered across all platforms: how to tell from a code whether it came from the server or a client SDK and which platform, the platform type table, and where to look next. Read when you get an unfamiliar error code."
---

`0` means success; anything non-zero is an error.

Every error code has the structure **prefix + 3-digit specific code (001–999)**. Once you can read the prefix, you can immediately tell whether the error was **returned by the server** or **produced by a client SDK**, and **which platform** it came from—so you know where to start troubleshooting.

---

## How to read an error code

```text
  1 0 6 0 0 1
  │ │ │ └─┴─┴── Specific code 001-999
  │ │ └──────── Platform type: 6 = Web
  └─┴────────── Product layer: 1 = SRTC
```

There are three cases:

| Digits | Source | Prefix | Example |
| --- | --- | --- | --- |
| 4 digits | Returned by the **server** | `1` | `1021` Token already used |
| 6 digits, 3rd digit is `0` | Client SDK, **common to all platforms** | `100` | `100008` Token invalid |
| 6 digits | Client SDK, **platform-specific** | `10` + platform type | `106001` Web: not currently in a channel |

---

## Platform types

The 3rd digit of a 6-digit error code indicates the platform:

| Type | Platform | SRTC prefix |
| :---: | --- | --- |
| 1 | Windows | `101` |
| 2 | Android phone | `102` |
| 3 | iOS phone | `103` |
| 4 | Linux C/C++ | `104` |
| 5 | macOS | `105` |
| 6 | Web (WebRTC) | `106` |
| 7 | Mini Program | `107` |
| 8 | Android set-top box | `108` |
| 9 | Android embedded | `109` |
| 80 | Server / embedded integration (C SDK) | `180` |

So `103002` reads as: SRTC layer + iOS + error number 002.

---

## Using it when troubleshooting

| Prefix | Meaning | Where to look first |
| --- | --- | --- |
| `1xxx` | The server rejected the request | Check the signature, token, and channel state. See [Server API error codes](/en/rtc/server-api/error-codes) |
| `100xxx` | Common SDK error, the same on every platform | Usually parameters, initialization order, or network issues |
| `10Nxxx` | Error specific to that platform | See that platform's error code page |
| `180xxx` | Errors from the C SDK itself (server / embedded integration) | See [C SDK error codes](/zh/rtc/capi/error-codes) (Chinese) |

Full error code tables for each platform:
[Web](/en/rtc/web/error-codes) · [Android](/en/rtc/android/error-codes) · [Windows](/zh/rtc/windows/error-codes) (Chinese) · [Swift](/en/rtc/swift/error-codes) · [iOS](/zh/rtc/ios/error-codes) (Chinese) · [C](/zh/rtc/capi/error-codes) (Chinese)

<Note>
**Read the C SDK at two levels.** Its **API return values** are simple status values such as `0 / -1 / -2 / -3 / -4`; they only express the result of the call and carry no reason. The actual reason is written to the log, which contains both the SDK's own `180xxx` codes and `1xxx` codes passed through from the server. See [C SDK error codes](/zh/rtc/capi/error-codes) (Chinese).
</Note>

<Warning>
Don't branch on error **messages**—messages change between versions; error codes don't.
</Warning>

---

## Difference from SMeeting

Same rules, only a different product layer number: SRTC uses `1`, SMeeting uses `2`.

If you use SMeeting, you see both kinds of error codes: `2xxxxx` come from the meeting layer, and `1xxxxx` come from the underlying SRTC (passed through unchanged by the meeting layer to help you locate the problem). See [SMeeting error code format](/en/meeting/error-codes).
