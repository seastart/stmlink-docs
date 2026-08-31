---
title: "Meeting 事件概览"
description: "选择并注册 SMeeting Android 的 Engine、IM、设备、房间、成员、消息、媒体与原始帧事件"
---

SMeeting Android 事件都通过 `MeetingEngine` 的可空属性注册。每组事件同时提供 `MeetingXxxSimpleEvent` 空实现，只覆写需要的方法即可。

```kotlin
engine.engineEvent = object : MeetingEngineSimpleEvent() {
    override fun onError(errorCode: Int, message: String?) {
        // 记录全局运行错误
    }
}

engine.userEvent = object : MeetingUserSimpleEvent() {
    override fun onUserEnter(uid: String) {
        // 刷新成员列表
    }
}
```

## 事件选择

| 事件接口 | 何时使用 |
| --- | --- |
| [MeetingEngineEvent](/zh/meeting/android/api-reference/MeetingEngineEvent) | Engine 全局运行错误 |
| [MeetingImEvent](/zh/meeting/android/api-reference/MeetingImEvent) | IM 连接、重连、呼叫与提醒 |
| [MeetingCameraDeviceEvent](/zh/meeting/android/api-reference/MeetingCameraDeviceEvent) | 摄像头列表、断开与运行错误 |
| [MeetingMicDeviceEvent](/zh/meeting/android/api-reference/MeetingMicDeviceEvent) | 麦克风列表与当前设备失效 |
| [MeetingScreenCaptureEvent](/zh/meeting/android/api-reference/MeetingScreenCaptureEvent) | Android 本地屏幕采集状态 |
| [MeetingRoomEvent](/zh/meeting/android/api-reference/MeetingRoomEvent) | 房间配置、连接、录制、共享、讨论组与签到 |
| [MeetingUserEvent](/zh/meeting/android/api-reference/MeetingUserEvent) | 成员、角色、权限、设备状态、等候室与轨道 |
| [MeetingMessageEvent](/zh/meeting/android/api-reference/MeetingMessageEvent) | 聊天、系统消息与应用扩展消息 |
| [MeetingMediaEvent](/zh/meeting/android/api-reference/MeetingMediaEvent) | 媒体连接、远端帧、统计、音量和网络质量 |
| [MeetingLocalVideoFrameEvent](/zh/meeting/android/api-reference/MeetingLocalVideoFrameEvent) | 本地 YUV 视频帧 |
| [MeetingLocalAudioFrameEvent](/zh/meeting/android/api-reference/MeetingLocalAudioFrameEvent) | 本地 PCM 音频帧 |
| [MeetingRemoteVideoEvent](/zh/meeting/android/api-reference/MeetingRemoteVideoEvent) | 单条远端视频的接收和卡顿状态 |

## 生命周期与线程

+ Engine、IM、摄像头设备和麦克风设备事件与 `MeetingEngine` 生命周期一致，赋 `null` 后停止新的分发。
+ 房间、成员、消息和媒体事件绑定当前会议，离会时自动清除；下一场会议需要重新赋值。
+ `MeetingRemoteVideoEvent` 随一次远端订阅传入，取消订阅或离会后停止分发。
+ 回调保持 SRTC、IM 或网络的实际来源线程，不自动切换到 Android 主线程。
+ 本地和远端原始帧回调处于高频媒体线程，不得执行阻塞操作。
