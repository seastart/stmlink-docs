---
title: "Cloud recording and live streaming"
description: "Cloud recording of the entire channel, VOD URLs, and live streaming; per-speaker voice recording is a separate set of endpoints, see \"Per-speaker voice recording\""
---

{/* The API reference on this page is auto-generated from the backend source. Do not edit it by hand—changes are overwritten on the next sync.
    Edit the rtc-backend source instead; see the "对外接口文档（srvapi）" section of its README. */}

## Get the default recording configuration

`POST /server/v1/mcu/record-config`

Authentication: required (see [Overview](/en/rtc/server-api/overview))

Query the app's current default recording configuration (layout, watermark, and user name label position). No request parameters;
the configuration is per app and determined by the app identity from authentication.

When a task is started without layout_data, this configuration is used—put your standard watermark, labels, and layout strategy here,
so you don't have to pass them every time you start a task.

**Request parameters**

None

**Response parameters**

<ResponseField name="app_id" type="string">
  App ID
</ResponseField>

<ResponseField name="layout" type="string">
  Layout type: auto, full, grids_2, grids_4, ...
</ResponseField>

<ResponseField name="watermark_type" type="integer">
  Watermark type: 0 default, 1 none, 2 single row, 3 multiple rows
</ResponseField>

<ResponseField name="window_tag_type" type="string">
  Label position in each view, a letter or combination: L left, R right, T top, B bottom; empty disables labels
</ResponseField>

<ResponseField name="created_at" type="integer">
  Configuration creation time, Unix timestamp in seconds
  Example: `1718194666`
</ResponseField>

<ResponseField name="updated_at" type="integer">
  Configuration last-modified time, Unix timestamp in seconds
  Example: `1718194705`
</ResponseField>


Response example:

```json
{
  "code": 0,
  "data": {
    "app_id": "",
    "created_at": 1718194666,
    "layout": "",
    "updated_at": 1718194705,
    "watermark_type": 0,
    "window_tag_type": ""
  }
}
```

---

## Update the default recording configuration

`POST /server/v1/mcu/save-record-config`

Authentication: required (see [Overview](/en/rtc/server-api/overview))

Update the app's default recording configuration. All three fields are optional; pass only what you want to change.
Changes affect only new tasks started afterward; in-progress tasks are not affected.

**Request parameters**

<ParamField body="layout" type="string">
  Layout type: auto (automatic), full (full screen), right_4 (small views on the right), top_4 (small views on top), br_7 (bottom L-shape), tl_7 (top L-shape), tb_8 (side-by-side), plus equal grids grids_N (N is 2, 3, 4, 5, 6, 8, 9, 12, 16, 20, 25)
  Example: `auto`
</ParamField>

<ParamField body="watermark_type" type="integer">
  Watermark type: 0 default, 1 none, 2 single row, 3 multiple rows
  Example: `1`
</ParamField>

<ParamField body="window_tag_type" type="string">
  Position of the user name label on each view, a letter or combination: L left, R right, T top, B bottom (such as LB for bottom left); empty means no label (max length 2)
  Example: `L`
</ParamField>


Request example:

```json
{
  "layout": "auto",
  "watermark_type": 1,
  "window_tag_type": "L"
}
```

**Response parameters**

`data` is null

Response example:

```json
{
  "code": 0,
  "data": null
}
```

---

## List recording tasks

`POST /server/v1/mcu/list-task`

Authentication: required (see [Overview](/en/rtc/server-api/overview))

List recording tasks with pagination. One recording = one task, and a task may have multiple recording files
(it rolls over to a new segment when the segment duration is exceeded, and resuming after an interruption also starts a new segment).

This endpoint returns only the tasks themselves. To get playable files, use "Get recording task details" (which inlines all files and URLs)
or "List recording files". Use task_status to tell in-progress tasks from ended ones; record_count is the number of files produced.

**Request parameters**

<ParamField body="channel" type="string">
  Channel; empty means no filter (up to 64 bytes; letters, digits, underscores (_), and hyphens (-) only)
  Example: `fire`
</ParamField>

<ParamField body="room_no" type="string">
  External meeting number; empty means no filter (max length 50)
  Example: `818595664`
</ParamField>

<ParamField body="task_status" type="integer">
  Task status; omit for no filter: 0 pending, 1 in progress, 2 stopping, 3 ended abnormally, 4 ended normally
  Example: `4`
</ParamField>

<ParamField body="title" type="string">
  Recording title, fuzzy match; empty means no filter (max length 100)
  Example: `Weekly sync`
</ParamField>

<ParamField body="tag" type="string">
  Tag, fuzzy match; empty means no filter (max length 50)
  Example: `R&D`
</ParamField>

<ParamField body="begin_at" type="integer">
  Start time, Unix timestamp in seconds, filtered by task creation time; 0 means no limit
  Example: `1718194666`
</ParamField>

<ParamField body="end_at" type="integer">
  End time, Unix timestamp in seconds; 0 means no limit
  Example: `1718799878`
</ParamField>

<ParamField body="page" type="integer">
  Page number, starting from 1
  Example: `1`
</ParamField>

<ParamField body="per-page" type="integer">
  Page size
  Example: `10`
</ParamField>


Request example:

```json
{
  "begin_at": 1718194666,
  "channel": "fire",
  "end_at": 1718799878,
  "page": 1,
  "per-page": 10,
  "room_no": "818595664",
  "tag": "R&D",
  "task_status": 4,
  "title": "Weekly sync"
}
```

**Response parameters**

<ResponseField name="task_id" type="string">
  Task ID
</ResponseField>

<ResponseField name="op_uid" type="string">
  Task initiator ID
</ResponseField>

<ResponseField name="op_name" type="string">
  Task initiator name
</ResponseField>

<ResponseField name="channel" type="string">
  Channel
</ResponseField>

<ResponseField name="title" type="string">
  Channel title
</ResponseField>

<ResponseField name="room_no" type="string">
  External meeting number
</ResponseField>

<ResponseField name="task_type" type="integer">
  Task type: 1 video recording, 2 stream mixing, 4 audio recording, 8 live stream; combine as bit flags
</ResponseField>

<ResponseField name="task_status" type="integer">
  0 pending, 1 in progress, 2 stopping, 3 ended abnormally, 4 ended normally
</ResponseField>

<ResponseField name="err_desc" type="string">
  Error description
</ResponseField>

<ResponseField name="began_at" type="integer">
  Recording start time, Unix timestamp in seconds; 0 means the underlying task hasn't started running yet
  Example: `1718194666`
</ResponseField>

<ResponseField name="ended_at" type="integer">
  Recording end time, Unix timestamp in seconds; 0 means not ended
  Example: `1718216393`
</ResponseField>

<ResponseField name="record_count" type="integer">
  Number of recording files. A recording that exceeds the segment duration (1 hour by default) or is resumed after an interruption produces additional files
</ResponseField>

<ResponseField name="total_duration" type="integer">
  Total duration of all recording files (seconds)
  Example: `21727`
</ResponseField>

<ResponseField name="total_size" type="integer">
  Total bytes of all recording files
</ResponseField>

<ResponseField name="tags" type="string">
  Recording tags, comma-separated
</ResponseField>

<ResponseField name="records" type="array<object>">
  List of recording files, returned only by task details; null in the list endpoint
  <Expandable title="Element fields">
    <ResponseField name="record_id" type="string">
      Recording file ID, used to get the playback URL
    </ResponseField>

    <ResponseField name="task_id" type="string">
      ID of the recording task it belongs to
    </ResponseField>

    <ResponseField name="channel" type="string">
      Channel
    </ResponseField>

    <ResponseField name="seq" type="integer">
      Segment sequence number, starting from 1; sort by it to get the playback order
    </ResponseField>

    <ResponseField name="vod_size" type="integer">
      Recording size (bytes)
    </ResponseField>

    <ResponseField name="duration" type="integer">
      Segment duration (seconds)
      Example: `3600`
    </ResponseField>

    <ResponseField name="began_at" type="integer">
      Segment start time, Unix timestamp in seconds, used to align with your own timeline
      Example: `1718194666`
    </ResponseField>

    <ResponseField name="ended_at" type="integer">
      Segment end time, Unix timestamp in seconds
      Example: `1718198266`
    </ResponseField>

    <ResponseField name="offset_ms" type="integer">
      Offset from the task start (milliseconds); use this for the progress bar in multi-segment continuous playback
      Example: `7200000`
    </ResponseField>

    <ResponseField name="reason" type="integer">
      Segment reason: 0 unknown, 1 split by duration, 2 resumed after interruption (gap from the previous segment), 3 end of task
    </ResponseField>

    <ResponseField name="width" type="integer">
      Video width
      Example: `1280`
    </ResponseField>

    <ResponseField name="height" type="integer">
      Video height
      Example: `720`
    </ResponseField>

    <ResponseField name="fps" type="integer">
      Frame rate
      Example: `15`
    </ResponseField>

    <ResponseField name="codec" type="string">
      Video codec
      Example: `h264`
    </ResponseField>

    <ResponseField name="bitrate" type="integer">
      Bitrate (bps)
    </ResponseField>

    <ResponseField name="is_done" type="boolean">
      Whether the upload is complete. false means it is still recording or uploading, and no playback URL is available
    </ResponseField>

    <ResponseField name="addr" type="string">
      Presigned playback URL, valid for 2 hours; returned only by task details, empty in the list endpoint
    </ResponseField>

    <ResponseField name="created_at" type="integer">
      Record creation time, Unix timestamp in seconds
    </ResponseField>

  </Expandable>
</ResponseField>

<ResponseField name="created_at" type="integer">
  Task creation time, Unix timestamp in seconds
  Example: `1718194666`
</ResponseField>

<ResponseField name="updated_at" type="integer">
  Task last-modified time, Unix timestamp in seconds
  Example: `1718194705`
</ResponseField>


Response example:

```json
{
  "_meta": {
    "currentPage": 1,
    "pageCount": 5,
    "perPage": 20,
    "totalCount": 100
  },
  "code": 0,
  "data": [
    {
      "began_at": 1718194666,
      "channel": "",
      "created_at": 1718194666,
      "ended_at": 1718216393,
      "err_desc": "",
      "op_name": "",
      "op_uid": "",
      "record_count": 0,
      "records": [
        {
          "addr": "",
          "began_at": 1718194666,
          "bitrate": 0,
          "channel": "",
          "codec": "h264",
          "created_at": 0,
          "duration": 3600,
          "ended_at": 1718198266,
          "fps": 15,
          "height": 720,
          "is_done": false,
          "offset_ms": 7200000,
          "reason": 0,
          "record_id": "",
          "seq": 0,
          "task_id": "",
          "vod_size": 0,
          "width": 1280
        }
      ],
      "room_no": "",
      "tags": "",
      "task_id": "",
      "task_status": 0,
      "task_type": 0,
      "title": "",
      "total_duration": 21727,
      "total_size": 0,
      "updated_at": 1718194705
    }
  ]
}
```

---

## Get recording task details

`POST /server/v1/mcu/detail`

Authentication: required (see [Overview](/en/rtc/server-api/overview))

Query the details of a recording task: task type, status, start and end times, total duration, and **all recording files from this recording**
(the records array, with each file's playback URL, duration, start and end times, and segment sequence number).

One recording produces multiple files: it rolls over to a new segment when the segment duration (1 hour by default) is exceeded, and if recording is interrupted and then resumed,
that also starts a new segment. To play the entire recording, play the files in records in seq order.

With task_id it queries by task; with only channel it returns the channel's most recent recording.
Use task_status to see how far the task has progressed (0 pending, 1 in progress, 2 stopping, 3 ended abnormally, 4 ended normally).

**Request parameters**

<ParamField body="task_id" type="string">
  Task ID
  Example: `sxjgwy`
</ParamField>

<ParamField body="channel" type="string">
  Channel (required when TaskId is not set)
  Example: `fire`
</ParamField>

<ParamField body="is_lan" type="boolean">
  Whether to return internal network playback URLs, for purely internal deployments or dedicated-line access; public network URLs are returned by default
</ParamField>


Request example:

```json
{
  "channel": "fire",
  "is_lan": false,
  "task_id": "sxjgwy"
}
```

**Response parameters**

<ResponseField name="task_id" type="string">
  Task ID
</ResponseField>

<ResponseField name="op_uid" type="string">
  Task initiator ID
</ResponseField>

<ResponseField name="op_name" type="string">
  Task initiator name
</ResponseField>

<ResponseField name="channel" type="string">
  Channel
</ResponseField>

<ResponseField name="title" type="string">
  Channel title
</ResponseField>

<ResponseField name="room_no" type="string">
  External meeting number
</ResponseField>

<ResponseField name="task_type" type="integer">
  Task type: 1 video recording, 2 stream mixing, 4 audio recording, 8 live stream; combine as bit flags
</ResponseField>

<ResponseField name="task_status" type="integer">
  0 pending, 1 in progress, 2 stopping, 3 ended abnormally, 4 ended normally
</ResponseField>

<ResponseField name="err_desc" type="string">
  Error description
</ResponseField>

<ResponseField name="began_at" type="integer">
  Recording start time, Unix timestamp in seconds; 0 means the underlying task hasn't started running yet
  Example: `1718194666`
</ResponseField>

<ResponseField name="ended_at" type="integer">
  Recording end time, Unix timestamp in seconds; 0 means not ended
  Example: `1718216393`
</ResponseField>

<ResponseField name="record_count" type="integer">
  Number of recording files. A recording that exceeds the segment duration (1 hour by default) or is resumed after an interruption produces additional files
</ResponseField>

<ResponseField name="total_duration" type="integer">
  Total duration of all recording files (seconds)
  Example: `21727`
</ResponseField>

<ResponseField name="total_size" type="integer">
  Total bytes of all recording files
</ResponseField>

<ResponseField name="tags" type="string">
  Recording tags, comma-separated
</ResponseField>

<ResponseField name="records" type="array<object>">
  List of recording files, returned only by task details; null in the list endpoint
  <Expandable title="Element fields">
    <ResponseField name="record_id" type="string">
      Recording file ID, used to get the playback URL
    </ResponseField>

    <ResponseField name="task_id" type="string">
      ID of the recording task it belongs to
    </ResponseField>

    <ResponseField name="channel" type="string">
      Channel
    </ResponseField>

    <ResponseField name="seq" type="integer">
      Segment sequence number, starting from 1; sort by it to get the playback order
    </ResponseField>

    <ResponseField name="vod_size" type="integer">
      Recording size (bytes)
    </ResponseField>

    <ResponseField name="duration" type="integer">
      Segment duration (seconds)
      Example: `3600`
    </ResponseField>

    <ResponseField name="began_at" type="integer">
      Segment start time, Unix timestamp in seconds, used to align with your own timeline
      Example: `1718194666`
    </ResponseField>

    <ResponseField name="ended_at" type="integer">
      Segment end time, Unix timestamp in seconds
      Example: `1718198266`
    </ResponseField>

    <ResponseField name="offset_ms" type="integer">
      Offset from the task start (milliseconds); use this for the progress bar in multi-segment continuous playback
      Example: `7200000`
    </ResponseField>

    <ResponseField name="reason" type="integer">
      Segment reason: 0 unknown, 1 split by duration, 2 resumed after interruption (gap from the previous segment), 3 end of task
    </ResponseField>

    <ResponseField name="width" type="integer">
      Video width
      Example: `1280`
    </ResponseField>

    <ResponseField name="height" type="integer">
      Video height
      Example: `720`
    </ResponseField>

    <ResponseField name="fps" type="integer">
      Frame rate
      Example: `15`
    </ResponseField>

    <ResponseField name="codec" type="string">
      Video codec
      Example: `h264`
    </ResponseField>

    <ResponseField name="bitrate" type="integer">
      Bitrate (bps)
    </ResponseField>

    <ResponseField name="is_done" type="boolean">
      Whether the upload is complete. false means it is still recording or uploading, and no playback URL is available
    </ResponseField>

    <ResponseField name="addr" type="string">
      Presigned playback URL, valid for 2 hours; returned only by task details, empty in the list endpoint
    </ResponseField>

    <ResponseField name="created_at" type="integer">
      Record creation time, Unix timestamp in seconds
    </ResponseField>

  </Expandable>
</ResponseField>

<ResponseField name="created_at" type="integer">
  Task creation time, Unix timestamp in seconds
  Example: `1718194666`
</ResponseField>

<ResponseField name="updated_at" type="integer">
  Task last-modified time, Unix timestamp in seconds
  Example: `1718194705`
</ResponseField>


Response example:

```json
{
  "code": 0,
  "data": {
    "began_at": 1718194666,
    "channel": "",
    "created_at": 1718194666,
    "ended_at": 1718216393,
    "err_desc": "",
    "op_name": "",
    "op_uid": "",
    "record_count": 0,
    "records": [
      {
        "addr": "",
        "began_at": 1718194666,
        "bitrate": 0,
        "channel": "",
        "codec": "h264",
        "created_at": 0,
        "duration": 3600,
        "ended_at": 1718198266,
        "fps": 15,
        "height": 720,
        "is_done": false,
        "offset_ms": 7200000,
        "reason": 0,
        "record_id": "",
        "seq": 0,
        "task_id": "",
        "vod_size": 0,
        "width": 1280
      }
    ],
    "room_no": "",
    "tags": "",
    "task_id": "",
    "task_status": 0,
    "task_type": 0,
    "title": "",
    "total_duration": 21727,
    "total_size": 0,
    "updated_at": 1718194705
  }
}
```

---

## List recording files

`POST /server/v1/mcu/list-record`

Authentication: required (see [Overview](/en/rtc/server-api/overview))

List recording files with pagination; each item is one file (segment) produced by a recording.

Ascending seq is the playback order; offset_ms is the offset from the task start, used for the progress bar in multi-segment continuous playback.
reason=2 means there is a time gap between this segment and the previous one (recording was interrupted and resumed); watch for it in continuous playback.

After getting the list, use "Batch get recording file playback URLs" to fetch this page's URLs in one go, which is much faster than fetching them one by one.

**Request parameters**

<ParamField body="task_id" type="string">
  Recording task ID; pass it to view only the files of one recording; empty means no filter
  Example: `sxjgwy`
</ParamField>

<ParamField body="channel" type="string">
  Channel; empty means no filter (up to 64 bytes; letters, digits, underscores (_), and hyphens (-) only)
  Example: `fire`
</ParamField>

<ParamField body="page" type="integer">
  Page number, starting from 1
  Example: `1`
</ParamField>

<ParamField body="per-page" type="integer">
  Page size
  Example: `10`
</ParamField>


Request example:

```json
{
  "channel": "fire",
  "page": 1,
  "per-page": 10,
  "task_id": "sxjgwy"
}
```

**Response parameters**

<ResponseField name="record_id" type="string">
  Recording file ID, used to get the playback URL
</ResponseField>

<ResponseField name="task_id" type="string">
  ID of the recording task it belongs to
</ResponseField>

<ResponseField name="channel" type="string">
  Channel
</ResponseField>

<ResponseField name="seq" type="integer">
  Segment sequence number, starting from 1; sort by it to get the playback order
</ResponseField>

<ResponseField name="vod_size" type="integer">
  Recording size (bytes)
</ResponseField>

<ResponseField name="duration" type="integer">
  Segment duration (seconds)
  Example: `3600`
</ResponseField>

<ResponseField name="began_at" type="integer">
  Segment start time, Unix timestamp in seconds, used to align with your own timeline
  Example: `1718194666`
</ResponseField>

<ResponseField name="ended_at" type="integer">
  Segment end time, Unix timestamp in seconds
  Example: `1718198266`
</ResponseField>

<ResponseField name="offset_ms" type="integer">
  Offset from the task start (milliseconds); use this for the progress bar in multi-segment continuous playback
  Example: `7200000`
</ResponseField>

<ResponseField name="reason" type="integer">
  Segment reason: 0 unknown, 1 split by duration, 2 resumed after interruption (gap from the previous segment), 3 end of task
</ResponseField>

<ResponseField name="width" type="integer">
  Video width
  Example: `1280`
</ResponseField>

<ResponseField name="height" type="integer">
  Video height
  Example: `720`
</ResponseField>

<ResponseField name="fps" type="integer">
  Frame rate
  Example: `15`
</ResponseField>

<ResponseField name="codec" type="string">
  Video codec
  Example: `h264`
</ResponseField>

<ResponseField name="bitrate" type="integer">
  Bitrate (bps)
</ResponseField>

<ResponseField name="is_done" type="boolean">
  Whether the upload is complete. false means it is still recording or uploading, and no playback URL is available
</ResponseField>

<ResponseField name="addr" type="string">
  Presigned playback URL, valid for 2 hours; returned only by task details, empty in the list endpoint
</ResponseField>

<ResponseField name="created_at" type="integer">
  Record creation time, Unix timestamp in seconds
</ResponseField>


Response example:

```json
{
  "_meta": {
    "currentPage": 1,
    "pageCount": 5,
    "perPage": 20,
    "totalCount": 100
  },
  "code": 0,
  "data": [
    {
      "addr": "",
      "began_at": 1718194666,
      "bitrate": 0,
      "channel": "",
      "codec": "h264",
      "created_at": 0,
      "duration": 3600,
      "ended_at": 1718198266,
      "fps": 15,
      "height": 720,
      "is_done": false,
      "offset_ms": 7200000,
      "reason": 0,
      "record_id": "",
      "seq": 0,
      "task_id": "",
      "vod_size": 0,
      "width": 1280
    }
  ]
}
```

---

## Get a recording file's playback URL

`POST /server/v1/mcu/vod-url`

Authentication: required (see [Overview](/en/rtc/server-api/overview))

Get the playback URL of a single recording file. The file must have finished uploading; no URL is available while it is recording or uploading.
The URL expires (2 hours). Don't cache it long term or store it in your database; get a new one before each playback.

**Request parameters**

<ParamField body="record_id" type="string" required>
  Recording file ID, taken from the task details or the recording file list
  Example: `rc3p9w`
</ParamField>

<ParamField body="is_lan" type="boolean">
  Whether to return internal network URLs, for purely internal deployments or dedicated-line access; public network URLs are returned by default
</ParamField>


Request example:

```json
{
  "is_lan": false,
  "record_id": "rc3p9w"
}
```

**Response parameters**

<ResponseField name="record_id" type="string">
  Recording file ID
</ResponseField>

<ResponseField name="addr" type="string">
  Presigned playback URL, valid for 2 hours
</ResponseField>

<ResponseField name="size" type="integer">
  Recording size (bytes)
</ResponseField>

<ResponseField name="duration" type="integer">
  Segment duration (seconds)
</ResponseField>

<ResponseField name="began_at" type="integer">
  Segment start time, Unix timestamp in seconds
</ResponseField>

<ResponseField name="offset_ms" type="integer">
  Offset from the task start (milliseconds)
</ResponseField>


Response example:

```json
{
  "code": 0,
  "data": {
    "addr": "",
    "began_at": 0,
    "duration": 0,
    "offset_ms": 0,
    "record_id": "",
    "size": 0
  }
}
```

---

## Batch get recording file playback URLs

`POST /server/v1/mcu/vod-url/batch`

Authentication: required (see [Overview](/en/rtc/server-api/overview))

Get playback URLs for recording files in bulk, up to 50 at a time; suited to fetching everything at once for continuous playback of an entire recording.

If issuing a URL fails for a single file (for example, it has been cleaned up), that item's addr is empty; other items are not affected.

**Request parameters**

<ParamField body="record_ids" type="array<string>" required>
  List of recording file IDs, up to 50 per request (max length 50)
  Example: `["rc3p9w","rc3p9x"]`
</ParamField>

<ParamField body="is_lan" type="boolean">
  Whether to return internal network URLs, for purely internal deployments or dedicated-line access; public network URLs are returned by default
</ParamField>


Request example:

```json
{
  "is_lan": false,
  "record_ids": [
    "rc3p9w",
    "rc3p9x"
  ]
}
```

**Response parameters**

<ResponseField name="record_id" type="string">
  Recording file ID
</ResponseField>

<ResponseField name="addr" type="string">
  Presigned playback URL, valid for 2 hours
</ResponseField>

<ResponseField name="size" type="integer">
  Recording size (bytes)
</ResponseField>

<ResponseField name="duration" type="integer">
  Segment duration (seconds)
</ResponseField>

<ResponseField name="began_at" type="integer">
  Segment start time, Unix timestamp in seconds
</ResponseField>

<ResponseField name="offset_ms" type="integer">
  Offset from the task start (milliseconds)
</ResponseField>


Response example:

```json
{
  "code": 0,
  "data": [
    {
      "addr": "",
      "began_at": 0,
      "duration": 0,
      "offset_ms": 0,
      "record_id": "",
      "size": 0
    }
  ]
}
```

---

## Delete a recording task

`POST /server/v1/mcu/del-task`

Authentication: required (see [Overview](/en/rtc/server-api/overview))

Delete a recording task together with all its recording files. After deletion it no longer appears in the list or details.

If you pass only channel without task_id, **all** tasks with video recording in that channel are deleted together.
To delete one specific recording, pass task_id.

**Request parameters**

<ParamField body="task_id" type="string">
  Task ID
  Example: `sxjgwy`
</ParamField>

<ParamField body="channel" type="string">
  Channel (required when TaskId is not set)
  Example: `fire`
</ParamField>

<ParamField body="is_lan" type="boolean">
  Whether to return internal network playback URLs, for purely internal deployments or dedicated-line access; public network URLs are returned by default
</ParamField>


Request example:

```json
{
  "channel": "fire",
  "is_lan": false,
  "task_id": "sxjgwy"
}
```

**Response parameters**

`data` is null

Response example:

```json
{
  "code": 0,
  "data": null
}
```

---

## Delete a recording file

`POST /server/v1/mcu/del-record`

Authentication: required (see [Overview](/en/rtc/server-api/overview))

Delete a single recording file; other files from the same recording are not affected.

**Request parameters**

<ParamField body="record_id" type="string" required>
  Recording file ID
  Example: `rc3p9w`
</ParamField>


Request example:

```json
{
  "record_id": "rc3p9w"
}
```

**Response parameters**

`data` is null

Response example:

```json
{
  "code": 0,
  "data": null
}
```

---

## Start a recording or live streaming task

`POST /server/v1/mcu/start`

Authentication: required (see [Overview](/en/rtc/server-api/overview))

Start a server-side recording, stream mixing, or live streaming task. A channel has only one in-progress task per type:
calling again doesn't create a new task but updates the existing one with the parameters passed in.

**Request parameters**

<ParamField body="task_type" type="integer" required>
  Task type as bit flags: 1 video recording, 2 stream mixing, 4 audio recording, 8 live stream; for example, 3 means video recording + stream mixing, 9 means video recording + live stream
  Example: `9`
</ParamField>

<ParamField body="op_uid" type="string">
  Task initiator ID
  Example: `1001`
</ParamField>

<ParamField body="op_name" type="string">
  Task initiator name (max length 100)
  Example: `Alice`
</ParamField>

<ParamField body="channel" type="string" required>
  Channel (up to 64 bytes; letters, digits, underscores (_), and hyphens (-) only)
  Example: `fire`
</ParamField>

<ParamField body="title" type="string" required>
  Channel title. Becomes the recording title and is also the default watermark content (when watermark.text is empty)
  Example: `Weekly project sync 2024-06-12`
</ParamField>

<ParamField body="room_no" type="string">
  External meeting number. A meeting number from your own business, used only for lookup; not validated on the RTC side (max length 50)
  Example: `818595664`
</ParamField>

<ParamField body="tags" type="string">
  Recording tags, comma-separated (note: in "Update a recording task's title and tags", tags is an array)
  Example: `Weekly sync,R&D`
</ParamField>

<ParamField body="layout_data" type="object">
  Layout data. If omitted, the app's default recording configuration is used (see "Get the default recording configuration")
  <Expandable title="Fields">
    <ParamField body="layout" type="string" required>
      Layout type: auto (automatic), full (full screen), right_4 (small views on the right), top_4 (small views on top), br_7 (bottom L-shape), tl_7 (top L-shape), tb_8 (side-by-side), plus equal grids grids_N (N is 2, 3, 4, 5, 6, 8, 9, 12, 16, 20, 25)
      Example: `auto`
    </ParamField>

    <ParamField body="watermark" type="object">
      Watermark
      <Expandable title="Fields">
        <ParamField body="type" type="integer">
          Type: 0 default, 1 none, 2 single row, 3 multiple rows
          Example: `1`
        </ParamField>

        <ParamField body="text" type="string">
          Custom text; empty means automatic (channel title)
        </ParamField>

        <ParamField body="size" type="integer">
          Font size; 0 means the default value
        </ParamField>

        <ParamField body="color" type="string">
          Font color; empty means the default value
        </ParamField>

        <ParamField body="ol_color" type="string">
          Outline color; empty means the default value
        </ParamField>

        <ParamField body="ol_width" type="integer">
          Outline width; 0 means the default value
        </ParamField>

      </Expandable>
    </ParamField>

    <ParamField body="nobody_text" type="string">
      Text shown when no one is in the channel; empty means recording stops when no one is in the channel
    </ParamField>

    <ParamField body="tag" type="object">
      Default name label
      <Expandable title="Fields">
        <ParamField body="type" type="string">
          Type, a letter or combination: L left, R right, T top, B bottom
          Example: `L`
        </ParamField>

        <ParamField body="text" type="string">
          Custom text; empty means automatic (display name)
        </ParamField>

        <ParamField body="size" type="integer">
          Font size; 0 means default
        </ParamField>

        <ParamField body="color" type="string">
          Font color; empty means default
        </ParamField>

        <ParamField body="bg_color" type="string">
          Background color; empty means default
        </ParamField>

      </Expandable>
    </ParamField>

    <ParamField body="polling_dur" type="integer">
      Rotation interval (seconds); 0 disables rotation
    </ParamField>

    <ParamField body="div_list" type="array<object>">
      List of logical blocks
      <Expandable title="Element fields">
        <ParamField body="cells" type="array<object>">
          List of grid cells; empty means the remaining cells share the users here
        </ParamField>

        <ParamField body="uids" type="array<string>">
          List of user IDs; empty means rotating through all remaining online users, multiple means rotating among these users
        </ParamField>

      </Expandable>
    </ParamField>

    <ParamField body="names" type="object">
      User name table, corresponding to McuDiv.Uids (optional)
    </ParamField>

  </Expandable>
</ParamField>


Request example:

```json
{
  "channel": "fire",
  "layout_data": {
    "div_list": [
      {
        "cells": [
          {
            "bind_share": false,
            "idx": 0,
            "tag": {
              "bg_color": "",
              "color": "",
              "size": 0,
              "text": "",
              "type": "L"
            }
          }
        ],
        "uids": [
          ""
        ]
      }
    ],
    "layout": "auto",
    "names": {},
    "nobody_text": "",
    "polling_dur": 0,
    "tag": {
      "bg_color": "",
      "color": "",
      "size": 0,
      "text": "",
      "type": "L"
    },
    "watermark": {
      "color": "",
      "ol_color": "",
      "ol_width": 0,
      "size": 0,
      "text": "",
      "type": 1
    }
  },
  "op_name": "Alice",
  "op_uid": "1001",
  "room_no": "818595664",
  "tags": "Weekly sync,R&D",
  "task_type": 9,
  "title": "Weekly project sync 2024-06-12"
}
```

**Response parameters**

<ResponseField name="task_id" type="string">
  ID of this task, used to stop the task, query details, and get playback URLs
</ResponseField>


Response example:

```json
{
  "code": 0,
  "data": {
    "task_id": ""
  }
}
```

---

## Stop a recording or live streaming task

`POST /server/v1/mcu/stop`

Authentication: required (see [Overview](/en/rtc/server-api/overview))

Stop an in-progress recording, stream mixing, or live streaming task. Recording files are transcoded only after the task stops; playback URLs become available after that.
In-progress tasks stop automatically when the channel is destroyed, so you don't need to stop them manually first.

**Request parameters**

<ParamField body="task_id" type="string">
  Task ID
  Example: `sxjgwy`
</ParamField>

<ParamField body="channel" type="string">
  Channel (required when TaskId is not set)
  Example: `fire`
</ParamField>

<ParamField body="task_type" type="integer">
  Task type (optional). Omit to stop tasks of all types in the channel; if set, only the specified types are stopped. Values are the same as for the start endpoint
  Example: `1`
</ParamField>


Request example:

```json
{
  "channel": "fire",
  "task_id": "sxjgwy",
  "task_type": 1
}
```

**Response parameters**

`data` is null

Response example:

```json
{
  "code": 0,
  "data": null
}
```

---

## Update a recording task's title and tags

`POST /server/v1/mcu/update-task`

Authentication: required (see [Overview](/en/rtc/server-api/overview))

Update a recording task's title and tags for archiving and organization; the recording files themselves are not affected.
Both the title and tags can be matched by search in the recording task list.

**Request parameters**

<ParamField body="task_id" type="string" required>
  Task ID
  Example: `sxjgwy`
</ParamField>

<ParamField body="title" type="string">
  Recording title; omit to leave unchanged (max length 100)
  Example: `Weekly project sync (archived)`
</ParamField>

<ParamField body="tags" type="array<string>">
  Tags, up to 10. They are replaced as a whole, not appended—include any tags you want to keep (max length 10)
  Example: `["Weekly sync","R&D"]`
</ParamField>


Request example:

```json
{
  "tags": [
    "Weekly sync",
    "R&D"
  ],
  "task_id": "sxjgwy",
  "title": "Weekly project sync (archived)"
}
```

**Response parameters**

`data` is null

Response example:

```json
{
  "code": 0,
  "data": null
}
```

---

## Get live stream playback URLs

`POST /server/v1/mcu/live-url`

Authentication: required (see [Overview](/en/rtc/server-api/overview))

Get live stream playback URLs; returns rtmp / flv / hls URLs at once, so you can choose one for your player.

Unlike recording playback, live stream URLs are available while the task is **in progress**—provided that
task_type included the live streaming bit (8) when the task was started. The URLs expire; don't cache them long term.

**Request parameters**

<ParamField body="task_id" type="string">
  Task ID
  Example: `sxjgwy`
</ParamField>

<ParamField body="channel" type="string">
  Channel (required when TaskId is not set)
  Example: `fire`
</ParamField>

<ParamField body="is_lan" type="boolean">
  Whether to return internal network playback URLs, for purely internal deployments or dedicated-line access; public network URLs are returned by default
</ParamField>


Request example:

```json
{
  "channel": "fire",
  "is_lan": false,
  "task_id": "sxjgwy"
}
```

**Response parameters**

<ResponseField name="rtmp" type="string">
  RTMP playback URL; lowest latency, suited to players that need low latency
</ResponseField>

<ResponseField name="flv" type="string">
  HTTP-FLV playback URL, commonly used on the Web
</ResponseField>

<ResponseField name="hls" type="string">
  HLS (m3u8) playback URL; best compatibility, relatively higher latency
</ResponseField>


Response example:

```json
{
  "code": 0,
  "data": {
    "flv": "",
    "hls": "",
    "rtmp": ""
  }
}
```

---

