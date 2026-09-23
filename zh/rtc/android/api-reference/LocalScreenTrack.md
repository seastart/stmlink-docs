---
title: "LocalScreenTrack"
description: "Android 录屏：申请授权、启停屏幕采集、配置前台服务通知"
---

## 说明

`LocalScreenTrack` 用于发起录屏授权、启动/停止屏幕采集，并可作为 `publishLocalVideo` 的输入轨道。

## LocalScreenTrack 自身方法

### setEvent(e)
```kotlin
fun setEvent(e: RTCScreenStateEvent?)
```
方法说明：设置或清除屏幕采集状态回调。页面销毁时应传入 `null`，解除页面与 Track 之间的引用。

参数说明：
- `e`：`RTCScreenStateEvent?`，屏幕采集状态回调实现；`null` 表示清除回调。
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

### startCapture(intent, resultListener)
```kotlin
fun startCapture(intent: Intent, resultListener: RTCResultListener?)
```
方法说明：提交屏幕采集启动操作。`onSuccess()` 只表示 SDK 已接纳本次操作，不表示采集已经建立；后续真实状态通过 `RTCScreenStateEvent` 通知。结果回调不保证位于主线程。

参数说明：
- `intent`：`Intent`，由 `request` 授权成功回调返回的录屏授权数据。
- `resultListener`：`RTCResultListener?`，启动操作受理结果；`onFail(code)` 表示本次操作未被接纳，且不会产生本次请求对应的屏幕生命周期事件。可为 `null`。
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

## RTCScreenStateEvent 回调接口

`RTCScreenStateEvent` 为录屏状态回调接口，通过 `setEvent(e)` 注册。

### onScreenCaptureStateChanged(state, args)
```kotlin
fun onScreenCaptureStateChanged(state: ScreenCaptureState, args: String?)
```
方法说明：屏幕采集真实生命周期状态变化回调。启动操作是否被 SDK 接纳由 `startCapture` 的 `RTCResultListener` 单独表达。

参数说明：
- `state`：`ScreenCaptureState`，包含 `START`、`STOP`、`ERROR`，枚举值参见 [枚举定义](/zh/rtc/android/enums)。
- `args`：`String?`，扩展信息，可为 `null`。
返回值说明：无（`Unit`）。

> 从 2.0.29 起，`onScreenRecordStateChanged(ScreenRecordState, ...)` 已替换为 `onScreenCaptureStateChanged(ScreenCaptureState, ...)`，`ScreenRecordState.AUDIO_ERROR` 不再提供。
