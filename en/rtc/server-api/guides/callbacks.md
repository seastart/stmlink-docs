---
title: "Callback events guide"
description: "How SRTC notifies your backend when channels, users, devices, or recordings change: request format, signature verification, response requirements, the fields of each event, synchronous events that can reject an operation, and idempotency. Read this when setting up callbacks."
---

Callbacks let your backend learn about changes on the RTC side without polling. Register the URL with [Configure callbacks](/en/rtc/server-api/channel#configure-callbacks).
Subscribing to any event is optional, and **events you don't subscribe to are not sent**.

## Request format

We send a POST request to the `cb_url` you registered. The event name appears in both the query parameters and the request body:

```text
POST {your cb_url}?event=user_join
Content-Type: application/json; charset=utf-8
```

```json
{
  "app_id": "68b3ft51smhz0x5glscw9whm78bw57uu",
  "time": 1718250917,
  "event": "user_join",
  "data": { "channel": "fire", "uid": "1001" }
}
```

Events differ only in `data`; the three outer fields are always the same. `time` is the Unix timestamp (in seconds) when the event occurred.

## Verify the signature (required)

The signature in the callback request headers uses **exactly the same algorithm as server API calls** (see the [Overview](/en/rtc/server-api/overview)),
just in the opposite direction: this time we sign with your `app_key` and you verify. The request headers are `app_id` / `nonce` / `timestamp` / `signature`.

Without signature verification, anyone who knows your callback URL can forge events. **Don't skip this step.**

## Response requirements

+ The HTTP status code must be `200`
+ The response body must be standard JSON: `{"code": 0}`
+ Our request timeout is **5 seconds**. Your handler must return within that time (move heavy work to async processing)

How failures are determined, and what happens, depends on the kind of event:

| | Asynchronous notification events | Synchronous events |
| --- | --- | --- |
| You return non-200 / non-JSON / a non-zero `code` | Retried up to 5 times, then dropped | **The operation is rejected** |
| Purpose | Lets you know what happened | Lets you decide whether to allow it, and supply data |

Only `agent_join` and `agent_operate` are synchronous; all others are asynchronous notifications.

## Asynchronous notification events

### `channel_open` — Channel opened

```json
{ "channel": "fire" }
```

### `channel_destroy` — Channel destroyed

```json
{ "channel": "fire", "reason": 2 }
```

`reason`: `1` destroyed explicitly (the destroy endpoint was called), `2` destroyed automatically because the online count reached 0.

### `user_join` — User joins the channel

```json
{ "channel": "fire", "uid": "1001" }
```

### `user_leave` — User leaves the channel

```json
{ "channel": "fire", "uid": "1001", "reason": 1, "online": 3 }
```

+ `reason`: `1` left voluntarily, `2` removed, `3` replaced by a later join with the same `uid`, `4` heartbeat timeout, `5` channel destroyed, `6` switched to audience
+ `online` is the number of online users in the channel **after** this user left; `0` means the channel is now empty

### `im_connect` / `im_disconnect` — IM device online / offline

```json
{ "uid": "1001", "sid": "co63jg6g54hu3b0xhtie", "device_type": 3, "device_id": "aacc" }
```

`im_disconnect` has an extra `reason`, with the same values as `user_leave`.

`device_type`: `0` unknown, `1` Windows, `2` Android, `3` iOS, `4` Linux, `5` macOS, `6` WebRTC, `7` WeChat Mini Program.
From `80` up is the range for agents joining on the server side (`81` MCU, `82` SIP, `83` H.323, `84` GB28181, `85` RTSP, `86` RTMP, `87` file playback, `88` stream distribution, `89` transcription).

### `agent_online` / `agent_offline` — Device online / offline

Tells you whether a device is online **outside the channel**: a phone or GB28181 camera is online once it registers with the device gateway, and offline once it unregisters or disconnects.
This is unrelated to whether it's in a channel (for joining and leaving a channel, see `user_join` / `user_leave`).

```json
{ "id": "sz8nk8", "type": 4, "contact": "34020000001320000001", "name": "Main gate camera", "gw": "devgate-1" }
```

`agent_offline` has two extra fields:

```json
{ "id": "sz8nk8", "type": 4, "contact": "34020000001320000001", "name": "Main gate camera", "gw": "devgate-1", "reason": 4, "heartbeat_at": 1718250917 }
```

+ `id` is the device ID in [List devices](/en/rtc/server-api/agent#list-devices); `gw` is the gateway the device is on
+ `type`: `2` SIP, `3` H.323, `4` GB28181 surveillance
+ `contact` identifies the device: the registration username for SIP, the short number for H.323, and the device number for GB28181 (`sip_no`, not a channel number)
+ `reason`: `1` the device unregistered, `4` heartbeat timeout
+ `heartbeat_at` is the time of the last heartbeat. An offline event caused by heartbeat timeout waits for the timeout to be determined, so it's sent **5–7 minutes after the actual disconnect**.
  When you need the actual disconnect time, use this field

Only **registration-mode** devices (`regsip`, `regh323`, `gb28181`) have an online status and send these two events;
with direct IP and RTSP stream pull, we connect to the device ourselves, so there is no online or offline.

Each status change is sent only once: periodic registration refreshes and GB28181 Keepalives don't send `agent_online` again;
when heartbeats resume after going offline, an online event is sent again. Devices don't belong to a particular app, so every app that subscribes to this event receives it.

### `mcu_task` — Recording, stream mixing, or live streaming task status changes

```json
{
  "channel": "fire",
  "task_id": "sxjgwy",
  "task_type": 9,
  "task_status": 1,
  "err_desc": "",
  "began_at": 1718250917,
  "ended_at": 0,
  "record_count": 0,
  "total_duration": 0,
  "total_size": 0
}
```

+ `task_type` is a bit mask; for its meaning, see the [Cloud recording and live streaming guide](/en/rtc/server-api/guides/recording)
+ `task_status`: `0` pending, `1` in progress, `2` ending, `3` ended abnormally, `4` ended normally
+ `err_desc` has content only when the task ended abnormally
+ `record_count` / `total_duration` / `total_size` are the number of files, total duration (seconds), and total bytes produced by this recording

This is the most reliable signal of "whether the recording is actually running"—more meaningful than a successful response from the start endpoint.

**When the task ends, `record_count` in this event is often still 0**: recording files start transcoding and uploading only after the task ends.
Once all files are uploaded, we **send this event once more**, and the counts in that one are complete. Use it for reconciliation.

### `mcu_record` — A recording file is complete

```json
{
  "channel": "fire",
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

**One recording produces multiple files, and this event is sent per file—several times per task.** Two situations start a new file:

+ The recording is longer than the segment limit (1 hour by default): it is split into rolling segments by duration during transcoding, with continuous time between segments
+ The underlying recording stops automatically partway through because there has been no audio or video for 30 seconds, and is then restarted: a new segment starts, **with a time gap between segments**

So:

+ **Get playback URLs by `record_id`, not `task_id`**—`task_id` belongs to the task, and one task has several
  `record_id`s. Pass it when calling [Get a recording file's playback URL](/en/rtc/server-api/mcu#get-a-recording-files-playback-url)
+ `seq` starts at 1; sorting by it gives the playback order
+ `offset_ms` is this segment's offset (in milliseconds) from the start of the whole recording; use it to build the progress bar for continuous playback of several segments.
  `began_at`/`ended_at` are wall-clock times, for aligning with the timeline of your own business
+ `reason`: `1` split by duration, `2` resumed after an interruption (**there is a gap from the previous segment**; continuous playback jumps there, so it's worth showing a hint in your UI),
  `3` final segment when the task ended, `0` unknown
+ `is_last` being `true` means all files of this recording have been produced, and you can start assembling the complete playback

`vod_size` is in bytes; `duration` is in seconds.

<Tip>
  To get all playable URLs for the whole recording at once, call
  [Get recording task details](/en/rtc/server-api/mcu#get-recording-task-details)—every segment in its `records` array
  already includes its playback URL, which is easier than getting them one by one.
</Tip>

### `mcu_alarm` — Recording task alarm

```json
{
  "task_id": "sxjgwy",
  "task_type": 1,
  "task_status": 3,
  "channel": "fire",
  "title": "Weekly project sync 2024-06-12",
  "room_no": "818595664",
  "gw": "mcu-gw-01",
  "alarm_at": 1718250917,
  "alarm_brief": "任务异常结束"
}
```

(The `alarm_brief` above means "Task ended abnormally".) Use it to feed your own alerting system. Recording is billed continuously, and if no one notices an abnormal interruption, what you lose is the recording itself.

### `talkrec_task` — Voice recording task status changes

```json
{
  "channel": "fire",
  "task_id": "tk8kjx",
  "task_status": 1,
  "err_desc": ""
}
```

`task_status`: `0` pending, `1` in progress, `3` ended abnormally, `4` ended normally (there is no "ending" state as in mcu).

Starting voice recording is asynchronous—calling the endpoint only means the request was accepted. The task changes to in progress only after the voice recording gateway joins the channel successfully,
so this event is the most reliable signal of "whether voice recording is actually running".

### `talkrec_record` — A voice segment is complete

```json
{
  "channel": "fire",
  "task_id": "tk8kjx",
  "record_id": "rc3p9w",
  "uid": "1001",
  "name": "Alice",
  "vod_key": "talkrec/2024/06/12/rc3p9w.mp3",
  "vod_size": 51200,
  "duration_ms": 4200,
  "began_at": 1718250917,
  "ended_at": 1718250921,
  "end_reason": 1
}
```

Unlike video recording, voice recording sends a callback **each time a segment closes**, so one task sends many of them—split into tracks by speaker,
one segment per utterance. This is the data source for live captions, push-to-talk records, and per-person timing.

+ `record_id` is the segment ID used to get the playback URL, not `task_id`
+ `duration_ms` is in milliseconds (segments are usually only a few seconds long, so second-level precision isn't enough)
+ `end_reason`, why the segment closed: `0` unknown, `1` normal end (talk button released), `2` split on timeout, `3` user left, `4` task stopped, `5` idle timeout (fallback)

`end_reason` is worth watching: `2` means the segment was cut off by the duration limit (one utterance is split into several segments),
and `5` means the server closed the segment as a fallback. If it appears often, silence detection isn't wrapping up segments properly, and it's worth checking the audio quality.

## Synchronous events

For these two events, we **wait for your answer** before continuing, so your handling must be fast (5-second timeout).

### `agent_join` — Device requests to join the channel

```json
{
  "type": 4,
  "no": "818595664",
  "is_audience": false,
  "uid": "gb_34020000001320000001",
  "name": "Main gate camera",
  "net": "内网",
  "sg": "",
  "extend_info": "{\"gw\":\"devgate-1\"}"
}
```

`type` is the agent type: `1` MCU, `2` SIP, `3` H.323, `4` GB28181 surveillance, `5` RTSP stream pull, `6` RTMP stream pull, `7` file playback, `8` stream distribution, `9` transcription.
`no` is the target room number the device wants to join (the meeting number in your own business).

You need to turn it into a session: use `no` to find the corresponding channel, call [Get a channel join token](/en/rtc/server-api/channel#get-a-channel-join-token) to get a `sid`, and return it to us as is:

```json
{"code": 0, "data": "_agent_co63jg6g54hu3b0xhtie"}
```

Returning a non-zero `code` rejects the device's join. If your user details don't need extended `props` and the device is unconditionally trusted, you can skip subscribing to this event.

<Warning>
  When calling [Get a channel join token](/en/rtc/server-api/channel#get-a-channel-join-token), **you must put the
  `extend_info` received in this callback into the endpoint's `props` parameter as is** (use `extend_info` as the key, and the string you received as the value;
  don't parse or rewrite it):

  ```json
  {
    "channel": "fire",
    "uid": "gb_34020000001320000001",
    "props": {
      "extend_info": "{\"gw\":\"devgate-1\"}",
      "your_own_fields": "..."
    }
  }
  ```

  This field carries the ID of the gateway the device belongs to, which we use to associate the device in the channel back to its gateway. **If it's lost, these capabilities, which
  depend on notifying the gateway in return, silently stop working**: [Remove a user from the channel](/en/rtc/server-api/channel#remove-a-user-from-the-channel) has no effect on the device (the gateway
  treats it as a disconnect, and the device then rejoins automatically), and [Turn device video on or off](/en/rtc/server-api/agent#turn-device-video-on-or-off) and
  [Turn device audio on or off](/en/rtc/server-api/agent#turn-device-audio-on-or-off) fail. Put your own `props` fields in as usual;
  the two don't conflict.
</Warning>

### `agent_operate` — A device in the channel is controlled (microphone or camera on/off)

```json
{
  "channel": "fire",
  "uid": "gb_34020000001320000001",
  "by_admin": true,
  "op_uid": "1001",
  "op_type": "camera"
}
```

Returning a non-zero `code` rejects the operation. If you don't subscribe to this event, all media operations on devices are allowed automatically.

## Idempotency and ordering

Callbacks are delivered **at least once**, with no guarantee of ordering or uniqueness:

+ Retries lead to duplicate deliveries, so make your handling idempotent by a combination such as `channel` + `uid` + `time`
+ The network and queues can reorder events, so don't rely on "join arrives before leave" to track state yourself; when you need authoritative state, use the query endpoints
