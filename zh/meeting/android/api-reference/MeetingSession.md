---
title: "MeetingSession"
description: "一次已接受的会议会话，承载会中事件、会控、媒体、共享、消息与订阅能力"
---

`MeetingSession` 由 `MeetingEngine.enterMeeting(...)` 或 `enterMeetingByMeetingId(...)` 成功返回。它只属于当前这次入会，离会后不可复用。

## 生命周期状态

| 状态 | 含义 |
| --- | --- |
| `JOINING` | 正在执行入会流程 |
| `ACTIVE` | 已加入 RTC 频道，可以调用会中接口 |
| `LEAVING` | 正在屏蔽回调并回收资源 |
| `CLOSED` | 已关闭，不再接受会中调用 |

```kotlin
val meetingId: String
val uid: String
val state: MeetingSessionState
```

旧 Session 的 generation 失效后，`state` 返回 `CLOSED`；继续调用其他会中方法会抛出 `IllegalStateException`，从而避免旧会议句柄误操作下一场会议。

## 信息与管理入口

```kotlin
val infosManager: InfosManager
val signInManager: SignInManager
```

两个类型均位于 `cn.seastart.meeting.manager` 包。`infosManager` 提供房间、成员和轨道的本地快照；`signInManager` 提供会中签到能力。

## 注册 Session 级事件

```kotlin
session.setRoomEvent(event: MeetingRoomEvent?)
session.setUserEvent(event: MeetingUserEvent?)
session.setRoomMsgEvent(event: RoomMsgEvent?)
session.setMediaEvent(event: MeetingMediaEvent?)
session.setLocalVideoFrameEvent(event: MeetingLocalVideoFrameEvent?)
session.setLocalAudioFrameEvent(event: MeetingLocalAudioFrameEvent?)
session.setExtensionMessageEvent(event: ExtensionMessageEvent?)
```

传 `null` 可取消监听。事件作用域和线程契约见 [事件接口](/zh/meeting/android/api-reference/meeting-events)。

## 退出会议

```kotlin
fun leave()
```

`leave()` 会使当前 Session 失效，停止采集、共享和订阅，移除渲染控件，并终止本次 Session 的后续回调。SDK 级资源仍由 `MeetingEngine.release()` 释放。

## 常用会中能力

| 分类 | 主要方法 |
| --- | --- |
| 摄像头 | `requestOpenCamera`、`closeCamera`、`switchCamera`、`switchLight`、`addPreview`、`removePreview` |
| 麦克风 | `requestOpenMic`、`closeMic` |
| 屏幕与白板 | `initScreenShare`、`startScreenShare`、`stopScreenShare`、`requestShareBoard`、`stopShareWhiteBoard` |
| 房间消息 | `sendRoomChatMessage`、`sendRoomCustomMessage`、`getRoomChatMsgList` |
| 举手与确认 | `requestHandUp`、`cancelHandUp`、`confirmOpenCameraAgree/Refuse`、`confirmOpenMicAgree/Refuse` |
| 云录制 | `startCloudRecord`、`stopCloudRecord`、`enableCourseRecordTrack`、`disableCourseRecordTrack` |
| 远端视频 | `startPlayRemoteVideo`、`stopPlayRemoteVideo`、`getRemoteVideoTrack` |
| 合成流 | `startPlayRemoteMixture`、`stopPlayRemoteMixture`、`getRemoteMixtureTrack` |
| 网宿流 | `subscribeWsStream`、`unsubscribeWsStream`、`getWsStreamTrack` |
| 音频路由 | `getAudioRouterManager`、`releaseAudioRouterManager`、`toggleRemoteAudioMute` |

主持人会控、等候室和讨论组接口也全部属于 Session，包括 `adminDestroyMeeting`、`adminUpdateRoom*`、`adminUpdateUser*`、`adminMove*WaitingRoom`、`createSubMeeting`、`startSubMeeting` 等。

## 使用示例

```kotlin
engine.enterMeeting(
    activity,
    roomNo,
    null,
    nick,
    avatar,
    "wangsucdn",
    false,
    null,
    object : MeetingValueResultCallback<MeetingSession> {
        override fun onSuccess(value: MeetingSession) {
            session = value
            value.setUserEvent(object : MeetingUserSimpleEvent() {
                override fun onUserEnter(uid: String) {
                    // 更新成员列表
                }
            })
        }

        override fun onFail(errorCode: Int, message: String?) {
            // 根据 errorCode 生成用户提示；message 仅用于诊断
        }
    }
)
```
