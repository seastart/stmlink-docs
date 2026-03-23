---
title: "LocalScreenTrack"
description: "Android SRTC 音视频 SDK LocalScreenTrack 接口参考"
---

## 说明

`LocalScreenTrack` 用于发起录屏授权、启动/停止屏幕采集，并可作为 `publishLocalVideo` 的输入轨道。

## LocalScreenTrack 自身方法

### setEvent(e)
```kotlin
fun setEvent(e: RTCScreenStateEvent)
```
方法说明：设置录屏状态回调。  
参数说明：
- `e`：`RTCScreenStateEvent`，录屏状态回调实现。
返回值说明：无（`Unit`）。

### request(result)
```kotlin
fun request(result: (Boolean, Intent?) -> Unit)
```
方法说明：请求系统录屏权限。授权成功后回调的 `Intent` 需用于 `startCapture`。  
参数说明：
- `result`：`(Boolean, Intent?) -> Unit`，权限请求结果回调。
返回值说明：无（`Unit`）。

### setRecordNotification(smallIcon, title, desc, buttonText)
```kotlin
fun setRecordNotification(smallIcon: Int, title: String?, desc: String?, buttonText: String?)
```
方法说明：设置录屏通知栏样式。  
参数说明：
- `smallIcon`：`Int`，通知小图标资源 ID。
- `title`：`String?`，通知标题，可为 `null`。
- `desc`：`String?`，通知描述，可为 `null`。
- `buttonText`：`String?`，通知按钮文本，可为 `null`。
返回值说明：无（`Unit`）。

### startCapture(intent, hasBar)
```kotlin
fun startCapture(intent: Intent, hasBar: Boolean)
```
方法说明：开始屏幕采集。  
参数说明：
- `intent`：`Intent`，由 `request` 授权成功回调返回的录屏授权数据。
- `hasBar`：`Boolean`，是否包含系统栏参数（当前版本内部未使用，建议按业务语义传值）。
返回值说明：无（`Unit`）。

### stopCapture()
```kotlin
fun stopCapture()
```
方法说明：停止屏幕采集。  
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
