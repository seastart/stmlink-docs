---
title: "错误码"
description: "SMeeting Android SDK 的错误来源、202xxx 常量与应用处理原则"
---

Meeting 一次性结果和 Engine 错误事件统一返回：

```kotlin
fun onFail(errorCode: Int, message: String?)
fun onError(errorCode: Int, message: String?)
```

`message` 仅用于开发诊断，不保证适合直接展示给用户。应用应根据 `errorCode` 维护用户文案和国际化。

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

## MeetingErrorCode

完整类名：`cn.seastart.meeting.error.MeetingErrorCode`

### 通用错误（202000～202099）

| 常量 | 值 | 说明 |
| --- | --- | --- |
| `UNDEFINED_ERROR` | `202000` | 无法进一步识别或分类的最终兜底错误 |
| `SDK_NOT_INITIALIZED` | `202001` | Meeting SDK 尚未完成初始化 |
| `SDK_NOT_READY` | `202002` | RTC 引擎或 Meeting 必需运行状态尚未就绪 |
| `INVALID_PARAMETER` | `202003` | Meeting 公共接口参数不合法 |
| `INVALID_RESPONSE_DATA` | `202004` | 上游成功响应缺少必需字段或字段格式无效 |
| `TOKEN_INVALID` | `202005` | Meeting 在本地确认令牌无效 |
| `TOKEN_EXPIRED` | `202006` | Meeting 在本地确认令牌已过期 |

### Session 错误（202100～202199）

| 常量 | 值 | 说明 |
| --- | --- | --- |
| `SESSION_ALREADY_ACTIVE` | `202101` | 已有加入中或活动 Session 时再次发起入会 |
| `SESSION_NOT_ACTIVE` | `202102` | 当前不存在可用的活动 Session |
| `ENTER_MEETING_CANCELLED` | `202103` | 入会流程被显式取消 |
| `WAITING_ROOM_CONTEXT_MISSING` | `202104` | 退出等候室时缺少有效会议上下文 |
| `AUDIENCE_OPERATION_FORBIDDEN` | `202105` | 观众调用了开设备、共享或发流等受限能力 |

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

### IM 错误（202300～202349）

| 常量 | 值 | 说明 |
| --- | --- | --- |
| `IM_ENABLE_CANCELLED` | `202301` | 启用 IM 的网络流程被取消 |
| `IM_TOKEN_MISSING` | `202302` | IM 授权成功响应中缺少 IM token |

### HTTP 错误（202350～202399）

| 常量 | 值 | 说明 |
| --- | --- | --- |
| `HTTP_CLIENT_NOT_INITIALIZED` | `202351` | Meeting 内部 HTTP 客户端尚未初始化 |
| `NETWORK_ERROR` | `202352` | DNS、连接或断网等本地网络传输失败 |
| `REQUEST_TIMEOUT` | `202353` | 本地 HTTP 请求超时 |
| `REQUEST_CANCELLED` | `202354` | HTTP 请求被取消并需要转换为失败回调 |
| `EMPTY_RESPONSE_BODY` | `202355` | HTTP 请求成功但响应体为空 |

## 推荐处理方式

```kotlin
override fun onFail(errorCode: Int, message: String?) {
    logger.error("Meeting failed: code=$errorCode, message=$message")

    val userMessage = when (errorCode) {
        MeetingErrorCode.TOKEN_EXPIRED -> "登录信息已过期，请重新登录"
        MeetingErrorCode.SESSION_ALREADY_ACTIVE -> "已有会议正在进行"
        MeetingErrorCode.SCREEN_PERMISSION_DENIED -> "未获得屏幕录制权限"
        else -> "操作失败，请稍后重试"
    }
    showToast(userMessage)
}
```

日志中可同时记录 `errorCode` 和 `message`；UI 只使用应用自己维护的文案。
