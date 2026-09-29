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
For `uid`, use the device's user ID in the channel (prefixed with `_agent_`, from the user list or the `user_join` callback).
If you don't pass `uid`, the operation applies to all devices in the channel.

If you subscribe to the `agent_operate` callback, both operations first ask your backend, and a non-zero return rejects them.

## Device type numbers

`list-invite` and `invite` use numeric types, which are a different scheme from the `type` strings:

| Number | Meaning | Corresponding `type` |
| --- | --- | --- |
| 2 | SIP | `ipsip` / `regsip` |
| 3 | H.323 | `iph323` / `regh323` |
| 4 | GB28181 surveillance | `gb28181` |
| 5 | RTSP stream pull | `rtsp` |

The `device_type` of users in the channel is a third numbering scheme (the agent range starting at `80`); see the [Callback events guide](/en/rtc/server-api/guides/callbacks).
