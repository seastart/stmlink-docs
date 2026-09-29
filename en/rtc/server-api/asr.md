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

+ Calling it again for the same channel doesn't start a second recognition session
+ It recognizes audio from every user in the channel whose mic is on; results carry uid and name to identify the speaker
+ Query transcription results by channel with "List speech recognition sentences"

Charges accrue continuously once started; it stops automatically when the channel is destroyed. You can also end it early with "Stop speech recognition".

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

## List speech recognition sentences

`POST /server/v1/asr/list-sentence`

Authentication: required (see [Overview](/en/rtc/server-api/overview))

List a channel's transcription results with pagination; each item is one sentence, with the speaker and time.

+ Read the results in created_at order to reconstruct the full conversation; this is the data source for generating meeting minutes
+ Results are kept after the channel is destroyed and can be queried afterward

Sentence boundaries are decided by the recognition engine based on pauses in speech and don't necessarily match "one complete unit of meaning"—
when summarizing minutes, merge consecutive sentences before handing them to the model.

**Request parameters**

<ParamField body="channel" type="string" required>
  Channel name
  Example: `fire`
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
  "sort": ""
}
```

**Response parameters**

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
      "created_at": 1718250918,
      "name": "Alice",
      "sentence": "Let's finalize this plan next week",
      "uid": "1001"
    }
  ]
}
```

---

