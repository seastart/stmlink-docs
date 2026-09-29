---
title: "Callback events guide"
description: "How SMeeting notifies your backend when meetings, members, or recordings change: request format, signature verification, response requirements, the fields of each event, and idempotency. Read this when setting up callbacks."
---

Callbacks let your backend learn about changes on the meeting side without polling. Register the URL with [Configure event notifications](/en/meeting/server-api/meet#configure-event-notifications).
Subscribing to any event is optional, and **events you don't subscribe to are not sent**.

## Request format

We send a POST request to the `cb_url` you registered. The event name appears in both the query parameters and the request body:

```text
POST {your cb_url}?event=user_enter
Content-Type: application/json; charset=utf-8
```

```json
{
  "app_id": "68b3ft51smhz0x5glscw9whm78bw57uu",
  "time": 1718250917,
  "event": "user_enter",
  "data": { "meeting_id": "sny038", "room_no": "803707296", "user_id": "1001" }
}
```

Events differ only in `data`; the three outer fields are always the same. `time` is the Unix timestamp (in seconds) when the event occurred.

## Verify the signature (required)

The signature in the callback request headers uses **exactly the same algorithm as calls to the server API** (see the [Overview](/en/meeting/server-api/overview)),
just in the opposite direction: this time we sign with your `app_key` and you verify. The request headers are `app_id` / `nonce` / `timestamp` / `signature`.

Without signature verification, anyone who knows your callback URL can forge events. **Don't skip this step.**

## Response requirements

+ The HTTP status code must be `200`
+ The response body must be standard JSON: `{"code": 0}`
+ Our request timeout is **10 seconds**. Your handler must return within that time (move heavy work to async processing)

A non-200 status, a non-JSON body, or a non-zero `code` counts as a failure.

## Events at a glance

| Event | When it fires |
| --- | --- |
| `user_enter` | A user enters the meeting |
| `user_exit` | A user exits the meeting |
| `meeting_status_change` | The meeting status changes (between not started, in progress, and ended)|
| `mcu_status_change` | The status of a recording, stream mixing, or live streaming task changes |
| `mcu_record_done` | A recording file is ready and you can get its playback URL (sent once per file when a recording produces several) |
| `mcu_alarm` | A recording task encounters an error |

### `user_enter` — User enters the meeting

```json
{
  "meeting_id": "sny038",
  "room_no": "803707296",
  "user_id": "1001",
  "real_name": "Alice",
  "nickname": "Alice",
  "role": 1
}
```

`role`: `0` regular member, `1` host, `2` co-host.

When the same `user_id` enters the meeting on multiple devices, the event fires once for each device.

### `user_exit` — User exits the meeting

Has two more fields than `user_enter`:

```json
{ "meeting_id": "sny038", "user_id": "1001", "reason": 1, "online": 3 }
```

+ `reason`: `1` exited voluntarily, `2` removed, `3` replaced by the same user entering again, `4` heartbeat timeout, `5` meeting destroyed, `6` switched to audience
+ `online` is the number of online members in the meeting **after** this user exits; `0` means everyone has exited

Checking `online == 0` to tell that "the meeting is actually empty" is more reliable than keeping your own count.

### `meeting_status_change` — Meeting status changes

```json
{ "meeting_id": "sny038", "room_no": "803707296", "from_status": 1, "to_status": 2 }
```

Status values: `1` not started, `2` in progress, `3` ended. `from_status` is included so you can tell
a "normal start" (1→2) apart from cases like "an abnormal restart".

### `mcu_status_change` — Recording task status changes

```json
{
  "meeting_id": "sny038",
  "task_id": "sxjgwy",
  "task_type": 1,
  "task_status": 1,
  "err_desc": "",
  "began_at": 1718250917,
  "ended_at": 0,
  "record_count": 0,
  "total_duration": 0,
  "total_size": 0
}
```

+ `task_type` is a bit mask; for the values, see the [Cloud recording and live streaming guide](/en/meeting/server-api/guides/recording)
+ `task_status`: `0` pending, `1` in progress, `2` ending, `3` ended abnormally, `4` ended normally
+ `err_desc` has content only when `task_status=3`
+ `record_count` / `total_duration` / `total_size` are the number of files, total duration (seconds), and total bytes produced by this recording

`0` and `2` are transitional states. Your backend usually only needs to care about `1` (started), `3` (failed), and `4` (ended).

**When the task ends, `record_count` in this event is often still 0**: recording files start transcoding and uploading only after the task ends.
After all files are uploaded, **this event is sent again**, and the counts in that one are complete.

### `mcu_record_done` — A recording file is ready

```json
{
  "meeting_id": "sny038",
  "task_id": "sxjgwy",
  "record_id": "rc3p9w",
  "seq": 2,
  "is_last": false,
  "task_type": 1,
  "vod_size": 481920000,
  "duration": 3600,
  "offset_ms": 3600000,
  "began_at": 1718254517,
  "ended_at": 1718258117,
  "reason": 1
}
```

**This event is the right time to get the playback URL.** When the task's `task_status` changes to `4` (ended normally), the file
is often still being transcoded and uploaded, so requesting the URL then may return nothing.

**One recording of a meeting produces multiple files, and this event is sent per file.** A recording longer than the segment limit (1 hour by default)
is split into segments by duration, and a recording that resumes after an interruption also starts a new segment. So:

+ **Get the playback URL by `record_id`, not `task_id`**. See [Get the playback URL of a recording file](/en/meeting/server-api/mcu#get-the-playback-url-of-a-recording-file)
+ `seq` starts at 1, and sorting by it gives the playback order; `offset_ms` is the offset (milliseconds) from the start of the whole recording, for continuous playback
+ `reason`: `1` split by duration, `2` resumed after an interruption (**there is a time gap from the previous segment**), `3` final segment at the end, `0` unknown
+ `is_last` is `true` when all files of this recording are ready

`duration` is this segment's duration (seconds), and `vod_size` is its size in bytes.

<Tip>
  To get all playable URLs of a meeting in one call, use
  [Get playback URLs of all recordings in a meeting](/en/meeting/server-api/mcu#get-playback-urls-of-all-recordings-in-a-meeting).
  It returns every segment, sorted by segment number.
</Tip>

### `mcu_alarm` — Recording task error

```json
{
  "meeting_id": "sny038",
  "task_id": "sxjgwy",
  "title": "Weekly sync",
  "task_type": 1,
  "task_status": 1,
  "gw": "mcu-gw-01",
  "alarm_at": 1718250917,
  "alarm_brief": "推流中断"
}
```

(The `alarm_brief` above means "Stream push interrupted".) `gw` is the gateway node running the task. Giving us this value speeds up troubleshooting a lot. Note that an alarm **doesn't mean the task has stopped**—
rely on `task_status` in `mcu_status_change`.

## Idempotency and retry

Network jitter can cause the same event to be delivered more than once. Make your handling idempotent by `event` + business key (`meeting_id`, `task_id`,
`user_id`). Don't deduplicate by `time`—there can be several events of the same type within the same second.
