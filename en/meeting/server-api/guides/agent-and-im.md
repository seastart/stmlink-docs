---
title: "Device integration and IM"
description: "SMeeting reuses the SRTC device integration and IM endpoints as-is. Explains the two differences when calling them through SMeeting (domain and signing credentials) and why a device's target is the room number room_no, not the meeting_id."
---

For integrating SIP / H.323 / GB28181 and other devices, and for out-of-meeting IM messages, SMeeting doesn't provide a separate set of endpoints—
requests are forwarded as-is to the underlying SRTC, with exactly the same parameters and response structure.

So the documentation for these two groups of endpoints is the two SRTC pages:

<Columns cols={2}>
  <Card title="Device integration" href="/en/rtc/server-api/agent">
    Add, delete, update, and query devices, list gateways, invite devices, turn device audio and video on or off, and switch the video a device watches during the meeting
  </Card>
  <Card title="IM messages" href="/en/rtc/server-api/im">
    Out-of-meeting instant messages, IM grants, and device online status management
  </Card>
</Columns>

### Two differences when calling them

**Use the SMeeting domain**. The endpoint paths (`/server/v1/agent/...`, `/server/v1/im/...`) and parameters
stay the same; you just send the requests to the SMeeting address, with no need to integrate with the SRTC domain separately.

**Sign with the SMeeting app_id / app_key as well**. For the signing algorithm, see the [Overview](/en/meeting/server-api/overview).
Authentication is already done at the SMeeting layer when requests are forwarded.

### What to use as the target when a device enters the meeting

In SMeeting, the `no` parameter of inviting a device (`/server/v1/agent/invite`) is **the meeting room number `room_no`**,
not `meeting_id`. When the device enters, SMeeting looks up the current meeting of that room by its room number and brings the device into it;
passing `meeting_id` fails because no meeting can be found.

```json
{
  "agents": [
    { "type": 4, "contact": "37070000082008000001:34020000001320000001" }
  ],
  "no": "021890611"
}
```

Take each device's `type` and `contact` in `agents` from the [device list](/en/rtc/server-api/agent). For GB28181 devices,
`contact` uses the format `deviceId:channelId`. For all fields, see [Invite devices to the channel](/en/rtc/server-api/agent#invite-devices-to-the-channel).

For which meeting restrictions a device bypasses, how to remove it, how to detect a failed invitation, and how all this compares with calling users (`call-users`), see [Invite and remove](/en/meeting/server-api/guides/invite-and-kickout).

Each device can also carry four optional switches that decide what it sends first after entering and whether it plays the meeting audio: `camera_enabled` (send the camera picture, default `true`),
`mic_enabled` (the device microphone's audio goes into the meeting, default `true`), `share_enabled` (start sharing right away, default `false`), and
`speaker_enabled` (the meeting audio plays through the device speaker; SIP/H.323 default `true`, GB28181 defaults to the device gateway configuration, usually `false`).

+ They are **still subject to the meeting's disable policies**: if the meeting has disabled cameras / microphones / sharing, passing `true` won't turn them on
+ `share_enabled` only takes effect for stream-pulling devices such as RTSP / GB28181: on entering, the device requests sharing under the meeting's sharing exclusivity rules; if allowed, its main picture is published as the share; **if rejected (for example, someone else is already sharing), it falls back to a regular camera picture**
+ SIP/H.323 devices don't support `share_enabled: true`: if any one of them passes it, the whole invitation returns error code `1037`. To share, press the share button on the endpoint
+ `speaker_enabled` pairs with `mic_enabled`, one for the downlink and one for the uplink: with `false`, a SIP/H.323 endpoint doesn't hear the meeting audio; with `true`, the device gateway starts a GB28181 voice broadcast to a GB28181 device (requires broadcast enabled on the gateway, and a device that supports it with a speaker / sound column attached); ignored for stream-pulling devices such as RTSP. See ["Device speaker" in the SRTC device access guide](/en/rtc/server-api/guides/agents#device-speaker)
+ To switch the device speaker during the meeting, call SRTC's [Turn device speaker on or off](/en/rtc/server-api/agent#turn-device-speaker-on-or-off) directly (forwarded through SMeeting like turning device audio/video on or off; for `channel` / `uid`, see the next section)

### What to use for channel and user ID when operating a device in a meeting

Turning a device's audio/video or speaker on or off, sending DTMF, and [switching the video a device watches](/en/rtc/server-api/agent#switch-the-video-a-device-watches)
all target a device that is already in the meeting. In SMeeting, the `channel` parameter of these APIs is **the meeting ID `meeting_id`** (not the room number),
and `uid` is the device's in-meeting user ID (prefixed with `_agent_`, taken from the participant list or the member-joined callback).

When switching the video a device watches, set `sub_uid` to the `user_id` of the participant to watch:

```json
{
  "channel": "<meeting_id>",
  "uid": "_agent_co63jg6g54hu3b0xhtie",
  "sub_uid": "1001",
  "sub_tdesc": "camera_big"
}
```

### Making a device share its picture

In SMeeting, use the meeting-layer [Ask a member to share](/en/meeting/server-api/meet-admin#ask-a-member-to-share) to make a device share,
with `target_id` set to the device's in-meeting user ID:

+ This only applies to **stream-pulling devices** such as RTSP / GB28181 (only one picture): the device doesn't need to confirm; the server makes it start sharing directly, the main picture **switches** to being the share, and the camera picture is withdrawn; when the share ends, it switches back to the camera picture
+ **SIP/H.323 endpoints don't support starting sharing remotely**; targeting one returns error code `2126`. To share, press the share button on the endpoint to send dual-stream content (the camera picture keeps going); it counts as meeting sharing too
+ It is mutually exclusive with sharing by regular members (error `2104` if someone is already sharing), and the sharing status and the `share_state_change` callback are updated as usual
+ To end it, use [Stop the current share](/en/meeting/server-api/meet-admin#stop-the-current-share), which also makes the device stop sending the shared picture

Don't call SRTC's [Turn device sharing on or off](/en/rtc/server-api/agent#turn-device-sharing-on-or-off) directly: it only makes the device send / withdraw the picture, doesn't enforce exclusivity,
and doesn't update the meeting's sharing status. Shares an endpoint starts from its local share button, and shares from stream-pulling devices entering with `share_enabled`,
are allowed or rejected by SMeeting automatically under the same exclusivity rules; you don't need to handle them.
