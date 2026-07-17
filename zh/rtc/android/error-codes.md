---
title: "错误码"
description: "Android SRTC 音视频 SDK 错误码枚举与处理说明"
---

### StatusCode
错误码枚举定义如下（以 `StatusCode.kt` 为准）：

| 枚举名 | 枚举值 | 说明 |
| --- | --- | --- |
| OK | `0` | 成功 |
| SystemError | `100001` | 系统内部错误 |
| NotInitialized | `100002` | 未初始化 |
| MediaNotInitialized | `100003` | 媒体模块尚未初始化 |
| ProtocolParsingError | `100004` | 协议解析错误 |
| Timeout | `100005` | 超时 |
| InvalidArgs | `100006` | 参数错误 |
| Conflict | `100007` | 重复操作 |
| SdkTokenInvalid | `100008` | SDK Token 失效 |
| NetError | `100009` | 网络错误 |
| MediaNetError | `100010` | 媒体网络错误 |
| DeviceNotfound | `100011` | 设备不存在 |
| LACK_PERMISSION | `102001` | 缺少权限 |
| ERROR_TRACK_TYPE | `102002` | 错误的 Track 类型 |
