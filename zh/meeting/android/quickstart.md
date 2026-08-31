---
title: "快速开始"
description: "使用 SMeeting Android 2.0.35 完成初始化、创建会议、注册事件、入会、发布本地音视频与订阅远端视频"
---

## 前置准备

+ 按[集成](/zh/meeting/android/integration)添加 `cn.seastart.meeting:meeting:2.0.35`。
+ 从业务服务端获取 `meetToken`，不要在客户端保存生成 token 所需的密钥。
+ 在应用侧申请相机和录音运行时权限。
+ 准备部署环境约定的 `streamVendor`；示例使用 `wangsucdn`，实际值以后端配置为准。

## 1. 创建并初始化 Engine

应用应集中持有一个 `MeetingEngine`。回调保持实际来源线程，UI 操作前切换到主线程。

```kotlin
private lateinit var meetingEngine: MeetingEngine

fun initMeeting(application: Application, meetToken: String) {
    meetingEngine = MeetingEngine.create(application)
    meetingEngine.initSdk(
        meetToken,
        null,
        object : MeetingResultCallback {
            override fun onSuccess() {
                // SDK 已就绪
            }

            override fun onFailure(errorCode: Int, message: String?) {
                // message 只用于诊断；用户文案根据 errorCode 生成
            }
        }
    )
}
```

不再使用 SDK 时释放 Engine：

```kotlin
fun releaseMeeting() {
    meetingEngine.release()
}
```

## 2. 创建会议

即时会议成功后直接返回 `MeetingCreatedBean`，不再暴露 `Data<T>` 网络包装。

```kotlin
val option = CreateImmediateMeetingOption(
    content = "产品评审",
    attendType = AttendType.ATTEND_NOT_LIMIT,
    mode = MeetingMode.Normal,
    entryMutePolicy = MuteState.MuteState3
)

meetingEngine.createImmediateMeeting(
    "项目周会",
    option,
    object : MeetingValueResultCallback<MeetingCreatedBean> {
        override fun onSuccess(value: MeetingCreatedBean) {
            val meetingId = value.meetingId
            val roomNo = value.roomNo
        }

        override fun onFailure(errorCode: Int, message: String?) {
            // 创建失败
        }
    }
)
```

预约会议使用 `createScheduleMeeting()`，其中 `planTime` 为秒级 Unix 时间戳，`planDur` 单位为分钟。

## 3. 注册会中事件

房间、成员、消息和媒体事件应在入会前赋值，以免错过初始事件；离会后它们会自动清除。

```kotlin
meetingEngine.roomEvent = object : MeetingRoomSimpleEvent() {
    override fun onDisconnected(
        reason: LeaveReason,
        statusCode: Int,
        message: String?
    ) {
        // 会议已真实断开
    }
}

meetingEngine.userEvent = object : MeetingUserSimpleEvent() {
    override fun onUserEnter(uid: String) {
        val member = meetingEngine.infosManager.getMemberByUid(uid)
        // 刷新成员列表
    }

    override fun onTrackAdded(uid: String, trackInfo: TrackInfo) {
        // 可根据 trackInfo.desc 决定是否订阅
    }
}
```

完整事件选择见 [Meeting 事件概览](/zh/meeting/android/api-reference/meeting-events)。

## 4. 加入和离开会议

入会成功返回 `MeetingEnterInfo`，会中接口仍在 `MeetingEngine` 上调用；不要引用 SDK 内部 `MeetingSession`。

```kotlin
meetingEngine.enterMeeting(
    activity = this,
    roomNo = "10000001",
    password = null,
    nick = "张三",
    avatar = "",
    streamVendor = "wangsucdn",
    isAudience = false,
    extendInfo = null,
    callback = object : MeetingValueResultCallback<MeetingEnterInfo> {
        override fun onSuccess(value: MeetingEnterInfo) {
            val meetingId = value.meetingId
            val myUid = value.uid
            // 已完成服务端入会和 SRTC join
        }

        override fun onFailure(errorCode: Int, message: String?) {
            // 入会失败
        }
    }
)
```

按会议 ID 入会时使用 `enterMeetingByMeetingId()`，其余参数相同。离会调用：

```kotlin
meetingEngine.exitMeeting()
```

## 5. 打开并发布摄像头、麦克风

`openCamera()` / `openMic()` 只做会前本地采集；入会后发布到会议必须使用 `openCameraAndPublish()` / `openMicAndPublish()`。

```kotlin
meetingEngine.openCameraAndPublish(
    localPreview,
    PreOptionCamera._480P,
    object : MeetingResultCallback {
        override fun onSuccess() {
            // 摄像头已采集并发布
        }

        override fun onFailure(errorCode: Int, message: String?) {
            // 已回滚本次发布和采集
        }
    }
)

meetingEngine.openMicAndPublish(
    PreOptionMic.def,
    object : MeetingResultCallback {
        override fun onSuccess() {
            // 麦克风已采集并发布
        }

        override fun onFailure(errorCode: Int, message: String?) {
            // 已回滚本次发布和采集
        }
    }
)
```

关闭设备：

```kotlin
meetingEngine.closeCamera()
meetingEngine.closeMic()
```

远端视频渲染控件必须使用 `VcsPlayerGlTextureView` 或 `VcsPlayerGlSurfaceView`；普通 Android `TextureView` / `SurfaceView` 不生效。

## 6. 订阅远端视频

从 `InfosManager` 查询轨道，再通过异步结果回调获取 `RemoteVideoTrack`。

```kotlin
val targetUid = "remote-user-001"
val trackInfo = meetingEngine.infosManager
    .getTrackInfoByTrackDesc(targetUid, TrackDesc.TRACK_MAIN.value)
    ?: return

meetingEngine.startPlayRemoteVideo(
    uid = targetUid,
    trackDesc = trackInfo.desc,
    view = remoteView,
    event = object : MeetingRemoteVideoSimpleEvent() {
        override fun onReceiveStreamStatusChange(
            uid: String,
            trackDesc: String,
            isChoke: Boolean
        ) {
            // 更新卡顿提示
        }
    },
    callback = object : MeetingValueResultCallback<RemoteVideoTrack> {
        override fun onSuccess(value: RemoteVideoTrack) {
            // 订阅成功，value 可继续管理渲染控件
        }

        override fun onFailure(errorCode: Int, message: String?) {
            // 订阅失败
        }
    }
)
```

取消订阅：

```kotlin
meetingEngine.stopPlayRemoteVideo(targetUid, trackInfo.desc)
```

## 下一步

+ [MeetingEngine](/zh/meeting/android/api-reference/MeetingEngine)：全部公开方法、参数和返回值
+ [模型类型](/zh/meeting/android/types)：配置和结果模型
+ [错误码](/zh/meeting/android/error-codes)：`202xxx` 与透传错误处理
+ [摄像头预设](/zh/meeting/android/presets/camera)：分辨率与码率选择
+ [音频路由](/zh/meeting/android/advanced/audio-routing)：扬声器、听筒、蓝牙和有线耳机
