---
title: "错误码"
description: "iOS SRTC 音视频 SDK 错误码枚举与处理说明"
---

### RTCEngineError
错误码

| **枚举名** | **枚举值** | **说明** |
| --- | :---: | --- |
| RTCEngineErrorOK | `0` | 无错误 |
| **系统级错误码** | | |
| RTCEngineErrorSystemError | `100001` | 系统内部错误 |
| RTCEngineErrorNotInitialized | `100002` | 未初始化 |
| RTCEngineErrorMediaNotInitialized | `100003` | 媒体模块尚未初始化 |
| RTCEngineErrorProtocolParsingError | `100004` | 协议解析错误 |
| **通用错误码** | | |
| RTCEngineErrorTimeout | `100005` | 超时 |
| RTCEngineErrorInvalidArgs | `100006` | 参数错误 |
| RTCEngineErrorConflict | `100007` | 重复操作冲突 |
| RTCEngineErrorSdkTokenInvalid | `100008` | 令牌失效 |
| **网络错误码** | | |
| RTCEngineErrorNetError | `100009` | 网络错误 |
| RTCEngineErrorMediaNetError | `100010` | 媒体网络错误 |
| RTCEngineErrorNotFound | `100011` | 目标不存在 |
| **客户端错误码** | | |
| RTCEngineErrorDeviceNoAuthorized | `103001` | 设备访问无权限 |
| RTCEngineErrorNotJoinedChannel | `103002` | 未加入频道 |
| RTCEngineErrorForbidden | `103003` | 操作不被允许 |
| RTCEngineErrorStreamNotFound | `103004` | 码流不存在 |


