---
title: "错误码"
description: "SRTC HarmonyOS SDK 的错误类型 SRTCError、数字错误码表与处理建议"
---

SDK 抛出的错误统一是 `SRTCError`，它继承 `Error`，并额外带三个字段：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `kind` | `SRTCErrorKind` | 错误种类，用来分支处理 |
| `code` | `number` | 完整数字错误码（含平台前缀），用于日志与跨端对齐 |
| `detail` | `string` | 纯文本描述，**不含**错误码 |

`toString()` 输出 `"{code}: {detail}"`，方便日志里一行同时拿到码和描述。

---

### 错误码是怎么拼出来的

+ **SDK 内部错误**：原始码 < 1000，会被加上平台前缀拼成 6 位数。
  HarmonyOS 的 RTC 前缀是 **`108`**，所以内部错误码形如 `108001` ~ `108026`。
+ **业务后端透传的错误码**：≥ 1000 时**原样保留**，不再加前缀。

这套编号与其它端一致（windows=101、android=102、iOS=103、linux=104、macOS=105、
web=106、小程序=107、HarmonyOS=108），所以同一类错误在各端的后三位是相同的，
跨端排障时可以直接对齐。

<Note>
`apiRequestFailed` 的 `code` 语义与其它错误不同：它带的是**后端返回的码**。
后端码 ≥ 1000 时原样透出，< 1000 时同样会被加上 `108` 前缀。
</Note>

---

### 连接相关

| `kind` | `code` | 构造参数 | 说明 | 建议处理 |
| --- | --- | --- | --- | --- |
| `notConnected` | `108001` | — | 当前未连接 | 检查调用时机，等入会成功后再操作 |
| `tokenExpired` | `108002` | — | Token 已过期 | 重新向业务后端获取 Token |
| `tokenInvalid` | `108004` | — | Token 不合法 | 检查 Token 编码与签发逻辑 |
| `alreadyJoined` | `108005` | — | 已经加入该频道 | 避免重复入会，或先离开 |
| `connectionFailed` | `108006` | `msg` | 连接失败 | 记录服务端地址、网络环境与错误详情 |
| `connectionTimeout` | `108007` | — | 连接超时 | 提示用户重试并检查网络连通性 |

---

### 信令相关

| `kind` | `code` | 构造参数 | 说明 | 建议处理 |
| --- | --- | --- | --- | --- |
| `apiRequestFailed` | 后端码 | `statusCode`, `msg` | HTTP API 请求失败 | 见上方 Note，按后端码排查 |
| `signatureError` | `108008` | — | 签名生成失败 | 检查服务端鉴权逻辑 |
| `signalingConnectFailed` | `108009` | `msg` | 信令通道连接失败 | 检查网络可达性、代理与防火墙 |
| `signalingSubscribeFailed` | `108010` | `msg` | 信令通道订阅失败 | 检查 Token 是否有效、连接是否已建立 |
| `messageDecodeFailed` | `108011` | `msg` | 信令消息解码失败 | 检查服务端消息格式与 SDK 版本兼容性 |

---

### WebRTC / 传输相关

| `kind` | `code` | 构造参数 | 说明 | 建议处理 |
| --- | --- | --- | --- | --- |
| `webrtcError` | `108012` | `msg` | 底层 WebRTC 错误 | 记录日志，优先定位设备与 SDP 过程 |
| `sdpNegotiationFailed` | `108013` | `msg` | SDP 协商失败 | 检查编解码能力与服务端协商 |
| `transportNotReady` | `108014` | — | 传输层尚未就绪 | 等连接完成后再发布 / 订阅 |
| `peerConnectionFailed` | `108015` | — | PeerConnection 创建或运行失败 | 检查 ICE / STUN / TURN 与权限 |

---

### 轨道与采集相关

| `kind` | `code` | 构造参数 | 说明 | 建议处理 |
| --- | --- | --- | --- | --- |
| `trackNotFound` | `108003` | `id` | 找不到指定轨道 | 检查 `uid` / `trackId` 是否匹配 |
| `trackAlreadyPublished` | `108016` | `id` | 轨道已发布 | 避免重复发布同一对象 |
| `trackNotPublished` | `108017` | `id` | 轨道未发布 | 取消发布前先确认状态 |
| `captureError` | `108018` | `msg` | 采集失败 | 检查权限、设备占用、是否已 `SRTC.init` |
| `codecNotSupported` | `108019` | `codec` | 编解码器不支持 | 见下方「编解码相关的坑」 |
| `maxPublishLimitReached` | `108020` | — | 超过可发布轨道上限 | 控制并发发布数量 |
| `deviceNotFound` | `108021` | `id` | 找不到设备 | 设备可能已拔出，重新枚举 |

---

### 引擎与通用错误

| `kind` | `code` | 构造参数 | 说明 | 建议处理 |
| --- | --- | --- | --- | --- |
| `engineNotSupported` | `108022` | `vendor` | 当前流媒体引擎不支持 | 检查频道的 `stream_vendor` 配置 |
| `engineDisconnected` | `108023` | — | 引擎已断开 | 等待重连或重新入会 |
| `invalidState` | `108024` | `msg` | 当前状态不允许该操作 | 检查调用顺序 |
| `internalError` | `108025` | `msg` | SDK 内部错误 | 结合日志排查 |
| `cancelled` | `108026` | — | 操作被取消 | 业务层通常可忽略或重试 |

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
      case SRTCErrorKind.captureError:
        console.error(`采集失败: ${err.detail}`);
        break;
      default:
        console.error(`SRTC error ${err.code}: ${err.detail}`);
    }
  } else {
    console.error(`未知错误: ${String(e)}`);
  }
}
```

<Warning>
**`JSON.stringify(new Error())` 的结果是 `{}`。**

ArkTS 里直接把错误对象序列化进日志会得到一个空对象，什么线索都没有。排障时请显式取
`code` / `detail`（SDK 错误）或 `code` / `message`（系统 `BusinessError`）。
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
