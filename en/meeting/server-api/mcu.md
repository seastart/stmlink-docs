---
title: "Meeting recording and live streaming"
description: "Cloud recording of the whole meeting, playback URLs, and the live stream pull URL; for more ways to pull and push, see \"Media output\""
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
  Layout type: auto (automatic), full (full screen), right_4 (small views on the right), top_4 (small views on top), br_7 (bottom L-shape), tl_7 (top L-shape), tb_8 (side-by-side), equal grids grids_N (N is 2, 3, 4, 5, 6, 8, 9, 12, 16, 20, 25), ring layouts ring_16 (large ring: 25-cell grid with the middle 9 cells merged) and ring_12 (small ring: 16-cell grid with the middle 4 cells merged)
  Example: `auto`
</ResponseField>

<ResponseField name="watermark_type" type="integer">
  Watermark type: 0 default, 1 none, 2 single row, 3 multiple rows
</ResponseField>

<ResponseField name="window_tag_type" type="string">
  Position of the user name label on each view, a letter or combination: L left, R right, T top, B bottom (such as LB for bottom left); empty means no label
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
    "layout": "auto",
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
  Layout type: auto (automatic), full (full screen), right_4 (small views on the right), top_4 (small views on top), br_7 (bottom L-shape), tl_7 (top L-shape), tb_8 (side-by-side), equal grids grids_N (N is 2, 3, 4, 5, 6, 8, 9, 12, 16, 20, 25), ring layouts ring_16 (large ring: 25-cell grid with the middle 9 cells merged) and ring_12 (small ring: 16-cell grid with the middle 4 cells merged)
  Example: `auto`
</ParamField>

<ParamField body="watermark_type" type="integer">
  Watermark type: 0 default, 1 none, 2 single row, 3 multiple rows
  Example: `1`
</ParamField>

<ParamField body="window_tag_type" type="string">
  Position of the user name label on each view, a letter or combination: L left, R right, T top, B bottom (such as LB for bottom left); empty means no label
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

## Get live stream URLs (legacy endpoint, served by stream/pull-url internally)

`POST /server/v1/mcu/live-url`

Authentication: required (see [Overview](/en/meeting/server-api/overview))

Get the live stream playback URL: returns the HTTP-FLV URL of the composite video (H264 video + AAC audio); rtmp and hls are discontinued and always empty.

Equivalent to Request a pull URL in "Media output" (protocol=flv, video=mcu); use that endpoint for new integrations: it also supports RTSP, single-user video, and any combination.

The live URL is available only while a stream mixing task is **in progress**, provided that task_type included the stream mixing bit (2) when the task was started; when no stream mixing task is in progress, success is returned with data null.

- The URL is signed and valid for 24 hours by default (adjustable with expire, up to one day); after expiry, new pull requests are rejected, while playback already in progress is not affected.
Just call this API to get a fresh URL before playback; don't cache it for long. The actual validity is given by the returned expire_at
- The audio source is selectable: mix for the meeting's mixed audio (default), none for no audio, or user for one audio track of a specific user (with audio_uid and audio_desc)
- The stream is subscribed only when someone pulls it, and unsubscribed automatically after the last puller disconnects; pulling stops when the task stops

**Request parameters**

<ParamField body="room_no" type="string">
  Room number
</ParamField>

<ParamField body="meeting_id" type="string">
  Meeting ID (required if room_no is not set)
</ParamField>

<ParamField body="audio" type="string">
  Audio source: mix is the mixed audio of the room (default; auto means the same), none means no audio, user is a specific user's audio (audio_uid is also required)
  Example: `mix`
</ParamField>

<ParamField body="audio_uid" type="string">
  Required when audio is user: whose audio to use (in-meeting user ID) (max length 64)
  Example: `1001`
</ParamField>

<ParamField body="audio_desc" type="string">
  Optional when audio is user: which of that user's audio tracks to use (exact match on the track description); defaults to the first one (max length 50)
  Example: `mic`
</ParamField>

<ParamField body="expire" type="integer">
  URL validity in seconds; defaults to 24 hours if omitted, up to one day
  Example: `86400`
</ParamField>


Request example:

```json
{
  "audio": "mix",
  "audio_desc": "mic",
  "audio_uid": "1001",
  "expire": 86400,
  "meeting_id": "",
  "room_no": ""
}
```

**Response parameters**

<ResponseField name="rtmp" type="string">
  Discontinued; always an empty string (kept so that existing callers don't fail to parse)
</ResponseField>

<ResponseField name="flv" type="string">
  HTTP-FLV playback URL (composite video in H264 + AAC audio); signed, and can be pulled repeatedly until it expires
  Example: `http://1.2.3.4:8080/f/eyJhcHBpZCI6....flv`
</ResponseField>

<ResponseField name="hls" type="string">
  Discontinued; always an empty string (kept so that existing callers don't fail to parse)
</ResponseField>

<ResponseField name="expire_at" type="integer">
  Expiry time of the flv URL, Unix timestamp in seconds; after expiry, new pull requests are rejected, while playback already in progress is not affected
  Example: `1718198266`
</ResponseField>


Response example:

```json
{
  "code": 0,
  "data": {
    "expire_at": 1718198266,
    "flv": "http://1.2.3.4:8080/f/eyJhcHBpZCI6....flv",
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

For live streaming, include the stream mixing bit (2) in the task, then use the "Media output" endpoints to get a pull URL or start a push (RTMP/RTMPS).

The live stream bit (8) has been merged into stream mixing (2) and is handled as stream mixing when passed:
- Composite-mode meetings (or meetings that have automatically started a stream mixing task): the meeting's composite video is reused as is and its layout isn't changed, so layout_data doesn't apply to this part; the other bits start their own tasks (for example, 9 starts only video recording 1), and 8 alone returns the task_id of the meeting's composite task directly
- Other meetings: a stream mixing task is started, and task_type in status callbacks is still the value you passed (8, 9, and so on)

**Request parameters**

<ParamField body="room_no" type="string">
  Room number
</ParamField>

<ParamField body="meeting_id" type="string">
  Meeting ID
</ParamField>

<ParamField body="task_type" type="integer" required>
  Task type, a bit mask: 1 video recording, 2 stream mixing, 4 audio recording; e.g. 3 = video recording + stream mixing. Live pulling and pushing use the mixed video, see "Media output" (8, the live stream, has been merged into 2 and is handled as 2 when passed; for composite-mode meetings, see the endpoint description)
  Example: `3`
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
    <ParamField body="layout" type="string">
      Layout type: auto (automatic), full (full screen), right_4 (small views on the right), top_4 (small views on top), br_7 (bottom L-shape), tl_7 (top L-shape), tb_8 (side-by-side), equal grids grids_N (N is 2, 3, 4, 5, 6, 8, 9, 12, 16, 20, 25), ring layouts ring_16 (large ring: 25-cell grid with the middle 9 cells merged) and ring_12 (small ring: 16-cell grid with the middle 4 cells merged). If omitted, the server's default layout is used (auto by default; the deployer can change it)
      Example: `auto`
    </ParamField>

    <ParamField body="watermark" type="object">
      Watermark
      <Expandable title="Fields">
        <ParamField body="type" type="integer">
          Type. 0: default, 1: none, 2: single row, 3: multiple rows
          Example: `1`
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
          Example: `L`
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
  "meeting_id": "",
  "op_name": "",
  "op_uid": "",
  "room_no": "",
  "tags": "",
  "task_type": 3,
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

Stop a recording task

When task_type includes the live stream bit (8), it's handled the same way as when starting: in a composite-mode meeting (or a meeting that has automatically started a stream mixing task), the meeting's composite video is not stopped and only the other bits are stopped (for example, 9 stops only video recording 1); 8 alone returns success directly.

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

