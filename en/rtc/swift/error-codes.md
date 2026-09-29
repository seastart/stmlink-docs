---
title: "Error codes"
description: "The SRTCError enum of the SRTC Swift SDK: cases for connection, signaling, WebRTC/transport, tracks and capture, engine, and virtual background errors, with a suggested fix for each, plus a recommended do/catch pattern. Read when handling errors thrown by the Swift SDK."
---

The error model currently exposed by the Swift SDK is `SRTCError`. It isn't a traditional table of integer error codes, but a Swift enum with semantic cases.

The benefits of this design:

+ Callers can branch directly on the error category
+ Error info can carry a context string
+ It fits Swift's `try / catch` style better than plain integer codes

---

### Connection

| Error | Description | Suggested handling |
| --- | --- | --- |
| `tokenExpired` | The token has expired | Get a new token from your backend |
| `tokenInvalid` | The token is invalid | Check the token encoding and issuing logic |
| `alreadyJoined` | Already joined the channel | Avoid joining twice, or leave first |
| `notConnected` | Not currently connected | Check when the call is made |
| `connectionFailed(String)` | Connection failed | Log the server address, network environment, and error details |
| `connectionTimeout` | Connection timed out | Prompt the user to retry and check network connectivity |

---

### Signaling

| Error | Description | Suggested handling |
| --- | --- | --- |
| `apiRequestFailed(statusCode:message:)` | HTTP API request failed | Check the response from the demo backend / your backend |
| `signatureError` | Failed to generate the signature | Check the server-side authentication logic |
| `signalingConnectFailed(String)` | Failed to connect the signaling channel | Check network reachability, proxy, and firewall settings |
| `signalingSubscribeFailed(String)` | Failed to subscribe on the signaling channel | Check that the token is valid and the connection is established |
| `messageDecodeFailed(String)` | Failed to decode a signaling message | Check the server message format and SDK version compatibility |

---

### WebRTC / transport

| Error | Description | Suggested handling |
| --- | --- | --- |
| `webrtcError(String)` | Underlying WebRTC error | Log it; start by investigating devices and the SDP process |
| `sdpNegotiationFailed(String)` | SDP negotiation failed | Check codecs, engine capabilities, and server-side negotiation |
| `transportNotReady` | The transport layer isn't ready yet | Wait for the connection to complete before publishing / subscribing |
| `peerConnectionFailed` | PeerConnection creation or operation failed | Check ICE / STUN / TURN / platform permissions |

---

### Tracks and capture

| Error | Description | Suggested handling |
| --- | --- | --- |
| `trackNotFound(String)` | The specified track wasn't found | Check that `uid` / `trackId` match |
| `trackAlreadyPublished(String)` | The track is already published | Avoid publishing the same object twice |
| `trackNotPublished(String)` | The track isn't published | Confirm the state before unpublishing |
| `captureError(String)` | Capture failed | Check permissions, whether the device is in use, and the platform version |
| `codecNotSupported(String)` | Codec not supported | Adjust the encoding preference or preset |
| `maxPublishLimitReached` | The limit of publishable tracks was exceeded | Limit the number of concurrently published tracks |
| `deviceNotFound(String)` | Device not found | Check whether the device list changed or the device was unplugged |

---

### Engine and general errors

| Error | Description | Suggested handling |
| --- | --- | --- |
| `engineNotSupported(String)` | Not supported by the current media streaming engine | Check the `stream_vendor` configuration |
| `engineDisconnected` | The engine is disconnected | Wait for reconnection or rejoin the channel |
| `invalidState(String)` | The current state doesn't allow this operation | Check the call order |
| `internalError(String)` | Internal SDK error | Investigate with the logs |
| `cancelled` | The operation was canceled | Your code can usually ignore it or retry |

---

### Virtual background

| Error | Description | Suggested handling |
| --- | --- | --- |
| `virtualBackgroundAlreadyInstalled` | The component is already installed; this call was discarded | Usually safe to ignore, or check `virtualBackground.isInstalled` first |
| `virtualBackgroundNotInstalled` | The toggle was called before the component was installed | Call `installVirtualBackground()` first |
| `virtualBackgroundModelNotFound(String)` | The model file doesn't exist | Check `modelPath`; pass `nil` to use the built-in model |
| `virtualBackgroundSessionFailed(String)` | Failed to create the inference session | A runtime environment issue; investigate with the logs |

For usage, see [Virtual background](/zh/rtc/swift/advanced/virtual-background) (Chinese).

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
    case .captureError(let message):
        print("Capture failed:", message)
    default:
        print("SRTC error:", error.localizedDescription)
    }
} catch {
    print("Unknown error:", error.localizedDescription)
}
```

If your app already has a unified error dialog, map `SRTCError` to your own error domain rather than exposing the English `localizedDescription` directly to end users.
