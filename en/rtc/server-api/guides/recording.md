---
title: "Cloud recording and live streaming guide"
description: "How cloud recording, stream mixing, audio recording, and live streaming work for a whole channel: combining task types, how one recording yields multiple files, layouts and grid assignment, and how to get recording files and live stream URLs. Read this before integrating cloud recording."
---

This page covers how cloud recording and live streaming work as a whole. For the parameters and response structure of each endpoint, see [Cloud recording and live streaming](/en/rtc/server-api/mcu).

<Note>This page covers recording the **whole channel**: the entire channel is mixed into one stream. The output is **not necessarily a single file**—long recordings are split into segments by duration; see "One recording produces multiple files" below. If what you need is audio **split into tracks by speaker and into segments by utterance**, that is a different set of endpoints: see [Per-speaker voice recording](/en/rtc/server-api/talkrec). The differences between the two are in the comparison table below.</Note>

## One task, four capabilities

`task_type` is a **bit mask**. Each of the four independent capabilities takes one bit; add the values of the ones you want at the same time:

| Value | Capability | Output | How to get it |
| --- | --- | --- | --- |
| 1 | Video recording | Recording files (possibly several segments) | [Get a recording file's playback URL](/en/rtc/server-api/mcu#get-a-recording-files-playback-url) |
| 2 | Stream mixing | Mixes multiple streams into one | Re-streaming, for downstream systems that don't support multiple streams |
| 4 | Audio recording | Audio-only file | Same as video recording |
| 8 | Live stream | Live stream playback URL | [Get live stream playback URLs](/en/rtc/server-api/mcu#get-live-stream-playback-urls) |

So `3` = video recording + stream mixing, `9` = video recording + live stream, and `15` = all four.

<Warning>Don't treat `3` as a separate "hybrid mode" type. Earlier docs listed the values as "1 recording, 2 mixing, 3 hybrid", which was wrong—it left out audio recording and live stream, and misrepresented how the values combine.</Warning>

## One recording produces multiple files

**Recording is not "one recording, one file".** Two situations split it into multiple files:

+ The recording is longer than the segment limit (1 hour by default): when transcoding after the task ends, it is split into rolling segments by duration, with continuous time between segments
+ The underlying recording stops automatically partway through because there has been no audio or video for 30 seconds, and is then restarted: a new segment starts, **with a time gap between segments**

So the data model has **two levels**: one recording = one task (`task_id`), and the task has N recording files (`record_id`):

| What you need | Endpoint |
| --- | --- |
| All playable URLs for the whole recording (most common) | [Get recording task details](/en/rtc/server-api/mcu#get-recording-task-details); every segment in the `records` array already includes its URL |
| Page through the files of one recording | [List recording files](/en/rtc/server-api/mcu#list-recording-files) |
| The URL of a single segment | [Get a recording file's playback URL](/en/rtc/server-api/mcu#get-a-recording-files-playback-url), passing `record_id` |
| URLs of several segments in one call | [Batch get recording file playback URLs](/en/rtc/server-api/mcu#batch-get-recording-file-playback-urls) |

Each file carries these fields, which are enough to build complete playback:

+ `seq` starts at 1; sorting by it gives the playback order
+ `offset_ms` is this segment's offset (in milliseconds) from the start of the whole recording; use it to build the progress bar for continuous playback
+ `began_at` / `ended_at` are wall-clock times, for aligning with the timeline of your own business
+ `reason=2` means **there is a time gap between this segment and the previous one** (recording was interrupted and then restarted); continuous playback jumps there

<Note>
  Recording files start transcoding and uploading only **after the task ends**. There is a wait between stopping the recording and being able to play it, which is longer for long recordings.
  To tell when a recording is playable, rely on the `mcu_record` callback (`is_last` is `true` on the last one), not on the task status
  changing to "ended". See the [Callback events guide](/en/rtc/server-api/guides/callbacks).
</Note>

### Audio recording is not voice recording

Audio recording (`task_type=4`) on this page is **MCU mixed audio recording**: the entire channel is mixed into one audio stream, one file per task.

If what you need is audio **split into tracks by speaker and into segments by utterance** (push-to-talk records, per-person timing, sentence-by-sentence transcription), use
[Per-speaker voice recording](/en/rtc/server-api/talkrec), which is a different set of endpoints:

| | MCU audio recording (`task_type=4`) | Voice recording (talkrec) |
| --- | --- | --- |
| Output | The whole channel mixed into one stream (long recordings are split into multiple segments by duration) | One segment per utterance, each a separate file |
| Tracks | Not split; everyone is mixed together | Split by speaker, with `uid` / `name` |
| When it's available | After the task stops and transcoding finishes | As soon as each segment closes, while recording continues |
| Best for | Archiving the channel's audio | Push-to-talk, record keeping, per-sentence processing |

You can run both at the same time; they don't affect each other.

## Key differences between video recording and live streaming

| | Video recording | Live streaming |
| --- | --- | --- |
| When the URL is available | After the task **stops and transcoding finishes** | While the task is **in progress** |
| Use | Playback and archiving afterward | Distributing the video to an audience that doesn't take part in the interaction |
| URL expiration | Yes; get a new URL before each playback | Yes |

This difference determines the call sequence: a live stream "can be distributed as soon as it starts", while a recording "has output only after it ends".

## Choosing a layout

`layout_data.layout` determines the video layout. `auto` picks a grid automatically based on the number of online users, which **works for most cases**; specify a layout only when you need a fixed one:

| Value | Description |
| --- | --- |
| `auto` | Automatic, picks a grid based on the number of online users |
| `full` | Single full-screen view |
| `grids_N` | Equal grid, where N is 2, 3, 4, 5, 6, 8, 9, 12, 16, 20, or 25 (`grids_3` is a pyramid layout)|
| `right_4` / `top_4` | Main view + small views on the right / at the top |
| `br_7` / `tl_7` | Bottom L-shape / top L-shape |
| `tb_8` | Side-by-side layout |

Note that N in `grids_N` is **not continuous** (there is no 7, 10, or 11). Passing an unsupported value returns an error.

If you don't pass `layout_data`, the app's [default recording configuration](/en/rtc/server-api/mcu#get-the-default-recording-configuration) is used—put a common watermark, labels, and layout policy there so you don't have to pass them every time you start a task.

## Pinning users to specific cells

`layout_data.div_list` pins specific users to specific cells. Cells without an assignment are filled automatically in the order users joined.

+ `cells[].idx` is the cell index, in the same order as `<td>` cells in an HTML table (left to right, top to bottom)
+ **Leaving `uids` empty** means "the remaining online users rotate through these cells" (global rotation); **listing several** means those users rotate through these cells (group rotation)
+ `polling_dur` is the rotation interval in seconds; `0` means no rotation
+ When `cells[].bind_share` is `true`, the cell is bound to the channel's screen sharing stream first

A typical use is "main speaker pinned to the large cell, everyone else rotating through the small cells": put the main speaker's `uid` in the large cell's `cells`, and leave `uids` empty in the small cells' `cells` with `polling_dur` set.

## Behavior when no one is in the channel

`layout_data.nobody_text` determines what happens when no one is in the channel:

+ **Empty** → recording pauses (recommended, to avoid long stretches of black video)
+ **Text set** → recording continues and shows the text

## Watermark and user name labels

+ `watermark.type`: `0` default, `1` none, `2` single row, `3` multiple rows. If `watermark.text` is empty, the task's `title` is used as the watermark
+ The position of user name labels is written as a combination of letters: `L` left, `R` right, `T` top, `B` bottom, which can be combined (`LB` = bottom left). **Empty means no labels**

## Full sequence

```text
1. Optional: configure the app's default recording settings    POST /server/v1/mcu/save-record-config
2. Once someone is in the channel, start the task              POST /server/v1/mcu/start        → task_id
   ├─ task_type includes 8 → live stream URL available now     POST /server/v1/mcu/live-url
   └─ Need to change the layout → call start again with the same parameters (for the same channel and type, this updates the task instead of creating a new one)
3. End                                                         POST /server/v1/mcu/stop
4. Get playback after transcoding finishes                     POST /server/v1/mcu/vod-url
5. Archive and organize                                        POST /server/v1/mcu/update-record
```

When a channel is destroyed, in-progress tasks **stop automatically**; you don't need to call stop first.

## Billing note

Video recording, audio recording, and live streaming are server-side capabilities that incur ongoing costs. If you forget to stop a task after starting it, it keeps running until the channel is destroyed—so explicitly call stop in your end-of-call flow rather than relying only on channel destruction.
