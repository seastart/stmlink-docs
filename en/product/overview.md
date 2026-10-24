---
title: "Product overview"
description: "Everything STMLink offers on one page: SRTC and SMeeting SDKs, Room Connector for meeting-room hardware, cloud and per-speaker voice recording, speech recognition, the admin console, endpoint apps, and self-hosted and cross-domain solution (CDS) deployment. Start here if you don't write code."
---

We provide a complete **self-hostable** real-time audio and video platform: from low-level audio and video capabilities,
to ready-to-use meetings, to meeting-room hardware integration and cross-network deployment. This page connects them by
"what problem each one solves", and you can click into any item for details.

For product highlights and industry solutions, you can also visit our [website](https://www.stmlink.com/en/).

---

## Platform capabilities

<Columns cols={2}>
  <Card title="SRTC Audio & Video SDK" icon="video" href="/en/rtc/overview">
    Low-latency audio and video calls, live streaming, and push-to-talk. Covers Web, Mini Programs, Android, iOS, Windows, Mac, and HarmonyOS, plus server-side C / Python SDKs
  </Card>
  <Card title="SMeeting Conferencing SDK" icon="users" href="/en/meeting/overview">
    Ready-made meeting features such as host, meeting controls, raise hand, waiting room, scheduling, and sign-in, plus low-code integration with UI
  </Card>
  <Card title="Room Connector" icon="tv" href="/en/product/device-access/overview">
    SIP / H.323 video endpoints from Huawei, Kedacom, and others, GB28181 surveillance cameras, and RTSP streams enter meetings without replacing any devices
  </Card>
  <Card title="Cloud recording" icon="circle-dot" href="/en/rtc/server-api/guides/recording">
    Server-side multi-view composite recording and re-streaming, with recordings stored centrally for online playback and download
  </Card>
  <Card title="Voice recording" icon="microphone" href="/en/rtc/server-api/talkrec">
    Per-speaker segmented audio recording for push-to-talk, dispatch, law enforcement, and other scenarios that need an audit trail
  </Card>
  <Card title="Speech recognition and meeting minutes" icon="closed-captioning" href="/en/rtc/server-api/asr">
    Live captions and transcription during the meeting, and minutes after it
  </Card>
  <Card title="AI voice / video agents" icon="robot" href="/en/rtc/python/quickstart">
    Use the Python SDK to plug speech recognition, LLMs, and speech synthesis into calls for AI customer service and AI assistants
  </Card>
  <Card title="Interactive whiteboard" icon="pen" href="/en/rtc/whiteboard">
    Real-time multi-user whiteboard collaboration and document annotation
  </Card>
</Columns>

---

## Management and operations

<Columns cols={2}>
  <Card title="Admin console" icon="gauge" href="/en/product/admin-console">
    Apps, channels and meetings, recording, devices, usage statistics, call quality, and node operations, all in one console
  </Card>
  <Card title="Try it online" icon="play" href="/en/product/demos">
    RTC demo and meeting demo—try before you decide
  </Card>
</Columns>

---

## Endpoint apps

Besides the SDKs, we also offer endpoint apps you can install directly on devices:

<Columns cols={2}>
  <Card title="Soft SIP / H.323 endpoint" icon="phone" href="/en/product/terminals/softsip">
    An app for Android devices that turns large displays and all-in-one units into standard SIP / H.323 video endpoints
  </Card>
  <Card title="Android TV edition" icon="display" href="/en/product/terminals/tv">
    For meeting-room TVs and large displays: remote-control operation, one-click meeting entry, and casting
  </Card>
</Columns>

---

## Deployment

<Columns cols={2}>
  <Card title="Components and architecture" icon="sitemap" href="/en/product/deploy/architecture">
    Fully offline installation on Linux servers with x86 or ARM, via Docker or the offline installer
  </Card>
  <Card title="Network and port requirements" icon="network-wired" href="/en/product/deploy/ports">
    Clients need only 3 ports; firewall commands included, ready for your firewall change request
  </Card>
  <Card title="Internal network and public internet" icon="route" href="/en/product/deploy/networks">
    One platform serves users on the internal network and the public internet at the same time
  </Card>
  <Card title="Access across a cross-domain solution" icon="shield-halved" href="/en/product/deploy/optical-gap">
    With the internal network and the public internet isolated by a cross-domain solution (CDS), public-internet users still enter meetings through just 3 tunnel channels
  </Card>
</Columns>

---

## Where to start

| I am | Start here |
| --- | --- |
| Presales, project manager | This page → [Room Connector](/en/product/device-access/overview) → [Components and architecture](/en/product/deploy/architecture) |
| Implementation, operations | [Network and port requirements](/en/product/deploy/ports) → [Device integration](/en/product/device-access/overview) |
| Developer | [SRTC or SMeeting?](/en/choose) → the Quickstart for your platform |
