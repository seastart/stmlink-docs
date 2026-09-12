---
title: "错误码"
description: "SMeeting HarmonyOS SDK 的错误类型 SMeetingError、数字错误码表与处理建议"
---

会议 SDK 抛出的错误是 `SMeetingError`，继承 `Error`，额外带三个字段：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `kind` | `SMeetingErrorKind` | 错误种类，用来分支处理 |
| `code` | `number` | 完整数字错误码（含平台前缀） |
| `detail` | `string` | 纯文本描述，**不含**错误码 |

`toString()` 输出 `"{code}: {detail}"`。

---

### 错误码是怎么拼出来的

+ **SDK 内部错误**：原始码 < 1000，加平台前缀拼成 6 位数。
  HarmonyOS 的**会议**前缀是 **`208`**，所以内部错误码形如 `208001` ~ `208009`。
+ **业务后端透传的错误码**：≥ 1000 时**原样保留**。

<Note>
注意会议与 RTC 用**两套前缀**：RTC 是 `108`、会议是 `208`
（各端都是这个规则，首位 `1` 表示 RTC、`2` 表示会议业务）。
所以看到 `208xxx` 就知道是会议层的错，`108xxx` 是底层 RTC 的错。

调用会议接口时**两种都可能收到** —— 会议层的操作最终会落到 RTC 层。
</Note>

---

### 错误清单

| `kind` | `code` | 构造参数 | 说明 | 建议处理 |
| --- | --- | --- | --- | --- |
| `notLoggedIn` | `208001` | — | 未登录 | 先调 `login(token)` |
| `tokenExpired` | `208002` | — | Token 已过期 | 重新向业务后端获取 |
| `notInMeeting` | `208003` | — | 当前不在会议中 | 检查调用时机，先 `enterRoom` |
| `unauthorized` | `208004` | — | 权限不足 | 会控接口需要主持人 / 联席主持人身份 |
| `tokenInvalid` | `208005` | — | Token 不合法 | 检查签发逻辑 |
| `alreadyInMeeting` | `208006` | — | 已在会议中 | 避免重复入会，或先 `exitRoom` |
| `networkError` | `208007` | `msg` | 网络错误 | 提示重试并检查连通性 |
| `deviceError` | `208008` | `msg` | 设备错误 | 检查摄像头 / 麦克风权限与占用 |
| `internalError` | `208009` | `msg` | SDK 内部错误 | 结合日志排查 |
| `apiError` | 后端码 | `code`, `message` | 业务后端返回错误 | 按后端码排查 |

<Note>
`unauthorized`（`208004`）是会控接口最常见的错误。所有 `admin*` 方法都要求
主持人或联席主持人身份 —— UI 上应该按 `Role` 提前隐藏 / 禁用按钮，
而不是等调用失败再提示。
</Note>

---

### 推荐的处理方式

```typescript
import { SMeetingError, SMeetingErrorKind } from 'smeeting';

try {
  await meeting.enterRoom({ nickname: '张三', roomNo: '123456' });
} catch (e) {
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
常见的有 `captureError`（采集失败）、`codecNotSupported`、`transportNotReady`。

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
