---
title: "错误码"
description: "SRTC Swift SDK 错误类型 SRTCError 的分类说明与处理建议"
---

Swift SDK 当前公开的错误模型是 `SRTCError`。它不是传统的整数错误码表，而是一个带语义的 Swift 枚举。

这样设计的好处是：

+ 调用方可以直接按错误类别分支处理
+ 错误信息能保留上下文字符串
+ 比纯整数码更适合 Swift 的 `try / catch` 风格

---

### 连接相关

| 错误 | 说明 | 建议处理 |
| --- | --- | --- |
| `tokenExpired` | Token 已过期 | 重新向业务后端获取 Token |
| `tokenInvalid` | Token 不合法 | 检查 Token 编码和签发逻辑 |
| `alreadyJoined` | 已经加入频道 | 避免重复入会，或先执行离开 |
| `notConnected` | 当前未连接 | 检查调用时机 |
| `connectionFailed(String)` | 连接失败 | 记录服务端地址、网络环境、错误详情 |
| `connectionTimeout` | 连接超时 | 提示用户重试并检查网络连通性 |

---

### 信令相关

| 错误 | 说明 | 建议处理 |
| --- | --- | --- |
| `apiRequestFailed(statusCode:message:)` | HTTP API 请求失败 | 检查 demo 后端 / 业务后端响应 |
| `signatureError` | 签名生成失败 | 检查服务端鉴权逻辑 |
| `mqttConnectionFailed(String)` | MQTT 连接失败 | 检查 MQTT 地址和网络可达性 |
| `mqttSubscribeFailed(String)` | MQTT 订阅失败 | 检查 topic 权限和连接状态 |
| `messageDecodeFailed(String)` | 信令消息解码失败 | 检查服务端消息格式与 SDK 版本兼容性 |

---

### WebRTC / 传输相关

| 错误 | 说明 | 建议处理 |
| --- | --- | --- |
| `webrtcError(String)` | 底层 WebRTC 错误 | 记录日志，优先定位设备和 SDP 过程 |
| `sdpNegotiationFailed(String)` | SDP 协商失败 | 检查编解码器、引擎能力和服务端协商 |
| `transportNotReady` | 传输层尚未就绪 | 等待连接完成后再发布 / 订阅 |
| `peerConnectionFailed` | PeerConnection 创建或运行失败 | 检查 ICE / STUN / TURN / 平台权限 |

---

### 轨道与采集相关

| 错误 | 说明 | 建议处理 |
| --- | --- | --- |
| `trackNotFound(String)` | 找不到指定轨道 | 检查 `uid` / `trackId` 是否匹配 |
| `trackAlreadyPublished(String)` | 轨道已发布 | 避免重复发布同一对象 |
| `trackNotPublished(String)` | 轨道未发布 | 取消发布前先确认状态 |
| `captureError(String)` | 采集失败 | 检查权限、设备占用、平台版本 |
| `codecNotSupported(String)` | 编解码器不支持 | 调整编码偏好或预设 |
| `maxPublishLimitReached` | 超过可发布轨道上限 | 控制并发发布数量 |
| `deviceNotFound(String)` | 找不到设备 | 检查设备列表是否变化或设备已拔出 |

---

### 引擎与通用错误

| 错误 | 说明 | 建议处理 |
| --- | --- | --- |
| `engineNotSupported(String)` | 当前流媒体引擎不支持 | 检查 `stream_vendor` 配置 |
| `engineDisconnected` | 引擎已断开 | 等待重连或重新入会 |
| `invalidState(String)` | 当前状态不允许该操作 | 检查调用顺序 |
| `internalError(String)` | SDK 内部错误 | 结合日志排查 |
| `cancelled` | 操作被取消 | 业务层通常可忽略或重试 |

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
    case .captureError(let message):
        print("采集失败:", message)
    default:
        print("SRTC error:", error.localizedDescription)
    }
} catch {
    print("Unknown error:", error.localizedDescription)
}
```

如果你在业务层已经有统一错误弹窗，建议把 `SRTCError` 映射成你们自己的错误域，而不是直接把英文 `localizedDescription` 原样暴露给最终用户。
