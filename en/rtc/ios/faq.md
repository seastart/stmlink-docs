---
title: "FAQ"
description: "Common iOS (Objective-C) SRTC SDK integration problems: build failures, network requests failing (ATS), App Store upload failures, dyld Library not loaded crashes with manual integration, and ITMS-90171 / ITMS-90166 rejections. Read when integration or App Store submission fails."
---

#### 1. Build fails after integrating the SDK
> The SDK currently requires iOS 16.0 or later (since `3.1.0`; iOS 10.0 before that) and Xcode 14.0 or later. Make sure your setup meets these requirements. Also set Bitcode to NO.
>

#### 2. Possible causes of network requests failing after network permission is granted
> Add the following configuration to Info.plist:
>

```xml
<key>NSAppTransportSecurity</key>
<dict>
	<key>NSAllowsArbitraryLoads</key>
	<true/>
</dict>
```


#### 3. Uploading to the App Store fails after integrating the SDK
> The SDK currently supports arm64 only. Check your project configuration for any other architectures and remove them if present.
>


#### 4. Crash on launch with manual integration: dyld: Library not loaded: @rpath/xxxxx.framework/xxxxx
> Solution: Add the dependency under **General** -> **Frameworks, Libraries, and Embedded Content**, and set **Embed** for the corresponding dynamic library to **Embed & Sign**.
>

![](/zh/rtc/ios/images/162287_1646648601308-e47d7e73-d5c2-499d-baf0-7c46925be1bb.png)


#### 5. App Store upload rejected with ITMS-90171 / ITMS-90166, saying RTCEngineKit.bundle must not contain a standalone executable
> This is a defect in SDK `3.1.1` and earlier: `RTCEngineKit.bundle` is a pure resource bundle, yet the build output included a useless placeholder executable and the `CFBundleExecutable` key in `Info.plist`. Upgrade to `3.1.2` or later and re-archive and upload; your project needs no changes.
>
