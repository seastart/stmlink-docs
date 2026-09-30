---
title: "错误码"
description: "微信小程序 SRTC SDK（0.3.0 起）的错误码：SdkError 的 code / baseCode 怎么判断、language 参数如何影响服务端报错语言，以及 107xxx 客户端错误码的含义、常见原因与建议给用户的提示。"
---

<Warning>
**0.3.0 起错误码全面重排，报错文案改为英文**（破坏性变更）。本页按 0.3.0 及以后的版本列出；旧版以前大多落在 `107000`，与新码的对照见 [更新日志 · v0.3.0](/zh/rtc/wechat-miniprogram/changelog)。
</Warning>

### 怎么判断错误

SDK 抛出的错误是 `SdkError`（继承自 `Error`，包里导出了 `SdkError` 与 `ErrorCode`）：

| 字段 | 说明 |
| --- | --- |
| `code` | 完整错误码。SDK 自身的错误为 `107` + 3 位低位码（如 `107006`）；`1000`–`99999` 是服务端返回的业务错误码，原样透传 |
| `baseCode` | 低 3 位语义码，对照 `ErrorCode` 枚举，各端 SDK 同义；服务端错误码返回自身 |
| `message` / `msg` | 错误详情（两者相同，`msg` 为兼容旧版保留）。SDK 自身的报错固定为英文，服务端错误的文案语言跟随 `language` |

**请按 `code` / `baseCode` 判断，不要按文案判断** —— 文案只给开发者和日志看，会随版本调整。需要给终端用户看的提示，按下表「建议给用户的提示」自行映射，不要直接展示 `message`。

```typescript
import { SRTC, SdkError, ErrorCode } from '@seastart/srtc-wx-sdk';

try {
  await channel.publishLocalTrack(track);
} catch (e) {
  if (e instanceof SdkError && e.baseCode === ErrorCode.ConnectionFailed) { // 107006
    wx.showToast({ title: '网络异常，请检查网络后重试', icon: 'none' });
  } else {
    console.error(e.code, e.message);
  }
}
```

### language 参数

初始化参数 `language` 设置 SDK 语言（语言标签，如 `zh-CN`、`en`），是进程级全局配置：

```typescript
const srtc = new SRTC({
  language: 'en',   // 不传则跟随 wx.getAppBaseInfo().language，取不到时为 zh
});
```

+ SDK 请求服务端时带上 `Accept-Language`，**服务端业务错误（`1000`–`99999`）的 `message` 随之返回中文或英文**
+ **SDK 自身的报错（`107xxx`）固定为英文，不受 `language` 影响**

---

### 客户端错误码

低 3 位的跨端含义见 [错误码规则与总表](/zh/rtc/error-codes)。「建议给用户的提示」只填需要让终端用户知道的码，其余多为接入代码的问题，按「常见原因」排查即可。

| 错误码 | `ErrorCode` | 含义 | 常见原因 | 建议给用户的提示 |
| --- | --- | --- | --- | --- |
| `107000` | `Unknown` | 未分类错误 | 兜底码，正常不应出现，看 `message` 与日志 | —— |
| `107001` | `NotInChannel` | 不在频道内 | 未加入频道，或已离开频道后又调用发布、订阅、`changePusherOptions` 开麦 / 开摄像头 | —— |
| `107002` | `TokenExpired` | Token 已过期 | 加入频道或启用 IM 时 Token 已超过有效期，重新签发 | —— |
| `107003` | `TrackNotFound` | 流轨道不存在 | 按 uid + id / desc 找不到远端轨道：对方未发布或已取消发布 | —— |
| `107005` | `AlreadyJoined` | 已加入 | 重复启用 IM | —— |
| `107006` | `ConnectionFailed` | 连接失败 | `wx.request` 失败或 HTTP 非 200（状态见 `message`）；检查服务域名是否已加入小程序的 request 合法域名 | 网络异常，请检查网络后重试 |
| `107009` | `SignalingConnectFailed` | 信令连接失败 | 信令服务不可达；检查 socket 合法域名 | 网络异常，请检查网络后重试 |
| `107010` | `SignalingSubscribeFailed` | 信令订阅失败 | 同上 | 网络异常，请检查网络后重试 |
| `107011` | `MessageDecodeFailed` | 响应解析失败 | 接口返回的内容不是 JSON 或缺 `code` 字段，多为服务地址指向了错误的服务，或中间有代理改写 | —— |
| `107020` | `MaxPublishLimitReached` | 超过发布上限 | 已发布的音频 / 视频轨道数达到上限 | —— |
| `107024` | `InvalidState` | 当前状态不允许该操作 | 调用顺序不对，如实例已销毁、本地用户信息尚未就绪 | —— |
| `107025` | `InternalError` | SDK 内部错误 | 请带上日志联系我们 | —— |
| `107031` | `InvalidArgument` | 参数非法 | 必填参数为空、参数类型不符 | —— |
| `107034` | `MaxSubscribeLimitReached` | 超过订阅上限 | 已订阅的音频 / 视频轨道数达到上限 | —— |
| `107035` | `PublishDescConflict` | 发布描述冲突 | 同一个 `desc` 已被其它轨道占用，换一个 `desc` 或先取消发布 | —— |
| `107037` | `PlayViewNotFound` | 播放节点不存在 | `freshPlayerStyle` 查询不到节点，页面渲染完成后再调用 | —— |
| `107204` | `UserNotFound` | 频道内没有该用户 | 订阅 / 查询的 uid 不在频道内 | —— |

<Note>
推流 / 拉流过程中的失败通过 `UP_PUSH_FAIL` / `DOWN_PLAY_FAIL` 事件通知，事件里带的是微信 `live-pusher` / `live-player` 的原生错误码（如 5000、5001），不是上表的码，含义见微信官方文档。
</Note>

---

### 服务端错误码

`1000`–`99999` 的码来自服务端，SDK 原样透传；给用户看时**直接展示服务端返回的 `message`**（语言跟随 `language`）。常见的有：

| 错误码 | 说明 |
| :---: | --- |
| `1011` | 应用无效 |
| `1021` | 加入频道的 Token 已被使用 |
| `1022` | 该会话不在频道中 |
| `1023` | 成员不在频道中 |
| `1024` | 频道未开启 |
| `1025` | 频道已开启 |

完整清单见 [服务端 API · 错误码](/zh/rtc/server-api/error-codes)。
