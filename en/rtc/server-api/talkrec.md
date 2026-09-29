---
title: "Per-speaker voice recording"
description: "Per-speaker voice recording by a server-side listener: split into segments by utterance, with segment-level query and playback; for mixed recording of the entire channel, see \"Cloud recording and live streaming\""
---

{/* The API reference on this page is auto-generated from the backend source. Do not edit it by hand—changes are overwritten on the next sync.
    Edit the rtc-backend source instead; see the "对外接口文档（srvapi）" section of its README. */}

## Start voice recording

`POST /server/v1/talkrec/start`

Authentication: required (see [Overview](/en/rtc/server-api/overview))

Start voice recording for a channel. The server joins the channel as an audience member and records passively, with a separate track per speaker and automatic segmentation based on media frames,
cutting the audio into "one utterance = one voice segment"; each segment is a separate file with the speaker and start/end times.

+ The channel must already be open; otherwise the "Channel is not open" error is returned
+ Only one voice recording runs per channel at a time: calling again returns the task_id of the existing task and doesn't join the channel a second time
+ No client changes needed: the server splits segments automatically by speech and silence, without relying on any state reported by the client

Starting is asynchronous: a successful response means only that the request was accepted; the task becomes in progress after the voice recording gateway joins the channel.
Watch task_status in "Get voice recording task details", or handle the `talkrec_task` event callback.

**Request parameters**

<ParamField body="channel" type="string" required>
  Channel (up to 64 bytes; letters, digits, underscores (_), and hyphens (-) only)
  Example: `fire`
</ParamField>

<ParamField body="title" type="string">
  Channel title, used only for lists and console display (max length 100)
  Example: `Line 3 repair intercom`
</ParamField>

<ParamField body="op_uid" type="string">
  Task initiator ID. A user ID from your own business, used only for lookup; not validated on the RTC side (max length 100)
  Example: `1001`
</ParamField>

<ParamField body="op_name" type="string">
  Task initiator name (max length 100)
  Example: `Alice`
</ParamField>


Request example:

```json
{
  "channel": "fire",
  "op_name": "Alice",
  "op_uid": "1001",
  "title": "Line 3 repair intercom"
}
```

**Response parameters**

<ResponseField name="task_id" type="string">
  ID of this voice recording task, used to stop the task, query details, and filter voice segments by task
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

## Stop voice recording

`POST /server/v1/talkrec/stop`

Authentication: required (see [Overview](/en/rtc/server-api/overview))

Stop voice recording. On stop, the server closes every unfinished utterance into a complete voice segment,
so the last few segments may appear in the voice segment list only after this call returns.

Voice segments already produced are not deleted and can still be queried and played.

**Request parameters**

<ParamField body="task_id" type="string">
  Task ID
  Example: `sxjgwy`
</ParamField>

<ParamField body="channel" type="string">
  Channel (required when TaskId is not set) (up to 64 bytes; letters, digits, underscores (_), and hyphens (-) only)
  Example: `fire`
</ParamField>


Request example:

```json
{
  "channel": "fire",
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

## Get voice recording task details

`POST /server/v1/talkrec/detail`

Authentication: required (see [Overview](/en/rtc/server-api/overview))

Query the details of a voice recording task: status, start and end times, and the number and total size of voice segments produced.

With task_id it queries by task; with only channel it returns the channel's unfinished voice recording first,
or the most recent one if all have ended; `data` is null if the channel has never had a voice recording.

Use task_status to see how far the task has progressed (0 pending, 1 in progress, 3 ended abnormally, 4 ended normally);
on failure, err_desc gives the reason.

**Request parameters**

<ParamField body="task_id" type="string">
  Task ID
  Example: `sxjgwy`
</ParamField>

<ParamField body="channel" type="string">
  Channel (required when TaskId is not set) (up to 64 bytes; letters, digits, underscores (_), and hyphens (-) only)
  Example: `fire`
</ParamField>


Request example:

```json
{
  "channel": "fire",
  "task_id": "sxjgwy"
}
```

**Response parameters**

<ResponseField name="task_id" type="string">
  Task ID
</ResponseField>

<ResponseField name="channel" type="string">
  Channel
  Example: `fire`
</ResponseField>

<ResponseField name="title" type="string">
  Channel title
</ResponseField>

<ResponseField name="op_uid" type="string">
  Task initiator ID
</ResponseField>

<ResponseField name="op_name" type="string">
  Task initiator name
</ResponseField>

<ResponseField name="task_status" type="integer">
  Task status: 0 pending, 1 in progress, 3 ended abnormally, 4 ended normally
</ResponseField>

<ResponseField name="err_desc" type="string">
  Error description
</ResponseField>

<ResponseField name="began_at" type="integer">
  Task start time, Unix timestamp in seconds
  Example: `1718194666`
</ResponseField>

<ResponseField name="ended_at" type="integer">
  Task end time, Unix timestamp in seconds; 0 means not ended
</ResponseField>

<ResponseField name="seg_count" type="integer">
  Number of voice segments produced
</ResponseField>

<ResponseField name="total_size" type="integer">
  Total bytes of voice segments
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
    "channel": "fire",
    "created_at": 1718194666,
    "ended_at": 0,
    "err_desc": "",
    "op_name": "",
    "op_uid": "",
    "seg_count": 0,
    "task_id": "",
    "task_status": 0,
    "title": "",
    "total_size": 0,
    "updated_at": 1718194705
  }
}
```

---

## List voice segments

`POST /server/v1/talkrec/list-record`

Authentication: required (see [Overview](/en/rtc/server-api/overview))

List voice segments with pagination; each item is one utterance.

In intercom scenarios a single segment is usually only a few seconds long, and one active channel can produce tens of thousands of segments a day.
**Always pass task_id or channel to narrow the scope**; don't page through everything without filters.

After getting the list, use "Batch get voice segment playback URLs" to fetch this page's playback URLs in one go,
which is much faster than fetching them one by one; keeping each page within 50 items matches the batch endpoint's limit exactly.

**Request parameters**

<ParamField body="task_id" type="string">
  Voice recording task ID; pass it to view only the segments of one voice recording; empty means no filter
  Example: `sxjgwy`
</ParamField>

<ParamField body="channel" type="string">
  Channel; empty means no filter (up to 64 bytes; letters, digits, underscores (_), and hyphens (-) only)
  Example: `fire`
</ParamField>

<ParamField body="uid" type="string">
  Speaker ID; empty means no filter (max length 100)
  Example: `1001`
</ParamField>

<ParamField body="begin_at" type="integer">
  Start time, Unix timestamp in seconds, filtered by utterance start time; 0 means no limit
  Example: `1718194666`
</ParamField>

<ParamField body="end_at" type="integer">
  End time, Unix timestamp in seconds; 0 means no limit
  Example: `1718799878`
</ParamField>

<ParamField body="search" type="array<string>">
  General search
</ParamField>

<ParamField body="sort" type="string">
  Sort order (sortable fields: began_at, duration_ms, vod_size)
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
  "search": [
    ""
  ],
  "sort": "",
  "task_id": "sxjgwy",
  "uid": "1001"
}
```

**Response parameters**

<ResponseField name="record_id" type="string">
  Voice segment ID, used to get the playback URL
</ResponseField>

<ResponseField name="task_id" type="string">
  ID of the voice recording task it belongs to
</ResponseField>

<ResponseField name="channel" type="string">
  Channel
  Example: `fire`
</ResponseField>

<ResponseField name="uid" type="string">
  Speaker ID
  Example: `1001`
</ResponseField>

<ResponseField name="name" type="string">
  Speaker's display name
  Example: `Alice`
</ResponseField>

<ResponseField name="vod_size" type="integer">
  Segment size (bytes)
</ResponseField>

<ResponseField name="duration_ms" type="integer">
  Segment duration (milliseconds)
  Example: `5200`
</ResponseField>

<ResponseField name="began_at" type="integer">
  Utterance start time, Unix timestamp in seconds
  Example: `1718194666`
</ResponseField>

<ResponseField name="ended_at" type="integer">
  Utterance end time, Unix timestamp in seconds
  Example: `1718194671`
</ResponseField>

<ResponseField name="codec" type="string">
  Audio codec
  Example: `opus`
</ResponseField>

<ResponseField name="sample_rate" type="integer">
  Sample rate
  Example: `48000`
</ResponseField>

<ResponseField name="end_reason" type="integer">
  Segment close reason: 0 unknown, 1 normal end (talk button released), 2 split on timeout, 3 user left, 4 task stopped, 5 idle timeout (fallback)
</ResponseField>

<ResponseField name="created_at" type="integer">
  Record creation time, Unix timestamp in seconds
  Example: `1718194672`
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
      "channel": "fire",
      "codec": "opus",
      "created_at": 1718194672,
      "duration_ms": 5200,
      "end_reason": 0,
      "ended_at": 1718194671,
      "name": "Alice",
      "record_id": "",
      "sample_rate": 48000,
      "task_id": "",
      "uid": "1001",
      "vod_size": 0
    }
  ]
}
```

---

## Get a voice segment's playback URL

`POST /server/v1/talkrec/vod-url`

Authentication: required (see [Overview](/en/rtc/server-api/overview))

Get the playback URL of a single voice segment; it can be played directly with `<audio>` (Opus/Ogg format).

The URL expires (2 hours). Don't cache it long term or store it in your database; get a new one before each playback.

**Request parameters**

<ParamField body="record_id" type="string" required>
  Voice segment ID, taken from the voice segment list
  Example: `sxjgwy`
</ParamField>

<ParamField body="is_lan" type="boolean">
  Whether to return internal network URLs, for purely internal deployments or dedicated-line access; public network URLs are returned by default
</ParamField>


Request example:

```json
{
  "is_lan": false,
  "record_id": "sxjgwy"
}
```

**Response parameters**

<ResponseField name="record_id" type="string">
  Voice segment ID
</ResponseField>

<ResponseField name="addr" type="string">
  Presigned playback URL, valid for 2 hours
</ResponseField>

<ResponseField name="vod_size" type="integer">
  Segment size (bytes)
</ResponseField>

<ResponseField name="duration_ms" type="integer">
  Segment duration (milliseconds)
</ResponseField>


Response example:

```json
{
  "code": 0,
  "data": {
    "addr": "",
    "duration_ms": 0,
    "record_id": "",
    "vod_size": 0
  }
}
```

---

## Batch get voice segment playback URLs

`POST /server/v1/talkrec/vod-url/batch`

Authentication: required (see [Overview](/en/rtc/server-api/overview))

Get voice segment playback URLs in bulk, so the voice segment list can fetch all URLs on the page at once. Up to 50 IDs per request.

Unlike the single-item endpoint, this one doesn't fail as a whole when one item can't be fetched—that item's
`addr` is an empty string (for example, the file has been cleaned up) and the rest are returned as usual.

**Request parameters**

<ParamField body="record_ids" type="array<string>" required>
  List of voice segment IDs, up to 50 per request (max length 50)
  Example: `["sxjgwy","sxjgwz"]`
</ParamField>

<ParamField body="is_lan" type="boolean">
  Whether to return internal network URLs, for purely internal deployments or dedicated-line access; public network URLs are returned by default
</ParamField>


Request example:

```json
{
  "is_lan": false,
  "record_ids": [
    "sxjgwy",
    "sxjgwz"
  ]
}
```

**Response parameters**

<ResponseField name="record_id" type="string">
  Voice segment ID
</ResponseField>

<ResponseField name="addr" type="string">
  Presigned playback URL, valid for 2 hours
</ResponseField>

<ResponseField name="vod_size" type="integer">
  Segment size (bytes)
</ResponseField>

<ResponseField name="duration_ms" type="integer">
  Segment duration (milliseconds)
</ResponseField>


Response example:

```json
{
  "code": 0,
  "data": [
    {
      "addr": "",
      "duration_ms": 0,
      "record_id": "",
      "vod_size": 0
    }
  ]
}
```

---

## Delete a voice segment

`POST /server/v1/talkrec/del-record`

Authentication: required (see [Overview](/en/rtc/server-api/overview))

Delete a voice segment. After deletion it no longer appears in the voice segment list and its playback URL can no longer be fetched.
The audio file itself is reclaimed asynchronously by a scheduled job on the server and doesn't affect this endpoint's response.

**Request parameters**

<ParamField body="record_id" type="string" required>
  Voice segment ID, taken from the voice segment list
  Example: `sxjgwy`
</ParamField>


Request example:

```json
{
  "record_id": "sxjgwy"
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

