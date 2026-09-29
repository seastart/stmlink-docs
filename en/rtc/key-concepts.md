---
title: "Key concepts"
description: "The SRTC model of channels, users, and tracks: when channels open and are destroyed, how uid maps to channels, explicit subscription, and in-channel vs. out-of-channel IM messages. Read before calling any SRTC API."
---

SRTC does only three things: **real-time message delivery, state sync, and audio and video transport**. It has no user system and no business rules—those are up to you. The whole model has just three objects:

```text
Channel
 └── User
      └── Track
```

---

## Channel

A channel is an audio and video space; users in the same channel can send and receive audio and video with each other. You define the channel name and channel info yourself.

### Opening and destruction

+ When the first user joins, the channel **opens automatically** if it isn't open yet
+ You can also open it manually in advance—useful when you need to set channel properties beforehand
+ If no one joins within 2 hours of the channel opening, or 2 hours after the last user leaves, the channel is **destroyed automatically**

<Tip>
If channel properties need to be in place before the first person arrives (for example, layout configuration or business flags), use the server API to open the channel manually in advance and write the properties, to avoid the brief inconsistency of "join first, then change properties".
</Tip>

---

## User

**SRTC has no user system of its own.** You define all user information; SRTC only trusts the `uid` issued in the token.

Two rules govern how a uid relates to channels:

+ One uid can join **multiple different** channels at the same time
+ When the same uid joins the **same** channel again, the later join replaces the earlier one

Usually you can use your system's user ID directly as the uid. If the same business user needs multiple coexisting identities in one channel (for example, online on multiple devices at once), append a sessionId or device identifier to the uid.

If you need a restriction like "a uid can only be in one channel at a time", enforce it in your backend—SRTC doesn't impose this constraint.

For how uids are issued, see [Token and authentication](/en/rtc/token).

---

## Track

Each audio stream and each video stream is a track. A user can:

+ Publish multiple local tracks (camera, screen sharing, microphone, and more)
+ Subscribe to multiple remote tracks

SRTC only transports the media data in tracks; **you define what each track means for your business**—use the `desc` field to mark whether a track is the camera or screen sharing, and the receiver decides how to render it accordingly.

### Subscription is explicit

Joining a channel doesn't mean you automatically receive all video. You need to subscribe to the tracks you want, or turn on auto-subscribe. This design lets you control bandwidth as needed—for example, a 3×3 grid subscribes only to the nine tracks on the current page and switches when the user pages.

---

## Messaging

Besides audio and video, SRTC provides two messaging paths. They differ in only one way: **whether the user is in the channel when sending and receiving messages.**

| | In-channel custom messages | Out-of-channel IM messages |
| --- | --- | --- |
| Prerequisite | Joined the channel | IM enabled (`enableIm`); no need to be in any channel |
| How to send | Sent directly by the client SDK | **Only sent by your backend calling the server API** |
| How to receive | Channel event `custom_msg` | IM event `im_msg` |
| Typical use | In-call signaling such as raise hand, whiteboard sync, and status broadcasts | Pre-call ringing, meeting invitations, notifications and reminders |
| Lifecycle | Ends with the channel | Independent of channels; received as long as the connection is up |

<Warning>
**IM here is not a chat product.** The name suggests WeChat, customer service systems, or third-party IM cloud services, but SRTC's IM is just a **real-time messaging path outside of channels**, used to push messages to a user before they join a channel.

It **does not provide** conversation lists, chat history, message roaming, groups, read receipts, or offline message queues. Messages aren't persisted—the only guarantee is that messages missed during a disconnect are resent after reconnecting. Fallbacks for a recipient who is offline for a long time (storing in a database, forwarding as push notifications, SMS) must be handled on your side.
</Warning>

Requiring sends to go through your backend is intentional: because messages pass through your server first, you get the chance to apply business rules such as sensitive-word filtering, rate limiting, and permission checks.

The same uid can connect to IM on multiple devices at once, and each connection has its own `sid`—so "send to a person" and "send to a device" are two different things.

+ Client usage: [Web channel messages](/en/rtc/web/channel-messages)
+ Server API: [Server API · IM messages](/en/rtc/server-api/im)

---

## Relationship to SMeeting

If what you need are **meeting rules** such as host, raise hand, and mute all, they aren't in SRTC—that's the scope of [SMeeting](/en/meeting/overview). SRTC gives you the transport; you write the rules yourself.

For how to choose between them, see [Choosing SRTC or SMeeting](/en/choose).

---

## Next steps

+ [Token and authentication](/en/rtc/token)—the step you must understand before integrating
+ Choose your platform and start integrating: [Web](/en/rtc/web/integration) · [Android](/en/rtc/android/integration) · [Windows](/zh/rtc/windows/integration) (Chinese) · [Swift](/en/rtc/swift/integration) · [iOS](/zh/rtc/ios/integration) (Chinese) · [C](/en/rtc/capi/integration)
