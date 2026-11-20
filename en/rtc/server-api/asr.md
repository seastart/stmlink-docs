---
title: "Transcription"
description: "Start and stop ASR speech recognition and get the results"
---

{/* The API reference on this page is auto-generated from the backend source. Do not edit it by hand—changes are overwritten on the next sync.
    Edit the rtc-backend source instead; see the "对外接口文档（srvapi）" section of its README. */}

## Start speech recognition

`POST /server/v1/asr/start`

Authentication: required (see [Overview](/en/rtc/server-api/overview))

Start real-time speech recognition for a channel to transcribe what's said into text, for meeting minutes, captions, and search.

+ Calling it again for the same channel doesn't start a second recognition session; it returns the session already in progress
+ It recognizes audio from every user in the channel whose mic is on; results carry uid and name to identify the speaker
+ One meeting in a channel (from when the channel opens until it is destroyed) is one recognition session; transcription results and meeting minutes are archived by session
+ Stopping and starting again during the meeting (for example, to change the translation language) keeps the original session and returns the original session_id, so a meeting produces only one set of minutes; a new meeting after the channel is destroyed is a new session
+ Query transcription results by session or by channel with "List speech recognition sentences"

Charges accrue continuously once started; it stops automatically when the channel is destroyed. You can also end it early with "Stop speech recognition".
If the app has automatic minutes enabled, meeting minutes are generated when the session ends, and the channel message ai_summary_ready is sent when they are ready;
if the same session is started again and ends, the minutes are regenerated from all transcripts and overwrite the original ones;
if translate_lang is passed (or the app has real-time translation enabled), the translation of each finalized sentence is delivered through the channel message asr_trans.

**Request parameters**

<ParamField body="channel" type="string" required>
  Channel name
  Example: `fire`
</ParamField>

<ParamField body="translate_lang" type="string">
  Target language for real-time translation. If set, each finalized sentence in this session is translated automatically and the translation is delivered through the channel message asr_trans; if omitted, the app's setting applies (max length 16)
  Example: `en`
</ParamField>


Request example:

```json
{
  "channel": "fire",
  "translate_lang": "en"
}
```

**Response parameters**

<ResponseField name="session_id" type="string">
  Recognition session ID, used to query sentences and get meeting minutes
</ResponseField>


Response example:

```json
{
  "code": 0,
  "data": {
    "session_id": ""
  }
}
```

---

## Stop speech recognition

`POST /server/v1/asr/stop`

Authentication: required (see [Overview](/en/rtc/server-api/overview))

Stop speech recognition for a channel. Transcription results already produced are not deleted and can still be queried with "List speech recognition sentences".

Stops automatically when the channel is destroyed, so you don't need to stop it manually first.

**Request parameters**

<ParamField body="channel" type="string" required>
  Channel name
  Example: `fire`
</ParamField>


Request example:

```json
{
  "channel": "fire"
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

## List speech recognition sessions

`POST /server/v1/asr/list-session`

Authentication: required (see [Overview](/en/rtc/server-api/overview))

List the app's speech recognition sessions with pagination, with the meeting minutes status of each. One meeting in a channel (from open to destroy) is one session; stopping and starting again during the meeting stays in the same session.

Channel names get reused (the same meeting room hosts meetings every day), so sessions are what tell the transcriptions and minutes of each meeting apart.

**Request parameters**

<ParamField body="channel" type="string">
  Channel name; omit for all channels (max length 100)
  Example: `fire`
</ParamField>

<ParamField body="begin_at" type="integer">
  Start time (filters by session start time), Unix timestamp in seconds; 0 means no limit
</ParamField>

<ParamField body="end_at" type="integer">
  End time, Unix timestamp in seconds; 0 means no limit
</ParamField>

<ParamField body="sort" type="string">
  Sort order; defaults to start time, newest first (sortable fields: started_at, sentence_count)
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
  "begin_at": 0,
  "channel": "fire",
  "end_at": 0,
  "page": 1,
  "per-page": 10,
  "sort": ""
}
```

**Response parameters**

<ResponseField name="session_id" type="string">
  Recognition session ID
</ResponseField>

<ResponseField name="channel" type="string">
  Channel name
  Example: `fire`
</ResponseField>

<ResponseField name="started_at" type="integer">
  Recognition start time, Unix timestamp in seconds
  Example: `1718250918`
</ResponseField>

<ResponseField name="ended_at" type="integer">
  Recognition end time, Unix timestamp in seconds; 0 means recognition is in progress
</ResponseField>

<ResponseField name="status" type="integer">
  Session status: 1 recognizing, 2 ended
</ResponseField>

<ResponseField name="sentence_count" type="integer">
  Number of transcribed sentences
</ResponseField>

<ResponseField name="summary_status" type="integer">
  Minutes status: -1 not generated, 0 queued, 1 generating, 2 completed, 3 failed
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
      "channel": "fire",
      "ended_at": 0,
      "sentence_count": 0,
      "session_id": "",
      "started_at": 1718250918,
      "status": 0,
      "summary_status": 0
    }
  ]
}
```

---

## List speech recognition sentences

`POST /server/v1/asr/list-sentence`

Authentication: required (see [Overview](/en/rtc/server-api/overview))

List a channel's transcription results with pagination; each item is one sentence, with the speaker and time.

+ Read the results in created_at order to reconstruct the full conversation; this is the data source for generating meeting minutes
+ Pass session_id to get only the sentences of one recognition session; begin_ms / end_ms are milliseconds from the start of that session and can be used directly as a caption timeline
+ Results are kept after the channel is destroyed and can be queried afterward

Sentence boundaries are decided by the recognition engine based on pauses in speech and don't necessarily match "one complete unit of meaning"—
when summarizing minutes, merge consecutive sentences before handing them to the model.

**Request parameters**

<ParamField body="channel" type="string">
  Channel name; required when session_id is not passed
  Example: `fire`
</ParamField>

<ParamField body="session_id" type="string">
  Recognition session ID; if set, only sentences from that session are returned
</ParamField>

<ParamField body="sort" type="string">
  Sort order
</ParamField>

<ParamField body="search" type="array<string>">
  General search; can search transcription content
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
  "search": [
    ""
  ],
  "session_id": "",
  "sort": ""
}
```

**Response parameters**

<ResponseField name="sentence_id" type="string">
  Sentence ID; matches sentence_id in the asr_trans channel message
</ResponseField>

<ResponseField name="channel" type="string">
  Channel name
  Example: `fire`
</ResponseField>

<ResponseField name="uid" type="string">
  Speaker's user ID
  Example: `1001`
</ResponseField>

<ResponseField name="name" type="string">
  Speaker's display name
  Example: `Alice`
</ResponseField>

<ResponseField name="sentence" type="string">
  Transcribed text of one sentence
  Example: `Let's finalize this plan next week`
</ResponseField>

<ResponseField name="created_at" type="integer">
  Time the sentence was produced, Unix timestamp in seconds
  Example: `1718250918`
</ResponseField>

<ResponseField name="session_id" type="string">
  ID of the recognition session it belongs to; empty for early data
</ResponseField>

<ResponseField name="begin_ms" type="integer">
  Sentence start time, in milliseconds from the start of the session
  Example: `65200`
</ResponseField>

<ResponseField name="end_ms" type="integer">
  Sentence end time, in milliseconds from the start of the session
  Example: `68900`
</ResponseField>

<ResponseField name="trans_text" type="string">
  Translated text; empty when translation is not enabled
</ResponseField>

<ResponseField name="trans_lang" type="string">
  Translation language, such as en
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
      "begin_ms": 65200,
      "channel": "fire",
      "created_at": 1718250918,
      "end_ms": 68900,
      "name": "Alice",
      "sentence": "Let's finalize this plan next week",
      "sentence_id": "",
      "session_id": "",
      "trans_lang": "",
      "trans_text": "",
      "uid": "1001"
    }
  ]
}
```

---

