---
title: "LocalCameraTrack"
description: "Android SRTC 音视频 SDK LocalCameraTrack 接口参考"
---

+ 提供摄像头打开、关闭操作，摄像头预览画面渲染
+ 为 publishLocalVideo 提供配置参数

### startCapture()
开始采集

```kotlin
fun startCapture(listener: RTCResultListener?)
```kotlin

参数

| listener | 操作结果回调 |
| --- | --- |


### stopCapture()
停止采集

```kotlin
fun stopCapture()
```

### switchCameraPosition()
切换前后摄像头

```kotlin
fun switchCameraPosition(position: CameraCaptureOptions.CamraPosition) 
```html

参数

| position | 前后摄像头标识，<br/>CamraPosition.FRONT  前置摄像头<br/>CamraPosition.BACK  后置摄像头 |
| --- | --- |


### setCameraAngleOffset(）
设置摄像头偏移角度

ps: 这个方法是用于应对特殊设备的，有些设备摄像头安置角度与普通手机不一致，可以通过这个方法调整。

```kotlin
fun setCameraAngleOffset(offset: Int)
```

参数

| offset | 摄像头角度偏移量，<br/>参考值：0, 90, 180, 270 |
| --- | --- |


### addPlayView()
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

+ 此处移除所有渲染控件，本质上是清空当前 uid、trackDesc 对应的渲染控件列表

```kotlin
fun removeAllPlayView()
```

