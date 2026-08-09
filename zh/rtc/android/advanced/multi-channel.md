---
title: "多频道"
description: "使用一个 RTCEngine 同时加入多个频道，并按频道隔离事件、发布订阅、成员状态和媒体统计"
---

Android SRTC SDK 支持一个 `RTCEngine` 在同一初始化周期内同时加入多个频道。每次 `join(...)` 返回一个 `RTCChannel` 句柄；本地摄像头、麦克风和屏幕采集由 Engine 共享，各频道的信令、流媒体会话、成员、远端轨道和统计相互独立。

## 对象与作用域

| 对象或能力 | 作用域 | 说明 |
| --- | --- | --- |
| `RTCEngine` | 应用 / SDK 初始化周期 | 管理 SDK 生命周期、IM、共享采集设备和所有频道。 |
| 第一条 `RTCChannel` | 默认频道 | `RTCEngine` 上的扁平频道接口会委托给它。 |
| 后续 `RTCChannel` | 单个额外频道 | 发布、订阅、查询、统计和离会都只影响该频道。 |
| 本地 Camera / Mic / Screen Track | Engine 共享 | 采集只需启动一次，同一 Track 可以发布到多个频道。 |
| `RTCClientEvent` / `RTCMediaEvent` | 单个频道 | 回调仍携带 `channel` 参数，便于复用监听器并校验归属。 |
| 设备事件、PCM / 本地视频帧事件 | Engine 全局 | 不会因加入多个频道而重复产生设备级回调。 |

:::note
第一条 `join` 是“默认频道”，不是第一个完成 `onJoinSucceed` 的频道。默认频道离开后，下一次新建的频道可以占用默认槽。多频道业务应始终保存并使用每次 `join` 返回的 `RTCChannel`，不要依赖扁平接口推断目标频道。
:::

## 接入流程

### 1. 创建 Engine

多频道只需要一个 `RTCEngine`：

```kotlin
val rtcEngine = RTCEngine.create(
    app = application,
    enableLocalLog = true,
    engineEvent = object : RTCEngineSimpleEvent() {
        override fun onError(channelId: String?, errorCode: Int, message: String?) {
            // channelId 有值时可路由到对应频道；null 表示 Engine 全局错误
        }
    }
)
rtcEngine.initSDK()
```

### 2. 启动共享采集

采集和频道发布相互独立。以下 Track 在 Engine 内共享，只启动一次：

```kotlin
val cameraTrack = rtcEngine.getLocalCameraTrack(PreOptionCamera._720P)
val micTrack = rtcEngine.getLocalMicTrack(PreOptionMic.def)

cameraTrack.startCapture(object : RTCResultListener {
    override fun onSuccess() {
        // 记录摄像头就绪
    }
    override fun onFail(code: Int) {
        // 处理摄像头启动失败
    }
})
micTrack.startCapture(object : RTCResultListener {
    override fun onSuccess() {
        // 记录麦克风就绪
    }
    override fun onFail(code: Int) {
        // 处理麦克风启动失败
    }
})
```

等待各自的 `RTCResultListener.onSuccess()` 后再发布。仅设置本地音频帧监听器不会打开麦克风；需要 PCM 时仍须调用 `micTrack.startCapture(...)`。

### 3. 为每个频道创建回调并加入

首次 `RTCClientEvent` 必须通过本次 `join(...)` 传入，因为加入成功或失败事件可能紧随其后发生。`RTCChannel.setRtcClientEvent(...)` 只用于入会成功后替换或解绑监听器。

```kotlin
private val channels = mutableMapOf<String, RTCChannel>()

private fun joinOneChannel(key: String, activity: Activity, token: String) {
    val clientEvent = object : RTCClientSimpleEvent() {
        override fun onJoinSucceed(channel: String, uid: String, whiteBoard: String?) {
            val rtcChannel = channels[key] ?: return

            // 同一份共享采集 Track，按频道分别发布
            rtcChannel.publishLocalVideo(
                cameraTrack,
                PublishCustomOptions(TrackDesc.TRACK_MAIN.value, null, null),
                null
            )
            rtcChannel.publishLocalAudio(
                micTrack,
                PublishCustomOptions(TrackDesc.TRACK_AUDIO.value, null, null),
                null
            )
        }

        override fun onJoinFailed(channel: String?, statusCode: Int) {
            channels.remove(key)
        }

        override fun onStreamTrackAdd(
            uid: String,
            channel: String,
            trackId: String,
            trackDesc: String
        ) {
            subscribeVideo(key, uid, trackId, trackDesc)
        }

        override fun onDisconnected(
            channel: String,
            leaveReason: LeaveReason,
            statusCode: Int,
            message: String
        ) {
            // 只清理 channel 对应的 UI 与业务状态
        }
    }

    val rtcChannel = rtcEngine.join(
        activity = activity,
        token = token,
        clientEvent = clientEvent,
        options = JoinOptions(autoSubscribeAudio = true, autoSubscribeVideo = false)
    ) ?: return

    channels[key] = rtcChannel
    rtcChannel.setRtcMediaEvent(object : RTCMediaSimpleEvent() {
        override fun onMediaConnected(channel: String) {
            // 当前频道媒体连接成功
        }

        override fun onMediaMetric(channel: String, metric: MediaMetric.Metric) {
            // 每个频道拥有独立统计快照
        }
    })
}
```

SDK 保证 `join(...)` 返回后才派发 `onJoinSucceed(...)`。非空句柄只代表请求已被接受；在收到成功回调前调用发布、订阅等频道操作会被 `CHANNEL_NOT_START` 阻断。

### 4. 按频道订阅与渲染

远端轨道必须从产生事件的同一个 `RTCChannel` 获取和订阅：

```kotlin
private fun subscribeVideo(
    key: String,
    uid: String,
    trackId: String,
    trackDesc: String
) {
    val rtcChannel = channels[key] ?: return
    val remoteTrack = rtcChannel.getRemoteVideoTrack(uid, trackDesc)
    remoteTrack?.addPlayView(remoteViewFor(key, uid, trackDesc))
    rtcChannel.subscribeRemoteTrack(uid, trackId, null, null)
}
```

不要拿频道 A 的 `uid` / `trackId` 到频道 B 的句柄上查询或订阅。即使字符串相同，两条频道 Session 中的成员、Track 和媒体状态也互不共享。

## 共享采集与频道发布

采集、发布和静音是三个不同层次：

| 操作 | 影响范围 | 典型用途 |
| --- | --- | --- |
| `track.startCapture(...)` / `stopCapture()` | 所有频道共享的数据源 | 打开或关闭物理设备。 |
| `channel.publishLocalAudio/Video(...)` | 当前频道 | 决定是否把共享采集数据送入该频道。 |
| `channel.enableLocalAudio(track, false)` | 当前频道的已发布音频 | 高频静音，不移除远端 Track。 |
| `channel.unPublishLocalAudio/Video(...)` | 当前频道 | 停止该频道发布，不关闭共享采集。 |

因此，频道 A 取消发布不会影响频道 B；但调用 `micTrack.stopCapture()` 或 `cameraTrack.stopCapture()` 会关闭共享数据源，所有仍在发布该 Track 的频道都将失去采集数据。

## 离开与释放

离开单个频道时调用对应句柄，不影响其他频道：

```kotlin
channels.remove("channel-a")?.leave()
```

全部结束时，先逐频道停止发布和离会，再关闭共享采集，最后释放 Engine：

```kotlin
channels.values.toList().forEach { channel ->
    channel.unPublishLocalAudio(micTrack, null)
    channel.unPublishLocalVideo(cameraTrack, null)
    channel.leave()
}
channels.clear()

micTrack.stopCapture()
cameraTrack.stopCapture()
rtcEngine.releaseSDK()
```

`releaseSDK()` 会兜底释放当前初始化周期中的全部频道和共享资源。需要再次使用时重新调用 `initSDK()`。

## 失败与错误处理

+ `join(...)` 返回 `null`：请求在频道 Session 创建前被拒绝，仍以本次 `onJoinFailed(...)` 的状态码为准。
+ 重复加入同一频道：`onJoinFailed(channel, RtcChannelErrorCode.CHANNEL_ALREADY_EXISTS)`（`102208`），已有频道和监听器不受影响。
+ SDK 未初始化或已释放：`join(...)` 同步抛出 `SdkNotInitializedException`。
+ 入会后的异步操作失败：通过各操作的 `RTCResultListener.onFail(code)` 返回。
+ Engine 阻断操作或全局错误：通过 `RTCEngineEvent.onError(channelId, errorCode, message)` 返回。
+ 频道断开与重连：通过带 `channel` 参数的 `onDisconnected`、`onReconnecting`、`onReconnected` 区分。

错误码归属和 `102xxx` 分域常量见 [错误码](/zh/rtc/android/error-codes)。完整频道接口见 [RTCChannel](/zh/rtc/android/api-reference/RTCChannel)。
