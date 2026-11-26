---
title: "Simultaneous Interpretation"
description: "Turn in-meeting simultaneous interpretation on or off and set member languages: each finalized sentence is translated into the languages of the members and synthesized into speech, delivered through the channel message asr_trans; builds on \"Transcription\""
---

{/* The API reference on this page is auto-generated from the backend source. Do not edit it by hand—changes are overwritten on the next sync.
    Edit the rtc-backend source instead; see the "对外接口文档（srvapi）" section of its README. */}

## Start simultaneous interpretation

`POST /server/v1/interp/start`

Authentication: required (see [Overview](/en/rtc/server-api/overview))

Start simultaneous interpretation in a channel: each finalized sentence is translated into the languages of the members in the channel and synthesized into speech, delivered through the channel message asr_trans (with audio_url).

+ Builds on speech recognition: if speech recognition is not yet running in the channel, it is started automatically, and the returned session_id is the same as from "Start speech recognition"
+ Members set their own language with "Set a member's interpretation language"; members who have not set one count as Chinese. Each sentence is translated only into "languages of members in the channel − the speaker's language"
+ After it starts, the channel message interp_enabled is sent (enabled=true; duck_volume is the volume of the speaker's original voice while the interpretation audio plays), and interp_enabled / interp_duck_volume in the channel properties (props)
are updated accordingly, so members who join later read the current state from the channel properties
+ Repeated calls are idempotent and can be used to switch the AI profile during a meeting; interpretation stops when speech recognition stops

The app's AI profile must include a large language model, otherwise "LLM not configured or not enabled" is returned. If the profile has no speech synthesis, only the translated text is delivered, without audio_url.

**Request parameters**

<ParamField body="channel" type="string" required>
  Channel name
  Example: `fire`
</ParamField>

<ParamField body="profile" type="string">
  AI profile name (configured under "AI Services & Profiles" in the admin console). If omitted, the profile in the app's AI settings is used, falling back to the default profile (max length 64)
  Example: `default`
</ParamField>


Request example:

```json
{
  "channel": "fire",
  "profile": "default"
}
```

**Response parameters**

<ResponseField name="session_id" type="string">
  Recognition session ID (interpretation runs on the transcription session)
</ResponseField>

<ResponseField name="duck_volume" type="number">
  Volume the speaker's original voice is lowered to while interpretation audio plays (0~1, 0 = muted), from the AI profile
  Example: `0.2`
</ResponseField>


Response example:

```json
{
  "code": 0,
  "data": {
    "duck_volume": 0.2,
    "session_id": ""
  }
}
```

---

## Stop simultaneous interpretation

`POST /server/v1/interp/stop`

Authentication: required (see [Overview](/en/rtc/server-api/overview))

Stop simultaneous interpretation in a channel. Speech recognition continues as before (translation falls back to the single-language real-time translation in the app's settings). Returns success even if interpretation is not on.

After it stops, the channel message interp_enabled (enabled=false) is sent.

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

## Set a member's interpretation language

`POST /server/v1/interp/set-lang`

Authentication: required (see [Overview](/en/rtc/server-api/overview))

Set a member's interpretation language ("My language"): it decides which language the member's speech is recognized in, and which language other people's speech is translated into for the member.

+ Can be set as soon as the channel is open; if interpretation is not on yet, the setting is kept and takes effect when it starts; cleared when the channel is destroyed
+ After it is set, the channel message interp_lang (uid, lang) is sent, which clients use to decide whether to play a given interpretation audio
+ While recognition is running, the member's recognition language switches immediately; the last sentence spoken before the switch is still output
+ For members who mix Chinese and English when speaking, Chinese is recommended

**Request parameters**

<ParamField body="channel" type="string" required>
  Channel name
  Example: `fire`
</ParamField>

<ParamField body="uid" type="string" required>
  Member's user ID (letters, digits, underscores (_), and hyphens (-) only)
  Example: `1001`
</ParamField>

<ParamField body="lang" type="string">
  Language code (zh / en, etc.; regional codes such as zh-CN are treated as zh); empty = restore the default language (max length 16)
  Example: `en`
</ParamField>


Request example:

```json
{
  "channel": "fire",
  "lang": "en",
  "uid": "1001"
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

## Get interpretation status and member languages

`POST /server/v1/interp/langs`

Authentication: required (see [Overview](/en/rtc/server-api/overview))

Get the channel's interpretation status and member language table. Fetch the full table once on joining, then update incrementally from the channel messages interp_enabled / interp_lang.

langs only contains members who have set a language; the others use default_lang.

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

<ResponseField name="enabled" type="boolean">
  Whether simultaneous interpretation is on
</ResponseField>

<ResponseField name="duck_volume" type="number">
  Volume the speaker's original voice is lowered to while interpretation audio plays (0~1); 0 when interpretation is off
</ResponseField>

<ResponseField name="default_lang" type="string">
  Language used for members who have not set one
  Example: `zh`
</ResponseField>

<ResponseField name="langs" type="object">
  Members who have set a language: uid → language
  Example: `{"1001":"en"}`
</ResponseField>


Response example:

```json
{
  "code": 0,
  "data": {
    "default_lang": "zh",
    "duck_volume": 0,
    "enabled": false,
    "langs": {
      "1001": "en"
    }
  }
}
```

---

