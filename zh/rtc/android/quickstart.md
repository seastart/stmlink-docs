---
title: "快速开始"
description: "Android SRTC 音视频 SDK 快速接入与基础流程"
---

### Step 1：创建并初始化 RTCEngine

```kotlin
val rtcEngine = RTCEngine.create(
    app = application,
    enableLocalLog = true,
    localLogPath = null,
    version = "app: ${BuildConfig.VERSION_NAME}"
)

rtcEngine.initSDK()
```

### Step 2：设置回调与媒体参数

```kotlin
rtcEngine.setRtcClientEvent(clientEvent)
rtcEngine.setRtcMediaEvent(mediaEvent)
rtcEngine.setRtcImEvent(imEvent)

// 可选：测试回调
rtcEngine.setRtcTestEvent(testEvent)

// 可选：全局媒体参数
rtcEngine.setMediaOptions(RTCMediaOptions())
```

### Step 3：加入/离开频道

```kotlin
val joinOptions = JoinOptions(
    autoSubscribeAudio = true,
    autoSubscribeVideo = true
)

rtcEngine.join(
    activity = this,
    token = token,
    options = joinOptions,
    resultListener = object : RTCResultListener {
        override fun onSuccess() {
            // join 请求发送成功，最终以 onJoinSucceed 回调为准
        }

        override fun onFail(code: Int) {
            // join 请求失败
        }
    }
)

// 离开频道
rtcEngine.leave()
```

### Step 4：本地采集与发布

#### 摄像头

```kotlin
val cameraTrack = rtcEngine.getLocalCameraTrack(PreOptionCamera._720P)
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

    override fun onFail(code: Int) {}
})
```

#### 麦克风

```kotlin
val micTrack = rtcEngine.getLocalMicTrack(PreOptionMic.def)

rtcEngine.publishLocalAudio(
    track = micTrack,
    publishCustomOpt = PublishCustomOptions(TrackDesc.TRACK_AUDIO.value, null, null),
    listener = null
)

val micVolume = micTrack.getVolume()
```

#### 屏幕共享

```kotlin
val screenTrack = rtcEngine.getLocalScreenTrack(this, PreOptionScreen.def)

screenTrack.setEvent(object : RTCScreenStateEvent {
    override fun onScreenRecordStateChanged(state: ScreenRecordState, args: String?) {
        // 录屏状态变化
    }
})

screenTrack.request { granted, intent ->
    if (granted && intent != null) {
        screenTrack.startCapture(intent, hasBar = true)
        rtcEngine.publishLocalVideo(
            track = screenTrack,
            publishCustomOpt = PublishCustomOptions(TrackDesc.TRACK_SHARE.value, null, null),
            listener = null
        )
    }
}
```

### Step 5：自定义视频流

SDK 提供两种方式：

1. `CustomVideoTrack`：推送已编码数据（如 H264/H265）。
2. `LocalCustomVideoTrack`：推送原始 YUV 帧到已发布轨道。

```kotlin
// 方式1：编码流
val encodedTrack = rtcEngine.getCustomVideoTrack()
encodedTrack?.startCustomVideo(customVideoOptions, null)
encodedTrack?.inputData(stamp, data, angle)

// 方式2：原始帧
val localCustomTrack = rtcEngine.getLocalCustomVideoTrack(PreOptionCustomVideo.def)
rtcEngine.publishLocalVideo(localCustomTrack, null, null)
localCustomTrack.inputData(yuv, width, height, strideY, strideU, strideV, rotation, stamp)
```

### Step 6：远端订阅与播放

```kotlin
val remoteVideoTrack = rtcEngine.getRemoteVideoTrack(uid, trackDesc)
remoteVideoTrack?.addPlayView(remoteView)

rtcEngine.subscribeRemoteTrack(uid, trackId, object : RTCResultListener {
    override fun onSuccess() {}
    override fun onFail(code: Int) {}
})

// 取消订阅
rtcEngine.unSubscribeRemoteTrack(uid, trackId)

// 合成音频播放
rtcEngine.getRemoteAudioMixTrack()?.startPlay()
```

### Step 7：查询信息与释放资源

```kotlin
val channelInfo = rtcEngine.getChannelInfo()
val meInfo = rtcEngine.getMeInfo()
val users = rtcEngine.getUserInfos()

rtcEngine.releaseSDK()
```
