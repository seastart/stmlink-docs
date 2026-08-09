---
title: "RTCChannel"
description: "单个频道的操作句柄，隔离该频道的生命周期、事件、成员和 Track、发布订阅、ASR 与媒体统计"
---

`RTCChannel` 由 `RTCEngine.join(...)` 返回，所有方法只作用于该句柄绑定的频道 Session。第一条 `join` 返回默认频道句柄；`RTCEngine` 上保留的扁平频道接口与该句柄操作同一条 Session。

非空句柄只表示 SDK 已接受加入请求。发布、订阅和信息查询应等待 `RTCClientEvent.onJoinSucceed(...)` 后调用。

## 标识与生命周期

### channelId

```kotlin
val channelId: String?
```

频道 ID。token 可解析时可能在入会成功前可用，否则由成功回调填充；不能以非空值判断入会成功。

### leave()

```kotlin
fun leave()
```

离开并拆除当前频道，不影响其他频道和共享采集设备。

### resume()

```kotlin
fun resume()
```

应用从息屏等状态恢复后，立即触发当前频道的心跳检查。

## 监听器

```kotlin
fun setRtcClientEvent(e: RTCClientEvent?)
fun setRtcMediaEvent(e: RTCMediaEvent?)
```

+ `setRtcClientEvent`：入会成功后替换或解绑频道会控监听器。首次监听器必须传给 `join(...)`。
+ `setRtcMediaEvent`：替换或解绑当前频道媒体监听器；可在 `join(...)` 返回句柄后设置。

## 频道、成员与 Track 查询

```kotlin
fun getChannelInfo(): ChannelInfo?
fun getMeInfo(): UserInfo?
fun isAudience(): Boolean
fun getUserInfos(): MutableList<UserInfo>
fun getUserInfo(uid: String): UserInfo?
fun getTrackInfos(uid: String): List<TrackInfo>
fun getTrackInfoByTrackDesc(uid: String, trackDesc: String): TrackInfo?
fun getTrackInfoByTrackId(uid: String, trackId: String): TrackInfo?
```

这些查询只读取当前频道的数据。未入会或目标不存在时，可空方法返回 `null`，列表方法返回空列表；`isAudience()` 在未入会时返回 `false`。

## 发布本地 Track

```kotlin
fun publishLocalVideo(
    track: LocalVideoTrack,
    publishCustomOpt: PublishCustomOptions?,
    listener: RTCResultListener?
)

fun publishLocalAudio(
    track: LocalAudioTrack,
    publishCustomOpt: PublishCustomOptions?,
    listener: RTCResultListener?
)

fun unPublishLocalVideo(track: LocalVideoTrack, listener: RTCResultListener?)
fun unPublishLocalAudio(track: LocalAudioTrack, listener: RTCResultListener?)
fun enableLocalAudio(track: LocalAudioTrack, enable: Boolean): Boolean
```

本地 Track 由 `RTCEngine` 创建并共享，但发布状态按频道隔离。观众调用发布接口会失败并返回 `FORBIDDEN_FOR_AUDIENCE`。`enableLocalAudio` 只对当前频道已发布的音频进行低延迟启停，不关闭麦克风采集，也不移除远端 Track。

## 订阅远端 Track

```kotlin
fun getRemoteVideoTrack(uid: String, trackDesc: String): RemoteVideoTrack?
fun getRemoteStreamTrack(uid: String, trackDesc: String): RemoteVideoTrack?
fun getRemoteMixtureTrack(): RemoteVideoTrack?
fun getRemoteAudioMixTrack(): RemoteAudioMixTrack?

fun subscribeRemoteTrack(
    uid: String,
    trackId: String,
    preferTrackIds: MutableList<String>?,
    result: RTCResultListener?
)
fun unSubscribeRemoteTrack(uid: String, trackId: String)

fun subscribeRemoteStream(
    streamName: String,
    uid: String,
    trackDesc: String,
    kind: String?,
    result: RTCResultListener?
)
fun unSubscribeRemoteStream(
    streamName: String,
    uid: String,
    trackDesc: String,
    kind: String?
)

fun subscribeRemoteMixture()
fun unSubscribeRemoteMixture()
```

远端 Track、订阅 ID 和渲染对象必须来自同一个频道。`getRemoteStreamTrack` 与 `subscribeRemoteStream` 仅对网宿流媒体引擎有效；其他引擎返回 `STREAM_VENDOR_NOT_SUPPORTED` 或空结果。

## 统计与 ASR

```kotlin
fun getMetric(): MediaMetric.Metric?
fun startAsr()
fun stopAsr()
fun isStartAsr(): Boolean
```

每个频道拥有独立的媒体统计与 ASR 状态。`getMetric()` 返回最近一次线程安全快照，不主动触发底层统计采集。

完整多频道接入流程见 [多频道](/zh/rtc/android/advanced/multi-channel)。
