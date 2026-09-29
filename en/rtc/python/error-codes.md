---
title: "Error codes"
description: "The Python SDK's SdkError: the three kinds of code values (the SDK's own 180xxx, server 1xxx passed through unchanged, and -1 internal errors), causes and troubleshooting for common errors, and how to handle join failures."
---

When an API fails it raises `srtc.SdkError`, which has two fields:

| Field | Type | Description |
| --- | --- | --- |
| `code` | `int` | Error code |
| `msg` | `str` | Error reason |

```python
try:
    ch = await srtc.Channel.join(token)
except srtc.SdkError as e:
    print(e.code, e.msg)
```

`code` falls into three kinds:

| Value | Source | Description |
| --- | --- | --- |
| `180xxx` | The SDK itself | The same set as [C SDK · Error codes](/en/rtc/capi/error-codes#180xxx-in-logs-sdk-errors); server-side integrations share the `180` prefix |
| `≥1000` (such as `1033`) | Server | The business-level reason for rejection, passed through unchanged by the SDK. For the full list, see [Server API · Error codes](/en/rtc/server-api/error-codes) |
| `-1` | SDK internal | Failures with no specific error code (such as a malformed token or no network connectivity); check `msg` |

---

## Common errors

| Code | Meaning | Common causes and fixes |
| --- | --- | --- |
| `180001` | Not in a channel | An in-channel API was called after the channel disconnected (`ch.closed` is `True`) |
| `180002` | Token expired | The token wasn't used before it timed out. **Issue a new one for every `join`** |
| `180003` | Track doesn't exist | The subscribed uid / track_id is wrong, or the other side has unpublished |
| `180300` / `180301` | Publish / subscribe failed | Media negotiation failed; check the network |
| `180302` / `180303` | Publish / subscribe negotiation timed out | The server's media ports are unreachable; check the firewall |
| `1021` | Token already used | The same token was used twice |
| `1032` | Session is not online | A token from a session that already left the channel was reused |
| `1033` | Concurrency limit reached | The app's concurrency license quota is used up; expand the license or wait for other sessions to end |
| `1034` / `1035` | No available node / node fully loaded | The server's media nodes are busy. The SDK backs off and retries automatically when **reconnecting**; if the **initial join** fails, you need to retry later |

<Tip>
When a join fails, handle it by error code: `1021` / `1032` / `180002` are token problems—**issue a new token** before retrying; `1034` / `1035` are temporary—retry later with a new token; `1033` is a license quota problem, and retrying doesn't help.
</Tip>

---

## Logging

The SDK uses Python's standard `logging`, with the logger name `srtc`:

```python
import logging

logging.basicConfig(level=logging.INFO)
logging.getLogger("srtc").setLevel(logging.DEBUG)     # Turn on when troubleshooting
```

Logs from the native core (signaling, media connections) go directly to the process's stdout / stderr, not through `logging`.
