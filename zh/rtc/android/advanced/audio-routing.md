### step 1: 获取音频路由管理类
```kotlin
// 通过 rtcEngine 的 getAudioRouterManager 获取音频路由管理类
audioRouterManager = rtcEngine.getAudioRouterManager()
```

### step 2: 设置回调监听
```kotlin
audioRouterManager.setAudioRouterCalllback(object : AudioRouterCallback {
    override fun exitOutputDeviceChange(audioOutputDevices: java.util.HashMap<AudioRouterManager.AudioOutputDeviceType?, AudioDeviceInfo?>) {
        TODO("Not yet implemented")
    }
    override fun activeOutputDeviceChange(audioOutputDevice: Pair<AudioRouterManager.AudioOutputDeviceType, AudioDeviceInfo?>) {
        TODO("Not yet implemented")
    }
    override fun onAudioBecomingNoisy() {
        TODO("Not yet implemented")
    }
})
```

### step 3: 设置音频模式
<font style="color:#DF2A3F;">ps：每次切换场景，根据业务需求，都需要设置一次音频模式</font>

```kotlin
audioRouterManager.setMode(AudioManager.MODE_IN_COMMUNICATION)
```

### step 4: 设置其他参数
```kotlin
// 此处设置的是允许自动切换路由，扬声器比听筒优先级高，蓝牙耳机比有线耳机优先级高
audioRouterManager.setAutoChangeAudioRouter(true, true, false)
```

### step 5: 启动路由
```kotlin
audioRouterManager.init()
```

### step 6: 切换路由
此操作大部分情况下是由用户点击按钮执行

```kotlin
// 切换路由，selectType 为 AudioOutputDeviceType 枚举类型
audioRouterManager?.switchAudioRouter(selectType)
```

### step 6: 释放资源
```kotlin
// 通过 rtcEngine 中的 releaseAudioRouterManager 释放资源
rtcEngine.releaseAudioRouterManager()
audioRouterManager = null
```

