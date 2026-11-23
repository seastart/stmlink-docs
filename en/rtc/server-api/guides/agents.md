---
title: "Device integration guide"
description: "How to register SIP / H.323 phones, GB28181 surveillance devices, and RTSP streams through a device gateway and bring them into a channel: the six integration types, GB28181 channels, inviting devices, and controlling them in the channel. Read this before integrating hardware devices."
---

Device integration brings things that don't run our SDK into the channel: the SIP phone in a meeting room, the GB28181 camera on the wall,
an RTSP stream. They join through a **device gateway** acting on their behalf, and appear in the channel as a regular user (with a `uid` prefixed with `_agent_`).

For the parameters and response structure of each endpoint, see [Device integration](/en/rtc/server-api/agent).

## Three steps

```text
1. Get a gateway              POST /server/v1/agent/list-gw?type=regsip   → gw
2. Register the device        POST /server/v1/agent/create?type=regsip    → device ID
3. Bring it into the channel  POST /server/v1/agent/invite                → wait for the user_join callback
```

Devices don't connect to RTC directly. Each one is attached to a gateway, which handles signaling and media conversion. So **step 1 can't be skipped**—
a wrong `gw` keeps the device from coming online.

## Six integration types

`type` is a **URL query parameter** (`?type=regsip`), not part of the request body. The request body fields of [Add a device](/en/rtc/server-api/agent#add-a-device) and
[Update a device](/en/rtc/server-api/agent#update-a-device) change with it:

| `type` | Description | Type-specific required fields |
| --- | --- | --- |
| `ipsip` | SIP phone, direct IP | `uri` (`ip:port`)|
| `regsip` | SIP phone, registration mode | `username` (must not contain `:`), `auth_pwd` |
| `iph323` | H.323 endpoint, direct IP | `uri` (`ip:port`)|
| `regh323` | H.323 endpoint, registration mode | `username` (**numeric short number only**), `auth_pwd` |
| `gb28181` | GB28181 surveillance device | `sip_no` (18–20 digits), `auth_pwd`, optional `subjects` |
| `rtsp` | RTSP stream pull | `uri` (must start with `rtsp`), optional `transport_type` (`UDP` default / `TCP`)|

The table lists only the fields **specific** to each type. For the full request body of each value, see
[Add a device](/en/rtc/server-api/agent#add-a-device) (with a section per `type`).
All types require `display_name` (display name) and `gw` (device gateway); `remark` is optional.
For types other than `rtsp`, also note: registration mode requires the device to register with the gateway itself, while with direct IP we connect to the device.
Which one to choose depends on whether we can reach the network the device is on.
To be notified when a registration-mode device comes online or goes offline, subscribe to the `agent_online` / `agent_offline` callbacks; see the [Callback events guide](/en/rtc/server-api/guides/callbacks).

When updating a device, `type` **must match the type the device was registered with**; you can't use it to turn a SIP device into an RTSP one.
To change the integration type, delete the device and register it again.

## GB28181 channels

A GB28181 device (an NVR or a dome camera) may have several camera channels, and each GB28181 channel is a separate video in the SRTC channel.
`subjects` is a map of "channel number → channel name":

```json
{"50010700001320000001": "Guest seats", "50010700001320000002": "Audience seats"}
```

There are three ways to maintain them, with the same result:

+ Pass them all at once in `subjects` when registering the device
+ Add or rename them one by one later with [Set a GB28181 device channel](/en/rtc/server-api/agent#set-a-gb28181-device-channel)
+ Don't want to build the numbers yourself → first call [Generate a GB28181 channel number](/en/rtc/server-api/agent#generate-a-gb28181-channel-number) to generate them according to the standard, then register

Likewise, the device's own `sip_no` can be obtained with [Generate a GB28181 device SIP number](/en/rtc/server-api/agent#generate-a-gb28181-device-sip-number).
Both "generate" endpoints **only return a number and don't save anything**; you still have to register it yourself.

For a GB28181 camera to register, the device must be configured with the "upper-level platform" info (SIP number, domain, IP, port)—
get these values from [List device gateway platform info](/en/rtc/server-api/agent#list-device-gateway-platform-info).

## Inviting devices and controlling them in the channel

Get `agents[].type` and `contact` for [Invite devices to the channel](/en/rtc/server-api/agent#invite-devices-to-the-channel) from
[List devices](/en/rtc/server-api/agent#list-devices). Each channel of a GB28181 device is a separate entry, and its `contact` is the channel number.

**Joining is asynchronous**: a successful response only means the invitation was sent. The device is actually online only when the `user_join` callback arrives.
If you subscribe to the `agent_join` callback, you must also return `sid` in it, or the device can't join—see the [Callback events guide](/en/rtc/server-api/guides/callbacks).

Devices can't turn their own microphone and camera on or off; only the server can send these commands:
[Turn device video on or off](/en/rtc/server-api/agent#turn-device-video-on-or-off) / [Turn device audio on or off](/en/rtc/server-api/agent#turn-device-audio-on-or-off).
Whether the meeting audio plays through the device speaker is controlled with [Turn device speaker on or off](/en/rtc/server-api/agent#turn-device-speaker-on-or-off) (see "Device speaker" below).
For `uid`, use the device's user ID in the channel (prefixed with `_agent_`, from the user list or the `user_join` callback).
If you don't pass `uid`, the operation applies to all devices in the channel.

If you subscribe to the `agent_operate` callback, both operations first ask your backend, and a non-zero return rejects them.

### Initial switches when inviting

When you [invite devices to the channel](/en/rtc/server-api/agent#invite-devices-to-the-channel), each item in `agents[]` can carry four optional switches that decide what the device sends first after joining and whether it plays the meeting audio:

| Parameter | Default | Meaning |
| --- | --- | --- |
| `camera_enabled` | `true` | Whether to send the camera picture after joining |
| `mic_enabled` | `true` | Whether the device microphone's audio goes into the meeting after joining (uplink) |
| `share_enabled` | `false` | Whether to start sharing right after joining |
| `speaker_enabled` | SIP/H.323 `true`; GB28181 takes the device gateway configuration (default `false`) | Whether the meeting audio plays through the device speaker (downlink); ignored for stream-pulling devices such as RTSP |

+ `mic_enabled` and `speaker_enabled` are a pair: the former decides whether the meeting hears what the device says, the latter whether the device side hears what is said in the meeting
+ The first three switches only express "want it on" and are **still subject to the meeting's disable policies**: if the meeting has disabled cameras, `camera_enabled: true` won't turn the camera on (your backend rejects it through the `agent_operate` callback)
+ `share_enabled` only takes effect for **stream-pulling devices** such as RTSP / GB28181: after joining, the device first requests sharing through `agent_operate` (`agent_start_share`); if allowed, its main picture is published as screen sharing; **if rejected, it falls back to publishing a regular camera picture** (no video if `camera_enabled` is `false`)
+ SIP/H.323 devices **don't support** `share_enabled: true`: if any one of them passes it, the whole invitation returns error code `1037` and no device is called. To share, press the share button on the endpoint (see the next section)

### Device sharing

A device's share is published in the channel as screen sharing (`screen`); clients and the MCU composite layout treat it like regular screen sharing. The two kinds of devices behave differently:

+ **Stream-pulling devices such as RTSP / GB28181** (only one picture): sharing **switches** the main picture to be published as screen sharing, and the camera picture is withdrawn; stopping the share switches back to the camera picture
+ **SIP/H.323 endpoints**: sharing **can't be started remotely from the platform**; it can only be started by pressing the share button on the endpoint. The dual-stream content is published as screen sharing, and the camera picture keeps going

A share can be started in two ways:

+ **The endpoint presses its local share button** (SIP/H.323 only): your backend is asked first through the `agent_operate` callback (`op_type` is `agent_start_share`); a non-zero return rejects it and the endpoint receives a rejection. When the endpoint stops sharing, the callback is sent with `agent_stop_share`. See the [Callback events guide](/en/rtc/server-api/guides/callbacks)
+ **Started from the server**: [Turn device sharing on or off](/en/rtc/server-api/agent#turn-device-sharing-on-or-off), with `enabled` set to `true` to start and `false` to stop. `true` only works for stream-pulling devices and returns error code `1037` for SIP/H.323 endpoints; `false` works for both kinds, and withdraws dual-stream content a SIP/H.323 endpoint started with its share button. This API **doesn't enforce sharing exclusivity**; if only one person may share in the channel at a time, check this in your backend before calling

### Device speaker

`speaker_enabled` decides whether the meeting audio (the channel mix) is sent to the device and played through its speaker. The effect by device type:

| Device | When omitted | On (`true`) | Off (`false`) |
| --- | --- | --- | --- |
| SIP/H.323 endpoint | `true` (the endpoint always hears the meeting audio) | Sends the meeting audio to the endpoint | The endpoint doesn't hear the meeting audio; the gateway sends silent frames instead, so the media connection stays up |
| GB28181 camera | Takes the device gateway configuration (default `false`) | The gateway starts a GB28181 **voice broadcast** to the device, and the meeting audio plays through the device's speaker / sound column | Ends the voice broadcast |
| Stream-pulling devices such as RTSP | — | No speaker: ignored when inviting; in the channel the call succeeds but has no effect | Same |

A GB28181 voice broadcast requires all of the following:

+ Voice broadcast is enabled on the device gateway (for private deployments, turn it on in the gateway configuration)
+ The device itself supports GB28181 voice broadcast and has a speaker or sound column attached
+ The gateway only sends G.711A (PCMA) audio to the device

To switch it in the channel, use [Turn device speaker on or off](/en/rtc/server-api/agent#turn-device-speaker-on-or-off) (`uid`, `channel`, `enabled`). For GB28181 the broadcast is started **asynchronously**:
a successful response only means the command was sent; if the device refuses the broadcast (not supported, no speaker attached, etc.), this isn't reflected in the API result and only shows up in the device gateway logs.

## Device type numbers

`list-invite` and `invite` use numeric types, which are a different scheme from the `type` strings:

| Number | Meaning | Corresponding `type` |
| --- | --- | --- |
| 2 | SIP | `ipsip` / `regsip` |
| 3 | H.323 | `iph323` / `regh323` |
| 4 | GB28181 surveillance | `gb28181` |
| 5 | RTSP stream pull | `rtsp` |

The `device_type` of users in the channel is a third numbering scheme (the agent range starting at `80`): devices joining through the device gateway report their actual type, which is `80` plus the number in the table (SIP `82`, H.323 `83`, GB28181 `84`, RTSP `85`); see the [Callback events guide](/en/rtc/server-api/guides/callbacks).

## Parameter naming conventions

Switch-type parameters are distinguished by suffix: `xxx_disabled` means **not allowed** (a permission / policy, such as the meeting forbidding cameras), `xxx_state` is **the current state as queried**, and `xxx_enabled` means **on / off** (a command, or the desired initial value when inviting, still subject to `_disabled`).
