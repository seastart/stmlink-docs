---
title: "Admin console features"
description: "What the built-in admin console does, menu by menu with screenshots: usage stats, channel and meeting management, in-meeting controls, recording, devices, contacts, VOD, licensing, accounts, and media node and gateway operations. Read when evaluating the product or preparing training."
---

Every platform comes with a web-based **admin console** (after deployment, open `https://<your-domain>/admin/`). Administrators can manage apps,
meetings, recording, devices, and servers without writing code. Switch the **app** in the lower-left corner: audio and video apps (SRTC) and meeting apps (SMeeting) show slightly different menus.

![Admin console home](/zh/product/images/admin-home.png)

---

## Menus at a glance

| Menu | What it does | App type |
| --- | --- | --- |
| **Home** | Today's channel / meeting count and duration, with weekly, monthly, and yearly trends | All |
| **Channel management** | Channel list, online users, assigned media node; open details to see users and call quality | Audio and video |
| **Meeting management** | Meeting list (upcoming / in progress / ended), scheduled meetings, meeting details, and in-meeting controls | Meeting |
| **Recording management** | Default recording layout, watermark, and window labels; recording file playback and download; voice recording | All |
| **Device management** | Register SIP / H.323 endpoints, RTSP streams, and GB28181 cameras, and view their online status; see [Device integration](/en/product/device-access/overview) | All |
| **Contacts management** | Departments and members, used for meeting invitations | Meeting |
| **Video on demand** | Cloud media library, cloud editing, cloud transcoding, transcoding templates, and VOD nodes | All |
| **Top-up management** | View this platform's platform code (provided when applying for a license), and allocate user concurrency, device concurrency, and validity period to apps | All |
| **File licenses** | Import license files and view the total and remaining quota of each license | All |
| **Device licenses** | Activation records and expiry dates of client devices | All |
| **System management** | Console accounts, roles, and menu permissions | All |
| **Operations management** | Client access addresses (network lines), media nodes, media gateways, MCU alarms, and operation logs | All |

Menus are shown according to the account's role permissions. If you can't see a menu, ask your administrator to grant the permission.

---

## Meeting management and in-meeting controls

You can control meetings in progress directly from the console: **mute all / unmute all, lock the meeting, start recording, invite members or devices, view meeting monitoring, and end the meeting**.
Below that, you can view and export in-meeting members, members who have exited, members who haven't entered, sign-in records, and chat history.

![Meeting details](/zh/product/images/admin-meeting-detail.png)

---

## Recording management

Set the default video layout for cloud recording (auto grid, or a custom layout with specified members, up to 25 tiles), the recording watermark, and window labels;
play back and download recordings under **Recording files**; and view per-speaker audio segments under **Voice recording**.

![Recording settings](/zh/product/images/admin-record.png)

---

## Operations management

**Media nodes**: each media forwarding node's online status, load level, CPU / memory, channel and user counts, network line, and historical load curve.
For multi-node deployments, you also adjust the scheduling policy here.

![Media nodes](/zh/product/images/admin-sfu-node.png)

**Media gateways**: the running status, task count, and load of gateways such as MCU, device gateway, voice recording, and speech recognition.

![Media gateways](/zh/product/images/admin-media-gw.png)

**System configuration → Network**: the access addresses each network line delivers to clients; see [Internal and public networks](/en/product/deploy/networks).
