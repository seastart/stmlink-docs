---
title: "Meeting recording and live streaming"
description: "Cloud recording of the whole meeting, playback URLs, and live streaming"
---

{/* The API reference on this page is auto-generated from the backend source. Do not edit it by hand—changes are overwritten on the next sync.
    Edit the meeting-backend source instead; see the "对外接口文档（srvapi）" section of its README. */}

## Get recording settings

`POST /server/v1/mcu/record-config`

Authentication: required (see [Overview](/en/meeting/server-api/overview))

Global default recording settings

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
  Watermark type. 1: none, 2: single row, 3: multiple rows
</ResponseField>

<ResponseField name="window_tag_type" type="string">
  Window label position, a letter or combination: L left, R right, T top, B bottom; empty disables labels
</ResponseField>

<ResponseField name="created_at" type="integer">
  Settings creation time (timestamp)
</ResponseField>

<ResponseField name="updated_at" type="integer">
  Settings update time (timestamp)
</ResponseField>


Response example:

```json
{
  "code": 0,
  "data": {
    "app_id": "",
    "created_at": 0,
    "layout": "",
    "updated_at": 0,
    "watermark_type": 0,
    "window_tag_type": ""
  }
}
```

---

## Save recording settings

`POST /server/v1/mcu/save-record-config`

Authentication: required (see [Overview](/en/meeting/server-api/overview))

Update the global default recording settings

**Request parameters**

<ParamField body="layout" type="string">
  Layout type: auto, full, grids_2, grids_4, ...
</ParamField>

<ParamField body="watermark_type" type="integer">
  Watermark type. 1: none, 2: single row, 3: multiple rows
</ParamField>

<ParamField body="window_tag_type" type="string">
  Window label position, a letter or combination: L left, R right, T top, B bottom; empty disables labels
</ParamField>


Request example:

```json
{
  "layout": "",
  "watermark_type": 0,
  "window_tag_type": ""
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

Authentication: required (see [Overview](/en/meeting/server-api/overview))

List recording tasks. One recording = one task, and a task may contain multiple recording files
(a new segment starts when the segment duration is exceeded, and also when recording resumes after an interruption).

To get playable files, use "Get recording task details" (includes all files and URLs inline) or "List recording files".

**Request parameters**

<ParamField body="room_no" type="string">
  Room number; empty means any
</ParamField>

<ParamField body="meeting_id" type="string">
  Meeting ID; empty means any
</ParamField>

<ParamField body="task_status" type="integer">
  Task status; omit for any. 0: pending, 1: in progress, 2: stopping, 3: ended abnormally, 4: ended normally
</ParamField>

<ParamField body="title" type="string">
  Recording title, fuzzy match; empty means any (max length 100)
</ParamField>

<ParamField body="tag" type="string">
  Tag, fuzzy match; empty means any (max length 50)
</ParamField>

<ParamField body="begin_at" type="integer">
  Start time
</ParamField>

<ParamField body="end_at" type="integer">
  End time
</ParamField>

<ParamField body="page" type="integer">
  Page number, starting from 1
  Example: `1`
</ParamField>

<ParamField body="per-page" type="integer">
  Items per page
  Example: `10`
</ParamField>


Request example:

```json
{
  "begin_at": 0,
  "end_at": 0,
  "meeting_id": "",
  "page": 1,
  "per-page": 10,
  "room_no": "",
  "tag": "",
  "task_status": 0,
  "title": ""
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
  External room number
</ResponseField>

<ResponseField name="task_type" type="integer">
  Task type, a bit mask: 1 video recording, 2 stream mixing, 4 audio recording, 8 live stream
</ResponseField>

<ResponseField name="task_status" type="integer">
  0: pending, 1: in progress, 2: stopping, 3: ended abnormally, 4: ended normally
</ResponseField>

<ResponseField name="err_desc" type="string">
  Error description
</ResponseField>

<ResponseField name="began_at" type="integer">
  Recording start time (timestamp); 0 means the underlying task has not started running yet
</ResponseField>

<ResponseField name="ended_at" type="integer">
  Recording end time (timestamp); 0 means not ended
</ResponseField>

<ResponseField name="record_count" type="integer">
  Number of recording files; a recording produces extra files when it exceeds the segment duration or resumes after an interruption
</ResponseField>

<ResponseField name="total_duration" type="integer">
  Total duration of all recording files (seconds)
</ResponseField>

<ResponseField name="total_size" type="integer">
  Total size of all recording files (bytes)
</ResponseField>

<ResponseField name="tags" type="string">
  Recording tags, comma-separated
</ResponseField>

<ResponseField name="records" type="array<object>">
  Recording file list; returned only in task details
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
      Segment number, starting from 1; sorting by it gives the playback order
    </ResponseField>

    <ResponseField name="vod_size" type="integer">
      Recording size (bytes)
    </ResponseField>

    <ResponseField name="duration" type="integer">
      Segment duration (seconds)
    </ResponseField>

    <ResponseField name="began_at" type="integer">
      Segment start time (timestamp)
    </ResponseField>

    <ResponseField name="ended_at" type="integer">
      Segment end time (timestamp)
    </ResponseField>

    <ResponseField name="offset_ms" type="integer">
      Offset from the task start (ms), used for the progress bar in multi-segment playback
    </ResponseField>

    <ResponseField name="reason" type="integer">
      Segment reason. 0: unknown, 1: split by duration, 2: resumed after an interruption (gap after the previous segment)
    </ResponseField>

    <ResponseField name="addr" type="string">
      Presigned playback URL; returned only in task details
    </ResponseField>

    <ResponseField name="created_at" type="integer">
      Record creation time (timestamp)
    </ResponseField>

  </Expandable>
</ResponseField>

<ResponseField name="created_at" type="integer">
  Task creation time (timestamp)
</ResponseField>

<ResponseField name="updated_at" type="integer">
  Task update time (timestamp)
</ResponseField>

<ResponseField name="now" type="integer">
  Current time, used to calculate the recording duration when the frontend's local clock is inaccurate
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
      "began_at": 0,
      "channel": "",
      "created_at": 0,
      "ended_at": 0,
      "err_desc": "",
      "now": 0,
      "op_name": "",
      "op_uid": "",
      "record_count": 0,
      "records": [
        {
          "addr": "",
          "began_at": 0,
          "channel": "",
          "created_at": 0,
          "duration": 0,
          "ended_at": 0,
          "offset_ms": 0,
          "reason": 0,
          "record_id": "",
          "seq": 0,
          "task_id": "",
          "vod_size": 0
        }
      ],
      "room_no": "",
      "tags": "",
      "task_id": "",
      "task_status": 0,
      "task_type": 0,
      "title": "",
      "total_duration": 0,
      "total_size": 0,
      "updated_at": 0
    }
  ]
}
```

---

## Get recording task details

`POST /server/v1/mcu/detail`

Authentication: required (see [Overview](/en/meeting/server-api/overview))

Recording task details: task status, start and end times, total duration, and all recording files of this recording
(the records array, with each file's playback URL, duration, start and end times, and segment number).

**Request parameters**

<ParamField body="task_id" type="string">
  Task ID
</ParamField>

<ParamField body="meeting_id" type="string">
  Meeting ID (required if task_id is not set)
</ParamField>

<ParamField body="is_lan" type="boolean">
  Whether to return internal network playback URLs
</ParamField>


Request example:

```json
{
  "is_lan": false,
  "meeting_id": "",
  "task_id": ""
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
  External room number
</ResponseField>

<ResponseField name="task_type" type="integer">
  Task type, a bit mask: 1 video recording, 2 stream mixing, 4 audio recording, 8 live stream
</ResponseField>

<ResponseField name="task_status" type="integer">
  0: pending, 1: in progress, 2: stopping, 3: ended abnormally, 4: ended normally
</ResponseField>

<ResponseField name="err_desc" type="string">
  Error description
</ResponseField>

<ResponseField name="began_at" type="integer">
  Recording start time (timestamp); 0 means the underlying task has not started running yet
</ResponseField>

<ResponseField name="ended_at" type="integer">
  Recording end time (timestamp); 0 means not ended
</ResponseField>

<ResponseField name="record_count" type="integer">
  Number of recording files; a recording produces extra files when it exceeds the segment duration or resumes after an interruption
</ResponseField>

<ResponseField name="total_duration" type="integer">
  Total duration of all recording files (seconds)
</ResponseField>

<ResponseField name="total_size" type="integer">
  Total size of all recording files (bytes)
</ResponseField>

<ResponseField name="tags" type="string">
  Recording tags, comma-separated
</ResponseField>

<ResponseField name="records" type="array<object>">
  Recording file list; returned only in task details
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
      Segment number, starting from 1; sorting by it gives the playback order
    </ResponseField>

    <ResponseField name="vod_size" type="integer">
      Recording size (bytes)
    </ResponseField>

    <ResponseField name="duration" type="integer">
      Segment duration (seconds)
    </ResponseField>

    <ResponseField name="began_at" type="integer">
      Segment start time (timestamp)
    </ResponseField>

    <ResponseField name="ended_at" type="integer">
      Segment end time (timestamp)
    </ResponseField>

    <ResponseField name="offset_ms" type="integer">
      Offset from the task start (ms), used for the progress bar in multi-segment playback
    </ResponseField>

    <ResponseField name="reason" type="integer">
      Segment reason. 0: unknown, 1: split by duration, 2: resumed after an interruption (gap after the previous segment)
    </ResponseField>

    <ResponseField name="addr" type="string">
      Presigned playback URL; returned only in task details
    </ResponseField>

    <ResponseField name="created_at" type="integer">
      Record creation time (timestamp)
    </ResponseField>

  </Expandable>
</ResponseField>

<ResponseField name="created_at" type="integer">
  Task creation time (timestamp)
</ResponseField>

<ResponseField name="updated_at" type="integer">
  Task update time (timestamp)
</ResponseField>

<ResponseField name="now" type="integer">
  Current time, used to calculate the recording duration when the frontend's local clock is inaccurate
</ResponseField>


Response example:

```json
{
  "code": 0,
  "data": {
    "began_at": 0,
    "channel": "",
    "created_at": 0,
    "ended_at": 0,
    "err_desc": "",
    "now": 0,
    "op_name": "",
    "op_uid": "",
    "record_count": 0,
    "records": [
      {
        "addr": "",
        "began_at": 0,
        "channel": "",
        "created_at": 0,
        "duration": 0,
        "ended_at": 0,
        "offset_ms": 0,
        "reason": 0,
        "record_id": "",
        "seq": 0,
        "task_id": "",
        "vod_size": 0
      }
    ],
    "room_no": "",
    "tags": "",
    "task_id": "",
    "task_status": 0,
    "task_type": 0,
    "title": "",
    "total_duration": 0,
    "total_size": 0,
    "updated_at": 0
  }
}
```

---

## List recording files

`POST /server/v1/mcu/list-record`

Authentication: required (see [Overview](/en/meeting/server-api/overview))

List recording files. Each entry is one file (segment) produced by a recording.

Ascending seq is the playback order; offset_ms is the offset from the task start, used for the progress bar in multi-segment playback;
reason=2 means there is a time gap between this segment and the previous one (recording was interrupted and then resumed).

**Request parameters**

<ParamField body="task_id" type="string">
  Recording task ID; set it to see only the files of one recording. Empty means any
</ParamField>

<ParamField body="meeting_id" type="string">
  Meeting ID; empty means any
</ParamField>

<ParamField body="page" type="integer">
  Page number, starting from 1
  Example: `1`
</ParamField>

<ParamField body="per-page" type="integer">
  Items per page
  Example: `10`
</ParamField>


Request example:

```json
{
  "meeting_id": "",
  "page": 1,
  "per-page": 10,
  "task_id": ""
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
  Segment number, starting from 1; sorting by it gives the playback order
</ResponseField>

<ResponseField name="vod_size" type="integer">
  Recording size (bytes)
</ResponseField>

<ResponseField name="duration" type="integer">
  Segment duration (seconds)
</ResponseField>

<ResponseField name="began_at" type="integer">
  Segment start time (timestamp)
</ResponseField>

<ResponseField name="ended_at" type="integer">
  Segment end time (timestamp)
</ResponseField>

<ResponseField name="offset_ms" type="integer">
  Offset from the task start (ms), used for the progress bar in multi-segment playback
</ResponseField>

<ResponseField name="reason" type="integer">
  Segment reason. 0: unknown, 1: split by duration, 2: resumed after an interruption (gap after the previous segment)
</ResponseField>

<ResponseField name="addr" type="string">
  Presigned playback URL; returned only in task details
</ResponseField>

<ResponseField name="created_at" type="integer">
  Record creation time (timestamp)
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
      "began_at": 0,
      "channel": "",
      "created_at": 0,
      "duration": 0,
      "ended_at": 0,
      "offset_ms": 0,
      "reason": 0,
      "record_id": "",
      "seq": 0,
      "task_id": "",
      "vod_size": 0
    }
  ]
}
```

---

## Get the playback URL of a recording file

`POST /server/v1/mcu/vod-url`

Authentication: required (see [Overview](/en/meeting/server-api/overview))

Get the playback URL of a single recording file. The URL expires (after 2 hours), so do not cache it long-term

**Request parameters**

<ParamField body="record_id" type="string" required>
  Recording file ID, taken from the task details or the recording file list
</ParamField>

<ParamField body="is_lan" type="boolean">
  Whether to return LAN (internal network) URLs
</ParamField>


Request example:

```json
{
  "is_lan": false,
  "record_id": ""
}
```

**Response parameters**

<ResponseField name="url" type="string">
  Recording URL
</ResponseField>

<ResponseField name="size" type="integer">
  Recording size (bytes)
</ResponseField>

<ResponseField name="mcu_at" type="integer">
  Segment start time (compatibility field, same as began_at)
</ResponseField>

<ResponseField name="mcu_dur" type="integer">
  Segment duration (seconds) (compatibility field, same as duration)
</ResponseField>

<ResponseField name="record_id" type="string">
  Recording file ID, used to get the URL of or delete a single file
</ResponseField>

<ResponseField name="task_id" type="string">
  ID of the recording task it belongs to
</ResponseField>

<ResponseField name="seq" type="integer">
  Segment number, starting from 1; sorting by it gives the playback order
</ResponseField>

<ResponseField name="began_at" type="integer">
  Segment start time (timestamp)
</ResponseField>

<ResponseField name="ended_at" type="integer">
  Segment end time (timestamp)
</ResponseField>

<ResponseField name="duration" type="integer">
  Segment duration (seconds)
</ResponseField>

<ResponseField name="offset_ms" type="integer">
  Offset from the task start (ms), used for the progress bar in multi-segment playback
</ResponseField>

<ResponseField name="reason" type="integer">
  Segment reason. 0: unknown, 1: split by duration, 2: resumed after an interruption (gap after the previous segment)
</ResponseField>


Response example:

```json
{
  "code": 0,
  "data": {
    "began_at": 0,
    "duration": 0,
    "ended_at": 0,
    "mcu_at": 0,
    "mcu_dur": 0,
    "offset_ms": 0,
    "reason": 0,
    "record_id": "",
    "seq": 0,
    "size": 0,
    "task_id": "",
    "url": ""
  }
}
```

---

## Get playback URLs of multiple recording files

`POST /server/v1/mcu/vod-url/batch`

Authentication: required (see [Overview](/en/meeting/server-api/overview))

Get playback URLs of recording files in batch, up to 50 at a time; useful for fetching everything at once for continuous playback of a whole meeting

**Request parameters**

<ParamField body="record_ids" type="array<string>" required>
  Recording file ID list, up to 50 per request (max length 50)
</ParamField>

<ParamField body="is_lan" type="boolean">
  Whether to return LAN (internal network) URLs
</ParamField>


Request example:

```json
{
  "is_lan": false,
  "record_ids": [
    ""
  ]
}
```

**Response parameters**

<ResponseField name="url" type="string">
  Recording URL
</ResponseField>

<ResponseField name="size" type="integer">
  Recording size (bytes)
</ResponseField>

<ResponseField name="mcu_at" type="integer">
  Segment start time (compatibility field, same as began_at)
</ResponseField>

<ResponseField name="mcu_dur" type="integer">
  Segment duration (seconds) (compatibility field, same as duration)
</ResponseField>

<ResponseField name="record_id" type="string">
  Recording file ID, used to get the URL of or delete a single file
</ResponseField>

<ResponseField name="task_id" type="string">
  ID of the recording task it belongs to
</ResponseField>

<ResponseField name="seq" type="integer">
  Segment number, starting from 1; sorting by it gives the playback order
</ResponseField>

<ResponseField name="began_at" type="integer">
  Segment start time (timestamp)
</ResponseField>

<ResponseField name="ended_at" type="integer">
  Segment end time (timestamp)
</ResponseField>

<ResponseField name="duration" type="integer">
  Segment duration (seconds)
</ResponseField>

<ResponseField name="offset_ms" type="integer">
  Offset from the task start (ms), used for the progress bar in multi-segment playback
</ResponseField>

<ResponseField name="reason" type="integer">
  Segment reason. 0: unknown, 1: split by duration, 2: resumed after an interruption (gap after the previous segment)
</ResponseField>


Response example:

```json
{
  "code": 0,
  "data": [
    {
      "began_at": 0,
      "duration": 0,
      "ended_at": 0,
      "mcu_at": 0,
      "mcu_dur": 0,
      "offset_ms": 0,
      "reason": 0,
      "record_id": "",
      "seq": 0,
      "size": 0,
      "task_id": "",
      "url": ""
    }
  ]
}
```

---

## Get playback URLs of all recordings in a meeting

`POST /server/v1/mcu/vods-url`

Authentication: required (see [Overview](/en/meeting/server-api/overview))

Playback URLs of all recordings in a meeting. When a recording produces multiple files, all of them are returned, sorted by segment number.

url/size/mcu_at/mcu_dur are legacy fields with unchanged meaning (mcu_at is the segment start time, mcu_dur is the segment duration);
new fields such as record_id / seq / offset_ms are for locating a file precisely and for multi-segment playback.

**Request parameters**

<ParamField body="meeting_id" type="string">
  Meeting ID (required if room_no is not set)
</ParamField>

<ParamField body="room_no" type="string">
  Room number
</ParamField>

<ParamField body="is_lan" type="boolean">
  Whether to return LAN (internal network) URLs
</ParamField>


Request example:

```json
{
  "is_lan": false,
  "meeting_id": "",
  "room_no": ""
}
```

**Response parameters**

<ResponseField name="url" type="string">
  Recording URL
</ResponseField>

<ResponseField name="size" type="integer">
  Recording size (bytes)
</ResponseField>

<ResponseField name="mcu_at" type="integer">
  Segment start time (compatibility field, same as began_at)
</ResponseField>

<ResponseField name="mcu_dur" type="integer">
  Segment duration (seconds) (compatibility field, same as duration)
</ResponseField>

<ResponseField name="record_id" type="string">
  Recording file ID, used to get the URL of or delete a single file
</ResponseField>

<ResponseField name="task_id" type="string">
  ID of the recording task it belongs to
</ResponseField>

<ResponseField name="seq" type="integer">
  Segment number, starting from 1; sorting by it gives the playback order
</ResponseField>

<ResponseField name="began_at" type="integer">
  Segment start time (timestamp)
</ResponseField>

<ResponseField name="ended_at" type="integer">
  Segment end time (timestamp)
</ResponseField>

<ResponseField name="duration" type="integer">
  Segment duration (seconds)
</ResponseField>

<ResponseField name="offset_ms" type="integer">
  Offset from the task start (ms), used for the progress bar in multi-segment playback
</ResponseField>

<ResponseField name="reason" type="integer">
  Segment reason. 0: unknown, 1: split by duration, 2: resumed after an interruption (gap after the previous segment)
</ResponseField>


Response example:

```json
{
  "code": 0,
  "data": [
    {
      "began_at": 0,
      "duration": 0,
      "ended_at": 0,
      "mcu_at": 0,
      "mcu_dur": 0,
      "offset_ms": 0,
      "reason": 0,
      "record_id": "",
      "seq": 0,
      "size": 0,
      "task_id": "",
      "url": ""
    }
  ]
}
```

---

## Get live stream URLs

`POST /server/v1/mcu/live-url`

Authentication: required (see [Overview](/en/meeting/server-api/overview))

Get live stream URLs

**Request parameters**

<ParamField body="room_no" type="string">
  Room number
</ParamField>

<ParamField body="meeting_id" type="string">
  Meeting ID
</ParamField>


Request example:

```json
{
  "meeting_id": "",
  "room_no": ""
}
```

**Response parameters**

<ResponseField name="rtmp" type="string">
  RTMP playback URL
</ResponseField>

<ResponseField name="flv" type="string">
  HTTP-FLV playback URL
</ResponseField>

<ResponseField name="hls" type="string">
  HLS playback URL
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

## Delete a recording task

`POST /server/v1/mcu/del-task`

Authentication: required (see [Overview](/en/meeting/server-api/overview))

Delete a recording task together with all of its recording files

**Request parameters**

<ParamField body="task_id" type="string">
  Task ID
</ParamField>

<ParamField body="meeting_id" type="string">
  Meeting ID (required if task_id is not set)
</ParamField>

<ParamField body="is_lan" type="boolean">
  Whether to return internal network playback URLs
</ParamField>


Request example:

```json
{
  "is_lan": false,
  "meeting_id": "",
  "task_id": ""
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

Authentication: required (see [Overview](/en/meeting/server-api/overview))

Delete a single recording file; other files from the same recording are not affected

**Request parameters**

<ParamField body="record_id" type="string" required>
  Recording file ID
</ParamField>


Request example:

```json
{
  "record_id": ""
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

## Start or update a recording task

`POST /server/v1/mcu/start`

Authentication: required (see [Overview](/en/meeting/server-api/overview))

Start a recording task

**Request parameters**

<ParamField body="room_no" type="string">
  Room number
</ParamField>

<ParamField body="meeting_id" type="string">
  Meeting ID
</ParamField>

<ParamField body="task_type" type="integer" required>
  Task type, a bit mask: 1 video recording, 2 stream mixing, 4 audio recording, 8 live stream; e.g. 3 = video recording + stream mixing, 9 = video recording + live stream
  Example: `9`
</ParamField>

<ParamField body="title" type="string">
  Recording task title
</ParamField>

<ParamField body="op_uid" type="string">
  Task initiator ID
</ParamField>

<ParamField body="op_name" type="string">
  Task initiator name
</ParamField>

<ParamField body="tags" type="string">
  Recording tags, comma-separated
</ParamField>

<ParamField body="layout_data" type="object" required>
  Layout data
  <Expandable title="Fields">
    <ParamField body="layout" type="string" required>
      Layout type
    </ParamField>

    <ParamField body="watermark" type="object">
      Watermark
      <Expandable title="Fields">
        <ParamField body="type" type="integer">
          Type. 0: default, 1: none, 2: single row, 3: multiple rows
        </ParamField>

        <ParamField body="text" type="string">
          Custom text; empty means automatic (meeting title)
        </ParamField>

        <ParamField body="size" type="integer">
          Font size; 0 means the default
        </ParamField>

        <ParamField body="color" type="string">
          Font color; empty means the default
        </ParamField>

        <ParamField body="ol_color" type="string">
          Outline color; empty means the default
        </ParamField>

        <ParamField body="ol_width" type="integer">
          Outline width; 0 means the default
        </ParamField>

      </Expandable>
    </ParamField>

    <ParamField body="nobody_text" type="string">
      Text shown when no one is in the meeting; empty means recording stops when no one is present
    </ParamField>

    <ParamField body="tag" type="object">
      Default name label
      <Expandable title="Fields">
        <ParamField body="type" type="string">
          Type, a letter or combination: L left, R right, T top, B bottom
        </ParamField>

        <ParamField body="text" type="string">
          Custom text; empty means automatic (in-meeting display name)
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
      Logical block list
      <Expandable title="Element fields">
        <ParamField body="cells" type="array<object>">
          Grid cell list; empty means the remaining cells share the users here
        </ParamField>

        <ParamField body="uids" type="array<string>">
          User ID list. Empty: rotate through all remaining online users; multiple IDs: rotate among these users only
        </ParamField>

      </Expandable>
    </ParamField>

  </Expandable>
</ParamField>


Request example:

```json
{
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
              "type": ""
            }
          }
        ],
        "uids": [
          ""
        ]
      }
    ],
    "layout": "",
    "nobody_text": "",
    "polling_dur": 0,
    "tag": {
      "bg_color": "",
      "color": "",
      "size": 0,
      "text": "",
      "type": ""
    },
    "watermark": {
      "color": "",
      "ol_color": "",
      "ol_width": 0,
      "size": 0,
      "text": "",
      "type": 0
    }
  },
  "meeting_id": "",
  "op_name": "",
  "op_uid": "",
  "room_no": "",
  "tags": "",
  "task_type": 9,
  "title": ""
}
```

**Response parameters**

<ResponseField name="<key>" type="string">
  Keys are dynamic; see the description above
</ResponseField>


Response example:

```json
{
  "code": 0,
  "data": {}
}
```

---

## Stop a recording task

`POST /server/v1/mcu/stop`

Authentication: required (see [Overview](/en/meeting/server-api/overview))

**Request parameters**

<ParamField body="room_no" type="string">
  Room number
</ParamField>

<ParamField body="meeting_id" type="string">
  Meeting ID
</ParamField>

<ParamField body="task_type" type="integer">
  Task type (optional). If omitted, tasks of all types in the meeting are stopped; if set, only the given types are stopped. Values are the same as for the start endpoint
  Example: `1`
</ParamField>


Request example:

```json
{
  "meeting_id": "",
  "room_no": "",
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

