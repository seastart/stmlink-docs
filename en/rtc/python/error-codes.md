---
title: "Error codes"
description: "The Python SDK's SdkError: the three kinds of code values (the SDK's own 180xxx, server 1xxx passed through unchanged, and -1 internal errors) and base_code / ErrorCode, causes and troubleshooting for common errors, how to handle join failures, and setting the language of server error messages with set_language."
---

When an API fails it raises `srtc.SdkError`, which has the following fields:

| Field | Type | Description |
| --- | --- | --- |
| `code` | `int` | Error code |
| `msg` | `str` | Error reason. In English for SDK errors; for the language of server errors, see [Language](#language) below |
| `base_code` | `int` | Since 0.2.0. The last three digits of an SDK error code (shared across SDKs), for comparing with `srtc.ErrorCode`; server error codes return themselves |

```python
try:
    ch = await srtc.Channel.join(token)
except srtc.SdkError as e:
    print(e.code, e.msg)
    if e.base_code == srtc.ErrorCode.TOKEN_INVALID:
        ...  # Invalid token; check how it was issued
```

Branch on `code` / `base_code` to tell errors apart, not on the `msg` text.

`code` falls into three kinds:

| Value | Source | Description |
| --- | --- | --- |
| `180xxx` | The SDK itself | The same set as [C SDK · Error codes](/en/rtc/capi/error-codes#180xxx-in-logs-sdk-errors); server-side integrations share the `180` prefix, and the last three digits are the same across all SDKs (see [Error code format](/en/rtc/error-codes) for the numbering rules) |
| `≥1000` (such as `1033`) | Server | The business-level reason for rejection, passed through unchanged by the SDK. For the full list, see [Server API · Error codes](/en/rtc/server-api/error-codes) |
| `-1` | SDK internal | Internal error with no specific error code; should not occur normally. Check `msg` |

<Warning>
Error codes were renumbered in 0.2.0 (for example, invalid argument changed from `180900` to `180031`, and "not allowed to publish a composite stream" changed from `180004` to `180040`). The table below applies to 0.2.0 and later. For the old-to-new mapping, see [Changelog · 0.2.0](/en/rtc/python/changelog).
</Warning>

---

## Common errors

| Code | `ErrorCode` | Meaning | Common causes and fixes |
| --- | --- | --- | --- |
| `180001` | `NOT_IN_CHANNEL` | Not in a channel | An in-channel API was called after the channel disconnected (`ch.closed` is `True`) |
| `180002` | `TOKEN_EXPIRED` | Token expired | The token wasn't used before it timed out. **Issue a new one for every `join`** |
| `180003` | `TRACK_NOT_FOUND` | Track doesn't exist | The subscribed uid / track_id is wrong, or the other side has unpublished |
| `180004` | `TOKEN_INVALID` | Invalid token | The token failed to parse or is incomplete; check that it was passed in full and was issued for this environment |
| `180006` | `CONNECTION_FAILED` | Connection failed | Network request failed or HTTP status other than 200; check the network and the service address |
| `180007` | `CONNECTION_TIMEOUT` | Connection timed out | `join` did not complete within `timeout` |
| `180014` | `TRANSPORT_NOT_READY` | Transport not ready | The channel is reconnecting; **just retry later** |
| `180025` | `INTERNAL_ERROR` | Internal SDK error | For example, failure to create a local audio track. Contact us with the logs |
| `180031` | `INVALID_ARGUMENT` | Invalid argument | An argument has a wrong value, such as a channel count other than 1 or 2, or a mismatched track kind |
| `180040` | `NOT_MCU_PUBLISHER` | Not allowed to publish a composite stream | Publishing a composite stream requires connecting with the `__mcu__` identity |
| `180300` / `180301` | `PUBLISH_FAILED` / `SUBSCRIBE_FAILED` | Publish / subscribe failed | Media negotiation failed; check the network |
| `180302` / `180303` | `PUBLISH_TIMEOUT` / `SUBSCRIBE_TIMEOUT` | Publish / subscribe negotiation timed out | The server's media ports are unreachable; check the firewall |
| `1021` | —— | Token already used | The same token was used twice |
| `1032` | —— | Session is not online | A token from a session that already left the channel was reused |
| `1033` | —— | Concurrency limit reached | The app's concurrency license quota is used up; expand the license or wait for other sessions to end |
| `1034` / `1035` | —— | No available node / node fully loaded | The server's media nodes are busy. The SDK backs off and retries automatically when **reconnecting**; if the **initial join** fails, you need to retry later |

For all values of `srtc.ErrorCode` and what each code means, see [C SDK · Error codes](/en/rtc/capi/error-codes#180xxx-in-logs-sdk-errors) (the value of `ErrorCode` is the last three digits of the error code).

<Tip>
When a join fails, handle it by error code: `1021` / `1032` / `180002` / `180004` are token problems—**issue a new token** before retrying; `1034` / `1035` / `180006` are temporary—retry later with a new token; `1033` is a license quota problem, and retrying doesn't help.
</Tip>

---

## Language

The `msg` of server errors (`code` ≥1000) is generated by the server, and its language can be set (since 0.2.0):

```python
import srtc

srtc.set_language("en")      # such as "en" or "zh-CN"; pass None or an empty string to follow the system language again
```

+ Applies process-wide and can be called at any time, including before creating a `Channel`
+ When it isn't called, the system language is used: the first non-empty value among the environment variables `LC_ALL`, `LC_MESSAGES`, and `LANG`; when it is `C` / `POSIX` or none of them is set, the server replies in Chinese
+ Only affects the text of server errors; SDK errors (`180xxx`) are always in English

---

## Logging

The SDK uses Python's standard `logging`, with the logger name `srtc`:

```python
import logging

logging.basicConfig(level=logging.INFO)
logging.getLogger("srtc").setLevel(logging.DEBUG)     # Turn on when troubleshooting
```

Logs from the native core (signaling, media connections) go directly to the process's stdout / stderr, not through `logging`.
