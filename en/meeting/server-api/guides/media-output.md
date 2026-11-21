---
title: "Media output guide"
description: "Send a meeting's video and audio out: HTTP-FLV / RTSP pull URLs and RTMP / RTMPS push tasks. Video from the composite video or any one user, audio from the meeting's mixed audio or any one user, in any combination; covers the stream mixing dependency, protocol limits, push status and alarms, and migrating from the old endpoints"
---

This page covers how media output works at the meeting layer. For the parameters and response structure of each endpoint, see [Media output](/en/meeting/server-api/stream).

<Note>Media output at the meeting layer passes through to the SRTC endpoints of the same name, so the capabilities, protocol limits, and error codes are exactly the same as SRTC's; for details, see the SRTC [Media output guide](/en/rtc/server-api/guides/media-output). This page covers only the meeting-layer differences and common usage.</Note>

## One set of sources, two kinds of output

| Output | Endpoint | Protocol | Suited to |
| --- | --- | --- | --- |
| Pull | [Request a pull URL](/en/meeting/server-api/stream) | HTTP-FLV, RTSP | Web players, business systems, and NVRs / surveillance platforms that pull the stream themselves |
| Push | [Start a push](/en/meeting/server-api/stream#start-a-push) | RTMP, RTMPS | Pushing to WeChat Channels, Douyin, your own CDN, or other live streaming platforms |

Video and audio each choose their own source, for both pulling and pushing:

| Parameter | Values | Description |
| --- | --- | --- |
| `video` | `mcu` / `user` / `none`, required | `mcu` is the meeting's composite video; `user` is one user's video (with `video_uid`, the in-meeting user ID); `none` means no video |
| `video_desc` | Track description | When the user publishes multiple video tracks at once (such as camera and screen sharing), specifies one of them; if omitted, the first one to arrive is used |
| `audio` | `auto` (default) / `mix` / `user` / `none` | `auto` follows the video: the composite video comes with the meeting's mixed audio, a single user's video with that user's own audio, and it can't be used without video; `mix` is the meeting's mixed audio; `user` is one user's audio (with `audio_uid`) |
| `audio_desc` | Track description | When the user publishes multiple audio tracks, specifies one of them; if omitted, the first one is used |

`video` and `audio` can't both be `none`. Video and audio can come from different users; for example, "presenter's video + the meeting's mixed audio" is `video=user`, `video_uid=presenter`, `audio=mix`.

## Differences from SRTC

+ Use `meeting_id` to specify the meeting instead of SRTC's `channel`
+ `video_uid` / `audio_uid` take the in-meeting user ID
+ **Stopping a push requires both `meeting_id` and `push_id`**; `1074` is returned if the push doesn't belong to this meeting
+ Starting a push requires the meeting to be in progress (someone is in the meeting); when the meeting ends and everyone leaves, all of its pushes stop automatically
+ Requesting a pull URL or starting a push returns `2101` if the meeting for `meeting_id` doesn't exist

## The composite video and mixed audio depend on a stream mixing task

When the composite video (`video=mcu`) or the meeting's mixed audio is used, the meeting must have a **stream mixing task in progress** (`task_type` includes `2`):

+ **Composite-mode meetings** start a stream mixing task automatically on the server once people enter, so you can use it directly
+ **Regular meetings** need you to [start a recording task](/en/meeting/server-api/mcu) first with `task_type` including `2` (for example, `2` for stream mixing only, `3` for video recording + stream mixing). The layout is configured there; see the [Cloud recording and stream mixing guide](/en/meeting/server-api/guides/recording)

Without a stream mixing task, pulling returns `1073` right away; a push can be created in advance, stays in `waiting`, and starts automatically once the stream mixing task starts.
Using only a single user's video and audio doesn't depend on a stream mixing task.

## Key points of pulling and pushing

+ **HTTP-FLV** video is H264 only, without transcoding (no video can be pulled if the publisher uses VP8; the composite video is always H264); audio is transcoded to AAC
+ **RTSP** video is passed through as is (H264 / H265 / VP8); audio is transcoded to AAC by default, and `rtsp_audio=opus` passes it through as is; RTSP over TCP only
+ Pull URLs are signed and valid for 24 hours by default; sources are subscribed only when someone pulls, nothing is consumed when no one is pulling, and there is nothing to stop
+ **Pushes**: a meeting can push multiple streams at once; starting again for the same push URL in the same meeting returns the existing `push_id` (updated to the new sources if they changed)
+ Push status is `waiting` / `connecting` / `publishing` / `retrying` / `stopped`; check it with [List push tasks](/en/meeting/server-api/stream#list-push-tasks)
+ Audio only (`video=none`) has limits: HTTP-FLV doesn't fill in silence when the audio drops out, and many live streaming platforms don't accept audio-only pushes

## Push failure alarms

When a push keeps failing (retrying for about 90 seconds), you are notified through the [`mcu_alarm` callback](/en/meeting/server-api/guides/callbacks):
**`task_type` `0` means it's a push alarm, and `task_id` is then the `push_id`**—not a recording task, so don't pass it to `mcu/*` endpoints.
An alarm doesn't mean the push has stopped; rely on `status` in the push list.

## Migrating from the old usage

The old live streaming endpoints and usage have been removed with no compatibility period; switch your callers to the new endpoints:

| Old usage | New usage |
| --- | --- |
| `layout_data.push_url` / `push_audio*` of `mcu/start` | Removed. Use `stream/push/start` with `video=mcu`, and `audio` equivalent to the old `push_audio`; stop with `stream/push/stop` |
| `task_type` including `8` (live stream) | Type `8` has been removed; use `2` (stream mixing) plus the media output endpoints above. Passing `8` or a combination that includes `8` (such as `9`) to `mcu/start` or `mcu/stop` returns parameter error `10070` (invalid request parameters); at upgrade time, the `task_type` of historical tasks has `8` replaced with `2` (for example, `9` → `3`) |
| `mcu/live-url` | Removed. Use `stream/pull-url` (`protocol=flv`, `video=mcu`), which returns `url` and `expire_at`; when no stream mixing task is in progress, error code `1073` is returned (previously success with `data` null) |
