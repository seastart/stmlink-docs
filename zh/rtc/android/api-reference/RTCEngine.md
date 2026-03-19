---
title: "RTCEngine"
description: "Android SRTC 音视频 SDK RTCEngine 接口参考"
---

## 静态方法

### version()
```kotlin
fun version(): String
```
方法说明：获取 SDK 版本号。  
参数说明：无。  
返回值说明：`String`，SDK 版本号。

### buildTime()
```kotlin
fun buildTime(): String
```
方法说明：获取 SDK 构建时间。  
参数说明：无。  
返回值说明：`String`，构建时间字符串。

### create(app, enableLocalLog, localLogPath, version)
```kotlin
fun create(
    app: Application,
    enableLocalLog: Boolean,
    localLogPath: String? = null,
    version: String = ""
): RTCEngine
```
方法说明：创建 `RTCEngine` 实例。  
参数说明：
- `app`：`Application`，应用上下文。
- `enableLocalLog`：`Boolean`，是否启用本地日志存储。
- `localLogPath`：`String?`，日志目录；`null` 时使用默认路径。
- `version`：`String`，上层应用版本标识（可用于日志/排障）。
返回值说明：`RTCEngine`，引擎实例。

## 生命周期

### initSDK()
```kotlin
fun initSDK()
```
方法说明：初始化 RTC SDK。  
参数说明：无。  
返回值说明：无（`Unit`）。

### releaseSDK()
```kotlin
fun releaseSDK()
```
方法说明：释放 RTC SDK 相关资源。  
参数说明：无。  
返回值说明：无（`Unit`）。

## IM 相关

### enableIm(token, resultListener)
```kotlin
fun enableIm(token: String, resultListener: RTCResultListener?)
```
方法说明：启动即时通讯能力。  
参数说明：
- `token`：`String`，IM/频道鉴权令牌。
- `resultListener`：`RTCResultListener?`，启动结果回调，可为 `null`。
返回值说明：无（`Unit`）。

### disableIm()
```kotlin
fun disableIm()
```
方法说明：关闭即时通讯能力。  
参数说明：无。  
返回值说明：无（`Unit`）。

## 语音转写相关

### startAsr()
```kotlin
fun startAsr()
```
方法说明：开启语音转写。  
参数说明：无。  
返回值说明：无（`Unit`）。

### stopAsr()
```kotlin
fun stopAsr()
```
方法说明：停止语音转写。  
参数说明：无。  
返回值说明：无（`Unit`）。

### isStartAsr()
```kotlin
fun isStartAsr(): Boolean
```
方法说明：查询语音转写当前是否开启。  
参数说明：无。  
返回值说明：`Boolean`，`true` 表示已开启。

## 频道相关

### join(activity, token, options, resultListener)
```kotlin
fun join(
    activity: Activity,
    token: String,
    options: JoinOptions? = null,
    resultListener: RTCResultListener?
)
```
方法说明：加入频道。  
参数说明：
- `activity`：`Activity`，当前页面上下文。
- `token`：`String`，包含入会必要信息的令牌。
- `options`：`JoinOptions?`，入会选项（如自动订阅音视频），可为 `null`。
- `resultListener`：`RTCResultListener?`，调用结果回调。
返回值说明：无（`Unit`）。

### leave()
```kotlin
fun leave()
```
方法说明：离开当前频道。  
参数说明：无。  
返回值说明：无（`Unit`）。

### resume()
```kotlin
fun resume()
```
方法说明：恢复操作（常用于息屏恢复后触发心跳）。  
参数说明：无。  
返回值说明：无（`Unit`）。

## 回调设置

### setRtcImEvent(e)
```kotlin
fun setRtcImEvent(e: RTCImEvent)
```
方法说明：设置 IM 事件监听器。  
参数说明：
- `e`：`RTCImEvent`，IM 回调实现。
返回值说明：无（`Unit`）。

### setRtcClientEvent(e)
```kotlin
fun setRtcClientEvent(e: RTCClientEvent)
```
方法说明：设置会控事件监听器。  
参数说明：
- `e`：`RTCClientEvent`，会控回调实现。
返回值说明：无（`Unit`）。

### setRtcMediaEvent(e)
```kotlin
fun setRtcMediaEvent(e: RTCMediaEvent)
```
方法说明：设置媒体事件监听器。  
参数说明：
- `e`：`RTCMediaEvent`，媒体回调实现。
返回值说明：无（`Unit`）。

### setRtcTestEvent(e)
```kotlin
fun setRtcTestEvent(e: RTCTestEvent)
```
方法说明：设置测试事件监听器。  
参数说明：
- `e`：`RTCTestEvent`，测试回调实现。
返回值说明：无（`Unit`）。

## 媒体配置

### mediaOptions()
```kotlin
fun mediaOptions(): RTCMediaOptions
```
方法说明：获取当前媒体配置。  
参数说明：无。  
返回值说明：`RTCMediaOptions`，当前生效的媒体参数。

### setMediaOptions(options)
```kotlin
fun setMediaOptions(options: RTCMediaOptions)
```
方法说明：设置媒体配置。  
参数说明：
- `options`：`RTCMediaOptions`，新的媒体参数。
返回值说明：无（`Unit`）。

## 音频路由

### getAudioRouterManager()
```kotlin
fun getAudioRouterManager(): AudioRouterManager
```
方法说明：获取音频路由管理器。  
参数说明：无。  
返回值说明：`AudioRouterManager`，路由管理实例。

### releaseAudioRouterManager()
```kotlin
fun releaseAudioRouterManager()
```
方法说明：释放音频路由相关资源。  
参数说明：无。  
返回值说明：无（`Unit`）。

## Track 获取

### getLocalCameraTrack(preOpt)
```kotlin
fun getLocalCameraTrack(preOpt: PreOptionCamera = PreOptionCamera._480P): LocalCameraTrack
```
方法说明：获取本地摄像头轨道控制器。  
参数说明：
- `preOpt`：`PreOptionCamera`，摄像头采集/发布预设。
返回值说明：`LocalCameraTrack`，本地摄像头轨道实例。

### getLocalScreenTrack(activity, preOpt)
```kotlin
fun getLocalScreenTrack(activity: Activity, preOpt: PreOptionScreen = PreOptionScreen.def): LocalScreenTrack
```
方法说明：获取本地屏幕共享轨道控制器。  
参数说明：
- `activity`：`Activity`，用于发起录屏权限请求。
- `preOpt`：`PreOptionScreen`，录屏采集/发布预设。
返回值说明：`LocalScreenTrack`，本地屏幕轨道实例。

### getLocalMicTrack(preOpt)
```kotlin
fun getLocalMicTrack(preOpt: PreOptionMic = PreOptionMic.def): LocalMicTrack
```
方法说明：获取本地麦克风轨道控制器。  
参数说明：
- `preOpt`：`PreOptionMic`，麦克风采集/发布预设。
返回值说明：`LocalMicTrack`，本地麦克风轨道实例。

### getCustomVideoTrack()
```kotlin
fun getCustomVideoTrack(): CustomVideoTrack?
```
方法说明：获取自定义编码视频轨道控制器。  
参数说明：无。  
返回值说明：`CustomVideoTrack?`，可能为 `null`。

### getLocalCustomVideoTrack(preOpt)
```kotlin
fun getLocalCustomVideoTrack(preOpt: PreOptionCustomVideo = PreOptionCustomVideo.def): LocalCustomVideoTrack
```
方法说明：获取本地自定义原始视频轨道控制器（向已发布轨道输入外部帧）。  
参数说明：
- `preOpt`：`PreOptionCustomVideo`，自定义视频预设。
返回值说明：`LocalCustomVideoTrack`，本地自定义轨道实例。

### getRemoteVideoTrack(uid, trackDesc)
```kotlin
fun getRemoteVideoTrack(uid: String, trackDesc: String): RemoteVideoTrack?
```
方法说明：按用户与轨道描述获取远端视频轨道。  
参数说明：
- `uid`：`String`，远端用户 ID。
- `trackDesc`：`String`，轨道描述（如 `camera_big` / `screen`）。
返回值说明：`RemoteVideoTrack?`，未找到时为 `null`。

### getRemoteMixtureTrack()
```kotlin
fun getRemoteMixtureTrack(): RemoteVideoTrack?
```
方法说明：获取远端合成视频轨道。  
参数说明：无。  
返回值说明：`RemoteVideoTrack?`，未找到时为 `null`。

### getRemoteAudioMixTrack()
```kotlin
fun getRemoteAudioMixTrack(): RemoteAudioMixTrack?
```
方法说明：获取远端混音轨道。  
参数说明：无。  
返回值说明：`RemoteAudioMixTrack?`，未找到时为 `null`。

## 发布与订阅

### publishLocalVideo(track, publishCustomOpt, listener)
```kotlin
fun publishLocalVideo(track: LocalVideoTrack, publishCustomOpt: PublishCustomOptions?, listener: RTCResultListener?)
```
方法说明：发布本地视频轨道。  
参数说明：
- `track`：`LocalVideoTrack`，本地视频轨道（摄像头/录屏/本地自定义）。
- `publishCustomOpt`：`PublishCustomOptions?`，发布自定义参数，可为 `null`。
- `listener`：`RTCResultListener?`，发布结果回调，可为 `null`。
返回值说明：无（`Unit`）。

### publishLocalAudio(track, publishCustomOpt, listener)
```kotlin
fun publishLocalAudio(track: LocalAudioTrack, publishCustomOpt: PublishCustomOptions?, listener: RTCResultListener?)
```
方法说明：发布本地音频轨道。  
参数说明：
- `track`：`LocalAudioTrack`，本地音频轨道。
- `publishCustomOpt`：`PublishCustomOptions?`，发布自定义参数，可为 `null`。
- `listener`：`RTCResultListener?`，发布结果回调，可为 `null`。
返回值说明：无（`Unit`）。

### unPublishLocalVideo(track, listener)
```kotlin
fun unPublishLocalVideo(track: LocalVideoTrack, listener: RTCResultListener?)
```
方法说明：取消发布本地视频轨道。  
参数说明：
- `track`：`LocalVideoTrack`，目标视频轨道。
- `listener`：`RTCResultListener?`，取消发布结果回调，可为 `null`。
返回值说明：无（`Unit`）。

### unPublishLocalAudio(track, listener)
```kotlin
fun unPublishLocalAudio(track: LocalAudioTrack, listener: RTCResultListener?)
```
方法说明：取消发布本地音频轨道。  
参数说明：
- `track`：`LocalAudioTrack`，目标音频轨道。
- `listener`：`RTCResultListener?`，取消发布结果回调，可为 `null`。
返回值说明：无（`Unit`）。

### subscribeRemoteTrack(uid, trackId, result)
```kotlin
fun subscribeRemoteTrack(uid: String, trackId: String, result: RTCResultListener?)
```
方法说明：订阅指定远端视频轨道。  
参数说明：
- `uid`：`String`，远端用户 ID。
- `trackId`：`String`，远端轨道 ID。
- `result`：`RTCResultListener?`，订阅结果回调，可为 `null`。
返回值说明：无（`Unit`）。

### unSubscribeRemoteTrack(uid, trackId)
```kotlin
fun unSubscribeRemoteTrack(uid: String, trackId: String)
```
方法说明：取消订阅指定远端视频轨道。  
参数说明：
- `uid`：`String`，远端用户 ID。
- `trackId`：`String`，远端轨道 ID。
返回值说明：无（`Unit`）。

### subscribeRemoteMixture()
```kotlin
fun subscribeRemoteMixture()
```
方法说明：订阅远端合成视频轨道。  
参数说明：无。  
返回值说明：无（`Unit`）。

### unSubscribeRemoteMixture()
```kotlin
fun unSubscribeRemoteMixture()
```
方法说明：取消订阅远端合成视频轨道。  
参数说明：无。  
返回值说明：无（`Unit`）。

## 信息查询

### getChannelInfo()
```kotlin
fun getChannelInfo(): ChannelInfo?
```
方法说明：获取当前频道信息。  
参数说明：无。  
返回值说明：`ChannelInfo?`，未入会或无数据时可能为 `null`。

### getMeInfo()
```kotlin
fun getMeInfo(): UserInfo?
```
方法说明：获取当前用户信息。  
参数说明：无。  
返回值说明：`UserInfo?`，未入会或无数据时可能为 `null`。

### getUserInfos()
```kotlin
fun getUserInfos(): MutableList<UserInfo>
```
方法说明：获取频道内全部成员信息（含自己）。  
参数说明：无。  
返回值说明：`MutableList<UserInfo>`，成员列表。

### getUserInfo(uid)
```kotlin
fun getUserInfo(uid: String): UserInfo?
```
方法说明：按用户 ID 获取成员信息。  
参数说明：
- `uid`：`String`，目标用户 ID。
返回值说明：`UserInfo?`，未找到时为 `null`。

### getTrackInfos(uid)
```kotlin
fun getTrackInfos(uid: String): List<TrackInfo>
```
方法说明：获取指定用户的轨道列表。  
参数说明：
- `uid`：`String`，目标用户 ID。
返回值说明：`List<TrackInfo>`，轨道信息列表。

### getTrackInfoByTrackDesc(uid, trackDesc)
```kotlin
fun getTrackInfoByTrackDesc(uid: String, trackDesc: String): TrackInfo?
```
方法说明：按用户 ID + 轨道描述获取轨道信息。  
参数说明：
- `uid`：`String`，目标用户 ID。
- `trackDesc`：`String`，轨道描述。
返回值说明：`TrackInfo?`，未找到时为 `null`。

### getTrackInfoByTrackId(uid, trackId)
```kotlin
fun getTrackInfoByTrackId(uid: String, trackId: String): TrackInfo?
```
方法说明：按用户 ID + 轨道 ID 获取轨道信息。  
参数说明：
- `uid`：`String`，目标用户 ID。
- `trackId`：`String`，轨道 ID。
返回值说明：`TrackInfo?`，未找到时为 `null`。
