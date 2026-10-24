---
title: "Soft SIP / H.323 endpoint"
sidebarTitle: "Soft SIP / H.323 endpoint"
description: "An Android app that turns large displays, all-in-one units, and boxes into standard SIP / H.323 video endpoints: point-to-point calls, registration to a SIP server or gatekeeper, entering our meetings, screen sharing, and whiteboard. Covers features, setup, and how to get it."
---

The **Soft SIP / H.323 endpoint** is an Android app (titled "会议室连接器" (*Room Connector*) inside the app). Install it on a meeting room's Android large display, all-in-one unit, or set-top box, and that device becomes a
**standard SIP / H.323 video conferencing endpoint**—without buying a separate hardware endpoint, it can call and be called by endpoints and
MCUs from brands such as Huawei and Kedacom, and enter meetings on our platform.

![Soft endpoint home](/zh/product/terminals/images/softsip-home.jpg)

---

## Use cases

+ The meeting room already has an Android large display / all-in-one unit and you want to connect it to an existing SIP / H.323 video conferencing system at low cost
+ A video wall or command-center display needs to join a higher-level organization's video conference as an endpoint
+ Use it with our meeting platform: register to the device gateway and dial the meeting ID to enter; see [Room Connector](/en/product/device-access/sip-h323)

---

## Main features

| Feature | Description |
| --- | --- |
| **Point-to-point calls** | Choose SIP or H.323 and enter the other endpoint's IP, E.164 number, or name to call; audio + video or audio only |
| **Answer incoming calls** | Answer / decline from the incoming-call pop-up; **auto-answer** is available for unattended large displays |
| **Registration** | Register to a SIP server or H.323 gatekeeper, with H.460 NAT traversal |
| **In-meeting controls** | Mute, video on/off, switch camera, mirror video, speaker / equal-split layouts |
| **Screen sharing** | Start and receive sharing (available on H.323 calls) |
| **Whiteboard** | Start a whiteboard during the meeting or join with a service code; pen, text, shapes, undo, and save |
| **Call history** | One-tap redial |

**In-meeting view**:

![In-meeting view](/zh/product/terminals/images/softsip-meeting.jpg)

**Whiteboard**:

![Whiteboard](/zh/product/terminals/images/softsip-whiteboard.png)

---

## How to use it

1. Install the app and complete **software activation** (we provide the activation details)
2. Configure **Settings** as needed:

   | Settings page | Contents |
   | --- | --- |
   | SIP service | Whether to register, server address, port, account, password |
   | 323 service | Gatekeeper address, E.164 number, H.460 NAT traversal, port |
   | Whiteboard service | Whiteboard server address |
   | Network | Local network information |
   | General | Display name, auto-answer, get logs |

   ![SIP service settings](/zh/product/terminals/images/softsip-settings.png)

3. Go back to the home page, choose a protocol, enter the other party's address, and tap **Call**; or wait for an incoming call

To enter meetings on our platform, point the SIP / 323 service at the device gateway (create the account in the admin console), then dial the **meeting ID** on the home page.
The steps are exactly the same as for [hardware endpoints](/en/product/device-access/sip-h323).

---

## Get it

The soft endpoint is delivered per project. **For the installation package and activation, [contact us](https://www.stmlink.com/en/contact)**.
