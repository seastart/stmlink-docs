---
title: "RemoteVideoTrack"
description: "Android SRTC 音视频 SDK RemoteVideoTrack 接口参考"
---

## 说明

`RemoteVideoTrack` 用于远端视频渲染与远端流状态监听。

## RemoteVideoTrack 自身方法

### setRemoteVideoEvent(event)
```kotlin
fun setRemoteVideoEvent(event: RTCRemoteVideoEvent)
```
方法说明：设置远端视频流状态监听，并注册全局时钟检测。  
参数说明：
- `event`：`RTCRemoteVideoEvent`，远端流状态事件回调实现。
返回值说明：无（`Unit`）。

状态触发说明：
- 订阅后连续约 3 秒未收到有效帧时，回调 `isChoke = true`。
- 收到有效帧并恢复后，回调 `isChoke = false`。

### removeRemoteVideoEvent()
```kotlin
fun removeRemoteVideoEvent()
```
方法说明：移除远端流状态监听，并取消全局时钟检测。  
参数说明：无。  
返回值说明：无（`Unit`）。

## 继承自 VideoTrack 的渲染方法

### addPlayView(view)
```kotlin
fun addPlayView(view: View): Boolean
```
方法说明：添加单个渲染控件。仅支持 `VcsPlayerGlTextureView` / `VcsPlayerGlSurfaceView`。  
参数说明：
- `view`：`View`，渲染控件。
返回值说明：`Boolean`，`true` 表示添加成功；类型不支持或重复添加时为 `false`。

### replacePlayView(views)
```kotlin
fun replacePlayView(views: MutableList<View>)
```
方法说明：替换全部渲染控件列表。  
参数说明：
- `views`：`MutableList<View>`，渲染控件集合，仅支持 `VcsPlayerGlTextureView` / `VcsPlayerGlSurfaceView`。
返回值说明：无（`Unit`）。

### removePlayView(view)
```kotlin
fun removePlayView(view: View)
```
方法说明：移除指定渲染控件。  
参数说明：
- `view`：`View`，目标渲染控件。
返回值说明：无（`Unit`）。

### removeAllPlayView()
```kotlin
fun removeAllPlayView()
```
方法说明：移除全部渲染控件。  
参数说明：无。  
返回值说明：无（`Unit`）。

## RTCRemoteVideoEvent 回调接口

`RTCRemoteVideoEvent` 为远端视频流状态回调接口，通过 `setRemoteVideoEvent(event)` 注册。

### onReceiveStreamStatusChange(uid, trackDesc, isChoke)
```kotlin
fun onReceiveStreamStatusChange(uid: String, trackDesc: String, isChoke: Boolean)
```
方法说明：远端视频流状态变化回调。  
参数说明：
- `uid`：`String`，远端用户 ID。
- `trackDesc`：`String`，轨道描述。
- `isChoke`：`Boolean`，是否卡顿；`true` 为卡顿，`false` 为恢复正常。
返回值说明：无（`Unit`）。
