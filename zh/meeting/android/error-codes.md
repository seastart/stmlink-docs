---
title: "错误码"
description: "SMeeting Android SDK 的错误来源、202xxx 常量与应用处理原则"
---

Meeting 一次性结果和 Engine 错误事件统一返回：

```kotlin
fun onFailure(errorCode: Int, message: String?)
fun onError(errorCode: Int, message: String?)
```

Meeting 自产错误提示为空；RTC 和后端提示原样透传，可为 null 或空字符串。应用为无提示的错误提供本地化文案。

## 错误来源

错误码是开放的 `Int`，不只包含 Meeting 自产错误：

| 来源 | 范围或形式 | 处理方式 |
| --- | --- | --- |
| Meeting SDK | `202000`～`202999` | 由 `MeetingErrorCode` 定义 |
| SRTC SDK | 通常为 `102xxx` | 保留底层原始错误码 |
| librtc | 底层定义 | 保留原始错误码 |
| Meeting 服务端 | 服务端业务码 | 保留有效业务码 |
| HTTP | HTTP 状态码或 Meeting 本地网络错误 | 按实际来源处理 |

因此不要把回调错误码强制转换为封闭枚举，也不要假设所有错误都能在 `MeetingErrorCode` 中找到。


HTTP 非 2xx 返回原始状态码和状态提示。Meeting 本地网络失败为 `202007`，超时为 `202353`，取消为 `202354`，空响应体为 `202355`，解析失败或缺少必需字段为 `202356`，这些本地错误的提示均为空。

MQTT 的 `mcu_task.err_desc`、`mcu_alarm.alarm_brief` 及聊天、自定义消息内容通过原有业务事件原样交付，保留已有过滤规则，不统一改写为 SDK 错误提示。

## MeetingErrorCode

完整类名：`cn.seastart.meeting.error.MeetingErrorCode`

### 通用错误（202000～202099）

| 常量 | 值 | 说明 |
| --- | --- | --- |
| `UNKNOWN` | `202000` | 无法进一步分类的兜底错误 |
| `NOT_LOGGED_IN` | `202001` | 未登录或 Meeting SDK 尚未完成初始化 |
| `TOKEN_EXPIRED` | `202002` | Meeting 在本地确认令牌已过期 |
| `NOT_IN_MEETING` | `202003` | 不在会议中或没有活动会议 |
| `TOKEN_INVALID` | `202005` | Meeting 在本地确认令牌无效 |
| `ALREADY_IN_MEETING` | `202006` | 已有加入中或活动会议 |
| `NETWORK_ERROR` | `202007` | DNS、连接或断网等本地网络传输失败 |
| `INVALID_STATE` | `202011` | RTC 或 Meeting 状态未就绪，或当前状态不允许操作 |
| `INVALID_ARGUMENT` | `202012` | Meeting 公共接口参数不合法 |

### Session 错误（202100～202199）

| 常量 | 值 | 说明 |
| --- | --- | --- |
| `ENTER_MEETING_CANCELLED` | `202103` | 入会流程被显式取消 |
| `WAITING_ROOM_CONTEXT_MISSING` | `202104` | 退出等候室时缺少有效会议上下文 |
| `AUDIENCE_OPERATION_FORBIDDEN` | `202105` | 观众调用了开设备、共享或发流等受限能力 |
| `SESSION_OPERATION_CANCELLED` | `202106` | 会中异步操作尚未完成时，所属会议已经开始结束 |

### 媒体错误（202200～202299）

| 常量 | 值 | 说明 |
| --- | --- | --- |
| `CAMERA_OPEN_FAILED` | `202201` | 无 RTC 原始码可透传时，Meeting 未能打开摄像头 |
| `MIC_OPEN_FAILED` | `202202` | 无 RTC 原始码可透传时，Meeting 未能打开麦克风 |
| `SCREEN_PERMISSION_DENIED` | `202203` | Android 录屏授权被拒绝 |
| `SCREEN_TRACK_UNAVAILABLE` | `202204` | 屏幕共享流程未能创建有效轨道 |
| `WHITEBOARD_REQUEST_CANCELLED` | `202205` | 白板共享请求被取消 |
| `WHITEBOARD_URL_MISSING` | `202206` | 白板接口成功但响应中缺少 URL |
| `CLOUD_RECORD_CAPTURE_DISABLED` | `202207` | 未开启客户端云录制采集配置时启动课程录制轨道 |
| `LOCAL_TRACK_UNAVAILABLE` | `202208` | Meeting 需要的本地媒体轨道不存在且无更精确错误 |
| `REMOTE_TRACK_UNAVAILABLE` | `202209` | Meeting 需要订阅的远端媒体轨道不存在 |
| `LOCAL_DEVICE_OPERATION_CANCELLED` | `202210` | 本地设备操作被更新的开启、关闭或释放动作取消 |
| `LOCAL_DEVICE_CAPABILITY_UNSUPPORTED` | `202211` | 当前 SRTC 采集链路不支持请求的本地设备能力 |
| `LOCAL_DEVICE_OPERATION_IN_PROGRESS` | `202212` | 同一本地设备上一次开启事务尚未结束，终态由该次操作给出 |

### IM 错误（202300～202349）

| 常量 | 值 | 说明 |
| --- | --- | --- |
| `IM_ENABLE_CANCELLED` | `202301` | 启用 IM 的网络流程被取消 |
| `IM_TOKEN_MISSING` | `202302` | IM 授权成功响应中缺少 IM token |

### HTTP 错误（202350～202399）

| 常量 | 值 | 说明 |
| --- | --- | --- |
| `HTTP_CLIENT_NOT_INITIALIZED` | `202351` | Meeting 内部 HTTP 客户端尚未初始化 |
| `REQUEST_TIMEOUT` | `202353` | 本地 HTTP 请求超时 |
| `REQUEST_CANCELLED` | `202354` | HTTP 请求取消，或主动停止尚未完成的屏幕共享启动 |
| `EMPTY_RESPONSE_BODY` | `202355` | HTTP 请求成功但响应体为空 |
| `RESPONSE_PARSE_FAILED` | `202356` | HTTP 响应存在，但无法转换为公共业务结果 |

## RTC 摄像头错误（原样透传）

以下错误来自 RTC `2.0.33`，随 Meeting `2.0.37` 生效，不属于 `MeetingErrorCode`。切换失败后不保证仍在采集，目标校验失败时可能保留原采集；SDK 不自动回退，恢复策略由应用决定。

| RTC 常量 | 值 | 说明 |
| --- | --- | --- |
| `CAMERA_FIRST_FRAME_TIMEOUT` | `102239` | 等待摄像头首帧超时 |
| `CAMERA_FORMAT_UNAVAILABLE` | `102242` | 没有可用的采集格式 |
| `CAMERA_OPEN_TIMEOUT` | `102243` | 打开摄像头超时 |
| `CAMERA_SESSION_TIMEOUT` | `102244` | 创建摄像头会话超时 |

## 推荐处理方式

```kotlin
override fun onFailure(errorCode: Int, message: String?) {
    logger.error("Meeting failed: code=$errorCode, message=$message")

    val userMessage = message?.takeIf { it.isNotBlank() } ?: when (errorCode) {
        MeetingErrorCode.TOKEN_EXPIRED -> "登录信息已过期，请重新登录"
        MeetingErrorCode.ALREADY_IN_MEETING -> "已有会议正在进行"
        MeetingErrorCode.SCREEN_PERMISSION_DENIED -> "未获得屏幕录制权限"
        else -> "操作失败，请稍后重试"
    }
    showToast(userMessage)
}
```

日志中保留原始错误码和提示。UI 优先使用上游非空提示，否则按错误码提供本地化文案，不根据码值范围猜测来源。

## 2.0.41 升级迁移

旧常量名称不保留兼容别名；其余已声明常量编号不变。尤其 `202002`、`202003`、`202006` 已有新含义，应用应更新硬编码和文案映射。

| 旧常量 | 旧码 | 新常量 | 新码 |
| --- | ---: | --- | ---: |
| `UNDEFINED_ERROR` | `202000` | `UNKNOWN` | `202000` |
| `SDK_NOT_INITIALIZED` | `202001` | `NOT_LOGGED_IN` | `202001` |
| `SDK_NOT_READY` | `202002` | `INVALID_STATE` | `202011` |
| `INVALID_PARAMETER` | `202003` | `INVALID_ARGUMENT` | `202012` |
| `INVALID_RESPONSE_DATA` | `202004` | `RESPONSE_PARSE_FAILED` | `202356` |
| `TOKEN_EXPIRED` | `202006` | `TOKEN_EXPIRED` | `202002` |
| `SESSION_ALREADY_ACTIVE` | `202101` | `ALREADY_IN_MEETING` | `202006` |
| `SESSION_NOT_ACTIVE` | `202102` | `NOT_IN_MEETING` | `202003` |
| `NETWORK_ERROR` | `202352` | `NETWORK_ERROR` | `202007` |
