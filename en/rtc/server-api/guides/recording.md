---
title: "Cloud recording and stream mixing guide"
description: "How cloud recording, stream mixing, and audio recording work for a whole channel: combining task types, layouts, and how to get recording files; for pulling and pushing the composite video, see the Media output guide"
---

This page covers how cloud recording and stream mixing work as a whole. For the parameters and response structure of each endpoint, see [Cloud recording and stream mixing](/en/rtc/server-api/mcu).

<Tip>To pull the composite video out for playback (HTTP-FLV / RTSP) or push it to a live streaming platform (RTMP / RTMPS), see the [Media output guide](/en/rtc/server-api/guides/media-output): start a stream mixing task first, then use the media output endpoints with `video=mcu`.</Tip>

<Note>This page covers recording the **whole channel**: the entire channel is mixed into one stream. The output is **not necessarily a single file**—long recordings are split into segments by duration; see "One recording produces multiple files" below. If what you need is audio **split into tracks by speaker and into segments by utterance**, that is a different set of endpoints: see [Per-speaker voice recording](/en/rtc/server-api/talkrec). The differences between the two are in the comparison table below.</Note>

## One task, three capabilities

`task_type` is a **bit mask**. Each of the three independent capabilities takes one bit; add the values of the ones you want at the same time:

| Value | Capability | Output | How to get it |
| --- | --- | --- | --- |
| 1 | Video recording | Recording files (possibly several segments) | [Get a recording file's playback URL](/en/rtc/server-api/mcu#get-a-recording-files-playback-url) |
| 2 | Stream mixing | Composite video and the channel's mixed audio, published back to the channel | Pull or push it with [media output](/en/rtc/server-api/guides/media-output) (`video=mcu`) |
| 4 | Audio recording | Audio-only file | Same as video recording |

So `3` = video recording + stream mixing, and `7` = all three.

<Warning>Don't treat `3` as a separate "hybrid mode" type. Earlier docs listed the values as "1 recording, 2 mixing, 3 hybrid", which was wrong—it left out audio recording and misrepresented how the values combine.</Warning>

<Note>The former `8` (live stream) has been merged into `2`. Values that include `8` now return an error; change them to `2` (for example, `9` → `3`). Live pulling and pushing now use the media output endpoints; for the migration table, see [Media output guide · Migrating from the old endpoints](/en/rtc/server-api/guides/media-output#migrating-from-the-old-endpoints). Historical tasks that have already ended may still have a `task_type` that includes `8` when queried.</Note>

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

## Choosing a layout

`layout_data.layout` determines the video layout. There are two kinds:

+ **`auto` (automatic layout)**: only users with video get a cell; the grid is picked by headcount and switches as people come and go. **Works for most cases.** `div_list` has no effect under `auto`
+ **Fixed layouts**: the structure does not change with headcount, and you can use `div_list` to pin specific people to specific cells (see the next section)

If `layout` is omitted, the server's default layout is used (`auto` by default; the deployer can change it).

| Value | Layout | Cells | Index of the large cell |
| --- | --- | --- | --- |
| `auto` | Automatic: 1 person → full screen; 2–6 → `grids_2`–`grids_6`; 7–9 → `grids_9`; 10–12 → `grids_12`; 13–16 → `grids_16`; 17–20 → `grids_20`; more → `grids_25` (up to 25 people shown) | Varies | — |
| `full` | Single full-screen view | 1 | 0 |
| `grids_N` | Equal grid, where N is 2, 3, 4, 5, 6, 8, 9, 12, 16, 20, or 25 (`grids_3` is a pyramid layout) | N | None, all equal |
| `right_4` | Small views on the right: large view on the left + a column of 4 small views on the right | 5 | 0 |
| `top_4` | Small views on top: a row of 4 small views on top + large view below | 5 | 4 |
| `br_7` | Bottom L-shape: large view at top left + 3 small views down the right and 4 along the bottom | 8 | 0 |
| `tl_7` | Top L-shape: 4 small views along the top and 3 down the left + large view at bottom right | 8 | 5 |
| `tb_8` | Side-by-side: two large views side by side in the middle + a row of 4 small views on top and at the bottom | 10 | 4, 5 |
| `ring_16` | Large ring: a 5×5 grid with the middle 9 cells merged into one large view, 16 small views around it | 17 | 6 |
| `ring_12` | Small ring: a 4×4 grid with the middle 4 cells merged into one large view, 12 small views around it | 13 | 5 |

<Warning>A value not in this table **does not return an error**; it is silently treated as `auto`. N in `grids_N` is not continuous (there is no 7, 10, or 11), so check the table before spelling it out.</Warning>

**The watermark and name labels can fall back to defaults; the layout cannot.** When `layout_data` omits `watermark` / `tag`,
`watermark_type` / `window_tag_type` from the [default recording configuration](/en/rtc/server-api/mcu#get-the-default-recording-configuration) are used. The layout, however, is not taken from that configuration—if you need a fixed layout,
pass it in `layout_data.layout` every time you start a task.

## Pinning users to specific cells

`layout_data.div_list` only works with **fixed layouts**. Each element pins one cell:

+ `cells[0].idx`: the cell index, starting at `0`, in the same order as `<td>` cells in an HTML table (left to right, top to bottom); see the table above for the index of the large cell. **It must be less than the layout's cell count**
+ `uids[0]`: the person pinned to this cell (use the `uid`). If that person is not in the channel, the cell stays empty for them
+ When `cells[0].bind_share` is `true`, the cell always shows the current screen share (regardless of who is sharing; `uids` is ignored). When no one is sharing, the cell stays empty
+ Only the **first** entry of `cells` and of `uids` in an element is used; extras are ignored. To pin several cells, put several elements in `div_list`

How the remaining cells are filled depends on `polling_dur`:

| `polling_dur` | Remaining cells |
| --- | --- |
| `0` (default) | **Left empty**; no one is filled in automatically |
| Greater than `0` | Filled with the other users who have video, in the order they joined the channel; when there are more people than cells, a new batch rotates in every `polling_dur` seconds (values below 5 are treated as 5) |

So if you want a fixed layout with "a few people pinned and everyone else arranged automatically", **you must set `polling_dur`**; otherwise only the pinned cells show video.

Typical use: "main speaker pinned to the large view, screen share pinned to one small view, everyone else rotating through the remaining small views":

```json
{
  "layout": "right_4",
  "polling_dur": 10,
  "div_list": [
    { "cells": [{ "idx": 0 }], "uids": ["main speaker's uid"] },
    { "cells": [{ "idx": 1, "bind_share": true }] }
  ]
}
```

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
   ├─ task_type includes 2 → pull / push with media output     POST /server/v1/stream/pull-url, stream/push/start
   └─ Need to change the layout → call start again with the same parameters (for the same channel and type, this updates the task instead of creating a new one)
3. End                                                         POST /server/v1/mcu/stop
4. Get playback after transcoding finishes                     POST /server/v1/mcu/vod-url
5. Archive and organize                                        POST /server/v1/mcu/update-record
```

When a channel is destroyed, in-progress tasks **stop automatically**; you don't need to call stop first.

## Billing note

Video recording, stream mixing, and audio recording (as well as pushes) are server-side capabilities that incur ongoing costs. If you forget to stop a task after starting it, it keeps running until the channel is destroyed—so explicitly call stop in your end-of-call flow rather than relying only on channel destruction.
