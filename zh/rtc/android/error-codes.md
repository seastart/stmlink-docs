---
title: "错误码"
description: "Android SRTC 的 librtc 状态码、SDK 自产 102xxx 分域错误码、查询 API 与透传规则"
---

Android SRTC SDK 自身定义的错误码分为两类：

+ `StatusCode`：librtc 本地状态码映射后的 Android 错误码。
+ `cn.seastart.rtc.error`：Android SDK 主动产生的 `102xxx` 统一语义错误码。

回调参数统一使用 `Int`。librtc 本地错误映射为 Android `102xxx` 错误码；后端业务码保留原值。HTTP 库和流媒体厂商错误仍可能返回其他数值，调用方应保留未知错误码的兜底处理。

## 错误文案 `message`

从 2.0.36 起，`RTCClientEvent.onJoinFailed(...)` 与 `RTCResultListener.onFail(...)` 增加 `message: String` 参数。后端错误有可用文案时，`message` 可提供后端返回的内容。可通过 [`RTCEngine.setLanguage(...)`](/zh/rtc/android/api-reference/RTCEngine) 设置请求语言；实际文案以后端返回为准。设置为 `RtcLanguage.SYSTEM` 时，请求跟随系统语言。

SDK 自产错误和 librtc 本地错误的 `message` 为空字符串；诊断详情仅用于日志。后端返回的错误码与提示按来源原样透传，不根据错误码范围判定来源。非空 String 回调遇到后端 null 提示时返回空字符串，不补写文案。应用可按错误码为无提示的失败提供本地化文案。

HTTP 非 2xx 保留原始状态码和状态消息；没有 HTTP 状态码时，请求超时返回 `102007`，普通网络失败返回 `102006`，解析失败、缺少 `code` 或空响应返回 `102011`，提示为空。取消请求仍走取消回调。

`RTCEngineEvent.onError(...)` 的 `message` 为可空类型，参见 [RTCEngineEvent](/zh/rtc/android/api-reference/RTCEngineEvent)。

## librtc 状态码 `StatusCode`

下表对照 2.0.35 与 2.0.36 的公开枚举值；新值自 2.0.36 起生效。升级时若应用写死了旧数值，应改用新值，优先引用枚举常量。

| 枚举名 | 2.0.35 | 2.0.36 起 | 说明 |
| --- | ---: | ---: | --- |
| `OK` | `0` | `0` | 成功。 |
| `SystemError` | `100001` | `102025` | 系统内部错误。 |
| `NotInitialized` | `100002` | `102024` | native 客户端未初始化。 |
| `MediaNotInitialized` | `100003` | `102024` | 媒体模块尚未初始化。 |
| `ProtocolParsingError` | `100004` | `102011` | 协议解析错误。 |
| `Timeout` | `100005` | `102007` | 操作超时。 |
| `InvalidArgs` | `100006` | `102031` | 参数非法。 |
| `Conflict` | `100007` | `102005` | 操作冲突。 |
| `SdkTokenInvalid` | `100008` | `102004` | SDK Token 无效或已过期。 |
| `NetError` | `100009` | `102006` | 信令网络错误。 |
| `MediaNetError` | `100010` | `102012` | 媒体网络错误。 |
| `NotFound` | `100011` | `102204` | 目标资源不存在。 |
| `UserCancelled` | `100012` | `102026` | 用户取消操作。 |

`NotInitialized` 与 `MediaNotInitialized` 共用 `102024`；`NotFound` 与 `RtcErrorCode.USER_NOT_FOUND` 共用 `102204`。

## 2.0.38 统一错误码 `RtcErrorCode`

从 2.0.38 起，原 7 个分域错误码对象合并为 `cn.seastart.rtc.error.RtcErrorCode`。以下列出全部 40 个常量；应用升级时应同步修改常量引用和本地化映射。

| 常量 | 值 | 说明 |
| --- | ---: | --- |
| `NOT_IN_CHANNEL` | `102001` | 不在频道内：未加入、已离开，或频道未开始 |
| `TRACK_NOT_FOUND` | `102003` | 流轨道不存在 |
| `TOKEN_INVALID` | `102004` | Token 不合法：解析失败或内容不完整 |
| `ALREADY_JOINED` | `102005` | 已加入 / 重复操作冲突 |
| `CONNECTION_FAILED` | `102006` | 连接失败：网络请求失败且没有上游错误码。HTTP 非 2xx 保留原始状态码。 |
| `CONNECTION_TIMEOUT` | `102007` | 连接 / 请求超时 |
| `MESSAGE_DECODE_FAILED` | `102011` | 信令消息 / 服务端响应解析失败（不是 JSON、缺 `code` 字段、字段不合法） |
| `WEBRTC_ERROR` | `102012` | 底层 WebRTC / 媒体网络错误 |
| `SDP_NEGOTIATION_FAILED` | `102013` | SDP 协商失败 |
| `TRANSPORT_NOT_READY` | `102014` | 传输未就绪 / 正在重连，稍后重试即可 |
| `CAPTURE_FAILED` | `102018` | 采集失败：设备被占用、打开失败、硬件错误 |
| `DEVICE_NOT_FOUND` | `102021` | 设备不存在，或指定的设备已拔出 |
| `ENGINE_NOT_SUPPORTED` | `102022` | 流媒体引擎不支持 |
| `ENGINE_DISCONNECTED` | `102023` | native 客户端或频道已关闭。 |
| `INVALID_STATE` | `102024` | 当前状态不允许该操作：调用顺序不对、未初始化、需在加入频道前设置 |
| `INTERNAL_ERROR` | `102025` | SDK 内部错误 |
| `CANCELLED` | `102026` | 操作被取消 |
| `VIRTUAL_BACKGROUND_NOT_INSTALLED` | `102028` | 虚拟背景未安装 |
| `VIRTUAL_BACKGROUND_MODEL_NOT_FOUND` | `102029` | 虚拟背景模型不存在或无效 |
| `INVALID_ARGUMENT` | `102031` | 参数非法 |
| `SCREEN_SHARE_DENIED` | `102039` | 屏幕共享被拒绝：用户取消，或系统未授权录屏 |
| `PERMISSION_DENIED` | `102042` | 设备权限被拒（无法区分摄像头 / 麦克风时；能区分时用 231 / 251） |
| `FORBIDDEN` | `102043` | 当前身份 / 角色不允许该操作 |
| `USER_NOT_FOUND` | `102204` | 频道内没有该用户 |
| `CHANNEL_JOIN_NATIVE_EXCEPTION` | `102209` | 加入频道时底层异常（仅 Android） |
| `CHANNEL_RESOURCE_CREATE_FAILED` | `102212` | 加入频道时本地资源创建失败（仅 Android） |
| `CHANNEL_JOIN_DISCONNECTED` | `102213` | 加入频道过程中连接断开（仅 Android） |
| `CAMERA_PERMISSION_DENIED` | `102231` | 无摄像头权限 |
| `CAMERA_SESSION_FAILED` | `102233` | 摄像头会话创建失败 |
| `CAMERA_REQUEST_FAILED` | `102234` | 摄像头采集请求失败 |
| `CAMERA_DISCONNECTED` | `102235` | 摄像头被系统断开 |
| `CAMERA_FIRST_FRAME_TIMEOUT` | `102239` | 摄像头首帧超时 |
| `CAMERA_FORMAT_UNAVAILABLE` | `102242` | 摄像头格式不可用 |
| `CAMERA_OPEN_TIMEOUT` | `102243` | 摄像头打开超时 |
| `CAMERA_SESSION_TIMEOUT` | `102244` | 摄像头会话超时 |
| `MIC_PERMISSION_DENIED` | `102251` | 无麦克风权限 |
| `MIC_FORMAT_UNSUPPORTED` | `102255` | 麦克风格式不支持 |
| `SCREEN_CAPTURE_REQUEST_REJECTED` | `102270` | 屏幕共享请求不被受理：授权界面已销毁或重复请求（仅 Android） |
| `SUBSCRIBE_FAILED` | `102301` | 订阅失败 / 订阅被拒 |
| `OPERATION_IGNORED` | `102312` | 操作被忽略，不算失败（仅 Android） |

### 从 2.0.37 迁移

旧 `102001` 的权限含义迁移到 `102042`；新 `102001` 表示不在频道，不能沿用旧的硬编码提示。下表的新常量均属于 `RtcErrorCode`。

| 旧常量 | 旧码 | 新常量 | 新码 |
| --- | ---: | --- | ---: |
| `RtcCameraErrorCode.LEGACY_LACK_PERMISSION` | `102001` | `PERMISSION_DENIED` | `102042` |
| `RtcChannelErrorCode.TRACK_TYPE_INVALID` | `102002` | `INVALID_ARGUMENT` | `102031` |
| `RtcCommonErrorCode.SDK_NOT_INIT` | `102201` | `INVALID_STATE` | `102024` |
| `RtcChannelErrorCode.CHANNEL_NOT_START` | `102202` | `NOT_IN_CHANNEL` | `102001` |
| `RtcCommonErrorCode.STREAM_NOT_READY` | `102203` | `TRANSPORT_NOT_READY` | `102014` |
| `RtcErrorCode.USER_NOT_FOUND` | `102204` | `USER_NOT_FOUND` | `102204` |
| `RtcChannelErrorCode.TRACK_NOT_FOUND` | `102205` | `TRACK_NOT_FOUND` | `102003` |
| `RtcChannelErrorCode.STREAM_VENDOR_NOT_SUPPORTED` | `102206` | `ENGINE_NOT_SUPPORTED` | `102022` |
| `RtcChannelErrorCode.FORBIDDEN_FOR_AUDIENCE` | `102207` | `FORBIDDEN` | `102043` |
| `RtcChannelErrorCode.CHANNEL_ALREADY_EXISTS` | `102208` | `ALREADY_JOINED` | `102005` |
| `RtcChannelErrorCode.CHANNEL_JOIN_NATIVE_EXCEPTION` | `102209` | `CHANNEL_JOIN_NATIVE_EXCEPTION` | `102209` |
| `RtcChannelErrorCode.CHANNEL_JOIN_PAYLOAD_INVALID` | `102210` | `MESSAGE_DECODE_FAILED` | `102011` |
| `RtcChannelErrorCode.CHANNEL_INFO_INVALID` | `102211` | `MESSAGE_DECODE_FAILED` | `102011` |
| `RtcChannelErrorCode.CHANNEL_RESOURCE_CREATE_FAILED` | `102212` | `CHANNEL_RESOURCE_CREATE_FAILED` | `102212` |
| `RtcChannelErrorCode.CHANNEL_JOIN_DISCONNECTED_WITHOUT_STATUS` | `102213` | `CHANNEL_JOIN_DISCONNECTED` | `102213` |
| `RtcCommonErrorCode.NATIVE_CLIENT_CLOSED` | `102214` | `ENGINE_DISCONNECTED` | `102023` |
| `RtcChannelErrorCode.NATIVE_CHANNEL_CLOSED` | `102215` | `ENGINE_DISCONNECTED` | `102023` |
| `RtcCameraErrorCode.CAMERA_DEVICE_NOT_FOUND` | `102230` | `DEVICE_NOT_FOUND` | `102021` |
| `RtcCameraErrorCode.CAMERA_PERMISSION_DENIED` | `102231` | `CAMERA_PERMISSION_DENIED` | `102231` |
| `RtcCameraErrorCode.CAMERA_OPEN_FAILED` | `102232` | `CAPTURE_FAILED` | `102018` |
| `RtcCameraErrorCode.CAMERA_SESSION_FAILED` | `102233` | `CAMERA_SESSION_FAILED` | `102233` |
| `RtcCameraErrorCode.CAMERA_REQUEST_FAILED` | `102234` | `CAMERA_REQUEST_FAILED` | `102234` |
| `RtcCameraErrorCode.CAMERA_DISCONNECTED` | `102235` | `CAMERA_DISCONNECTED` | `102235` |
| `RtcCameraErrorCode.CAMERA_RUNTIME_ERROR` | `102236` | `CAPTURE_FAILED` | `102018` |
| `RtcCameraErrorCode.CAMERA_STATE_INVALID` | `102237` | `INVALID_STATE` | `102024` |
| `RtcCameraErrorCode.CAMERA_FIRST_FRAME_TIMEOUT` | `102239` | `CAMERA_FIRST_FRAME_TIMEOUT` | `102239` |
| `RtcCameraErrorCode.VIRTUAL_BACKGROUND_MODEL_INVALID` | `102240` | `VIRTUAL_BACKGROUND_MODEL_NOT_FOUND` | `102029` |
| `RtcCameraErrorCode.VIRTUAL_BACKGROUND_NOT_INSTALL` | `102241` | `VIRTUAL_BACKGROUND_NOT_INSTALLED` | `102028` |
| `RtcCameraErrorCode.CAMERA_FORMAT_UNAVAILABLE` | `102242` | `CAMERA_FORMAT_UNAVAILABLE` | `102242` |
| `RtcCameraErrorCode.CAMERA_OPEN_TIMEOUT` | `102243` | `CAMERA_OPEN_TIMEOUT` | `102243` |
| `RtcCameraErrorCode.CAMERA_SESSION_TIMEOUT` | `102244` | `CAMERA_SESSION_TIMEOUT` | `102244` |
| `RtcMicErrorCode.MIC_DEVICE_NOT_FOUND` | `102250` | `DEVICE_NOT_FOUND` | `102021` |
| `RtcMicErrorCode.MIC_PERMISSION_DENIED` | `102251` | `MIC_PERMISSION_DENIED` | `102251` |
| `RtcMicErrorCode.MIC_OPEN_FAILED` | `102252` | `CAPTURE_FAILED` | `102018` |
| `RtcMicErrorCode.MIC_READ_FAILED` | `102253` | `CAPTURE_FAILED` | `102018` |
| `RtcMicErrorCode.MIC_STATE_INVALID` | `102254` | `INVALID_STATE` | `102024` |
| `RtcMicErrorCode.MIC_FORMAT_UNSUPPORTED` | `102255` | `MIC_FORMAT_UNSUPPORTED` | `102255` |
| `RtcScreenErrorCode.SCREEN_CAPTURE_OPERATION_REJECTED` | `102270` | `SCREEN_CAPTURE_REQUEST_REJECTED` | `102270` |
| `RtcStreamErrorCode.ERROR_PARAM_ILLEGAL` | `102310` | `INVALID_ARGUMENT` | `102031` |
| `RtcStreamErrorCode.ERROR_OPERATION_CANCEL` | `102311` | `CANCELLED` | `102026` |
| `RtcStreamErrorCode.ERROR_OPERATION_IGNORE` | `102312` | `OPERATION_IGNORED` | `102312` |
| `RtcStreamErrorCode.ERROR_ABOUT_SDP_OPERATION` | `102313` | `SDP_NEGOTIATION_FAILED` | `102013` |
| `RtcStreamErrorCode.ERROR_SUBSCRIBE_REFUSE` | `102314` | `SUBSCRIBE_FAILED` | `102301` |
| `RtcHttpErrorCode.HTTP_NOT_INITIALIZED` | `102350` | `INVALID_STATE` | `102024` |
| `RtcHttpErrorCode.HTTP_INVALID_ARGUMENT` | `102351` | `INVALID_ARGUMENT` | `102031` |
| `RtcHttpErrorCode.HTTP_NETWORK_ERROR` | `102352` | `CONNECTION_FAILED` | `102006` |
| `RtcHttpErrorCode.HTTP_RESPONSE_INVALID` | `102353` | `MESSAGE_DECODE_FAILED` | `102011` |

## 错误目录查询

`RtcErrorCatalog.find(code)` 只按数值查询 SDK 已定义的错误描述，不能据此判断错误来源。未收录的错误码返回 `null`；`StatusCode.NotFound` 与 SDK 的 `USER_NOT_FOUND` 同为 `102204`，查询该值会命中 `USER_NOT_FOUND`。

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
| `defaultMessage` | `String` | 仅供日志排查的默认说明，不作为 SDK 自产错误的回调提示。 |
| `recoverable` | `Boolean` | 调用方是否可通过重试或修正状态恢复。 |

`RtcErrorCatalog.all` 返回当前 SDK 的全部自产错误描述。`RtcErrorModule` 领域及预留范围如下：

| 领域 | 号码范围 |
| --- | --- |
| `COMMON` | `102000..102099` |
| `CHANNEL` | `102200..102229` |
| `CAMERA` | `102230..102249` |
| `MIC` | `102250..102269` |
| `SCREEN` | `102270..102299` |
| `STREAM` | `102300..102349` |

可调用 `RtcErrorModule.owns(code)` 判断一个 SDK 自产错误是否落在该领域的预留号码范围内；这不等同于判断错误是否已被 `RtcErrorCatalog` 正式定义。

## 回调处理建议

+ `RTCClientEvent.onJoinFailed(channel, statusCode, message)`：处理入会失败。
+ `RTCResultListener.onFail(code, message)`：处理具体异步操作失败。
+ `RTCEngineEvent.onError(channelId, errorCode, message)`：处理 Engine 阻断操作和全局错误。
+ `RTCClientEvent.onDisconnected(channel, leaveReason, statusCode, message)`：处理频道不可恢复断连。

记录错误时同时保留频道 ID、原始数值和运行时 `message`。不要只依赖枚举或 `RtcErrorCatalog`，否则 SDK 尚未认识的新上游错误会丢失。
