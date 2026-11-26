---
title: "Live captions and transcription"
sidebarTitle: "Captions and transcription"
description: "Live captions and transcription: per-speaker recognition, Chinese as you speak and English per sentence, translated captions, per-app hot words, the transcript after the meeting, who turns it on, and how each client gets results. Read when evaluating caption needs."
---

Once transcription is on during a meeting, whatever each unmuted speaker says becomes text in real time: shown as captions in web meetings, available as a full transcript after the meeting,
and the basis for [meeting minutes](/en/product/ai/summary) and [simultaneous interpretation](/en/product/ai/interpretation).

---

## What it does

| Capability | Description |
| --- | --- |
| **Per-speaker transcription** | Each unmuted speaker's voice is recognized separately, and every sentence carries the speaker's ID and name—no voiceprint diarization needed |
| **In-meeting captions** | Chinese appears as you speak (interim results first, corrected to the final text once the sentence ends); English appears as a whole sentence once it ends |
| **Live translated captions** | Each final sentence is translated into a specified language by the LLM, and the translation is shown with the original |
| **Hot words** | Configure proper nouns (company names, product names, personal names) per app to improve recognition accuracy |
| **Transcript archive** | Final sentences are archived per "session" and can be viewed after the meeting in the meeting client, the admin console, or through the server API |

---

## Who turns it on, and where

+ **In the meeting**: the host turns on "Meeting transcription" in the "Captions and transcription" panel of the web meeting, and all members see captions right away; each person can also turn off "Show captions" locally without affecting others. For translation, choose the "Live translation" language before turning on transcription
+ **Your business system**: call the [start speech recognition](/en/rtc/server-api/asr) endpoint from the server to start transcription for a channel
+ **Admin console**: configure hot words and live translation under **AI capabilities → App AI settings**; view the transcript of each session under **Minutes records**

Transcription is organized by **session**: one channel from opening to destruction is one session. Turning transcription off and on again during the meeting keeps the same session—the transcript continues, and only one set of minutes is produced at the end.

---

## Supported languages

| Language | Caption behavior | Notes |
| --- | --- | --- |
| Chinese | Appears as you speak, corrected to the final text once the sentence ends | Default language; supports hot words |
| English | Appears as a whole sentence once it ends, with no interim results | In our tests, the final text arrives about 0.8 seconds after the pause at the end of a sentence; the English model doesn't support hot words |

+ Which language a speaker is recognized in depends on the service chosen per language for "Speech recognition" in the [AI profile](/en/product/ai/models#ai-profiles); languages that aren't configured aren't recognized
+ Chinese-only meetings need no language settings. In meetings with both Chinese and English, once members set "My language" in simultaneous interpretation, each is recognized in their own language
+ **People who mix Chinese and English are best recognized as Chinese**: the Chinese model can recognize English words mixed in (with lower accuracy), while the English model can barely recognize Chinese

---

## Live translated captions

Turn on **Live translation** in **App AI settings** and choose a target language (such as English), or specify a target language when starting transcription. From then on, every final sentence is also translated:

+ Translation doesn't block the original: original captions still appear first, and the translation follows (about 1 second from final text to translation in our tests, depending on the LLM's speed)
+ When the LLM's concurrency is full, that sentence is **skipped** rather than delayed, so translations don't fall further and further behind
+ An LLM must be configured in the AI profile

Live translation produces text in **one** target language only. If each person should hear their own language, use [simultaneous interpretation](/en/product/ai/interpretation).

---

## Hot words

Proper nouns that are recognized poorly (such as company names and product models) can be added as hot words under **AI capabilities → App AI settings → Hot words**. Each entry has a word and a weight (1–100 recommended; higher means more likely to match).

+ Hot words apply per app; they are sent to the recognition service when transcription starts and used for the whole session. Changes take effect the next time transcription starts
+ Apps without hot words use the platform's default hot words; at deployment, a global hot word list can also be configured on the recognition service for all apps
+ The English recognition model doesn't support hot words

---

## View the transcript after the meeting

| Where | How |
| --- | --- |
| Web meeting client | The minutes page of a past meeting has a "Transcript" tab |
| Admin console | **AI capabilities → Minutes records**; switch to "Transcript" when viewing minutes |
| SMeeting Web SDK | `aiTranscript()` returns all sentences of a session; see [SMeeting · aiTranscript](/en/meeting/web/api-reference/SMeeting) |
| Server API | [Speech recognition session list and sentence list](/en/rtc/server-api/asr) |

Each sentence carries the speaker and its start and end times (relative to the start of the session); with live translation on, it also carries the translation.

---

## How each client gets captions

| Usage | How |
| --- | --- |
| Web meeting client | Built-in caption overlay and transcription switch; no development needed |
| SMeeting conferencing SDK (Web) | Events `ASR_RESULT` (original) and `ASR_TRANSLATION` (translation); see [SMeeting Web API](/en/meeting/web/api-reference/SMeeting) |
| SRTC Audio & Video SDK (all platforms) | Recognition results are sent as the in-channel custom message `asr_res` and translations as `asr_trans`; any client can receive these in-channel custom messages and display them itself |

<Note>
The ready-made caption, minutes, and transcript APIs of the conferencing SDK are currently available on **Web** only; other platforms can display captions themselves from SRTC channel messages.
</Note>
