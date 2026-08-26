---
title: "错误码"
description: "Android SRTC 的 librtc 状态码、SDK 自产 102xxx 分域错误码、查询 API 与透传规则"
---

Android SRTC 的错误码分为两类：

+ `StatusCode`：librtc 已定义的 native 状态码镜像，范围主要为 `100xxx`。
+ `cn.seastart.rtc.error`：Android SDK 主动产生的 `102xxx` 分域错误码。

回调参数统一使用 `Int` 并保留原值。native、后端、HTTP 库或流媒体厂商返回的错误不会被重新映射，因此调用方必须保留未知错误码的兜底处理。

## librtc 状态码 `StatusCode`

| 枚举名 | 值 | 说明 |
| --- | ---: | --- |
| `OK` | `0` | 成功。 |
| `SystemError` | `100001` | 系统内部错误。 |
| `NotInitialized` | `100002` | native 客户端未初始化。 |
| `MediaNotInitialized` | `100003` | 媒体模块尚未初始化。 |
| `ProtocolParsingError` | `100004` | 协议解析错误。 |
| `Timeout` | `100005` | 操作超时。 |
| `InvalidArgs` | `100006` | 参数非法。 |
| `Conflict` | `100007` | 操作冲突，例如重复加入同一频道。 |
| `SdkTokenInvalid` | `100008` | SDK Token 无效或已过期。 |
| `NetError` | `100009` | 信令网络错误。 |
| `MediaNetError` | `100010` | 媒体网络错误。 |
| `NotFound` | `100011` | 目标资源不存在。 |
| `UserCancelled` | `100012` | 用户取消操作。 |

旧文档中的 `DeviceNotfound` 已删除，`100011` 的当前枚举名是 `NotFound`。`LibRtcStatusCode` 也已删除，librtc 常量只由 `StatusCode` 公开。

## SDK 公共与频道错误

### `RtcCommonErrorCode`

| 常量 | 值 | 说明 |
| --- | ---: | --- |
| `SDK_NOT_INIT` | `102201` | RTC SDK 尚未初始化。 |
| `STREAM_NOT_READY` | `102203` | 当前操作依赖的流媒体资源尚未准备好。 |
| `NATIVE_CLIENT_CLOSED` | `102214` | Kotlin 层持有的 native client 已关闭。 |

### `RtcChannelErrorCode`

| 常量 | 值 | 说明 |
| --- | ---: | --- |
| `TRACK_TYPE_INVALID` | `102002` | 发布或取消发布时传入了不支持的 Track 类型。 |
| `CHANNEL_NOT_START` | `102202` | 目标频道尚未加入成功。 |
| `USER_NOT_FOUND` | `102204` | 目标成员不存在。 |
| `TRACK_NOT_FOUND` | `102205` | 目标 Track 不存在。 |
| `STREAM_VENDOR_NOT_SUPPORTED` | `102206` | 当前流媒体引擎不支持该操作。 |
| `FORBIDDEN_FOR_AUDIENCE` | `102207` | 观众身份不允许发布本地流。 |
| `CHANNEL_ALREADY_EXISTS` | `102208` | 当前 Engine 已存在相同频道。 |
| `CHANNEL_JOIN_NATIVE_EXCEPTION` | `102209` | 调用 native join 时发生异常。 |
| `CHANNEL_JOIN_PAYLOAD_INVALID` | `102210` | native join 成功回调数据无法解析。 |
| `CHANNEL_INFO_INVALID` | `102211` | native 频道信息为空或非法。 |
| `CHANNEL_RESOURCE_CREATE_FAILED` | `102212` | 频道业务对象或流媒体资源创建失败。 |
| `CHANNEL_JOIN_DISCONNECTED_WITHOUT_STATUS` | `102213` | 入会阶段断开且 native 未提供有效状态码。 |
| `NATIVE_CHANNEL_CLOSED` | `102215` | Kotlin 层持有的 native channel 已关闭。 |

## 采集错误

### `RtcCameraErrorCode`

| 常量 | 值 | 说明 |
| --- | ---: | --- |
| `LEGACY_LACK_PERMISSION` | `102001` | 兼容已发布旧权限错误值，不再用于新的权限判断。 |
| `CAMERA_DEVICE_NOT_FOUND` | `102230` | 未找到可用摄像头。 |
| `CAMERA_PERMISSION_DENIED` | `102231` | 应用没有摄像头权限。 |
| `CAMERA_OPEN_FAILED` | `102232` | 摄像头打开失败。 |
| `CAMERA_SESSION_FAILED` | `102233` | 摄像头采集会话创建失败。 |
| `CAMERA_REQUEST_FAILED` | `102234` | 摄像头采集请求下发失败。 |
| `CAMERA_DISCONNECTED` | `102235` | 摄像头在运行期间断开。 |
| `CAMERA_RUNTIME_ERROR` | `102236` | 摄像头运行时系统错误。 |
| `CAMERA_STATE_INVALID` | `102237` | 操作不符合摄像头状态机约束。 |

### `RtcMicErrorCode`

| 常量 | 值 | 说明 |
| --- | ---: | --- |
| `MIC_DEVICE_NOT_FOUND` | `102250` | 未找到请求的麦克风设备。 |
| `MIC_PERMISSION_DENIED` | `102251` | 应用没有录音权限。 |
| `MIC_OPEN_FAILED` | `102252` | 麦克风打开或启动失败。 |
| `MIC_READ_FAILED` | `102253` | SDK 检测到麦克风读取失败或停滞。 |
| `MIC_STATE_INVALID` | `102254` | 操作不符合麦克风状态机约束。 |
| `MIC_FORMAT_UNSUPPORTED` | `102255` | 请求的麦克风采集格式不受支持。 |

### `RtcScreenErrorCode`

| 常量 | 值 | 说明 |
| --- | ---: | --- |
| `SCREEN_CAPTURE_OPERATION_REJECTED` | `102270` | 当前 SDK 状态不能接纳新的屏幕采集启动操作。 |

## 流媒体与 HTTP 错误

### `RtcStreamErrorCode`

| 常量 | 值 | 说明 |
| --- | ---: | --- |
| `ERROR_PARAM_ILLEGAL` | `102310` | 流媒体配置参数非法。 |
| `ERROR_OPERATION_CANCEL` | `102311` | 方向相反的待处理操作互相抵消。 |
| `ERROR_OPERATION_IGNORE` | `102312` | 重复操作被忽略。 |
| `ERROR_ABOUT_SDP_OPERATION` | `102313` | SDP 创建、设置或协商失败。 |
| `ERROR_SUBSCRIBE_REFUSE` | `102314` | RTC 服务端拒绝订阅请求。 |

### `RtcHttpErrorCode`

| 常量 | 值 | 说明 |
| --- | ---: | --- |
| `HTTP_NOT_INITIALIZED` | `102350` | RTC HTTP 能力尚未初始化。 |
| `HTTP_INVALID_ARGUMENT` | `102351` | SDK 检测到 HTTP 请求参数非法。 |
| `HTTP_NETWORK_ERROR` | `102352` | HTTP 请求失败且没有上游错误码可透传。 |
| `HTTP_RESPONSE_INVALID` | `102353` | HTTP 响应为空或无法解析。 |

## 错误目录查询

`RtcErrorCatalog` 只查询 SDK 自产的 `102xxx` 错误。对 librtc、后端和厂商透传码返回 `null`。

```kotlin
val descriptor: RtcErrorDescriptor? = RtcErrorCatalog.find(errorCode)

descriptor?.let {
    Log.e(
        "SRTC",
        "code=${it.code} name=${it.name} module=${it.module} " +
            "recoverable=${it.recoverable} message=${it.defaultMessage}"
    )
}
```

`RtcErrorDescriptor` 字段：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `code` | `Int` | 稳定的六位 SDK 错误码。 |
| `name` | `String` | 稳定英文名称，适合日志和监控。 |
| `module` | `RtcErrorModule` | 错误所属领域。 |
| `defaultMessage` | `String` | 不含运行时现场信息的默认说明。 |
| `recoverable` | `Boolean` | 调用方是否可通过重试或修正状态恢复。 |

`RtcErrorCatalog.all` 返回当前 SDK 的全部自产错误描述。`RtcErrorModule` 领域及预留范围如下：

| 领域 | 号码范围 |
| --- | --- |
| `LEGACY` | `102000..102099` |
| `COMMON` | `102200..102229` |
| `CHANNEL` | `102200..102229` |
| `CAMERA` | `102230..102249` |
| `MIC` | `102250..102269` |
| `SCREEN` | `102270..102289` |
| `STREAM` | `102300..102349` |
| `HTTP` | `102350..102379` |

`COMMON` 与 `CHANNEL` 目前共享历史号段，但具体错误码全局唯一。
可调用 `RtcErrorModule.owns(code)` 判断一个 SDK 自产错误是否落在该领域的预留号码范围内；这不等同于判断错误是否已被 `RtcErrorCatalog` 正式定义。

## 回调处理建议

+ `RTCClientEvent.onJoinFailed(channel, statusCode)`：处理入会失败。
+ `RTCResultListener.onFail(code)`：处理具体异步操作失败。
+ `RTCEngineEvent.onError(channelId, errorCode, message)`：处理 Engine 阻断操作和全局错误。
+ `RTCClientEvent.onDisconnected(channel, leaveReason, statusCode, message)`：处理频道不可恢复断连。

记录错误时同时保留频道 ID、原始数值和运行时 `message`。不要只依赖枚举或 `RtcErrorCatalog`，否则 SDK 尚未认识的新上游错误会丢失。
