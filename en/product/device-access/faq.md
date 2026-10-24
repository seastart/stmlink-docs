---
title: "Room Connector FAQ"
sidebarTitle: "FAQ"
description: "Troubleshooting checklist for Room Connector, organized by symptom: endpoints that won't register or can't dial in, black screen or one-way audio after entering, GB28181 cameras offline or failing invitations, RTSP streams with no video, and devices rejected for exceeding concurrency."
---

First confirm two basic things—many problems are solved right here:

1. **Are the ports open?** The signaling ports and the RTP port range between devices and the device gateway must all be open; see [Network and port requirements](/en/product/deploy/ports#device-gateway)
2. **Did you choose the right gateway for the device?** The "Device gateway" selected when registering the device must be the gateway the endpoint actually registers to or can reach

---

## Endpoint can't register

| Check | Description |
| --- | --- |
| Address and port | The endpoint must use the **device gateway address**, SIP port 5060, H.323 gatekeeper port 1719 |
| Username format | H.323 usernames **must be digits only** (E.164 short number); SIP usernames can't contain colons |
| Username, password | The authentication username and password on the endpoint exactly match the console account |
| Gateway selection | The "Device gateway" selected for the console account is the one the endpoint registers to |
| Network | `ping` the device gateway address from the endpoint's network; across NAT, registration goes endpoint → gateway, so the gateway address must be reachable from the endpoint |

---

## Endpoint can't dial in to the meeting

| Symptom / check | Cause and fix |
| --- | --- |
| An unregistered endpoint dialed only the meeting ID | Unregistered endpoints must dial `meetingID@deviceGatewayAddress` |
| The meeting ID is right but it still can't enter | The meeting must **exist and not have ended**; device dial-ins always go to the app specified at deployment, so a meeting outside that app can't be found |
| Rejected as soon as it dials | The device gateway has the incoming-call IP allowlist on, and the endpoint's IP isn't on it |
| Only SRTC is used, with no meeting layer | Dial the **channel name**, not a meeting ID |

---

## Endpoint entered the meeting but can't see the meeting's video

The endpoint sees the whole meeting composited by the MCU. Check in this order:

1. **Is the MCU deployed and running?** Without the MCU, the endpoint receives no video. The MCU's heartbeat is visible under **Operations management → Media gateways** in the admin console
2. **Is the RTP port range open?** The device gateway's RTP port range (default 58000-59000/UDP) must be fully open to the endpoint
3. **Is the address the gateway gives the endpoint correct?** The "device access gateway IP" set at deployment is written into call signaling, and the endpoint sends media back to that address.
   When the endpoint reaches the gateway through NAT, this must be the post-NAT address, with **same-port-number** mapping
4. **Does the endpoint send and receive on different ports?** Some endpoints (common among custom models for courts and government agencies) receive and send on different ports,
   so "the meeting can see the endpoint, but the endpoint can't see the meeting". RTP address learning must be turned off on the device gateway; contact us to adjust the configuration

---

## The meeting can't see the endpoint's video or hear its audio

| Check | Description |
| --- | --- |
| Endpoint video codec | The endpoint must use **H.264** (the default on most endpoints); audio G.711A |
| Endpoint camera and microphone | The endpoint itself isn't muted and its video isn't off; check whether the host turned off this endpoint's audio or video during the meeting |
| Ports | Same as above: the RTP port range must be open |

---

## GB28181 camera won't connect

| Symptom / check | Cause and fix |
| --- | --- |
| Registration status on the camera stays "Offline" | The platform info (SIP server ID, domain, address, port 5070) must exactly match "Platform info" in the console; the camera must be able to reach port 5070 on the gateway |
| Device id, password | The camera's "SIP username / authentication ID" = "Device id" in the console; passwords match on both sides |
| Registers, then goes offline after a while | Change the camera's **heartbeat interval to 30 seconds** |
| Invitation reports "Device is busy" | This message doesn't mean the device is busy—almost always **the camera hasn't registered**. Confirm the console status is "Online" before inviting |
| Device online, but no video after inviting | You invite a **GB28181 channel**: confirm the channel id matches the camera's "Video Channel Encoding ID"; set the camera's codec to H.264 |

---

## RTSP stream shows no video

| Check | Description |
| --- | --- |
| Does the URL play? | First open the same URL in VLC; if it doesn't play, the problem is the URL, account, or device |
| Can the gateway reach it? | The device gateway pulls the stream, so the gateway's server must be able to reach the camera's port 554 |
| Transport | If UDP is blocked or loses many packets, change it to **TCP** in the console |
| Stream codec | H.265 is transcoded in real time; with many streams the gateway may run out of CPU, so switch the camera to H.264 |

---

## Device rejected, concurrency limit exceeded

Each device in a meeting uses **one user concurrency** and **one device concurrency** slot. Once the quota is used up, new devices can't enter;
expand the license or have unused devices exit first. The device gateway itself also needs a license file; without an imported license, devices can't connect properly.

---

## Still not working

When contacting us, provide: device brand and model, integration method (SIP / H.323 / GB28181 / RTSP, registration or direct IP),
when the problem occurred, and the meeting ID. We can locate the issue from the device gateway's logs.
