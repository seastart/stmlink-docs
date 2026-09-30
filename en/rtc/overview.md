---
title: "Overview"
description: "What SRTC is, its architecture, and which platforms it supports, with links to each platform's integration and quickstart pages. Read this first when evaluating SRTC or picking your platform SDK."
---

SRTC is a converged audio and video communication component. Built on low-latency audio and video and real-time multi-user interaction, it combines standard audio/video protocol interoperability, MCU (server-side mixing and recording), self-hosted live streaming, and more. It can be deployed on public cloud, private cloud, or hybrid cloud, giving developers a low-cost solution for interactive audio and video.

If you are still deciding between SRTC and SMeeting (the SDK behind STMLink Meeting), see [Choosing SRTC or SMeeting](/en/choose) first.

### Architecture

The real-time audio and video component focuses on cross-platform multi-user audio and video calls and low-latency interaction. It provides SDKs for WeChat Mini Program, Web, Android, iOS, Windows, Linux, and other platforms, so you can integrate quickly and connect to third-party private cloud backends. Combined with our other products, it also supports capabilities such as instant messaging and whiteboards, extending to more business scenarios.

![SRTC architecture](/zh/rtc/images/421454_1722664667226-c4e3c4c0-9b66-4bbc-a905-f4fed9746fe7.jpeg)

SRTC only handles the audio and video transport itself. It has **no user system and no business rules**—your backend owns both and works with SRTC through the server API.



### Platform support

All platforms interoperate, and behavior is aligned across them.

| Platform | Description | Docs |
| --- | --- | --- |
| Web | Browsers, and also WeChat Mini Program (embedded via `web-view`) | [Integration](/en/rtc/web/integration) · [Quickstart](/en/rtc/web/quickstart) |
| Android | Phones, set-top boxes, embedded devices | [Integration](/en/rtc/android/integration) · [Quickstart](/en/rtc/android/quickstart) |
| Windows | Desktop clients, C++ API | [Integration](/en/rtc/windows/integration) · [Quickstart](/en/rtc/windows/quickstart) |
| Swift | iOS and macOS, `import SRTC` | [Integration](/en/rtc/swift/integration) · [Quickstart](/en/rtc/swift/quickstart) |
| iOS | Objective-C, `RTCEngineKit` | [Integration](/en/rtc/ios/integration) · [Quickstart](/en/rtc/ios/quickstart) |
| C | Server and embedded, pure C API | [Integration](/en/rtc/capi/integration) · [Quickstart](/en/rtc/capi/quickstart) |
| Python | Server-side AI (voice bots, recording, transcription), sends and receives PCM, supports pipecat | [Integration](/en/rtc/python/integration) · [Quickstart](/en/rtc/python/quickstart) |
| Server | HTTP endpoints and event callbacks | [Server API](/en/rtc/server-api/overview) |

<Note>
Each platform is distributed differently: Web via npm, Android via Maven, and Windows as a zip downloaded from the artifact repository. See the corresponding integration page for each.
Swift uses Swift Package Manager (prebuilt XCFramework), and Python uses PyPI (`pip install srtc`). Contact us for the iOS and C SDK packages.
</Note>
