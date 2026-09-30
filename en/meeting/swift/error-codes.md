---
title: "Error handling"
description: "SMeetingError, the error type of the SMeeting Swift SDK: the full error code format (iOS 203xxx / macOS 205xxx), the low code and suggested handling for each case, how language affects server error messages, common causes of unauthorized, and a recommended do-catch pattern. Read when handling or troubleshooting errors."
---

The error type the SDK throws is `SMeetingError`, a semantic Swift enum that also provides integer error codes unified across platforms.

+ Use `switch` to branch on meaning
+ Use `error.code` to get the full error code and `error.baseCode` to get the low 3-digit semantic code, handy for logs, support tickets, and cross-platform comparison
+ Use `error.message` to get the English description; `error.localizedDescription` outputs `"<code>: <message>"`
+ Errors from the RTC layer (capture, permissions, publishing and subscribing) are **passed through unchanged** as `SRTCError`; see [SRTC error codes](/en/rtc/swift/error-codes)

<Note>
Since **1.4.0**, error codes are adjusted according to the cross-platform unified table, and error messages are in English. For the mapping between the old codes (1.3.10 and earlier) and the new ones, see the [Changelog](/en/meeting/swift/changelog).
</Note>

---

### Error list

| Error | Low code | Description (`message`) | Suggested handling |
| --- | :---: | --- | --- |
| `notLoggedIn` | `001` | `Not logged in to the meeting SDK` | Call `login(token:)` first |
| `tokenExpired` | `002` | `Token has expired` | Get a new token from your backend |
| `notInMeeting` | `003` | `Not in a meeting` | Check when you call it; in-meeting APIs require `enterRoom` first |
| `unauthorized` | `004` | `You don't have permission for this operation` | Check the room policies and your own role; see below |
| `tokenInvalid` | `005` | `Invalid token format` | Check your backend's issuing logic and whether the token was truncated in transit |
| `alreadyInMeeting` | `006` | `Already in a meeting; exit first` | Call `exitRoom()` before entering a new meeting |
| `networkError(String)` | `007` | `Network error: <detail>` | Can't connect, non-HTTP response, etc.; ask the user to check the network and retry |
| `httpError(status:message:)` | `007` | `Network error: HTTP <status>: <detail>` | Non-200 HTTP response; `httpStatus` holds the status code. Prompt a retry and log the status code |
| `deviceError(String)` | `008` | `Device error: <detail>` | Reserved; capture / permission failures are passed through as `SRTCError` |
| `internalError(String)` | `009` | `Internal error: <detail>` | Troubleshoot using the associated string and logs |
| `userNotFound(String)` | `010` | `User not found in the meeting: <uid>` | Go by the latest member list |
| `invalidState(String)` | `011` | `Invalid state: <detail>` | The current state doesn't allow this operation (for example, the camera isn't on yet, or sharing is already on); check the call order |
| `invalidArgument(String)` | `012` | `Invalid argument: <detail>` | Check the arguments |
| `remoteTrackUnavailable(uid:desc:)` | `209` | `Remote track not found: uid=<uid> desc=<desc>` | The member is present but this track doesn't exist (they haven't turned it on, or have turned it off); wait for the track event before subscribing |
| `requestTimeout(String)` | `353` | `Request timeout: <detail>` | Tell the user the network is slow and retry |
| `requestCancelled` | `354` | `Request cancelled` | The caller canceled the task; usually safe to ignore |
| `responseParseFailed(String)` | `356` | `Response parse failed: <detail>` | The response isn't JSON, lacks the `code` field, or has an unexpected structure; check the server and SDK versions |
| `apiError(code:message:)` | Server code | Business error message returned by the server | Handle it by the server error code; the message language follows `language` |

`message` is an English description for developers and logs. **For messages shown to end users, map `code` / `baseCode` yourself**—don't show `message` directly.

---

### Error code format

`SMeetingError.code` returns the full error code:

+ **Client errors**: platform prefix + a 3-digit low code. The iOS prefix is `203` and the macOS prefix is `205`
+ **Errors passed through from the server** (`apiError` with a server code of 1000 or greater) are kept as-is, without a prefix
+ **HTTP status codes are never folded into the error code**: non-200 HTTP responses are always `007` (`httpError`), with the status in `httpStatus`

`baseCode` is the low 3-digit semantic code and means the same as on Web, Android, HarmonyOS, and other platforms; for server codes, `baseCode` returns the code itself.

Examples:

| Scenario | iOS | macOS | `baseCode` |
| --- | --- | --- | --- |
| `notLoggedIn` | `203001` | `205001` | `1` |
| `unauthorized` | `203004` | `205004` | `4` |
| HTTP 500 | `203007` | `205007` | `7` |
| Server returns `2001` | `2001` | `2001` | `2001` |

This lets you tell at a glance whether an error was "stopped by the client itself" or "returned by the server."

`SMeetingError` implements `CustomNSError`: once bridged to `NSError`, `domain = "cn.seastart.smeeting"` and `code` is the full code. Integrations that go through `NSError`, such as ObjC, uni-app, or Flutter, can check the code directly.

---

### Error language

`meeting.language` (such as `"en"` or `"zh-CN"`; `nil` follows the system language) is the same process-wide setting as `meeting.srtc.language`. Requests from both the meeting layer and the RTC layer to the backend carry `Accept-Language`, and **the messages of backend business errors (codes ≥ 1000)** come back in Chinese or English accordingly; the SDK's own errors are always in English and aren't affected.

```swift
meeting.language = "en"   // Set it before login
```

---

### Common sources of `unauthorized`

This is the error you're most likely to run into, and it almost always comes from room policies:

| Call | Trigger condition |
| --- | --- |
| `requestOpenMic(...)` | The room has mute all on and members aren't allowed to unmute themselves, and you're not the host / a co-host |
| `requestOpenCamera(...)` | The room has camera off for everyone and members aren't allowed to turn them back on themselves, and you're not the host / a co-host |
| `requestShare(...)` | The room has sharing disabled, and you're not the host / a co-host |

We recommend graying out buttons in the UI in advance based on `RoomInfo`, rather than letting users tap them and then get an error.

---

### Recommended handling

```swift
do {
    try await meeting.requestOpenMic()
} catch let error as SMeetingError {
    switch error {
    case .tokenExpired, .tokenInvalid, .notLoggedIn:
        await reLogin()
    case .unauthorized:
        showToast("The host has muted everyone")
    case .apiError(let code, let message):
        showToast(message)   // Server message; its language follows language
        log("meeting api error \(code)")
    default:
        showToast(myHint(for: error.baseCode))
        log(error.localizedDescription)
    }
} catch let error as SRTCError {
    // Errors passed through from the RTC layer, such as 103231 no camera permission, 103251 no microphone permission, 103039 screen sharing denied
    showToast(myHint(for: error.baseCode))
    log(error.localizedDescription)
} catch {
    log("\(error)")
}
```

Key points:

+ Besides `SMeetingError`, the RTC layer's `SRTCError` is also thrown unchanged; handle both
+ For messages shown to end users, map `baseCode` to your own text; use `error.localizedDescription` when writing logs, because it includes the error code
+ `SMeetingError` conforms to `Equatable`, so you can compare it directly with a specific case; it's distributed with library evolution enabled, and later versions may add cases, so keep a `default` branch in your `switch`

---

### APIs that don't throw

The following APIs are designed not to throw, so you can call them directly; repeated calls or calls in a mismatched state are safely ignored:

+ `logout()`
+ `exitRoom()`
+ `closeMic()` / `closeCamera()` / `stopShare()`
+ `disableIm()`
+ `toggleRemoteAudioMute(_:)`
+ `getRoomInfo()` / `getWhiteBoard()` / `getUsersInfo()` / `getUsersInfoList()` / `getRemoteVideoTrack(uid:desc:)` / `getDevices(kind:)`

---

### Related pages

+ [Key concepts](/en/meeting/swift/key-concepts)
+ [API reference - SMeetingEngine](/en/meeting/swift/api-reference/SMeetingEngine)
