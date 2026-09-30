---
title: "错误码"
description: "SRTC Swift SDK 的错误类型 SRTCError：完整错误码规则（iOS 103xxx / macOS 105xxx）、各 case 的低位码与处理建议、language 与后端错误文案"
---

Swift SDK 对外抛出的错误类型是 `SRTCError`，一个带语义的 Swift 枚举，同时提供跨端统一的整数错误码：

+ 用 `switch` 按 case 分支处理
+ 用 `error.code` 拿到完整错误码，`error.baseCode` 拿到低 3 位语义码
+ 用 `error.message` 拿到英文描述；`error.localizedDescription` 输出 `"<code>: <message>"`

<Note>
自 **1.5.0** 起错误码按跨端统一码表重排、报错文案改为英文。1.4.7 及以前的旧码与新码的对照见 [更新日志](/zh/rtc/swift/changelog)。
</Note>

---

### 错误码规则

`SRTCError.code` 返回的是完整错误码：

+ **SDK 自身的错误**：平台前缀 + 3 位低位码。iOS 前缀 `103`，macOS 前缀 `105`，如 iOS 无摄像头权限为 `103231`
+ **后端业务错误**（码 1000–99999）：原样透传，不加前缀
+ **HTTP 状态码不会拼进错误码**：HTTP 非 200、网络失败一律为 `006`，HTTP 状态只在 `apiRequestFailed` 的 `statusCode` 与描述里

`baseCode` 是低 3 位语义码，与 Web / Android / 鸿蒙等端同义，适合做跨端统一的提示映射；后端业务码的 `baseCode` 返回自身。

| 场景 | iOS `code` | macOS `code` | `baseCode` |
| --- | --- | --- | --- |
| `cameraPermissionDenied` | `103231` | `105231` | `231` |
| `notConnected` | `103001` | `105001` | `1` |
| 后端返回 `1002` | `1002` | `1002` | `1002` |

`SRTCError` 实现了 `CustomNSError`：桥接成 `NSError` 后 `domain = "cn.seastart.srtc"`、`code` 为完整码，有系统原始错误时（如 `screenShareDenied`）放在 `NSUnderlyingErrorKey`。ObjC / uni-app / Flutter 等走 `NSError` 的集成方可直接按码判断。

---

### 报错语言

+ `message` / `localizedDescription` **一律英文**，给开发者和日志看；**给终端用户的提示请按 `code` / `baseCode` 自行映射**，不要直接展示 `message`
+ `SRTCEngine.language`（如 `"en"`、`"zh-CN"`，`nil` 跟随系统语言）决定请求后端时的 `Accept-Language` 头，**后端业务错误（码 1000–99999）的文案**随之返回中文或英文；SDK 自身报错不受它影响

```swift
srtc.language = "en"   // 进程级全局设置，建议在 joinChannel / enableIm 之前设置
```

---

### 连接相关

| 错误 | 低位码 | 说明 | 建议处理 |
| --- | :---: | --- | --- |
| `notConnected` | `001` | 当前未连接 / 已离开频道 | 检查调用时机 |
| `tokenExpired` | `002` | Token 已过期 | 重新向业务后端获取 Token |
| `tokenInvalid` | `004` | Token 不合法 | 检查 Token 编码和签发逻辑 |
| `alreadyJoined` | `005` | 已经加入频道，或重复 `enableIm` | 避免重复调用，或先执行离开 |
| `connectionFailed(String)` | `006` | 连接失败 | 记录服务端地址、网络环境、错误详情 |
| `connectionTimeout` | `007` | 连接超时 | 提示用户重试并检查网络连通性 |

---

### 信令相关

| 错误 | 低位码 | 说明 | 建议处理 |
| --- | :---: | --- | --- |
| `apiRequestFailed(statusCode:message:)` | `006` / 后端码 | HTTP 非 200、网络请求失败（`statusCode` 为 HTTP 状态，网络失败为 `0`）；`statusCode` ≥ 1000 时是后端业务错误，`code` 即后端码 | 网络类错误提示重试；后端业务码按服务端错误码处理 |
| `signatureError` | `008` | 签名生成失败 | 检查服务端鉴权逻辑 |
| `signalingConnectFailed(String)` | `009` | 信令通道连接失败 | 检查网络可达性、代理与防火墙设置 |
| `signalingSubscribeFailed(String)` | `010` | 信令通道订阅失败 | 检查 Token 是否有效、连接是否已建立 |
| `messageDecodeFailed(String)` | `011` | 响应不是 JSON、缺 `code` 字段或结构不符 | 检查服务端响应格式与 SDK 版本兼容性 |

---

### WebRTC / 传输相关

| 错误 | 低位码 | 说明 | 建议处理 |
| --- | :---: | --- | --- |
| `webrtcError(String)` | `012` | 底层 WebRTC 错误 | 记录日志，优先定位设备和 SDP 过程 |
| `sdpNegotiationFailed(String)` | `013` | SDP 协商失败 | 检查编解码器、引擎能力和服务端协商 |
| `transportNotReady` | `014` | 传输层尚未就绪，或频道正在重连 | 稍后重试，或等待重连完成 |
| `peerConnectionFailed` | `015` | PeerConnection 进入 failed / closed | 检查 ICE / STUN / TURN 与网络环境 |

---

### 轨道与采集相关

| 错误 | 低位码 | 说明 | 建议处理 |
| --- | :---: | --- | --- |
| `trackNotFound(String)` | `003` | 找不到指定轨道 | 检查 `uid` / `trackId` 是否匹配 |
| `trackAlreadyPublished(String)` | `016` | 轨道已发布 | 避免重复发布同一对象 |
| `trackNotPublished(String)` | `017` | 轨道未发布 | 取消发布前先确认状态 |
| `captureError(String)` | `018` | 其它采集失败 | 检查设备占用、结合描述排查 |
| `codecNotSupported(String)` | `019` | 编解码器不支持 | 调整编码偏好或预设 |
| `maxPublishLimitReached` | `020` | 超过可发布轨道上限 | 控制并发发布数量 |
| `deviceNotFound(String)` | `021` | 找不到设备：没有可用摄像头 / 显示器，或设备已拔出 | 检查设备列表是否变化 |
| `userNotFound(String)` | `204` | 频道内没有该用户（如订阅的用户已离开） | 以最新的用户列表为准 |
| `cameraPermissionDenied` | `231` | 无摄像头权限 | 引导用户到系统设置开启；确认 Info.plist 含 `NSCameraUsageDescription` |
| `cameraFormatUnavailable(String)` | `242` | 摄像头没有可用的采集格式 | 换一个设备或降低采集规格 |
| `microphonePermissionDenied` | `251` | 无麦克风权限（开麦时抛出） | 引导用户到系统设置开启；确认 Info.plist 含 `NSMicrophoneUsageDescription` |
| `screenShareDenied(String, underlying:)` | `039` | 屏幕共享被拒绝：用户在系统弹窗里取消，或系统未授予屏幕录制权限 | macOS 引导到「隐私与安全性 → 屏幕录制」开启；`underlying` 为系统原始错误 |
| `publishFailed(String)` | `300` | 发布失败：引擎未连接 / 已断开（非重连中）时发起发布等 | 重新入会后再发布 |
| `subscribeFailed(String)` | `301` | 订阅失败：引擎未连接 / 已断开（非重连中）时发起订阅等 | 重新入会后再订阅 |

---

### 引擎与通用错误

| 错误 | 低位码 | 说明 | 建议处理 |
| --- | :---: | --- | --- |
| `engineNotSupported(String)` | `022` | 当前流媒体引擎不支持 | 检查 `stream_vendor` 配置 |
| `engineDisconnected` | `023` | 引擎已断开 | 等待重连或重新入会 |
| `invalidState(String)` | `024` | 当前状态不允许该操作 | 检查调用顺序 |
| `internalError(String)` | `025` | SDK 内部错误 | 结合日志排查 |
| `cancelled` | `026` | 操作被取消 | 业务层通常可忽略或重试 |
| `invalidArgument(String)` | `031` | 参数非法：必填参数为空、轨道类型不符等 | 检查传参 |
| `featureNotSupported(String)` | `032` | 当前系统版本 / 环境 / 模式不支持该能力：如 macOS 12.3 以下共享屏幕、ReplayKit 不可用、多频道共享轨道开 simulcast | 换用支持的方式，或给用户提示 |

---

### 虚拟背景相关

| 错误 | 低位码 | 说明 | 建议处理 |
| --- | :---: | --- | --- |
| `virtualBackgroundAlreadyInstalled` | `027` | 组件已装载，本次指令被丢弃 | 通常可忽略，或先判 `virtualBackground.isInstalled` |
| `virtualBackgroundNotInstalled` | `028` | 组件未装载就调开关 | 先 `installVirtualBackground()` |
| `virtualBackgroundModelNotFound(String)` | `029` | 模型文件不存在 | 检查 `modelPath`；传 `nil` 用内置模型 |
| `virtualBackgroundSessionFailed(String)` | `030` | 推理会话创建失败 | 属运行环境问题，结合日志排查 |

用法见 [虚拟背景](/zh/rtc/swift/advanced/virtual-background)。

---

### 推荐的错误处理方式

```swift
do {
    try await viewModel.join(with: token)
} catch let error as SRTCError {
    switch error {
    case .tokenExpired, .tokenInvalid:
        // 重新获取 Token
        break
    case .cameraPermissionDenied, .microphonePermissionDenied:
        showPermissionGuide()
    default:
        // 按 baseCode 映射成面向用户的提示，message 只写日志
        showToast(myHint(for: error.baseCode))
        log(error.localizedDescription)
    }
} catch {
    print("Unknown error:", error.localizedDescription)
}
```

`SRTCError` 以库演进模式分发，后续版本可能新增 case，`switch` 里请保留 `default` 分支。
