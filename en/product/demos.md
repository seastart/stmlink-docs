---
title: "Try it online"
description: "What the two web demos let you try, with screenshots: the meeting demo (scheduling, meeting controls, permissions, inviting members and devices, chat, layouts, history) and the RTC demo (calls, multi-user meetings, push-to-talk, multi-channel, remote monitoring), and how to get an account."
---

We've prepared two web demos you can try in a browser without installing anything.
**To get the demo URL and account, [contact us](https://www.stmlink.com/en/contact)**, and we'll set up a dedicated demo account for you.

---

## Meeting demo

A complete meeting product built on the SMeeting conferencing SDK, suited to evaluating meeting features and interactions. It's also the
UI that [low-code integration with UI](/en/meeting/ui-sdk/server-integration) lets you embed directly in your system.

### Before the meeting

The home page after login has three entry points—"Join meeting", "Instant meeting", and "Schedule meeting"—with today's meetings and meeting history on the left.

![Meeting demo home](/zh/product/images/demo-meeting-home.jpg)

**Scheduled meeting**: set the meeting name, start time, duration, and meeting mode, upload meeting materials, and pick invitees from contacts.
Advanced options let you turn on "Invitees only", "Waiting room", "Allow members to enter before the host", and a meeting password.

![Scheduled meeting](/zh/product/images/demo-meeting-schedule.jpg)

**Instant meeting**: give it a name, choose whether the microphone, camera, and speaker are on when you enter, and start right away.

### During the meeting

Bottom toolbar: speaker, microphone, camera, share screen, record, members, chat, sub-meetings, invite, sign-in, and settings.
In the upper-left corner you can lock the meeting and view quality monitoring; in the upper-right corner you switch layouts.

![In-meeting toolbar](/zh/product/images/demo-meeting-toolbar.jpg)

**Member management and permissions**: view members by "Waiting room / In meeting / Not entered". The host can mute all and unmute all,
set whether members can unmute themselves and turn on their cameras, and choose who can share the screen.

![Member management and permissions](/zh/product/images/demo-meeting-members.jpg)

**Invite**: invite members from contacts by department (they receive a meeting reminder), or switch to "Invite device" to bring meeting-room endpoints and surveillance cameras into the meeting
(to connect devices, see [Room Connector](/en/product/device-access/overview)).

![Invite members](/zh/product/images/demo-meeting-invite.jpg)

![Invite devices](/zh/product/images/demo-meeting-invite-device.jpg)

**Chat**: in-meeting text chat, with file sending.

![In-meeting chat](/zh/product/images/demo-meeting-chat.jpg)

**Layout**: grid views (default, full screen, split in two, 4 tiles, 5 tiles, and more) and speaker views (small windows on the right, small windows on top, L-shaped layout).

![Switch layouts](/zh/product/images/demo-meeting-layout.jpg)

There are also **sub-meetings** (split into a given number of groups), **sign-in** (start a timed sign-in and view sign-in records), **cloud recording**, and more.

### After the meeting

Meeting history shows each meeting's time, meeting ID, type, materials, and invitees, and you can **Restart** the same meeting with one click.

![Meeting history](/zh/product/images/demo-meeting-history.jpg)

---

## RTC demo

Shows the underlying capabilities of the SRTC audio and video SDK, suited to evaluating call quality and various real-time scenarios.

![RTC demo](/zh/product/images/demo-rtc-home.jpg)

| Scenario | What you can try |
| --- | --- |
| **Call** | Enter the other user's identifier to start a one-to-one audio / video call; answer, decline, and hang up |
| **Multi-user meeting** | Multi-user audio and video, screen sharing, whiteboard sharing, chat, transcription (live captions), cloud recording, local recording, network quality, active speaker indication, and inviting members and devices |
| **Push-to-talk** | Hold-to-talk intercom, in-channel text messages, and per-speaker voice recording, suited to dispatch scenarios |
| **Multiple channels** | Join several channels at once, and listen and speak in each separately |
| **Remote monitoring** | A supervisor console views several endpoints in a 9-tile grid; click to listen, hold to talk for directed intercom; monitored Android endpoints join the channel and publish without user interaction |

**Call**: enter the other user's identifier to call; once they answer, you're in a one-to-one call.

![One-to-one call](/zh/product/images/demo-rtc-call.jpg)

**Multi-user meeting**: the top shows the channel and network quality score (MOS); the bottom toolbar has speaker, audio, video, share screen, share whiteboard,
cloud recording, local recording, invite (members or devices), chat, and transcription.

![Multi-user meeting](/zh/product/images/demo-rtc-room.jpg)

**Push-to-talk**: after you open it, you automatically join the channel with listening always on; hold the button (or hold the space bar) to talk. In-channel text messages are on the right.
You can turn on voice recording, which records each utterance as one segment; view the recordings in the admin console.

![Push-to-talk](/zh/product/images/demo-rtc-intercom.jpg)

**Remote monitoring supervisor console**:

![Remote monitoring supervisor console](/zh/product/images/demo-rtc-monitor.jpg)

---

## Tips

+ Use **two devices** (or two browsers) to join the same meeting / channel so you can see them interact
+ We recommend the latest Chrome or Edge; allow camera and microphone access the first time
+ To try **meeting-room endpoint and surveillance camera integration**, contact us to arrange a device demo
