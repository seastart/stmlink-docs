---
title: "LocalCameraTrack"
description: "API reference for Android LocalCameraTrack: camera capture, preset copy semantics, front/back and device-level camera switching with first-frame success criteria, mirroring, angle offset, flash control, and inherited rendering methods. Read when controlling the local camera."
---

## Description

`LocalCameraTrack` handles local camera capture, preview rendering, and camera control, and serves as the input track for `publishLocalVideo`.

Camera operations count as successful only when **the new video actually produces frames**, and results are reported asynchronously through `RTCResultListener`. If you start a new operation before the previous one has a result, the previous callback is silently dropped, and only the last operation reports a result.

## preOpt

```kotlin
var preOpt: PreOptionCamera
```
Property description: The current capture and publishing preset; see [Camera preset](/en/rtc/android/presets/camera).

- Both assignment and `getLocalCameraTrack(preOpt)` **copy `preOpt.capture`**, so modifying `capture` on the original object after getting the track has no effect; reassign `track.preOpt = opt` instead. Modifying `preOpt.publish` still takes effect.
- After a successful switch, the SDK writes back `capture.deviceId` and `capture.position` with the device actually in effect; you can read it together with `getCurrentCameraId()`.

## LocalCameraTrack methods

### startCapture(listener)
```kotlin
fun startCapture(listener: RTCResultListener?)
```
Description: Starts camera capture. Camera permission is required before calling. Starting succeeds only when the camera actually produces the first frame.  
`deviceId` and `position` in `capture` are both **suggestions** here: if the suggested device isn't available, the SDK tries devices in the same position first and then all available devices, rather than failing just because the suggestion is invalid. The automatically selected result isn't written back to the configuration; query it with `getCurrentCameraId()`.  
If capture is already running, this call returns success immediately, and **none of the new `capture` takes effect** (including resolution, frame rate, and device intent); to change parameters, call `stopCapture()` first and then start again.  
Parameters:
- `listener`: `RTCResultListener?`, the start result callback. Without permission, it calls back `onFail(RtcCameraErrorCode.CAMERA_PERMISSION_DENIED, "")` (`102231`); if all available devices have been tried and there's still no video, it calls back `onFail(RtcCameraErrorCode.CAMERA_FIRST_FRAME_TIMEOUT, "")` (`102239`). For failure codes, see [Error codes](/en/rtc/android/error-codes).

Returns: None (`Unit`).

### stopCapture()
```kotlin
fun stopCapture()
```
Description: Stops camera capture.  
Parameters: None.  
Returns: None (`Unit`).

### switchCameraPosition(position, listener)
```kotlin
@JvmOverloads
fun switchCameraPosition(
    position: CameraCaptureOptions.CamraPosition,
    listener: RTCResultListener? = null
)
```
Description: Switches the camera position. The position is a **command**: the SDK tries cameras only within that position—if the first one in the position can't be opened, it tries the next—but it never switches to another position. The switch succeeds only when the new camera actually produces the first frame; on success, the SDK writes the position back to the configuration and clears `deviceId`.  
You can call it directly when capture isn't running (the first time, after `stopCapture()`, or after a failed start) without calling `startCapture()` first; when capture is running, the current resolution and frame rate are kept.  
**On failure, it doesn't automatically fall back to the original camera.** If the target device or format validation fails, the original capture may be kept, so a failure callback doesn't necessarily mean the camera has stopped; if you need to close it, still call `stopCapture()`.

If your app only needs to restore a working video, it can call `startCapture(listener)`, but that call's device configuration is only a suggestion and doesn't guarantee the original device is selected. To restore the original camera exactly, save `getCurrentCameraId()` before switching, and after a failure call `switchCameraDevice(previousId, listener)` with the non-empty snapshot. If the restore itself fails, tell the user the video is interrupted instead of retrying in a loop.
Parameters:
- `position`: `CameraCaptureOptions.CamraPosition`, the target camera position:
  - `FRONT`: front camera
  - `BACK`: back camera
  - `External`: external camera
- `listener`: `RTCResultListener?`, the switch result callback; optional. If this request is superseded by a later request or canceled by `stopCapture()`, no result is called back. For failure codes, see [Error codes](/en/rtc/android/error-codes).

Returns: None (`Unit`).

### switchCameraDevice(cameraId, listener)
```kotlin
@JvmOverloads
fun switchCameraDevice(cameraId: String, listener: RTCResultListener? = null)
```
Description: Switches to a camera exactly by its real Camera2 `cameraId`. Use it when the device has multiple cameras and you need to pick a specific one (not just front/back). `cameraId` comes from `CameraDeviceCapability.cameraId` returned by [`RTCEngine.getCameraDevices`](/en/rtc/android/api-reference/RTCEngine).  
The ID is a **command**: only this device is tried; if it can't be opened, the call fails without switching to another device. Other semantics match `switchCameraPosition`—it can be called directly when capture isn't running, success is judged by the first frame, and **there's no automatic fallback on failure**. On success, the SDK writes the device ID actually in effect and its position back to the configuration.  
Parameters:
- `cameraId`: `String`, the native Camera2 ID of the target camera.
- `listener`: `RTCResultListener?`, the switch result callback; optional. If this request is superseded by a later request or canceled by `stopCapture()`, no result is called back. For failure codes, see [Error codes](/en/rtc/android/error-codes).

Returns: None (`Unit`).

### getCurrentCameraId()
```kotlin
fun getCurrentCameraId(): String
```
Description: Queries the camera ID actually in effect, returning the ID of the last device that actually produced a first frame. It covers cases your app can't infer: the device suggested to `startCapture` became invalid and the SDK automatically picked another one, or `switchCameraPosition` picked a different camera in the same position. A multi-camera selection UI can use it to show the actual selection.  
The value is a historical record and **doesn't indicate whether capture is currently running**: during a switch, after a failed start, and after `stopCapture()`, it keeps the previous value. To determine capture state, rely on the capture-related callbacks.  
Parameters: None.  
Returns: `String`, the Camera2 device ID actually in effect; an empty string if capture has never succeeded or the SDK has been released.

### openFrontCameraMirror()
```kotlin
fun openFrontCameraMirror()
```
Description: Turns on front camera mirroring (the default). Applies only to the front camera; other cameras keep their original behavior.  
Parameters: None.  
Returns: None (`Unit`).

### closeFrontCameraMirror()
```kotlin
fun closeFrontCameraMirror()
```
Description: Turns off front camera mirroring (that is, the local preview and front camera video keep their actual, non-mirrored orientation).  
Parameters: None.  
Returns: None (`Unit`).

### isFrontCameraMirrorOpen()
```kotlin
fun isFrontCameraMirrorOpen(): Boolean
```
Description: Queries whether front camera mirroring is currently on.  
Parameters: None.  
Returns: `Boolean`, `true` if mirroring is on, `false` if it's off.

> Front camera mirroring affects only **local preview rendering**; it doesn't change the video encoded and published to remote users. In normal display mode, the new setting applies from the next frame. After enabling `customDisplayCtrl(true)` on the view, the preview uses the view's own rotation and flip settings and doesn't stack the track's default front camera mirroring.

### setCameraAngleOffset(offset)
```kotlin
fun setCameraAngleOffset(offset: Int)
```
Description: Sets the camera angle offset, used for orientation correction on special devices. The SDK automatically normalizes it to `0/90/180/270`.  
Parameters:
- `offset`: `Int`, the angle offset; `0/90/180/270` recommended.
Returns: None (`Unit`).

### switchLight(open)
```kotlin
fun switchLight(open: Boolean)
```
Description: Toggles the camera flash.  
Parameters:
- `open`: `Boolean`, `true` turns the flash on, `false` turns it off.
Returns: None (`Unit`).

## Rendering methods inherited from VideoTrack

Views use `VcsPlayerGlTextureView` / `VcsPlayerGlSurfaceView` from the `cn.seastart.rtc.media.original.render` package; for display control and lifecycle, see [Video rendering](/en/rtc/android/api-reference/RemoteVideoTrack).

### addPlayView(view)
```kotlin
fun addPlayView(view: View): Boolean
```
Description: Adds a single render view. Only `VcsPlayerGlTextureView` / `VcsPlayerGlSurfaceView` are supported.  
Parameters:
- `view`: `View`, the render view.
Returns: `Boolean`, `true` if added successfully; `false` if the type isn't supported or the view was already added.

### replacePlayView(views)
```kotlin
fun replacePlayView(views: MutableList<View>)
```
Description: Replaces the entire list of render views.  
Parameters:
- `views`: `MutableList<View>`, the collection of render views; only `VcsPlayerGlTextureView` / `VcsPlayerGlSurfaceView` are supported.
Returns: None (`Unit`).

### removePlayView(view)
```kotlin
fun removePlayView(view: View)
```
Description: Removes the specified render view.  
Parameters:
- `view`: `View`, the target render view.
Returns: None (`Unit`).

### removeAllPlayView()
```kotlin
fun removeAllPlayView()
```
Description: Removes all render views.  
Parameters: None.  
Returns: None (`Unit`).
