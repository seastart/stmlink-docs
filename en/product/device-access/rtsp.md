---
title: "RTSP streams"
description: "Bring any IP camera, encoder, NVR, or media server that outputs an RTSP URL into meetings: register the stream URL in the admin console, choose UDP or TCP, look up URL formats for common brands, and invite the stream into the meeting."
---

As long as a device can provide an RTSP URL (`rtsp://...`), you can pull its video into a meeting. The device doesn't need to support GB28181
or register—the device gateway pulls the stream itself.

---

## 1. Prepare the stream URL

First open the stream URL in a player (such as VLC). **Continue only once it plays.** Common formats:

| Brand | Main stream URL format |
| --- | --- |
| Hikvision | `rtsp://username:password@IP:554/Streaming/Channels/101` |
| Dahua | `rtsp://username:password@IP:554/cam/realmonitor?channel=1&subtype=0` |
| Uniview | `rtsp://username:password@IP:554/media/video1` |

Check the device manual for specifics. If the device requires login, put the username and password in the URL.

---

## 2. Register it in the console

Admin console **Device management** → **RTSP** → **Add account**:

![Add an RTSP stream](/zh/product/device-access/images/admin-rtsp-add.png)

| Field | What to enter |
| --- | --- |
| Transport | **UDP** (default) or **TCP**. TCP is more stable when the network has packet loss, crosses subnets, or passes through firewalls |
| Stream URL | The RTSP URL verified in step 1; must start with `rtsp` |
| Display name | The name shown in the meeting |
| Device gateway | Which gateway pulls the stream; this gateway must be able to reach the device's IP |

The list after registering:

![RTSP stream list](/zh/product/device-access/images/admin-rtsp-list.png)

RTSP streams have no online status, so `--` in the list is normal—the gateway pulls the stream only when it's invited into a meeting.

---

## 3. Invite into the meeting

+ **Admin console**: meeting details → **Invite** → **Invite device** → **Surveillance cameras**
+ **Meeting client**: the host clicks **Invite** → **Invite device** → **Surveillance cameras**
+ **Business system**: call [Invite devices to the channel](/en/rtc/server-api/agent#invite-devices-to-the-channel)

---

## Codecs

| | Support |
| --- | --- |
| H.264 video | Forwarded directly, with no quality loss and no transcoding resources used |
| H.265 video | The gateway converts it to H.264 automatically, which uses gateway CPU; evaluate server capacity for many streams |
| Audio | If the stream has audio, it enters the meeting too; the gateway transcodes automatically |

<Tip>
Set the camera to **H.264 main stream** at **1080P or lower** to use the fewest resources. H.265 works, but every stream needs real-time transcoding.
</Tip>
