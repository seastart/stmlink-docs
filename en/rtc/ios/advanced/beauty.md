---
title: "Beauty filter"
description: "Add beauty filters in the Objective-C SRTC SDK on iOS: install the video render module with a license key, set smoothing, whitening, rosiness, sharpening, and filter parameters, choose from the built-in filters, toggle the beauty filter on or off, and uninstall the module."
---

### Step 1: **Install the video render module**
Use the license key to install and initialize the beauty filter service; you can also set the log level. We recommend installing the video render module when your app starts.

```objectivec
/// Install the video render module
/// @param authData license key
/// @param authDataSize license key length
/// @param logLevel log level
[[RTCEngineKit sharedEngine] installRenderModule:g_auth_package authDataSize:sizeof(g_auth_package) logLevel:RTCEngineLogLevelError];
```

### Step 2: **Set beauty effect parameters**
The video render module currently provides only basic beauty effects. After installing the video render module, set the effects with the following properties:

| **Property** | **Type** | **Description** |
| --- | :---: | --- |
| blurLevel | float | Smoothing level, range 0.0–1.0, default 0.5 |
| whiteLevel | float | Whitening level, range 0.0–1.0, default 0.3 |
| redLevel | float | Rosiness level, range 0.0–1.0, default 0.3 |
| sharpenLevel | float | Sharpening level, range 0.0–1.0, default 0.3 |
| filterLevel | float | Filter level, range 0.0–1.0, default 0.8 |
| filterName | NSString | Filter effect, default "origin"; origin means the original image |


The video render module currently supports the following filter effects:

| **Filter effect** | **Description** |
| --- | --- |
| origin | Original image |
| bailiang1 | Bright white 1 |
| bailiang2 | Bright white 2 |
| bailiang3 | Bright white 3 |
| bailiang4 | Bright white 4 |
| bailiang5 | Bright white 5 |
| bailiang6 | Bright white 6 |
| bailiang7 | Bright white 7 |
| fennen1 | Pink 1 |
| fennen2 | Pink 2 |
| fennen3 | Pink 3 |
| fennen4 | Pink 4 |
| fennen5 | Pink 5 |
| fennen6 | Pink 6 |
| gexing1 | Stylized 1 |
| gexing2 | Stylized 2 |
| gexing3 | Stylized 3 |
| gexing4 | Stylized 4 |
| gexing5 | Stylized 5 |
| gexing6 | Stylized 6 |
| gexing7 | Stylized 7 |
| gexing10 | Stylized 10 |
| gexing11 | Stylized 11 |
| heibai1 | Black and white 1 |
| heibai2 | Black and white 2 |
| heibai3 | Black and white 3 |
| heibai4 | Black and white 4 |
| lengsediao1 | Cool tone 1 |
| lengsediao2 | Cool tone 2 |
| lengsediao3 | Cool tone 3 |
| lengsediao4 | Cool tone 4 |
| lengsediao5 | Cool tone 5 |
| lengsediao6 | Cool tone 6 |
| lengsediao7 | Cool tone 7 |
| lengsediao8 | Cool tone 8 |
| lengsediao11 | Cool tone 11 |
| nuansediao1 | Warm tone 1 |
| nuansediao2 | Warm tone 2 |


### Step 3: **Turn the beauty filter on or off**
The beauty filter is on by default after the video render module is installed. To turn it on or off later, use the following API:

```objectivec
/// Turns the beauty filter on or off
/// @param enabled YES: turn the beauty filter on; NO: turn it off
[[RTCEngineKit sharedEngine] enabledBeauty:YES];
```

### Step 4: **Uninstall the video render module**
```objectivec
/// Uninstall the video render module
[[RTCEngineKit sharedEngine] uninstallRenderModule];
```

