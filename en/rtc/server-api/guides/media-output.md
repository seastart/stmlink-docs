---
title: "Media output guide"
description: "Send a channel's video and audio out: HTTP-FLV / RTSP pull URLs and RTMP / RTMPS push tasks. Video from the composite video or any one user, audio from the channel's mixed audio or any one user, in any combination; covers the stream mixing dependency, protocol limits, push status and alarms, and migration from the old endpoints"
---

This page covers how media output works as a whole: how to choose video and audio, the limits of pulling and pushing, and how to manage push tasks.
For the parameters and response structure of each endpoint, see [Media output](/en/rtc/server-api/stream).

## One set of sources, two kinds of output

Media output answers two questions: **what you want** (where the video and the audio each come from) and **how you get it** (pull or push). The two are independent:

| Output | Endpoint | Protocol | Suited to |
| --- | --- | --- | --- |
| Pull | [Request a pull URL](/en/rtc/server-api/stream#request-a-pull-url) | HTTP-FLV, RTSP | Web players, business systems, NVRs / surveillance platforms, and transcription or analysis services that pull the stream themselves |
| Push | [Start a push](/en/rtc/server-api/stream#start-a-push) | RTMP, RTMPS | Pushing to WeChat Channels, Douyin, your own CDN, or other live streaming platforms, which distribute it to the audience |

Pulling and pushing use **the same set of source parameters**, so you learn them once.

## Choosing video and audio

| Parameter | Values | Description |
| --- | --- | --- |
| `video` | `mcu` / `user` / `none`, required | `mcu` is the channel's composite video; `user` is one user's video; `none` means no video |
| `video_uid` | uid | Required when `video=user` |
| `video_desc` | Track description | When the user publishes multiple video tracks at once (such as camera and screen sharing), specifies one of them; if omitted, the first one to arrive is used |
| `audio` | `auto` (default) / `mix` / `user` / `none` | `mix` is the channel's mixed audio; `user` is one user's audio; `none` means no audio |
| `audio_uid` | uid | Required when `audio=user` |
| `audio_desc` | Track description | When the user publishes multiple audio tracks, specifies one of them; if omitted, the first one is used |

`audio=auto` means **the audio follows the video**:

| `video` | `auto` resolves to |
| --- | --- |
| `mcu` | The channel's mixed audio |
| `user` | The audio of the user in the video (`audio_desc` can still pick the track) |
| `none` | Not allowed; returns a parameter error—without video you must say explicitly where the audio comes from |

`video` and `audio` can't both be `none`. Video and audio can come from different users. Common combinations:

| You want | Parameters |
| --- | --- |
| The whole channel's composite video and mixed audio (live streaming) | `video=mcu` |
| One user's video and audio (a single stream, such as monitoring one terminal) | `video=user`, `video_uid=A` |
| Presenter's video + the channel's mixed audio (so viewers hear questions) | `video=user`, `video_uid=presenter`, `audio=mix` |
| A user's screen sharing + their microphone | `video=user`, `video_uid=A`, `video_desc=screen` |
| The composite video without audio | `video=mcu`, `audio=none` |
| Only the channel's mixed audio (for example, for a transcription service) | `video=none`, `audio=mix` |
| Only one user's audio | `video=none`, `audio=user`, `audio_uid=A` |

## The composite video and mixed audio depend on a stream mixing task

When `video=mcu`, or the audio resolves to the channel's mixed audio (`audio=mix`, or `auto` following the composite video),
the channel must have a **stream mixing task in progress**—`task_type` includes `2` when you [start a recording or stream mixing task](/en/rtc/server-api/mcu).
The composite video's layout, watermark, and user name labels are all configured there; media output only uses the result. See the [Cloud recording and stream mixing guide](/en/rtc/server-api/guides/recording).

Without a stream mixing task, pulling and pushing behave differently:

| | Pull | Push |
| --- | --- | --- |
| Behavior | Returns error code `1073` right away instead of issuing a URL that can't be pulled | Can be created in advance; the push stays in `waiting` and starts automatically once the stream mixing task starts |
| Reason | Once a URL is issued it's out of our control, and an unpullable URL just leaves the player waiting | Matches the habit of "set up the push first, then start the meeting" |

Using only a single user's video and audio (`video=user`, `audio=auto` or `user`) doesn't depend on a stream mixing task and doesn't use MCU resources.

## Pulling: HTTP-FLV and RTSP

|  | HTTP-FLV (`protocol=flv`) | RTSP (`protocol=rtsp`) |
| --- | --- | --- |
| Video | H264 only, no transcoding. If the publisher uses VP8, **no video can be pulled** (the player gets a 404) | Passed through as is; H264, H265, and VP8 all work. VP8 / H265 need player support (ffmpeg and VLC work, many NVRs don't) |
| Audio | Opus transcoded to AAC (48 kHz mono) | Transcoded to AAC by default; pass `rtsp_audio=opus` to pass Opus through as is and skip server-side transcoding |
| Transport | HTTP | RTSP over TCP only (for example, ffplay with `-rtsp_transport tcp`) |
| Typical players | Web (flv.js, mpegts.js), ffmpeg | NVRs, surveillance platforms, VLC, ffmpeg |

+ **The composite video is always H264**, so HTTP-FLV with `video=mcu` isn't affected by the publishers' codecs. To pull a single user's video over HTTP-FLV, have the publisher use H264
+ RTSP defaults to AAC for compatibility: NVRs, surveillance platforms, and most RTSP clients only accept AAC / G.711, not Opus. Use `rtsp_audio=opus` when you're sure the player supports Opus
+ The URL is signed and valid for 24 hours by default (adjustable with `expire`, at most one day); it can be pulled repeatedly by multiple players until it expires. After expiry, new pull requests are rejected, while **playback already in progress continues**.
  The actual validity period is the returned `expire_at`; request a new URL before each playback instead of caching it for a long time
+ **On-demand subscription**: sources are subscribed only when someone pulls and unsubscribed automatically after the last player disconnects, so nothing is consumed when no one is pulling, and there is no stop endpoint
+ URLs can be generated in advance: if the source hasn't published yet when pulling, the player gets a 404 and should retry; if the user leaves and comes back, the pull doesn't break, with a gap in between
+ RTSP doesn't fill in silence: while the audio source is absent (not published, or muted and not sending), the audio is a gap, which players generally handle fine

### Limits of audio only (`video=none`)

Audio-only HTTP-FLV has no video timeline, so **it doesn't fill in silence when the audio source drops out**: if the source stops sending for more than 3 seconds, the audio in the FLV has a gap,
web players may stall buffering, and it resumes when the source comes back (the connection isn't closed). If you need continuous audio, use RTSP, or include video.

## Push tasks

A push is a separate task: [Start a push](/en/rtc/server-api/stream#start-a-push) returns a `push_id`,
which you use to [stop the push](/en/rtc/server-api/stream#stop-a-push) and [check its status](/en/rtc/server-api/stream#list-push-tasks).

+ **A channel can push multiple streams at once**: for example, the composite video to WeChat Channels and a guest's own video to another platform at the same time
+ **Starting again for the same push URL in the same channel doesn't start another push**: if the sources are unchanged, the existing `push_id` is returned; if they changed, this push is updated to the new sources—so you don't need to stop and restart to switch the video
+ Push URLs support `rtmp://` and `rtmps://` and must include the stream key (URLs with an empty stream name such as `rtmp://host/app/` return `1075`)
+ The channel must already be open; **when the channel is destroyed, all of its pushes stop automatically**
+ Video is pushed as H264 only, without transcoding (the composite video is always H264; when pushing a single user's video, have the publisher use H264); audio is transcoded from Opus to AAC
+ Push URLs in the push list are masked (the stream key is replaced with `***`); the full URL exists only in your own copy

### Push status

| `status` | Meaning |
| --- | --- |
| `waiting` | Waiting for the source: the stream mixing task hasn't started, or the user to push hasn't published or has left for now. **Not a failure and no alarm**; pushing starts automatically once the source appears |
| `connecting` | The source is available and the live streaming platform is being connected |
| `publishing` | Pushing |
| `retrying` | Pushing to the live streaming platform failed (couldn't connect, rejected, or disconnected partway); reconnects automatically after 3 seconds, see `err` for the reason |
| `stopped` | Stopped (the stop endpoint was called, or the channel was destroyed) |

When `push_id` is omitted, the push list returns pushes in progress and those stopped within the last day.

### Audio-only pushes

Pushes with `video=none` work at the protocol level, but **many live streaming platforms require video**; whether audio only is accepted depends on the platform.
When the audio source stops sending, there is no video timeline to fill in silence: a pause within 10 seconds is a gap, and after more than 10 seconds the push disconnects and goes back to `waiting`.
When the source returns, the platform is reconnected, and the platform usually treats it as a new live session.

### Push failure alarms

When a push keeps failing (stays in `retrying` for about 90 seconds), you are notified once through the [`mcu_alarm` callback](/en/rtc/server-api/guides/callbacks):

+ **`task_type` `0`** means it's a push alarm, and **`task_id` is then the `push_id`**
+ `push_id` has the same format as an MCU task ID but isn't an MCU task—**don't pass it to `mcu/detail` or other `mcu/*` endpoints**
+ An alarm doesn't mean the push has stopped; the gateway keeps retrying. Whether it has recovered is shown by `status` in the push list

`waiting` never triggers an alarm—an absent source is a normal business state, not a fault.

## Error codes

| Error code | Meaning | What to do |
| --- | --- | --- |
| `1070` | No stream output gateway available | Pulling requires the media gateway with the pull module enabled; for self-hosted deployments, check with whoever deployed it |
| `1071` | The stream output gateway failed to issue a pull URL | Retry later; contact us if it keeps failing |
| `1072` | No live push gateway available | Pushing requires the media gateway with the push module enabled |
| `1073` | No stream mixing task in progress in the channel | Start a stream mixing task with `task_type` including `2` first, or use a single user's video / audio instead |
| `1074` | Push task not found | Check the `push_id` |
| `1075` | Invalid push URL | Use `rtmp://` or `rtmps://` and include the stream key |
| `1076` | The live push gateway rejected the push request | Retry later; contact us if it keeps failing |

For all error codes, see [Error codes](/en/rtc/server-api/error-codes).

## Self-hosted deployment

Media output is handled by the media gateway, which must be deployed separately with the pull ports open (RTSP 8554, HTTP-FLV 8556)
and outbound access to the live streaming platforms allowed (RTMP 1935 / RTMPS 443). See [Network and port requirements](/en/product/deploy/ports).

## Migrating from the old endpoints

The old single-stream and live streaming endpoints have been removed with no compatibility period. Move your callers to the new endpoints before upgrading:

| Old usage | New usage |
| --- | --- |
| `stream/flv-url` (`uid`, `desc`, `audio`…) | `stream/pull-url` with `protocol=flv`, `video=user`, `video_uid=old uid`, `video_desc=old desc`; map the audio parameters to `audio` / `audio_uid` / `audio_desc` with the same meaning |
| `stream/rtsp-url` | `stream/pull-url` with `protocol=rtsp`, `video=user`, `video_uid=old uid`. Note that audio **now defaults to AAC**; pass `rtsp_audio=opus` to keep the old Opus passthrough |
| `mcu/live-url` | `stream/pull-url` with `protocol=flv`, `video=mcu` (no `task_id` needed; located by `channel`) |
| `layout_data.push_url` / `push_audio*` of `mcu/start` | `stream/push/start` with `video=mcu`, and `audio` equivalent to the old `push_audio`; stop with `stream/push/stop`—it no longer stops together with the MCU task |
| `task_type` including `8` (live stream) | Change to `2` (stream mixing), for example `9` → `3`; passing `8` returns an error. The stream mixing task publishes the composite video back to the channel; then pull or push it with the endpoints above |

+ Error code `1047` (invalid MCU push URL) has been removed and replaced by `1075`; `1048` (task in push mode has no playback URL) has been removed—pulling and pushing are independent, so this case no longer exists
+ Type 8 tasks still in progress at upgrade time are automatically handled as stream mixing; historical tasks that have already ended may still have a `task_type` that includes `8` when queried
+ The `mcu_alarm` callback for push alarms adds the `task_type=0` case; use `task_type` to tell MCU task alarms from push alarms
