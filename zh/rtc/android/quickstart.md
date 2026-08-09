---
title: "快速开始"
description: "Android SRTC 的最小接入流程，涵盖 Engine 初始化、显式音视频采集、单频道发布订阅与资源释放"
---

本文按“创建 Engine → 绑定回调 → 加入频道 → 启动采集并发布 → 订阅远端媒体 → 离会释放”的顺序，给出 Android SRTC SDK 的最小可用流程。

开始前请先完成以下准备：

+ 按照 [集成](/zh/rtc/android/integration) 完成 Maven 仓库、SDK 依赖和基础环境配置。
+ 准备服务端签发的频道 `token`。
+ 在应用侧申请摄像头和麦克风运行时权限。
+ 如需管理扬声器、听筒或蓝牙耳机等输出设备，请参考 [音频路由使用](/zh/rtc/android/advanced/audio-routing)。

## Step 1：创建并初始化 `RTCEngine`

`RTCEngine.create(...)` 必须传入 Engine 级错误监听器。它用于接收无法归入频道业务回调的错误，以及调用未开始频道等阻断错误；`channelId` 无法确定时为 `null`。

```kotlin
private lateinit var rtcEngine: RTCEngine

fun initRtcSdk(application: Application) {
    rtcEngine = RTCEngine.create(
        app = application,
        enableLocalLog = true,
        engineEvent = object : RTCEngineSimpleEvent() {
            override fun onError(channelId: String?, errorCode: Int, message: String?) {
                // 统一记录或展示 Engine 错误
            }
        },
        localLogPath = null,
        version = "app: ${BuildConfig.VERSION_NAME}"
    )
    rtcEngine.initSDK()
}
```

完整参数说明见 [RTCEngine](/zh/rtc/android/api-reference/RTCEngine) 和 [RTCEngineEvent](/zh/rtc/android/api-reference/RTCEngineEvent)。

## Step 2：准备频道回调与媒体回调

每次 `join(...)` 都要传入该频道自己的 `RTCClientEvent`。只覆写少数事件时，建议继承 `RTCClientSimpleEvent`，避免直接实现完整接口。

```kotlin
private val clientEvent = object : RTCClientSimpleEvent() {
    override fun onJoinSucceed(channel: String, uid: String, whiteBoard: String?) {
        // 真正入会成功；可在这里更新 UI 或开始发布
    }

    override fun onJoinFailed(channel: String?, statusCode: Int) {
        // 入会失败；statusCode 见错误码文档
    }

    override fun onRemoteUserJoin(channel: String, uid: String) {
        // 维护本频道成员列表
    }

    override fun onStreamTrackAdd(
        uid: String,
        channel: String,
        trackId: String,
        trackDesc: String
    ) {
        subscribeRemoteVideo(uid, trackId, trackDesc)
    }

    override fun onDisconnected(
        channel: String,
        leaveReason: LeaveReason,
        statusCode: Int,
        message: String
    ) {
        // 本频道发生不可恢复断连
    }
}

rtcEngine.setRtcMediaEvent(object : RTCMediaSimpleEvent() {
    override fun onMediaConnected(channel: String) {
        // 默认频道的流媒体服务器连接成功
    }

    override fun onVolumesReport(
        channel: String,
        volumes: MutableMap<UserTrackDesc, VolumeInfo>
    ) {
        // 频道音量信息，可用于说话人高亮
    }
})
```

所有频道级回调都会显式携带 `channel`，即使监听器只绑定在一个 `RTCChannel` 上，也应使用该参数进行日志和状态隔离。更多定义见 [RTCClientEvent](/zh/rtc/android/api-reference/RTCClientEvent) 与 [RTCMediaEvent](/zh/rtc/android/api-reference/RTCMediaEvent)。

## Step 3：加入频道

`join(...)` 会同步返回 `RTCChannel?`：

+ 返回非空仅表示 SDK 已接受请求并创建频道句柄，不代表已经入会成功。
+ 真正结果以 `onJoinSucceed(...)` 或 `onJoinFailed(...)` 为准。
+ SDK 未初始化或已经释放时会同步抛出 `SdkNotInitializedException`。

```kotlin
private var defaultChannel: RTCChannel? = null

fun joinChannel(activity: Activity, token: String) {
    defaultChannel = rtcEngine.join(
        activity = activity,
        token = token,
        clientEvent = clientEvent,
        options = JoinOptions(
            autoSubscribeAudio = true,
            autoSubscribeVideo = false
        )
    )

    if (defaultChannel == null) {
        // 请求在创建频道会话前被拒绝；具体原因仍通过 onJoinFailed 返回
    }
}
```

第一条 `join` 创建默认频道，`RTCEngine` 上的发布、订阅、查询和 `leave()` 等扁平接口都作用于它。SDK 也支持同时加入多个频道；快速开始只讲单频道流程，具体接入见 [多频道](/zh/rtc/android/advanced/multi-channel)。

## Step 4：启动本地采集并发布

以下发布流程应在 `onJoinSucceed(...)` 之后执行。采集与发布是两个独立动作：先显式启动本地采集，再把同一个本地轨道发布到频道。取消发布不会自动停止共享采集；不再需要设备时还要调用轨道的 `stopCapture()`。

### 4.1 摄像头采集与发布

```kotlin
private lateinit var cameraTrack: LocalCameraTrack

fun startCamera(previewView: VcsPlayerGlTextureView) {
    cameraTrack = rtcEngine.getLocalCameraTrack(PreOptionCamera._720P)
    cameraTrack.addPlayView(previewView)
    cameraTrack.startCapture(object : RTCResultListener {
        override fun onSuccess() {
            rtcEngine.publishLocalVideo(
                track = cameraTrack,
                publishCustomOpt = PublishCustomOptions(
                    desc = TrackDesc.TRACK_MAIN.value,
                    props = null,
                    simulcasts = null
                ),
                listener = null
            )
        }

        override fun onFail(code: Int) {
            // 例如未授予 CAMERA 权限
        }
    })
}
```

详细说明见 [LocalCameraTrack](/zh/rtc/android/api-reference/LocalCameraTrack)。

### 4.2 麦克风采集与发布

麦克风采集模块已与入会、发布解耦。`publishLocalAudio(...)` 不再负责打开麦克风，必须先调用 `LocalMicTrack.startCapture(...)`。

```kotlin
private lateinit var micTrack: LocalMicTrack

fun startMicrophone() {
    micTrack = rtcEngine.getLocalMicTrack(PreOptionMic.def)
    micTrack.startCapture(object : RTCResultListener {
        override fun onSuccess() {
            rtcEngine.publishLocalAudio(
                track = micTrack,
                publishCustomOpt = PublishCustomOptions(
                    desc = TrackDesc.TRACK_AUDIO.value,
                    props = null,
                    simulcasts = null
                ),
                listener = null
            )
        }

        override fun onFail(code: Int) {
            // 例如未授予 RECORD_AUDIO 权限或麦克风打开失败
        }
    })
}
```

显式采集也可以脱离频道使用。先设置 `setRtcLocalAudioFrameEvent(...)`，再调用 `micTrack.startCapture(...)`，即可接收本地 PCM 数据用于录制或处理；仅注册回调不会自动打开麦克风。详见 [LocalMicTrack](/zh/rtc/android/api-reference/LocalMicTrack) 与 [RTCEngine](/zh/rtc/android/api-reference/RTCEngine#setrtclocalaudioframeevente)。

### 4.3 屏幕共享（可选）

```kotlin
val screenTrack = rtcEngine.getLocalScreenTrack(this, PreOptionScreen.def)

screenTrack.request { granted, intent ->
    if (granted && intent != null) {
        screenTrack.startCapture(intent, hasBar = true)
        rtcEngine.publishLocalVideo(
            track = screenTrack,
            publishCustomOpt = PublishCustomOptions(
                desc = TrackDesc.TRACK_SHARE.value,
                props = null,
                simulcasts = null
            ),
            listener = null
        )
    }
}
```

接口细节见 [LocalScreenTrack](/zh/rtc/android/api-reference/LocalScreenTrack)。

## Step 5：订阅并播放远端媒体

收到 `onStreamTrackAdd(...)` 后，从默认频道获取远端轨道、绑定渲染 View，再发起订阅：

```kotlin
private fun subscribeRemoteVideo(uid: String, trackId: String, trackDesc: String) {
    val remoteTrack = rtcEngine.getRemoteVideoTrack(uid, trackDesc)
    remoteTrack?.addPlayView(remoteView)

    rtcEngine.subscribeRemoteTrack(
        uid = uid,
        trackId = trackId,
        preferTrackIds = null,
        result = object : RTCResultListener {
            override fun onSuccess() = Unit
            override fun onFail(code: Int) {
                // 订阅失败
            }
        }
    )
}

// 放在前面的 clientEvent 实现中
override fun onStreamTrackRemove(uid: String, channel: String, trackInfo: TrackInfo) {
    rtcEngine.unSubscribeRemoteTrack(uid, trackInfo.id)
    rtcEngine.getRemoteVideoTrack(uid, trackInfo.desc)?.removePlayView(remoteView)
}
```

详细说明见 [RemoteVideoTrack](/zh/rtc/android/api-reference/RemoteVideoTrack)。

## Step 6：离开频道并释放资源

```kotlin
// 先从默认频道停止发布
rtcEngine.unPublishLocalAudio(micTrack, null)
rtcEngine.unPublishLocalVideo(cameraTrack, null)

// 再关闭共享采集设备
micTrack.stopCapture()
cameraTrack.stopCapture()

// 离开默认频道；也可调用 defaultChannel?.leave()
rtcEngine.leave()

// 应用不再使用 RTC 时释放 Engine
rtcEngine.releaseSDK()
```

`releaseSDK()` 会释放本轮初始化周期中的全部频道与共享资源；后续仍可重新调用 `initSDK()`。

## 更多能力

+ 多频道并发加入、按频道发布订阅与资源隔离：[多频道](/zh/rtc/android/advanced/multi-channel)
+ 麦克风输入设备枚举、切换与 PCM 回调：[LocalMicTrack](/zh/rtc/android/api-reference/LocalMicTrack)
+ 自定义视频推流：[自定义推流](/zh/rtc/android/advanced/custom-track)
+ 电子白板：[电子白板](/zh/rtc/whiteboard)
+ 音频输出设备管理：[音频路由使用](/zh/rtc/android/advanced/audio-routing)
+ SDK 完整接口：[RTCEngine](/zh/rtc/android/api-reference/RTCEngine)
