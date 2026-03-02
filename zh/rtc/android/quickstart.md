### step 1: 初始化SDK
#### 创建 rtcEngine
+ 此操作建议在应用启动时执行，会在创建 rtcEngine 时初始化一些基础功能模块，例如日志模块

```kotlin
// 创建 rtcEngine
rtcEngine = RTCEngine.create(
    app, enableLocalLog, localLogPath, 
    "app: ${BuildConfig.VERSION_NAME}"
)
```

#### 初始化 sdk
```kotlin
// 初始化与 rtc 相关的功能
rtcEngine?.initSDK()
```

#### 设置回调
```kotlin
// 设置会控监听事件
rtcEngine.setRtcClientEvent(this)
// 设置流媒体监听事件
rtcEngine.setRtcMediaEvent(this)
```

#### 配置流媒体参数，<font style="color:#DF2A3F;">若无特殊需求，不必配置</font>
```kotlin
//RTCMediaOptions 在入会前配置流媒体全局参数，没有特殊需要可以不调用
rtcEngine.setMediaOptions(RTCMediaOptions())
```

### step 2：加入和离开频道
#### 加入频道
```kotlin
// 加入频道
rtcEngine.join(activity, token, object : RTCResultListener {
    override fun onSuccess() {
        Log.i(TAG, "join--onSuccess: ")
    }

    override fun onFail(code: Int) {
        Log.i(TAG, "join--onFail: code = $code")
    }
})

// 等待回调 RTCClientEvent 中的 onJoinSucceed 
override fun onJoinSucceed(channel: String, uid: String, whiteBoard: String?)
```

#### 离开频道
```kotlin
// 离开频道
rtcEngine.leave()
```

### step 3：流控制
#### 摄像头流控制
<font style="color:#E8323C;">注意：控制实例可以在初始化后就获取，但是采集和发布方法必须等加入房间后再调用</font>

+ 摄像头主码流、辅码流控制

```kotlin
// 获取摄像头控制实例, 需要传入预设参数，目前有四组：1080P、720P、480P、180P
val camearTrack = rtcEngine.getLocalCameraTrack(PreOptionCamera._1080P)

// 添加渲染控件
cameraTrack.addPlayView(vcsPlayerGlTextureView)
// 替换渲染控件
cameraTrack.replacePlayView(vcsPlayerGlTextureViewList)
// 移除渲染控件
cameraTrack.removePlayView(vcsPlayerGlTextureView)
// 移除所有渲染控件
cameraTrack.removeAllPlayView()

// 开始采集
cameraTrack.startCapture(object : RTCResultListener {
	override fun onSuccess() {
		TODO("Not yet implemented")
	}

	override fun onFail(code: Int) {
		TODO("Not yet implemented")
	}
})

// 停止采集
cameraTrack.stopCapture()

// 切换前后摄像头
cameraTrack.switchCameraPosition(
    if (isFrontCamera) {
        CameraCaptureOptions.CamraPosition.FRONT
    } else {
        CameraCaptureOptions.CamraPosition.BACK
    }
)

// 发布摄像头流
// 自定义配置信息，包含流描述和扩展信息
val publishCustomOptions = PublishCustomOptions(
    TrackDesc.TRACK_MAIN.value, null,
    // 辅码流配置
    mutableListOf(
        PublishCustomOptions(TrackDesc.TRACK_SUB.value, null, null)
    )
)
rtcEngine?.publishLocalVideo(
    // 传入 cameraTrack，和配置信息
    cameraTrack, publishCustomOptions,
    object : RTCResultListener {
        override fun onSuccess() {
            // 发布失败
        }

        override fun onFail(code: Int) {
            // 发布成功
        }
    }
)

// 取消发布摄像头流
rtcEngine?.unPublishLocalVideo(
    track,
    object : RTCResultListener {
        override fun onSuccess() {
            // 取消发布成功
        }

        override fun onFail(code: Int) {
            // 取消发布失败
        }
    }
)
```

#### 麦克风流控制
<font style="color:#E8323C;">注意：控制实例可以在初始化后就获取，但是采集和发布方法必须等加入房间后再调用</font>

```kotlin
// 获取麦克风控制实例，需要传入预设参数，目前只有一组：PreOptionMic.def
val micTrack = rtcEngine.getLocalMicTrack(PreOptionMic.def)

// 打开麦克风并发布本地音流
// 自定义配置信息，包含流描述和扩展信息
val publishCustomOptions = PublishCustomOptions(TrackDesc.TRACK_AUDIO.value, null, null)
RtcHelper.instance.rtcEngine?.publishLocalAudio(
    // 传入 micTrack，和配置信息
    micTrack, publishCustomOptions,
    object : RTCResultListener {
        override fun onSuccess() {
            // 发布成功
        }

        override fun onFail(code: Int) {
            // 发布失败
        }
    }
)

// 关闭麦克风并停止发布本地音频流
rtcEngine?.unPublishLocalAudio(
    track,
    object : RTCResultListener {
        override fun onSuccess() {
            // 取消发布成功
        }

        override fun onFail(code: Int) {
            // 取消发布失败
        }
    }
)

// 获取实时麦克风音量大小
val volume = micTrack.getVolume()
```

#### 录屏流控制
<font style="color:#E8323C;">注意：控制实例可以在初始化后就获取，但是采集和发布方法必须等加入房间后再调用</font>

```kotlin
// 获取录屏流控制实例
val screenTrack = rtcEngine.getLocalScreenTrack(this, PreOptionScreen.def)

// 设置录屏通知栏样式
screenTrack.setRecordNotification(R.mipmap.logo, "正在共享屏幕", "点击按钮结束录制", "停止录制")
// 设置录屏状态回调
screenTrack.setEvent(object : RTCScreenStateEvent {
 	override fun onScreenStateChanged(eventId: Int, args: String?) {
    	when (eventId) {
			VCS_EVENT_TYPE.ScreenRecordError -> {
				// 录屏出错
			}
			VCS_EVENT_TYPE.ScreenRecordStart -> {
				// 录屏开始
			}
			VCS_EVENT_TYPE.ScreenRecordStop -> {
				// 录屏结束
			}
		}
	}
})

// 请求录屏权限
screenTrack.request(result = { result: Boolean, intent: Intent? ->  
    if(result) {
        // 开始录屏
        screenTrack.startCapture(intent!!, true, LocalScreenTrack.CapOptType.SCREEN_CAP_OPT_DEF)
        // 发布录屏流
        // 自定义配置信息，包含流描述和扩展信息
        val publishCustomOptions = PublishCustomOptions(TrackDesc.TRACK_SHARE.value, null, null)
        rtcEngine?.publishLocalVideo(
            screenTrack, publishCustomOptions,
            object : RTCResultListener {
                override fun onSuccess() {
                    // 发布成功
                }
                
                override fun onFail(code: Int) {
                    // 发布失败
                }
            }
        )
    } else {
        TODO("Not yet implemented")
    }
})

// 停止录屏
screenTrack.stopCapture()

// 停止发布录屏流
rtcEngine?.unPublishLocalVideo(screenTrack, object : RTCResultListener {
    override fun onSuccess() {
        // 停止发布成功
    }
    override fun onFail(code: Int) {
        // 停止发布失败
    }

})

```

#### 自定义流控制
```kotlin
// 获取自定义流控制实例
val customVideoTrack = rtcEngine.getCustomVideoTrack()

// 开始发布自定义视频流
// customVideoOptions 中包含必填的流参数
customVideoTrack.startCustomVideo(customVideoOptions, object : RTCResultListener {
    override fun onSuccess() {
        TODO("Not yet implemented")
    }
    override fun onFail(code: Int) {
        TODO("Not yet implemented")
    }
})

// 发送编码后的流
// stamp：时间戳；data：流数据；angle:角度信息
customVideoTrack.inputData(stamp, data, angle)

// 停止发布自定义视频流
customVideoTrack.stopCustomVideo(object : RTCResultListener {
    override fun onSuccess() {
        TODO("Not yet implemented")
    }
    override fun onFail(code: Int) {
        TODO("Not yet implemented")
    }
})
```

#### 订阅远端视频流
<font style="color:#E8323C;">注意：控制实例可以在初始化后就获取，但是订阅方法必须等加入房间后再调用</font>

```kotlin
// 获取远端视频流控制类
val remoteVideoTrack = rtcEngine.getRemoteVideoTrack(uid, trackDesc)

// 添加渲染控件
remoteVideoTrack.addPlayView(vcsPlayerGlTextureView)
// 替换渲染控件
remoteVideoTrack.replacePlayView(vcsPlayerGlTextureViewList)
// 移除渲染控件
remoteVideoTrack.removePlayView(vcsPlayerGlTextureView)
// 移除所有渲染控件
remoteVideoTrack.removeAllPlayView()

// 设置监听，按需设置
remoteVideoTrack.setRemoteVideoEvent(
    object : RTCRemoteVideoEvent {
        override fun onReceiveStreamStatusChange(uid: String, trackDesc: String, isChoke: Boolean) {
            // 远端流状态变化
        }
    }
)

// 订阅远端流。参数：用户 id，轨道id
rtcEngine?.subscribeRemoteTrack(
    uid, trackId, 
    object : RTCResultListener { 
        override fun onSuccess() {
        }
        override fun onFail(code: Int) {
        }
})

// 取消订阅远端流。参数：用户 id，轨道id
remoteVideoTrack.unSubscribeRemoteTrack(uid, trackId)
```

#### 订阅远端合成视频流
<font style="color:#E8323C;">注意：控制实例可以在初始化后就获取，但是订阅方法必须等加入房间后再调用</font>

```kotlin
// 获取远端合成视频流控制类
val remoteMixtureTrack = rtcEngine.getRemoteMixtureTrack()

// 添加渲染控件
remoteMixtureTrack.addPlayView(vcsPlayerGlTextureView)
// 替换渲染控件
remoteMixtureTrack.replacePlayView(vcsPlayerGlTextureViewList)
// 移除渲染控件
remoteMixtureTrack.removePlayView(vcsPlayerGlTextureView)
// 移除所有渲染控件
remoteMixtureTrack.removeAllPlayView()

// 设置监听，按需设置
remoteMixtureTrack.setRemoteVideoEvent(
    object : RTCRemoteVideoEvent {
        override fun onReceiveStreamStatusChange(uid: String, trackDesc: String, isChoke: Boolean) {
            // 远端流状态变化
        }
    }
)

// 订阅远端合成视频流
rtcEngine?.subscribeRemoteMixture()

// 取消订阅远端合成视频流
remoteVideoTrack.unSubscribeRemoteTrack()
```

#### 订阅房间混音流
<font style="color:#E8323C;">注意：控制实例可以在初始化后就获取，但是操作方法必须等加入房间后再调用</font>

```kotlin
// 获取房间混音流控制类
val remoteAudioMixTrack = rtcEngine.getRemoteAudioMixTrack()

// 播放混音流
remoteAudioMixTrack.startPlay()

// 停止播放混音流
remoteAudioMixTrack.stopPlay()
```

### step 4：信息获取
```kotlin
// 获取频道信息
val channelInfo = rtcEngine.getChannelInfo()

// 获取自身用户信息
val meInfo = rtcEngine.getMeInfo()

// 获取全部成员信息，包括自己
val userInfos = rtcEngine.getUserInfos()

// 根据 uid 获取指定成员信息
val userInfo = rtcEngine.getUserInfo(uid)

// 根据 uid 获取指定用户的轨道列表
val trackInfoMap = rtcEngine.getTrackInfos(uid)

// 根据 uid、trackDesc 获取指定用户的指定轨道信息
val trackInfo = rtcEngine.getTrackInfoByTrackDesc(uid, trackDesc)

// 根据 uid、trackId 获取指定用户的指定轨道信息
val trackInfo = rtcEngine.getTrackInfoByTrackId(uid, trackId)
```

### step 5：释放资源
<font style="color:#DF2A3F;">注意：该接口与 initSDK 配对使用</font>

```kotlin
// 释放资源
rtcEngine.releaseSDK()
```





#### 
### 
#### 
### 
#### 
### 
