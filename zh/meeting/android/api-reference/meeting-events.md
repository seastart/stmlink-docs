---
title: "Meeting 事件接口"
description: "2.0.34 按 Engine 与 Session 生命周期划分的 IM、房间、成员、媒体和设备事件"
---

2.0.34 不再让 Meeting 事件继承底层 RTC 事件，也不保留旧 `ImEvent`、`RoomEvent`、`UserEvent`、`MediaEvent` 兼容层。事件按生命周期注册。

## Engine 级事件

通过 `MeetingEngine.set*Event()` 注册，与 SDK 生命周期一致：

| 接口 | 主要回调 |
| --- | --- |
| `MeetingEngineEvent` | `onError(errorCode, message)` |
| `MeetingImEvent` | IM 连接、断开、重连、普通消息、呼叫、会议提醒、等候室和子会议消息 |
| `MeetingCameraDeviceEvent` | 摄像头设备列表变化、设备断开和设备错误 |
| `MeetingMicDeviceEvent` | 麦克风设备列表变化和设备失效 |

每个接口都有对应空实现：`MeetingEngineSimpleEvent`、`MeetingImSimpleEvent`、`MeetingCameraDeviceSimpleEvent`、`MeetingMicDeviceSimpleEvent`。

```kotlin
engine.setEngineEvent(object : MeetingEngineSimpleEvent() {
    override fun onError(errorCode: Int, message: String?) {
        // 未被一次性结果回调消费的 Engine 或 Session 错误
    }
})
```

## Session 级事件

通过当前 `MeetingSession.set*Event()` 注册，只接收本次会议的事件：

| 接口 | 主要回调 |
| --- | --- |
| `MeetingRoomEvent` | 频道连接、房间状态、主持人转移、共享、录制、签到和讨论组事件 |
| `MeetingUserEvent` | 成员进退会、角色和名称、设备状态、轨道、举手和会控请求 |
| `RoomMsgEvent` | 房间聊天消息和系统消息 |
| `MeetingMediaEvent` | 媒体连接、远端视频帧、统计、音量、活跃说话人与网络质量 |
| `MeetingRemoteVideoEvent` | 指定远端视频轨道的接收卡顿状态 |
| `MeetingLocalVideoFrameEvent` | 显式订阅的本地 YUV 视频帧和尺寸变化 |
| `MeetingLocalAudioFrameEvent` | 显式订阅的本地 PCM 音频帧 |
| `ExtensionMessageEvent` | 会中自定义业务消息 |

主要 Meeting 接口也提供 `MeetingRoomSimpleEvent`、`MeetingUserSimpleEvent`、`MeetingMediaSimpleEvent`、`MeetingRemoteVideoSimpleEvent`、`MeetingLocalVideoFrameSimpleEvent` 和 `MeetingLocalAudioFrameSimpleEvent`，调用方只需覆写关心的方法。

```kotlin
session.setUserEvent(object : MeetingUserSimpleEvent() {
    override fun onUserEnter(uid: String) {
        // 远端成员加入
    }

    override fun onUserExit(userInfo: UserInfo) {
        // 远端成员离开；Meeting 层暂不额外暴露离开原因
    }
})
```

## 线程契约

+ Engine、Session 业务、IM、设备、媒体统计和一次性结果回调运行在主线程。
+ 本地音视频帧、远端视频帧和远端视频接收状态运行在 RTC 媒体线程，不能直接更新 UI。
+ 音量 Map 和活跃说话人 List 在切换线程前已创建快照。
+ 本地帧只在显式设置监听时向 RTC 注册；使用完请传 `null` 取消监听，避免持续复制媒体数据。

## 生命周期约束

SDK 使用 `channelId + generation` 过滤旧频道迟到回调。Session 进入 `LEAVING` 或 `CLOSED` 后不再分发会中事件；新会议必须在新返回的 Session 上重新注册监听。
