---
title: "错误码规则与总表"
description: "SRTC 错误码的编号规则与跨端统一码表：从一个错误码看出它来自服务端还是哪个平台的 SDK，低 3 位码各端同义；含 language 参数说明、各端按新码发版的进度与旧码 → 新码对照。遇到不认识的错误码或升级 SDK 时读。"
---

`0` 代表成功，非 0 都是错误。

错误码分两类：**4~5 位的是服务端返回的业务错误码**，**6 位的是客户端 SDK 自己产生的错误码**。6 位码的结构是 **端前缀 + 3 位低位码**，低 3 位按本页的统一码表分配，**同一个低位码在各端含义相同**。

---

## 怎么读一个错误码

```text
  1 0 6 2 3 1
  │ │ │ └─┴─┴── 低 3 位码 000-999：231 = 无摄像头权限（各端同义）
  │ │ └──────── 端侧类型：6 = Web
  └─┴────────── 业务层：10 = SRTC
```

| 位数 | 来源 | 结构 | 示例 |
| --- | --- | --- | --- |
| 4~5 位（1000–99999） | **服务端**返回，SDK 原样透传 | 服务端错误码 | `1021` Token 已被使用 |
| 6 位 | 客户端 **SDK** 产生 | `10` + 端侧类型 + 低 3 位 | `106231` Web 端：无摄像头权限 |

所以看到 `102231` 和 `106231`，读作：同一个错误（无摄像头权限），分别来自 Android 端和 Web 端。

---

## 端侧类型

| 类型 | 平台 | SRTC 前缀 |
| :---: | --- | --- |
| 1 | Windows | `101` |
| 2 | Android 手机 | `102` |
| 3 | iOS 手机 | `103` |
| 4 | Linux C/C++ | `104` |
| 5 | macOS | `105` |
| 6 | Web（WebRTC） | `106` |
| 7 | 小程序 | `107` |
| 8 | 鸿蒙（HarmonyOS NEXT） | `108` |
| 9 | Android 嵌入式 | `109` |
| 80 | 服务端 / 嵌入式接入（Go / Python / C SDK） | `180` |

<Note>
Swift SDK 同时支持 iOS 和 macOS，按运行平台使用 `103` 或 `105` 前缀。
</Note>

---

## 按码判断，不要按文案

+ **判断错误类型只看错误码**。SDK 自身的报错文案一律是英文，只给开发者和日志看，会随版本调整；不要拿它做分支判断，也不要直接展示给终端用户
+ 需要给终端用户看的提示，请按错误码自行映射。各平台错误码页的「建议给用户的提示」列给出了参考文案
+ 跨端对比同一类错误时，可以只比低 3 位（各端 SDK 提供 `baseCode` 之类的字段，具体见各平台错误码页）

### language 参数

各端 SDK 提供 `language` 设置（名称以各端接口文档为准，如 Web 的初始化参数 `language`、C SDK 的 `rtc_set_language`）：

+ 取值为语言标签，如 `zh-CN`、`en`。不设置时跟随系统语言，取不到时为中文
+ SDK 请求服务端时带上 `Accept-Language`，**服务端业务错误（1000–99999）的文案随之返回中文或英文**
+ **SDK 自身的报错（6 位码）固定为英文，不受 `language` 影响**
+ iOS（Objective-C）自 RTCEngineKit 3.2.1 起提供 `RTCEngineKit.language`（3.2.0 中 RTC 层请求不带 `Accept-Language`）

所以同一个应用里同时看到中文和英文的报错是正常的：前者来自服务端，后者来自 SDK。

---

## 统一码表（低 3 位）

号段：`000–099` 通用语义；`200–299` 频道 / 设备细分；`300–349` 流媒体。

**一种语义只有一个码**，各端遇到同一场景用同一个码。不是每个端都会用到全部的码，某端实际会产生哪些码见该端的错误码页。

| 低位 | 名称 | 含义 |
| :---: | --- | --- |
| 000 | Unknown | 未分类错误（兜底，正常不应出现） |
| 001 | NotInChannel | 不在频道内：未加入、已离开，或频道未开始 |
| 002 | TokenExpired | Token 已过期 |
| 003 | TrackNotFound | 流轨道不存在 |
| 004 | TokenInvalid | Token 不合法：解析失败或内容不完整 |
| 005 | AlreadyJoined | 已加入 / 重复操作冲突 |
| 006 | ConnectionFailed | 连接失败：网络请求失败或 HTTP 非 200（HTTP 状态见错误详情） |
| 007 | ConnectionTimeout | 连接 / 请求超时 |
| 008 | SignatureError | 签名错误 |
| 009 | SignalingConnectFailed | 信令连接失败 |
| 010 | SignalingSubscribeFailed | 信令订阅失败 |
| 011 | MessageDecodeFailed | 信令消息 / 服务端响应解析失败（不是 JSON、缺 `code` 字段、字段不合法） |
| 012 | WebrtcError | 底层 WebRTC / 媒体网络错误 |
| 013 | SdpNegotiationFailed | SDP 协商失败 |
| 014 | TransportNotReady | 传输未就绪 / 正在重连，稍后重试即可 |
| 015 | PeerConnectionFailed | 媒体连接（PeerConnection）创建失败或断开 |
| 016 | TrackAlreadyPublished | 同一轨道重复发布 |
| 017 | TrackNotPublished | 轨道未发布 |
| 018 | CaptureFailed | 采集失败：设备被占用、打开失败、硬件错误 |
| 019 | CodecNotSupported | 编解码器不支持 |
| 020 | MaxPublishLimitReached | 超过发布上限 |
| 021 | DeviceNotFound | 设备不存在，或指定的设备已拔出 |
| 022 | EngineNotSupported | 流媒体引擎不支持 |
| 023 | EngineDisconnected | 引擎已断开或已关闭（离开频道、销毁实例后仍在等待或调用） |
| 024 | InvalidState | 当前状态不允许该操作：调用顺序不对、未初始化、需在加入频道前设置 |
| 025 | InternalError | SDK 内部错误 |
| 026 | Cancelled | 操作被取消 |
| 027 | VirtualBackgroundAlreadyInstalled | 虚拟背景已安装 |
| 028 | VirtualBackgroundNotInstalled | 虚拟背景未安装 |
| 029 | VirtualBackgroundModelNotFound | 虚拟背景模型不存在或无效 |
| 030 | VirtualBackgroundSessionFailed | 虚拟背景处理失败 |
| 031 | InvalidArgument | 参数非法 |
| 032 | FeatureNotSupported | 当前环境 / 系统版本 / 模式不支持该能力 |
| 033 | TrackNotCaptured | 轨道还没采集（或已停止）就发布 / 播放 |
| 034 | MaxSubscribeLimitReached | 超过订阅上限 |
| 035 | PublishDescConflict | 发布描述（desc / 流槽位）已被其它轨道占用 |
| 036 | PlayFailed | 播放失败（不是自动播放策略导致） |
| 037 | PlayViewNotFound | 播放容器不存在 |
| 038 | PopupBlocked | 弹窗被浏览器拦截 |
| 039 | ScreenShareDenied | 屏幕共享被拒绝：用户取消，或系统未授权录屏 |
| 040 | NotMcuPublisher | 无权发布合成流（需以 MCU 身份接入） |
| 041 | OperationTooFrequent | 操作过于频繁 |
| 042 | PermissionDenied | 设备权限被拒（无法区分摄像头 / 麦克风时；能区分时用 231 / 251） |
| 043 | Forbidden | 当前身份 / 角色不允许该操作 |
| 044 | AudioRouteSwitchFailed | 音频路由切换失败 |
| 204 | UserNotFound | 频道内没有该用户 |
| 209 | ChannelJoinNativeException | 加入频道时底层异常（仅 Android） |
| 212 | ChannelResourceCreateFailed | 加入频道时本地资源创建失败（仅 Android） |
| 213 | ChannelJoinDisconnected | 加入频道过程中连接断开（仅 Android） |
| 231 | CameraPermissionDenied | 无摄像头权限 |
| 233 | CameraSessionFailed | 摄像头会话创建失败 |
| 234 | CameraRequestFailed | 摄像头采集请求失败 |
| 235 | CameraDisconnected | 摄像头被系统断开 |
| 239 | CameraFirstFrameTimeout | 摄像头首帧超时 |
| 242 | CameraFormatUnavailable | 摄像头格式不可用 |
| 243 | CameraOpenTimeout | 摄像头打开超时 |
| 244 | CameraSessionTimeout | 摄像头会话超时 |
| 251 | MicPermissionDenied | 无麦克风权限 |
| 255 | MicFormatUnsupported | 麦克风格式不支持 |
| 270 | ScreenCaptureRequestRejected | 屏幕共享请求不被受理：授权界面已销毁或重复请求（仅 Android） |
| 300 | PublishFailed | 发布失败（含流媒体引擎未连接 / 已断开） |
| 301 | SubscribeFailed | 订阅失败 / 订阅被拒 |
| 302 | PublishTimeout | 发布协商超时 |
| 303 | SubscribeTimeout | 订阅协商超时 |
| 304 | SubscribeTrackNotFound | 订阅时轨道还不存在，SDK 会自动重试（Go / Python / C SDK） |
| 312 | OperationIgnored | 操作被忽略，不算失败（仅 Android） |

几个容易混淆的码，按「最具体的原因优先」：

+ 媒体连接创建失败、或进入 failed / closed → **015**，不管发生在发布、订阅还是加入频道阶段
+ 正在重连、稍后可重试 → **014**；引擎已被关闭或销毁 → **023**
+ 流媒体引擎未连接（且不在重连中）时发布 / 订阅，或被拒绝、协商失败且没有更具体的码 → **300 / 301**
+ 当前环境不支持 → **032**，不用 018（采集失败）

---

## 各端按新码发版的进度

本表是 2026-09-30 定稿的第 2 版，**各端以自己按新码发版的版本为准**。尚未发版的端，仍以该端错误码页列出的码为准。

| 端 | 前缀 | 按本表发版的版本 |
| --- | --- | --- |
| Web | `106` | `@seastart/srtc-web-sdk` 0.7.0 起 |
| 微信小程序 | `107` | `@seastart/srtc-wx-sdk` 0.3.0 起 |
| C SDK / Python SDK | `180` | C SDK 0.1.0、Python SDK（`srtc`）0.2.0 起 |
| Swift（iOS / macOS） | `103` / `105` | SRTC Swift SDK 1.5.0 起（[更新日志](/zh/rtc/swift/changelog)） |
| iOS（Objective-C） | `103` | RTCEngineKit 3.2.0 起（[更新日志](/zh/rtc/ios/changelog)） |
| 鸿蒙 | `108` | SRTC 鸿蒙 SDK 1.1.0 起（[更新日志](/zh/rtc/harmony/changelog)） |
| Android、Windows | `102`、`101` | **尚未按新码发版**，以各端发版为准，目前仍按该端错误码页 |

---

## 旧码 → 新码对照

### 旧版通用码 `100001`–`100012`

旧版部分端（iOS Objective-C、Windows 等）对外的 `100xxx` 通用码取消，改为「本端前缀 + 低 3 位」。例如旧的 `100008`（令牌失效）变为「本端前缀 + `004`」。**该端按新码发版后生效。**

| 旧码 | 旧名称 | 新低位码 |
| :---: | --- | :---: |
| `100001` | SystemError | 025 |
| `100002` | NotInitialized | 024 |
| `100003` | MediaNotInitialized | 024 |
| `100004` | ProtocolParsingError | 011 |
| `100005` | Timeout | 007 |
| `100006` | InvalidArgs | 031 |
| `100007` | Conflict | 005 |
| `100008` | SdkTokenInvalid | 004 |
| `100009` | NetError | 006 |
| `100010` | MediaNetError | 012 |
| `100011` | NotFound | 204（查成员时）；其它「不存在」场景按语义，如 003 |
| `100012` | UserCancelled | 026 |

### 已按新码发版的端

| 端 | 主要变化 | 详细对照 |
| --- | --- | --- |
| Web / 微信小程序 | 以前大多落在兜底码 `106000` / `107000`，现在按场景拆成独立码；HTTP 失败由不带码的 `Error` 改为 `106006` / `107006`；采集与权限失败由浏览器原始异常改为 `106231` / `106251` / `106039` / `106021` / `106018`。`106001`–`106003` 含义不变 | [Web 更新日志](/zh/rtc/web/changelog) · [Web 错误码](/zh/rtc/web/error-codes) |
| C SDK / Python SDK | 以前落在 `180000` 或没有错误码的失败，现在都有具体的码；「无权发布合成流」由 `180004` 改为 `180040`，`180004` 改为表示 Token 不合法 | [C SDK 更新日志](/zh/rtc/capi/changelog) · [Python SDK 更新日志](/zh/rtc/python/changelog) |
| Swift | 见其更新日志中的对照表 | [Swift 更新日志](/zh/rtc/swift/changelog) |
| iOS（Objective-C） | `RTCEngineError` 枚举名保留、取值改为 `103` + 低 3 位，需重新编译；`100001`–`100012` 按上表映射；无权限由 `103001` 拆为 `103231`（摄像头）/ `103251`（麦克风）；新增虚拟背景 `103027`–`103030` | [iOS 更新日志](/zh/rtc/ios/changelog) · [iOS 错误码](/zh/rtc/ios/error-codes) |
| 鸿蒙 | 网络失败 / HTTP 非 200 由 `108404`、`108500` 等统一为 `108006`（HTTP 状态见 `httpStatus`）；采集异常由系统 `BusinessError` 改为 `SRTCError`（原码在 `systemCode`）；`001`–`026` 不变 | [鸿蒙更新日志](/zh/rtc/harmony/changelog) · [鸿蒙错误码](/zh/rtc/harmony/error-codes) |

其它端（Android、Windows）的旧码对照，随该端按新码发版时在其更新日志中给出。

---

## 排查时怎么用

| 码 | 说明 | 先看哪里 |
| --- | --- | --- |
| `1xxx` 等（1000–99999） | 服务端拒绝了请求 | 检查签名、Token、频道状态。见 [服务端 API 错误码](/zh/rtc/server-api/error-codes) |
| `10Nxxx` | 该平台 SDK 自身的错误，低 3 位见上方统一码表 | 见对应平台的错误码页 |
| `180xxx` | Go / Python / C SDK（服务端 / 嵌入式接入）自身的错误 | 见 [C SDK 错误码](/zh/rtc/capi/error-codes)、[Python SDK 错误码](/zh/rtc/python/error-codes) |

各平台完整错误码表：
[Web](/zh/rtc/web/error-codes) · [Android](/zh/rtc/android/error-codes) · [Windows](/zh/rtc/windows/error-codes) · [Swift](/zh/rtc/swift/error-codes) · [iOS](/zh/rtc/ios/error-codes) · [鸿蒙](/zh/rtc/harmony/error-codes) · [C](/zh/rtc/capi/error-codes) · [Python](/zh/rtc/python/error-codes)

<Note>
**C SDK 分两层看。** 它的**接口返回值**是 `0 / -1 / -2 / -3 / -4` 这样的简单状态值，只表达调用层面的结果、不含原因；具体原因用 `rtc_get_last_error` 取，也会打在日志里，那里既有 SDK 自身的 `180xxx`，也有服务端透传的 `1xxx`。见 [C SDK 错误码](/zh/rtc/capi/error-codes)。
</Note>

---

## 与 SMeeting 的区别

同一套规则，只是业务层号不同：SRTC 用 `10`，SMeeting 用 `20`，两层的低 3 位码是**两套独立的表**。

如果你用的是 SMeeting，会同时看到两类错误码：`20Nxxx` 来自会议层，`10Nxxx` 来自底层 SRTC（会议层原样透传，便于定位）。见 [SMeeting 错误码规则与总表](/zh/meeting/error-codes)。
