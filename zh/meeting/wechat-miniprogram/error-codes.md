---
title: "错误码"
description: "微信小程序 SMeeting SDK（0.1.0 起）的错误码：怎么按 code 区分会议层 207xxx、透传的 SRTC 层 107xxx 与服务端业务码，language 参数如何影响服务端报错语言，以及各码的含义、常见原因与建议给用户的提示。"
---

<Warning>
**0.1.0 起错误码重排，报错文案改为英文**（破坏性变更）。本页按 0.1.0 及以后的版本列出，升级说明见 [更新日志 · v0.1.0](/zh/meeting/wechat-miniprogram/changelog)。
</Warning>

### 怎么判断错误

会议 SDK 抛出的错误可能来自三处，**按完整的 `code` 区分**：

| `code` | 来源 | 说明 |
| --- | --- | --- |
| `207xxx` | 会议层 SDK | 见下方「会议层错误码」 |
| `107xxx` | 底层 SRTC SDK，原样透传 | 推拉流、信令、网络等，见 [小程序 SRTC 错误码](/zh/rtc/wechat-miniprogram/error-codes) |
| `1000`–`99999` | 服务端业务错误，原样透传 | 会议服务端见 [服务端 API 错误码](/zh/meeting/server-api/error-codes)；给用户看时直接展示服务端返回的 `message` |

错误对象的字段与 SRTC 的 `SdkError` 相同：`code`（完整码）、`baseCode`（低 3 位）、`message` / `msg`（英文详情）。包里导出了 `SdkError` 与 `MeetingErrorCode`（会议层低 3 位）。

+ **请按 `code` 判断，不要按文案判断** —— 文案只给开发者和日志看，会随版本调整。需要给终端用户看的提示，按下表「建议给用户的提示」自行映射，不要直接展示 `message`
+ **会议层和 SRTC 层的低 3 位是两套独立的表**（`207003` 是不在会议中，`107003` 是流轨道不存在），在会议 SDK 里请比较完整的 `code`，只比 `baseCode` 会混淆

```typescript
try {
  const pusherOptions = await smeeting.requestOpenCamera();
} catch (e: any) {
  if (e?.code === 207004) {
    wx.showToast({ title: '主持人已禁止打开摄像头', icon: 'none' });
  } else if (e?.code >= 1000 && e?.code < 100000) {
    wx.showToast({ title: e.message, icon: 'none' }); // 服务端业务错误，文案语言跟随 language
  } else {
    console.error(e?.code, e?.message);
  }
}
```

### language 参数

初始化参数 `language` 设置 SDK 语言（语言标签，如 `zh-CN`、`en`），是进程级全局配置，**会同时设置底层 SRTC**：

```typescript
const smeeting = new SMeeting({
  language: 'en',   // 不传则跟随 wx.getAppBaseInfo().language，取不到时为 zh
});
```

+ 请求会议服务端和 SRTC 服务端时都带上 `Accept-Language`，**服务端业务错误（`1000`–`99999`）的 `message` 随之返回中文或英文**
+ **SDK 自身的报错（`207xxx`，以及透传的 `107xxx`）固定为英文，不受 `language` 影响**

---

### 会议层错误码

低 3 位的跨端含义见 [错误码规则与总表](/zh/meeting/error-codes)。

| 错误码 | `MeetingErrorCode` | 含义 | 常见原因 | 建议给用户的提示 |
| --- | --- | --- | --- | --- |
| `207000` | `Unknown` | 未分类错误 | 兜底码，正常不应出现，看 `message` 与日志 | —— |
| `207001` | `NotLoggedIn` | 未登录 | 没调 `login`，或登录失败后调用了需要登录的方法 | —— |
| `207002` | `TokenExpired` | Token 已过期 | `login` 时 Token 已超过有效期，重新签发 | 登录已过期，请重新进入 |
| `207003` | `NotInMeeting` | 不在会议中 | 没进入会议，或已退出后调用会中方法 | —— |
| `207004` | `Unauthorized` | 无权限 | 非主持人执行主持人操作；或房间已禁止打开摄像头 / 麦克风 | 主持人已禁止该操作 |
| `207005` | `TokenInvalid` | Token 无效 | `login` 的 Token 无法解析，检查是否完整拷贝、是否为本环境签发 | —— |
| `207006` | `AlreadyInMeeting` | 已在会议中 | 重复进入会议，需先退出当前会议 | —— |
| `207007` | `NetworkError` | 网络错误 | 请求会议服务端失败或 HTTP 非 200（状态见 `message`）；检查服务域名是否已加入小程序的 request 合法域名 | 网络异常，请检查网络后重试 |
| `207010` | `UserNotFound` | 会议中没有该成员 | 按 uid 查询的用户不在房间内 | —— |
| `207011` | `InvalidState` | 当前状态不允许 | 摄像头 / 麦克风已开启时重复开启 | —— |
| `207012` | `InvalidArgument` | 参数非法 | 预留，本版暂未使用 | —— |
| `207356` | `ResponseParseFailed` | 响应解析失败 | 会议服务端的响应不是 JSON 或缺 `code` 字段，多为服务地址配置错误，或中间有代理改写 | —— |

透传的 SRTC 层错误码（`107xxx`）见 [小程序 SRTC 错误码](/zh/rtc/wechat-miniprogram/error-codes)，其中 `107006`、`107009`、`107010` 可提示用户「网络异常，请检查网络后重试」。
