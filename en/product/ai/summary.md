---
title: "Meeting minutes"
sidebarTitle: "Meeting minutes"
description: "Automatic meeting minutes: the customer's own LLM turns the transcript into Markdown minutes (summary, points, decisions, action items). Custom templates, one set per session with regeneration, who can view them where, and what to configure. Read when evaluating minutes needs."
---

For meetings with [transcription](/en/product/ai/transcription) on, the LLM turns the full transcript into **meeting minutes** once transcription ends.
Meeting members can see them in their past meetings, with no manual write-up afterward.

---

## What the minutes look like

The built-in "General meeting" template outputs Markdown with four fixed sections:

| Section | Content |
| --- | --- |
| Meeting summary | Three to five sentences on the purpose of the meeting and the overall conclusion |
| Topics and discussion points | Itemized by topic, with each side's views and the speaker noted |
| Conclusions / decisions | Each agreed item listed |
| Action items | A table of item, owner, and due date; anything not mentioned in the transcript is written as "Not specified" |

The template tells the LLM to **rely only on the transcript and not make anything up**, keeping numbers, proper nouns, and names as they are. Minutes quality depends on the LLM used and on recognition accuracy;
for important meetings, we still recommend a manual review afterward.

---

## How minutes are generated

1. The host turns on meeting transcription, and the meeting proceeds as usual
2. When transcription ends (the host turns off "Meeting transcription", or the meeting ends), the platform assembles the session's final sentences into a transcript in the form `[min:sec] speaker: content`
3. The LLM generates minutes from the transcript using the template; for very long transcripts (more than about 12,000 characters), it summarizes in segments first and then merges them, to stay within the model's context length
4. When generation completes, members still in the meeting see a "Meeting minutes generated" notice; on failure it retries automatically, and if it still fails you can regenerate manually

**One meeting, one set of minutes**: minutes are generated per transcription **session**. Turning transcription off and on during the meeting keeps the same session; at the end, minutes are regenerated from all transcribed content and **overwrite** the previous minutes, so you never get several versions.
The host or a console administrator can also **regenerate** with a different template, which likewise overwrites the existing minutes.

---

## What needs configuring

| Setting | Where | Description |
| --- | --- | --- |
| LLM | Admin console **AI capabilities → AI services and profiles** | Register the customer's LLM service and add it to an AI profile; see [AI services and profiles](/en/product/ai/models). No minutes are generated without an LLM |
| Automatic minutes | **AI capabilities → App AI settings → Meeting minutes** | Turn on "Generate minutes automatically"; when off, minutes can be generated manually when needed |
| Minutes template | Same place, choose "Minutes template" | The default template is used if none is chosen |

### Minutes templates

Maintained under **AI capabilities → Minutes templates**. Three are built in: **General meeting** (default), **Review meeting**, and **Weekly meeting**. You can edit them directly or add new ones.

A template is simply a prompt for the LLM, with two placeholders:

+ `{{transcript}}`: the full transcript (required; otherwise the LLM gets no meeting content)
+ `{{meeting_info}}`: meeting information (channel, start and end times, etc.)

When the customer has a fixed minutes format (for example, project meetings that list "Risks and help needed" separately), adapt the section requirements of a built-in template.

---

## Who can view them, and where

| Where | Who can view |
| --- | --- |
| Web meeting client, "Past meetings" | Users logged in under the same app (same permission as viewing recording details); there are two tabs, "Minutes" and "Transcript" |
| Admin console **AI capabilities → Minutes records** | Console accounts with permission for that menu; can view minutes and transcripts, and regenerate with a chosen template |
| SMeeting Web SDK | `aiSummary()` gets minutes, and `adminAiSummaryGenerate()` lets the host regenerate them; see [SMeeting Web API](/en/meeting/web/api-reference/SMeeting) |
| Server API | [Get / generate meeting minutes](/en/rtc/server-api/ai), limited to the app's own data; your business system can use it to push minutes into OA or project management systems |

<Note>
Meeting content is the customer's confidential information: by default, prompts sent to the LLM and the LLM's output are **not written to service logs**; the LLM address is provided by the customer, and the platform has no public models built in.
</Note>
