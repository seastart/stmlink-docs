---
title: "Error codes"
description: "RTCEngineError values for the iOS (Objective-C) SRTC SDK, grouped into system (100001–100004), common (100005–100008), network (100009–100011), and client (103001–103004) errors. Read when handling or logging errors from iOS SDK callbacks."
---

### RTCEngineError
Error codes

| **Enum name** | **Value** | **Description** |
| --- | :---: | --- |
| RTCEngineErrorOK | `0` | No error |
| **System errors** | | |
| RTCEngineErrorSystemError | `100001` | Internal system error |
| RTCEngineErrorNotInitialized | `100002` | Not initialized |
| RTCEngineErrorMediaNotInitialized | `100003` | The media module isn't initialized yet |
| RTCEngineErrorProtocolParsingError | `100004` | Protocol parsing error |
| **Common errors** | | |
| RTCEngineErrorTimeout | `100005` | Timed out |
| RTCEngineErrorInvalidArgs | `100006` | Invalid arguments |
| RTCEngineErrorConflict | `100007` | Conflict from a repeated operation |
| RTCEngineErrorSdkTokenInvalid | `100008` | The SDK token is invalid |
| **Network errors** | | |
| RTCEngineErrorNetError | `100009` | Network error |
| RTCEngineErrorMediaNetError | `100010` | Media network error |
| RTCEngineErrorNotFound | `100011` | Target doesn't exist |
| **Client errors** | | |
| RTCEngineErrorDeviceNoAuthorized | `103001` | No permission to access the device |
| RTCEngineErrorNotJoinedChannel | `103002` | Not in the channel |
| RTCEngineErrorForbidden | `103003` | Operation not allowed |
| RTCEngineErrorStreamNotFound | `103004` | Stream doesn't exist |


