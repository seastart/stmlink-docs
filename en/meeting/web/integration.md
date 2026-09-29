---
title: "Integration"
description: "Supported browsers, WeChat Mini Program embedding via web-view, protocol requirements for publishing and receiving streams, and how to install the SMeeting Web SDK via npm or a local copy. Read this before writing any meeting code for the Web."
---

## Supported platforms

The SMeeting Web SDK supports mainstream desktop and mobile browsers:

| Browser | Minimum version | Notes |
| --- | :---: | --- |
| Chrome | 72+ | Recommended, full feature support |
| Edge | 79+ | Chromium-based |
| Firefox | 66+ | Selecting a speaker output device is not supported |
| Safari | 14+ | Sharing system audio during screen sharing is not supported |
| WeChat in-app browser | iOS 14.3+ / Android | Sending and receiving are supported. Older iOS versions below 14.3 can only receive streams |
| Mobile Chrome / Safari | Latest | Basic audio and video calls are supported |

> **Tip:** We recommend that users use the latest version of Chrome for the best experience.

## WeChat Mini Program scenario

When you need meetings inside a WeChat Mini Program, **we recommend embedding a page built on this Web SDK through the Mini Program's `<web-view>`**, rather than building a separate native Mini Program implementation. This way one set of Web code covers both browsers and the Mini Program, features and future iterations naturally stay in sync, and maintenance cost is lowest.

Key points:

+ The embedded page must be served over **HTTPS**, and its domain must be configured as a **business domain** in the Mini Program admin console and pass verification
+ Pass parameters between the Mini Program and the embedded page through the `web-view` communication mechanism; the room number, token, and so on can be delivered in the URL query
+ The page runs in the WeChat in-app browser. On iOS 14.3 and later and on Android, both publishing and receiving work normally; only older iOS versions below 14.3 are limited by the system WebView and can only receive streams

## URL domain and protocol restrictions
| Scenario    | Protocol    | Receive audio and video    | Publish audio and video    | Notes    |
| --- | --- | --- | --- | --- |
| Production    | HTTPS    | Supported    | Supported    | **Recommended**    |
| Production    | HTTP    | Supported    | Not supported    |     |
| Local development    | http://localhost    | Supported    | Supported    | **Recommended**    |
| Local development    | http://127.0.0.1    | Supported    | Supported    |     |
| Local development    | http://[local IP]    | Supported    | Not supported    |     |
| Local development    | file:///    | Supported    | Supported    |     |


## Install
### npm
```bash
npm install @seastart/smeeting-web-sdk@latest --save
```

### Local copy
Download the SDK package manually:

1. Download [smeeting.js](https://www.unpkg.com/@seastart/smeeting-web-sdk@latest/smeeting.js) and [smeeting.d.ts](https://www.unpkg.com/@seastart/smeeting-web-sdk@latest/smeeting.d.ts)
2. Copy `smeeting.js` and `smeeting.d.ts` into your project.



## Usage
Import it with `import` or load it with a `script` tag

```typescript
import { SMeeting } from '@seastart/smeeting-web-sdk';
// or
<script src="smeeting.js"></script>
```

  
  


  
 
