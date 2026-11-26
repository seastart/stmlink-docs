---
title: "Audio and video AI processing"
sidebarTitle: "Noise suppression and virtual background"
description: "On-device AI processing: AI noise suppression (RNNoise, DeepFilterNet), virtual background (blur / replace), and beauty filter, with a capability × platform support table linking to each guide. Check when asked whether a platform can suppress noise or replace the background."
---

Noise suppression, virtual background, and beauty filter all run **locally on the device**: processing happens after capture and before sending, without going through the server,
and no server-side AI services need configuring. What the other side sees and hears is the processed result, and so is the recording.

---

## What it does

| Capability | Effect | Notes |
| --- | --- | --- |
| **AI noise suppression · RNNoise** | Removes keyboard sounds, fan noise, and ambient noise | Lightweight; suppresses non-stationary noise better than the browser's built-in noise suppression |
| **AI noise suppression · DeepFilterNet** | Same as above, with higher quality | Suppression strength adjustable at runtime; more computation and larger assets than RNNoise, and the SDK warns when the device lacks compute |
| **Virtual background** | Person segmentation, then background blur or replacement with a specified image | In-house component, no license key needed; provides parameters to keep frame rate up on low-end devices |
| **Beauty filter** | Skin smoothing, whitening, rosiness, sharpening, filters | Video rendering component; requires a component key |

---

## Platform support

In the tables, ✅ links to the corresponding integration guide; platforms not listed and blank cells mean the docs don't currently cover that capability.

### SRTC Audio & Video SDK

| Capability | Web | Android | iOS (Objective-C) | Swift | Windows | WeChat Mini Program |
| --- | --- | --- | --- | --- | --- | --- |
| AI noise suppression · RNNoise | [✅](/en/rtc/web/advanced/rnnoise) | | | | | |
| AI noise suppression · DeepFilterNet | [✅](/en/rtc/web/advanced/deepfilternet) | [✅](/en/rtc/android/advanced/deepfilternet) | | [✅](/en/rtc/swift/advanced/deepfilternet) | | |
| AI noise suppression (built-in SDK mode) | | | | | [✅](/en/rtc/windows/api-reference/IRTCChannelSetting) noise suppression mode can be AI / AI + acoustic | |
| Virtual background | | [✅](/en/rtc/android/api-reference/RTCEngine#virtual-background) | [✅](/en/rtc/ios/advanced/virtual-background) | [✅](/en/rtc/swift/advanced/virtual-background) iOS only | | |
| Beauty filter | | | [✅](/en/rtc/ios/advanced/beauty) | | | [✅](/zh/rtc/wechat-miniprogram/api-reference/streaming) (Chinese) built into the WeChat live-pusher component |

### SMeeting Conferencing SDK

| Capability | Web | Android | iOS (Objective-C) | Swift | Windows |
| --- | --- | --- | --- | --- | --- |
| AI noise suppression · DeepFilterNet | [✅](/en/meeting/web/advanced/deepfilternet) | [✅](/en/meeting/android/advanced/deepfilternet) | | [✅](/en/meeting/swift/advanced/deepfilternet) | |
| AI noise suppression (built-in SDK mode) | | | | | [✅](/en/meeting/windows/api-reference/smeeting-settings) noise suppression mode |
| Virtual background | | [✅](/en/meeting/android/api-reference/MeetingEngine#virtual-background) | [✅](/en/meeting/ios/advanced/virtual-background) | [✅](/en/meeting/swift/advanced/virtual-background) iOS only | |

<Note>
On Web, noise suppression comes as standalone npm plugins (`@seastart/srtc-plugin-rnnoise`, `@seastart/srtc-plugin-deepfilternet`), and the model and wasm files must be hosted with your website; see each page.
For the general mechanism of attaching processors, see [Audio processors](/en/rtc/web/advanced/audio-processor).
</Note>

---

## Selection advice

+ **Noise suppression only**: on Web, start with RNNoise (small assets); if you need better suppression and the device has enough performance, use DeepFilterNet
+ **Don't stack two layers of noise suppression**: when a plugin does noise suppression, the SDK turns off the browser's built-in noise suppression to avoid muffled voices
+ **Virtual background**: watch the frame rate on low-end phones; you can increase the person segmentation inference interval to gain frame rate—see each platform's page for the parameters
