---
title: "Overview"
description: "What the SMeeting conferencing SDK (STMLink Meeting) covers, the three integration options from server-side low-code integration to fully custom UI, and supported platforms. Start here to decide how to add video meetings to your product."
---

SMeeting (the SDK behind STMLink Meeting) is a complete audio and video conferencing SDK. It is built on top of [SRTC audio and video](/en/rtc/overview) and turns the rules that only meetings need—host, raise hand, mute all, waiting room, recording—into ready-made capabilities, so you don't have to implement them again.

Still deciding between SRTC and SMeeting? See [Choosing SRTC or SMeeting](/en/choose) first.

---

## What you can do

| | |
| --- | --- |
| **Meeting management** | Create, update, and cancel meetings; scheduled and instant meetings; meeting list and details |
| **Audio and video** | Camera, microphone, screen sharing, subscribing to multiple members' video |
| **Meeting controls** | Host / co-host, mute all, remove a member, change roles, lock the meeting |
| **Member interaction** | Raise a hand to request to speak, host asks to unmute, in-meeting chat, custom messages |
| **Meeting features** | Waiting room, sub-meetings, sign-in, roll call |
| **Recording and live streaming** | Server-side MCU stream mixing, recording, layout configuration, re-streaming |
| **Out-of-meeting messages** | A notification path independent of meetings for calls, meeting reminders, help requests, and more (not a chat tool; see [Three types of messages](/en/meeting/key-concepts#three-types-of-messages)) |

---

## Three integration options

Ordered from least to most effort; choose based on how much customization you need:

| Option | What you do | UI | Best for |
| --- | --- | --- | --- |
| **Server-side low-code integration** | Your backend calls 3 endpoints and builds a URL | Deployed by us | Attaching meetings to an existing business workflow (reviews, tickets, tendering and bidding) |
| **Low-code integration with UI** | Take our frontend source code, modify it, and deploy it yourself | Our source code, which you can modify | Your own branding with light customization |
| **Custom integration** | Integrate the SDKs for each platform and build your own UI | Entirely your own | Building a meeting product with deeply customized interactions |

### Server-side low-code integration

**You don't integrate any SDK or build a meeting UI.** The meeting client, user system, and login state are already deployed by us. Your backend does only three things: create the meeting, get a login-free token for the user, and redirect the user's browser to the meeting page.

Best for: you want to "add a video meeting entry to this review," not build a meeting product.

Start with [Server-side low-code integration](/en/meeting/ui-sdk/server-integration).

### Low-code integration with UI

Bring in the meeting UI source code we provide, deploy it yourself, and adapt it as needed; on the server side, you only need to connect the accounts.

Best for: you want to launch quickly, but the UI must match your brand.

See [Web](/en/meeting/ui-sdk/web) · [iOS](/en/meeting/ui-sdk/ios) · [Android](/en/meeting/ui-sdk/android) · [Windows](/en/meeting/ui-sdk/windows).

### Custom integration

You build the UI yourself and call the SDK for each platform to implement meeting features; your server calls the meeting backend APIs and exposes a callback endpoint to receive events.

Best for: the UI must follow your own design guidelines, and the interaction flows need customization.

Choose your platform from the platform support table below.

---

## Platform support

| Platform | Docs |
| --- | --- |
| Web | [Web SDK](/en/meeting/web/integration) |
| Android | [Android SDK](/en/meeting/android/integration) |
| Windows | [Windows SDK](/en/meeting/windows/integration) |
| iOS / macOS (Swift) | [Swift SDK](/en/meeting/swift/integration) |
| iOS (Objective-C) | [iOS SDK](/en/meeting/ios/quickstart) |
| Server | [Server API](/en/meeting/server-api/overview) |

<Note>
For WeChat Mini Program scenarios, we recommend embedding a page built with the Web SDK through `<web-view>`, so that one codebase covers both browsers and mini programs. See [Web SDK integration](/en/meeting/web/integration).
</Note>

---

## Next steps

+ [Quickstart](/en/meeting/quickstart)—an overview of the integration flow
+ [Key concepts](/en/meeting/key-concepts)—rooms, meetings, members, and roles
+ [Token and authentication](/en/meeting/token)—the grant flow and secret key security
