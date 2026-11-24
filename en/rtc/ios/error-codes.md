---
title: "Error codes"
description: "RTCEngineError values for the iOS (Objective-C) SRTC SDK: since 3.2.0, SDK errors are the iOS prefix 103 plus the low 3 digits of the cross-platform unified table, and backend business codes (1000–99999) are passed through. Includes the old (3.1.2 and earlier) values. Read when handling or logging errors from iOS SDK callbacks or upgrading from 3.1.x."
---

<Note>
Since **3.2.0**, error codes have been renumbered according to the [cross-platform unified table](/en/rtc/error-codes) as "iOS prefix `103` + low 3 digits". Enum names are kept but their values changed, so you must recompile with the new headers. The "3.1.2 and earlier" column below lists the old values; for details, see the [Changelog](/en/rtc/ios/changelog).
</Note>

### Error code rules

+ `0`: success
+ `103000`–`103999`: SDK local errors. Full code = `103` + the low 3 digits of the unified table, e.g. `103006` = `103` + `006` (connection failed). The low 3 digits mean the same as on other platforms
+ `1000`–`99999`: backend business codes, passed through by the SDK as is without a prefix. For their meanings, see [Server API error codes](/en/rtc/server-api/error-codes)

The `errCode` of `engineChannel:onDisconnected:errCode:errMsg:` and `onImDisconnected:errCode:errMsg:` follows the same rules. When an API that only returns an error code hits a backend business code, read [RTCEngineKit.lastServerErrorMessage](/en/rtc/ios/api-reference/RTCEngineKit#lastservererrormessage) immediately to get the server-side message (since `3.2.1`; language follows [RTCEngineKit.language](/en/rtc/ios/api-reference/RTCEngineKit#language)). **Branch on the error code, not on the error message**: `errMsg` comes from the backend and is for logging only.

### RTCEngineError
Error codes

| **Enum name** | **Value** | **3.1.2 and earlier** | **Description** |
| --- | :---: | :---: | --- |
| RTCEngineErrorOK | `0` | `0` | No error |
| **Connection and signaling** | | | |
| RTCEngineErrorNotJoinedChannel | `103001` | `103002` | Not in a channel |
| RTCEngineErrorStreamNotFound | `103003` | `103004` | Stream doesn't exist |
| RTCEngineErrorSdkTokenInvalid | `103004` | `100008` | Invalid token |
| RTCEngineErrorConflict | `103005` | `100007` | Conflict from a repeated operation, e.g. joining a channel twice |
| RTCEngineErrorNetError | `103006` | `100009` | Network error (including non-200 HTTP) |
| RTCEngineErrorTimeout | `103007` | `100005` | Connection or request timed out |
| RTCEngineErrorProtocolParsingError | `103011` | `100004` | Protocol parsing error |
| RTCEngineErrorMediaNetError | `103012` | `100010` | Media network error |
| **State and general** | | | |
| RTCEngineErrorNotInitialized | `103024` | `100002` | Not initialized, or the current state doesn't allow the operation (e.g. calling `switchCamera` while capture isn't on) |
| RTCEngineErrorMediaNotInitialized | `103024` | `100003` | Deprecated; same value as `RTCEngineErrorNotInitialized`. Don't write both in a `switch` |
| RTCEngineErrorSystemError | `103025` | `100001` | Internal system error |
| RTCEngineErrorUserCancelled | `103026` | `100012` | Cancelled by the user |
| RTCEngineErrorInvalidArgs | `103031` | `100006` | Invalid arguments, e.g. passing track `0`–`2` for a custom stream |
| **Virtual background** | | | |
| RTCEngineErrorVirtualBackgroundAlreadyInstalled | `103027` | New | The virtual background component is already installed |
| RTCEngineErrorVirtualBackgroundNotInstalled | `103028` | New | The virtual background component isn't installed |
| RTCEngineErrorVirtualBackgroundModelNotFound | `103029` | New | The portrait segmentation model file doesn't exist or is invalid |
| RTCEngineErrorVirtualBackgroundSessionFailed | `103030` | New | Failed to create the inference session |
| **Permissions and devices** | | | |
| RTCEngineErrorDeviceNoAuthorized | `103042` | `103001` | No device access permission. Kept as a definition, but **the SDK no longer returns it**; use the camera / microphone codes below instead |
| RTCEngineErrorForbidden | `103043` | `103003` | The current identity or role isn't allowed to perform the operation |
| RTCEngineErrorSwitchAudioRouteFail | `103044` | `103005` | Failed to switch the audio route |
| RTCEngineErrorCameraNoAuthorized | `103231` | New | No camera permission |
| RTCEngineErrorMicNoAuthorized | `103251` | New | No microphone permission |
| **Users** | | | |
| RTCEngineErrorNotFound | `103204` | `100011` | The user isn't in the channel |

<Warning>
In 3.1.2 and earlier, missing camera / microphone permission always returned `RTCEngineErrorDeviceNoAuthorized`, and the four virtual background failures returned `RTCEngineErrorConflict` / `RTCEngineErrorNotFound` / `RTCEngineErrorSystemError`. When upgrading from those versions, besides recompiling, change the corresponding branches to the new enums according to the table above.
</Warning>
