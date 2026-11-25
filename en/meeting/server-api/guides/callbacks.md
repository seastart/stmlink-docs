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
| `mcu_status_change` | The status of a recording or stream mixing task changes |
| `mcu_record_done` | A recording file is ready and you can get its playback URL (sent once per file when a recording produces several) |
| `mcu_alarm` | A recording task encounters an error, or a push task keeps failing |
| `user_mic_state_change` | A user turns the microphone on or off |
| `user_camera_state_change` | A user turns the camera on or off |
| `user_extra_screen_state_change` | A user starts or stops pushing an extra screen (a secondary screen pushed by a client) |
| `share_state_change` | The meeting's sharing status changes (sharing starts / stops) |
| `device_invite_failed` | A device invited by the platform failed to enter (busy, declined, no answer, unreachable, stream pull failed, entry refused, and so on) |
| `user_online` | A user comes online: a person establishes an IM connection, or a device registers with the device gateway / becomes reachable by probing, regardless of whether they're in a meeting (not sent by default; the deployer must enable it) |
| `user_offline` | A user goes offline: a person's IM connection closes, or a device unregisters / times out on heartbeat / becomes unreachable by probing, regardless of whether they're in a meeting (not sent by default; the deployer must enable it) |

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

Sent only after the user has actually connected to the meeting (joined its audio/video channel). Users held in the waiting room, or whose join fails partway, do not trigger it.

When the same `user_id` enters the meeting on multiple devices, the event fires once for each device.

### `user_exit` — User exits the meeting

Has two more fields than `user_enter`:

```json
{ "meeting_id": "sny038", "user_id": "1001", "reason": 1, "online": 3 }
```

+ `reason`: `1` exited voluntarily, `2` removed, `3` replaced by the same user entering again, `4` heartbeat timeout, `5` meeting destroyed, `6` switched to audience, `7` device connection lost
+ `7` only applies to SIP / H.323 terminals joined through the device gateway: the terminal dropped abnormally (signaling or media timeout, network failure). A normal hang-up on the terminal is still `1`, so you can tell a normal hang-up from an unexpected drop
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

+ `task_type` is a bit mask; for the values, see the [Cloud recording and stream mixing guide](/en/meeting/server-api/guides/recording)
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

**Push tasks that keep failing also use this event**: `task_type` `0` means it's a push alarm, and `task_id` is then the push task's `push_id`,
not a recording task, so don't pass it to `mcu/*` endpoints; whether the push has recovered is shown by `status` in [List push tasks](/en/meeting/server-api/stream#list-push-tasks).
See the [Media output guide](/en/meeting/server-api/guides/media-output).

### `user_mic_state_change` / `user_camera_state_change` / `user_extra_screen_state_change` — User media status changes

The three events share one structure. Read the status field that matches the event name; the other two are a snapshot at the time of sending:

```json
{
  "meeting_id": "sny038",
  "room_no": "803707296",
  "user_id": "1001",
  "real_name": "Alice",
  "nickname": "Alice",
  "avatar": "https://example.com/a.png",
  "role": 1,
  "device_type": 6,
  "join_at": 1718250900,
  "mic_state": 1,
  "camera_state": 2,
  "extra_screen_state": 2,
  "ts_ms": 1718250917123
}
```

+ `mic_state` / `camera_state` / `extra_screen_state`: `1` on, `2` off — the same values as the [in-meeting member list](/en/meeting/server-api/meet#list-in-meeting-members)
+ Sent only when the status actually flips. The camera counts as on while either its high or low stream is published; both appearing together sends one event
+ "Extra screen" means an extra screen pushed by a client (a secondary screen, such as the always-on second view each participant keeps in remote bid evaluation). Each person pushes their own and keeps it on; it is independent of meeting sharing (`share_state_change`)
+ Dual-stream content sharing from a SIP/H.323 endpoint doesn't use this event; it counts as meeting sharing and shows up in `share_state_change`
+ When one action toggles several media at once (for example, joining with both microphone and camera on), each is sent separately with the same `ts_ms`
+ No "off" events are sent when a user leaves; treat `user_exit` as "everything off"
+ Status reflects whether the stream is being published: a microphone that is only muted locally while still published does not trigger "off"

### `share_state_change` — Meeting sharing status changes

Both start and stop of sharing use this event, for screen sharing and whiteboard sharing alike:

```json
{
  "meeting_id": "sny038",
  "room_no": "803707296",
  "from_state": 0,
  "to_state": 1,
  "user_id": "1001",
  "nickname": "Alice",
  "ts_ms": 1718250917123
}
```

+ `from_state` / `to_state`: `0` no sharing, `1` screen, `2` whiteboard. `0→1/2` is a start, `1/2→0` is a stop, `1↔2` switches the sharing type
+ `user_id` is the person who started or stopped sharing; on stop it is the previous sharer
+ A stop is sent when the sharer stops, the host stops it, the host disables sharing, or the sharer leaves
+ When a new sharer takes over from a sharer who has dropped off, a stop for the previous sharer is sent first, then a start for the new one
+ "Start" is sent as soon as sharing is granted, without waiting for the client to actually push the screen
+ Dual-stream content sharing from a SIP/H.323 endpoint is meeting sharing too: when the endpoint presses its local share button, this event is sent (the platform can't start sharing on these endpoints remotely) and `user_id` is that device

### `device_invite_failed` — Device invitation failed

Sent when a device invited with [Invite devices to the channel](/en/rtc/server-api/agent#invite-devices-to-the-channel) (`agent/invite`) failed to enter:

```json
{
  "meeting_id": "sny038",
  "room_no": "021890611",
  "device": { "type": 2, "contact": "192.168.0.18:5060", "name": "Main conference room" },
  "reason": "busy",
  "code": 0,
  "msg": "SIP/2.0 486 Busy Here"
}
```

+ `meeting_id`: the current meeting found by `room_no`; empty if none is found (for example, the meeting was deleted), and the event is still sent
+ `room_no`: the room number given in the invitation
+ `device`: the invited device. `type` is the device type (`2` SIP, `3` H.323, `4` GB28181, `5` RTSP, and so on), `contact` is the device identifier from the invitation, and `name` is the device name
+ `code`: when `reason` is `join_refused`, the error code for the refused entry (for example, the meeting has ended); `0` otherwise
+ `msg`: the original description, such as a SIP status line, an H.323 release reason, a stream pull error, or a server message, for troubleshooting

`reason` values:

| Value | Meaning | Typical source |
| --- | --- | --- |
| `busy` | Endpoint busy | SIP 486 / 600, H.323 user busy |
| `rejected` | Endpoint declined | SIP 603 / 403, H.323 rejected |
| `no_answer` | No answer | SIP 408 / 480, ringing timeout, H.323 no answer |
| `unreachable` | Can't call / can't connect | Network unreachable, SIP 404 / 5xx, H.323 connection failed |
| `stream_failed` | Stream pull failed | RTSP / GB28181 / file can't be opened or has no data |
| `join_refused` | Entry refused | The call went through, but the meeting refused the device (for example, the meeting has ended), and retries still failed |
| `error` | Other | Fallback |

+ **Sent only for devices invited by the platform**; failures of devices dialing in by themselves (the endpoint dials the meeting number) are not sent
+ At most once per invitation; a device that entered successfully and then dropped off is not an invitation failure, that goes through `user_exit` (`reason` `7`)
+ A device already in another meeting that is invited over and refused entry to the new meeting is also sent as `join_refused`

<Warning>
  This event requires **a newer device gateway version** to be reported, and it's sent only after the deployer appends
  `agent_invite_failed` to `rtc.callback_events` in the SMeeting server configuration (off by default). For private deployments, ask your deployer to enable it; for SaaS, contact us.
</Warning>

Calls to users have no failure callback; for how to detect failures, see [Invite and remove](/en/meeting/server-api/guides/invite-and-kickout#how-to-detect-a-failed-invitation).

### `user_online` / `user_offline` — User comes online / goes offline

Tells you whether a user is **online**, regardless of whether they're in a meeting (for entering and exiting meetings, see `user_enter` / `user_exit`). People and devices share these two events, distinguished by `is_agent`:

+ **People**: a person comes online when the client enables out-of-meeting messages (for example, by calling `smeeting.enableIm()` on Web) and establishes an IM connection, and goes offline when they disconnect, are kicked, or time out on heartbeat
+ **Devices**: SIP / H.323 endpoints and GB28181 devices connected through the device gateway come online when they register with the device gateway, and go offline when they unregister or time out on heartbeat;
  direct-IP endpoints are probed periodically by the device gateway: online when reachable, offline when unreachable

A person comes online:

```json
{
  "user_id": "1001",
  "is_agent": false,
  "device_type": 3,
  "device_id": "aacc",
  "sid": "co63jg6g54hu3b0xhtie",
  "name": "",
  "contact": ""
}
```

A device goes offline (`user_offline` has two more fields than `user_online`, `reason` and `heartbeat_at`, at the same level as the other fields):

```json
{
  "user_id": "_agent_sz8nk8",
  "is_agent": true,
  "device_type": 84,
  "device_id": "sz8nk8",
  "sid": "",
  "name": "Front gate camera",
  "contact": "34020000001320000001",
  "reason": 4,
  "heartbeat_at": 1718250917
}
```

| Field | Type | Description |
| --- | --- | --- |
| `user_id` | string | For a person, your user ID; for a device, `_agent_` + device ID, matching the `user_id` in `user_enter` after the device enters a meeting (when a GB28181 device enters by channel, the in-meeting `user_id` also ends with `_<channel ID>`) |
| `is_agent` | boolean | `true` for a device, `false` for a person |
| `device_type` | integer | For a person, the client type: `1` Windows, `2` Android, `3` iOS, `4` Linux, `5` macOS, `6` WebRTC, `7` WeChat Mini Program, `8` HarmonyOS; for a device, `80` + device type: `82` SIP, `83` H.323, `84` GB28181 |
| `device_id` | string | For a person, the unique device ID reported by the client; for a device, the device ID, that is, `id` in [List devices](/en/rtc/server-api/agent#list-devices) |
| `sid` | string | The person's IM session ID, different for each client of the same user; empty for a device |
| `name` | string | The device name; empty for a person |
| `contact` | string | The device identifier: the registered username for SIP, the short number for H.323, the device number for GB28181, and the registered address for direct-IP devices; empty for a person |
| `reason` | integer | `user_offline` only. Why the user went offline: `1` disconnected / device unregistered, `2` kicked, `3` replaced by another login, `4` heartbeat timeout, `7` device unreachable by probing (direct-IP devices only) |
| `heartbeat_at` | integer | `user_offline` only. The Unix timestamp (seconds) of the device's last heartbeat; `0` for a person |

+ **Multi-device sign-in counts per connection**: when the same person enables out-of-meeting messages on several clients, each client sends its own online and offline event, distinguished by `sid`.
  To tell whether the person is still online, aggregate the `sid`s of all clients by `user_id` yourself; a single `user_offline` doesn't mean the person is offline
+ **Devices count per status change**: periodic registration refreshes and heartbeats don't resend online; an event is sent only when the device actually switches between online and offline, and a device that resumes heartbeats after going offline sends online again
+ An offline caused by heartbeat timeout waits for the timeout to be determined, so it's sent **5–7 minutes after the actual disconnection**; when you need the actual disconnection time, use `heartbeat_at`
+ Devices don't belong to any single app, so every app subscribed to these events receives the same device's online and offline events

<Warning>
  These two events are **not sent by default**: the deployer must append
  `im_connect`, `im_disconnect` (people online / offline) and `agent_online`, `agent_offline` (devices online / offline) to `rtc.callback_events` in the SMeeting server configuration.
  If you only need people or only devices, appending the corresponding two is enough. After the deployer enables them, you still need to subscribe to these two events when you [Configure event notifications](/en/meeting/server-api/meet#configure-event-notifications).
  For private deployments, ask your deployer to enable it; for SaaS, contact us.
</Warning>

## Idempotency and retry

Network jitter can cause the same event to be delivered more than once. Make your handling idempotent by `event` + business key (`meeting_id`, `task_id`,
`user_id`). Don't deduplicate by `time`—there can be several events of the same type within the same second.

Media status and sharing status events are not guaranteed to arrive in order (for example, when the microphone is toggled quickly, "off" may arrive before "on").
Trust the one with the largest `ts_ms` (milliseconds); the three media status fields are a full snapshot at the time of sending, so you can simply overwrite.
