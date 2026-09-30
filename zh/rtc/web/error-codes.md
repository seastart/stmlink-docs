---
title: "错误码"
description: "Web SRTC SDK（0.7.0 起）的错误码：SdkError 的 code / baseCode 怎么判断、language 参数如何影响服务端报错语言，以及 106xxx 客户端错误码的含义、常见原因与建议给用户的提示。处理入会、采集、发布订阅失败时读。"
---

<Warning>
**0.7.0 起错误码全面重排，报错文案改为英文**（破坏性变更）。本页按 0.7.0 及以后的版本列出；旧版以前大多落在 `106000`，与新码的对照见 [更新日志 · v0.7.0](/zh/rtc/web/changelog)。
</Warning>

### 怎么判断错误

SDK 抛出的错误是 `SdkError`（继承自 `Error`，包里导出了 `SdkError` 与 `ErrorCode`）：

| 字段 | 说明 |
| --- | --- |
| `code` | 完整错误码。SDK 自身的错误为 `106` + 3 位低位码（如 `106231`）；`1000`–`99999` 是服务端返回的业务错误码，原样透传 |
| `baseCode` | 低 3 位语义码，对照 `ErrorCode` 枚举，各端 SDK 同义；服务端错误码返回自身 |
| `message` / `msg` | 错误详情（两者相同，`msg` 为兼容旧版保留）。SDK 自身的报错固定为英文，服务端错误的文案语言跟随 `language` |
| `name` / `cause` | 采集失败时 `name` 保留浏览器原值（如 `NotAllowedError`），原始异常在 `cause` |

**请按 `code` / `baseCode` 判断，不要按文案判断** —— 文案只给开发者和日志看，会随版本调整。需要给终端用户看的提示，按下表「建议给用户的提示」自行映射，不要直接展示 `message`。

```typescript
import { SRTC, SdkError, ErrorCode } from '@seastart/srtc-web-sdk';

try {
  await camera.startCapture();
} catch (e) {
  if (e instanceof SdkError) {
    switch (e.baseCode) {
      case ErrorCode.CameraPermissionDenied: // 106231
        showToast('请允许浏览器使用摄像头');
        break;
      case ErrorCode.CaptureFailed:          // 106018
        showToast('设备可能被其它程序占用，请关闭后重试');
        break;
      default:
        console.error(e.code, e.message);
    }
  }
}
```

### language 参数

初始化参数 `language` 设置 SDK 语言（语言标签，如 `zh-CN`、`en`），是进程级全局配置：

```typescript
const srtc = new SRTC({
  language: 'en',   // 不传则跟随 navigator.language，取不到时为 zh
});
```

+ SDK 请求服务端时带上 `Accept-Language`，**服务端业务错误（`1000`–`99999`）的 `message` 随之返回中文或英文**
+ 浏览器阻止自动播放时弹出的提示框按 `language` 显示中文或英文，可用初始化参数 `autoPlayDialogText` 覆盖文案
+ **SDK 自身的报错（`106xxx`）固定为英文，不受 `language` 影响**

---

### 客户端错误码

低 3 位的跨端含义见 [错误码规则与总表](/zh/rtc/error-codes)。「建议给用户的提示」只填需要让终端用户知道的码，其余多为接入代码的问题，按「常见原因」排查即可。

| 错误码 | `ErrorCode` | 含义 | 常见原因 | 建议给用户的提示 |
| --- | --- | --- | --- | --- |
| `106000` | `Unknown` | 未分类错误 | 兜底码，正常不应出现，看 `message` 与日志 | —— |
| `106001` | `NotInChannel` | 不在频道内 | 未加入频道，或已离开频道后又调用发布 / 订阅等频道接口 | —— |
| `106002` | `TokenExpired` | Token 已过期 | 加入频道或启用 IM 时 Token 已超过有效期，重新签发 | —— |
| `106003` | `TrackNotFound` | 流轨道不存在 | 按 uid + id / desc 找不到远端轨道：对方未发布或已取消发布 | —— |
| `106005` | `AlreadyJoined` | 已加入 | 重复启用 IM、重复加入白板 | —— |
| `106006` | `ConnectionFailed` | 连接失败 | 网络请求失败或 HTTP 非 200（状态见 `message`），或 SFU 接口多次重试仍失败 | 网络异常，请检查网络后重试 |
| `106007` | `ConnectionTimeout` | 连接超时 | 加入频道时媒体连接迟迟建不起来，检查 UDP 是否放通 | 网络异常，请检查网络后重试 |
| `106009` | `SignalingConnectFailed` | 信令连接失败 | 信令服务不可达，检查网络与防火墙 | 网络异常，请检查网络后重试 |
| `106010` | `SignalingSubscribeFailed` | 信令订阅失败 | 同上 | 网络异常，请检查网络后重试 |
| `106011` | `MessageDecodeFailed` | 响应解析失败 | 接口返回的内容不是 JSON 或缺 `code` 字段，多为服务地址指向了错误的服务，或中间有代理改写 | —— |
| `106013` | `SdpNegotiationFailed` | SDP 协商失败 | CDN 流媒体引擎的 SDP 交换接口返回错误 | —— |
| `106014` | `TransportNotReady` | 传输未就绪 | 频道或流媒体引擎正在重连、发布 / 订阅的媒体连接尚未连上，**稍后重试**即可 | 网络异常，请检查网络后重试 |
| `106015` | `PeerConnectionFailed` | 媒体连接失败 | 发布 / 订阅的 PeerConnection 进入 failed / closed，检查网络与 UDP 端口 | 网络异常，请检查网络后重试 |
| `106018` | `CaptureFailed` | 采集失败 | 设备被其它程序占用、硬件错误（浏览器 `NotReadableError` / `AbortError`） | 设备可能被其它程序占用，请关闭后重试 |
| `106019` | `CodecNotSupported` | 编解码器不支持 | 当前浏览器缺 OPUS / H264 | 当前浏览器不支持该功能，请使用最新版 Chrome / Edge |
| `106020` | `MaxPublishLimitReached` | 超过发布上限 | 已发布的音频 / 视频轨道数达到流媒体引擎的上限 | —— |
| `106021` | `DeviceNotFound` | 设备不存在 | 找不到摄像头 / 麦克风，或指定的 `deviceId` 已拔出（浏览器 `NotFoundError` / `OverconstrainedError`） | 未检测到摄像头或麦克风，请检查设备连接 |
| `106022` | `EngineNotSupported` | 流媒体引擎不支持 | 服务端下发了当前 SDK 版本不认识的流媒体引擎，升级 SDK | —— |
| `106024` | `InvalidState` | 当前状态不允许该操作 | 调用顺序不对，如实例已销毁、本地用户信息尚未就绪 | —— |
| `106025` | `InternalError` | SDK 内部错误 | 如处理器插件没有产出轨道。请带上日志联系我们 | —— |
| `106026` | `Cancelled` | 操作被取消 | 调用过程中离开了频道 | —— |
| `106031` | `InvalidArgument` | 参数非法 | 必填参数为空、传入的 `MediaStreamTrack` 类型不符等 | —— |
| `106032` | `FeatureNotSupported` | 当前浏览器不支持该能力 | 屏幕共享、画中画、联播、本地录制（MediaRecorder）等 | 当前浏览器不支持该功能，请使用最新版 Chrome / Edge |
| `106033` | `TrackNotCaptured` | 轨道未采集 | 没调 `startCapture`（或已停止）就发布、播放或设置处理器 | —— |
| `106034` | `MaxSubscribeLimitReached` | 超过订阅上限 | 已订阅的音频 / 视频轨道数达到流媒体引擎的上限 | —— |
| `106035` | `PublishDescConflict` | 发布描述冲突 | 同一个 `desc`（或 CDN 流槽位）已被其它轨道占用，换一个 `desc` 或先取消发布 | —— |
| `106036` | `PlayFailed` | 播放失败 | 播放失败且不是浏览器自动播放策略导致（自动播放被拦截走 `track_autoplay_fail` 事件） | 播放失败，请刷新页面重试 |
| `106037` | `PlayViewNotFound` | 播放容器不存在 | 画中画 / 弹出窗口传入了没有 `addPlayView` 过的容器 | —— |
| `106038` | `PopupBlocked` | 弹窗被拦截 | 弹出窗口播放时 `window.open` 被浏览器拦截 | 弹窗被拦截，请允许本站弹出窗口 |
| `106039` | `ScreenShareDenied` | 屏幕共享被拒绝 | 用户在选择窗口里取消，或系统未授权浏览器录屏 | 已取消屏幕共享；若没有弹出选择窗口，请在系统设置中允许浏览器录屏 |
| `106204` | `UserNotFound` | 频道内没有该用户 | 订阅 / 查询的 uid 不在频道内 | —— |
| `106231` | `CameraPermissionDenied` | 无摄像头权限 | 用户或系统拒绝了摄像头授权（浏览器 `NotAllowedError` / `SecurityError`） | 请允许浏览器使用摄像头 |
| `106251` | `MicPermissionDenied` | 无麦克风权限 | 用户或系统拒绝了麦克风授权 | 请允许浏览器使用麦克风 |
| `106300` | `PublishFailed` | 发布失败 | 流媒体引擎未连接或已断开（不在重连中）时发布 | 网络异常，请检查网络后重试 |
| `106301` | `SubscribeFailed` | 订阅失败 | 流媒体引擎未连接或已断开（不在重连中）时订阅 | 网络异常，请检查网络后重试 |
| `106302` | `PublishTimeout` | 发布协商超时 | CDN 流媒体引擎发布超时，网络不通或服务端不可达 | 网络异常，请检查网络后重试 |
| `106303` | `SubscribeTimeout` | 订阅协商超时 | 同上（订阅） | 网络异常，请检查网络后重试 |

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
