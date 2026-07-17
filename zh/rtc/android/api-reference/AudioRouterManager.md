---
title: "AudioRouterManager"
description: "Android SRTC 音视频 SDK 音频路由管理类 AudioRouterManager 接口参考"
---

`AudioRouterManager` 负责管理扬声器 / 听筒 / 有线耳机 / 蓝牙耳机之间的音频输出路由。本页为接口参考；完整的初始化顺序、自动切换策略与最佳实践请见 [音频路由使用](/zh/rtc/android/advanced/audio-routing)。

## 获取与释放

通过 `RTCEngine` 获取单例，不要自行 `new`：

```kotlin
val audioRouterManager = rtcEngine.getAudioRouterManager()
// ...
rtcEngine.releaseAudioRouterManager()
```

## 实例方法

### setAudioRouterCalllback(callback)
```java
public void setAudioRouterCalllback(AudioRouterCallback callback)
```
方法说明：设置音频路由回调监听。  
参数说明：
- `callback`：`AudioRouterCallback`，路由变化回调实现。

返回值说明：无（`void`）。

> 方法名为 `setAudioRouterCalllback`（`Calllback` 含 3 个 `l`），请按源码原样调用。

### setAutoChangeAudioRouter(isAutoChange)
```java
public void setAutoChangeAudioRouter(boolean isAutoChange)
```
方法说明：设置是否自动切换音频路由（简化版）。等价于 `setAutoChangeAudioRouter(isAutoChange, false, false)`，即听筒优先级高于扬声器、蓝牙耳机优先级高于有线耳机。  
参数说明：
- `isAutoChange`：`boolean`，`true` 由内部自动选路，`false` 仅监听不自动切换。

返回值说明：无（`void`）。

### setAutoChangeAudioRouter(isAutoChange, isPrioritySpeaker, isPriorityWiredEarphone)
```java
public void setAutoChangeAudioRouter(boolean isAutoChange, boolean isPrioritySpeaker, boolean isPriorityWiredEarphone)
```
方法说明：设置自动切换策略（完整版）。  
参数说明：
- `isAutoChange`：`boolean`，是否自动切换路由。
- `isPrioritySpeaker`：`boolean`，`true` 扬声器优先于听筒，`false` 听筒优先于扬声器。
- `isPriorityWiredEarphone`：`boolean`，`true` 有线耳机优先于蓝牙耳机，`false` 蓝牙耳机优先于有线耳机。

返回值说明：无（`void`）。

### setMode(mode)
```java
public void setMode(int mode)
```
方法说明：设置音频模式。取值以 `AudioManager` 为准（如 `MODE_IN_COMMUNICATION`）。Android 6.0+ 下 `init()` 不会自动设置模式，建议每次切换业务场景前主动调用。  
参数说明：
- `mode`：`int`，`AudioManager` 音频模式。

返回值说明：无（`void`）。

### init()
```java
public void init()
```
方法说明：启动音频路由监听。建议在获取实例、设置回调与策略之后调用。  
参数说明：无。  
返回值说明：无（`void`）。

### switchAudioRouter(type)
```java
public void switchAudioRouter(AudioOutputDeviceType type)
```
方法说明：手动切换到指定输出设备。传入 `UN_KNOW` 表示按当前自动选路策略重新选择最合适的路由。  
参数说明：
- `type`：`AudioOutputDeviceType`，目标输出设备类型。

返回值说明：无（`void`）。

### release(changeMode)
```java
public void release(boolean changeMode)
```
方法说明：释放音频路由资源，停止监听并注销回调。  
参数说明：
- `changeMode`：`boolean`，`true` 释放时把音频模式恢复为 `MODE_NORMAL` 并切回扬声器；`false` 不主动恢复模式。

返回值说明：无（`void`）。

> `rtcEngine.releaseAudioRouterManager()` 内部调用 `release(true)`。

### getExitAudioOutputDevices()
```java
public HashMap<AudioOutputDeviceType, AudioDeviceInfo> getExitAudioOutputDevices()
```
方法说明：获取当前存在（可选）的输出设备集合。  
参数说明：无。  
返回值说明：`HashMap<AudioOutputDeviceType, AudioDeviceInfo>`，设备类型到设备信息的映射。

### getActiveAudioOutputDevice()
```java
public Pair<AudioOutputDeviceType, AudioDeviceInfo> getActiveAudioOutputDevice()
```
方法说明：获取当前实际生效的输出设备。  
参数说明：无。  
返回值说明：`Pair<AudioOutputDeviceType, AudioDeviceInfo>`，`first` 为设备类型，`second` 为设备信息。

### getAudioRouterCallback()
```java
public AudioRouterCallback getAudioRouterCallback()
```
方法说明：获取当前已设置的路由回调。  
参数说明：无。  
返回值说明：`AudioRouterCallback`，当前回调实例，可能为 `null`。

### getAudioManager()
```java
public AudioManager getAudioManager()
```
方法说明：获取内部持有的系统 `AudioManager`。  
参数说明：无。  
返回值说明：`AudioManager`。

### requestAudioFocus()
```java
public int requestAudioFocus()
```
方法说明：请求音频焦点。  
参数说明：无。  
返回值说明：`int`，请求结果（同系统 `AudioManager.requestAudioFocus` 返回值）。

### releaseAudioFocus()
```java
public int releaseAudioFocus()
```
方法说明：释放音频焦点。  
参数说明：无。  
返回值说明：`int`，释放结果。

### setFocusChangeListener(listener)
```java
public void setFocusChangeListener(AudioManager.OnAudioFocusChangeListener listener)
```
方法说明：设置外部音频焦点变化监听器。  
参数说明：
- `listener`：`AudioManager.OnAudioFocusChangeListener`，焦点变化监听器。

返回值说明：无（`void`）。

## 静态方法

### getValidBluetoothName(curName, context, callback)
```java
public static synchronized void getValidBluetoothName(String curName, Context context, ValidBluetoothNameCallback callback)
```
方法说明：纠正部分机型通过 `AudioDeviceInfo.getProductName()` 获取到的不准确蓝牙名称。Android 12+ 需关注 `BLUETOOTH_CONNECT` 权限。  
参数说明：
- `curName`：`String`，当前获取到的蓝牙名称。
- `context`：`Context`，上下文。
- `callback`：`ValidBluetoothNameCallback`，纠正后的名称回调。

返回值说明：无（`void`）。

## 枚举 AudioOutputDeviceType

| 枚举值 | 说明 |
| --- | --- |
| `UN_KNOW` | 未知 / 触发按策略自动选择。 |
| `SPEAKER` | 扬声器。 |
| `EARPIECE` | 听筒。 |
| `WIRED_EARPHONE` | 有线耳机。 |
| `BLUETOOTH_HEADSET` | 蓝牙耳机。 |

## 回调接口

### AudioRouterCallback
```java
public interface AudioRouterCallback {
    void exitOutputDeviceChange(HashMap<AudioOutputDeviceType, AudioDeviceInfo> audioOutputDevices);
    void activeOutputDeviceChange(Pair<AudioOutputDeviceType, AudioDeviceInfo> audioOutputDevice);
    void onAudioBecomingNoisy();
}
```
- `exitOutputDeviceChange`：当前“可选”的输出设备列表发生变化（插拔耳机、连接/断开蓝牙等）。
- `activeOutputDeviceChange`：当前“实际生效”的输出设备发生变化，UI 展示当前设备应以此为准。
- `onAudioBecomingNoisy`：路由切换后系统可能产生噪音（如耳机拔出转外放），可在此暂停播放或降低音量。

### ValidBluetoothNameCallback
```java
public interface ValidBluetoothNameCallback {
    void onValidBluetoothName(String name);
}
```
- `onValidBluetoothName`：返回纠正后的蓝牙设备名称。
