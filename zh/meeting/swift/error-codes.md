---
title: "错误处理"
description: "SMeeting Swift SDK 的错误类型 SMeetingError：完整错误码规则（iOS 203xxx / macOS 205xxx）、各 case 的低位码与处理建议、language 与后端错误文案"
---

SDK 对外抛出的错误类型是 `SMeetingError`，一个带语义的 Swift 枚举，同时提供跨端统一的整数错误码。

+ 用 `switch` 按语义分支处理
+ 用 `error.code` 拿到完整错误码，`error.baseCode` 拿到低 3 位语义码，方便日志、工单与跨端对照
+ 用 `error.message` 拿到英文描述；`error.localizedDescription` 输出 `"<code>: <message>"`
+ RTC 层（采集、权限、推拉流）的错误以 `SRTCError` **原样透传**，见 [SRTC 错误码](/zh/rtc/swift/error-codes)

<Note>
自 **1.4.0** 起错误码按跨端统一码表调整、报错文案改为英文。1.3.10 及以前的旧码与新码的对照见 [更新日志](/zh/meeting/swift/changelog)。
</Note>

---

### 错误清单

| 错误 | 低位码 | 描述（`message`） | 建议处理 |
| --- | :---: | --- | --- |
| `notLoggedIn` | `001` | `Not logged in to the meeting SDK` | 先调用 `login(token:)` |
| `tokenExpired` | `002` | `Token has expired` | 向业务后端重新获取 token |
| `notInMeeting` | `003` | `Not in a meeting` | 检查调用时机，会中接口需要先 `enterRoom` |
| `unauthorized` | `004` | `You don't have permission for this operation` | 检查房间策略与自己的角色，见下文 |
| `tokenInvalid` | `005` | `Invalid token format` | 检查后端签发逻辑与传输过程中是否被截断 |
| `alreadyInMeeting` | `006` | `Already in a meeting; exit first` | 先 `exitRoom()` 再进入新会议 |
| `networkError(String)` | `007` | `Network error: <detail>` | 连不上、非 HTTP 响应等，提示用户检查网络后重试 |
| `httpError(status:message:)` | `007` | `Network error: HTTP <status>: <detail>` | HTTP 非 200，`httpStatus` 为状态码；提示重试并记录状态码 |
| `deviceError(String)` | `008` | `Device error: <detail>` | 保留；采集 / 权限失败以 `SRTCError` 透传 |
| `internalError(String)` | `009` | `Internal error: <detail>` | 结合关联字符串与日志排查 |
| `userNotFound(String)` | `010` | `User not found in the meeting: <uid>` | 以最新的成员列表为准 |
| `invalidState(String)` | `011` | `Invalid state: <detail>` | 当前状态不允许该操作（如尚未开启摄像头、已开启共享），检查调用顺序 |
| `invalidArgument(String)` | `012` | `Invalid argument: <detail>` | 检查传参 |
| `remoteTrackUnavailable(uid:desc:)` | `209` | `Remote track not found: uid=<uid> desc=<desc>` | 成员在、但这路轨道不存在（对方未开启或已关闭），等待轨道事件后再订阅 |
| `requestTimeout(String)` | `353` | `Request timeout: <detail>` | 提示网络较慢并重试 |
| `requestCancelled` | `354` | `Request cancelled` | 调用方取消了任务，通常可忽略 |
| `responseParseFailed(String)` | `356` | `Response parse failed: <detail>` | 响应不是 JSON、缺 `code` 字段或结构不符，检查服务端与 SDK 版本 |
| `apiError(code:message:)` | 服务端码 | 服务端返回的业务错误文案 | 按服务端错误码处理，文案语言随 `language` |

`message` 是给开发者和日志看的英文描述，**给终端用户的提示请按 `code` / `baseCode` 自行映射**，不要直接展示 `message`。

---

### 错误码规则

`SMeetingError.code` 返回的是完整错误码：

+ **客户端错误**：平台前缀 + 3 位低位码。iOS 前缀 `203`，macOS 前缀 `205`
+ **服务端透传错误**（`apiError` 且服务端码不小于 1000）原样保留，不加前缀
+ **HTTP 状态码不会拼进错误码**：HTTP 非 200 一律为 `007`（`httpError`），状态在 `httpStatus` 里

`baseCode` 是低 3 位语义码，与 Web / Android / 鸿蒙等端同义；服务端码的 `baseCode` 返回自身。

举例：

| 场景 | iOS | macOS | `baseCode` |
| --- | --- | --- | --- |
| `notLoggedIn` | `203001` | `205001` | `1` |
| `unauthorized` | `203004` | `205004` | `4` |
| HTTP 500 | `203007` | `205007` | `7` |
| 服务端返回 `2001` | `2001` | `2001` | `2001` |

这样一眼就能区分「客户端自己拦下来的」和「服务端返回的」。

`SMeetingError` 实现了 `CustomNSError`：桥接成 `NSError` 后 `domain = "cn.seastart.smeeting"`、`code` 为完整码，ObjC / uni-app / Flutter 等走 `NSError` 的集成方可直接按码判断。

---

### 报错语言

`meeting.language`（如 `"en"`、`"zh-CN"`，`nil` 跟随系统语言）与 `meeting.srtc.language` 是同一个进程级设置。会议层和 RTC 层请求后端时都带上 `Accept-Language`，**后端业务错误（码 ≥ 1000）的文案**随之返回中文或英文；SDK 自身的报错一律英文，不受影响。

```swift
meeting.language = "en"   // 建议在 login 之前设置
```

---

### `unauthorized` 的常见来源

这是最容易遇到的一个错误，几乎都来自房间策略：

| 调用 | 触发条件 |
| --- | --- |
| `requestOpenMic(...)` | 房间全体静音且禁止自我解除，且你不是主持人 / 联席主持人 |
| `requestOpenCamera(...)` | 房间全体禁画且禁止自我解除，且你不是主持人 / 联席主持人 |
| `requestShare(...)` | 房间禁止共享，且你不是主持人 / 联席主持人 |

建议在 UI 上根据 `RoomInfo` 提前把按钮置灰，而不是让用户点了才收到报错。

---

### 推荐的处理方式

```swift
do {
    try await meeting.requestOpenMic()
} catch let error as SMeetingError {
    switch error {
    case .tokenExpired, .tokenInvalid, .notLoggedIn:
        await reLogin()
    case .unauthorized:
        showToast("主持人已开启全体静音")
    case .apiError(let code, let message):
        showToast(message)   // 服务端文案，语言随 language
        log("meeting api error \(code)")
    default:
        showToast(myHint(for: error.baseCode))
        log(error.localizedDescription)
    }
} catch let error as SRTCError {
    // RTC 层透传的错误，如 103231 无摄像头权限、103251 无麦克风权限、103039 屏幕共享被拒
    showToast(myHint(for: error.baseCode))
    log(error.localizedDescription)
} catch {
    log("\(error)")
}
```

要点：

+ 除了 `SMeetingError`，RTC 层的 `SRTCError` 也会原样抛出，两类都要处理
+ 面向最终用户的提示请按 `baseCode` 映射成自己的文案；写日志时用 `error.localizedDescription`，它带错误码
+ `SMeetingError` 遵循 `Equatable`，可以直接和具体 case 比较；它以库演进模式分发，后续版本可能新增 case，`switch` 里请保留 `default` 分支

---

### 不会抛错的接口

以下接口设计成不抛错，可以放心直接调用，重复调用或状态不匹配时会被安全忽略：

+ `logout()`
+ `exitRoom()`
+ `closeMic()` / `closeCamera()` / `stopShare()`
+ `disableIm()`
+ `toggleRemoteAudioMute(_:)`
+ `getRoomInfo()` / `getWhiteBoard()` / `getUsersInfo()` / `getUsersInfoList()` / `getRemoteVideoTrack(uid:desc:)` / `getDevices(kind:)`

---

### 相关页面

+ [核心概念](/zh/meeting/swift/key-concepts)
+ [接口文档 - SMeetingEngine](/zh/meeting/swift/api-reference/SMeetingEngine)
