### version()
获取 RTC-SDK 版本号

```kotlin
fun version(): String
```

返回值

| RTC-SDK 版本信息 |
| --- |


### buildTime()
获取 RTC-SDK 构建时间信息

```kotlin
fun buildTime(): String
```

返回值 

| RTC-SDK 构建时间，精确到年月日 |
| --- |


## 初始化 SDK
### create()
用于创建实例

+ <font style="color:#DF2A3F;">PS：在这个方法中初始化了通用的能力，如日志模块。可以在应用刚启动的时候就执行这一步操作。</font>

```kotlin
fun create(
    app: Application, 
    enableLocalLog: Boolean,
    localLogPath: String? = null, 
    version: String = ""
)
```

参数

| app | application 上下文 |
| --- | --- |
| enableLocalLog | 是否允许存储本地日志 |
| localLogPath | 本地日志存储地址。不填会有默认值：Android\data\<包名>\files\logs |
| version | 上层版本信息。会在管理后台体现 |


### initSDK()
用于初始化 SDK

+ <font style="color:#DF2A3F;">PS：在这个方法中初始化了与 RTC 相关的能力。可以在适当的时机调用，但是必须调用。</font>

```kotlin
fun initSDK()
```

### releaseSDK()
用于释放 SDK

+ <font style="color:#DF2A3F;">PS：在这个方法中释放了与 RTC 相关的资源。</font>

```kotlin
fun releaseSDK()
```

## 参数配置
### setRtcClientEvent()
设置会控事件监听器

```kotlin
fun setRtcClientEvent(event: RTCClientEvent)
```

参数

| event | 会控事件监听器，详见 [RTCClientEvent](https://www.yuque.com/anyconf/rtcengine/vncb76) |
| --- | --- |


### setRtcMediaEvent()
设置流媒体事件监听器

```kotlin
fun setRtcMediaEvent(event: RTCMediaEvent)
```

参数

| event | 流媒体事件监听器，详见 [RTCMediaEvent](https://www.yuque.com/anyconf/rtcengine/hcv144) |
| --- | --- |


### setRtcImEvent()
设置即时通讯事件监听器

```kotlin
fun setRtcImEvent(e: RTCImEvent)
```

参数

| event | 即时通讯事件监听器，详见 [RTCImEvent](https://www.yuque.com/anyconf/rtcengine/rw76z9extiv1sbnd) |
| --- | --- |


### mediaOptions()
获取全局流媒体配置参数

```kotlin
fun mediaOptions():RTCMediaOptions
```

返回值

| 全局流媒体配置参数，详见“数据类型”中 [RTCMediaOptions](https://www.yuque.com/anyconf/rtcengine/linzbg) |
| --- |


### setMediaOptions()
设置全局流媒体配置参数，可以只配置需要修改的值，不需要修改的值置null。<font style="color:#DF2A3F;">如无特殊需求，不需要配置。</font>

```kotlin
fun setMediaOptions(options:RTCMediaOptions)
```

## 操作相关
### enableIm()
启动即时通讯

```kotlin
fun enableIm(token: String, resultListener: RTCResultListener?)
```

参数

| token | 授权token |
| --- | --- |
| RTCResultListener | 操作结果回调，其中包含onSuccess、onFail 接口 |


### disableIm()
关闭即时通讯

```kotlin
fun disableIm()
```

### startAsr()
开启语音转写

```kotlin
fun startAsr()
```

### stopAsr()
停止语音转写

```kotlin
fun stopAsr()
```

### isStartAsr()
获取语音转写是否开启

```kotlin
fun isStartAsr(): Boolean
```

### join()
加入频道，需要收到 onJoinSucceed 回调，才算加入频道成功

```kotlin
fun join(activity: Activity, token: String, resultListener: RTCResultListener?)
```

参数

| activity | activity 实例 |
| --- | --- |
| token | 包含加入 channel 所必要的信息，来源于后端加入会议的接口 |
| resultListener | 操作结果回调，其中包含onSuccess、onFail 接口 |


### leave()
离开频道

```kotlin
fun leave()
```

### resume()
恢复操作，一般用于移动端息屏后恢复时，立即发送一个心跳

```kotlin
fun resume()
```

### getAudioRouterManager()
获取音频路由管理类

```kotlin
fun getAudioRouterManager(): AudioRouterManager
```

返回值

| 音频路由管理类，详见 [AudioRouterManager](https://www.yuque.com/anyconf/rtcengine/aee6xrbwtbdapvtv) |
| --- |


### releaseAudioRouterManager()
释放音频路由相关资源

```kotlin
fun releaseAudioRouterManager()
```

### getLocalCameraTrack()
获取本地摄像头控制类

```kotlin
fun getLocalCameraTrack(preOpt: PreOptionCamera): LocalCameraTrack
```

参数

| preOpt | 预设参数，目前只有唯一值：PreOptionCamera.def |
| --- | --- |


返回值

| 本地摄像头流控制类，详见 [LocalCameraTrack](https://www.yuque.com/anyconf/rtcengine/oitcx8) |
| --- |


### getLocalMicTrack()
获取本地麦克风流控制类

```kotlin
fun getLocalMicTrack(preOpt: PreOptionMic): LocalMicTrack
```

参数

| preOpt | 预设参数，目前只有唯一值：PreOptionCamera.def |
| --- | --- |


返回值

| 本地麦克风流控制类，详见 [LocalMicTrack](https://www.yuque.com/anyconf/rtcengine/cvxzep) |
| --- |


### getLocalScreenTrack()
获取录屏流控制类

```kotlin
fun getLocalScreenTrack(activity: Activity, preOpt: PreOptionScreen): LocalScreenTrack
```

参数

| activity | activity 实例 |
| --- | --- |
| preOpt | 预设参数，目前只有唯一值：PreOptionScreen.def |


返回值

| 本地录屏流控制类，详见 [LocalScreenTrack](https://www.yuque.com/anyconf/rtcengine/buff33) |
| --- |


### getCustomVideoTrack()
获取自定义视频流控制类

```kotlin
fun getCustomVideoTrack(): CustomVideoTrack
```

返回值

| 自定义流控制类，详见 [CustomVideoTrack](https://www.yuque.com/anyconf/rtcengine/dz0lyh) |
| --- |


### getRemoteVideoTrack()
获取远端视频流控制类，可能为空，表示未找到指定的远端视频流控制类

```kotlin
fun getRemoteVideoTrack(uid: String, trackDesc: String): RemoteVideoTrack?
```

参数

| uid | 用户 id |
| --- | --- |
| trackDesc | 轨道描述 |


返回值

| 远端视频流控制类，详见 [RemoteVideoTrack](https://www.yuque.com/anyconf/rtcengine/zt5ybe) |
| --- |


### getRemoteMixtureTrack()
获取远端合成视频流控制类

```kotlin
fun getRemoteMixtureTrack(): RemoteVideoTrack?
```

返回值

| 远端视频流控制类，详见 [RemoteVideoTrack](https://www.yuque.com/anyconf/rtcengine/zt5ybe) |
| --- |


### getRemoteAudioMixTrack()
获取远端混音流控制类

```kotlin
fun getRemoteAudioMixTrack(): RemoteAudioMixTrack
```

返回值

| 远端混音流控制类，详见 [RemoteAudioMixTrack](https://www.yuque.com/anyconf/rtcengine/cqghwx) |
| --- |


### publishLocalVideo()
发布本地视频流

+ 可以通过 PublishCustomOptions 配置流描述，如果不配置 PublishCustomOptions，sdk 中会设置默认的流描述，详见枚举类型的 [TrackDesc](https://www.yuque.com/anyconf/rtcengine/co4luv4dhreapv0g)
+ 摄像头流可以通过 PublishCustomOptions 配置辅码流，但只能配置一条辅码流且辅码流不能嵌套配置辅码流。

```kotlin
fun publishLocalVideo(track: LocalVideoTrack, 
                      publishCustomOpt: PublishCustomOptions?, 
                      listener: RTCResultListener?)
```

参数

| track | 本地视频控制类。这是一个抽象类，具体实现包括：LocalCameraTrack、LocalScreenTrack |
| --- | --- |
| publishCustomOpt | 自定义发布参数。详见数据类型的 [PublishCustomOptions](https://www.yuque.com/anyconf/rtcengine/linzbg) |
| listener | 结果回调 |


### publishLocalAudio()
发布本地音频流

```kotlin
fun publishLocalAudio(track: LocalAudioTrack, 
                      publishCustomOpt: PublishCustomOptions?, 
                      listener: RTCResultListener?)
```

参数

| track | 本地音频控制类。这是一个抽象类，具体实现包括：LocalMicTrack |
| --- | --- |
| publishCustomOpt | 自定义发布参数。详见数据类型的 [PublishCustomOptions](https://www.yuque.com/anyconf/rtcengine/linzbg) |
| listener | 结果回调 |


### unPublishLocalVideo()
取消发布本地视频流

```kotlin
fun unPublishLocalVideo(track: LocalVideoTrack, listener: RTCResultListener?)
```

参数

| track | 本地视频控制类。这是一个抽象类，具体实现包括：LocalCameraTrack、LocalScreenTrack |
| --- | --- |
| listener | 结果回调 |


### unPublishLocalAudio()
取消发布本地音频流

```kotlin
fun unPublishLocalAudio(track: LocalAudioTrack, listener: RTCResultListener?)
```

参数

| track | 本地音频控制类。这是一个抽象类，具体实现包括：LocalMicTrack |
| --- | --- |
| listener | 结果回调 |


### subscribeRemoteTrack() 
订阅远端流

```kotlin
fun subscribeRemoteTrack(uid: String, trackId: String, listener: RTCResultListener?)
```

参数

| uid | 用户 id |
| --- | --- |
| trackId | 轨道 id |
| listener | 结果回调 |


### unSubscribeRemoteTrack()
取消订阅远端流

```kotlin
fun unSubscribeRemoteTrack(uid: String, trackId: String)
```

参数

| uid | 用户 id |
| --- | --- |
| trackId | 轨道id |


### subscribeRemoteMixture()
订阅合成视频流

```kotlin
fun subscribeRemoteMixture()
```

### unSubscribeRemoteMixture()
取消订阅合成视频流

```kotlin
fun unSubscribeRemoteMixture()
```

## 信息获取
### getChannelInfo()
获取频道信息

```kotlin
fun getChannelInfo(): ChannelInfo?
```

返回值

| 频道信息，详见“数据类型”中  [ChannelInfo](https://www.yuque.com/anyconf/rtcengine/linzbg) |
| --- |


### getMeInfo()
获取自己的用户信息

```kotlin
fun getMeInfo(): UserInfo?
```

返回值

| 自己的用户信息，详见“数据类型”中  [UserInfo](https://www.yuque.com/anyconf/rtcengine/linzbg) |
| --- |


### getUserInfos()
获取全部成员的用户信息，包括自己

```kotlin
fun getUserInfos(): MutableList<UserInfo>
```

返回值

| 所有成员信息的集合 |
| --- |


### getUserInfo()
获取指定 uid 的其他成员信息

```kotlin
fun getUserInfo(uid: String): UserInfo?
```

参数

| uid | 用户 id |
| --- | --- |


返回值

| 指定成员的用户信息，详见“数据类型”中  [UserInfo](https://www.yuque.com/anyconf/rtcengine/linzbg) |
| --- |


### getTrackInfos()
根据 uid 获取轨道信息列表

```kotlin
fun getTrackInfos(uid: String): List<TrackInfo>
```

参数

| uid | 用户 id |
| --- | --- |


返回值

| 指定成员的轨道信息集合 |
| --- |


### getTrackInfoByTrackDesc()
根据 uid、trackDes 获取 trackInfo

```kotlin
fun getTrackInfoByTrackDesc(uid: String, trackDesc: String): TrackInfo?
```

参数

| uid | 用户 id |
| --- | --- |
| trackDesc | 轨道描述 |


返回值

| 指定成员和轨道描述的轨道信息 |
| --- |


### getTrackInfoByTrackId()
根据 uid、trackId 获取 trackInfo

```kotlin
fun getTrackInfoByTrackId(uid: String, trackId: String): TrackInfo?
```

参数

| uid | 用户 id |
| --- | --- |
| trackId | 轨道id |


返回值

| 指定成员和轨道号的轨道信息 |
| --- |


