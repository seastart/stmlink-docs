---
title: "Media output"
description: "Pull URLs (HTTP-FLV / RTSP) and push tasks (RTMP / RTMPS): video from the composite video or any one user, audio from the channel's mixed audio or any one user, in any combination"
---

{/* The API reference on this page is auto-generated from the backend source. Do not edit it by hand—changes are overwritten on the next sync.
    Edit the rtc-backend source instead; see the "对外接口文档（srvapi）" section of its README. */}

## Request a pull URL

`POST /server/v1/stream/pull-url`

Authentication: required (see [Overview](/en/rtc/server-api/overview))

Requests a pull URL (HTTP-FLV or RTSP) for audio and video in a channel. Video and audio each choose their own source:
video is the channel's composite video, one of a user's video tracks, or none; audio is the channel's mixed audio, one of a user's audio tracks, or none, following the video by default.
For example, "presenter's video + channel mixed audio" is video=user, video_uid=presenter, audio=mix.

- When the composite video or the channel's mixed audio is used, the channel must have a stream mixing task in progress (task_type of mcu/start includes 2); otherwise error code 1073 is returned
- flv: video must be H264 (no transcoding; if the publisher uses VP8, no video can be pulled, so have the publisher use H264); audio is transcoded to AAC
- rtsp: only RTSP over TCP is supported (the player must use TCP, for example ffplay with `-rtsp_transport tcp`); video is passed through as is (H264 or VP8),
audio is transcoded to AAC by default; pass rtsp_audio=opus to pass Opus through as is and skip server-side transcoding
- The URL is signed and can be pulled repeatedly by multiple players until it expires; after expiry, new pull requests are rejected, while playback already in progress is not affected
- Sources are subscribed only when someone pulls and unsubscribed automatically after the last player disconnects, so nothing is consumed when no one is pulling; there is no stop endpoint to call
- The channel being open and the user being online are not checked, so URLs can be generated in advance; if the source hasn't published yet when pulling, the player gets a 404 and should retry
- If the user leaves and comes back, the pull doesn't break; there is just a gap in between

The actual validity period is the returned expire_at (the server-side limit may be shorter than the requested value).

**Request parameters**

<ParamField body="channel" type="string" required>
  Channel (up to 64 bytes; letters, digits, underscores (_), and hyphens (-) only)
  Example: `fire`
</ParamField>

<ParamField body="protocol" type="string" required>
  Pull protocol: flv (HTTP-FLV), rtsp (RTSP over TCP)
  Example: `flv`
</ParamField>

<ParamField body="video" type="string" required>
  Video source: mcu is the channel's composite video (the channel must have a stream mixing task in progress), user is a specific user's video (with video_uid), none means no video
  Example: `mcu`
</ParamField>

<ParamField body="video_uid" type="string">
  Required when video is user: which user's video to use (letters, digits, underscores (_), and hyphens (-) only)
  Example: `1001`
</ParamField>

<ParamField body="video_desc" type="string">
  Optional when video is user: when the user publishes multiple video tracks at once (such as camera and screen sharing), specifies one of them (exact match on the track description); if omitted, the first one to arrive is used (max length 50)
  Example: `camera`
</ParamField>

<ParamField body="audio" type="string">
  Audio source: auto follows the video (default; the composite video comes with the channel's mixed audio, a single user's video with that user's own audio; auto can't be used without video), mix is the channel's mixed audio (the channel must have a stream mixing task in progress), user is a specific user's audio (with audio_uid), none means no audio. Video and audio can't both be none
  Example: `auto`
</ParamField>

<ParamField body="audio_uid" type="string">
  Required when audio is user: which user's audio to use (letters, digits, underscores (_), and hyphens (-) only)
  Example: `1002`
</ParamField>

<ParamField body="audio_desc" type="string">
  When the user publishes multiple audio tracks, specifies one of them (exact match on the track description); if omitted, the first one is used. Effective when audio is user, or auto following a single user's video (max length 50)
  Example: `mic`
</ParamField>

<ParamField body="expire" type="integer">
  URL validity in seconds; defaults to 24 hours if omitted, up to one day
  Example: `86400`
</ParamField>

<ParamField body="rtsp_audio" type="string">
  Audio codec for RTSP, effective only when protocol is rtsp: aac (default, compatible with NVRs and surveillance platforms), opus (passed through as is, no server-side transcoding)
  Example: `aac`
</ParamField>


Request example:

```json
{
  "audio": "auto",
  "audio_desc": "mic",
  "audio_uid": "1002",
  "channel": "fire",
  "expire": 86400,
  "protocol": "flv",
  "rtsp_audio": "aac",
  "video": "mcu",
  "video_desc": "camera",
  "video_uid": "1001"
}
```

**Response parameters**

<ResponseField name="url" type="string">
  Pull URL; signed, and can be pulled repeatedly by multiple players until it expires
  Example: `http://1.2.3.4:8080/f/eyJhcHBpZCI6....flv`
</ResponseField>

<ResponseField name="expire_at" type="integer">
  URL expiry time, Unix timestamp in seconds; after expiry, new pull requests are rejected, while playback already in progress is not affected
  Example: `1718198266`
</ResponseField>


Response example:

```json
{
  "code": 0,
  "data": {
    "expire_at": 1718198266,
    "url": "http://1.2.3.4:8080/f/eyJhcHBpZCI6....flv"
  }
}
```

---

## Start a push

`POST /server/v1/stream/push/start`

Authentication: required (see [Overview](/en/rtc/server-api/overview))

Start a push: pushes the selected video and audio in the channel to your RTMP live room (rtmp:// and rtmps:// are supported) and returns a push_id.
The source parameters are the same as for requesting a pull URL, and a channel can have multiple pushes at once (for example, the composite video to one platform and a guest's own video to another).

+ The channel must already be open; when the channel is destroyed, all of its pushes stop automatically
+ Calling again for the same push URL in the same channel doesn't start another push: if the sources are unchanged, the existing push_id is returned; if they changed, this push is updated to the new sources
+ While a source doesn't exist yet (for example, the stream mixing task hasn't started, or the user to push hasn't published), the push stays in waiting; this is not a failure, and pushing starts automatically once the source appears
+ Pushes reconnect automatically after a disconnection; persistent failures are reported through the MCU alarm callback (mcu_alarm): task_type 0 means it's a push alarm, and task_id is then the push_id (same format as an MCU task ID but not an MCU task; don't pass it to mcu/detail or other mcu/* endpoints)
+ Query push status with List push tasks; error code 1072 is returned when no push service is available, 1075 when the push URL is invalid, and 1076 when the push service rejects the push

**Request parameters**

<ParamField body="channel" type="string" required>
  Channel, which must already be open (up to 64 bytes; letters, digits, underscores (_), and hyphens (-) only)
  Example: `fire`
</ParamField>

<ParamField body="push_url" type="string" required>
  Push URL; rtmp:// and rtmps:// are supported, and it must include the stream key (URLs with an empty stream name such as rtmp://host/app/ are rejected) (max length 1024)
  Example: `rtmp://live.example.com/app/stream_key`
</ParamField>

<ParamField body="video" type="string" required>
  Video source: mcu is the channel's composite video (the channel must have a stream mixing task in progress), user is a specific user's video (with video_uid), none means no video
  Example: `mcu`
</ParamField>

<ParamField body="video_uid" type="string">
  Required when video is user: which user's video to use (letters, digits, underscores (_), and hyphens (-) only)
  Example: `1001`
</ParamField>

<ParamField body="video_desc" type="string">
  Optional when video is user: when the user publishes multiple video tracks at once (such as camera and screen sharing), specifies one of them (exact match on the track description); if omitted, the first one to arrive is used (max length 50)
  Example: `camera`
</ParamField>

<ParamField body="audio" type="string">
  Audio source: auto follows the video (default; the composite video comes with the channel's mixed audio, a single user's video with that user's own audio; auto can't be used without video), mix is the channel's mixed audio (the channel must have a stream mixing task in progress), user is a specific user's audio (with audio_uid), none means no audio. Video and audio can't both be none
  Example: `auto`
</ParamField>

<ParamField body="audio_uid" type="string">
  Required when audio is user: which user's audio to use (letters, digits, underscores (_), and hyphens (-) only)
  Example: `1002`
</ParamField>

<ParamField body="audio_desc" type="string">
  When the user publishes multiple audio tracks, specifies one of them (exact match on the track description); if omitted, the first one is used. Effective when audio is user, or auto following a single user's video (max length 50)
  Example: `mic`
</ParamField>


Request example:

```json
{
  "audio": "auto",
  "audio_desc": "mic",
  "audio_uid": "1002",
  "channel": "fire",
  "push_url": "rtmp://live.example.com/app/stream_key",
  "video": "mcu",
  "video_desc": "camera",
  "video_uid": "1001"
}
```

**Response parameters**

<ResponseField name="push_id" type="string">
  Push task ID, used to stop the push and query its status
  Example: `p7k2xq`
</ResponseField>


Response example:

```json
{
  "code": 0,
  "data": {
    "push_id": "p7k2xq"
  }
}
```

---

## Stop a push

`POST /server/v1/stream/push/stop`

Authentication: required (see [Overview](/en/rtc/server-api/overview))

Stops a push. Stopping a push that has already stopped is treated as success; error code 1074 is returned if the push_id doesn't exist.

**Request parameters**

<ParamField body="push_id" type="string" required>
  Push task ID, from the response of Start a push
  Example: `p7k2xq`
</ParamField>


Request example:

```json
{
  "push_id": "p7k2xq"
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

## List push tasks

`POST /server/v1/stream/push/list`

Authentication: required (see [Overview](/en/rtc/server-api/overview))

Queries the push tasks of a channel: sources, masked push URL, push status, and most recent error, in reverse order of creation.
If push_id is omitted, pushes in progress and those stopped within the last day are returned.

Status values: waiting for the source, connecting to the live streaming platform, publishing,
retrying after a push failure (see err for the reason), stopped.

**Request parameters**

<ParamField body="channel" type="string" required>
  Channel (up to 64 bytes; letters, digits, underscores (_), and hyphens (-) only)
  Example: `fire`
</ParamField>

<ParamField body="push_id" type="string">
  Push task ID; pass it to see only that push. If omitted, pushes in progress and those stopped within the last day in the channel are returned
  Example: `p7k2xq`
</ParamField>


Request example:

```json
{
  "channel": "fire",
  "push_id": "p7k2xq"
}
```

**Response parameters**

<ResponseField name="push_id" type="string">
  Push task ID
  Example: `p7k2xq`
</ResponseField>

<ResponseField name="channel" type="string">
  Channel
  Example: `fire`
</ResponseField>

<ResponseField name="video" type="string">
  Video source: mcu is the composite video, user is a specific user, none means no video
  Example: `mcu`
</ResponseField>

<ResponseField name="video_uid" type="string">
  Whose video is used when video is user
  Example: `1001`
</ResponseField>

<ResponseField name="video_desc" type="string">
  Which of the user's video tracks is used when video is user; empty means the first one to arrive
  Example: `camera`
</ResponseField>

<ResponseField name="audio" type="string">
  Audio source: auto follows the video, mix is the channel's mixed audio, user is a specific user, none means no audio
  Example: `auto`
</ResponseField>

<ResponseField name="audio_uid" type="string">
  Whose audio is used when audio is user
  Example: `1002`
</ResponseField>

<ResponseField name="audio_desc" type="string">
  Which of the user's audio tracks; empty means the first one
  Example: `mic`
</ResponseField>

<ResponseField name="push_url" type="string">
  Push URL with the stream key masked (only the scheme, server, and first path segment are kept)
  Example: `rtmp://live.example.com/app/***`
</ResponseField>

<ResponseField name="status" type="string">
  Push status: waiting for the source (for example, the mixing task hasn't started or the user to push hasn't published; pushing starts automatically once the source appears, and this is not a failure), connecting to the live streaming platform, publishing, retrying after a push failure (see err for the reason), stopped
  Example: `publishing`
</ResponseField>

<ResponseField name="err" type="string">
  Most recent error; empty when everything is normal
  Example: `connection refused`
</ResponseField>

<ResponseField name="created_at" type="integer">
  Creation time, Unix timestamp in seconds
  Example: `1718194666`
</ResponseField>

<ResponseField name="started_at" type="integer">
  Push start time (when it was first handed to the push service), Unix timestamp in seconds; 0 means not started yet
  Example: `1718194667`
</ResponseField>

<ResponseField name="ended_at" type="integer">
  Stop time, Unix timestamp in seconds; 0 means not stopped
  Example: `1718198266`
</ResponseField>


Response example:

```json
{
  "code": 0,
  "data": [
    {
      "audio": "auto",
      "audio_desc": "mic",
      "audio_uid": "1002",
      "channel": "fire",
      "created_at": 1718194666,
      "ended_at": 1718198266,
      "err": "connection refused",
      "push_id": "p7k2xq",
      "push_url": "rtmp://live.example.com/app/***",
      "started_at": 1718194667,
      "status": "publishing",
      "video": "mcu",
      "video_desc": "camera",
      "video_uid": "1001"
    }
  ]
}
```

---

