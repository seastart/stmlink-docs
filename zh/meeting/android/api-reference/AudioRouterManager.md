---
title: "AudioRouterManager"
description: "Android SMeeting 会议 SDK AudioRouterManager 接口参考"
---

### setAudioRouterCalllback()
设置音频路由监听事件

```java
public void setAudioRouterCalllback(AudioRouterCallback callback)
```html

参数

| callback | AudioRouterCallback 类型，音频路由变化监听接口 |
| --- | --- |


AudioRouterCallback  接口说明

| 接口名称 | 接口说明 | 返回值 |
| --- | --- | --- |
| exitOutputDeviceChange | 当前存在的音频输出设备变化 | audioOutputDevices： HashMap<AudioOutputDeviceType, AudioDeviceInfo> 类型，当前存在的音频输出设备列表 |
| activeOutputDeviceChange | 当前活跃的音频输出设备变化 | audioOutputDevice：Pair<AudioOutputDeviceType, AudioDeviceInfo> 类型，当前活跃的音频输出设备 |
| onAudioBecomingNoisy | 路由变化后可能会产生噪音 |  |


### setAutoChangeAudioRouter()
设置是否自动切换音频路由。默认听筒优先级高于扬声器，默认蓝牙耳机优先级高于有线耳机

```java
public void setAutoChangeAudioRouter(boolean isAutoChange)
```

参数

| isAutoChange | 是否由内部自动切换音频路由。true：是；false：否 |
| --- | --- |


### setAutoChangeAudioRouter()
设置是否自动切换音频路由，只有 isAutoChange 为 true 时，isPrioritySpeaker 和 isPriorityWiredEarphone 的值才有意义

```java
public void setAutoChangeAudioRouter(
    boolean isAutoChange, boolean isPrioritySpeaker, boolean isPriorityWiredEarphone
)
```html

参数

| isAutoChange | 是否由内部自动切换音频路由。<br/>true：是；false：否 |
| --- | --- |
| isPrioritySpeaker | 扬声器和听筒的优先级。默认 false<br/>true：扬声器优先级更高；false：听筒优先级更高 |
| isPriorityWiredEarphone | 蓝牙耳机和有线耳机的优先级。默认 false<br/>true：有线耳机优先级更高；false：蓝牙耳机优先级更高 |


### setMode()
设置音频音频模式。

ps：切换场景时，需要设置一次音频模式

```kotlin
public void setMode(int mode)
```

参数

| mode | 音频模式。<br/>AudioManager.MODE_NORMAL<br/>AudioManager.MODE_RINGTONE<br/>AudioManager.MODE_IN_CALL<br/>AudioManager.MODE_IN_COMMUNICATION<br/>AudioManager.MODE_CALL_SCREENING<br/>AudioManager.MODE_CALL_REDIRECT<br/>AudioManager.MODE_COMMUNICATION_REDIRECT |
| --- | --- |


### init()
启动路由

```kotlin
public void init()
```kotlin

### switchAudioRouter()
切换路由

```kotlin
public void switchAudioRouter(AudioOutputDeviceType type)
```

参数

| type | AudioOutputDeviceType 枚举类型 |
| --- | --- |


AudioOutputDeviceType 属性说明

| 枚举名称 | 说明 |
| --- | --- |
| UN_KNOW | 未知 |
| SPEAKER | 扬声器 |
| EARPIECE | 听筒 |
| WIRED_EARPHONE | 有线耳机 |
| BLUETOOTH_HEADSET | 蓝牙耳机 |


### release()
释放资源

```java
public void release(boolean changeMode)
```html

参数

| changeMode | Boolean 类型，是否将音频模式重置为 AudioManager.MODE_NORMAL，音频路由切换到扬声器。 |
| --- | --- |


### getExitAudioOutputDevices()
获取当前存在的音频输出设备

```kotlin
public HashMap<AudioOutputDeviceType, AudioDeviceInfo> getExitAudioOutputDevices()
```

返回值

| HashMap 类型，当前存在的音频输出设备 |
| --- |


### getActiveAudioOutputDevice()
获取当前活跃的音频输出设备

```kotlin
public Pair<AudioOutputDeviceType, AudioDeviceInfo> getActiveAudioOutputDevice()
```kotlin

返回值

| Pair 类型，当前活跃的音频输出设备 |
| --- |


### getValidBluetoothName()
修正蓝牙耳机名称

ps：由于部分机型无法通过 AudioDeviceInfo#getProductName() 获取到正确的蓝牙耳机名称，可以通过该方法对名称做纠正

```kotlin
public static synchronized void getValidBluetoothName(String curName, Context context, ValidBluetoothNameCallback callback)
```

参数

| curName | String 类型，当前的蓝牙名称 |
| --- | --- |
| context | 上下文 |
| callback | ValidBluetoothNameCallback 回调 |


ValidBluetoothNameCallback 回调说明

| 接口名称 | 接口说明 | 返回值 |
| --- | --- | --- |
| onValidBluetoothName | 返回有效的蓝牙名称 | name： String 类型，蓝牙名称 |


