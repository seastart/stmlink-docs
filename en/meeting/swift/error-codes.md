---
title: "Error handling"
description: "The SMeetingError enum of the SMeeting Swift SDK: every case with its client code, how codes get the iOS 203 / macOS 205 prefix while server codes pass through, common causes of unauthorized, a recommended do-catch pattern, and which APIs never throw. Read when handling or troubleshooting errors."
---

The error type the SDK throws is `SMeetingError`, a semantic Swift enum that also provides an integer error code.

+ Use `switch` to branch on meaning
+ Use `error.code` to get the integer error code, handy for logs and support tickets
+ Use `error.message` to get a plain-text description
+ `error.localizedDescription` outputs `"<code>: <message>"`

---

### Error list

| Error | Client code | Description | Suggested handling |
| --- | :---: | --- | --- |
| `notLoggedIn` | `1` | `您尚未登录meeting sdk` (You are not logged in to the meeting SDK) | Call `login(token:)` first |
| `tokenExpired` | `2` | `token已过期` (The token has expired) | Get a new token from your backend |
| `notInMeeting` | `3` | `您不在会议中` (You are not in a meeting) | Check when you call it; in-meeting APIs require `enterRoom` first |
| `unauthorized` | `4` | `您没有权限进行此操作` (You don't have permission for this operation) | Check the room policies and your own role; see below |
| `tokenInvalid` | `5` | `Token 格式无效` (Invalid token format) | Check your backend's issuing logic and whether the token was truncated in transit |
| `alreadyInMeeting` | `6` | `已在会议中，请先退出` (Already in a meeting; exit it first) | Call `exitRoom()` before entering a new meeting |
| `networkError(String)` | `7` | `网络错误: <detail>` (Network error: \<detail\>) | Ask the user to check the network and retry |
| `deviceError(String)` | `8` | `设备错误: <detail>` (Device error: \<detail\>) | Check whether the device is turned on and whether it's in use |
| `internalError(String)` | `9` | `内部错误: <detail>` (Internal error: \<detail\>) | Troubleshoot using the associated string and logs |
| `apiError(code:message:)` | Server code | Business error returned by the server | Handle it by the server error code; `message` can be shown to the user directly |

---

### Error code format

`SMeetingError.code` returns the full, assembled error code:

+ **Client errors** (those in the table above whose client code is less than 1000) get a platform prefix, forming a 6-digit number: the iOS prefix is `203`, and the macOS prefix is `205`
+ **Errors passed through from the server** (`apiError` with a server code of 1000 or greater) are kept as-is, without a prefix

Examples:

| Scenario | iOS | macOS |
| --- | --- | --- |
| `notLoggedIn` | `203001` | `205001` |
| `unauthorized` | `203004` | `205004` |
| Server returns `2001` | `2001` | `2001` |

This lets you tell at a glance whether an error was "stopped by the client itself" or "returned by the server."

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
        showToast(message)
        log("meeting api error \(code)")
    default:
        showToast(error.message)
        log(error.localizedDescription)
    }
} catch {
    // Errors thrown by the underlying audio and video layer
    log("\(error)")
}
```

Key points:

+ Besides `SMeetingError`, the underlying audio and video layer may also throw its own error types (for example, capture failures or connection failures), so don't omit the catch-all `catch` branch
+ Prefer `error.message` when showing messages to end users; use `error.localizedDescription` when writing logs, because it includes the error code
+ `SMeetingError` conforms to `Equatable`, so you can compare it directly with a specific case

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
