---
title: "错误处理"
description: "SMeeting Swift SDK 错误类型 SMeetingError 的分类、错误码规则与处理建议"
---

SDK 对外抛出的错误类型是 `SMeetingError`，一个带语义的 Swift 枚举，同时提供整数错误码。

+ 用 `switch` 按语义分支处理
+ 用 `error.code` 拿到整数错误码，方便日志与工单排查
+ 用 `error.message` 拿到纯文本描述
+ `error.localizedDescription` 输出 `"<code>: <message>"`

---

### 错误清单

| 错误 | 客户端码 | 描述 | 建议处理 |
| --- | :---: | --- | --- |
| `notLoggedIn` | `1` | 您尚未登录 meeting sdk | 先调用 `login(token:)` |
| `tokenExpired` | `2` | token 已过期 | 向业务后端重新获取 token |
| `notInMeeting` | `3` | 您不在会议中 | 检查调用时机，会中接口需要先 `enterRoom` |
| `unauthorized` | `4` | 您没有权限进行此操作 | 检查房间策略与自己的角色，见下文 |
| `tokenInvalid` | `5` | Token 格式无效 | 检查后端签发逻辑与传输过程中是否被截断 |
| `alreadyInMeeting` | `6` | 已在会议中，请先退出 | 先 `exitRoom()` 再进入新会议 |
| `networkError(String)` | `7` | 网络错误 | 提示用户检查网络后重试 |
| `deviceError(String)` | `8` | 设备错误 | 检查设备是否已开启、是否被占用 |
| `internalError(String)` | `9` | 内部错误 | 结合关联字符串与日志排查 |
| `apiError(code:message:)` | 服务端码 | 服务端返回的业务错误 | 按服务端错误码处理，`message` 可直接用于提示 |

---

### 错误码规则

`SMeetingError.code` 返回的是拼接后的完整错误码：

+ **客户端错误**（上表中客户端码小于 1000 的那些）会加上平台前缀，拼成 6 位数：iOS 前缀 `203`，macOS 前缀 `205`
+ **服务端透传错误**（`apiError` 且服务端码不小于 1000）原样保留，不加前缀

举例：

| 场景 | iOS | macOS |
| --- | --- | --- |
| `notLoggedIn` | `203001` | `205001` |
| `unauthorized` | `203004` | `205004` |
| 服务端返回 `2001` | `2001` | `2001` |

这样一眼就能区分「客户端自己拦下来的」和「服务端返回的」。

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
        showToast(message)
        log("meeting api error \(code)")
    default:
        showToast(error.message)
        log(error.localizedDescription)
    }
} catch {
    // 底层音视频层抛出的错误
    log("\(error)")
}
```

要点：

+ 除了 `SMeetingError`，底层音视频层也可能抛出自己的错误类型（例如采集失败、连接失败），所以 `catch` 兜底分支不要省
+ 面向最终用户提示时优先用 `error.message`；写日志时用 `error.localizedDescription`，它带错误码
+ `SMeetingError` 遵循 `Equatable`，可以直接和具体 case 比较

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
+ [接口文档 - SMeeting](/zh/meeting/swift/api-reference/SMeeting)
