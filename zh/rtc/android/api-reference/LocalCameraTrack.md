---
title: "LocalCameraTrack"
description: "本地摄像头采集、预览渲染、前后置切换、镜像与闪光灯控制"
---

## 说明

`LocalCameraTrack` 用于本地摄像头采集、预览渲染与摄像头控制，并作为 `publishLocalVideo` 的输入轨道。

摄像头操作以**新画面真正出帧**为成功判据，结果通过 `RTCResultListener` 异步回调。一次操作尚未出结果时又发起新的操作，前一次的回调静默丢弃，只有最后一次给出结果。

## preOpt

```kotlin
var preOpt: PreOptionCamera
```
属性说明：当前采集与发布预设，见 [摄像头预设](/zh/rtc/android/presets/camera)。

- 赋值和 `getLocalCameraTrack(preOpt)` 都会**复制一份 `preOpt.capture`**，因此拿到轨道后再修改原对象的 `capture` 不会生效，需要重新赋值 `track.preOpt = opt`；修改 `preOpt.publish` 仍然生效。
- `capture.deviceId` 与 `capture.position` 由 SDK 在切换成功后回写为实际生效的设备，可配合 `getCurrentCameraId()` 读取。

## LocalCameraTrack 自身方法

### startCapture(listener)
```kotlin
fun startCapture(listener: RTCResultListener?)
```
方法说明：启动摄像头采集。调用前需具备相机权限。摄像头真正产出首帧才算启动成功。  
`capture` 中的 `deviceId` 与 `position` 在这里都是**建议值**：建议的设备不可用时，SDK 会依次尝试同方向、再到全部可用设备，不会因为建议无效直接失败；自动选中的结果不会写回配置，需通过 `getCurrentCameraId()` 查询。  
已经在采集时本次调用直接返回成功，且**新的 `capture` 整份都不生效**（含分辨率、帧率与设备意图）；要换参数需先 `stopCapture()` 再启动。  
参数说明：
- `listener`：`RTCResultListener?`，启动结果回调；无权限时回调 `onFail(RtcCameraErrorCode.CAMERA_PERMISSION_DENIED)`（`102231`），可用设备全部试过仍无画面时回调 `onFail(RtcCameraErrorCode.CAMERA_FIRST_FRAME_TIMEOUT)`（`102239`）。失败码含义见 [错误码](/zh/rtc/android/error-codes)。

返回值说明：无（`Unit`）。

### stopCapture()
```kotlin
fun stopCapture()
```
方法说明：停止摄像头采集。  
参数说明：无。  
返回值说明：无（`Unit`）。

### switchCameraPosition(position, listener)
```kotlin
@JvmOverloads
fun switchCameraPosition(
    position: CameraCaptureOptions.CamraPosition,
    listener: RTCResultListener? = null
)
```
方法说明：切换摄像头朝向。方向是**指令**：只在该方向内依次尝试，方向内第一颗打不开会继续试下一颗，但不会切到其他方向。新摄像头真正产出首帧才算成功，成功后由 SDK 把方向写回配置并清空 `deviceId`。  
未在采集时（首次、`stopCapture()` 之后、上次启动失败之后）可以直接调用，无需先 `startCapture()`；已在采集时沿用当前的分辨率与帧率。  
**失败不会自动回退到原摄像头**。目标设备或格式校验失败时可能保留原采集，因此失败回调不代表摄像头一定已停止；需要关闭时仍应调用 `stopCapture()`。

应用若只需恢复可用画面，可调用 `startCapture(listener)`，但其设备配置为建议值，不保证选中原设备。若需精确恢复原摄像头，应在切换前保存 `getCurrentCameraId()`，失败后使用非空快照调用 `switchCameraDevice(previousId, listener)`；恢复本身失败时应提示画面中断，避免循环重试。
参数说明：
- `position`：`CameraCaptureOptions.CamraPosition`，目标摄像头位置：
  - `FRONT`：前置摄像头
  - `BACK`：后置摄像头
  - `External`：外接摄像头
- `listener`：`RTCResultListener?`，切换结果回调，可不传。本次请求被后一次请求取代或被 `stopCapture()` 取消时不回调任何结果。失败码含义见 [错误码](/zh/rtc/android/error-codes)。

返回值说明：无（`Unit`）。

### switchCameraDevice(cameraId, listener)
```kotlin
@JvmOverloads
fun switchCameraDevice(cameraId: String, listener: RTCResultListener? = null)
```
方法说明：按真实 Camera2 `cameraId` 精确切换摄像头。适用于设备存在多颗摄像头、需要指定具体某一颗（而非仅前/后置）的场景。`cameraId` 取自 [`RTCEngine.getCameraDevices`](/zh/rtc/android/api-reference/RTCEngine) 返回的 `CameraDeviceCapability.cameraId`。  
ID 是**指令**：只尝试这一颗设备，打不开即失败，不会换到别的设备。其余语义与 `switchCameraPosition` 一致——未在采集时可直接调用、以首帧为成功判据、**失败不自动回退**。成功后由 SDK 把实际生效的设备 ID 与其方向写回配置。  
参数说明：
- `cameraId`：`String`，目标摄像头的 Camera2 原生 ID。
- `listener`：`RTCResultListener?`，切换结果回调，可不传。本次请求被后一次请求取代或被 `stopCapture()` 取消时不回调任何结果。失败码含义见 [错误码](/zh/rtc/android/error-codes)。

返回值说明：无（`Unit`）。

### getCurrentCameraId()
```kotlin
fun getCurrentCameraId(): String
```
方法说明：查询实际生效的摄像头 ID，返回最后一次真正产出过首帧的设备 ID。用于覆盖应用无从推断的情况：`startCapture` 的建议设备失效后由 SDK 自动选中了另一颗，或 `switchCameraPosition` 在同方向内改选了另一颗，多摄选择界面可用它显示真实选中态。  
该值是历史记录，**不代表当前是否正在采集**：切换中、启动失败后、`stopCapture()` 之后都保留上一次的值，判断采集状态请依赖采集相关回调。  
参数说明：无。  
返回值说明：`String`，实际生效的 Camera2 设备 ID；尚未成功采集过或 SDK 已释放时返回空串。

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

> 前置镜像仅影响**本地预览渲染**，不改变编码发布到远端的画面；正常显示模式从下一帧采用新配置。启用控件的 `customDisplayCtrl(true)` 后，预览使用控件自身的旋转和翻转设置，不叠加轨道的默认前置镜像。

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

控件使用 `cn.seastart.rtc.media.original.render` 包中的 `VcsPlayerGlTextureView` / `VcsPlayerGlSurfaceView`；显示控制与生命周期见 [视频渲染](/zh/rtc/android/api-reference/RemoteVideoTrack)。

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
