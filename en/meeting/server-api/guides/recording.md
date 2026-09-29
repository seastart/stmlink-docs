---
title: "Cloud recording and live streaming guide"
description: "How cloud recording, stream mixing, and live streaming work for meetings: combining task types, when tasks start automatically, layouts and grid assignment, and how to get recording files and live stream URLs. Read this before integrating meeting recording."
---

This page covers how cloud recording and live streaming work as a whole. For the parameters and response structure of each endpoint, see [Meeting recording and live streaming](/en/meeting/server-api/mcu).

## One task, four capabilities

`task_type` is a **bit mask**. Each of the four independent capabilities takes one bit; add the values of the ones you want at the same time:

| Value | Capability | Output | How to get it |
| --- | --- | --- | --- |
| 1 | Video recording | Recording files (possibly several segments) | [Get the playback URL of a recording file](/en/meeting/server-api/mcu#get-the-playback-url-of-a-recording-file) |
| 2 | Stream mixing | Mixes multiple streams into one | Re-streaming, for downstream systems that don't support multiple streams |
| 4 | Audio recording | Audio-only file | Same as video recording |
| 8 | Live stream | Live stream playback URL | [Get live stream URLs](/en/meeting/server-api/mcu#get-live-stream-urls) |

So `3` = video recording + stream mixing, `9` = video recording + live stream, and `15` = all four.

<Warning>Don't treat `3` as a separate "hybrid mode" type. Earlier docs listed the values as "1 recording, 2 mixing, 3 hybrid", which was wrong—it left out audio recording and live stream, and misrepresented how the values combine.</Warning>

## Some tasks start automatically

This is where SMeeting differs most from the underlying SRTC: **not every recording needs you to call start manually**.
When the first person enters the meeting, the server decides whether to start a task based on the meeting's own settings:

| Meeting | Automatically started `task_type` |
| --- | --- |
| Regular meeting, `auto_record` off | None |
| Regular meeting, `auto_record` on | `1` video recording |
| **Scheduled** meeting in composite mode, `auto_record` off | `2` stream mixing |
| **Scheduled** meeting in composite mode, `auto_record` on | `3` video recording + stream mixing |

If live streaming is enabled in your deployment, `8` (live stream) is added to every row above—for example, a regular meeting with
`auto_record` on actually starts `9`. This switch is set by the deployment, not by the API. If you're not sure, ask us.

Automatically started tasks use the meeting's own `layout_data` for the layout, or `auto` if none is set.

So: **set `auto_record` to `true` when you create the meeting, and you don't need to manage starting and stopping recording in your business logic.**
Calling [start](/en/meeting/server-api/mcu#start-or-update-a-recording-task) manually is for cases like "deciding to record partway through the meeting".

## Calling start again for the same meeting updates the task instead of creating one

A meeting has only one in-progress task per type. Calling `start` again with different parameters changes the existing task
(for example, switching the layout). It doesn't create another task or a second recording file.

## Key differences between video recording and live streaming

| | Video recording | Live streaming |
| --- | --- | --- |
| When the URL is available | After you receive the `mcu_record_done` callback | While the task is **in progress** |
| Use | Playback and archiving afterward | Distributing the video to an audience that doesn't take part in the interaction |
| URL expiration | Yes; get a new URL before each playback | Yes |

<Note>To get playback URLs, wait for the [`mcu_record_done` callback](/en/meeting/server-api/guides/callbacks). Don't request them as soon as the task ends—transcoding usually isn't finished yet.</Note>

## Choosing a layout

`layout_data.layout` determines the video layout. `auto` picks a grid automatically based on the number of online members, which **works for most cases**;
specify a layout only when you need a fixed one:

| Value | Description |
| --- | --- |
| `auto` | Automatic, picks a grid based on the number of online members |
| `full` | Single full-screen view |
| `grids_N` | Equal grid, where N is 2, 3, 4, 5, 6, 8, 9, 12, 16, 20, or 25 (`grids_3` is a pyramid layout)|
| `right_4` / `top_4` | Main view + small views on the right / at the top |
| `br_7` / `tl_7` | Bottom L-shape / top L-shape |
| `tb_8` | Side-by-side layout |

Note that N in `grids_N` is **not continuous** (there is no 7, 10, or 11). Passing an unsupported value returns an error.

If you don't want to pass the layout every time, put a common watermark, labels, and layout policy in the [recording settings](/en/meeting/server-api/mcu#save-recording-settings).

## Pinning members to specific views

`layout_data.div_list` pins specific users to specific views. Views without an assignment are filled automatically in the order members entered the meeting.

+ `cells[].idx` is the view index, in the same order as `<td>` cells in an HTML table (left to right, top to bottom)
+ **Leaving `uids` empty** means "the remaining online users rotate through these views" (global rotation); **listing several** means those users rotate through these views (group rotation)
+ `polling_dur` is the rotation interval in seconds; `0` means no rotation
+ When `cells[].bind_share` is `true`, the view is bound to the in-meeting screen sharing stream first

A typical use is "host pinned to the large view, everyone else rotating through the small views": put the host's
`user_id` in the large view's `cells`, and leave `uids` empty in the small views' `cells` with `polling_dur` set.

## Behavior when no one is in the meeting

`layout_data.nobody_text` determines what happens when no one is in the meeting:

+ **Empty** → recording pauses (recommended, to avoid long stretches of black video)
+ **Text set** → recording continues and shows the text

## Watermark and member name labels

+ `watermark.type`: `0` default, `1` none, `2` single row, `3` multiple rows. If `watermark.text` is empty, the meeting title is used as the watermark
+ The position of member name labels is written as a combination of letters: `L` left, `R` right, `T` top, `B` bottom, which can be combined (`LB` = bottom left). **Empty means no labels**
+ Leave font size, color, and outline at their defaults; set them only when you have specific visual requirements

## Full sequence

```text
1. Optional: configure the app's default recording settings    POST /server/v1/mcu/save-record-config
2. Set auto_record when creating the meeting                   POST /server/v1/meet/create
   → the task starts automatically when the first person enters; skip to step 5
   Or: start manually partway through the meeting              POST /server/v1/mcu/start        → task_id
3. task_type includes 8 → live stream URL available right away POST /server/v1/mcu/live-url
4. End                                                         POST /server/v1/mcu/stop
5. Get playback after the mcu_record_done callback             POST /server/v1/mcu/vod-url   (one segment by record_id)
   For all segments of the meeting                             POST /server/v1/mcu/vods-url
```

## One recording produces multiple files

**Recording is not "one recording, one file".** Two situations split it into multiple files:

+ The recording is longer than the segment limit (1 hour by default): when transcoding after the task ends, it is split into rolling segments by duration, with continuous time between segments
+ The underlying recording stops automatically partway through because there has been no audio or video for 30 seconds, and is then restarted: a new segment starts, **with a time gap between segments**

So keep three things in mind when integrating:

1. **Get URLs by `record_id`, not `task_id`.** The `mcu_record_done` callback is sent per file, so one recording sends several,
   each with its own `record_id`. `task_id` identifies the whole task and only locates the task.
2. **`vods-url` returns all segments of the meeting in one call**, sorted by segment number. Each segment includes `record_id` / `seq` / `began_at` /
   `duration` / `offset_ms`. For continuous playback, play in `seq` order and use `offset_ms` to build the progress bar.
3. **There is a time gap between a `reason=2` segment and the previous one** (recording was interrupted). Continuous playback jumps there, so it's worth showing a hint in your UI.

The four `vods-url` fields `url` / `size` / `mcu_at` / `mcu_dur` keep their meaning (`mcu_at` is this segment's start time,
`mcu_dur` is this segment's duration). If you already integrated with these fields, you don't need to change anything.

<Note>
  Recording files start transcoding and uploading only **after the task ends**. So there is a wait between stopping the recording and being able to play it,
  and longer for long recordings. To tell when a recording is playable, rely on the `mcu_record_done` callback (`is_last` is `true` on the last one),
  not on the task status changing to "ended".
</Note>

## Billing note

Video recording, audio recording, and live streaming are server-side capabilities that incur ongoing costs. Leaving `auto_record` on means every meeting is recorded—
confirm that's what you want before going live. For manually started tasks, it's best to explicitly call stop in your meeting-ending flow.
