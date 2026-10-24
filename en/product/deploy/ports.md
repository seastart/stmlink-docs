---
title: "Network and port requirements"
description: "Ports a self-hosted deployment opens: client ports 443/TCP, 18883/TCP, 39001/UDP; device gateway SIP / H.323 / GB28181 ports and RTP range; multi-node and MCU live ports; ports never to expose; firewall commands. Use it for firewall change requests to network and security teams."
---

**The short version**: a standard deployment only needs to open three ports to clients—**443/TCP, 18883/TCP, and 39001/UDP**;
add the device gateway set if you connect hardware devices; no other port is exposed externally.

All ports below are defaults. They can be changed at deployment, so go by the actual on-site configuration.

---

## Quick reference

```text
Clients (required):       443/TCP   18883/TCP   39001/UDP
Add for devices:          1720, 1740-1759/TCP   1719/UDP   5060, 5070/TCP+UDP   58000-59000/UDP
Add for media nodes:      39002/UDP (between nodes only)
All other ports:          never exposed externally
```

---

## Client access (required)

Open to: the networks of all users of the apps, desktop clients, web, and Mini Programs.

| Port | Protocol | Purpose |
| --- | --- | --- |
| **443** | TCP | HTTPS unified entry point: APIs, admin console, web client, recording downloads, web signaling (WSS) |
| **18883** | TCP | Signaling for native clients (Android, iOS, Windows, Mac, and others) (MQTT over TLS) |
| **39001** | **UDP** | Audio and video media. All users share this one port |

<Warning>
**39001/UDP must be open.** Audio and video use UDP only, with no TCP fallback. The typical symptom when this port is blocked:
**users can log in and enter meetings, but see no video and hear no audio**.
</Warning>

+ The web client uses only 443 and 39001/UDP; native clients need all three
+ Clients connect only to these three ports. If you change 443 or 18883, also update the access addresses under **System configuration → Network** in the admin console
+ 80/TCP doesn't need to be open externally

---

## Device gateway

Needed only when connecting [hardware devices](/en/product/device-access/overview). Open to **the subnets where the devices are**, not the internet.

| Port | Protocol | Purpose |
| --- | --- | --- |
| 5060 | TCP + UDP | SIP signaling (endpoint registration, calls) |
| 1720 | TCP | H.323 call signaling |
| 1719 | UDP | H.323 gatekeeper (endpoint registration) |
| 1740-1759 | TCP | H.323 media control, one per call |
| 5070 | TCP + UDP | GB28181 signaling |
| 58000-59000 | UDP | Device audio and video (RTP), 2–4 ports per call; **the whole range must be open** |

**When there's NAT between devices and the device gateway**:

+ At deployment, set the "device access gateway IP" to the address the devices see (the post-NAT address)
+ Port mappings on the NAT must **keep the same port numbers**, especially for the RTP port range; otherwise calls connect but have no audio or video

With RTSP, the direction is reversed: the device gateway connects to the camera, so open gateway → camera 554/TCP (and the camera's RTP ports).

---

## Between servers

In a single-server deployment, services talk over loopback, so **nothing extra needs to be opened**. In split-server or multi-node deployments, open the following on the **internal network between servers**:

| Scenario | Port | Description |
| --- | --- | --- |
| Multiple media nodes | 39002/UDP | Cascaded forwarding between media nodes; open in both directions between nodes |
| Extension services on separate servers | 8701/TCP | The MCU, device gateway, and others call platform APIs |
| Extension services on separate servers | 11883/TCP, 39001/UDP | The MCU, device gateway, and others enter meetings as members and must reach the signaling and media ports |
| Extension services on separate servers | 8721/TCP (MCU), 8722/TCP (device gateway) | The platform sends recording and call commands |

---

## MCU live streaming (optional, off by default)

Needed only when using the MCU's built-in live streaming:

| Port | Protocol | Purpose |
| --- | --- | --- |
| 1935 | TCP | RTMP |
| 7001 | TCP | HTTP-FLV playback |
| 7002 | TCP | HLS playback |

These ports have no encryption or authentication. For public audiences, we recommend reverse proxying them through 443 instead of exposing them directly.

---

## Never expose externally

The following ports are used only on the server itself or the internal network. **Don't open them to the internet**:

| Port | Description |
| --- | --- |
| 8799 | Installer; close it after installation |
| 18083 | MQTT management console |
| 8700 / 8701 / 8702 / 8720 / 8721 / 8722 / 8729 / 8730 | Internal service APIs, exposed only through 443 |
| 1883 / 8083 / 11883 | MQTT internal ports |
| 5432 / 6379 / 9000 / 8123 | Database, Redis, log database |
| 8797 / 8798 | Monitoring center |
| 22 | SSH; we recommend restricting source IPs |

---

## Outbound connections from servers

On internal-only networks, the following features need **outbound** access from the server:

| Feature | Destination |
| --- | --- |
| Event callbacks | The callback URL of the customer's business system (443 / 80) |
| Storing recordings in object storage | OSS / S3 endpoint (443) |
| Speech recognition | Recognition engine service (default 10096) |
| MCU re-streaming / stream pulling | CDN (1935 / 443), cameras (554) |

---

## Firewall configuration examples

**Minimal set** (firewalld):

```bash
firewall-cmd --permanent --add-port=443/tcp
firewall-cmd --permanent --add-port=18883/tcp
firewall-cmd --permanent --add-port=39001/udp
firewall-cmd --reload
```

**Adding the device gateway**:

```bash
firewall-cmd --permanent --add-port=5060/tcp --add-port=5060/udp
firewall-cmd --permanent --add-port=5070/tcp --add-port=5070/udp
firewall-cmd --permanent --add-port=1720/tcp
firewall-cmd --permanent --add-port=1740-1759/tcp
firewall-cmd --permanent --add-port=1719/udp
firewall-cmd --permanent --add-port=58000-59000/udp
firewall-cmd --reload
```

**Between media nodes** (open only to the peer node's IP):

```bash
firewall-cmd --permanent --add-rich-rule='rule family=ipv4 source address=<peer-node-IP> port port=39002 protocol=udp accept'
firewall-cmd --reload
```

With ufw, the equivalents are `ufw allow 443/tcp`, `ufw allow 39001/udp`, and so on.

---

## Verifying after installation

| Check | How |
| --- | --- |
| Ports are listening | Run `ss -tulnp` on the server and confirm 443, 18883, 39001, and others are listed |
| Clients can connect | The web client opens and you can log in → 443 is open |
| Media works | Two people in the same meeting can see each other → 39001/UDP is open |
