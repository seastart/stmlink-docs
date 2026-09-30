---
title: "Error codes"
description: "C SDK return values (RTC_OK, RTC_ERROR, RTC_INVALID_PARAM, RTC_NOT_CONNECTED, RTC_TIMEOUT) and their causes, the SDK's own 180xxx codes and server 1xxx codes you get from rtc_get_last_error or the logs, and how to check return values and clean up on failure."
---

The C interface reports results through return values. Functions that return `int` all use the five values below: `RTC_OK` is `0`, and every failure is negative.

```c
#define RTC_OK              0   // Success
#define RTC_ERROR          -1   // General error
#define RTC_INVALID_PARAM  -2   // Invalid parameter
#define RTC_NOT_CONNECTED  -3   // Not connected
#define RTC_TIMEOUT        -4   // Timeout
```

---

## Values

| Constant | Value | Meaning | Common causes and what to check |
| --- | --- | --- | --- |
| `RTC_OK` | `0` | Success | — |
| `RTC_ERROR` | `-1` | General error | Rejected by the server, underlying negotiation failed, token session no longer valid, identity doesn't meet the requirement (such as publishing a composite stream without the `__mcu__` identity). **Turn on DEBUG logs to see the specific reason** |
| `RTC_INVALID_PARAM` | `-2` | Invalid parameter | Instance/track handle invalid or already destroyed, `NULL` passed for a required pointer, empty token string, keyframe requested for a non-video track |
| `RTC_NOT_CONNECTED` | `-3` | Not connected | A function that needs a connection was called before successfully joining the channel; for `rtc_get_connection_quality` it also means "no quality report received yet" |
| `RTC_TIMEOUT` | `-4` | Timeout | Returned only by `rtc_join_channel_sync`. Token expired, no network connectivity, server unreachable |

<Note>
`RTC_ERROR` is a catch-all failure code. Get the specific reason with [`rtc_get_last_error`](/en/rtc/capi/api-reference/engine#rtc_get_last_error) (since 0.0.9); it returns the `180xxx` / `1xxx` error codes described in the next two sections. You can also raise the log level to see the reason:

```c
rtc_set_log_level(RTC_LOG_DEBUG);
```

The logs then print a more specific error, such as `180001: Not in channel` or `1021: ...`. The difference between these two kinds of codes is explained in the next two sections.
</Note>

---

## `180xxx` in logs: SDK errors

The five C return values only describe the result "at the call level" and carry no reason. Get the reason with `rtc_get_last_error`; it is also printed in the logs. **6-digit codes starting with `180` are errors produced by the SDK itself**: `180` is the prefix for server-side / embedded integrations, and the last three digits identify the specific error and **are the same across all SDKs** (see [Error code format](/en/rtc/error-codes) for the numbering rules). Reasons for SDK errors are in English; branch on the error code, not on the message text.

<Warning>
Error codes were renumbered in 0.1.0 (for example, "not allowed to publish a composite stream" changed from `180004` to `180040`, and `180004` now means invalid token). The table below applies to 0.1.0 and later. For the old-to-new mapping, see [Changelog · 0.1.0](/en/rtc/capi/changelog).
</Warning>

| Code | Meaning | Common causes |
| --- | --- | --- |
| `180000` | Unclassified error | Fallback code that should not occur normally; check the reason text and the surrounding logs |
| `180001` | Not in a channel | An in-channel function was called before joining the channel (or after leaving); `RTC_NOT_CONNECTED` maps to this code |
| `180002` | Token expired | The token wasn't used before it timed out, or it was already used by another session |
| `180003` | Track doesn't exist | The target uid / trackId / desc is wrong, or the other side hasn't published that track yet |
| `180004` | Invalid token | The token failed to parse or is incomplete; check that it was copied in full and was issued for this environment |
| `180006` | Connection failed | Network request failed or HTTP status other than 200; check the network and the service address. The SDK retries automatically while reconnecting |
| `180007` | Connection timed out | `rtc_join_channel_sync` did not complete within `timeout_ms` |
| `180009` / `180010` | Signaling connection failed / signaling subscription failed | The signaling service is unreachable; check the network and firewall |
| `180011` | Failed to parse the response | The server's response can't be parsed, usually because the service address points to the wrong service or a proxy in between rewrites the response |
| `180012` | Underlying WebRTC error | For example, failure to create a data channel |
| `180013` | SDP negotiation failed | Media negotiation failed |
| `180014` | Transport not ready | The channel is reconnecting or the media streaming engine isn't connected; **just retry later** |
| `180015` | Media connection failed | The media connection failed to be created or was disconnected; check that the UDP ports are open |
| `180019` | Codec not supported | An unsupported codec was passed to `rtc_create_local_track` |
| `180020` | Publish limit exceeded | The number of published audio / video tracks has reached the limit |
| `180023` | Media streaming engine closed | The channel was left or the connection dropped while waiting |
| `180024` | Operation not allowed in the current state | Calls made out of order, such as the track not being ready or the engine not initialized |
| `180025` | Internal SDK error | For example, failure to create a track or out of memory. Contact us with the logs |
| `180026` | Operation cancelled | The channel was left or the instance was destroyed during the call |
| `180031` | Invalid argument | A required argument is empty, a video track has no width/height/frame rate, the track kind doesn't match, etc.; `RTC_INVALID_PARAM` maps to this code |
| `180032` | Capability not supported by the current engine | For example, the current media streaming engine doesn't support layer switching |
| `180034` | Subscription limit exceeded | The number of subscribed audio / video tracks has reached the limit |
| `180035` | Publish desc conflict | The stream slot is already taken by another track; use a different `desc` or unpublish first |
| `180040` | Not allowed to publish a composite stream | Publishing an MCU composite stream requires connecting with the `__mcu__` / `__amcu__` identity; regular identities are rejected |
| `180204` | User is not in the channel | The target uid is not in the channel |
| `180300` | Publish failed | Media negotiation failed, or the media streaming engine is disconnected; check the network and encoding parameters |
| `180301` | Subscribe failed | Media negotiation failed, or the target track has been unpublished |
| `180302` | Publish negotiation timed out | No network connectivity or server unreachable |
| `180303` | Subscribe negotiation timed out | Same as above |
| `180304` | Track doesn't exist when subscribing | The other side hasn't finished publishing yet. **The SDK backs off and retries automatically**, so occasional occurrences in the logs are normal; investigate only if it keeps appearing |

<Tip>
When you see `180002` (token expired), first make sure the token isn't being reused: every process needs its own issued token. This and the server's `1032` below are two symptoms of the same kind of problem.
</Tip>

---

## `1xxx` and similar in logs: server business error codes

**Four-digit codes (≥1000) come from the server.** They are business-level reasons for rejection, passed through unchanged by the SDK, for example:

| Server code | Description | How it shows up on the C side |
| --- | --- | --- |
| `1021` | Channel token already used | `rtc_join_channel_sync` returns `RTC_ERROR` |
| `1032` | Session is not online | `rtc_join_channel_sync` returns `RTC_ERROR` |

For the full list, see [Server API · Error codes](/en/rtc/server-api/error-codes). When a publish / subscribe is rejected by the server (such as `1033` concurrency limit reached or `1035` node overloaded), `rtc_get_last_error` returns the server code as-is since 0.1.0 instead of wrapping it as `180300` / `180301`.

The language of server error reasons is set by [`rtc_set_language`](/en/rtc/capi/api-reference/engine#rtc_set_language); by default it follows the system language.

<Warning>
A token is bound to one session, and the session is no longer valid once the process leaves the channel. Reusing the same token to start a second process gets `1032` (`RTC_ERROR` on the C side)—issue a separate token for every process.
</Warning>

---

## Checking return values

Check the return value of every function that returns `int`. When a critical path such as joining the channel fails, you must run the cleanup flow to avoid leaking handles:

```c
void* rtc = rtc_create();

int ret = rtc_join_channel_sync(rtc, token, 10000);
if (ret != RTC_OK) {
    char msg[256];
    int code = rtc_get_last_error(rtc, msg, sizeof(msg));   // Specific reason, e.g. 1033 concurrency limit reached
    fprintf(stderr, "join failed: %d, code=%d %s\n", ret, code, msg);
    rtc_destroy(rtc);        // Destroy the instance even on failure
    return -1;
}
```

`rtc_create` / `rtc_create_local_track` return pointers, which are `NULL` on failure; just check for `NULL`.
