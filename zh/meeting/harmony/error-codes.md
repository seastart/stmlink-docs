---
title: "错误码"
description: "SMeeting HarmonyOS SDK 的错误类型 SMeetingError、数字错误码表与处理建议"
---

会议 SDK 抛出的错误是 `SMeetingError`，继承 `Error`，额外带这些字段：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `kind` | `SMeetingErrorKind` | 错误种类，用来分支处理 |
| `code` | `number` | 完整数字错误码（含平台前缀） |
| `baseCode` | `number`（只读） | 低 3 位语义码，跨端统一（如 `208010` → `10`）；后端业务码返回自身。1.1.0 起 |
| `detail` | `string` | 纯文本描述，**不含**错误码；1.1.0 起一律英文 |
| `httpStatus` | `number \| undefined` | HTTP 非 200 时的状态码（此时 `code` 为 `208007`），其它情况为 `undefined`。1.1.0 起 |

`toString()` 输出 `"{code}: {detail}"`。

<Note>
自 **1.1.0** 起错误码按 SMeeting [统一错误码表](/zh/meeting/error-codes)调整（`208` + 统一码表低 3 位，与 Swift 等端同号），报错文案改为英文。
1.0.0 的旧码与新码的对照见[更新日志](/zh/meeting/harmony/changelog)。

`detail` 是给开发者和日志看的，**给终端用户的提示请按 `code` / `baseCode` 自行映射**，不要直接展示 `detail`。
</Note>

---

### 错误码是怎么拼出来的

+ **SDK 内部错误**：低 3 位语义码加平台前缀拼成 6 位数。
  HarmonyOS 的**会议**前缀是 **`208`**，所以内部错误码形如 `208001`、`208011`、`208356`。
+ **业务后端透传的错误码**：≥ 1000 时**原样保留**，文案语言随 `SMeetingEngine.setLanguage` 返回中文或英文。
+ **HTTP 状态码不会拼进错误码**（1.1.0 起）：HTTP 非 200 一律为 `208007`，状态在 `httpStatus`；
  后端返回 < 1000 的异常码（如 `-1`）也报 `208007`。1.0.0 会出 `208404`、`208200`、`207999` 这类码。

<Note>
注意会议与 RTC 用**两套前缀**：RTC 是 `108`、会议是 `208`
（各端都是这个规则，首位 `1` 表示 RTC、`2` 表示会议业务）。
所以看到 `208xxx` 就知道是会议层的错，`108xxx` 是底层 RTC 的错。

调用会议接口时**两种都可能收到** —— 会议层的操作最终会落到 RTC 层。
</Note>

---

### 错误清单

| `kind` | `code` | 描述（`detail`） | 说明 | 建议处理 |
| --- | --- | --- | --- | --- |
| `notLoggedIn` | `208001` | `Not logged in to the meeting SDK` | 未登录 | 先调 `login(token)` |
| `tokenExpired` | `208002` | `Token has expired` | Token 已过期 | 重新向业务后端获取 |
| `notInMeeting` | `208003` | `Not in a meeting` | 当前不在会议中 | 检查调用时机，先 `enterRoom` |
| `unauthorized` | `208004` | `You don't have permission for this operation` | 权限不足 | 会控接口需要主持人 / 联席主持人身份 |
| `tokenInvalid` | `208005` | `Invalid token format` | Token 不合法 | 检查签发逻辑 |
| `alreadyInMeeting` | `208006` | `Already in a meeting; exit first` | 已在会议中 | 避免重复入会，或先 `exitRoom` |
| `networkError` | `208007` | `Network error: <detail>` | 连不上等传输层失败；HTTP 非 200（`httpStatus` 有值，1.1.0 起）；后端返回 < 1000 的异常码（1.1.0 起） | 提示重试并检查连通性，记录 `httpStatus` |
| `deviceError` | `208008` | `Device error: <detail>` | 设备错误（保留；采集 / 权限失败以 `SRTCError` 透传） | 检查摄像头 / 麦克风权限与占用 |
| `internalError` | `208009` | `Internal error: <detail>` | SDK 内部错误 | 结合日志排查 |
| `userNotFound` | `208010` | `User not found in the meeting: <uid>` | 会议中没有该成员（1.1.0 起，原为 `208009`） | 以最新的成员列表为准 |
| `invalidState` | `208011` | `Invalid state: <detail>` | 当前状态不允许，如 `switchCamera` 时尚未开启摄像头、屏幕共享已开启（1.1.0 起，原为 `208008` / `208009`） | 检查调用顺序 |
| `invalidArgument` | `208012` | `Invalid argument: <detail>` | 参数非法（1.1.0 起） | 检查传参 |
| `remoteTrackUnavailable` | `208209` | `Remote track not found: uid=<uid> desc=<desc>` | 成员在、但这路轨道不存在（1.1.0 起，原为 `208009`） | 对方未开启或已关闭，等轨道事件后再订阅 |
| `requestTimeout` | `208353` | `Request timeout: <detail>` | 会议请求超时（1.1.0 起，原并入 `208007`） | 提示网络较慢并重试 |
| `responseParseFailed` | `208356` | `Response parse failed: <detail>` | 响应不是 JSON、缺 `code` 字段或缺必需字段（1.1.0 起，原为 `208200` / `207999`） | 检查服务端与 SDK 版本 |
| `apiError` | 后端码 | 后端返回的文案 | 业务后端返回错误 | 按后端码排查，文案语言随 `setLanguage` |

<Note>
`unauthorized`（`208004`）是会控接口最常见的错误。所有 `admin*` 方法都要求
主持人或联席主持人身份 —— UI 上应该按 `Role` 提前隐藏 / 禁用按钮，
而不是等调用失败再提示。
</Note>

---

### 推荐的处理方式

```typescript
import { SMeetingError, SMeetingErrorKind, SRTCError } from 'smeeting';

try {
  await meeting.enterRoom({ nickname: '张三', roomNo: '123456' });
} catch (e) {
  if (e instanceof SRTCError) {
    // RTC 层原样透传的错误（108xxx），如 108231 无摄像头权限、108251 无麦克风权限
    console.error(`SRTC error ${e.code}: ${e.detail}`);
    return;
  }
  const err = e as SMeetingError;
  if (err.kind !== undefined) {
    switch (err.kind) {
      case SMeetingErrorKind.tokenExpired:
      case SMeetingErrorKind.tokenInvalid:
        // 重新登录
        break;
      case SMeetingErrorKind.alreadyInMeeting:
        // 已在会中，可以直接跳到会议页
        break;
      case SMeetingErrorKind.unauthorized:
        console.warn('权限不足');
        break;
      case SMeetingErrorKind.networkError:
        // HTTP 非 200 时 httpStatus 有值
        console.warn(`网络错误 ${err.code} http=${err.httpStatus}`);
        break;
      default:
        console.error(`SMeeting error ${err.code}: ${err.detail}`);
    }
  } else {
    console.error(`未知错误: ${String(e)}`);
  }
}
```

<Warning>
**`JSON.stringify(new Error())` 的结果是 `{}`。**

ArkTS 里直接把错误对象序列化进日志会得到空对象。排障时请显式取 `code` / `detail`。
</Warning>

---

### 入会失败还有一条独立通路

`enterRoom()` 抛错只覆盖"请求阶段就失败"。**入会请求成功、但后续被服务端拒绝**
（比如会议已锁定、被移入等候室）走的是事件：

```typescript
onRoomJoinFailed: (meeting, data) => {
  // data.uid / data.name / data.errDesc / data.failedType
  console.error(`入会失败(${data.failedType}): ${data.errDesc}`);
}
```

所以入会的错误处理要**同时**写 `try/catch` 和 `onRoomJoinFailed`，只写一边会漏。

---

### 底层 RTC 错误

会议 SDK 内部用的是 SRTC，所以媒体相关的失败可能抛出 `SRTCError`（`108xxx`）。
采集 / 权限错误**原样透传**、不由会议层重新包装，常见的有 `cameraPermissionDenied`（`108231`）、
`micPermissionDenied`（`108251`）、`screenShareDenied`（`108039`）、`deviceNotFound`（`108021`）、
`captureError`（`108018`），以及 `codecNotSupported`、`transportNotReady`。

1.1.0 起 `smeeting` 直接转出 `SRTCError` / `SRTCErrorKind`，只依赖 `smeeting` 的业务代码也能 `instanceof SRTCError`。

完整清单见 [SRTC 错误码](/zh/rtc/harmony/error-codes)。

<Warning>
**H264 不支持时不报错，而是静默退回 VP8。**

`@ohos/webrtc` 的 H264 / H265 纯硬编、没有软编兜底。设备不支持时 SDK 会退回默认编码，
**不抛异常** —— 表现是本机有画面但与其它端互通不上。

自测要核对实际协商到的编码，别以"看到画面"为准。方法见
[SRTC 的通话质量](/zh/rtc/harmony/advanced/call-quality)。
</Warning>

---

### 相关阅读

+ [事件参考](/zh/meeting/harmony/events)
+ [类型定义](/zh/meeting/harmony/types)
+ [SRTC 错误码](/zh/rtc/harmony/error-codes)
