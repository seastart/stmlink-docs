---
title: "FAQ"
description: "Common problems when integrating the iOS SMeeting SDK (Objective-C): build failures, network requests failing after network permission is granted, App Store upload failures, and the dyld Library not loaded crash with manual integration. Read when an integration or packaging step fails."
---

#### Build fails after integrating the component
> The SDK currently supports iOS 16.0 and later (since `2.1.0`; iOS 10.0 before that) and Xcode 14.0 and later. Make sure your setup meets these requirements. Also set Bitcode to NO.
>

#### Possible causes of network requests failing after network permission is granted
> Add the following configuration to info.plist:
>

```xml
<key>NSAppTransportSecurity</key>
<dict>
	<key>NSAllowsArbitraryLoads</key>
	<true/>
</dict>
```

#### Uploading an app with the SDK to the App Store fails
> The SDK currently supports arm64 only. Check your project configuration for any other architectures and remove them if present.
>

#### Crash on launch with manual integration: dyld: Library not loaded: @rpath/xxxxx.framework/xxxxx
> Solution: Add the dependency under General -> Frameworks, Libraries, and Embedded Content, and set Embed for the corresponding dynamic library to Embed & Sign
>

![](/zh/meeting/ios/images/344416_1646648601308-e47d7e73-d5c2-499d-baf0-7c46925be1bb.png)



