---
title: "RTCEngine"
description: "Android 音视频 SDK 的核心入口：生命周期、频道进出、媒体采集发布订阅、信息查询"
---

`RTCEngine` 是 Android SRTC SDK 的核心入口，负责 SDK 生命周期、频道进出、事件监听、媒体采集/发布/订阅以及信息查询。完整最小接入流程见 [快速开始](/zh/rtc/android/quickstart)。

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

### create(app, enableLocalLog, engineEvent, localLogPath, version)
```kotlin
fun create(
    app: Application,
    enableLocalLog: Boolean,
    engineEvent: RTCEngineEvent,
    localLogPath: String? = null,
    version: String = ""
): RTCEngine
```
方法说明：创建 `RTCEngine` 实例。  
参数说明：
- `app`：`Application`，应用上下文。
- `enableLocalLog`：`Boolean`，是否启用本地日志存储。
- `engineEvent`：`RTCEngineEvent`，与 Engine 同生命周期的错误监听器，参见 [RTCEngineEvent](/zh/rtc/android/api-reference/RTCEngineEvent)。
- `localLogPath`：`String?`，日志目录；`null` 时使用默认路径。
- `version`：`String`，上层应用版本标识（可用于日志/排障）。

返回值说明：`RTCEngine`，引擎实例。

## 生命周期

### initSDK()
```kotlin
fun initSDK()
```
方法说明：初始化 RTC SDK。调用任何频道、采集、发布、订阅接口前必须先调用。  
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

### join(activity, token, clientEvent, options)
```kotlin
fun join(
    activity: Activity,
    token: String,
    clientEvent: RTCClientEvent,
    options: JoinOptions? = null
): RTCChannel?
```
方法说明：加入一条频道并返回该频道的操作句柄。第一条频道同时成为默认频道，`RTCEngine` 上的扁平频道接口会委托给它；后续频道使用各自返回的 [`RTCChannel`](/zh/rtc/android/api-reference/RTCChannel)。
参数说明：
- `activity`：`Activity`，当前页面上下文。
- `token`：`String`，包含入会必要信息的令牌。
- `clientEvent`：`RTCClientEvent`，本频道的首次会控监听器；入会结果通过 `onJoinSucceed` / `onJoinFailed` 返回。
- `options`：`JoinOptions?`，自动订阅配置，可设置 `autoSubscribeAudio` 与 `autoSubscribeVideo`。

返回值说明：`RTCChannel?`。非空仅表示 SDK 已接受请求并创建 Session，不代表入会成功；请求在创建前被拒绝时返回 `null`，失败原因仍通过本次 `clientEvent.onJoinFailed(...)` 返回。SDK 未初始化或已释放时同步抛出 `SdkNotInitializedException`。

> 重复加入相同频道会返回 `null`，并以 `RtcChannelErrorCode.CHANNEL_ALREADY_EXISTS`（`102208`）回调失败；已有频道与监听器保持不变。完整多频道流程见 [多频道](/zh/rtc/android/advanced/multi-channel)。

### leave()
```kotlin
fun leave()
```
方法说明：离开默认频道。额外频道应调用对应 `RTCChannel.leave()`。
参数说明：无。  
返回值说明：无（`Unit`）。

### resume()
```kotlin
fun resume()
```
方法说明：恢复操作（常用于息屏恢复后立即发送一次心跳）。  
参数说明：无。  
返回值说明：无（`Unit`）。

### isAudience()
```kotlin
fun isAudience(): Boolean
```
方法说明：查询当前是否为观众身份。观众可订阅远端、可本地采集（摄像头/麦克风/屏幕），但**不可发布本地流**。以底层缓存的自己信息 `is_audience` 为准；未入会时返回 `false`。  
参数说明：无。  
返回值说明：`Boolean`，`true` 表示当前为观众。

> 入会后的初始身份用本方法读取；身份在会中发生变化时，由 [`RTCClientEvent.onMeMembershipChanged`](/zh/rtc/android/api-reference/RTCClientEvent) 通知。

## 回调设置

### setRtcImEvent(e)
```kotlin
fun setRtcImEvent(e: RTCImEvent)
```
方法说明：设置 IM 事件监听器。  
参数说明：
- `e`：`RTCImEvent`，IM 回调实现。参见 [RTCImEvent](/zh/rtc/android/api-reference/RTCImEvent)。

返回值说明：无（`Unit`）。

### setRtcMediaEvent(e)
```kotlin
fun setRtcMediaEvent(e: RTCMediaEvent)
```
方法说明：设置默认频道媒体事件监听器。额外频道使用 `RTCChannel.setRtcMediaEvent(...)`。
参数说明：
- `e`：`RTCMediaEvent`，媒体回调实现。参见 [RTCMediaEvent](/zh/rtc/android/api-reference/RTCMediaEvent)。

返回值说明：无（`Unit`）。

### setRtcCameraDeviceEvent(e)

```kotlin
fun setRtcCameraDeviceEvent(e: RTCCameraDeviceEvent?)
```

方法说明：设置 Engine 全局摄像头设备监听器，传 `null` 解绑。摄像头采集由所有频道共享，因此事件不携带频道 ID，也不会因多频道而重复回调。详见 [RTCCameraDeviceEvent](/zh/rtc/android/api-reference/RTCCameraDeviceEvent)。

### setRtcLocalVideoFrameEvent(e)
```kotlin
fun setRtcLocalVideoFrameEvent(e: RTCLocalVideoFrameEvent?)
```
方法说明：设置本地视频帧外部回调。仅用于应用层显式获取本地视频帧数据（例如做本地美颜、二次处理或自绘预览），SDK 内部预览渲染不依赖该接口。传 `null` 可移除回调。  
参数说明：
- `e`：`RTCLocalVideoFrameEvent?`，本地视频帧回调实现；`null` 表示移除。

返回值说明：无（`Unit`）。

`RTCLocalVideoFrameEvent` 接口方法：

```kotlin
interface RTCLocalVideoFrameEvent {
    fun onLocalVideoFrame(yuv: ByteArray?, width: Int, height: Int, stamp: Long, format: Int, facing: Int)
    fun onLocalVideoFrameSizeChanged(width: Int, height: Int, facing: Int)
}
```

- `onLocalVideoFrame`：回调一帧本地视频。`yuv` 为 SDK 为外部应用单独拷贝的数据，应用层可自行缓存或处理；`stamp` 为帧时间戳；`format` 为帧格式；`facing` 为摄像头朝向。
- `onLocalVideoFrameSizeChanged`：本地视频帧尺寸或摄像头方向发生变化时回调。

### setRtcLocalScreenFrameEvent(e)
```kotlin
fun setRtcLocalScreenFrameEvent(e: RTCLocalScreenFrameEvent?)
```
方法说明：设置 Engine 级本地屏幕 I420 帧回调。同一次共享采集发布到多个频道时只回调一份数据；未设置监听器时不会为应用复制 YUV 数据。传 `null` 可移除回调。OOK 的屏幕采集由厂商内部管理，不支持该原始帧回调。

参数说明：
- `e`：`RTCLocalScreenFrameEvent?`，本地屏幕帧回调实现；`null` 表示移除。

返回值说明：无（`Unit`）。

`RTCLocalScreenFrameEvent` 接口方法：

```kotlin
interface RTCLocalScreenFrameEvent {
    fun onLocalScreenFrame(
        yuv: ByteArray,
        width: Int,
        height: Int,
        stamp: Long,
        format: Int,
        rotation: Int
    )
}
```

- `yuv`：紧凑排列的 I420 数据，顺序为 Y、U、V。SDK 已创建独立副本，回调返回后应用仍可缓存或异步处理。
- `width` / `height`：实际分发帧的宽高。
- `stamp`：基于单调时钟的纳秒时间戳。
- `format`：视频格式，当前固定为 `VCS_EVENT_TYPE.YUVI420`。
- `rotation`：顺时针旋转角度，取值为 `0`、`90`、`180` 或 `270`。

回调在屏幕采集线程同步执行，应用不应阻塞。单应用目标不可见时可能收到黑帧，静态页面可能收到最近真实帧的保活重放帧，与实际发送链路保持一致。

### setRtcLocalAudioFrameEvent(e)

```kotlin
fun setRtcLocalAudioFrameEvent(e: RTCLocalAudioFrameEvent?)
```

方法说明：设置共享麦克风采集的本地 PCM 回调，传 `null` 解绑。注册监听器不会自动打开麦克风；必须调用 `LocalMicTrack.startCapture(...)`。详见 [RTCLocalAudioFrameEvent](/zh/rtc/android/api-reference/RTCLocalAudioFrameEvent)。

### setRtcMicDeviceEvent(e)

```kotlin
fun setRtcMicDeviceEvent(e: RTCMicDeviceEvent?)
```

方法说明：设置 Engine 全局麦克风输入设备监听器，传 `null` 解绑。详见 [RTCMicDeviceEvent](/zh/rtc/android/api-reference/RTCMicDeviceEvent)。

## 媒体质量

### getMetric()
```kotlin
fun getMetric(): MediaMetric.Metric?
```
方法说明：主动获取默认频道最近一次采集到的媒体质量快照（含 `qualityReport`）。返回线程安全副本，不触发底层 `getStats`；采样周期约 5 秒，起播初期可能为 `null`。额外频道使用 `RTCChannel.getMetric()`；弱网档位变化请优先监听 [`RTCMediaEvent.onNetworkQualityChanged`](/zh/rtc/android/api-reference/RTCMediaEvent)。
参数说明：无。  
返回值说明：`MediaMetric.Metric?`，最近一次质量快照；尚无数据时为 `null`。字段参见 [媒体质量](/zh/rtc/android/media-quality)，获取方式与弱网处理见 [网络质量](/zh/rtc/android/network-quality)。

## 音频路由

### getAudioRouterManager()
```kotlin
fun getAudioRouterManager(): AudioRouterManager
```
方法说明：获取音频路由管理器（单例）。  
参数说明：无。  
返回值说明：`AudioRouterManager`，路由管理实例。详见 [AudioRouterManager](/zh/rtc/android/api-reference/AudioRouterManager) 与 [音频路由使用](/zh/rtc/android/advanced/audio-routing)。

### releaseAudioRouterManager()
```kotlin
fun releaseAudioRouterManager()
```
方法说明：释放音频路由相关资源（内部调用 `release(true)`，恢复系统音频模式并切回扬声器）。  
参数说明：无。  
返回值说明：无（`Unit`）。

## 设备能力

### getCameraDevices()
```kotlin
fun getCameraDevices(): List<CameraDeviceCapability>
```
方法说明：获取当前系统可用的摄像头设备能力列表（Camera2）。返回列表中的 `cameraId` 可用于 [`LocalCameraTrack.switchCameraDevice`](/zh/rtc/android/api-reference/LocalCameraTrack) 精确切换摄像头。  
参数说明：无。  
返回值说明：`List<CameraDeviceCapability>`，无可用设备时返回空列表。类型定义见 [类型定义](/zh/rtc/android/types)。

> 摄像头设备的动态变化通过 [`RTCCameraDeviceEvent`](/zh/rtc/android/api-reference/RTCCameraDeviceEvent) 通知。

### getMicDevices()

```kotlin
fun getMicDevices(): List<MicDeviceCapability>
```

方法说明：获取当前系统可用的麦克风输入设备能力列表。返回值字段见 [类型定义](/zh/rtc/android/types)。

### switchMicDevice(deviceId)

```kotlin
fun switchMicDevice(deviceId: String)
```

方法说明：切换共享麦克风采集使用的输入设备。`deviceId` 来自 `getMicDevices()`，只在本次设备连接期间有效；采集中切换会重建录音链路。也可以通过 `LocalMicTrack` 上的同名方法操作。

## Track 获取

### getLocalCameraTrack(preOpt)
```kotlin
fun getLocalCameraTrack(preOpt: PreOptionCamera = PreOptionCamera._480P): LocalCameraTrack
```
方法说明：获取本地摄像头轨道控制器。  
参数说明：
- `preOpt`：`PreOptionCamera`，摄像头采集/发布预设，默认 `_480P`。参见 [摄像头预设](/zh/rtc/android/presets/camera)。

返回值说明：`LocalCameraTrack`，本地摄像头轨道实例。

### getLocalScreenTrack(activity, preOpt)
```kotlin
fun getLocalScreenTrack(activity: Activity, preOpt: PreOptionScreen = PreOptionScreen.def): LocalScreenTrack
```
方法说明：获取本地屏幕共享轨道控制器。  
参数说明：
- `activity`：`Activity`，用于发起录屏权限请求。
- `preOpt`：`PreOptionScreen`，录屏采集/发布预设。参见 [屏幕共享预设](/zh/rtc/android/presets/screen-sharing)。

返回值说明：`LocalScreenTrack`，本地屏幕轨道实例。

### getLocalMicTrack(preOpt)
```kotlin
fun getLocalMicTrack(preOpt: PreOptionMic = PreOptionMic.def): LocalMicTrack
```
方法说明：获取本地麦克风轨道控制器。  
参数说明：
- `preOpt`：`PreOptionMic`，麦克风采集/发布预设。参见 [麦克风预设](/zh/rtc/android/presets/microphone)。

返回值说明：`LocalMicTrack`，本地麦克风轨道实例。获取轨道不会自动打开麦克风；必须调用 [`LocalMicTrack.startCapture(...)`](/zh/rtc/android/api-reference/LocalMicTrack) 后再发布。

### getLocalCustomVideoTrack(preOpt)
```kotlin
fun getLocalCustomVideoTrack(preOpt: PreOptionCustomVideo = PreOptionCustomVideo.def): LocalCustomVideoTrack
```
方法说明：获取本地自定义视频轨道控制器，用于向已发布轨道推送外部**原始 YUV 帧**（白板、画布、播放器画面等）。轨道实例在 SDK 内按单例缓存，重复调用返回同一实例并用传入的 `preOpt` 覆盖旧值。  
参数说明：
- `preOpt`：`PreOptionCustomVideo`，自定义视频采集/发布预设，默认 `PreOptionCustomVideo.def`（轨道描述 `custom`）；以屏幕共享描述发布时用 `PreOptionCustomVideo.screen`。参见 [自定义视频流预设](/zh/rtc/android/presets/custom-video)。

返回值说明：`LocalCustomVideoTrack`，本地自定义视频轨道实例。参见 [LocalCustomVideoTrack](/zh/rtc/android/api-reference/LocalCustomVideoTrack)。

> 完整接入流程见 [自定义推流](/zh/rtc/android/advanced/custom-track)。

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
返回值说明：`RemoteAudioMixTrack?`，未找到时为 `null`。参见 [RemoteAudioMixTrack](/zh/rtc/android/api-reference/RemoteAudioMixTrack)。

## 发布与订阅

### publishLocalVideo(track, publishCustomOpt, listener)
```kotlin
fun publishLocalVideo(track: LocalVideoTrack, publishCustomOpt: PublishCustomOptions?, listener: RTCResultListener?)
```
方法说明：发布本地视频轨道。  
参数说明：
- `track`：`LocalVideoTrack`，本地视频轨道（摄像头 [`LocalCameraTrack`](/zh/rtc/android/api-reference/LocalCameraTrack) / 录屏 [`LocalScreenTrack`](/zh/rtc/android/api-reference/LocalScreenTrack) / 本地自定义 [`LocalCustomVideoTrack`](/zh/rtc/android/api-reference/LocalCustomVideoTrack)）。传入其他类型时通过 `listener.onFail` 返回 `RtcChannelErrorCode.TRACK_TYPE_INVALID`（`102002`，参见 [错误码](/zh/rtc/android/error-codes)）。
- `publishCustomOpt`：`PublishCustomOptions?`，发布自定义参数，可为 `null`。参见 [摄像头预设](/zh/rtc/android/presets/camera)。
- `listener`：`RTCResultListener?`，发布结果回调，可为 `null`。

返回值说明：无（`Unit`）。

> **注意**：摄像头推流采用声明式对账，快速连续 `publish`/`unpublish` 时，中间被后续操作合并的调用可能不回调；请以最后一次调用的回调或最终状态为准，不要假设“每次调用必有一次回调”。

### publishLocalAudio(track, publishCustomOpt, listener)
```kotlin
fun publishLocalAudio(track: LocalAudioTrack, publishCustomOpt: PublishCustomOptions?, listener: RTCResultListener?)
```
方法说明：把已经采集的本地音频轨道发布到默认频道。该接口不会自动启动麦克风采集；应先调用 `LocalMicTrack.startCapture(...)`。
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

> **注意**：同 `publishLocalVideo`，快速连续操作时中间被合并的调用可能不回调，以最后一次为准。

### unPublishLocalAudio(track, listener)
```kotlin
fun unPublishLocalAudio(track: LocalAudioTrack, listener: RTCResultListener?)
```
方法说明：取消默认频道中的本地音频发布，不会停止共享麦克风采集；不再需要采集时还应调用 `LocalMicTrack.stopCapture()`。
参数说明：
- `track`：`LocalAudioTrack`，目标音频轨道。
- `listener`：`RTCResultListener?`，取消发布结果回调，可为 `null`。

返回值说明：无（`Unit`）。

### subscribeRemoteTrack(uid, trackId, preferTrackIds, result)
```kotlin
fun subscribeRemoteTrack(
    uid: String,
    trackId: String,
    preferTrackIds: MutableList<String>?,
    result: RTCResultListener?
)
```
方法说明：订阅指定远端视频轨道。  
参数说明：
- `uid`：`String`，远端用户 ID。
- `trackId`：`String`，目标（默认）远端轨道 ID。
- `preferTrackIds`：`MutableList<String>?`，候选层列表，用于大小流/联播场景下声明可接受的多路轨道优先级。传 `null` 时按仅订阅 `trackId` 处理；若传入列表中不含 `trackId`，SDK 会自动将其插入到列表首位。
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

## 网宿通用流（高级 / 特定引擎）

> ⚠️ **仅网宿引擎可用**：以下接口**仅在网宿（Wangsu）流媒体引擎下有效**，用于按上层直接给定的流名订阅一路“通用流”，属于特定接入场景的高级能力。在非网宿引擎下调用：`getRemoteStreamTrack` 返回 `null`，`subscribeRemoteStream` 通过 `result.onFail` 返回不支持错误，`unSubscribeRemoteStream` 直接忽略。一般接入方无需使用本组接口。

### getRemoteStreamTrack(uid, trackDesc)
```kotlin
fun getRemoteStreamTrack(uid: String, trackDesc: String): RemoteVideoTrack?
```
方法说明：获取网宿通用流的视频流控制类（用于 `addPlayView` 渲染）。不依赖房间成员，按订阅时传入的 `(uid, trackDesc)` 获取；可在 `subscribeRemoteStream` 之前调用——先获取控制类并 `addPlayView`，再订阅，画面到达后即渲染。  
参数说明：
- `uid`：`String`，渲染路由标识（上层自定义；可与流名相同）。
- `trackDesc`：`String`，特殊流标识，用于渲染绑定与区分多路通用流。

返回值说明：`RemoteVideoTrack?`，非网宿引擎或频道未启动时为 `null`。

### subscribeRemoteStream(streamName, uid, trackDesc, kind, result)
```kotlin
fun subscribeRemoteStream(
    streamName: String,
    uid: String,
    trackDesc: String,
    kind: String?,
    result: RTCResultListener?
)
```
方法说明：订阅一路网宿通用流（流名由上层直接给定，如 `"rtc_v_lesson_fknqb"`）。  
参数说明：
- `streamName`：`String`，完整流名，直接用于网宿 HTTP 请求。
- `uid`：`String`，渲染路由标识（上层自定义；可与 `streamName` 相同）。
- `trackDesc`：`String`，特殊流标识，用于渲染绑定与区分多路通用流。
- `kind`：`String?`，可选，`"video"` / `"audio"`；为空时按流名前缀推断（`rtc_v` → video，`rtc_a` → audio）。
- `result`：`RTCResultListener?`，订阅结果回调，可为 `null`。

返回值说明：无（`Unit`）。

### unSubscribeRemoteStream(streamName, uid, trackDesc, kind)
```kotlin
fun unSubscribeRemoteStream(streamName: String, uid: String, trackDesc: String, kind: String?)
```
方法说明：取消订阅网宿通用流。  
参数说明：
- `streamName`：`String`，订阅时传入的完整流名。
- `uid`：`String`，订阅时传入的渲染路由标识。
- `trackDesc`：`String`，订阅时传入的特殊流标识。
- `kind`：`String?`，可选，`"video"` / `"audio"`；为空时按流名前缀推断。

返回值说明：无（`Unit`）。

## 信息查询

### getChannelInfo()
```kotlin
fun getChannelInfo(): ChannelInfo?
```
方法说明：获取当前频道信息。  
参数说明：无。  
返回值说明：`ChannelInfo?`，未入会或无数据时可能为 `null`。参见 [类型定义](/zh/rtc/android/types)。

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

## 通用回调结果类型

多数异步接口通过 `RTCResultListener` 返回调用结果。

### RTCResultListener
```java
public interface RTCResultListener {
    void onSuccess();
    void onFail(int code);
}
```
- `onSuccess()`：调用成功。
- `onFail(int code)`：调用失败，`code` 为错误码，参见 [错误码](/zh/rtc/android/error-codes)。

### RTCValueResultListener\<T\>
```kotlin
interface RTCValueResultListener<T> {
    fun onSuccess(t: T)
    fun onFail(code: Int)
}
```
- `onSuccess(t)`：调用成功并返回结果对象 `t`。
- `onFail(code)`：调用失败，`code` 为错误码。

`RTCResultListener2<T>` 已更名为 `RTCValueResultListener<T>`，除类型名外方法签名不变。
