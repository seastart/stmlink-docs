---
title: "Single-stream output"
description: "Output one user's audio and video in a channel as an RTSP / HTTP-FLV pull URL for NVRs, recorders, or third-party players"
---

{/* The API reference on this page is auto-generated from the backend source. Do not edit it by hand—changes are overwritten on the next sync.
    Edit the rtc-backend source instead; see the "对外接口文档（srvapi）" section of its README. */}

## Get a single-stream RTSP pull URL

`POST /server/v1/stream/rtsp-url`

Authentication: required (see [Overview](/en/rtc/server-api/overview))

Get an RTSP pull URL for one user's audio/video in a channel. The server subscribes to the user's streams as an audience member
and outputs them over RTSP as is, without transcoding; suited to feeding in-channel video into an NVR, recorder, or other system that accepts only RTSP.

+ The URL is signed and can be pulled repeatedly by multiple players until it expires; after expiry, new pull requests are rejected, while playback already in progress is not affected
+ The server subscribes only when someone pulls and unsubscribes automatically after the last player disconnects, so an unused URL consumes no resources; there is no stop endpoint to call
+ It doesn't check whether the channel is open or the user is online, so you can generate the URL in advance; if the user hasn't published yet when a player pulls, the player gets a 404 and should retry
+ If the user leaves and comes back, the pull isn't interrupted; there is just a blank gap in between
+ Only RTSP over TCP is supported (the player must use TCP, for example ffplay with `-rtsp_transport tcp`)
+ No transcoding: audio is Opus and video uses the codec the publisher actually uses (H264 or VP8); if your player doesn't support VP8, have the publisher use H264

The actual validity period is the returned expire_at (the server-side limit may be shorter than the requested value).

**Request parameters**

<ParamField body="channel" type="string" required>
  Channel (up to 64 bytes; letters, digits, underscores (_), and hyphens (-) only)
  Example: `fire`
</ParamField>

<ParamField body="uid" type="string" required>
  User ID of the publisher to pull (letters, digits, underscores (_), and hyphens (-) only)
  Example: `1001`
</ParamField>

<ParamField body="media" type="string" required>
  Media type: audio for audio only, video for video only, av for audio and video
  Example: `av`
</ParamField>

<ParamField body="desc" type="string">
  Video track description, used to pick one track when the user publishes multiple video tracks at once (such as camera and screen sharing); if omitted, whichever track arrives first is output (max length 50)
  Example: `camera`
</ParamField>

<ParamField body="expire" type="integer">
  URL validity period (seconds); defaults to one hour if omitted, up to one day
  Example: `3600`
</ParamField>


Request example:

```json
{
  "channel": "fire",
  "desc": "camera",
  "expire": 3600,
  "media": "av",
  "uid": "1001"
}
```

**Response parameters**

<ResponseField name="url" type="string">
  RTSP pull URL; signed, and can be pulled repeatedly until it expires
  Example: `rtsp://1.2.3.4:8554/s/eyJhcHBpZCI6...`
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
    "url": "rtsp://1.2.3.4:8554/s/eyJhcHBpZCI6..."
  }
}
```

---

## Get a single-stream HTTP-FLV pull URL (H264 video only)

`POST /server/v1/stream/flv-url`

Authentication: required (see [Overview](/en/rtc/server-api/overview))

Get the HTTP-FLV pull URL of a user in the channel (video + optional audio). The server subscribes to the user's video as an audience member,
and outputs the video as HTTP-FLV without transcoding, suitable for players or third-party platforms that only accept FLV.

+ By default the same user's audio is included (audio=same): this API used to output video only and now includes audio by default; pass audio=none if you only want video
+ You can choose another audio source: mix for the channel's mixed audio (requires an in-progress stream mixing or live streaming task in the channel), or user for a specific user's audio (with audio_uid).
For example, "presenter's video + channel mixed audio" is uid=presenter, audio=mix
+ Audio is transcoded to AAC on the server; the video must be H264, and if the publisher uses VP8 or another codec, pull requests get a 404, so have the publisher use H264
+ The URL is signed and can be pulled repeatedly by multiple players until it expires; after expiry, new pull requests are rejected, while playback already in progress is not affected
+ The server subscribes only when someone pulls and unsubscribes automatically after the last player disconnects, so an unused URL consumes no resources; there is no stop endpoint to call
+ It doesn't check whether the channel is open or the user is online, so you can generate the URL in advance; if the user hasn't published yet when a player pulls, the player gets a 404 and should retry
+ If the user leaves and comes back, the pull isn't interrupted; there is just a blank gap in between

The actual validity period is the returned expire_at (the server-side limit may be shorter than the requested value).

**Request parameters**

<ParamField body="channel" type="string" required>
  Channel (up to 64 bytes; letters, digits, underscores (_), and hyphens (-) only)
  Example: `fire`
</ParamField>

<ParamField body="uid" type="string" required>
  User ID of the publisher to pull (letters, digits, underscores (_), and hyphens (-) only)
  Example: `1001`
</ParamField>

<ParamField body="desc" type="string">
  Video track description, used to pick one track when the user publishes multiple video tracks at once (such as camera and screen sharing); if omitted, whichever track arrives first is output (max length 50)
  Example: `camera`
</ParamField>

<ParamField body="audio" type="string">
  Audio source: same for the same user's audio (default), none for no audio, mix for the channel's mixed audio (requires an in-progress stream mixing or live streaming task in the channel), or user for a specific user's audio (audio_uid is then required)
  Example: `same`
</ParamField>

<ParamField body="audio_uid" type="string">
  Required when audio is user: whose audio to use (letters, digits, underscores (_), and hyphens (-) only)
  Example: `1002`
</ParamField>

<ParamField body="audio_desc" type="string">
  Audio track description, used to pick one track when the user publishes multiple audio tracks; defaults to the first one. Takes effect when audio is same or user (max length 50)
  Example: `mic`
</ParamField>

<ParamField body="expire" type="integer">
  URL validity period (seconds); defaults to one hour if omitted, up to one day
  Example: `3600`
</ParamField>


Request example:

```json
{
  "audio": "same",
  "audio_desc": "mic",
  "audio_uid": "1002",
  "channel": "fire",
  "desc": "camera",
  "expire": 3600,
  "uid": "1001"
}
```

**Response parameters**

<ResponseField name="url" type="string">
  HTTP-FLV pull URL; signed, and can be pulled repeatedly until it expires
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

