---
title: "Choosing SRTC or SMeeting"
description: "How SRTC (audio and video SDK) and SMeeting (conferencing SDK) are layered, how their terms and capabilities differ, and which one fits your product. Read before you start integrating, if you're not sure which layer to build on."
---

We offer two products, and **SMeeting is built on top of SRTC**. Here is the difference in one line each:

+ **SRTC** gives you the audio and video transport. Who can speak, who the host is, when a meeting starts—you write these rules yourself.
+ **SMeeting** (the SDK behind STMLink Meeting) gives you the meeting rules too. Host, raise hand, mute all, waiting room, and recording are all built in.

If you're still unsure, start with this question: **do you want to write the rules for "who can do what in a meeting" yourself, or use them as is?**

---

## How to choose

| Your situation | Choose |
| --- | --- |
| You're building a meeting product and need meeting controls such as host, raise hand, mute all, and waiting room | **SMeeting** |
| You want to launch as fast as possible and can accept the meeting UI we provide | **SMeeting** (low-code integration with UI) |
| Your interaction isn't a meeting: interactive live streaming with guests, one-to-one customer service calls, AI voice conversations, remote inspection | **SRTC** |
| You already have your own business rules and UI and only lack audio and video transport | **SRTC** |
| Server-side recording by a bot in the channel, re-streaming, AI agent integration | **SRTC** (C SDK or the platform SDKs) |

<Tip>
When in doubt, look at SMeeting first. Meeting control rules look simple, but actually implementing them (state sync across devices, host permissions, state recovery after reconnecting) is the most time-consuming part of a meeting product. If your product is a meeting, writing it all yourself isn't worth it.
</Tip>

---

## How they relate

SMeeting isn't a replacement for SRTC; it's a higher-level wrapper around it:

```text
┌────────────────────────────────────────────────────────────┐
│  Your business                                             │
├────────────────────────────────────────────────────────────┤
│  SMeeting   Rooms / meetings / members / meeting controls  │  ← Meeting semantics
├────────────────────────────────────────────────────────────┤
│  SRTC       Channels / users / tracks                      │  ← Audio and video transport
└────────────────────────────────────────────────────────────┘
```

When you use SMeeting, SRTC still works underneath, just wrapped inside—you don't need to call it directly.

---

## Terminology mapping

The terms of the two layers **are not interchangeable**. When reading the docs, keep track of which layer you're in:

| | SRTC | SMeeting |
| --- | --- | --- |
| Space | Channel `channel` | Room `room` / meeting `meeting` |
| Entering and leaving | Join / leave | Enter / exit |
| People | User `uid` | Member |
| Media | Track `track` | Managed by the meeting layer |

<Warning>
The APIs of the two layers can't be mixed. SMeeting's server API doesn't accept channel names, and SRTC's API doesn't recognize meeting numbers. The sample code in the docs only works in the layer it belongs to.
</Warning>

---

## Capability differences

| Capability | SRTC | SMeeting |
| --- | :---: | :---: |
| Audio and video calls, screen sharing | ✅ | ✅ |
| Custom signaling (business messages meant for programs) | ✅ | ✅ |
| In-meeting text chat (with history, chat can be disabled) | Build it yourself | ✅ |
| Out-of-meeting notification channel (calling, reminders) | ✅ (IM channel, out-of-channel messaging) | ✅ |
| Cloud recording, MCU stream mixing | ✅ | ✅ |
| Host and meeting controls (mute all, remove members, change roles) | Build it yourself | ✅ |
| Raise hand, ask to unmute | Build it yourself | ✅ |
| Waiting room, sub-meetings, sign-in | Build it yourself | ✅ |
| Meeting scheduling and lifecycle management | Build it yourself | ✅ |
| Ready-made meeting UI | ❌ | ✅ (low-code integration with UI) |
| One user online on multiple devices at once | Plan the uid yourself | ✅ (distinguished automatically by device type) |
| Server / embedded integration (recording, AI agents) | ✅ (C SDK) | ❌ |

---

## FAQ

**If I use SMeeting, can I still call SRTC directly?**

Usually you don't need to. SMeeting already wraps the audio and video capabilities in meeting semantics. A few platforms (such as Swift) keep an entry point to the underlying layer for scenarios we don't cover, but a normal integration doesn't use it.

**How costly is it to switch from SRTC to SMeeting later?**

Client code basically has to be rewritten—the two layers have different APIs and conceptual models. On the server, if you already treat audio and video as a separate module, the changes are smaller. So **try to make the right choice up front**, rather than thinking "use SRTC for now and switch later".

**Can I use both at the same time?**

Not recommended within the same business scenario. Separate scenarios are fine—for example, SMeeting for meetings and SRTC for one-to-one customer service calls, each integrated independently.

**Is self-hosted deployment any different?**

Both support it. SMeeting requires one additional meeting-layer service.

---

## Next steps

Once you've chosen, start with that product's overview:

+ [SRTC overview](/en/rtc/overview)—audio and video SDK
+ [SMeeting overview](/en/meeting/overview)—conferencing SDK

If you're still unsure, contact us directly and describe your business scenario.
