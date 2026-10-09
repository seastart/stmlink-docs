---
title: "错误码"
description: "SRTC HarmonyOS SDK 的错误类型 SRTCError、数字错误码表与处理建议"
---

SDK 抛出的错误统一是 `SRTCError`，它继承 `Error`，并额外带以下字段：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `kind` | `SRTCErrorKind` | 错误种类，用来分支处理 |
| `code` | `number` | 完整数字错误码（SDK 错误含平台前缀 `108`；后端业务码原样），用于日志与跨端对齐 |
| `detail` | `string` | 纯文本描述，**不含**错误码，自 1.1.0 起**一律英文** |
| `baseCode` | `number`（只读） | 低 3 位语义码，跨端统一（如 `108231` → `231`）；后端业务码返回自身。1.1.0 起 |
| `httpStatus` | `number \| undefined` | 请求失败时的 HTTP 状态：非 200 时为实际状态，连不上 / 超时为 `0`。只有 `kind = apiRequestFailed` 且码为 `108006` 时有值。1.1.0 起 |
| `systemCode` | `number \| undefined` | 被包装的系统 `BusinessError.code`（如 `201`），采集 / 权限失败时有值。1.1.0 起 |
| `cause` | `Object \| undefined` | 原始异常：采集失败时是系统抛出的 `BusinessError` / `Error`，SDP 协商失败时是底层 `Error`。1.1.0 起 |

`toString()` 输出 `"{code}: {detail}"`，方便日志里一行同时拿到码和描述。

另有静态方法 `SRTCError.isServerError(e: Object): boolean`（1.1.0 起）：`e` 是 `SRTCError` 且码在后端业务区间 1000–99999 时返回 `true`。用它区分「后端业务错误（不必重试）」与「网络 / 解码失败（可重试）」——不要写成 `e instanceof SRTCError`，`108006` / `108011` 也是 `SRTCError`。

<Note>
自 **1.1.0** 起错误码按跨端[统一错误码表](/zh/rtc/error-codes)（第 2 版）重排：新增 `031`–`301` 若干码，网络 / HTTP 失败不再拼出 `108404` / `108500`，采集异常不再直接抛系统 `BusinessError`。1.0.1 及以前的旧码与新码对照见[更新日志](/zh/rtc/harmony/changelog)。下表「版本」列标注了各码的生效版本。
</Note>

---

### 错误码是怎么拼出来的

+ **SDK 内部错误**：原始码 < 1000，会被加上平台前缀拼成 6 位数。
  HarmonyOS 的 RTC 前缀是 **`108`**，所以内部错误码形如 `108001`、`108231`。
+ **业务后端透传的错误码**：1000–99999 **原样保留**，不再加前缀。
+ **HTTP 状态码不会拼进错误码**（1.1.0 起）：网络失败 / HTTP 非 200 一律 `108006`，HTTP 状态只在 `httpStatus` 与 `detail` 里。

这套编号与其它端一致（windows=101、android=102、iOS=103、linux=104、macOS=105、
web=106、小程序=107、HarmonyOS=108），同一类错误在各端的低 3 位相同，
跨端排障或统一做用户提示时直接比 `baseCode`。

<Note>
**`code` 与 `kind` 不是一一对应的。** HTTP API 请求失败的 `kind` 一律是 `apiRequestFailed`，`code` 按原因区分：

+ 后端返回业务错误：`code` 为后端码（≥ 1000，原样透出）
+ 网络失败 / HTTP 非 200，或后端返回了 < 1000 的异常码：`108006`（HTTP 状态见 `httpStatus`）
+ 响应不是 JSON、缺 `code` 字段或缺必需字段：`108011`

所以按 `kind` 分支时，`apiRequestFailed` 里还要再看 `code`。
</Note>

---

### 报错语言

+ `detail` **一律英文**，给开发者和日志看，会随版本调整；不要拿它做分支判断，也不要直接展示给终端用户，请按 `code` / `baseCode` 自行映射提示文案。
+ `SRTC.setLanguage(lang)`（1.1.0 起，缺省跟随系统语言）决定请求后端时的 `Accept-Language` 头，**后端业务错误（1000–99999）的文案**随之返回中文或英文；SDK 自身报错不受它影响。

```typescript
import { SRTC } from 'srtc';

SRTC.setLanguage('en');   // 进程级全局，下次请求生效；传空恢复跟随系统
```

---

### 连接相关

| `kind` | `code` | 版本 | 说明 | 建议处理 |
| --- | --- | --- | --- | --- |
| `notConnected` | `108001` | 0.0.1 | 当前未连接 / 已离开频道 | 检查调用时机，等入会成功后再操作 |
| `tokenExpired` | `108002` | 0.0.1 | Token 已过期 | 重新向业务后端获取 Token |
| `tokenInvalid` | `108004` | 0.0.1 | Token 不合法 | 检查 Token 编码与签发逻辑 |
| `alreadyJoined` | `108005` | 0.0.1 | 已经加入该频道，或重复 `enableIm` | 避免重复调用，或先离开 |
| `connectionFailed` | `108006` | 0.0.1 | 连接失败。1.1.0 起 HTTP 请求的网络失败 / 非 200 也是这个码，但 `kind` 为 `apiRequestFailed` | 记录服务端地址、网络环境、`httpStatus` 与错误详情 |
| `connectionTimeout` | `108007` | 0.0.1 | 连接超时 | 提示用户重试并检查网络连通性 |

---

### 信令相关

| `kind` | `code` | 版本 | 说明 | 建议处理 |
| --- | --- | --- | --- | --- |
| `apiRequestFailed` | 后端码 / `108006` / `108011` | 0.0.1 | HTTP API 请求失败，见上方 Note | 后端码按业务排查；`108006` 看 `httpStatus` 与网络；`108011` 检查服务端版本 |
| `signatureError` | `108008` | 0.0.1 | 签名生成失败 | 检查服务端鉴权逻辑 |
| `signalingConnectFailed` | `108009` | 0.0.1 | 信令通道连接失败 | 检查网络可达性、代理与防火墙 |
| `signalingSubscribeFailed` | `108010` | 0.0.1 | 信令通道订阅失败 | 检查 Token 是否有效、连接是否已建立 |
| `messageDecodeFailed` | `108011` | 0.0.1 | 消息解码失败（含网宿 CDN 响应不是 JSON） | 检查服务端消息格式与 SDK 版本兼容性 |

---

### WebRTC / 传输相关

| `kind` | `code` | 版本 | 说明 | 建议处理 |
| --- | --- | --- | --- | --- |
| `webrtcError` | `108012` | 0.0.1 | 底层 WebRTC 错误 | 记录日志，优先定位设备与 SDP 过程 |
| `sdpNegotiationFailed` | `108013` | 0.0.1 | SDP 协商失败；1.1.0 起底层抛的异常也包成这个码，原异常在 `cause` | 检查编解码能力与服务端协商 |
| `transportNotReady` | `108014` | 0.0.1 | 传输层尚未就绪，或频道 / 引擎正在重连 | 稍后重试，或等 `onReconnected` 后再发布 / 订阅 |
| `peerConnectionFailed` | `108015` | 0.0.1 | PeerConnection 创建失败或进入 failed / closed（发布、订阅、入会阶段都是这个码） | 检查 ICE / STUN / TURN 与网络 |

---

### 轨道与采集相关

| `kind` | `code` | 版本 | 说明 | 建议处理 |
| --- | --- | --- | --- | --- |
| `trackNotFound` | `108003` | 0.0.1 | 找不到指定轨道 | 检查 `trackId` 是否匹配 |
| `trackAlreadyPublished` | `108016` | 0.0.1 | 轨道已发布 | 避免重复发布同一对象 |
| `trackNotPublished` | `108017` | 0.0.1 | 轨道未发布 | 取消发布前先确认状态 |
| `captureError` | `108018` | 0.0.1 | 采集失败（设备被占用、硬件错误、底层抛空 `Error` 等） | 看 `systemCode` / `cause`；检查设备占用、是否已 `SRTC.init` |
| `codecNotSupported` | `108019` | 0.0.1 | 编解码器不支持 | 见下方「编解码相关的坑」 |
| `maxPublishLimitReached` | `108020` | 0.0.1 | 超过可发布轨道上限 | 控制并发发布数量 |
| `deviceNotFound` | `108021` | 0.0.1 | 找不到设备（该类设备一个都没有，或指定的 `deviceId` 不在枚举结果里） | 设备可能已拔出，重新枚举 |
| `trackNotCaptured` | `108033` | 1.1.0 | 轨道还没 `startCapture()`（或已停止）就发布 | 先开始采集再发布 |
| `screenShareDenied` | `108039` | 1.1.0 | 屏幕共享被拒（系统授权窗未通过） | 提示用户重新发起并在授权窗点同意，见下方 Warning |
| `cameraPermissionDenied` | `108231` | 1.1.0 | 无摄像头权限 | 引导用户到系统设置中开启摄像头权限 |
| `micPermissionDenied` | `108251` | 1.1.0 | 无麦克风权限 | 引导用户到系统设置中开启麦克风权限 |

<Note>
**采集失败一律是 `SRTCError`（1.1.0 起）。** 此前采集失败直接抛系统 `BusinessError` 或空 `Error`；现在统一包装，原 `BusinessError.code` 放 `systemCode`、原异常放 `cause`。以前按 `e.code === 201` 判断无权限的代码，改为判断 `kind`（`cameraPermissionDenied` / `micPermissionDenied`）。

摄像头 / 麦克风的 `108231` / `108251` 主要来自采集前的**只读权限预检**：SDK 不申请权限、不弹授权框，权限由宿主申请，见[集成方式](/zh/rtc/harmony/integration)。
</Note>

<Warning>
**`108039` 目前只覆盖系统码 `201`。** 用户在屏幕共享授权窗点「取消」时，系统实际抛出的码尚待确认，可能落到 `108018`。需要区分「用户取消」时请结合 `systemCode` 判断。
</Warning>

---

### 频道成员相关

| `kind` | `code` | 版本 | 说明 | 建议处理 |
| --- | --- | --- | --- | --- |
| `userNotFound` | `108204` | 1.1.0 | 频道内没有该用户（订阅时 `uid` 不存在） | 以 `onUserJoin` / `onUserLeave` 维护的成员列表为准 |

---

### 流媒体（发布 / 订阅）相关

| `kind` | `code` | 版本 | 说明 | 建议处理 |
| --- | --- | --- | --- | --- |
| `publishFailed` | `108300` | 1.1.0 | 发布失败：SeaStart 引擎未连接 / 已断开（非重连中） | 等重连或重新入会后再发布 |
| `subscribeFailed` | `108301` | 1.1.0 | 订阅失败：SeaStart 引擎未连接 / 已断开（非重连中） | 等重连或重新入会后再订阅 |

引擎**正在重连**时发布 / 订阅报的是 `108014`（稍后可重试），不是 `108300` / `108301`。

---

### 引擎与通用错误

| `kind` | `code` | 版本 | 说明 | 建议处理 |
| --- | --- | --- | --- | --- |
| `engineNotSupported` | `108022` | 0.0.1 | 当前流媒体引擎不支持 | 检查频道的 `stream_vendor` 配置 |
| `engineDisconnected` | `108023` | 0.0.1 | 引擎已关闭或销毁 | 重新入会 |
| `invalidState` | `108024` | 0.0.1 | 当前状态不允许该操作（1.1.0 起有更具体原因时改用对应的码） | 检查调用顺序 |
| `internalError` | `108025` | 0.0.1 | SDK 内部错误 | 结合日志排查 |
| `cancelled` | `108026` | 0.0.1 | 操作被取消 | 业务层通常可忽略或重试 |
| `invalidArgument` | `108031` | 1.1.0 | 参数非法（如订阅时轨道类型不符、发布描述或发布配置为空） | 检查入参 |
| `featureNotSupported` | `108032` | 1.1.0 | 当前环境不支持该能力（如 `setOutputDevice()`、同一视频轨发布到多个频道时开 Simulcast） | 改用替代方案，不要重试 |

<Note>
`108027`–`108030` 在统一码表里是虚拟背景相关码，鸿蒙 SDK 不使用。
</Note>

---

### 推荐的处理方式

```typescript
import { SRTCError, SRTCErrorKind } from 'srtc';

try {
  const channel = await srtc.joinChannel(token, options);
} catch (e) {
  const err = e as SRTCError;
  if (err.kind !== undefined) {
    switch (err.kind) {
      case SRTCErrorKind.tokenExpired:
      case SRTCErrorKind.tokenInvalid:
        // 重新向业务后端取 Token
        break;
      case SRTCErrorKind.cameraPermissionDenied:
      case SRTCErrorKind.micPermissionDenied:
        // 引导用户去系统设置开权限（SDK 不弹授权框）
        break;
      case SRTCErrorKind.captureError:
        console.error(`采集失败: ${err.detail}, systemCode=${err.systemCode}`);
        break;
      case SRTCErrorKind.apiRequestFailed:
        if (SRTCError.isServerError(err)) {
          // 后端业务错误（1000–99999），文案语言随 SRTC.setLanguage
        } else {
          // 108006 网络 / HTTP 失败（看 err.httpStatus）或 108011 响应解码失败，可重试
        }
        break;
      default:
        console.error(`SRTC error ${err.code} (base ${err.baseCode}): ${err.detail}`);
    }
  } else {
    console.error(`未知错误: ${String(e)}`);
  }
}
```

<Warning>
**`JSON.stringify(new Error())` 的结果是 `{}`。**

ArkTS 里直接把错误对象序列化进日志会得到一个空对象，什么线索都没有。排障时请显式取
`code` / `detail`（SDK 错误）或 `code` / `message`（系统 `BusinessError`）。1.1.0 起采集失败已包成 `SRTCError`，系统原码在 `systemCode`。
</Warning>

建议在业务层把 `SRTCError` 映射成你们自己的错误域，而不是把英文 `detail` 直接展示给最终用户。

---

### 编解码相关的坑

<Warning>
**`codecNotSupported` 不一定会抛出来 —— 更常见的情况是「静默降级」。**

`@ohos/webrtc` 的 H264 / H265 是**纯硬编，没有软编兜底**。当设备能力表里查不到 H264 时，
SDK 内部会跳过编码偏好设置、**退回默认顺序（通常是 VP8）**，这个过程**不报错**。

表现是本机看得到画面，但与 Web / iOS / Android / CDN 互通不上。所以自测不能以
"看到画面"为准，要核对实际协商到的编码格式：

```typescript
import { videoCodecReport, videoCodecNames, isCodecSupported, Codec } from 'srtc';

console.info(`codecs = [${videoCodecNames().join(', ')}]`);
console.info(`H264 supported = ${isCodecSupported(Codec.h264)}`);
videoCodecReport().forEach((line: string) => console.info(line));
```

`videoCodecReport()` 会把收发两个方向的能力连同 `sdpFmtpLine` 一起列出来，
用它确认**发送侧**有没有 `video/H264`。只有接收侧有是不够的 —— 收得下不代表发得出。
</Warning>
