---
title: "Reference backend implementation"
description: "What your backend should wrap around the SRTC server API and where to draw permission boundaries, plus conventions for channel and user props, custom messages, when to use IM instead of in-channel messages, and track desc values. Read this when designing your own backend."
---

**Your backend** receives requests from your client, makes business decisions, and then calls the SRTC server API with `app_key`.

This page is a reference for building your own backend, which calls the [SRTC server API](/en/rtc/server-api/overview).

## Why this layer is required

The SRTC server API has **the highest authority across the board**. Every request must be HMAC-signed with `app_key`, and **`app_key` must never appear on the client**
—if it leaks, others can use your app's identity to join any channel and remove any user.

So only your backend can do the following:

| Capability | SRTC server API |
| --- | --- |
| Issue channel join tokens | `channel/grant` |
| Channel controls (removing users, changing user properties) | `channel/kick-user`, `channel/update-user` |
| Starting and stopping recording, live streaming, voice recording, and transcription | `mcu/*`, `talkrec/*`, `asr/*` |
| Device integration (SIP / GB28181 surveillance, etc.) | `agent/*` |

The client only gets a token to join the channel and sends and receives streams; everything else goes through your backend.

## One endpoint per capability

Usually each of your business endpoints maps to one capability, and your backend code decides which SRTC server API to call:

```text
POST /your-backend/room/start-record   →  calls mcu/start internally
POST /your-backend/room/kick           →  calls channel/kick-user internally
```

Each endpoint should validate its parameters and check permissions.

## Where to check audio and video permissions

For turning the camera or microphone on or off, sharing, and so on, wrap them as backend "endpoints"—`/open-video`, `/open-audio`, `/start-share`. They only check permissions and don't need to call any SRTC server API.

In effect, before your client turns on the camera, it first asks your backend
"is this user allowed to turn on video right now?" (whether the call has started, whether the host has disabled their video,
whether the concurrency limit has been exceeded). If not, the backend returns an error code, and the client shows the user a message accordingly.

## props conventions

SRTC channels and users each carry a `props` extension field. You define its content; the SRTC server only stores and broadcasts it.
For example:

**Channel props**—shared state for the whole channel

```json
{
  "share_state": true,
  "share_uid": "1001",
  "share_track": 3
}
```

**User props**—state of a single user

```json
{
  "avatar": "https://example.com/avatar.jpg",
  "audio_state": true,
  "video_state": false
}
```

Change `props` with [Update user info](/en/rtc/server-api/channel#update-user-info) or
[Update channel info](/en/rtc/server-api/channel#update-channel-info). The server broadcasts a change event to everyone in the channel,
and clients refresh their UI accordingly. **This is the easiest way to sync state such as "who is sharing"**,
without building a messaging path of your own.

## Custom message conventions

When you need to send a one-time notification (rather than persistent state), use
[Send a custom message](/en/rtc/server-api/channel#send-a-custom-message). You define the message body structure entirely;
you can follow a two-part `action` + `content` format:

```json
{ "action": "chat",        "content": "Message text" }
{ "action": "video_open",  "content": { "uid": "1001" } }
{ "action": "video_close", "content": { "uid": "1001" } }
{ "action": "audio_open",  "content": { "uid": "1001" } }
{ "action": "audio_close", "content": { "uid": "1001" } }
{ "action": "share_start", "content": { "uid": "1001", "track": 3 } }
{ "action": "share_stop",  "content": { "uid": "1001" } }
```

**Use props for state, custom messages for actions**: props describe "what things look like now", and users who join later can read them too;
custom messages describe "what just happened", and only users online at the time receive them.

## IM messages vs. in-channel custom messages

Both can "send a message to someone", so they're easy to confuse. **The dividing line is whether the recipient is in the channel.**

| | In-channel custom messages | IM messages |
| --- | --- | --- |
| Endpoint | [Send a custom message](/en/rtc/server-api/channel#send-a-custom-message) | [Send an IM message](/en/rtc/server-api/im#send-an-im-message) |
| Prerequisite | Sender and recipients are **all in the same channel** | The device only needs to be online on IM; **it doesn't have to be in any channel** |
| Required | `channel` | No concept of a channel |
| Addressing | `ruids`; **leave empty to broadcast to the whole channel** | `ruids` by user / `rsids` by device; **recipients must be named** |
| Credential | Channel join token | A separate IM token (`im/grant`) |

In short: **use custom messages for things inside the channel, and IM for bringing people into the channel.**

### When only IM works

The key is that **the other party hasn't joined the channel yet**, so channel messages can't reach them at all. These are the two most typical scenarios.

#### Calling: bringing someone into the channel

1. The caller asks your backend to start a call. The backend generates a channel name and notifies the callee over IM:

```json
{
  "action": "call_invite",
  "content": { "channel": "room-a1b2c3", "caller": "1001", "name": "Alice" }
}
```

2. The callee's device rings when it receives this. Answering, declining, or being busy each sends an IM back to the caller:

```json
{ "action": "call_answer", "content": { "channel": "room-a1b2c3" } }
{ "action": "call_refuse", "content": { "channel": "room-a1b2c3" } }
{ "action": "call_busy",   "content": { "channel": "room-a1b2c3" } }
```

3. After answering, each side gets a token and joins the channel. **From then on, interactions (mute, sharing, chat) should switch to in-channel
   custom messages**—the users are already in the channel, so there's no need to go through IM.

Call timeouts and caller cancellation work the same way, each with its own message (`call_timeout` / `call_cancel`); you choose the command names.

#### Having a terminal join the channel silently

A controlled terminal has no interactive UI. Your backend sends a command to have it join the channel and publish on its own:

```json
{
  "action": "monitor_start",
  "content": { "channel": "mon-9527", "audio": true }
}
{ "action": "monitor_stop", "content": {} }
```

When the terminal receives `monitor_start`, it gets a token, joins the specified channel, and publishes its camera stream, with no user action needed.
It isn't in any channel before it receives this message, so IM is the only way.

#### Others

Cross-channel notifications (messages to people who aren't in this channel), system announcements, and so on—any scenario where
"the recipient isn't in this channel" belongs to IM.

### Three capabilities unique to IM

+ **Delivery by device**: one uid may be online on several devices at once (phone + PC). `rsids` delivers to a specific device,
  while `ruids` sends to all of that user's online devices. Channel messages don't have this dimension
+ **Query online devices**: [Get users' online devices](/en/rtc/server-api/im#get-users-online-devices),
  so you can check whether the other party is online before calling
+ **Force a device offline**: [Force an IM device offline](/en/rtc/server-api/im#force-an-im-device-offline), used when a later login replaces an earlier one

Devices coming online and going offline also trigger `im_connect` / `im_disconnect` callbacks to your backend, which you can use to track online status.

<Note>
For messages that **must not be lost**, such as calls and invitations, remember to set `important` to `true`—they are resent after a reconnect.
Ordinary state sync doesn't need it; the cost is slightly higher latency. Both endpoints have this field.
</Note>

## Tracks

Each track a client publishes carries a `desc` description, which the server and other clients use to tell what it's for:

| `desc` | Meaning |
| --- | --- |
| `mic` | Microphone |
| `camera_big` | Camera high stream |
| `camera_small` | Camera low stream (simulcast secondary layer) |
| `screen` | Screen sharing |

When subscribing, pick the one you need by `desc`—for example, a 3×3 monitoring grid subscribes only to `camera_big`.
