---
title: "错误码规则与总表"
description: "SMeeting 错误码的编号规则与会议层跨端统一码表，以及为什么会同时看到 20Nxxx 和 10Nxxx 两类错误码；含 language 参数说明、各端按新码发版的进度与旧码 → 新码对照。遇到不认识的错误码或升级 SDK 时读。"
---

`0` 代表成功，非 0 都是错误。

错误码分两类：**4~5 位的是服务端返回的业务错误码**，**6 位的是客户端 SDK 自己产生的错误码**。6 位码的结构是 **端前缀 + 3 位低位码**，会议层的低 3 位按本页的统一码表分配，**同一个低位码在各端含义相同**。

---

## 怎么读一个错误码

```text
  2 0 6 0 0 3
  │ │ │ └─┴─┴── 低 3 位码 000-999：003 = 不在会议中（各端同义）
  │ │ └──────── 端侧类型：6 = Web
  └─┴────────── 业务层：20 = SMeeting
```

| 位数 | 来源 | 结构 | 示例 |
| --- | --- | --- | --- |
| 4~5 位（1000–99999） | **服务端**返回，SDK 原样透传 | 服务端错误码 | `2xxx` 会议服务的业务错误 |
| 6 位 | 会议层 **SDK** 产生 | `20` + 端侧类型 + 低 3 位 | `206003` Web 端：不在会议中 |

---

## 端侧类型

| 类型 | 平台 | SMeeting 前缀 |
| :---: | --- | --- |
| 1 | Windows | `201` |
| 2 | Android 手机 | `202` |
| 3 | iOS 手机 | `203` |
| 4 | Linux C/C++ | `204` |
| 5 | macOS | `205` |
| 6 | Web | `206` |
| 7 | 小程序 | `207` |
| 8 | 鸿蒙（HarmonyOS NEXT） | `208` |
| 9 | Android 嵌入式 | `209` |

<Note>
Swift SDK 同时支持 iOS 和 macOS，会按运行平台自动使用 `203` 或 `205` 前缀。
</Note>

---

## 为什么会看到 10Nxxx 开头的错误码

**这是正常的，不是 bug。**

SMeeting 建在 SRTC 之上。当错误发生在底层音视频通道时（如采集失败、设备权限被拒、推拉流失败），SMeeting 会把 SRTC 的原始错误码**原样透传**给你，而不是包装成自己的码 —— 这样你能直接定位到问题出在哪一层。

| 你看到的 | 含义 | 去哪儿查 |
| --- | --- | --- |
| `2xxx` 等 | 会议服务端拒绝了请求（无权限、会议不存在……） | [服务端 API 错误码](/zh/meeting/server-api/error-codes) |
| `20Nxxx` | 会议层 SDK 的错误 | 下方统一码表、对应平台的错误码页 |
| `1xxx` | 底层 SRTC **服务端**错误 | [SRTC 错误码规则与总表](/zh/rtc/error-codes) |
| `10Nxxx` | 底层 SRTC **客户端**错误（如「无摄像头权限」`106231`） | [SRTC 错误码规则与总表](/zh/rtc/error-codes) |

会议层和 SRTC 层的低 3 位是**两套独立的表**：在 Web 会议 SDK 里同时看到 `206003` 和 `106003` 并不矛盾，前者是「不在会议中」，后者是「流轨道不存在」。所以会议 SDK 里判断错误时请比较**完整的 6 位码**，不要只比低 3 位。

<Tip>
排查时先看前两位：`20` 开头找会议层的原因（权限、会议状态、成员角色），`10` 开头找音视频层的原因（设备、Token、频道、网络）。
</Tip>

---

## 按码判断，不要按文案

+ **判断错误类型只看错误码**。SDK 自身的报错文案一律是英文，只给开发者和日志看，会随版本调整；不要拿它做分支判断，也不要直接展示给终端用户
+ 需要给终端用户看的提示，请按错误码自行映射。各平台错误码页的「建议给用户的提示」列给出了参考文案

### language 参数

各端会议 SDK 提供 `language` 设置（名称以各端接口文档为准，如 Web 的初始化参数 `language`），**会同时设置底层 SRTC**：

+ 取值为语言标签，如 `zh-CN`、`en`。不设置时跟随系统语言，取不到时为中文
+ SDK 请求会议服务端和 SRTC 服务端时都带上 `Accept-Language`，**服务端业务错误（1000–99999）的文案随之返回中文或英文**
+ **SDK 自身的报错（`20Nxxx`，以及透传的 `10Nxxx`）固定为英文，不受 `language` 影响**

---

## 统一码表（会议层低 3 位）

**一种语义只有一个码**，各端遇到同一场景用同一个码。不是每个端都会用到全部的码，某端实际会产生哪些码见该端的错误码页。

| 低位 | 名称 | 含义 |
| :---: | --- | --- |
| 000 | Unknown | 未分类错误（兜底，正常不应出现） |
| 001 | NotLoggedIn | 未登录 / SDK 未初始化 |
| 002 | TokenExpired | Token 已过期 |
| 003 | NotInMeeting | 不在会议中 / 会话未激活 |
| 004 | Unauthorized | 无权限：非主持人执行主持人操作，或房间已禁止打开摄像头 / 麦克风 / 共享 |
| 005 | TokenInvalid | Token 格式无效、无法解析 |
| 006 | AlreadyInMeeting | 已在会议中，需先退出 |
| 007 | NetworkError | 网络错误：请求失败或 HTTP 非 200（HTTP 状态见错误详情） |
| 008 | DeviceError | 设备错误（新版本的设备错误透传 SRTC 层的码，本码仅保留） |
| 009 | InternalError | SDK 内部错误 |
| 010 | UserNotFound | 会议中没有该成员 |
| 011 | InvalidState | 当前状态不允许：已开启 / 尚未开启、SDK 未就绪、实例已销毁 |
| 012 | InvalidArgument | 参数非法 |
| 013 | HostNotSet | 主持人异常或未设置 |
| 103 | EnterMeetingCancelled | 进入会议被取消 |
| 104 | WaitingRoomContextMissing | 等候室上下文缺失 |
| 105 | AudienceOperationForbidden | 观众身份禁止该操作 |
| 106 | SessionOperationCancelled | 会话操作被取消 |
| 201 | CameraOpenFailed | 打开摄像头失败（会议层编排失败；底层采集错误透传 SRTC 的码） |
| 202 | MicOpenFailed | 打开麦克风失败（同上） |
| 203 | ScreenPermissionDenied | 屏幕共享权限被拒 |
| 204 | ScreenTrackUnavailable | 屏幕共享轨道不可用 |
| 205 | WhiteboardRequestCancelled | 白板请求被取消 |
| 206 | WhiteboardUrlMissing | 白板地址缺失 |
| 207 | CloudRecordCaptureDisabled | 云录制已禁用采集 |
| 208 | LocalTrackUnavailable | 本地轨道不可用 |
| 209 | RemoteTrackUnavailable | 远端轨道不可用（成员在会议中，但没有该轨道） |
| 210 | LocalDeviceOperationCancelled | 本地设备操作被取消 |
| 211 | LocalDeviceCapabilityUnsupported | 本地设备能力不支持 |
| 212 | LocalDeviceOperationInProgress | 本地设备操作进行中 |
| 301 | ImEnableCancelled | 启用 IM 被取消 |
| 302 | ImTokenMissing | IM Token 缺失 |
| 351 | HttpClientNotInitialized | HTTP 客户端未初始化 |
| 353 | RequestTimeout | 请求超时 |
| 354 | RequestCancelled | 请求被取消 |
| 355 | EmptyResponseBody | 响应体为空 |
| 356 | ResponseParseFailed | 响应解析失败：不是 JSON 或缺 `code` 字段 |

---

## 各端按新码发版的进度

本表是 2026-09-30 定稿的第 2 版，**各端以自己按新码发版的版本为准**。尚未发版的端，仍以该端错误码页列出的码为准。

| 端 | 前缀 | 按本表发版的版本 |
| --- | --- | --- |
| Web | `206` | `@seastart/smeeting-web-sdk` 0.3.0 起 |
| 微信小程序 | `207` | `@seastart/smeeting-wx-sdk` 0.1.0 起 |
| Swift（iOS / macOS） | `203` / `205` | 以 Swift SDK [更新日志](/zh/meeting/swift/changelog) 为准 |
| Android、iOS（Objective-C）、鸿蒙、Windows | `202`、`203`、`208`、`201` | **尚未按新码发版**，以各端发版为准，目前仍按该端错误码页 |

---

## 旧码 → 新码对照

| 端 | 主要变化 | 详细对照 |
| --- | --- | --- |
| Web / 微信小程序 | 以前除 `206001`–`206004`（`207001`–`207004`）外都落在兜底码 `206000` / `207000`，现在按场景拆成独立码；请求会议服务端的网络 / HTTP 失败改为 `206007` / `207007`，响应无法解析改为 `206356` / `207356`；采集与权限失败透传 SRTC 层的 `106231` 等。`001`–`004` 含义不变 | [Web 更新日志](/zh/meeting/web/changelog) · [Web 错误码](/zh/meeting/web/error-codes) |
| Swift | 见其更新日志中的对照表 | [Swift 更新日志](/zh/meeting/swift/changelog) |

其它端（Android、iOS Objective-C、鸿蒙、Windows）的旧码对照，随该端按新码发版时在其更新日志中给出。透传的 SRTC 层旧码（如 `100xxx` 通用码）见 [SRTC 旧码 → 新码对照](/zh/rtc/error-codes)。

---

## 各平台完整错误码表

[Web](/zh/meeting/web/error-codes) · [Android](/zh/meeting/android/error-codes) · [Windows](/zh/meeting/windows/error-codes) · [Swift](/zh/meeting/swift/error-codes) · [iOS](/zh/meeting/ios/error-codes) · [鸿蒙](/zh/meeting/harmony/error-codes)
