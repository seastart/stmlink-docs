# 音频路由使用说明

本文档基于 `rtc/src/main/java/cn/seastart/rtc/media/audioRouter/AudioRouterManager.java` 的实际实现整理，适用于在通话、会议、语音互动等场景中管理扬声器 / 听筒 / 有线耳机 / 蓝牙耳机路由。

## 1. 获取 `AudioRouterManager`

```kotlin
// 通过 rtcEngine 获取音频路由管理类
var audioRouterManager = rtcEngine.getAudioRouterManager()
```

`rtcEngine.getAudioRouterManager()` 会返回单例对象；对应释放方法为：

```kotlin
rtcEngine.releaseAudioRouterManager()
audioRouterManager = null
```

---

## 2. 推荐初始化顺序

推荐在进入房间 / 开始通话时按下面顺序初始化：

1. 获取 `AudioRouterManager`
2. 设置回调监听
3. 设置音频模式 `setMode(...)`
4. 设置自动切换策略 `setAutoChangeAudioRouter(...)`
5. 调用 `init()` 启动路由监听

完整示例：

```kotlin
// 省略 import，以下示例假设相关类型已可直接使用

private var audioRouterManager: AudioRouterManager? = null

private fun initAudioRouterManager() {
    audioRouterManager = rtcEngine.getAudioRouterManager()

    // 注意：API 名称为 setAudioRouterCalllback（Calllback 有 3 个 l）
    audioRouterManager?.setAudioRouterCalllback(object : AudioRouterCallback {
        override fun exitOutputDeviceChange(
            audioOutputDevices: HashMap<AudioRouterManager.AudioOutputDeviceType, AudioDeviceInfo?>
        ) {
            // 当前存在的输出设备发生变化
            // 例如：插入有线耳机、连接蓝牙耳机、拔出耳机等
        }

        override fun activeOutputDeviceChange(
            audioOutputDevice: Pair<AudioRouterManager.AudioOutputDeviceType, AudioDeviceInfo?>
        ) {
            // 当前实际生效的输出设备发生变化
            // audioOutputDevice.first  为设备类型
            // audioOutputDevice.second 为设备信息（Android 6.0+ 可用）
        }

        override fun onAudioBecomingNoisy() {
            // 路由切换后系统可能产生噪音
            // 例如可在这里做暂停播放、降低音量等处理
        }
    })

    // 每次切换业务场景时，都应根据场景重新设置 mode
    audioRouterManager?.setMode(AudioManager.MODE_IN_COMMUNICATION)

    // 开启自动切换：扬声器优先级高于听筒；蓝牙耳机优先级高于有线耳机
    audioRouterManager?.setAutoChangeAudioRouter(
        true,
        true,
        false
    )

    // 启动路由监听
    audioRouterManager?.init()
}
```

---

## 3. `setMode` 使用说明

```kotlin
audioRouterManager?.setMode(AudioManager.MODE_IN_COMMUNICATION)
```

支持的模式以 `AudioManager` 为准，常用值包括：

- `AudioManager.MODE_NORMAL`
- `AudioManager.MODE_RINGTONE`
- `AudioManager.MODE_IN_CALL`
- `AudioManager.MODE_IN_COMMUNICATION`
- `AudioManager.MODE_CALL_SCREENING`
- `AudioManager.MODE_CALL_REDIRECT`
- `AudioManager.MODE_COMMUNICATION_REDIRECT`

### 说明

- 当前项目 `minSdk = 24`，实际走的是 Android 6.0+ 路径。
- 在 6.0+ 实现中，`init()` **不会自动设置音频模式**，需要业务层主动调用 `setMode(...)`。
- 因此建议：**每次切换场景前都重新设置一次 mode**，例如语聊、会议、媒体播放等场景切换时都重新调用。

---

## 4. `setAutoChangeAudioRouter` 自动切换策略

### 4.1 简单用法

```kotlin
audioRouterManager?.setAutoChangeAudioRouter(true)
```

等价于：

```kotlin
audioRouterManager?.setAutoChangeAudioRouter(
    true,
    false,
    false
)
```

即：

- 开启自动切换
- **听筒优先级高于扬声器**
- **蓝牙耳机优先级高于有线耳机**

### 4.2 完整用法

```kotlin
audioRouterManager?.setAutoChangeAudioRouter(
    isAutoChange = true,
    isPrioritySpeaker = true,
    isPriorityWiredEarphone = false
)
```

参数含义：

- `isAutoChange`
  - `true`：由内部自动切换音频路由
  - `false`：仅监听设备变化，不自动切换，由业务层手动调用 `switchAudioRouter(...)`
- `isPrioritySpeaker`
  - `true`：扬声器优先级高于听筒
  - `false`：听筒优先级高于扬声器
- `isPriorityWiredEarphone`
  - `true`：有线耳机优先级高于蓝牙耳机
  - `false`：蓝牙耳机优先级高于有线耳机

### 4.3 自动切换规则（基于代码实现）

自动切换总体遵循以下策略：

1. 后接入的设备通常会触发一次重新选路。
2. 大类优先级：**蓝牙耳机 / 有线耳机 > 听筒 / 扬声器**。
3. 同组内优先级可通过参数自定义：
   - 蓝牙耳机 vs 有线耳机：由 `isPriorityWiredEarphone` 控制
   - 听筒 vs 扬声器：由 `isPrioritySpeaker` 控制
4. 设备移除后，会按照剩余设备重新选择可用路由。

例如：

- 同时存在蓝牙耳机和有线耳机：
  - `isPriorityWiredEarphone = false` 时，优先蓝牙耳机
  - `isPriorityWiredEarphone = true` 时，优先有线耳机
- 没有耳机类设备时：
  - `isPrioritySpeaker = false` 时，优先听筒
  - `isPrioritySpeaker = true` 时，优先扬声器

---

## 5. 回调说明

### 5.1 当前存在的输出设备变化

```kotlin
override fun exitOutputDeviceChange(
    audioOutputDevices: HashMap<AudioRouterManager.AudioOutputDeviceType, AudioDeviceInfo?>
) {
}
```

表示当前“可选”的音频输出设备列表发生变化，例如：

- 连接 / 断开蓝牙耳机
- 插入 / 拔出有线耳机
- 系统可用输出设备发生变化

可用设备类型来自 `AudioOutputDeviceType`：

- `SPEAKER`：扬声器
- `EARPIECE`：听筒
- `WIRED_EARPHONE`：有线耳机
- `BLUETOOTH_HEADSET`：蓝牙耳机
- `UN_KNOW`：未知 / 自动选择占位值

> 当前项目 `minSdk = 24`，因此这里的 `AudioDeviceInfo` 在实际项目中通常可用；源码中“低于 Android 6.0 时可能为 null”的说明主要是兼容性保留。

### 5.2 当前活跃输出设备变化

```kotlin
override fun activeOutputDeviceChange(
    audioOutputDevice: Pair<AudioRouterManager.AudioOutputDeviceType, AudioDeviceInfo?>
) {
}
```

表示当前真正生效的输出设备发生变化。通常 UI 上的“当前扬声器 / 蓝牙 / 听筒状态”应该以这个回调为准。

### 5.3 路由变化可能产生噪音

```kotlin
override fun onAudioBecomingNoisy() {
}
```

例如耳机拔出、A2DP 断开后系统可能转到外放，可在这里做业务保护：

- 暂停播放器
- 降低音量
- 弹提示给用户

---

## 6. 获取当前可用设备和当前生效设备

### 6.1 获取当前存在的输出设备

```kotlin
val devices = audioRouterManager?.getExitAudioOutputDevices()
devices?.forEach { (type, info) ->
    val name = info?.productName?.toString() ?: type.name
}
```

### 6.2 获取当前活跃输出设备

```kotlin
val activeDevice = audioRouterManager?.getActiveAudioOutputDevice()
val activeType = activeDevice?.first
val activeInfo = activeDevice?.second
```

### 6.3 蓝牙名称纠正（可选）

部分机型通过 `AudioDeviceInfo.getProductName()` 获取到的蓝牙名称可能不准确，此时可以使用：

```kotlin
if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M) {
    AudioRouterManager.getValidBluetoothName(
        curName = activeInfo?.productName?.toString().orEmpty(),
        context = this
    ) { validName ->
        // validName 为纠正后的蓝牙名称
    }
}
```

> 如果要获取更准确的蓝牙设备名称，请确保蓝牙相关权限已授权；Android 12 及以上需要关注 `BLUETOOTH_CONNECT` 权限。

---

## 7. 手动切换路由

大多数情况下，这一步是用户点击 UI 按钮触发的。

```kotlin
audioRouterManager?.switchAudioRouter(selectType)
```

其中 `selectType` 为 `AudioOutputDeviceType` 枚举值，例如：

```kotlin
audioRouterManager?.switchAudioRouter(AudioRouterManager.AudioOutputDeviceType.SPEAKER)
audioRouterManager?.switchAudioRouter(AudioRouterManager.AudioOutputDeviceType.EARPIECE)
audioRouterManager?.switchAudioRouter(AudioRouterManager.AudioOutputDeviceType.WIRED_EARPHONE)
audioRouterManager?.switchAudioRouter(AudioRouterManager.AudioOutputDeviceType.BLUETOOTH_HEADSET)
```

### 特殊值：`UN_KNOW`

```kotlin
audioRouterManager?.switchAudioRouter(AudioRouterManager.AudioOutputDeviceType.UN_KNOW)
```

传入 `UN_KNOW` 时，不表示切换到“未知设备”，而是表示：**按当前自动选路策略重新选择一个最合适的路由**。

适合以下场景：

- 用户点“恢复系统推荐路由”
- 插拔设备后，主动要求 SDK 重新计算最佳设备

---

## 8. 释放资源

推荐通过 `rtcEngine` 统一释放：

```kotlin
rtcEngine.releaseAudioRouterManager()
audioRouterManager = null
```

根据 `RTCEngineImpl` 的实现，`releaseAudioRouterManager()` 内部会调用：

```kotlin
audioRouterManager.release(true)
```

这意味着释放时会执行以下动作：

- 停止音频路由监听
- 注销相关广播 / 回调
- 将音频模式恢复为 `AudioManager.MODE_NORMAL`
- 将输出切回扬声器

如果业务层直接调用：

```kotlin
audioRouterManager?.release(false)
```

则表示释放时**不主动恢复 mode**。

---

## 9. 常用设备枚举

```kotlin
AudioRouterManager.AudioOutputDeviceType.UN_KNOW
AudioRouterManager.AudioOutputDeviceType.SPEAKER
AudioRouterManager.AudioOutputDeviceType.EARPIECE
AudioRouterManager.AudioOutputDeviceType.WIRED_EARPHONE
AudioRouterManager.AudioOutputDeviceType.BLUETOOTH_HEADSET
```

含义如下：

- `UN_KNOW`：未知 / 触发自动选择
- `SPEAKER`：扬声器
- `EARPIECE`：听筒
- `WIRED_EARPHONE`：有线耳机
- `BLUETOOTH_HEADSET`：蓝牙耳机

---

## 10. 推荐实践

1. **进入房间时初始化，退出房间时释放**，不要在每次按钮点击时重复创建。
2. **每次切换业务场景都调用一次 `setMode(...)`**。
3. UI 上展示“当前正在使用哪个设备”时，优先以 `activeOutputDeviceChange(...)` 为准。
4. 需要展示“用户可选哪些设备”时，以 `exitOutputDeviceChange(...)` 或 `getExitAudioOutputDevices()` 为准。
5. 使用蓝牙设备时，建议在真机上验证：
   - 连接蓝牙耳机
   - 断开蓝牙耳机
   - 插入 / 拔出有线耳机
   - 手动切换扬声器 / 听筒 / 蓝牙
6. 如果业务中同时存在多种音频播放/通话状态，建议重点验证不同设备切换下的实际表现。

---

## 11. Demo 中的实际初始化方式

`app/src/main/java/cn/seastart/rtcdemo/activity/RoomActivity.kt` 中实际使用方式如下：

```kotlin
audioRouterManager = rtcEngine.getAudioRouterManager()
audioRouterManager?.setAudioRouterCalllback(/* callback */)
audioRouterManager?.setMode(AudioManager.MODE_IN_COMMUNICATION)
audioRouterManager?.setAutoChangeAudioRouter(true, true, false)
audioRouterManager?.init()
```

可以直接作为会议场景接入参考。
