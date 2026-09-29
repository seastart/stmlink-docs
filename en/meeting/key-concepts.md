---
title: "Key concepts"
description: "The SMeeting model: rooms vs. meetings and the meeting lifecycle, built-in roles (host, co-host, regular member), audience, custom roles, the three types of messages, multi-device presence, and how SMeeting terms differ from the underlying SRTC layer."
---

The SMeeting model is organized around three kinds of state: **meeting state**, **member state**, and **media state**. The APIs and events in every platform's SDK exist to synchronize these three kinds of state; once you understand this, most of the APIs become intuitive.

---

## Rooms and meetings

The two words often appear together but mean different things:

| Concept | Description |
| --- | --- |
| **Room** | A relatively fixed meeting space with a room number |
| **Meeting** | A specific meeting session with a meeting ID; it must be created before anyone can enter it |

In day-to-day integration, you mostly work with the **meeting ID**: you get it when you create a meeting and use it afterward for entering, meeting controls, and recording. The room number is mainly used for sharing externally (sending the number to invitees).

### Lifecycle

```text
Log in  →  Before the meeting (create / query / update meetings)  →  Enter the meeting  →  In the meeting  →  Exit the meeting  →  Log out
```

+ You can call the meeting management APIs only **after logging in**
+ You can call the in-meeting APIs (media control, meeting controls, messages) only **after entering the meeting**
+ Exiting a meeting doesn't affect the login state; you can go on to enter the next meeting

Every platform's SDK returns a clear error (not logged in / not in a meeting) when you call something at the wrong time, so you don't need to track this state yourself.

---

## Members and roles

SMeeting **has a built-in set of in-meeting roles** in three tiers that cover most meeting scenarios, so you don't need to design your own. The `role` field in the APIs and in every platform's SDK takes these three values by default:

| Role | `role` | Who decides | Capabilities |
| --- | --- | --- | --- |
| **Host** | 1 | The meeting's `host_uid`: the `creator` when the meeting is created on the server, or the creator themselves when it is created through the SDK. A meeting has only one host | Full meeting controls: mute all, remove members, change roles, lock the meeting, turn the waiting room on or off, end the meeting |
| **Co-host** | 2 | Assigned by the host (by changing roles during the meeting), or written into `co_hosts` when creating / updating the meeting | Most meeting controls; the exact operations depend on what each platform's SDK exposes |
| **Regular member** | 0 | Default | Turning their own audio and video on or off, raising a hand, chatting |

There is also the **audience** (`is_audience` when entering the meeting). It is not a role but a way of entering: audience members only receive streams, don't take part in interaction, and don't appear in the member list; this is independent of the three tiers above. It corresponds to the audience in the underlying SRTC—note that SRTC also has a `role` field (regular user / audience), which is not the same thing as these three meeting-layer tiers.

If your business also needs to distinguish identities such as "instructor / teaching assistant / student," the simplest approach is: keep carrying meeting control permissions with the three tiers above, put the business identity in the member's extension field (`extend_info`), and render it as needed in your own UI. When your identity system is too different to fit into three tiers, you can replace the built-in roles entirely; see "Custom roles" below.

Most meeting control actions take a **request–approve** form: a member raises a hand to ask to unmute, and the host approves; the host asks a member to unmute, and the member accepts or declines. It is designed this way because turning on a camera or microphone involves user privacy, so the host can't force it on unilaterally.

### Custom roles

The three built-in tiers **can be disabled entirely** and replaced with a role system defined completely by you. In some projects, the roles have nothing to do with "host / co-host / regular member": a typical example is tendering and bidding, where experts, clarifying parties, witnesses, and supervisors are each a separate identity, and who can see whose video, and who hears the real voice versus an altered voice, are all decided by identity.

<Note>
**We have already built this tendering and bidding scenario**: there is a standard tendering and bidding meeting product with customized roles that you can use directly, without implementing these roles and UI yourself. For other scenarios that need custom roles, you can develop them yourself or have us develop them for you—contact us either way.
</Note>

When developing it yourself, turn on **external role mode** (server configuration option `app.enable_role`, off by default; it requires self-hosted deployment, contact us to enable it). `role` then becomes a field defined by your business:

+ **The values and their meanings are entirely up to you**; the server only stores and passes them through, without interpreting them. Number custom values starting from `1`; `0` means not set (treated as a regular member)
+ **Roles come only from the member registration list**: preset them with `conferee_details[].role` when creating / updating a meeting, and adjust them during the meeting with the "Update a member's in-meeting role" endpoint (changes made during the meeting are also saved, and still apply after re-entering). Roles are no longer derived from `creator` / `co_hosts`, and **anyone not registered has no role**
+ **The server no longer makes meeting control decisions based on roles**: all the built-in restrictions such as "regular members can't unmute themselves / turn on video / start sharing" are skipped, and who can do what is decided by your customized client UI
+ **There is no built-in host concept**: the transfer host endpoint returns an error in this mode
+ **Disabling chat applies equally to everyone**: disabling chat for everyone / for a single member works as usual, and the server no longer makes an exception for the host

One point you must think through first: **"who can hear whom and who can see whom" is not distributed by the server based on roles**. The SMeeting server doesn't do role-based selective delivery; all it gives you is the `role` field. Differentiated listening and viewing must be implemented on the client—after getting each member's `role` from the member list, decide yourself whose streams to subscribe to, whom to mute, and which video not to render; the same goes for audio processing such as voice changing, which your business implements itself.

---

## Three types of messages

SMeeting has three kinds of "messages," with different APIs and use cases. Developers most often confuse the last two:

| | In-meeting chat | In-meeting custom messages | Out-of-meeting messages (IM) |
| --- | --- | --- | --- |
| Prerequisite | Entered the meeting | Entered the meeting | Logged in with IM enabled; **doesn't need to be in a meeting** |
| Content | Text for people to read | Business signaling for programs to read | Calls, meeting reminders, being admitted from the waiting room, sub-meeting help requests |
| History | Yes, can be fetched page by page | No | No |
| Meeting controls | Chat can be disabled by the host (for everyone or a single member) | Not affected by disabling chat | Not applicable |
| Typical use | Text communication during the meeting | Custom buttons, business state sync | Pre-meeting pop-ups such as "Someone is calling you. Answer?" |

<Warning>
**The name "IM" is easy to misunderstand.** It is not a chat tool, nor a replacement for third-party instant messaging cloud services—it is a **notification path independent of meetings**, whose job is to push messages to users even before they have entered a meeting.

It **does not provide**: friend relationships, conversation lists, chat history, message roaming, groups, read receipts, or offline message queues. Fallback handling for users who stay offline for a long time (storing messages, forwarding to push notifications, SMS) must be done by your own business system.

For text communication in a meeting, use **in-meeting chat**, not IM.
</Warning>

An easy way to remember how the three relate: **in-meeting chat is for people, custom messages are for programs, and IM finds people outside the meeting.**

Under the hood, the two in-meeting message types use [SRTC's in-channel messages](/en/rtc/key-concepts#messaging), and out-of-meeting messages use SRTC's IM channel (out-of-channel messaging)—but you don't need to deal with this layer directly when using SMeeting.

---

## One user, multiple devices at once

SMeeting has built-in multi-device presence: when the same user enters a meeting from a phone and a computer at the same time, they are recognized as two member identities (distinguished by device type) and don't replace each other.

SMeeting handles this mapping automatically—under the hood, each device takes its own RTC identity, but in meeting terms they belong to the same user. You don't need to build the uid yourself.

---

## How terms differ from the RTC layer

SMeeting is built on SRTC, and the terms of the two layers are **not interchangeable**. Mixing them up will keep tripping you up when reading the API docs:

| Concept | Meeting layer (SMeeting) | RTC layer (SRTC) |
| --- | --- | --- |
| Space | room / meeting | channel |
| Entering and leaving | enter / exit | join / leave |
| People | members | channel user uid |
| Media | Managed by the meeting layer | track |

In the SMeeting APIs, you only see names with meeting semantics.

<Note>
In a few places you will see RTC-layer wording, and it is not a typo: error messages containing "频道" (channel), such as "该会话不在频道中" ("the session is not in the channel"), really come from the underlying RTC layer and are passed through to you as-is to help with troubleshooting.
</Note>

---

## Relationship to SRTC

When you use SMeeting, the underlying SRTC is still working, just wrapped inside; a normal integration doesn't need to call it directly.

If you find yourself repeatedly bypassing the meeting layer to operate the layer underneath, it usually means you should reconsider your choice—see [Choosing SRTC or SMeeting](/en/choose).

---

## Next steps

+ [Token and authentication](/en/meeting/token)—the grant flow and secret key security
+ [Quickstart](/en/meeting/quickstart)—an overview of the flows for the three integration options
