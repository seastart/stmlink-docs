---
title: "Device integration and IM"
description: "SMeeting reuses the SRTC device integration and IM endpoints as-is. Explains the two differences when calling them through SMeeting (domain and signing credentials) and why a device's target is the meeting_id, not the room number."
---

For integrating SIP / H.323 / GB28181 and other devices, and for out-of-meeting IM messages, SMeeting doesn't provide a separate set of endpoints—
requests are forwarded as-is to the underlying SRTC, with exactly the same parameters and response structure.

So the documentation for these two groups of endpoints is the two SRTC pages:

<Columns cols={2}>
  <Card title="Device integration" href="/en/rtc/server-api/agent">
    Add, delete, update, and query devices, list gateways, invite devices, and turn device audio and video on or off during the meeting
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

The `no` parameter of inviting a device (`/server/v1/agent/invite`) is the target channel name. In SMeeting,
**the meeting ID (`meeting_id`) is the channel name at the RTC layer**, so pass `meeting_id` directly as `no`.

Note that it's not the room number `room_no`—that is the number users enter in the client, and one room can host several meetings
one after another. Only `meeting_id` uniquely identifies the specific meeting the device should enter.
