---
title: "Error codes"
description: "SRTCError, the error type of the SRTC Swift SDK: the full error code format (iOS 103xxx / macOS 105xxx), the low code and suggested handling for each case, and how language affects server error messages. Read when handling errors thrown by the Swift SDK."
---

The error type thrown by the Swift SDK is `SRTCError`, a Swift enum with semantic cases that also provides integer error codes unified across platforms:

+ Branch on cases with `switch`
+ Get the full error code from `error.code`, and the low 3-digit semantic code from `error.baseCode`
+ Get the English description from `error.message`; `error.localizedDescription` outputs `"<code>: <message>"`

<Note>
Since **1.5.0**, error codes are renumbered according to the cross-platform unified table, and error messages are in English. For the mapping between the old codes (1.4.7 and earlier) and the new ones, see the [Changelog](/en/rtc/swift/changelog).
</Note>

---

### Error code format

`SRTCError.code` returns the full error code:

+ **The SDK's own errors**: platform prefix + a 3-digit low code. The iOS prefix is `103` and the macOS prefix is `105`; for example, missing camera permission on iOS is `103231`
+ **Server business errors** (codes 1000–99999): passed through unchanged, with no prefix
+ **HTTP status codes are never folded into the error code**: non-200 HTTP responses and network failures are always `006`; the HTTP status is only in the `statusCode` of `apiRequestFailed` and in the description

`baseCode` is the low 3-digit semantic code. It means the same as on Web, Android, HarmonyOS, and other platforms, which makes it suitable for mapping user messages uniformly across platforms; for server business codes, `baseCode` returns the code itself.

| Scenario | iOS `code` | macOS `code` | `baseCode` |
| --- | --- | --- | --- |
| `cameraPermissionDenied` | `103231` | `105231` | `231` |
| `notConnected` | `103001` | `105001` | `1` |
| Server returns `1002` | `1002` | `1002` | `1002` |

`SRTCError` implements `CustomNSError`: once bridged to `NSError`, `domain = "cn.seastart.srtc"` and `code` is the full code; when there's an original system error (such as for `screenShareDenied`), it's in `NSUnderlyingErrorKey`. Integrations that go through `NSError`, such as ObjC, uni-app, or Flutter, can check the code directly.

---

### Error language

+ `message` / `localizedDescription` are **always in English**, meant for developers and logs; **for messages shown to end users, map `code` / `baseCode` yourself**—don't show `message` directly
+ `SRTCEngine.language` (such as `"en"` or `"zh-CN"`; `nil` follows the system language) sets the `Accept-Language` header on requests to the backend, and **the messages of server business errors (codes 1000–99999)** come back in Chinese or English accordingly; the SDK's own errors aren't affected

```swift
srtc.language = "en"   // Process-wide global setting; set it before joinChannel / enableIm
```

---

### Connection

| Error | Low code | Description | Suggested handling |
| --- | :---: | --- | --- |
| `notConnected` | `001` | Not currently connected / already left the channel | Check when the call is made |
| `tokenExpired` | `002` | The token has expired | Get a new token from your backend |
| `tokenInvalid` | `004` | The token is invalid | Check the token encoding and issuing logic |
| `alreadyJoined` | `005` | Already joined the channel, or `enableIm` called twice | Avoid repeated calls, or leave first |
| `connectionFailed(String)` | `006` | Connection failed | Log the server address, network environment, and error details |
| `connectionTimeout` | `007` | Connection timed out | Prompt the user to retry and check network connectivity |

---

### Signaling

| Error | Low code | Description | Suggested handling |
| --- | :---: | --- | --- |
| `apiRequestFailed(statusCode:message:)` | `006` / server code | Non-200 HTTP response or network request failure (`statusCode` is the HTTP status, or `0` for network failures); when `statusCode` ≥ 1000 it's a server business error and `code` is the server code | For network errors, prompt a retry; handle server business codes according to the server error codes |
| `signatureError` | `008` | Failed to generate the signature | Check the server-side authentication logic |
| `signalingConnectFailed(String)` | `009` | Failed to connect the signaling channel | Check network reachability, proxy, and firewall settings |
| `signalingSubscribeFailed(String)` | `010` | Failed to subscribe on the signaling channel | Check that the token is valid and the connection is established |
| `messageDecodeFailed(String)` | `011` | The response isn't JSON, lacks the `code` field, or has an unexpected structure | Check the server response format and SDK version compatibility |

---

### WebRTC / transport

| Error | Low code | Description | Suggested handling |
| --- | :---: | --- | --- |
| `webrtcError(String)` | `012` | Underlying WebRTC error | Log it; start by investigating devices and the SDP process |
| `sdpNegotiationFailed(String)` | `013` | SDP negotiation failed | Check codecs, engine capabilities, and server-side negotiation |
| `transportNotReady` | `014` | The transport layer isn't ready yet, or the channel is reconnecting | Retry later, or wait for reconnection to finish |
| `peerConnectionFailed` | `015` | The PeerConnection entered failed / closed | Check ICE / STUN / TURN and the network environment |

---

### Tracks and capture

| Error | Low code | Description | Suggested handling |
| --- | :---: | --- | --- |
| `trackNotFound(String)` | `003` | The specified track wasn't found | Check that `uid` / `trackId` match |
| `trackAlreadyPublished(String)` | `016` | The track is already published | Avoid publishing the same object twice |
| `trackNotPublished(String)` | `017` | The track isn't published | Confirm the state before unpublishing |
| `captureError(String)` | `018` | Other capture failures | Check whether the device is in use, and investigate using the description |
| `codecNotSupported(String)` | `019` | Codec not supported | Adjust the encoding preference or preset |
| `maxPublishLimitReached` | `020` | The limit of publishable tracks was exceeded | Limit the number of concurrently published tracks |
| `deviceNotFound(String)` | `021` | Device not found: no camera / display is available, or the device was unplugged | Check whether the device list changed |
| `userNotFound(String)` | `204` | The user isn't in the channel (for example, the user you're subscribing to has left) | Go by the latest user list |
| `cameraPermissionDenied` | `231` | No camera permission | Guide the user to enable it in system settings; make sure Info.plist contains `NSCameraUsageDescription` |
| `cameraFormatUnavailable(String)` | `242` | The camera has no usable capture format | Switch to another device or lower the capture spec |
| `microphonePermissionDenied` | `251` | No microphone permission (thrown when turning on the microphone) | Guide the user to enable it in system settings; make sure Info.plist contains `NSMicrophoneUsageDescription` |
| `screenShareDenied(String, underlying:)` | `039` | Screen sharing was denied: the user canceled in the system dialog, or the system didn't grant screen recording permission | On macOS, guide the user to enable it under **Privacy & Security → Screen Recording**; `underlying` is the original system error |
| `publishFailed(String)` | `300` | Publishing failed: for example, publishing while the engine isn't connected / is disconnected (not reconnecting) | Rejoin the channel, then publish again |
| `subscribeFailed(String)` | `301` | Subscribing failed: for example, subscribing while the engine isn't connected / is disconnected (not reconnecting) | Rejoin the channel, then subscribe again |

---

### Engine and general errors

| Error | Low code | Description | Suggested handling |
| --- | :---: | --- | --- |
| `engineNotSupported(String)` | `022` | Not supported by the current media streaming engine | Check the `stream_vendor` configuration |
| `engineDisconnected` | `023` | The engine is disconnected | Wait for reconnection or rejoin the channel |
| `invalidState(String)` | `024` | The current state doesn't allow this operation | Check the call order |
| `internalError(String)` | `025` | Internal SDK error | Investigate with the logs |
| `cancelled` | `026` | The operation was canceled | Your code can usually ignore it or retry |
| `invalidArgument(String)` | `031` | Invalid argument: a required parameter is empty, the track type doesn't match, etc. | Check the arguments |
| `featureNotSupported(String)` | `032` | The capability isn't supported by the current OS version / environment / mode: for example, screen sharing below macOS 12.3, ReplayKit unavailable, or simulcast on a track shared across multiple channels | Use a supported approach, or show the user a message |

---

### Virtual background

| Error | Low code | Description | Suggested handling |
| --- | :---: | --- | --- |
| `virtualBackgroundAlreadyInstalled` | `027` | The component is already installed; this call was discarded | Usually safe to ignore, or check `virtualBackground.isInstalled` first |
| `virtualBackgroundNotInstalled` | `028` | The toggle was called before the component was installed | Call `installVirtualBackground()` first |
| `virtualBackgroundModelNotFound(String)` | `029` | The model file doesn't exist | Check `modelPath`; pass `nil` to use the built-in model |
| `virtualBackgroundSessionFailed(String)` | `030` | Failed to create the inference session | A runtime environment issue; investigate with the logs |

For usage, see [Virtual background](/en/rtc/swift/advanced/virtual-background).

---

### Recommended error handling

```swift
do {
    try await viewModel.join(with: token)
} catch let error as SRTCError {
    switch error {
    case .tokenExpired, .tokenInvalid:
        // Get a new token
        break
    case .cameraPermissionDenied, .microphonePermissionDenied:
        showPermissionGuide()
    default:
        // Map baseCode to a user-facing message; write message only to the logs
        showToast(myHint(for: error.baseCode))
        log(error.localizedDescription)
    }
} catch {
    print("Unknown error:", error.localizedDescription)
}
```

`SRTCError` is distributed with library evolution enabled, and later versions may add cases; keep a `default` branch in your `switch`.
