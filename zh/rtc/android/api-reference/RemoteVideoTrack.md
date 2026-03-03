---
title: "RemoteVideoTrack"
description: "Android SRTC 音视频 SDK RemoteVideoTrack 接口参考"
---

+ 提供远端视频流渲染，事件回调

### setRemoteVideoEvent()
设置远端流监听事件

```kotlin
fun setRemoteVideoEvent(event: RTCRemoteVideoEvent)
```html

RTCRemoteVideoEvent  接口说明

| 接口名称 | 接口说明 | 参数 |
| --- | --- | --- |
| onReceiveStreamStatusChange | 流媒体接收远端流状态变更回调 | uid：String类型，用户id<br/>trackDesc：String类型，轨道描述<br/>isChoke：Boolean类型，是否阻塞 |


### removeRemoteVideoEvent()
移除远端流监听事件

```java
fun removeRemoteVideoEvent()
```

### addPlayView(view: View)
添加渲染控件

```kotlin
fun addPlayView(view: View): Boolean
```html

参数

| view | 渲染控件，View的类型必须是下述中的一种<br/>VcsPlayerGlTextureView<br/>VcsPlayerGlSurfaceView |
| --- | --- |


### replacePlayView()
替换渲染控件

```kotlin
fun replacePlayView(views: MutableList<View>)
```

| views | 渲染控件集合，View的类型必须是下述中的一种<br/>VcsPlayerGlTextureView<br/>VcsPlayerGlSurfaceView |
| --- | --- |


### removePlayView()
移除指定的渲染控件

```kotlin
fun removePlayView(view: View)
```html

参数

| view | 渲染控件，View的类型必须是下述中的一种<br/>VcsPlayerGlTextureView<br/>VcsPlayerGlSurfaceView |
| --- | --- |


### removeAllPlayView()
移除所有渲染控件

+ 此处移除所有渲染控件，本质上是清空当前 uid、trackId 对应的渲染控件列表

```kotlin
fun removeAllPlayView()
```



