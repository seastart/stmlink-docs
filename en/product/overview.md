---
title: "Product overview"
description: "Everything STMLink offers: SRTC and SMeeting SDKs, Room Connector, cloud and voice recording, AI capabilities (captions, minutes, interpretation, voice agent—self-hosted with your own LLM), the admin console, endpoint apps, and self-hosted and CDS deployment. Start here if you don't code."
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
  <Card title="Interactive whiteboard" icon="pen" href="/en/rtc/whiteboard">
    Real-time multi-user whiteboard collaboration and document annotation
  </Card>
</Columns>

---

## AI capabilities

Recognition and synthesis can run offline on CPU, and the LLM is the customer's own, so the whole stack can be self-hosted. For the full picture, see [AI capabilities overview](/en/product/ai/overview).

<Columns cols={2}>
  <Card title="Live captions and meeting minutes" icon="closed-captioning" href="/en/product/ai/transcription">
    Per-speaker captions and live translation during the meeting; automatic minutes and the full transcript afterward
  </Card>
  <Card title="Simultaneous interpretation" icon="language" href="/en/product/ai/interpretation">
    Each person picks their own language and hears interpretation audio of others, with the original voice turned down automatically; currently Chinese ↔ English
  </Card>
  <Card title="AI voice agent and custom agents" icon="robot" href="/en/product/ai/voice-agent">
    A built-in web voice agent ready to use; or build your own agent with the Python SDK and connect phone lines
  </Card>
  <Card title="AI noise suppression and virtual background" icon="wand-magic-sparkles" href="/en/product/ai/media-ai">
    AI noise suppression, background blur / replacement, and beauty filter running locally on the device, with support per platform at a glance
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
| Presales, project manager | This page → [Room Connector](/en/product/device-access/overview) → [AI capabilities overview](/en/product/ai/overview) → [Components and architecture](/en/product/deploy/architecture) |
| Implementation, operations | [Network and port requirements](/en/product/deploy/ports) → [Room Connector](/en/product/device-access/overview) |
| Developer | [SRTC or SMeeting?](/en/choose) → the Quickstart for your platform |
