---
title: "快速开始"
description: "Android SRTC 音视频 SDK 快速接入与基础流程"
---

# 快速开始

本文按“初始化 → 绑定回调 → 加入频道 → 发布本地媒体 → 订阅远端媒体 → 离会释放”的顺序，给出 Android SRTC SDK 的最小可用流程。

开始前请先完成以下准备：

- 按照 [集成](/zh/rtc/android/integration) 完成 Maven 仓库、SDK 依赖和基础环境配置。
- 准备好服务端签发的 `token`，它是调用 `join(...)` 的必填参数。
- 如果要打开摄像头、麦克风或屏幕共享，请在应用侧先处理好 Android 运行时权限。
- 如果业务中需要管理扬声器、听筒、蓝牙耳机等输出设备，可继续参考 [音频路由使用](/zh/rtc/android/advanced/audio-routing)。

## Step 1：创建并初始化 `RTCEngine`

在调用任何频道、采集、发布、订阅相关接口前，先创建 `RTCEngine` 实例并调用 `initSDK()`。

- `app`：建议传 `Application` 实例。
- `enableLocalLog`：是否启用本地日志，联调阶段建议开启。
- `localLogPath`：日志目录；不传时使用 SDK 默认目录。
- `version`：上层应用版本标识，建议写入 App 版本号，便于排查问题。

```kotlin
private lateinit var rtcEngine: RTCEngine

fun initRtcSdk(application: Application) {
    rtcEngine = RTCEngine.create(
        app = application,
        enableLocalLog = true,
        localLogPath = null,
        version = "app: ${BuildConfig.VERSION_NAME}"
    )

    rtcEngine.initSDK()
}
```

如果需要查看完整参数说明，可参考 [RTCEngine](/zh/rtc/android/api-reference/RTCEngine)。

## Step 2：绑定常见回调与媒体参数

建议在加入频道前就把回调绑定好，这样从 `join(...)` 开始产生的状态变化都能及时接收到。

```kotlin
rtcEngine.setRtcClientEvent(object : RTCClientEvent {
    override fun onJoinSucceed(channel: String, uid: String, whiteBoard: String?) {
        // 自己加入频道成功
        // 后续可以在这里更新 UI、记录当前 uid、开始展示会中状态
    }

    override fun onRemoteUserJoin(channel: String, uid: String) {
        // 远端用户加入频道
    }

    override fun onStreamTrackAdd(uid: String, channel: String, trackId: String, trackDesc: String) {
        // 收到新增码流通知
        // 通常在这里决定是否订阅远端视频轨道
    }

    override fun onStreamTrackRemove(uid: String, channel: String, trackInfo: TrackInfo) {
        // 远端码流移除
        // 通常在这里移除对应渲染视图并清理状态
    }

    override fun onDisconnected(leaveReason: LeaveReason, statusCode: Int, message: String) {
        // 服务断开且不可恢复
        // 一般需要提示用户并重新加入频道或重新鉴权
    }
})

rtcEngine.setRtcMediaEvent(object : RTCMediaEvent {
    override fun onMediaConnected() {
        // 流媒体服务器连接成功
    }

    override fun onVolumesReport(volumes: MutableMap<UserTrackDesc, VolumeInfo>) {
        // 音量信息上报
        // 可用于说话人高亮、音量柱动画等
    }
})

rtcEngine.setRtcImEvent(imEvent)

// 可选：本地视频帧外部回调（如需自行处理本地画面时设置）
rtcEngine.setRtcLocalVideoFrameEvent(object : RTCLocalVideoFrameEvent {
    override fun onLocalVideoFrame(yuv: ByteArray?, width: Int, height: Int, stamp: Long, format: Int, facing: Int) {
        // 拿到本地一帧视频（yuv 为 SDK 单独拷贝的数据）
    }

    override fun onLocalVideoFrameSizeChanged(width: Int, height: Int, facing: Int) {
        // 本地帧尺寸或摄像头方向变化
    }
})
```

常见回调建议重点关注：

- `RTCClientEvent.onJoinSucceed(...)`：以这个回调作为“真正入会成功”的依据。
- `RTCClientEvent.onRemoteUserJoin(...)` / `onRemoteUserLeave(...)`：维护成员列表。
- `RTCClientEvent.onStreamTrackAdd(...)` / `onStreamTrackRemove(...)`：维护远端轨道订阅与渲染。
- `RTCClientEvent.onDisconnected(...)`：处理不可恢复断连。
- `RTCMediaEvent.onVolumesReport(...)`：做说话人检测或音量展示。

更多回调定义可参考：

- [RTCClientEvent](/zh/rtc/android/api-reference/RTCClientEvent)
- [RTCMediaEvent](/zh/rtc/android/api-reference/RTCMediaEvent)
- [RTCImEvent](/zh/rtc/android/api-reference/RTCImEvent)

## Step 3：加入频道

调用 `join(...)` 后，`RTCResultListener.onSuccess()` 只表示请求发送成功；是否真正加入频道，以 `RTCClientEvent.onJoinSucceed(...)` 回调为准。

`options` 为预留参数，当前版本未生效，传 `null` 即可。

```kotlin
rtcEngine.join(
    activity = this,
    token = token,
    options = null,
    resultListener = object : RTCResultListener {
        override fun onSuccess() {
            // join 请求已成功发出
        }

        override fun onFail(code: Int) {
            // join 请求失败，例如 token 无效或参数错误
        }
    }
)
```

远端媒体的订阅时机由业务层控制：在 `onStreamTrackAdd(...)` 中按需调用 `subscribeRemoteTrack(...)`（见 Step 5）。

## Step 4：发布本地媒体

### 4.1 摄像头采集与发布

操作顺序建议固定为：

1. 获取 `LocalCameraTrack`
2. 绑定本地预览视图
3. 调用 `startCapture(...)` 启动采集
4. 在启动成功后调用 `publishLocalVideo(...)`

```kotlin
val cameraTrack = rtcEngine.getLocalCameraTrack(PreOptionCamera._720P)

// previewView 需为 SDK 支持的渲染控件类型
cameraTrack.addPlayView(previewView)

cameraTrack.startCapture(object : RTCResultListener {
    override fun onSuccess() {
        rtcEngine.publishLocalVideo(
            track = cameraTrack,
            publishCustomOpt = PublishCustomOptions(
                desc = TrackDesc.TRACK_MAIN.value,
                props = null,
                simulcasts = mutableListOf(
                    PublishCustomOptions(TrackDesc.TRACK_SUB.value, null, null)
                )
            ),
            listener = null
        )
    }

    override fun onFail(code: Int) {
        // 常见原因：未授予 CAMERA 权限
    }
})
```

常见补充操作：

- 切换前后摄像头：`cameraTrack.switchCameraPosition(...)`
- 特殊设备方向校正：`cameraTrack.setCameraAngleOffset(...)`

详细说明可参考 [LocalCameraTrack](/zh/rtc/android/api-reference/LocalCameraTrack)。

### 4.2 麦克风采集与发布

麦克风轨道获取后，可以直接调用 `publishLocalAudio(...)` 发布本地音频。

```kotlin
val micTrack = rtcEngine.getLocalMicTrack(PreOptionMic.def)

rtcEngine.publishLocalAudio(
    track = micTrack,
    publishCustomOpt = PublishCustomOptions(
        TrackDesc.TRACK_AUDIO.value,
        null,
        null
    ),
    listener = null
)

val micVolume = micTrack.getVolume()
```

其中：

- `TrackDesc.TRACK_AUDIO.value`：表示按音频轨道发布。
- `micTrack.getVolume()`：可用于显示当前本地麦克风音量。

详细说明可参考 [LocalMicTrack](/zh/rtc/android/api-reference/LocalMicTrack)。

### 4.3 屏幕共享（可选）

如果业务中需要共享屏幕，建议按下面顺序操作：

1. 获取 `LocalScreenTrack`
2. 设置 `RTCScreenStateEvent`
3. 调用 `request(...)` 拉起系统录屏授权
4. 在授权成功回调中调用 `startCapture(...)`
5. 再调用 `publishLocalVideo(...)` 发布屏幕轨道

```kotlin
val screenTrack = rtcEngine.getLocalScreenTrack(this, PreOptionScreen.def)

screenTrack.setEvent(object : RTCScreenStateEvent {
    override fun onScreenRecordStateChanged(state: ScreenRecordState, args: String?) {
        // 录屏状态变化，例如开始、停止、异常中断等
    }
})

screenTrack.request { granted, intent ->
    if (granted && intent != null) {
        screenTrack.startCapture(intent, hasBar = true)

        rtcEngine.publishLocalVideo(
            track = screenTrack,
            publishCustomOpt = PublishCustomOptions(
                TrackDesc.TRACK_SHARE.value,
                null,
                null
            ),
            listener = null
        )
    }
}
```

开始接入屏幕共享前，建议先确认 [集成](/zh/rtc/android/integration) 中提到的前台服务、Manifest 合并等注意事项。接口细节可参考：

- [LocalScreenTrack](/zh/rtc/android/api-reference/LocalScreenTrack)（含 `RTCScreenStateEvent` 回调说明）

## Step 5：订阅并播放远端媒体

推荐把远端视频处理拆成下面几个动作：

1. 在 `onStreamTrackAdd(...)` 中拿到 `uid`、`trackId`、`trackDesc`
2. 用 `getRemoteVideoTrack(uid, trackDesc)` 获取轨道对象
3. 先绑定远端渲染视图
4. 再调用 `subscribeRemoteTrack(uid, trackId, ...)` 发起订阅
5. 在 `onStreamTrackRemove(...)` 中取消订阅并移除渲染视图

```kotlin
override fun onStreamTrackAdd(uid: String, channel: String, trackId: String, trackDesc: String) {
    val remoteVideoTrack = rtcEngine.getRemoteVideoTrack(uid, trackDesc)
    remoteVideoTrack?.addPlayView(remoteView)

    // preferTrackIds 为大小流/联播候选层，最简用法传 null 即可
    rtcEngine.subscribeRemoteTrack(uid, trackId, null, object : RTCResultListener {
        override fun onSuccess() {
            // 订阅成功
        }

        override fun onFail(code: Int) {
            // 订阅失败
        }
    })
}

override fun onStreamTrackRemove(uid: String, channel: String, trackInfo: TrackInfo) {
    rtcEngine.unSubscribeRemoteTrack(uid, trackInfo.trackId)

    rtcEngine.getRemoteVideoTrack(uid, trackInfo.trackDesc)
        ?.removePlayView(remoteView)
}
```

如果你使用的是远端合成音频，也可以直接播放混音轨道：

```kotlin
rtcEngine.getRemoteAudioMixTrack()?.startPlay()
```

详细说明可参考：

- [RemoteVideoTrack](/zh/rtc/android/api-reference/RemoteVideoTrack)
- [RemoteAudioMixTrack](/zh/rtc/android/api-reference/RemoteAudioMixTrack)

## Step 6：查询信息、离开频道并释放资源

离会前后，业务层通常会读取当前频道信息、当前用户信息和成员列表；当页面销毁或应用不再使用 RTC 能力时，记得调用 `releaseSDK()`。

```kotlin
val channelInfo = rtcEngine.getChannelInfo()
val meInfo = rtcEngine.getMeInfo()
val users = rtcEngine.getUserInfos()

// 离开当前频道
rtcEngine.leave()

// 不再使用 RTC 能力时释放资源
rtcEngine.releaseSDK()
```

建议：

- 页面退出时先 `leave()`，再根据生命周期决定是否 `releaseSDK()`。
- 如果你还初始化了音频路由管理器，离会或销毁时也要同步释放，具体可参考 [音频路由使用](/zh/rtc/android/advanced/audio-routing)。

## 更多能力

本文只覆盖最小可跑通的主线能力。如果你还需要以下高级场景，可继续阅读对应文档：

- 自定义编码视频流： [CustomVideoTrack](/zh/rtc/android/api-reference/CustomVideoTrack)
- 观众身份与摄像头设备管理： [RTCEngine](/zh/rtc/android/api-reference/RTCEngine)（`isAudience` / `getCameraDevices`）
- 引擎完整接口： [RTCEngine](/zh/rtc/android/api-reference/RTCEngine)
- 音频输出设备管理： [音频路由使用](/zh/rtc/android/advanced/audio-routing)

