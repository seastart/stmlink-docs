---
title: "LocalCameraTrack"
description: "Android SRTC 音视频 SDK LocalCameraTrack 接口参考"
---

## 说明

`LocalCameraTrack` 用于本地摄像头采集、预览渲染与摄像头控制，并作为 `publishLocalVideo` 的输入轨道。

## LocalCameraTrack 自身方法

### startCapture(listener)
```kotlin
fun startCapture(listener: RTCResultListener?)
```
方法说明：启动摄像头采集。调用前需具备相机权限。  
参数说明：
- `listener`：`RTCResultListener?`，启动结果回调；无权限时会回调 `onFail(StatusCode.LACK_PERMISSION.value)`。
返回值说明：无（`Unit`）。

### stopCapture()
```kotlin
fun stopCapture()
```
方法说明：停止摄像头采集。  
参数说明：无。  
返回值说明：无（`Unit`）。

### switchCameraPosition(position)
```kotlin
fun switchCameraPosition(position: CameraCaptureOptions.CamraPosition)
```
方法说明：切换摄像头朝向。  
参数说明：
- `position`：`CameraCaptureOptions.CamraPosition`，目标摄像头位置：
  - `FRONT`：前置摄像头
  - `BACK`：后置摄像头
  - `External`：外接摄像头
返回值说明：无（`Unit`）。

### switchCameraDevice(cameraId)
```kotlin
fun switchCameraDevice(cameraId: String)
```
方法说明：按真实 Camera2 `cameraId` 精确切换摄像头。适用于设备存在多颗摄像头、需要指定具体某一颗（而非仅前/后置）的场景。`cameraId` 取自 [`RTCEngine.getCameraDevices`](/zh/rtc/android/api-reference/RTCEngine) 返回的 `CameraDeviceCapability.cameraId`。  
参数说明：
- `cameraId`：`String`，目标摄像头的 Camera2 原生 ID。
返回值说明：无（`Unit`）。

### openFrontCameraMirror()
```kotlin
fun openFrontCameraMirror()
```
方法说明：打开前置摄像头镜像（默认状态）。仅对前置摄像头生效，其他摄像头保持原逻辑。  
参数说明：无。  
返回值说明：无（`Unit`）。

### closeFrontCameraMirror()
```kotlin
fun closeFrontCameraMirror()
```
方法说明：关闭前置摄像头镜像（即本地预览与前置画面保持“所见非镜像”的实际朝向）。  
参数说明：无。  
返回值说明：无（`Unit`）。

### isFrontCameraMirrorOpen()
```kotlin
fun isFrontCameraMirrorOpen(): Boolean
```
方法说明：查询前置摄像头镜像当前是否开启。  
参数说明：无。  
返回值说明：`Boolean`，`true` 表示镜像开启，`false` 表示关闭。

> 前置镜像仅影响**本地预览渲染**，不改变编码发布到远端的画面。

### setCameraAngleOffset(offset)
```kotlin
fun setCameraAngleOffset(offset: Int)
```
方法说明：设置摄像头角度偏移，用于特殊设备方向校正。SDK 会自动归一化为 `0/90/180/270`。  
参数说明：
- `offset`：`Int`，角度偏移值，建议传 `0/90/180/270`。
返回值说明：无（`Unit`）。

### switchLight(open)
```kotlin
fun switchLight(open: Boolean)
```
方法说明：切换摄像头闪光灯状态。  
参数说明：
- `open`：`Boolean`，`true` 打开闪光灯，`false` 关闭闪光灯。
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
